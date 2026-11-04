
<!-- [ID:26_AUTO_DISCOVERY_UMUM_S189] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 1. KONFIGURASI SUMBER & BATAS KETAT SWEETSPOT AI (45K CHARS / 20 HAL 
PDF)​
# 
======================================================================
========​
RAW_PDF_FILES = [​
    "blueprint_utama_1.pdf",       # Masukkan PDF ke-1 (dan ke-2 jika 
terpisah)​
    "blueprint_utama_2.pdf"​
]​
RAW_MD_FILES = [​
    "blueprint_utama.md",          # MD Mentah 3.8 Juta Karakter​
    "hasil_lama_tidak_maksimal.md" # Opsional​
]​
​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S190] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# KUNCI SWEETSPOT SESUAI ATURAN GEMINI / ARGON APPS:​
MAX_MD_SWEETSPOT_CHARS = 45000     # Maksimal 45.000 karakter per file 



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S191] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 3

MD dalam 1 sesi chat​
MAX_PDF_SWEETSPOT_PAGES = 20       # Maksimal 20 halaman per file PDF 
dalam 1 sesi chat​
MAX_MASTER_FILES = 3               # 1-3 File Master Peta Otak Utuh 
(masing-masing <= 45.000 karakter)​
​
OUTPUT_DIR        = Path("OUTPUT_FINAL_SWEETSPOT_LOSSLESS")​
MINERU_OUT_DIR    = OUTPUT_DIR / "01_MINERU_RAW_DAN_GAMBAR"​
MASTER_BLUEPRINT  = OUTPUT_DIR / 
"02_MASTER_1_SAMPAI_3_FILE_SWEETSPOT_45K"​
MODUL_MD_45K_DIR  = OUTPUT_DIR / "03_MODUL_MD_MURNI_MAKS_45K_CHARS"​
MODUL_PDF_20P_DIR = OUTPUT_DIR / "04_MODUL_PDF_MURNI_MAKS_20_HALAMAN"​
IMAGES_GLOBAL_DIR = OUTPUT_DIR / "05_KOLEKSI_GAMBAR_DIAGRAM_PDF"​
​
for d in [OUTPUT_DIR, MINERU_OUT_DIR, MASTER_BLUEPRINT, 
MODUL_MD_45K_DIR, MODUL_PDF_20P_DIR, IMAGES_GLOBAL_DIR]:​
    d.mkdir(parents=True, exist_ok=True)​
​
# 
======================================================================
========​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S192] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 3. EKSTRAKSI PDF VIA MINERU + PENYELAMATAN GAMBAR & PEMOTONG PDF 20 
HALAMAN​



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S193] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 6

    part = 1​
​
    for start_p in range(0, total_pages, MAX_PDF_SWEETSPOT_PAGES):​
        end_p = min(start_p + MAX_PDF_SWEETSPOT_PAGES - 1, total_pages 
- 1)​
        new_doc = fitz.open()​
        new_doc.insert_pdf(doc, from_page=start_p, to_page=end_p)​
        out_pdf = MODUL_PDF_20P_DIR / 
f"{pdf_stem}_PART_{part:02d}_HAL_{start_p+1}_SD_{end_p+1}.pdf"​
        new_doc.save(str(out_pdf))​
        new_doc.close()​
        part += 1​
    doc.close()​
​
# 
======================================================================
========​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S194] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 8

    }​
