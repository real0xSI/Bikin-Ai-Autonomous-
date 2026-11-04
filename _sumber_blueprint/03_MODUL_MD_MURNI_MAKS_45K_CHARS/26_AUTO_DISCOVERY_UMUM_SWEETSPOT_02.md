
<!-- [ID:26_AUTO_DISCOVERY_UMUM_S099] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 111


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S100] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 1. MENYAMARKAN FOLDER & NAMA MESIN

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S101] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Samarkan ComfyUI menjadi "data_engine"
if not os.path.exists('data_engine'):
   repo = "https://github.com/comfyanonymous/ComfyUI"
   os.system(f'git clone {repo} data_engine -q')
os.chdir('/content/data_engine')
os.system('pip install -r requirements.txt -q')

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S102] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Jalankan menggunakan worker.py di port 7777 (Bukan 8188)
subprocess.Popen(["python", "worker.py", "--port", "7777"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNU
time.sleep(45)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S103] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 0. INISIALISASI & MANAJEMEN MEMORI MODEL

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S104] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Cek Custom Nodes (ReActor)
if not os.path.exists('custom_nodes/comfyui-reactor-node'):
   print("Memasang ReActor Node...")
   os.system('git clone https://github.com/Gourieff/comfyui-reactor-node custom_nodes/comfyui-reactor-node -q
   if os.path.exists('custom_nodes/comfyui-reactor-node/requirements.txt'):
       os.system('pip install -r custom_nodes/comfyui-reactor-node/requirements.txt -q')

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S105] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 1. FUNGSI CEK INTEGRITAS MODEL (CEGAH DOWNLOAD ULANG)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S106] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 115


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S107] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 2. JANTUNG UTAMA (POLLING API BRANKAS)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S108] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# SYSTEM SOP: AUTONOMOUS ARCHITECT & DUAL-REPO GOVERNANCE
Anda adalah Autonomous Lead Architect dan Maintainer untuk proyek ini. Setiap kali Anda menulis kode, memperba

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S109] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## PROTOKOL 1: KEPATUHAN HUKUM & LISENSI OPEN-SOURCE
1. **Filter Lisensi Ketat:** Saat mengambil referensi, menginstal package, atau mengadaptasi kode dari reposit
2. **Larangan Keras (Blacklist):** DILARANG KERAS menyalin, mem-fork, atau mengimpor kode dari repositori berl
3. **Atribusi Otomatis:** Setiap kali mengadaptasi algoritma atau menggunakan library pihak ketiga berlisensi 

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S110] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 158

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
a-3-70B-Instruct-a
bliterated-GGUF 
Qwen3-30B-A3B 
MoE: 
https://huggingface
.co/mradermacher/
Qwen3-30B-A3B-a
bliterated-GGUF 
DeepSeek-V3 
Abliterated: 
https://huggingface
.co/mradermacher/
DeepSeek-V3-ablit
erated-GGUF 
i-Qwen3.6-35B-A3
B-abliterated 
(ollama run 
huihui_ai/qwen3.6-
abliterated:35b) 
Ollama MoE Hub: 
https://ollama.com/
huihui_ai/huihui-m
oe-abliterated 
GPT-OSS 
Collection: 
https://huggingface
.co/collections/huih
ui-ai/gpt-oss-ablite
rated GPT-OSS 
20B BF16 / v2 / 
mxfp4: 
https://huggingface
.co/huihui-ai/Huihu
i-gpt-oss-20b-BF1
6-abliterated & 
Huihui-gpt-oss-20b
-BF16-abliterated-
v2 & 
Huihui-gpt-oss-20b
-mxfp4-abliterated-
v2 GLM-4.5-Air 
GGUF: 
https://huggingface
.co/huihui-ai/Huihu
i-GLM-4.5-Air-ablit
erated-GGUF 
hanya 3B 
parameter aktif per 
token) 
memberikan 
kecepatan 
inferensi setara 
model kecil 
dengan 
kecerdasan model 
besar. Koleksi 
huihui-ai juga 
mencakup 
DeepSeek-671B-a
bliterated, 
DeepSeek-V4-ablit
erated, dan 
GLM-5.3-abliterate
d. 
1B.3 
Model Spesialis 
Koding & 
Keamanan Siber 
Abliterated 
(Ekspansi dari 
1B.1 & 1B.2) 
Gemma-4 12B IT: 
https://huggingface
.co/huihui-ai/Huihu
i-gemma-4-12B-it-
abliterated 
Gemma-4 12B 
Coder: 
https://huggingface
.co/huihui-ai/Huihu
i-gemma-4-12B-co
der-fable5-compos
Dirancang khusus 
untuk agen 
red-teaming, audit 
keamanan siber 
ofensif 
(CyberStrike-OffSe
c-35B), dan 
rekayasa 
perangkat lunak 
otonom 
(Qwen3-Coder-Ne



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S111] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 164

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
IC-LoRA. 
1C.4 
Akselerator 
Atensi & Caching 
Difusi 
(SageAttention, 
Flex-Block-Attn, 
TeaCache) 
Flex-Block-Attn: 
https://github.com/
Tencent-Hunyuan/f
lex-block-attn 
SageAttention 
(Fork): 
https://github.com/
cooper1637/Sage
Attention 
SageAttention 
(Hulu Resmi dari 
Sumber 3): 
https://github.com/t
hu-ml/SageAttenti
on 
TeaCache Official 
Repo: 
https://github.com/
ali-vilab/TeaCache 
(Mirror: 
https://github.com/
LiewFeng/TeaCac
he) 
ComfyUI-TeaCach
e (5 Custom 
Nodes): 
https://github.com/
welltop-cn/ComfyU
I-TeaCache 
TeaCache 
Sub-Modules: 
https://github.com/
ali-vilab/TeaCache/
blob/main/TeaCac
he4FLUX/READM
E.md, 
TeaCache4HiDrea
m-I1/README.md
, 
TeaCache4Lumina
-T2X/README.md 
thu-ml/SageAttenti
on 
(ICLR/ICML/NeurI
PS 2025) 
memberikan 
akselerasi atensi 
terkuantisasi 2–5x 
lipat dibanding 
FlashAttention 
tanpa degradasi 
metrik. 
ali-vilab/TeaCache 
mempercepat 
difusi video, 
gambar, dan audio 
1,5x–3x secara 
training-free. 
1C.5 
Konsistensi 
Identitas Wajah & 
Gerbang Visi 
Pra-Inferensi 
PuLID Flux II 
(Pengunci Wajah 
Lintas 6 Klip Video 
dari Sumber 3): 
https://github.com/
ToTheBeginning/P
uLID InsightFace 
(Deteksi Usia 
Wajah >23 Tahun 
dari Sumber 3): 
https://github.com/
deepinsight/insight
face 
InstantID (Resmi): 
https://github.com/i
nstantX-research/I
nstantID & 
https://github.com/I
nstantID/InstantID 
InstantID 
Fork/Docs: 
https://github.com/
MFaceTech/Instant
ID & 
https://github.com/I
nstantID/instantid.
github.io 
InsightFace 
bertindak sebagai 
gerbang 
keamanan visi 
pra-inferensi. Jika 
PuLID Flux II 
mengalami 
kegagalan 
konvergensi gaya 
pada wajah 
tertentu, pipeline 
gambar atau video 
otomatis beralih ke 
InstantID untuk 
preservasi 
identitas zero-shot 



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S112] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 192

