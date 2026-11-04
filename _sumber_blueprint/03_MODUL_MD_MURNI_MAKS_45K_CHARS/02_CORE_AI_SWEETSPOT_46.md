
<!-- [ID:02_CORE_AI_S265] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 229

Laporan Arsitektur Produksi dan 
Verifikasi Kompilasi 
Monolith-Orchestrator BikinAI Super 
Intelligence v4.0.0 (V4.0.txt) 
File Python telah siap. Seluruh kode produksi utuh untuk BikinAI Super Intelligence — Master 
Engine v4.0.0 Monolith-Orchestrator telah ditulis secara lengkap ke dalam berkas V4.0.txt di 
lingkungan eksekusi latar belakang tanpa pemotongan maupun penggunaan penampung 
sementara. Berkas produksi berukuran 75.093 bita yang terdiri atas 1.730 baris kode tersebut 
telah melewati pengujian pohon sintaks abstrak melalui ast.parse serta kompilasi kode bita 
melalui py_compile.compile pada Python 3.11.8 dengan hasil seratus persen bebas dari 
kesalahan sintaks. 
Parameter Artefak Produksi 
Spesifikasi Terverifikasi 
Status Validasi 
Nama Berkas Keluaran 
V4.0.txt 
Tersimpan di Sandbox 
Ukuran & Volume Kode 
75.093 bita / 1.730 baris kode 
utuh 
Tanpa Pemotongan 
Validasi Pohon Sintaks 
(ast.parse) 
Pemeriksaan struktur tata 
bahasa AST Python 3.11.8 
Lulus (0 Kesalahan) 
Validasi Kompilasi 
(py_compile) 
Kompilasi bytecode mode ketat 
(doraise=True) 
Lulus (0 Kesalahan) 
Basis Data Inti 
~/.bikinai_vault/bikinai_master_
vault.db (16 Tabel SQLite WAL) 
Terinisialisasi Otomatis 
Server Web & Hub 
Omnichannel 
Dual Web Server Port 8080 (5 
Endpoint GET, 8 Endpoint 
POST) 
Aktif & Terintegrasi 
Fondasi Konkurensi, Autentikasi Fail-Closed, dan 
Skema 16 Tabel SQLite WAL 
Arsitektur penyimpanan data pada V4.0.txt dirancang untuk mengatasi keterbatasan 
penguncian tingkat berkas (file-level locking) yang lazim terjadi pada implementasi SQLite 
konvensional ketika menerima lonjakan transaksi asinkron dari ribuan pengguna secara 
bersamaan. Melalui komponen SingleWriterSQLiteDaemon, seluruh operasi penulisan 
(INSERT, UPDATE, DELETE) diserialisasikan ke dalam satu antrean memori asyncio.Queue 
yang diproses oleh pekerja tunggal di latar belakang, sementara operasi pembacaan dieksekusi 
secara paralel melalui fungsi manajemen konteks get_db(). Konfigurasi mesin basis data pada 
jalur ~/.bikinai_vault/bikinai_master_vault.db secara otomatis menerapkan PRAGMA 
journal_mode=WAL, PRAGMA synchronous=NORMAL, PRAGMA foreign_keys=ON, serta 
PRAGMA busy_timeout=5000 untuk menjamin durabilitas transaksi sekaligus mempertahankan 
latensi baca di bawah satu milidetik. 
Untuk mencegah kondisi balapan (race condition) pada pemotongan saldo koin pengguna 
tanpa menghentikan alur eksekusi pengguna lain, sistem menerapkan pemisahan kunci 



<!-- [ID:02_CORE_AI_S266] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 233

\text{Combo Grading Score} = (40 \times \text{Quality Score}) - (10 \times \text{Average 
Latency}) - (5 \times \text{Cost Multiplier}) 
Kunci Agen Nama 
Lengkap 
Model di 
Rolling Pool 
Skor Kualitas Latensi 
Rata-Rata 
(Detik) 
Pengali 
Biaya 
Combo 
Grading 
Score 
Status 
Abliterated 
DEEPSEEK DeepSeek 
R1 0528 
Deep 
Thought 
9,9 
1,40 s 
1,0 
377,0 
Tidak 
ARGON 
Argon Ultra 
Reasoning 
v4 
9,8 
1,10 s 
1,2 
375,0 
Tidak 
HERMES 
Hermes 4 
405B 
Flagship 
Uncensored 
9,9 
1,50 s 
1,5 
373,5 
Ya (True) 
HARNESS 
HARNESS 
OpenHands 
Autonomous 
Coder 
9,7 
1,20 s 
1,1 
370,5 
Tidak 
MUSE 
MUSE Spark 
1.2 Creative 
SOTA 
9,5 
0,80 s 
0,9 
367,5 
Tidak 
QWEN 
Qwen 2.5 
72B Instruct 
High-Context 
9,4 
0,90 s 
0,8 
363,0 
Tidak 
GROQ_CER
EBRAS 
Groq-Cerebr
as Ultra-Low 
Latency 
9,1 
0,25 s 
0,7 
358,0 
Tidak 
NANO_MUS
E 
NANO_MUS
E Glimmer 
Fast Edge 
8,7 
0,30 s 
0,4 
343,0 
Tidak 
Berdasarkan evaluasi kuantitatif pada seluruh agen di atas, DEEPSEEK (DeepSeek R1 0528 
Deep Thought) memimpin peringkat keseluruhan dengan skor komposit 377,0 (kualitas 9,9, 
latensi 1,40 detik, pengali biaya 1,0), disusul oleh ARGON (Argon Ultra Reasoning v4) dengan 
skor 375,0 (kualitas 9,8, latensi 1,10 detik, pengali biaya 1,2) serta HERMES (Hermes 4 405B 
Flagship Uncensored) pada skor 373,5 (kualitas 9,9, latensi 1,50 detik, pengali biaya 1,5, 
berstatus abliterated). Untuk tugas rekayasa perangkat lunak dan penulisan kreatif cepat, 
HARNESS mencatat skor 370,5 pada batas latensi tepat 1,20 detik, sedangkan MUSE (367,5, 
latensi 0,80 detik) dan QWEN (363,0, latensi 0,90 detik) menjaga keseimbangan antara 
kapasitas konteks tinggi dan waktu tunggu sub-detik. Di sisi kecepatan ekstrem, 
GROQ_CEREBRAS (358,0, latensi 0,25 detik) dan NANO_MUSE (343,0, latensi 0,30 detik) 
menyediakan respons hampir instan dengan beban biaya terendah. Ketika menerima kueri 
pengguna, SmartRouterV4.dispatch menerapkan Staggered Speculative Hedging: agen 
Tier-1 dieksekusi pada t = 0, dan apabila belum selesai dalam ambang waktu 1,2 detik, agen 
Tier-2 yang memiliki latensi lebih rendah ditembakkan secara paralel untuk menjamin 



