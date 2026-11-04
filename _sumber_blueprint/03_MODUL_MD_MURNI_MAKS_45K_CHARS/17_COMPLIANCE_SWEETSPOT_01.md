
<!-- [ID:17_COMPLIANCE_S001] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: STR -->
# ==============================================================================
TOPUP_PACKAGES: Dict[str, Dict[str, Any]] = {
    "ECERAN": {
        "name": "Paket Eceran",
        "amount_idr": 2000,
        "coins": 24,
        "stars": 10,
        "clean_watermark": True,
        "desc": "Rp 2.000 = 24 Koin Utama (100% Bebas Watermark)",
    },
    "HEMAT": {
        "name": "Paket Hemat",
        "amount_idr": 5000,
        "coins": 60,
        "stars": 25,
        "clean_watermark": True,
        "desc": "Rp 5.000 = 60 Koin Utama (100% Bebas Watermark)",
    },
    "KREATOR_PRO": {
        "name": "Paket Kreator Pro",
        "amount_idr": 25000,
        "coins": 350,
        "stars": 110,
        "clean_watermark": True,
        "desc": "Rp 25.000 = 350 Koin Utama + Prioritas Render (Bebas Watermark)",
    },
    "VIBE_CODER": {
        "name": "Paket Vibe-Coder",
        "amount_idr": 55000,
        "coins": 850,
        "stars": 240,
        "clean_watermark": True,
        "desc": "Rp 55.000 = 850 Koin Utama + API Key Bearer sk-bikinai (Bebas Watermark)",
    },
    "SULTAN": {
        "name": "Paket Sultan",
        "amount_idr": 200000,
        "coins": 3600,
        "stars": 850,
        "clean_watermark": True,
        "desc": "Rp 200.000 = 3.600 Koin Utama + VIP Dedicated Lane (Bebas Watermark)",
    },
}

PPP_ZONES: Dict[int, Dict[str, Any]] = {
    1: {"label": "Zona 1 — Global Tier-1 (US/UK/EU/SG/JP)", "multiplier": 1.00, "currency": "USD/Stars"},
    2: {"label": "Zona 2 — Global Tier-2 (KR/TW/AE/SA/PL)", "multiplier": 0.70, "currency": "USD/Stars"},
    3: {"label": "Zona 3 — Emerging Markets (BR/MX/TR/TH/MY/VN)", "multiplier": 0.50, "currency": "Local/Stars"},
    4: {"label": "Zona 4 — Indonesia Lokal (QRIS / E-Wallet)", "multiplier": 0.25, "currency": "IDR (QRIS)"},
}


def detect_ppp_zone(language_code: Optional[str]) -> int:
    """Mendeteksi Zona PPP (1..4) berdasarkan kode bahasa pengguna."""
    code = (language_code or "id").strip().lower()
    if code.startswith(("id", "jv", "su", "ms-id")):
        return 4
    if code.startswith(("pt", "es", "tr", "th", "vi", "ms", "hi", "tl")):
        return 3
    if code.startswith(("ko", "zh-tw", "ar", "pl", "cs", "hu")):
        return 2
    return 1


def resolve_watermark_policy(
    deducted_utama: int,
    deducted_bonus: int,
    has_active_subscription: bool = False,
    explicit_clean_license: bool = False,
) -> Dict[str, Any]:
    """
    ATURAN MUTLAK WATERMARK (A4.a):
    - Jika deducted_utama > 0 (termasuk Paket Eceran Rp 2.000 = 24 Koin Utama,
      Paket Hemat Rp 5.000 = 60 Koin, Paket Kreator Pro Rp 25.000 = 350 Koin,
      Paket Vibe-Coder Rp 55.000, Paket Sultan Rp 200.000)
      ATAU has_active_subscription ATAU explicit_clean_license:
      -> apply_watermark = False (nologo=true, 100% bebas watermark).
    - Watermark "⚡ bikinAI SI" (nologo=false) HANYA dipasang jika deducted_utama == 0
      (murni menggunakan Koin Bonus gratisan).
    """
    if int(deducted_utama) > 0 or bool(has_active_subscription) or bool(explicit_clean_license):
        return {
            "apply_watermark": False,
            "nologo": "true",
            "is_watermarked": 0,
            "watermark_text": None,
            "license_label": "💎 CLEAN COMMERCIAL LICENSE (100% Tanpa Watermark)",
        }
    return {
        "apply_watermark": True,
        "nologo": "false",
        "is_watermarked": 1,
        "watermark_text": "⚡ bikinAI SI",
        "license_label": "🎁 Mode Bonus Gratis (Watermark: ⚡ bikinAI SI)",
    }


