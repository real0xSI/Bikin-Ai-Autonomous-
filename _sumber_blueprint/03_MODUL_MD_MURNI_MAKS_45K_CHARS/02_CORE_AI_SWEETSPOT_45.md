
<!-- [ID:02_CORE_AI_S247] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 168

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



<!-- [ID:02_CORE_AI_S248] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 169

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



<!-- [ID:02_CORE_AI_S249] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 170

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



<!-- [ID:02_CORE_AI_S250] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 172

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



<!-- [ID:02_CORE_AI_S251] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 178

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



<!-- [ID:02_CORE_AI_S252] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 180

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



<!-- [ID:02_CORE_AI_S253] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 189

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



<!-- [ID:02_CORE_AI_S254] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# --- 3. LAYER 2: SELF-HOSTED GATEWAYS & SEMANTIC CACHE ---​
REDIS_CONN_STRING="redis://default:password@endpoint.upstash.io:6379"​
OMNIROUTE_BASE_URL="http://127.0.0.1:4000/v1"​
NINEROUTER_BASE_URL="http://127.0.0.1:4001/v1"​
NEW_API_HORIZON_URL="http://127.0.0.1:3001/v1"​
PORTKEY_GATEWAY_URL="http://127.0.0.1:8787/v1"​
SESSION_SECRET="gunakan_string_acak_kriptografis_minimal_64_karakter"​
ROUTELLM_THRESHOLD="0.11593"​
​

<!-- [ID:02_CORE_AI_S255] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# --- 5. LAYER 4: TIER-2 LOCAL UNCENSORED & SOTA INFERENCE (KELOMPOK 
1B/1D) ---​
LLAMA_CPP_LOCAL_URL="http://127.0.0.1:8080/v1"​
VLLM_LOCAL_URL="http://127.0.0.1:8000/v1"​
OLLAMA_LOCAL_URL="http://127.0.0.1:11434/v1"​
LOCAL_REASONING_MODEL="deepseek-ai/DeepSeek-R1-0528-Qwen3-8B"​
LOCAL_UNCENSORED_MODEL="huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF"​
LOCAL_MOE_MODEL="huihui_ai/qwen3.6-abliterated:35b"​
​

<!-- [ID:02_CORE_AI_S256] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 202

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



<!-- [ID:02_CORE_AI_S257] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 204

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



<!-- [ID:02_CORE_AI_S258] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 208

