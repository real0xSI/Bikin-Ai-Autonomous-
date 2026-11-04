
<!-- [ID:13_DATA_SCHEMA_S021] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: ORDER_ID, PAID -->
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
import imaplib
import email
import re
from html import unescape


<!-- [ID:13_DATA_SCHEMA_S022] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: PROV_NAME, PROVIDER_NAME -->
## Halaman 380

   await db.commit()
   cur = await db.execute(
       "SELECT setting_key, setting_val FROM system_settings;"
   )
   for k, v in await cur.fetchall():
       if k == "MINIAPP_URL" and v.startswith("https://"):
           RUNTIME_CONFIG["MINIAPP_URL"] = v
       elif k == "OWNER_ID_RUNTIME" and v.isdigit() and int(v) > 0:
           RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = int(v)
       elif k == "PILIHAN_MESIN_MEDIA" and v.isdigit():
           RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] = int(v)
       elif k in (
           "LAUNCH_PRODUCTION_MODE",
           "HAPPY_HOUR_MODE",
           "AUTO_APPROVE_SANDBOX_TOPUP",
       ):
           RUNTIME_CONFIG[k] = v == "1"
       elif k in (
           "ID_ACTIVE_CATEGORY",
           "ID_ACTIVE_PROVIDER",
           "GLOBAL_ACTIVE_PROVIDER",
           "BANSOS_OPERATION_MODE",
           "PRIMARY_ROLLING_AGENT",
           "ROUTER_COMBO_STRATEGY",
           "WEB_BRAND_NAME",
           "CUSTOM_WEB_DOMAIN",
       ):
           RUNTIME_CONFIG[k] = v
       elif k.startswith("QRIS_SLOT_"):
           try:
               slot_data = json.loads(v)
               prov_name = k.replace("QRIS_SLOT_", "")
               if prov_name in QRIS_BARCODE_SLOTS:
                   QRIS_BARCODE_SLOTS[prov_name].update(slot_data)
           except Exception:
               pass
async def save_persistent_setting(
   db: aiosqlite.Connection, key: str, val: str
) -> None:
   async def _tx(conn: aiosqlite.Connection) -> None:
       await conn.execute(
           "INSERT OR REPLACE INTO system_settings (setting_key, setting_val) VALUES (?, ?);",
           (key, str(val)),
       )
   await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
async def save_qris_barcode_slot(
   db: aiosqlite.Connection,
   provider_name: str,
   file_id: str = "",
   raw_payload: str = "",
) -> None:
   """Menyimpan gambar barcode QRIS dan/atau string EMVCo per provider (GoPay/ShopeePay/DANA)."""
   if provider_name not in QRIS_BARCODE_SLOTS:
       QRIS_BARCODE_SLOTS[provider_name] = {"file_id": "", "raw_payload": ""}
   if file_id:
       QRIS_BARCODE_SLOTS[provider_name]["file_id"] = file_id
   if raw_payload:
       QRIS_BARCODE_SLOTS[provider_name]["raw_payload"] = raw_payload
   await save_persistent_setting(
       db,
       f"QRIS_SLOT_{provider_name}",
       json.dumps(QRIS_BARCODE_SLOTS[provider_name]),
   )
async def set_topic_binding(
   db: aiosqlite.Connection,
   key: str,



<!-- [ID:13_DATA_SCHEMA_S023] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :80 -->
## Halaman 433

           text, parse_mode="Markdown", reply_markup=reply_markup
       )
   except Exception:
       try:
           await message.edit_text(
               text, parse_mode=None, reply_markup=reply_markup
           )
       except Exception:
           pass
async def animate_render_progress_status(
   bot: Bot, chat_id: int, status_msg: Message, job_id: str, engine_label: str
) -> None:
   """
   [SOLUSI POIN ARCH #10]:
   Menampilkan animasi progres nyata (25% -> 65% -> 90%) + indikator aksi Telegram
   agar pengguna tahu sistem sedang bekerja normal dan tidak mengira error.
   """
   try:
       await bot.send_chat_action(chat_id=chat_id, action="upload_photo")
       await safe_edit_markdown(
           status_msg,
           f"⏳ **[25%] MENYIAPKAN KLASTER GPU...**\n"
           f"┣ 🆔 **Pesanan:** `{job_id}`\n"
           f"┣ ⚡ **Mesin AI:** `{engine_label}`\n"
           f"┗ `███░░░░░░░` _Mengalokasikan node inferensi..._",
       )
       await asyncio.sleep(0.6)
       await safe_edit_markdown(
           status_msg,
           f"⚡ **[70%] SEDANG MERENDER KARYA 4K...**\n"
           f"┣ 🆔 **Pesanan:** `{job_id}`\n"
           f"┣ ⚡ **Mesin AI:** `{engine_label}`\n"
           f"┗ `███████░░░` _Menajamkan detail & pencahayaan..._",
       )
   except Exception:
       pass
async def increment_user_usage_counter(
   db: aiosqlite.Connection, user_id: int, is_render: bool = False
) -> None:
   col = "free_img_used_today" if is_render else "chat_used_today"
   async def _tx(conn: aiosqlite.Connection) -> None:
       await conn.execute(
           f"UPDATE users SET {col} = {col} + 1 WHERE internal_user_id = ?;",
           (user_id,),
       )
   await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
async def update_personal_memory_if_needed(
   db: aiosqlite.Connection, user_id: int, text: str, current_mem: str
) -> str:
   low = text.lower()
   new_fact = (
       text[:80]
       if any(
           k in low
           for k in (
               "nama saya ",
               "panggil saya ",
               "usaha saya ",
               "jualan ",
               "bisnis saya ",
           )
       )
       else ""
   )