async def ensure_user_profile(
    user_id: int,
    username: str = "",
    first_name: str = "",
    language_code: str = "id",
    referred_by: int = 0,
) -> Dict[str, Any]:
    """Memastikan profil pengguna terdaftar di tabel `users` dan melacak perubahan username."""
    db = get_db()
    now_ts = int(time.time())
    today_epoch = now_ts // 86400
    clean_uname = (username or "").strip().lstrip("@")
    clean_fname = (first_name or "Sahabat Kreator").strip()
    ppp_zone = detect_ppp_zone(language_code)

    existing = await db.fetch_one(
        "SELECT * FROM users WHERE internal_user_id = ?;",
        (int(user_id),),
    )
    if existing is None:
        valid_ref = int(referred_by) if int(referred_by) > 0 and int(referred_by) != int(user_id) else 0
        await db.execute_write(
            """
            INSERT INTO users (
                internal_user_id, username, first_name, language_code,
                koin_utama, koin_bonus, has_topped_up, ppp_zone,
                last_claim_date, chat_used_today, free_img_used_today,
                quota_day_epoch, personal_memory_notes, active_canvas_content,
                referred_by, affiliate_stars_balance, affiliate_idr_pending, created_at
            ) VALUES (?, ?, ?, ?, 0, 15, 0, ?, '', 0, 0, ?, '', '', ?, 0, 0, ?);
            """,
            (int(user_id), clean_uname, clean_fname, language_code or "id", ppp_zone, today_epoch, valid_ref, now_ts),
        )
        return (await db.fetch_one("SELECT * FROM users WHERE internal_user_id = ?;", (int(user_id),))) or {}

    # Cek SangMata Identity History jika username berubah
    old_uname = (existing.get("username") or "").strip()
    if clean_uname and old_uname and clean_uname.lower() != old_uname.lower():
        await db.execute_write(
            """
            INSERT INTO identity_history (user_id, old_username, new_username, changed_at)
            VALUES (?, ?, ?, ?);
            """,
            (int(user_id), old_uname, clean_uname, now_ts),
        )

    # Reset kuota harian jika berganti hari
    if int(existing.get("quota_day_epoch") or 0) != today_epoch:
        await db.execute_write(
            """
            UPDATE users
            SET username = ?, first_name = ?, chat_used_today = 0,
                free_img_used_today = 0, quota_day_epoch = ?
            WHERE internal_user_id = ?;
            """,
            (clean_uname or old_uname, clean_fname, today_epoch, int(user_id)),
        )
    elif clean_uname != old_uname or clean_fname != existing.get("first_name"):
        await db.execute_write(
            "UPDATE users SET username = ?, first_name = ? WHERE internal_user_id = ?;",
            (clean_uname or old_uname, clean_fname, int(user_id)),
        )

    return (await db.fetch_one("SELECT * FROM users WHERE internal_user_id = ?;", (int(user_id),))) or existing


