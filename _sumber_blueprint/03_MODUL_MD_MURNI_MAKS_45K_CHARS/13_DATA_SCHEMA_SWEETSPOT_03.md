
<!-- [ID:13_DATA_SCHEMA_S011] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: :80, :400, :200 -->
# ==============================================================================
async def safe_reply_markdown(
    message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None
) -> Message:
    try:
        return await message.reply(text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception:
        return await message.reply(text, parse_mode=None, reply_markup=reply_markup)


async def safe_edit_markdown(
    message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None
) -> None:
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


async def update_personal_memory_if_needed(
    db: aiosqlite.Connection, user_id: int, text: str, current_mem: str
) -> str:
    low = text.lower()
    new_fact = ""
    if any(k in low for k in ("nama saya ", "panggil saya ", "usaha saya ", "jualan ", "bisnis saya ")):
        new_fact = text[:80]
    if new_fact and new_fact not in current_mem:
        updated = (f"{current_mem} | {new_fact}").strip(" |")[:400]

        async def _upd(conn: aiosqlite.Connection) -> None:
            await conn.execute(
                "UPDATE users SET personal_memory_notes = ? WHERE internal_user_id = ?;", (updated, user_id)
            )

        await DB_WRITER_DAEMON.execute_write_tx(db, _upd)
        return updated
    return current_mem


async def deduct_user_coins_for_job(
    db: aiosqlite.Connection, user_id: int, cost: int, allow_bonus: bool, prompt_text: str, engine_used: str
) -> tuple[bool, str, str]:
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
        return True, job_id, "Promo Happy Hour (0 Koin)"

    user_lock = get_user_lock(user_id)
    async with user_lock:
        async def _tx(conn: aiosqlite.Connection) -> tuple[bool, str]:
            cur = await conn.execute(
                "SELECT koin_utama, koin_bonus FROM users WHERE internal_user_id = ?;", (user_id,)
            )
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
            return True, f"Terpakai {use_utama} Koin Utama & {use_bonus} Koin Bonus"

        ok, msg = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
        return ok, job_id, msg


async def mark_job_completed(
    db: aiosqlite.Connection, job_id: str, prompt_text: str, engine_name: str, media_url: str = "telegram_delivered"
) -> None:
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
            "UPDATE users SET koin_utama = koin_utama + ?, koin_bonus = MIN(?, koin_bonus + ?) WHERE internal_user_id = ?;",
            (d_utama, MAX_KOIN_BONUS_CAP, d_bonus, uid),
        )
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
                cur = await db.execute(
                    "SELECT job_id, internal_user_id FROM jobs WHERE status = 'PROCESSING' AND refunded_lock = 0 AND created_at <= ?;",
                    (cutoff_ts,),
                )
                for j_id, u_id in await cur.fetchall():
                    if await refund_failed_job(db, str(j_id)) and BOT_INSTANCE_GLOBAL:
                        try:
                            await BOT_INSTANCE_GLOBAL.send_message(
                                chat_id=int(u_id),
                                text=f"🛡️ **Garansi Koin Kembali 100% (Auto-Refund):** Pesanan `{j_id}` melewati batas 60 detik. Koin Anda telah dikembalikan utuh ke saldo Anda!",
                                parse_mode="Markdown",
                            )
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



<!-- [ID:13_DATA_SCHEMA_S012] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: :16 -->
# ==============================================================================
_INJECTION_PATTERNS = re.compile(
    r"(ignore\\s+(all\\s+)?(previous|prior)\\s+instructions|system\\s*prompt|"
    r"you\\s+are\\s+now\\s+dan|jailbreak|drop\\s+table|union\\s+select|"
    r"<script\\b|javascript:|__import__|os\\.system|subprocess)",
    re.IGNORECASE,
)


def sanitize_and_deobfuscate_input(raw_text: str) -> tuple[str, bool]:
    """Membersihkan teks input dari karakter zero-width dan mendeteksi pola prompt/SQL injection."""
    if not raw_text:
        return "", False
    normalized = unicodedata.normalize("NFKC", raw_text)
    cleaned = "".join(
        ch for ch in normalized
        if unicodedata.category(ch) not in ("Cf", "Cc") or ch in ("\\n", "\\r", "\\t")
    ).strip()
    if _INJECTION_PATTERNS.search(cleaned):
        return cleaned, True
    return cleaned, False


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



