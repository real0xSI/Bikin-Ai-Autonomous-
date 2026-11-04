
<!-- [ID:13_DATA_SCHEMA_S005] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: INT, :16 -->
# ==============================================================================
WAITING_PROMPT_EDIT_USERS: set[int] = set()

_INJECTION_PATTERNS = re.compile(
    r"(ignore\s+(all\s+)?(previous|prior)\s+instructions|system\s*prompt|"
    r"you\s+are\s+now\s+dan|jailbreak|drop\s+table|union\s+select|"
    r"<script\b|javascript:|__import__|os\.system|subprocess)",
    re.IGNORECASE,
)


def sanitize_and_deobfuscate_input(raw_text: str) -> tuple[str, bool]:
    """Membersihkan teks input dari karakter zero-width dan mendeteksi pola prompt/SQL injection."""
    if not raw_text:
        return "", False
    normalized = unicodedata.normalize("NFKC", raw_text)
    cleaned = "".join(
        ch for ch in normalized
        if unicodedata.category(ch) not in ("Cf", "Cc") or ch in ("\n", "\r", "\t")
    ).strip()
    if _INJECTION_PATTERNS.search(cleaned):
        return cleaned, True
    return cleaned, False


async def safe_reply_markdown(
    message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None
) -> Message:
    """Mengirim balasan dengan parse_mode Markdown dan fallback otomatis ke plain text jika ada karakter khusus."""
    try:
        return await message.reply(text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception:
        return await message.reply(text, parse_mode=None, reply_markup=reply_markup)


async def safe_edit_markdown(
    message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None
) -> None:
    """Menyunting pesan dengan parse_mode Markdown dan fallback otomatis ke plain text jika ada karakter khusus."""
    try:
        await message.edit_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception:
        try:
            await message.edit_text(text, parse_mode=None, reply_markup=reply_markup)
        except Exception:
            pass


async def increment_user_usage_counter(
    db: aiosqlite.Connection, user_id: int, is_render: bool = False
) -> None:
    """Menambah penghitung kuota harian chat_used_today atau free_img_used_today."""
    col = "free_img_used_today" if is_render else "chat_used_today"

    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(
            f"UPDATE users SET {col} = {col} + 1 WHERE internal_user_id = ?;",
            (user_id,),
        )

    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


def issue_stateless_ed25519_voucher(user_id: int, compute_units: int = 10, ttl_seconds: int = 86400) -> str:
    """Menerbitkan kode Stateless Ed25519 Compute Voucher (VCH-...) untuk portal eksternal."""
    now_ts = int(time.time())
    nonce = hashlib.sha256(f"{user_id}:{now_ts}:{os.urandom(8).hex()}".encode()).hexdigest()[:16]
    payload_dict = {
        "n": nonce,
        "u": int(user_id),
        "c": int(compute_units),
        "exp": now_ts + ttl_seconds,
    }
    payload_bytes = json.dumps(payload_dict, separators=(",", ":")).encode("utf-8")
    priv_key = Ed25519PrivateKey.from_private_bytes(ED25519_PRIV_BYTES)
    signature = priv_key.sign(payload_bytes)
    b64_payload = base64.urlsafe_b64encode(payload_bytes).decode("ascii").rstrip("=")
    b64_sig = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")
    return f"VCH-{b64_payload}.{b64_sig}"


async def verify_and_redeem_ed25519_voucher(db: aiosqlite.Connection, voucher_code: str) -> tuple[bool, str]:
    """Memverifikasi tanda tangan Ed25519 dan mencatat nullifier agar voucher tidak bisa dipakai ganda."""
    code = voucher_code.strip()
    if not code.startswith("VCH-") or "." not in code:
        return False, "Format kode voucher tidak valid."
    try:
        body = code[4:]
        b64_payload, b64_sig = body.split(".", 1)
        pad_p = "=" * (-len(b64_payload) % 4)
        pad_s = "=" * (-len(b64_sig) % 4)
        payload_bytes = base64.urlsafe_b64decode(b64_payload + pad_p)
        sig_bytes = base64.urlsafe_b64decode(b64_sig + pad_s)

        pub_key = Ed25519PublicKey.from_public_bytes(ED25519_PUB_BYTES)
        pub_key.verify(sig_bytes, payload_bytes)

        data = json.loads(payload_bytes.decode("utf-8"))
        exp = int(data.get("exp", 0))
        now_ts = int(time.time())
        if exp <= now_ts:
            return False, "Voucher sudah kedaluwarsa."

        nullifier_hash = hashlib.sha256(sig_bytes).hexdigest()

        async def _tx(conn: aiosqlite.Connection) -> bool:
            cur = await conn.execute(
                "SELECT 1 FROM redeemed_nullifiers WHERE nullifier_hash = ?;",
                (nullifier_hash,),
            )
            if await cur.fetchone():
                return False
            await conn.execute(
                "INSERT INTO redeemed_nullifiers (nullifier_hash, expires_at) VALUES (?, ?);",
                (nullifier_hash, exp),
            )
            return True

        ok = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
        if not ok:
            return False, "Voucher sudah pernah digunakan sebelumnya."
        return True, f"Voucher valid ({data.get('c', 10)} Compute Units)."
    except Exception as e:
        return False, f"Verifikasi kriptografi gagal: {e}"


async def handle_voucher_redeem_api(request: web.Request) -> web.Response:
    """Endpoint HTTP /api/voucher/redeem untuk memverifikasi Stateless Ed25519 Compute Voucher."""
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "message": "Invalid JSON"}, status=400)

    voucher_code = str(data.get("voucher") or "").strip()
    async with aiosqlite.connect(DB_PATH) as db:
        ok, msg = await verify_and_redeem_ed25519_voucher(db, voucher_code)
    return web.json_response({"ok": ok, "message": msg}, status=200 if ok else 400)


