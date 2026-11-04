
<!-- [ID:02_CORE_AI_S145] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER, ESTIMASI -->
## Halaman 22

Dengan menyimpan file_id tersebut di v4.0, pengiriman aset cache atau template populer ke 
pengguna berikutnya berlangsung dalam 0,05 detik dengan pemakaian bandwidth server 0 
byte. 
4.​ [FAKTA] [Bersumber] Invisible Prompt Bridge (Penerjemah Otomatis Bahasa Awam ke SOTA): 
○​ Model video dan gambar SOTA (Wan 2.2, Flux.1, LTX-Video, Illustrious XL) jauh lebih akurat saat 
menerima instruksi bahasa Inggris teknis. Di v4.0, pengguna Indonesia tetap mengetik bahasa 
sehari-hari/daerah, lalu router secara tak terlihat menerjemahkan dan memperkaya prompt 
tersebut di latar belakang sebelum dikirim ke GPU tanpa membingungkan pengguna. 
5.​ [FAKTA] [Bersumber] Strict Privacy Pinning pada Mode Unfiltered: 
○​ Mencegah kueri dari portal bebas (NOCTURNE_UNCENSORED) jatuh ke endpoint GET publik 
ketika server utama sibuk, sehingga privasi pengguna 100% terjaga di jalur terenkripsi. 
 
2. BIZ/MARKET: STRATEGI PASAR & MONETISASI LENGKAP (FORMAT WAJIB 
E1–E7) 
 
●​ E1. Benchmark Kompetitor: 
○​ [FAKTA] [Bersumber] @TeleportAppBot (Telegram Store/App Builder): Harga mulai 990 
₽/bulan (792 ₽/bulan tahunan), komisi afiliasi 50%, dan memakai Automated Sales Manager 
("Maksim") yang otomatis mengirim pesan follow-up saat pengguna melihat tarif tetapi belum 
membayar. 
○​ [FAKTA] [Bersumber] Gateway API (OpenRouter, Fal.ai, Novita AI): Sistem deposit saldo (5–
10) dengan hambatan wajib kartu kredit/Visa atau dompet kripto. 
○​ [ESTIMASI] [Bersumber] Benchmark 4-Zona PPP (isi link sumber.html): Zona 1 Global Tier-1 
$20/bln (100%), Zona 2 Tier-2 $14/bln (70%), Zona 3 Emerging $10/bln (50%), Zona 4 Indonesia 
$5/bln (25% PPP). 
●​ E2. Willingness-to-Pay (WTP) — Indonesia vs. Global & Solusi "Vibecoders" (Case 1): 
○​ [FAKTA] [Bersumber] Pasar Awam & UMKM Indonesia: Menyukai uji coba eceran murah via 
QRIS instan tanpa kartu Visa, sedangkan segmen Sultan/Agensi bersedia membayar mahal 
untuk kepraktisan 1-klik dan jalur cepat. 
○​ [FAKTA] [Bersumber] Cara Meraih Pasar "Vibecoders / Pengguna Mandiri" (Jawaban Case 
1): Para vibecoders memang tahu cara mencari API LLM teks murah/gratis, tetapi mereka 
tetap membutuhkan 3 hal yang bisa Anda jual: 
1.​ Eceran Endpoint API Terpadu (sk-bikinai-... via QRIS): Mereka butuh endpoint tunggal 
yang menggabungkan Combo Grading (anti-rate-limit 429) untuk dipasang di Cursor / 
Cline / Claude Code / proyek mereka dengan pembayaran QRIS ketengan mulai Rp 
10.000 tanpa perlu kartu Visa atau akun kripto. 
2.​ Akses GPU Render Media SOTA via API: Vibecoders tidak bisa merender video Wan 
2.2, Kling 3.0, Veo 3, atau suara Fish Audio S2-Pro di laptop biasa karena butuh GPU 
10GB–80GB VRAM. Mereka akan membeli akses API media dari agregator Anda. 
3.​ Program White-Label / Clone Bot Reseller (50% Revenue Share): Seperti mereka 
ingin berbisnis, sediakan fitur /buat_toko_ai di mana vibecoder cukup menempelkan 
token @BotFather milik mereka ke sistem Anda; mereka yang mencari pembeli, sistem 
Anda yang memproses render & kasir QRIS, lalu laba bersih dibagi otomatis 50:50! 
●​ E3. Rekomendasi Angka Komplit: Eceran, Paket Tier, Subscription, & B2B (Jawaban Case 2): 
○​ [FAKTA] [Bersumber] Pasar Indonesia (Zona 4 PPP — QRIS): 
1.​ Eceran / Ketengan (Pay-As-You-Go): Rp 1.500 (15 Koin — pas untuk 3x Gambar 4K atau 
1x Video AI). 



<!-- [ID:02_CORE_AI_S146] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 27