<!-- [ID:02_CORE_AI_S267] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 246

No 
Nama Sumber & 
Keluarga Model 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis, 
Format & Peran 
Failover 
er2.5-v1-abliterate
d Gemma-4 
26B-A4B MoE: 
https://huggingface
.co/huihui-ai/Huihu
i-gemma-4-26B-A4
B-it-abliterated 
Qwen3-Coder-Nex
t: 
https://huggingface
.co/huihui-ai/Huihu
i-Qwen3-Coder-Ne
xt-abliterated 
CyberStrike-OffSe
c-35B: 
https://huggingface
.co/huihui-ai/Huihu
i-CyberStrike-OffS
ec-35B-abliterated 
Qwythos-9B-1M 
Context: 
https://huggingface
.co/huihui-ai/Huihu
i-Qwythos-9B-Clau
de-Mythos-5-1M-a
bliterated-GGUF 
xt & 
Gemma-4-12B-co
der) tanpa 
pemblokiran 
heuristik. 
1B.4 
Keluarga 
Penalaran SOTA 
DeepSeek-R1 & 
V3 
R1-0528-Qwen3-8
B: 
https://huggingface
.co/deepseek-ai/D
eepSeek-R1-0528-
Qwen3-8B R1 
GGUF (Unsloth): 
https://huggingface
.co/unsloth/DeepS
eek-R1-GGUF 
R1-0528 (684B 
Full): 
https://huggingface
.co/deepseek-ai/D
eepSeek-R1-0528 
R1-Distill-Qwen-32
B: 
Huihui 
Qwen3.5-4B-Clau
de-4.6-Opus 
Reasoning Distill: 
https://huggingface
.co/huihui-ai/Huihu
i-Qwen3.5-4B-Cla
ude-4.6-Opus-ablit
erated 
Llama-3.2-3B-Instr
uct Abliterated: 
https://huggingface
.co/huihui-ai/Llama
-3.2-3B-Instruct-ab
literated 
DeepSeek-R1-052
8-Qwen3-8B 
mencapai akurasi 
86,0% pada AIME 
2024, melampaui 
o3-mini (79,6%) 
dan 
Gemini-2.5-Flash-
Thinking (82,3%), 
sehingga menjadi 
worker penalaran 
lokal utama. 



<!-- [ID:02_CORE_AI_S268] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 247

No 
Nama Sumber & 
Keluarga Model 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis, 
Format & Peran 
Failover 
https://huggingface
.co/deepseek-ai/D
eepSeek-R1-Distill
-Qwen-32B 
V3-Base: 
https://huggingface
.co/deepseek-ai/D
eepSeek-V3-Base 
1B.5 
Katalog 
Uncensored 
Berbasis Dataset 
Dolphin 
(Retraining-Based) 
Katalog: 
https://huggingface
.co/models?datase
t=dataset:cognitive
computations/dolp
hin 
Dolphin-2.9-Llama
3-8B: 
https://huggingface
.co/cognitivecomp
utations/dolphin-2.
9-llama3-8b 
Dolphin-2.7-Mixtral
-8x7B-4bit (Apple 
MLX): 
https://huggingface
.co/mlx-community
/dolphin-2.7-mixtra
l-8x7b-4bit 
Digunakan 
sebagai jalur 
alternatif apabila 
tugas agen 
membutuhkan 
gaya percakapan 
yang dilatih ulang 
secara penuh 
pada dataset 
tanpa filter 
(fine-tuned) 
dibandingkan 
penyuntingan 
bobot 
(abliteration). 
Berbeda dengan 
abliteration yang 
memodifikasi 
matriks bobot 
secara bedah 
vektor, keluarga 
Dolphin melatih 
ulang model pada 
korpus instruksi 
bersih tanpa 
penolakan. 
1B.6 
Model Dasar 
Qwen, Bobot 
Router & Dataset 
Kalibrasi 
Abliteration 
Qwen3.5-4B: 
https://huggingface
.co/Qwen/Qwen3.
5-4B 
Qwen2.5-1.5B-Inst
ruct: 
https://huggingface
.co/Qwen/Qwen2.
5-1.5B-Instruct 
Qwen3-8B-Base: 
https://huggingface
.co/Qwen/Qwen3-
8B-Base 
Qwen3-235B-A22
B: 
https://huggingface
Qwen3.8-27B 
Base: 
https://huggingface
.co/Qwen/Qwen3.
8-27B 
Qwen3.6-35B-A3B 
Base: 
https://huggingface
.co/Qwen/Qwen3.
6-35B-A3B 
Menyediakan 
model fondasi 
untuk eksperimen 
ablasi mandiri, 
bobot faktorisasi 
matriks untuk 
lm-sys/RouteLLM, 
serta pasangan 
dataset kalibrasi 
semantik yang 
terbukti menekan 
derau (noise) 
ruang residual 
hingga 
D_{\text{KL}} = 
0,0509. 



<!-- [ID:02_CORE_AI_S269] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 248

No 
Nama Sumber & 
Keluarga Model 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis, 
Format & Peran 
Failover 
.co/Qwen/Qwen3-
235B-A22B 
RouteLLM 
Weights: 
https://huggingface
.co/routellm/mf_gp
t4_augmented 
Semantic-Harmles
s: 
https://huggingface
.co/datasets/hereti
c-org/Semantic-Ha
rmless 
Semantic-Harmful: 
https://huggingface
.co/datasets/hereti
c-org/Semantic-Ha
rmful Multilingual: 
https://huggingface
.co/datasets/hereti
c-org/Multilingual-
Harmless-Harmful 
1C. Model & Engine Multimodal SOTA (Video, Gambar, Suara, Musik, Visi - Tanpa 
Login) 
Integrasi seluruh tautan dari sub-kategori 1C pada LINK SUMBER.pdf dan komponen 
multimodal dari Kategori 3 pada Link_daftar_vps server.txt diperkuat dengan repositori resmi 
ali-vilab/TeaCache (CVPR 2025 Highlight), thu-ml/SageAttention (hulu resmi dari fork 
cooper1637), instantX-research/InstantID (pendamping PuLID), serta mesin TTS lokal 
berkecepatan ekstrem OHF-Voice/piper1-gpl (penerus resmi rhasspy/piper yang diarsipkan 
pada Oktober 2025) dan k2-fsa/sherpa-onnx. Kombinasi ini memungkinkan agen melakukan 
degradasi anggun (graceful degradation) dari sintesis video/suara berkapasitas besar pada 
GPU menuju model ultra-ringan yang tetap berjalan mulus di atas CPU atau perangkat tepi 
(edge). 
No 
Nama Sumber & 
Modalitas 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis, 
Kebutuhan VRAM 
& Peran Failover 
1C.1 
Koleksi Lengkap 
Wan2.1 & Wan2.2 
(Generasi & 
Penyuntingan 
Video SOTA) 
Koleksi: 
https://huggingface
.co/collections/Wa
n-AI/wan21 
T2V-1.3B: 
Wan-AI Org & 
Diffusers 
Collections 
(Wan2.2-diffusers, 
Wan2.1-diffusers): 
Mencakup T2V, 
I2V, 
First-Last-Frame-t
o-Video (FLF2V), 
dan Video 