<!-- [ID:13_DATA_SCHEMA_S024] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :400, :200 -->
## Halaman 434

   if new_fact and new_fact not in current_mem:
       updated = (f"{current_mem} | {new_fact}").strip(" |")[:400]
       async def _upd(conn: aiosqlite.Connection) -> None:
           await conn.execute(
               "UPDATE users SET personal_memory_notes = ? WHERE internal_user_id = ?;",
               (updated, user_id),
           )
       await DB_WRITER_DAEMON.execute_write_tx(db, _upd)
       return updated
   return current_mem
async def deduct_user_coins_for_job(
   db: aiosqlite.Connection,
   user_id: int,
   cost: int,
   allow_bonus: bool,
   prompt_text: str,
   engine_used: str,
) -> tuple[bool, str, str, int]:
   """
   Memotong koin secara atomik & mengembalikan jumlah Koin Utama yang terpakai (deducted_utama).
   Jika pengguna memiliki Koin Utama dan cukup untuk membayar job, sistem memprioritaskan
   pemotongan Koin Utama agar hasil karya pengguna langsung 100% BEBAS WATERMARK!
   """
   job_id = f"JOB-{user_id}-{int(time.time() * 1000)}"
   if cost <= 0 or RUNTIME_CONFIG["HAPPY_HOUR_MODE"]:
       async def _free_tx(conn: aiosqlite.Connection) -> None:
           await conn.execute(
               "INSERT INTO jobs (job_id, internal_user_id, cost, deducted_bonus, deducted_utama, status, pro
               (
                   job_id,
                   user_id,
                   prompt_text[:200],
                   engine_used,
                   int(time.time()),
               ),
           )
       await DB_WRITER_DAEMON.execute_write_tx(db, _free_tx)
       return True, job_id, "Promo Gratis (0 Koin • Ber-Watermark)", 0
   async with get_user_lock(user_id):
       async def _tx(conn: aiosqlite.Connection) -> tuple[bool, str, int]:
           cur = await conn.execute(
               "SELECT koin_utama, koin_bonus, subscription_until FROM users WHERE internal_user_id = ?;",
               (user_id,),
           )
           row = await cur.fetchone()
           if not row:
               return (
                   False,
                   "Akun belum terdaftar. Ketik /start terlebih dahulu.",
                   0,
               )
           utama, bonus, sub_until = (
               int(row[0]),
               int(row[1]),
               int(row[2] or 0),
           )
           has_sub = sub_until > int(time.time())
           if allow_bonus:
               if utama + bonus < cost:
                   return (
                       False,
                       f"Saldo koin belum cukup (Butuh {cost} Koin, Saldo: {utama} Utama + {bonus} Bonus). Te
                       0,
                   )
               # Prioritaskan Koin Utama jika cukup agar pengguna berbayar langsung mendapat hasil Free Water



