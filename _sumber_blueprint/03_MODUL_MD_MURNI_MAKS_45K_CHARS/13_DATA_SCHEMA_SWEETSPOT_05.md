
<!-- [ID:13_DATA_SCHEMA_S041] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 643

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



<!-- [ID:13_DATA_SCHEMA_S042] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: USER_ID -->
# 1. PERTAHANAN SEC-02: Zero-RAM Per-User Mutex + Atomic SQLite WAL 
Escrow​
USER_LOCKS = defaultdict(asyncio.Lock)​
​
async def atomic_escrow_charge(db: aiosqlite.Connection, user_id: int, 
cost: int, job_id: str) -> bool:​
    """Menangkal 50 request paralel dalam 1 milidetik tanpa Redis."""​
    async with USER_LOCKS[user_id]:​
        cursor = await db.execute(​
            """​
            UPDATE users ​
            SET koin_utama = koin_utama - ? ​
            WHERE user_id = ? AND koin_utama >= ?​
            RETURNING koin_utama;​
            """,​
            (cost, user_id, cost)​
        )​



<!-- [ID:13_DATA_SCHEMA_S043] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 94

Penyedia Hosting 
Kuota Gratis (Status 
Oktober 2026) 
Dukungan Backend / 
Fungsi 
Batasan Kritis & Aturan 
2026 yang Wajib 
Diketahui 
Unlimited Requests, 
500 builds/bln, 100 
custom domains/proyek 
CPU/req), D1 SQL (5 
GB), R2 Storage (10 
GB), KV (1 GB) 
Mengizinkan proyek 
personal maupun 
komersial kecil secara 
gratis. 
Vercel Hobby 
100 GB transfer/bln, 1 
juta edge requests, 1 
juta function 
invocations, 50 custom 
domains/proyek 
Serverless & Edge 
Functions (Node.js / 
Web API) 
Khusus 
non-komersial, tidak 
mendukung repo milik 
Git Organization, dan 
sejak 16 Sep 2026 
hanya menyimpan 3 
production deploy 
terakhir. 
Appwrite Sites 
2 Proyek, 5 GB 
bandwidth, 2 GB 
storage, 15 menit build 
timeout, custom 
domain + SSL 
Terpadu dengan Auth 
(75rb MAU), 1 
Database, 1 Bucket, 2 
Functions (750rb 
eksekusi) 
Proyek otomatis dijeda 
(paused) setelah 1 
minggu tanpa 
aktivitas. Sangat 
cocok untuk aplikasi 
full-stack terpadu. 
Deno Deploy 
20 Aplikasi, 50 
custom domains, 1 
juta req/bln, 20 GB 
egress, 15 CPU hours, 
350 GB-h memori 
V8 Isolates di 35+ 
region untuk 
TypeScript/JS APIs & 
SSR 
Tidak memiliki sistem 
file tradisional 
(serverless) atau 
koneksi jangka 
panjang. 
GitHub Pages 
1 GB storage/repo, 
100 GB bandwidth/bln, 
10 builds/jam, custom 
domain + HTTPS 
Khusus statis 
(HTML/CSS/JS/Jekyll) 
Repositori wajib Public 
pada akun GitHub 
Free; tidak ditujukan 
untuk menjalankan 
situs bisnis komersial. 
Sevalla (Static) 
100 Situs Statis, 100 
GB bandwidth, 600 
build minutes, 1 GB 
ukuran per situs di 
260+ lokasi edge 
Khusus situs statis (git 
push auto-deploy) 
Hanya hosting statis 
yang gratis; aplikasi 
container dan database 
berbayar mulai $5/bln. 
Render (Hobby) 
750 jam/bln (512 MB 
RAM, 0.1 CPU), 25 
servis, 2 custom 
domains 
Web Services 
(Docker/Node/Python/
Go) & Static 
PERUBAHAN 2026: 
Bandwidth dipangkas 
dari 100 GB menjadi 5 
GB/bln (23 April 2026); 
tidur setelah 15 menit 
idle; Postgres gratis 
dihapus setelah 30 
hari; port SMTP 
diblokir. 
Kategori 3: Database Cloud Gratis Terbaik (Pendamping Hosting 



<!-- [ID:13_DATA_SCHEMA_S044] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 375

                       (now_ts,),
                   )
                   await db.execute(
                       "DELETE FROM omni_resource_registry WHERE expires_at <= ?;",
                       (now_ts,),
                   )
                   await db.commit()
                   await db.execute("PRAGMA wal_checkpoint(PASSIVE);")
               except Exception:
                   pass
           return result
DB_WRITER_DAEMON = SingleWriterSQLiteDaemon()
@asynccontextmanager
async def get_db() -> AsyncIterator[aiosqlite.Connection]:
   """Menggunakan koneksi persisten WAL terkelola tanpa memintal thread baru tiap panggilan."""
   conn = await DB_WRITER_DAEMON.get_shared_connection()
   yield conn

<!-- [ID:13_DATA_SCHEMA_S045] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: :300 -->
## Halaman 387

           except Exception:
               pass
       # Gagal 3x -> Berhenti retry berisiko, catat ke human_escalation_queue & kabari Owner
       AUTONOMIC_GUARD.record_telemetry(component, False)
       inc_id = f"INC-{int(time.time())}-{secrets.token_hex(3).upper()}"
       err_detail = str(error)[:300]
       async def _esc_tx(conn: aiosqlite.Connection) -> None:
           await conn.execute(
               """
               INSERT OR REPLACE INTO human_escalation_queue
               (incident_id, component, error_class, error_detail, attempts, status, created_at)
               VALUES (?, ?, ?, ?, ?, 'OPEN', ?);
               """,
               (
                   inc_id,
                   component,
                   err_class,
                   err_detail,
                   attempts,
                   int(time.time()),
               ),
           )
       await DB_WRITER_DAEMON.execute_write_tx(db, _esc_tx)
       owner_id = int(RUNTIME_CONFIG.get("OWNER_ID_RUNTIME") or 0)
       if owner_id > 0 and BOT_INSTANCE_GLOBAL:
           try:
               await BOT_INSTANCE_GLOBAL.send_message(
                   chat_id=owner_id,
                   text=(
                       f"🚨 **SELF-HEALING ESCALATION (GAGAL 3x BERTURUT-TURUT)**\n"
                       f"┣ 🆔 **Insiden:** `{inc_id}`\n"
                       f"┣ ⚙️ **Komponen:** `{component}`\n"
                       f"┣ 🏷️ **Klasifikasi:** `{err_class}`\n"
                       f"┣ 🛠️ **Handler Dicoba:** `{handler_name}` ({attempts}x)\n"
                       f"┗ 📝 **Detail:** `{err_detail}`\n\n"
                       f"_Retry otomatis dihentikan agar aman. Insiden telah masuk ke Human Queue di `/admin`
                   ),
                   parse_mode="Markdown",
               )
           except Exception:
               pass
       return {
           "healed": False,
           "escalated": True,
           "incident_id": inc_id,
           "component": component,
           "error_class": err_class,
           "handler": handler_name,
           "attempts": attempts,
       }