<!-- [ID:02_CORE_AI_S270] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 249

No 
Nama Sumber & 
Modalitas 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis, 
Kebutuhan VRAM 
& Peran Failover 
https://huggingface
.co/Wan-AI/Wan2.
1-T2V-1.3B/tree/m
ain T2V-14B: 
https://huggingface
.co/Wan-AI/Wan2.
1-T2V-14B 
I2V-14B-720P 
VAE: 
https://huggingface
.co/Wan-AI/Wan2.
1-I2V-14B-720P/bl
ob/main/Wan2.1_
VAE.pth 
I2V-14B-480P: 
https://huggingface
.co/Wan-AI/Wan2.
1-I2V-14B-480P 
FLF2V-14B-720P: 
https://huggingface
.co/Wan-AI/Wan2.
1-FLF2V-14B-720
P VACE-14B: 
https://huggingface
.co/Wan-AI/Wan2.
1-VACE-14B 
VACE-1.3B: 
https://huggingface
.co/Wan-AI/Wan2.
1-VACE-1.3B 
Wan2.2-TI2V-5B 
MoE: 
https://huggingface
.co/Wan-AI/Wan2.
2-TI2V-5B 
https://huggingface
.co/Wan-AI/collecti
ons Official HF 
Space (ZeroGPU 
Fallback): 
https://huggingface
.co/spaces/Wan-AI
/Wan2.1 
TeaCache4Wan2.
1 Script: 
https://github.com/
ali-vilab/TeaCache/
blob/main/TeaCac
he4Wan2.1/READ
ME.md 
All-in-one Creation 
& Editing (VACE) 
berlisensi 
Apache-2.0. 
Wan2.1 
merupakan model 
video pertama 
yang mampu 
merender teks 
visual bahasa 
Inggris dan 
Mandarin secara 
akurat. 
1C.2 
Tencent 
HunyuanVideo 
Suite (T2V, I2V, 
Avatar & Foley) 
HunyuanVideo-1.5 
(Distilasi 4–12 
Langkah): 
https://github.com/
Tencent-Hunyuan/
HunyuanVideo-1.5 
Lisensi 1.5: 
https://github.com/
Digunakan secara 
berpasangan: 
HunyuanVideo-Fol
ey sebagai 
generator efek 
suara utama dan 
hkchengrex/MMAu
dio (157 juta 
HunyuanVideo-1.5 
memangkas waktu 
render sebesar 
75% (<75 detik 
pada RTX 4090) 
melalui distilasi 
langkah dan 
sgl-kernel==0.3.18



<!-- [ID:02_CORE_AI_S271] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 250

No 
Nama Sumber & 
Modalitas 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis, 
Kebutuhan VRAM 
& Peran Failover 
Tencent-Hunyuan/
HunyuanVideo-1.5
/blob/main/LICEN
SE HunyuanVideo 
Base: 
https://github.com/
Tencent-Hunyuan/
HunyuanVideo 
HunyuanVideo-I2V
: 
https://github.com/
Tencent-Hunyuan/
HunyuanVideo-I2V 
HunyuanVideo-Av
atar (10 GB 
VRAM): 
https://github.com/t
encent-hunyuan/h
unyuanvideo-avata
r 
HunyuanVideo-Fol
ey: 
https://github.com/
Tencent-Hunyuan/
HunyuanVideo-Fol
ey MMAudio 
(157M V2A Foley 
dari Sumber 3): 
https://github.com/
hkchengrex/MMAu
dio 
parameter) 
sebagai fallback 
ringan untuk 
sinkronisasi 
Video-to-Audio 
(V2A). 
. 
HunyuanVideo-Av
atar berjalan 
hanya dalam 10 
GB VRAM 
menggunakan 
integrasi Wan2GP 
dan TeaCache. 
1C.3 
Lightricks 
LTX-Video & 
LTX-2 (Video + 
Audio 
Tersinkronisasi 8 
GB VRAM) 
Repo Kode: 
https://github.com/
Lightricks/ltx-video 
Bobot HF: 
https://huggingface
.co/Lightricks/LTX-
Video 
TeaCache4LTX-Vi
deo: 
https://github.com/
ali-vilab/TeaCache/
blob/main/TeaCac
he4LTX-Video/RE
ADME.md 
Varian 
terkuantisasi 8-bit 
LTX-VideoQ8 
merender video 
720 \times 480 
\times 121 frame 
dalam <1 menit 
pada RTX 4060 (8 
GB VRAM), 
mendukung 
long-shot 60 detik 
dan kontrol 



<!-- [ID:02_CORE_AI_S272] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 252