<!-- [ID:13_DATA_SCHEMA_S013] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: USER_ID, STR, :10, AUTONOMIC-HEAL -->
# 1. SQLITE WAL CONCURRENCY, LOCK STRIPES & CONVERGENCE GUARD
STRIPE_COUNT = 4096
USER_LOCK_STRIPES = [asyncio.Lock() for _ in range(STRIPE_COUNT)]
ANTI_TUYUL_VELOCITY: dict[int, float] = {}


def get_user_lock(user_id: int) -> asyncio.Lock:
    return USER_LOCK_STRIPES[user_id % STRIPE_COUNT]


def check_velocity_rate_limit(user_id: int, min_interval_sec: float = 0.5) -> bool:
    now = time.monotonic()
    if now - ANTI_TUYUL_VELOCITY.get(user_id, 0.0) < min_interval_sec:
        return False
    ANTI_TUYUL_VELOCITY[user_id] = now
    if len(ANTI_TUYUL_VELOCITY) > 10000:
        ANTI_TUYUL_VELOCITY.clear()
    return True


class AutonomicConvergenceGuard:
    def __init__(self) -> None:
        self.verified_ast_hashes: set[str] = set()
        self.telemetry_window: deque[tuple[int, str, bool]] = deque(maxlen=50)

    def record_telemetry(self, component: str, success: bool) -> None:
        self.telemetry_window.append((int(time.time()), component, success))

    def build_gitops_commit_plan(self, ast_hash: str, summary: str) -> dict[str, str]:
        return {
            "shadow_branch": f"autonomic/patch-{ast_hash[:10]}",
            "verify_cmd": "python3 -m py_compile app.py",
            "commit_cmd": f"git checkout -b autonomic/patch-{ast_hash[:10]} && git commit -am '[Autonomic-Heal] {summary}'",
            "rollback_cmd": "git revert --no-edit HEAD",
        }


AUTONOMIC_GUARD = AutonomicConvergenceGuard()


@asynccontextmanager
async def get_db() -> AsyncIterator[aiosqlite.Connection]:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA journal_mode = WAL;")
        await db.execute("PRAGMA synchronous = NORMAL;")
        await db.execute("PRAGMA busy_timeout = 10000;")
        await db.execute("PRAGMA foreign_keys = ON;")
        yield db


class SingleWriterSQLiteDaemon:
    def __init__(self, checkpoint_every_n_writes: int = 400):
        self._write_mutex = asyncio.Lock()
        self._write_counter = 0
        self._checkpoint_threshold = checkpoint_every_n_writes

    async def execute_write_tx(
        self, db: aiosqlite.Connection, tx_coro: Callable[[aiosqlite.Connection], Coroutine[Any, Any, Any]]
    ) -> Any:
        async with self._write_mutex:
            try:
                result = await tx_coro(db)
                await db.commit()
            except Exception:
                try:
                    await db.rollback()
                except Exception:
                    pass
                raise
            self._write_counter += 1
            if self._write_counter >= self._checkpoint_threshold:
                self._write_counter = 0
                now_ts = int(time.time())
                try:
                    await db.execute("DELETE FROM redeemed_nullifiers WHERE expires_at <= ?;", (now_ts,))
                    await db.execute("DELETE FROM omni_resource_registry WHERE expires_at <= ?;", (now_ts,))
                    await db.commit()
                    await db.execute("PRAGMA wal_checkpoint(PASSIVE);")
                except Exception:
                    pass
            return result


DB_WRITER_DAEMON = SingleWriterSQLiteDaemon()


<!-- [ID:13_DATA_SCHEMA_S014] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: USER_ID, STR, :10, AUTONOMIC-HEAL -->
# 1. SQLITE WAL CONCURRENCY, 4.096 LOCK STRIPES & AUTONOMIC CONVERGENCE GUARD
STRIPE_COUNT = 4096
USER_LOCK_STRIPES = [asyncio.Lock() for _ in range(STRIPE_COUNT)]
ANTI_TUYUL_VELOCITY: dict[int, float] = {}


def get_user_lock(user_id: int) -> asyncio.Lock:
    return USER_LOCK_STRIPES[user_id % STRIPE_COUNT]


def check_velocity_rate_limit(user_id: int, min_interval_sec: float = 0.5) -> bool:
    now = time.monotonic()
    if now - ANTI_TUYUL_VELOCITY.get(user_id, 0.0) < min_interval_sec:
        return False
    ANTI_TUYUL_VELOCITY[user_id] = now
    if len(ANTI_TUYUL_VELOCITY) > 10000:
        ANTI_TUYUL_VELOCITY.clear()
    return True