async def deduct_user_coins_for_job(
    db: aiosqlite.Connection,
    user_id: int,
    cost: int,
    allow_bonus: bool,
    prompt_text: str,
    engine_used: str,
) -> tuple[bool, str, str]:
    """Memotong koin pengguna secara atomik dengan Lock Striping dan mencatat job di tabel jobs."""
    job_id = f"JOB-{user_id}-{int(time.time() * 1000)}"
    if cost <= 0 or RUNTIME_CONFIG["HAPPY_HOUR_MODE"]:
        async def _free_tx(conn: aiosqlite.Connection) -> None:
            await conn.execute(
                """
                INSERT INTO jobs (job_id, internal_user_id, cost, deducted_bonus, deducted_utama, status, prompt_text, engine_used, created_at)
                VALUES (?, ?, 0, 0, 0, 'PROCESSING', ?, ?, ?);
                """,
                (job_id, user_id, prompt_text[:200], engine_used, int(time.time())),
            )
        await DB_WRITER_DAEMON.execute_write_tx(db, _free_tx)
        return True, job_id, "Happy Hour / 0 Koin"

    user_lock = get_user_lock(user_id)
    async with user_lock:
        async def _tx(conn: aiosqlite.Connection) -> tuple[bool, str]:
            cur = await conn.execute(
                "SELECT koin_utama, koin_bonus FROM users WHERE internal_user_id = ?;",
                (user_id,),
            )
            row = await cur.fetchone()
            if not row:
                return False, "Akun belum terdaftar. Ketik /start terlebih dahulu."
            utama, bonus = int(row[0]), int(row[1])

            if allow_bonus:
                if utama + bonus < cost:
                    return False, f"Saldo koin tidak cukup (Butuh {cost} Koin, Saldo: {utama} Utama + {bonus} Bonus)."
                use_bonus = min(bonus, cost)
                use_utama = cost - use_bonus
            else:
                if utama < cost:
                    return False, f"Mesin flagship ini memerlukan {cost} Koin Utama (Saldo Koin Utama Anda: {utama})."
                use_bonus = 0
                use_utama = cost

            await conn.execute(
                "UPDATE users SET koin_utama = koin_utama - ?, koin_bonus = koin_bonus - ? WHERE internal_user_id = ?;",
                (use_utama, use_bonus, user_id),
            )
            await conn.execute(
                """
                INSERT INTO jobs (job_id, internal_user_id, cost, deducted_bonus, deducted_utama, status, prompt_text, engine_used, created_at)
                VALUES (?, ?, ?, ?, ?, 'PROCESSING', ?, ?, ?);
                """,
                (job_id, user_id, cost, use_bonus, use_utama, prompt_text[:200], engine_used, int(time.time())),
            )
            return True, f"Terpotong {use_utama} Koin Utama & {use_bonus} Koin Bonus"

        ok, msg = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
        return ok, job_id, msg