No 
Nama Sumber & 
Modalitas 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis, 
Kebutuhan VRAM 
& Peran Failover 
dalam hitungan 
detik. 
1C.6 
Mesin Suara 
(TTS) 
Ultra-Ringan CPU 
& Edge 
(Kokoro-82M, 
Piper, 
Sherpa-ONNX) 
Kokoro-82M v1.0: 
https://huggingface
.co/hexgrad/Kokor
o-82M 
Kokoro-82M 
v1.1-zh: 
https://huggingface
.co/hexgrad/Kokor
o-82M-v1.1-zh 
Skrip EN: 
https://huggingface
.co/hexgrad/Kokor
o-82M-v1.1-zh/blo
b/main/samples/m
ake_en.py Skrip 
ZH: 
https://huggingface
.co/hexgrad/Kokor
o-82M-v1.1-zh/blo
b/main/samples/m
ake_zh.py Misaki 
G2P: 
https://github.com/
hexgrad/misaki 
Piper TTS (C++ 
ONNX Archive): 
https://github.com/
rhasspy/piper & 
Releases: 
https://github.com/
rhasspy/piper/rele
ases Piper1-GPL 
(Repositori Aktif 
Baru): 
https://github.com/
OHF-Voice/piper1-
gpl Sherpa-ONNX 
(Runtime 
TTS/ASR Lintas 
Platform): 
https://github.com/
k2-fsa/sherpa-onn
x 
Kokoro-82M 
(Apache-2.0, 
StyleTTS 2 + 
iSTFTNet) berjalan 
sangat cepat di 
CPU dengan biaya 
setara Rp 
1/naskah 
(<$0,06/jam audio 
24 kHz). Sebagai 
fallback biner C++ 
murni tanpa 
ketergantungan 
PyTorch, sistem 
otomatis beralih ke 
OHF-Voice/piper1-
gpl atau 
k2-fsa/sherpa-onn
x. 
1C.7 
Mesin TTS Emosi 
Multi-Karakter & 
Voice Cloning 
SOTA (Fish 
Speech, 
CosyVoice, 
F5-TTS, ChatTTS) 
Fish Speech 
(S2-Pro & Drama 
3): 
https://github.com/f
ishaudio/fish-spee
ch Rilis Fish 
Speech: 
https://github.com/f
ishaudio/fish-spee
ch/releases Ref 
Arsitektur: 
https://github.com/f
ishaudio/fish-spee
ch?ref=archy.net 
Fun-CosyVoice 
3.0: 
https://github.com/
Rantai Failover 
Audio: Fish 
Speech Drama 3 
(MoE 35B-A3B, 16 
pembicara, 
15.000+ tag 
emosi/menyanyi, 
RTF 0,195) 
\rightarrow 
Fun-CosyVoice 3.0 
(streaming vLLM 
0.11.x+ & gRPC) 
\rightarrow F5-TTS 
(Flow Matching 
non-autoregresif di 
.safetensors) 
\rightarrow 
Memberikan 
redundansi penuh 
dari kloning suara 
studio beremosi 
kompleks hingga 
sintesis dialogis 
cepat pada 
perangkat keras 
terbatas (F5-TTS 
mendukung papan 
komputasi NPU 6 
TOPS FP16). 



<!-- [ID:02_CORE_AI_S273] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 253