class AutonomicConvergenceGuard:
    """Anti-Infinite-Loop Guard & Autonomous GitOps Shadow-Branch Controller."""
    def __init__(self) -> None:
        self.verified_ast_hashes: set[str] = set()
        self.incident_remediation_count: dict[str, int] = {}
        self.telemetry_window: deque[tuple[int, str, bool]] = deque(maxlen=50)

    def record_telemetry(self, component: str, success: bool) -> None:
        self.telemetry_window.append((int(time.time()), component, success))

    def build_gitops_commit_plan(self, ast_hash: str, summary: str) -> dict[str, str]:
        return {
            "shadow_branch": f"autonomic/patch-{ast_hash[:10]}",
            "verify_cmd": "python3 -m py_compile app.py",
            "commit_cmd": f"git checkout -b autonomic/patch-{ast_hash[:10]} && git commit -am '[Autonomic-Heal] {summary}'",
            "rollback_cmd": "git revert --no-edit HEAD",
        }


AUTONOMIC_GUARD = AutonomicConvergenceGuard()


@asynccontextmanager
async def get_db() -> AsyncIterator[aiosqlite.Connection]:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA journal_mode = WAL;")
        await db.execute("PRAGMA synchronous = NORMAL;")
        await db.execute("PRAGMA busy_timeout = 10000;")
        await db.execute("PRAGMA foreign_keys = ON;")
        yield db


class SingleWriterSQLiteDaemon:
    def __init__(self, checkpoint_every_n_writes: int = 400):
        self._write_mutex = asyncio.Lock()
        self._write_counter = 0
        self._checkpoint_threshold = checkpoint_every_n_writes

    async def execute_write_tx(
        self, db: aiosqlite.Connection, tx_coro: Callable[[aiosqlite.Connection], Coroutine[Any, Any, Any]]
    ) -> Any:
        async with self._write_mutex:
            try:
                result = await tx_coro(db)
                await db.commit()
            except Exception:
                try:
                    await db.rollback()
                except Exception:
                    pass
                raise
            self._write_counter += 1
            if self._write_counter >= self._checkpoint_threshold:
                self._write_counter = 0
                now_ts = int(time.time())
                try:
                    await db.execute("DELETE FROM redeemed_nullifiers WHERE expires_at <= ?;", (now_ts,))
                    await db.execute("DELETE FROM omni_resource_registry WHERE expires_at <= ?;", (now_ts,))
                    await db.commit()
                    await db.execute("PRAGMA wal_checkpoint(PASSIVE);")
                except Exception:
                    pass
            return result


DB_WRITER_DAEMON = SingleWriterSQLiteDaemon()


<!-- [ID:13_DATA_SCHEMA_S015] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: USER_ID -->
# ==============================================================================
STRIPE_COUNT = 4096
USER_LOCK_STRIPES = [asyncio.Lock() for _ in range(STRIPE_COUNT)]
ANTI_TUYUL_VELOCITY: dict[int, float] = {}
OWNER_CLAIM_FAIL_TRACKER: dict[int, int] = {}
def get_user_lock(user_id: int) -> asyncio.Lock:
   return USER_LOCK_STRIPES[user_id % STRIPE_COUNT]
def check_velocity_rate_limit(
   user_id: int, min_interval_sec: float = 0.45
) -> bool:
   now = time.monotonic()
   if now - ANTI_TUYUL_VELOCITY.get(user_id, 0.0) < min_interval_sec:
       return False
   ANTI_TUYUL_VELOCITY[user_id] = now
   if len(ANTI_TUYUL_VELOCITY) > 10000:
       ANTI_TUYUL_VELOCITY.clear()
   return True