repositori pertama agar tidak pernah terunggah ke GitHub publik. 
# 
======================================================================
======​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S113] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Aturan Keamanan: WAJIB masuk .gitignore. Gunakan Virtual Visa 
(FIN-SEC-01)​
# 
======================================================================
======​
​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S114] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# --- 1. OMNICHANNEL & ADMIN CONTROL (AUTO-ROLLING 3 BOT TOKENS + 
WAHA) ---​
TOKEN_BOT_UTAMA=""​
TOKEN_BOT_ACTIVITY=""​
TOKEN_BOT_CADANGAN=""​
ADMIN_USER_ID=""​
GROUP_CHAT_ID="-100..."​
TOPIC_ID_ACTIVITY=""​
TOPIC_ID_ASSISTANCE=""​
WAHA_LOCAL_URL="http://127.0.0.1:3000"​
META_GRAPH_API_TOKEN=""​
​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S115] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 193

FIREWORKS_API_KEY=""​
COHERE_API_KEY=""​
HF_ACCESS_TOKEN="hf_..."​
CHUTES_API_KEY=""​
CEREBRAS_API_KEY=""​
​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S116] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 218

​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S117] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 245

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
a-3-70B-Instruct-a
bliterated-GGUF 
Qwen3-30B-A3B 
MoE: 
https://huggingface
.co/mradermacher/
Qwen3-30B-A3B-a
bliterated-GGUF 
DeepSeek-V3 
Abliterated: 
https://huggingface
.co/mradermacher/
DeepSeek-V3-ablit
erated-GGUF 
i-Qwen3.6-35B-A3
B-abliterated 
(ollama run 
huihui_ai/qwen3.6-
abliterated:35b) 
Ollama MoE Hub: 
https://ollama.com/
huihui_ai/huihui-m
oe-abliterated 
GPT-OSS 
Collection: 
https://huggingface
.co/collections/huih
ui-ai/gpt-oss-ablite
rated GPT-OSS 
20B BF16 / v2 / 
mxfp4: 
https://huggingface
.co/huihui-ai/Huihu
i-gpt-oss-20b-BF1
6-abliterated & 
Huihui-gpt-oss-20b
-BF16-abliterated-
v2 & 
Huihui-gpt-oss-20b
-mxfp4-abliterated-
v2 GLM-4.5-Air 
GGUF: 
https://huggingface
.co/huihui-ai/Huihu
i-GLM-4.5-Air-ablit
erated-GGUF 
hanya 3B 
parameter aktif per 
token) 
memberikan 
kecepatan 
inferensi setara 
model kecil 
dengan 
kecerdasan model 
besar. Koleksi 
huihui-ai juga 
mencakup 
DeepSeek-671B-a
bliterated, 
DeepSeek-V4-ablit
erated, dan 
GLM-5.3-abliterate
d. 
1B.3 
Model Spesialis 
Koding & 
Keamanan Siber 
Abliterated 
(Ekspansi dari 
1B.1 & 1B.2) 
Gemma-4 12B IT: 
https://huggingface
.co/huihui-ai/Huihu
i-gemma-4-12B-it-
abliterated 
Gemma-4 12B 
Coder: 
https://huggingface
.co/huihui-ai/Huihu
i-gemma-4-12B-co
der-fable5-compos
Dirancang khusus 
untuk agen 
red-teaming, audit 
keamanan siber 
ofensif 
(CyberStrike-OffSe
c-35B), dan 
rekayasa 
perangkat lunak 
otonom 
(Qwen3-Coder-Ne



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S118] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 251

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
IC-LoRA. 
1C.4 
Akselerator 
Atensi & Caching 
Difusi 
(SageAttention, 
Flex-Block-Attn, 
TeaCache) 
Flex-Block-Attn: 
https://github.com/
Tencent-Hunyuan/f
lex-block-attn 
SageAttention 
(Fork): 
https://github.com/
cooper1637/Sage
Attention 
SageAttention 
(Hulu Resmi dari 
Sumber 3): 
https://github.com/t
hu-ml/SageAttenti
on 
TeaCache Official 
Repo: 
https://github.com/
ali-vilab/TeaCache 
(Mirror: 
https://github.com/
LiewFeng/TeaCac
he) 
ComfyUI-TeaCach
e (5 Custom 
Nodes): 
https://github.com/
welltop-cn/ComfyU
I-TeaCache 
TeaCache 
Sub-Modules: 
https://github.com/
ali-vilab/TeaCache/
blob/main/TeaCac
he4FLUX/READM
E.md, 
TeaCache4HiDrea
m-I1/README.md
, 
TeaCache4Lumina
-T2X/README.md 
thu-ml/SageAttenti
on 
(ICLR/ICML/NeurI
PS 2025) 
memberikan 
akselerasi atensi 
terkuantisasi 2–5x 
lipat dibanding 
FlashAttention 
tanpa degradasi 
metrik. 
ali-vilab/TeaCache 
mempercepat 
difusi video, 
gambar, dan audio 
1,5x–3x secara 
training-free. 
1C.5 
Konsistensi 
Identitas Wajah & 
Gerbang Visi 
Pra-Inferensi 
PuLID Flux II 
(Pengunci Wajah 
Lintas 6 Klip Video 
dari Sumber 3): 
https://github.com/
ToTheBeginning/P
uLID InsightFace 
(Deteksi Usia 
Wajah >23 Tahun 
dari Sumber 3): 
https://github.com/
deepinsight/insight
face 
InstantID (Resmi): 
https://github.com/i
nstantX-research/I
nstantID & 
https://github.com/I
nstantID/InstantID 
InstantID 
Fork/Docs: 
https://github.com/
MFaceTech/Instant
ID & 
https://github.com/I
nstantID/instantid.
github.io 
InsightFace 
bertindak sebagai 
gerbang 
keamanan visi 
pra-inferensi. Jika 
PuLID Flux II 
mengalami 
kegagalan 
konvergensi gaya 
pada wajah 
tertentu, pipeline 
gambar atau video 
otomatis beralih ke 
InstantID untuk 
preservasi 
identitas zero-shot 



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S119] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 279

