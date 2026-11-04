
<!-- [ID:16_INFRA_DEVOPS_S077] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 226

Nama Tabel Fondasi Baru 
Kolom Utama & Kunci Indeks 
Fungsi Arsitektural untuk 50% 
Pengembangan Selanjutnya 
language_code, ppp_zone, 
device_fp_hash 
dan ID Facebook Messenger 
milik 1 orang ke dalam 1 
dompet internal_user_id 
terpadu melalui kode tautan 
lintas-platform. 
wallet_ledger 
tx_id (PK), internal_user_id 
(FK), wallet_type 
('UTAMA','BONUS'), 
delta_amount, balance_after, 
tx_type, idempotency_key 
(UNIQUE), created_at 
Buku besar akuntansi 
append-only (immutable 
ledger). Kolom 
idempotency_key memastikan 
bahwa jika webhook QRIS atau 
Telegram Stars menembak 2–3 
kali karena gangguan jaringan, 
saldo koin pengguna hanya 
bertambah tepat 1 kali. 
phash_audit_log 
job_id (PK), internal_user_id 
(FK), perceptual_hash_64bit 
(INDEX), media_type, 
expires_at (INDEX) 
Mengimplementasikan Blind 
pHash Ledger (48 Jam) pada 
Bagian 5.3 cetak biru. 
Menyimpan sidik jari matematis 
64-bit dari gambar/video untuk 
audit kepatuhan internal Admin, 
yang dihapus otomatis oleh 
cron job setiap 48 jam. 
langgraph_checkpoints 
thread_id (PK), checkpoint_ns 
(PK), checkpoint_id (PK), 
parent_checkpoint_id, 
state_blob, created_at 
Menyimpan status percakapan 
dan kemajuan subtugas 
7-Node LangGraph Supervisor 
secara persisten 
(AsyncSqliteSaver). Jika VPS 
mengalami restart saat 
merender klip ke-3 dari 6 klip 
iklan 30 detik, sistem otomatis 
melanjutkan dari klip ke-4 tanpa 
membakar ulang modal GPU 
klip 1–3. 
Observabilitas Mandiri (Self-Hosted Langfuse) dan Standarisasi 
Dokumentasi API 
Mengoperasikan sistem agregator yang merutekan permintaan melintasi puluhan kunci API 
gratis (98% Quota Surfing), memadatkan konteks (RTK/Caveman), mengorkestrasi 7 agen 
otonom, dan mengeksekusi 3 mode pabrik media (PILIHAN_MESIN_MEDIA 1, 2, dan 3) 
membutuhkan visibilitas telemetri yang presisi agar tidak terjadi kebocoran biaya tersembunyi 
(silent margin erosion). Sebagai solusi open-source bermodal Rp 0, arsitektur perlu 
menyertakan kolektor observabilitas Langfuse Self-Hosted (atau lapisan pencatatan telemetri 
ringan berbasis OpenTelemetry) yang melacak setiap jejak eksekusi agen (agent traces) 
secara asinkron di latar belakang. 
Melalui instrumentasi telemetri ini, setiap pemanggilan dari Muse Orchestrator ke 9Router 



<!-- [ID:16_INFRA_DEVOPS_S078] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 264

(100% Tanpa Kartu Visa/Mastercard) 
Kelompok 2 mengonsolidasikan seluruh penyedia kuota API gratis ("bansos" token), 
infrastruktur basis data, serverless worker, serta gerbang pembayaran lokal dan bot 
omnichannel dari Kelompok 2 (LINK SUMBER.pdf) dan Kategori 1 (Link_daftar_vps 
server.txt). Selain menggabungkan seluruh tautan tersebut, bagian ini menyertakan Audit 
Status Kuota Kuartal IV 2026 berdasarkan bukti riset terkini serta menambahkan penyedia 
alternatif tanpa kartu kredit—seperti Cloudflare Workers AI (10.000 Neurons/hari), Fireworks 
AI ($1 kredit gratis tanpa kartu), Alibaba Cloud Model Studio (~1.000.000 token gratis per 
model), dan Backblaze B2 (10 GB object storage gratis tanpa kartu)—agar skrip auto-rolling 
memiliki cadangan aktif ketika titik akhir lama mengalami perubahan kebijakan. Di samping itu, 
untuk mengimbangi batas kuota API eksternal, pengaktifan TeaCache (ali-vilab/TeaCache) 
pada pipeline difusi lokal mampu mempercepat waktu render video dan gambar sebesar 1,5x 
hingga hampir 3x lipat secara training-free, misalnya memangkas waktu inferensi Wan2.1 T2V 
14B dari 1.829 detik menjadi hanya 578 detik dengan mengaktifkan parameter --use_ret_steps. 
2A. Penyedia Kunci API LLM, Visi & Multimodal Gratis (Tanpa Kartu Kredit) 
Tabel berikut mengintegrasikan seluruh 11 penyedia dari sub-kategori 2A (LINK SUMBER.pdf) 
dan penyedia kognitif dari Kategori 1 (Link_daftar_vps server.txt), dilengkapi dengan parameter 
perutean terbaru dan alternatif pengganti untuk layanan yang mengalami perubahan kebijakan 
pada paruh kedua tahun 2026. Dalam merancang logika perutean, agen memprioritaskan 
Google AI Studio untuk konteks dokumen panjang hingga 1 juta token, Mistral Experiment Tier 
untuk pemrosesan volume masif hingga 1 miliar token per bulan, Groq untuk latensi rendah 
pada tugas latar belakang, dan openrouter/free sebagai penyeimbang beban otomatis yang 
kebal terhadap penghapusan model individual. 
No 
Nama Penyedia 
Layanan 
Tautan 
Pendaftaran & 
Konsol Kunci 
(Eksisting & 
Gabungan) 
Alternatif / 
Endpoint Spesifik 
& Status Audit 
2026 
Kapasitas Kuota 
Gratis, Batas Laju 
& Peran Rolling 
2A.1 
Google AI Studio 
(Gemini API Free 
Tier) 
Konsol Utama: 
https://aistudio.goo
gle.com Direct API 
Key: 
https://aistudio.goo
gle.com/app/apike
y 
Model Aktif 2026: 
gemini-3.5-flash & 
gemini-3.1-flash-lit
e (varian Pro kini 
khusus berbayar). 
100% Tanpa 
Kartu. Mendukung 
jendela konteks 
raksasa hingga 1 
juta token untuk 
pemrosesan 
dokumen panjang 
dan multimodal 
(teks, gambar, 
audio). 
2A.2 
Mistral AI 
Console (Tier 
Eksperimen — 
Volume Gratis 
Terbesar 2026) 
Konsol: 
https://console.mis
tral.ai 
Syarat: Login 
Gmail/GitHub, 
verifikasi nomor 
HP, dan 
mengaktifkan 
opt-in pelatihan 
100% Tanpa 
Kartu. 
Menyediakan 
kuota permanen 
terbesar di industri 
saat ini: ~1 Miliar 



<!-- [ID:16_INFRA_DEVOPS_S079] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 266