SELF_HEALING_ORCHESTRATOR = SelfHealingOrchestrator()

<!-- [ID:13_DATA_SCHEMA_S046] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 445

                   await db.commit()
                   await db.execute("PRAGMA wal_checkpoint(PASSIVE);")
               except Exception:
                   pass
           return result
DB_WRITER_DAEMON = SingleWriterSQLiteDaemon()
@asynccontextmanager
async def get_db() -> AsyncIterator[aiosqlite.Connection]:
   conn = await DB_WRITER_DAEMON.get_shared_connection()
   yield conn

<!-- [ID:13_DATA_SCHEMA_S047] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==============================================================================
async def main() -> None:
   global BOT_INSTANCE_GLOBAL, BOT_USERNAME_GLOBAL
   if not BOT_TOKEN:
       print("❌ TOKEN_BOT_UTAMA belum diatur!")
       return
   async with aiosqlite.connect(DB_PATH) as db:
       await init_master_db(db)
   await start_embedded_web_servers(port=8080)
   asyncio.create_task(_background_dead_job_sweeper_loop())
   bot = Bot(token=BOT_TOKEN)
   BOT_INSTANCE_GLOBAL = bot
   me = await bot.get_me()
   BOT_USERNAME_GLOBAL = me.username or "bikinAI_bot"
   dp = Dispatcher()
   print(f"🚀 bikinAI Super Intelligence v4.0.0 (@{BOT_USERNAME_GLOBAL}) SIAP BEROPERASI 100%!")
   await dp.start_polling(bot)
if __name__ == "__main__":
   asyncio.run(main())
KONTRAK OUTPUT — STATE UPDATE (BAGIAN A)
====================================================================

<!-- [ID:13_DATA_SCHEMA_S048] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: STR, CUSTOM_LABEL:SUB, FITUR_X, :3000 -->
# 4. AUTO-DISCOVERY CLASSIFIER & EKSTRAKTOR DNA KODE/GAMBAR​
# 
======================================================================
========​
def classify_with_auto_discovery(title: str, content: str) -> 
tuple[str, list[str]]:​
    """​
    Mendeteksi domain utama DAN menangkap seluruh label kustom/asing 
ke dalam AUTO_DISCOVERY​
    agar tidak ada 1 pun fitur atau teks berlabel aneh yang terlewat.​
    """​
    combined_lower = (title * 3 + "\n" + content).lower()​
    ​
    # 1. Tangkap semua label eksplisit di dalam kurung siku: misal 
[CUSTOM_LABEL:SUB], [FITUR_X], dll.​
    discovered_tags = re.findall(r"\[([A-Za-z0-9_\-\s:]{3,40})\]", 
title + "\n" + content[:3000])​
    clean_tags = list(dict.fromkeys([t.strip().upper() for t in 
discovered_tags if not t.strip().isdigit()]))​
​
    # 2. Cek apakah tag eksplisit cocok dengan salah satu dari 25 
domain​
    for tag in clean_tags:​
        for dom_key in DOMAIN_SCHEMA:​
            short_dom = dom_key.split("_", 1)[1]​
            if short_dom in tag:​
                return dom_key, clean_tags​
​
    # 3. Hitung skor kata kunci terhadap 25 domain​
    scores = {}​
    for dom, kw_list in DOMAIN_SCHEMA.items():​



<!-- [ID:13_DATA_SCHEMA_S049] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: STR, :3000 -->
# 5. KLASIFIKASI AUTO-DISCOVERY & DETEKTOR DUPLIKAT PARSIAL UNTUK 
AUDIT MANUAL​
# 
======================================================================
========​
def classify_and_extract_dna(title: str, content: str) -> tuple[str, 
list[str], dict]:​
    combined = (title * 3 + "\n" + content).lower()​
    raw_tags = re.findall(r"\[([A-Za-z0-9_\-\s:]{3,40})\]", title + 
"\n" + content[:3000])​
    clean_tags = list(dict.fromkeys([t.strip().upper() for t in 
raw_tags if not t.strip().isdigit()]))​
​
    matched_dom = None​
    for tag in clean_tags:​
        for dom_key in DOMAIN_SCHEMA:​



<!-- [ID:13_DATA_SCHEMA_S050] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: :25, A-ZA-Z0-9_, :15, DICT -->
## Halaman 6

            if dom_key.split("_", 1)[1] in tag:​
                matched_dom = dom_key​
                break​
        if matched_dom:​
            break​
​
    if not matched_dom:​
        scores = {d: sum(combined.count(kw) for kw in kws) for d, kws 
in DOMAIN_SCHEMA.items()}​
        scores = {k: v for k, v in scores.items() if v > 0}​
        if scores:​
            matched_dom = max(scores, key=scores.get)​
        elif clean_tags:​
            safe_tag = re.sub(r"[^A-Z0-9_]", "_", clean_tags[0])[:25]​
            matched_dom = f"26_AUTO_DISCOVERY_{safe_tag}"​
        else:​
            matched_dom = "26_AUTO_DISCOVERY_UMUM"​
​
    funcs = 