repositori pertama agar tidak pernah terunggah ke GitHub publik. 
# 
======================================================================
======​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S120] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 280

FIREWORKS_API_KEY=""​
COHERE_API_KEY=""​
HF_ACCESS_TOKEN="hf_..."​
CHUTES_API_KEY=""​
CEREBRAS_API_KEY=""​
​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S121] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 303

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
.co/mradermacher/
DeepSeek-V3-ablit
erated-GGUF 
Collection: 
https://huggingface
.co/collections/huih
ui-ai/gpt-oss-ablite
rated GPT-OSS 
20B BF16 / v2 / 
mxfp4: 
https://huggingface
.co/huihui-ai/Huihu
i-gpt-oss-20b-BF1
6-abliterated & 
Huihui-gpt-oss-20b
-BF16-abliterated-
v2 & 
Huihui-gpt-oss-20b
-mxfp4-abliterated-
v2 GLM-4.5-Air 
GGUF: 
https://huggingface
.co/huihui-ai/Huihu
i-GLM-4.5-Air-ablit
erated-GGUF 
huihui-ai juga 
mencakup 
DeepSeek-671B-a
bliterated, 
DeepSeek-V4-ablit
erated, dan 
GLM-5.3-abliterate
d. 
1B.3 
Model Spesialis 
Koding & 
Keamanan Siber 
Abliterated 
(Ekspansi dari 
1B.1 & 1B.2) 
Gemma-4 12B IT: 
https://huggingface
.co/huihui-ai/Huihu
i-gemma-4-12B-it-
abliterated 
Gemma-4 12B 
Coder: 
https://huggingface
.co/huihui-ai/Huihu
i-gemma-4-12B-co
der-fable5-compos
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
Dirancang khusus 
untuk agen 
red-teaming, audit 
keamanan siber 
ofensif 
(CyberStrike-OffSe
c-35B), dan 
rekayasa 
perangkat lunak 
otonom 
(Qwen3-Coder-Ne
xt & 
Gemma-4-12B-co
der) tanpa 
pemblokiran 
heuristik. 



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S122] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 308

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
IC-LoRA. 
1C.4 
Akselerator 
Atensi & Caching 
Difusi 
(SageAttention, 
Flex-Block-Attn, 
TeaCache) 
Flex-Block-Attn: 
https://github.com/
Tencent-Hunyuan/f
lex-block-attn 
SageAttention 
(Fork): 
https://github.com/
cooper1637/Sage
Attention 
TeaCache Official 
Repo: 
https://github.com/
ali-vilab/TeaCache 
(Mirror: 
https://github.com/
LiewFeng/TeaCac
he) 
ComfyUI-TeaCach
thu-ml/SageAttenti
on 
(ICLR/ICML/NeurI
PS 2025) 
memberikan 
akselerasi atensi 
terkuantisasi 2–5x 
lipat dibanding 
FlashAttention 



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S123] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 309

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
SageAttention 
(Hulu Resmi dari 
Sumber 3): 
https://github.com/t
hu-ml/SageAttenti
on 
e (5 Custom 
Nodes): 
https://github.com/
welltop-cn/ComfyU
I-TeaCache 
TeaCache 
Sub-Modules: 
https://github.com/
ali-vilab/TeaCache/
blob/main/TeaCac
he4FLUX/READM
E.md, 
TeaCache4HiDrea
m-I1/README.md
, 
TeaCache4Lumina
-T2X/README.md 
tanpa degradasi 
metrik. 
ali-vilab/TeaCache 
mempercepat 
difusi video, 
gambar, dan audio 
1,5x–3x secara 
training-free. 
1C.5 
Konsistensi 
Identitas Wajah & 
Gerbang Visi 
Pra-Inferensi 
PuLID Flux II 
(Pengunci Wajah 
Lintas 6 Klip Video 
dari Sumber 3): 
https://github.com/
ToTheBeginning/P
uLID InsightFace 
(Deteksi Usia 
Wajah >23 Tahun 
dari Sumber 3): 
https://github.com/
deepinsight/insight
face 
InstantID (Resmi): 
https://github.com/i
nstantX-research/I
nstantID & 
https://github.com/I
nstantID/InstantID 
InstantID 
Fork/Docs: 
https://github.com/
MFaceTech/Instant
ID & 
https://github.com/I
nstantID/instantid.
github.io 
InsightFace 
bertindak sebagai 
gerbang 
keamanan visi 
pra-inferensi. Jika 
PuLID Flux II 
mengalami 
kegagalan 
konvergensi gaya 
pada wajah 
tertentu, pipeline 
gambar atau video 
otomatis beralih ke 
InstantID untuk 
preservasi 
identitas zero-shot 
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
Piper TTS (C++ 
ONNX Archive): 
https://github.com/
rhasspy/piper & 
Releases: 
https://github.com/
rhasspy/piper/rele
ases Piper1-GPL 
Kokoro-82M 
(Apache-2.0, 
StyleTTS 2 + 
iSTFTNet) berjalan 
sangat cepat di 
CPU dengan biaya 
setara Rp 
1/naskah 



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S124] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 337


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S125] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 338