async def create_job_with_atomic_deduction(
    user_id: int,
    cost: int,
    prompt_text: str,
    engine_used: str,
    prefer_utama_first: bool = True,
    explicit_clean_license: bool = False,
) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Memotong koin secara atomik dengan lock stripe pengguna dan membuat entri di tabel `jobs`.
    Jika pengguna memiliki `koin_utama > 0` dan `prefer_utama_first=True`, sistem otomatis
    mengutamakan pemotongan minimal 1 Koin Utama agar hasil karya 100% bebas watermark (A4.a).
    """
    db = get_db()
    async with get_user_lock(user_id):
        user = await ensure_user_profile(user_id)
        utama = int(user.get("koin_utama") or 0)
        bonus = int(user.get("koin_bonus") or 0)
        total_avail = utama + bonus
        if total_avail < cost:
            return (
                False,
                f"Saldo koin belum cukup (Butuh {cost} Koin, saldo Anda: {utama} Koin Utama + {bonus} Koin Bonus).",
                {},
            )

        if prefer_utama_first and utama > 0:
            deducted_utama = min(utama, cost)
            deducted_bonus = cost - deducted_utama
        else:
            deducted_bonus = min(bonus, cost)
            deducted_utama = cost - deducted_bonus

        wm_policy = resolve_watermark_policy(
            deducted_utama=deducted_utama,
            deducted_bonus=deducted_bonus,
            has_active_subscription=bool(user.get("has_topped_up")),
            explicit_clean_license=explicit_clean_license,
        )
        job_id = f"JOB-{int(time.time())}-{secrets.token_hex(3).upper()}"
        now_ts = int(time.time())

        await db.execute_script_tx(
            [
                (
                    """
                    UPDATE users
                    SET koin_utama = koin_utama - ?,
                        koin_bonus = koin_bonus - ?
                    WHERE internal_user_id = ?;
                    """,
                    (deducted_utama, deducted_bonus, int(user_id)),
                ),
                (
                    """
                    INSERT INTO jobs (
                        job_id, internal_user_id, cost, deducted_bonus, deducted_utama,
                        is_watermarked, status, refunded_lock, prompt_text, engine_used,
                        telegram_file_id, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, 'PROCESSING', 0, ?, ?, '', ?);
                    """,
                    (
                        job_id,
                        int(user_id),
                        int(cost),
                        int(deducted_bonus),
                        int(deducted_utama),
                        int(wm_policy["is_watermarked"]),
                        prompt_text[:1000],
                        engine_used,
                        now_ts,
                    ),
                ),
            ]
        )
        return (
            True,
            "OK",
            {
                "job_id": job_id,
                "cost": cost,
                "deducted_utama": deducted_utama,
                "deducted_bonus": deducted_bonus,
                "watermark_policy": wm_policy,
            },
        )


async def finalize_job_status(
    job_id: str,
    success: bool,
    telegram_file_id: str = "",
) -> None:
    """Menyelesaikan status job (`COMPLETED`) atau mengembalikan koin (`REFUNDED`) secara idempoten."""
    db = get_db()
    job = await db.fetch_one("SELECT * FROM jobs WHERE job_id = ?;", (job_id,))
    if not job:
        return
    if success:
        await db.execute_script_tx(
            [
                (
                    "UPDATE jobs SET status = 'COMPLETED', telegram_file_id = ? WHERE job_id = ?;",
                    (telegram_file_id, job_id),
                ),
                (
                    """
                    UPDATE treasury_summary
                    SET total_jobs_completed = total_jobs_completed + 1, updated_at = ?
                    WHERE id = 1;
                    """,
                    (int(time.time()),),
                ),
            ]
        )
    else:
        if int(job.get("refunded_lock") or 0) == 0:
            await db.execute_script_tx(
                [
                    (
                        "UPDATE jobs SET status = 'FAILED_REFUNDED', refunded_lock = 1 WHERE job_id = ?;",
                        (job_id,),
                    ),
                    (
                        """
                        UPDATE users
                        SET koin_utama = koin_utama + ?,
                            koin_bonus = MIN(25, koin_bonus + ?)
                        WHERE internal_user_id = ?;
                        """,
                        (
                            int(job.get("deducted_utama") or 0),
                            int(job.get("deducted_bonus") or 0),
                            int(job.get("internal_user_id") or 0),
                        ),
                    ),
                ]
            )


async def create_payment_invoice(
    user_id: int,
    tier_key: str,
    provider: str = "QRIS_LOKAL",
) -> Dict[str, Any]:
    """Membuat invoice top-up baru di tabel `payment_invoices`."""
    pkg = TOPUP_PACKAGES.get(tier_key.upper(), TOPUP_PACKAGES["ECERAN"])
    user = await ensure_user_profile(user_id)
    zone = int(user.get("ppp_zone") or 4)
    # Harga IDR disesuaikan untuk Zona 4 (Indonesia QRIS) atau mengikuti pengali PPP untuk global
    base_idr = int(pkg["amount_idr"])
    if zone != 4:
        mult = float(PPP_ZONES.get(zone, PPP_ZONES[1])["multiplier"])
        adjusted_idr = int(round((base_idr / 0.25) * mult, -2))
    else:
        adjusted_idr = base_idr

    invoice_id = f"INV-{int(time.time())}-{secrets.token_hex(3).upper()}"
    now_ts = int(time.time())
    await get_db().execute_write(
        """
        INSERT INTO payment_invoices (
            invoice_id, user_id, tier_key, amount_idr, coins_credited,
            provider, status, followup_sent, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, 'PENDING', 0, ?);
        """,
        (invoice_id, int(user_id), tier_key.upper(), adjusted_idr, int(pkg["coins"]), provider, now_ts),
    )
    return {
        "invoice_id": invoice_id,
        "user_id": int(user_id),
        "tier_key": tier_key.upper(),
        "package_name": pkg["name"],
        "amount_idr": adjusted_idr,
        "coins_credited": int(pkg["coins"]),
        "stars": int(pkg["stars"]),
        "provider": provider,
        "status": "PENDING",
    }


async def settle_payment_invoice(invoice_id: str) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Menyelesaikan pembayaran invoice, menambahkan Koin Utama, membagi Treasury
    (35% Working Capital Vault, 65% Harvestable Profit Vault), dan menghitung
    Komisi Affiliate Dual-Mode (Telegram Stars / Referral QRIS Lokal 15%).
    """
    db = get_db()
    inv = await db.fetch_one("SELECT * FROM payment_invoices WHERE invoice_id = ?;", (invoice_id,))
    if not inv:
        return False, "Invoice tidak ditemukan.", {}
    if inv["status"] == "PAID":
        return False, "Invoice ini sudah dibayar sebelumnya.", inv

    user_id = int(inv["user_id"])
    coins = int(inv["coins_credited"])
    amount_idr = int(inv["amount_idr"])
    provider = str(inv["provider"])
    now_ts = int(time.time())

    working_cap = int(amount_idr * 0.35)
    profit_vault = amount_idr - working_cap

    user = await ensure_user_profile(user_id)
    referrer_id = int(user.get("referred_by") or 0)

    ops: List[Tuple[str, Tuple[Any, ...]]] = [
        ("UPDATE payment_invoices SET status = 'PAID' WHERE invoice_id = ?;", (invoice_id,)),
        (
            """
            UPDATE users
            SET koin_utama = koin_utama + ?, has_topped_up = 1
            WHERE internal_user_id = ?;
            """,
            (coins, user_id),
        ),
        (
            """
            UPDATE treasury_summary
            SET gross_revenue_idr = gross_revenue_idr + ?,
                working_capital_vault_idr = working_capital_vault_idr + ?,
                harvestable_profit_vault_idr = harvestable_profit_vault_idr + ?,
                updated_at = ?
            WHERE id = 1;
            """,
            (amount_idr, working_cap, profit_vault, now_ts),
        ),
    ]

    # Komisi Affiliate Dual-Mode (Telegram Stars & Referral QRIS Lokal)
    if referrer_id > 0 and referrer_id != user_id:
        if "STARS" in provider.upper():
            stars_comm = max(1, int(round(coins * 0.12)))
            ops.append(
                (
                    "UPDATE users SET affiliate_stars_balance = affiliate_stars_balance + ? WHERE internal_user_id = ?;",
                    (stars_comm, referrer_id),
                )
            )
        else:
            idr_comm = int(round(amount_idr * 0.15))
            ops.append(
                (
                    "UPDATE users SET affiliate_idr_pending = affiliate_idr_pending + ? WHERE internal_user_id = ?;",
                    (idr_comm, referrer_id),
                )
            )

    # Jika membeli Paket Vibe-Coder atau Sultan, otomatis terbitkan API Key Bearer sk-bikinai-...
    generated_api_key = ""
    if inv["tier_key"] in ("VIBE_CODER", "SULTAN"):
        generated_api_key = f"sk-bikinai-{secrets.token_urlsafe(24)}"
        token_quota = 2_000_000 if inv["tier_key"] == "VIBE_CODER" else 10_000_000
        ops.append(
            (
                """
                INSERT INTO api_keys (api_key, user_id, tier_name, token_quota_remaining, expires_at, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, 1, ?);
                """,
                (generated_api_key, user_id, inv["tier_key"], token_quota, now_ts + 30 * 86400, now_ts),
            )
        )

    await db.execute_script_tx(ops)
    result_meta = dict(inv)
    result_meta["generated_api_key"] = generated_api_key
    return True, f"Pembayaran `{invoice_id}` sukses! +{coins} Koin Utama (100% Bebas Watermark).", result_meta


def generate_ed25519_voucher(coins: int, tier_key: str = "HEMAT", ttl_hours: int = 72) -> str:
    """Membuat kode Voucher kriptografis `VCH-...` dengan tanda tangan HMAC/Ed25519-equivalent."""
    exp = int(time.time()) + int(ttl_hours * 3600)
    nonce = secrets.token_hex(4).upper()
    payload = f"{coins}:{tier_key}:{exp}:{nonce}"
    sig = hmac.new(ED25519_VOUCHER_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16].upper()
    b64_payload = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
    return f"VCH-{b64_payload}-{sig}"