Komponen Blueprint 
Fondasi Desain v1.0 
(Dipertahankan) 
Celah Skala Produksi 
yang Ditemukan pada 
v1.0 
Spesifikasi Upgrade di 
Blueprint v2.0 
(Production-Grade) 
Agen #7 (V2A 
Foley/MMAudio + 
Kokoro-82M). 
Dapur 9Router & 
Manajemen Kuota 
(localhost:20128/v1) 
98% Quota Surfing, 
kompresi token 
RTK/Caveman (hemat 
20–65%), dan 3-Tier 
Fallback otomatis ke 
OpenRouter :free. 
Kueri berulang dari 
ribuan UMKM tetap 
memicu inferensi LLM 
penuh (membakar 
kuota harian) dan 
Auto-Intent Detection 
memakan ~500 ms per 
pesan. 
Penempatan Valkey + 
RedisVL 
(SemanticCache & 
SemanticRouter) di 
depan 9Router (~120 
MB RAM). Memangkas 
panggilan LLM 
68,8%–86% dengan 
latensi cache hit ~25 
ms (250x lebih cepat). 
Pabrik Render Video 
& Audio 30 Detik 
(stateless_gpu_worke
r.py) 
Memecah video 30 
detik menjadi 6 klip 
\times 5 detik dan 
menjahitnya dengan 
FFmpeg. 
Bobot Wan 14B FP16 
(~28 GB) memicu OOM 
di GPU 24 GB (waktu 
render 542 detik), 
terjadi character drift 
antar-klip, video bisu 
tanpa efek foley, dan 
biaya idle/cold-start 
GPU. 
Standarisasi Wan 2.2 
MoE FP8 Scaled (14 
GB VRAM) + 
SageAttention & 
TeaCache + 
torch.compile (54% 
lebih cepat) di atas 
RunPod Serverless 
FlashBoot (<250 ms 
cold-start) + rantai 
Last-Frame Extraction 
+ PuLID Flux II + audio 
Kokoro-82M & 
MMAudio. 
Konkurensi & Lapisan 
Database 
(config_and_db.py) 
USER_LOCKS = 
defaultdict(asyncio.Loc
k) dan UPDATE ... 
RETURNING pada 
SQLite WAL untuk 
mencegah TOCTOU 
(SEC-02). 
defaultdict tanpa 
eviction memicu 
Memory Exhaustion 
(OOM >2 GB RAM) jika 
diserang jutaan user_id 
acak. Single-writer 
SQLite WAL memicu 
SQLITE_BUSY saat 
ribuan webhook 
menulis serentak. 
Refactoring ke 
Fixed-Size Lock 
Striping (4.096 stripes 
= ~250 KB RAM 
permanen), pemisahan 
4 Read Pool 
(?mode=ro) + 1 
Dedicated 
Single-Writer Queue 
(batch commit 10 ms), 
dan kesiapan migrasi 
ke Turso (libSQL) 
Concurrent Writes. 
Keamanan Input, 
Auth TMA & 
Anti-Tuyul 
(security_gate.py) 
Sanitasi NFKC 
(SEC-01), 24-byte 
header guard 
(SEC-06), InsightFace 
Pembaca PDF rentan 
Indirect Prompt 
Injection; konteks 
multi-turn rentan 
Three-Stage 
Low-Latency AI 
Guardrail (<80 ms 
p99: Static \rightarrow 



<!-- [ID:02_CORE_AI_S147] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 28

Komponen Blueprint 
Fondasi Desain v1.0 
(Dipertahankan) 
Celah Skala Produksi 
yang Ditemukan pada 
v1.0 
Spesifikasi Upgrade di 
Blueprint v2.0 
(Production-Grade) 
>23 tahun (AI-SEC-02), 
HMAC initData 60 detik 
(API-01), dan sistem 2 
dompet. 
context drift; initData 
masih bisa di-replay 
ribuan kali di dalam 
jendela 60 detik; serta 
koin_bonus rentan 
ditimbun 30 hari 
(hoarding attack) lalu 
dibuka dengan top-up 
Rp 5.000. 
Llama Prompt Guard 
2 86M ONNX 
\rightarrow NeMo 
Guardrails + Llama 
Guard 3 8B INT4), 
Dual-LLM Sandbox 
untuk PDF, 
BoundedReplayGuard 
(65s Ring Buffer), 
Hard-Cap koin_bonus 
25 Koin, WebGL 
Fingerprinting (maks 
2 akun/device), & 
Cloudflare Turnstile. 
Isolasi Hukum 
Voucher & Ekonomi 
Global 
(payment_and_suppo
rt.py) 
Pemisahan merek web 
independen 
(NocturneAI.art) via 
kode voucher dan 
deteksi bahasa 
language_code. 
Validasi voucher via 
koneksi database 
langsung meninggalkan 
jejak jaringan forensik 
antar-server; 
penentuan harga via 
language_code mudah 
diakali pengguna Barat 
dengan mengubah 
bahasa ke id. 
Stateless Ed25519 
Signed Capability 
Voucher 
(Zero-Database & 
Zero-Network Link 
antara bot SFW dan 
web Unfiltered) + 
Matriks Harga 3-Zona 
PPP dengan Tri-Factor 
Geo-Locking 
(Payment Rail 
Hard-Binding QRIS 
khusus Zona 3). 
1.2 Topologi Makro 4-Zona Terisolasi 
1.​ Zona 1 — Omnichannel Ingress & Gatekeeper: Menangani webhook dari Telegram 
Bot, WhatsApp (Cloud API / WAHA), dan Facebook Messenger (Auto-Reply 
Comment), mengubahnya menjadi kontrak standar UnifiedMessageEvent (Pydantic v2), 
mengeksekusi penguncian Fixed-Size Lock Striping, dan menyaring input lewat 
Three-Stage AI Guardrail (<80 ms). 
2.​ Zona 2 — 24/7 Receptionist VPS (Oracle Cloud Ampere A1 ARM / VPS Ringan): 
Menjalankan 7-Node LangGraph Hierarchical Supervisor, Valkey Semantic Cache & 
Vector Router, 9Router (localhost:20128/v1), Single-Writer SQLite WAL / Turso 
libSQL, dan kolektor telemetri Langfuse Self-Hosted. 
3.​ Zona 3 — Dual Execution Pipelines (Jalur A SFW vs. Jalur B Unfiltered): 
○​ Jalur A (Komersial SFW): Diteruskan ke Fal.ai, Replicate, BytePlus Seedance, 
PiAPI Suno, atau RunPod Wan 2.2 dengan safety_checker: true dan Forced 
Negative Prompt. 
○​ Jalur B (Studio Web Independen Unfiltered — NocturneAI.art / 
VelvetRender.sh): Diisolasi secara hukum dan jaringan menggunakan Stateless 



