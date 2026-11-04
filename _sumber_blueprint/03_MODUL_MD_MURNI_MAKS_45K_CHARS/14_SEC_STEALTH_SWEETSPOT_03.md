
<!-- [ID:14_SEC_STEALTH_S025] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 1

Direktori dan Analisis Platform AI 
Multimodal dengan Pendaftaran Instan 
Setara Dahl Global 
Untuk mendapatkan pengalaman pendaftaran yang sama persis dengan Dahl Global 
(inference.dahl.global)—yakni pembuatan akun instan di browser menggunakan pengenal 
kriptografis (fingerprint atau token ID) tanpa verifikasi email, tanpa SMS, tanpa CAPTCHA, dan 
tanpa kartu kredit—namun dilengkapi fitur lengkap untuk generasi gambar, video, suara, 
musik, riset web, pembuatan kode, dan model Frontier SOTA terbaru, pilihan utama yang 
aktif per Oktober 2026 adalah NanoGPT (nano-gpt.com), PayPerQ (ppq.ai), Pollinations.ai 
(pollinations.ai), BazaarLink (bazaarlink.ai), dan Venice AI (venice.ai). Sementara Dahl 
Global hanya menyediakan 4 hingga 5 model teks open-source di atas jaringan GPU 
terdesentralisasi Gonka (MiniMax M2.7, DeepSeek Flash, GLM 5.3 Flash, Qwen 3.8 Flash, 
serta Kimi K2.6 yang tercatat di komunitas), kelima platform alternatif tersebut menerapkan 
arsitektur autentikasi tanpa friksi (zero-friction auth) yang setara sekaligus membuka akses ke 
ratusan hingga lebih dari seribu model lintas modalitas. 
Kemunculan ratusan situs serupa dengan harga sangat murah dan pendaftaran sederhana 
didorong oleh dua fondasi infrastruktur yang berkembang pesat pada tahun 2026. Pertama, 
Dahl Global sejatinya merupakan salah satu broker di atas protokol komputasi terdesentralisasi 
Gonka Network, yang melalui layanan OpenBroker (openbroker.gonka.gg) telah 
memfasilitasi 164 broker terdaftar dengan akses model dan struktur harga yang nyaris identik. 
Kedua, ratusan situs AI relay di tingkat global maupun lokal (termasuk di Indonesia) dibangun 
menggunakan perangkat lunak open-source New API (QuantumNous/new-api) dan One API 
(songquanpeng/one-api) yang memungkinkan operator mana pun membuka gerbang API 
kompatibel OpenAI tanpa CAPTCHA dalam hitungan menit. Namun, hasil pengujian dari 
BazaarLink Probe pada Oktober 2026 menunjukkan bahwa sejumlah situs relay tidak resmi 
melakukan praktik model swapping (mengganti model SOTA dengan model yang lebih murah 
secara diam-diam) dan token padding, sehingga pemilihan platform perlu memprioritaskan 
penyedia yang transparan dan teruji. 
Bedah Mekanisme Dahl Global: Mengapa Sangat 
Murah dan Mudah? 
Memahami cara kerja Dahl Global (inference.dahl.global) adalah langkah awal untuk 
menyaring ratusan situs lain yang benar-benar menggunakan mekanisme serupa. Dokumentasi 
teknis Dahl Inference menunjukkan bahwa platform ini menghilangkan seluruh alur pendaftaran 
tradisional (seperti konfirmasi email, OTP nomor telepon, atau CAPTCHA berlapis) dan 
menggantinya dengan tiga tahapan autentikasi berbasis fingerprint satu kali: 
1.​ Pembuatan Akun Khusus Browser (Browser-Only Sign-Up): Pengguna cukup 
membuka inference.dahl.global/account melalui peramban web dan mengetikkan 
username sederhana sepanjang 3–20 karakter (huruf, angka, atau garis bawah). 
Permintaan pendaftaran dari script otomatis atau curl ditolak dengan kode 403 
browser_required, yang menggantikan fungsi CAPTCHA tradisional tanpa menyulitkan 



<!-- [ID:14_SEC_STEALTH_S026] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 2

pengguna manusia. 
2.​ Kunci Fingerprint 32 Karakter Sebagai Password: Begitu akun dibuat, sistem 
menampilkan 32-karakter fingerprint tepat satu kali di layar. Fingerprint ini berfungsi 
sebagai kata sandi sekaligus identitas tunggal Anda; server hanya menyimpan nilai 
hash-nya dan secara desain tidak menyediakan pemulihan via email. Untuk masuk 
kembali (sign in), Anda bahkan tidak memerlukan username—cukup mengirimkan 
fingerprint 32 karakter tersebut. 
3.​ Alokasi Kuota Gratis 100 Juta Token: Saat akun aktif, kunci API pertama (Bearer API 
key) langsung diterbitkan dengan saldo awal 0 token, sementara bonus selamat datang 
sebesar 100 juta token gratis dimasukkan ke dalam account pool yang tinggal 
dialokasikan pengguna ke kunci API tersebut sebelum memanggil endpoint 
/v1/chat/completions. 
Harga Dahl Global yang sangat rendah—yakni $0.30 untuk volume harian 10 juta token 
(input + output), atau diklaim hingga 99% lebih hemat dibandingkan rata-rata korporat sebesar 
$40.00—dimungkinkan karena Dahl tidak mengoperasikan pusat data terpusat sendiri, 
melainkan bertindak sebagai gateway untuk Gonka Network (gonka.ai). Gonka adalah 
jaringan Layer-1 terdesentralisasi berbasis Proof-of-Compute (PoC) yang didukung oleh 
investasi $50 juta dari Bitfury dan mengoordinasikan sekitar 11.000 hingga 14.000+ GPU setara 
H100 milik penyedia perangkat keras independen. Keterbatasan utama Dahl Global adalah 
cakupannya yang hanya melayani model teks dan kode yang disepakati oleh tata kelola 
(governance) jaringan Gonka, sehingga tidak menyediakan fitur pembuatan gambar, video, 
suara, musik, maupun model SOTA tertutup (closed-source). 
5 Website Multimodal "All-in-One" dengan Cara Daftar 
Setara Dahl Global (Live Oktober 2026) 
Jika syarat utama Anda adalah cara daftar yang mengikuti filosofi Dahl (tanpa verifikasi 
email, tanpa CAPTCHA, tanpa KYC, menggunakan token/ID rahasia atau langsung pakai di 
browser) tetapi wajib memiliki generasi gambar, video, suara, musik, riset, coding, dan LLM 
Frontier SOTA, berikut adalah analisis mendalam terhadap 5 platform utama yang beroperasi 
penuh per Oktober 2026. 
1. NanoGPT (nano-gpt.com & cake.nano-gpt.com/studio) — Kembaran 
Terbaik & Terlengkap 
NanoGPT merupakan padanan paling komprehensif untuk kebutuhan Anda karena 
menggabungkan sistem autentikasi tanpa akun milik Dahl dengan katalog multimodal yang 
mencakup 1.212 model AI dari 122+ laboratorium AI (dengan 110 model baru ditambahkan 
dalam 30 hari terakhir per akhir Oktober 2026). Anda tidak perlu membuat akun, memasukkan 
email, atau melewati pemeriksaan KYC untuk mulai menggunakannya. Begitu membuka 
nano-gpt.com, sistem secara otomatis membuat User ID lokal di peramban dan mengizinkan 
Anda langsung mencoba model gratis di web. Untuk memulihkan sesi dan saldo di perangkat 
lain tanpa email—persis seperti fungsi fingerprint 32 karakter di Dahl—Anda cukup membuka 
menu Settings dan men-generate Revocable Sign-in Token (atau menggunakan Passkey 
terenkripsi). Kunci API tunggal (single key) langsung tersedia tanpa registrasi akun dan 
kompatibel penuh dengan standar OpenAI. 