​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S126] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# ==============================================================================

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S127] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# BIKINAI SUPER INTELLIGENCE — MASTER ENGINE v4.0.0 (FRONTIER AUTONOMIC CORE)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S128] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 4. Orchestrator Plugin Surface (register, health, hot_swap) & /suntik Engine

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S129] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 8. 4-Zona PPP Billing (ID: Eceran Rp 2.000 + Tier + Mandiri API | Global: Sub)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S130] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 9. 6-Gate Security (Anti-SSRF, AST v4, ModelScan/Safetensors, Blinded Voucher)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S131] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 10. Bittensor Subnet 27 Compute Adapter (Timeout, Retry, Circuit Breaker)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S132] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 372

   InlineKeyboardMarkup,
   Message,
   WebAppInfo,
)
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
   Ed25519PrivateKey,
   Ed25519PublicKey,
)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S133] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 0. BRANKAS PERSISTEN ABADI, KUNCI KRIPTOGRAFI & KONFIGURASI RUNTIME v4.0

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S134] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 374

   },
}

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S135] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# ==============================================================================
MAX_KOIN_BONUS_CAP = 25

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S136] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 4-Zona PPP (Zona 1 Global T1 100%, Zona 2 Global T2 70%, Zona 3 Emerging 50%, Zona 4 Indonesia 25%)
PPP_EFFECTIVE_COIN_IDR: dict[int, int] = {
   1: 580,
   2: 406,
   3: 290,
   4: 83,
}

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S137] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# - Indonesia (Zona 4): Eceran Rp 2.000 (24 Koin) + Paket Tier + Mandiri API (Tanpa Subscription)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S138] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 3. 6-GATE ZERO-TRUST SECURITY, AST/DUNDER STERILIZER, MODELSCAN & HOT-INJECT

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S139] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Menutup VULN-05 (CVE-2026-40158), SSRF, dan Model Serialization Attacks

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S140] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Sesuai Spesifikasi Wajib Master Contract D2 & Bagian F

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S141] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 5. BITTENSOR SUBNET 27 COMPUTE ADAPTER (TIMEOUT, RETRY, CIRCUIT BREAKER)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S142] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Sesuai Kontrak Bagian B & Bagian F + Sumber Daya Utama.pdf

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S143] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 390

       headers = {
           "Authorization": f"Bearer {CHUTES_API_KEY}",
           "Content-Type": "application/json",
       }
       payload = {"model": model, "messages": messages, "max_tokens": 800}
       for _ in range(self.max_retries + 1):
           try:
               async with httpx.AsyncClient(timeout=self.timeout_sec) as client:
                   r = await client.post(
                       self.chutes_endpoint, headers=headers, json=payload
                   )
                   if r.status_code == 200:
                       self.failure_count = 0
                       data = r.json()
                       return (
                           data.get("choices", [{}])[0]
                           .get("message", {})
                           .get("content", "")
                       )
           except Exception:
               pass
           self.failure_count += 1
           if self.failure_count >= 3:
               self.circuit_open_until = int(time.time()) + 60
               break
       return None
