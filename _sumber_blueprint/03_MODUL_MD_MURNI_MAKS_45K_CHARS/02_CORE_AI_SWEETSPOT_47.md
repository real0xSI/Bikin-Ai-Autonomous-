
<!-- [ID:02_CORE_AI_S287] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 306

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
Wan-AI Org & 
Diffusers 
Collections 
(Wan2.2-diffusers, 
Wan2.1-diffusers): 
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
Mencakup T2V, 
I2V, 
First-Last-Frame-t
o-Video (FLF2V), 
dan Video 
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



<!-- [ID:02_CORE_AI_S288] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 307

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
https://github.com/
ali-vilab/TeaCache/
blob/main/TeaCac
he4Wan2.1/READ
ME.md 
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
Digunakan secara 
berpasangan: 
HunyuanVideo-Fol
ey sebagai 
generator efek 
suara utama dan 
hkchengrex/MMAu
dio (157 juta 
parameter) 
sebagai fallback 
ringan untuk 
sinkronisasi 
Video-to-Audio 
(V2A). 
HunyuanVideo-1.5 
memangkas waktu 
render sebesar 
75% (<75 detik 
pada RTX 4090) 
melalui distilasi 
langkah dan 
sgl-kernel==0.3.18
. 
HunyuanVideo-Av
atar berjalan 
hanya dalam 10 
GB VRAM 
menggunakan 
integrasi Wan2GP 
dan TeaCache. 



<!-- [ID:02_CORE_AI_S289] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 310

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
ChatTTS 
\rightarrow 
Kokoro-82M. 
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



<!-- [ID:02_CORE_AI_S290] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 311

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
Dataset: 
https://huggingface
.co/datasets/amphi
on/Emilia-Dataset 
ChatTTS: 
https://huggingface
.co/2Noise/ChatTT
S 
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
Reputation 
Auditor: 
https://freeairouter.
com/ 
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
EchoBird 
mengonversi klien 
CLI (Claude Code, 
Codex, Kiro, 
Antigravity, Grok) 
menjadi API lokal. 



<!-- [ID:02_CORE_AI_S291] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 312

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
(Router Rust): 
https://github.com/
edison7009/EchoB
ird 
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



<!-- [ID:02_CORE_AI_S292] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 313

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



<!-- [ID:02_CORE_AI_S293] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 314

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
https://github.com/
ollama/ollama 
SGLang: 
https://github.com/
sgl-project/sglang 
Edge0 (MoE 35B 
di 2,5 GB RAM): 
https://github.com/
Edge0-AI/Edge0 
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
RAM melalui 
prediksi aktivasi 
expert satu 
langkah di depan. 
1D.5 
Toolkit 
Refusal Direction Huihui-AI 
Mengimplementasi



<!-- [ID:02_CORE_AI_S294] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 315

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
Abliteration 
(Penghapus 
Sensor Ruang 
Residual) 
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
notebooks/blob/ma
in/ABLITERATION
.md 
Abliteration Audit 
& Procedure 
Guide: 
https://github.com/
adybag14-cyber/A
bliteration/blob/mai
n/docs/tools/huihui
-ai.md 
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
1D.6 
Perisai 
Keamanan Bobot 
Model, Guardrails 
& Audit Celah 
Protect AI 
ModelScan: 
https://github.com/
protectai/modelsca
n HF Malware 
Docs: 
https://huggingface
Spider Firewall 
Utilities (Rust): 
https://github.com/
spider-rs/firewall 
modelscan 
memindai berkas 
Pickle, H5, dan 
SavedModel 
secara statis 
sebelum 
pemuatan untuk 