async def mark_job_completed(
    db: aiosqlite.Connection, job_id: str, prompt_text: str, engine_name: str, media_url: str = "telegram_delivered"
) -> None:
    """Menandai job selesai dan menyimpan jejak ke syndicated_assets."""
    sig = hashlib.sha256(f"{engine_name}:{prompt_text.strip().lower()}".encode()).hexdigest()[:24]
    asset_id = f"AST-{sig[:10]}-{int(time.time())}"

    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("UPDATE jobs SET status = 'COMPLETED' WHERE job_id = ?;", (job_id,))
        await conn.execute(
            """
            INSERT OR REPLACE INTO syndicated_assets (asset_id, prompt_signature, engine_name, media_url, times_reused, created_at)
            VALUES (?, ?, ?, ?, 1, ?);
            """,
            (asset_id, sig, engine_name, media_url, int(time.time())),
        )

    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def refund_failed_job(db: aiosqlite.Connection, job_id: str) -> bool:
    """Mengembalikan 100% koin pengguna secara otomatis jika render gagal (Refund Sweeper)."""
    if not RUNTIME_CONFIG["SUBBOT_REFUND_SWEEPER_ACTIVE"]:
        return False

    async def _tx(conn: aiosqlite.Connection) -> bool:
        cur = await conn.execute(
            "SELECT internal_user_id, deducted_bonus, deducted_utama, refunded_lock FROM jobs WHERE job_id = ?;",
            (job_id,),
        )
        row = await cur.fetchone()
        if not row or int(row[3]) == 1:
            return False
        uid, d_bonus, d_utama = int(row[0]), int(row[1]), int(row[2])
        await conn.execute(
            """
            UPDATE users
            SET koin_utama = koin_utama + ?,
                koin_bonus = MIN(?, koin_bonus + ?)
            WHERE internal_user_id = ?;
            """,
            (d_utama, MAX_KOIN_BONUS_CAP, d_bonus, uid),
        )
        await conn.execute(
            "UPDATE jobs SET status = 'REFUNDED', refunded_lock = 1 WHERE job_id = ?;",
            (job_id,),
        )
        return True

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def _background_dead_job_sweeper_loop() -> None:
    """Daemon latar belakang yang menyapu job menggantung (>60 detik) dan mengembalikan koin otomatis."""
    while True:
        await asyncio.sleep(30)
        if not RUNTIME_CONFIG.get("SUBBOT_REFUND_SWEEPER_ACTIVE", True):
            continue
        try:
            cutoff_ts = int(time.time()) - 60
            async with aiosqlite.connect(DB_PATH) as db:
                cur = await db.execute(
                    "SELECT job_id, internal_user_id FROM jobs WHERE status = 'PROCESSING' AND refunded_lock = 0 AND created_at <= ?;",
                    (cutoff_ts,),
                )
                stale_jobs = await cur.fetchall()
                for j_id, u_id in stale_jobs:
                    refunded = await refund_failed_job(db, str(j_id))
                    if refunded and BOT_INSTANCE_GLOBAL:
                        try:
                            await BOT_INSTANCE_GLOBAL.send_message(
                                chat_id=int(u_id),
                                text=f"🛡️ **Auto-Refund Sweeper:** Tugas `{j_id}` melewati batas 60 detik. Koin Anda telah dikembalikan 100% secara otomatis!",
                                parse_mode="Markdown",
                            )
                        except Exception:
                            pass
        except Exception:
            pass


async def broadcast_to_bound_topic(bot: Bot, db: aiosqlite.Connection, binding_key: str, text: str) -> None:
    """Mengirim notifikasi otomatis ke topik grup yang telah diikat (misal: Live Neural Feed)."""
    if binding_key == "ACTIVITY_TOPIC" and not RUNTIME_CONFIG["SUBBOT_NEURAL_FEED_ACTIVE"]:
        return
    bound = await get_topic_binding(db, binding_key)
    if not bound:
        return
    chat_id, topic_id = bound
    try:
        kwargs: dict[str, Any] = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        if topic_id > 0:
            kwargs["message_thread_id"] = topic_id
        await bot.send_message(**kwargs)
    except Exception:
        pass



<!-- [ID:13_DATA_SCHEMA_S006] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# ==============================================================================
MAX_KOIN_BONUS_CAP = 25
PPP_EFFECTIVE_COIN_IDR = {1: 580, 2: 260, 3: 84}