<!-- [ID:02_CORE_AI_S148] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 29

Ed25519 Voucher. Beban kerja dieksekusi pada kontainer GPU dengan isolasi 
kernel (runsc/gVisor), pemrosesan murni di RAM volatil /dev/shm (noexec, nosuid, 
nodev, size=16g), suntikan Negative Tensor Permanen (anti-CSAM/anti-gore), dan 
penghancuran memori instan (zero-overwrite). 
4.​ Zona 4 — Zero-Knowledge Edge Delivery: Cloudflare Worker Edge Relay menyedot 
output media dari CDN hulu dengan kecepatan 10 Gbps (0% beban bandwidth VPS), 
melucuti metadata EXIF/PNG Info secara streaming, mengenkripsi file dengan 
AES-256-GCM menjadi .bin di Cloudflare R2 (auto-delete 24 jam), dan mendekripsinya 
langsung di RAM browser pengguna menggunakan Web Crypto API 
(window.crypto.subtle). 
BAGIAN II: EKSPANSI STACK AI ENGINE (SOTA) & 
ORKESTRASI 7-AGEN LANGGRAPH 
2.1 Katalog Lengkap Engine AI (Fondasi v1.0 + Ekspansi Aditif SOTA 
v2.0) 
Seluruh model pada v1.0 (Gemini Flash, Qwen 2.5, Llama 3.3, DeepSeek R1/V3, Claude 
Sonnet/Opus, Nous Hermes 3, Mistral Nemo, Flux.1 Schnell/Dev, Wan 2.1/2.2, LTX-Video, 
HunyuanVideo, Kling 1.6/2.6/3.0, Google Veo, Sora, Runway, Suno v4/v6, Udio, 
Real-ESRGAN 4K) dipertahankan sepenuhnya dan diperkuat dengan engine SOTA berbiaya 
ultra-rendah berikut: 
Kategori 
Modalitas 
Engine AI 
(Gabungan 
v1.0 & Aditif 
SOTA v2.0) 
Lisensi / Jalur 
Akses 
Spesifikasi 
Teknis & 
Keunggulan 
Produksi 
Biaya Modal 
Operasional 
(HPP) 
Penempatan 
Kasta (Tier) 
LLM & 
Reasoning 
Cepat 
DeepSeek-V4.
1-Flash (552B 
MoE, 8B/16B 
aktif), Gemini 
2.5 Flash, 
Llama 3.3 70B, 
Groq 
Open-Weight / 
API (9Router, 
SiliconFlow, 
OpenRouter 
ZDR) 
Konteks 1,05M 
token, 
arsitektur 
Causal 
Encoder-Decod
er, mendukung 
Zero Data 
Retention 
(ZDR). 
Rp 0 (Free 
Tier) s/d 
$0,042/1M 
input ($0,01 
cached) 
Tier Eco (0 
Koin) & Otak 
Muse Lapis 
1–2 
LLM 
Multimodal & 
Coding 
Qwen 3.7 
Plus, 
Qwen3-Omni-
30B-A3B-Thin
king, Kimi 
K2.7 Code, 
Claude Sonnet 
Open-Weight / 
API (9Router, 
Kiro Free, 
OpenRouter) 
Pemahaman 
dokumen 
PDF/Excel, 
audio, dan 
instruksi 
bahasa Asia 
Tenggara & 
global yang 
sangat presisi. 
Rp 0 (via Kiro) 
s/d $0,14/1M 
input; 
$0,55/1M 
output 
Tier Pro (Otak 
Kampanye & 
Analisis 
Dokumen) 
LLM Unfiltered 
(Bebas 
Nous Hermes 
3 (70B/405B), 
API 
OpenRouter / 
Patuh pada 
instruksi kreatif 
Rp 0 (:free) s/d 
$0,15/1M 
Khusus Jalur B 
(Web Studio 



<!-- [ID:02_CORE_AI_S149] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 30

Kategori 
Modalitas 
Engine AI 
(Gabungan 
v1.0 & Aditif 
SOTA v2.0) 
Lisensi / Jalur 
Akses 
Spesifikasi 
Teknis & 
Keunggulan 
Produksi 
Biaya Modal 
Operasional 
(HPP) 
Penempatan 
Kasta (Tier) 
Sensor) 
Qwen 2.5 72B 
Instruct, Mistral 
Nemo 
Unfiltered 
Novita AI / 
Groq 
horor/dewasa 
fiksi tanpa 
penolakan 
moral, terisolasi 
dari API 
korporat. 
token 
Independen) 
Video 
Generatif 
(Self-Hosted 
GPU) 
Wan 2.2 MoE 
(5B & 14B FP8 
Scaled), Wan 
2.5/2.6, 
LTX-Video, 
HunyuanVideo 
Apache 2.0 
(RunPod 
Serverless / 
Vast.ai 
ComfyUI) 
Pemisahan 
pakar 
high-noise & 
low-noise; 
kualitas 99,5% 
setara FP16 
hanya dengan 
14 GB VRAM + 
akselerasi 54% 
via 
SageAttention 
& TeaCache. 
Rp 110 – Rp 
250 / klip 5 
detik (di RTX 
4090 
FlashBoot) 
Tier Pro 
(Mesin Utama 
Margin 
85%–95%) 
Video 
Komersial 
Flagship (API) 
Seedance 1.5 
Pro, 
Open-Sora 2.0 
(11B), MiniMax 
H3, Kling 
2.6/3.0 (MC), 
Veo, Runway 
API BytePlus / 
Fal.ai / 
WaveSpeed / 
Replicate 
Gerakan tarian 
(motion control) 
dan aksi 
sinematik 
sangat mulus 
tanpa perlu 
sewa GPU per 
jam. 
$0,012/detik 
(~Rp 950/klip 
Seedance) s/d 
Rp 2.500 
(Kling/Veo) 
Tier Pro+ & 
Tier Ultra 
Konsistensi 
Karakter 
Visual 
PuLID Flux II, 
FLUX.2 
Multi-Ref (10 
refs), InstantID 
+ IP-Adapter 
Open-Source 
Node di dalam 
Pipeline 
ComfyUI 
Mengunci 
identitas wajah 
(termasuk 
profile view 
menyamping) & 
pakaian lintas 6 
klip video (30 
detik) tanpa 
model pollution. 
Rp 0 (Berjalan 
di sisa 10 GB 
VRAM yang 
sama) 
Tier Pro & 
Paket Story 30 
Detik 
Voiceover / 
TTS Instan 
Kokoro-82M 
v1.0 (Hexgrad) 
Apache 2.0 
(RAM Lokal / 
OpenRouter 
API) 
Latensi 28 ms 
TTFB (tercepat 
di industri), 
kualitas suara 
natural (ELO 
1.059), sangat 
ringan di RAM. 
$0,62/1M 
karakter (~Rp 
1 per naskah 
iklan 30 detik!) 
Tier Eco & 
Paket Story 30 
Detik 
Efek Suara 
MMAudio 
Open-Source 
MMAudio 
Rp 15 / klip 8 Paket Story 30 