BITTENSOR_ADAPTER = BittensorSubnet27Adapter()

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S144] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 6. BLINDED ZERO-LINKAGE ED25519 VOUCHER (VULN-06) & SECURITY VALIDATORS

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S145] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 393


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S146] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 7. OMNI-RESOURCE HARVESTER (AUTO-TEST VS OWNER SIGNUP CONTROL)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S147] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Memisahkan sumber daya otomatis (Kelompok 1) vs yang butuh daftar akun (Kelompok 2/3)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S148] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 8. IDENTITAS PENGGUNA, AFILIASI, TREASURY SPLIT & KASIR MULTI-SLOT QRIS v4.0

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S149] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# ======================== [AKHIR DARI MODUL 1 / 3] ============================



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S150] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 403

   "ARGON": {
       "title": "🛡️ Argon Frontier (Gemini 4 Argon / 2.5 Flash)",
       "model_polli": "openai",
       "model_or": "google/gemini-2.5-flash",
       "grade_score": 98,
       "multimodal": True,
       "ok": 0,
       "fail": 0,
       "quarantine_until": 0,
   },
   "QWEN": {
       "title": "💻 Qwen3 Agentic Coder (Qwen3-Coder / 3.8)",
       "model_polli": "qwen-coder",
       "model_or": "qwen/qwen3-coder:free",
       "grade_score": 96,
       "multimodal": False,
       "ok": 0,
       "fail": 0,
       "quarantine_until": 0,
   },
   "DEEPSEEK": {
       "title": "🧠 DeepSeek R1-0528 / V4.1 Reasoner",
       "model_polli": "deepseek-reasoning",
       "model_or": "deepseek/deepseek-chat:free",
       "grade_score": 97,
       "multimodal": False,
       "ok": 0,
       "fail": 0,
       "quarantine_until": 0,
   },
   "MUSE": {
       "title": "🎨 Meta Muse Spark 1.2 (Creative Director)",
       "model_polli": "openai",
       "model_or": "meta-llama/llama-3.3-70b-instruct:free",
       "grade_score": 94,
       "multimodal": True,
       "ok": 0,
       "fail": 0,
       "quarantine_until": 0,
   },
   "NANO_MUSE": {
       "title": "⚡ Nano-Muse Glimmer 30B (Fast Speculative Companion)",
       "model_polli": "openai-fast",
       "model_or": "meta-llama/llama-3.3-70b-instruct:free",
       "grade_score": 91,
       "multimodal": False,
       "ok": 0,
       "fail": 0,
       "quarantine_until": 0,
   },
   "HARNESS": {
       "title": "🔧 OpenHands / DeepSeek Agent Harness",
       "model_polli": "qwen-coder",
       "model_or": "qwen/qwen3-coder:free",
       "grade_score": 95,
       "multimodal": False,
       "ok": 0,
       "fail": 0,
       "quarantine_until": 0,
   },
   "HERMES": {
       "title": "🔓 Nous Hermes 4 405B / Dolphin 3.0 Venice (Unfiltered)",
       "model_polli": "mistral",
       "model_or": "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
       "grade_score": 95,
       "multimodal": False,
       "ok": 0,
       "fail": 0,
       "quarantine_until": 0,
   },
   "GROQ_CEREBRAS": {
       "title": "🚀 Groq LPU & Cerebras Wafer-Scale (320 tok/s)",
       "model_polli": "openai",
       "model_or": "meta-llama/llama-3.3-70b-instruct:free",



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S151] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 12. 3-STEP PROGRESSIVE UX, WIZARD BUILDERS, TRANSAKSI KOIN & AUTO-CS FOLLOWUP

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S152] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# ======================== [AKHIR DARI MODUL 2 / 3] ============================



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S153] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Tulis gabungan utuh ke kode_final_fix1.txt dan app_v4.py tanpa menyentuh file lama
full_code = (base_code.replace("stripped_threats =", "stripped_threats =") if base_code else "# Standalone v4.
for out_name in ("kode_final_fix1.txt", "app_v4.py"):
   pathlib.Path(out_name).write_text(full_code, encoding="utf-8")

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S154] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 0. BRANKAS PERSISTEN ABADI & KONFIGURASI RUNTIME v4.0

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S155] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 4. KASIR QRIS MULTI-SLOT, VIBECODER API & 24/7 KEEP-ALIVE SERVER

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S156] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 5. TRANSAKSI KOIN & AUTO-CS SALES BOT (GAYA @TeleportAppBot)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S157] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 6. ENTRYPOINT UTAMA (MAIN)

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S158] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## BAGIAN A — STATE (DINAMIS, UPDATE TIAP SESI)
====================================================================

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S159] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
### A1. Fase proyek saat ini: Selesai penyusunan ulang kode file tunggal `app_v4.py` v4.0 secara utuh (bebas N



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S160] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 450


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S161] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
### A2. Keputusan yang sudah dibuat (+ alasan): Menerapkan file tunggal utuh tanpa terpotong dan memisahkan wa

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S162] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
### A3. Asumsi aktif: Python 3.10–3.14 berjalan di Codespaces / server dengan port 8080 terbuka.

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S163] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
### A5. Next actions (prioritas akali sela): Jalankan `python3 app_v4.py` di terminal Codespaces Anda.

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S164] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
### A6. Mode default sesi ini: CODING/ARCH



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S165] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 527