Komponen Blueprint 
Saat Ini 
Kekuatan Desain 
Eksisting 
Celah Arsitektural & 
Risiko Skala Produksi 
Rekomendasi Ekspansi 
Aditif (Solusi Tingkat 
Enterprise) 
Anti-Tuyul 
(security_gate.py) 
24-byte (SEC-06), 
InsightFace >23 tahun 
(AI-SEC-02), dan 
sistem 2 dompet. 
terhadap Indirect 
Prompt Injection. Klaim 
koin harian Rp 400 dan 
afiliasi rentan 
ditambang oleh 
emulator farm (tuyul) 
yang mengakali diskon 
Rp 500/video. 
dengan Llama Prompt 
Guard 2 (86M) + NeMo 
Guardrails, serta 
penyematan TMA 
Behavioral 
Biometrics, WebGL 
Fingerprinting, & 
Cloudflare Turnstile. 
Dimensi 1: Ekspansi Stack AI Engine (SOTA) dan 
Orkestrasi Multi-Agen Hirarkis 
Integrasi Aditif Engine SOTA Multi-Modal Berbiaya Ultra-Rendah 
Untuk mempertahankan keunggulan kompetitif "Sultan Super-App" sekaligus menekan Harga 
Pokok Penjualan (HPP) di bawah batas psikologis kompetitor, tumpukan (stack) engine AI pada 
bikinAI Super Intelligence perlu diperluas dengan model State-of-the-Art (SOTA) generasi 
terbaru yang memiliki efisiensi Mixture-of-Experts (MoE) dan kuantisasi presisi rendah. 
Penambahan ini bersifat murni aditif terhadap engine yang sudah terdaftar pada cetak biru, 
yakni Gemini Flash, Qwen 2.5, Llama 3.3, DeepSeek R1/V3, Claude Sonnet, Nous Hermes 3, 
Mistral Nemo, Flux.1, Wan 2.1/2.2, LTX-Video, Hunyuan, Kling, Veo, Sora, Runway, dan 
Suno/Udio. 
Pada lapisan penalaran teks, orkestrasi, dan multimoda, integrasi DeepSeek-V4.1-Flash dan 
DeepSeek-V4-Pro (melalui SiliconFlow, OpenRouter, atau Parasail dengan dukungan Zero 
Data Retention / ZDR) memberikan lompatan efisiensi yang masif. DeepSeek-V4.1-Flash 
merupakan model MoE multimodal dengan tulang punggung 552 miliar parameter yang hanya 
mengaktifkan sekitar 8 miliar parameter saat fase prefill dan 16 miliar parameter saat decode, 
menghasilkan kecerdasan setara model flagship dengan tarif input serendah 
0,06 per 1 
0, 042–
juta token (dan cached input $0,01 per 1 juta token) serta output 
0,24 per 1 juta token. 
0, 084–
Untuk tugas pemrograman kompleks dan agen otonom, Qwen 3.8 Max, Qwen 3.7 Plus ($0,14 
input / $0,55 output per 1 juta token), Qwen3-Omni-30B-A3B-Thinking, serta Kimi K2.7 Code 
menjadi tulang punggung tambahan di dalam 9Router ketika kuota gratis harian mencapai 
ambang rotasi 98%. 
Pada lapisan generasi video mandiri (Mode 3: Pabrik GPU ComfyUI) dan grosir (Mode 2: API 
Pay-Per-Generate), sistem wajib mengadopsi arsitektur penuh keluarga Wan 2.2 MoE (5B & 
14B) serta Wan 2.5 / 2.6, berdampingan dengan Seedance 1.5 Pro (BytePlus, dengan tarif 
turun drastis ke $0,012 per detik render), Open-Sora 2.0 (11B), dan MiniMax H3. Keunggulan 
krusial Wan 2.2 terletak pada pemisahan pakar (expert) untuk tahap high-noise dan low-noise 
yang menghasilkan detail visual jauh lebih tajam tanpa penalti komputasi tambahan, sementara 
rilis Wan 2.5 mempercepat render 720p hingga 30%. 
Celah terbesar pada pembuatan video AI 30 detik di pasar saat ini adalah ketiadaan narasi 
suara berlatensi instan yang murah serta ketiadaan efek suara lingkungan (foley) yang menyatu 
dengan gerakan visual. Menggunakan Suno v4/v6 (yang memiliki HPP lebih tinggi dan 
dirancang untuk komposisi lagu utuh di Tier Ultra) atau ElevenLabs (
80 per 1 juta karakter) 
18–



<!-- [ID:02_CORE_AI_S259] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 209

