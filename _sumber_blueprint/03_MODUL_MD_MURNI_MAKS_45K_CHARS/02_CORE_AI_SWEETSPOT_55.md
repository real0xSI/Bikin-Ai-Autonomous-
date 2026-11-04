
<!-- [ID:02_CORE_AI_S407] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 646

SUMBER) & PETA JALAN EKSEKUSI 
6.1 Tabel Master Link Pendaftaran & Repositori Resmi (v1.0 + 
Ekspansi SOTA v2.0) 
Gelombang Prioritas 
Nama Layanan & 
Tautan Resmi 
Fungsi Utama dalam 
Sistem v2.0 
Biaya 
🟢 GELOMBANG 1 
(Wajib di Awal: Markas, 
Otak, Cache, Guardrail, 
& Sandbox Rp 0) 
1. Telegram 
BotFather: 
[https://t.me/BotFather](
https://t.me/BotFather) 
2. 9Router Repo: 
[https://github.com/dec
olua/9router](https://gith
ub.com/decolua/9router
) 3. Google AI Studio 
(Gemini API): 
[https://aistudio.google.
com/app/apikey](https:/
/aistudio.google.com/ap
p/apikey) 4. Groq 
Cloud (Llama 3.3 & 
Whisper): 
[https://console.groq.co
m/keys](https://console.
groq.com/keys) 5. 
OpenRouter (:free 
LLM & Kokoro TTS): 
[https://openrouter.ai/se
ttings/keys](https://open
router.ai/settings/keys) 
6. SiliconFlow 
(DeepSeek-V4.1-Flash 
Murah): 
[https://www.siliconflow.
com/models](https://ww
w.siliconflow.com/mode
ls) 7. Cloudflare 
(Pages, R2 10GB, 
Workers & Turnstile): 
[https://dash.cloudflare.
com/sign-up](https://da
sh.cloudflare.com/sign-
up) 8. Oracle Cloud 
Free Tier (VPS ARM 
24/7): 
[https://www.oracle.com
Membangun Bot 
Utama, Grup Forum 
Komunitas, Dapur 
9Router + Valkey 
Cache (~25 ms), 
Database SQLite 
WAL/Turso, Mini App 
Terenkripsi (.bin) + 
Turnstile Anti-Tuyul, 
serta Mode Sandbox 
[1]. 
Rp 0 (100% Gratis) 



<!-- [ID:02_CORE_AI_S408] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 649

Gelombang Prioritas 
Nama Layanan & 
Tautan Resmi 
Fungsi Utama dalam 
Sistem v2.0 
Biaya 
Klip): 
[https://github.com/ToT
heBeginning/PuLID](htt
ps://github.com/ToTheB
eginning/PuLID) 26. 
SageAttention & 
TeaCache (Akselerasi 
GPU 54%): 
[https://github.com/thu-
ml/SageAttention](https
://github.com/thu-ml/Sa
geAttention) 27. Llama 
Prompt Guard 2 (86M) 
& NeMo Guardrails: 
[https://github.com/NVI
DIA/NeMo-Guardrails](
https://github.com/NVID
IA/NeMo-Guardrails) 
28. InsightFace 
(Vision Gate Usia >23 
Thn): 
[https://github.com/dee
pinsight/insightface](htt
ps://github.com/deepins
ight/insightface) 29. 
LangGraph & 
Langfuse Self-Hosted 
(Observabilitas): 
[https://langfuse.com/se
lf-hosting](https://langfu
se.com/self-hosting) 
30. HuggingFace & 
Civitai Token: 
[https://huggingface.co/
settings/tokens](https://
huggingface.co/settings
/tokens) & 
[https://civitai.com/](http
s://civitai.com/) 31. 
Backblaze B2 
(Cadangan R2 10GB): 
[https://www.backblaze.
com/cloud-storage](http
s://www.backblaze.com
/cloud-storage) 32. 



<!-- [ID:02_CORE_AI_S409] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 663

DOKUMEN MASTER BLUEPRINT 
(END-TO-END): EKOSISTEM OTONOM 
bikinAI Super Intelligence 
Dokumen ini merangkum secara utuh seluruh arsitektur teknis, model bisnis agregator, 
perhitungan biaya operasional 24/7, bedah psikologi kompetitor, otomatisasi multi-agen, hingga 
rekayasa pertahanan siber tingkat lanjut (Red-Teaming & Zero-Knowledge Security) untuk 
membangun dan mengembangkan bikinAI Super Intelligence dari titik modal Rp 0 hingga 
skala komersial global. 
BAGIAN I: VISI EKOSISTEM & ARSITEKTUR 
END-TO-END 
Kekuatan utama bisnis agregator AI bukanlah menciptakan model dari nol, melainkan 
orkestrasi dan efisiensi biaya (arbitrase API & GPU): membeli komputasi secara 
grosir/detikan atau memanfaatkan celah free-tier resmi, lalu menjualnya secara eceran lewat 
antarmuka yang sangat mudah diakses. Kunci agar biaya harian tidak membengkak saat sistem 
berjalan 24 jam penuh adalah memisahkan "Kantor Resepsionis" (yang harus menyala 24 
jam namun sangat ringan) dari "Pabrik Render GPU" (yang hanya menyala saat ada 
pesanan masuk). 
1.1 Bedah Komponen Dasar Arsitektur (End-to-End) 
1.​ Telegram Bot (Etalase, Kasir, & Remote Control): Berfungsi sebagai front-end tempat 
pengguna mengetik perintah (misalnya /buat_video atau /buat_kampanye 'Promo Diskon 
Akhir Tahun'), mengecek saldo kredit, dan membayar lewat QRIS atau pembayaran 
global. Dibangun menggunakan library gratis Aiogram (Python) atau Telegraf (Node.js). 
2.​ Agentic AI / Muse / Orchestrator (Otak & Project Manager Mandiri): Berperan sebagai 
Project Manager Mandiri yang menerima perintah besar dari Telegram, membuat 
roadmap, dan membaginya menjadi subtugas otomatis (Tugas A: Tulis naskah, Tugas B: 
Bikin prompt visual, Tugas C: Bikin gambar/video). Dibangun menggunakan modul 
Python Async Agent mandiri yang bebas dari batas pemakaian personal, atau kerangka 
kerja open-source seperti Hermes Agent / LangGraph. 
3.​ 9Router & OpenRouter (Manajer Distribusi & Penyelamat Token): 
○​ 9Router (decolua/9router): Berjalan di localhost server (http://localhost:20128/v1) 
sebagai pengatur dan pemilah permintaan dari Muse ke API AI. Memiliki fitur 
kompresi token (RTK & Caveman) yang menghemat pemakaian token 20%–65%, 
serta 3-Tier Fallback Otomatis. Jika satu AI habis kuota, otomatis bergeser 
(fallback) ke AI alternatif/gratis (seperti Kiro AI Free, OpenCode Free, Gemini API 
Free Tier, Qwen, Llama, atau NVIDIA NIM) tanpa error. 
○​ OpenRouter: Dipasang di dalam 9Router sebagai cadangan (Tier-2/Tier-3) yang 
menyediakan puluhan model berlabel :free (Llama 3.3, Qwen 2.5, DeepSeek 
R1/V3) serta model berbiaya sangat murah (
0,20 per 1 juta token). 
0, 05–



<!-- [ID:02_CORE_AI_S410] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 664

4.​ Infrastruktur / Server 24 Jam (VPS / Oracle Cloud / PythonAnywhere): Tempat 
menjalankan kode Bot, database pengguna, dan 9Router secara non-stop 24 jam di 
background tanpa mengandalkan Google Colab yang sering terputus. 
○​ Catatan Teknis PythonAnywhere vs. Oracle Cloud: Akun gratis PythonAnywhere 
memblokir koneksi keluar (outbound) ke API di luar whitelist dan membatasi proses 
Node.js (9Router). Untuk server 24 jam bermodal Rp 0 selamanya, gunakan 
Oracle Cloud Free Tier (Ampere A1 ARM: 2–4 OCPU & 12–24 GB RAM gratis 
selamanya + 2 VM AMD Micro) dengan trik upgrade ke status Pay-As-You-Go 
(PAYG) (tagihan tetap Rp 0 selama di dalam batas gratis, bebas error Out of 
Capacity, dan anti-suspend), atau gunakan VPS Linux Ubuntu murah seharga Rp 
20.000–Rp 25.000/bulan. 
5.​ Vast.ai / RunPod / API Grosir (Pabrik Render Video & Gambar): Menyewa GPU 
(minimal 24 GB VRAM seperti NVIDIA RTX 3090 atau RTX 4090) untuk menjalankan 
ComfyUI API (model open-source Wan 2.1/2.2, HunyuanVideo, LTX-Video, Flux) dengan 
sistem On-Demand / Auto-Start & Stop atau Serverless. Untuk model komersial 
tertutup (Kling AI, Google Veo, Runway, Sora, Suno), sistem menembak API grosir 
Pay-Per-Call (Fal.ai, Replicate, Novita AI, PiAPI) tanpa biaya sewa GPU per jam. 
1.2 Spesifikasi 5 Agentic AI dalam Ekosistem bikinAI Super 
Intelligence 
Sistem dirancang ramping menggunakan 5 Agentic AI (1 Koordinator + 3 Pekerja Spesialis + 
1 Agen CS Otomatis): 
Nama Agen 
Peran dalam Sistem 
Model AI (via 9Router / 
OpenRouter) 
Biaya Modal 
1. Gatekeeper & 
Billing Agent 
Mengecek saldo koin 
user secara atomik, 
memvalidasi keamanan 
prompt 
(anti-spam/CSAM), 
mendeteksi bahasa 
pengguna 
(language_code), dan 
memotong kuota 
otomatis setelah 
pembayaran sukses. 
Script Python murni + 
LLM ringan (Qwen / 
Gemini Flash Free) 
Rp 0 
2. Orchestrator Agent 
(Muse/PM) 
Menerima perintah 
kasar dari user di 
Telegram/WA/FB, lalu 
memecahnya menjadi 
roadmap subtugas 
JSON (Naskah, Prompt 
Visual, Audio/Video). 
Claude Sonnet (via Kiro 
Free di 9Router) / 
DeepSeek 
Rp 0 
3. Prompt Engineer & 
Sanitizer Agent 
Mengubah bahasa 
daerah/Indonesia/asing 
pendek dari user 
menjadi prompt bahasa 
Gemini Flash / Llama 
3.3 70B (:free di 
OpenRouter) / Hermes 
3 (jalur Unfiltered) 
Rp 0 



<!-- [ID:02_CORE_AI_S411] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 665

Nama Agen 
Peran dalam Sistem 
Model AI (via 9Router / 
OpenRouter) 
Biaya Modal 
Inggris sinematik 
lengkap dengan 
camera movement dan 
lighting, serta 
melakukan 
Auto-Rewrite agar 
aman bagi API hulu. 
4. Media Worker & 
Compiler Agent 
Mengirim JSON 
workflow ke API 
ComfyUI di 
Vast.ai/RunPod atau 
Fal.ai, memantau 
antrean render 
(polling), menjahit klip 
panjang dengan 
FFmpeg, lalu mengirim 
hasil akhirnya kembali 
ke pengguna. 
Script Python Async + 
Webhook + FFmpeg 
Rp 0 (di luar sewa 
GPU) 
5. AI Support & Triage 
Agent (CS 24 Jam) 
Melayani komplain 
pribadi pelanggan, 
mengecek status 
Job_ID yang gagal 
secara read-only di 
database, memproses 
auto-refund jika terbukti 
timeout, membaca 
bukti transfer dengan 
Vision AI, dan mengirim 
tombol eskalasi 1-klik 
ke Admin. 
Gemini Flash Free / 
Qwen 2.5 72B (via 
9Router) 
Rp 0 
1.3 Kebijakan Mutlak: 100% Legal & Open-Source (Surface Web) 
Seluruh fondasi teknologi berdiri 100% di atas ekosistem open-source resmi dan free-tier legal 
di Surface Web (GitHub, HuggingFace, Civitai, Google AI Studio, OpenRouter, Groq, NVIDIA 
NIM, Cloudflare). Penggunaan sumber dari dark web dihapus dan dieliminasi sepenuhnya 
karena membawa risiko Malware Stealer (pencurian sesi Telegram dan pembelokan webhook 
pembayaran QRIS) serta Downtime Mendadak akibat akun/API curian yang mati dalam 
hitungan jam. 
1.4 Strategi Omnichannel "1 Otak, 3 Pintu" (Telegram, Facebook, 
WhatsApp) 
Untuk menjangkau seluruh lapisan pengguna tanpa biaya pembuatan aplikasi Android/iOS dari 
nol, sistem menggunakan arsitektur Omnichannel Webhook (1 Server Otak Pusat, 3 Pintu 
Masuk) dengan 1 saldo koin yang terhubung lintas platform: 



<!-- [ID:02_CORE_AI_S412] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 678

Node & Vektor Serangan (Red 
Team) 
Kelemahan Solusi Blue Team 
Standar di VPS Kecil 
Solusi Taktis bikinAI Super 
Intelligence (Hemat RAM & 
Anti-Bobol) 
Race Condition (TOCTOU) — 
50 request paralel dalam 1 
milidetik menguras saldo API 
20x lipat dengan modal 1 koin. 
FOR UPDATE (tidak ada di 
SQLite!) atau memasang 
server Redis + Lua yang 
memakan ratusan MB RAM 
VPS. 
bytes RAM) + 1-Baris Atomic 
Conditional UPDATE ... 
RETURNING di SQLite WAL. 
Saldo dipotong (escrow) di 
milidetik pertama sebelum 
menyentuh Router. 
Node 1 (SEC-06): Polyglot File 
Injection & Decompression 
Bomb — File 500 KB meledak 
jadi 16 GB di RAM server. 
Memeriksa di server setelah 
seluruh file selesai diunggah ke 
VPS. 
Client-Side <canvas> 
Re-encoding di HP Pembeli 
(Menggambar ulang foto ke 
.webp maks 1280x1280 di 
browser HP pengguna sebelum 
diunggah—bom piksel & skrip 
ekor langsung hancur di HP 
penyerang!) + 24-Byte Header 
Guard (MAX_IMAGE_PIXELS) 
di server. 
Node 2 & 3 (SEC-01): 
Semantic Router Poisoning / 
Polyglot Prompt — Karakter 
U+200B atau metafora medis 
menipu Router sehingga 
prompt eksplisit nyasar ke API 
SFW dan membuat akun SFW 
diblokir. 
Memasang model CLIP 
Embedding lokal di Router 
yang memakan >2 GB RAM 
VPS. 
NFKC Unicode Strip 
(unicodedata.normalize) + 
Zero-Passthrough Canonical 
Reconstruction: Teks asli 
ketikan user dilarang pernah 
diteruskan mentah ke API 
gambar! Muse menulis ulang 
prompt dari nol, ditambah 
Forced Negative Prompt & 
safety_checker: true di Jalur A 
(SFW) dengan rotasi API Key 
gratis/saldo mikro ($1) via 
9Router. 
Node 4 (SEC-05): Denial of 
Wallet (DoW) — Parameter 
ganjil memicu crash di 95% 
komputasi dan auto-retry 
berantai membakar saldo di 3 
engine. 
Sekadar membatasi retry tanpa 
menyelamatkan komputasi 
yang sudah berjalan 90%. 
Two-Phase Circuit Breaker 
(3-Second Cut-Off): Izinkan 
auto-failover ke Engine B 
hanya jika gagal di bawah 3 
detik (Pre-Flight/Queue Reject 
= Rp 0 terpakai). Jika gagal di 
atas 3 detik (Mid-Compute), 0x 
Failover ke mesin 
lain—langsung masuk ke 
Reconciliation Polling + Preset 
Parameter Clamping 
(pengguna hanya bisa klik 
tombol resolusi kelipatan 64). 
Node 5 (SEC-03): Webhook 
Spoofing & SSRF Media 
Sekadar memblokir daftar IP 
lokal di VPS (rawan ditembus 
Zero-VPS Fetching 
(Cloudflare Edge Fetcher) + 



<!-- [ID:02_CORE_AI_S413] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 679

Node & Vektor Serangan (Red 
Team) 
Kelemahan Solusi Blue Team 
Standar di VPS Kecil 
Solusi Taktis bikinAI Super 
Intelligence (Hemat RAM & 
Anti-Bobol) 
Fetcher — Tembak webhook 
palsu untuk auto-refund koin 
atau curi metadata internal 
169.254.169.254. 
DNS Rebinding). 
Strict Domain Whitelist 
(ALLOWED_UPSTREAM_CD
N) + HMAC Capability Token 
URL + One-Way 
refunded_lock di Database. 
VPS tidak pernah mengunduh 
file dari URL luar! 
Node 6 (SEC-04): 
Side-Channel Timing & Domain 
Association — Membongkar 
hubungan jalur SFW dan 
Unfiltered dari selisih waktu 
respon & domain yang sama. 
Hanya menyeragamkan 
struktur JSON tanpa 
menyamakan waktu tunggu 
respon. 
Constant-Time 50ms Queue 
ACK (Semua request di jalur 
mana pun langsung dibalas 
tiket antrean dalam 50ms yang 
seragam) + Pemisahan domain 
Kasir Utama dari domain 
Ephemeral Edge Worker 
pengirim .bin. 
Bukti Kode Pertahanan Inti (Anti-TOCTOU, Anti-SSRF, & Two-Phase Circuit 
Breaker) 
import asyncio​
import hmac​
import hashlib​
import time​
import unicodedata​
from collections import defaultdict​
from urllib.parse import urlparse​
import aiosqlite​
​

<!-- [ID:02_CORE_AI_S414] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 682

6.1 Tabel Master Link Pendaftaran Resmi (Diurutkan Berdasarkan 3 
Gelombang Prioritas) 
Gelombang Prioritas 
Nama Layanan & 
Tautan Resmi 
Fungsi Utama dalam 
Sistem Kita 
Biaya 
🟢 GELOMBANG 1 
(Wajib Daftar di Awal 
untuk Tahap 1, 2 & 
Mode Testing Rp 0) 
1. Telegram 
BotFather: 
[https://t.me/BotFather](
https://t.me/BotFather) 
2. 9Router Repo: 
[https://github.com/dec
olua/9router](https://gith
ub.com/decolua/9router
) 3. Google AI Studio 
(Gemini API): 
[https://aistudio.google.
com/app/apikey](https:/
/aistudio.google.com/ap
p/apikey) 4. Groq 
Cloud (Llama 3.3 & 
Whisper): 
[https://console.groq.co
m/keys](https://console.
groq.com/keys) 5. 
OpenRouter (:free 
LLM): 
[https://openrouter.ai/se
ttings/keys](https://open
router.ai/settings/keys) 
6. Cloudflare (Pages, 
R2 10GB, Workers & 
AI): 
[https://dash.cloudflare.
com/sign-up](https://da
sh.cloudflare.com/sign-
up) 7. Oracle Cloud 
Free Tier (VPS 24/7): 
[https://www.oracle.com
/cloud/free/](https://ww
w.oracle.com/cloud/free
/) 8. Pollinations AI 
(Sandbox Media 
Gratis): 
[https://pollinations.ai/](
https://pollinations.ai/) 
9. AWS Builder ID 
(Kiro AI Free di 
Membangun Bot 
Utama, Grup Forum 
Komunitas, Dapur 
9Router + Muse, 
Database Koin, Mini 
App / Web Studio 
Terenkripsi (.bin), serta 
Uji Coba Generate 
Gambar/Video Mode 
Sandbox [1]. 
Rp 0 (100% Gratis) 



<!-- [ID:02_CORE_AI_S415] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 685

Gelombang Prioritas 
Nama Layanan & 
Tautan Resmi 
Fungsi Utama dalam 
Sistem Kita 
Biaya 
hub.com/devlikeapro/w
aha) 
6.2 Panduan Eksekusi Tahap 1 hingga Tahap 5 (Roadmap 
Implementasi) 
Tahap 1: Setup Markas, 3 Bot Ekosistem, & Grup Forum Komunitas Telegram 
1.​ Buat 3 Bot di @BotFather: 
○​ Bot #1 (TOKEN_BOT_UTAMA): bikinAI Super Intelligence ⚡ (Kasir, Chat 
Multimodal, & Studio SFW). 
○​ Bot #2 (TOKEN_BOT_ACTIVITY): bikinAI Activity & Creative Bot 🤖 (Pelapor 
otomatis ke topik Activity Bot, Asisten Grup di Creative Assistance, dan CS AI 24 
jam). Wajib matikan /setprivacy \rightarrow Disable pada Bot #2. 
○​ Bot #3 (TOKEN_BOT_CADANGAN): bikinAI Backup Studio (Cadangan pemulihan 
10 detik). 
2.​ Pasang Daftar Command (/setcommands), Bio SEO 120 Karakter (/setabouttext), & 
Deskripsi (/setdescription) pada Bot #1. 
3.​ Buat 1 Supergroup Telegram (bikinAI Sharing Area & Community), Aktifkan Fitur 
Topics, dan Buat 6 Kamar Topik: 
○​ 📈 Activity Bot (Kunci Topik / Close Topic) 
○​ 📢 Pengumuman & Info (Kunci Topik / Close Topic) 
○​ 📚 Tutorial & Klaim Harian (Kunci Topik / Close Topic) 
○​ 🤖 Creative Assistance (Biarkan Terbuka) 
○​ 💡 Belajar & Sharing Karya (Biarkan Terbuka) 
○​ ⁉️ Laporan Error & Saran (Biarkan Terbuka) 
4.​ Angkat Bot #1 dan Bot #2 menjadi Administrator Grup (nyalakan izin Manage Topics, 
Delete Messages, Invite Users, Pin Messages). 
5.​ Ambil Data ID Konfigurasi: 
○​ Salin tautan topik (Copy Topic Link) dari 📈 Activity Bot dan 🤖 Creative Assistance 
(contoh: [https://t.me/c/1234567890/5](https://t.me/c/1234567890/5)). Tambahkan 
-100 di depan angka tengah untuk mendapatkan GROUP_CHAT_ID 
(-1001234567890), dan ambil angka ujung belakang sebagai TOPIC_ID_ACTIVITY 
(5) serta TOPIC_ID_ASSISTANCE. 
○​ Ambil ADMIN_USER_ID pribadi Anda melalui @userinfobot. 
Tahap 2: Instalasi Server 24 Jam & Dapur 9Router 
●​ Menyiapkan VPS Linux Ubuntu (Oracle Cloud Free Tier / VPS ringan), memasang 
Node.js, Python 3.11+, dan FFmpeg. 
●​ Menjalankan npm install -g 9router di background (pm2) dan mengonfigurasi 3-Tier 
Fallback (Kiro/Gemini/Groq Gratis \rightarrow OpenRouter :free \rightarrow Cadangan 
Murah). 
Tahap 3: Perakitan 6 Modul Kode Inti Python (Utuh & Terisolasi) 



<!-- [ID:02_CORE_AI_S416] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 2. KAMUS 25 DOMAIN + MESIN AUTO-DISCOVERY AKTIF (MENANGKAP SEMUA 
LABEL LIAR)​
# 
======================================================================
========​
DOMAIN_SCHEMA = {​
    "01_ARCH": ["monorepo", "tech stack", "microservice", "env", "api 
gateway", "dependency", "arsitektur", "architecture"],​
    "02_CORE_AI": ["llm", "router", "sota", "rag", "memory", "fine 
tuning", "fine-tuning", "fallback", "embedding", "prompt"],​
    "03_V_OFFICE": ["177 agen", "kantor virtual", "virtual office", 
"org chart", "state machine", "message broker", "consensus", 
"handoff", "shift", "agent_"],​
    "04_PROMPT_LIB": ["system prompt", "few shot", "few-shot", "json 
schema", "negative prompt", "chain template"],​
    "05_TOOLS_ENGINE": ["playwright", "puppeteer", "ffmpeg", "mcp", 
"browser agent", "file converter", "search api"],​
    "06_AGGREGATOR": ["scraper", "scraping", "spider", "crawler", 
"aggregator", "social listener", "market spy", "deduplicator", 
"normalizer"],​
    "07_CONTENT_FACTORY": ["copywriting", "script director", "video 
assembler", "carousel", "localization", "quality gate", "pabrik 
aset"],​
    "08_OMNI_SOCIAL": ["whatsapp", "telegram", "instagram", 
"facebook", "threads", "tiktok", "comment bot", "sosial media", 
"auto-upload"],​
    "09_COMMERCE_AFF": ["affiliate", "marketplace", "cloaking", 



<!-- [ID:02_CORE_AI_S417] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# Inisialisasi Matrix Factorization Router (Hemat 85% Token)
client = Controller(
    routers=["mf"],
    strong_model="gemini-2.5-pro",
    weak_model="groq/llama-3.3-70b-versatile",
    config={"mf": {"checkpoint_path": "routellm/mf_gpt4_augmented"}}
)


<!-- [ID:02_CORE_AI_S418] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# Request cerdas ber-threshold 0.11593
response = client.chat.completions.create(
    model="router-mf-0.11593",
    messages=[{"role": "user", "content": user_prompt}]
)


<!-- [ID:02_CORE_AI_S419] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## AI
- <isi provider utama>
- Fallback: <isi>


<!-- [ID:02_CORE_AI_S420] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Langkah kerja
1. Load brain + memory.
2. Baca task_spec dari orchestrator.
3. Cek gate: apakah aksi menyentuh FIN/LEG/PUB/INC/PPL/STR/DEP/CHAIN?
4. Jika ya → kirim ke ApprovalBroker, tunggu keputusan.
5. Jika tidak → eksekusi, tulis artifact, audit, handoff.
6. Tulis ringkasan ke memory/last_summary.md.


<!-- [ID:02_CORE_AI_S421] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# Memory — {name} ({id})

- `last_summary.md` — ringkasan kerja terakhir (≤ 500 kata).
- `context.json` — state terstruktur (task aktif, prioritas).
- `history/` — arsip per tanggal.

Aturan: memory hanya append. Rotasi > 30 hari → `history/`.


<!-- [ID:02_CORE_AI_S422] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# Tools — {name} ({id})

Tool yang boleh dipakai agent ini. Akses sesuai `tools` di `agents.yaml`.
Default: llm, memory, audit. Tool tambahan wajib approval X002.


<!-- [ID:02_CORE_AI_S423] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# AI Gateway

Satu pintu untuk semua panggilan LLM. Tidak ada agent yang boleh panggil
provider langsung.


<!-- [ID:02_CORE_AI_S424] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Aturan
1. Semua panggilan lewat `/chat` dengan `INTERNAL_KEY`.
2. Cost guard dicek sebelum panggil. Kalau budget habis → tolak.
3. Fallback berjenjang: primary → fallback → local.
4. Setiap panggilan diaudit (agent, provider, model, token, USD, latency).


<!-- [ID:02_CORE_AI_S425] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## PROTOKOL 3: ZERO-HARDCODE & PORTABILITAS INFRASTRUKTUR
1. **Larangan Hardcode:** DILARANG KERAS menulis API Key, Token PAT, System Prompt, URL Webhook, alamat IP, atau path direktori lokal secara permanen (hardcoded) di dalam file kode mana pun.
2. **Abstraksi Dinamis:** Seluruh konfigurasi URL repositori, domain aktif, dan System Prompt harus dipanggil secara dinamis pada saat runtime dari database Turso (`infrastructure_registry` dan `ai_prompts_vault`) menggunakan variabel lingkungan (`os.getenv`).
3. **Aturan Kelengkapan Kode:** Saat memperbarui atau memperbaiki file yang sudah ada, dilarang menghapus atau mengurangi fungsionalitas yang sudah berjalan. Hanya tambahkan fitur baru atau perbaiki blok yang rusak secara utuh.


<!-- [ID:02_CORE_AI_S426] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# - Parallel Hedged AI Router (<3.5s Fast-Reply, Anti-macet 2-3x tanya!)

<!-- [ID:02_CORE_AI_S427] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 7. PARALLEL HEDGED AI ROUTER (<3.5s FAST-FAIL, TIDAK PERLU TANYA 2-3 KALI!)

<!-- [ID:02_CORE_AI_S428] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 4. SMART ROUTER v4.0, 8-AGENT ROLLING POOL, BITTENSOR SUBNET 27 & SOTA AUDIO

<!-- [ID:02_CORE_AI_S429] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 6 CALLBACK ROUTERS UTUH (menu:*, wiz:*, drv:*, adm:*, bns:*, bind:*)

<!-- [ID:02_CORE_AI_S430] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ## BAGIAN C — ROLE ROUTER (STATIS)
Sebelum menjawab, klasifikasikan ke SATU domain:

- CODING/ARCH (Frontier Level Max)
- BIZ/MARKET (harga, positioning, kompetitor, GTM, WTP, PNL, Frontier Level Free Tier Growth Hack Mindset)
- OPS (infra, biaya, monitoring, SLA, otomasi)
- SECURITY/LEGAL (threat model, compliance, ToS, privasi)
- PRODUCT/UX (fitur, alur, prioritas roadmap)

Aturan:

1. Jawab HANYA di domain relevan. Jangan menyeret ke arsitektur
  kecuali user minta atau minta multi-perspektif.
2. Ambigu → tanya: "Ini mau dijawab dari sisi BIZ atau ARCH?"
3. Multi-perspektif → label: BIZ: / ARCH: / OPS: / dll.
4. Jika user menyebut "all-in-one" atau "gabungkan semua":
  beri jawaban berlabel per domain, urut dari yang paling
  dibutuhkan user saat itu.

====================================================================

<!-- [ID:02_CORE_AI_S431] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ## BAGIAN C — ROLE ROUTER (STATIS)
Sebelum menjawab, klasifikasikan ke **SATU** domain:

- **CODING**/**ARCH** (Frontier Level Max)
- **BIZ**/**MARKET** (harga, positioning, kompetitor, **GTM**, **WTP**, **PNL**, Frontier Level Free Tier Growth Hack Mindset)
- **OPS** (infra, biaya, monitoring, **SLA**, otomasi)
- **SECURITY**/**LEGAL** (threat model, compliance, ToS, privasi)
- **PRODUCT**/UX (fitur, alur, prioritas roadmap)

Aturan:

<!-- [ID:02_CORE_AI_S432] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# === 1. TELEGRAM & OMNICHANNEL === TOKEN_BOT_UTAMA="" TOKEN_BOT_ACTIVITY="" TOKEN_BOT_CADANGAN="" ADMIN_USER_ID="" GROUP_CHAT_ID="-100..." TOPIC_ID_ACTIVITY="" TOPIC_ID_ASSISTANCE="" # === 2. FRONTIER COGNITIVE & 9ROUTER (KATEGORI 1 - GRATIS) === GEMINI_API_KEY="" GROQ_API_KEY="" OPENROUTER_API_KEY="" NVIDIA_NIM_API_KEY="" SILICONFLOW_API_KEY="" TURSO_DATABASE_URL="" TURSO_AUTH_TOKEN="" # === 3. STORAGE, PAYMENT & MEDIA (KATEGORI 1 & 2) === CLOUDFLARE_ACCOUNT_ID="" PAKASIR_API_KEY="" CRYPTOBOT_API_TOKEN="" FAL_KEY="" NOVITA_API_KEY="" 

B. Keamanan & Stabilitas (Priority #1 — Isolasi Kartu Visa & Kredensial)

• Aturan Isolasi Kartu Debit Visa (FIN-SEC-01): Jika Anda menggunakan aplikasi bank digital seperti Bank Jago (atau Jenius), buatlah 1 Kantong Baru bernama "Vault API bikinAI" dan terbitkan 1 Kartu Debit Visa Virtual khusus yang terhubung ke kantong tersebut. Jangan pernah menautkan kartu dari kantong tabungan utama Anda ke website mana pun di Kategori 2.

• Aturan Zero-Commit pada GitHub: File .env yang berisi kumpulan kunci di atas wajib dimasukkan ke dalam daftar .gitignore sejak detik pertama agar tidak pernah terunggah secara tidak sengaja ke repositori GitHub dan dipindai oleh bot scanner publik.

C. Strategi Bisnis, Marketing Teknis, & ROI Realistis (Memanfaatkan Kredit Gratis Pendaftaran)

• Saat Anda mendaftar akun di NVIDIA NIM (#8), SiliconFlow (#9), Novita AI (#20), dan Fal.ai (#19), penyedia tersebut sering memberikan Bonus Kredit Pendaftaran Awal (Sign-up Free Credits senilai $0,50 hingga $5+).

• Dengan menggabungkan kredit sambutan gratis tersebut bersama mode Sandbox Pollinations (#29) dan kuota gratis Gemini/Groq/OpenRouter, Anda sudah bisa menghasilkan puluhan video dan ratusan gambar HD promosi pertama untuk dipamerkan di Facebook dan Grup Telegram Anda dengan pengeluaran uang tunai Rp 0, lalu menggunakan uang Top-Up dari pelanggan pertama untuk mulai memutar mesin Autonomous Treasury Anda!

Silakan Anda kerjakan pendaftaran Kategori 1 (No. 1 s/d 17) sekarang. Begitu sudah terkumpul di Notepad Anda, langsung beri komando "Mulai Tahap 2"!
```