<!-- [ID:14_SEC_STEALTH_S027] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_92 -->
## Halaman 5

(mendukung hingga 8 gambar referensi untuk konsistensi karakter), GPT Image, Seedream, 
NanoBanana, dan Kontext, sementara generasi video mendukung text-to-video, image-to-video, 
dan transisi keyframe awal-akhir menggunakan Seedance, Veo (alpha), dan Wan-Fast. Untuk 
suara dan musik, Pollinations mengintegrasikan ElevenLabs (>30 pilihan suara yang 
kompatibel langsung dengan format TTS OpenAI), Whisper STT di atas infrastruktur OVHcloud 
dengan fitur speaker diarization (pemisahan pembicara berformat JSON), serta pembuatan 
musik dan sintesis video musik. 
4. BazaarLink 
(bazaa[span_92](start_span)[span_92](end_span)rlink.ai / 
api.bazaarlink.ai/v1) — Pendaftaran Mandiri 1 Perintah POST Tanpa 
Captcha 
Berbasis di Taiwan dengan pemrosesan data di Tokyo (AWS bersertifikasi ISO 27001 dan SOC 
2), BazaarLink menawarkan metode pendaftaran tanpa formulir web, tanpa email, dan tanpa 
CAPTCHA melalui fitur AI Agent Self-Registration yang dibuka kembali pada Oktober 2026. 
Pengguna atau agen cukup mengirimkan satu permintaan POST ke 
https://bazaarlink.ai/api/v1/agents/register berisi payload name. Server langsung 
mengembalikan api_key (ditampilkan satu kali saja, persis seperti fingerprint Dahl) dan 
claim_token yang berlaku selama 7 hari untuk mengklaim akun di kemudian hari. Akun tanpa 
deposit ini langsung dapat memanggil 6 model gratis (atau menggunakan perutean pintar 
"model": "auto:free") dengan batas 10 RPM dan 60 unit tertimbang per hari. Untuk 
menggunakan model berbayar tanpa kartu kredit atau akun bank, agen dapat mendaftar dan 
melakukan top-up secara gasless menggunakan protokol kripto POST 
https://bazaarlink.ai/api/v1/agents/register/x402 (menggunakan USD₮0 di jaringan X Layer 
melalui fasilitator OKX x402). 
Katalog BazaarLink menaungi 180+ model aktif (mencakup 169 model teks, 101 model 
gambar, 42 model video, 44 model file, dan 18 model audio). Enam model gratisnya meliputi 
Qwen3.7 Flash, DeepSeek V4 Flash 0731 (Free), NVIDIA Nemotron 3.5 Lightning Free, stealth: 
Glyph Cluster (coding), reflection: Beam Free, dan reflection: Beam. Pada jajaran Frontier 
SOTA berbayar, BazaarLink menawarkan diskon besar seperti Gemini 4 Argon (diskon 50%), 
Gemini 3.8 Flash & 3.7 Flash (diskon 50%), DeepSeek V4.1 Flash 1017 (diskon 30%, yang 
menurut blog platform mengungguli Opus 5 pada benchmark coding DeepSWE dengan biaya ~
2 input / $10 output), dan 
0. 2𝑝𝑒𝑟𝑡𝑢𝑔𝑎𝑠), 𝐷𝑒𝑒𝑝𝑆𝑒𝑒𝑘𝑉4𝑃𝑟𝑜0813(𝑑𝑖𝑠𝑘𝑜𝑛30%), 𝐾𝑖𝑚𝑖𝐾3. 1𝑃𝑟𝑜(
Claude Haiku 5.5. Untuk kebutuhan multimodal dan riset, tersedia endpoint 
/v1/images/generations (openai/gpt-image-2.5-sunburst), /v1/videos (bytedance/seedance-2.5, 
seedance-2.0, Veo 3.1, MiniMax Hailuo 3 Max, Grok Imagine Video 1.5 Lite), 
/v1/audio/transcriptions, Web Search API kompatibel Tavily (search, extract, crawl, map), 
serta fitur pencarian web dan media sosial live dengan menambahkan akhiran :online atau 
:social pada ID model (gratis 5 pencarian/hari tanpa saldo, atau 10 pencarian/hari dengan 
saldo). 
5. Venice AI (venice.ai / api.venice.ai/api/v1) — Penggunaan Tanpa 
Akun & Autentikasi Wallet x402 
Venice AI adalah platform berfokus privasi dan tanpa sensor (uncensored) yang menyediakan 
272 model AI lintas teks, gambar, video, audio, musik, dan kode. Untuk penggunaan dasar di 



<!-- [ID:14_SEC_STEALTH_S028] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SP
AN_121, S
PAN_121 -->
## Halaman 9

Nama 
Platform & 
Endpoint 
Mekanisme 
Pendaftara
n (Setara 
Dahl) 
Kuota 
Gratis / 
Deposit 
Minimum 
LLM 
Frontier 
SOTA & 
Coding 
Generate 
Gambar 
Generate 
Video 
Suara 
(TTS/STT) 
& Musik 
Fitur Riset 
& Agen 
d_span)[sp
an_121](st
art_span)[s
pan_121](e
nd_span)ce
.ai/api/v1) 
tanpa API 
key/email 
USD/DIEM/
x402 
(816B 
coding), 
DeepSeek 
V4.1 Flash, 
Mercury 3 
(1000+ 
tok/s) 
background
, buat 
variasi 
Veo, 
Runway, 
Seedance, 
Wan 2.7 
ech (Voice 
Mode) 
real-time, 
E2EE TEE 
Enclave 
Jaringan Kembaran Langsung Dahl Global: Ekosistem 
Broker Gonka Network 
Apabila Anda menyukai Dahl Global secara spesifik karena infrastruktur Gonka Network-nya 
(kuota token gratis jutaan hingga ratusan juta token dan biaya seperseratus sen dolar), penting 
untuk diketahui bahwa Dahl hanyalah satu dari banyak pintu masuk ke jaringan yang sama. 
Berdasarkan data live dari portal komunitas gnk.space/try dan pemantau jaringan 
power.gnk.space (Oktober 2026), terdapat 2,65 juta inferensi harian (12,86 miliar token/24 
jam) yang mengalir melalui berbagai broker dan gateway saudara Dahl Global. 
Pintu masuk resmi terbesar adalah Proxy by Gonka.gg (proxy.gonka.gg / Base URL: 
https://api.proxy.gonka.gg/v1), sebuah proxy produksi buatan Gonka Labs yang menangani 
35,3% dari seluruh trafik gateway jaringan Gonka (4,54 miliar token/24 jam). Cara daftarnya 
sangat mirip dengan Dahl: pendaftaran instan tanpa kartu kredit, langsung mendapatkan 
1.000.000 token gratis, dan kunci rahasia sk-... hanya ditampilkan satu kali (dashboard hanya 
menyimpan hash dan 8 karakter awal, persis seperti fingerprint Dahl). Keunggulan utamanya 
dibandingkan Dahl adalah harga dasar yang jauh lebih rendah—mulai dari $0.00123 per 1 juta 
token (tarif flat yang sama untuk input dan output) serta bonus 2x lipat volume token jika 
mengisi saldo dengan kripto GNK atau WGNK. Selain itu, proxy.gonka.gg dilengkapi fitur 
Workspaces (agen AI yang menulis dokumen, slides presentasi, tabel sheets, dan kode dalam 
satu sesi), dukungan MCP di dalam chat, Web Search, Deep Research, serta kemampuan 
membaca lampiran file (PDF, XLSX, CSV, HTML, gambar) tanpa biaya tambahan. 
Gonka Labs juga mengoperasikan OpenBroker (openbroker.gonka.gg / Base URL: 
https://api.openbroker.gonka.gg/v1) sebagai "broker untuk para broker" dengan markup 0%. 
Layanan inilah yang menjelaskan mengapa ratusan situs serupa Dahl bermunculan: tercatat 
ada 164 broker terdaftar di OpenBroker yang memproses rata-rata 31,5 miliar token per hari. 
Pendaftarannya menggunakan dompet kripto sebagai identitas (wallet-as-identity), 
melakukan deposit minimal 100 GNK untuk mengaktifkan akun, dan pengguna langsung dapat 
menerbitkan kunci API (obk-...) sendiri untuk memanggil MiniMax M2.7, DeepSeek V4 Flash, 
dan GLM 5.3 Flash. Bagi pengguna yang ingin menjalankan gateway sendiri di komputer lokal 
tanpa kunci API sama sekali, Gonka Labs menyediakan OpenGNK (github.com/gonkalabs), 
sebuah proxy berbasis Docker di http://localhost:8080/v1 dengan konfigurasi 
api_key="not-needed" yang dapat dipadukan dengan token uji coba gratis dari gonka.gg/faucet. 
Selain layanan inti Gonka Labs, terdapat sejumlah broker independen di jaringan Gonka 
dengan fitur tambahan yang melengkapi kekurangan Dahl Global: 



<!-- [ID:14_SEC_STEALTH_S029] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_183, SPAN
_183 -->
## Halaman 10

Nama Broker 
Gonka 
Base URL 
Endpoint 
Metode Daftar & 
Bonus Gratis 
Harga Dasar (Per 
1M Token) 
Fitur pembeda dari 
Dahl Global 
Proxy by 
Gonka.gg 
(proxy.gonka.gg) 
https://api.proxy.go
nka.gg/v1 
Daftar tanpa kartu; 
kunci sk-... tampil 
1x; 1M token 
gratis 
Mulai $0.00123 / 
1M (input = 
output); bonus 2x 
via GNK/WGNK 
Memiliki 
Workspaces 
(Docs, Slides, 
Sheets), MCP, 
Web Search, 
Deep Research, 
dan baca 
file/gambar gratis 
Easy GonkaAI 
API 
(gonka-api.org) 
https://h[span_183
](start_span)[span
_183](end_span)s
kyauefqcgbvgvxklu
j.supabase.co/func
tions/v1/gonka 
Daftar tanpa kartu 
(tersedia mode 
For Agents); 10M 
token gratis 
Pay-as-you-go via 
kripto tanpa 
langganan 
Menambahkan 
fitur Vision 
(pengenalan 
gambar) & 
Real-Time Web 
Search otomatis, 
Stable JSON 
mode, dan Private 
data masking 
GonkaRouter 
(gonkarouter.io) 
https://api.gonkaro
uter.io/v1 
Pendaftaran 
instan; 10M token 
gratis (atau $20 
kredit awal tercatat 
di indeks) 
Mulai $0.0048 / 
1M (pembayaran 
crypto-native) 
Optimasi konteks 
panjang 1M token 
pada 
GLM-5.3-Flash, 
mendukung 
Function Calling 
dan Private VPC 
Deployment 
JoinGonka 
Gateway 
(gate.joingonka.ai) 
https://gate.joingon
ka.ai/v1 
Daftar 2 menit; 
kunci jg-... tampil 
1x; 3M token 
gratis 
$0.008 / 1M 
(diklaim ~630x 
lebih murah dari 
GPT-5.5) 
Mendukung 2 
format API 
sekaligus dengan 
1 kunci: OpenAI 
(/v1/chat/completio
ns) & native 
Anthropic 
(/v1/messages) 
untuk Claude 
Code 
Gonka24 
(gonka24.com) 
https://api.gonka24
.com/v1 
Daftar tanpa kartu 
kredit; $10 kredit 
gratis 
MiniMax M2.7: 
0.072; 
0. 018/
DeepSeek V4 
Flash: 
0.14; 
0. 07/
Kimi K2.6: 0. 055/
0.32 
Menyediakan 
adaptor Anthropic 
Messages untuk 
Claude Code, 
Cursor, Cline, 
Continue, dan 
Aider 
GonkaGate 
(gonkagate.com) & 
Hyperfusion 
https://api.gonkaga
te.com/v1 & 
https://api.hyperfus
Kunci gp-... 
dengan saldo 
prabayar USD 
Rincian biaya 
jaringan + biaya 
platform terpisah 
Mendukung 
streaming, tool 
calling, dan 



<!-- [ID:14_SEC_STEALTH_S030] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 19

VPS maupun mesin lokal Anda. 
1A. Umpan Proksi Publik, Cermin CDN (jsDelivr/Fastly), API Nir-Kunci 
& Daemon Pemanen Lokal 
1.​ Monosans Proxy List (Repositori Induk) — URL Polos: 
https://github.com/monosans/proxy-list — Kegunaan & Aturan Terbaru: Repositori utama 
penyedia daftar proksi HTTP, SOCKS4, dan SOCKS5 gratis yang diperiksa ulang setiap 
jam menggunakan proxy-scraper-checker tanpa batas kuota dan tanpa kunci API, 
diurutkan dari waktu respons tercepat. 
2.​ Monosans SOCKS5 (Direct Raw Stream) — URL Polos: 
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt — 
Kegunaan & Aturan Terbaru: Umpan teks mentah daftar proksi SOCKS5 aktif yang dapat 
langsung dihubungkan ke skrip perayap web atau perintah terminal tanpa autentikasi. 
3.​ Monosans HTTP Proxy (Direct Raw Stream) — URL Polos: 
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt — Kegunaan 
& Aturan Terbaru: Umpan teks mentah proksi HTTP tercepat siap pakai untuk rotasi 
alamat IP otomatis pada modul web scraping. 
4.​ Monosans Metadata Proksi & ASN (JSON Stream) — URL Polos: 
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies.json — Kegunaan & 
Aturan Terbaru: Umpan berformat JSON yang memuat detail waktu timeout, alamat 
exit_ip, nomor sistem otonom (ASN), dan geolokasi MaxMind GeoLite2 untuk pemfilteran 
proksi berbasis negara secara terprogram. 
5.​ Monosans Geolocation Anonymous SOCKS4 (Raw Stream) — URL Polos: 
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation_anony
mous/socks4.txt — Kegunaan & Aturan Terbaru: Daftar proksi SOCKS4 anonim yang 
telah dikelompokkan dengan informasi geolokasi (tautan telah diperbaiki dari kesalahan 
format https//raw.githubu: pada dokumen sumber). 
6.​ Monosans jsDelivr CDN Mirror (HTTP, SOCKS5 & SOCKS4) — URL Polos HTTP: 
https://cdn.jsdelivr.net/gh/monosans/proxy-list@main/proxies/http.txt | URL Polos 
SOCKS5: https://cdn.jsdelivr.net/gh/monosans/proxy-list@main/proxies/socks5.txt | URL 
Polos SOCKS4: https://cdn.jsdelivr.net/gh/monosans/proxy-list@main/proxies/socks4.txt 
— Kegunaan & Aturan Terbaru: Jalur cermin jaringan distribusi konten (CDN) jsDelivr 
untuk memastikan skrip pemanen proksi tetap berhasil mengunduh daftar IP meskipun 
domain raw.githubusercontent.com mengalami pembatasan laju (rate-limit) atau 
pemblokiran DNS oleh ISP lokal. 
7.​ TheSpeedX PROXY-List (Repositori & Umpan Mega Pool) — URL Polos Repositori: 
https://github.com/TheSpeedX/PROXY-List | URL Polos Raw HTTP: 
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt | URL Polos 
Raw SOCKS4: 
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt | URL Polos 
Raw SOCKS5: 
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt | URL Polos 
Fastly CDN SOCKS5: 
https://fastly.jsdelivr.net/gh/TheSpeedX/PROXY-List@master/socks5.txt | URL Polos 
SOCKS-List: 
https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt — 



<!-- [ID:14_SEC_STEALTH_S031] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 20

Kegunaan & Aturan Terbaru: Kolam proksi berkapasitas masif (menyediakan 5.610 proksi 
aktif terverifikasi per pemindaian dibandingkan sekitar 408 pada Monosans) beserta 
cermin Fastly CDN sebagai jalur failover utama saat umpan dasar mengalami kejenuhan 
pengguna konkuren. 
8.​ Proxifly Free Proxy List (Repositori & CDN Update 5 Menit) — URL Polos Repositori: 
https://github.com/proxifly/free-proxy-list | URL Polos CDN Semua Proksi: 
https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt | URL Polos 
CDN HTTP: 
https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/http/data.txt | 
URL Polos CDN SOCKS4: 
https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks4/data.txt | 
URL Polos CDN SOCKS5: 
https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks5/data.txt | 
URL Polos CDN Proksi AS: 
https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/countries/US/data.txt — 
Kegunaan & Aturan Terbaru: Memanen dan memvalidasi proksi bebas duplikat setiap 5 
menit dari 143 negara dalam format .json, .txt, dan .csv (pembaruan Oktober 2026 
mencatat 84.522 proksi aktif yang mencakup 77.345 SOCKS5, 5.717 HTTP, 940 HTTPS, 
dan 520 SOCKS4). Dapat dipanggil langsung melalui URL CDN di atas atau melalui 
modul npm install proxifly tanpa registrasi. 
9.​ Jetkai Proxy-List (Raw HTTP/HTTPS & Fastly CDN SOCKS5) — URL Polos Raw 
HTTP: 
https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt | 
URL Polos Raw HTTPS: 
https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt 
| URL Polos Fastly CDN SOCKS5: 
https://fastly.jsdelivr.net/gh/jetkai/proxy-list@main/online-proxies/txt/proxies-socks5.txt — 
Kegunaan & Aturan Terbaru: Umpan proksi terverifikasi yang memisahkan proksi 
mendukung HTTPS secara spesifik dan menyediakan jalur Fastly CDN untuk ketahanan 
jaringan. 
10.​Roosterkid OpenProxyList (Raw & Fastly CDN) — URL Polos Raw HTTPS: 
https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt | URL 
Polos Raw SOCKS5: 
https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt | URL 
Polos Fastly CDN HTTPS: 
https://fastly.jsdelivr.net/gh/roosterkid/openproxylist@main/HTTPS_RAW.txt — Kegunaan 
& Aturan Terbaru: Umpan mentah proksi HTTPS dan SOCKS5 independen untuk 
memperkaya variasi subnet IP pada mesin rotasi proksi lokal. 
11.​Clarketm, Hookzof, BlackSnowDot & Rantai 10+ Umpan Proksi GitHub Lainnya — 
URL Polos Clarketm: 
https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt | URL Polos 
Hookzof SOCKS5: https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt 
| URL Polos Hookzof Telegram SOCKS JSON: 
https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/socks.json | URL Polos 
Hookzof Telegram MTProto JSON: 
https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/mtproto.json | URL Polos 
BlackSnowDot HTTP (Update 1 Menit): 
https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/http



<!-- [ID:14_SEC_STEALTH_S032] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 21

.txt | URL Polos BlackSnowDot HTTPS: 
https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/http
s.txt | URL Polos BlackSnowDot SOCKS: 
https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/soc
ks.txt | URL Polos ShiftyTR HTTP: 
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt | URL Polos 
ShiftyTR HTTPS: https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt | 
URL Polos ShiftyTR SOCKS5: 
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt | URL Polos 
UptimerBot HTTP: 
https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt | URL Polos 
UptimerBot SOCKS5: 
https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt | URL 
Polos RX4096 HTTP: 
https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.txt | URL Polos 
RX4096 SOCKS5: 
https://raw.githubusercontent.com/RX4096/proxy-list/main/online/socks5.txt | URL Polos 
mmpx12 HTTP: https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt | 
URL Polos mmpx12 SOCKS5: 
https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt | URL Polos 
manuGMG SOCKS5: 
https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt | URL Polos 
Vakhov Fresh Proxy List: https://github.com/vakhov/fresh-proxy-list | URL Polos GFPCom 
Free Proxy List (V2Ray/XRay/WireGuard): https://github.com/gfpcom/free-proxy-list | URL 
Polos Zloi-User HideIP.me: https://github.com/zloi-user/hideip.me | URL Polos Fate0 
ProxyList: https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list | URL Polos 
Zaeem20 FREE_PROXIES_LIST (Update 10 Menit): 
https://github.com/Zaeem20/FREE_PROXIES_LIST — Kegunaan & Aturan Terbaru: 
Rantai umpan proksi cadangan berlapis yang diperbarui setiap 1 hingga 60 menit dalam 
format TXT, JSON, dan YAML (termasuk dukungan MTProto khusus bot Telegram pada 
Hookzof dan terowongan V2Ray/WireGuard pada GFPCom). 
12.​Titik Akhir REST API Proksi Publik Tanpa Registrasi (Non-GitHub Failover) — URL 
Polos ProxyScrape v2 SOCKS5: 
https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=1000
0&country=all | URL Polos ProxyScrape v2 HTTP: 
https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&co
untry=all | URL Polos GeoNode JSON API: 
https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sor
t_type=desc&protocols=http%2Chttps | URL Polos Proxy-List Download API: 
https://www.proxy-list.download/api/v1/get?type=http | URL Polos ProxyScan API: 
https://www.proxyscan.io/download?type=http | URL Polos OpenProxyList HTTP: 
https://api.openproxylist.xyz/http.txt | URL Polos OpenProxyList SOCKS4: 
https://api.openproxylist.xyz/socks4.txt — Kegunaan & Aturan Terbaru: Titik akhir REST 
API langsung di luar infrastruktur GitHub untuk menjamin ketersediaan suplai IP (1.092+ 
proksi per siklus dari ProxyScrape dan hingga 500 proksi terbaru per halaman dari 
GeoNode) tanpa memerlukan pembuatan akun. 
13.​Daemon Pemanen & Verifikator Proksi Lokal (Proxy Pool Harvesters) — URL Polos 
jhao104 Proxy Pool (Utama): https://github.com/jhao104/proxy_pool | URL Polos ccfleaf 



<!-- [ID:14_SEC_STEALTH_S033] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 22

Proxy Pool (Mirror/Fork): https://github.com/ccfleaf/jhao104-proxy_pool | URL Polos 
WangYihang Go Proxy-Verifier: https://github.com/WangYihang/Proxy-Verifier | URL Polos 
WangYihang Sources Config: 
https://raw.githubusercontent.com/WangYihang/Proxy-Verifier/main/sources.yaml | URL 
Polos pchide Proxy-List-Live (Update 2-3 Menit): https://github.com/pchide/Proxy-List-Live 
| URL Polos VolkanSah Auto-Proxy-Fetcher: 
https://github.com/VolkanSah/Auto-Proxy-Fetcher | URL Polos GokuCodeZ Proxy-Scraper 
(10k/10s): https://github.com/GokuCodeZ/Proxy-Scraper | URL Polos noctiro getproxy: 
https://github.com/noctiro/getproxy | URL Polos saschazesiger 
Proxy-Grabber-and-Checker: 
https://github.com/saschazesiger/Proxy-Grabber-and-Checker — Kegunaan & Aturan 
Terbaru: Perangkat lunak daemon lokal untuk memanen, menguji kebocoran cache/hash 
(melalui arsitektur 4-modul Go pada WangYihang/Proxy-Verifier atau validasi ip.sb pada 
jhao104/proxy_pool), menyimpan proksi hidup ke Redis, dan menyajikannya melalui 
endpoint lokal http://127.0.0.1:5010/get/. 
14.​Pollinations AI & Titik Akhir Inferensi Publik Tanpa Kunci (Zero-Auth Endpoints) — 
URL Polos Repositori Pollinations: https://github.com/pollinations/pollinations | URL Polos 
Portal Web & Sandbox: https://pollinations.ai/ | URL Polos Endpoint API Terpadu v0.3.0 
(OpenAI-Compatible): https://gen.pollinations.ai/v1 | URL Polos Dokumentasi API 
Pollinations: https://gen.pollinations.ai/docs | URL Polos Dokumentasi Markdown GitHub: 
https://github.com/pollinations/pollinations/blob/main/APIDOCS.md | URL Polos Portal 
OAuth & Kunci Opsional: https://enter.pollinations.ai | URL Polos PyPI SDK Resmi (Rilis 
Apr 2026): https://pypi.org/project/PollinationAI-SDK/ | URL Polos UncloseAI (Zero-Auth 
Qwen3.8-27B): https://uncloseai.com | URL Polos DuckDuckGo AI Chat: 
https://duckduckgo.com/duckchat | URL Polos AI Horde: https://aihorde.net | URL Polos 
Veo AI Free (6 Request/Jam per IP Tanpa Login): https://veoaifree.com | URL Polos 
Cloudflare AI Playground: https://playground.ai.cloudflare.com — Kegunaan & Aturan 
Terbaru: Titik akhir inferensi nir-kunci yang langsung merespons panggilan HTTP untuk 
pembuatan teks, gambar, video, dan suara sebagai Fallback Mode [1] ketika seluruh 
kuota API komersial/gratis sedang habis. Berdasarkan pembaruan 2026, Pollinations 
menyediakan endpoint publik gratis tanpa kunci serta mendukung standar OpenAI SDK 
penuh di https://gen.pollinations.ai/v1 (kunci publik pk_ lama dibatasi 1 pollen/IP/jam, 
sementara kunci rahasia sk_ dapat dibuat gratis di enter.pollinations.ai), sedangkan 
uncloseai.com menerima string tidak kosong apa pun sebagai kunci untuk menjalankan 
model turboderp/Qwen3.8-27B-exl3 secara langsung. 
1B. Bobot Model LLM Tanpa Sensor (Abliterated / Uncensored) & 
Penalaran SOTA (Direct Pull Tanpa Login) 
Seluruh bobot model di bawah ini menggunakan format .safetensors atau .gguf yang aman dari 
eksekusi kode arbitrer dan dapat diunduh langsung tanpa login menggunakan perintah llama 
serve -hf <repo>, ollama run hf.co/<repo>, atau huggingface-cli download. 
1.​ Ekosistem Huihui-AI (Model Abliterated Generasi Terbaru 2026) — URL Polos Profil 
& Katalog Utama: https://huggingface.co/huihui-ai | URL Polos Qwen3.8-27B Abliterated 
(Safetensors): https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated | URL 
Polos Qwen3.8-27B Abliterated (GGUF): 
https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF | URL Polos 