​
# 
======================================================================
========​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S195] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S196] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# SEL 1: INSTALASI & MOUNT GOOGLE DRIVE OTOMATIS​
# 
======================================================================
========​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S197] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Hapus tanda '#' di baris bawah ini saat pertama kali menjalankan di 
Colab:​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S198] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 1. Mount Google Drive Otomatis agar proses 45 menit 100% aman dari 



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S199] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 2. LOKASI FILE MENTAH ANDA (TARUH DI GOOGLE DRIVE ATAU FOLDER COLAB)​
# 
======================================================================
========​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S200] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Anda bisa menaruh file PDF & MD di Google Drive agar tidak perlu 
upload berulang kali​
RAW_PDF_FILES = [​
    "blueprint_utama_1.pdf",       # Ganti dengan path PDF ke-1 Anda 
(total 868 hal)​
    "blueprint_utama_2.pdf"        # Ganti dengan path PDF ke-2 Anda 
(jika ada)​
]​
RAW_MD_FILES = [​
    "blueprint_utama.md",          # MD Mentah 3.8 Juta Karakter​
    "hasil_lama_tidak_maksimal.md" # Opsional: file lama untuk ikut 
diaudit silang​
]​
​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S201] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# BATAS KETAT SWEETSPOT AI SESUAI ATURAN GEMINI / ARGON APPS:​
MAX_MD_SWEETSPOT_CHARS = 45000     # Maksimal 45.000 karakter per file 
MD (1 sesi chat)​
MAX_PDF_SWEETSPOT_PAGES = 20       # Maksimal 20 halaman per file PDF 
(1 sesi chat)​
​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S202] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Struktur Folder Output di Google Drive​
MINERU_OUT_DIR    = BASE_DRIVE_DIR / "01_MINERU_RAW_EXTRACTION"​
MASTER_BLUEPRINT  = BASE_DRIVE_DIR / 
"02_MASTER_PETA_OTAK_SWEETSPOT_45K"​
MODUL_MD_45K_DIR  = BASE_DRIVE_DIR / 
"03_MODUL_MD_AUDIT_SIAP_PAKAI_45K"​
MODUL_PDF_20P_DIR = BASE_DRIVE_DIR / "04_MODUL_PDF_VISUAL_MAKS_20_HAL"​
IMAGES_GLOBAL_DIR = BASE_DRIVE_DIR / "05_KOLEKSI_GAMBAR_DIAGRAM_ASLI"​



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S203] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 3

BOT_AUTONOMOUS_DIR= BASE_DRIVE_DIR / "06_BOT_OTONOM_GITHUB_CODESPACES"​
​
for d in [MINERU_OUT_DIR, MASTER_BLUEPRINT, MODUL_MD_45K_DIR, 
MODUL_PDF_20P_DIR, IMAGES_GLOBAL_DIR, BOT_AUTONOMOUS_DIR]:​
    d.mkdir(parents=True, exist_ok=True)​
​
# 
======================================================================
========​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S204] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 9

# 
======================================================================
========​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S205] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 14

membuatkan foldernya! 
○​ Menulis masing-masing potongan kode ke file tujuannya secara presisi. 
○​ Mengarsipkan obrolan tadi ke folder .bot_history_inbox/ dan mengosongkan 
inbox_ai.md untuk sesi chat berikutnya. 
○​ Menjalankan git add ., git commit, dan git push otomatis ke repositori GitHub Anda! 


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S206] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Bootstrap OpenClaw self-evolving skill
npm i -g clawhub
clawhub install RangeKing/self-evo-agent


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S207] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Mission
<isi misi>


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S208] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Target 12 bulan
- <tulis target>
""",
    "office/brain/strategy.md": """# Strategy

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S209] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Prioritas Q1
1. ...
2. ...


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S210] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Kode
- Bahasa: TypeScript + Python
- Formatter: Prettier / Ruff
- Lint: ESLint / Ruff
- Commit: Conventional Commits
- Branch: feat/, fix/, chore/, sec/


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S211] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Dokumentasi
- Setiap folder wajib README.md
- Setiap keputusan besar wajib ADR di docs/ADR/
- Setiap agent wajib SOP di office/agents/<id>/SOP.md
""",
    "office/brain/stack.md": """# Stack

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S212] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# ==== AI ====
OPENAI_API_KEY=
ANTHROPIC_API_KEY=


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S213] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# ==== GitHub ====
GITHUB_APP_ID=
GITHUB_APP_PRIVATE_KEY=
GITHUB_PAT=


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S214] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# SOP — {name} ({id})


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S215] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Objective
{objective}


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S216] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Input
{input_list}


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S217] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Output
{output_list}


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S218] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Brain files WAJIB dibaca
- office/brain/vision.md
- office/brain/strategy.md
- office/brain/principles.md
- office/brain/security-rules.md
- office/brain/onchain-rules.md (jika menyentuh on-chain)


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S219] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Escalation
{escalation_rule}


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S220] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## KPI
{kpi_block}


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S221] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Tools
{tools_list}


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S222] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Payment Service