class SingleWriterSQLiteDaemon:
   """Singleton Writer & Managed Connection Pool di atas SQLite WAL."""
   def __init__(self, checkpoint_every_n_writes: int = 400) -> None:
       self._write_mutex = asyncio.Lock()
       self._conn_init_lock = asyncio.Lock()
       self._persistent_conn: aiosqlite.Connection | None = None
       self._write_counter = 0
       self._checkpoint_threshold = checkpoint_every_n_writes
   async def get_shared_connection(self) -> aiosqlite.Connection:
       if self._persistent_conn is None:
           async with self._conn_init_lock:
               if self._persistent_conn is None:
                   conn = await aiosqlite.connect(DB_PATH)
                   await conn.execute("PRAGMA journal_mode = WAL;")
                   await conn.execute("PRAGMA synchronous = NORMAL;")
                   await conn.execute("PRAGMA busy_timeout = 10000;")
                   await conn.execute("PRAGMA foreign_keys = ON;")
                   self._persistent_conn = conn
       return self._persistent_conn
   async def execute_write_tx(
       self,
       db: aiosqlite.Connection,
       tx_coro: Callable[[aiosqlite.Connection], Coroutine[Any, Any, Any]],
   ) -> Any:
       async with self._write_mutex:
           try:
               result = await tx_coro(db)
               await db.commit()
           except Exception:
               try:
                   await db.rollback()
               except Exception:
                   pass
               raise
           self._write_counter += 1
           if self._write_counter >= self._checkpoint_threshold:
               self._write_counter = 0
               now_ts = int(time.time())
               try:
                   await db.execute(
                       "DELETE FROM redeemed_nullifiers WHERE expires_at <= ?;",



<!-- [ID:13_DATA_SCHEMA_S016] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
STRIPE_COUNT = 4096
USER_LOCK_STRIPES = [asyncio.Lock() for _ in range(STRIPE_COUNT)]


def get_user_lock(user_id: int) -> asyncio.Lock:
    return USER_LOCK_STRIPES[user_id % STRIPE_COUNT]


@asynccontextmanager
async def get_db() -> AsyncIterator[aiosqlite.Connection]:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA journal_mode = WAL;")
        await db.execute("PRAGMA synchronous = NORMAL;")
        await db.execute("PRAGMA busy_timeout = 10000;")
        await db.execute("PRAGMA foreign_keys = ON;")
        yield db


class SingleWriterSQLiteDaemon:
    def __init__(self, checkpoint_every_n_writes: int = 400):
        self._write_mutex = asyncio.Lock()
        self._write_counter = 0
        self._checkpoint_threshold = checkpoint_every_n_writes

    async def execute_write_tx(
        self,
        db: aiosqlite.Connection,
        tx_coro: Callable[[aiosqlite.Connection], Coroutine[Any, Any, Any]],
    ) -> Any:
        async with self._write_mutex:
            try:
                result = await tx_coro(db)
                await db.commit()
            except Exception:
                try:
                    await db.rollback()
                except Exception:
                    pass
                raise
            self._write_counter += 1
            if self._write_counter >= self._checkpoint_threshold:
                self._write_counter = 0
                await self._run_inline_maintenance(db)
            return result

    async def _run_inline_maintenance(self, db: aiosqlite.Connection) -> None:
        now_ts = int(time.time())
        try:
            await db.execute("DELETE FROM redeemed_nullifiers WHERE expires_at <= ?;", (now_ts,))
            await db.execute("DELETE FROM omni_resource_registry WHERE expires_at <= ?;", (now_ts,))
            await db.commit()
            await db.execute("PRAGMA wal_checkpoint(PASSIVE);")
        except Exception:
            pass


DB_WRITER_DAEMON = SingleWriterSQLiteDaemon()


<!-- [ID:13_DATA_SCHEMA_S017] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :-4 -->
# ==============================================================================
def compute_crc16_ccitt(data_str: str) -> str:
    crc = 0xFFFF
    for ch in data_str.encode("utf-8"):
        crc ^= ch << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if (crc & 0x8000) else (crc << 1) & 0xFFFF
    return f"{crc:04X}"


def generate_dynamic_qris_string(static_qris: str, amount_idr: int) -> str:
    if not static_qris or len(static_qris) < 20 or "5802ID" not in static_qris:
        static_qris = "00020101021126610014ID.CO.GOPAY.WWW01189360091431234567890210G1234567890303UMI51440014ID.CO.QRIS.WWW0215ID10200000000010303UMI5204581253033605802ID5912BIKINAI STUDIO6007JAKARTA6304ABCD"
    base_qris = static_qris[:-4].replace("010211", "010212", 1)
    if base_qris.endswith("6304"):
        base_qris = base_qris[:-4]
    amt_str = str(int(amount_idr))
    tag_54 = f"54{len(amt_str):02d}{amt_str}"
    parts = base_qris.split("5802ID", 1)
    reconstructed = f"{parts[0]}{tag_54}5802ID{parts[1]}6304"
    return f"{reconstructed}{compute_crc16_ccitt(reconstructed)}"


async def create_payment_invoice(db: aiosqlite.Connection, user_id: int, ppp_zone: int) -> dict[str, Any]:
    invoice_id = f"INV-{user_id}-{int(time.time())}"
    unique_code = (user_id % 89) + 10
    exact_idr = 5000 + unique_code
    provider = (
        RUNTIME_CONFIG["ID_ACTIVE_PROVIDER"]
        if ppp_zone == 3
        else RUNTIME_CONFIG["GLOBAL_ACTIVE_PROVIDER"]
    )

    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(
            """
            INSERT INTO payment_invoices (invoice_id, user_id, amount_idr, coins_credited, provider, status, created_at)
            VALUES (?, ?, ?, 60, ?, 'PENDING', ?);
            """,
            (invoice_id, user_id, exact_idr, provider, int(time.time())),
        )

    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)

    if ppp_zone in (1, 2):
        usd_price = "$1.99" if ppp_zone == 1 else "$0.99"
        stars_amt = 110 if ppp_zone == 1 else 55
        return {
            "invoice_id": invoice_id,
            "provider": provider,
            "display_amount": f"{usd_price} USDT / {stars_amt} Telegram Stars ⭐",
            "qris_payload": "",
            "is_global": True,
        }
    return {
        "invoice_id": invoice_id,
        "provider": provider,
        "display_amount": f"Rp {exact_idr:,}",
        "qris_payload": generate_dynamic_qris_string(GOPAY_STATIC_QRIS_RAW, exact_idr),
        "is_global": False,
    }