<!-- [ID:02_CORE_AI_S150] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 31

Kategori 
Modalitas 
Engine AI 
(Gabungan 
v1.0 & Aditif 
SOTA v2.0) 
Lisensi / Jalur 
Akses 
Spesifikasi 
Teknis & 
Keunggulan 
Produksi 
Biaya Modal 
Operasional 
(HPP) 
Penempatan 
Kasta (Tier) 
Video (V2A 
Foley) & 
Musik 
(157M), 
HunyuanVideo
-Foley, Suno 
v4/v6 Studio, 
Udio 
(CVPR/Tencent
) & PiAPI 
(Suno) 
menyelaraskan 
efek suara 
langkah 
kaki/ambien 
48kHz per 
frame (CLIP 8 
FPS + 
Synchformer 
25 FPS) dalam 
1,23 detik. 
dtk (MMAudio) 
& ~Rp 800 
(Lagu utuh 
Suno) 
Detik & Tier 
Ultra 
2.2 Arsitektur 7-Node LangGraph Hierarchical Supervisor 
(StateGraph) 
Untuk mencegah kegagalan berantai pada fitur unggulan "1 Perintah Jadi Paket Kampanye 
Utuh" dan "Paket Story / Iklan Utuh 30 Detik", eksekusi linier digantikan oleh LangGraph 
Hierarchical Supervisor Pattern dengan penyimpanan status persisten AsyncSqliteSaver 
(langgraph_checkpoints). Jika server restart saat merender klip ke-3 dari 6 adegan, sistem 
otomatis melanjutkan dari klip ke-4 tanpa membakar ulang modal GPU klip 1–3: 
Node Agen 
Peran Spesifik di Dalam Siklus 
StateGraph 
Input & Output pada 
AgentState 
Node #1: Gatekeeper & 
Billing Agent 
Mengeksekusi Three-Stage 
Guardrail (<80 ms), mendeteksi 
zona PPP (ppp_zone), 
memeriksa SemanticCache 
Valkey (~25 ms), dan 
melakukan pemotongan koin 
atomik 
(atomic_escrow_charge). 
In: UnifiedMessageEvent Out: 
escrow_tx_id, intent, ppp_zone 
Node #2: Muse Supervisor 
(Central Controller) 
Memegang kendali pusat atas 
Shared Workflow State 
menggunakan primitif 
Command(goto=...). 
Mengevaluasi hasil kerja setiap 
agen pekerja dan 
memerintahkan self-correction 
loop jika terjadi cacat output. 
In: AgentState Out: Routing 
Command(goto=NextAgent) 
Node #3: Prompt Engineer & 
Heat Router Agent 
Melakukan Zero-Passthrough 
Canonical Reconstruction 
(menulis ulang prompt dari nol 
dalam bahasa Inggris 
sinematik) dan menghitung 
Multi-Dimensional Semantic 
Heat Score (0–100). 
In: Raw user request Out: 
canonical_prompts[], 
heat_score, target_zone 