No 
Nama Penyedia 
Layanan 
Tautan 
Pendaftaran & 
Konsol Kunci 
(Eksisting & 
Gabungan) 
Alternatif / 
Endpoint Spesifik 
& Status Audit 
2026 
Kapasitas Kuota 
Gratis, Batas Laju 
& Peran Rolling 
Gmail dan 
verifikasi nomor 
HP. 
akses gratis ke 91 
titik akhir model 
(termasuk model 
bahasa, visi, dan 
multimodal SOTA) 
dengan batas laju 
tinggi 40 RPM 
untuk pembuatan 
prototipe dan riset. 
2A.6 
Cloudflare 
Workers AI 
(Alternatif Baru 
Inferensi 
Serverless) 
Pendaftaran: 
https://dash.cloudfl
are.com/sign-up 
Konsol: 
https://dash.cloudfl
are.com 
Catatan 2026: 
Mencakup ~80 
model terbuka; 
model berat 
seperti Kimi 
K2.6/K2.7 Code 
dan GLM-5.2 kini 
memerlukan paket 
berbayar, 
sehingga kuota 
gratis difokuskan 
pada model 
ukuran 
kecil-menengah. 
100% Tanpa 
Kartu. 
Memberikan kuota 
permanen 10.000 
Neurons/hari 
(direset setiap 
pukul 00:00 UTC) 
di samping 
100.000 
permintaan/hari 
untuk Cloudflare 
Workers. 
2A.7 
SiliconFlow, 
Fireworks AI & 
Alibaba Model 
Studio (Kredit 
Sambutan Tanpa 
Kartu) 
SiliconFlow 
(Sumber 3): 
https://cloud.silicon
flow.com/ 
Fireworks AI: 
https://fireworks.ai 
Alibaba Cloud 
Model Studio 
(Wilayah 
Singapura, aktivasi 
mulai Sept 2026). 
SiliconFlow 
menyediakan 
akses ke 
DeepSeek-V4.1-Fl
ash & Qwen. 
Fireworks AI 
memberikan $1 
kredit gratis 
tanpa kartu pada 
laju 10 RPM, 
sementara Alibaba 
Cloud Model 
Studio 
memberikan 
~1.000.000 token 
gratis per model 
(berlaku 90 hari) 
sebelum 
mewajibkan detail 



<!-- [ID:16_INFRA_DEVOPS_S080] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_4 -->
## Halaman 268

No 
Nama Penyedia 
Layanan 
Tautan 
Pendaftaran & 
Konsol Kunci 
(Eksisting & 
Gabungan) 
Alternatif / 
Endpoint Spesifik 
& Status Audit 
2026 
Kapasitas Kuota 
Gratis, Batas Laju 
& Peran Rolling 
terdesentralisasi 
Bittensor. 
2A.11 
Civitai & Spider 
Cloud API (Model 
Unfiltered & Web 
Crawling API) 
Civitai Account 
(Sumber 3): 
https://c[span_4](st
art_span)[span_4](
end_span)ivitai.co
m/user/account 
Spider Cloud API 
(Tanpa Kartu): 
https://spider.cloud 
100% Tanpa 
Kartu. Kunci API 
Civitai digunakan 
untuk menarik 
checkpoint gambar 
tanpa filter dan 
negative 
embeddings 
secara terprogram, 
sedangkan Spider 
Cloud memberikan 
kunci API gratis 
tanpa kartu untuk 
smart web 
scraping. 
2A.12 
Cerebras Cloud, 
GitHub Models & 
SambaNova 
(Status Transisi / 
Legacy) 
Cerebras: 
https://cloud.cereb
ras.ai 
(https://api.cerebra
s.ai/v1) GitHub 
Models: 
https://github.com/
marketplace/model
s SambaNova: 
https://cloud.samb
anova.ai 
Peringatan 
Otomasi Kode: 
Akun lama 
Cerebras masih 
menikmati 1M 
token/hari (2.600+ 
tok/s pada WSE-3 
untuk Llama 4 
Scout, Qwen3 
32B, 
gpt-oss-120b), 
namun per 16 Juli 
2026 akun baru 
dialihkan ke uji 
coba $5 yang 
wajib kartu. GitHub 
Models pensiun 
pada 30 Juli 2026, 
dan SambaNova 
menghentikan 
kredit akun baru 
pada Agustus 
2026. 
Kode agen wajib 
membungkus 
ketiga penyedia ini 
di dalam blok 
try-except dengan 
fallback instan ke 
Mistral (2A.2), 
Google AI Studio 
(2A.1), dan Groq 
(2A.3) apabila 
menerima kode 
status HTTP 401, 
402, 403, atau 
404. 
2B. Infrastruktur Hosting, Proksi Tepi, GPU Notebook, Memori & Database Gratis 



<!-- [ID:16_INFRA_DEVOPS_S081] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 270

No 
Nama Layanan 
Infrastruktur 
Tautan Pendaftaran & 
Repositori (Eksisting & 
Gabungan) 
Peran Utama & Rantai 
Rolling Failover 
Infrastruktur 
Object Storage gratis 
tanpa kartu Visa 
sebagai cadangan 
langsung (failover) 
untuk penyimpanan 
berkas media dan 
model di samping 
Supabase Storage dan 
Cloudflare R2. 
2B.4 
Google Colaboratory 
& Kaggle Notebooks 
(Komputasi GPU Cloud 
Gratis) 
Google Colab (GPU 
T4): 
https://colab.research.g
oogle.com Kaggle (30 
Jam/Minggu Dual-T4 / 
P100): 
https://www.kaggle.com 
100% Tanpa Kartu. 
Digunakan secara 
bergantian (rolling) 
untuk mengeksekusi 
proses abliteration 
bobot model 
(jim-plus/llm-abliteration 
atau AIAnytime/ablate) 
maupun merender 
suara dan video ketika 
mesin lokal tidak 
memiliki GPU 
memadai. 
2B.5 
Vercel, Mem0, Letta & 
E2B Sandbox 
(Hosting, Memori 
Persisten & Eksekusi 
Kode Aman) 
Vercel: 
https://vercel.com 
Mem0: 
https://github.com/mem
0ai/mem0 Letta / 
MemGPT: 
https://github.com/letta-
ai/letta-node E2B Code 
Sandbox: 
https://e2b.dev 
100% Tanpa Kartu 
(Login via GitHub). 
Mem0 (mem0 init 
--agent) dan Letta 
membentuk memori 
lintas sesi ganda (cloud 
dan lokal), Vercel 
menyajikan antarmuka 
web atau router ringan, 
dan E2B memberikan 
kredit kotak pasir gratis 
untuk mengeksekusi 
kode yang dihasilkan 
agen secara terisolasi. 
2C. Identitas Pengembang, Bot Omnichannel & Gerbang Pembayaran Otomatis 
(100% Tanpa Kartu Visa) 
Sub-kategori 2C mengintegrasikan komponen operasional dari Kategori 1 pada Link_daftar_vps 
server.txt yang memungkinkan agen beroperasi sebagai entitas bisnis otonom (Autonomous 
Treasury) yang menerima pembayaran lokal (QRIS) maupun global (Crypto USDT) tanpa 
memerlukan kartu perbankan Visa atau Mastercard. Dengan menyiapkan tiga token bot 
Telegram terpisah dan tiga gerbang pembayaran QRIS lokal yang didampingi kasir kripto 