Semua uang keluar WAJIB lewat sini. Tidak ada jalur lain.


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S223] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Scanner Service (READ-ONLY)


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S224] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Non-root user (wajib)
RUN useradd -m -u 10001 app && chown -R app:app /app
USER app

EXPOSE 8000
HEALTHCHECK CMD curl -fsS http://localhost:8000/health || exit 1
CMD ["uvicorn", "office.orchestrator.api:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/ /app/services/
RUN useradd -m -u 10001 app && chown -R app:app /app
USER app

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S225] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## 1. Bot Defense
- Enable "Bot Fight Mode" (free) atau "Super Bot Fight Mode" (Pro).
- Challenge: semua `POST` ke `/api/*`, `/payment/*`, `/scan/*`.
- Block: user-agent kosong + request ke endpoint sensitif.


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S226] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## 3. Geo & ASN
- Block: TOR exit, ASN hosting publik (opsional).
- Owner bypass: header `CF-Connecting-IP` di-whitelist untuk IP owner.


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S227] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Infra


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S228] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Scanner hanya butuh:
INTERNAL_KEY=ubah-ini

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S229] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# TIDAK BOLEH berisi:

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S230] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Routing default per kategori agent
DEFAULT_ROUTE = {
    "exec":  [("anthropic","claude-3-5-sonnet"), ("openai","gpt-4o"), ("local","llama3")],
    "eng":   [("openai","gpt-4o"), ("anthropic","claude-3-5-sonnet"), ("local","llama3")],
    "ai":    [("openai","gpt-4o-mini"), ("anthropic","claude-3-5-sonnet"), ("local","llama3")],
    "sec":   [("anthropic","claude-3-5-sonnet"), ("openai","gpt-4o"), ("local","llama3")],
    "mkt":   [("openai","gpt-4o-mini"), ("local","llama3")],
    "fin":   [("anthropic","claude-3-5-sonnet"), ("openai","gpt-4o-mini")],
    "default":[("openai","gpt-4o-mini"), ("local","llama3")],
}


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S231] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Audit Service

Append-only log verifier + forensics.


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S232] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Jadwal
- `nightly-audit.yml` panggil `/verify` setiap malam.
- Kalau `ok=false` → alert critical ke owner + otomatis L4_READONLY.


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S233] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Bot Adapters