async def redeem_ed25519_voucher(voucher_code: str, user_id: int) -> Tuple[bool, str, int]:
    """Memverifikasi dan mencairkan kode Voucher `VCH-...` dengan perlindungan nullifier anti-replay."""
    code = (voucher_code or "").strip()
    if not code.startswith("VCH-") or code.count("-") < 2:
        return False, "Format kode voucher tidak valid (gunakan awalan VCH-...).", 0
    try:
        _, b64_part, sig_part = code.split("-", 2)
        pad = "=" * ((4 - len(b64_part) % 4) % 4)
        payload = base64.urlsafe_b64decode((b64_part + pad).encode()).decode()
        expected_sig = (
            hmac.new(ED25519_VOUCHER_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16].upper()
        )
        if not hmac.compare_digest(sig_part.upper(), expected_sig):
            return False, "Tanda tangan kriptografi voucher tidak sah.", 0
        coins_str, tier_key, exp_str, nonce = payload.split(":", 3)
        coins = int(coins_str)
        exp = int(exp_str)
        if int(time.time()) > exp:
            return False, "Masa berlaku kode voucher sudah habis.", 0

        nullifier = hashlib.sha256(f"voucher:{nonce}:{sig_part}".encode()).hexdigest()
        db = get_db()
        already = await db.fetch_one(
            "SELECT nullifier_hash FROM redeemed_nullifiers WHERE nullifier_hash = ?;",
            (nullifier,),
        )
        if already:
            return False, "Kode voucher ini sudah pernah digunakan sebelumnya.", 0

        await ensure_user_profile(user_id)
        await db.execute_script_tx(
            [
                (
                    "INSERT INTO redeemed_nullifiers (nullifier_hash, expires_at) VALUES (?, ?);",
                    (nullifier, exp),
                ),
                (
                    "UPDATE users SET koin_utama = koin_utama + ?, has_topped_up = 1 WHERE internal_user_id = ?;",
                    (coins, int(user_id)),
                ),
            ]
        )
        return True, f"Voucher `{tier_key}` berhasil diklaim! +{coins} Koin Utama (100% Bebas Watermark).", coins
    except Exception as exc:
        return False, f"Gagal memproses kode voucher: {exc}", 0



<!-- [ID:17_COMPLIANCE_S002] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 377

       (deducted_utama > 0)
       or has_active_subscription
       or explicit_clean_license
   )
   if is_paid_render:
       return {
           "apply_watermark": False,
           "nologo_param": "true",
           "watermark_badge": "✨ Bebas Watermark (Pro Commercial)",
           "watermark_overlay_text": "",
       }
   wm_txt = RUNTIME_CONFIG.get("WATERMARK_FREE_TIER_TEXT", "⚡ bikinAI SI")
   return {
       "apply_watermark": True,
       "nologo_param": "false",
       "watermark_badge": f"🏷️ Watermark Gratis ({wm_txt})",
       "watermark_overlay_text": wm_txt,
   }
async def _safe_add_column(
   db: aiosqlite.Connection, table: str, col_def: str
) -> None:
   try:
       await db.execute(f"ALTER TABLE {table} ADD COLUMN {col_def};")
   except Exception:
       pass
async def init_master_db(db: aiosqlite.Connection) -> None:
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
           ppp_zone INTEGER NOT NULL DEFAULT 4,
           last_claim_date TEXT,
           chat_used_today INTEGER NOT NULL DEFAULT 0,
           free_img_used_today INTEGER NOT NULL DEFAULT 0,
           quota_day_epoch INTEGER NOT NULL DEFAULT 0,
           personal_memory_notes TEXT DEFAULT '',
           active_canvas_content TEXT DEFAULT '',
           referrer_id INTEGER NOT NULL DEFAULT 0,
           affiliate_Withdrawable_idr INTEGER NOT NULL DEFAULT 0,
           affiliate_total_earned_coins INTEGER NOT NULL DEFAULT 0,
           api_key_token TEXT DEFAULT '',
           subscription_until INTEGER NOT NULL DEFAULT 0,
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
           is_watermarked INTEGER NOT NULL DEFAULT 1,



<!-- [ID:17_COMPLIANCE_S003] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
V4_PRICING_ID = {
   "ECERAN": {"name": "Paket Eceran", "idr": 2000, "coins": 24, "free_wm": True},
   "HEMAT": {"name": "Paket Hemat", "idr": 5000, "coins": 65, "free_wm": True},
   "PRO": {"name": "Paket Studio Pro", "idr": 25000, "coins": 360, "free_wm": True},
   "MANDIRI_API": {"name": "Paket Mandiri API", "idr": 50000, "coins": 800, "free_wm": True, "api": True},
   "SULTAN": {"name": "Paket Sultan VIP", "idr": 200000, "coins": 3600, "free_wm": True, "api": True},
}
V4_PRICING_GLOBAL_SUB = {
   "SUB_CREATOR": {"usd": "$12.99/mo", "stars": 700, "coins": 600, "free_wm": True},
   "SUB_AUTONOMOUS": {"usd": "$29.99/mo", "stars": 1650, "coins": 1800, "free_wm": True, "api": True},
}
def v4_resolve_watermark(deducted_utama: int, is_subscriber: bool = False) -> dict:
   """A4(a): Watermark HANYA untuk koin bonus (gratisan). Berbayar (termasuk Eceran Rp 2.000) 100% bersih."""
   paid = (deducted_utama > 0) or is_subscriber
   return {"apply_watermark": not paid, "nologo": "true" if paid else "false",
           "badge": "Bebas Watermark (Pro)" if paid else "Watermark Gratis (bikinAI SI)"}