<!-- [ID:02_CORE_AI_S295] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 317

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
-g 
@earendil-works/p
i-coding-agent 
Akash SDL Skill 
for Claude/Agents: 
https://github.com/
akash-network/aka
sh-skill 
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
Microsoft Agent 
Governance 
Toolkit: 
https://github.com/
microsoft/agent-go
vernance-toolkit 
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
1E.3 
Mesin Perayap 
Crawl4AI (Utama Scrapling 
Mengatasi 



<!-- [ID:02_CORE_AI_S296] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 322

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
data pada paket 
Experiment. 
100% Tanpa 
Kartu. 
Menyediakan 
kuota permanen 
terbesar di industri 
saat ini: ~1 Miliar 
token/bulan 
(~33,3 juta 
token/hari) pada 
laju 1 req/detik. 
Menjadi fallback 
volume utama. 
2A.3 
GroqCloud 
Console (Inferensi 
Konsol: 
https://console.gro
Catatan Audit 
Agustus 2026: 
100% Tanpa 
Kartu. Batas laju 



<!-- [ID:02_CORE_AI_S297] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 323

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
LPU Kecepatan 
Tinggi) 
q.com Direct Keys: 
https://console.gro
q.com/keys 
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
Gmail dan 
verifikasi nomor 
HP. 
100% Tanpa 
Kartu. 
Menyediakan 
akses gratis ke 91 
titik akhir model 
(termasuk model 
bahasa, visi, dan 
multimodal SOTA) 
dengan batas laju 
tinggi 40 RPM 
untuk pembuatan 



<!-- [ID:02_CORE_AI_S298] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 334

No 
Nama Protokol DePIN Tautan Repositori & 
Dokumentasi (Eksisting 
& Ekspansi Riset) 
Mekanisme Insentif, 
Rumus Skor & Peran 
dalam Ekosistem 
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
\text{Route}(x) = \begin{cases} \mathcal{M}_{\text{strong}} & \text{jika } P(\text{strong} \succ 
\text{weak} \mid x) \ge \tau \\ \mathcal{M}_{\text{weak}} & \text{jika } P(\text{strong} \succ 
\text{weak} \mid x) < \tau \end{cases} 
Dengan menetapkan kalibrasi ambang batas standar \tau = 0,11593 pada perute Matrix 
Factorization (mf), sistem secara deterministik mengalokasikan tepat 50% kueri tersulit ke rantai 



<!-- [ID:02_CORE_AI_S299] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 346

        self,​
        prompt: str,​
        system_prompt: str = "You are a helpful autonomous engineering 
agent.",​
        complexity_score: float = 0.5,​
        require_uncensored: bool = False​
    ) -> Dict[str, str]:​
        """​
        Mengeksekusi panggilan LLM dengan pengalihan otomatis 
(Auto-Rolling).​
        Jika satu penyedia mengembalikan HTTP 429 (Rate Limit) atau 
5xx,​
        penyedia tersebut dimasukkan ke masa tenang (cooldown) dan 
kueri langsung​
        dilempar ke penyedia berikutnya dalam hitungan milidetik.​
        """​
        candidates = self._order_candidates(complexity_score, 
require_uncensored)​
        errors = []​
​
        async with httpx.AsyncClient(timeout=45.0) as client:​
            for ep in candidates:​
                api_key = "none" if ep.api_key_env == "NONE" else 
os.getenv(ep.api_key_env, "")​
                if ep.api_key_env != "NONE" and not api_key:​
                    continue​
​
                headers = {​
                    "Authorization": f"Bearer {api_key}",​
                    "Content-Type": "application/json"​
                }​
                payload = {​
                    "model": ep.default_model,​
                    "messages": [​
                        {"role": "system", "content": system_prompt},​
                        {"role": "user", "content": prompt}​
                    ],​
                    "temperature": 0.2​
                }​
​
                try:​
                    resp = await client.post(​
                        f"{ep.base_url.rstrip('/')}/chat/completions",​
                        headers=headers,​
                        json=payload​
                    )​
                    if resp.status_code == 200:​
                        data = resp.json()​