untuk sekadar mengisi narasi iklan UMKM 30 detik akan menggerus margin keuntungan. Untuk 
mengatasi hal tersebut, arsitektur perlu mengintegrasikan Kokoro-82M (Hexgrad) sebagai 
mesin Text-to-Speech (TTS) utama dan MMAudio (157M) bersama HunyuanVideo-Foley 
sebagai mesin Video-to-Audio (V2A). Kokoro-82M adalah model open-weight berlisensi Apache 
2.0 dengan 82 juta parameter yang mencapai latensi audio pertama (Time-to-First-Byte) 
terendah di industri sebesar 28 ms pada GPU modern (skor ELO 1.059). Jika diakses melalui 
API OpenRouter atau penyedia terkelola, biayanya hanya $0,62 per 1 juta karakter (sekitar Rp 
1 per naskah video 30 detik), dan model ini cukup ringan untuk dijalankan langsung di RAM 
worker tanpa membebani VRAM utama. Sementara itu, MMAudio dan HunyuanVideo-Foley 
bekerja menggunakan algoritma flow-matching dan penyelarasan tingkat frame (melalui 
ekstraktor fitur CLIP pada 8 FPS dan Synchformer pada 25 FPS) untuk membaca klip video 
bisu hasil render Wan atau Flux, lalu mensintesis efek suara langkah kaki, pergerakan objek, 
maupun ambien ruangan beresolusi 48kHz yang tersinkronisasi presisi dengan visual hanya 
dalam waktu 1,23 detik untuk klip berdurasi 8 detik. 
Untuk mengatasi masalah character drift—yakni perubahan struktur wajah, gaya rambut, dan 
pakaian karakter saat Muse memecah video 30 detik menjadi 6 klip berdurasi 5 
detik—tumpukan visual wajib menambahkan PuLID Flux II, FLUX.2 (yang mendukung hingga 
10 gambar referensi sekaligus), serta kombinasi InstantID + IP-Adapter di dalam alur kerja 
ComfyUI. Berbeda dengan InstantID standar yang terkadang mengalami penurunan kemiripan 
wajah saat karakter menoleh ke samping (profile view), PuLID Flux II mengunci identitas wajah 
secara konsisten tanpa mencemari bobot gaya model utama (zero model pollution). 
Kategori 
Modalitas 
Engine AI 
Tambahan 
(Aditif) 
Lisensi / Akses Spesifikasi & 
Keunggulan 
Teknis 
Biaya 
Operasional 
(HPP) 
Penempatan 
Kasta (Tier) 
LLM & 
Reasoning 
DeepSeek-V4.
1-Flash (552B 
MoE, 8B/16B 
aktif) 
Open-Weight / 
API 
(SiliconFlow, 
OpenRouter) 
Konteks 1,05M 
token, 
arsitektur 
Causal 
Encoder-Decod
er, mendukung 
ZDR. 
0,06 / 
0, 042–
1M input; $0,01 
cached 
Tier Eco & Otak 
Muse 
(Cadangan 
Lapis 2) 
LLM 
Multimodal 
Qwen 3.7 Plus 
/ 
Qwen3-Omni-
30B-A3B 
Open-Weight / 
API 
Pemahaman 
dokumen, 
audio, dan 
instruksi 
multibahasa 
Asia Tenggara 
yang presisi. 
$0,14 / 1M 
input; $0,55 / 
1M output 
Tier Pro (Otak 
Kampanye & 
Analisis PDF) 
Video 
Generatif 
(Self-Hosted) 
Wan 2.2 MoE 
(5B & 14B 
FP8) & Wan 
2.5 
Apache 2.0 
(Komersial 
Penuh) 
Arsitektur pakar 
high-noise/low-
noise, kualitas 
99,5% setara 
FP16 dengan 
separuh VRAM 
(12–14 GB). 
Rp 110–Rp 250 
/ klip 5 detik (di 
RTX 4090) 
Tier Pro (Mesin 
Utama Margin 
85%) 
Video 
Komersial 
Seedance 1.5 
Pro & 
API BytePlus / 
Fal.ai / 
Gerakan 
tarian/aksi 
~$0,012 / detik 
(Rp 950 / klip 5 
Tier Pro+ / Tier 
Ultra 



<!-- [ID:02_CORE_AI_S260] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 210

Kategori 
Modalitas 
Engine AI 
Tambahan 
(Aditif) 
Lisensi / Akses Spesifikasi & 
Keunggulan 
Teknis 
Biaya 
Operasional 
(HPP) 
Penempatan 
Kasta (Tier) 
(API Grosir) 
Open-Sora 2.0 
(11B) 
ComfyUI 
sangat mulus, 
kepatuhan 
prompt 
sinematik 
tinggi. 
detik) 
Konsistensi 
Karakter 
PuLID Flux II & 
FLUX.2 
Multi-Ref 
Open-Source 
Node ComfyUI 
Mengunci 
identitas wajah 
& pakaian 
lintas 6 klip 
video (30 detik) 
tanpa model 
pollution. 
Rp 0 (Berjalan 
di dalam 
pipeline GPU 
yang sama) 
Tier Pro & 
Paket Story 30 
Detik 
Voiceover / 
TTS Instan 
Kokoro-82M 
v1.0 
Apache 2.0 
(OpenRouter / 
Lokal) 
Latensi 28 ms 
TTFB, kualitas 
suara natural 
(ELO 1.059), 
ukuran model 
sangat ringan. 
$0,62 / 1M 
karakter (~Rp 1 
/ narasi iklan) 
Tier Eco 
(Gratis) & Tier 
Pro (Narasi 
Video) 
Efek Suara 
Video (V2A 
Foley) 
MMAudio 
(157M) & 
HunyuanVideo
-Foley 
Open-Source 
(CVPR 2025 / 
Tencent) 
Menghasilkan 
audio foley & 
ambien 48kHz 
yang sinkron 
per frame 
dalam 1,23 
detik. 
~Rp 15 / klip 8 
detik (Inferensi 
GPU 1,2 detik) 
Paket Story 30 
Detik & Tier 
Ultra 
Evolusi 5 Agen Menjadi 7-Node LangGraph Hierarchical Supervisor 
Dalam cetak biru 50% saat ini, kelima agen (Gatekeeper & Billing, Orchestrator/Muse, Prompt 
Engineer & Sanitizer, Media Worker & Compiler, serta AI Support & Triage) dihubungkan 
melalui pemanggilan skrip Python asinkron standar. Ketika pengguna mengeksekusi fitur 
unggulan "1 Perintah Jadi Paket Kampanye Utuh" atau "Paket Story / Iklan Utuh 30 Detik 
(6 Klip + Jahit FFmpeg + Voiceover/Musik)" seharga 100 Koin (Rp 10.000), eksekusi linier 
menghadapi risiko kegagalan berantai: apabila klip ke-4 mengalami distorsi visual atau wajah 
karakter berubah, sistem linier tetap menjahitnya menjadi video cacat yang memicu komplain 
dan refund penuh. 
Solusi arsitektural tingkat lanjut adalah memformalkan orkestrasi menggunakan LangGraph 
Hierarchical Supervisor Pattern (StateGraph) di mana Muse Orchestrator bertindak sebagai 
Central Traffic Controller yang memegang kendali atas objek status bersama (Shared Workflow 
State) menggunakan primitif Command(goto=...) dan anotasi Literal[...]. Pekerja spesialis 
(worker agents) tidak pernah memutuskan sendiri agen mana yang berjalan selanjutnya; 
mereka mengeksekusi tugas spesifik, memperbarui graph state, dan mengembalikan kontrol ke 
Supervisor untuk dievaluasi sebelum alur kerja dilanjutkan atau diinstruksikan melakukan 
self-correction loop. Selain mempertahankan 5 agen asli secara utuh, arsitektur ini diperluas 
menjadi 7 Agen Spesialis dengan menyematkan Visual Continuity & Character Lock Agent 



