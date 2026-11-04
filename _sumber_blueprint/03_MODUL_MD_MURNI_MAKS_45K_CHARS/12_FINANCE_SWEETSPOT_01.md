
<!-- [ID:12_FINANCE_S001] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# 7. USER IDENTITY, TREASURY & INVOICE ENGINE
async def ensure_user_and_track_identity(db: aiosqlite.Connection, user_id: int, username: str, first_name: str = "", lang_code: str = "id") -> dict[str, Any]:
    today_epoch = int(time.time()) // 86400
    clean_uname = (username or "Kreator").replace("`", "").replace("*", "").replace("_", "\\_")
    raw_uname = username or "Kreator"
    default_ppp_zone = 3 if (not lang_code or lang_code.lower().startswith(("id", "in", "ms"))) else 1

    async def _tx(conn: aiosqlite.Connection) -> dict[str, Any]:
        cur_check = await conn.execute("SELECT username FROM users WHERE internal_user_id = ?;", (user_id,))
        existing = await cur_check.fetchone()
        name_changed_msg = ""
        if not existing:
            await conn.execute(
                "INSERT INTO users (internal_user_id, username, first_name, language_code, koin_utama, koin_bonus, ppp_zone, quota_day_epoch, created_at) VALUES (?, ?, ?, 'id', 0, 4, ?, ?, ?);",
                (user_id, raw_uname, first_name or raw_uname, default_ppp_zone, today_epoch, int(time.time())),
            )
        else:
            old_uname = existing[0]
            if RUNTIME_CONFIG["SUBBOT_SANGMATA_ACTIVE"] and old_uname and old_uname != raw_uname and raw_uname != "Kreator":
                await conn.execute("INSERT INTO identity_history (user_id, old_username, new_username, changed_at) VALUES (?, ?, ?, ?);", (user_id, old_uname, raw_uname, int(time.time())))
                await conn.execute("UPDATE users SET username = ? WHERE internal_user_id = ?;", (raw_uname, user_id))
                name_changed_msg = f"@{old_uname} -> @{raw_uname}"

        await conn.execute(
            "UPDATE users SET chat_used_today = CASE WHEN quota_day_epoch < ? THEN 0 ELSE chat_used_today END, free_img_used_today = CASE WHEN quota_day_epoch < ? THEN 0 ELSE free_img_used_today END, quota_day_epoch = ? WHERE internal_user_id = ? AND quota_day_epoch < ?;",
            (today_epoch, today_epoch, today_epoch, user_id, today_epoch),
        )
        cur = await conn.execute("SELECT koin_utama, koin_bonus, has_topped_up, ppp_zone, chat_used_today, free_img_used_today, last_claim_date, personal_memory_notes, active_canvas_content FROM users WHERE internal_user_id = ?;", (user_id,))
        row = await cur.fetchone()
        return {
            "koin_utama": int(row[0]), "koin_bonus": int(row[1]), "has_topped_up": bool(row[2]),
            "ppp_zone": int(row[3]), "chat_used_today": int(row[4]), "free_img_used_today": int(row[5]),
            "last_claim_date": row[6] or "", "memory": row[7] or "", "canvas": row[8] or "",
            "identity_alert": name_changed_msg, "safe_uname": clean_uname,
        }

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def record_job_and_split_profit(db: aiosqlite.Connection, revenue_idr: int, actual_hpp_idr: int, buffer_ratio: float = 0.10) -> dict[str, int]:
    if RUNTIME_CONFIG.get("BANSOS_OPERATION_MODE") == "SILENT_PROFIT":
        actual_hpp_idr = 0
    required_working_capital = int(math.ceil(actual_hpp_idr * (1.0 + buffer_ratio)))
    net_harvestable_profit = max(0, revenue_idr - required_working_capital)

    async def _tx(conn: aiosqlite.Connection) -> int:
        now_ts = int(time.time())
        await conn.execute("INSERT OR IGNORE INTO treasury_summary VALUES (1, 0, 0, 0, 0, 0, ?);", (now_ts,))
        cur = await conn.execute(
            "UPDATE treasury_summary SET gross_revenue_idr = gross_revenue_idr + ?, working_capital_vault_idr = working_capital_vault_idr + ?, harvestable_profit_vault_idr = MAX(0, harvestable_profit_vault_idr + ?), total_jobs_completed = total_jobs_completed + 1, updated_at = ? WHERE id = 1 RETURNING total_jobs_completed;",
            (revenue_idr, required_working_capital, net_harvestable_profit, now_ts),
        )
        row = await cur.fetchone()
        return int(row[0]) if row else 1

    jobs_done = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    return {"working_capital_locked_idr": required_working_capital, "net_profit_ready_to_harvest_idr": net_harvestable_profit, "fomo_counter": RUNTIME_CONFIG["FOMO_COUNTER_BASE"] + jobs_done}