<!-- [ID:02_CORE_AI_S151] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 32

Node Agen 
Peran Spesifik di Dalam Siklus 
StateGraph 
Input & Output pada 
AgentState 
Node #4: Visual Continuity & 
Character Lock Agent (Baru) 
Mengekstrak frame terakhir dari 
klip ke-N dengan FFmpeg, 
membuat turnaround sheet 
(depan, 3/4, samping), dan 
menyuntikkan embedding 
wajah via PuLID Flux II ke start 
frame klip ke-(N+1) agar 6 klip 
(30 detik) 100% bebas 
character drift. 
In: clip_N_output.mp4 Out: 
pulid_face_embed, 
clip_N+1_seed_frame 
Node #5: Stateless Media 
Worker Agent 
Mengeksekusi render 
paralel/sekuensial ke RunPod 
Serverless FlashBoot (Wan 2.2 
FP8 + TeaCache) atau API 
Grosir dengan Two-Phase 
Circuit Breaker (3s Cut-Off) dan 
pemeriksaan 1ms Shannon 
Entropy (anti-layar hitam). 
In: ComfyWorkflowJSON, 
pulid_face_embed Out: 
raw_video_clips[] di /dev/shm 
Node #6: V2A Foley & Audio 
Mastering Agent (Baru) 
Memproduksi 3 jalur audio 
(stems): narasi Kokoro-82M 
(~Rp 1), efek gerakan sinkron 
MMAudio / 
HunyuanVideo-Foley (48kHz 
dalam 1,23 dtk), dan musik 
latar Suno. Menerapkan 
FFmpeg Auto-Ducking 
(menurunkan musik saat narasi 
bicara) & crossfade. 
In: raw_video_clips[], 
voice_script Out: 
mastered_audio.wav, 
final_30s_muxed.mp4 
Node #7: AI Support & Triage 
Agent (CS 24/7) 
Memiliki koneksi database 
Read-Only (?mode=ro) untuk 
mengaudit Job_ID yang 
dikeluhkan pelanggan, 
mengeksekusi 
safe_one_time_refund jika 
terbukti gagal di hulu, dan 
mengirim tombol eskalasi 1-klik 
ke Admin. 
In: Tiket komplain / bukti 
transfer Out: Resolusi otomatis 
/ Webhook Admin 
2.3 Matriks Routing 4-Zona Berdasarkan Semantic Heat Score & 
Isolasi Voucher Ed25519 
A. Tabel 4-Zona Eksekusi Pre-Flight Heat Router 
Zona & Rentang Heat 
Score 
Klasifikasi Konteks 
Semantik 
Tindakan Pre-Flight & 
Transformasi Prompt 
Rute Eksekusi Engine 
& Isolasi Pengiriman 
🟢 Zona Hijau (Skor 0 
– 25) 
Konten komersial 
UMKM, iklan produk, 
Zero-Passthrough 
Canonical 
Diteruskan ke pipa 
@bikinAI_bot (Fal.ai, 



<!-- [ID:02_CORE_AI_S152] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 33

Zona & Rentang Heat 
Score 
Klasifikasi Konteks 
Semantik 
Tindakan Pre-Flight & 
Transformasi Prompt 
Rute Eksekusi Engine 
& Isolasi Pengiriman 
lanskap, edukasi, 
animasi umum (100% 
SFW). 
Reconstruction + 
Injeksi Forced Negative 
Prompt (nsfw, nude, 
gore, blood). 
Replicate, Kling, Veo, 
Wan 2.2) dengan 
safety_checker: true. 
🟡 Zona Kuning (Skor 
26 – 60) 
Konten ambigu, 
sinematik gelap, aksi 
laga/horor mistis fiksi, 
atau mode busana 
yang rawan memicu 
false-positive sensor di 
API hulu. 
Muse Auto-Rewrite 
(AGG-01) menulis 
ulang kalimat 
menggunakan Qwen 
3.7 / Llama 3.3 70B 
menjadi narasi artistik 
dewasa (>25 tahun) 
yang sopan dan aman 
bagi API hulu. 
Dirender pada engine 
Tier Pro/Ultra yang 
mendukung kontrol 
estetika sinematik + 
pemeriksaan 1ms 
Shannon Entropy 
untuk mencegah black 
image. 
🟣 Zona Magenta 
(Skor 61 – 99) 
Permintaan kreatif 
eksplisit / Unfiltered 
dewasa yang sah (>23 
tahun, karakter fiksi 
murni). 
Di ruang chat 
@bikinAI_bot, bot 
menolak secara sopan 
(Rp 0 dipotong) dan 
menyajikan tombol 
konversi [🎟️ Tukar 
Koin ke Compute 
Voucher]. 
Dieksekusi eksklusif di 
Studio Web 
Independen 
(NocturneAI.art / 
VelvetRender.sh) via 
Nous Hermes 3 
Uncensored & GPU 
Worker /dev/shm 
(enable_safety_checke
r: false) + pengiriman 
.bin AES-256-GCM. 
🔴 Zona Merah Fatal 
(Skor 100) 
Indikasi CSAM, 
unggahan wajah usia 
<23 tahun pada 
InsightFace, deepfake 
selebriti/tokoh nyata, 
atau instruksi bahaya 
fisik. 
Hard-Block di 
Gerbang Lokal pada 
Biaya Rp 0 sebelum 
menyentuh Master API 
Key mana pun. 
Permintaan dihentikan 
total, dicatat ke log 
kepatuhan internal, dan 
fitur upload akun 
dikenakan cooldown 24 
jam tanpa merampas 
saldo uang yang 
memicu sengketa bank. 
B. Isolasi Kriptografis Tanpa Koneksi Database (Stateless Ed25519 Capability 
Voucher) 
Agar tidak ada satu pun koneksi jaringan, kueri SQL, atau panggilan API antara server 
@bikinAI_bot (SaaS produktivitas domestik) dan server NocturneAI.art (studio web independen 
global): 
1.​ Saat pengguna menukar koin di @bikinAI_bot, bot memotong koin secara atomik dan 
menandatangani payload biner (voucher_nonce, coin_amount, origin_ppp_tier, 
expiry_timestamp) menggunakan Kunci Privat Ed25519 yang hanya ada di server 
@bikinAI_bot, menghasilkan kode VCH-<base64url_payload>.<ed25519_signature>. 
2.​ Server NocturneAI.art hanya menyimpan Kunci Publik Ed25519 untuk memverifikasi 
tanda tangan tersebut secara matematis dalam 0,1 milidetik dan mencatat 
voucher_nonce ke tabel lokalnya sendiri untuk mencegah double-spending. Secara 