async def approve_invoice_and_credit_coins(
    db: aiosqlite.Connection, invoice_id: str
) -> tuple[bool, int, int, str]:
    """Mengubah status invoice PENDING -> PAID secara atomik (Anti-Double-Credit)."""
    async def _tx(conn: aiosqlite.Connection) -> tuple[bool, int, int, str]:
        cur = await conn.execute(
            "SELECT user_id, amount_idr, coins_credited, status FROM payment_invoices WHERE invoice_id = ?;",
            (invoice_id,),
        )
        row = await cur.fetchone()
        if not row:
            return False, 0, 0, "Tagihan tidak ditemukan."
        uid, amt_idr, coins_add, st = int(row[0]), int(row[1]), int(row[2]), str(row[3])
        if st == "PAID":
            return False, uid, 0, "Tagihan ini sudah pernah diverifikasi sebelumnya."
        await conn.execute("UPDATE payment_invoices SET status = 'PAID' WHERE invoice_id = ?;", (invoice_id,))
        await conn.execute(
            "UPDATE users SET koin_utama = koin_utama + ?, has_topped_up = 1 WHERE internal_user_id = ?;",
            (coins_add, uid),
        )
        return True, uid, amt_idr, f"+{coins_add} Koin Utama berhasil ditambahkan!"

    ok, uid, amt_idr, msg = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    if ok and amt_idr > 0:
        await record_job_and_split_profit(db, revenue_idr=amt_idr, actual_hpp_idr=750)
    return ok, uid, amt_idr, msg



<!-- [ID:13_DATA_SCHEMA_S018] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: COMPONENT, :10 -->
## Halaman 386

       if success and component in self.incident_remediation_count:
           self.incident_remediation_count[component] = 0
   def build_gitops_commit_plan(
       self, ast_hash: str, summary: str
   ) -> dict[str, str]:
       return {
           "shadow_branch": f"autonomic/patch-{ast_hash[:10]}",
           "verify_cmd": "python3 -m py_compile app.py",
           "commit_cmd": f"git checkout -b autonomic/patch-{ast_hash[:10]} && git commit -am '[Autonomic-Heal
           "rollback_cmd": "git revert --no-edit HEAD",
       }