<!-- [ID:16_INFRA_DEVOPS_S082] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 272

No 
Nama Layanan & 
Fungsi Operasional 
Tautan Resmi (Dari 
Sumber Induk 3) 
Mekanisme Integrasi & 
Failover Otomatis 
Crypto USDT Global) 
dengan mengetik /start 
\rightarrow Crypto Pay 
\rightarrow Create App 
untuk mengambil 
CRYPTOBOT_API_TO
KEN. Pendapatan 
USDT yang terkumpul 
dapat langsung dipakai 
untuk mengisi ulang 
saldo komputasi GPU 
di Novita AI, RunPod, 
Vast.ai, dan PiAPI 
tanpa pernah 
menyentuh rekening 
bank tradisional. 
Kelompok 3: Wajib Kartu Visa/Mastercard ATAU Wajib Dompet Kripto 
(DePIN, Airdrop & Wholesale GPU) 
Kelompok 3 menyatukan seluruh layanan dari Kelompok 3 (LINK SUMBER.pdf) dan Kategori 
2 (Link_daftar_vps server.txt), serta memperluas jaringan komputasi terdesentralisasi (DePIN) 
dengan ekosistem Akash Network (akash-network/node) dari hasil riset terbaru. Sesuai 
protokol keamanan finansial FIN-SEC-01, apabila arsitek sistem memutuskan untuk 
mengaktifkan layanan pada sub-kategori 3A, wajib diterbitkan satu Kartu Debit Visa Virtual 
terisolasi (misalnya melalui kantong terpisah bernama "Vault API bikinAI" pada aplikasi bank 
digital seperti Bank Jago atau Jenius dengan saldo terukur ~Rp 20.000 untuk verifikasi) dan 
dilarang keras menautkan kartu dari rekening tabungan utama. 
3A. Penyedia Cloud, VPS Gratis Selamanya & API Grosir yang Membutuhkan 
Kartu Visa / Mastercard (atau Crypto USDT saat Top-Up) 
Pada sub-kategori ini, sebagian besar platform API grosir (Fal.ai, Novita AI, RunPod, Vast.ai, 
Replicate, PiAPI, WaveSpeed AI) mengizinkan pembuatan akun gratis saat ini juga 
menggunakan login Google atau GitHub untuk mengambil kunci API dan menikmati bonus 
kredit pendaftaran awal (Sign-up Free Credits senilai $0,50 hingga $5+), sementara kartu Visa 
atau pembayaran Crypto USDT baru dibutuhkan ketika mengaktifkan fitur Auto-Topup dari 
pendapatan pelanggan. 
No 
Nama Layanan Cloud / 
API Grosir 
Tautan Resmi 
(Gabungan Sumber 1 & 
Sumber 3) 
Status Kartu Visa vs 
Crypto USDT & Peran 
dalam Sistem 
3A.1 
Oracle Cloud Always 
Free Tier (VPS ARM 
24 Jam Gratis 
Selamanya) 
Pendaftaran: 
https://www.oracle.com/
cloud/free/ 
Wajib Verifikasi Kartu 
Visa/Mastercard 
(saldo minimal ~Rp 
20.000 untuk 
pengecekan otorisasi 
yang langsung 



<!-- [ID:16_INFRA_DEVOPS_S083] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 273

No 
Nama Layanan Cloud / 
API Grosir 
Tautan Resmi 
(Gabungan Sumber 1 & 
Sumber 3) 
Status Kartu Visa vs 
Crypto USDT & Peran 
dalam Sistem 
dikembalikan otomatis). 
Memberikan 4 ARM 
Ampere OCPUs + 24 
GB RAM gratis 
selamanya untuk 
menjalankan 
OmniRoute, 9Router, 
New-API Horizon, dan 
jhao104/proxy_pool 
24/7. 
3A.2 
Modal Serverless 
GPU, GCP, AWS & 
Fly.io 
Modal (
30/𝐵𝑢𝑙𝑎𝑛𝐾𝑟𝑒𝑑𝑖𝑡𝐺𝑃𝑈): ℎ
300 Trial): 
https://cloud.google.co
m/free AWS Free Tier: 
https://aws.amazon.co
m/free/ Fly.io (Docker 
Hosting): https://fly.io 
Wajib Kartu 
Visa/Mastercard untuk 
membuka kuota. Modal 
sangat bernilai strategis 
karena memberikan 
kredit komputasi GPU 
serverless sebesar $30 
setiap bulan secara 
berulang setelah kartu 
diverifikasi, 
menjadikannya fallback 
utama untuk merender 
video Wan2.2 atau 
HunyuanVideo-1.5 di 
cloud dengan biaya Rp 
0. 
3A.3 
Novita AI, RunPod, 
Vast.ai & PiAPI (Grosir 
GPU & Media — 
Mendukung Crypto 
USDT Tanpa Kartu 
Visa) 
Novita AI: 
https://novita.ai/ 
RunPod (FlashBoot 
24GB VRAM): 
https://www.runpod.io/ 
Vast.ai (Sewa RTX 
3090/4090 Termurah): 
https://cloud.vast.ai/ 
PiAPI (Musik Suno v6 
Studio & Udio): 
https://piapi.ai/ 
Daftar Akun Gratis via 
Google/GitHub 
sekarang. Keunggulan 
krusial keempat 
penyedia ini adalah 
dukungan pengisian 
saldo menggunakan 
Crypto USDT 
(misalnya dari 
pendapatan 
@CryptoBot pada 2C.4 
via jaringan TRON, 
Solana, atau Coinbase 
Commerce) sehingga 
dapat dioperasikan 
sepenuhnya tanpa 
kartu Visa. 
3A.4 
Fal.ai, WaveSpeed AI, Fal.ai (Kling 3.0, Veo, 
Daftar Akun Gratis via 



<!-- [ID:16_INFRA_DEVOPS_S084] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 274

No 
Nama Layanan Cloud / 
API Grosir 
Tautan Resmi 
(Gabungan Sumber 1 & 
Sumber 3) 
Status Kartu Visa vs 
Crypto USDT & Peran 
dalam Sistem 
Replicate & OpenAI 
Moderation (API 
Media & Moderasi 
Grosir) 
Wan 2.2, Seedance, 
Flux): 
https://fal.ai/dashboard/
keys WaveSpeed AI 
(Seedance 1.5 Pro & 
Wan 2.2): 
https://wavespeed.ai/ 
Replicate (4K 
Real-ESRGAN & 
Motion Control): 
https://replicate.com/ac
count/api-tokens 
OpenAI Platform: 
https://platform.openai.
com/api-keys 
GitHub/Google 
sekarang untuk 
mengambil kunci API. 
Kartu Visa baru 
diperlukan saat 
mengaktifkan 
Auto-Topup komersial. 
Pada OpenAI, titik akhir 
omni-moderation-latest 
bersifat gratis untuk 
memfilter teks 
multibahasa, dan 
organisasi yang 
memenuhi syarat 
berbagi trafik dapat 
memperoleh hingga 1 
juta token/hari pada 
model GPT-5.x serta 10 
juta token/hari pada 
model kecil. 
3B. Jaringan DePIN, Mining AI & Marketplace Komputasi Terdesentralisasi (Wajib 
Dompet Kripto & Spesifikasi GPU) 
Proyek di dalam sub-kategori 3B tidak memerlukan kartu perbankan maupun akun Gmail, 
melainkan menggunakan autentikasi pasangan kunci kriptografi (dompet Bittensor 
coldkey/hotkey, dompet Solana, atau dompet Cosmos/Akash). Selain Bittensor, Nosana, dan 
IO.net dari berkas sumber, riset menambahkan Akash Network (akash-network/node, yang 
baru merilis versi v2.1.2 dan v3.0.0-a0 pada tahun 2026) sebagai pasar komputasi awan 
peer-to-peer yang dilengkapi keterampilan agen khusus (akash-skill) untuk men-deploy 
kontainer Docker secara otomatis. 
No 
Nama Protokol DePIN Tautan Repositori & 
Dokumentasi (Eksisting 
& Ekspansi Riset) 
Mekanisme Insentif, 
Rumus Skor & Peran 
dalam Ekosistem 
3B.1 
Bittensor Ecosystem 
(Subtensor Monorepo, 
Subnet 27 Compute & 
Score Predict) 
Monorepo & SDK: 
https://github.com/Rao
Foundation/bittensor 
(atau 
opentensor/bittensor) 
Subnet Template: 
https://github.com/open
tensor/bittensor-subnet-
template Testnet Guide: 
https://github.com/open
tensor/bittensor-subnet-
Menggunakan dompet 
lokal (btcli wallet 
new_coldkey & 
new_hotkey). 
Menyediakan GPU 
menganggur (minimal 
4–8 core CPU, 16 GB 
RAM, 24 GB VRAM 
A100, SSD 100 GB 
5.000 IOPS) ke Subnet 
27 atau menjalankan 