<!-- [ID:02_CORE_AI_S153] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 36

Compute Voucher dibatasi maksimal 3 voucher per hari per akun. 
3.4 Tabel Biaya Tetap 24/7 & Simulasi Keuntungan Bulanan (Upgrade 
v2.0) 
A. Biaya Tetap Infrastruktur 24 Jam (Termasuk Valkey Cache, Guardrail ONNX, & 
Langfuse) 
Seluruh komponen tambahan pada v2.0 (Valkey Semantic Cache ~120 MB RAM, Llama 
Prompt Guard 2 86M ONNX ~350 MB RAM, dan Langfuse Telemetry Collector) berjalan 
langsung di dalam kapasitas Oracle Cloud Free Tier Ampere A1 (12–24 GB RAM Gratis 
Selamanya) sehingga biaya tetap bulanan tetap Rp 0 (Skema Gerilya) hingga Rp 
41.000/bulan (Skema VPS Stabil)! 
B. Simulasi Keuntungan Bulanan (Gabungan Pasar Domestik QRIS + 20% Trafik 
Global PPP) 
Skala Trafik 
Harian 
Total Video / 
Bulan 
Omzet Kotor 
(80% Zona 3 
QRIS + 20% 
Zona 1/2 
Global) 
Biaya Server 
24 Jam + 
LLM (Valkey 
Hit 75%) 
Biaya GPU 
(Wan 2.2 
FP8 + 
TeaCache) 
Potongan 
Gateway 
(QRIS / 
Stars) 
Laba Bersih 
/ Bulan 
(v2.0) 
Sepi (10 
video/hari) 
300 video 
Rp 960.000 Rp 25.000 
Rp 60.000 
Rp 28.000 
Rp 847.000 
(Naik ~88% 
dari v1.0) 
Sedang (50 
video/hari) 
1.500 video Rp 
4.800.000 
Rp 41.000 
Rp 300.000 Rp 140.000 Rp 
4.319.000 
(Naik ~79% 
dari v1.0) 
Ramai (200 
video/hari) 
6.000 video Rp 
19.200.000 
Rp 75.000 
Rp 
1.080.000 
Rp 560.000 Rp 
17.485.000 
(Naik ~74% 
dari v1.0) 
BAGIAN IV: HARDENING KEAMANAN BERLAPIS 
(DEFENSE-IN-DEPTH) & MITIGASI ANTI-TUYUL 
4.1 Arsitektur Three-Stage Low-Latency AI Guardrail (<80 ms p99) & 
Dual-LLM PDF Sandbox 
Untuk mengatasi Indirect Prompt Injection pada dokumen PDF/Word/Excel yang diunggah 
pengguna serta mencegah Multi-Turn Context Drift pada kompresi memori 9Router tanpa 
memperlambat bot: 
1.​ Stage 1 — Sub-Millisecond Static Gate (<1 ms): Normalisasi Unicode NFKC (SEC-01), 
penghapusan karakter kontrol (Cf, Cc, Cs), validasi skema ketat Pydantic v2, dan 24-Byte 
Header Guard (MAX_IMAGE_PIXELS = 2_073_600) untuk menolak Decompression 