<!-- [ID:02_CORE_AI_S261] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 213

memverifikasi keaslian voucher secara matematis dalam 0,1 milidetik, kemudian mencatat 
voucher_nonce yang telah diklaim ke dalam database lokalnya sendiri guna mencegah 
double-spending. Dengan arsitektur asimetris ini, tidak ada satu pun koneksi jaringan, panggilan 
API, atau berbagi database antara @bikinAI_bot (entitas SaaS produktivitas Indonesia) dan 
NocturneAI.art (platform eksperimen open-source global). 
Pada tingkat perangkat keras, ketika worker GPU di Vast.ai atau RunPod mengeksekusi beban 
kerja dari jalur Unfiltered, kontainer Docker wajib dijalankan menggunakan runtime isolasi 
kernel (seperti runsc / gVisor atau bubblewrap untuk sub-proses) dengan kebijakan jaringan 
Egress Whitelist yang hanya mengizinkan lalu lintas keluar menuju Cloudflare Worker Edge 
Relay. Seluruh bobot model LoRA tambahan, gambar input, dan tensor latent diproses secara 
eksklusif di dalam partisi memori volatil /dev/shm (berbasis tmpfs RAM Linux yang di-mount 
dengan parameter keamanan noexec,nosuid,nodev,size=16g) serta disuntikkan Negative 
Embedding Permanen pada level tensor conditioning GPU. Begitu output selesai dienkripsi 
menggunakan AES-256-GCM menjadi blob .bin di dalam RAM dan dikirim ke Edge Relay, 
ruang memori /dev/shm langsung ditimpa nol (zero-overwrite) dan kunci enkripsi sesi 
dihancurkan tanpa pernah menyentuh piringan diska (hardisk fisik host). 
Dimensi 2: Hardening Keamanan Berlapis 
(Defense-in-Depth) dan Mitigasi Anti-Fraud 
Penambalan Celah Kritis pada Kode Pertahanan Saat Ini (Audit 
SEC-01 s/d SEC-06) 
Kode pertahanan inti yang terdapat pada Bagian 5.4 dokumen cetak biru telah dirancang 
secara cerdas untuk menangkis serangan Financial Race Condition (TOCTOU SEC-02), 
Polyglot Prompt (SEC-01), dan Webhook Spoofing (SEC-03) tanpa ketergantungan pada server 
Redis eksternal yang boros memori. Meskipun demikian, bedah kode tingkat produksi 
mengungkap empat celah kerentanan turunan (second-order vulnerabilities) yang perlu segera 
ditambal agar sistem tahan terhadap serangan berskala besar. 
Kerentanan pertama terletak pada potensi Memory Exhaustion (OOM) akibat deklarasi 
USER_LOCKS = defaultdict(asyncio.Lock) yang bersifat tak terbatas (unbounded dictionary). 
Walaupun satu instans objek asyncio.Lock hanya memakan sekitar 64 bytes, entri kamus 
Python beserta referensi objek integer di dalamnya mengonsumsi sekitar 240–280 bytes per 
kunci unik. Apabila penyerang melancarkan serangan enumerasi ID melalui webhook atau 
botnet yang memicu inisialisasi 5 hingga 10 juta user_id acak yang berbeda, USER_LOCKS 
akan tumbuh secara permanen di memori karena tidak memiliki mekanisme penghapusan 
(eviction), menguras >2 GB RAM dan menjatuhkan VPS kecil. Solusi yang jauh lebih tangguh 
adalah mengganti defaultdict dengan Fixed-Size Lock Striping—yakni mengalokasikan 
sebuah array statis berisi 4.096 objek asyncio.Lock saat aplikasi menyala, lalu memetakan 
setiap pengguna menggunakan operasi modulo USER_LOCK_STRIPES[user_id % 4096]. 
Pendekatan ini mengunci penggunaan RAM di angka ~250 KB selamanya (100% kebal 
terhadap serangan jutaan ID palsu) sambil tetap menjamin penguncian eksklusif per pengguna. 
Kerentanan kedua muncul dari fitur Auto-Intent Detection untuk Pembacaan Dokumen 
PDF/Word/Excel (Bagian 4.1 cetak biru) yang membuka vektor serangan Indirect Prompt 
Injection. Fungsi sanitize_polyglot_prompt saat ini membersihkan karakter tak terlihat Unicode 
(Cf, Cc, Cs), namun belum mengisolasi teks yang diekstrak dari dokumen eksternal. Penyerang 



