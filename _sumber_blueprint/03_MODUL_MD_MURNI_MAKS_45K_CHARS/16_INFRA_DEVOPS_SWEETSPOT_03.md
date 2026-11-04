
<!-- [ID:16_INFRA_DEVOPS_S022] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 69

Kasta / Tier 
Pilihan Engine AI 
di Dalamnya 
Harga ke User 
(Koin / Rupiah) 
Modal Anda (HPP) Margin Laba 
🟢 TIER ECO 
(Gratis / 
Pemancing) 
• Chat, Coding & 
Baca PDF: Gemini 
Flash, Qwen 2.5, 
Llama 3.3, 
DeepSeek (via 
9Router) • 
Gambar Draft: 
Flux Schnell 
0 Koin (Gratis) 
(30 chat/hari, atau 
Unlimited bagi 
yang pernah 
top-up) 
Rp 0 
Penarik trafik & 
user retention 
🔵 TIER PRO 
(Andalan Margin 
Tebal) 
• Otak 
Kampanye: Muse 
+ Claude (via 
9Router) • 
Gambar HD & 
Upscale 4K: 
Flux.1 Dev / 
Real-ESRGAN • 
Video AI: Wan 2.1 
/ 2.2 (T2V, I2V, 
Motion VACE), 
LTX-Video, 
Hunyuan (via GPU 
Vast.ai / RunPod) 
• Gambar HD / 
Upscale: 4–5 Koin 
(Rp 400–500) • 
Video 5 dtk: 20 
Koin (Rp 2.000) • 
Paket Kampanye 
Utuh: 25 Koin (Rp 
2.500) 
• Gambar: ~Rp 
0–25 • Video: ~Rp 
300–500 • 
Kampanye: ~Rp 
350 
~80% – 85% 
🟣 TIER ULTRA 
(Model Komersial 
Flagship) 
• Video Flagship 
& Motion: Kling 
1.6/2.6/3.0 (Std & 
Pro), Seedance, 
Google Veo, Sora, 
Runway • Musik 
Studio: Suno 
v4/v6 Studio & 
Udio • Chat 
Flagship: Claude 
Sonnet/Opus 
Resmi 
• Musik Suno: 15 
Koin (Rp 1.500) • 
Video Flagship: 
25–50 Koin (Rp 
2.500 – Rp 5.000) 
• Chat Flagship: 2 
Koin (Rp 200) 
Ditembak via API 
pay-per-use (Fal.ai 
/ Replicate / Novita 
/ PiAPI) tanpa 
sewa GPU per 
jam. Modal Video: 
~Rp 1.500–2.500 
~45% – 50% (0% 
Risiko GPU 
Menganggur!) 
B. Tabel Harga Jual Video Berdasarkan Durasi (Solusi Atas Kelemahan 
Kompetitor) 
Di grup kompetitor, pengguna mengeluhkan tidak bisa membuat video Text-to-Video berdurasi 
30 detik. Di sistem kita, Muse otomatis memecah naskah 30 detik menjadi 6 adegan \times 5 
detik, merendernya di GPU, lalu menggabungkannya secara otomatis dengan FFmpeg beserta 
musik/narasi suara menjadi 1 video utuh: 
Jenis Layanan 
Video 
Durasi 
Harga ke User 
(Koin / Rupiah) 
Modal GPU Anda 
(HPP) 
Keuntungan 
Bersih 
Video Klip 
Standar 
5 Detik 
20 Koin (Rp 
2.000) 
~Rp 200 – Rp 350 ~Rp 1.650 / video 



<!-- [ID:16_INFRA_DEVOPS_S023] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 70

Jenis Layanan 
Video 
Durasi 
Harga ke User 
(Koin / Rupiah) 
Modal GPU Anda 
(HPP) 
Keuntungan 
Bersih 
(720p/1080p) 
Video Klip 
Panjang / HD 
10 Detik 
35 Koin (Rp 
3.500) 
~Rp 500 – Rp 700 ~Rp 2.800 / video 
Paket Story / 
Iklan Utuh (6 Klip 
+ Jahit FFmpeg + 
Voiceover/Musik) 
30 Detik 
100 Koin (Rp 
10.000) 
~Rp 1.800 – Rp 
2.200 
~Rp 7.800 / video 
2.5 Tabel Simulasi Prediksi Keuntungan Bulanan 
Asumsi menggunakan Skema Stabil (Biaya tetap VPS + cadangan LLM = Rp 41.000/bulan), 
harga jual rata-rata Rp 2.000/video, dan HPP GPU rata-rata Rp 350/video: 
Skala Trafik 
Harian 
Total Video / 
Bulan 
Omzet Kotor 
(Rp 
2.000/video) 
Biaya Server 
24 Jam + 
LLM 
Biaya GPU 
(Vast.ai / 
RunPod) 
Potongan 
QRIS 
(~0,7%) 
Laba Bersih 
/ Bulan 
Sepi (10 
video/hari) 
300 video 
Rp 600.000 Rp 41.000 
Rp 105.000 Rp 4.200 
Rp 449.800 
Sedang (50 
video/hari) 
1.500 video Rp 
3.000.000 
Rp 41.000 
Rp 525.000 Rp 21.000 
Rp 
2.413.000 
Ramai (200 
video/hari) 
6.000 video Rp 
12.000.000 
Rp 75.000 
(upgrade 
VPS) 
Rp 
1.800.000 
(semakin 
hemat krn 
antrean 
padat) 
Rp 84.000 
Rp 
10.041.000 
BAGIAN III: STRATEGI AKUISISI PASAR, BEDAH 
KOMPETITOR, & RETENSI PENGGUNA 
3.1 5 Alasan Pengguna Pindah dari Aplikasi Gratis (Gemini/Dola) & 
Rela Membayar di Bot Kita 
1.​ Super-App Satu Pintu Tanpa Pindah Aplikasi: Pengguna tidak perlu menginstal 5 
aplikasi berbeda yang memakan memori HP; chat, baca PDF, buat gambar, musik Suno, 
hingga video selesai di dalam Telegram/WA/FB mereka. 
2.​ Eksekusi "1 Perintah Jadi Paket Kampanye Utuh" (Muse Orchestrator): Cukup ketik 
1 kalimat perintah, Muse langsung menghasilkan Naskah Copywriting + Prompt Visual + 
Poster + Video sekaligus. 
3.​ Bayar Eceran (Pay-As-You-Go) Rp 2.000 via QRIS: Aplikasi resmi membatasi kuota 
video harian dan mengharuskan langganan Rp 320.000/bulan ($20) dengan kartu kredit. 
Di bikinAI, pengguna bisa beli eceran Rp 2.000–Rp 5.000 kapan saja lewat QRIS. 
4.​ Preset Lokal & Komersial Siap Klik: Tombol siap pakai seperti "Video Affiliate TikTok", 
"Foto Produk UMKM Jadi Studio Mewah", dan "Motion Control Dance". 
5.​ Efek Viral Watermark Gratis: Hasil generate dari koin klaim harian gratis menyertakan 
watermark halus @bikinAI_bot di sudut video, menjadi iklan gratis setiap kali dibagikan 