No 
Nama Sumber & 
Modalitas 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis, 
Kebutuhan VRAM 
& Peran Failover 
QwenAudio/CosyV
oice F5-TTS 
Weights: 
https://huggingface
.co/SWivid/F5-TTS 
F5-TTS Edge 
Forum: 
https://huggingface
.co/SWivid/F5-TTS
/discussions Emilia 
Dataset: 
https://huggingface
.co/datasets/amphi
on/Emilia-Dataset 
ChatTTS: 
https://huggingface
.co/2Noise/ChatTT
S 
ChatTTS 
\rightarrow 
Kokoro-82M. 
1D. Agregator API, Smart Router, Semantic Cache, Abliteration Toolkit & Pemindai 
Malware (Open-Source Lokal) 
Sub-kategori 1D menggabungkan seluruh 43 perkakas infrastruktur dari LINK SUMBER.pdf 
dengan Valkey/RedisVL, Langfuse, dan NVIDIA NeMo Guardrails dari Link_daftar_vps 
server.txt, serta menambahkan Portkey-AI/gateway (gerbang TypeScript ultra-cepat yang 
merutekan ke 1.600+ LLM dengan 50+ guardrails bawaan), lemonade-server.ai, dan direktori 
pemantau kuota API waktu nyata cheahjs/free-llm-api-resources. Keberadaan banyak 
gerbang mandiri ini memastikan bahwa apabila satu proses gateway mengalami gangguan 
(seperti masalah konversi antarmuka pada new-api#6352 atau kondisi balapan kuota TOCTOU 
pada one-api#2440), lalu lintas langsung dialihkan ke Portkey-AI/gateway atau BerriAI/litellm. 
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
Spesifikasi Teknis 
& Peran dalam 
Rantai Failover 
1D.1 
Agregator Titik 
Akhir Gratis & 
Konverter Klien 
OmniRoute (359 
Penyedia, 150+ 
Gratis): 
https://github.com/
diegosouzapw/Om
niRoute 
FreeLLMAPI (34 
Penyedia, 635 
Endpoint): 
https://github.com/t
Live Free API 
Tracker: 
https://github.com/
cheahjs/free-llm-a
pi-resources 
Awesome Free 
Models: 
https://github.com/
12britz/awesome-f
ree-models 
OmniRoute 
(1.200+ model) 
dan freellmapi (7,4 
miliar token/bulan) 
menyatukan 
ratusan kuota 
gratis di balik satu 
titik akhir /v1. 
9router, 
AIClient2API, dan 



<!-- [ID:02_CORE_AI_S274] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 254

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
Spesifikasi Teknis 
& Peran dalam 
Rantai Failover 
ashfeenahmed/fre
ellmapi 9Router 
(Jembatan Koding 
Tanpa Batas): 
https://github.com/
decolua/9router 
AIClient2API: 
https://github.com/j
ustlovemaki/AIClie
nt2API EchoBird 
(Router Rust): 
https://github.com/
edison7009/EchoB
ird 
Reputation 
Auditor: 
https://freeairouter.
com/ 
EchoBird 
mengonversi klien 
CLI (Claude Code, 
Codex, Kiro, 
Antigravity, Grok) 
menjadi API lokal. 
1D.2 
Enterprise 
Self-Hosted API 
Gateways 
(One-API, 
New-API, LiteLLM, 
Portkey) 
One-API: 
https://github.com/
songquanpeng/on
e-api One-API 
Releases: 
https://github.com/
songquanpeng/on
e-api/releases 
One-API Charity 
Stations (公益站): 
https://github.com/
songquanpeng/on
e-api/issues 
New-API 
Container: 
https://github.com/
users/Calcium-Ion/
packages/containe
r/new-api/3539675
21?tag=v0.4.7.0 
New-API Horizon: 
https://github.com/
Calcium-Ion/new-a
pi-horizon Horizon 
Releases: 
https://github.com/
Calcium-Ion/new-a
pi-horizon/releases 
Horizon 
Portkey AI 
Gateway (Utama): 
https://github.com/
Portkey-AI/gatewa
y (npx 
@portkey-ai/gatew
ay) Portkey Fork: 
https://github.com/
stardog-union/port
key-ai-gateway 
Portkey Vigilnz 
Security Plugin: 
https://github.com/
Portkey-AI/gatewa
y/issues/1766 
Portkey 
Architecture 
Discussion: 
https://github.com/
Portkey-AI/gatewa
y/discussions/1576 
New-API Horizon 
memangkas 50% 
beban CPU/RAM 
pada konkurensi 
ekstrem dan +5% 
via optimasi SSE. 
Portkey-AI/gatewa
y menambahkan 
dukungan rute ke 
1.600+ LLM dan 
50+ guardrails 
dengan konfigurasi 
deklaratif JSON 
untuk automatic 
retries dan 
conditional 
fallbacks. 



<!-- [ID:02_CORE_AI_S275] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 255

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
Spesifikasi Teknis 
& Peran dalam 
Rantai Failover 
Issues/SSE: 
https://github.com/
Calcium-Ion/new-a
pi-horizon/issues 
New-API Key Tool: 
https://github.com/
Calcium-Ion/new-a
pi-key-tool Bug 
Report #6352: 
https://github.com/
QuantumNous/ne
w-api/issues/6352 
LazyRouter: 
https://github.com/l
achlanchen/LazyR
outer LiteLLM: 
https://github.com/
BerriAI/litellm 
1D.3 
ML Smart 
Routers, 
Semantic Cache 
& MCP Gateways 
RouteLLM (UC 
Berkeley): 
https://github.com/l
m-sys/routellm 
RouteLLM Local 
Guide: 
https://github.com/l
m-sys/RouteLLM/b
lob/main/examples
/routing_to_local_
models.md 
LiteLLM+RouteLL
M: 
https://github.com/
BerriAI/litellm/disc
ussions/4753 
RouterBench: 
https://github.com/
withmartian/router
bench Weave-OS 
Router (<50ms 
Go): 
https://github.com/
weave-os/router 
ClawRouter (<1ms 
Spider Hybrid 
Cache Server 
(Rust): 
https://github.com/
spider-rs/hybrid_c
ache_server & 
https://github.com/
spider-rs/spider_re
mote_cache 
Auto-Updated LLM 
Capability Registry 
(Vision/Audio): 
https://github.com/
spider-rs/llm_mod
els 
redis-vl-python 
mencegat kueri 
berulang dalam 
~25ms melalui 
semantic cache 
sebelum 
menyentuh router. 
RouteLLM (\tau = 
0,11593), 
weave-os/router 
(<50ms), dan 
ClawRouter 
(<1ms) memilah 
instruksi mudah ke 
model lokal dan 
instruksi sulit ke 
model frontier, 
sementara 
Langfuse menjaga 
batas margin biaya 
75%. 



<!-- [ID:02_CORE_AI_S276] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 256

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
Spesifikasi Teknis 
& Peran dalam 
Rantai Failover 
Local): 
https://github.com/
BlockRunAI/ClawR
outer Bifrost (Go 
MCP Gateway): 
https://github.com/
maximhq/bifrost 
AgentGateway 
(Rust MCP): 
https://github.com/
agentgateway/age
ntgateway Tyk 
Gateway: 
https://github.com/
TykTechnologies/ty
k Open-Connector 
(1.500+ SaaS): 
https://github.com/
oomol-lab/open-co
nnector 
Context-Mode 
(Kompresi 98%): 
https://github.com/
mksglu/context-mo
de Valkey & 
RedisVL (Sumber 
3): 
https://github.com/
redis/redis-vl-pytho
n Langfuse 
Self-Hosted 
(Sumber 3): 
https://github.com/l
angfuse/langfuse 
1D.4 
Mesin Inferensi 
Lokal (C++, 
CUDA, ROCm, 
Apple Metal, 
Low-RAM) 
llama.cpp: 
https://github.com/
ggerganov/llama.c
pp 
(https://llama.app/i
nstall.sh) vLLM: 
https://github.com/
vllm-project/vllm 
Ollama: 
Lemonade Server: 
https://lemonade-s
erver.ai/ 
(lemonade pull 
<repo>) llama.cpp 
Pre-built Releases: 
https://github.com/
ggerganov/llama.c
pp/releases 
Menyediakan 
eksekusi lokal 
dengan biaya nol. 
Edge0 
memungkinkan 
streaming bobot 
model MoE 35B 
dari SSD hanya 
dalam 2,5 GB 



<!-- [ID:02_CORE_AI_S277] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 257

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
Spesifikasi Teknis 
& Peran dalam 
Rantai Failover 
https://github.com/
ollama/ollama 
SGLang: 
https://github.com/
sgl-project/sglang 
Edge0 (MoE 35B 
di 2,5 GB RAM): 
https://github.com/
Edge0-AI/Edge0 
RAM melalui 
prediksi aktivasi 
expert satu 
langkah di depan. 
1D.5 
Toolkit 
Abliteration 
(Penghapus 
Sensor Ruang 
Residual) 
Refusal Direction 
(Arditi et al.): 
https://github.com/
andyrdt/refusal_dir
ection FailSpy 
Abliterator: 
https://github.com/
FailSpy/abliterator 
spkgyk 
Abliteration: 
https://github.com/
spkgyk/abliteration 
jim-plus 
LLM-Abliteration 
(Sharded): 
https://github.com/j
im-plus/llm-ablitera
tion Orion-zhen 
Abliteration 
(CUDA/ROCm): 
https://github.com/
Orion-zhen/abliter
ation AIAnytime 
Ablate (Optuna 
KL): 
https://github.com/
AIAnytime/ablate 
Heretic v2.0 
(ARA): 
https://github.com/
p-e-w/heretic/issue
s/472 Math Docs: 
https://github.com/
danielsobrado/llm_
Huihui-AI 
Abliteration Audit 
& Procedure 
Guide: 
https://github.com/
adybag14-cyber/A
bliteration/blob/mai
n/docs/tools/huihui
-ai.md 
Mengimplementasi
kan ortogonalisasi 
bobot permanen, 
Biprojection 
(--projected), 
Norm-Preserving 
(--normpreserve), 
dan Subspace 
Ablation terpandu 
divergensi KL 
tanpa memerlukan 
TransformerLens. 



<!-- [ID:02_CORE_AI_S278] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 259

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
1E.1 
Stasiun Kerja 
Agen Otonom & 
Self-Evolving 
Harnesses 
OpenClaw (5.380 
Skills): 
https://github.com/
openclaw/opencla
w Nous Hermes 
Agent: 
https://github.com/
NousResearch/her
mes-agent 
HKUDS Nanobot: 
https://github.com/
HKUDS/nanobot 
HF Smolagents 
(~1.000 baris): 
https://github.com/
huggingface/smola
gents Aider: 
https://github.com/
Aider-AI/aider 
OpenHands CLI 
Harness (Sumber 
3): 
https://github.com/
All-Hands-AI/Open
Hands 
Hermes Install 
Script: 
https://hermes-age
nt.nousresearch.c
om/install.sh Pi 
Terminal Coding 
Agent: npm install 
-g 
@earendil-works/p
i-coding-agent 
Akash SDL Skill 
for Claude/Agents: 
https://github.com/
akash-network/aka
sh-skill 
OpenClaw, 
Hermes Agent, 
OpenHands, dan 
Pi dapat langsung 
diarahkan ke 
server lokal 
(http://127.0.0.1:80
80/v1) maupun 
router OmniRoute 
dan 9Router untuk 
eksekusi koding 
otonom tanpa 
henti. 
1E.2 
Pustaka 
Orkestrasi Agen 
Modular & Tata 
Kelola Runtime 
PydanticAI: 
https://github.com/
pydantic/pydantic-
ai Instructor: 
https://github.com/j
xnl/instructor 
LangGraph: 
https://github.com/l
angchain-ai/langgr
aph Rig (Rust): 
https://github.com/
0xPlaygrounds/rig 
Mastra (TS): 
https://github.com/
mastra-ai/mastra 
VoltAgent (TS): 
https://github.com/
voltagent/voltagent 
Digunakan secara 
berlapis: 
LangGraph 
sebagai supervisor 
hierarkis 7-node, 
PydanticAI + 
Instructor untuk 
jaminan skema 
JSON, dan 
Microsoft Agent 
Governance 
Toolkit untuk 
penegakan 
kebijakan 
deterministik 
OWASP Agentic 
Top 10. 
Menjamin keluaran 
agen selalu patuh 
pada skema tipe 
data (type-safe) 
dan setiap 
eksekusi kode 
terisolasi dengan 
hak akses 
minimum 
(least-privilege). 



<!-- [ID:02_CORE_AI_S279] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 265

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
data pada paket 
Experiment. 
token/bulan 
(~33,3 juta 
token/hari) pada 
laju 1 req/detik. 
Menjadi fallback 
volume utama. 
2A.3 
GroqCloud 
Console (Inferensi 
LPU Kecepatan 
Tinggi) 
Konsol: 
https://console.gro
q.com Direct Keys: 
https://console.gro
q.com/keys 
Catatan Audit 
Agustus 2026: 
Model 
llama-3.3-70b dan 
llama-3.1-8b telah 
dihapus dari tier 
gratis per 16 
Agustus 2026; 
gunakan endpoint 
/v1/models untuk 
menarik daftar 
model aktif 
(termasuk Whisper 
suara) secara 
dinamis. 
100% Tanpa 
Kartu. Batas laju 
30 RPM, 
1.000–14.400 
RPD, dan 
6.000–30.000 
TPM; tidak melatih 
data pengguna, 
sangat ideal untuk 
tugas latar 
belakang agen 
berkecepatan 
tinggi. 
2A.4 
OpenRouter 
(Gerbang Model 
:free & 
Auto-Router) 
Portal: 
https://openrouter.
ai Direct Keys: 
https://openrouter.
ai/settings/keys 
Solusi 
Anti-Delisting 
2026: Gunakan 
slug dinamis 
openrouter/free 
agar sistem 
merutekan 
otomatis ke model 
gratis yang sedang 
aktif, atau panggil 
meta-llama/llama-
3.3-70b-instruct:fre
e, 
qwen/qwen3-coder
:free (konteks 1M), 
dan 
openai/gpt-oss-12
0b:free. 
100% Tanpa 
Kartu. Kuota 20 
RPM dan 50 RPD 
tanpa saldo 
(meningkat 
permanen menjadi 
1.000 RPD jika 
pernah mengisi 
saldo $10 satu 
kali). 
2A.5 
NVIDIA NIM API 
Catalog (91 Model 
Frontier Gratis) 
Portal: 
https://build.nvidia.
com/ 
Syarat: Gabung 
NVIDIA Developer 
Program gratis via 
100% Tanpa 
Kartu. 
Menyediakan 



<!-- [ID:02_CORE_AI_S280] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 267

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
hanya 
membutuhkan 
email untuk 
membuka akses 
kuota koding 
Claude dan Kiro 
gratis di 9Router. 
2A.9 
Hugging Face 
Access Tokens & 
Inference 
Providers 
Token: 
https://huggingface
.co/settings/tokens 
Dapat digunakan 
untuk menarik 
model 
GGUF/Safetensor
s 
(Wan/Flux/Kokoro) 
sekaligus 
memanggil 
Hugging Face 
Inference 
Providers. 
100% Tanpa 
Kartu. 
Menyertakan 
kredit bulanan 
$0,10/bulan yang 
dapat dirutekan ke 
mitra (Cerebras, 
Groq, Together, 
Fireworks, Novita, 
Scaleway, Z.ai), 
setara ~590.000 
token output pada 
gpt-oss-120b. 
2A.10 
Cohere 
Dashboard & 
Chutes AI 
(Bittensor 
Serverless) 
Cohere: 
https://dashboard.
cohere.com 
Chutes AI: 
https://chutes.ai 
Dokumentasi API 
Chutes: 
https://docs.chutes
.ai/ 
100% Tanpa 
Kartu. Cohere 
menyediakan Trial 
API Key otomatis 
dengan kuota 
1.000 
panggilan/bulan, 
sedangkan Chutes 
AI menyajikan 
inferensi 
serverless 
berbiaya nol atau 
rendah di atas 
jaringan 



<!-- [ID:02_CORE_AI_S281] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 276

No 
Nama Protokol DePIN Tautan Repositori & 
Dokumentasi (Eksisting 
& Ekspansi Riset) 
Mekanisme Insentif, 
Rumus Skor & Peran 
dalam Ekosistem 
Docker): 
https://github.com/akas
h-network/console 
Agent SDL Generator 
Skill: 
https://github.com/akas
h-network/akash-skill 
Awesome Deployment 
Templates: 
https://github.com/akas
h-network/awesome-ak
ash Helm Charts & 
RPC Proxy: 
https://github.com/akas
h-network/helm-charts 
& 
https://github.com/akas
h-network/rpc-proxy 
Docs Architecture: 
https://akash.network/d
ocs/node-operators/arc
hitecture/ 
repositori akash-skill 
untuk menghasilkan 
berkas konfigurasi SDL 
secara otomatis dan 
men-deploy kontainer 
agregator ke jaringan 
Akash tanpa kartu 
kredit. 
Mekanika Matematika Perutean Pintar, Abliteration 
Bebas Malware, dan Evaluasi SOTA 
Keberhasilan operasional dari ratusan tautan di atas bergantung pada ketepatan matematis di 
tiga titik kendali: (1) algoritma perutean kueri yang menghemat kuota model frontier, (2) 
prosedur penghapusan sensor (abliteration) yang menjaga integritas kognitif model tanpa 
menyisipkan malware, dan (3) pemilihan model penalaran kompak yang mampu bersaing 
dengan model raksasa di perangkat keras lokal. 
Formulasi Keputusan Smart Router dan Ekonomi DePIN 
Ketika sebuah instruksi x masuk ke lapisan gateway, sistem terlebih dahulu memeriksa 
kecocokan semantik pada Valkey/RedisVL (semantic cache dengan latensi ~25 milidetik). 
Apabila terjadi cache miss, kueri diteruskan ke kerangka kerja lm-sys/RouteLLM yang 
memanfaatkan bobot faktorisasi matriks (routellm/mf_gpt4_augmented) hasil pelatihan pada 
data preferensi Chatbot Arena. Perute memproyeksikan representasi laten dari prompt x dan 
kapabilitas model untuk menghitung probabilitas kemenangan model kuat 
(\mathcal{M}_{\text{strong}}, seperti kuota gratis Gemini 3.5 Flash, Mistral Large, atau 
DeepSeek-R1 684B) terhadap model lemah atau lokal (\mathcal{M}_{\text{weak}}, seperti 
DeepSeek-R1-0528-Qwen3-8B atau Huihui-Qwen3.8-27B-abliterated di llama.cpp) 
menggunakan fungsi keputusan berambang batas \tau: 