<!-- [ID:02_CORE_AI_S262] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 214

dapat mengunggah file PDF katalog produk yang di dalamnya telah disisipi instruksi 
tersembunyi (teks putih berukuran mikro) yang memerintahkan agen untuk memanipulasi status 
Job_ID atau membocorkan konfigurasi sistem. Untuk memitigasi risiko ini, arsitektur wajib 
menerapkan Privilege Separation (Dual-LLM Sandbox): pemrosesan teks dokumen 
PDF/Word/Excel harus ditangani oleh instans LLM pembaca yang sama sekali tidak memiliki 
akses ke alat (tools), fungsi database, maupun rute safe_one_time_refund, serta membungkus 
seluruh teks ekstraksi di dalam tag pembatas XML acak per-sesi. 
Kerentanan ketiga adalah Multi-Turn Context Drift pada fitur Smart Context Compression di 
dapur 9Router (Bagian 3.2 cetak biru). Penyelarasan keamanan LLM umumnya dioptimalkan 
untuk menolak instruksi berbahaya pada satu giliran pesan tunggal (single-turn), namun rentan 
ditembus ketika penyerang membangun konteks percakapan yang tampak wajar selama 10–15 
giliran lalu mengarahkan model ke topik terlarang. Ketika 9Router merangkum obrolan panjang 
tersebut menjadi memori padat (compressed context), instruksi manipulatif penyerang dapat 
ikut terkompresi ke dalam system summary sehingga dianggap sebagai instruksi terpercaya 
pada giliran berikutnya. Oleh karena itu, setiap hasil kompresi konteks wajib melewati 
pemindaian klasifikator keamanan tingkat dialog sebelum disimpan kembali ke memori sesi. 
Kerentanan keempat berkaitan dengan Token Replay Attack di Dalam Jendela 60 Detik pada 
Validasi initData (API-01). Cetak biru telah menetapkan pemeriksaan kedaluwarsa auth_date 
maksimal 60 detik pada tanda tangan HMAC-SHA256 Telegram.WebApp.initData. Namun, di 
dalam rentang 60 detik sebelum auth_date kedaluwarsa, penyerang yang menyadap string 
initData melalui DevTools masih dapat menembakkan string yang sama ribuan kali secara 
paralel untuk mencetak ribuan Short-Lived JWT. Selain itu, implementasi HMAC wajib 
mengecualikan field hash dan signature dari string pemeriksaan agar kompatibel dengan 
pembaruan protokol Ed25519 Telegram terbaru. Menyimpan nilai hash yang sudah ditukar di 
dalam struktur Bounded Ring Buffer berkapasitas tetap selama 65 detik secara efektif menutup 
celah replay tersebut dengan konsumsi RAM di bawah 1 MB. 
Arsitektur AI WAF dan Guardrail Tiga Lapis Berlatensi Rendah 
Menjalankan LLM berukuran besar sebagai hakim keamanan (LLM-as-a-Judge) pada setiap 
pesan yang masuk akan menambah latensi beberapa detik pada jalur kritis dan menggandakan 
konsumsi token harian. Sebaliknya, hanya mengandalkan ekspresi reguler (regex) atau daftar 
kata kunci statis gagal mendeteksi lima dari enam kategori kegagalan AI yang bersifat 
semantik—seperti polite policy violation, roleplay framing, dan rephrased jailbreaks. Untuk 
mencapai keamanan tingkat enterprise tanpa mengorbankan kecepatan respons bot, modul 
security_gate.py perlu mengimplementasikan arsitektur Three-Stage Low-Latency AI 
Guardrail yang menjaga total anggaran latensi di bawah 80 milidetik (p99). 
Pada tahap pertama (Sub-Millisecond Static Gate, <1 ms), sistem mengeksekusi normalisasi 
Unicode NFKC, penyaringan karakter kontrol, validasi skema struktur Pydantic, dan 
pemeriksaan 24-Byte Header Guard untuk gambar. Apabila lolos, pesan masuk ke tahap kedua 
(Fast First-Pass Injection Filter, 20–50 ms) yang ditenagai oleh Llama Prompt Guard 2 
(86M)—sebuah model klasifikasi berbasis tulang punggung mDeBERTa dengan 86 juta 
parameter (~0,3B total parameter) yang hanya membutuhkan memori di bawah 1 GB sehingga 
dapat berjalan sangat cepat di CPU ARM Oracle Cloud (menggunakan kuantisasi ONNX INT8) 
maupun di irisan tipis GPU untuk menangkap upaya prompt injection dan jailbreak sebelum 
menyentuh model utama. Hanya untuk pesan yang ditandai mencurigakan oleh tapis pertama 
atau yang mengarah ke pembuatan media sensitif, sistem memicu tahap ketiga (Dialog & 
Hazard Classification Rails, 20–65 ms) yang menggabungkan kerangka kerja open-source 