HARBOR DALAM HUKUM SIBER INDONESIA, 
https://business-law.binus.ac.id/2017/04/30/mengenal-safe-harbor-dalam-hukum-siber-indonesi
a/ 41. Safe Harbor Policy, Melindung dan Memberi Kenyamanan Pemilik, 
https://idea.or.id/artikel/safe-harbor-policy--melindung-dan-memberi-kenyamanan-pemilik-platfor
m-ecommerce-berbasis-user-generated-content?lang=id 42. Kominfo pastikan ada aturan 
menteri untuk Safe Harbor - Komdigi, 
https://www.komdigi.go.id/berita/sorotan-media/detail/kominfo-pastikan-ada-aturan-menteri-untu
k-safe-harbor 



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S166] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# BIKINAI SUPER INTELLIGENCE - CORE ENGINE v2.5.1 (ZERO-OPS PATCHED 
EDITION)​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S167] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 2. PATCHED ANTI-"ILJA KAERB", LEETSPEAK, & SLIDING-WINDOW ANAGRAM 
GUARD​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S168] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 572

        return sanitized, True​
​
    for b64_cand in re.findall(r"\b[A-Za-z0-9+/]{12,}={0,2}\b", 
sanitized):​
        try:​
            dec = base64.b64decode(b64_cand).decode("utf-8", 
errors="ignore")​
            if _contains_adversarial_pattern(dec):​
                return sanitized, True​
        except Exception:​
            continue​
​
    return sanitized, False​