Semua adapter WAJIB:
1. Verifikasi signature (x-hub-signature-256 untuk Meta, dll).
2. Teruskan ke `bots.core.dispatcher.dispatch()` — TIDAK boleh route sendiri.
3. Verifikasi owner + PIN dilakukan dispatcher (bukan adapter).


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S234] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Pola Regex ekstraksi nominal masuk untuk berbagai Bank & QRIS di Indonesia
BANK_AMOUNT_PATTERNS = [
    r"Rp[\s\.]*([0-9\.,]+)",                  # Format umum: Rp 50.142 / Rp50,142.00
    r"IDR[\s\.]*([0-9\.,]+)",                 # Format BCA / Mandiri: IDR 50,142.00
    r"Nominal\s*:\s*Rp\s*([0-9\.,]+)",        # Format QRIS Merchant / BRI
    r"sebesar\s*Rp\s*([0-9\.,]+)"             # Format Bank Jago / SeaBank / Livin
]


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S235] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# ================= KONFIGURASI PRIBADI ANDA =================
STATIC_QRIS_STRING = "00020101021126..."  # Isi dengan string QRIS Statis milik Anda
IMAP_HOST = "imap.gmail.com"
EMAIL_USER = "email_mutasi_anda@gmail.com"
EMAIL_APP_PASSWORD = "xxxx xxxx xxxx xxxx" # Google App Password (16 karakter)
INVOICE_EXPIRY_SECONDS = 900               # 15 Menit

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S236] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# ============================================================


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S237] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# =====================================================================

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S238] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 1. PROFIL ENDPOINT & JSON-PATH EXTRACTOR TIAP MERCHANT

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S239] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
#    (Bisa ditambah provider baru kapan saja tanpa ubah logika mesin!)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S240] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 3. MESIN PENEMBAK API LANGSUNG (DENGAN TLS CHROME IMPERSONATION)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S241] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 4. ENDPOINT KONEKSI AKUN MERCHANT (LOGIN 1X SIMPAN SELAMANYA)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S242] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 5. PLUG-AND-PLAY: TAMBAH PROFIL API BANK / QRIS BARU (MISAL NOBU)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S243] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 1. REGISTRY ATURAN BACA MUTASI UNIVERSAL (BISA DITAMBAH TANPA CODING)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S244] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 3. ENDPOINT PLUG-AND-PLAY: TAMBAH QRIS APA SAJA OTOMATIS TERDETEKSI

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S245] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 5. UNIVERSAL MUTATION INGESTION + AUTO-PAYMENT TREASURY TRIGGER

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S246] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# ── Konfigurasi ─────────────────────────────────────────────────────
BASE = "https://inference.dahl.global"
HERE = Path(__file__).resolve().parent
CREDS_DIR = HERE / "creds"
MODEL_DEFAULT = "deepseek-ai/DeepSeek-V4-Flash-0731"
POOL_FILE = HERE / "keys.txt"


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S247] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Lock untuk thread-safe file writing
FILE_LOCK = threading.Lock()


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S248] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# === 1. IDENTITAS BOT & KUNCI OWNER (WAJIB DIISI) ===
TOKEN_BOT_UTAMA=""
ADMIN_USER_ID=""
WEB_PORTAL_BRAND_NAME="AetherFree AI Studio"
MINIAPP_PUBLIC_URL=""
CUSTOM_WEB_DOMAIN=""


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S249] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# === 3. KASIR OTOMATIS 2 ARAH (INDONESIA & GLOBAL) ===
GOPAY_STATIC_QRIS_RAW=""
PAKASIR_SLUG=""
PAKASIR_API_KEY=""
DUITKU_MERCHANT_CODE=""
DUITKU_API_KEY=""
CRYPTOBOT_API_TOKEN=""


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S250] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# BIKINAI — MASTER ENGINE v3.7.1 (STRICT TECHNICAL SEPARATION & CANONICAL REPOS)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S251] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# BIKINAI SUPER INTELLIGENCE — MASTER ENGINE v3.7.0 (FRONTIER AUTONOMIC CORE)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S252] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# BIKINAI SUPER INTELLIGENCE — MASTER ENGINE v3.6.0 (AUTONOMOUS AGENTIC CORE)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S253] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Fitur Terintegrasi Utuh (v1.0 -> v3.6.0 Tanpa Pengurangan):

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S254] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 3. 8-Agent Rolling Pool (Argon, Qwen, DeepSeek, Muse, Nano-Muse, Harness,

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S255] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
#    Nous Hermes, Groq/Cerebras/Pollinations) + Auto Circuit-Breaker 60s

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S256] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 5. Patch Audit Keamanan: Invoice Ledger Anti-Bypass Top-Up, HMAC-SHA256

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S257] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 6. Full Mini App SFW (Exclusive Radio Group + Context-Aware Engine Locking)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S258] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
#    & NocturneAI 3-Tab Web Studio (/api/nocturne/chat & /api/nocturne/generate)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S259] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 0. BRANKAS PERSISTEN ABADI, KUNCI ED25519 & KONFIGURASI RUNTIME

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S260] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 4. FULL WEBSITE-GRADE MINI APP SFW & NOCTURNEAI 3-TAB WEB STUDIO (PORT 8080)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S261] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Menjawab Catatan #5, #8, #9, #11, #12:

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S262] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# - Exclusive Radio Group (data-group) & Context-Aware Engine Locking di Mini App

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S263] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# - NocturneAI 3-Tab Utuh (Live Uncensored Chat, Media Generator + Download HD,

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S264] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
#   dan Dompet Penukaran Voucher Ed25519)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S265] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# - 100% Bahasa Konsumen (Bebas Istilah Dapur Developer di Layar Pembeli)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S266] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 5. SECURITY VALIDATORS (HMAC MINI APP, INPUT SANITIZER, & ED25519 VOUCHER)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S267] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 6. ROLLING 8-AGENT POOL (ARGON, QWEN, DEEPSEEK, MUSE, NANO-MUSE, HARNESS, HERMES, GROQ)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S268] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 7. IDENTITAS PENGGUNA (SANGMATA), BRANKAS TREASURY & INVOICE LEDGER

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S269] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 8. DUAL-RAIL GEO PAYMENT & ANTI-BYPASS INVOICE VERIFIER (PATCH AUDIT-01)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S270] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 9. MEDIA FETCHER, WEBAPP API & NOCTURNE STUDIO BACKEND HANDLERS

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S271] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 11. HELPER TRANSAKSI KOIN, AUTO-REFUND SWEEPER & BROADCAST TOPIK

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S272] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 15. SETUP GRUP OTONOM (/setup_grup, /ikat), WELCOME GATE, UPLOAD FOTO & CHAT NATURAL

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S273] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 16. ENTRYPOINT UTAMA (MAIN)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S274] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# SYSTEM SOP: AUTONOMOUS ARCHITECT & DUAL-REPO GOVERNANCE

