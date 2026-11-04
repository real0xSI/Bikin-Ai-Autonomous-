
<!-- [ID:11_WEB_PLATFORM_S001] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: WEBSOCKET -->
# Simpan daftar transaksi & koneksi WebSocket layar pembeli
TRANSACTIONS = {}
ACTIVE_WEBSOCKETS: dict[str, list[WebSocket]] = {}

class OrderRequest(BaseModel):
    external_id: str          # ID unik dari Bot Tele / WA / Web Anda
    channel: str              # Contoh: "telegram", "whatsapp", "miniapp", "web", "facebook"
    amount: int               # Harga asli (misal: 25000)
    customer_name: str
    webhook_callback_url: str # URL bot/web Anda yang akan ditembak otomatis saat LUNAS


<!-- [ID:11_WEB_PLATFORM_S002] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 73

2.​ Inline Keyboard Kontekstual: Di bawah setiap hasil gambar yang dikirim bot, otomatis 
muncul tombol lanjutan: [🎬 Gerakkan Jadi Video (20 Koin)], [🔍 Upscale 4K (4 Koin)], 
[📝 Buat Caption TikTok (Gratis)], [🔄 Variasi Baru]. 
4.2 Tampilan Menu "Sultan Super-App" & 3 Opsi Bio Powerful SEO 
(120 Karakter) 
A. Pilihan Bio SEO Profil Bot (About Text Maksimal 120 Karakter) 
●​ Opsi 1 (Global & Indonesia — 116 Karakter): ⚡ All-in-One AI Generator: Video 
(Kling/Wan/Veo), Flux HD Image, Suno Music & Copywriting. Free Daily Credits! 🎁🚀 
●​ Opsi 2 (Kata Kunci Pencarian Tinggi — 118 Karakter): 🧠 Super AI Studio: Text/Image 
to Video, Motion Control, 4K Upscale, Suno Audio & Unfiltered AI. Claim Free Coins! ⚡ 
●​ Opsi 3 (Fokus Kreator & Kampanye — 114 Karakter): 🎬 #1 Autonomous AI Studio: 
Kling, Wan2.1, Flux, Suno & Auto-Campaigns in 1 Click. Free Daily Coins & Instant Pay! 
B. Desain Kartu Menu Utama (/start — Gaya #1 Sultan Super-App) 
🧠 bikinAI Super Intelligence — All-in-One AI Studio 
━━━━━━━━━━━━━━━━━━ 👤 Kreator: @NamaUser (Tier: Pro Member 🌟) 💎 
Koin Utama: 50 Koin (Rp 5.000) 🎁 Koin Bonus: 4 Koin (Rp 400) (Klaim harian: Tersedia ✅) 
⚡ Mesin Aktif: Muse Orchestrator v2 + 9Router Turbo 🟢 
━━━━━━━━━━━━━━━━━━ Ketik perintah apa saja, kirim foto/PDF/suara 
langsung di chat ini, atau pilih Studio di bawah: 
[ 🚀 Buka Studio Visual & Klaim Harian (Mini App) ] [ 🎬 Buat Video AI ] [ 🎨 Buat Gambar HD ] 
[ 🕺 Motion Control ] [ 🎵 Musik & Suara (Suno) ] [ ✨ Paket Kampanye Otomatis (Muse) ] [ 🔍 
Upscale 4K ] [ 🎁 Klaim Koin Harian ] [ 💳 Top-Up QRIS / Stars ] [ ⚙️ Ganti Engine AI ] [ 🎧 CS 
AI & Komunitas ] 
4.3 Kode Konfigurasi Panel Saklar 1 Angka (config.py) 
Agar Anda tidak perlu menyewa GPU Vast.ai saat tahap pembangunan/pengujian dan bisa 
mengganti mesin atau tampilan dalam 0 detik tanpa mematikan bot yang sedang dipakai 
pelanggan: 
# 
=====================================================================​

<!-- [ID:11_WEB_PLATFORM_S003] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 97

Untuk memangkas waktu pengerjaan antarmuka dari nol, ThemeWagon (themewagon.com) 
menyediakan lebih dari 150 template responsif gratis yang bersifat open-source dan diizinkan 
untuk proyek komersial. Apabila Anda membangun situs berbasis Astro dan Tailwind CSS, 
direktori themewagon.com/theme-framework/astro/ menyediakan 17 template gratis yang siap 
digunakan, meliputi AstroWind, AstroPaper, dan Astroplate untuk website blog/dokumentasi, 
Astroship, Play, dan DataNova untuk produk SaaS atau startup, serta AgenceX, Astrolus, 
Tailcast, dan AstroDeck untuk landing page bisnis dan agensi. Selain itu, katalog resmi Astro 
di astro.build/themes (dengan filter gratis) juga menawarkan tema berbasis Astro 6 dan 
Tailwind CSS 4 berlisensi MIT tanpa ketergantungan framework UI tambahan. 
Jika salah satu dari ketiga website Anda adalah dashboard admin, aplikasi web interaktif, atau 
e-commerce, koleksi tahun 2026 di ThemeWagon dan StartBootstrap 
(startbootstrap.com/themes, seluruhnya berbasis Bootstrap 5 dan berlisensi MIT) menawarkan 
fondasi kode yang matang. Anda dapat mengunduh Aurora Free (dibangun dengan React JS, 
Material UI, dan Vite yang menyertakan 7 halaman siap pakai termasuk autentikasi dan berjalan 
di Node.js v20), DashDarkX (template admin React + Material UI dengan mode gelap bawaan), 
NickelFox (dashboard penjualan React MUI dengan dukungan multibahasa), Spark atau 
Material Dashboard 3 (60+ komponen UI Bootstrap 5), serta Productly, Techie, dan JoBest 
untuk situs e-commerce dan landing page. Untuk situs portofolio atau profil perusahaan yang 
mengutamakan kecepatan muat ekstrem dengan HTML5 dan CSS3 murni tanpa framework 
berat, HTML5 UP (html5up.net, lisensi Creative Commons Attribution 3.0) dan Themefisher 
(themefisher.com/best-free-html5-templates) menyediakan tema teruji seperti Phantom (layout 
grid portofolio yang telah diunduh lebih dari 448.000 kali), Directive, Prologue, Spectral, 
Telephasic, Kross, dan Airspace. 
Saat memodifikasi komponen UI di dalam GitHub Codespaces, padukan Tailwind CSS dengan 
daisyUI (daisyui.com), sebuah plugin murni CSS tanpa beban JavaScript browser yang 
menyediakan 68 komponen siap pakai dan lebih dari 600 utility classes. Keunggulan 
strategis daisyUI di tahun 2026 adalah tersedianya Official MCP Server, yang memungkinkan 
agen coding AI di dalam editor Anda menulis kode antarmuka jauh lebih ringkas dan akurat. 
Apabila proyek Anda membutuhkan komponen interaktif berbasis JavaScript atau React, Anda 
dapat memadukannya dengan shadcn/ui, Flowbite, Headless UI, atau HeroUI. 
B. Layanan Form Backend, Web Analytics, dan Uptime Monitoring 
Gratis 
Agar ketiga website statis maupun dinamis Anda dapat menerima pesan dari pengunjung, 
melacak trafik tanpa melanggar privasi, dan terpantau kesehatannya selama 24/7, integrasikan 
tiga layanan operasional gratis berikut: 
Kategori Layanan 
Penyedia Terbaik 
(2026) 
Kuota Gratis & 
Spesifikasi Utama 
Keunggulan & Catatan 
Implementasi untuk 3 
Website 
Form Backend 
(Utama) 
Web3Forms 
(web3forms.com) 
250 
submissions/bulan, 
Unlimited Forms, 
Unlimited Domains, 
riwayat 30 hari 
Cukup 1 akun untuk 
melayani seluruh form 
di 3 website berbeda; 
sudah termasuk 
proteksi spam 
hCaptcha dan custom 
redirect (tanpa fitur 



<!-- [ID:11_WEB_PLATFORM_S004] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 118

seluruh permintaan k dibatasi secara ketat oleh rasio Harga Pokok Penjualan maksimum 
\gamma_{\max} = 0,05 (5%):
Melalui persamaan deterministik ini, seorang pelanggan paket Rp 99.000 memiliki jatah plafon 
pemakaian API grosir berbayar maksimal sebesar Rp 4.950 (\approx \text{US\$0,31}). Dengan 
harga grosir berdiskon 95% di PayPerQ, NanoGPT, dan WaveSpeed, anggaran Rp 4.950 tersebut 
sudah mencukupi untuk merender puluhan gambar HD, beberapa klip video sinematik, dan jutaan 
token teks. Detik itu juga ketika seorang *power user* menghabiskan jatah plafon biaya grosir Rp 
4.950 miliknya di tengah bulan, pemutus sirkuit gateway tidak mematikan akun pelanggan 
tersebut, melainkan secara transparan mengalihkan seluruh permintaan berikutnya dari pelanggan 
itu ke **Kolam Eksekusi 100% Gratis Permanen** (Mistral 1B Pool, Gemini 3.5 Flash, NgodeAI Rp 
0, Pollinations.ai, Kokoro-82M, dan Wan2.2/LTX-VideoQ8 lokal) yang memiliki biaya marginal Rp 0 
bagi server. Dengan mekanisme *graceful degradation* ini, pelanggan tetap menikmati layanan 
tanpa batas sepanjang bulan, sementara operator platform terlindung 100% dari risiko *boncos* 
dan mengunci laba bersih minimal 95% pada setiap pelanggan tanpa terkecuali.
http://googleusercontent.com/visual_element_2

<!-- [ID:11_WEB_PLATFORM_S005] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 134

Berikut adalah panduan arsitektur frontend lengkap, struktur proyek, dan seluruh kode produksi 
(production-ready) untuk membangun antarmuka web dan dashboard platform agregator AI 
AETHEROS v3.0. 
Aplikasi ini dibangun menggunakan arsitektur Next.js 15 (App Router), React 19, TypeScript, 
dan Tailwind CSS v4 dengan filosofi desain Futuristic Obsidian Luxury (latar #030712 dengan 
aksen cyan, violet neon, dan pendaran cahaya radial). Seluruh modul yang dirancang di bawah 
mengintegrasikan studio multimodal, monitor kesehatan provider multi-jalur, dashboard margin 
FinOps 95%, radar adaptasi mandiri repositori GitHub, serta konsol omnichannel bot. 
Struktur Direktori Proyek 
aetheros-studio/ ├── app/ │ ├── api/ │ │ ├── generate/ │ │ │ └── route.ts │ │ └── 
payment/ │ │ └── qris/ │ │ └── route.ts │ ├── globals.css │ ├── layout.tsx │ └── page.tsx 
├── components/ │ ├── FinOpsTreasuryDashboard.tsx │ ├── HeroPromptStudio.tsx │ ├── 
Navbar.tsx │ ├── OmnichannelBridge.tsx │ ├── SelfEvolvingRadar.tsx │ └── 
SystemHealthMonitor.tsx ├── lib/ │ └── utils.ts ├── .env.example ├── next.config.ts ├── 
package.json ├── postcss.config.mjs └── tsconfig.json 
1. Inisialisasi Dependensi dan Konfigurasi Inti 
package.json 
Pastikan seluruh pustaka utilitas animasi, ikon, dan manipulasi kelas terpasang secara presisi: 
{​
  "name": "aetheros-studio",​
  "version": "3.0.0",​
  "private": true,​
  "scripts": {​
    "dev": "next dev",​
    "build": "next build",​
    "start": "next start",​
    "lint": "next lint"​
  },​
  "dependencies": {​
    "clsx": "^2.1.1",​
    "lucide-react": "^0.475.0",​
    "motion": "^12.4.7",​
    "next": "15.1.7",​
    "react": "^19.0.0",​
    "react-dom": "^19.0.0",​
    "tailwind-merge": "^3.0.1"​
  },​
  "devDependencies": {​
    "@tailwindcss/postcss": "^4.0.6",​
    "@types/node": "^22.13.4",​
    "@types/react": "^19.0.8",​
    "@types/react-dom": "^19.0.3",​



<!-- [ID:11_WEB_PLATFORM_S006] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 57

2. Gemini AI (gemini.google.com) – Berada di posisi kedua dengan sekitar 33,1 juta kunjungan.
3. Character.ai – Sekitar 7,6 juta kunjungan (Sangat populer di kalangan Gen Z untuk hiburan/ngobrol dengan bot persona).
4. Claude (claude.ai) – Sekitar 3,9 juta kunjungan.
5. DeepSeek (chat.deepseek.com) – Sekitar 3,8 juta kunjungan.
6. Perplexity (perplexity.ai) – Sekitar 3,2 juta kunjungan. (Sisa top 10 lainnya diisi oleh platform AI penunjang produktivitas dan generator visual
yang berfluktuasi seperti platform pembuat presentasi dan gambar).
Kata Kunci (Keywords) Paling Sering Dipakai di Indonesia (Tren 2026)
Berdasarkan analisis tren Google terkini di 2026, pencarian AI di Indonesia sudah tidak lagi sekadar bertanya "Apa itu AI?", melainkan bergeser pada
niat praktis (Prompt-Based Search) dan kecepatan tren (Velocity/Breakout Topic). Berikut adalah susunan kata yang paling sering dipakai orang
Indonesia saat ini:
1. "Gimana cara..." / "Cara bikin..." (Fokus Visual & Kreatif) Orang Indonesia paling banyak mencari tutorial praktis. Kueri seperti "Gimana cara
bikin foto AI" atau "Cara edit foto pakai AI" adalah kata kunci yang mendominasi. Mereka menggunakan AI sebagai teman berkreasi.
2. Penyebutan Nama Brand Secara Langsung Netizen jarang mengetik "Kecerdasan Buatan". Mereka langsung mengetik nama produknya seperti
"ChatGPT", "Gemini AI", atau "Character AI" saat melakukan pencarian di Google.
3. Penambahan kata "Terbaru 2026" (Velocity Keyword) Di tahun 2026, pengguna sering menambahkan embel-embel tahun atau kebaruan.
Contoh kueri breakout (melesat cepat) adalah "AI website builder terbaru 2026" atau mencari rekomendasi tools spesifik terkini.
4. "Gratis" & "Bahasa Indonesia" Kata modifier ini masih menempel kuat. Pencarian seperti "Web AI gratis" atau "AI buat presentasi gratis"
merupakan pola pencarian yang sangat khas dari audiens Indonesia yang selalu mencari versi tidak berbayar dengan dukungan bahasa lokal.
Sources
1. 10 Situs AI yang Paling Sering Digunakan Publik RI 2026
2. Ini Kata Kunci Paling Dicari Orang Indonesia di Google 2025
3. 15 AI Terpopuler di Dunia 2026, ChatGPT Masih Belum Terkejar
4. Google Trends 2026: Definisi & Fitur Baru yang Wajib Tahu
User prompt: Dari seluruh data yang google punya alias kamu dari awal ai hingga detik ini 10 october 2026. jika saya mau menjadi agregator atau
jembatan untuk mereka yang mau instant murah dan penyuka ai. karena nnti saya akan fokus buat bot telegram ai yang bisa render gambar video
misalnya atau mungkin jika berkembang bisa website dll. yang jelas untuk memulai dan mencari nama yang pas agar SEO nomer 1 dan benar benar
berdasar volume pasti nama bot saya tersebut gitu.
Response: Memilih nama murni berdasarkan volume pencarian tertinggi (seperti "Cara Bikin Foto AI Gratis") memang menjamin pencarian yang
banyak, namun itu akan menjadi bumerang untuk SEO. Nama yang terlalu umum (generic exact match) tidak bisa dipatenkan sebagai brand dan Anda
akan bersaing langsung dengan artikel raksasa dari media berita atau blog tutorial.
Strategi terbaik untuk mendominasi SEO #1 dan tetap mudah diingat oleh pasar Indonesia adalah menggabungkan 1 Kata Brand Singkat + Kata
Kunci Volume Tinggi.
Berikut adalah racikan formula nama dan rekomendasi untuk bot Telegram AI Anda berdasarkan perilaku pencarian netizen Indonesia hingga
Oktober 2026:
Kata Kunci Inti (Core Keywords) untuk Pasar Indonesia
Orang Indonesia yang mencari solusi "instan dan murah" tidak mencari istilah teknis seperti "Aggregator" atau "Render". Mereka menggunakan
bahasa fungsional:
Kata Kerja: Bikin, Buat, Edit, Nyari.
Kata Benda: Foto, Gambar, Video, Bot, AI.
Kata Sifat/Solusi: Gampang, Cepat, Instan, Murah, Gratis.
Rekomendasi Nama Bot & Domain (Berdasarkan Niat Pencarian)
1. Kategori Fungsional & Kasual (Paling berpotensi viral & SEO Friendly) Nama-nama ini memotong langsung ke tujuan pengguna yang tidak mau
ribet.
Bikin.ai (Paling kuat. Mencakup segala niat pencarian "Gimana cara bikin...")
GampangAI (Menjawab masalah utama pengguna: ingin yang instan dan tidak pusing memikirkan prompt rumit)
Ngebot.ai (Mengambil istilah slang "nge-bot" yang sangat familiar di kalangan pengguna Telegram/Discord Indonesia)
2. Kategori Visual Spesifik (Karena fokus render gambar/video) Jika Anda ingin mendominasi pencarian spesifik pembuat gambar.



<!-- [ID:11_WEB_PLATFORM_S007] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 672

2.​ Inline Keyboard Kontekstual: Di bawah setiap hasil gambar yang dikirim bot, otomatis 
muncul tombol lanjutan: [🎬 Gerakkan Jadi Video (20 Koin)], [🔍 Upscale 4K (4 Koin)], 
[📝 Buat Caption TikTok (Gratis)], [🔄 Variasi Baru]. 
4.2 Tampilan Menu "Sultan Super-App" & 3 Opsi Bio Powerful SEO 
(120 Karakter) 
A. Pilihan Bio SEO Profil Bot (About Text Maksimal 120 Karakter) 
●​ Opsi 1 (Global & Indonesia — 116 Karakter): ⚡ All-in-One AI Generator: Video 
(Kling/Wan/Veo), Flux HD Image, Suno Music & Copywriting. Free Daily Credits! 🎁🚀 
●​ Opsi 2 (Kata Kunci Pencarian Tinggi — 118 Karakter): 🧠 Super AI Studio: Text/Image 
to Video, Motion Control, 4K Upscale, Suno Audio & Unfiltered AI. Claim Free Coins! ⚡ 
●​ Opsi 3 (Fokus Kreator & Kampanye — 114 Karakter): 🎬 #1 Autonomous AI Studio: 
Kling, Wan2.1, Flux, Suno & Auto-Campaigns in 1 Click. Free Daily Coins & Instant Pay! 
B. Desain Kartu Menu Utama (/start — Gaya #1 Sultan Super-App) 
🧠 bikinAI Super Intelligence — All-in-One AI Studio 
━━━━━━━━━━━━━━━━━━ 👤 Kreator: @NamaUser (Tier: Pro Member 🌟) 💎 
Koin Utama: 50 Koin (Rp 5.000) 🎁 Koin Bonus: 4 Koin (Rp 400) (Klaim harian: Tersedia ✅) 
⚡ Mesin Aktif: Muse Orchestrator v2 + 9Router Turbo 🟢 
━━━━━━━━━━━━━━━━━━ Ketik perintah apa saja, kirim foto/PDF/suara 
langsung di chat ini, atau pilih Studio di bawah: 
[ 🚀 Buka Studio Visual & Klaim Harian (Mini App) ] [ 🎬 Buat Video AI ] [ 🎨 Buat Gambar HD ] 
[ 🕺 Motion Control ] [ 🎵 Musik & Suara (Suno) ] [ ✨ Paket Kampanye Otomatis (Muse) ] [ 🔍 
Upscale 4K ] [ 🎁 Klaim Koin Harian ] [ 💳 Top-Up QRIS / Stars ] [ ⚙️ Ganti Engine AI ] [ 🎧 CS 
AI & Komunitas ] 
4.3 Kode Konfigurasi Panel Saklar 1 Angka (config.py) 
Agar Anda tidak perlu menyewa GPU Vast.ai saat tahap pembangunan/pengujian dan bisa 
mengganti mesin atau tampilan dalam 0 detik tanpa mematikan bot yang sedang dipakai 
pelanggan: 
# 
=====================================================================​

<!-- [ID:11_WEB_PLATFORM_S008] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Frontend
- Next.js (apps/web, apps/admin)


<!-- [ID:11_WEB_PLATFORM_S009] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# Admin Dashboard (Owner Only)

Next.js 14 App Router. Server-side proxy ke orchestrator.


<!-- [ID:11_WEB_PLATFORM_S010] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Keamanan
1. `middleware.ts` → 401 kalau tidak ada `owner_session` cookie.
2. Semua request server-side pakai `INTERNAL_KEY` (bukan di browser).
3. `INTERNAL_KEY` TIDAK PERNAH dikirim ke client.
4. Dashboard hanya untuk owner. Jangan diakses publik.