<!-- [ID:16_INFRA_DEVOPS_S085] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 275

No 
Nama Protokol DePIN Tautan Repositori & 
Dokumentasi (Eksisting 
& Ekspansi Riset) 
Mekanisme Insentif, 
Rumus Skor & Peran 
dalam Ekosistem 
template/blob/main/doc
s/running_on_testnet.m
d Min Compute Spec: 
https://github.com/open
tensor/bittensor-subnet-
template/blob/main/min
_compute.yml Subnet 
27 Compute: 
https://github.com/com
mune-ai/compute-ni 
Score Predict Subnet: 
https://github.com/scor
e-technologies/score-pr
edict/blob/main/READ
ME.md 
model Random Forest 
di score-predict 
menghasilkan imbalan 
token TAO melalui 
Yuma Consensus. 
3B.2 
Nosana & IO.net 
(Jaringan Klaster GPU 
Terdesentralisasi 
Berbasis Solana) 
Nosana CLI: 
https://github.com/nosa
na-ci/nosana-cli 
Nosana LLM 
Benchmarking: 
https://github.com/nosa
na-ci/nosana-llm-bench
marking Nosana Portal: 
https://github.com/nosa
na-ci/nosana.io IO.net 
Launch Binaries: 
https://github.com/ionet
-official/io_launch_binar
ies/issues/48 
Wajib dompet kripto 
Solana (SOL / NOS / 
IO). Memungkinkan 
monetisasi GPU 
menganggur di luar jam 
kerja agen untuk 
menerima distribusi 
insentif atau airdrop, 
sekaligus menyediakan 
komputasi inferensi 
berbiaya jauh di bawah 
cloud tradisional. 
3B.3 
Akash Network 
(Alternatif Superior 
Baru — Decentralized 
Serverless Cloud & 
Agent Deployment) 
Node Source Code: 
https://github.com/akas
h-network/node & 
Releases (v2.1.2 / 
v3.0.0-a0): 
https://github.com/ovrcl
k/akash/releases Install 
Script: 
https://raw.githubuserco
ntent.com/akash-netwo
rk/node/main/install.sh 
Provider Daemon: 
https://github.com/akas
h-network/provider 
Web Console (Deploy 
Dibangun di atas 
Cosmos SDK dan 
CometBFT (berlisensi 
Apache-2.0) 
menggunakan token 
AKT. Berfungsi ganda: 
pemilik perangkat keras 
dapat menjalankan 
daemon provider untuk 
menyewakan kapasitas 
komputasi, sementara 
agen koding AI (seperti 
Claude Code atau 
OpenClaw) dapat 
menggunakan 



<!-- [ID:16_INFRA_DEVOPS_S086] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_19, SPAN_21 -->
## Halaman 277

\text{Route}(x) = \begin{cases} \mathcal{M}_{\text{strong}} & \text{jika } P(\text{strong} \succ 
\text{weak} \mid x) \ge \tau \\ \mathcal{M}_{\text{weak}} & \text{jika } P(\text{strong} \succ 
\text{weak} \mid x) < \tau \end{cases} 
Dengan menetapkan kalibrasi ambang batas standar \tau = 0,11593 pada perute Matrix 
Factorization (mf), sistem secara deterministik mengalokasikan tepat 50% kueri tersulit ke rantai 
API cloud dan 50% sisanya ke mesin inferensi lokal, memangkas konsumsi kuota token 
eksternal hingga 40%–70% tanpa penurunan kualitas yang terukur. 
Apabila perangkat keras lokal memiliki siklus GPU yang menganggur saat beban kueri rendah, 
arsitektur ini dapat mengalihkan kapasitas GPU ke protokol Bittensor Subnet 27 
(commune-ai/compute-ni), di mana perolehan insentif token TAO ditentukan secara matematis 
oleh skor total node penambang (S_{\text{total}}): 
S_{\text{GPU}} = \text{Perf}_{\text{base}} \times N_{\text{GPU}} \times 
\left(\frac{100}{\text{Max\_Scenario}}\right), \quad S_{\text{total}} = S_{\text{GPU}} + 
B_{\text{alloc}} 
Dalam persamaan tersebut, \text{Perf}_{\text{base}} merepresentasikan kinerja dasar unit GPU, 
N_{\text{GPU}} adalah jumlah kartu grafis, \text{Max\_Scenario} merupakan batas skenario 
tertinggi jaringan (contohnya 3,90 \times 8 = 31,2 yang menghasilkan faktor pengali \approx 
3,2051 untuk batas skor GPU 100), dan B_{\text{alloc}} adalah bonus alokasi sebesar 100 poin 
ketika mesin sedang dialokasikan secara aktif kepada validator melalui register.py (sehingga 
skor maksimum mencapai 200 poin). Pada subnet prediksi olahraga 
score-technologies/score-predict, imbalan penambang yang mengeksekusi pengklasifikasi 
Random Forest dikalikan lagi dengan streak multiplier (hingga 1,8\times untuk \ge 20 prediksi 
benar berturut-turut) dan 7-day win rate multiplier (1,3\times untuk akurasi \ge 
70\[span_19](start_span)[span_19](end_span)[span_21](start_span)[span_21](end_span)%, 
atau penalti 0,9\times jika di bawah 40\%). 
Ortogonalisasi Ruang Residual (Abliteration) dan Perisai Serialisasi 
Bobot 
Untuk melayani kueri penelitian akademik, pengujian penetrasi siber (red-teaming), dan 
instruksi tanpa filter tanpa memicu penolakan heuristik ("I'm sorry, I cannot fulfill this request"), 
arsitektur ini mengadopsi metodologi Abliteration yang berlandaskan pembuktian Arditi et al. 
(andyrdt/refusal_direction) bahwa perilaku penolakan pada transformator dimediasi oleh satu 
arah vektor tunggal di dalam aliran residual (residual stream). Dengan mengevaluasi himpunan 
prompt sensitif \mathcal{D}_{\text{harmful}} (berukuran N) dan himpunan prompt netral 
\mathcal{D}_{\text{harmless}} (berukuran M) pada posisi token instruksi terakhir di lapisan 
kandidat l, vektor perbedaan rata-rata \mathbf{v}^{(l)} dan vektor satuan arah penolakan 
\hat{\mathbf{r}} diekstraksi sebagai berikut: 
\mathbf{v}^{(l)} = \frac{1}{N} \sum_{i=1}^{N} \mathbf{a}_{\text{harmful}, i}^{(l)} - \frac{1}{M} 
\sum_{j=1}^{M} \mathbf{a}_{\text{harmless}, j}^{(l)}, \quad \hat{\mathbf{r}} = 
\frac{\mathbf{v}^{(l)}}{\Vert\mathbf{v}^{(l)}\Vert_2} 
Agar penghapusan sensor tidak mengikis kemampuan penalaran umum atau memicu nilai NaN 
dan Inf pada model sensitif (sebagaimana sering terjadi pada Simple Abliteration generasi 
pertama), implementasi produksi pada jim-plus/llm-abliteration dan Orion-zhen/abliteration 
menerapkan Biprojection (Gram-Schmidt orthogonalization) terhadap arah rata-rata aktivasi 
tidak berbahaya yang telah dinormalisasi (\hat{\mathbf{d}}_{\text{harmless}}) sebelum 
memodifikasi matriks bobot \mathbf{W} \in \mathbb{R}^{d_{\text{out}} \times d_{\text{in}}}: 



<!-- [ID:16_INFRA_DEVOPS_S087] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_72 -->
## Halaman 290

Komponen Sistem Jalur Primer (Tier 
1) 
Jalur Sekunder 
(Tier 2 — 
Auto-Rollover) 
Jalur Tersier / 
Lokal (Tier 3 — 
Zero-Dependency 
Fallback) 
Kondisi Pemicu 
Pengalihan 
(Trigger Condition) 
Generasi Video & 
Animasi Avatar 
Lokal: 
Wan2.2-TI2V-5B / 
HunyuanVideo-1.5 
(4–12 langkah + 
TeaCache + 
SageAttention) 
Lokal VRAM 
Rendah (8–10 
GB): LTX-VideoQ8 
/ 
HunyuanVideo-Av
atar (via Wan2GP) 
Cloud 
Gratis/Grosir: 
Modal ($30/bln 
gratis) \rightarrow 
Pollinations AI 
(Mode 1) 
\rightarrow Fal.ai / 
WaveSpeed / 
Novita 
Penggunaan 
VRAM melampaui 
kapasitas fisik 
kartu grafis lokal 
atau antrean 
render > 180 detik. 
Database 
Transaksional & 
Memori Agen 
Turso Cloud (5 GB 
libSQL Concurrent 
Writes) + Mem0 
(@mem0/cli) 
Supabase (500 
MB PostgreSQL + 
pgvector) + Letta 
(@letta-ai/letta-clie
nt) 
Neon Serverless 
Postgres (500 MB) 
\rightarrow SQLite 
/ Valkey Lokal 
pada disk VPS 
Batas koneksi 
konkuren tercapai, 
waktu respons 
kueri > 200ms, 
atau pemeliharaan 
jaringan cloud. 
Object Storage 
Media & Bobot 
Cloudflare R2 / 
Supabase Storage 
(1 GB Gratis) 
Backblaze B2 (10 
GB Pertama 100% 
Gratis Tanpa Kartu 
Visa) 
Penyimpanan 
Sistem Berkas 
Lokal Terkompresi 
(mksglu/context-m
ode) 
Kuota 
penyimpanan 1 
GB penuh atau 
kegagalan unggah 
objek HTTP 5xx. 
Kasir 
Pembayaran 
Otomatis 
(Treasury) 
Paka[span_72](sta
rt_span)[span_72](
end_span)sir 
(QRIS Otomatis 
Indonesia Tanpa 
Kartu Visa) 
Tripay \rightarrow 
Duitku (Alternatif 
QRIS Lokal) 
Telegram 
@CryptoBot (Kasir 
Crypto Pay USDT 
Global 1-Klik) 
Webhook 
pembayaran QRIS 
primer tidak 
merespons dalam 
3.000ms atau 
transaksi berasal 
dari pembeli 
internasional. 
Kesimpulan dan Rekomendasi Arsitektural 
Sintesis komprehensif terhadap seluruh 199 tautan dari ketiga dokumen sumber induk beserta 
puluhan repositori dan titik akhir alternatif dari riset terbaru membuktikan bahwa ketahanan 
sistem AI otonom berbiaya nol hanya dapat dicapai melalui abstraksi perutean berlapis yang 
memberikan imunitas terhadap kepunahan titik akhir (endpoint extinction immunity). Perubahan 
drastis kebijakan penyedia cloud sepanjang paruh kedua tahun 2026—seperti berhentinya 
layanan GitHub Models pada akhir Juli, peralihan Cerebras ke sistem uji coba berbayar untuk 
akun baru pada pertengahan Juli, dan penghapusan model Llama lama dari paket gratis Groq 
pada bulan Agustus—menegaskan bahwa setiap titik akhir eksternal bersifat sementara. 
Dengan menggabungkan penyedia kuota gratis permanen berkapasitas masif seperti Mistral 
Experiment Tier (~1 miliar token/bulan), Google AI Studio (konteks 1 juta token pada Gemini 
3.5 Flash), NVIDIA NIM (91 model pada 40 RPM), dan Cloudflare Workers AI (10.000 
Neurons/hari) di belakang agregator lokal (OmniRoute, 9Router, New-API Horizon, dan Portkey 
Gateway), agen AI dapat terus beroperasi tanpa gangguan meskipun satu atau beberapa 



<!-- [ID:16_INFRA_DEVOPS_S088] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 321

No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Keunggulan 
Arsitektural & 
Peran Failover 
e2b-dev/awesome
-ai-agents 
Learning Resource 
(DevKay): 
https://github.com/
DharminJoshi/Awe
some-Agentic-AI-L
earning-Resource-
By-DevKay 
Free-for-Dev 
(Induk 1.200+ 
Layanan): 
https://github.com/
ripienaar/free-for-d
ev Free-for-Dev 
(Fork Mikro): 
https://github.com/j
ixserver/free-for-de
v-1 FreeStack 
Search: 
https://github.com/
n8watkins/freestac
k Public APIs: 
https://github.com/
public-apis/public-
apis Kurator API: 
https://github.com/
chukwulasu Topik 
AI Agents: 
https://github.com/t
opics/ai-agents 
Open-R1 Blog: 
https://huggingface
.co/blog/open-r1 
Kelompok 2: Bisa Daftar Sekarang Juga via GitHub / Gmail / Telegram 
(100% Tanpa Kartu Visa/Mastercard) 
Kelompok 2 mengonsolidasikan seluruh penyedia kuota API gratis ("bansos" token), 
infrastruktur basis data, serverless worker, serta gerbang pembayaran lokal dan bot 
omnichannel dari Kelompok 2 (LINK SUMBER.pdf) dan Kategori 1 (Link_daftar_vps 
server.txt). Selain menggabungkan seluruh tautan tersebut, bagian ini menyertakan Audit 
Status Kuota Kuartal IV 2026 berdasarkan bukti riset terkini serta menambahkan penyedia 
alternatif tanpa kartu kredit—seperti Cloudflare Workers AI (10.000 Neurons/hari), Fireworks 



<!-- [ID:16_INFRA_DEVOPS_S089] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 324

No 
Nama Penyedia 
Layanan 
Tautan 
Pendaftaran & 
Konsol Kunci 
(Eksisting & 
Gabungan) 
Alternatif / 
Endpoint Spesifik 
& Status Audit 
2026 
Kapasitas Kuota 
Gratis, Batas Laju 
& Peran Rolling 
prototipe dan riset. 
2A.6 
Cloudflare 
Workers AI 
(Alternatif Baru 
Inferensi 
Serverless) 
Pendaftaran: 
https://dash.cloudfl
are.com/sign-up 
Konsol: 
https://dash.cloudfl
are.com 
Catatan 2026: 
Mencakup ~80 
model terbuka; 
model berat 
seperti Kimi 
K2.6/K2.7 Code 
dan GLM-5.2 kini 
memerlukan paket 
berbayar, 
sehingga kuota 
gratis difokuskan 
pada model 
ukuran 
kecil-menengah. 
100% Tanpa 
Kartu. 
Memberikan kuota 
permanen 10.000 
Neurons/hari 
(direset setiap 
pukul 00:00 UTC) 
di samping 
100.000 
permintaan/hari 
untuk Cloudflare 
Workers. 
2A.7 
SiliconFlow, 
Fireworks AI & 
Alibaba Model 
Studio (Kredit 
Sambutan Tanpa 
Kartu) 
SiliconFlow 
(Sumber 3): 
https://cloud.silicon
flow.com/ 
Fireworks AI: 
https://fireworks.ai 
Alibaba Cloud 
Model Studio 
(Wilayah 
Singapura, aktivasi 
mulai Sept 2026). 
SiliconFlow 
menyediakan 
akses ke 
DeepSeek-V4.1-Fl
ash & Qwen. 
Fireworks AI 
memberikan $1 
kredit gratis 
tanpa kartu pada 
laju 10 RPM, 
sementara Alibaba 
Cloud Model 
Studio 
memberikan 
~1.000.000 token 
gratis per model 
(berlaku 90 hari) 
sebelum 
mewajibkan detail 
tagihan. 
2A.8 
AWS Builder ID 
(Jembatan Kiro AI 
/ Claude Gratis) 
Profil: 
https://profile.aws.
amazon.com/ 
Terintegrasi 
langsung dengan 
decolua/9router 
dan 
justlovemaki/AIClie
nt2API. 
100% Tanpa 
Kartu. Merupakan 
profil identitas 
pengembang 
mandiri (bukan 
AWS Console 
reguler) yang 



<!-- [ID:16_INFRA_DEVOPS_S090] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 326

No 
Nama Penyedia 
Layanan 
Tautan 
Pendaftaran & 
Konsol Kunci 
(Eksisting & 
Gabungan) 
Alternatif / 
Endpoint Spesifik 
& Status Audit 
2026 
Kapasitas Kuota 
Gratis, Batas Laju 
& Peran Rolling 
negative 
embeddings 
secara terprogram, 
sedangkan Spider 
Cloud memberikan 
kunci API gratis 
tanpa kartu untuk 
smart web 
scraping. 
2A.12 
Cerebras Cloud, 
GitHub Models & 
SambaNova 
(Status Transisi / 
Legacy) 
Cerebras: 
https://cloud.cereb
ras.ai 
(https://api.cerebra
s.ai/v1) GitHub 
Models: 
https://github.com/
marketplace/model
s SambaNova: 
https://cloud.samb
anova.ai 
Peringatan 
Otomasi Kode: 
Akun lama 
Cerebras masih 
menikmati 1M 
token/hari (2.600+ 
tok/s pada WSE-3 
untuk Llama 4 
Scout, Qwen3 
32B, 
gpt-oss-120b), 
namun per 16 Juli 
2026 akun baru 
dialihkan ke uji 
coba $5 yang 
wajib kartu. GitHub 
Models pensiun 
pada 30 Juli 2026, 
dan SambaNova 
menghentikan 
kredit akun baru 
pada Agustus 
2026. 
Kode agen wajib 
membungkus 
ketiga penyedia ini 
di dalam blok 
try-except dengan 
fallback instan ke 
Mistral (2A.2), 
Google AI Studio 
(2A.1), dan Groq 
(2A.3) apabila 
menerima kode 
status HTTP 401, 
402, 403, atau 
404. 
2B. Infrastruktur Hosting, Proksi Tepi, GPU Notebook, Memori & Database Gratis 
(Tanpa Kartu Kredit) 
Seluruh komponen di bawah ini berasal dari sub-kategori 2B (LINK SUMBER.pdf) serta layanan 
penyimpanan dan infrastruktur dari Kategori 1 dan Kategori 2 (Link_daftar_vps server.txt — 
khususnya Backblaze B2 yang terbukti memberikan 10 GB pertama tanpa kartu Visa). Dengan 
menggabungkan Turso, Supabase, dan Neon, agen memiliki tiga mesin basis data SQL dan 
vektor terpisah yang saling mem-backup secara otomatis. 



<!-- [ID:16_INFRA_DEVOPS_S091] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 328

No 
Nama Layanan 
Infrastruktur 
Tautan Pendaftaran & 
Repositori (Eksisting & 
Gabungan) 
Peran Utama & Rantai 
Rolling Failover 
Infrastruktur 
Supabase Storage dan 
Cloudflare R2. 
2B.4 
Google Colaboratory 
& Kaggle Notebooks 
(Komputasi GPU Cloud 
Gratis) 
Google Colab (GPU 
T4): 
https://colab.research.g
oogle.com Kaggle (30 
Jam/Minggu Dual-T4 / 
P100): 
https://www.kaggle.com 
100% Tanpa Kartu. 
Digunakan secara 
bergantian (rolling) 
untuk mengeksekusi 
proses abliteration 
bobot model 
(jim-plus/llm-abliteration 
atau AIAnytime/ablate) 
maupun merender 
suara dan video ketika 
mesin lokal tidak 
memiliki GPU 
memadai. 
2B.5 
Vercel, Mem0, Letta & 
E2B Sandbox 
(Hosting, Memori 
Persisten & Eksekusi 
Kode Aman) 
Vercel: 
https://vercel.com 
Mem0: 
https://github.com/mem
0ai/mem0 Letta / 
MemGPT: 
https://github.com/letta-
ai/letta-node E2B Code 
Sandbox: 
https://e2b.dev 
100% Tanpa Kartu 
(Login via GitHub). 
Mem0 (mem0 init 
--agent) dan Letta 
membentuk memori 
lintas sesi ganda (cloud 
dan lokal), Vercel 
menyajikan antarmuka 
web atau router ringan, 
dan E2B memberikan 
kredit kotak pasir gratis 
untuk mengeksekusi 
kode yang dihasilkan 
agen secara terisolasi. 
2C. Identitas Pengembang, Bot Omnichannel & Gerbang Pembayaran Otomatis 
(100% Tanpa Kartu Visa) 
Sub-kategori 2C mengintegrasikan komponen operasional dari Kategori 1 pada Link_daftar_vps 
server.txt yang memungkinkan agen beroperasi sebagai entitas bisnis otonom (Autonomous 
Treasury) yang menerima pembayaran lokal (QRIS) maupun global (Crypto USDT) tanpa 
memerlukan kartu perbankan Visa atau Mastercard. Dengan menyiapkan tiga token bot 
Telegram terpisah dan tiga gerbang pembayaran QRIS lokal yang didampingi kasir kripto 
otomatis, sistem transaksi tetap berjalan meskipun salah satu penyedia gerbang pembayaran 
mengalami gangguan pemeliharaan. 
No 
Nama Layanan & 
Fungsi Operasional 
Tautan Resmi (Dari 
Sumber Induk 3) 
Mekanisme Integrasi & 
Failover Otomatis 
2C.1 
GitHub Signup, 
Telegram @BotFather 
& @userinfobot 
GitHub Account: 
https://github.com/signu
p BotFather: 
Akun GitHub digunakan 
sebagai kunci OAuth 
1-klik di seluruh 



<!-- [ID:16_INFRA_DEVOPS_S092] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 330

No 
Nama Layanan & 
Fungsi Operasional 
Tautan Resmi (Dari 
Sumber Induk 3) 
Mekanisme Integrasi & 
Failover Otomatis 
KEN. Pendapatan 
USDT yang terkumpul 
dapat langsung dipakai 
untuk mengisi ulang 
saldo komputasi GPU 
di Novita AI, RunPod, 
Vast.ai, dan PiAPI 
tanpa pernah 
menyentuh rekening 
bank tradisional. 
Kelompok 3: Wajib Kartu Visa/Mastercard ATAU Wajib Dompet Kripto 
(DePIN, Airdrop & Wholesale GPU) 
Kelompok 3 menyatukan seluruh layanan dari Kelompok 3 (LINK SUMBER.pdf) dan Kategori 
2 (Link_daftar_vps server.txt), serta memperluas jaringan komputasi terdesentralisasi (DePIN) 
dengan ekosistem Akash Network (akash-network/node) dari hasil riset terbaru. Sesuai 
protokol keamanan finansial FIN-SEC-01, apabila arsitek sistem memutuskan untuk 
mengaktifkan layanan pada sub-kategori 3A, wajib diterbitkan satu Kartu Debit Visa Virtual 
terisolasi (misalnya melalui kantong terpisah bernama "Vault API bikinAI" pada aplikasi bank 
digital seperti Bank Jago atau Jenius dengan saldo terukur ~Rp 20.000 untuk verifikasi) dan 
dilarang keras menautkan kartu dari rekening tabungan utama. 
3A. Penyedia Cloud, VPS Gratis Selamanya & API Grosir yang Membutuhkan 
Kartu Visa / Mastercard (atau Crypto USDT saat Top-Up) 
Pada sub-kategori ini, sebagian besar platform API grosir (Fal.ai, Novita AI, RunPod, Vast.ai, 
Replicate, PiAPI, WaveSpeed AI) mengizinkan pembuatan akun gratis saat ini juga 
menggunakan login Google atau GitHub untuk mengambil kunci API dan menikmati bonus 
kredit pendaftaran awal (Sign-up Free Credits senilai $0,50 hingga $5+), sementara kartu Visa 
atau pembayaran Crypto USDT baru dibutuhkan ketika mengaktifkan fitur Auto-Topup dari 
pendapatan pelanggan. 
No 
Nama Layanan Cloud / 
API Grosir 
Tautan Resmi 
(Gabungan Sumber 1 & 
Sumber 3) 
Status Kartu Visa vs 
Crypto USDT & Peran 
dalam Sistem 
3A.1 
Oracle Cloud Always 
Free Tier (VPS ARM 
24 Jam Gratis 
Selamanya) 
Pendaftaran: 
https://www.oracle.com/
cloud/free/ 
Wajib Verifikasi Kartu 
Visa/Mastercard 
(saldo minimal ~Rp 
20.000 untuk 
pengecekan otorisasi 
yang langsung 
dikembalikan otomatis). 
Memberikan 4 ARM 
Ampere OCPUs + 24 
GB RAM gratis 
selamanya untuk 



<!-- [ID:16_INFRA_DEVOPS_S093] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 331

No 
Nama Layanan Cloud / 
API Grosir 
Tautan Resmi 
(Gabungan Sumber 1 & 
Sumber 3) 
Status Kartu Visa vs 
Crypto USDT & Peran 
dalam Sistem 
menjalankan 
OmniRoute, 9Router, 
New-API Horizon, dan 
jhao104/proxy_pool 
24/7. 
3A.2 
Modal Serverless 
GPU, GCP, AWS & 
Fly.io 
Modal (
30/𝐵𝑢𝑙𝑎𝑛𝐾𝑟𝑒𝑑𝑖𝑡𝐺𝑃𝑈): ℎ
300 Trial): 
https://cloud.google.co
m/free AWS Free Tier: 
https://aws.amazon.co
m/free/ Fly.io (Docker 
Hosting): https://fly.io 
Wajib Kartu 
Visa/Mastercard untuk 
membuka kuota. Modal 
sangat bernilai strategis 
karena memberikan 
kredit komputasi GPU 
serverless sebesar $30 
setiap bulan secara 
berulang setelah kartu 
diverifikasi, 
menjadikannya fallback 
utama untuk merender 
video Wan2.2 atau 
HunyuanVideo-1.5 di 
cloud dengan biaya Rp 
0. 
3A.3 
Novita AI, RunPod, 
Vast.ai & PiAPI (Grosir 
GPU & Media — 
Mendukung Crypto 
USDT Tanpa Kartu 
Visa) 
Novita AI: 
https://novita.ai/ 
RunPod (FlashBoot 
24GB VRAM): 
https://www.runpod.io/ 
Vast.ai (Sewa RTX 
3090/4090 Termurah): 
https://cloud.vast.ai/ 
PiAPI (Musik Suno v6 
Studio & Udio): 
https://piapi.ai/ 
Daftar Akun Gratis via 
Google/GitHub 
sekarang. Keunggulan 
krusial keempat 
penyedia ini adalah 
dukungan pengisian 
saldo menggunakan 
Crypto USDT 
(misalnya dari 
pendapatan 
@CryptoBot pada 2C.4 
via jaringan TRON, 
Solana, atau Coinbase 
Commerce) sehingga 
dapat dioperasikan 
sepenuhnya tanpa 
kartu Visa. 
3A.4 
Fal.ai, WaveSpeed AI, 
Replicate & OpenAI 
Moderation (API 
Media & Moderasi 
Grosir) 
Fal.ai (Kling 3.0, Veo, 
Wan 2.2, Seedance, 
Flux): 
https://fal.ai/dashboard/
keys WaveSpeed AI 
(Seedance 1.5 Pro & 
Daftar Akun Gratis via 
GitHub/Google 
sekarang untuk 
mengambil kunci API. 
Kartu Visa baru 
diperlukan saat 



<!-- [ID:16_INFRA_DEVOPS_S094] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 332

No 
Nama Layanan Cloud / 
API Grosir 
Tautan Resmi 
(Gabungan Sumber 1 & 
Sumber 3) 
Status Kartu Visa vs 
Crypto USDT & Peran 
dalam Sistem 
Wan 2.2): 
https://wavespeed.ai/ 
Replicate (4K 
Real-ESRGAN & 
Motion Control): 
https://replicate.com/ac
count/api-tokens 
OpenAI Platform: 
https://platform.openai.
com/api-keys 
mengaktifkan 
Auto-Topup komersial. 
Pada OpenAI, titik akhir 
omni-moderation-latest 
bersifat gratis untuk 
memfilter teks 
multibahasa, dan 
organisasi yang 
memenuhi syarat 
berbagi trafik dapat 
memperoleh hingga 1 
juta token/hari pada 
model GPT-5.x serta 10 
juta token/hari pada 
model kecil. 
3B. Jaringan DePIN, Mining AI & Marketplace Komputasi Terdesentralisasi (Wajib 
Dompet Kripto & Spesifikasi GPU) 
Proyek di dalam sub-kategori 3B tidak memerlukan kartu perbankan maupun akun Gmail, 
melainkan menggunakan autentikasi pasangan kunci kriptografi (dompet Bittensor 
coldkey/hotkey, dompet Solana, atau dompet Cosmos/Akash). Selain Bittensor, Nosana, dan 
IO.net dari berkas sumber, riset menambahkan Akash Network (akash-network/node, yang 
baru merilis versi v2.1.2 dan v3.0.0-a0 pada tahun 2026) sebagai pasar komputasi awan 
peer-to-peer yang dilengkapi keterampilan agen khusus (akash-skill) untuk men-deploy 
kontainer Docker secara otomatis. 
No 
Nama Protokol DePIN Tautan Repositori & 
Dokumentasi (Eksisting 
& Ekspansi Riset) 
Mekanisme Insentif, 
Rumus Skor & Peran 
dalam Ekosistem 
3B.1 
Bittensor Ecosystem 
(Subtensor Monorepo, 
Subnet 27 Compute & 
Score Predict) 
Monorepo & SDK: 
https://github.com/Rao
Foundation/bittensor 
(atau 
opentensor/bittensor) 
Subnet Template: 
https://github.com/open
tensor/bittensor-subnet-
template Testnet Guide: 
https://github.com/open
tensor/bittensor-subnet-
template/blob/main/doc
s/running_on_testnet.m
d Min Compute Spec: 
https://github.com/open
tensor/bittensor-subnet-
Menggunakan dompet 
lokal (btcli wallet 
new_coldkey & 
new_hotkey). 
Menyediakan GPU 
menganggur (minimal 
4–8 core CPU, 16 GB 
RAM, 24 GB VRAM 
A100, SSD 100 GB 
5.000 IOPS) ke Subnet 
27 atau menjalankan 
model Random Forest 
di score-predict 
menghasilkan imbalan 
token TAO melalui 
Yuma Consensus. 