Anda adalah Autonomous Lead Architect dan Maintainer untuk proyek ini. Setiap kali Anda menulis kode, memperbarui fitur, mengelola repositori, atau memodifikasi infrastruktur, Anda WAJIB mematuhi 4 Protokol Mutlak berikut tanpa pengecualian:


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S275] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# BIKINAI SUPER INTELLIGENCE — MASTER ENGINE v3.4.0 (ZERO-TYPO PRODUCTION CORE)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S276] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# - Auto-Detect GitHub Codespaces Mini App URL (Tanpa perlu /set_miniapp ulang!)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S277] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
#   + Independent External Unfiltered Portal (/unfiltered-portal) di Port 8080

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S278] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 0. BRANKAS PERSISTEN ABADI & AUTO-DETECT URL MINI APP CODESPACES

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S279] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 4. FULL WEBSITE-GRADE MINI APP SFW & PORTAL UNFILTERED EKSTERNAL (PORT 8080)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S280] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Menjawab Catatan #1: Mini App dilengkapi Banner Sambutan SFW, Upload Foto

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S281] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# - Embedded Dual Web Server Handler (Mini App SFW + Unfiltered Portal Port 8080)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S282] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# - Dual-Rail Geo Payment Engine (Auto ID QRIS/PG vs Global Crypto/Stars)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S283] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# - Wizard State & Menu Builders (Tombol Mini App Permanen di Baris Teratas!)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S284] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 5. IDENTITAS PENGGUNA (SANGMATA TRACKER) & BRANKAS KEUANGAN

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S285] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 6. DUAL-RAIL GEO PAYMENT ENGINE (OTOMATIS LOKAL ID vs GLOBAL CRYPTO/STARS)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S286] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Menjawab Catatan #3: Pengguna otomatis diarahkan sesuai wilayahnya; Owner

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S287] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# mengatur provider aktif di /admin hanya untuk kendali limit & preferensi!

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S288] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Menjawab Catatan #6: Menembak endpoint secara paralel dengan batas waktu ketat

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S289] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 8. STATE WIZARD & PEMBANGUN MENU (MINI APP SELALU TAMPIL DI PALING ATAS!)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S290] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Menjawab Catatan #1: Tombol Peluncur Mini App dikunci permanen di baris #1!

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S291] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# - Pemrosesan Multimodal Ingest (F.photo | F.document) & Render Otomatis

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S292] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# - Schedulers / Bimbingan Topik Grup Otomatis (/setup_grup, /ikat)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S293] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# - Built-in SangMata Tracker & Cyber Welcome Gate (Menyapa Member Baru)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S294] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# - Zero-Clutter Natural Chat Engine + Rotasi Footer Dinamis

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S295] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 12. HANDLER UPLOAD FOTO REFERENSI & PDF (LANGSUNG RENDER KE CHAT)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S296] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 13. HANDLER OBROLAN NYAMAN TANPA TOMBOL (ROBOT FOOTER DINAMIS & GEMINI STYLE)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S297] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Menjawab Catatan #6 & #7: Tombol tidak muncul terus, melainkan hanya saat diminta

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S298] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# dengan mengetik "tampilin tombol" atau "menu". Bahasa Indonesia 100% murni!

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S299] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 14. ENTRYPOINT UTAMA (MAIN)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S300] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 9. SECURITY SHIELD, STATELESS ED25519 VOUCHER & TRANSAKSI KOIN / JOB LEDGER

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S301] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 11. CALLBACK QUERY HANDLERS (MENU, WIZARD, DERIVATIVE UPSELL & ADMIN)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S302] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# ------------------------------------------------------------------------------

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S303] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 2. ORCHESTRATOR TIPIS, PLUGIN SURFACE, 6-GATE ZERO-TRUST STERILIZER,

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S304] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
#    VOUCHER ED25519 & AUTO-CS "SISKA"

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S305] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 5. DUAL WEB SERVER PORT 8080 + HUB OMNICHANNEL LINTAS PLATFORM (A4.b)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S306] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# ==============================================================================


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S307] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# HANDLERS UNTUK SELURUH ENDPOINT PORT 8080

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S308] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 6. MODUL 3 LENGKAP — SELURUH COMMAND, CALLBACK & INSPEKTOR LAYAR PEMBELI (A4.c)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S309] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# COMMAND HANDLERS LENGKAP (23 COMMANDS)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S310] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# HANDLER F.new_chat_members, F.photo | F.document, DAN F.text

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S311] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# BACKGROUND AUTONOMOUS DAEMONS LOOP & ENTRYPOINT main()

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S312] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# MASTER CONTRACT — STUDIO AI AGREGATOR
Versi: 1.0 | Pemilik: saya | Update STATE tiap akhir sesi.

====================================================================

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S313] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# ## BAGIAN A — STATE (DINAMIS, UPDATE TIAP SESI)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S314] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
### A1. Fase proyek saat ini

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S315] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
### A2. Keputusan yang sudah dibuat (+ alasan)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S316] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
### A3. Asumsi aktif

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S317] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
### A4. Open questions

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S318] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
### A5. Next actions (prioritas akali sela)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S319] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
### A6. Mode default sesi ini

====================================================================

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S320] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Ambigu → tanya: *Ini mau dijawab dari sisi BIZ atau ARCH?*

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S321] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Multi-perspektif → label: BIZ: / ARCH: / OPS: / dll.

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S322] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Jika user menyebut *all-in-one* atau *gabungkan semua*:
beri jawaban berlabel per domain, urut dari yang paling dibutuhkan user saat itu.

====================================================================