<!-- [ID:14_SEC_STEALTH_S034] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# --- KUNCI PROXY UNTUK AKUN GRATIS PYTHONANYWHERE ---
apihelper.proxy = {'https': 'http://proxy.server:3128'}

<!-- [ID:14_SEC_STEALTH_S035] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# Tembus Firewall Gratisan
apihelper.proxy = {'https': 'http://proxy.server:3128'}
TOKEN_UTAMA = "8885292945:AAGK66Dng-81kTW9-vv0Yoy4Pzi43nU3ns0"
USERNAME_PA = "bikinaibot"
bot = telebot.TeleBot(TOKEN_UTAMA)
app = Flask(__name__)

<!-- [ID:14_SEC_STEALTH_S036] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## PROTOKOL 2: ALUR KERJA DUAL-REPO (WRITE-CLEAN, DEPLOY-LOCKED)
1. **Sumber Konteks Tunggal:** Saat membaca kode untuk debugging atau penambahan fitur, SELALU tarik kode dari
2. **Standar Shadow Vault (Private Repo):** Kode yang di-commit ke `private_repo_url` harus 100% bersih (Clean
3. **Standar Public Release (Public Repo):** Sebelum melakukan push ke `public_repo_url`, Anda wajib menjalank
4. **Sinkronisasi Turso:** Setiap kali rilis selesai, simpan hash commit Private, hash commit Public, dan kunc

<!-- [ID:14_SEC_STEALTH_S037] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 151

(Langsung Terkoneksi) 
Pada lapisan rotasi IP dan titik akhir publik nir-autentikasi, ketergantungan tunggal pada 
monosans/proxy-list memiliki risiko kejenuhan alamat IP akibat tingginya pengguna konkuren 
yang memanen dari satu daftar yang sama. Penelusuran mendalam terhadap ekosistem 
pemanen proksi terbuka mengungkap repositori dengan frekuensi pembaruan jauh lebih cepat 
(setiap 1 hingga 10 menit), volume kolam IP yang jauh lebih masif (hingga 5.610+ proksi aktif 
per pemindaian pada TheSpeedX/PROXY-List dan 6.900+ bintang pada proxifly/free-proxy-list), 
serta jalur akses melalui jaringan distribusi konten (cdn.jsdelivr.net dan fastly.jsdelivr.net) untuk 
menembus pembatasan laju permintaan (rate-limit) atau pemblokiran ISP terhadap domain 
raw.githubusercontent.com. Selain itu, penyediaan titik akhir REST API nir-kunci seperti 
ProxyScrape v2 dan GeoNode API beserta perkakas verifikasi berbasis Go 
(WangYihang/Proxy-Verifier) menjamin bahwa agen tetap dapat memperoleh IP bersih yang 
teruji bebas cache meskipun seluruh repositori GitHub mengalami gangguan layanan. 
No 
Nama Sumber & 
Fungsi Utama 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Bukti Teknis, 
Kapasitas & Peran 
Failover 
1A.1 
Monosans Proxy 
List (Repositori 
Induk & Raw 
SOCKS5/HTTP/JS
ON) 
Repo: 
https://github.com/
monosans/proxy-li
st SOCKS5: 
https://raw.githubu
sercontent.com/m
onosans/proxy-list/
main/proxies/sock
s5.txt HTTP: 
https://raw.githubu
sercontent.com/m
onosans/proxy-list/
main/proxies/http.t
xt JSON ASN: 
https://raw.githubu
sercontent.com/m
onosans/proxy-list/
main/proxies.json 
CDN HTTP: 
https://cdn.jsdelivr.
net/gh/monosans/
proxy-list@main/pr
oxies/http.txt CDN 
SOCKS5: 
https://cdn.jsdelivr.
net/gh/monosans/
proxy-list@main/pr
oxies/socks5.txt 
CDN SOCKS4: 
https://cdn.jsdelivr.
net/gh/monosans/
proxy-list@main/pr
oxies/socks4.txt 
Geo Anon: 
https://raw.githubu
sercontent.com/m
onosans/proxy-list/
main/proxies_geol
ocation_anonymou
s/socks4.txt 
Diperbarui setiap 
jam tanpa kunci 
API, diurutkan dari 
respons tercepat, 
dilengkapi 
metadata exit_ip, 
ASN, dan 
geolokasi 
MaxMind 
GeoLite2. Jalur 
CDN jsDelivr 
menjamin 
unduhan tetap 
berhasil meski 
GitHub Raw 
diblokir ISP. 
1A.2 
TheSpeedX & 
Proxifly Mega 
Proxy Pools 
(Alternatif Superior 
Volume & 
Kecepatan) 
(Diperluas dari 
umpan dasar 
1A.1) 
TheSpeedX Repo: 
https://github.com/
TheSpeedX/PROX
Y-List Raw HTTP: 
https://raw.githubu
sercontent.com/Th
eSpeedX/PROXY-
TheSpeedX/PROX
Y-List (5,9 ribu 
bintang) 
menyediakan 
5.610 proksi aktif 
terverifikasi 
(dibandingkan 



<!-- [ID:14_SEC_STEALTH_S038] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 152

No 
Nama Sumber & 
Fungsi Utama 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Bukti Teknis, 
Kapasitas & Peran 
Failover 
List/master/http.txt 
Raw SOCKS4: 
https://raw.githubu
sercontent.com/Th
eSpeedX/PROXY-
List/master/socks4
.txt Raw SOCKS5: 
https://raw.githubu
sercontent.com/Th
eSpeedX/PROXY-
List/master/socks5
.txt Fastly CDN: 
https://fastly.jsdeliv
r.net/gh/TheSpeed
X/PROXY-List@m
aster/socks5.txt 
SOCKS-List: 
https://raw.githubu
sercontent.com/Th
eSpeedX/SOCKS-
List/master/socks5
.txt Proxifly 
(Update 5 Menit): 
https://github.com/
proxifly/free-proxy-
list 
~408 pada 
monosans). 
proxifly/free-proxy-
list (6,9 ribu 
bintang) 
memperbarui 
daftar HTTP, 
SOCKS4, dan 
SOCKS5 setiap 5 
menit dari 100+ 
negara. 
1A.3 
Multi-Repo Raw 
Proxy Streams 
(Jalur Rolling 15+ 
Sumber 
Independen) 
(Cadangan 
berlapis untuk 
monosans) 
Jetkai HTTP: 
https://raw.githubu
sercontent.com/jet
kai/proxy-list/main/
online-proxies/txt/p
roxies-http.txt 
Jetkai HTTPS: 
https://raw.githubu
sercontent.com/jet
kai/proxy-list/main/
online-proxies/txt/p
roxies-https.txt 
Jetkai SOCKS5 
(Fastly): 
https://fastly.jsdeliv
r.net/gh/jetkai/prox
y-list@main/online
Menggabungkan 
lebih dari 15 
umpan mentah 
independen yang 
diperbarui setiap 1 
hingga 60 menit 
dalam format TXT, 
JSON, CSV, dan 
YAML (termasuk 
konfigurasi 
V2Ray/XRay, 
WireGuard, dan 
MTProto Telegram 
pada gfpcom dan 
hookzof). 



<!-- [ID:14_SEC_STEALTH_S039] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 153

No 
Nama Sumber & 
Fungsi Utama 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Bukti Teknis, 
Kapasitas & Peran 
Failover 
-proxies/txt/proxies
-socks5.txt 
Roosterkid 
HTTPS: 
https://raw.githubu
sercontent.com/ro
osterkid/openproxy
list/main/HTTPS_
RAW.txt 
Roosterkid 
SOCKS5: 
https://raw.githubu
sercontent.com/ro
osterkid/openproxy
list/main/SOCKS5
_RAW.txt Clarketm 
Raw: 
https://raw.githubu
sercontent.com/cla
rketm/proxy-list/ma
ster/proxy-list-raw.t
xt Hookzof 
SOCKS5: 
https://raw.githubu
sercontent.com/ho
okzof/socks5_list/
master/proxy.txt 
Hookzof 
JSON/MTProto: 
https://raw.githubu
sercontent.com/ho
okzof/socks5_list/
master/tg/socks.js
on & mtproto.json 
BlackSnowDot 
(Update 1 Menit): 
https://raw.githubu
sercontent.com/Bl
ackSnowDot/proxy
list-update-every-
minute/main/http.tx
t & https.txt & 
socks.txt ShiftyTR: 



<!-- [ID:14_SEC_STEALTH_S040] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 154

No 
Nama Sumber & 
Fungsi Utama 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Bukti Teknis, 
Kapasitas & Peran 
Failover 
https://raw.githubu
sercontent.com/Sh
iftyTR/Proxy-List/m
aster/http.txt & 
https.txt & 
socks5.txt 
UptimerBot: 
https://raw.githubu
sercontent.com/Up
timerBot/proxy-list/
main/proxies/http.t
xt & socks5.txt 
RX4096: 
https://raw.githubu
sercontent.com/R
X4096/proxy-list/m
ain/online/http.txt 
& socks5.txt 
mmpx12: 
https://raw.githubu
sercontent.com/m
mpx12/proxy-list/m
aster/http.txt & 
socks5.txt 
manuGMG: 
https://raw.githubu
sercontent.com/m
anuGMG/proxy-36
5/main/SOCKS5.tx
t Vakhov / gfpcom 
/ zloi-user / fate0: 
https://github.com/
vakhov/fresh-proxy
-list, 
https://github.com/
gfpcom/free-proxy-
list, 
https://github.com/
zloi-user/hideip.me
, 
https://raw.githubu
sercontent.com/fat
e0/proxylist/master



<!-- [ID:14_SEC_STEALTH_S041] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 155

No 
Nama Sumber & 
Fungsi Utama 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Bukti Teknis, 
Kapasitas & Peran 
Failover 
/proxy.list 
1A.4 
Zero-Auth Public 
Proxy APIs 
(REST Endpoints 
Tanpa Registrasi) 
(Tambahan jalur 
non-GitHub) 
ProxyScrape v2 
API: 
https://api.proxyscr
ape.com/v2/?requ
est=displayproxies
&protocol=socks5
&timeout=10000&
country=all 
GeoNode JSON 
API: 
https://proxylist.ge
onode.com/api/pro
xy-list?limit=500&p
age=1&sort_by=la
stChecked&sort_ty
pe=desc&protocol
s=http%2Chttps 
Proxy-List 
Download API: 
https://www.proxy-l
ist.download/api/v
1/get?type=http 
(mendukung https, 
socks4, socks5) 
ProxyScan API: 
https://www.proxys
can.io/download?t
ype=http 
OpenProxyList 
API: 
https://api.openpro
xylist.xyz/http.txt & 
socks4.txt 
Memberikan jalur 
pengalihan di luar 
infrastruktur 
GitHub. 
proxyscrape.com 
menyumbang 
1.092+ proksi 
terverifikasi per 
siklus, sementara 
geonode.com 
menyajikan hingga 
500 proksi per 
halaman yang 
diurutkan 
berdasarkan 
lastChecked 
terbaru. 
1A.5 
Proxy Pool 
Auto-Harvester & 
Verifier Engines 
(Daemon Lokal) 
Utama: 
https://github.com/j
hao104/proxy_poo
l 
(http://127.0.0.1:50
10/get/) 
Mirror/Fork: 
https://github.com/
ccfleaf/jhao104-pr
Go Proxy-Verifier: 
https://github.com/
WangYihang/Prox
y-Verifier 
(sources.yaml: 
https://raw.githubu
sercontent.com/W
angYihang/Proxy-
Verifier/main/sourc
jhao104/proxy_po
ol (23,8 ribu 
bintang) 
memvalidasi 
proksi via ip.sb ke 
Redis lokal. 
Sebagai alternatif 
berkinerja tinggi, 
WangYihang/Prox



<!-- [ID:14_SEC_STEALTH_S042] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 156

No 
Nama Sumber & 
Fungsi Utama 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Bukti Teknis, 
Kapasitas & Peran 
Failover 
oxy_pool 
es.yaml) Live 
Scanner (Update 
2-3 Menit): 
https://github.com/
pchide/Proxy-List-
Live 
Auto-Proxy-Fetche
r: 
https://github.com/
VolkanSah/Auto-Pr
oxy-Fetcher Fast 
Scraper (10k/10s): 
https://github.com/
GokuCodeZ/Proxy
-Scraper Shell 
Harvester: 
https://github.com/
noctiro/getproxy 
Grabber & 
Checker: 
https://github.com/
saschazesiger/Pro
xy-Grabber-and-C
hecker 
y-Verifier berbasis 
Go memisahkan 4 
modul 
(downloader, 
echo-server, 
verifier dengan 
validasi hash 
anti-cache, dan 
exporter). 
1A.6 
Pollinations AI 
(Zero-Auth 
Multimodal 
Endpoint & 
Sandbox) 
Repo: 
https://github.com/
pollinations/pollinat
ions 
Web/Endpoint: 
https://pollinations.
ai/ 
Digunakan 
sebagai Fallback 
Mode [1] untuk 
generasi gambar, 
teks, dan audio 
HTTP langsung 
ketika seluruh 
kunci API 
komersial atau 
gratis sedang 
habis kuota. 
Merespons 
permintaan HTTP 
secara instan 
untuk sintesis teks, 
gambar, dan suara 
tanpa pembuatan 
akun maupun 
kunci API. 
1B. Model LLM Uncensored / Abliterated & Penalaran SOTA (Direct Pull tanpa 
Login) 
Seluruh bobot model pada sub-kategori 1B didistribusikan dalam format tensor nir-eksekusi 
yang aman dari penyusupan malware (.safetensors dan .gguf) serta dapat ditarik tanpa akun 
menggunakan perintah llama serve -hf <repo>, ollama run hf.co/<repo>, atau docker model run 
hf.co/<repo>. Sebagai peningkatan substansial di atas model abliterated generasi awal 
(bartowski dan mradermacher), riset mengidentifikasi ekosistem huihui-ai di Hugging Face 



<!-- [ID:14_SEC_STEALTH_S043] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# --- 2. LAYER 1: EDGE NETWORK & PROXY HARVESTER ENDPOINTS ---​
CF_WORKER_PROXY_URL="https://proxy-gateway.domain-anda.workers.dev"​
CF_WORKER_VALID_KEY=""​
LOCAL_PROXY_POOL_API="http://127.0.0.1:5010"​
FORCE_DOH_DNS="https://1.1.1.1/dns-query"​
​

<!-- [ID:14_SEC_STEALTH_S044] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 238

(Langsung Terkoneksi) 
Pada lapisan rotasi IP dan titik akhir publik nir-autentikasi, ketergantungan tunggal pada 
monosans/proxy-list memiliki risiko kejenuhan alamat IP akibat tingginya pengguna konkuren 
yang memanen dari satu daftar yang sama. Penelusuran mendalam terhadap ekosistem 
pemanen proksi terbuka mengungkap repositori dengan frekuensi pembaruan jauh lebih cepat 
(setiap 1 hingga 10 menit), volume kolam IP yang jauh lebih masif (hingga 5.610+ proksi aktif 
per pemindaian pada TheSpeedX/PROXY-List dan 6.900+ bintang pada proxifly/free-proxy-list), 
serta jalur akses melalui jaringan distribusi konten (cdn.jsdelivr.net dan fastly.jsdelivr.net) untuk 
menembus pembatasan laju permintaan (rate-limit) atau pemblokiran ISP terhadap domain 
raw.githubusercontent.com. Selain itu, penyediaan titik akhir REST API nir-kunci seperti 
ProxyScrape v2 dan GeoNode API beserta perkakas verifikasi berbasis Go 
(WangYihang/Proxy-Verifier) menjamin bahwa agen tetap dapat memperoleh IP bersih yang 
teruji bebas cache meskipun seluruh repositori GitHub mengalami gangguan layanan. 
No 
Nama Sumber & 
Fungsi Utama 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Bukti Teknis, 
Kapasitas & Peran 
Failover 
1A.1 
Monosans Proxy 
List (Repositori 
Induk & Raw 
SOCKS5/HTTP/JS
ON) 
Repo: 
https://github.com/
monosans/proxy-li
st SOCKS5: 
https://raw.githubu
sercontent.com/m
onosans/proxy-list/
main/proxies/sock
s5.txt HTTP: 
https://raw.githubu
sercontent.com/m
onosans/proxy-list/
main/proxies/http.t
xt JSON ASN: 
https://raw.githubu
sercontent.com/m
onosans/proxy-list/
main/proxies.json 
CDN HTTP: 
https://cdn.jsdelivr.
net/gh/monosans/
proxy-list@main/pr
oxies/http.txt CDN 
SOCKS5: 
https://cdn.jsdelivr.
net/gh/monosans/
proxy-list@main/pr
oxies/socks5.txt 
CDN SOCKS4: 
https://cdn.jsdelivr.
net/gh/monosans/
proxy-list@main/pr
oxies/socks4.txt 
Geo Anon: 
https://raw.githubu
sercontent.com/m
onosans/proxy-list/
main/proxies_geol
ocation_anonymou
s/socks4.txt 
Diperbarui setiap 
jam tanpa kunci 
API, diurutkan dari 
respons tercepat, 
dilengkapi 
metadata exit_ip, 
ASN, dan 
geolokasi 
MaxMind 
GeoLite2. Jalur 
CDN jsDelivr 
menjamin 
unduhan tetap 
berhasil meski 
GitHub Raw 
diblokir ISP. 
1A.2 
TheSpeedX & 
Proxifly Mega 
Proxy Pools 
(Alternatif Superior 
Volume & 
Kecepatan) 
(Diperluas dari 
umpan dasar 
1A.1) 
TheSpeedX Repo: 
https://github.com/
TheSpeedX/PROX
Y-List Raw HTTP: 
https://raw.githubu
sercontent.com/Th
eSpeedX/PROXY-
TheSpeedX/PROX
Y-List (5,9 ribu 
bintang) 
menyediakan 
5.610 proksi aktif 
terverifikasi 
(dibandingkan 



<!-- [ID:14_SEC_STEALTH_S045] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 239

No 
Nama Sumber & 
Fungsi Utama 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Bukti Teknis, 
Kapasitas & Peran 
Failover 
List/master/http.txt 
Raw SOCKS4: 
https://raw.githubu
sercontent.com/Th
eSpeedX/PROXY-
List/master/socks4
.txt Raw SOCKS5: 
https://raw.githubu
sercontent.com/Th
eSpeedX/PROXY-
List/master/socks5
.txt Fastly CDN: 
https://fastly.jsdeliv
r.net/gh/TheSpeed
X/PROXY-List@m
aster/socks5.txt 
SOCKS-List: 
https://raw.githubu
sercontent.com/Th
eSpeedX/SOCKS-
List/master/socks5
.txt Proxifly 
(Update 5 Menit): 
https://github.com/
proxifly/free-proxy-
list 
~408 pada 
monosans). 
proxifly/free-proxy-
list (6,9 ribu 
bintang) 
memperbarui 
daftar HTTP, 
SOCKS4, dan 
SOCKS5 setiap 5 
menit dari 100+ 
negara. 
1A.3 
Multi-Repo Raw 
Proxy Streams 
(Jalur Rolling 15+ 
Sumber 
Independen) 
(Cadangan 
berlapis untuk 
monosans) 
Jetkai HTTP: 
https://raw.githubu
sercontent.com/jet
kai/proxy-list/main/
online-proxies/txt/p
roxies-http.txt 
Jetkai HTTPS: 
https://raw.githubu
sercontent.com/jet
kai/proxy-list/main/
online-proxies/txt/p
roxies-https.txt 
Jetkai SOCKS5 
(Fastly): 
https://fastly.jsdeliv
r.net/gh/jetkai/prox
y-list@main/online
Menggabungkan 
lebih dari 15 
umpan mentah 
independen yang 
diperbarui setiap 1 
hingga 60 menit 
dalam format TXT, 
JSON, CSV, dan 
YAML (termasuk 
konfigurasi 
V2Ray/XRay, 
WireGuard, dan 
MTProto Telegram 
pada gfpcom dan 
hookzof). 