async def execute_manual_profit_harvest(db: aiosqlite.Connection) -> tuple[bool, int, int]:
    async def _tx(conn: aiosqlite.Connection) -> tuple[bool, int, int]:
        now_ts = int(time.time())
        await conn.execute("INSERT OR IGNORE INTO treasury_summary VALUES (1, 0, 0, 0, 0, 0, ?);", (now_ts,))
        cur = await conn.execute("SELECT harvestable_profit_vault_idr, total_harvested_by_owner_idr FROM treasury_summary WHERE id = 1;")
        row = await cur.fetchone()
        if not row or int(row[0]) <= 0:
            return False, 0, int(row[1]) if row else 0
        avail, new_total = int(row[0]), int(row[1]) + int(row[0])
        await conn.execute("UPDATE treasury_summary SET harvestable_profit_vault_idr = 0, total_harvested_by_owner_idr = ?, updated_at = ? WHERE id = 1;", (new_total, now_ts))
        return True, avail, new_total

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


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
    parts = base_qris.split("5802ID", 1)
    reconstructed = f"{parts[0]}54{len(amt_str):02d}{amt_str}5802ID{parts[1]}6304"
    return f"{reconstructed}{compute_crc16_ccitt(reconstructed)}"


async def create_payment_invoice(db: aiosqlite.Connection, user_id: int, ppp_zone: int, tier_key: str = "HEMAT") -> dict[str, Any]:
    invoice_id = f"INV-{user_id}-{int(time.time())}"
    unique_code = (user_id % 89) + 10
    if ppp_zone in (1, 2):
        pkg = PPP_PRICING_PACKAGES["GLOBAL"].get(tier_key, PPP_PRICING_PACKAGES["GLOBAL"]["HEMAT"])
        exact_idr, coins_amt, provider = pkg["idr_eq"], pkg["coins"], RUNTIME_CONFIG["GLOBAL_ACTIVE_PROVIDER"]
        display_amt, qris_str, is_global = f"{pkg['usd']} USDT / {pkg['stars']} Telegram Stars ⭐", "", True
    else:
        pkg = PPP_PRICING_PACKAGES["ID"].get(tier_key, PPP_PRICING_PACKAGES["ID"]["HEMAT"])
        exact_idr, coins_amt, provider = pkg["idr"] + unique_code, pkg["coins"], RUNTIME_CONFIG["ID_ACTIVE_PROVIDER"]
        display_amt, qris_str, is_global = f"Rp {exact_idr:,}", generate_dynamic_qris_string(GOPAY_STATIC_QRIS_RAW, exact_idr), False

    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("INSERT INTO payment_invoices (invoice_id, user_id, amount_idr, coins_credited, provider, status, created_at) VALUES (?, ?, ?, ?, ?, 'PENDING', ?);", (invoice_id, user_id, exact_idr, coins_amt, provider, int(time.time())))

    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    return {"invoice_id": invoice_id, "pkg_name": pkg["name"], "coins": coins_amt, "provider": provider, "display_amount": display_amt, "qris_payload": qris_str, "is_global": is_global}


async def approve_invoice_and_credit_coins(db: aiosqlite.Connection, invoice_id: str) -> tuple[bool, int, int, int, str]:
    async def _tx(conn: aiosqlite.Connection) -> tuple[bool, int, int, int, str]:
        cur = await conn.execute("SELECT user_id, amount_idr, coins_credited, status FROM payment_invoices WHERE invoice_id = ?;", (invoice_id,))
        row = await cur.fetchone()
        if not row:
            return False, 0, 0, 0, "Tagihan tidak ditemukan."
        uid, amt_idr, coins_add, st = int(row[0]), int(row[1]), int(row[2]), str(row[3])
        if st == "PAID":
            return False, uid, 0, 0, "Tagihan sudah diverifikasi."
        await conn.execute("UPDATE payment_invoices SET status = 'PAID' WHERE invoice_id = ?;", (invoice_id,))
        await conn.execute("UPDATE users SET koin_utama = koin_utama + ?, has_topped_up = 1 WHERE internal_user_id = ?;", (coins_add, uid))
        return True, uid, amt_idr, coins_add, f"+{coins_add} Koin Utama ditambahkan!"

    ok, uid, amt_idr, coins_add, msg = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    if ok and amt_idr > 0:
        await record_job_and_split_profit(db, revenue_idr=amt_idr, actual_hpp_idr=int(amt_idr * 0.12))
    return ok, uid, amt_idr, coins_add, msg