<!-- [ID:16_INFRA_DEVOPS_S024] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# [2] Mode API Grosir Pay-Per-Generate (Fal.ai / Replicate / Novita / 
PiAPI - Tanpa sewa GPU per jam)​



<!-- [ID:16_INFRA_DEVOPS_S025] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# [3] Mode Pabrik GPU Mandiri (Vast.ai / RunPod 24GB VRAM ComfyUI 
Serverless/Auto-Stop)​
PILIHAN_MESIN_MEDIA = 1​
​

<!-- [ID:16_INFRA_DEVOPS_S026] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# [3] Groq Cloud Super-Fast (Llama 3.3 70B Gratis - Kecepatan 0.2 
detik)​

<!-- [ID:16_INFRA_DEVOPS_S027] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 76

Kode & Tahap Pertahanan 
Ancaman Fatal yang Dicegah Mekanisme Teknis Pertahanan 
di Sistem Kita 
Tahap 3: Pre-Inference 
Guardrail AI-SEC-01, 
AI-SEC-02 
• Token Smuggling / bahasa 
slang yang menembus filter 
kata biasa (AI-SEC-01). • 
Liabilitas hukum berat akibat 
pengguna mengunggah foto 
orang nyata/selebriti tanpa izin 
atau anak di bawah umur pada 
fitur Img2Img / Image-to-Video 
(AI-SEC-02). 
• Filter Multibahasa & 
Pre-Inference Vision Gate: 
Memindai konteks semantik 
kalimat serta memasang 
pemeriksa wajah otomatis 
(InsightFace Age/Gender 
Classifier + Hash Check) di 
memori yang menolak otomatis 
foto wajah dengan estimasi 
usia di bawah 21–23 tahun 
sebelum masuk ke antrean 
GPU. 
Tahap 4: Antrean & 
Orkestrasi 
• Tabrakan VRAM GPU saat 
pesanan membludak & 
kehilangan status (state) saat 
layar ditutup. 
• Persistent Async Queue: 
Mengatur antrean secara 
asinkron dan menyimpan 
Job_ID secara terpisah dari 
mesin GPU untuk menjaga 
kontinuitas alur kerja. 
Tahap 5: Stateless GPU 
Worker GPU-01 
• Penyadapan model, log 
prompt, atau file gambar oleh 
pemilik fisik mesin (host node) 
di marketplace GPU seperti 
Vast.ai (GPU-01), serta output 
anatomi ilegal. 
• RAM-Only Processing 
(/dev/shm) & Negative 
Tensor: Menyuntikkan 
Negative Embedding 
Permanen 
(anti-minor/anti-gore) langsung 
di level tensor conditioning 
GPU, memproses seluruh file 
murni di memori volatil 
/dev/shm (tmpfs berbasis RAM 
Linux) tanpa pernah menyentuh 
hardisk fisik, lalu langsung 
menghancurkannya 
(zero-overwrite) setelah 
dienkripsi dengan AES-GCM. 
Tahap 6: Zero-Knowledge 
CDN INFRA-01, WV-01 
• Pemindai otomatis 
Cloud/CDN (Cloudflare R2 / 
S3) yang men-suspend akun 
karena mendeteksi file 
.png/.mp4 dewasa (INFRA-01). 
• Crash layar putih di iPhone 
akibat batas memori iOS 
WKWebView Jetsam RAM 
Limit (WV-01). 
• Client-Side Encrypted Blob 
Delivery (.bin): CDN hanya 
menyimpan dan 
mendistribusikan file biner 
terenkripsi (.bin) yang mustahil 
dipindai sensor cloud. Browser 
pengguna mendekripsinya 
langsung di RAM via Web 
Crypto API 
(window.crypto.subtle) 
menjadi Blob URL, dipadukan 
dengan Virtual Scrolling 



<!-- [ID:16_INFRA_DEVOPS_S028] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 77

Kode & Tahap Pertahanan 
Ancaman Fatal yang Dicegah Mekanisme Teknis Pertahanan 
di Sistem Kita 
(hanya merender 4–6 item di 
layar) dan 
URL.revokeObjectURL() 
otomatis agar iPhone tidak 
pernah crash. 
5.3 Solusi Cerdas Atas Risiko Hukum & 5 Masalah Kritis Agregator 
(AGG-01 s/d AGG-05) 
Sekadar memasang checkbox "Saya berusia 18+ dan untuk penggunaan pribadi" atau 
ancaman "Menuntut balik pengguna" tidak memberikan kekebalan hukum (null and void 
terhadap tindak pidana, menciptakan jebakan Self-Incrimination, dan tidak dibaca oleh robot 
moderator platform). Perlindungan sesungguhnya dicapai melalui Safe Harbor via Technical 
Due Diligence serta penutupan 5 Celah Agregator (AGG-01 s/d AGG-05) dengan rekayasa 
cerdas berikut: 
Identifikasi Masalah Agregator Kelemahan Solusi Standar 
Solusi Lebih Cerdas di bikinAI 
Super Intelligence 
AGG-01 & AGG-02: Jebakan 
Master API Key Disita & Ilusi 
"Hanya Perantara" (Satu 
pembeli nakal membuat deposit 
API Rp 5 juta kita diblokir 
provider hulu). 
Menolak prompt mentah dan 
menghanguskan saldo pembeli 
setelah 3x pelanggaran 
(memicu pembeli marah dan 
melaporkan rekening QRIS kita 
ke bank). 
1. Pre-Flight Guardrail di Rp 
0: Tolak mutlak CSAM/wajah 
anak/artis di gerbang lokal 
sebelum menyentuh Master 
API Key (modal terpakai Rp 0, 
akun di-cooldown tanpa 
merampas uang yang memicu 
laporan bank). 2. Muse 
Auto-Rewrite: Untuk prompt 
yang sekadar nyerempet/kasar, 
Muse otomatis menulis ulang 
kalimatnya menjadi prompt fiksi 
dewasa (>25 tahun) yang 
sopan dan aman bagi API hulu. 
AGG-03: Kebocoran Dapur 
Bisnis (Inspect Element URL 
asli), Link Mati 15 Menit, & 
Blokir ISP Indonesia 
(TrustPositif/Komdigi). 
Menyuruh VPS backend 
mengunduh semua video dari 
engine pusat, menghapus EXIF 
dengan FFmpeg, lalu 
mengunggahnya ke R2 
(membuat CPU & RAM VPS 
murah langsung 100% dan 
mati!). 
Cloudflare Workers Zero-VPS 
Edge Relay: Jangan lewatkan 
file video ke VPS Bot! Gunakan 
Cloudflare Workers (gratis 
100.000 request/hari) untuk 
menyedot file langsung dari 
URL engine hulu di jaringan 
Edge 10 Gbps, melucuti header 
metadata/EXIF secara 
streaming, mengenkripsinya ke 
.bin, dan menyimpannya ke R2. 
Beban VPS 0%, dapur API 
tersembunyi rapat, dan bebas 
blokir ISP Indonesia tanpa 
VPN! 



