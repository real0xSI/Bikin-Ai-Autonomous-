
<!-- [ID:08_OMNI_SOCIAL_S071] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_358, SPAN_359, SPAN_360, SPAN_361, SPAN_362 -->
## Halaman 499

agnostik model berlisensi MIT), Mastra dan Volt Agent (untuk ekosistem TypeScript), Rig 
(kerangka kerja berbasis Rust untuk kinerja dan keamanan memori tingkat tinggi), serta Akka 
dan Ray untuk sistem agen terdistribusi yang toleran terhadap kesalahan. Khusus untuk alur 
kerja koding hierarkis, fractal menyediakan runtime Python dengan delegasi rekursif, Git 
worktrees per node, dan penyimpanan status persisten berbasis SQLite. 
Pada kategori agen yang mampu berevolusi secara mandiri (self-evolving agents) dan stasiun 
kerja multi-kanal, OpenClaw (openclaw) menonjol sebagai agen AI personal kode terbuka yang 
memiliki ekosistem masif mencakup 5.380 keterampilan (skills) dan 36 agen spesialis 
(sebagaimana terdokumentasi dalam adriannoes/awesome-agentic-ai), dilengkapi dengan 
kontrol peramban (browser control), integrasi pesan, memori persisten, serta kemampuan 
mendaftarkan server model lokal tanpa sensor secara langsung melalui baris perintah openclaw 
onboard --non-interactive --mode local 
--custom-base[span_358](start_span)[span_358](end_span)[span_359](start_span)[span_359](
end_span)[span_360](start_span)[span_360](end_span)-url http://127.0.0.1:8080/v1. Sejalan 
dengan itu, Hermes Agent dari Nous Research merupakan agen AI personal kode terbuka 
yang mampu memperbaiki dirinya sendiri (self-improving) melalui siklus pembelajaran tertutup 
(closed learning loop), mendukung penjadwalan cron, integrasi protokol MCP, gerbang 
multi-platform (Telegram, Discord, Slack, WhatsApp, Signal), serta konfigurasi langsung ke 
server lokal melalui hermes config set 
model.base[span_361](start_span)[span_361](end_span)[span_362](start_span)[span_362](en
d_span)_url http://127.0.0.1:8080/v1. Pendekatan evolusioner yang lebih radikal ditunjukkan 
oleh GenericAgent, yang menumbuhkan pohon keterampilannya sendiri (skill tree) melalui 
mekanisme kristalisasi keterampilan otomatis hanya dari \sim 3.000 baris kode benih (seed 
code) dan 9 alat atomik yang memberikan kendali penuh atas sistem operasi (peramban, 
terminal, sistem berkas, dan visi layar). Sementara itu, nanobot dari HKU Data Science Lab 
(dirilis hingga v0.2.1) mempertahankan inti kode tetap ultra-ringan dan mudah dibaca namun 
menyertakan meja kerja lengkap yang mencakup WebUI, tujuan berkelanjutan (sustained 
goals), dukungan MCP, pembuatan gambar, perutean model multi-penyedia, dan akses 
multi-kanal melalui Telegram, Signal, serta Matrix. Ekosistem stasiun kerja ini juga diperkaya 
oleh CoPaw dan QwenPaw dari Alibaba (mendukung kolaborasi multi-agen, pemijahan 
sub-agen, MCP, dan kanal DingTalk, Feishu, WeChat, Discord, serta Telegram berlisensi MIT), 
Octop dari Tencent Cloud (asisten multi-pengguna dengan delegasi ACP ke Claude Code atau 
OpenCode, persetujuan alat, pelindung shell, dan redaksi data pribadi/PII), OpenHuman (agen 
local-first yang berjalan sepenuhnya di perangkat dengan 118 integrasi OAuth, pohon memori 
hierarkis, dan kompresi TokenJuice), Mercury Agent (agen berfokus keamanan izin alat dan 
anggaran token), Trustclaw dari ComposioHQ, OneBox (agen Android Apache-2.0 yang 
mengendalikan 90+ alat dalam aplikasi), serta agen koding terminal Pi 
(@earendil-works[span_366](start_span)[span_366](end_span)[span_367](start_span)[span_36
7](end_span)[span_368](start_span)[span_368](end_span)/pi-coding-agent) dan Aider. 
Infrastruktur Memori Persisten: Mem0 dan Letta 
Agar agen otonom dapat mempertahankan pengetahuan lintas sesi (mencakup memori jangka 
pendek, jangka panjang, kerja, episodik, dan semantik), sistem membutuhkan lapisan 
penyimpanan memori terdedikasi. mem0ai/mem0 menyediakan infrastruktur memori drop-in 
yang memungkinkan agen mendaftarkan dirinya sendiri secara otonom melalui CLI (npm install 
-g @mem0/cli atau pip install mem0-cli) menggunakan perintah mem0 init --agent --agent-caller 
nama-agen, menyimpan konteks melalui mem0 add, dan melakukan pencarian semantik 



<!-- [ID:08_OMNI_SOCIAL_S072] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 508

Render Gratis pada Endpoint Mini App 
Teks kebijakan privasi di dalam MINIAPP_FULL_WEBSITE_HTML menyatakan bahwa 
komunikasi antara Mini App dan server dilindungi oleh tanda tangan kriptografi HMAC-SHA256. 
Namun, audit forensik pada fungsi JavaScript runGenerate() dan endpoint backend 
handle_webapp_execute_api (/api/webapp/execute) membuktikan bahwa klaim tersebut belum 
diimplementasikan di level kode. Antarmuka frontend hanya mengirimkan angka mentah 
st.user_id yang diambil dari tg.initDataUnsafe?.user tanpa menyertakan string bertanda tangan 
window.Telegram.WebApp.initData. Lebih jauh lagi, fungsi handle_webapp_execute_api di sisi 
server sama sekali tidak memanggil fungsi pemotongan saldo deduct_user_coins_for_job. 
Konsekuensi berantai dari celah ini sangat merugikan secara finansial maupun operasional 
karena pengguna yang melakukan render melalui Mini App tidak pernah dipotong koinnya sama 
sekali. Selain itu, apabila variabel user_id bernilai kosong atau 0 saat diakses dari peramban 
eksternal, ekspresi int(data.get("user_id") or RUNTIME_CONFIG["OWNER_ID_RUNTIME"] or 
0) justru mengalihkan beban dan pengiriman hasil render ke ruang obrolan pribadi milik 
pengelola utama. Pihak luar yang memindai port 8080 juga dapat mengirimkan permintaan 
POST palsu berisi user_id acak untuk melakukan serangan spamming media ke pengguna 
Telegram mana pun atas nama bot tanpa autentikasi kriptografi. 
3. Kebocoran Render Gratis dan Prompt Statis Terkunci pada Handler 
Foto dan Obrolan Alami 
Pada bagian ke-12 (handle_multimodal_photo_and_pdf) dan bagian ke-13 
(handle_natural_conversation) di dalam App.py, alur pemotongan koin dan pemeriksaan kuota 
harian dilewati sepenuhnya. Ketika pengguna mengunggah foto referensi (F.photo), sistem tidak 
mengunduh foto tersebut dari server Telegram (bot.download(message.photo[-1])) untuk dikirim 
ke model Image-to-Image atau Reference Lock, melainkan mengeksekusi variabel statis 
en_prompt = f"Cute cat holding a sign board with clear text 'ayo coba bikinAI', Indonesian street 
storefront, {clean_caption}, Seedream 4.5 8k photorealistic" dan merendernya secara gratis 
tanpa memotong koin. Hal serupa terjadi ketika pengguna mengetik kalimat "buat gambar ..." di 
ruang obrolan; sistem langsung memanggil fetch_clean_image_bytes dan mengirimkan gambar 
4K beserta tombol derivative upsell tanpa memeriksa ataupun memotong saldo koin_bonus 
maupun koin_utama. 
4. Kondisi Balapan (Race Condition) Pengambilalihan Hak Akses 
Owner 
Fungsi penjaga keamanan is_verified_owner_dm(user_id: int, chat_type: str) memiliki logika 
otomatis if RUNTIME_CONFIG["OWNER_ID_RUNTIME"] == 0: 
RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = user_id. Apabila pengelola belum mengisi 
variabel lingkungan ADMIN_USER_ID di dalam berkas .env saat server pertama kali 
dinyalakan, nilai awal OWNER_ID_RUNTIME berada pada angka 0. Pengguna eksternal 
pertama yang secara kebetulan atau sengaja mengetik /admin, /set_miniapp, atau 
/pasang_bansos di pesan pribadi bot akan langsung dikukuhkan oleh sistem sebagai pemilik 
sah dan disimpan secara permanen ke dalam tabel system_settings melalui 
save_persistent_setting(db, "OWNER_ID_RUNTIME", ...). 