<!-- [ID:12_FINANCE_S002] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# 7. IDENTITAS PENGGUNA, TREASURY SPLIT & 3-TIER PPP INVOICE ENGINE
async def ensure_user_and_track_identity(db: aiosqlite.Connection, user_id: int, username: str, first_name: str = "", lang_code: str = "id") -> dict[str, Any]:
    today_epoch = int(time.time()) // 86400
    clean_uname = (username or "Kreator").replace("`", "").replace("*", "").replace("_", "\\_")
    raw_uname = username or "Kreator"
    default_ppp_zone = 3 if (not lang_code or lang_code.lower().startswith(("id", "in", "ms"))) else 1

    async def _tx(conn: aiosqlite.Connection) -> dict[str, Any]:
        cur_check = await conn.execute("SELECT username FROM users WHERE internal_user_id = ?;", (user_id,))
        existing = await cur_check.fetchone()
        name_changed_msg = ""
        if not existing:
            await conn.execute(
                "INSERT INTO users (internal_user_id, username, first_name, language_code, koin_utama, koin_bonus, ppp_zone, quota_day_epoch, created_at) VALUES (?, ?, ?, 'id', 0, 4, ?, ?, ?);",
                (user_id, raw_uname, first_name or raw_uname, default_ppp_zone, today_epoch, int(time.time())),
            )
        else:
            old_uname = existing[0]
            if RUNTIME_CONFIG["SUBBOT_SANGMATA_ACTIVE"] and old_uname and old_uname != raw_uname and raw_uname != "Kreator":
                await conn.execute("INSERT INTO identity_history (user_id, old_username, new_username, changed_at) VALUES (?, ?, ?, ?);", (user_id, old_uname, raw_uname, int(time.time())))
                await conn.execute("UPDATE users SET username = ? WHERE internal_user_id = ?;", (raw_uname, user_id))
                name_changed_msg = f"@{old_uname} -> @{raw_uname}"

        await conn.execute(
            "UPDATE users SET chat_used_today = CASE WHEN quota_day_epoch < ? THEN 0 ELSE chat_used_today END, free_img_used_today = CASE WHEN quota_day_epoch < ? THEN 0 ELSE free_img_used_today END, quota_day_epoch = ? WHERE internal_user_id = ? AND quota_day_epoch < ?;",
            (today_epoch, today_epoch, today_epoch, user_id, today_epoch),
        )
        cur = await conn.execute("SELECT koin_utama, koin_bonus, has_topped_up, ppp_zone, chat_used_today, free_img_used_today, last_claim_date, personal_memory_notes, active_canvas_content FROM users WHERE internal_user_id = ?;", (user_id,))
        row = await cur.fetchone()
        return {
            "koin_utama": int(row[0]), "koin_bonus": int(row[1]), "has_topped_up": bool(row[2]),
            "ppp_zone": int(row[3]), "chat_used_today": int(row[4]), "free_img_used_today": int(row[5]),
            "last_claim_date": row[6] or "", "memory": row[7] or "", "canvas": row[8] or "",
            "identity_alert": name_changed_msg, "safe_uname": clean_uname,
        }

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def record_job_and_split_profit(db: aiosqlite.Connection, revenue_idr: int, actual_hpp_idr: int, buffer_ratio: float = 0.10) -> dict[str, int]:
    if RUNTIME_CONFIG.get("BANSOS_OPERATION_MODE") == "SILENT_PROFIT":
        actual_hpp_idr = 0
    required_working_capital = int(math.ceil(actual_hpp_idr * (1.0 + buffer_ratio)))
    net_harvestable_profit = max(0, revenue_idr - required_working_capital)

    async def _tx(conn: aiosqlite.Connection) -> int:
        now_ts = int(time.time())
        await conn.execute("INSERT OR IGNORE INTO treasury_summary VALUES (1, 0, 0, 0, 0, 0, ?);", (now_ts,))
        cur = await conn.execute(
            "UPDATE treasury_summary SET gross_revenue_idr = gross_revenue_idr + ?, working_capital_vault_idr = working_capital_vault_idr + ?, harvestable_profit_vault_idr = MAX(0, harvestable_profit_vault_idr + ?), total_jobs_completed = total_jobs_completed + 1, updated_at = ? WHERE id = 1 RETURNING total_jobs_completed;",
            (revenue_idr, required_working_capital, net_harvestable_profit, now_ts),
        )
        row = await cur.fetchone()
        return int(row[0]) if row else 1

    jobs_done = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    return {"working_capital_locked_idr": required_working_capital, "net_profit_ready_to_harvest_idr": net_harvestable_profit, "fomo_counter": RUNTIME_CONFIG["FOMO_COUNTER_BASE"] + jobs_done}


async def execute_manual_profit_harvest(db: aiosqlite.Connection) -> tuple[bool, int, int]:
    async def _tx(conn: aiosqlite.Connection) -> tuple[bool, int, int]:
        now_ts = int(time.time())
        await conn.execute("INSERT OR IGNORE INTO treasury_summary VALUES (1, 0, 0, 0, 0, 0, ?);", (now_ts,))
        cur = await conn.execute("SELECT harvestable_profit_vault_idr, total_harvested_by_owner_idr FROM treasury_summary WHERE id = 1;")
        row = await cur.fetchone()
        if not row or int(row[0]) <= 0:
            return False, 0, int(row[1]) if row else 0
        avail, new_total = int(row[0]), int(row[1]) + int(row[0])
        await conn.execute("UPDATE treasury_summary SET harvestable_profit_vault_idr = 0, total_harvested_by_owner_idr = ?, updated_at = ? WHERE id = 1;", (new_total, now_ts))
        return True, avail, new_total

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


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
    parts = base_qris.split("5802ID", 1)
    reconstructed = f"{parts[0]}54{len(amt_str):02d}{amt_str}5802ID{parts[1]}6304"
    return f"{reconstructed}{compute_crc16_ccitt(reconstructed)}"