<!-- [ID:02_CORE_AI_S154] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 37

Bomb (SEC-06). 
2.​ Stage 2 — Fast First-Pass Injection Filter (20–50 ms): Menjalankan Llama Prompt 
Guard 2 (86M) (berbasis mDeBERTa, dikuantisasi ke ONNX INT8 di CPU ARM/VPS, 
makan RAM <400 MB) untuk mendeteksi upaya prompt injection dan jailbreak secara 
instan. 
3.​ Stage 3 — Dialog & Hazard Classification Rails (20–65 ms): Hanya dipicu untuk pesan 
mencurigakan atau pembuatan media sensitif, menggunakan NVIDIA NeMo Guardrails 
(Colang) untuk melacak alur percakapan multi-giliran (anti-context drift sebelum 
dirangkum oleh 9Router) dan Llama Guard 3 8B (INT4) / InsightFace >23 Tahun 
(AI-SEC-02). 
4.​ Privilege Separation (Dual-LLM PDF Sandbox): Teks yang diekstrak dari file 
PDF/Word/Excel dibungkus di dalam tag XML acak per sesi 
(<untrusted_doc_9f8a>...</untrusted_doc_9f8a>) dan diproses oleh instans LLM 
pembaca terisolasi yang sama sekali tidak memiliki akses ke tools, database, 
maupun fungsi safe_one_time_refund. 
4.2 Matriks Pertahanan Anti-Tuyul (Sybil Resistance) & Anti-Hoarding 
Koin Bonus 
Menutup celah peternakan akun kloningan (emulator farm) yang menimbun klaim harian Rp 400 
(4 Koin Bonus): 
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
skrip Telethon). 
Saat membuka Mini 
App untuk klaim harian, 
JS mengekstrak hash 
gabungan dari WebGL 
Renderer/Vendor, 
AudioContext 
Oscillator, Canvas 2D 
Entropy, resolusi layar 
fisik, dan daftar font 
sistem. 
Maksimal 2 
telegram_user_id per 
1 device_fp_hash 
yang diizinkan 
mengklaim koin harian 
dalam 24 jam. Akun 
ke-3 pada perangkat 
yang sama otomatis 
ditolak. 
2. Behavioral 
Biometrics & Sensor 
Telemetry 
Bot pengklik otomatis 
(Auto-Clicker / Macro) 
dan tembakan POST 
request langsung ke 
endpoint klaim harian. 
Merekam varians 
tekanan/radius 
sentuhan (touchstart 
\rightarrow touchend), 
mikro-getaran giroskop 
HP 
(DeviceOrientationEven
t), dan kurva waktu 
interaksi sejak halaman 
dimuat. 
Jika varians koordinat 
klik = 0.0 (klik robotik di 
piksel yang sama 
persis) atau giroskop 
bernilai statis mutlak 
pada perangkat seluler, 
tandai sebagai 
SUSPECTED_BOT. 
3. Cloudflare Turnstile 
+ Hard-Cap Saldo 
koin_bonus (25 Koin) 
Serangan penimbunan 
(Hoarding Attack) 
koin_bonus selama 30 
Menyematkan widget 
Cloudflare Turnstile 
(Gratis 100%) di dalam 
Pengguna tidak bisa 
menimbun koin_bonus 
melebihi 25 Koin 