async def init_master_db(db: aiosqlite.Connection) -> None:
    await db.execute("PRAGMA journal_mode = WAL;")
    await db.execute("PRAGMA synchronous = NORMAL;")
    await db.execute("PRAGMA busy_timeout = 10000;")
    await db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            internal_user_id INTEGER PRIMARY KEY,
            username TEXT DEFAULT 'Kreator',
            first_name TEXT DEFAULT '',
            language_code TEXT DEFAULT 'id',
            koin_utama INTEGER NOT NULL DEFAULT 0 CHECK (koin_utama >= 0),
            koin_bonus INTEGER NOT NULL DEFAULT 4 CHECK (koin_bonus >= 0 AND koin_bonus <= 25),
            has_topped_up INTEGER NOT NULL DEFAULT 0,
            ppp_zone INTEGER NOT NULL DEFAULT 3,
            last_claim_date TEXT,
            chat_used_today INTEGER NOT NULL DEFAULT 0,
            free_img_used_today INTEGER NOT NULL DEFAULT 0,
            quota_day_epoch INTEGER NOT NULL DEFAULT 0,
            personal_memory_notes TEXT DEFAULT '',
            active_canvas_content TEXT DEFAULT '',
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS identity_history (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            old_username TEXT,
            new_username TEXT,
            changed_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            internal_user_id INTEGER NOT NULL,
            cost INTEGER NOT NULL,
            deducted_bonus INTEGER NOT NULL DEFAULT 0,
            deducted_utama INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'PROCESSING',
            refunded_lock INTEGER NOT NULL DEFAULT 0,
            prompt_text TEXT DEFAULT '',
            engine_used TEXT DEFAULT '',
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS redeemed_nullifiers (
            nullifier_hash TEXT PRIMARY KEY,
            expires_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS treasury_summary (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            gross_revenue_idr INTEGER NOT NULL DEFAULT 0,
            working_capital_vault_idr INTEGER NOT NULL DEFAULT 0,
            harvestable_profit_vault_idr INTEGER NOT NULL DEFAULT 0,
            total_harvested_by_owner_idr INTEGER NOT NULL DEFAULT 0,
            total_jobs_completed INTEGER NOT NULL DEFAULT 0,
            updated_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS bot_bindings (
            binding_key TEXT PRIMARY KEY,
            chat_id INTEGER NOT NULL,
            topic_id INTEGER NOT NULL DEFAULT 0,
            topic_title TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS system_settings (
            setting_key TEXT PRIMARY KEY,
            setting_val TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS user_feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            feedback_text TEXT NOT NULL,
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS omni_resource_registry (
            resource_id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            resource_name TEXT NOT NULL,
            endpoint_url TEXT NOT NULL,
            secret_or_meta TEXT NOT NULL,
            is_live_verified INTEGER NOT NULL DEFAULT 0,
            expires_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS syndicated_assets (
            asset_id TEXT PRIMARY KEY,
            prompt_signature TEXT NOT NULL,
            engine_name TEXT NOT NULL,
            media_url TEXT NOT NULL,
            times_reused INTEGER NOT NULL DEFAULT 1,
            created_at INTEGER NOT NULL
        );
        """
    )
    await db.commit()

    # Muat kembali pengaturan persisten (seperti MINIAPP_URL & OWNER_ID) jika pernah disimpan
    cur = await db.execute("SELECT setting_key, setting_val FROM system_settings;")
    for k, v in await cur.fetchall():
        if k == "MINIAPP_URL" and v.startswith("https://"):
            RUNTIME_CONFIG["MINIAPP_URL"] = v
        elif k == "OWNER_ID_RUNTIME" and v.isdigit():
            RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = int(v)


async def save_persistent_setting(db: aiosqlite.Connection, key: str, val: str) -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(
            "INSERT OR REPLACE INTO system_settings (setting_key, setting_val) VALUES (?, ?);",
            (key, str(val)),
        )
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def set_topic_binding(
    db: aiosqlite.Connection, key: str, chat_id: int, topic_id: int, title: str = ""
) -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(
            "INSERT OR REPLACE INTO bot_bindings (binding_key, chat_id, topic_id, topic_title) VALUES (?, ?, ?, ?);",
            (key, chat_id, topic_id, title),
        )
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def get_topic_binding(db: aiosqlite.Connection, key: str) -> tuple[int, int] | None:
    cur = await db.execute("SELECT chat_id, topic_id FROM bot_bindings WHERE binding_key = ?;", (key,))
    row = await cur.fetchone()
    return (int(row[0]), int(row[1])) if row else None


async def get_all_topic_bindings(db: aiosqlite.Connection) -> dict[str, tuple[int, int, str]]:
    cur = await db.execute("SELECT binding_key, chat_id, topic_id, topic_title FROM bot_bindings;")
    rows = await cur.fetchall()
    return {r[0]: (int(r[1]), int(r[2]), str(r[3] or r[0])) for r in rows}



<!-- [ID:13_DATA_SCHEMA_S007] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# ==============================================================================
MAX_KOIN_BONUS_CAP = 25
PPP_EFFECTIVE_COIN_IDR = {1: 580, 2: 260, 3: 84}


async def init_master_db(db: aiosqlite.Connection) -> None:
    await db.execute("PRAGMA journal_mode = WAL;")
    await db.execute("PRAGMA synchronous = NORMAL;")
    await db.execute("PRAGMA busy_timeout = 10000;")
    await db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            internal_user_id INTEGER PRIMARY KEY,
            username TEXT DEFAULT 'Kreator',
            first_name TEXT DEFAULT '',
            language_code TEXT DEFAULT 'id',
            koin_utama INTEGER NOT NULL DEFAULT 0 CHECK (koin_utama >= 0),
            koin_bonus INTEGER NOT NULL DEFAULT 4 CHECK (koin_bonus >= 0 AND koin_bonus <= 25),
            has_topped_up INTEGER NOT NULL DEFAULT 0,
            ppp_zone INTEGER NOT NULL DEFAULT 3,
            last_claim_date TEXT,
            chat_used_today INTEGER NOT NULL DEFAULT 0,
            free_img_used_today INTEGER NOT NULL DEFAULT 0,
            quota_day_epoch INTEGER NOT NULL DEFAULT 0,
            personal_memory_notes TEXT DEFAULT '',
            active_canvas_content TEXT DEFAULT '',
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS identity_history (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            old_username TEXT,
            new_username TEXT,
            changed_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            internal_user_id INTEGER NOT NULL,
            cost INTEGER NOT NULL,
            deducted_bonus INTEGER NOT NULL DEFAULT 0,
            deducted_utama INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'PROCESSING',
            refunded_lock INTEGER NOT NULL DEFAULT 0,
            prompt_text TEXT DEFAULT '',
            engine_used TEXT DEFAULT '',
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS redeemed_nullifiers (
            nullifier_hash TEXT PRIMARY KEY,
            expires_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS treasury_summary (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            gross_revenue_idr INTEGER NOT NULL DEFAULT 0,
            working_capital_vault_idr INTEGER NOT NULL DEFAULT 0,
            harvestable_profit_vault_idr INTEGER NOT NULL DEFAULT 0,
            total_harvested_by_owner_idr INTEGER NOT NULL DEFAULT 0,
            total_jobs_completed INTEGER NOT NULL DEFAULT 0,
            updated_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS bot_bindings (
            binding_key TEXT PRIMARY KEY,
            chat_id INTEGER NOT NULL,
            topic_id INTEGER NOT NULL DEFAULT 0,
            topic_title TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS system_settings (
            setting_key TEXT PRIMARY KEY,
            setting_val TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS user_feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            feedback_text TEXT NOT NULL,
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS omni_resource_registry (
            resource_id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            resource_name TEXT NOT NULL,
            endpoint_url TEXT NOT NULL,
            secret_or_meta TEXT NOT NULL,
            is_live_verified INTEGER NOT NULL DEFAULT 0,
            expires_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS syndicated_assets (
            asset_id TEXT PRIMARY KEY,
            prompt_signature TEXT NOT NULL,
            engine_name TEXT NOT NULL,
            media_url TEXT NOT NULL,
            times_reused INTEGER NOT NULL DEFAULT 1,
            created_at INTEGER NOT NULL
        );
        """
    )
    await db.commit()

    # Muat kembali pengaturan persisten (seperti MINIAPP_URL & OWNER_ID) jika pernah disimpan
    cur = await db.execute("SELECT setting_key, setting_val FROM system_settings;")
    for k, v in await cur.fetchall():
        if k == "MINIAPP_URL" and v.startswith("https://"):
            RUNTIME_CONFIG["MINIAPP_URL"] = v
        elif k == "OWNER_ID_RUNTIME" and v.isdigit():
            RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = int(v)
        elif k == "PILIHAN_MESIN_MEDIA" and v.isdigit():
            RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] = int(v)
        elif k in ("LAUNCH_PRODUCTION_MODE", "HAPPY_HOUR_MODE"):
            RUNTIME_CONFIG[k] = (v == "1")
        elif k in ("ID_ACTIVE_CATEGORY", "ID_ACTIVE_PROVIDER", "GLOBAL_ACTIVE_PROVIDER"):
            RUNTIME_CONFIG[k] = v


async def save_persistent_setting(db: aiosqlite.Connection, key: str, val: str) -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(
            "INSERT OR REPLACE INTO system_settings (setting_key, setting_val) VALUES (?, ?);",
            (key, str(val)),
        )
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def set_topic_binding(
    db: aiosqlite.Connection, key: str, chat_id: int, topic_id: int, title: str = ""
) -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(
            "INSERT OR REPLACE INTO bot_bindings (binding_key, chat_id, topic_id, topic_title) VALUES (?, ?, ?, ?);",
            (key, chat_id, topic_id, title),
        )
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def get_topic_binding(db: aiosqlite.Connection, key: str) -> tuple[int, int] | None:
    cur = await db.execute("SELECT chat_id, topic_id FROM bot_bindings WHERE binding_key = ?;", (key,))
    row = await cur.fetchone()
    return (int(row[0]), int(row[1])) if row else None


async def get_all_topic_bindings(db: aiosqlite.Connection) -> dict[str, tuple[int, int, str]]:
    cur = await db.execute("SELECT binding_key, chat_id, topic_id, topic_title FROM bot_bindings;")
    rows = await cur.fetchall()
    return {r[0]: (int(r[1]), int(r[2]), str(r[3] or r[0])) for r in rows}



<!-- [ID:13_DATA_SCHEMA_S008] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
## Halaman 446

           log_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, old_username TEXT, new_usernam
       );
       CREATE TABLE IF NOT EXISTS jobs (
           job_id TEXT PRIMARY KEY, internal_user_id INTEGER NOT NULL, cost INTEGER NOT NULL, deducted_bonus 
       );
       CREATE TABLE IF NOT EXISTS payment_invoices (
           invoice_id TEXT PRIMARY KEY, user_id INTEGER NOT NULL, amount_idr INTEGER NOT NULL, coins_credited
       );
       CREATE TABLE IF NOT EXISTS redeemed_nullifiers (nullifier_hash TEXT PRIMARY KEY, expires_at INTEGER NO
       CREATE TABLE IF NOT EXISTS treasury_summary (
           id INTEGER PRIMARY KEY CHECK (id = 1), gross_revenue_idr INTEGER NOT NULL DEFAULT 0, working_capit
       );
       CREATE TABLE IF NOT EXISTS bot_bindings (binding_key TEXT PRIMARY KEY, chat_id INTEGER NOT NULL, topic
       CREATE TABLE IF NOT EXISTS system_settings (setting_key TEXT PRIMARY KEY, setting_val TEXT NOT NULL);
       CREATE TABLE IF NOT EXISTS user_feedback (feedback_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEG
       CREATE TABLE IF NOT EXISTS omni_resource_registry (resource_id TEXT PRIMARY KEY, category TEXT NOT NUL
       CREATE TABLE IF NOT EXISTS syndicated_assets (asset_id TEXT PRIMARY KEY, prompt_signature TEXT NOT NUL
       CREATE TABLE IF NOT EXISTS pending_human_approvals (approval_id TEXT PRIMARY KEY, action_type TEXT NOT
       CREATE TABLE IF NOT EXISTS human_escalation_queue (incident_id TEXT PRIMARY KEY, component TEXT NOT NU
       CREATE TABLE IF NOT EXISTS geo_community_clusters (country_lang_code TEXT PRIMARY KEY, user_count INTE
   """)
   await db.commit()
async def save_persistent_setting(db: aiosqlite.Connection, key: str, val: str) -> None:
   async def _tx(conn: aiosqlite.Connection) -> None:
       await conn.execute("INSERT OR REPLACE INTO system_settings (setting_key, setting_val) VALUES (?, ?);",
   await DB_WRITER_DAEMON.execute_write_tx(db, _tx)

<!-- [ID:13_DATA_SCHEMA_S009] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: :80, :400, :200 -->
# 10. HELPER TRANSAKSI KOIN, AUTO-REFUND SWEEPER & BROADCAST TOPIK
async def safe_reply_markdown(message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None) -> Message:
    try:
        return await message.reply(text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception:
        return await message.reply(text, parse_mode=None, reply_markup=reply_markup)


async def safe_edit_markdown(message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None) -> None:
    try:
        await message.edit_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception:
        try:
            await message.edit_text(text, parse_mode=None, reply_markup=reply_markup)
        except Exception:
            pass


async def increment_user_usage_counter(db: aiosqlite.Connection, user_id: int, is_render: bool = False) -> None:
    col = "free_img_used_today" if is_render else "chat_used_today"
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(f"UPDATE users SET {col} = {col} + 1 WHERE internal_user_id = ?;", (user_id,))
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def update_personal_memory_if_needed(db: aiosqlite.Connection, user_id: int, text: str, current_mem: str) -> str:
    low = text.lower()
    new_fact = text[:80] if any(k in low for k in ("nama saya ", "panggil saya ", "usaha saya ", "jualan ", "bisnis saya ")) else ""
    if new_fact and new_fact not in current_mem:
        updated = (f"{current_mem} | {new_fact}").strip(" |")[:400]
        async def _upd(conn: aiosqlite.Connection) -> None:
            await conn.execute("UPDATE users SET personal_memory_notes = ? WHERE internal_user_id = ?;", (updated, user_id))
        await DB_WRITER_DAEMON.execute_write_tx(db, _upd)
        return updated
    return current_mem


async def deduct_user_coins_for_job(db: aiosqlite.Connection, user_id: int, cost: int, allow_bonus: bool, prompt_text: str, engine_used: str) -> tuple[bool, str, str]:
    job_id = f"JOB-{user_id}-{int(time.time() * 1000)}"
    if cost <= 0 or RUNTIME_CONFIG["HAPPY_HOUR_MODE"]:
        async def _free_tx(conn: aiosqlite.Connection) -> None:
            await conn.execute("INSERT INTO jobs (job_id, internal_user_id, cost, deducted_bonus, deducted_utama, status, prompt_text, engine_used, created_at) VALUES (?, ?, 0, 0, 0, 'PROCESSING', ?, ?, ?);", (job_id, user_id, prompt_text[:200], engine_used, int(time.time())))
        await DB_WRITER_DAEMON.execute_write_tx(db, _free_tx)
        return True, job_id, "Promo Happy Hour (0 Koin)"

    async with get_user_lock(user_id):
        async def _tx(conn: aiosqlite.Connection) -> tuple[bool, str]:
            cur = await conn.execute("SELECT koin_utama, koin_bonus FROM users WHERE internal_user_id = ?;", (user_id,))
            row = await cur.fetchone()
            if not row:
                return False, "Ketik /start terlebih dahulu."
            utama, bonus = int(row[0]), int(row[1])
            if allow_bonus:
                if utama + bonus < cost:
                    return False, f"Saldo koin belum cukup (Butuh {cost} Koin, Saldo: {utama} Utama + {bonus} Bonus)."
                use_bonus = min(bonus, cost)
                use_utama = cost - use_bonus
            else:
                if utama < cost:
                    return False, f"Memerlukan {cost} Koin Utama (Saldo: {utama})."
                use_bonus, use_utama = 0, cost
            await conn.execute("UPDATE users SET koin_utama = koin_utama - ?, koin_bonus = koin_bonus - ? WHERE internal_user_id = ?;", (use_utama, use_bonus, user_id))
            await conn.execute("INSERT INTO jobs (job_id, internal_user_id, cost, deducted_bonus, deducted_utama, status, prompt_text, engine_used, created_at) VALUES (?, ?, ?, ?, ?, 'PROCESSING', ?, ?, ?);", (job_id, user_id, cost, use_bonus, use_utama, prompt_text[:200], engine_used, int(time.time())))
            return True, f"Terpakai {use_utama} Koin Utama & {use_bonus} Koin Bonus"

        ok, msg = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
        return ok, job_id, msg


async def mark_job_completed(db: aiosqlite.Connection, job_id: str, prompt_text: str, engine_name: str, media_url: str = "telegram_delivered") -> None:
    sig = hashlib.sha256(f"{engine_name}:{prompt_text.strip().lower()}".encode()).hexdigest()[:24]
    asset_id = f"AST-{sig[:10]}-{int(time.time())}"
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("UPDATE jobs SET status = 'COMPLETED' WHERE job_id = ?;", (job_id,))
        await conn.execute("INSERT OR REPLACE INTO syndicated_assets (asset_id, prompt_signature, engine_name, media_url, times_reused, created_at) VALUES (?, ?, ?, ?, 1, ?);", (asset_id, sig, engine_name, media_url, int(time.time())))
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def refund_failed_job(db: aiosqlite.Connection, job_id: str) -> bool:
    if not RUNTIME_CONFIG["SUBBOT_REFUND_SWEEPER_ACTIVE"]:
        return False
    async def _tx(conn: aiosqlite.Connection) -> bool:
        cur = await conn.execute("SELECT internal_user_id, deducted_bonus, deducted_utama, refunded_lock FROM jobs WHERE job_id = ?;", (job_id,))
        row = await cur.fetchone()
        if not row or int(row[3]) == 1:
            return False
        uid, d_bonus, d_utama = int(row[0]), int(row[1]), int(row[2])
        await conn.execute("UPDATE users SET koin_utama = koin_utama + ?, koin_bonus = MIN(?, koin_bonus + ?) WHERE internal_user_id = ?;", (d_utama, MAX_KOIN_BONUS_CAP, d_bonus, uid))
        await conn.execute("UPDATE jobs SET status = 'REFUNDED', refunded_lock = 1 WHERE job_id = ?;", (job_id,))
        return True
    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def _background_dead_job_sweeper_loop() -> None:
    while True:
        await asyncio.sleep(30)
        if not RUNTIME_CONFIG.get("SUBBOT_REFUND_SWEEPER_ACTIVE", True):
            continue
        try:
            cutoff_ts = int(time.time()) - 60
            async with get_db() as db:
                cur = await db.execute("SELECT job_id, internal_user_id FROM jobs WHERE status = 'PROCESSING' AND refunded_lock = 0 AND created_at <= ?;", (cutoff_ts,))
                for j_id, u_id in await cur.fetchall():
                    if await refund_failed_job(db, str(j_id)) and BOT_INSTANCE_GLOBAL:
                        try:
                            await BOT_INSTANCE_GLOBAL.send_message(chat_id=int(u_id), text=f"🛡️ **Garansi Koin Kembali 100% (Auto-Refund):** Pesanan `{j_id}` melewati batas 60 detik. Koin Anda telah dikembalikan utuh!", parse_mode="Markdown")
                        except Exception:
                            pass
        except Exception:
            pass


async def broadcast_to_bound_topic(bot: Bot, db: aiosqlite.Connection, binding_key: str, text: str) -> None:
    if binding_key == "ACTIVITY_TOPIC" and not RUNTIME_CONFIG["SUBBOT_NEURAL_FEED_ACTIVE"]:
        return
    bound = await get_topic_binding(db, binding_key)
    if not bound:
        return
    chat_id, topic_id = bound
    try:
        kwargs: dict[str, Any] = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        if topic_id > 0:
            kwargs["message_thread_id"] = topic_id
        await bot.send_message(**kwargs)
    except Exception:
        pass



<!-- [ID:13_DATA_SCHEMA_S010] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: :80, :400, :200 -->
# 10. HELPER TRANSAKSI KOIN, AUTO-REFUND SWEEPER & BROADCAST TOPIK
async def safe_reply_markdown(message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None) -> Message:
    try:
        return await message.reply(text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception:
        return await message.reply(text, parse_mode=None, reply_markup=reply_markup)


async def safe_edit_markdown(message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None) -> None:
    try:
        await message.edit_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception:
        try:
            await message.edit_text(text, parse_mode=None, reply_markup=reply_markup)
        except Exception:
            pass


async def increment_user_usage_counter(db: aiosqlite.Connection, user_id: int, is_render: bool = False) -> None:
    col = "free_img_used_today" if is_render else "chat_used_today"
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(f"UPDATE users SET {col} = {col} + 1 WHERE internal_user_id = ?;", (user_id,))
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def update_personal_memory_if_needed(db: aiosqlite.Connection, user_id: int, text: str, current_mem: str) -> str:
    low = text.lower()
    new_fact = text[:80] if any(k in low for k in ("nama saya ", "panggil saya ", "usaha saya ", "jualan ", "bisnis saya ")) else ""
    if new_fact and new_fact not in current_mem:
        updated = (f"{current_mem} | {new_fact}").strip(" |")[:400]
        async def _upd(conn: aiosqlite.Connection) -> None:
            await conn.execute("UPDATE users SET personal_memory_notes = ? WHERE internal_user_id = ?;", (updated, user_id))
        await DB_WRITER_DAEMON.execute_write_tx(db, _upd)
        return updated
    return current_mem


async def deduct_user_coins_for_job(db: aiosqlite.Connection, user_id: int, cost: int, allow_bonus: bool, prompt_text: str, engine_used: str) -> tuple[bool, str, str]:
    job_id = f"JOB-{user_id}-{int(time.time() * 1000)}"
    if cost <= 0 or RUNTIME_CONFIG["HAPPY_HOUR_MODE"]:
        async def _free_tx(conn: aiosqlite.Connection) -> None:
            await conn.execute("INSERT INTO jobs (job_id, internal_user_id, cost, deducted_bonus, deducted_utama, status, prompt_text, engine_used, created_at) VALUES (?, ?, 0, 0, 0, 'PROCESSING', ?, ?, ?);", (job_id, user_id, prompt_text[:200], engine_used, int(time.time())))
        await DB_WRITER_DAEMON.execute_write_tx(db, _free_tx)
        return True, job_id, "Promo Happy Hour (0 Koin)"

    async with get_user_lock(user_id):
        async def _tx(conn: aiosqlite.Connection) -> tuple[bool, str]:
            cur = await conn.execute("SELECT koin_utama, koin_bonus FROM users WHERE internal_user_id = ?;", (user_id,))
            row = await cur.fetchone()
            if not row:
                return False, "Akun belum terdaftar. Ketik /start terlebih dahulu."
            utama, bonus = int(row[0]), int(row[1])
            if allow_bonus:
                if utama + bonus < cost:
                    return False, f"Saldo koin belum cukup (Butuh {cost} Koin, Saldo: {utama} Utama + {bonus} Bonus)."
                use_bonus = min(bonus, cost)
                use_utama = cost - use_bonus
            else:
                if utama < cost:
                    return False, f"Fitur Pro ini memerlukan {cost} Koin Utama (Saldo Koin Utama Anda: {utama})."
                use_bonus, use_utama = 0, cost
            await conn.execute("UPDATE users SET koin_utama = koin_utama - ?, koin_bonus = koin_bonus - ? WHERE internal_user_id = ?;", (use_utama, use_bonus, user_id))
            await conn.execute("INSERT INTO jobs (job_id, internal_user_id, cost, deducted_bonus, deducted_utama, status, prompt_text, engine_used, created_at) VALUES (?, ?, ?, ?, ?, 'PROCESSING', ?, ?, ?);", (job_id, user_id, cost, use_bonus, use_utama, prompt_text[:200], engine_used, int(time.time())))
            return True, f"Terpakai {use_utama} Koin Utama & {use_bonus} Koin Bonus"

        ok, msg = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
        return ok, job_id, msg


async def mark_job_completed(db: aiosqlite.Connection, job_id: str, prompt_text: str, engine_name: str, media_url: str = "telegram_delivered") -> None:
    sig = hashlib.sha256(f"{engine_name}:{prompt_text.strip().lower()}".encode()).hexdigest()[:24]
    asset_id = f"AST-{sig[:10]}-{int(time.time())}"
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("UPDATE jobs SET status = 'COMPLETED' WHERE job_id = ?;", (job_id,))
        await conn.execute("INSERT OR REPLACE INTO syndicated_assets (asset_id, prompt_signature, engine_name, media_url, times_reused, created_at) VALUES (?, ?, ?, ?, 1, ?);", (asset_id, sig, engine_name, media_url, int(time.time())))
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def refund_failed_job(db: aiosqlite.Connection, job_id: str) -> bool:
    if not RUNTIME_CONFIG["SUBBOT_REFUND_SWEEPER_ACTIVE"]:
        return False
    async def _tx(conn: aiosqlite.Connection) -> bool:
        cur = await conn.execute("SELECT internal_user_id, deducted_bonus, deducted_utama, refunded_lock FROM jobs WHERE job_id = ?;", (job_id,))
        row = await cur.fetchone()
        if not row or int(row[3]) == 1:
            return False
        uid, d_bonus, d_utama = int(row[0]), int(row[1]), int(row[2])
        await conn.execute("UPDATE users SET koin_utama = koin_utama + ?, koin_bonus = MIN(?, koin_bonus + ?) WHERE internal_user_id = ?;", (d_utama, MAX_KOIN_BONUS_CAP, d_bonus, uid))
        await conn.execute("UPDATE jobs SET status = 'REFUNDED', refunded_lock = 1 WHERE job_id = ?;", (job_id,))
        return True
    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def _background_dead_job_sweeper_loop() -> None:
    while True:
        await asyncio.sleep(30)
        if not RUNTIME_CONFIG.get("SUBBOT_REFUND_SWEEPER_ACTIVE", True):
            continue
        try:
            cutoff_ts = int(time.time()) - 60
            async with get_db() as db:
                cur = await db.execute("SELECT job_id, internal_user_id FROM jobs WHERE status = 'PROCESSING' AND refunded_lock = 0 AND created_at <= ?;", (cutoff_ts,))
                for j_id, u_id in await cur.fetchall():
                    if await refund_failed_job(db, str(j_id)) and BOT_INSTANCE_GLOBAL:
                        try:
                            await BOT_INSTANCE_GLOBAL.send_message(chat_id=int(u_id), text=f"🛡️ **Garansi Koin Kembali 100% (Auto-Refund):** Pesanan `{j_id}` melewati batas 60 detik. Koin Anda telah dikembalikan utuh ke saldo Anda!", parse_mode="Markdown")
                        except Exception:
                            pass
        except Exception:
            pass


async def broadcast_to_bound_topic(bot: Bot, db: aiosqlite.Connection, binding_key: str, text: str) -> None:
    if binding_key == "ACTIVITY_TOPIC" and not RUNTIME_CONFIG["SUBBOT_NEURAL_FEED_ACTIVE"]:
        return
    bound = await get_topic_binding(db, binding_key)
    if not bound:
        return
    chat_id, topic_id = bound
    try:
        kwargs: dict[str, Any] = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        if topic_id > 0:
            kwargs["message_thread_id"] = topic_id
        await bot.send_message(**kwargs)
    except Exception:
        pass