<!-- [ID:08_OMNI_SOCIAL_S073] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 529

Keduanya" untuk Global, & Tombol Harvest Manual (Solusi Catatan 
#2, #4, & #7) 
●​ Arsitektur Sub-Menu Pembayaran di /admin (Solusi Catatan #2 & #4): Agar layar 
utama /admin tidak penuh sesak, pengaturan pembayaran kini memiliki tombol khusus 
[💳 Buka Sub-Menu Pengaturan Pembayaran] yang dibagi menjadi 3 halaman 
sub-menu terpisah: 
○​ Sub-Menu A — 📲 Kasir Lokal: QRIS Direct (0% Biaya): Pilih antara QRIS 
GoPay Merchant, QRIS ShopeePay Merchant, atau QRIS DANA Bisnis. 
○​ Sub-Menu B — 🏦 Kasir Lokal: Payment Gateway Resmi: Pilih antara Duitku, 
Tripay, Pakasir, atau Midtrans (digunakan saat QRIS Direct Anda mendekati batas 
limit harian/bulanan). 
○​ Sub-Menu C — 🌐 Kasir Global (Otomatis untuk Pembeli Luar Negeri): 
Dilengkapi 3 pilihan eksplisit sesuai permintaan Anda di Catatan #4: 
1.​ [₮ Hanya Crypto USDT (@CryptoBot)] 
2.​ [⭐ Hanya Telegram Stars] 
3.​ [🌐 Aktifkan Keduanya Sekaligus (USDT + Telegram Stars)] (Saat opsi 
ke-3 ini dipilih, pembeli luar negeri akan melihat kedua tombol pilihan 
pembayaran tersebut sekaligus di layar tagihan mereka!). 
●​ Penguncian Permanen Tombol Harvest Manual (Solusi Catatan #7): Tombol [🌾 
Panen Laba Bersih Sekarang (Manual Harvest)] dikunci permanen di baris paling atas 
menu /admin (beserta perintah cepat /harvest) untuk memindahkan saldo laba bersih siap 
panen ke catatan penarikan pemilik kapan saja. 
3. Buku Manual Developer & SOP Peluncuran di Dalam /admin (Solusi 
Catatan #3) 
Di dalam /admin, tombol [📖 Buku Manual Developer & SOP Live] kini membuka panduan 
interaktif 4-Bab yang khusus ditulis untuk Anda sebagai Solo Developer: 
●​ Bab 1 (Setup & Ikatan Grup Otomatis): Cara kerja /setup_grup (membuat & mengikat 6 
topik sekaligus via API Telegram) dan /ikat (mengikat topik lama/baru berdasarkan ID 
angka, sehingga bebas ganti nama topik kapan saja). 
●​ Bab 2 (Manajemen Kasir & Limit): Cara mengganti kasir lokal saat limit penuh, cara 
mengaktifkan kedua pembayaran global (USDT + Stars), dan cara melakukan Manual 
Harvest. 
●​ Bab 3 (Operasi /bansos & Infrastruktur): Cara meng-ACC API gratis, mengecek 
domain kosong lintas ekstensi, mengikat storage gratis, dan memakai /pasang_bansos. 
●​ Bab 4 (Arsitektur Teknis & Troubleshooting): Panduan lokasi database abadi 
(~/.bikinai_vault/bikinai_master_vault.db), pemindahan ke VPS, dan pemeriksaan 5 
Sub-Bot Operasional (SangMata Tracker, Welcome Gate, Neural Feed, Auto-Refund, 
Social Auto-Poster). 
4. Upgrade Portal Web Eksternal (NocturneAI) Menjadi Aplikasi Web 
Profesional Utuh — Bisa Chat & Generate Langsung! (Solusi Catatan 
#5) 
Menjawab Catatan #5 Anda: Portal web rekomendasi eksternal (/unfiltered-portal) kini dirombak 



<!-- [ID:08_OMNI_SOCIAL_S074] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 535

Komponen Eksisting 
(v2.5 / v3.2.0) 
Identifikasi Bottleneck / 
Keterbatasan 
Alternatif Proaktif SOTA 
(2026) 
Mekanisme Integrasi 
Additive & Keunggulan 
Teknis 
fungsi atau penyuntikan 
parameter secara 
manual. 
JSON-RPC. Agen 
menemukan alat baru 
secara dinamis saat 
runtime (Dynamic Tool 
Discovery) melalui satu 
titik gateway terpusat 
tanpa memodifikasi 
system prompt utama. 
Jembatan Unfiltered 
(Plausible Deniability 
Bridge) 
Penerbitan Stateless 
Compute Voucher 
(VCH-... dengan 
Ed25519) ke portal web 
eksternal 
(NocturneAI.art) 
memerlukan 
perlindungan terhadap 
pemblokiran domain 
(domain seizure) dan 
scraping. 
Zero-Knowledge 
Ephemeral Relay + 
Automated Fast-Flux 
Domain Rotation 
Mempertahankan tanda 
tangan Ed25519 tanpa 
koneksi database, 
namun menambahkan 
enkripsi payload kueri 
sisi klien dan rotasi 
sub-domain otomatis 
melalui API Cloudflare 
sehingga bot utama di 
Telegram/WA tetap 
100% bersih secara 
hukum. 
Modul 1: Cross-Platform Telemetry dan Automated 
Triage Pipeline 
Untuk mengelola ekosistem yang merentang dari Telegram, WhatsApp, Facebook Messenger, 
Instagram DM, hingga Mini Apps dan Portal Web Independen, sistem tidak dapat 
mengandalkan pemeriksaan log pasif. Diperlukan arsitektur penginderaan aktif (Active Sensing 
Layer) yang menormalisasi seluruh interaksi dan anomali menjadi aliran peristiwa terstruktur 
(Unified Telemetry Event Stream) yang diumpankan secara langsung ke siklus kontrol MAPE-K. 
 



<!-- [ID:08_OMNI_SOCIAL_S075] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 548

Lini Monetisasi & 
Strategi 
Mekanisme Teknis di 
Balik Layar 
Struktur Biaya Modal 
(COGS) & Potongan 
Margin Laba Bersih 
Realistis 
kunci API komunitas 
(seperti Arxpays/AI24X) 
dengan batas waktu 
pemutusan otomatis 
(Auto-Cutoff TTL), lalu 
mengaktifkannya dalam 
Mode Silent. 
membelanjakan Koin 
Utama dengan tarif 
normal. 
Lini 3: Viral 
Watermark Loop + 
Royalti Preset + Float 
Yield (>100% Effective 
Margin) 
Menggabungkan 
Dynamic Dual-Tier 
Watermarking, 
ekonomi royalti kreator 
10% di topik Galeri 
Kreator & Preset, serta 
pencairan dana di 
muka (Upfront Coin 
Float & Breakage). 
Biaya akuisisi 
pelanggan (CAC) 
menjadi negatif karena 
pengguna gratisan 
menjadi papan iklan 
berjalan saat 
membagikan 
video/gambar 
ber-watermark 
@UsernameBotAnda 
ke TikTok/IG/WA. 
105% – 125% 
Effective ROI 
terhadap Pengeluaran 
Operasional 
Untuk memahami bagaimana Lini 3 mampu memberikan pengembalian bersih melampaui 
100% dari pengeluaran operasional komputasi, terdapat tiga mekanisme pengganda uang yang 
bekerja secara otomatis tanpa biaya pemasaran. Pengganda pertama adalah Arsitektur 
Dynamic Dual-Tier Watermarking: setiap permintaan ke API hulu terlebih dahulu dilucuti dari 
tanda air bawaan penyedia melalui parameter nologo=true&private=true. Apabila pengguna 
memakai Koin Bonus (hasil klaim gratis harian di topik Blueprint & Koin Gratis), pipa 
pemrosesan gambar dan video secara otomatis menyematkan tanda air semi-transparan yang 
elegan bertuliskan bikinAI SI • @UsernameBotAnda di sudut kanan bawah. Karena pemrosesan 
pengguna gratisan ini diarahkan oleh Resource-Aware Constraint Solver ke jalur /bansos yang 
berbiaya modal Rp 0, setiap karya yang mereka pamerkan ke TikTok, Instagram, atau grup 
WhatsApp berfungsi sebagai iklan akuisisi gratis yang mendatangkan pengguna berbayar 
baru—khususnya pelaku UMKM dan kreator konten yang rela melakukan Top-Up Koin Utama 
demi memperoleh Commercial Clean License (hasil render 100% bersih tanpa tanda air). 
Pengganda kedua berasal dari pasar kreator mandiri di topik Galeri Kreator & Preset, di mana 
pengguna meracik dan memamerkan preset karya mereka untuk mendapatkan komisi royalti 
koin sebesar 10% setiap kali preset tersebut dipakai oleh anggota lain. Ketika preset populer 
tersebut dieksekusi di atas mesin yang sedang terhubung ke jalur Silent Mode /bansos, platform 
membukukan 90% pendapatan koin tanpa mengeluarkan biaya pembuatan konten maupun 
biaya komputasi hulu. Pengganda ketiga adalah efek Prepaid Coin Breakage & Crypto Float: 
karena seluruh transaksi melalui Kategori 1 (QRIS Direct), Kategori 2 (Duitku, Tripay, Pakasir, 
Midtrans), maupun Kategori 3 (Crypto USDT via @CryptoBot dan Telegram Stars) dibayar lunas 
di muka untuk membeli saldo koin, dana tunai langsung terkumpul di kas sebelum beban API 
muncul. Akumulasi dari persentase saldo koin yang mengendap tidak terpakai oleh pengguna 
kasual (unredeemed breakage) ditambah imbal hasil likuiditas dari saldo USDT sebelum ditarik 
melalui tombol [Harvest Laba Bersih Sekarang (Manual Override)] di panel /admin 
menghasilkan rasio laba bersih terhadap biaya komputasi aktual yang menembus angka di atas 



<!-- [ID:08_OMNI_SOCIAL_S076] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 567

Lini Monetisasi & 
Arbitrase 
Komputasi 
Mekanisme Teknis 
Eksekusi (Otonom 
100%) 
Biaya Modal 
(HPP) 
Harga Jual 
Pelanggan 
Margin Laba 
Bersih Aktual 
Zeigarnik 
Cliffhanger Blur 
Thumbnail saat 
kuota habis. 
Dalam hal pemasaran teknis (technical growth hacking) yang berjalan tanpa tim pemasaran 
manusia, sistem mengombinasikan empat mesin pertumbuhan otonom yang saling 
menguatkan. Pertama, mekanisme Zeigarnik Cliffhanger Blur Upsell ditingkatkan dari 
sekadar menampilkan teks skenario konsep menjadi pratinjau visual nyata berbiaya Rp 0: saat 
seorang pengguna kehabisan kuota gratis harian dan meminta pembuatan video, sistem 
diam-diam merender satu bingkai konsep (keyframe) menggunakan mesin gambar gratis Rp 0 
(Pollinations / HF ZeroGPU) dalam 1,2 detik, menerapkan efek kabur (Gaussian Blur) beserta 
lencana gembok di memori RAM, lalu mengirimkannya ke pengguna bersama kalimat pemicu 
psikologis bahwa konsep visual telah siap di memori sementara dan dapat langsung dieksekusi 
menjadi video HD hanya dengan menekan tombol [Top-Up Instan QRIS Rp 5.000 / Eksekusi 
Sekarang]. Kedua, pada Supergroup Telegram 6 Topik, Activity Bot (Bot #2) menyiarkan 
notifikasi sosial (FOMO telemetry) secara otomatis setiap kali ada pesanan yang berhasil 
diselesaikan (dengan nama pengguna disensor sebagian seperti @M***k dan tanpa 
melampirkan berkas media agar 100% aman dari sensor Telegram), yang kini dilengkapi 
dengan tombol tautan dalam (deep-link) [Gunakan Gaya & Parameter Ini] 
(t.me/bikinAI_bot?start=clone_<job_hash>). Ketika anggota grup menekan tombol tersebut, bot 
utama langsung membuka Kartu Draf Interaktif dengan rasio, durasi, dan mesin AI yang sudah 
terisi persis seperti pesanan sukses tersebut, memangkas friksi pengetikan menjadi nol 
(Zero-Typing). Ketiga, pada saluran WhatsApp (WAHA dengan penundaan pengetikan 
manusiawi Human-Like Typing Jitter) dan Facebook Messenger (Tahap 5), modul Auto-Reply 
Comment Funnel secara otomatis membalas komentar warganet pada unggahan video promosi 
di halaman Facebook/Instagram dengan mengirimkan draf interaktif langsung ke kotak masuk 
Messenger mereka. Keempat, skrip programmatic_seo_gen.py secara berkala men-generate 
lebih dari 500 halaman arahan (landing pages) berdesain Futuristic Luxury (Astro 5.0 / Next.js 
15 + Tailwind v4 di Cloudflare Pages dengan biaya Rp 0) yang menargetkan kata kunci spesifik 
industri UMKM lokal maupun global (seperti "Pembuat Video Iklan Kosmetik TikTok 9:16 
Otomatis" atau "Generator Logo Vektor SVG Kemasan Kopi"), yang langsung mengarahkan 
trafik organik Google ke dalam corong Zero-Typing Wizard Telegram dan Mini App. 
Implementasi Kode Inti Produksi yang Telah Ditambal 
(Patched Core Engine v2.5.1 - Zero-Ops Edition) 
Kode produksi di bawah ini merupakan pemutakhiran langsung (drop-in replacement) untuk 
berkas core_engine_v2_5.py pada Master Blueprint v2.5. Seluruh perbaikan hasil 
audit—meliputi antrean penulis tunggal SingleWriterSQLiteDaemon dengan pemeliharaan 
otomatis .db-wal dan pembersihan berkala phash_audit_log, algoritma de-obfuskasi jendela 
geser anagram untuk menangkap "ilja kaerb" dan substitusi leetspeak, pencairan voucher 
satu-kali redeem_stateless_ed25519_voucher_once dengan Cryptographic Nullifier lokal, 
pemotongan dompet berjenjang (Waterfall Dual-Wallet) beserta reset kuota harian inline tanpa 



<!-- [ID:08_OMNI_SOCIAL_S077] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 592

(Agen #6) serta V2A Foley & Audio Mastering Agent (Agen #7). 
Di dalam siklus eksekusi StateGraph tersebut, Visual Continuity & Character Lock Agent 
bertugas mengekstrak frame terakhir dari klip ke-N menggunakan FFmpeg, membangun 
turnaround sheet (referensi multi-sudut tampak depan, 3/4, dan profil samping), serta 
menyuntikkan embedding identitas wajah melalui PuLID Flux II beserta penguncian deskripsi 
pakaian ke dalam start frame klip ke-(N+1) sehingga transisi antar-adegan 30 detik bebas dari 
character drift. Selanjutnya, setelah keenam klip video selesai dirender, V2A Foley & Audio 
Mastering Agent mengambil alih untuk memisahkan produksi suara menjadi tiga jalur (stems) 
independen: narasi suara (voiceover) dari Kokoro-82M, lapisan suara ambien dan efek gerakan 
sinkron dari MMAudio/HunyuanVideo-Foley, serta musik latar dari Suno/Udio. Agen ke-7 ini 
secara otomatis menerapkan audio ducking (menurunkan desibel ambien dan musik saat narasi 
berbicara), melakukan crossfade pada sambungan antar-segmen, dan menormalisasi 
kekerasan audio sebelum menyerahkan aset akhir ke Media Worker & Compiler Agent untuk 
dijahit menjadi satu file .mp4 utuh. 
Secara makro, topologi sistem yang telah diperluas ini beroperasi dalam empat zona arsitektur 
yang terisolasi secara ketat. Zona Pertama (Omnichannel Ingress & Gatekeeper) menangani 
pesan masuk dari Telegram, WhatsApp, dan Facebook Messenger melalui pemotongan koin 
escrow atomik dan gerbang keamanan berlapis. Zona Kedua (24/7 Receptionist VPS) 
menjalankan LangGraph 7-Agent Supervisor di atas mesin distribusi 9Router dan lapisan 
Valkey Semantic Cache. Zona Ketiga (Dual Execution Pipelines) membelah eksekusi beban 
berat menjadi Jalur Komersial SFW (Fal.ai, Replicate, RunPod Wan 2.2, Suno) dan Jalur 
Sandbox Terisolasi (Universal Compute Voucher pada domain independen dengan pemrosesan 
RAM /dev/shm). Terakhir, Zona Keempat (Zero-Knowledge Edge Delivery) memanfaatkan 
Cloudflare Workers Relay untuk menyedot media dari hulu, melucuti metadata EXIF secara 
streaming, mengenkripsi file menjadi biner .bin di penyimpanan Cloudflare R2, dan 
mendekripsinya langsung di memori RAM peramban pengguna menggunakan Web Crypto API. 
Pipeline Routing Dinamis dan Arsitektur Isolasi Kontainer untuk 
Model Unfiltered 
Sesuai dengan visi produk pada config.py (PILIHAN_OTAK_UNFILTERED yang mencakup 
Nous Hermes 3 Uncensored, Qwen 2.5 72B Instruct, dan Mistral Nemo Unfiltered, serta 
kapabilitas render visual tanpa sensor di Novita AI dan ComfyUI mandiri), sistem dirancang 
untuk melayani kebebasan berekspresi pengguna global (termasuk genre horor, fiksi dewasa, 
dan eksperimen artistik tanpa sensor) sembari tetap menegakkan pencegahan mutlak terhadap 
konten ilegal internasional (seperti CSAM, kekerasan dunia nyata, atau deepfake 
non-konsensual terhadap tokoh nyata yang dicegat oleh InsightFace >23 Tahun dan Negative 
Tensor). Namun, mengizinkan lalu lintas unfiltered bercampur di dalam proses memori atau 
identitas jaringan yang sama dengan Bot Telegram utama (@bikinAI_bot) akan memicu 
pemblokiran oleh pemindai otomatis Telegram maupun pencabutan akun oleh payment gateway 
QRIS lokal. 
Untuk menyempurnakan mekanisme Pre-Flight Heat Router (AGG-04) dan Website Studio 
Independen (NocturneAI.art / VelvetRender.sh) yang telah dirancang pada Bagian V cetak 
biru, Prompt Engineer & Sanitizer Agent menerapkan pemetaan Multi-Dimensional Semantic 
Heat Scoring yang membagi setiap permintaan ke dalam empat zona rute eksekusi 
sebagaimana dirinci pada tabel berikut. 



<!-- [ID:08_OMNI_SOCIAL_S078] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 596

NVIDIA NeMo Guardrails (menggunakan bahasa definisi alur Colang untuk melacak status 
percakapan multi-giliran dan meredaksi PII) dengan klasifikator Llama Guard 3 8B yang 
dikuantisasi ke INT4 (memangkas kebutuhan VRAM ke 4 GB dan latensi p50 ke ~20 ms tanpa 
penurunan akurasi klasifikasi pada 8 bahasa sesuai taksonomi bahaya MLCommons). 
Biometrik Perilaku, Device Fingerprinting, dan Mitigasi Eksploitasi 
Tuyul (Sybil Resistance) 
Sistem ekonomi mikro bikinAI Super Intelligence mengandalkan instrumen akuisisi Klaim 
Harian Rp 400 (4 Koin Bonus) dan Bonus Referral +2 Koin Bonus. Meskipun cetak biru 
telah memisahkan koin_utama dari koin_bonus serta menetapkan bahwa koin_bonus baru 
terbuka penuh untuk fitur mahal (Video Flagship/Suno) apabila akun tersebut pernah melakukan 
Top-Up minimal 1 kali (Rp 5.000) seumur hidup, struktur insentif ini masih menyisakan dua 
celah ekonomi Sybil (tuyul) yang krusial. 
Pertama, terdapat celah Arbitrase Penimbunan Koin Bonus (Hoarding Attack). Operator 
peternakan akun (bot farm) dapat menjalankan 200 akun Telegram kloningan menggunakan 
skrip otomatis untuk mengklaim 4 Koin Bonus per hari selama 30 hari berturut-turut, sehingga 
setiap akun mengumpulkan tabungan 120 Koin Bonus (senilai Rp 12.000). Pada hari ke-30, 
operator hanya perlu membayar Top-Up QRIS sebesar Rp 5.000 pada satu akun untuk 
membuka pembatasan (unlock full access) atas seluruh 120 Koin Bonus tersebut, sehingga 
memperoleh daya beli komputasi senilai Rp 17.000 (cukup untuk merender 8 video 5 detik atau 
11 lagu Suno yang memiliki modal HPP nyata Rp 3.000–Rp 16.500) hanya dengan uang Rp 
5.000. Kedua, ratusan akun tuyul yang tidak pernah melakukan top-up tetap dapat menguras 
kuota free-tier untuk menghasilkan ribuan gambar Flux HD dan Upscale 4K setiap hari guna 
dijual kembali di luar platform, yang pada akhirnya mempercepat habisnya kuota harian API 
milik pelanggan asli. 
Untuk menutup celah ini secara permanen, proses klaim koin harian yang sudah ditempatkan di 
dalam Telegram Mini App (TMA) pada cetak biru wajib diperkuat dengan matriks pertahanan 
Sybil Resistance dan pembatasan ekonomi sebagaimana dirinci pada tabel berikut. 
Lapisan Anti-Fraud 
(Anti-Tuyul) 
Vektor Serangan yang 
Dicegah 
Mekanisme Teknis 
Implementasi (Biaya 
Rp 0) 
Kebijakan Penindakan 
Otomatis 
(Enforcement) 
1. Hardware & WebGL 
Device Fingerprinting 
di TMA 
Peternakan 50–1.000 
akun Telegram 
kloningan di dalam 1 
perangkat 
Android/Emulator 
(LDPlayer, Nox, atau 
skrip Python Telethon). 
Saat pengguna 
membuka Mini App 
untuk klaim harian, 
JavaScript 
mengekstrak hash 
gabungan dari WebGL 
Renderer/Vendor, 
AudioContext 
Oscillator, Canvas 2D 
Entropy, resolusi layar 
fisik, dan daftar font 
sistem. 
Maksimal 2 
telegram_user_id per 
1 
device_fingerprint_ha
sh yang diizinkan 
mengklaim koin harian 
dalam jendela 24 jam. 
Akun ke-3 pada 
perangkat yang sama 
otomatis ditolak 
klaimnya. 
2. Behavioral 
Biometrics & Sensor 
Telemetry 
Bot pengklik otomatis 
(Auto-Clicker / Macro) 
dan injeksi POST 
Merekam kurva 
akselerasi sentuhan 
(touchstart -> touchend 
Jika varians koordinat 
klik = 0,0 (klik robotik di 
piksel yang sama 



<!-- [ID:08_OMNI_SOCIAL_S079] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 603

Kampanye Muse = 25 Koin, Paket Story 30 Detik = 100 Koin), sehingga logika aplikasi dan 
database escrow tidak perlu diubah sedikit pun. Namun, katalog harga Top-Up Koin disesuaikan 
secara otomatis ke dalam 3 Zona Ekonomi (PPP Tiers) sebagaimana dirumuskan dalam tabel 
berikut. 
Zona 
Ekonomi 
(PPP Tier) 
Cakupan 
Negara & 
Kode 
Bahasa 
Harga 
Dasar per 1 
Koin 
Paket 
Pemula (50 
Koin) 
Paket 
Kreator 
(160 Koin) 
Paket 
Agensi 
(600 Koin) 
Harga 
Efektif 
Video 5s 
(20 Koin) 
Margin 
Laba 
Bersih 
Rata-Rata 
Zona 3: 
Penetrasi 
Lokal 
(Indonesia
) 
Indonesia 
(id, IP ASN 
Indonesia, 
Pembayara
n QRIS) 
Rp 100 
(~$0,0062) 
Rp 5.000 
(2 Video + 
2 Gambar 
HD) 
Rp 15.000 
(Bonus 10 
Koin) 
Rp 50.000 
(Bonus 100 
Koin) 
Rp 1.666 – 
Rp 2.000 
(~0, 10–
0,125) 
80% – 85% 
(Tier Pro) / 
45% – 50% 
(Tier Ultra) 
Zona 2: 
Emerging 
Global 
(Menenga
h) 
Asia 
Tenggara 
non-SG 
(ms, vi, th, 
tl), India 
(hi), LATAM 
(es, pt), 
MENA (ar), 
CIS (ru) 
~$0,018 
(~Rp 290) 
$0,99 (atau 
55 
Telegram 
Stars) 
$2,49 (atau 
135 
Telegram 
Stars) 
$7,99 (atau 
430 
Telegram 
Stars) 
$0,26 – 
$0,36 (~Rp 
4.200–Rp 
5.800) 
91% – 94% 
(Tier Pro) / 
75% – 82% 
(Tier Ultra) 
Zona 1: 
Global 
Premium 
(Indeks 
Ekonomi 
Tinggi) 
AS, Inggris, 
Uni Eropa, 
Kanada, 
Australia, 
Jepang, 
Korea, 
Singapura 
(en, de, fr, 
ja, ko) 
~$0,040 
(~Rp 640) 
$1,99 (atau 
110 
Telegram 
Stars) 
$4,99 (atau 
270 
Telegram 
Stars) 
$14,99 
(atau 800 
Telegram 
Stars) 
$0,50 – 
$0,80 (~Rp 
8.000–Rp 
12.800) 
95% – 97% 
(Tier Pro) / 
85% – 90% 
(Tier Ultra) 
Sebagaimana terlihat pada perbandingan ekonomi unit di atas, biaya HPP komputasi di balik 
layar tetap sama (rata-rata Rp 350 per video untuk Tier Pro dan Rp 1.500–Rp 2.500 untuk Tier 
Ultra komersial). Namun, di Zona 1 Global Premium, harga jual efektif 
0,80 per video (Rp 
0, 50–
8.000–Rp 12.800) masih memberikan penghematan lebih dari 40%–50% bagi pengguna 
Barat/Jepang dibandingkan platform SaaS AI lokal mereka (tanpa keharusan berlangganan 
bulanan), sembari mendongkrak margin laba bersih Tier Ultra dari 45%–50% menjadi 
85%–90% dan margin Tier Pro menjadi 95%–97%. 
Mekanisme Penguncian Region (Multi-Factor Geo-Locking) dan Unit 
Economics Lintas Negara 
Mengandalkan variabel message.from_user.language_code == "id" semata sebagai penentu 
harga regional (seperti yang tertulis pada Bagian 3.6 cetak biru) menciptakan celah arbitrase 
harga (regional price spoofing): pengguna dari Amerika Serikat atau Eropa cukup mengganti 
bahasa aplikasi Telegram mereka ke Bahasa Indonesia untuk memunculkan harga Zona 3. 
Untuk menutup celah arbitrase tersebut tanpa menyulitkan pengguna domestik Indonesia, 



<!-- [ID:08_OMNI_SOCIAL_S080] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 604

arsitektur kasir payment_and_support.py wajib menerapkan mekanisme Tri-Factor Payment & 
Telemetry Geo-Locking. 
Kunci pertahanan pertama dan paling absolut adalah Payment Rail Hard-Binding 
(Penguncian Instrumen Pembayaran). Tarif penetrasi Zona 3 (Rp 5.000 / Rp 15.000 / Rp 
50.000) secara eksklusif hanya dapat dibayar menggunakan instrumen QRIS Domestik 
Indonesia (melalui Pakasir, Tripay, atau Duitku). Karena pembayaran QRIS hanya dapat 
dieksekusi melalui aplikasi perbankan atau e-wallet teregulasi Bank Indonesia (BCA, Mandiri, 
BRI, GoPay, OVO, DANA, ShopeePay) yang mewajibkan verifikasi identitas kependudukan 
nasional (e-KTP KYC), warga negara asing di luar Indonesia secara teknis tidak dapat 
menyelesaikan transaksi QRIS meskipun mereka menggunakan VPN Indonesia dan mengubah 
bahasa Telegram ke id. Jika pengguna memilih membayar menggunakan Telegram Stars atau 
Crypto USDT, sistem secara otomatis menonaktifkan harga Rupiah Zona 3 dan menyajikan 
struktur harga Zona 2 atau Zona 1. 
Untuk membedakan secara akurat antara pengguna Zona 2 (Emerging Global - $0,99) dan 
Zona 1 (Global Premium - $1,99) pada saluran pembayaran Telegram Stars serta USDT, 
Cloudflare Worker Edge Relay dan Mini App mengevaluasi korelasi tiga sinyal telemetri: header 
geolokasi jaringan CF-IPCountry dari Cloudflare, reputasi Autonomous System Number 
(CF-Connecting-IP ASN untuk mendeteksi IP datacenter/VPN komersial), serta zona waktu 
sistem operasi perangkat (Intl.DateTimeFormat().resolvedOptions().timeZone) disertai awalan 
nomor telepon jika pengguna terhubung melalui pintu WhatsApp. Pengguna hanya diberikan 
tarif subsidi Zona 2 apabila CF-IPCountry berada di daftar negara Emerging (seperti Malaysia, 
Vietnam, Thailand, India, Brasil, atau Turki), IP bukan berasal dari ASN penyedia VPN/Proxy, 
dan zona waktu perangkat selaras dengan negara tersebut. Apabila terdeteksi ketidaksesuaian 
sinyal (misalnya language_code diatur ke ru atau hi, namun timeZone berada di Europe/London 
atau menggunakan IP VPN), kasir secara otomatis memberlakukan tarif standar Zona 1 Global 
Premium. Sebagai pengaman tambahan terhadap praktik jual-beli akun lintas negara, saldo 
Koin dikunci secara permanen pada internal_user_id pembeli (tidak ada fitur transfer koin 
antar-pengguna) dan pencetakan Universal Compute Voucher dibatasi maksimal 3 voucher aktif 
per hari per akun. 
Dimensi 5: Future-Proofing untuk 50% Dokumen 
Selanjutnya 
Struktur Direktori Modular (Hexagonal Architecture) dan Kontrak 
Skema 
Mengingat cetak biru saat ini berada pada titik 50% dan paruh kedua pengembangan akan 
berfokus pada penulisan kode utuh untuk 6 modul Python (config_and_db.py, security_gate.py, 
muse_router.py, stateless_gpu_worker.py, payment_and_support.py, dan main_bot.py), 
perakitan miniapp_studio.html, pembuatan Cloudflare Worker Edge Relay, serta 
penyambungan webhook WhatsApp dan Facebook Messenger, arsitektur kode harus 
mengadopsi pola Ports and Adapters (Hexagonal Architecture) sejak hari pertama. 
Risiko utang teknis (technical debt) terbesar pada sistem omnichannel adalah mengikat logika 
bisnis agen dan kasir secara langsung pada objek pustaka spesifik platform (seperti 
meneruskan objek aiogram.types.Message milik Telegram langsung ke dalam fungsi 
muse_router.py atau payment_and_support.py). Jika ikatan erat (tight coupling) itu terjadi, maka 



<!-- [ID:08_OMNI_SOCIAL_S081] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 605

ketika developer mengintegrasikan WhatsApp (WAHA / Meta Cloud API) dan Facebook 
Messenger pada Tahap 5, seluruh fungsi agen harus dibongkar ulang. Dengan memisahkan 
Domain Core dari Platform Ingress Adapters dan menstandardisasi kontrak pesan 
menggunakan skema UnifiedMessageEvent berbasis Pydantic v2, penambahan pintu 
komunikasi keempat di masa depan (seperti Discord, Instagram DM, atau aplikasi web mandiri) 
dapat dilakukan dengan zéro refactoring pada ke-7 agen inti. 
Lapisan Arsitektur (Folder / 
Modul) 
File Inti di Dalamnya 
Tanggung Jawab & Prinsip 
Isolasi (Zero-Refactoring 
Guarantee) 
core/domain/ (Kontrak & 
Skema Murni) 
schemas.py, events.py, 
exceptions.py 
Mendefinisikan 
UnifiedMessageEvent 
(abstraksi pesan lintas 
Telegram/WA/FB), JobManifest, 
AgentState (TypedDict untuk 
LangGraph), dan PricingTier. 
Bebas dari library eksternal. 
core/config/ (Hot-Reload 
Saklar 1 Angka) 
config_manager.py, 
pricing_ppp.yaml 
Membungkus variabel 
PILIHAN_MESIN_MEDIA, 
PILIHAN_OTAK_MUSE, 
PILIHAN_OTAK_UNFILTERED
, dan 
PILIHAN_TAMPILAN_MENU di 
dalam Singleton Atomic Config 
yang dapat diubah live lewat 
/admin tanpa me-restart proses 
Python. 
adapters/ingress/ (3 Pintu 
Omnichannel) 
telegram_adapter.py, 
whatsapp_waha.py, 
fb_messenger.py 
Menerjemahkan webhook 
spesifik platform (Aiogram, 
WAHA JSON, Meta Graph API) 
menjadi objek standar 
UnifiedMessageEvent lalu 
mengirimkannya ke 
Gatekeeper. 
services/security/ (Modul 2: 
security_gate.py) 
initdata_auth.py, guardrails.py, 
sybil_shield.py, vision_gate.py 
Menjalankan HMAC-SHA256 
initData + Anti-Replay, sanitasi 
NFKC, Llama Prompt Guard 2 / 
NeMo, verifikasi Device 
Fingerprint TMA, dan 
InsightFace >23 tahun. 
services/agents/ (Modul 3: 
muse_router.py) 
supervisor_graph.py, 
prompt_sanitizer.py, 
continuity_lock.py, 
foley_audio.py 
Mengimplementasikan 7-Node 
LangGraph Supervisor, 
koneksi ke 9Router 
(http://localhost:20128/v1), 
Valkey Semantic Cache, dan 
Heat Score Router. 
services/workers/ (Modul 4: 
stateless_gpu_worker.py) 
comfy_serverless.py, 
wholesale_api.py, 
Mengelola Two-Phase Circuit 
Breaker (3s Cut-Off), 



<!-- [ID:08_OMNI_SOCIAL_S082] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 634

Zona 
Ekonomi 
(PPP Tier) 
Cakupan 
Negara, 
Bahasa & 
Sinyal 
Jaringan 
Harga 
Dasar per 1 
Koin 
Paket 
Pemula (50 
Koin) 
Paket 
Kreator 
(160 Koin) 
Paket 
Agensi 
(600 Koin) 
Harga 
Efektif 
Video 5s 
(20 Koin) 
Margin 
Laba 
Bersih 
Rata-Rata 
Zona 3: 
Penetrasi 
Lokal 
(Indonesia
) 
Indonesia 
(id, IP ASN 
Indonesia, 
Pembayara
n Wajib 
QRIS 
Domestik) 
Rp 100 
(~$0,0062) 
Rp 5.000 
(2 Video + 
2 Gambar 
HD) 
Rp 15.000 
(Bonus 10 
Koin) 
Rp 50.000 
(Bonus 100 
Koin) 
Rp 1.666 – 
Rp 2.000 
(~0, 10–
0,125) 
80%–89% 
(Tier Pro) 
45%–50% 
(Tier Ultra) 
Zona 2: 
Emerging 
Global 
(Menenga
h) 
Asia 
Tenggara 
non-SG 
(ms, vi, th, 
tl), India 
(hi), LATAM 
(es, pt), 
MENA (ar), 
CIS (ru) 
$0,018 
(~Rp 290) 
$0,99 (atau 
55 
Telegram 
Stars) 
$2,49 (atau 
135 
Telegram 
Stars) 
$7,99 (atau 
430 
Telegram 
Stars) 
$0,26 – 
$0,36 (~Rp 
4.200–Rp 
5.800) 
91%–94% 
(Tier Pro) 
75%–82% 
(Tier Ultra) 
Zona 1: 
Global 
Premium 
(Ekonomi 
Tinggi) 
AS, Inggris, 
Uni Eropa, 
Kanada, 
Australia, 
Jepang, 
Korea, 
Singapura 
(en, de, fr, 
ja, ko) 
$0,040 
(~Rp 640) 
$1,99 (atau 
110 
Telegram 
Stars) 
$4,99 (atau 
270 
Telegram 
Stars) 
$14,99 
(atau 800 
Telegram 
Stars) 
$0,50 – 
$0,80 (~Rp 
8.000–Rp 
12.800) 
95%–97% 
(Tier Pro) 
85%–90% 
(Tier Ultra) 
3.3 Penguncian Region Anti-Arbitrase (Tri-Factor Payment & 
Telemetry Geo-Locking) 
Untuk mencegah pengguna dari negara Zona 1 (AS/Eropa) mengubah bahasa Telegram 
mereka ke id demi mendapatkan harga murah Zona 3: 
1.​ Kunci #1 — Payment Rail Hard-Binding (Mutlak): Harga Rupiah Zona 3 (Rp 5.000 / Rp 
15.000 / Rp 50.000) hanya bisa dibayar menggunakan QRIS Domestik Indonesia (via 
Pakasir/Tripay/Duitku) yang mewajibkan akun bank/e-wallet Indonesia ber-KYC e-KTP. 
Jika pengguna memilih membayar dengan Telegram Stars atau Crypto USDT, harga 
Rupiah Zona 3 otomatis terkunci dan sistem menyajikan harga Zona 2 atau Zona 1. 
2.​ Kunci #2 — Korelasi 3 Sinyal Telemetri (Zona 2 vs. Zona 1): Cloudflare Worker & Mini 
App memeriksa kesesuaian antara header geolokasi CF-IPCountry, reputasi 
CF-Connecting-IP ASN (penolak IP VPN/Datacenter), dan zona waktu OS perangkat 
(Intl.DateTimeFormat().resolvedOptions().timeZone). Tarif subsidi Zona 2 hanya 
diberikan jika ketiga sinyal tersebut selaras di negara Emerging tanpa VPN. 
3.​ Kunci #3 — Non-Transferable Wallet & Batas Voucher: Saldo koin dikunci permanen 
pada internal_user_id (tidak ada fitur kirim koin antar-akun) dan pencetakan Ed25519 



<!-- [ID:08_OMNI_SOCIAL_S083] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 637

Lapisan Anti-Fraud 
(Anti-Tuyul) 
Vektor Serangan yang 
Dicegah 
Mekanisme Teknis 
Implementasi (Biaya 
Rp 0) 
Kebijakan Penindakan 
Otomatis 
(Enforcement) 
hari (120 Koin) lalu 
dibuka serentak 
dengan 1x top-up Rp 
5.000. 
TMA sebelum tombol 
klaim aktif, ditambah 
Hard-Cap Saldo 
koin_bonus Maksimal 
25 Koin (Rp 2.500). 
(setara 1 video 5 detik 
+ 1 gambar HD). Klaim 
baru hanya masuk jika 
saldo koin_bonus < 25, 
memaksa sirkulasi 
pemakaian harian yang 
sehat. 
BAGIAN V: HEXAGONAL ARCHITECTURE, SKEMA 
DATABASE TURSO/SQLITE, & KODE INTI v2.0 
5.1 Struktur Direktori Modular (Ports and Adapters / Hexagonal 
Architecture) 
Agar penambahan pintu WhatsApp (WAHA / Cloud API) dan Facebook Messenger pada 
Tahap 5 tidak pernah memaksa pembongkaran ulang kode ke-7 agen inti (Zero-Refactoring 
Guarantee), struktur proyek dikunci sebagai berikut: 
Lapisan Arsitektur (Folder / 
Modul) 
File Inti di Dalamnya 
Tanggung Jawab & Prinsip 
Isolasi (Zero-Refactoring 
Guarantee) 
core/domain/ (Kontrak & 
Skema Murni) 
schemas.py, events.py, 
exceptions.py 
Mendefinisikan 
UnifiedMessageEvent 
(abstraksi pesan lintas 
Telegram/WA/FB), JobManifest, 
AgentState (TypedDict untuk 
LangGraph), dan PricingTier. 
Murni Pydantic v2, bebas dari 
library platform eksternal. 
core/config/ (Hot-Reload 
Saklar 1 Angka) 
config_manager.py, 
pricing_ppp.yaml 
Membungkus variabel saklar 
PILIHAN_MESIN_MEDIA, 
PILIHAN_OTAK_MUSE, 
PILIHAN_OTAK_UNFILTERED
, dan 
PILIHAN_TAMPILAN_MENU di 
dalam Singleton Atomic Config 
yang dapat diubah live lewat 
/admin dalam 0 detik tanpa 
restart. 
adapters/ingress/ (3 Pintu 
Omnichannel) 
telegram_adapter.py, 
whatsapp_waha.py, 
fb_messenger.py 
Menerjemahkan webhook 
spesifik platform (Aiogram, 
WAHA JSON, Meta Graph API) 
menjadi objek standar 
UnifiedMessageEvent lalu 
mengirimkannya ke 



<!-- [ID:08_OMNI_SOCIAL_S084] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 666

Platform 
Cara Integrasi Gratis (Rp 0) 
Keunggulan Strategis untuk 
Bisnis Anda 
1. Telegram Bot 
Daftar resmi di BotFather 
(100% Gratis selamanya, tanpa 
batas pesan). 
Markas Utama (Fitur 
Terlengkap): Mendukung 
menu tombol berlapis, kirim file 
video besar (hingga 2GB), grup 
komunitas Forum Topics, dan 
tampilan Mini App. 
2. Facebook Messenger 
Gunakan Meta for Developers 
(Messenger API Resmi) yang 
dihubungkan ke Facebook 
Page bisnis Anda (100% 
Gratis). 
Mesin Akuisisi Pelanggan 
Viral: Saat Anda posting 
contoh video AI di Facebook, 
pasang fitur Auto-Reply 
Comment. Begitu ada orang 
berkomentar "Mau coba", bot 
otomatis mengirim pesan ke 
inbox Messenger mereka dan 
langsung melayani pembuatan 
gambar/video di sana. 
3. WhatsApp (WA) 
• Opsi A (Resmi): Meta 
WhatsApp Cloud API 
memberikan kuota gratis untuk 
membalas pesan masuk 
(Service Conversations dalam 
jendela 24 jam). • Opsi B 
(Open-Source Mandiri): 
Pasang WAHA (WhatsApp 
HTTP API) atau Baileys di 
VPS Anda (Rp 0, cukup scan 
QR dari nomor WA khusus 
bot). 
Pasar Paling Luas: 
Menjangkau pengguna 
awam/UMKM yang belum 
punya Telegram. Mereka cukup 
simpan nomor WA bot Anda 
dan kirim pesan seperti chatting 
biasa. 
BAGIAN II: FINANSIAL, HITUNGAN BIAYA 
OPERASIONAL 24/7, & SIMULASI KEUNTUNGAN 
2.1 Tabel Biaya Tetap Bulanan (Base Infrastructure 24/7) 
Biaya untuk membiarkan "Toko Utama" (Bot Telegram/WA/FB + 9Router + 5 Agentic AI + 
Database) menyala 24 jam sehari selama 30 hari penuh: 
Komponen 
Skema 1: Gerilya 
(Modal Rp 0) 
Skema 2: Stabil (Modal 
Minim) 
Keterangan 
Server Bot & 9Router 
(24 Jam) 
Rp 0 (Oracle Cloud 
Free / GCP Micro / 
Meta Muse VM) 
Rp 25.000 / bln (VPS 
KVM 1–2GB RAM 
lokal/NatVPS) 
Biaya harian Skema 2 
cuma ~Rp 833 / hari. 
Telegram / FB / WA 
Bot API 
Rp 0 
Rp 0 
Gratis penuh. 
LLM / Teks / Prompt 
(9Router) 
Rp 0 (Combo Full-Free: 
Kiro + Gemini + Groq + 
Rp 16.000 / bln ($1 
saldo cadangan 
9Router memeras yang 
gratis dulu (98% limit), 



<!-- [ID:08_OMNI_SOCIAL_S085] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 671

Sabar (absen klaim 5 hari berturut-turut di Mini App) atau Jalur Cepat (langsung 
Top-Up QRIS Rp 5.000 karena merasa sudah punya tabungan awal). 
2.​ Sistem 2 Dompet Terpisah (koin_utama vs. koin_bonus): 
○​ 🟢 Koin Bonus (Hasil Klaim Harian & Referral Pendaftaran): Bebas dipakai 
100% untuk fitur yang HPP-nya mendekati Rp 0 (Gambar Standar/HD, Upscale, 
Asisten Teks). Untuk fitur yang membakar saldo API/GPU mahal (Video 
Flagship/Suno), Koin Bonus baru terbuka full jika akun tersebut sudah pernah 
melakukan Top-Up minimal 1 kali (Rp 5.000) seumur hidup sebagai verifikasi 
manusia asli, atau berfungsi sebagai potongan diskon Rp 500 per video. 
3.​ Mesin Pertumbuhan Grup Otomatis: Tombol [🎁 Klaim Kredit Harian] mewajibkan 
pengguna sudah tergabung di dalam Grup Komunitas bikinAI (dicek otomatis lewat 
fungsi getChatMember Telegram API). 
3.5 Program Affiliate Gratis (2 Jalur Sekaligus — Modal Rp 0) 
1.​ In-Bot Referral (database.py): Setiap pengguna mendapat tautan 
[https://t.me/bikinAI_bot?start=ref_USERID](https://t.me/bikinAI_bot?start=ref_USERID). 
Pengundang mendapat +2 Koin Bonus saat teman bergabung ke grup, ditambah 
Komisi 10%–15% Koin Utama Seumur Hidup setiap kali teman tersebut melakukan 
Top-Up QRIS/Stars. 
2.​ Telegram Official Affiliate Program (@BotFather): Mengaktifkan fitur afiliasi resmi 
Telegram dengan bagi hasil 15%–20% Telegram Stars, sehingga ribuan pemilik channel 
global ikut mempromosikan bot Anda secara otomatis. 
3.6 Sistem Cerdas Multi-Bahasa Global (Auto-Localization) 
●​ Deteksi Bahasa Otomatis (message.from_user.language_code): Jika bahasa HP 
pengguna adalah id, bot menampilkan antarmuka Bahasa Indonesia & pembayaran 
QRIS. Jika selain id, bot otomatis menyajikan antarmuka Bahasa Inggris Internasional 
& pembayaran Telegram Stars / Crypto USDT. 
●​ Polyglot Muse Translation: Pengguna dari negara mana pun bebas mengetik prompt 
dalam bahasa ibu mereka (Inggris, Indonesia, Rusia, Arab, Jepang, Spanyol); Muse 
otomatis membalas dengan bahasa yang sama namun menerjemahkan instruksi render 
ke bahasa Inggris teknis untuk GPU. 
BAGIAN IV: UI/UX SULTAN SUPER-APP, MODULAR 
GATEWAY, & PANEL SAKLAR 1 ANGKA 
4.1 Smart Multimodal UX di Telegram (Sepintar Aplikasi Gemini/Qwen) 
1.​ Auto-Intent Detection (Tanpa Wajib Ketik /command): Pengguna cukup mengetik 
kalimat biasa, mengirim foto, mengirim dokumen PDF/Word/Excel, atau mengirim Voice 
Note (diterjemahkan via Whisper Free API di Groq). Gatekeeper/Muse otomatis 
mendeteksi niat pengguna (CHAT, GENERATE_IMAGE, GENERATE_VIDEO, 
ORCHESTRATE_CAMPAIGN, READ_DOCUMENT, IMAGE_TO_VIDEO) dalam 0,5 
detik. 