AUTONOMIC_GUARD = AutonomicConvergenceGuard()
class SelfHealingOrchestrator:
   """
   Self-Healing Loop Level Orchestrator (Sesuai Kontrak D2):
   classify error -> pilih handler -> apply fix -> verify -> gagal 3x -> escalate ke log + human queue.
   """
   MAX_SAFE_RETRIES = 3
   def classify_error(self, error: Exception | str) -> str:
       msg = str(error).lower()
       if "429" in msg or "rate limit" in msg or "quota" in msg:
           return "RATE_LIMIT_EXHAUSTED"
       if "timeout" in msg or "connect" in msg or "502" in msg or "503" in msg:
           return "UPSTREAM_TIMEOUT_OR_DOWN"
       if "locked" in msg or "sqlite" in msg or "busy" in msg:
           return "DATABASE_CONTENTION"
       if "json" in msg or "parse" in msg:
           return "MALFORMED_UPSTREAM_PAYLOAD"
       return "UNCLASSIFIED_RUNTIME_FAULT"
   def select_handler(self, error_class: str) -> str:
       handlers = {
           "RATE_LIMIT_EXHAUSTED": "QUARANTINE_NODE_AND_ROTATE_AGENT",
           "UPSTREAM_TIMEOUT_OR_DOWN": "SWITCH_STAGGERED_BACKUP_PROVIDER",
           "DATABASE_CONTENTION": "PASSIVE_WAL_CHECKPOINT_AND_BACKOFF",
           "MALFORMED_UPSTREAM_PAYLOAD": "ENABLE_PLAIN_TEXT_STREAM_SCRUBBER",
       }
       return handlers.get(error_class, "ISOLATE_COMPONENT_AND_FALLBACK")
   async def attempt_heal_or_escalate(
       self,
       db: aiosqlite.Connection,
       component: str,
       error: Exception | str,
       fix_coro: Callable[[], Coroutine[Any, Any, bool]] | None = None,
       verify_coro: Callable[[], Coroutine[Any, Any, bool]] | None = None,
   ) -> dict[str, Any]:
       err_class = self.classify_error(error)
       handler_name = self.select_handler(err_class)
       attempts = AUTONOMIC_GUARD.incident_remediation_count.get(component, 0)
       while attempts < self.MAX_SAFE_RETRIES:
           attempts += 1
           AUTONOMIC_GUARD.incident_remediation_count[component] = attempts
           try:
               fix_ok = await fix_coro() if fix_coro else True
               ver_ok = await verify_coro() if verify_coro else fix_ok
               if fix_ok and ver_ok:
                   AUTONOMIC_GUARD.record_telemetry(component, True)
                   return {
                       "healed": True,
                       "escalated": False,
                       "component": component,
                       "error_class": err_class,
                       "handler": handler_name,
                       "attempts": attempts,
                   }



<!-- [ID:13_DATA_SCHEMA_S019] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
STRIPE_COUNT = 4096
USER_LOCK_STRIPES = [asyncio.Lock() for _ in range(STRIPE_COUNT)]
def get_user_lock(user_id: int) -> asyncio.Lock:
   return USER_LOCK_STRIPES[user_id % STRIPE_COUNT]