<!-- [ID:02_CORE_AI_S155] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 39

Lapisan Arsitektur (Folder / 
Modul) 
File Inti di Dalamnya 
Tanggung Jawab & Prinsip 
Isolasi (Zero-Refactoring 
Guarantee) 
Gatekeeper. 
services/security/ (Modul 2: 
security_gate.py) 
initdata_auth.py, guardrails.py, 
sybil_shield.py, vision_gate.py 
Menjalankan HMAC-SHA256 
initData + 
BoundedReplayGuard, sanitasi 
NFKC, Llama Prompt Guard 2 
(86M) / NeMo, verifikasi Device 
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
Valkey SemanticCache & 
SemanticRouter, serta Heat 
Score Router. 
services/workers/ (Modul 4: 
stateless_gpu_worker.py) 
comfy_serverless.py, 
wholesale_api.py, 
ffmpeg_compiler.py, 
aes_gcm_packager.py 
Mengelola Two-Phase Circuit 
Breaker (3s Cut-Off), 
Reconciliation Polling (5s), 
eksekusi /dev/shm, ekstraksi 
frame PuLID, penggabungan 
audio MMAudio/Kokoro, 
Cost-Based Margin Guard 
(75%), dan enkripsi .bin. 
services/billing/ (Modul 1 & 5: 
payment_and_support.py) 
wallet_repository.py, 
qris_gateway.py, 
stars_crypto.py, 
voucher_crypto.py 
Mengelola Fixed-Size Lock 
Striping, Single-Writer Queue 
SQLite/Turso, transaksi 
koin_utama & koin_bonus, 
penerbitan Ed25519 Compute 
Voucher, komisi afiliasi 2 jalur, 
serta AI Support & Triage 
Agent. 
edge/cloudflare_worker/ 
(Relay Zero-VPS) 
worker_relay.ts, wrangler.toml Menyedot media dari CDN hulu 
(ALLOWED_UPSTREAM_CDN
), melucuti EXIF secara 
streaming, mengenkripsi ke 
.bin, dan menyimpannya ke R2 
dengan auto-delete 24 jam. 
5.2 Skema Database Lengkap (6 Tabel Fondasi: SQLite WAL 
Single-Writer & Turso libSQL Ready) 
Selain tabel users dan jobs, sistem menyiapkan 4 tabel struktural tambahan (platform_identities, 
wallet_ledger, phash_audit_log, dan langgraph_checkpoints): 
-- PRAGMA OPTIMIZATION UNTUK MENGELIMINASI SQLITE_BUSY DI VPS RINGAN​
PRAGMA journal_mode = WAL;​



<!-- [ID:02_CORE_AI_S156] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 47

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



<!-- [ID:02_CORE_AI_S157] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 50

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



<!-- [ID:02_CORE_AI_S158] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 64

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



<!-- [ID:02_CORE_AI_S159] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 65

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



<!-- [ID:02_CORE_AI_S160] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 66

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



<!-- [ID:02_CORE_AI_S161] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# [1] 9Router Localhost (Otomatis rotasi semua API gratis + 98% Quota 
Surfing) -> REKOMENDASI UTAMA​

<!-- [ID:02_CORE_AI_S162] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# [4] OpenRouter Auto-Free (Otomatis pilih Qwen 2.5 / DeepSeek R1 
berlabel :free)​

<!-- [ID:02_CORE_AI_S163] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# [1] Nous Hermes 3 Uncensored (via OpenRouter / Novita)​

<!-- [ID:02_CORE_AI_S164] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# [2] Qwen 2.5 72B Instruct (via 9Router / Groq)​

<!-- [ID:02_CORE_AI_S165] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 79

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



<!-- [ID:02_CORE_AI_S166] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 80

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

<!-- [ID:02_CORE_AI_S167] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 83

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



<!-- [ID:02_CORE_AI_S168] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 86

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