<!-- [ID:02_CORE_AI_S263] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_26, SPAN_8 -->
## Halaman 220

open-source Redis berkinerja tinggi) dan pustaka Python RedisVL (SemanticCache serta 
Semanti[span_26](start_span)[span_26](end_span)cRouter) di dalam VPS yang sama—yang 
hanya membutuhkan ~120 MB RAM dari jatah 12–24 GB RAM gratis di Oracle Cloud Ampere 
A1—menghasilkan penghematan biaya dan akselerasi performa yang dramatis. Berdasarkan 
tolok ukur produksi, penerapan semantic caching memangkas volume panggilan API ke LLM 
sebesar 40% hingga 86% dengan tetap mempertahankan akurasi respons di atas 91%. Ketika 
Prompt Engineer Agent selesai menyusun struktur JSON kampanye atau menerjemahkan 
prompt bahasa daerah/Indonesia menjadi prompt sinematik bahasa Inggris untuk Wan 2.2 dan 
Flux, pasangan vektor embedding dan respons tersebut disimpan di Valkey dengan 
Time-to-Live (TTL) terukur. Saat kueri serupa masuk dan melampaui ambang kemiripan kosinus 
yang ketat (misalnya similarity_threshold=0.92[span_8](start_span)[span_8](end_span) atau 
distance_threshold=0.12 pada RedisVL untuk mencegah jawaban yang salah), sistem langsung 
mengembalikan hasil dari memori dalam waktu 25 hingga 27 milidetik (terdiri dari ~22 ms 
pembuatan embedding lokal, ~2 ms pencarian indeks vektor Valkey, dan ~1 ms pengambilan 
JSON)—sebuah percepatan hingga 250 kali lipat dibandingkan panggilan API Gemini atau 
DeepSeek penuh yang memakan waktu 2.700 ms hingga 7.000 ms. Lebih jauh lagi, komponen 
SemanticRouter pada RedisVL menggantikan panggilan LLM pada Auto-Intent Detection 
dengan klasifikasi vektor deterministik yang mengelompokkan niat pesan pengguna ke dalam 6 
rute aksi hanya dalam beberapa milidetik pada biaya Rp 0. 
Optimasi TCO Pabrik Render GPU: Kuantisasi FP8/GGUF, TeaCache, 
dan SageAttention 
Dalam perhitungan finansial Bagian 2.2 cetak biru, diasumsikan waktu render 1 video 5 detik 
(model Wan 2.1/2.2) pada GPU RTX 3090/4090 (24 GB VRAM) adalah 40–60 detik dengan 
HPP rata-rata Rp 300–Rp 500 per video. Namun, temuan teknis di lapangan menunjukkan 
bahwa apabila worker ComfyUI di RunPod atau Vast.ai dijalankan dengan konfigurasi bawaan 
(NORMAL_VRAM atau menggunakan bobot model FP16 tanpa kuantisasi), kartu 24 GB VRAM 
akan mengalami Out-of-Memory (OOM) pada UNETLoader atau terjebak pada utilisasi GPU 
rendah (30–40%) dengan CPU bottleneck 100% karena bobot Wan 14B FP16 membutuhkan 
~28 GB VRAM. Tanpa akselerasi tingkat lanjut, waktu render dasar untuk 1 klip Wan 2.1 720p 
I2V di RTX 4090 mencapai 542,09 detik (~9 menit). 
Untuk mengunci waktu render secara konsisten di angka 40–60 detik (480p/540p) atau 248 
detik (720p HD penuh) serta memangkas Total Cost of Ownership (TCO) pabrik GPU hingga 
lebih dari 50%, modul stateless_gpu_worker.py wajib menerapkan standarisasi kuantisasi bobot 
model dan kompilasi graf. Pada mesin GPU 24 GB VRAM (RTX 3090/4090), worker tidak boleh 
memuat model FP16 (28 GB), melainkan wajib menggunakan checkpoint FP8 Scaled 
(wan2.2_t2v_14B_fp8_scaled.safetensors dan 
wan2.2_i2v_low_noise_14b_fp8_scaled.safetensors bersama wan2.2_vae.safetensors) yang 
memangkas konsumsi VRAM menjadi 14 GB namun mempertahankan ~99,5% kualitas visual 
FP16 (nyaris lossless untuk video). Ruang kosong VRAM sebesar 10 GB yang tersisa pada 
kartu 24 GB tersebut memungkinkan sistem memuat node PuLID Flux II, CLIP Vision, dan 
MMAudio secara berdampingan di memori GPU tanpa perlu melakukan block swapping ke 
RAM sistem. Apabila sistem menyewa GPU sekunder yang lebih murah dengan 12–16 GB 
VRAM (seperti RTX 4060 Ti atau RTX 3060), worker dapat menggunakan varian kuantisasi 
GGUF Q8_0 (10 GB VRAM, retensi kualitas 98–99%) yang dipadukan dengan LoRA akselerasi 
LightX2V 4-step, atau menggunakan model terpadu Wan 2.2 5B FP16 