async def create_payment_invoice(db: aiosqlite.Connection, user_id: int, ppp_zone: int, tier_key: str = "HEMAT") -> dict[str, Any]:
    invoice_id = f"INV-{user_id}-{int(time.time())}"
    unique_code = (user_id % 89) + 10
    if ppp_zone in (1, 2):
        pkg = PPP_PRICING_PACKAGES["GLOBAL"].get(tier_key, PPP_PRICING_PACKAGES["GLOBAL"]["HEMAT"])
        exact_idr, coins_amt, provider = pkg["idr_eq"], pkg["coins"], RUNTIME_CONFIG["GLOBAL_ACTIVE_PROVIDER"]
        display_amt, qris_str, is_global = f"{pkg['usd']} USDT / {pkg['stars']} Telegram Stars ⭐", "", True
    else:
        pkg = PPP_PRICING_PACKAGES["ID"].get(tier_key, PPP_PRICING_PACKAGES["ID"]["HEMAT"])
        exact_idr, coins_amt, provider = pkg["idr"] + unique_code, pkg["coins"], RUNTIME_CONFIG["ID_ACTIVE_PROVIDER"]
        display_amt, qris_str, is_global = f"Rp {exact_idr:,}", generate_dynamic_qris_string(GOPAY_STATIC_QRIS_RAW, exact_idr), False

    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("INSERT INTO payment_invoices (invoice_id, user_id, amount_idr, coins_credited, provider, status, created_at) VALUES (?, ?, ?, ?, ?, 'PENDING', ?);", (invoice_id, user_id, exact_idr, coins_amt, provider, int(time.time())))

    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    return {"invoice_id": invoice_id, "pkg_name": pkg["name"], "coins": coins_amt, "provider": provider, "display_amount": display_amt, "qris_payload": qris_str, "is_global": is_global}


async def approve_invoice_and_credit_coins(db: aiosqlite.Connection, invoice_id: str) -> tuple[bool, int, int, int, str]:
    async def _tx(conn: aiosqlite.Connection) -> tuple[bool, int, int, int, str]:
        cur = await conn.execute("SELECT user_id, amount_idr, coins_credited, status FROM payment_invoices WHERE invoice_id = ?;", (invoice_id,))
        row = await cur.fetchone()
        if not row:
            return False, 0, 0, 0, "Tagihan tidak ditemukan."
        uid, amt_idr, coins_add, st = int(row[0]), int(row[1]), int(row[2]), str(row[3])
        if st == "PAID":
            return False, uid, 0, 0, "Tagihan ini sudah pernah diverifikasi."
        await conn.execute("UPDATE payment_invoices SET status = 'PAID' WHERE invoice_id = ?;", (invoice_id,))
        await conn.execute("UPDATE users SET koin_utama = koin_utama + ?, has_topped_up = 1 WHERE internal_user_id = ?;", (coins_add, uid))
        return True, uid, amt_idr, coins_add, f"+{coins_add} Koin Utama berhasil ditambahkan!"

    ok, uid, amt_idr, coins_add, msg = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    if ok and amt_idr > 0:
        await record_job_and_split_profit(db, revenue_idr=amt_idr, actual_hpp_idr=int(amt_idr * 0.12))
    return ok, uid, amt_idr, coins_add, msg