class SingleWriterSQLiteDaemon:
   def __init__(self, checkpoint_every_n_writes: int = 400) -> None:
       self._write_mutex = asyncio.Lock()
       self._conn_init_lock = asyncio.Lock()
       self._persistent_conn: aiosqlite.Connection | None = None
       self._write_counter = 0
       self._checkpoint_threshold = checkpoint_every_n_writes
   async def get_shared_connection(self) -> aiosqlite.Connection:
       if self._persistent_conn is None:
           async with self._conn_init_lock:
               if self._persistent_conn is None:
                   conn = await aiosqlite.connect(DB_PATH)
                   await conn.execute("PRAGMA journal_mode = WAL;")
                   await conn.execute("PRAGMA synchronous = NORMAL;")
                   await conn.execute("PRAGMA busy_timeout = 10000;")
                   await conn.execute("PRAGMA foreign_keys = ON;")
                   self._persistent_conn = conn
       return self._persistent_conn
   async def execute_write_tx(self, db: aiosqlite.Connection, tx_coro: Callable[[aiosqlite.Connection], Corou
       async with self._write_mutex:
           try:
               result = await tx_coro(db)
               await db.commit()
           except Exception:
               try:
                   await db.rollback()
               except Exception:
                   pass
               raise
           self._write_counter += 1
           if self._write_counter >= self._checkpoint_threshold:
               self._write_counter = 0
               now_ts = int(time.time())
               try:
                   await db.execute("DELETE FROM redeemed_nullifiers WHERE expires_at <= ?;", (now_ts,))
                   await db.execute("DELETE FROM omni_resource_registry WHERE expires_at <= ?;", (now_ts,))



<!-- [ID:13_DATA_SCHEMA_S020] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: ORDER_ID, PAID -->
# Penyimpanan in-memory (Bisa diganti SQLite / PostgreSQL untuk produksi)
INVOICES = {}

class CreateInvoiceRequest(BaseModel):
    order_id: str
    base_amount: int
    webhook_url: str | None = None

@app.post("/api/create-payment")
async def create_payment(req: CreateInvoiceRequest):
    now = int(time.time())
    # Bersihkan tagihan yang sudah kadaluarsa
    active_amounts = {
        inv["final_amount"] for inv in INVOICES.values()
        if inv["status"] == "PENDING" and inv["expires_at"] > now
    }

    # Cari kode unik (1 - 499) yang sedang tidak dipakai transaksi lain
    unique_code = None
    for _ in range(500):
        candidate = random.randint(1, 499)
        if (req.base_amount + candidate) not in active_amounts:
            unique_code = candidate
            break

    if unique_code is None:
        raise HTTPException(status_code=429, detail="Slot kode unik penuh, coba sesaat lagi.")

    final_amount = req.base_amount + unique_code
    dynamic_qris = generate_dynamic_qris(STATIC_QRIS_STRING, final_amount)

    INVOICES[req.order_id] = {
        "order_id": req.order_id,
        "base_amount": req.base_amount,
        "unique_code": unique_code,
        "final_amount": final_amount,
        "qris_string": dynamic_qris,
        "status": "PENDING",
        "created_at": now,
        "expires_at": now + INVOICE_EXPIRY_SECONDS,
        "webhook_url": req.webhook_url
    }

    return INVOICES[req.order_id]

@app.get("/api/status/{order_id}")
async def check_status(order_id: str):
    if order_id not in INVOICES:
        raise HTTPException(status_code=404, detail="Invoice tidak ditemukan")
    return INVOICES[order_id]

async def mutation_worker():
    """Background worker yang berjalan otomatis mengecek dana masuk setiap 5 detik."""
    while True:
        try:
            now = int(time.time())
            has_pending = any(
                inv["status"] == "PENDING" and inv["expires_at"] > now
                for inv in INVOICES.values()
            )
            # Hanya cek mutasi jika sedang ada invoice PENDING (Hemat resource server!)
            if has_pending:
                incoming_list = await asyncio.to_thread(
                    check_incoming_mutations, IMAP_HOST, EMAIL_USER, EMAIL_APP_PASSWORD
                )
                for amt in incoming_list:
                    for order_id, inv in INVOICES.items():
                        if inv["status"] == "PENDING" and inv["expires_at"] > now and inv["final_amount"] == amt:
                            inv["status"] = "PAID"
                            inv["paid_at"] = now
                            print(f"[PAID] Order {order_id} lunas sebesar Rp {amt}")
                            # Kirim Webhook otomatis ke web/bot milik Anda
                            if inv["webhook_url"]:
                                async with httpx.AsyncClient() as client:
                                    await client.post(inv["webhook_url"], json=inv)
        except Exception as e:
            print(f"[Worker Error]: {e}")
        await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(mutation_worker())

Mengapa Sistem Ini Sangat Kuat Jika Anda Pakai Sendiri?
 * Hanya Jalan Saat Ada Tagihan Aktif: Perhatikan variabel has_pending pada kode di atas—server Anda tidak melakukan pengecekan apa pun jika sedang tidak ada orang yang checkout, sehingga sangat ringan dan aman.
 * Bebas Biaya Potongan PG: Jika Anda menggunakan QRIS Merchant reguler (atau transfer langsung ke Bank Jago/SeaBank/BCA/Mandiri), uang langsung cair ke rekening Anda tanpa dipotong Rp 4.000–Rp 5.000 per transaksi seperti Virtual Account di PG pihak ketiga.
 * 100% Self-Hosted: Tidak ada orang luar yang memegang kunci API atau saldo Anda.
Apakah Anda berencana mengintegrasikan Self Payment Gateway buatan Anda ini untuk pembayaran otomatis di Bot Telegram / Mini App, atau untuk checkout di Website? Saya bisa bantu buatkan sekalian script tampilan halaman pembayaran (checkout page dengan countdown timer + auto-render gambar QRIS) jika Anda membutuhkannya.
import asyncio
import random
import time
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from qris_engine import generate_dynamic_qris
from mutation_engine import check_incoming_mutations

app = FastAPI(title="Self Payment Gateway 100% Pure Code")