<!-- [ID:02_CORE_AI_S282] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 289

                        headers=headers,​
                        json=payload​
                    )​
                    if resp.status_code == 200:​
                        data = resp.json()​
                        content = 
data["choices"][0]["message"]["content"]​
                        return {​
                            "provider_used": ep.name,​
                            "model_used": ep.default_model,​
                            "response": content​
                        }​
                    elif resp.status_code in (401, 402, 403, 404, 429, 
500, 502, 503, 504):​
                        # Aktifkan Circuit Breaker Cooldown selama 120 
detik untuk endpoint yang gagal​
                        ep.cooldown_until = time.time() + 120.0​
                        errors.append(f"{ep.name}: HTTP 
{resp.status_code}")​
                        continue​
                except Exception as exc:​
                    ep.cooldown_until = time.time() + 60.0​
                    errors.append(f"{ep.name}: {type(exc).__name__}")​
                    continue​
​
        raise RuntimeError(f"Seluruh jalur inferensi gagal dieksekusi. 
Rincian: {'; '.join(errors)}")​
 
4. Matriks Aturan Failover Multimodal, Database, dan Pembayaran 
untuk Agen AI 
Selain inferensi teks dan perayapan web, agen pemrograman wajib mengimplementasikan 
rantai pengalihan yang sama pada lapisan sintesis media, penyimpanan status, dan kasir 
pembayaran otomatis menggunakan aturan deterministik berikut: 
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
Sintesis Suara 
(TTS) & Voice 
Cloning 
fishaudio/fish-spee
ch (S2-Pro 4B / 
Drama 3 MoE 
35B-A3B via 
SGLang-Omni) 
QwenAudio/CosyV
oice 
(Fun-CosyVoice 
3.0 via vLLM 
0.11.x+) atau 
SWivid/F5-TTS 
hexgrad/Kokoro-8
2M (CPU 
Apache-2.0) 
\rightarrow 
OHF-Voice/piper1-
gpl / 
k2-fsa/sherpa-onn
x (C++ ONNX) 
Latensi TTFA > 
500ms, kehabisan 
VRAM GPU lokal, 
atau kegagalan 
daemon PyTorch. 



<!-- [ID:02_CORE_AI_S283] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 291

penyedia hulu menutup layanannya secara mendadak. 
Pada saat yang sama, kemandirian kognitif dan kepatuhan instruksi penuh kini dapat 
diwujudkan secara lokal melalui perpaduan antara model penalaran hasil distilasi kompak dan 
teknik abliteration selektif. Ketersediaan model DeepSeek-R1-0528-Qwen3-8B yang mencetak 
akurasi 86,0% pada tolok ukur AIME 2024 serta keluarga model tanpa sensor dari 
huihui-ai—seperti Huihui-Qwen3.8-27B-abliterated-GGUF dan 
Huihui-Qwen3.6-35B-A3B-abliterated yang mengablasi lapisan tengah-akhir secara selektif 
tanpa merusak lapisan awal maupun modul visual—memungkinkan mesin inferensi lokal 
(llama.cpp, vLLM, Ollama, atau Edge0 pada RAM 2,5 GB) mengambil alih lebih dari 50% beban 
kerja harian melalui pemilahan otomatis RouteLLM pada ambang batas \tau = 0,11593. 
Penegakan wajib terhadap format tensor nir-eksekusi (.safetensors dan .gguf) yang 
dikombinasikan dengan pemindaian statis protectai/modelscan serta tata kelola runtime 
Microsoft Agent Governance Toolkit menjamin bahwa kebebasan eksplorasi tanpa sensor 
tersebut sepenuhnya terlindung dari ancaman penyusupan malware serialisasi pickle maupun 
eksekusi perintah destruktif. 
Sebagai fondasi keberlanjutan jangka panjang, integrasi antara ketahanan akuisisi data web 
dan siklus ekonomi mandiri (self-sustaining compute loop) memastikan agregator mampu 
mendanai ekspansi perangkat kerasnya sendiri secara otonom. Menggantikan perayap web 
tunggal dengan rantai pengalihan spider-rs/spider \rightarrow D4Vinci/Scrapling (scrapling-rs) 
\rightarrow Crawl4AI (terisolasi secara internal) yang disuplai oleh lebih dari 15 umpan proksi 
multi-CDN (TheSpeedX, proxifly, monosans, jetkai, roosterkid, jhao104/proxy_pool) 
menghilangkan risiko kegagalan ekstraksi data akibat perubahan struktur DOM maupun 
proteksi Cloudflare Turnstile. Di hilir, perpaduan antara gerbang pembayaran tanpa kartu Visa 
(Pakasir \rightarrow Tripay \rightarrow Duitku \rightarrow @CryptoBot USDT) untuk membiayai 
pengisian saldo API grosir berbasis kripto (Novita AI, RunPod, Vast.ai, PiAPI) dan partisipasi 
perangkat keras menganggur pada jaringan DePIN (Bittensor Subnet 27, Nosana, IO.net, dan 
Akash Network) menutup siklus operasional sehingga seluruh ekosistem dapat tumbuh tanpa 
ketergantungan modal eksternal. 
Karya yang dikutip 
1. Free LLM APIs: No Credit Card, Verified Each Release, 
https://klymentiev.com/blog/free-llm-api 2. Free LLM API list. Permanent free tiers only. : 
r/better_claw - Reddit, 
https://www.reddit.com/r/better_claw/comments/1vef1nz/free_llm_api_list_permanent_free_tiers
_only/ 3. Free LLM APIs Compared: Rate Limits, Models, and Real Costs (2026), 
https://openrouter.ai/blog/tutorials/free-llm-apis-compared/ 4. 
Proxy-Grabber-and-Checker/Sources.txt at main - GitHub, 
https://github.com/saschazesiger/Proxy-Grabber-and-Checker/blob/main/Sources.txt 5. 
getproxy/start.sh at master - GitHub, https://github.com/noctiro/getproxy/blob/master/start.sh 6. 
huihui-ai/Huihui-Qwen3.8-27B-abliterated - Hugging Face, 
https://huggingface.co/huihui-ai/Huihui-Qwen3.8-27B-abliterated 7. gpt-oss-abliterated - a 
huihui-ai Collection - Hugging Face, 
https://huggingface.co/collections/huihui-ai/gpt-oss-abliterated 8. spider-rs/spider: Foundational 
low latency web data collecting in Rust, https://github.com/spider-rs/spider 9. 
huihui-ai/Huihui-Qwen3.8-Flash-Next-abliterated-v2-GGUF, 
https://huggingface.co/huihui-ai/Huihui-Qwen3.8-Flash-Next-abliterated-v2-GGUF 10. 
pchide/Proxy-List-Live - GitHub, https://github.com/pchide/Proxy-List-Live 11. 



<!-- [ID:02_CORE_AI_S284] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 301

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
yang telah melampaui 2,2 juta unduhan pada Oktober 2026. Keunggulan utama huihui-ai 
adalah kecepatan adaptasinya terhadap rilis model terbaru (mencakup keluarga Qwen3.8, 
Qwen3.6, Gemma-4, GLM-5.3, DeepSeek-V4, dan GPT-OSS) serta penerapan abliteration 
selektif pada lapisan tengah-akhir—misalnya hanya mengablasi lapisan 18 hingga 51 pada 
Huihui-Qwen3.8-27B-abliterated sambil mempertahankan 15 lapisan pertama, modul 
Multi-Token Prediction (MTP), dan proyeksi visual tetap utuh—sehingga menghilangkan 
mekanisme penolakan (refusal) tanpa mengorbankan kecerdasan penalaran maupun 
kapabilitas multimodal (Vision-Language). 
No 
Nama Sumber & 
Keluarga Model 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis, 
Format & Peran 
Failover 
1B.1 
Keluarga Qwen3 
& Qwen3.8 
Qwen3-8B 
(Bartowski): 
Creator Hub: 
https://huggingface
Kuantisasi GGUF 
dari 2-bit (IQ2_M 



<!-- [ID:02_CORE_AI_S285] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 304

No 
Nama Sumber & 
Keluarga Model 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis, 
Format & Peran 
Failover 
.co/huihui-ai/Huihu
i-Qwen3-Coder-Ne
xt-abliterated 
CyberStrike-OffSe
c-35B: 
https://huggingface
.co/huihui-ai/Huihu
i-CyberStrike-OffS
ec-35B-abliterated 
Qwythos-9B-1M 
Context: 
https://huggingface
.co/huihui-ai/Huihu
i-Qwythos-9B-Clau
de-Mythos-5-1M-a
bliterated-GGUF 
1B.4 
Keluarga 
Penalaran SOTA 
DeepSeek-R1 & 
V3 
R1-0528-Qwen3-8
B: 
https://huggingface
.co/deepseek-ai/D
eepSeek-R1-0528-
Qwen3-8B R1 
GGUF (Unsloth): 
https://huggingface
.co/unsloth/DeepS
eek-R1-GGUF 
R1-0528 (684B 
Full): 
https://huggingface
.co/deepseek-ai/D
eepSeek-R1-0528 
R1-Distill-Qwen-32
B: 
https://huggingface
.co/deepseek-ai/D
eepSeek-R1-Distill
-Qwen-32B 
V3-Base: 
https://huggingface
.co/deepseek-ai/D
eepSeek-V3-Base 
Huihui 
Qwen3.5-4B-Clau
de-4.6-Opus 
Reasoning Distill: 
https://huggingface
.co/huihui-ai/Huihu
i-Qwen3.5-4B-Cla
ude-4.6-Opus-ablit
erated 
Llama-3.2-3B-Instr
uct Abliterated: 
https://huggingface
.co/huihui-ai/Llama
-3.2-3B-Instruct-ab
literated 
DeepSeek-R1-052
8-Qwen3-8B 
mencapai akurasi 
86,0% pada AIME 
2024, melampaui 
o3-mini (79,6%) 
dan 
Gemini-2.5-Flash-
Thinking (82,3%), 
sehingga menjadi 
worker penalaran 
lokal utama. 
1B.5 
Katalog 
Uncensored 
Katalog: 
https://huggingface
Digunakan 
sebagai jalur 
Berbeda dengan 
abliteration yang 



<!-- [ID:02_CORE_AI_S286] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 305

No 
Nama Sumber & 
Keluarga Model 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis, 
Format & Peran 
Failover 
Berbasis Dataset 
Dolphin 
(Retraining-Based) 
.co/models?datase
t=dataset:cognitive
computations/dolp
hin 
Dolphin-2.9-Llama
3-8B: 
https://huggingface
.co/cognitivecomp
utations/dolphin-2.
9-llama3-8b 
Dolphin-2.7-Mixtral
-8x7B-4bit (Apple 
MLX): 
https://huggingface
.co/mlx-community
/dolphin-2.7-mixtra
l-8x7b-4bit 
alternatif apabila 
tugas agen 
membutuhkan 
gaya percakapan 
yang dilatih ulang 
secara penuh 
pada dataset 
tanpa filter 
(fine-tuned) 
dibandingkan 
penyuntingan 
bobot 
(abliteration). 
memodifikasi 
matriks bobot 
secara bedah 
vektor, keluarga 
Dolphin melatih 
ulang model pada 
korpus instruksi 
bersih tanpa 
penolakan. 
1B.6 
Model Dasar 
Qwen, Bobot 
Router & Dataset 
Kalibrasi 
Abliteration 
Qwen3.5-4B: 
https://huggingface
.co/Qwen/Qwen3.
5-4B 
Qwen2.5-1.5B-Inst
ruct: 
https://huggingface
.co/Qwen/Qwen2.
5-1.5B-Instruct 
Qwen3-8B-Base: 
https://huggingface
.co/Qwen/Qwen3-
8B-Base 
Qwen3-235B-A22
B: 
https://huggingface
.co/Qwen/Qwen3-
235B-A22B 
RouteLLM 
Weights: 
https://huggingface
.co/routellm/mf_gp
t4_augmented 
Semantic-Harmles
s: 
https://huggingface
Qwen3.8-27B 
Base: 
https://huggingface
.co/Qwen/Qwen3.
8-27B 
Qwen3.6-35B-A3B 
Base: 
https://huggingface
.co/Qwen/Qwen3.
6-35B-A3B 
Menyediakan 
model fondasi 
untuk eksperimen 
ablasi mandiri, 
bobot faktorisasi 
matriks untuk 
lm-sys/RouteLLM, 
serta pasangan 
dataset kalibrasi 
semantik yang 
terbukti menekan 
derau (noise) 
ruang residual 
hingga 
D_{\text{KL}} = 
0,0509. 