list(dict.fromkeys(re.findall(r"(?:def|class|function|interface|CREATE 
TABLE)\s+([a-zA-Z0-9_]+)", content)))​
    imgs = re.findall(r"!\[[^\]]*\]
", content)​
([
)] +)
    code_cnt = len(re.findall(r"```", content)) // 2​
    tbl_cnt = len(re.findall(r"^\|.+\|$", content, re.MULTILINE))​
    score = (code_cnt * 15) + (tbl_cnt * 2) + (len(funcs) * 5) + 
(len(imgs) * 8)​
​
    dna = {​
        "score": score,​
        "grade": "BINTANG_5_KODE_UTUH" if score >= 40 else 
("BINTANG_3_TABEL_STRUKTUR" if score >= 10 else 
"BINTANG_1_KONSEP_NARASI"),​
        "symbols": funcs[:15],​
        "images": imgs,​
        "code_blocks": code_cnt,​
        "table_rows": tbl_cnt​
    }​
    return matched_dom, clean_tags, dna​
​
def split_sections_lossless(md_text: str, source_tag: str) -> 
list[dict]:​
    lines = md_text.splitlines(keepends=True)​
    sections, curr_lines = [], []​
    curr_title = "ROOT_INTRODUCTION"​
    in_code = False​
​
    for line in lines:​



<!-- [ID:13_DATA_SCHEMA_S051] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# Database simulasi (Gunakan SQLite/PostgreSQL untuk produksi)
TRANSACTIONS = {}

async def dispatch_omnichannel_notification(invoice: dict):
    """
    Begitu pembayaran terdeteksi LUNAS, fungsi ini otomatis mengabari
    semua platform tempat pembeli bertransaksi (Telegram, WA, FB, atau Web).
    """
    channel = invoice.get("channel")       # 'telegram', 'whatsapp', 'facebook', 'web'
    target_id = invoice.get("customer_id") # Chat ID Tele / Nomor WA / PSID FB
    order_id = invoice["order_id"]
    amount = invoice["final_amount"]

    async with httpx.AsyncClient(timeout=10) as client:
        # 1. Tembak Webhook ke sistem utama Anda (Bot/Web Backend)
        if invoice.get("webhook_url"):
            await client.post(invoice["webhook_url"], json={
                "event": "payment.success",
                "order_id": order_id,
                "amount": amount,
                "channel": channel,
                "customer_id": target_id,
                "timestamp": int(time.time())
            })


<!-- [ID:13_DATA_SCHEMA_S052] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 1

dan Optimasi Efisiensi Biaya (TCO) 
Eliminasi Bottleneck Single-Writer SQLite WAL dan Manajemen 
Memori 
Keputusan cetak biru untuk menggunakan SQLite dalam mode WAL (Write-Ahead Logging) 
pada tahap modal Rp 0 hingga skala menengah sangat tepat karena menghilangkan beban 
memori dari database server eksternal. Namun, keterbatasan paling mendasar dari 
SQLite—bahkan ketika mode WAL telah diaktifkan—adalah batasan penulis tunggal 
(single-writer constraint): hanya satu transaksi tulis (INSERT, UPDATE, DELETE) yang dapat 
di-commit pada satu waktu karena SQLite mengunci seluruh struktur tabel/file saat menulis. 
Ketika ekosistem omnichannel (Telegram, WhatsApp, dan Facebook Messenger) menerima 
lonjakan trafik viral secara serentak—misalnya saat video promosi di Facebook memicu ratusan 
komentar "Mau coba" per menit yang mengaktifkan Auto-Reply Comment, pembuatan profil 
pengguna baru, klaim kredit harian, pemotongan escrow (atomic_escrow_charge), serta polling 
rekonsiliasi Job_ID—puluhan korutin aiosqlite yang memanggil db.commit() secara bersamaan 
akan saling memblokir dan memicu kegagalan sqlite3.OperationalError: database is locked 
(SQLITE_BUSY). 
Untuk mempertahankan biaya infrastruktur Rp 0 sekaligus mengeliminasi kegagalan 
SQLITE_BUSY, lapisan akses SQLite wajib direfaktor melalui pemisahan koneksi baca-tulis dan 
optimasi pragma tingkat kernel. Pertama, saat inisialisasi koneksi aiosqlite, sistem harus 
mengeksekusi serangkaian instruksi PRAGMA journal_mode=WAL; PRAGMA 
synchronous=NORMAL; PRAGMA busy_timeout=10000; PRAGMA temp_store=MEMORY; 
PRAGMA mmap_size=268435456; agar operasi baca/tulis memanfaatkan memory-mapped I/O 
sebesar 256 MB di RAM dan menunggu antrean kunci hingga 10.000 milidetik sebelum 
melempar kesalahan. Kedua, arsitektur koneksi harus dibagi menjadi Read Connection Pool 
(4 koneksi aiosqlite dengan parameter URI ?mode=ro yang melayani AI Support & Triage 
Agent, pengecekan saldo /start, dan pembacaan status secara paralel penuh tanpa hambatan 
kunci) dan Dedicated Single-Writer Coroutine (1 koneksi tulis eksklusif yang menarik mutasi 
transaksi dari asyncio.Queue internal dan melakukan batch commit setiap 10 milidetik). 
Implementasi Semantic Caching & Routing Berbasis Vektor (Valkey / 
RedisVL) 
Dalam operasional harian bikinAI Super Intelligence, pengguna dari segmen UMKM, kreator 
konten, dan afiliasi TikTok sering kali mengirimkan instruksi yang secara semantik identik 
meskipun kalimatnya berbeda—seperti "Buatkan kampanye promo diskon baju lebaran 50%" 
dan "Tolong bikin iklan promo gamis lebaran diskon setengah harga". Pada arsitektur saat ini, 
kedua permintaan tersebut dianggap sebagai kueri baru yang terpisah, sehingga 
masing-masing memicu pemanggilan API melalui 9Router, mengeksekusi penalaran Muse 
Orchestrator, dan menjalankan Prompt Engineer Agent dari awal. Selain itu, fitur Auto-Intent 
Detection pada Bagian 4.1 cetak biru menggunakan LLM di Gatekeeper untuk 
mengklasifikasikan niat pengguna (CHAT, GENERATE_IMAGE, GENERATE_VIDEO, 
ORCHESTRATE_CAMPAIGN, READ_DOCUMENT, IMAGE_TO_VIDEO) dalam waktu ~500 
ms pada setiap pesan masuk. 
Menambahkan lapisan Semantic Caching & Vector Routing menggunakan Valkey (varian 



<!-- [ID:13_DATA_SCHEMA_S053] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 7

Lapisan Arsitektur (Folder / 
Modul) 
File Inti di Dalamnya 
Tanggung Jawab & Prinsip 
Isolasi (Zero-Refactoring 
Guarantee) 
ffmpeg_compiler.py, 
aes_gcm_packager.py 
Reconciliation Polling (5s), 
eksekusi /dev/shm, ekstraksi 
frame PuLID, penggabungan 
audio MMAudio/Kokoro, dan 
enkripsi .bin. 
services/billing/ (Modul 1 & 5: 
payment_and_support.py) 
wallet_repository.py, 
qris_gateway.py, 
stars_crypto.py, 
voucher_crypto.py 
Mengelola Lock Striping, 
transaksi koin_utama & 
koin_bonus, penerbitan 
Ed25519 Compute Voucher, 
komisi afiliasi 2 jalur, serta AI 
Support & Triage Agent. 
edge/cloudflare_worker/ 
(Relay Zero-VPS) 
worker_relay.ts, wrangler.toml Menyedot media dari CDN hulu 
(v3.fal.media, 
replicate.delivery), melucuti 
EXIF secara streaming, 
mengenkripsi ke .bin, dan 
menyimpannya ke R2 dengan 
auto-delete 24 jam. 
Evolusi Database (SQLite WAL ke Turso/libSQL & PostgreSQL) dan 
State Checkpointer 
Untuk menjamin bahwa lapisan penyimpanan data yang saat ini berjalan di atas SQLite WAL 
lokal dapat bertransformasi menuju skala ratusan ribu pengguna global tanpa menulis ulang 
kueri aplikasi, modul config_and_db.py harus dibangun di atas pola Data Repository yang 
kompatibel dengan Turso (libSQL) dan PostgreSQL. Ketika volume transaksi tulis paralel 
melampaui kapasitas satu simpul SQLite WAL, tim pengembang dapat mengalihkan connection 
string ke Turso (libSQL)—sebuah fork open-source dari SQLite yang mempertahankan 
kompatibilitas sintaks SQLite 100% (termasuk klausa UPDATE ... RETURNING), namun telah 
memodifikasi mesin penyimpanan B-tree untuk melakukan deteksi konflik tingkat baris 
(row-level conflict detection) alih-alih mengunci seluruh file database. Arsitektur Concurrent 
Writes pada Turso mencegah transaksi pada baris yang berbeda saling menjegal, 
menghasilkan throughput penulisan paralel hingga 4x lipat lebih tinggi dengan Free Tier yang 
sangat memadai (penyimpanan 5 GB dan 500 juta pembacaan baris per bulan). 
Di samping tabel dasar users dan jobs yang sudah didefinisikan pada Bagian 5.4 cetak biru, 
empat tabel struktural berikut wajib disiapkan di dalam skema inisialisasi database sekarang 
agar fitur omnichannel, buku besar akuntansi anti-sengketa, audit keamanan, dan pemulihan 
status multi-agen pada 50% dokumen selanjutnya dapat langsung berjalan di atas fondasi yang 
kokoh. 
Nama Tabel Fondasi Baru 
Kolom Utama & Kunci Indeks 
Fungsi Arsitektural untuk 50% 
Pengembangan Selanjutnya 
platform_identities 
identity_id (PK), 
internal_user_id (FK), 
platform_type ('tg','wa','fb'), 
external_id (UNIQUE), 
Mewujudkan visi "1 Otak, 3 
Pintu" dengan 
menghubungkan akun 
Telegram, nomor WhatsApp, 



<!-- [ID:13_DATA_SCHEMA_S054] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 42

Signed Capability Voucher: 
import asyncio​
import base64​
import hashlib​
import hmac​
import json​
import time​
import unicodedata​
from collections import OrderedDict​
from urllib.parse import parse_qsl, urlparse​
import aiosqlite​
from cryptography.hazmat.primitives.asymmetric.ed25519 import (​
    Ed25519PrivateKey,​
    Ed25519PublicKey,​
)​
​
# 
=====================================================================​

<!-- [ID:13_DATA_SCHEMA_S055] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 4. STATELESS ED25519 SIGNED CAPABILITY VOUCHER (ZERO-DATABASE LINK)​

<!-- [ID:13_DATA_SCHEMA_S056] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 48

Gelombang Prioritas 
Nama Layanan & 
Tautan Resmi 
Fungsi Utama dalam 
Sistem v2.0 
Biaya 
/cloud/free/](https://ww
w.oracle.com/cloud/free
/) 9. Valkey & RedisVL 
(Semantic Cache & 
Router): 
[https://github.com/redi
s/redis-vl-python](https:
//github.com/redis/redis
-vl-python) 10. Turso 
Cloud (libSQL 
Concurrent Writes 
5GB Gratis): 
[https://turso.tech/](http
s://turso.tech/) 11. 
Pollinations AI 
(Sandbox Media 
Gratis): 
[https://pollinations.ai/](
https://pollinations.ai/) 
12. AWS Builder ID 
(Kiro AI Free di 
9Router): 
[https://profile.aws.ama
zon.com/](https://profile
.aws.amazon.com/) 13. 
NVIDIA NIM (Kredit 
LLM Gratis): 
[https://build.nvidia.com
/](https://build.nvidia.co
m/) 
🔵 GELOMBANG 2 
(Kasir 3-Zona PPP, 
Audio Instan, & API 
Grosir Pay-Per-Use) 
14. Pakasir (Gateway 
QRIS Zona 3): 
[https://pakasir.com/](ht
tps://pakasir.com/) 15. 
Tripay / Duitku 
(Alternatif QRIS): 
[https://tripay.co.id/](htt
ps://tripay.co.id/) / 
[https://www.duitku.com
/](https://www.duitku.co
m/) 16. Fal.ai (API 
Kling, Veo, Wan, 
Seedance, Flux): 
[https://fal.ai/dashboard
/keys](https://fal.ai/dash
Menghidupkan kasir 
3-Zona PPP (QRIS 
Domestik + Telegram 
Stars/Crypto Global) 
dan membuka seluruh 
mesin komersial Tier 
Pro & Tier Ultra pada 
saklar 
PILIHAN_MESIN_MED
IA = 2. 
Deposit sesuai 
pemakaian pembeli 



<!-- [ID:13_DATA_SCHEMA_S057] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 89

Panduan Eksekusi dan Katalog Live 
Pembuatan 3 Website Aktif Gratis (Edisi 
Oktober 2026) 
Berdasarkan pemindaian langsung (live scraping) terhadap ekosistem penyedia infrastruktur 
web per Jumat, 30 Oktober 2026, Anda dapat membangun, mengelola, dan mengaktifkan 3 
website yang sepenuhnya berbeda—lengkap dengan nama domain sendiri, hosting, panel 
kontrol, database, email custom dua arah (terima dan kirim), template CSS modern, form 
backend, analitik, hingga sistem pemantauan uptime—dengan biaya Rp 0 (100% gratis) 
menggunakan modal akun GitHub, Cloudflare, dan email standar (Gmail) yang sudah Anda 
miliki. Apabila Anda menginginkan ekstensi domain resmi Indonesia (.my.id, .biz.id, atau 
.web.id), promo registrar lokal yang aktif hari ini menawarkan harga tebus murah mulai dari Rp 
1.000 hingga Rp 3.000 untuk satu tahun penuh tanpa syarat berlangganan hosting. 
Lanskap free tier global pada tahun 2026 mengalami pergeseran kebijakan yang signifikan dan 
wajib Anda perhitungkan sebelum menulis kode di GitHub Codespaces. Berdasarkan laporan 
industri dan dokumentasi penyedia per pertengahan hingga akhir 2026, sejumlah layanan 
populer di tutorial lama telah memangkas kuotanya secara drastis: Render menurunkan 
bandwidth gratis dari 100 GB menjadi 5 GB/bulan sejak 23 April 2026 dengan database 
PostgreSQL yang kedaluwarsa dalam 30 hari, Koyeb mewajibkan kartu kredit dengan 
penahanan saldo (pre-authorisation hold) sebesar $29 sejak Februari 2026, Netlify 
memberlakukan batas keras 300 kredit/bulan, sementara PlanetScale dan Fly.io telah 
menghapus paket gratis permanen mereka. Sebaliknya, penyedia seperti Cloudflare Pages & 
Workers, Serv00, Alwaysdata, InfinityFree, Turso, dan Supabase tetap menyediakan kuota 
gratis yang besar tanpa syarat kartu kredit. 
Untuk memaksimalkan ketiga website Anda tanpa membebani batas kuota (rate limit) pada satu 
penyedia tunggal, strategi arsitektur yang paling tangguh adalah mendistribusikan beban ke 
kombinasi ekosistem terbaik. Tabel di bawah ini merangkum cetak biru (blueprint) alokasi 
infrastruktur untuk ketiga website Anda yang dapat langsung didaftarkan hari ini sebelum 
membuka GitHub Codespaces. 
Komponen Kebutuhan Website #1: Portofolio / 
Landing / SaaS Statis & 
Edge 
Website #2: Aplikasi 
Full-Stack / CMS 
Dinamis (PHP, Node.js, 
Python) 
Website #3: Web App / 
Dashboard Interaktif 
Modern 
Domain Utama (Opsi 
Rp 0 Murni) 
.is-a.dev (via PR 
GitHub) atau 
.dpdns.org (DigitalPlat) 
.us.kg atau .qzz.io (via 
DigitalPlat 
FreeDomain) 
.tech / .live (GitHub 
Student Pack) atau 
.pp.ua 
Domain Lokal (Opsi 
Promo Oktober 2026) 
.my.id Rp 1.000 di BOC 
(Kupon: MY1K) 
.biz.id Rp 1.000 di BOC 
(Kupon: BIZ1K) 
.web.id Rp 3.000 di 
IDwebhost (Tanpa 
Kupon) 
Hosting & Runtime 
Cloudflare Pages 
(Unlimited Bandwidth & 
Requests) 
Serv00 (3 GB NVMe, 
PHP 8.5/Node/Python) 
atau InfinityFree (5 
GB) 
Alwaysdata (1 GB 
SSD, Multi-bahasa) 
atau Vercel Hobby 
(100 GB) 



<!-- [ID:13_DATA_SCHEMA_S058] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 92

Promo ini berlangsung dari 1 Oktober hingga 31 Oktober 2026 (berakhir besok), tidak 
membutuhkan kode kupon (TANPA KODE KUPON), tidak memiliki syarat pembelian hosting, 
dan langsung aktif setelah pembayaran via Go-Pay, OVO, Virtual Account, atau minimarket. 
Terkait beredarnya info klaim domain gratis Rp 0 dari IDwebhost di berbagai blog, hasil 
pelacakan live menunjukkan bahwa IDwebhost memang sempat mengadakan Promo Akhir 
Pekan berkuota terbatas untuk 1 domain gratis per akun pada 18–20 September 2026 (kupon 
sEp18-mtSm) dan 16–18 Oktober 2026 (kupon mT5m-0kt15) melalui tautan 
https://order.idwebhost.com/domain-gratis. Namun, pada pengecekan langsung tanggal 30 
Oktober 2026, halaman klaim khusus tersebut tidak dapat diakses (inaccessible) dan 
periode promo pertengahan Oktober telah lewat. 
Selain kedua registrar di atas, IDCloudHost (idcloudhost.com/promo/promo-domain-id/) juga 
menawarkan promo aktif untuk pendaftaran baru .my.id, .biz.id, dan .web.id seharga Rp 5.000 
untuk tahun pertama dengan kode promo cuma5000 (sedangkan halaman domain gratis lama 
mereka dengan kode fdidch telah ditutup kecuali dibeli sepaket dengan Cloud Hosting, dan 
kode Rp 100 myid81 hanya berlaku khusus pada 17 Agustus 2026). Sebagai perbandingan 
pasar, DomaiNesia mematok promo domain mulai Rp 9.900/tahun, sementara Exabytes 
menawarkan .my.id mulai Rp 12.000/tahun. Apabila salah satu dari 3 website Anda 
membutuhkan ekstensi internasional, IDwebhost juga sedang memberikan diskon domain 
.cloud seharga Rp 30.900/tahun (berlaku hingga 31 Desember 2026, tanpa kupon) dan .bond 
seharga Rp 60.900/tahun (hingga 31 Oktober 2026), Qwords menawarkan .it.com seharga 
Rp 77.000, serta Rumahweb menyediakan promo .blog seharga Rp 42.000/tahun dan 
ekstensi .icu, .cyou, .sbs, atau .cfd mulai Rp 30 ribuan. 
2. Hosting, Panel Kontrol, dan Database Cloud Gratis 
untuk 3 Website 
Untuk memenuhi kebutuhan hosting beserta panel kontrol bagi 3 website berbeda yang 
dikodekan dari GitHub Codespaces, strategi terbaik adalah memadukan dua arsitektur: Hosting 
Berpanel Penuh (PaaS/Shared) untuk aplikasi dinamis yang membutuhkan manajemen 
file/database visual atau proses background via SSH, serta Edge/Git-Push Hosting yang 
otomatis mempublikasikan perubahan kode setiap kali Anda menjalankan git push dari 
Codespaces. 
Kategori 1: Hosting Gratis dengan Control Panel Penuh & Akses SSH 
(Untuk Website Dinamis / Backend) 
Penyedia hosting berpanel gratis terkuat untuk pengembang saat ini adalah Serv00 
(serv00.com), sebuah platform Eropa yang dioperasikan oleh hostUNO.com dengan lebih dari 
170.000 pengguna aktif. Dalam satu akun gratis tanpa iklan, Anda memperoleh 3 GB ruang 
simpan NVMe SSD, transfer bulanan tak terbatas, kemampuan menampung hingga 100 
website/domain, 10 database MySQL 8.0, 3 database PostgreSQL 16, database MongoDB 
6.0, RAM 512 MB, 15 proses sistem, 3 port TCP/UDP, serta backup harian selama 7 hari. 
Seluruh pengelolaan dilakukan melalui panel manajemen DevilWEB (dilengkapi antarmuka 
PhpMyAdmin di pma.serv00.com, PhpPgAdmin di 
pga.se[span_52](start_span)[span_52](end_span)rv00.com, dan RockMongo di 
moa.serv00.com) atau langsung melalui terminal SSH dan Git menggunakan utilitas baris 



<!-- [ID:13_DATA_SCHEMA_S059] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 93

perintah devil. Infrastruktur Serv00 mendukung hampir seluruh bahasa pemrograman modern: 
PHP (versi 5.6 hingga 8.5 dengan dukungan penuh .htaccess dan batas eksekusi 180 detik), 
Node.js (semua versi via NPM termasuk dukungan WebSocket), Python (Django/Flask versi 
2.7 dan 3.8–3.12), Ruby on Rails, Java (OpenJDK 8–27, Tomcat, GlassFish), Perl, Rust, 
C/C++, hingga .NET. Hal krusial yang harus Anda perhatikan: pendaftaran akun di 
https://www.serv00.com/register-account/ melewati proses tinjauan manual (manual review) 
yang memakan waktu beberapa jam hingga maksimal 72 jam guna mencegah 
penyalahgunaan, sehingga Anda wajib mendaftarkannya sekarang juga sebelum mulai menulis 
kode. 
Untuk panel PaaS yang langsung aktif tanpa antrean panjang, Alwaysdata 
(alwaysdata.com/en/offers/) menyediakan paket Free Public Cloud tanpa kartu kredit dan 
berlaku seumur hidup untuk kebutuhan personal/non-profit. Meskipun dokumentasi pihak ketiga 
dan laporan keamanan lama masih menyebut batas 100 MB, tabel harga resmi Alwaysdata 
tahun 2026 mencantumkan kuota gratis sebesar 1 GB SSD, RAM 256 MB, 1/4 CPU, dan rolling 
backup 3 hari. Keunggulan utama Alwaysdata untuk skenario 3 website Anda adalah 
kebijakannya yang mengizinkan jumlah website tak terbatas (unlimited sites), domain tak 
terbatas, database tak terbatas (MariaDB/MySQL, PostgreSQL, dan RabbitMQ), serta 
akun email tak terbatas di dalam satu akun selama total penggunaannya tidak melampaui 
kuota ruang simpan. Panel adminnya menyediakan konfigurasi server HTTP, WAF, Let's 
Encrypt SSL otomatis, akses SSH, SFTP, dan WebDAV, scheduled tasks (cron/daemon), serta 
dukungan multi-bahasa mulai dari PHP, Python, Node.js, Ruby, Java, Rust, Deno, Elixir, Lua, 
hingga Go. 
Apabila salah satu website Anda berbasis PHP atau WordPress dan Anda lebih menyukai 
antarmuka klasik bergaya cPanel, InfinityFree (infinityfree.com) menawarkan 5 GB ruang 
simpan, bandwidth tak terbatas, PHP 8.3 / 8.4, serta 400 database MySQL 8.0 / MariaDB 
11.4 tanpa iklan dan tanpa kartu kredit. Anda mendapatkan akses ke VistaPanel (cPanel) 
lengkap dengan Softaculous Installer (lebih dari 400 skrip siap pasang) dan Site.pro Website 
Builder (200+ template), dengan batasan teknis berupa ketiadaan akses SSH dan batas 
maksimum 30.000 inodes (jumlah file). Sebagai alternatif tambahan, ulasan di blog resmi 
WebHostMost (blog.webhostmost.com) mengonfirmasi paket gratis mereka per Maret 2026 
yang berjalan di atas prosesor AMD EPYC dan LiteSpeed Enterprise dengan dukungan PHP 
8.3, Node.js, MySQL, PostgreSQL, dan Unlimited Inodes, namun kapasitas penyimpanannya 
dibatasi ketat pada 125 MB NVMe SSD (untuk 1 domain utama dan 5 subdomain) serta 
mewajibkan pengguna login minimal sekali setiap 45 hari agar akun tetap aktif. 
Kategori 2: Edge, Static, dan SSR Hosting (Deploy Otomatis via git 
push dari Codespaces) 
Untuk website yang dikembangkan dengan framework modern di GitHub Codespaces (seperti 
Astro, Next.js, React, atau HTML/Tailwind statis), menghubungkan repositori GitHub langsung 
ke platform Edge meminimalkan waktu konfigurasi server. Tabel berikut membandingkan kuota 
dan batasan terbaru tahun 2026. 
Penyedia Hosting 
Kuota Gratis (Status 
Oktober 2026) 
Dukungan Backend / 
Fungsi 
Batasan Kritis & Aturan 
2026 yang Wajib 
Diketahui 
Cloudflare Pages + 
Workers 
Unlimited Sites, 
Unlimited Bandwidth, 
Workers (100rb 
req/hari, 10ms 
Maksimal 20.000 file 
dan 25 MiB per file. 



<!-- [ID:13_DATA_SCHEMA_S060] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 95

Statis & Edge) 
Apabila ketiga website Anda di-hosting pada Cloudflare Pages atau Vercel dan memerlukan 
penyimpanan data eksternal yang permanen, Turso (turso.tech) dan Cloudflare D1 
menawarkan kapasitas ruang simpan terbesar di tahun 2026. Berdasarkan pemantauan kuota 
per 19 Oktober 2026, paket gratis Turso (Edge SQLite) menyediakan 5 GB total 
penyimpanan, kuota hingga 100 database (sangat leluasa untuk melayani 3 website atau 
lebih), 500 juta baris dibaca (rows read) per bulan, 10 juta baris ditulis (rows written) per 
bulan, serta pemulihan point-in-time 1 hari. Di dalam ekosistem Cloudflare sendiri, Cloudflare 
D1 sudah memberikan database SQL serverless gratis dengan kapasitas 5 GB dan Cloudflare 
R2 menyediakan 10 GB object storage. 
Untuk proyek yang membutuhkan database relasional PostgreSQL lengkap dengan sistem 
autentikasi pengguna, Supabase (supabase.com) menawarkan paket gratis permanen yang 
mencakup 2 proyek aktif, masing-masing dengan 500 MB database PostgreSQL, 1 GB 
penyimpanan file, 50.000 pengguna aktif bulanan (MAU) pada fitur Auth, 500.000 eksekusi 
Edge Functions, 200 koneksi realtime bersamaan, serta 5 GB bandwidth keluar (egress). Perlu 
dicatat bahwa proyek gratis Supabase akan dijeda (paused) secara otomatis setelah 7 hari 
tanpa aktivitas, meskipun datanya tetap aman dan proyek dapat dicegah dari status jeda 
secara proaktif dalam waktu kurang dari 10 menit konfigurasi. Jika Anda membutuhkan lebih 
dari 2 proyek PostgreSQL, Neon (neon.tech) menyediakan kuota gratis tahun 2026 berupa 0,5 
GB penyimpanan per proyek, 100 CU-hours waktu komputasi/bulan, dan mendukung 
hingga 100 proyek (masing-masing 10 branches) dengan 5 GB network egress. Sementara itu, 
untuk mengisi kekosongan MySQL gratis pasca-dihapusnya paket gratis PlanetScale, Aiven 
menyediakan 1 layanan MySQL gratis, 1 PostgreSQL gratis (1 VM dedikasi, 1 CPU, 1 GB 
RAM, 1 GB storage), dan 1 layanan Valkey/Redis gratis, sedangkan MongoDB Atlas (Tier 
M0) tetap menyediakan 512 MB database NoSQL dokumen secara gratis selamanya. 
3. Arsitektur Email Custom Gratis: Terima dan Kirim di 
3 Domain dengan 1 Gmail 
Mengelola email custom profesional untuk 3 domain sekaligus (misalnya 
admin@website1.my.id, halo@website2.biz.id, dan support@website3.dpdns.org) sering kali 
terhambat oleh batasan penyedia gratis tradisional. Sebagai contoh, paket gratis ImprovMX per 
Agustus 2026 hanya mengizinkan 1 domain (maksimal 25 alias, 500 email diteruskan/hari) dan 
sama sekali tidak menyediakan fitur kirim email (0 SMTP), sedangkan Zoho Mail Forever 
Free Plan dibatasi ketat untuk 1 custom domain per organisasi dan menonaktifkan akses 
protokol IMAP, POP, maupun ActiveSync pada tingkat gratisnya. 
Dengan mengombinasikan Cloudflare Email Routing (untuk surat masuk) dan SMTP 
Transaksional Gratis Brevo atau Resend yang dihubungkan ke fitur "Send mail as" di Gmail 
pribadi Anda, Anda dapat menerima sekaligus membalas email dari ketiga domain custom 
Anda tanpa biaya bulanan. Ikuti prosedur konfigurasi berikut untuk mengaktifkannya: 
1.​ Aktifkan Penerusan Email Masuk di Cloudflare Email Routing: Masuk ke dashboard 
Cloudflare Anda, pilih domain pertama, lalu buka menu Email → Email Routing (atau 
Compute > Email Service > Email Routing). Klik Create address, ketik nama alamat 
sebelum tanda @ (seperti info atau admin), pilih alamat Gmail pribadi Anda sebagai 
tujuan (destination), dan klik tautan verifikasi yang dikirimkan Cloudflare ke inbox Gmail 
Anda. Setujui penambahan otomatis record DNS MX dan TXT oleh Cloudflare, serta 



<!-- [ID:13_DATA_SCHEMA_S061] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 107

| **Kelompok D: Cicil / Estafet Bulanan (Time-Decaying Trial & Kredit Awal)** | DigitalOcean 
(US200 / 60 hari), Linode (US100 / 60 hari), Vultr (US200–US300 / 30 hari), Kamatera (US100 / 30 
hari), AWS Free Plan (US200 kredit / 6 bulan), Microsoft Azure (US200 / 30 hari + VM 12 bulan), 
Alibaba Cloud ECS/Bailian (90 hari), AI21 Labs (US10 / 90 hari), AgentRouter (US200 kredit), 
FreeModel.dev (US300 kredit). | Arloji masa aktif berdetak detik itu juga saat akun diverifikasi, 
terlepas dari apakah server/API dipakai atau tidak. | **Jangan daftar bersamaan di Hari ke-1.** 
Daftar secara berurutan (estafet) hanya ketika kuota mesin sebelumnya hampir habis, lalu 
suntikkan kunci/IP baru ke .env secara langsung. |
| **Kelompok E: Grosir Komersial Pay-As-You-Go (Kartu / Crypto USDT)** | Fal.ai, WaveSpeed AI 
(US1 kredit awal), Novita AI (US0,50 kredit awal), RunPod, Vast.ai, Replicate, PiAPI, CometAPI, 
302.AI, Baseten (US30 kredit), Predibase (US25 kredit). | Akun dasar gratis; saldo baru terpotong 
saat memanggil model berbayar atau saat *Auto-Topup* diaktifkan. | **Buat akun via 
GitHub/Google di Hari ke-1 hanya untuk klaim kredit sambutan gratis.** Jangan isi saldo uang 
sendiri; aktifkan pengisian saldo otomatis dari kasir pendapatan pelanggan (@CryptoBot USDT / 
QRIS). |

<!-- [ID:13_DATA_SCHEMA_S062] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
### Lapisan 1: Pencegatan Memori Semantik 25 Milidetik dan Kompresi Token 98%
Permintaan yang wajib diproses oleh backend—seperti interaksi dari tiga bot Telegram yang 
dirangkai secara *failover* (TOKEN_BOT_UTAMA, TOKEN_BOT_ACTIVITY, 
TOKEN_BOT_CADANGAN) atau gateway WhatsApp mandiri devlikeapro/waha—tidak langsung 
diteruskan ke model bahasa besar, melainkan dicegat terlebih dahulu oleh lapisan memori 
semantik Valkey dan RedisVL (redis/redis-vl-python) atau spider-rs/hybrid_cache_server yang 
terhubung ke Upstash Serverless Redis (gratis 256 MB dan 500.000 perintah per bulan). Dalam 
skenario aplikasi viral, sebagian besar pengguna cenderung menanyakan pola pertanyaan atau 
instruksi populer yang serupa. RedisVL mengonversi kueri masuk menjadi representasi vektor dan 
melakukan pencarian kemiripan semantik dalam waktu sekitar 25 milidetik. Apabila ditemukan 
respons yang cocok di dalam memori cache, jawaban langsung disajikan kepada pengguna tanpa 
memotong kuota API eksternal sedikit pun. Apabila terjadi *cache miss*, payload instruksi dan 
keluaran alat terlebih dahulu dipadatkan menggunakan mksglu/context-mode (yang mampu 
memangkas ukuran token konteks hingga 98% melalui *sandboxing* keluaran) yang 
dikombinasikan dengan fitur *Real-Time Token Compression* (RTK) pada OmniRoute guna 
menghemat 20% hingga 40% konsumsi token sebelum menyentuh model.

<!-- [ID:13_DATA_SCHEMA_S063] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 37

Rules), bandwidth tak terbatas pada Pages, 5 GB penyimpanan SQLite + 5 juta 
pembacaan baris/hari pada Cloudflare D1, serta 10 GB penyimpanan objek + 1 juta 
operasi Kelas A + 10 juta operasi Kelas B per bulan pada R2. 
2.​ Rantai Failover Database SQL, NoSQL & Vektor Gratis (Turso, Supabase, Neon, 
MongoDB Atlas, Hostim, Convex, Appwrite, Firebase) — URL Polos Turso Cloud 
(Distributed SQLite/libSQL): https://turso.tech/ | URL Polos Halaman Harga & Batas Kuota 
Turso: https://turso.tech/pricing | URL Polos Supabase (PostgreSQL + pgvector + Auth + 
Storage): https://supabase.com | URL Polos Neon Serverless Postgres: https://neon.tech 
| URL Polos MongoDB Atlas (512 MB M0 Cluster Gratis Selamanya): 
https://www.mongodb.com/atlas | URL Polos Hostim.dev (Managed Postgres/MySQL 256 
MB & Redis 128 MB Gratis Selamanya Tanpa Kartu): https://hostim.dev/ | URL Polos 
Convex (Realtime Backend-as-a-Service Gratis 1 Juta Operasi): https://www.convex.dev/ 
| URL Polos Appwrite Cloud (Alternatif Firebase Open-Source Gratis 2 GB Storage): 
https://appwrite.io/ | URL Polos Firebase Realtime Database & Firestore (Gratis 1 GB 
Storage): https://firebase.google.com/products/database — Kegunaan & Aturan Terbaru 
(Audit Oktober 2026): Seluruhnya 100% tanpa kartu kredit (login via GitHub/Google). 
Perhatikan penyesuaian kuota terbaru tahun 2026: Turso Free Tier kini memberikan 5 GB 
total penyimpanan (turun dari 9 GB lama), maksimal 100 database, 500 juta baris 
dibaca/bulan, 10 juta baris ditulis/bulan, 3 GB sinkronisasi/bulan, dan 1 hari point-in-time 
restore tanpa jeda (never pauses). Supabase Free Tier memberikan 500 MB database 
Postgres, 1 GB file storage, 5 GB egress/bulan, 50.000 MAU Auth, 500.000 invokasi 
Edge Functions/bulan, dan maksimal 2 proyek aktif, namun proyek akan dijeda (pause) 
otomatis setelah 7 hari tanpa aktivitas dan tidak memiliki backup otomatis. Neon Free Tier 
memberikan 100 CU-hours komputasi/bulan, hingga 100 proyek (10 branch per proyek), 
5 GB transfer jaringan, serta penyimpanan 0,5 GB (ditingkatkan menjadi 1 GB per proyek 
pada Oktober 2026); komputasi akan tidur (scale-to-zero) setelah 5 menit idle tetapi 
proyek tidak pernah dijeda permanen. Catatan: PlanetScale telah menghapus paket 
gratisnya secara permanen dan CockroachDB Basic telah menutup pembuatan klaster 
gratis baru; gunakan Hostim.dev atau Aiven jika Anda membutuhkan MySQL gratis tanpa 
kartu kredit. 
3.​ Upstash Serverless Redis / Workflow & Backblaze B2 Object Storage — URL Polos 
Upstash Utama (Redis 256 MB & 500K Commands/Bulan Gratis): https://upstash.com | 
URL Polos Upstash Workflow (Gratis 1.000 Steps/Hari): 
https://upstash.com/pricing/workflow | URL Polos Upstash Search: 
https://upstash.com/pricing/search | URL Polos Backblaze B2 Cloud Storage (Gratis 10 
GB Pertama Tanpa Kartu Visa): https://www.backblaze.com/cloud-storage | URL Polos 
Informasi Produk Backblaze B2: https://www.backblaze.com/b2/cloud-storage.html — 
Kegunaan & Aturan Terbaru (Oktober 2026): 100% tanpa kartu kredit. Upstash 
menyediakan REDIS_CONN_STRING gratis untuk caching One-API/New-API dan 
antrean jhao104/proxy_pool. Backblaze B2 menyediakan 10 GB penyimpanan objek .bin 
dan media secara gratis tanpa meminta kartu pembayaran (kartu baru diminta jika 
membuka batas di atas 10 GB), dilengkapi unduhan (egress) gratis hingga 3x lipat 
volume data yang disimpan. 
4.​ Google Colaboratory, Kaggle Notebooks & Lightning AI (Komputasi GPU Cloud 
Gratis Tanpa Kartu) — URL Polos Google Colaboratory (GPU T4 Gratis): 
https://colab.research.google.com | URL Polos Kaggle Notebooks (Gratis 30 Jam/Minggu 
GPU Dual-T4 atau P100): https://www.kaggle.com | URL Polos Workspace Kode Kaggle: 
https://www.kaggle.com/code | URL Polos Lightning AI (Kredit Studio PyTorch/GPU 