<!-- [ID:02_CORE_AI_S264] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 227

mencatat metrik api_key_id, provider_tier (Tier 1 Gratis vs. Tier 2 OpenRouter :free vs. Tier 3 
Saldo Cadangan $1), rasio penghematan token dari kompresi RTK/Caveman, serta rasio 
Semantic Cache Hit/Miss. Lebih penting lagi, pada tahap penyelesaian pekerjaan di 
stateless_gpu_worker.py, sistem menerapkan Cost-Based Rate Limiting & Margin Guard: 
worker mengalkulasi biaya HPP aktual dalam Rupiah (actual_provider_cost_idr berdasarkan 
detik pemakaian GPU RunPod/Vast.ai atau tarif per panggilan Fal.ai/Seedance) dan 
membandingkannya secara langsung dengan nilai Koin yang dipotong dari pengguna. Apabila 
rasio HPP terhadap harga jual pada suatu model melampaui ambang aman 75% akibat 
perubahan tarif provider hulu atau lonjakan waktu queueing, sistem secara otomatis mengirim 
peringatan instan ke Admin dan menggeser rute ke model alternatif yang lebih efisien. 
Untuk memastikan penyambungan antara backend Python, antarmuka miniapp_studio.html, 
studio independen NocturneAI.art, dan Cloudflare Worker Edge Relay pada 50% dokumen 
selanjutnya berjalan mulus, seluruh kontrak komunikasi wajib dibakukan menggunakan 
spesifikasi OpenAPI 3.1 (dihasilkan otomatis melalui kerangka kerja FastAPI/Litestar pada 
gerbang API Mini App) dan ComfyUI JSON Workflow Registry. Seluruh file JSON workflow 
ComfyUI (untuk Wan 2.2 T2V, Wan 2.2 I2V, Flux HD, PuLID Character Lock, MMAudio Foley, 
dan Real-ESRGAN 4K) disimpan sebagai templat terparametrisasi yang telah dikunci 
resolusinya ke kelipatan 64 piksel (Preset Parameter Clamping sesuai pertahanan SEC-05), 
sehingga worker hanya perlu menyuntikkan prompt yang telah disanitasi, seed, dan URL 
gambar referensi tanpa risiko crash akibat manipulasi parameter dari sisi klien. 
Sintesis Rekomendasi Eksekusi Prioritas 
Keseluruhan bedah arsitektur ini menegaskan bahwa cetak biru 50% bikinAI Super 
Intelligence telah memiliki pondasi strategi bisnis, psikologi akuisisi pengguna, dan kerangka 
keamanan Zero-Knowledge yang sangat unggul. Untuk mengonversi cetak biru tersebut 
menjadi infrastruktur produksi berskala global yang tahan banting, hemat biaya, dan siap 
menyelesaikan 50% tahap pengembangan sisanya tanpa refactoring, langkah konstruksi harus 
difokuskan pada empat pilar eksekusi. 
Pada pilar keamanan dan konkurensi data (Modul 1 & 2), tim pengembang perlu segera 
mengganti defaultdict(asyncio.Lock) dengan Fixed-Size Lock Striping (4.096 stripes), 
menambahkan Bounded Replay Guard pada verifikasi HMAC initData, mengimplementasikan 
pemisahan koneksi baca/tulis pada SQLite WAL (dengan kesiapan migrasi ke Turso libSQL), 
serta menerapkan batas Hard-Cap 25 Koin Bonus yang dikombinasikan dengan WebGL 
Device Fingerprinting dan Cloudflare Turnstile di dalam Mini App untuk mematikan potensi 
eksploitasi tuyul. Pada pilar efisiensi kecerdasan dan pencegahan serangan siber (Modul 2 & 
3), penempatan Valkey Semantic Cache / RedisVL bersama Llama Prompt Guard 2 (86M) 
dan NeMo Guardrails di depan 9Router akan memangkas 40%–86% konsumsi kuota LLM, 
mempercepat respons cache hit hingga 25–27 milidetik (250x lebih cepat), serta melindungi 
pembaca dokumen PDF dari Indirect Prompt Injection dalam anggaran latensi di bawah 80 ms. 
Selanjutnya, pada pilar orkestrasi multi-agen dan pabrik media (Modul 3 & 4), peningkatan 
arsitektur menjadi 7-Node LangGraph Hierarchical Supervisor yang memadukan Wan 2.2 
FP8 Scaled (14 GB VRAM), akselerasi SageAttention + TeaCache (54% lebih cepat), 
pengunci karakter PuLID Flux II, narasi Kokoro-82M ($0,62/1M karakter), dan efek suara 
sinkron MMAudio (1,23 detik) di atas RunPod Serverless FlashBoot (<250 ms cold-start) 
akan menghasilkan kualitas video iklan 30 detik yang jauh melampaui kompetitor dengan 
margin keuntungan mencapai ~89%. Terakhir, pada pilar moneter dan isolasi hukum (Modul 5 & 