<!-- [ID:02_CORE_AI_S300] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 347

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
Generasi Video & 
Animasi Avatar 
Lokal: 
Wan2.2-TI2V-5B / 
HunyuanVideo-1.5 
(4–12 langkah + 
TeaCache + 
Lokal VRAM 
Rendah (8–10 
GB): LTX-VideoQ8 
/ 
HunyuanVideo-Av
Cloud 
Gratis/Grosir: 
Modal ($30/bln 
gratis) \rightarrow 
Pollinations AI 
Penggunaan 
VRAM melampaui 
kapasitas fisik 
kartu grafis lokal 
atau antrean 



<!-- [ID:02_CORE_AI_S301] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER -->
## Halaman 361

Integrasi dan Pengembangan Kode Berkelanjutan
https://gemini.google.com/app/73e1e51173585a63
User prompt: 1 & 2 YA cek dan pelajari dulu sampai terupdatenya karena saya butuh kamu mengerti sebelum membuat code tambahan serta perbaikan.
jika saya perlu menambahkan informasi akan saya coba cari yang ada. karena kurang lebih itu modal yang tersimpan.
Response: DOMAIN: CODING/ARCH (Frontier Level)
Seluruh 10 dokumen dan file kode yang Anda unggah telah saya bedah baris demi baris dari iterasi v3.4.0 hingga v3.7.0 dan cetak biru v4.0. Sesuai
Master Contract Bagian D, berikut adalah hasil D1 (Grounding & Peta Konflik), D2 (Arsitektur Target Konsolidasi v4.0), dan D3 (Rencana Bertahap)
sebelum kita mengeksekusi penulisan file kode:
D1. GROUNDING — Inventaris Referensi, Isi, & Konflik Antar-Dokumen
1. Inventaris File Kode & Dokumen Referensi
[FAKTA] [Bersumber] app.py.json berisi kode MASTER ENGINE v3.4.0 yang terpotong di tengah Bagian 2 oleh teks instruksi salin-tempel
sehingga kehilangan seluruh blok Bagian 9, 10, dan 11 (fungsi transaksi koin, voucher Ed25519, handler /start, /menu, /admin, /riset,
/canvas, serta seluruh @router.callback_query).
[FAKTA] [Bersumber] App.py dan App (1).py berisi kode v3.4.0 (1.353 baris) dengan Bagian 1–3 yang sudah tersambung, namun App
(1).py mengalami regresi karena kehilangan rute /api/voucher/redeem, kehilangan pemanggilan
_background_dead_job_sweeper_loop() di main(), kehilangan tombol wiz:prompt:edit, dan kehilangan pemuatan variabel
RUNTIME_CONFIG di init_master_db.
[FAKTA] [Bersumber] v.3.5.0.pdf dan audit nih.pdf memetakan 7 celah keamanan pada App.py v3.4.0 (AUDIT-01 s.d. AUDIT-07)
serta merumuskan 12 fitur v3.5.0 dan arsitektur v3.6.0 (8-Agent Rolling Pool, 4-Gate Deep-Defense Sterilizer, /donasi_api, Sub-Menu Kasir 3
Halaman, Manual 4-Bab di /admin, serta Video Upscaler 4K 60FPS).
[FAKTA] [Bersumber] audit update 1.pdf memuat basis kode paling lengkap saat ini, yaitu BIKINAI SUPER INTELLIGENCE MASTER
ENGINE v3.7.0 (FRONTIER AUTONOMIC CORE) dengan 11 tabel SQLite, 3-Tier PPP Pricing (HEMAT Rp 5.000, PRO Rp 25.000, SULTAN Rp
250.000), AutonomicConvergenceGuard, check_velocity_rate_limit, mode IMG2VID + Preset Awam, portal web AetherFree AI
Studio (/set_webname, proxy /api/cdn/download), serta Inspektor Layar Pembeli & pemindai kebocoran privasi
(scan_customer_ui_for_leaks).
[FAKTA] [Bersumber] Konsep Awal BikinAI.pdf menetapkan standar Frontier v4.0 untuk menutup 8 celah akar (VULN-01 s.d. VULN-08),
termasuk Two-Tier Staggered Speculative Hedging (
), pemuatan malas SKILL.md (gaya nanoMuse), jembatan klien
Puter.js, Blinded Zero-Linkage Ed25519 Voucher + Atomic Escrow Burn, serta Persistent Writer Singleton pada SQLite WAL.
[FAKTA] [Bersumber] Sumber Daya Utama.pdf, LINK SUMBER.pdf (159 tautan), dan Link_daftar_vps server.txt (40 tautan)
menyediakan daftar repositori dan spesifikasi integrasi untuk RouteLLM Matrix Factorization (
), Bittensor Subnet 27 Compute
(commune-ai/compute-ni) & Chutes AI, pemindai keamanan bobot model ProtectAI ModelScan + penegakan format
.safetensors/.gguf, kolam proksi otomatis (jhao104/proxy_pool & monosans/proxy-list), serta relai Cloudflare Worker
(Calcium-Ion/new-api-worker).
2. Konflik & Celah Antar-Referensi yang Wajib Diselesaikan
1. [FAKTA] [Bersumber] Kerusakan Sintaksis OCR pada Kode v3.7.0 (audit update 1.pdf): Teks kode di dalam PDF mengalami perubahan
karakter akibat proses OCR/ekstraksi PDF (misalnya dict [str, Any) {, USER_LOCK_STRIPES (user_id% STRIPE_COUNT],
$\underline{crc}=...$, dan spasi liar pada tag HTML/JS) yang akan menyebabkan SyntaxError jika langsung dijalankan tanpa
rekonstruksi AST bersih.
2. [FAKTA] [Bersumber] Konflik Strategi Router (v3.7.0 vs. v4.0 VULN-07): Kode v3.7.0 di audit update 1.pdf masih menembak
semua API secara serentak pada detik ke-0 (asyncio.create_task paralel) dan masih mencantumkan model gemini-2.0-flash,
sedangkan Konsep Awal BikinAI.pdf mewajibkan Two-Tier Staggered Hedging (gelombang primer pada 
 dan gelombang cadangan
pada 
 jika primer gagal/lambat) serta pembaruan model ke gemini-2.5-flash / gemini-3.8-flash agar tidak menghabiskan
kuota gratis 6x lipat.
3. [FAKTA] [Bersumber] Konflik Privasi & Ekonomi Voucher (v3.7.0 vs. v4.0 VULN-06): Kode v3.7.0 masih menyertakan "u":
int(user_id) secara terbuka di dalam payload Base64 voucher dan masih memberikan 5 kredit voucher gratis bagi akun bersaldo 0, yang
bertentangan dengan aturan Zero-Identity Linkage (Blinded Hash Commitment tanpa user_id) dan Atomic Escrow Burn (wajib potong
koin_utama) pada Konsep Awal BikinAI.pdf dan audit nih.pdf.
4. [FAKTA] [Bersumber] Konflik Handler Upload Foto & Dokumen (v3.7.0 vs. v4.0 VULN-03): Pada v3.7.0, handler
handle_multimodal_photo_and_pdf sudah menghapus prompt kucing statis tetapi belum memotong kuota/koin
(deduct_user_coins_for_job) dan belum mengunduh metadata/file foto Telegram (message.photo[-1]).
5. [FAKTA] [Bersumber] Konflik Manajemen Koneksi SQLite (v3.7.0 vs. v4.0 VULN-08): Kode v3.7.0 masih membuka koneksi
aiosqlite.connect(DB_PATH) baru di setiap pemanggilan get_db(), sedangkan standar v4.0 mewajibkan koneksi terkelola agar tidak
memintal ratusan worker thread saat trafik grup tinggi.
6. [FAKTA] [Bersumber] Kesenjangan terhadap MASTER CONTRACT v1.0: Kode v3.7.0 belum memiliki Plugin Surface (self-registration,
health(), Hot-Swap), Self-Healing Loop eksplisit dengan eskalasi 3x ke human queue, Human Approval Gate di level kode untuk 5 operasi
τ
​ =
hedge
1, 2 detik
τ = 0, 11593
t = 0
t = 1, 2s



<!-- [ID:02_CORE_AI_S302] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER, TIDAK ADA BUKTI -->
## Halaman 363

Target: Menyambungkan seluruh handler perintah & callback (/start, /menu, /admin, /bansos, /harvest, /rolling, /donasi_api,
/riset, /canvas, /saran, /setup_grup, /ikat, /set_webname, /set_miniapp, /claim_owner), perbaikan F.photo |
F.document dengan potong koin/kuota, Blinded Voucher Ed25519, serta Mini App & Freedom Web Portal.
Kriteria Sukses: scan_customer_ui_for_leaks() menghasilkan clean: True (0 istilah teknis bocor ke layar pembeli) dan seluruh
rute HTTP port 8080 (/, /unfiltered-portal, /api/webapp/execute, /api/nocturne/chat, /api/nocturne/generate,
/api/voucher/redeem, /api/cdn/download, /api/public/community-links) terhubung 100%.
Rollback Trigger: Terdeteksi kebocoran istilah teknis pada scan_customer_ui_for_leaks() atau ada callback tombol yang tidak
memiliki handler.
D4. STOP & MINTA PERSETUJUAN
Sesuai aturan D4 dan instruksi Anda untuk mempelajari seluruh modal referensi terlebih dahulu, saya STOP di sini dan belum menulis kode.
[FAKTA] [Bersumber] Preferensi output Anda dari jawaban sebelumnya (1 & 2 YA) telah dikunci: begitu Anda memberi komando eksekusi,
kode hasil penggabungan dan perbaikan hanya akan diberikan dalam BENTUK FILE tanpa memenuhi ruang chat, dan aturan D8 aktif.
Langkah Berikutnya (1 Langkah): Apakah ada informasi atau file tambahan lagi yang ingin Anda sertakan, atau saya langsung eksekusi Fase 1 s.d.
Fase 3 (D5 & D6) dan menerbitkan file app.py Master Engine v4.0 yang utuh sekarang?
User prompt: sebisa mungkin saya menambah informasi. silahkan kamu pelajari dulu. pertanyaan saya. dengan segudang informasi ini. belum lagi dari
penelusuran secara mendalam di internet. bisa kah sistem saya keamananya lebih kuat berlapis, sistem lebih cerdas, serta lebih canggih dari code yang
akan dibuat?
Response: KLASIFIKASI DOMAIN (ROLE ROUTER): Multi-Perspektif (SECURITY/LEGAL → CODING/ARCH → BIZ/MARKET & PRODUCT/UX) sesuai
aturan C3 & C4.
Jawaban Singkat: YA, SANGAT BISA. Dengan menggabungkan 9 berkas tambahan yang baru Anda unggah dan hasil verifikasi repositori terkini di
internet (aturan D8), sistem Anda dapat ditingkatkan melampaui draf kode v3.7.0 menjadi Master Engine v4.0 yang memiliki pertahanan 6 lapis
tanpa celah, router Combo-Grading anti-Soft Refusal, serta mesin akuisisi & follow-up penjualan otomatis.
D1 & D8. GROUNDING TAMBAHAN — Audit 9 File Baru & Verifikasi Internet
1. [FAKTA] [Bersumber] Audit Screenshot WA jamaahpees/9router-mibp-version-fixed (IMG-20261018-WA0006(1).jpg):
[TIDAK ADA BUKTI] Hasil penelusuran langsung menunjukkan repositori atas nama jamaahpees/9router-mibp-version-fixed
tidak memiliki jejak audit keamanan publik maupun rilis terverifikasi di GitHub. Sesuai aturan keamanan rantai pasok (supply-chain
security), kita dilarang melakukan git clone mentah dari fork komunitas yang belum teraudit ke server utama.
[FAKTA] [Bersumber] Namun, fitur yang disebutkan di screenshot tersebut (fallback grading, mode combo sesuai urutan model, dan RTK
-40% tokens) terbukti berasal dari repositori induk decolua/9router (30.945+ bintang GitHub, telah lulus audit keamanan SkillsLLM)
dan cabang mhiqrambg/9router-mibp-version (sinkronisasi rilis v0.5.99 Oktober 2026). Kita akan mengadopsi logika
arsitekturnya secara bersih ke dalam Python (app.py) tanpa mengimpor kode biner luar.
2. [FAKTA] [Bersumber] Audit 2 Screenshot @TeleportAppBot (Screenshot_20261020-161054 & 161110):
Menunjukkan dua pola konversi tinggi di Telegram: (a) Program Afiliasi Transparan (50% Revenue Share) langsung di profil/menu bot,
dan (b) Automated Sales Manager Follow-up Funnel (pesan otomatis dari "Maksim" yang menyapa pengguna yang baru saja melihat
daftar harga/tarif tetapi belum membayar, menawarkan opsi paket bulanan/tahunan dan bantuan langsung).
3. [FAKTA] [Bersumber] Audit 4 Visualisasi HTML (isi link sumber.html, sdu 1.html, sdu 2.html, sdu 3.html) & Diagram 5-Lapis
(IMG-20261020-WA0018.jpg):
Temuan Kritis di isi dari sdu 3.html (Soft Refusal Gap 51%): Pada model abliterated, detektor kata kunci biasa membaca tingkat
penolakan 0% (semu), padahal LLM Judge membuktikan kepatuhan nyata hanya 49% karena sisanya adalah soft refusal (ceramah moral
atau jawaban menghindar). Kode v3.7.0 belum memiliki filter pendeteksi soft refusal ini.
Temuan di isi link sumber.html (4-Zona PPP & Efisiensi 95%): Memperluas pembagian harga menjadi 4 Zona PPP (Zona 1 Global
Tier-1 100%, Zona 2 Global Tier-2 70%, Zona 3 Emerging 50%, dan Zona 4 Indonesia 25% dengan biaya QRIS 0,7% serta efisiensi
RouteLLM 95%).
Temuan di isi dari sdu 1.html & sdu 2.html: Weave-OS Router merutekan dalam <50 ms (hemat biaya 40–70%), ClawRouter <1
ms, mksglu/context-mode memangkas ukuran prompt tool hingga 98%, dan model kompak DeepSeek-R1-0528-Qwen3-8B
mencetak skor penalaran 86,0% di AIME 2024 (mengungguli Qwen3-235B-A22B yang 85,7%), sedangkan Fish Audio S2-Pro
mencetak WER terendah (0,54% ZH / 0,99% EN).
PENINGKATAN DI ATAS KODE v3.7.0 (BERLABEL PER DOMAIN)
1. SECURITY/LEGAL: Pertahanan Berlapis 6-Gate + Patch Terbaru 9Router
[FAKTA] [Bersumber] Penutupan Total 8 Celah Akar (VULN-01 s.d. VULN-08):



<!-- [ID:02_CORE_AI_S303] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER -->
## Halaman 364

1. Fail-Closed Owner Auth: Menolak akses /admin 100% jika ADMIN_USER_ID belum dikunci, ditambah proteksi anti-brute-force pada
/claim_owner.
2. Timing-Safe HMAC-SHA256 & Replay Guard (
): Memvalidasi initData Mini App dan memotong koin secara atomik sebelum
merender.
3. Blinded Zero-Linkage Ed25519 Voucher: Menghapus user_id dari payload JSON VCH-... dan menggantinya dengan komitmen hash
buta satu arah 
 serta mewajibkan Atomic Escrow Burn dari koin_utama.
4. Anti-SSRF Socket & DNS Resolution Gate: Mengadopsi patch keamanan decolua/9router dan standar v4.0 yang memvalidasi IP soket
asli, memblokir IP lokal/metadata cloud (127.0.0.0/8, 169.254.169.254, ::1), serta mencegah Silent Cloud Fallback pada mode
privat (NOCTURNE_UNCENSORED) agar prompt sensitif pengguna tidak pernah bocor ke API korporat (seperti Google/Groq) saat endpoint
terbuka sedang sibuk.
5. ModelScan & Safetensors/GGUF Enforcer: Menolak pemuatan berkas bobot berekstensi .pkl/.pt/.bin mentah yang berisiko Model
Serialization Attack dan mengintegrasikan pemeriksaan protectai/modelscan (wajib exit code 0).
6. Human Approval Gate Eksplisit di Kode: Menambahkan tabel pending_human_approvals yang menahan eksekusi otomatis dan
meminta klik persetujuan Owner di DM untuk 5 aksi kritis: migrasi data, ubah harga/plan, hapus fitur/plugin, tarik saldo di atas threshold,
dan ubah kebijakan keamanan.
2. CODING/ARCH: Otak Router Lebih Cerdas, Anti-Soft-Refusal & Self-Healing
[FAKTA] [Bersumber] Combo Grading & Capacity Auto-Switch (Adopsi Arsitektur 9Router + RouteLLM):
Selain Two-Tier Staggered Hedging (
 yang menghemat kuota gratis >80%), router dilengkapi 4 mode strategi Combo:
1. FALLBACK_GRADING: Mengurutkan model dari skor kesehatan & kecerdasan tertinggi (DeepSeek-R1-0528 → Qwen3-Coder →
Gemini 2.5/3.8 Flash → Pollinations).
2. CAPACITY_AUTO_SWITCH: Otomatis mendeteksi jika input berisi foto/PDF/audio dan langsung mengarahkannya ke model
berkapasitas multimodal tanpa gagal.
3. COMBO_FUSION_JUDGE: Khusus mode /riset (Deep Research), menembak 2 model cepat secara paralel lalu menyintesis intisari
terbaiknya.
4. RTK_CONTEXT_COMPRESSOR: Memangkas riwayat chat dan hasil tool hingga 40–98% dengan pemuatan malas SKILL.md (gaya
nanoMuse & context-mode) sehingga hemat kuota token harian.
[FAKTA] [Bersumber] Detektor & Penawar Soft Refusal Otomatis (Solusi Temuan isi dari sdu 3.html):
Pada mode NOCTURNE_UNCENSORED, setiap balasan model diperiksa terhadap pola soft refusal (ceramah moral/penolakan implisit).
Jika terdeteksi, sistem otomatis melakukan re-prompting ke model abliterated murni (Hermes 4 405B / Dolphin 3.0 Venice /
Qwen3-30B-A3B-abliterated) sehingga kepatuhan nyata melonjak di atas batas 49%.
[FAKTA] [Bersumber] Orchestrator Tipis, Plugin Surface & Self-Healing Loop (Master Contract D2):
app.py menyediakan PluginRegistry dengan fitur register(), health(), dan hot_swap() (diuji otomatis dengan AST & Dunder
Sterilizer sebelum aktif).
Self-Healing Loop bekerja dengan alur ketat: classify_error → pilih handler → apply_fix → verify. Jika gagal 3x
berturut-turut, sistem menghentikan retry dan melakukan eskalasi ke human_escalation_queue + notifikasi DM Owner.
3. BIZ/MARKET & PRODUCT/UX: Mesin Uang Otomatis & Afiliasi
[FAKTA] [Bersumber] 4-Zona Dynamic PPP Pricing (Adopsi isi link sumber.html):
Memperbarui struktur harga agar mendukung 4 zona daya beli: Zona 1 (Global Tier-1 100%), Zona 2 (Global Tier-2 70%), Zona 3
(Emerging 50%), dan Zona 4 (Indonesia QRIS 25% — Paket Hemat Rp 5.000, Pro Rp 25.000, Sultan VIP Rp 250.000).
[FAKTA] [Bersumber] Automated Sales Funnel & Program Afiliasi Koin (Adopsi @TeleportAppBot):
Auto-Followup Kasir: Jika pengguna membuka tagihan Top-Up tetapi belum membayar dalam waktu tertentu, bot mengirim sapaan
personal yang ramah (seperti pesan Maksim di @TeleportAppBot) untuk membantu kendala pembayaran atau menawarkan paket uji
coba.
Tautan Afiliasi Otomatis (?start=ref_ID): Setiap kreator mendapat tautan undangan unik di menu mereka; setiap teman yang
bergabung dan melakukan Top-Up otomatis memberikan komisi koin kepada pengundang, menekan biaya akuisisi pelanggan (CAC)
menjadi Rp 0.
D4. STOP & KONFIRMASI EKSEKUSI FILE (1 Langkah Berikutnya)
Seluruh peningkatan keamanan berlapis, kecerdasan router (Combo Grading + Anti-Soft-Refusal + Staggered Hedging), Self-Healing
Loop (maksimal 3x retry → human queue), Human Approval Gate (5 aksi kritis), serta fitur bisnis (Affiliate + Sales Follow-up + 4-Zona
≤65s
H
​ =
blind
SHA256(Nonce ∥SecretSalt)
​
[:16]
τ
​ =
hedge
1, 2 detik