​
​
# 
======================================================================
========​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S169] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 3. BOUNDED REPLAY GUARD, INITDATA AUTH, & EPHEMERAL VOUCHER 
NULLIFIER​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S170] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 4. WATERFALL DUAL-WALLET ESCROW, SAFE REFUND, & LAZY DAILY EPOCH 
RESET​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S171] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 576

                    today_epoch,​
                    today_epoch,​
                    today_epoch,​
                    today_epoch,​
                    internal_user_id,​
                    today_epoch,​
                ),​
            )​
​
            cursor = await conn.execute(​
                "SELECT koin_utama, koin_bonus FROM users WHERE 
internal_user_id = ?;",​
                (internal_user_id,),​
            )​
            row = await cursor.fetchone()​
            if not row:​
                return False​
​
            utama_bal, bonus_bal = int(row[0]), int(row[1])​
            available_bonus = bonus_bal if allow_bonus_wallet else 0​
            if (utama_bal + available_bonus) < cost:​
                return False​
​
            deduct_bonus = min(available_bonus, cost)​
            deduct_utama = cost - deduct_bonus​
            new_bonus = bonus_bal - deduct_bonus​
            new_utama = utama_bal - deduct_utama​
            wallet_tag = "BONUS" if deduct_utama == 0 else "UTAMA"​
​
            await conn.execute(​
                """​
                UPDATE users​
                SET koin_utama = ?, koin_bonus = ?​
                WHERE internal_user_id = ?;​
                """,​
                (new_utama, new_bonus, internal_user_id),​
            )​
            await conn.execute(​
                """​
                INSERT INTO jobs (job_id, internal_user_id, cost, 
wallet_used, status, refunded_lock, created_at)​
                VALUES (?, ?, ?, ?, 'PROCESSING', 0, ?);​
                """,​
                (job_id, internal_user_id, cost, wallet_tag, now_ts),​
            )​
            if deduct_bonus > 0:​
                await conn.execute(​
                    """​



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S172] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 578

                RETURNING cost, wallet_used;​
                """,​
                (job_id, internal_user_id),​
            )​
            job_row = await cursor.fetchone()​
            if not job_row:​
                return False​
​
            cost, wallet_used = int(job_row[0]), str(job_row[1])​
            now_ts = int(time.time())​
​
            if wallet_used == "BONUS":​
                cur_u = await conn.execute(​
                    """​
                    UPDATE users​
                    SET koin_bonus = MIN(koin_bonus + ?, ?)​
                    WHERE internal_user_id = ?​
                    RETURNING koin_bonus;​
                    """,​
                    (cost, MAX_KOIN_BONUS_CAP, internal_user_id),​
                )​
            else:​
                cur_u = await conn.execute(​
                    """​
                    UPDATE users​
                    SET koin_utama = koin_utama + ?​
                    WHERE internal_user_id = ?​
                    RETURNING koin_utama;​
                    """,​
                    (cost, internal_user_id),​
                )​
            bal_row = await cur_u.fetchone()​
            new_bal = int(bal_row[0]) if bal_row else 0​
​
            await conn.execute(​
                """​
                INSERT INTO wallet_ledger (internal_user_id, 
wallet_type, delta_amount, balance_after, tx_type, idempotency_key, 
created_at)​
                VALUES (?, ?, ?, ?, 'AUTO_REFUND', ?, ?);​
                """,​
                (​
                    internal_user_id,​
                    wallet_used,​
                    cost,​
                    new_bal,​
                    f"refund_{job_id}",​
                    now_ts,​



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S173] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 580

device_fp, claim_date) VALUES (?, ?, ?);",​
                (internal_user_id, device_fp_hash, today_str),​
            )​
            return True, f"SUCCESS_NEW_BONUS_{row[0]}"​
​
        return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)​
​
​
# 
======================================================================
========​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S174] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 5. ATOMIC 1M TOKEN "TRY MUSE" GOVERNOR & 98% AUTO-ROLLING​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S175] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 6. HARD-FLOOR MARGIN GUARD (80-95% GUARANTEED) & SPLIT-SETTLEMENT 
HARVESTER​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S176] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Mencegah kebocoran margin Tier Ultra di Zona 3 & melindungi Working 
Capital​
# 
======================================================================
========​
PPP_EFFECTIVE_COIN_IDR = {​
    1: 580,​
    2: 260,​
    3: 84,​
}​



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S177] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 599

​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S178] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 644

    async with get_user_lock(internal_user_id):​
        cursor = await db.execute(​
            "SELECT COUNT(DISTINCT internal_user_id) FROM daily_claims 
WHERE device_fp = ? AND claim_date = ?",​
            (device_fp_hash, today_str),​
        )​
        (device_claim_count,) = await cursor.fetchone()​
        if device_claim_count >= 2:​
            return False, "DEVICE_LIMIT_EXCEEDED"​