<!-- [ID:12_FINANCE_S003] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
## Halaman 378

           created_at INTEGER NOT NULL
       );
       CREATE TABLE IF NOT EXISTS payment_invoices (
           invoice_id TEXT PRIMARY KEY,
           user_id INTEGER NOT NULL,
           amount_idr INTEGER NOT NULL,
           coins_credited INTEGER NOT NULL DEFAULT 65,
           provider TEXT NOT NULL,
           tier_key TEXT DEFAULT 'HEMAT',
           followup_sent INTEGER NOT NULL DEFAULT 0,
           status TEXT NOT NULL DEFAULT 'PENDING',
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
           requires_owner_signup INTEGER NOT NULL DEFAULT 0,
           is_live_verified INTEGER NOT NULL DEFAULT 0,
           expires_at INTEGER NOT NULL
       );
       CREATE TABLE IF NOT EXISTS syndicated_assets (
           asset_id TEXT PRIMARY KEY,
           prompt_signature TEXT NOT NULL,
           engine_name TEXT NOT NULL,
           media_url TEXT NOT NULL,
           telegram_file_id TEXT DEFAULT '',
           times_reused INTEGER NOT NULL DEFAULT 1,
           created_at INTEGER NOT NULL
       );
       CREATE TABLE IF NOT EXISTS pending_human_approvals (
           approval_id TEXT PRIMARY KEY,
           action_type TEXT NOT NULL,



<!-- [ID:12_FINANCE_S004] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
## 14. self payment gateway.md

```md
```yaml
import hmac
import hashlib
import base64
from datetime import datetime, timezone
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

class SnapBIConnector:
    """
    Modul Standar Nasional Open API Pembayaran (SNAP BI).
    Memungkinkan server Anda terkoneksi langsung ke API Bank/Instansi Resmi di Indonesia.
    """
    def __init__(self, client_id: str, client_secret: str, private_key_pem: bytes):
        self.client_id = client_id
        self.client_secret = client_secret
        self.private_key = serialization.load_pem_private_key(private_key_pem, password=None)

    @staticmethod
    def get_iso_timestamp() -> str:
        return datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')

    def generate_asymmetric_signature(self, timestamp: str) -> str:
        """Membuat X-SIGNATURE (RSA-SHA256) untuk meminta Access Token B2B ke Bank."""
        string_to_sign = f"{self.client_id}|{timestamp}".encode("utf-8")
        signature = self.private_key.sign(
            string_to_sign,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode("utf-8")

    def generate_symmetric_signature(
        self, http_method: str, endpoint_url: str, access_token: str, request_body: str, timestamp: str
    ) -> str:
        """Membuat X-SIGNATURE (HMAC-SHA512) untuk transaksi langsung (QRIS MPM / Cek Mutasi / VA)."""
        # 1. Minify & SHA-256 hash dari body JSON
        body_hash = hashlib.sha256(request_body.encode("utf-8")).hexdigest().lower()
        # 2. Susun StringToSign sesuai regulasi SNAP Bank Indonesia
        string_to_sign = f"{http_method.upper()}:{endpoint_url}:{access_token}:{body_hash}:{timestamp}"
        # 3. Kalkulasi HMAC-SHA512 menggunakan Client Secret instansi
        hmac_obj = hmac.new(
            self.client_secret.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha512
        )
        return base64.b64encode(hmac_obj.digest()).decode("utf-8")
import asyncio
import time
import random
import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Private Payment Gateway & Orchestrator Hub")


<!-- [ID:12_FINANCE_S005] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
async def ensure_user_and_track_identity(
    db: aiosqlite.Connection, user_id: int, username: str, first_name: str = "", lang_code: str = "id"
) -> dict[str, Any]:
    today_epoch = int(time.time()) // 86400
    clean_uname = (username or "Kreator").replace("`", "").replace("*", "").replace("_", "\\_")
    raw_uname = username or "Kreator"
    is_indo = not lang_code or lang_code.lower().startswith(("id", "in", "ms"))
    default_ppp_zone = 3 if is_indo else 1

    async def _tx(conn: aiosqlite.Connection) -> dict[str, Any]:
        cur_check = await conn.execute(
            "SELECT username, personal_memory_notes, active_canvas_content FROM users WHERE internal_user_id = ?;",
            (user_id,),
        )
        existing = await cur_check.fetchone()
        name_changed_msg = ""

        if not existing:
            await conn.execute(
                """
                INSERT INTO users (internal_user_id, username, first_name, language_code, koin_utama, koin_bonus, ppp_zone, quota_day_epoch, created_at)
                VALUES (?, ?, ?, 'id', 0, 4, ?, ?, ?);
                """,
                (user_id, raw_uname, first_name or raw_uname, default_ppp_zone, today_epoch, int(time.time())),
            )
        else:
            old_uname = existing[0]
            if (
                RUNTIME_CONFIG["SUBBOT_SANGMATA_ACTIVE"]
                and old_uname
                and old_uname != raw_uname
                and raw_uname != "Kreator"
            ):
                await conn.execute(
                    "INSERT INTO identity_history (user_id, old_username, new_username, changed_at) VALUES (?, ?, ?, ?);",
                    (user_id, old_uname, raw_uname, int(time.time())),
                )
                await conn.execute("UPDATE users SET username = ? WHERE internal_user_id = ?;", (raw_uname, user_id))
                name_changed_msg = f"@{old_uname} -> @{raw_uname}"

        await conn.execute(
            """
            UPDATE users
            SET chat_used_today = CASE WHEN quota_day_epoch < ? THEN 0 ELSE chat_used_today END,
                free_img_used_today = CASE WHEN quota_day_epoch < ? THEN 0 ELSE free_img_used_today END,
                quota_day_epoch = ?
            WHERE internal_user_id = ? AND quota_day_epoch < ?;
            """,
            (today_epoch, today_epoch, today_epoch, user_id, today_epoch),
        )
        cur = await conn.execute(
            "SELECT koin_utama, koin_bonus, has_topped_up, ppp_zone, chat_used_today, free_img_used_today, last_claim_date, personal_memory_notes, active_canvas_content FROM users WHERE internal_user_id = ?;",
            (user_id,),
        )
        row = await cur.fetchone()
        return {
            "koin_utama": int(row[0]),
            "koin_bonus": int(row[1]),
            "has_topped_up": bool(row[2]),
            "ppp_zone": int(row[3]),
            "chat_used_today": int(row[4]),
            "free_img_used_today": int(row[5]),
            "last_claim_date": row[6] or "",
            "memory": row[7] or "",
            "canvas": row[8] or "",
            "identity_alert": name_changed_msg,
            "safe_uname": clean_uname,
        }

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def record_job_and_split_profit(
    db: aiosqlite.Connection, revenue_idr: int, actual_hpp_idr: int, buffer_ratio: float = 0.10
) -> dict[str, int]:
    if RUNTIME_CONFIG.get("BANSOS_OPERATION_MODE") == "SILENT_PROFIT":
        actual_hpp_idr = 0
    required_working_capital = int(math.ceil(actual_hpp_idr * (1.0 + buffer_ratio)))
    net_harvestable_profit = max(0, revenue_idr - required_working_capital)

    async def _tx(conn: aiosqlite.Connection) -> int:
        now_ts = int(time.time())
        await conn.execute("INSERT OR IGNORE INTO treasury_summary VALUES (1, 0, 0, 0, 0, 0, ?);", (now_ts,))
        cur = await conn.execute(
            """
            UPDATE treasury_summary
            SET gross_revenue_idr = gross_revenue_idr + ?,
                working_capital_vault_idr = working_capital_vault_idr + ?,
                harvestable_profit_vault_idr = MAX(0, harvestable_profit_vault_idr + ?),
                total_jobs_completed = total_jobs_completed + 1,
                updated_at = ?
            WHERE id = 1
            RETURNING total_jobs_completed;
            """,
            (revenue_idr, required_working_capital, net_harvestable_profit, now_ts),
        )
        row = await cur.fetchone()
        return int(row[0]) if row else 1

    jobs_done = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    return {
        "working_capital_locked_idr": required_working_capital,
        "net_profit_ready_to_harvest_idr": net_harvestable_profit,
        "fomo_counter": RUNTIME_CONFIG["FOMO_COUNTER_BASE"] + jobs_done,
    }


async def execute_manual_profit_harvest(db: aiosqlite.Connection) -> tuple[bool, int, int]:
    async def _tx(conn: aiosqlite.Connection) -> tuple[bool, int, int]:
        now_ts = int(time.time())
        await conn.execute("INSERT OR IGNORE INTO treasury_summary VALUES (1, 0, 0, 0, 0, 0, ?);", (now_ts,))
        cur = await conn.execute(
            "SELECT harvestable_profit_vault_idr, total_harvested_by_owner_idr FROM treasury_summary WHERE id = 1;"
        )
        row = await cur.fetchone()
        if not row or int(row[0]) <= 0:
            return False, 0, int(row[1]) if row else 0
        avail = int(row[0])
        new_total = int(row[1]) + avail
        await conn.execute(
            "UPDATE treasury_summary SET harvestable_profit_vault_idr = 0, total_harvested_by_owner_idr = ?, updated_at = ? WHERE id = 1;",
            (new_total, now_ts),
        )
        return True, avail, new_total

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)



<!-- [ID:12_FINANCE_S006] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
async def ensure_user_and_track_identity(
    db: aiosqlite.Connection,
    user_id: int,
    username: str,
    first_name: str = "",
    lang_code: str = "id",
) -> dict[str, Any]:
    today_epoch = int(time.time()) // 86400
    clean_uname = username or "Kreator"
    is_indo = not lang_code or lang_code.lower().startswith(("id", "in", "ms"))
    default_ppp_zone = 3 if is_indo else 1

    async def _tx(conn: aiosqlite.Connection) -> dict[str, Any]:
        cur_check = await conn.execute(
            "SELECT username, personal_memory_notes, active_canvas_content FROM users WHERE internal_user_id = ?;",
            (user_id,),
        )
        existing = await cur_check.fetchone()
        name_changed_msg = ""

        if not existing:
            await conn.execute(
                """
                INSERT INTO users (internal_user_id, username, first_name, language_code, koin_utama, koin_bonus, ppp_zone, quota_day_epoch, created_at)
                VALUES (?, ?, ?, 'id', 0, 4, ?, ?, ?);
                """,
                (user_id, clean_uname, first_name or clean_uname, default_ppp_zone, today_epoch, int(time.time())),
            )
        else:
            old_uname = existing[0]
            if (
                RUNTIME_CONFIG["SUBBOT_SANGMATA_ACTIVE"]
                and old_uname
                and old_uname != clean_uname
                and clean_uname != "Kreator"
            ):
                await conn.execute(
                    "INSERT INTO identity_history (user_id, old_username, new_username, changed_at) VALUES (?, ?, ?, ?);",
                    (user_id, old_uname, clean_uname, int(time.time())),
                )
                await conn.execute("UPDATE users SET username = ? WHERE internal_user_id = ?;", (clean_uname, user_id))
                name_changed_msg = f"@{old_uname} -> @{clean_uname}"

        await conn.execute(
            """
            UPDATE users
            SET chat_used_today = CASE WHEN quota_day_epoch < ? THEN 0 ELSE chat_used_today END,
                free_img_used_today = CASE WHEN quota_day_epoch < ? THEN 0 ELSE free_img_used_today END,
                quota_day_epoch = ?
            WHERE internal_user_id = ? AND quota_day_epoch < ?;
            """,
            (today_epoch, today_epoch, today_epoch, user_id, today_epoch),
        )
        cur = await conn.execute(
            "SELECT koin_utama, koin_bonus, has_topped_up, ppp_zone, chat_used_today, free_img_used_today, last_claim_date, personal_memory_notes, active_canvas_content FROM users WHERE internal_user_id = ?;",
            (user_id,),
        )
        row = await cur.fetchone()
        return {
            "koin_utama": int(row[0]),
            "koin_bonus": int(row[1]),
            "has_topped_up": bool(row[2]),
            "ppp_zone": int(row[3]),
            "chat_used_today": int(row[4]),
            "free_img_used_today": int(row[5]),
            "last_claim_date": row[6] or "",
            "memory": row[7] or "",
            "canvas": row[8] or "",
            "identity_alert": name_changed_msg,
        }

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def record_job_and_split_profit(
    db: aiosqlite.Connection, revenue_idr: int, actual_hpp_idr: int, buffer_ratio: float = 0.10
) -> dict[str, int]:
    required_working_capital = int(math.ceil(actual_hpp_idr * (1.0 + buffer_ratio)))
    net_harvestable_profit = revenue_idr - required_working_capital

    async def _tx(conn: aiosqlite.Connection) -> int:
        now_ts = int(time.time())
        await conn.execute("INSERT OR IGNORE INTO treasury_summary VALUES (1, 0, 0, 0, 0, 0, ?);", (now_ts,))
        cur = await conn.execute(
            """
            UPDATE treasury_summary
            SET gross_revenue_idr = gross_revenue_idr + ?,
                working_capital_vault_idr = working_capital_vault_idr + ?,
                harvestable_profit_vault_idr = MAX(0, harvestable_profit_vault_idr + ?),
                total_jobs_completed = total_jobs_completed + 1,
                updated_at = ?
            WHERE id = 1
            RETURNING total_jobs_completed;
            """,
            (revenue_idr, required_working_capital, net_harvestable_profit, now_ts),
        )
        row = await cur.fetchone()
        return int(row[0]) if row else 1

    jobs_done = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    return {
        "working_capital_locked_idr": required_working_capital,
        "net_profit_ready_to_harvest_idr": max(0, net_harvestable_profit),
        "fomo_counter": RUNTIME_CONFIG["FOMO_COUNTER_BASE"] + jobs_done,
    }


async def execute_manual_profit_harvest(db: aiosqlite.Connection) -> tuple[bool, int, int]:
    async def _tx(conn: aiosqlite.Connection) -> tuple[bool, int, int]:
        now_ts = int(time.time())
        await conn.execute("INSERT OR IGNORE INTO treasury_summary VALUES (1, 0, 0, 0, 0, 0, ?);", (now_ts,))
        cur = await conn.execute(
            "SELECT harvestable_profit_vault_idr, total_harvested_by_owner_idr FROM treasury_summary WHERE id = 1;"
        )
        row = await cur.fetchone()
        if not row or int(row[0]) <= 0:
            return False, 0, int(row[1]) if row else 0
        avail = int(row[0])
        new_total = int(row[1]) + avail
        await conn.execute(
            "UPDATE treasury_summary SET harvestable_profit_vault_idr = 0, total_harvested_by_owner_idr = ?, updated_at = ? WHERE id = 1;",
            (new_total, now_ts),
        )
        return True, avail, new_total

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)