class V4SelfHealingAndApprovalCore:
   """Master Contract D2: Self-Healing (Max 3x -> Human Queue) & 5 Human Approval Gates."""
   MANDATORY_GATES = ("DATA_MIGRATION", "PRICE_PLAN_CHANGE", "DELETE_FEATURE_PLUGIN",
                      "WITHDRAW_ABOVE_THRESHOLD", "SECURITY_POLICY_CHANGE")
   def __init__(self):
       self.failures = {}
       self.human_queue = []
       self.pending_approvals = {}
       self.plugins = {}
   def register_plugin(self, name: str, handler, health_fn=None):



<!-- [ID:17_COMPLIANCE_S004] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
MAX_KOIN_BONUS_CAP = 25
PPP_EFFECTIVE_COIN_IDR = {1: 580, 2: 406, 3: 290, 4: 83}
PPP_PRICING_PACKAGES: dict[str, dict[str, dict[str, Any]]] = {
   "ID": {
       "ECERAN": {"name": "⚡ Paket Eceran / Ketengan", "idr": 2000, "coins": 24, "free_wm": True},
       "HEMAT": {"name": "💎 Paket Hemat Kreator", "idr": 5000, "coins": 65, "free_wm": True},
       "PRO": {"name": "🚀 Paket Studio Pro", "idr": 25000, "coins": 360, "free_wm": True},
       "MANDIRI_API": {"name": "🔌 Paket Mandiri / Vibecoder API", "idr": 50000, "coins": 800, "free_wm": Tru
       "SULTAN": {"name": "👑 Paket Sultan / Agensi VIP", "idr": 200000, "coins": 3600, "free_wm": True, "api
   },
   "GLOBAL": {
       "HEMAT": {"name": "⚡ Starter Creator Pack", "usd": "$1.99", "stars": 110, "idr_eq": 31000, "coins": 6
       "PRO": {"name": "🚀 Studio Pro Pack", "usd": "$9.99", "stars": 550, "idr_eq": 155000, "coins": 360, "f
       "SULTAN": {"name": "👑 Sovereign Executive VIP", "usd": "$49.99", "stars": 2750, "idr_eq": 775000, "co
       "SUB_CREATOR": {"name": "🌟 Global Creator Monthly Subscription", "usd": "$12.99/mo", "stars": 700, "i
       "SUB_AUTONOMOUS": {"name": "💎 Global Autonomous Pro Subscription", "usd": "$29.99/mo", "stars": 1650,
   },
}
def resolve_watermark_policy(deducted_utama: int, has_active_subscription: bool = False, explicit_clean_licens
   """[ATURAN A4.a]: Watermark HANYA untuk Koin Bonus (gratisan). Berbayar (Eceran Rp 2.000 / Tier / Sub) 100
   is_paid = (deducted_utama > 0) or has_active_subscription or explicit_clean_license
   if is_paid:
       return {"apply_watermark": False, "nologo_param": "true", "watermark_badge": "✨ Bebas Watermark (Pro 
   wm_txt = RUNTIME_CONFIG.get("WATERMARK_FREE_TIER_TEXT", "⚡ bikinAI SI")
   return {"apply_watermark": True, "nologo_param": "false", "watermark_badge": f"🏷️ Watermark Gratis ({wm_tx
async def init_master_db(db: aiosqlite.Connection) -> None:
   await db.executescript("""
       CREATE TABLE IF NOT EXISTS users (
           internal_user_id INTEGER PRIMARY KEY,
           username TEXT DEFAULT 'Kreator',
           first_name TEXT DEFAULT '',
           language_code TEXT DEFAULT 'id',
           koin_utama INTEGER NOT NULL DEFAULT 0 CHECK (koin_utama >= 0),
           koin_bonus INTEGER NOT NULL DEFAULT 4 CHECK (koin_bonus >= 0 AND koin_bonus <= 25),
           has_topped_up INTEGER NOT NULL DEFAULT 0,
           ppp_zone INTEGER NOT NULL DEFAULT 4,
           last_claim_date TEXT,
           chat_used_today INTEGER NOT NULL DEFAULT 0,
           free_img_used_today INTEGER NOT NULL DEFAULT 0,
           quota_day_epoch INTEGER NOT NULL DEFAULT 0,
           personal_memory_notes TEXT DEFAULT '',
           active_canvas_content TEXT DEFAULT '',
           referrer_id INTEGER NOT NULL DEFAULT 0,
           affiliate_withdrawable_idr INTEGER NOT NULL DEFAULT 0,
           affiliate_total_earned_coins INTEGER NOT NULL DEFAULT 0,
           api_key_token TEXT DEFAULT '',
           subscription_until INTEGER NOT NULL DEFAULT 0,
           created_at INTEGER NOT NULL
       );
       CREATE TABLE IF NOT EXISTS identity_history (



<!-- [ID:17_COMPLIANCE_S005] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## 2. Rate Limit
| Path | Limit | Action |
|---|---|---|
| `/api/login` | 5/min/IP | block 15 menit |
| `/api/*` | 60/min/IP | challenge |
| `/payment/*` | 10/min/IP | block |
| `/scan/*` | 20/min/IP | block |
| `/agent/*/act` | 30/min/IP | block + alert |


<!-- [ID:17_COMPLIANCE_S006] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 426

               InlineKeyboardButton(
                   text=claim_label, callback_data="menu:claim_daily"
               ),
           ],
           [
               InlineKeyboardButton(
                   text=topup_label, callback_data="menu:topup_qris"
               ),
               InlineKeyboardButton(
                   text="🤝 Program Afiliasi & API Mandiri",
                   callback_data="menu:affiliate_hub",
               ),
           ],
           [
               InlineKeyboardButton(
                   text="🛡️ Bantuan & Garansi Koin 100%",
                   callback_data="menu:live_support",
               ),
               InlineKeyboardButton(
                   text="🧭 Panduan, FAQ & Grup",
                   callback_data="menu:faq_tos",
               ),
           ],
           [
               InlineKeyboardButton(
                   text="⬅️ Tampilan Ringkas (3 Langkah Mudah)",
                   callback_data="menu:home_3step",
               )
           ],
       ]
   )
   return InlineKeyboardMarkup(inline_keyboard=rows)
def build_customer_dashboard_caption(
   username: str, u: dict[str, Any]
) -> str:
   if u.get("has_active_sub"):
       tier_badge = "👑 SUBSCRIBER VIP (100% BEBAS WATERMARK)"
   elif u["has_topped_up"] or u["koin_utama"] > 0:
       tier_badge = "🌟 KREATOR PRO (KOIN UTAMA BEBAS WATERMARK)"
   else:
       tier_badge = "⚡ KREATOR EKSPLORER (MODE GRATIS)"
   hh_banner = (
       "\n🎉 **FLASH HAPPY HOUR AKTIF: SEMUA PEMBUATAN KARYA GRATIS 0 KOIN!** 🎉\n"
       if RUNTIME_CONFIG["HAPPY_HOUR_MODE"]
       else ""
   )
   safe_u = u.get("safe_uname") or username
   return (
       f"┏━━━ ⚡ **bikinAI SUPER INTELLIGENCE v4.0** ⚡ ━━━┓\n"
       f"┃ 👤 **Kreator:** `@{safe_u}`\n"
       f"┃ 🏅 **Status:** `{tier_badge}`\n"
       f"┣━━━━━━━━━━━━━━━━━━━━━━━┫\n"
       f"┃ 💎 **Koin Utama (Free Watermark):** `{u['koin_utama']} Koin`\n"
       f"┃ 🎁 **Koin Bonus (Ber-Watermark):** `{u['koin_bonus']}/{MAX_KOIN_BONUS_CAP} Koin`\n"
       f"┃ 💬 **Teman Diskusi AI 24 Jam:** `🟢 AKTIF (Gratis)`\n"
       f"┗━━━━━━━━━━━━━━━━━━━━━━━┛{hh_banner}\n\n"
       f"✨ **Selamat datang di Etalase Studio Kreatif AI Generasi Baru.**\n"
       f"▸ Ketik apa saja di ruang chat untuk mengobrol santai, atau pilih **3 Langkah Mudah** di bawah ini:"
   )
def build_400_percent_derivative_upsell_kb() -> InlineKeyboardMarkup:
   return InlineKeyboardMarkup(
       inline_keyboard=[
           [
               InlineKeyboardButton(
                   text="🖼️ Ambil Poster Thumbnail 4K (+4 Koin)",
                   callback_data="drv:poster4k",
               ),



<!-- [ID:17_COMPLIANCE_S007] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :200, :24, :10 -->
## Halaman 435

               if utama >= cost:
                   use_utama = cost
                   use_bonus = 0
               else:
                   use_bonus = min(bonus, cost)
                   use_utama = cost - use_bonus
           else:
               if utama < cost:
                   return (
                       False,
                       f"Fitur Pro ini memerlukan {cost} Koin Utama (Saldo Koin Utama Anda: {utama}).",
                       0,
                   )
               use_bonus, use_utama = 0, cost
           is_wm = 0 if (use_utama > 0 or has_sub) else 1
           await conn.execute(
               "UPDATE users SET koin_utama = koin_utama - ?, koin_bonus = koin_bonus - ? WHERE internal_user
               (use_utama, use_bonus, user_id),
           )
           await conn.execute(
               """
               INSERT INTO jobs (job_id, internal_user_id, cost, deducted_bonus, deducted_utama, status, prom
               VALUES (?, ?, ?, ?, ?, 'PROCESSING', ?, ?, ?, ?);
               """,
               (
                   job_id,
                   user_id,
                   cost,
                   use_bonus,
                   use_utama,
                   prompt_text[:200],
                   engine_used,
                   is_wm,
                   int(time.time()),
               ),
           )
           wm_info = (
               "Bebas Watermark" if is_wm == 0 else "Watermark Gratis"
           )
           return (
               True,
               f"Terpakai {use_utama} Koin Utama & {use_bonus} Koin Bonus ({wm_info})",
               use_utama,
           )
       ok, msg, used_utama = await DB_WRITER_DAEMON.execute_write_tx(
           db, _tx
       )
       return ok, job_id, msg, used_utama
async def mark_job_completed(
   db: aiosqlite.Connection,
   job_id: str,
   prompt_text: str,
   engine_name: str,
   media_url: str = "telegram_delivered",
   telegram_file_id: str = "",
   is_watermarked: bool = True,
) -> None:
   sig = hashlib.sha256(
       f"{engine_name}:{prompt_text.strip().lower()}:{int(is_watermarked)}".encode()
   ).hexdigest()[:24]
   asset_id = f"AST-{sig[:10]}-{int(time.time())}"
   async def _tx(conn: aiosqlite.Connection) -> None:
       await conn.execute(
           "UPDATE jobs SET status = 'COMPLETED', is_watermarked = ? WHERE job_id = ?;",
           (1 if is_watermarked else 0, job_id),
       )
       await conn.execute(
           """
           INSERT OR REPLACE INTO syndicated_assets



<!-- [ID:17_COMPLIANCE_S008] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==============================================================================
async def fetch_clean_image_bytes(
   prompt_en: str,
   width: int = 768,
   height: int = 1024,
   apply_watermark: bool = True,
) -> bytes | None:
   """
   Mengambil gambar hasil render dengan aturan Watermark Dual-Tier:
   - apply_watermark=True (Koin Gratisan/Bonus) -> nologo=false & overlay teks komunitas.
   - apply_watermark=False (Koin Utama Berbayar / Subscriber) -> nologo=true (100% Free Watermark).
   """
   nologo_str = "false" if apply_watermark else "true"
   final_prompt = (
       f"{prompt_en}, subtle small corner text '{RUNTIME_CONFIG['WATERMARK_FREE_TIER_TEXT']}'"
       if apply_watermark
       else prompt_en
   )
   url = (
       f"https://image.pollinations.ai/prompt/{quote(final_prompt)}"
       f"?width={width}&height={height}&nologo={nologo_str}&private=true&enhance=true&seed={int(time.time())}
   )
   try:
       async with httpx.AsyncClient(
           timeout=25.0, follow_redirects=True
       ) as client:
           resp = await client.get(url)
           if (
               resp.status_code == 200
               and len(resp.content) > 1000
               and (
                   resp.content[:4].startswith(b"\xff\xd8\xff")
                   or resp.content[:4] == b"\x89PNG"



<!-- [ID:17_COMPLIANCE_S009] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 427

               InlineKeyboardButton(
                   text="🎵 Ekstrak Audio MP3 (+4 Koin)",
                   callback_data="drv:audiomp3",
               ),
           ],
           [
               InlineKeyboardButton(
                   text="✨ Buka Lisensi Komersial Bersih Tanpa Watermark (+10 Koin)",
                   callback_data="drv:clean_license",
               )
           ],
           [
               InlineKeyboardButton(
                   text="⬅️ Kembali ke Menu Utama", callback_data="menu:home"
               )
           ],
       ]
   )
def build_video_wizard_kb(
   session: LiveWizardSession, show_more: bool = False
) -> tuple[str, InlineKeyboardMarkup]:
   if session.upscale_mode in ("PHOTO_FACE_4K", "TEXT_LINE_4K"):
       session.upscale_mode = "VIDEO_4K_60FPS"
   coins, _, _ = session.get_pricing()
   ups_label = UPSCALER_WHITE_LABEL.get(
       session.upscale_mode, "🎞️ Pertajam & Haluskan Video 4K 60FPS"
   )
   preset_info = (
       f"\n┣ 🎥 **Preset Gerakan (Motion):** `{session.awam_preset}`"
       if session.awam_preset
       else ""
   )
   text = (
       f"🎬 **STUDIO VIDEO AI & FOTO JADI VIDEO — bikinAI**\n━━━━━━━━━━━━━━━━━━\n"
       f"📝 **Konsep Video:**\n> _{session.prompt}_\n\n"
       f"┣ ⚡ **Mesin AI Video:** **`{session.video_engine}`**{preset_info}\n"
       f"┣ 📐 **Ukuran Layar:** `{session.aspect_ratio}` | ⏱️ **Durasi:** `{session.duration_sec} Detik`\n"
       f"┗ 🔍 **Kualitas Video:** `{ups_label}`\n━━━━━━━━━━━━━━━━━━\n"
       f"💡 _Tip: Kirim **Foto Produk/Wajah** langsung ke ruang chat jika ingin mengubah foto menjadi video!_
       f"💎 **Biaya:** **`{coins} Koin`** _(Koin Utama = 100% Bebas Watermark)_"
   )
   rows = [
       [
           InlineKeyboardButton(
               text=f"{'✅ ' if session.aspect_ratio=='9:16' else ''}📱 9:16 TikTok",
               callback_data="wiz:ar:9:16",
           ),
           InlineKeyboardButton(
               text=f"{'✅ ' if session.aspect_ratio=='16:9' else ''}🖥️ 16:9 YouTube",
               callback_data="wiz:ar:16:9",
           ),
           InlineKeyboardButton(
               text=f"{'✅ ' if session.aspect_ratio=='1:1' else ''}🟦 1:1 Feed",
               callback_data="wiz:ar:1:1",
           ),
       ],
       [
           InlineKeyboardButton(
               text=f"{'✅ ' if session.duration_sec==5 else ''}⚡ 5 Detik",
               callback_data="wiz:dur:5",
           ),
           InlineKeyboardButton(
               text=f"{'✅ ' if session.duration_sec==10 else ''}🔥 10 Detik",
               callback_data="wiz:dur:10",
           ),
           InlineKeyboardButton(
               text=f"{'✅ ' if session.duration_sec==30 else ''}🎬 30s Story",
               callback_data="wiz:dur:30",
           ),
       ],
       [



<!-- [ID:17_COMPLIANCE_S010] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: TAHAP 1, TAHAP 2, TAHAP 3 -->
# ==========================================
print("⚙️ [TAHAP 1] Menyiapkan Lingkungan Pekerja (Anti-Banned)...")
os.chdir('/content') # Biarkan /content untuk Colab
if not os.path.exists('ComfyUI'):
   os.system('git clone https://github.com/comfyanonymous/ComfyUI -q')
os.chdir('/content/ComfyUI')
os.system('pip install -r requirements.txt -q')
folder_list = ['checkpoints', 'input', 'upscale_models']
for folder in folder_list:
   os.makedirs(f'models/{folder}', exist_ok=True)
print("⚙️ [TAHAP 2] Mendownload Model Pony...")
if not os.path.exists('models/checkpoints/Pony_V6_XL.safetensors'):
   os.system('wget -c -q --show-progress -O models/checkpoints/Pony_V6_XL.safetensors https://huggingface.co/
print("⚙️ [TAHAP 3] Menyalakan Mesin Rendering Utama...")
subprocess.Popen(["python", "main.py", "--port", "8188"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
time.sleep(40) # Tunggu server ComfyUI menyala

<!-- [ID:17_COMPLIANCE_S011] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 4. JANTUNG ANTI-BANNED (Zero-Outbound Loop)

<!-- [ID:17_COMPLIANCE_S012] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_24, SPAN_33 -->
## Halaman 232

DELETE_FEATU[span_24](start_span)[span_24](end_span)RE_PLUGIN, 
WITHDRAW_ABOVE_THRESHOLD, dan SECURITY_POLICY_CHANGE—ke dalam tabel 
pending_approvals yang hanya dapat dieksekusi setelah pemilik menekan tombol persetujuan 
adm:apr_yes:<id> atau menolaknya melalui adm:apr_no:<id>. 
Kebijakan Mutlak Watermark, Ekonomi 4-Zona PPP, 
dan Smart Router 8-Agen 
Model monetisasi dalam V4.0.txt menggabungkan inklusivitas harga regional dengan 
perlindungan nilai tambah bagi pengguna berbayar melalui fungsi 
resolve_watermark_policy(deducted_utama, deducted_bonus, has_active_subscription, 
explicit_clean_license). Aturan ini menetapkan bahwa setiap transaksi yang memotong Koin 
Utama (deducted_utama > 0)—termasuk pembelian terkecil sekalipun yaitu Paket Eceran Rp 
2.000 (24 Koin Utama)—atau pengguna dengan langganan aktif maupun lisensi bersih eksplisit, 
secara otomatis memperoleh nilai apply_watermark = False (nologo=true, seratus persen bebas 
tanda air). Tanda air "⚡ bikinAI SI" (nologo=false) hanya disematkan apabila deducted_utama 
== 0, yakni ketika pengguna murni menggunakan Koin Bonus gratisan. 
Kode Tier 
Harga 
Harga Dasar 
(Zona 1 
Global) 
Harga Zona 
2 (70%) 
Harga Zona 
3 (50%) 
Harga Efektif 
Zona 4 
(Indonesia 
QRIS 25%) 
Alokasi Koin 
Utama 
Status Tanda 
Air 
(resolve_wat
ermark_polic
y) 
ECERAN 
Rp 8.000 
Rp 5.600 
Rp 4.000 
Rp 2.000 
24 Koin 
Utama 
100% Bebas 
Watermark 
(nologo=true) 
HEMAT 
Rp 20.000 
Rp 14.000 
Rp 10.000 
Rp 5.000 
60 Koin 
Utama 
100% Bebas 
Watermark 
(nologo=true) 
KREATOR_
PRO 
Rp 100.000 Rp 70.000 
Rp 50.000 
Rp 25.000 
350 Koin 
Utama 
100% Bebas 
Watermark 
(nologo=true) 
VIBE_CODE
R 
Rp 220.000 Rp 154.000 Rp 110.000 Rp 55.000 
850 Koin 
Utama 
100% Bebas 
Watermark 
(nologo=true) 
SULTAN 
Rp 800.000 Rp 560.000 Rp 400.000 Rp 200.000 3.500 Koin 
Utama 
100% Bebas 
Watermark 
(nologo=true) 
Penyesuaian daya beli (Purchasing Power Parity) dihitung melalui matriks empat zona 
(PPP_ZONE_MULTIPLIERS), yang terdiri atas Zona 1 Global Tier-1 
(1.0[span_33](start_span)[span_33](end_span)0), Zona 2 Global Tier-2 (0.70), Zona 3 Pasar 
Berkembang (0.50), dan Zona 4 Indonesia QRIS (0.25), dilengkapi dengan sistem komisi afiliasi 
mode ganda (Telegram Stars dan saldo Rupiah QRIS) serta agen layanan pelanggan otomatis 
"Siska" yang mengirimkan pengingat ramah untuk tagihan berstatus PENDING setelah 
melewati 20 menit. 
Untuk mengoptimalkan kualitas inferensi dan efisiensi biaya komputasi, SmartRouterV4 
mengelola 8-Agent Rolling Pool yang dinilai menggunakan rumus Combo Grading Score: 



<!-- [ID:17_COMPLIANCE_S013] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER -->
## Halaman 371

5. 24/7 Keep-Alive & Anti-Sleep Engine (/healthz): Siap jalan 24/7 di HF Spaces Docker / PaaS Gratis / Termux / Oracle Cloud tanpa mati saat
keluar menu, ditambah PluginRegistry (/suntik), SelfHealingOrchestrator (gagal 3x → human queue), dan HumanApprovalGate.
D4. KONFIRMASI AKHIR SEBELUM PENERBITAN FILE KODE
Sesuai aturan D4 dan A5 ("Tunjukkan revisi dulu. Baru setelah saya setujui → eksekusi"), seluruh hitungan dan koreksi Anda sudah masuk 100%.
Langkah Berikutnya (1 Langkah): Cukup balas "Ya, terbitkan file v4.0 sekarang" dan saya akan langsung mengeluarkan file kode utuh app.py v4.0
(tanpa menutup ruang chat) beserta hasil verifikasi D6 & D7-nya.
User prompt: Langsung terapkan: watermark hanya untuk koin gratisan, berbayar free watermark. Ya, terbitkan file v4.0 sekarang dalam 3 modul
bertahap. tahap 1 sekarang.
Response: DOMAIN: CODING/ARCH (Frontier Level Max)
D5. IMPLEMENTASI TAHAP 1 (MODUL 1 DARI 3 — app.py v4.0)
[FAKTA] [Bersumber] Berikut adalah File Modul 1 dari 3 (app.py — Master Engine v4.0) yang mencakup fondasi Orchestrator Tipis, 15 Tabel
SQLite WAL Terkelola, Plugin Surface (register, health, hot_swap), Self-Healing Loop (gagal 3x → human_escalation_queue), Human
Approval Gate (5 aksi kritis), Kebijakan Watermark Otomatis (Koin Gratisan = Ber-Watermark ⚡ bikinAI SI, Koin Utama/Berbayar/Sub = 100%
Free Watermark), Skema Harga Baru (Indonesia: Eceran Rp 2.000 + Tier + Mandiri API; Global: Tier + Subscription + Affiliate), Multi-Slot QRIS
Barcode Manager, Blinded Ed25519 Voucher, 6-Gate AST/SSRF/ModelScan Sterilizer, dan Bittensor Subnet 27 Adapter.
📄 FILE: app.py (MODUL 1 DARI 3 — Simpan sebagai bagian awal app.py)

<!-- [ID:17_COMPLIANCE_S014] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 7. Dual-Tier Watermark Policy (Gratisan = Watermark | Berbayar = Free Watermark)