<!-- [ID:13_DATA_SCHEMA_S025] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
async def ensure_user_and_track_identity(db: aiosqlite.Connection, user_id: int, username: str, first_name: st
   today_epoch = int(time.time()) // 86400
   clean_uname = (username or "Kreator").replace("`", "").replace("*", "").replace("_", "\\_")
   is_indo = not lang_code or lang_code.lower().startswith(("id", "in", "ms"))
   default_ppp_zone = 4 if is_indo else 1
   async def _tx(conn: aiosqlite.Connection) -> dict[str, Any]:
       cur_check = await conn.execute("SELECT username FROM users WHERE internal_user_id = ?;", (user_id,))
       existing = await cur_check.fetchone()
       if not existing:
           valid_ref = referrer_candidate if (referrer_candidate > 0 and referrer_candidate != user_id) else 
           await conn.execute(
               "INSERT INTO users (internal_user_id, username, first_name, language_code, koin_utama, koin_bo
               (user_id, clean_uname, first_name or clean_uname, "id" if is_indo else "en", default_ppp_zone,
           )
       cur = await conn.execute("SELECT koin_utama, koin_bonus, has_topped_up, ppp_zone, subscription_until F
       row = await cur.fetchone()
       sub_until = int(row[4] or 0)
       return {"koin_utama": int(row[0]), "koin_bonus": int(row[1]), "has_topped_up": bool(row[2]), "ppp_zone
   return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
async def deduct_user_coins_for_job(db: aiosqlite.Connection, user_id: int, cost: int, allow_bonus: bool, prom
   job_id = f"JOB-{user_id}-{int(time.time() * 1000)}"
   if cost <= 0 or RUNTIME_CONFIG["HAPPY_HOUR_MODE"]:
       return True, job_id, "Promo Gratis (0 Koin)", 0
   async with get_user_lock(user_id):
       async def _tx(conn: aiosqlite.Connection) -> tuple[bool, str, int]:
           cur = await conn.execute("SELECT koin_utama, koin_bonus, subscription_until FROM users WHERE inter
           row = await cur.fetchone()
           if not row:
               return False, "Akun belum terdaftar.", 0
           utama, bonus, sub_until = int(row[0]), int(row[1]), int(row[2] or 0)
           has_sub = sub_until > int(time.time())
           if allow_bonus:
               if utama + bonus < cost:
                   return False, f"Saldo tidak cukup (Butuh {cost} Koin). Tersedia Eceran Rp 2.000 (24 Koin B
               if utama >= cost:
                   use_utama, use_bonus = cost, 0
               else:
                   use_bonus = min(bonus, cost)
                   use_utama = cost - use_bonus
           else:



<!-- [ID:13_DATA_SCHEMA_S026] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 449

               if utama < cost:
                   return False, f"Memerlukan {cost} Koin Utama.", 0
               use_bonus, use_utama = 0, cost
           is_wm = 0 if (use_utama > 0 or has_sub) else 1
           await conn.execute("UPDATE users SET koin_utama = koin_utama - ?, koin_bonus = koin_bonus - ? WHER
           await conn.execute("INSERT INTO jobs (job_id, internal_user_id, cost, deducted_bonus, deducted_uta
           return True, "Berhasil dipotong", use_utama
       return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
async def mark_job_completed(db: aiosqlite.Connection, job_id: str, prompt_text: str, engine_name: str, telegr
   async def _tx(conn: aiosqlite.Connection) -> None:
       await conn.execute("UPDATE jobs SET status = 'COMPLETED', is_watermarked = ? WHERE job_id = ?;", (1 if
   await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
async def _background_dead_job_sweeper_loop() -> None:
   while True:
       await asyncio.sleep(30)
       try:
           async with get_db() as db:
               cur = await db.execute("SELECT invoice_id, user_id, tier_key FROM payment_invoices WHERE statu
               for inv_id, u_id, t_key in await cur.fetchall():
                   async def _mark(conn: aiosqlite.Connection, iid=str(inv_id)):
                       await conn.execute("UPDATE payment_invoices SET followup_sent = 1 WHERE invoice_id = ?
                   await DB_WRITER_DAEMON.execute_write_tx(db, _mark)
                   if BOT_INSTANCE_GLOBAL:
                       try:
                           await BOT_INSTANCE_GLOBAL.send_message(
                               chat_id=int(u_id),
                               text=f"👋 **Halo! Saya Siska dari Tim Layanan Kreator `bikinAI`.**\n\nSaya mel
                               parse_mode="Markdown"
                           )
                       except Exception:
                           pass
       except Exception:
           pass

<!-- [ID:13_DATA_SCHEMA_S027] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 569

​
​
class SingleWriterSQLiteDaemon:​
    """​
    Menjamin seluruh transaksi tulis dieksekusi secara 
sekuensial-atomik​
    pada satu koneksi penulis tunggal, serta menjalankan 
auto-maintenance​
    WAL checkpoint & garbage collection phash_audit_log tanpa cron job 
eksternal.​
    """​
​
    def __init__(self, checkpoint_every_n_writes: int = 500):​
        self._write_mutex = asyncio.Lock()​
        self._write_counter = 0​
        self._checkpoint_threshold = checkpoint_every_n_writes​
​
    async def execute_write_tx(​
        self,​
        db: aiosqlite.Connection,​
        tx_coro: Callable[[aiosqlite.Connection], Coroutine[Any, Any, 
Any]],​
    ) -> Any:​
        async with self._write_mutex:​
            try:​
                await db.execute("BEGIN IMMEDIATE;")​
                result = await tx_coro(db)​
                await db.commit()​
            except Exception:​
                await db.rollback()​
                raise​
​
            self._write_counter += 1​
            if self._write_counter >= self._checkpoint_threshold:​
                self._write_counter = 0​
                await self._run_inline_maintenance(db)​
            return result​
​
    async def _run_inline_maintenance(self, db: aiosqlite.Connection) 
-> None:​
        now_ts = int(time.time())​
        try:​
            await db.execute(​
                "DELETE FROM phash_audit_log WHERE expires_at <= ?;", 
(now_ts,)​
            )​
            await db.commit()​
            await db.execute("PRAGMA wal_checkpoint(PASSIVE);")​



<!-- [ID:13_DATA_SCHEMA_S028] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
### Panduan Langkah demi Langkah: Merakit Sistem dari Awal hingga Meluncur
Eksekusi teknis dari peta jalan di atas dibagi ke dalam empat tahapan implementasi kode yang 
menghubungkan brankas kredensial, klaster kontainer backend, mesin kasir berpemutus sirkuit, 
hingga antarmuka website produksi.
#### Tahap 1 (Prioritas Urgent): Standarisasi Brankas Kredensial .env Master v3.0
Tahap pertama pada hari peluncuran adalah menyiapkan satu akun GitHub utama untuk 
autentikasi OAuth satu klik, mengambil tiga token bot dari @BotFather beserta ADMIN_USER_ID 
dari @userinfobot, serta mengumpulkan seluruh kunci API gratis dari penyedia Kelompok A dan B. 
Seluruh kredensial tersebut disatukan ke dalam berkas .env yang wajib dimasukkan ke dalam 
daftar .gitignore sejak detik pertama agar tidak pernah terunggah ke repositori publik dan dipindai 
oleh bot pencuri kunci:
```ini
# 
============================================================================
# MASTER .ENV BLUEPRINT v3.0 (OCTOBER 2026 AUDIT - ZERO-COST & 95% MARGIN)
# 
============================================================================


## Halaman 120

# --- 1. OMNICHANNEL BOT & ADMIN CONTROL ---
TOKEN_BOT_UTAMA="isi_token_bot_1"
TOKEN_BOT_ACTIVITY="isi_token_bot_2"
TOKEN_BOT_CADANGAN="isi_token_bot_3"
ADMIN_USER_ID="isi_angka_id_telegram"
WAHA_LOCAL_URL="http://127.0.0.1:3000"
# --- 2. GATEWAY, SEMANTIC CACHE & ROUTELLM ---
SESSION_SECRET="gunakan_string_acak_64_karakter_heksadesimal"
REDIS_CONN_STRING="redis://default:pass@endpoint.upstash.io:6379"
OMNIROUTE_BASE_URL="http://127.0.0.1:20128/v1"
NEW_API_HORIZON_URL="http://127.0.0.1:3001/v1"
NINEROUTER_BASE_URL="http://127.0.0.1:4001/v1"
ROUTELLM_THRESHOLD="0.11593"
HARD_CAP_COGS_RATIO="0.05"
# --- 3. TIER-1 PERPETUAL FREE CLOUD POOL (100% TANPA KARTU) ---
MISTRAL_API_KEY="isi_kunci_mistral_1b_pool"
GEMINI_API_KEY="isi_kunci_aistudio"
GROQ_API_KEY="isi_kunci_groq"
OPENROUTER_API_KEY="isi_kunci_openrouter"
NVIDIA_NIM_API_KEY="nvapi-..."
CLOUDFLARE_ACCOUNT_ID="isi_id_cf"
CLOUDFLARE_AI_TOKEN="isi_token_cf_workers_ai"
SILICONFLOW_API_KEY="sk-..."
MODELSCOPE_API_KEY="isi_token_modelscope"
OPENCODE_ZEN_KEY="isi_kunci_opencode"
# --- 4. TIER-2 ZERO-AUTH, LOKAL INDONESIA & GONKA NETWORK ---
NGODEAI_BASE_URL="https://llm.ngodeai.net/v1"
NGODEAI_API_KEY="isi_kunci_ngodeai_rp0"
POLLINATIONS_BASE_URL="https://gen.pollinations.ai/v1"


## Halaman 121

KILOCODE_GATEWAY_URL="https://api.kilo.ai/api/gateway"
LLM7_BASE_URL="https://api.llm7.io/v1"
GONKA_PROXY_URL="https://api.proxy.gonka.gg/v1"
GONKA_API_KEY="sk-..."
DAHL_FINGERPRINT_KEY="isi_32_karakter_fingerprint_dahl"
# --- 5. TIER-3 WHOLESALE PAYG (DIKUNCI OLEH 5% MARGIN GUARD) ---
NANOGPT_API_KEY="isi_token_nanogpt"
PAYPERQ_API_KEY="ppq_..."
WAVESPEED_API_KEY="isi_kunci_wavespeed"
FAL_KEY="isi_kunci_fal"
NOVITA_API_KEY="isi_kunci_novita"
# --- 6. DATABASE, OBJECT STORAGE & KASIR OTOMATIS (PAKASIR V2 + USDT) ---
TURSO_DATABASE_URL="libsql://nama-db.turso.io"
TURSO_AUTH_TOKEN="isi_token_turso"
SUPABASE_POSTGRES_DSN="postgresql://postgres:pass@db.supabase.co:5432/postgres"
NEON_SQL_DSN="postgresql://user:pass@ep.region.aws.neon.tech/neondb"
BACKBLAZE_B2_KEY_ID="isi_key_id_b2"
BACKBLAZE_B2_APP_KEY="isi_app_key_b2"
PAKASIR_SLUG="nama-proyek-utama"
PAKASIR_API_KEY="isi_kunci_pakasir_v2"
TRIPAY_API_KEY="isi_kunci_tripay"
DUITKU_API_KEY="isi_kunci_duitku"
CRYPTOBOT_API_TOKEN="isi_token_cryptobot"
```
#### Tahap 2 (Prioritas Main): Instalasi Panel Server Mandiri dan Kontainerisasi Backend
Pada mesin server yang digunakan (baik kontainer gratis Caasify, GitHub Codespaces, maupun 
VPS Oracle Cloud Always Free), instalasi diawali dengan memasang panel kontrol sumber terbuka 
1Panel (https://github.com/1Panel-dev/1Panel) atau Coolify v4.4.6 (https://coolify.io) untuk 
memfasilitasi pemantauan kontainer, pengaturan SSL otomatis, dan pencadangan ke 
penyimpanan objek S3/R2/Backblaze. Selanjutnya, seluruh layanan agregator inti (New-API 



<!-- [ID:13_DATA_SCHEMA_S029] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 381

   chat_id: int,
   topic_id: int,
   title: str = "",
) -> None:
   async def _tx(conn: aiosqlite.Connection) -> None:
       await conn.execute(
           "INSERT OR REPLACE INTO bot_bindings (binding_key, chat_id, topic_id, topic_title) VALUES (?, ?, ?
           (key, chat_id, topic_id, title),
       )
   await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
async def get_topic_binding(
   db: aiosqlite.Connection, key: str
) -> tuple[int, int] | None:
   cur = await db.execute(
       "SELECT chat_id, topic_id FROM bot_bindings WHERE binding_key = ?;",
       (key,),
   )
   row = await cur.fetchone()
   return (int(row[0]), int(row[1])) if row else None
async def get_all_topic_bindings(
   db: aiosqlite.Connection,
) -> dict[str, tuple[int, int, str]]:
   cur = await db.execute(
       "SELECT binding_key, chat_id, topic_id, topic_title FROM bot_bindings;"
   )
   return {
       r[0]: (int(r[1]), int(r[2]), str(r[3] or r[0]))
       for r in await cur.fetchall()
   }

<!-- [ID:13_DATA_SCHEMA_S030] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# Menambal bug ketiadaan pencatatan inkremen token pada 
muse_quota_ledger​
# 
======================================================================
========​
class MuseTokenGovernor:​
    SURFING_CUTOFF_98_PERCENT = 980_000​
​
    @classmethod​
    async def reserve_and_select_route(​
        cls,​
        db: aiosqlite.Connection,​
        is_paid_order: bool,​
        heat_score: int,​
        has_muse_key: bool,​
        estimated_tokens: int = 85,​
    ) -> tuple[str, str]:​
        if heat_score > 25:​
            return "9ROUTER_UNFILTERED", 
"nousresearch/hermes-3-llama-3.1-405b"​
​
        if is_paid_order and has_muse_key:​
​
            async def _reserve_tx(conn: aiosqlite.Connection) -> bool:​
                now_ts = int(time.time())​
                await conn.execute(​
                    """​
                    INSERT OR IGNORE INTO muse_quota_ledger (id, 
total_tokens_used, total_campaigns_planned, active_engine_mode, 
updated_at)​
                    VALUES (1, 0, 0, 'MUSE_PRIMARY', ?);​
                    """,​
                    (now_ts,),​
                )​
                cur = await conn.execute(​
                    """​



<!-- [ID:13_DATA_SCHEMA_S031] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## 4. MinerU_markdown_widget_bbe17bcf-1283-4bc9-ab4d-2faa312f6746_2117077223335690240.md

```md
## Arsitektur "Write-Clean, Deploy-Locked"

Pemisahan kode sumber bersih untuk pengembangan AI otonom dari biner produksi yang terkunci dan siap akuisisi.

### Tahap 1: Iterasi & Penulisan Bersih

Bot AI membaca dan menulis kode murni yang rapi ke Shadow Vault (Private Git) agar AI tidak kehilangan konteks pada update berikutnya.

INSPEKSI KOMPONEN & IZIN AKSES (FINE-GRAINED PAT) Terpilih: 1. Bot AI Otonom

### 1. Bot AI Otonom (Orchestrator)

Menulis fitur baru, membaca konteks kode bersih secara utuh, dan mengatur otomatisasi rilis tanpa terganggu kode yang sudah diacak.

Artefak & Konteks Memori AST Konteks Penuh, Rencana Eksekusi Agent, & Diff Patch Murni

agent_orchestrator.py

Izin Fine-Grained PAT & Token Akses Baca/Tulis ke Shadow Vault & Token Penulis Turso DB

Contents: Read & Write (Shadow)

### 2. Shadow Vault (Private Git)

Menyimpan 100% Clean Source Code, komentar rapi, dan dokumentasi lengkap sebagai sumber kebenaran tunggal (Single Source of Truth).

File & Data Tersimpan Kode Sumber Python/TS Asli, Dokumentasi Arsitektur, & Unit Test

src/core/*.py, docs/ARCHITECTURE.md

Izin Fine-Grained PAT Repositori Privat Terisolasi — Hanya diakses Bot AI & CI Trigger

Actions: Write | Contents: Read/Write

### 3. Turso Database (libSQL Vault)

Menyimpan System Prompts asli, kunci dekripsi tensor (K), dan log sinkronisasi versi di luar repositori Git.

Skema Tabel & Rahasia Tabel System Prompts, Kunci AES-GCM (K), & Riwayat Versi Rilis

system_prompts, encryption_keys

Izin Akses & Keamanan Token JWT libSQL Terbatas (Read-Only saat Runtime Produksi)

TURSO_AUTH_TOKEN (Scoped RW/RO)

### 4. Pipeline Pengunci (Compiler)

Mengubah kode bersih menjadi biner terkompilasi (.so / O-LLVM) dan mengunci bobot tensor secara otomatis sebelum rilis.

Proses Transformasi Build Cython/Nuitka + O-LLVM Control Flow Flattening & Enkripsi Tensor

build_locked.sh → core_engine.so

Izin Fine-Grained PAT Baca dari Shadow Vault, Tulis Biner ke Repo Publik

Shadow: Read | Public Repo: Write

### 5. Repo Publik / Produksi

Berisi kode biner terkunci yang aman dari pencurian atau rekayasa balik (tanpa kode sumber asli maupun prompt rahasia).

Artefak Produksi Publik File Shared Object (.so), Bobot Terenkripsi (.enc), & Wrapper Tipis

dist/core_engine.so, weights.enc

Izin Fine-Grained PAT Hanya menerima Push otomatis dari Pipeline CI/CD Pengunci

Contents: Write (CI Bot Only)

### 6. Paket Akuisisi (Pembeli)

Menerima akses bersih dari Shadow Vault + Export Database Turso saat transaksi jual-beli proyek (Exit/Acquisition).

Isi Paket Serah Terima 100% Clean Git History + Dump SQL Turso (Prompt & Kunci Dekripsi)

shadow_repo.bundle + turso_dump.sql

Protokol Transfer Hak Milik Transfer Kepemilikan Repo Privat & Rotasi Token Master Turso

Repo Transfer + Master DB Handover
```


<!-- [ID:13_DATA_SCHEMA_S032] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## 8. MinerU_markdown_widget_6d3f8eec-e509-4c24-b366-b00d2a2e9133_2117075762807734272.md

```md
# Kapasitas Penyimpanan dan Batas Proyek Hosting & Database Gratis (2026)

Panel 1: Penyedia Hosting Gratis (Berpanel Kontrol & Edge)

Penyedia & Panel

Batas Proyek & Keunggulan Utama

InfinityFree

VistaPanel / cPanel

5 GB

400 DB MySQL, PHP 8.4, 30rb Inodes, Bandwidth Unlimited

Serv00

DevilWEB + Akses SSH

3 GB NVMe

100 Websites, SSH, PHP/Node/Python, MySQL/PgSQL/Mongo

Appwrite Sites

Appwrite Console

2 GB

Maks 2 Proyek, Statis & SSR, Built-in Auth/DB/Functions

Alwaysdata

PaaS Admin + SSH

1 GB SSD

256 MB RAM, Backup 3 Hari, Multi-bahasa & SSH

GitHub Pages

Git / GitHub Actions

1 GB

Khusus Statis, 100 GB Bandwidth/bln, Repo Publik

WebHostMost

DirectAdmin / LiteSpeed

0.125 GB (125 MB NVMe)

1 Domain (+5 Subdomain), Inodes Unlimited, PHP 8.3 & Node.js

Panel 2: Penyedia Database Cloud Gratis

Penyedia & Engine

Kuota Database & Batas Operasi

Turso

Edge SQLite

5 GB

100 Databases, 500 Juta Reads & 10 Juta Writes/bln

Cloudflare D1

Serverless SQL (SQLite)

5 GB

Terintegrasi Workers (100rb req/hari), Tanpa Kartu Kredit

Aiven

PostgreSQL / MySQL

1 GB

1 Dedicated VM (1 CPU, 1 GB RAM), +1 MySQL & +1 Valkey

MongoDB Atlas

NoSQL Document (M0)

0.512 GB (512 MB)

Shared Cluster, ~100 ops/detik, Maks 500 koneksi

Supabase

Relational Postgres

0.5 GB (500 MB)

Maks 2 Proyek Aktif, +1 GB File Storage, 50rb MAU Auth

Neon

Serverless Postgres

0.5 GB / proyek

Hingga 100 Proyek, 100 CU-jam compute/bln, DB Branching

⚠️ Peringatan Pemangkasan Kuota & Syarat Baru Penyedia Lain (2026)

• Render: Bandwidth gratis dipangkas drastis dari 100 GB menjadi 5 GB/bulan (April 2026); layanan tidur setelah 15 menit idle & database Postgres gratis mati otomatis setelah 30 hari.

• Koyeb & PlanetScale: Koyeb menghapus paket Hobby bebas kartu dan mewajibkan Kartu Kredit (hold pra-otorisasi \$29) sejak Februari 2026. Paket gratis PlanetScale telah dihapus sepenuhnya.

Perbandingan kapasitas penyimpanan gratis (dalam GB) pada penyedia hosting berpanel kontrol dan database cloud per Oktober 2026. InfinityFree, Serv00, Cloudflare D1, dan Turso memimpin kapasitas ruang simpan gratis tanpa syarat kartu kredit.
```


<!-- [ID:13_DATA_SCHEMA_S033] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 44

​
async def atomic_escrow_charge(​
    db: aiosqlite.Connection, internal_user_id: int, cost: int, 
job_id: str​
) -> bool:​
    """Menangkal 50 request paralel dalam 1 milidetik tanpa Redis & 
tanpa memory leak."""​
    async with get_user_lock(internal_user_id):​
        cursor = await db.execute(​
            """​
            UPDATE users ​
            SET koin_utama = koin_utama - ? ​
            WHERE internal_user_id = ? AND koin_utama >= ?​
            RETURNING koin_utama;​
            """,​
            (cost, internal_user_id, cost),​
        )​
        row = await cursor.fetchone()​
        if not row:​
            return False​
​
        now_ts = int(time.time())​
        await db.execute(​
            """​
            INSERT INTO jobs (job_id, internal_user_id, cost, status, 
refunded_lock, created_at)​
            VALUES (?, ?, ?, 'PROCESSING', 0, ?)​
            """,​
            (job_id, internal_user_id, cost, now_ts),​
        )​
        await db.execute(​
            """​
            INSERT INTO wallet_ledger (internal_user_id, wallet_type, 
delta_amount, balance_after, tx_type, idempotency_key, created_at)​
            VALUES (?, 'UTAMA', ?, ?, 'ESCROW_HOLD', ?, ?)​
            """,​
            (internal_user_id, -cost, row[0], f"escrow_{job_id}", 
now_ts),​
        )​
        await db.commit()​
        return True​
​
async def claim_daily_bonus_safe(​
    db: aiosqlite.Connection, internal_user_id: int, device_fp_hash: 
str, today_str: str​
) -> tuple[bool, str]:​
    """Mencegah Emulator Farm (>2 akun/device) & Hoarding Attack (Max 
Cap 25 Koin)."""​



<!-- [ID:13_DATA_SCHEMA_S034] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: UPDATE -->
# --- SAKLAR WEBHOOK ---
@app.route('/' + TOKEN_UTAMA, methods=['POST'])
def getMessage():
   json_string = request.get_data().decode('utf-8')
   update = telebot.types.Update.de_json(json_string)
   bot.process_new_updates([update])
   return "!", 200
@app.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url=f'https://{USERNAME_PA}.pythonanywhere.com/' + TOKEN_UTAMA)
   return "Server Database BikinAI Aktif 24/7!", 200
3. Klik Save.
4. Buka tab Web (dari tombol menu tiga garis), dan klik tombol hijau Reload bikinaibot.pythonanywhere.com.
5. PythonAnywhere sudah selesai 100%. Anda bisa menutupnya selamanya.
TAHAP 2: Mesin Pekerja Kaggle/Colab (Bebas Banned)
Sekarang buka Kaggle atau Colab Anda. Kode di bawah ini TIDAK menggunakan bot.infinity_polling() sama sekali, melainkan hanya
looping ringan mengambil data dari PythonAnywhere. Kaggle tidak akan menyadarinya.
Paste kode ini lalu tekan Play:
import os
import time
import subprocess
import requests
from deep_translator import GoogleTranslator

<!-- [ID:13_DATA_SCHEMA_S035] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :16 -->
## Halaman 392

   """
   now_ts = int(time.time())
   nonce_hex = secrets.token_hex(8)
   blind_commitment = hashlib.sha256(
       f"{nonce_hex}:{user_id}".encode("utf-8") + VOUCHER_BLIND_SALT
   ).hexdigest()[:16]
   payload_bytes = json.dumps(
       {
           "n": nonce_hex,
           "b": blind_commitment,
           "c": int(compute_units),
           "t": "PRO_COMPUTE",
           "exp": now_ts + ttl_seconds,
       },
       separators=(",", ":"),
   ).encode("utf-8")
   signature = Ed25519PrivateKey.from_private_bytes(ED25519_PRIV_BYTES).sign(
       payload_bytes
   )
   b64_p = (
       base64.urlsafe_b64encode(payload_bytes).decode("ascii").rstrip("=")
   )
   b64_s = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")
   return f"VCH-{b64_p}.{b64_s}"
async def verify_and_redeem_ed25519_voucher(
   db: aiosqlite.Connection, voucher_code: str
) -> tuple[bool, str, int]:
   code = voucher_code.strip()
   if not code.startswith("VCH-") or "." not in code:
       return False, "Format Kode Akses VIP tidak sesuai.", 0
   try:
       b64_p, b64_s = code[4:].split(".", 1)
       payload_bytes = base64.urlsafe_b64decode(
           b64_p + "=" * (-len(b64_p) % 4)
       )
       sig_bytes = base64.urlsafe_b64decode(b64_s + "=" * (-len(b64_s) % 4))
       Ed25519PublicKey.from_public_bytes(ED25519_PUB_BYTES).verify(
           sig_bytes, payload_bytes
       )
       data = json.loads(payload_bytes.decode("utf-8"))
       exp, units = int(data.get("exp", 0)), int(data.get("c", 15))
       if exp <= int(time.time()):
           return False, "Kode Akses VIP sudah melewati masa berlaku.", 0
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
       if not await DB_WRITER_DAEMON.execute_write_tx(db, _tx):
           return (
               False,
               "Kode Akses VIP ini sudah pernah diaktifkan sebelumnya.",
               0,
           )
       return (
           True,
           f"Kode Akses VIP Aktif (+{units} Kredit Studio Bebas Watermark ditambahkan)!",
           units,
       )
   except Exception:
       return False, "Kode Akses VIP tidak dapat diverifikasi.", 0



<!-- [ID:13_DATA_SCHEMA_S036] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
async def ensure_user_and_track_identity(
   db: aiosqlite.Connection,
   user_id: int,
   username: str,
   first_name: str = "",
   lang_code: str = "id",
   referrer_candidate: int = 0,
) -> dict[str, Any]:
   today_epoch = int(time.time()) // 86400
   clean_uname = (
       (username or "Kreator")
       .replace("`", "")
       .replace("*", "")
       .replace("_", "\\_")
   )
   raw_uname = username or "Kreator"
   lang_clean = (lang_code or "id").lower()[:5]
   is_indo = lang_clean.startswith(("id", "in", "ms"))
   default_ppp_zone = 4 if is_indo else 1
   async def _tx(conn: aiosqlite.Connection) -> dict[str, Any]:
       cur_check = await conn.execute(
           "SELECT username FROM users WHERE internal_user_id = ?;",
           (user_id,),
       )
       existing = await cur_check.fetchone()
       name_changed_msg = ""
       if not existing:
           valid_ref = (
               referrer_candidate
               if (referrer_candidate > 0 and referrer_candidate != user_id)
               else 0
           )
           await conn.execute(
               """



<!-- [ID:13_DATA_SCHEMA_S037] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 437

               ):
                   cur_inv = await db.execute(
                       "SELECT invoice_id, user_id, tier_key FROM payment_invoices WHERE status = 'PENDING' A
                       (cs_cutoff_ts,),
                   )
                   for inv_id, u_id, t_key in await cur_inv.fetchall():
                       async def _mark_f(
                           conn: aiosqlite.Connection, iid: str = str(inv_id)
                       ) -> None:
                           await conn.execute(
                               "UPDATE payment_invoices SET followup_sent = 1 WHERE invoice_id = ?;",
                               (iid,),
                           )
                       await DB_WRITER_DAEMON.execute_write_tx(db, _mark_f)
                       try:
                           await BOT_INSTANCE_GLOBAL.send_message(
                               chat_id=int(u_id),
                               text=(
                                   f"👋 **Halo Kak! Saya Siska dari Tim Layanan Kreator `bikinAI`.**\n\n"
                                   f"Saya melihat Kakak baru saja mengecek paket **`{t_key}`** (Tagihan `{inv
                                   f"▸ Untuk memulai dengan sangat hemat, Kakak bisa mencoba **Paket Eceran Rp
                                   f"▸ Kalau Kakak butuh bantuan pembayaran atau ingin rekomendasi paket yang 
                               ),
                               parse_mode="Markdown",
                               reply_markup=InlineKeyboardMarkup(
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(
                                               text="⚡ Ambil Paket Eceran Rp 2.000 (24 Koin)",
                                               callback_data="menu:topup_pkg:ECERAN",
                                           )
                                       ],
                                       [
                                           InlineKeyboardButton(
                                               text="💳 Lihat Semua Pilihan Paket",
                                               callback_data="menu:topup_qris",
                                           )
                                       ],
                                   ]
                               ),
                           )
                       except Exception:
                           pass
       except Exception:
           pass
async def broadcast_to_bound_topic(
   bot: Bot, db: aiosqlite.Connection, binding_key: str, text: str
) -> None:
   if (
       binding_key == "ACTIVITY_TOPIC"
       and not RUNTIME_CONFIG["SUBBOT_NEURAL_FEED_ACTIVE"]
   ):
       return
   bound = await get_topic_binding(db, binding_key)
   if not bound:
       return
   chat_id, topic_id = bound
   try:
       kwargs: dict[str, Any] = {
           "chat_id": chat_id,
           "text": text,
           "parse_mode": "Markdown",
       }
       if topic_id > 0:
           kwargs["message_thread_id"] = topic_id
       await bot.send_message(**kwargs)
   except Exception:
       pass

<!-- [ID:13_DATA_SCHEMA_S038] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# Mengaktifkan penggunaan koin_bonus + koin_utama & one-way refund 
lock​
# 
======================================================================
========​
MAX_KOIN_BONUS_CAP = 25​
​
​
async def atomic_escrow_charge(​
    db: aiosqlite.Connection,​
    internal_user_id: int,​
    cost: int,​
    job_id: str,​
    allow_bonus_wallet: bool = True,​
) -> bool:​
    async with get_user_lock(internal_user_id):​
​
        async def _tx(conn: aiosqlite.Connection) -> bool:​
            now_ts = int(time.time())​
            today_epoch = now_ts // 86400​
​
            await conn.execute(​
                """​
                UPDATE users​
                SET chat_used_today = CASE WHEN quota_day_epoch < ? 
THEN 0 ELSE chat_used_today END,​
                    free_img_used_today = CASE WHEN quota_day_epoch < 
? THEN 0 ELSE free_img_used_today END,​
                    vouchers_minted_today = CASE WHEN quota_day_epoch 
< ? THEN 0 ELSE vouchers_minted_today END,​
                    quota_day_epoch = ?​
                WHERE internal_user_id = ? AND quota_day_epoch < ?;​
                """,​
                (​



<!-- [ID:13_DATA_SCHEMA_S039] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 577

                    INSERT INTO wallet_ledger (internal_user_id, 
wallet_type, delta_amount, balance_after, tx_type, idempotency_key, 
created_at)​
                    VALUES (?, 'BONUS', ?, ?, 'ESCROW_HOLD', ?, ?);​
                    """,​
                    (​
                        internal_user_id,​
                        -deduct_bonus,​
                        new_bonus,​
                        f"escrow_b_{job_id}",​
                        now_ts,​
                    ),​
                )​
            if deduct_utama > 0:​
                await conn.execute(​
                    """​
                    INSERT INTO wallet_ledger (internal_user_id, 
wallet_type, delta_amount, balance_after, tx_type, idempotency_key, 
created_at)​
                    VALUES (?, 'UTAMA', ?, ?, 'ESCROW_HOLD', ?, ?);​
                    """,​
                    (​
                        internal_user_id,​
                        -deduct_utama,​
                        new_utama,​
                        f"escrow_u_{job_id}",​
                        now_ts,​
                    ),​
                )​
            return True​
​
        return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)​
​
​
async def safe_one_time_refund(​
    db: aiosqlite.Connection, job_id: str, internal_user_id: int​
) -> bool:​
    """Mengembalikan saldo secara idempoten dengan pengunci satu-arah 
refunded_lock = 1."""​
    async with get_user_lock(internal_user_id):​
​
        async def _tx(conn: aiosqlite.Connection) -> bool:​
            cursor = await conn.execute(​
                """​
                UPDATE jobs​
                SET status = 'REFUNDED', refunded_lock = 1​
                WHERE job_id = ? AND internal_user_id = ? AND 
refunded_lock = 0 AND status != 'COMPLETED'​



<!-- [ID:13_DATA_SCHEMA_S040] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 579

                ),​
            )​
            return True​
​
        return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)​
​
​
async def claim_daily_bonus_safe(​
    db: aiosqlite.Connection,​
    internal_user_id: int,​
    device_fp_hash: str,​
    today_str: str,​
) -> tuple[bool, str]:​
    async with get_user_lock(internal_user_id):​
​
        async def _tx(conn: aiosqlite.Connection) -> tuple[bool, str]:​
            cursor = await conn.execute(​
                "SELECT COUNT(DISTINCT internal_user_id) FROM 
daily_claims WHERE device_fp = ? AND claim_date = ?;",​
                (device_fp_hash, today_str),​
            )​
            (device_count,) = await cursor.fetchone()​
            if device_count >= 2:​
                return False, "DEVICE_LIMIT_EXCEEDED"​
​
            cursor = await conn.execute(​
                """​
                UPDATE users​
                SET koin_bonus = MIN(koin_bonus + 4, ?), 
last_claim_date = ?​
                WHERE internal_user_id = ? AND (last_claim_date IS 
NULL OR last_claim_date != ?) AND koin_bonus < ?​
                RETURNING koin_bonus;​
                """,​
                (​
                    MAX_KOIN_BONUS_CAP,​
                    today_str,​
                    internal_user_id,​
                    today_str,​
                    MAX_KOIN_BONUS_CAP,​
                ),​
            )​
            row = await cursor.fetchone()​
            if not row:​
                return False, "ALREADY_CLAIMED_OR_CAP_25_REACHED"​
​
            await conn.execute(​
                "INSERT INTO daily_claims (internal_user_id, 