<!-- [ID:12_FINANCE_S007] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: INV_ID -->
# Masukkan fungsi pengubah QRIS Statis ke Dinamis yang sudah Anda punya di sini:
def ubah_qris_statis_ke_dinamis(nominal_akhir: int) -> str:
    # Panggil fungsi QRIS Statis-to-Dinamis yang sudah ada di sistem Anda
    return f"000201010212...NOMINAL_{nominal_akhir}...6304ABCD"

@app.post("/v1/checkout/create")
async def create_checkout(req: OrderRequest):
    """Endpoint tunggal yang dipanggil oleh Bot Tele, Bot WA, Mini App, FB, atau Web."""
    now = int(time.time())
    used_amounts = {
        tx["final_amount"] for tx in TRANSACTIONS.values()
        if tx["status"] == "PENDING" and tx["expires_at"] > now
    }

    # Buat angka unik 1 - 399 agar tidak bentrok antar pembeli di semua platform
    unique_code = next(c for c in random.sample(range(1, 400), 399) if (req.amount + c) not in used_amounts)
    final_amount = req.amount + unique_code
    qris_payload = ubah_qris_statis_ke_dinamis(final_amount)

    inv_id = f"PG-{now}-{random.randint(100,999)}"
    TRANSACTIONS[inv_id] = {
        "invoice_id": inv_id,
        "external_id": req.external_id,
        
Alasan utama banyak developer dan pebisnis digital di Indonesia beralih membangun Self Payment Gateway seperti yang ditawarkan pada pesan "Wts source code self payment gateway" adalah kedaulatan dana (Zero Third-Party Hold).
Pada payment gateway pihak ketiga, uang pembeli mampir dulu ke rekening penampung milik PG (rawan hold sepihak, pembekuan akun, biaya potongan per transaksi, hingga risiko PG kabur/scam). Sebaliknya, pada sistem Self Payment Gateway 100% pure code, uang dari pembeli langsung masuk detik itu juga ke rekening bank atau saldo merchant milik Anda sendiri, sementara source code di server Anda hanya bertugas sebagai pengatur nominal dan verifikator mutasi otomatis.
Berikut adalah bedah tuntas arsitektur di balik sistem tersebut dan source code intinya agar Anda bisa membangunnya sendiri dari nol.
1. Arsitektur Inti: Bagaimana Cara Kerjanya Tanpa Alat Tambahan?
Sistem ini hanya membutuhkan 1 VPS/Server dan bekerja melalui 3 Modul Utama yang berjalan di belakang layar:
Modul A: Dynamic Invoice & Unique Code Generator
Saat pembeli melakukan checkout (misal harga barang Rp 50.000), server Anda tidak boleh meminta pembayaran pas Rp 50.000 jika ada banyak pembeli bersamaan.
 * Server membuat angka unik acak (misal +142), sehingga tagihan terkunci di angka Rp 50.142.
 * Jika pembeli memilih Transfer Bank (BCA/Mandiri/BRI/BNI/Jago/SeaBank), sistem menampilkan nomor rekening Anda dengan nominal harus persis Rp 50.142.
 * Jika pembeli memilih QRIS (Support Semua E-Wallet & Bank), sistem mengambil teks QRIS Statis Anda, lalu menyuntikkan angka 50142 ke dalam struktur tag EMVCo secara on-the-fly sehingga ketika pembeli men-scan QR tersebut di GoPay/DANA/OVO/BCA Mobile, nominal Rp 50.142 langsung muncul otomatis dan tidak bisa diubah pembeli.
Modul B: Headless Mutation Engine (Pendeteksi Uang Masuk di Server)
Bagaimana server tahu uang Rp 50.142 sudah masuk ke rekening Anda tanpa bantuan HP sama sekali? Ada 2 metode pure code yang dipakai:
 * Metode Universal (Email Push / IMAP Stream — Support Semua Bank & Anti-Banned):
   * Hampir seluruh bank dan merchant modern di Indonesia (BCA, Livin' by Mandiri, BRImo, BNI Wondr, Bank Jago, SeaBank, GoPay Merchant, DANA Bisnis) mengirimkan notifikasi email otomatis tepat pada detik uang masuk.
   * Script di server Anda terhubung langsung ke protokol IMAP email Anda menggunakan App Password. Begitu ada transfer atau scan QRIS masuk, server menangkap email dari domain resmi bank dalam hitungan 1–2 detik, mengekstrak nominalnya dengan Regex, dan mencocokkannya dengan database tagihan.
   * Kelebihan: Bisa dipakai untuk bank/QRIS apa saja, 100% legal, akun bank tidak akan pernah terblokir karena tidak menyuntik aplikasi perbankan, dan tidak pernah logout sendiri.
 * Metode Direct API Session (Login 1x Simpan Token di Server):
   * Untuk akun yang memiliki portal JSON/Web API (seperti dashboard GoBiz/GoPay Merchant, OrderKuota, atau I-Banking Korporasi), pembeli cukup login 1x (memasukkan OTP lewat terminal/panel web di servernya).
   * Script akan menyimpan refresh_token / session_cookie di dalam server dan memperbaruinya secara otomatis (auto-refresh) setiap beberapa menit agar sesi tidak pernah mati, sambil mengecek endpoint mutasi secara berkala.
Modul C: Auto-Match & Webhook Dispatcher
Begitu Modul B mendeteksi dana masuk sebesar Rp 50.142:
 * Server mencari di database siapa yang memiliki tagihan PENDING dengan nominal 50142 dalam rentang waktu aktif (misal 15 menit terakhir).
 * Status tagihan langsung diubah menjadi PAID, dan server menembakkan webhook ke website/bot Anda untuk menyerahkan produk secara otomatis.
2. Blueprint Source Code Lengkap (Python) — Buat Sendiri Sekarang
Anda bisa langsung menggabungkan 3 komponen kode di bawah ini di server Anda menggunakan Python 3.
Komponen 1: Generator QRIS Statis ke Dinamis (qris_engine.py)
Kode ini menggunakan TLV (Tag-Length-Value) Parser sesuai standar resmi EMVCo. Anda cukup menaruh 1 teks QRIS Statis milik Anda, dan fungsi ini akan mengubahnya menjadi QRIS Dinamis dengan nominal terkunci berapa pun yang Anda inginkan.
def calculate_crc16(data: str) -> str:
    """Menghitung ulang Checksum CRC16-CCITT (0xFFFF, Poly 0x1021) standar EMVCo QRIS."""
    crc = 0xFFFF
    for char in data:
        crc ^= ord(char) << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"

def parse_emvco_tlv(qris_str: str) -> list:
    """Membedah struktur Tag-Length-Value (TLV) dari string QRIS."""
    i = 0
    tlv_list = []
    while i < len(qris_str):
        tag = qris_str[i:i+2]
        length = int(qris_str[i+2:i+4])
        value = qris_str[i+4:i+4+length]
        tlv_list.append((tag, value))
        i += 4 + length
        if tag == "63":  # Tag 63 adalah CRC (selalu di akhir)
            break
    return tlv_list

def generate_dynamic_qris(static_qris: str, amount: int) -> str:
    """Mengubah QRIS Statis apa pun menjadi QRIS Dinamis dengan nominal terkunci."""
    tlv_items = parse_emvco_tlv(static_qris.strip())
    new_tlv = []
    amount_str = str(int(amount))
    amount_injected = False

    for tag, value in tlv_items:
        if tag == "01":
            # Ubah Point of Initiation Method dari '11' (Statis) ke '12' (Dinamis)
            new_tlv.append(("01", "12"))
        elif tag in ("54", "63"):
            # Lewati tag nominal lama (jika ada) dan tag CRC lama
            continue
        elif tag == "58" and not amount_injected:
            # Sisipkan Tag 54 (Transaction Amount) tepat sebelum Tag 58 (Country Code ID)
            new_tlv.append(("54", amount_str))
            new_tlv.append((tag, value))
            amount_injected = True
        else:
            new_tlv.append((tag, value))

    # Rakit kembali string EMVCo
    rebuilt_str = "".join(f"{t}{len(v):02d}{v}" for t, v in new_tlv)
    rebuilt_str += "6304"  # Tambahkan header Tag CRC
    
    # Hitung ulang checksum CRC16 dan gabungkan
    crc_hex = calculate_crc16(rebuilt_str)
    return rebuilt_str + crc_hex

> Cara mendapatkan teks static_qris Anda: Upload gambar QRIS cetak Anda ke situs pembaca barcode (seperti zxing org atau qrscanner), lalu copy teks panjang yang diawali dengan 000201010211....
> 
Komponen 2: Mesin Pendeteksi Mutasi Tanpa HP (mutation_engine.py)
Kode ini berjalan di server untuk membaca notifikasi dana masuk secara otomatis dari berbagai bank/merchant di Indonesia dan mencocokkannya ke nominal tagihan:
import imaplib
import email
import re
from html import unescape


<!-- [ID:12_FINANCE_S008] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
STRIPE_COUNT = 4096
USER_LOCK_STRIPES = [asyncio.Lock() for _ in range(STRIPE_COUNT)]


def get_user_lock(user_id: int) -> asyncio.Lock:
    return USER_LOCK_STRIPES[user_id % STRIPE_COUNT]


class SingleWriterSQLiteDaemon:
    def __init__(self, checkpoint_every_n_writes: int = 500):
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