<!-- [ID:16_INFRA_DEVOPS_S029] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 85

Gelombang Prioritas 
Nama Layanan & 
Tautan Resmi 
Fungsi Utama dalam 
Sistem Kita 
Biaya 
(Daftar Saat Trafik 
Tinggi, Pabrik GPU 
Mandiri & Ekspansi 
WA/FB) 
24GB Termurah): 
[https://cloud.vast.ai/](ht
tps://cloud.vast.ai/) 19. 
RunPod (Secure 
Cloud & Serverless 
GPU): 
[https://www.runpod.io/]
(https://www.runpod.io/) 
20. HuggingFace 
Token: 
[https://huggingface.co/
settings/tokens](https://
huggingface.co/settings
/tokens) 21. Civitai API 
Key: 
[https://civitai.com/user/
account](https://civitai.c
om/user/account) 22. 
InsightFace (Vision 
Gate Usia >23 Thn): 
[https://github.com/dee
pinsight/insightface](htt
ps://github.com/deepins
ight/insightface) 23. 
OpenAI Moderation 
API (Gratis): 
[https://platform.openai.
com/api-keys](https://pl
atform.openai.com/api-
keys) 24. Backblaze 
B2 (Cadangan R2 
10GB): 
[https://www.backblaze.
com/cloud-storage](http
s://www.backblaze.com
/cloud-storage) 25. 
Meta Developers (FB 
& WA Resmi): 
[https://developers.face
book.com/](https://deve
lopers.facebook.com/) 
26. WAHA (WhatsApp 
HTTP API Gratis): 
[https://github.com/devli
keapro/waha](https://git
PILIHAN_MESIN_MED
IA = 3 (Pabrik GPU 
24GB VRAM sendiri di 
/dev/shm), 
mengaktifkan Vision 
Gate, dan membuka 
pintu WhatsApp & 
Facebook Messenger. 



<!-- [ID:16_INFRA_DEVOPS_S030] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 87

●​ Modul 1 (config_and_db.py): Panel Saklar 1 Angka, sistem 2 Dompet (koin_utama & 
koin_bonus), sistem Universal Compute Voucher, serta fungsi atomic_escrow_charge 
(Anti-TOCTOU SEC-02). 
●​ Modul 2 (security_gate.py): Verifikasi HMAC-SHA256 initData (60 detik) + JWT 
(API-01), sanitasi Unicode NFKC (SEC-01), pembatas piksel 24-byte header (SEC-06), 
serta Pre-Inference Vision Gate InsightFace (AI-SEC-02). 
●​ Modul 3 (muse_router.py): Otak Agentic Orchestrator (Project Manager), deteksi 
bahasa otomatis, Pre-Flight Heat Score Router, dan Auto-Rewrite. 
●​ Modul 4 (stateless_gpu_worker.py): Koneksi 3 mode mesin media, Two-Phase Circuit 
Breaker (3-Second Cut-Off) + Reconciliation Polling (SEC-05), pemrosesan RAM 
/dev/shm (GPU-01), jahit video FFmpeg, dan enkripsi output AES-GCM .bin (INFRA-01). 
●​ Modul 5 (payment_and_support.py): Kasir ganda (QRIS Otomatis Indonesia + 
Telegram Stars/Crypto Global), Decoupled SaaS Billing, program Affiliate, serta AI 
Support & Triage Agent (CS Otomatis + safe_one_time_refund Anti-Spoofing SEC-03). 
●​ Modul 6 (main_bot.py): Antarmuka utama Sultan Super-App, Auto-Intent Detection 
(Teks/Foto/PDF/Suara), pengirim laporan ke topik 📈 Activity Bot, dan asisten grup 🤖 
Creative Assistance. 
Tahap 4 & Tahap 5: Peluncuran Mini App / Website Independen & Omnichannel 
WA/FB 
●​ Memasang miniapp_studio.html & Cloudflare Worker Edge Relay (lengkap dengan 
Zero-Trust Decoy Landing Page, dekripsi Web Crypto API .bin, Virtual Scrolling, 
Client-Side <canvas> Re-encoding, dan Auto-Blur). 
●​ Menyambungkan webhook ke WhatsApp (WAHA / Cloud API) dan Facebook Messenger. 
Cara Menyimpan Dokumen Ini Menjadi File PDF di Perangkat Anda: Anda dapat langsung 
menekan tombol Salin (Copy) pada balasan ini lalu menempelkannya ke Google Docs / 
Microsoft Word dan pilih Download as PDF, atau tekan Ctrl + P (Print to PDF) langsung dari 
browser Anda. Seluruh tabel, kode pertahanan, dan daftar tautan di atas telah disusun dengan 
format cetak standar agar siap menjadi dokumen pegangan riset Anda sebelum kita melangkah 
ke eksekusi teknis berikutnya. 



<!-- [ID:16_INFRA_DEVOPS_S031] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 90

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
Panel Kontrol & 
Manajemen 
Cloudflare Dashboard 
+ Wrangler CLI 
DevilWEB Panel + 
SSH (Serv00) atau 
VistaPanel/cPanel 
(InfinityFree) 
Alwaysdata PaaS 
Admin Panel + 
SSH/SFTP 
Database Gratis 
Cloudflare D1 (5 GB 
SQL) atau Turso (5 GB 
Edge SQLite) 
MySQL 8.0 / 
PostgreSQL 16 
bawaan Serv00 (hingga 
13 DB) 
Supabase (500 MB 
Postgres + Auth) atau 
Neon (0,5 GB 
Postgres) 
Email Custom (Terima 
& Kirim) 
Cloudflare Email 
Routing (Inbox) + 
Brevo SMTP (300 
email/hari via Gmail) 
Cloudflare Email 
Routing + Zoho Mail 
Forever Free (5 user, 
khusus 1 domain) 
Cloudflare Email 
Routing (Inbox) + 
Resend SMTP (100 
email/hari via Gmail) 
Template CSS & UI 
Library 
ThemeWagon Astro 
(AstroWind / Astroship) 
+ daisyUI 
HTML5 UP (Phantom / 
Directive) atau 
StartBootstrap 
(Bootstrap 5) 
ThemeWagon 
React+Vite (Aurora 
Free / DashDarkX) + 
shadcn/ui 
Form, Analitik & 
Monitoring 
Web3Forms + 
Cloudflare Web 
Analytics + 
UptimeRobot 
Forminit (support file 
25 MB) + Cloudflare 
Analytics + Better 
Stack 
Web3Forms (unlimited 
domain) + Umami 
Cloud + UptimeRobot 
1. Perburuan Domain Gratis dan Promo Ekstrem 
(Status Live: 30 Oktober 2026) 
Fenomena ribuan situs berakhiran .my.id, .biz.id, .tech, hingga .us.kg yang bertebaran saat ini 
berasal dari dua jalur distribusi utama: program public namespace terbuka berbiaya Rp 0 yang 
mendukung integrasi Nameserver (NS) eksternal ke Cloudflare secara penuh, serta promo 
akuisisi pengguna baru pada tahun pertama dari registrar lokal Indonesia yang disubsidi oleh 
program promosi registri PANDI. 
Jalur A: Domain 100% Gratis (Rp 0 Tanpa Kartu Kredit) dengan 
Dukungan Cloudflare DNS 
Apabila Anda tidak ingin mengeluarkan biaya sepeser pun hari ini, hindari layanan domain 
gratis lawas yang sudah dihentikan (seperti Freenom .tk, .ml, atau .cf yang telah digugat secara 
hukum) dan beralihlah ke penyedia aktif tahun 2026 yang mengizinkan delegasi Nameserver 
(NS) langsung ke akun Cloudflare Anda. Pilihan utama yang paling fleksibel adalah DigitalPlat 
FreeDomain (domain.digitalplat.org / dash.domain.digitalplat.org), sebuah proyek open-source 
berlisensi AGPL-3.0 yang dikelola oleh organisasi nirlaba DigitalPlat Foundation dengan 
sponsor dari The Hack Foundation. Melalui dashboard resminya, Anda dapat mendaftarkan 
domain publik di bawah lima ekstensi aktif yaitu .dpdns.org, .us.kg, .qzz.io, .xx.kg, dan .qd.je. 
Meskipun secara teknis merupakan subdomain tingkat kedua, ekstensi ini berfungsi layaknya 
domain tradisional dan menerapkan prinsip Bring Your Own DNS tanpa hosting lock-in, 



<!-- [ID:16_INFRA_DEVOPS_S032] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 91

sehingga Anda dapat langsung mengarahkan Nameserver-nya ke Cloudflare. Berdasarkan 
dokumen Acceptable Use Policy DigitalPlat per 29 Juni 2026, tidak disebutkan batas numerik 
kaku untuk jumlah domain per akun, selama pengguna tidak melakukan penyalahgunaan 
seperti pendaftaran massal otomatis, pembuatan banyak akun (account farming), atau 
penimbunan nama domain (hoarding). 
Karena Anda sudah memiliki akun GitHub dan akan bekerja di GitHub Codespaces, opsi kedua 
yang sangat direkomendasikan untuk minimal satu website Anda (seperti portofolio developer 
atau dokumentasi proyek) adalah .is-a.dev atau ekstensi barunya .is-a.bot (is-a.dev), serta 
alternatif komunitas seperti .vexr.dev dan .eu.cc. Pendaftaran .is-a.dev sepenuhnya berbasis 
Git: Anda hanya perlu mengunjungi repositori is-a-dev/register di GitHub, melakukan fork, 
menambahkan file konfigurasi untuk mengarahkan domain atau NS Cloudflare Anda, lalu 
mengirimkan Pull Request. 
Sementara itu, maraknya penggunaan domain .tech, .me, dan .live secara gratis berasal dari 
GitHub Student Developer Pack (education.github.com/pack). Jika Anda berusia minimal 13 
tahun dan dapat mengunggah foto kartu pelajar/mahasiswa bertanggal aktif atau surat 
keterangan studi pada pengaturan GitHub Education, akun GitHub Anda berhak mengklaim 1 
domain .tech standar gratis selama 1 tahun (melalui get.tech/github-student-developer-pack), 
1 domain .me gratis selama 1 tahun via Namecheap, serta 1 domain gratis dari 25+ pilihan 
ekstensi (seperti .live, .studio, .software, .app, dan .dev) melalui Name.com tanpa 
informasi pembayaran. Paket mahasiswa ini juga membuka akses gratis ke GitHub Copilot 
Pro, seluruh IDE JetBrains, kredit cloud $200 di DigitalOcean, dan $100 di Microsoft Azure. 
Sebagai alternatif tambahan bagi non-pelajar, .pp.ua menyediakan domain tingkat ketiga gratis 
untuk penggunaan personal yang dapat diintegrasikan dengan Cloudflare (memerlukan aktivasi 
melalui aplikasi Telegram karena kendala pengiriman SMS), sedangkan nic.eu.org 
menyediakan domain gratis sejak 1996 yang kompatibel dengan Cloudflare khusus untuk 
pengguna individu atau organisasi non-profit (tidak mengizinkan situs komersial). 
Jalur B: Promo Domain Resmi Indonesia (.my.id, .biz.id, .web.id) Mulai 
Rp 1.000 
Jika Anda menginginkan nama domain resmi di bawah registri PANDI (.id) yang meningkatkan 
kredibilitas dan visibilitas di mesin pencari Google Indonesia, pendaftaran ekstensi .my.id 
(personal), .biz.id (UMKM/bisnis), dan .web.id (komunitas/pribadi) hanya mensyaratkan identitas 
KTP tanpa perlu dokumen badan usaha seperti NIB atau Akta Notaris. Penawaran paling 
ekonomis yang aktif pada 30 Oktober 2026 tersedia di BOC Indonesia 
(boc.co.id/promo/domain1k.php), yang menggelar promo Rp 1.000 per tahun untuk registrasi 
baru selama periode 1 Juli hingga 31 Desember 2026 pukul 17.00 WIB. Anda cukup 
memasukkan kode kupon MY1K untuk domain .my.id atau BIZ1K untuk domain .biz.id saat 
checkout. Layanan ini sudah mencakup manajemen DNS penuh (A, CNAME, MX, TXT) serta 
pengaturan flexible nameserver untuk diarahkan ke Cloudflare, dengan dukungan pembayaran 
instan via transfer BCA maupun gerbang pembayaran Xendit (QRIS, OVO, Indomaret, Virtual 
Account berbagai bank, dan kartu kredit), serta tidak mencantumkan batasan jumlah klaim 
domain per akun pada halaman ketentuannya. 
Penawaran terbaik kedua hadir di IDwebhost 
(idwebhost.com/promo/71319/tebus-domain-murah-indonesia[span_29](start_span)[span_29](e
nd_span)) melalui program Tebus Murah Domain Indonesia yang memangkas harga tahun 
pertama .my.id, .biz.id, dan .web.id dari harga normal Rp 55.000 menjadi Rp 3.000 per tahun. 



<!-- [ID:16_INFRA_DEVOPS_S033] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 96

aktifkan opsi Catch-All Rule jika Anda ingin seluruh email ke alamat apa pun di domain 
tersebut masuk ke Gmail Anda. Ulangi langkah ini untuk domain kedua dan ketiga; paket 
gratis Cloudflare menyediakan kuota hingga 200 alamat custom per domain, 200 
alamat tujuan terverifikasi, dan tidak membatasi jumlah pesan masuk (no 
message-count limit). 
2.​ Daftarkan Kredensial Pengiriman (Outgoing SMTP) di Brevo atau Resend: Agar 
Anda dapat mengirim dan membalas email menggunakan nama domain custom, buat 
akun gratis tanpa kartu kredit di Brevo (brevo.com), yang menyediakan kuota pengiriman 
permanen hingga 300 email per hari (~9.000 email/bulan) melalui SMTP maupun API 
serta penyimpanan hingga 100.000 kontak (dengan catatan setiap email menyertakan 
logo Brevo pada paket gratis). Sebagai alternatif atau pelengkap untuk domain lainnya, 
daftar juga akun gratis di Resend (resend.com), yang memberikan kuota 100 email per 
hari (3.000 email/bulan) lengkap dengan dukungan SMTP dan API. Tambahkan ketiga 
domain Anda di dashboard Brevo/Resend dan pasang record autentikasi DNS 
(TXT/SPF/DKIM) yang diminta ke DNS Cloudflare Anda (pastikan Anda menggabungkan 
record SPF jika sudah ada agar tidak terjadi duplikasi TXT SPF). 
3.​ Integrasikan SMTP ke Fitur "Send Mail As" di Gmail: Buka akun Gmail Anda, masuk 
ke Settings → Accounts and Import → Send mail as → Add another email address. 
Masukkan nama pengirim dan alamat email domain custom Anda, hapus tanda centang 
pada opsi "Treat as an alias" untuk menghindari kegagalan penyelarasan DMARC pada 
penerima seperti Yahoo, lalu masukkan detail server SMTP, port, username, dan 
password yang diperoleh dari Brevo atau Resend. Setelah Anda mengonfirmasi kode 
verifikasi yang masuk ke inbox Anda, Gmail akan secara otomatis menggunakan alamat 
domain custom yang sesuai saat Anda membalas email dari masing-masing website. 
Saat menguji pengiriman, selalu kirim email tes dari akun email kedua yang berbeda, 
karena pengiriman dari dan ke akun Gmail yang sama akan dideteksi sebagai loop dan 
diabaikan oleh Google. 
Apabila untuk salah satu dari ketiga website Anda dibutuhkan kotak masuk (hosted mailbox) 
terpisah yang tidak digabung ke Gmail pribadi, Anda tetap dapat mendaftarkan 1 domain 
tersebut ke Zoho Mail Forever Free Plan (zoho.com/mail). Paket ini memberikan kuota hingga 
5 pengguna gratis, ruang simpan 5 GB per pengguna, dan batas lampiran 25 MB, dengan 
syarat alamat IP Anda saat mendaftar mengarah ke pusat data US, IN, atau EU dan akses 
email dilakukan melalui Webmail Zoho atau aplikasi mobile resmi Zoho Mail. Selain itu, akun 
hosting gratis di Serv00 dan Alwaysdata juga sudah menyertakan fasilitas mailbox IMAP/POP3 
dan antarmuka Webmail bawaan tanpa biaya tambahan. 
4. Template CSS, UI Libraries, dan Kebutuhan Website 
Aktif (Form, Analytics, Monitoring) 
Untuk mempercepat pembuatan kode di GitHub Codespaces sekaligus melengkapi fitur 
operasional ketiga website Anda (form kontak, analitik pengunjung, dan penjaga uptime), 
manfaatkan repositori template terbuka dan layanan backend-as-a-service gratis di bawah ini. 
A. Sumber Template CSS & Starter Kit Terbaik (Siap Clone ke 
Codespaces) 



<!-- [ID:16_INFRA_DEVOPS_S034] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 98

Kategori Layanan 
Penyedia Terbaik 
(2026) 
Kuota Gratis & 
Spesifikasi Utama 
Keunggulan & Catatan 
Implementasi untuk 3 
Website 
upload file di paket 
gratis). 
Form Backend 
(Upload File) 
Forminit 
(eks-Getform.io) 
100 
submissions/bulan, 
arsip 30 hari, 
dukungan upload file 
hingga 25 MB 
Pilihan terbaik jika 
salah satu website 
membutuhkan form 
unggah dokumen/CV 
(fitur yang berbayar di 
Web3Forms, 
Formspree, dan 
Formcarry). 
Form Backend 
(Alternatif) 
Netlify Forms / Basin / 
Formcarry 
Netlify: Gratis di dalam 
batas 300 kredit 
platform (upload 8 MB); 
Basin & Formcarry: 50 
submissions/bln (1 
form) 
Formcarry menyimpan 
kelebihan pesan 
(over-quota) dengan 
aman hingga awal 
bulan berikutnya tanpa 
menghapus data. 
Web Analytics (Tanpa 
Batas) 
Cloudflare Web 
Analytics 
Unlimited Websites 
(untuk domain yang 
diproksi Cloudflare) & 
hingga 10 situs 
non-proksi; tanpa batas 
pageviews 
Bebas cookie 
(cookieless—tidak 
perlu banner GDPR), 
menampilkan metrik 
Core Web Vitals, dan 
otomatis diinjeksi tanpa 
skrip tambahan jika 
trafik melewati 
Cloudflare. 
Web Analytics 
(Events & Funnel) 
Umami Analytics 
(umami.is) 
Cloud Hobby: 100.000 
events/bln, 1 website, 
retensi 6 bulan; 
Self-Hosted (MIT): 
Unlimited websites & 
events 
Mendukung custom 
events, funnels, 
cohorts, dan user 
journeys. Anda dapat 
memakai Cloud Hobby 
untuk 1 web utama, 
atau meng-install versi 
self-hosted 
(Docker/Postgres) di 
Serv00/Alwaysdata 
untuk melacak 3+ web 
tanpa batas. 
Uptime Monitoring 
(Kuota Besar) 
UptimeRobot 
(uptimerobot.com) 
50 Monitor Gratis, 
interval cek 5 menit, 
retensi log 1 bulan, 
Public Status Page 
(stats.uptimerobot.com) 
Mendukung 
pemantauan 
HTTP/HTTPS, ping, 
port, dan keyword 
dengan notifikasi email. 
Sangat leluasa untuk 
memantau 3 website 



<!-- [ID:16_INFRA_DEVOPS_S035] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 99

Kategori Layanan 
Penyedia Terbaik 
(2026) 
Kuota Gratis & 
Spesifikasi Utama 
Keunggulan & Catatan 
Implementasi untuk 3 
Website 
sekaligus beserta 
endpoint API database 
Anda. 
Uptime Monitoring 
(Cepat & Chat Alert) 
Better Stack 
(betterstack.com) / 
Hyperping 
Better Stack: 10 
Monitor Gratis, 
interval 3 menit; 
Hyperping: 20 Monitor 
Gratis, 1 status page 
Better Stack 
menyertakan fitur 
screenshot-on-error 
dan peringatan instan 
gratis ke Telegram, 
Slack, Email, dan 
Webhook. 
5. Urutan Pendaftaran Sekarang Juga (Checklist 
Eksekusi Pra-Codespaces) 
Seluruh komponen di atas membentuk satu arsitektur terpadu yang berpusat pada akun GitHub 
dan Cloudflare Anda: kode sumber dan template UI (ThemeWagon, HTML5 UP, daisyUI) 
dikerjakan di dalam GitHub Codespaces, lalu didistribusikan ke tiga lingkungan hosting 
berbeda (Cloudflare Pages + Turso/D1 untuk situs pertama, Serv00 DevilWEB Panel + 
MySQL/Postgres untuk situs kedua, serta Alwaysdata PaaS Panel / Vercel + Supabase 
untuk situs ketiga). Di lapisan depan, Cloudflare Dashboard bertindak sebagai gerbang 
tunggal yang mengelola DNS, sertifikat SSL, Cloudflare Web Analytics, serta Cloudflare 
Email Routing untuk ketiga domain Anda, sementara pengiriman email keluar ditangani oleh 
Brevo/Resend SMTP melalui inbox Gmail pribadi Anda dan keandalan situs dijaga oleh 
Web3Forms serta UptimeRobot / Better Stack. 
Karena sebagian layanan menerapkan antrean persetujuan manual (khususnya Serv00 yang 
membutuhkan waktu beberapa jam hingga 72 jam) dan propagasi Nameserver domain 
memerlukan waktu sekitar 15 hingga 60 menit, lakukan pendaftaran sekarang juga sesuai 
urutan langkah di bawah ini sebelum Anda membuka GitHub Codespaces: 
1.​ Daftar Hosting Berpanel yang Memerlukan Antrean Persetujuan (5 Menit Pertama): 
Buka https://www.serv00.com/register-account/ dan ajukan pendaftaran akun gratis Anda 
terlebih dahulu agar segera masuk ke dalam antrean tinjauan manual (beberapa jam 
hingga 72 jam) untuk mendapatkan akses panel DevilWEB, SSH, 3 GB NVMe, dan 
dukungan 100 domain. Selanjutnya, buka https://www.alwaysdata.com/en/offers/ dan 
daftarkan akun Free Public Cloud (1 GB SSD) tanpa kartu kredit sebagai panel PaaS 
kedua yang langsung aktif untuk menampung banyak situs dan database sekaligus, serta 
buat akun di https://www.infinityfree.com/ apabila salah satu proyek Anda membutuhkan 
panel VistaPanel (cPanel) 5 GB yang aktif seketika. 
2.​ Klaim 3 Nama Domain Anda (Jalur Rp 0 atau Jalur Promo Lokal Rp 1.000–Rp 3.000): 
Untuk opsi Rp 0 murni, buka https://dash.domain.digitalplat.org/ guna mendaftarkan 
domain gratis berakhiran .dpdns.org, .us.kg, atau .qzz.io, lakukan fork pada repositori 
GitHub is-a-dev/register untuk mengklaim subdomain developer .is-a.dev, atau ajukan 
verifikasi kartu pelajar di https://education.github.com/pack untuk mengklaim domain 
.tech, .me, dan .live gratis 1 tahun. Apabila Anda memilih domain resmi Indonesia, 
segera buka https://boc.co.id/promo/domain1k.php untuk mendaftarkan .my.id (kode 



<!-- [ID:16_INFRA_DEVOPS_S036] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_132, SPAN_
134, SPAN_134, SPAN_136, SPAN_195 -->
## Halaman 100

kupon MY1K) dan .biz.id (kode kupon BIZ1K) seharga Rp 1.000/tahun via QRIS (berlaku 
hingga 31 Desember 2026), atau akses 
https://idwebhost.com/promo/71319/[span_132](start_span)[span_132](end_span)[span_
134](start_span)[span_134](end_span)[span_136](start_span)[span_136](end_span)tebu
s-domain-murah-indonesia sebelum 31 Oktober 2026 berakhir untuk menebus .my.id, 
.biz.id, dan .web.id seharga Rp 3.000/tahun tanpa kupon. 
3.​ Arahkan Nameserver Ketiga Domain ke Cloudflare & Aktifkan Email Custom Dua 
Arah: Tambahkan ketiga domain baru Anda ke dashboard Cloudflare pada paket Free 
($0), lalu ganti Nameserver di panel registrar domain Anda dengan dua Nameserver yang 
diberikan oleh Cloudflare. Di dalam dashboard Cloudflare masing-masing domain, buka 
menu Email → Email Routing untuk meneruskan seluruh email custom (admin@, info@, 
atau Catch-All) ke Gmail pribadi Anda, lalu daftar akun gratis di Brevo 
(https://www.brevo.com/, kuota 300 email/hari) atau Resend (https://resend.com/, kuota 
100 email/hari), verifikasi record DNS TXT/DKIM domain Anda di Cloudflare, dan 
hubungkan kredensial SMTP-nya ke menu Settings → Accounts and Import → Send 
mail as di Gmail Anda. 
4.​ Amankan Database Cloud & Access Key Form Kontak: Masuk menggunakan akun 
GitHub Anda di Turso (https://turso.tech/) untuk menyiapkan penyimpanan 5 GB Edge 
SQLite (hingga 100 database) serta di Supabase 
(https://sup[span_195](start_span)[span_195](end_span)abase.com/) untuk membuat 
hingga 2 proyek PostgreSQL (500 MB) + Auth. Setelah itu, kunjungi 
https://web3forms.com/ untuk membuat Access Key gratis (kuota 250 submissions/bulan 
untuk unlimited forms & domains) dan/atau https://forminit.com/ (kuota 100 
submissions/bulan dengan dukungan unggah file 25 MB) agar siap dipasang pada 
elemen <form> di ketiga website Anda. 
5.​ Tarik Template Pilihan ke GitHub Codespaces & Hubungkan Jalur Deployment: Buat 
3 repositori baru di GitHub dan jalankan GitHub Codespaces, lalu tarik (clone) template 
pilihan Anda dari ThemeWagon (themewagon.com/theme-framework/astro/ untuk 
Astro+Tailwind atau Aurora Free untuk React+Vite), StartBootstrap 
(startbootstrap.com/themes), atau HTML5 UP (html5up.net), serta tambahkan plugin 
daisyUI beserta MCP Server-nya untuk mempercepat penulisan komponen UI. 
Hubungkan repositori situs statis/SSR Anda ke Cloudflare Pages (atau Vercel Hobby / 
Appwrite Sites) agar ter-deploy otomatis setiap kali Anda melakukan git push, dan 
hubungkan repositori aplikasi dinamis Anda melalui SSH/Git ke panel Serv00 atau 
Alwaysdata. 
6.​ Pasang Web Analytics & Penjaga Uptime 24/7: Aktifkan fitur Cloudflare Web 
Analytics pada ketiga domain Anda di dashboard Cloudflare (dan daftar Umami Cloud 
Hobby di https://umami.is/ untuk 1 situs utama atau pasang Umami self-hosted di 
Serv00/Alwaysdata). Terakhir, buat akun gratis di UptimeRobot 
(https://uptimerobot.com/, 50 monitor interval 5 menit) atau Better Stack 
(https://betterstack.com/, 10 monitor interval 3 menit dengan notifikasi Telegram/Slack) 
untuk memantau URL ketiga website Anda secara berkelanjutan. 
Works cited 
1. A Free Domain Entry Point for Personal and Open Source Projects, 
https://silenceper.com/en/article/2026-05-29-freedomain-free-domain-for-projects/ 2. serv00.com 
- Revolutionary hosting for FREE!, https://www.serv00.com/ 3. Best free hosting platforms you 



<!-- [ID:16_INFRA_DEVOPS_S037] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 101

probably haven't tried in 2026, 
https://appwrite.io/blog/post/best-free-hosting-platforms-you-probably-havent-tried-in-2026 4. 
Brevo Pricing 2026: Free Plan Limits & Paid Tiers | Dreamlit AI, 
https://dreamlit.ai/blog/brevo-review 5. Cloudflare Free Email on Your Domain: 10-Minute Setup 
(2026), 
https://nesmachny.com/post/how-i-set-up-free-professional-email-for-my-startup-using-cloudflar
e-and-you-can-too 6. Promo domain Rp.1000 - BOC Indonesia, 
https://boc.co.id/promo/domain1k.php 7. Promo Tebus Murah Domain Indonesia .MY.ID .BIZ.ID 
dan .WEB.ID, https://idwebhost.com/promo/71319/tebus-domain-murah-indonesia 8. Promo 
Diskon Domain & Hosting Murah IDwebhost, https://idwebhost.com/promo 9. Best Render 
Alternatives in 2026 (+ Free Tier Changes), 
https://www.codecapsules.io/blog/best-render-alternatives-in-2026-where-to-go-when-render-fall
s-short/ 10. 2026 Free Cloud Database List | 6 Still-Free Options + PlanetScale, 
https://cloudinsight.cc/en/blog/free-cloud-database 11. InfinityFree: Free Website Hosting, 
https://www.infinityfree.com/ 12. Turso (Free) Free Tier Limits (19 Oct 2026), 
https://freetiertracker.com/s/turso/ 13. Supabase pricing: plans, free tier, and hidden costs - 
CloudZero, https://www.cloudzero.com/blog/supabase-pricing/ 14. Prices as light as air - 
Alwaysdata, https://www.alwaysdata.com/en/offers/ 15. DigitalPlat Domains, 
https://domain.digitalplat.org/ 16. Promo MY.ID dan BIZ.ID Rp 1.700 - Digital Registra, 
https://www.digitalregistra.co.id/promo-my-id-dan-biz-id-rp-1-700/ 17. a domain name for free? 
(really free...) : r/selfhosted - Reddit, 
https://www.reddit.com/r/selfhosted/comments/17n3t0s/a_domain_name_for_free_really_free/ 
18. Free Domain Names: How DigitalPlat's Open-Source Project Is, 
https://softouchsystems.com/2025/09/03/free-domain-names-digitalplat-open-source/ 19. 
Non-Profit Organization Announces Free Domain Names, 
https://www.searchenginejournal.com/free-domain-names/554514/ 20. GitHub - 
DigitalPlatDev/FreeDomain: Free domain registration and, 
https://github.com/DigitalPlatDev/FreeDomain 21. is-a.dev - Free subdomains for developers, 
https://is-a.dev/ 22. GitHub - harys722/free-domains: A big list of free subdomains for, 
https://github.com/harys722/free-domains 23. GitHub Student Developer Pack: How to Get It 
(2026) - Lilach Bullock, https://www.lilachbullock.com/github-student-developer-pack/ 24. GitHub 
Student Developer Pack, https://static.education.github.com/pack?sort=company 25. Unlocking 
the GitHub Student Developer Pack: The Ultimate Free, 
https://dev.to/mitanshubhasin/unlocking-the-github-student-developer-pack-the-ultimate-free-tool
kit-for-students-4pj3 26. Find the perfect domain name for your tech company on .Tech, 
https://get.tech/github-student-developer-pack 27. GitHub Student Developer Pack: Free Tools 
& Resources for Students, https://codehelper.me/articles/github-student-pack/ 28. Get Free 
PP.UA Sub-Domain DNS and Integrated with CloudFlare, 
https://www.youtube.com/watch?v=zrhxb8swVGM 29. EU.org: free domain names since 1996, 
https://nic.eu.org/ 30. Get Free Subdomain DNS from EU.ORG & Integrate with Cloudflare, 
https://www.youtube.com/watch?v=V1xnhqqg4Rw 31. Domain .MY.ID, .BIZ.ID, dan .WEB.ID 
Gratis 1 Tahun dari IDwebhost, 
https://www.fairusmajid.com/2026/09/domain-my-id-biz-id-web-id-gratis-1-tahun-idwebhost-sept
ember-2026.html 32. PROMO DOMAIN GRATIS 1 TAHUN DARI IDWEBHOST!, 
https://mailegzz.com/blogs-detail/?slug=-promo-domain-gratis-1-tahun-dari-idwebhost- 33. 
Promo Merdeka IDCloudHost Domain .my.id .biz.id .web.id Hanya, 
https://idcloudhost.com/promo/promo-domain-myid/ 34. Festival Promo Domain Spesial - 
IDCloudHost, https://idcloudhost.com/promo/promo-domain-id/ 35. Program Bagi Domain Gratis 



<!-- [ID:16_INFRA_DEVOPS_S038] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 102

(BIZ.ID & MY.ID) | IDCloudHost, https://idcloudhost.com/domain-gratis/ 36. Beli Domain Murah 
Indonesia Mulai dari Rp9.900/Tahun!, https://www.domainesia.com/domain/ 37. Promo Domain 
.MY.ID & .BIZ.ID Mulai Rp 12.000/Tahun! - Exabytes, 
https://www.exabytes.co.id/blog/promo-domain-harga-baru-transfer-dan-perpanjang-untuk-dom
ain-my-id-biz-id-mulai-dari-rp-12-000-tahun/ 38. Diskon .ID, .COM, hingga .ASIA (Update) 
Promo Domain 2026 Murah, https://www.qwords.com/blog/promo-domain/ 39. Promo 
Rumahweb Indonesia, https://www.rumahweb.com/promosi/ 40. Which plan to choose? - 
alwaysdata, https://help.alwaysdata.com/en/docs/admin-billing/billing/choose-its-paas/ 41. 
Serv00 Free Hosting Review - 1FreeHosting, https://1freehosting.com/provider/serv00 42. Sign 
in - serv00.com - Revolutionary hosting for FREE!, https://www.serv00.com/sign-in/ 43. 
Technologies - serv00.com - Revolutionary hosting for FREE!, 
https://www.serv00.com/technologies/ 44. Register account - serv00.com - Revolutionary 
hosting for FREE!, https://www.serv00.com/register-account/ 45. Pricing: Public Cloud - Plus 
Plans - alwaysdata, 
https://help.alwaysdata.com/en/docs/admin-billing/billing/public-cloud-prices/ 46. alwaysdata, 
the European Cloud, https://www.alwaysdata.com/en/ 47. alwaysdata - Grav Documentation, 
https://learn.getgrav.org/17/webservers-hosting/shared/alwaysdata 48. FS#51 : Multiple Free 
Public Cloud accounts obtained by a single, https://security.alwaysdata.com/task/51 49. Free 
Web Hosting 2026: Ranked By Real Limits (Not Marketing), 
https://blog.webhostmost.com/best-free-web-hosting/ 50. Supabase Free Tier Limits: What You 
Actually Get In 2026, https://aiagencyplus.com/supabase-free-tier-limits/ 51. Cloudflare: Build 
for the agent era, https://www.cloudflare.com/ 52. Top 5 Database-as-a-Service Platforms 2026: 
Supabase vs Neon vs, 
https://guptadeepak.com/tools/top-5-database-as-a-service-platforms-2026/ 53. ImprovMX Free 
Plan in 2026: Limits, Setup, and When to Pay, 
https://www.yuurrific.com/indie-hacking/custom-domain-email-addresses 54. Sending/Receiving 
Limits - ImprovMX Guides, https://improvmx.com/guides/sending-receiving-limits/ 55. 7 Brutal 
Truths: Is Zoho Email Still Free in 2026 ? - Codroid Labs, 
https://codroiditlabs.com/is-zoho-email-still-free-guide/ 56. Zoho Mail Pricing 2026: Every Plan 
and the Real Yearly Cost, https://fanpino.com/en/blog/zoho-mail-pricing-2026-plans-explained/ 
57. Resend vs Brevo (2026): Pricing, Free Plan & API - AISend, 
https://aisend.app/compare/resend-vs-brevo 58. Route emails · Cloudflare Email Service docs, 
https://developers.cloudflare.com/email-service/get-started/route-emails/ 59. Brevo Free Plan: 
Worth It or Too Limited? (2026), 
https://www.emailsoftwareinsights.com/reviews/brevo/pricing/free-plan/ 60. FAQs - What are the 
limits of the Free plan? - Brevo Help Center, 
https://help.brevo.com/hc/en-us/articles/208580669-FAQs-What-are-the-limits-of-the-Free-plan 
61. What are Resend account quotas and limits?, 
https://resend.com/docs/knowledge-base/account-quotas-and-limits 62. Forever FREE Business 
Email with Zoho Mail, 
https://help.zoho.com/portal/id/community/topic/forever-free-business-email-with-zoho-mail 63. 
11 Best Responsive Website Templates (2026) - ThemeWagon, 
https://themewagon.com/blog/best-responsive-website-templates/ 64. 150+ Best Free 
Responsive HTML5 Bootstrap Templates Collection, 
https://themewagon.com/blog/150-high-quality-multipage-onepage-multipurpose-templates-free-
download/ 65. Free Astro Templates for Blogs & Business - ThemeWagon, 
https://themewagon.com/theme-framework/astro/ 66. Themes | Astro, 
https://astro.build/themes/8/?search=&price%5B%5D=free 67. Free Bootstrap Themes & 



<!-- [ID:16_INFRA_DEVOPS_S039] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
### Matematika Konkurensi Ribuan Pengguna dan Bahaya Pendaftaran Buta
Ketika sebuah platform diluncurkan dan mengalami lonjakan viral hingga mencapai ribuan 
pengguna aktif secara bersamaan, ketergantungan pada satu atau dua penyedia API gratis 
tunggal dipastikan akan memicu kelumpuhan sistem dalam hitungan detik. Secara matematis, 
Google AI Studio membatasi paket gratis pada laju 5 hingga 15 permintaan per menit (RPM) dan 
100 hingga 1.000 permintaan per hari (RPD), OpenRouter pada model berlabel gratis membatasi 
20 RPM dan 50 hingga 200 RPD tanpa saldo, sementara GroqCloud membatasi 30 RPM. Apabila 
sistem hanya mengaktifkan segelintir penyedia pada hari peluncuran, gelombang permintaan ke-
31 pada menit pertama akan langsung memicu kode galat HTTP 429 yang menghentikan eksekusi 
agen.
Sebaliknya, mendaftarkan seluruh layanan secara serentak pada hari pertama—khususnya 
layanan infrastruktur VPS dan kredit uji coba yang membutuhkan verifikasi kartu pembayaran—
merupakan kesalahan strategis yang menghanguskan modal komputasi secara sia-sia. Audit 
terhadap kebijakan penyedia komputasi awan membuktikan bahwa hampir seluruh platform 
berbasis kredit uji coba langsung memulai hitungan mundur masa berlakunya detik itu juga saat 
pendaftaran dan verifikasi kartu disetujui, bukan saat server pertama kali dibuat. Apabila seorang 
arsitek sistem mendaftarkan DigitalOcean (kredit US200 selama 60 hari), Vultr (kredit US200–
US300 selama 30 hari), Linode/Akamai (kredit US100 selama 60 hari), Kamatera (kredit US100 
selama 30 hari), AWS Free Plan (kredit hingga US200 selama 6 bulan), Microsoft Azure (kredit 
US200 selama 30 hari dan VPS gratis 12 bulan), Alibaba Cloud Model Studio (kuota 1 juta token 
per model selama 90 hari), serta AI21 Labs (kredit US10 selama 3 bulan) secara bersamaan pada 
hari peluncuran, seluruh arloji masa aktif tersebut akan berdetak paralel dan hangus bersamaan 
tanpa terpakai secara maksimal.

<!-- [ID:16_INFRA_DEVOPS_S040] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
### Lapisan 0: Penyerapan Beban di Peramban Klien dan Perisai Jaringan Tepi
Saat terjadi lonjakan trafik viral, kesalahan arsitektural terbesar adalah membiarkan seluruh 
permintaan pengguna menghantam server VPS utama secara langsung. Pada lapisan terluar, 
aplikasi web di-hosting menggunakan Cloudflare Pages atau Vercel yang menyediakan bandwidth 
gratis tanpa memerlukan kartu kredit, dilindungi oleh Cloudflare Turnstile untuk memblokir bot 
otomatis pencuri kuota, serta dirutekan melalui skrip Calcium-Ion/new-api-worker di Cloudflare 
Workers (gratis 100.000 permintaan per hari) dengan aturan transformasi (*Transform Rules*) 
yang menghapus tajuk alamat IP asli pengunjung dan menyembunyikan IP server agregator. Lebih 
jauh lagi, untuk fitur percakapan teks, analisis gambar, audio, dan video dasar pada antarmuka 
web, sistem menanamkan pustaka JavaScript Puter.js (https://developer.puter.com) langsung di 
sisi frontend. Melalui mekanisme *User-Pays* yang berjalan transparan di peramban 
(puter.chat(...)), Puter.js memungkinkan pemanggilan lebih dari 400 model mutakhir—termasuk 
Claude Sonnet 5.5, GPT-5.4 Nano, Gemini 4 Argon, Gemini 3.8 Flash, Grok 4.7, DeepSeek, dan 
Kimi—tanpa memerlukan kunci API backend sama sekali. Dengan demikian, berapapun jumlah 



<!-- [ID:16_INFRA_DEVOPS_S041] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
### Lapisan 3: Eksekusi Paralel pada Kolam Zero-Auth, Kolam Multi-Cloud, dan Mesin Lokal 
Tanpa Sensor
Berdasarkan keputusan RouteLLM, kueri yang tergolong ringan atau membutuhkan eksekusi 
tanpa filter sensor (\mathcal{M}_{\text{weak}}) dialirkan ke rantai titik akhir nir-kunci (*Zero-Auth 