<!-- [ID:16_INFRA_DEVOPS_S095] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 333

No 
Nama Protokol DePIN Tautan Repositori & 
Dokumentasi (Eksisting 
& Ekspansi Riset) 
Mekanisme Insentif, 
Rumus Skor & Peran 
dalam Ekosistem 
template/blob/main/min
_compute.yml Subnet 
27 Compute: 
https://github.com/com
mune-ai/compute-ni 
Score Predict Subnet: 
https://github.com/scor
e-technologies/score-pr
edict/blob/main/READ
ME.md 
3B.2 
Nosana & IO.net 
(Jaringan Klaster GPU 
Terdesentralisasi 
Berbasis Solana) 
Nosana CLI: 
https://github.com/nosa
na-ci/nosana-cli 
Nosana LLM 
Benchmarking: 
https://github.com/nosa
na-ci/nosana-llm-bench
marking Nosana Portal: 
https://github.com/nosa
na-ci/nosana.io IO.net 
Launch Binaries: 
https://github.com/ionet
-official/io_launch_binar
ies/issues/48 
Wajib dompet kripto 
Solana (SOL / NOS / 
IO). Memungkinkan 
monetisasi GPU 
menganggur di luar jam 
kerja agen untuk 
menerima distribusi 
insentif atau airdrop, 
sekaligus menyediakan 
komputasi inferensi 
berbiaya jauh di bawah 
cloud tradisional. 
3B.3 
Akash Network 
(Alternatif Superior 
Baru — Decentralized 
Serverless Cloud & 
Agent Deployment) 
Node Source Code: 
https://github.com/akas
h-network/node & 
Releases (v2.1.2 / 
v3.0.0-a0): 
https://github.com/ovrcl
k/akash/releases Install 
Script: 
https://raw.githubuserco
ntent.com/akash-netwo
rk/node/main/install.sh 
Provider Daemon: 
https://github.com/akas
h-network/provider 
Web Console (Deploy 
Docker): 
https://github.com/akas
h-network/console 
Agent SDL Generator 
Skill: 
Dibangun di atas 
Cosmos SDK dan 
CometBFT (berlisensi 
Apache-2.0) 
menggunakan token 
AKT. Berfungsi ganda: 
pemilik perangkat keras 
dapat menjalankan 
daemon provider untuk 
menyewakan kapasitas 
komputasi, sementara 
agen koding AI (seperti 
Claude Code atau 
OpenClaw) dapat 
menggunakan 
repositori akash-skill 
untuk menghasilkan 
berkas konfigurasi SDL 
secara otomatis dan 
men-deploy kontainer 