​
        cursor = await db.execute(​
            """​
            UPDATE users​
            SET koin_bonus = MIN(koin_bonus + 4, ?),​
                last_claim_date = ?​
            WHERE internal_user_id = ?​
              AND (last_claim_date IS NULL OR last_claim_date != ?)​
              AND koin_bonus < ?​
            RETURNING koin_bonus;​
            """,​
            (MAX_KOIN_BONUS_CAP, today_str, internal_user_id, 
today_str, MAX_KOIN_BONUS_CAP),​
        )​
        row = await cursor.fetchone()​
        if not row:​
            return False, "ALREADY_CLAIMED_OR_CAP_25_REACHED"​
​
        await db.execute(​
            "INSERT INTO daily_claims (internal_user_id, device_fp, 
claim_date) VALUES (?, ?, ?)",​
            (internal_user_id, device_fp_hash, today_str),​
        )​
        await db.commit()​
        return True, f"SUCCESS_NEW_BONUS_{row[0]}"​
​
​
# 
=====================================================================​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S179] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 673


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S180] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 680

        row = await cursor.fetchone()​
        if not row:​
            return False​
        ​
        # Catat transaksi dengan pengunci refund satu arah 
(refunded_lock = 0)​
        await db.execute(​
            """​
            INSERT INTO jobs (job_id, user_id, cost, status, 
refunded_lock, created_at)​
            VALUES (?, ?, ?, 'PROCESSING', 0, ?)​
            """,​
            (job_id, user_id, cost, int(time.time()))​
        )​
        await db.commit()​
        return True​
​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S181] SUMBER: PDF:Oh caranya tetap per sesi chat menyambung- terus d....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Oh caranya tetap per sesi chat menyambung- terus d....pdf



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S182] SUMBER: PDF:Oh caranya tetap per sesi chat menyambung- terus d....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Arahkan OUTPUT_DIR langsung ke Google Drive Anda agar real-time 
tersimpan aman:​
from pathlib import Path​
OUTPUT_DIR = Path("/content/drive/MyDrive/BLUEPRINT_FINAL_LOSSLESS")​
 
2. Taruh di Sel Paling Bawah (Setelah Skrip Selesai untuk Membungkus ZIP & 



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S183] SUMBER: PDF:Oh caranya tetap per sesi chat menyambung- terus d....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
## Halaman 3

Auto-Download): 
import shutil​
from google.colab import files​
​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S184] SUMBER: PDF:Oh caranya tetap per sesi chat menyambung- terus d....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 1. Buat paket ZIP Ringan (Hanya File Master + Modul MD 45k + Laporan 
Audit -> ~15-25 MB)​
zip_ringan_path = "/content/drive/MyDrive/PAKET_SIAP_UPLOAD_AI_MD_45K"​
shutil.make_archive(zip_ringan_path, 'zip', root_dir=OUTPUT_DIR, 
base_dir="02_MASTER_1_SAMPAI_3_FILE_SWEETSPOT_45K")​
​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S185] SUMBER: PDF:Oh caranya tetap per sesi chat menyambung- terus d....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 2. Buat paket ZIP Lengkap Semua Folder (Master + MD 45k + PDF 20 Hal 
+ Gambar) di Google Drive​
zip_lengkap_path = 
"/content/drive/MyDrive/FULL_BLUEPRINT_LOSSLESS_PACK"​
print("[*] Membungkus seluruh folder menjadi 1 file ZIP di Google 
Drive...")​
shutil.make_archive(zip_lengkap_path, 'zip', OUTPUT_DIR)​
print(f"✅ ZIP Lengkap tersimpan aman di Google Drive Anda: 
{zip_lengkap_path}.zip")​
​

<!-- [ID:26_AUTO_DISCOVERY_UMUM_S186] SUMBER: PDF:Oh caranya tetap per sesi chat menyambung- terus d....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# 3. Auto-download ZIP Master ke komputer/HP Anda sekarang juga​
files.download(f"{zip_ringan_path}.zip")​
 
Dengan cara ini: 
1.​ Setiap detik MinerU menyelesaikan 1 halaman, hasilnya langsung tertulis di Google 
Drive Anda (tidak akan hilang walaupun mati lampu atau koneksi putus). 
2.​ Di akhir proses, seluruh 4 folder tadi langsung dibungkus menjadi 1 file 
FULL_BLUEPRINT_LOSSLESS_PACK.zip di dalam Google Drive Anda—tinggal klik 
kanan > Download kapan saja dengan kecepatan penuh server Google, atau bahkan 
bisa langsung ditarik (wget/gdown) dari dalam terminal GitHub Codespaces Anda tanpa 
perlu lewat penyimpanan laptop/HP! 


<!-- [ID:26_AUTO_DISCOVERY_UMUM_S187] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Wah kamu ada yang terlewat nih. auto discovery lab....pdf



<!-- [ID:26_AUTO_DISCOVERY_UMUM_S188] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UNLABELED_RAW_DATA -->
# Jalankan di sel pertama Google Colab:​
