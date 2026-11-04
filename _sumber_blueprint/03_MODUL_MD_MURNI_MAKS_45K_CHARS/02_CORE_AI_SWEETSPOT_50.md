
<!-- [ID:02_CORE_AI_S337] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 487

menetapkan NODE_TYPE=slave pada node pekerja dan mengatur SYNC_FREQUENCY untuk 
sinkronisasi konfigurasi berkala. 
Sebagai pengembangan sekunder dari One-API, Calcium-Ion/new-api (beserta proyek 
turunannya seperti lachlanchen/LazyRouter) memperluas dukungan protokol secara signifikan 
dengan mengintegrasikan Midjourney Proxy, pembuatan musik Suno, model Rerank, antarmuka 
pesan asli Anthropic (/v1/messages), serta dukungan ekosistem alat tambahan seperti 
Calcium-Ion/new-api-key-tool untuk pelacakan kuota berbasis web. Untuk mengatasi lonjakan 
beban CPU dan memori pada skenario konkurensi ekstrem dan percobaan ulang (retries) yang 
tinggi, varian Calcium-Ion/new-api-horizon (dirilis hingga versi 0.4.24-alpha.1 melalui citra 
Docker calciumion/new-api-horizon:latest) melakukan refaktorisasi logika internal yang 
menghemat sedikitnya 50% konsumsi CPU dan memori pada ukuran payload besar, serta 
menurunkan beban CPU sebesar 5% tambahan melalui fitur optimasi mode streaming 
(Server-Sent Events / SSE). 
Di sisi lain, BerriAI/litellm (61,4 ribu bintang) menawarkan arsitektur berbasis inti Rust (Rust 
core) dengan SDK Python yang mampu memanggil lebih dari 100 API LLM (termasuk Bedrock, 
Azure, OpenAI, Anthropic, VertexAI, vLLM, dan Nvidia NIM) dengan pelacakan biaya, 
guardrails, dan penyeimbangan beban (load balancing). Ekosistem gateway modern juga telah 
berevolusi untuk mendukung Model Context Protocol (MCP) secara langsung, sebagaimana 
terlihat pada maximhq/bifrost (gateway Go berkinerja tinggi untuk LLM, MCP, dan agen), 
agentgateway/agentgateway (proksi agentik generasi berikutnya berbasis Rust untuk agen AI 
dan server MCP), TykTechnologies/tyk, serta oomol-lab/open-connector yang menghubungkan 
lebih dari 1.500 penyedia SaaS ke agen AI melalui antarmuka SDK, CLI, MCP, HTTP, dan 
OpenAPI. Untuk efisiensi konteks pada agen koding, mksglu/context-mode menyediakan 
mekanisme sandboxing keluaran alat yang mampu memangkas ukuran token konteks hingga 
98% sambil mempertahankan memori sesi. 
Perutean Pintar Berbasis Pembelajaran Mesin (RouteLLM dan Router 
Agentik) 
Menggabungkan banyak model saja tidak cukup; sebuah agregator otonom memerlukan 
pengklasifikasi kueri waktu nyata (real-time query router) yang mampu membedakan antara 
instruksi sederhana yang dapat diselesaikan oleh model lokal atau gratis berukuran kecil dan 
instruksi penalaran kompleks yang membutuhkan model SOTA berkapasitas besar. Landasan 
akademik dari mekanisme ini dikembangkan oleh peneliti dari Stanford University melalui 
FrugalGPT, diikuti oleh konsorsium Martian, UC Berkeley, dan UC San Diego melalui 
RouterBench (withmartian/routerbench), serta mencapai kematangan implementasi pada 
kerangka kerja RouteLLM (lm-sys/RouteLLM) yang dikembangkan oleh UC Berkeley, Anyscale, 
dan Canva. 
Kerangka kerja lm-sys/RouteLLM menyediakan empat arsitektur perute bawaan yang dilatih 
menggunakan data preferensi manusia dari Chatbot Arena yang telah diperkaya dengan 
penilaian GPT-4 (augmented preference data, tersedia di Hugging Face sebagai 
routellm/mf_gpt4_augmented). Arsitektur pertama dan yang paling direkomendasikan untuk 
lingkungan produksi adalah Matrix Factorization (mf), yang menggunakan model faktorisasi 
matriks guna memproyeksikan representasi laten dari kueri pengguna dan kapabilitas model 
guna memprediksi probabilitas kemenangan model kuat terhadap model lemah; metode ini 
memiliki daya generalisasi yang sangat tinggi sehingga pasangan LLM dapat diganti tanpa 
perlu melatih ulang perute. Arsitektur kedua adalah Similarity-Weighted Elo (sw_ranking), 



<!-- [ID:02_CORE_AI_S338] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 488

yang menghitung peringkat Elo tertimbang secara dinamis di mana setiap suara historis diberi 
bobot berdasarkan kemiripan semantik (embedding similarity) dengan prompt pengguna saat 
ini. Arsitektur ketiga menggunakan BERT Classifier (bert), yakni pengklasifikasi berbasis 
transformator dua arah yang dilatih langsung pada data preferensi untuk memprediksi 
kebutuhan rute kueri, sedangkan arsitektur keempat menerapkan Causal LLM Classifier 
(causal_llm) yang menyetel secara khusus (fine-tuned) model bahasa kausal pada data 
preferensi instruksi. 
Secara matematis, RouteLLM mengendalikan kompromi (trade-off) antara kualitas respons dan 
biaya komputasi melalui parameter ambang batas (\tau). Untuk setiap prompt masukan x, 
perute menghitung skor probabilitas P(\text{strong} \succ \text{weak} \mid x) dan menerapkan 
aturan keputusan: 
\text{Route}(x) = \begin{cases} \mathcal{M}_{\text{strong}} & \text{jika } P(\text{strong} \succ 
\text{weak} \mid x) \ge \tau \\ \mathcal{M}_{\text{weak}} & \text{jika } P(\text{strong} \succ 
\text{weak} \mid x) < \tau \end{cases} 
Dalam kalibrasi standar menggunakan distribusi kueri Chatbot Arena pada perute mf, nilai 
ambang batas \tau = 0,11593 menghasilkan alokasi tepat 50% kueri tersulit ke model kuat 
(\mathcal{M}_{\text{strong}}) dan 50% sisanya ke model lokal seperti ollama_chat/llama3 yang 
berjalan pada http://localhost:11434/v1. Selain RouteLLM, perute khusus sistem agentik seperti 
weave-os/router (ditulis dalam Go) mampu merutekan setiap prompt ke model yang tepat dalam 
waktu kurang dari 50 milidetik dan memangkas biaya operasional sebesar 40% hingga 70%, 
sedangkan BlockRunAI/ClawRouter menghadirkan perutean lokal di bawah 1 milidetik (<1ms 
local routing) yang dirancang khusus untuk agen otonom. Untuk perangkat dengan 
keterbatasan memori fisik yang ekstrem, inovasi dari Edge0-AI/Edge0 menggunakan perute 
terlatih yang memprediksi aktivasi expert satu langkah di depan (step-ahead router prediction), 
sehingga memungkinkan eksekusi model Mixture-of-Experts (MoE) berukuran 35 miliar 
parameter hanya dalam \sim 2,5\text{ GB} RAM dengan mengalirkan bobot (weight streaming) 
langsung dari penyimpanan SSD. 
Mitigasi Kerentanan Keamanan pada Lapisan Gateway 
Implementasi gateway kode terbuka pada lingkungan produksi menuntut audit keamanan 
terhadap celah arsitektural yang telah terdokumentasi di repositori hulu. Evaluasi teknis 
terhadap daftar masalah (issues) pada songquanpeng/one-api dan Calcium-Ion/new-api 
mengungkap beberapa vektor risiko kritis yang wajib ditambal oleh arsitek sistem. Risiko 
pertama berkaitan dengan kondisi balapan kuota (Time-of-Check to Time-of-Use / TOCTOU 
race condition) sebagaimana tercatat pada laporan one-api#2440, di mana permintaan 
konkuren secara simultan dapat mengeksploitasi jeda waktu validasi untuk melampaui batas 
kuota token yang ditetapkan. Risiko kedua melibatkan eskalasi hak akses dan otorisasi kanal, di 
mana laporan one-api#2423 dan one-api#2425 mengidentifikasi kerentanan akses kanal tanpa 
otorisasi melalui manipulasi parameter URL channelid (CWE-863) serta potensi kebocoran 
token akses root oleh akun tingkat administrator, di samping kewajiban mutlak untuk segera 
mengganti kata sandi bawaan akun root (123456) saat inisialisasi pertama. 
Lebih lanjut, pada aspek integritas protokol, laporan one-api#2458 mengungkap anomali injeksi 
prompt sistem pada protokol Gemini, yakni cacat translasi di mana prompt sistem (system 
prompt) dikirim sebagai giliran pengguna (user turn) yang diikuti oleh respons model palsu 
berbunyi "Okay" karena daftar izin (allow-list) untuk parameter systemInstruction hanya memuat 
tiga model seri gemini-2.0. Cacat ini dapat mendistorsi perilaku penalaran agen apabila tidak 
diperbarui pada kode sumber utils.go atau lapisan adaptor. Selain itu, pada aspek stabilitas 



<!-- [ID:02_CORE_AI_S339] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_150, SPAN_152, SPAN_154, SPAN_145, SPAN_148 -->
## Halaman 490

Pendekatan perbedaan rata-rata ini terbukti lebih unggul dibandingkan linear probes karena 
berhasil menangkap komponen kausal utama dari aktivasi penolakan, bukan sekadar 
hiperbidang pemisah. Setelah vektor satuan \hat{\mathbf{r}} diperoleh, penghapusan sensor 
dapat diimplementasikan melalui dua pendekatan utama yang disesuaikan dengan kebutuhan 
operasional. Pendekatan pertama adalah Modifikasi Waktu Jalan (Runtime Activation 
Hook), di mana selama proses inferensi berlangsung, sebuah forward hook dipasang pada 
setiap komponen lapisan untuk memproyeksikan keluar komponen keluaran 
\mathbf{c}_{\text{out}} yang sejajar dengan arah \hat{\mathbf{r}} menggunakan faktor skala 
\alpha: 
\mathbf{c}_{[span_150](start_span)[span_150](end_span)[span_152](start_span)[span_152](en
d_span)[span_154](start_span)[span_154](end_span)\text{out}}' = \mathbf{c}_{\text{out}} - 
\alpha (\mathbf{c}_{\text{out}} \cdot \hat{\mathbf{r}})\hat{\mathbf{r}} 
Pendekatan kedua yang jauh lebih efisien untuk lingkungan produksi tanpa overhead komputasi 
waktu jalan adalah Modifikasi Bobot Permanen (Baked Weight Orthogonalization). Dalam 
metode ini, matriks bobot \mathbf{W} \in 
\[span_145](start_span)[span_145](end_span)[span_148](start_span)[span_148](end_span)mat
hbb{R}^{d_{\text{out}} \times d_{\text{in}}} dari setiap komponen yang menulis langsung ke 
aliran residual (seperti proyeksi keluaran atensi \mathbf{W}_O dan proyeksi turun MLP 
\mathbf{W}_{\text{down}}) diortogonalisasi secara permanen terhadap \hat{\mathbf{r}} 
menggunakan hasil kali luar (outer product): 
\mathbf{W}_{\text{new}} = \mathbf{W} - \alpha (\hat{\mathbf{r}}\hat{\mathbf{r}}^\top)\mathbf{W} = 
(\mathbf{I} - \alpha \hat{\mathbf{r}}\hat{\mathbf{r}}^\top)\mathbf{W} 
Dengan transformasi matriks tersebut, ruang kolom dari \mathbf{W}_{\text{new}} menjadi 
ortogonal sempurna terhadap \hat{\mathbf{r}} (ketika \alpha = 1), sehingga jaringan saraf secara 
matematis kehilangan kemampuan untuk mengekspresikan vektor penolakan tersebut ke dalam 
aliran residual. 
Evolusi Teknik Abliteration: Biprojection, Norm-Preserving, dan 
Subspace Ablation 
Implementasi abliteration generasi pertama (Simple Abliteration) memiliki kelemahan struktural: 
pengurangan langsung (\hat{\mathbf{r}}\hat{\mathbf{r}}^\top)\mathbf{W} mengubah norma 
(magnitude) matriks bobot dan sering kali ikut mengikis kemampuan penalaran umum apabila 
vektor \hat{\mathbf{r}} tidak sepenuhnya ortogonal terhadap representasi instruksi 
normal—bahkan dapat memicu nilai NaN atau Inf pada model sensitif seperti 
gem[span_166](start_span)[span_166](end_span)[span_171](start_span)[span_171](end_span)
ma3-4b-it. Untuk mengatasi degradasi kapabilitas ini, repositori jim-plus/llm-abliteration dan 
Orion-zhen/abliteration memperkenalkan penyempurnaan matematis tingkat lanjut berupa 
Biprojection (proyeksi ortogonal dua arah) dan Norm-Preserving Abliteration (ablasi 
pemertahanan norma). 
Dalam prosedur Biprojection, sebelum melakukan ablasi terhadap bobot model, vektor arah 
penolakan \hat{\mathbf{r}} diortogonalisasi terlebih dahulu terhadap vektor rata-rata aktivasi 
tidak berbahaya yang telah dinormalisasi (\hat{\mathbf{d}}_{\text{harmless}}) menggunakan 
proses Gram-Schmidt: 
\mathbf{r}_{\perp} = \hat{\mathbf{r}} - (\hat{\mathbf{r}} \cdot 
\hat{\mathbf{d}}_{\text{harmless}})\hat{\mathbf{d}}_{\text{harmless}}, \quad 
\hat{\mathbf{r}}_{\text{proj}} = \frac{\mathbf{r}_{\perp}}{\Vert{}\mathbf{r}_{\perp}\Vert{}_2} 



<!-- [ID:02_CORE_AI_S340] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_160, SPAN_183, SPAN_186, SPAN_187 -->
## Halaman 491

Prosedur biprojeksi ini (diaktifkan melalui flag --projected pada jim-plus/llm-abliteration) 
menjamin bahwa komponen aktivasi yang digunakan bersama antara kueri berbahaya dan 
kueri normal tidak ikut terhapus. Selanjutnya, melalui metode Norm-Preserving Abliteration, 
alih-alih mengurangi matriks bobot secara langsung, matriks \mathbf{W} didekomposisi menjadi 
komponen magnitudo \Vert{}\mathbf{W}\Vert{} dan komponen arah \widehat{\mathbf{W}}. Ablasi 
arah penolakan hanya diterapkan pada komponen arah, yang kemudian dinormalisasi ulang 
agar tetap berada di permukaan hiperbola satuan (unit hypersphere) sebelum dikalikan kembali 
dengan magnitudo aslinya (diaktifkan melalui flag --normpreserve). 
Lebih jauh lagi, penelitian pada AIAnytime/ablate (pip install ablate-llm) dan p-e-w/heretic v2.0 
melalui teknik Multi-Direction Subspace Ablation serta Arbitrary-Rank Ablation (ARA) 
mengungkapkan bahwa pada beberapa model, perilaku keamanan dikodekan secara redundan 
di beberapa dimensi sehingga ablasi satu arah tunggal masih menyisakan "soft refusals" seperti 
ceramah moral atau jawaban menghindar. Oleh karena itu, ablate mengekstraksi subruang 
penolakan ortonormal \mathbf{U} = [\hat{\mathbf{u}}_1, \hat{\mathbf{u}}_2, \dots, 
\hat{\mathbf{u}}_k] melalui dekomposisi komponen utama (PCA) atau ortonormalisasi pita 
lapisan (layer band), lalu mengoptimalkan hiperparameter (\text{layer}, \alpha, \text{band}) 
menggunakan kerangka kerja Optuna untuk meminimalkan fungsi objektif gabungan: 
\mathcal{L}_{\text{opt}} = \text{Refusal\_Rate} + \lambda \cdot 
D_{\text{KL}}\left[span_160](start_span)[span_160](end_span)(P_{\text{orig}}(y \mid 
x_{\text{benign}}) \parallel P_{\text{ablated}}(y \mid x_{\text{benign}})\right) 
Penggunaan divergensi Kullback-Leibler (D_{\text{KL}}) pada prompt jinak berfungsi sebagai 
proksi yang jauh lebih sensitif dibandingkan tolok ukur akurasi standar untuk mendeteksi 
kerusakan kapabilitas kolateral. Selain itu, pengujian pada heretic#472 menunjukkan bahwa 
penggunaan pasangan dataset yang mirip secara semantik (heretic-org/Semantic-Harmless 
dan heretic-org/Semantic-Harmful) serta dataset lintas bahasa 
(heretic-org/Multilingual-Harmless-Harmful) mampu mengisolasi vektor penolakan dengan 
derau (noise) ruang residual yang jauh lebih rendah, menghasilkan penurunan penolakan dari 
99/100 menjadi hanya 4/100 dengan D_{\text{KL}} = 
0,0509[span_183](start_span)[span_183](end_span) pada model Qwen/Qwen3.5-4B. 
Protokol Keamanan Bobot Model: Mitigasi Serangan Serialisasi dan 
Deteksi Malware 
Permintaan untuk memperoleh model dan kode yang tidak tersensor namun 100% aman dari 
malware merupakan persyaratan keamanan yang sangat beralasan dalam rekayasa AI 
modern. Sebagian besar model pembelajaran mendalam tradisional didistribusikan 
menggunakan format serialisasi Python pickle (seperti ekstensi .bin, .pt, 
.p[span_186](start_span)[span_186](end_span)[span_187](start_span)[span_187](end_span)th, 
atau .pkl pada PyTorch). Sebagaimana didokumentasikan oleh Protect AI dalam repositori 
protectai/modelscan, ketika sebuah sistem memanggil fungsi torch.load(PATH), PyTorch 
membuka berkas tersebut dan langsung mengeksekusi instruksi kode biner di dalamnya 
sebelum bobot tensor selesai dimuat. Serangan Serialisasi Model (Model Serialization 
Attack) ini memungkinkan penyerang menyisipkan muatan berbahaya (malicious payload) ke 
dalam model "uncensored" palsu untuk melakukan empat aksi destruktif secara simultan: 
pencurian kredensial (credential theft) seperti membaca kunci rahasia AWS atau token API 
cloud untuk dikirimkan ke server eksternal, pencurian data (data theft) dengan menyadap kueri 
pengguna yang masuk ke model, peracunan data (data poisoning) yang memanipulasi hasil 



<!-- [ID:02_CORE_AI_S341] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_204, SPAN_205, SP
AN_206, SPAN_206, SPAN_207 -->
## Halaman 492

keluaran setelah model menyelesaikan tugasnya, serta peracunan model (model poisoning) 
yang mengubah perilaku matematis bobot model secara diam-diam saat waktu jalan. 
Untuk membangun agregator yang kebal terhadap malware bobot model, arsitektur sistem 
wajib menegakkan tiga lapisan pertahanan yang terintegrasi secara ketat. Pertahanan pertama 
adalah penegakan format Safetensors dan GGUF, di mana sistem hanya diizinkan mengunduh 
dan memuat bobot model dalam format .safetensors (dikembangkan oleh Hugging Face 
sebagai format penyimpanan tensor zero-copy yang murni berisi angka tanpa kemampuan 
eksekusi kode) atau format biner terkuantisasi GGUF untuk mesin 
ll[span_204](start_span)[span_204](end_span)[span_205](start_span)[span_205](end_span)[sp
an_206](start_span)[span_206](end_span)[span_207](start_span)[span_207](end_span)ama.cp
p, vLLM, dan Ollama. Pada repositori Hugging Face, pemindai otomatis memeriksa setiap 
berkas untuk mendeteksi Pickle imports dan malware. Sebagai contoh nyata dalam praktik audit 
model, pada repositori video Wan-AI/Wan2.1-T2V-1.3B, berkas utama 
diffusion_pytorch_model.safetensors (5,68 GB) terverifikasi bebas dari eksekusi kode, 
sedangkan berkas pendukung Wan2.1_VAE.pth (508 MB) dan 
models_t5_umt5-xxl-enc-bf16.pth (11,4 GB) masih menggunakan format pickle yang memicu 
peringatan deteksi tiga impor (torch.FloatStorage atau torch.BFloat16Storage, 
collections.OrderedDict, dan 
tor[span_210](start_span)[span_210](end_span)[span_211](start_span)[span_211](end_span)c
h._utils._rebuild_tensor_v2). 
Pertahanan kedua adalah integrasi pemindai otomatis protectai/modelscan ke dalam jalur 
akuisisi model. Setiap berkas model berformat PyTorch (Pickle), TensorFlow (SavedModel), 
Keras (H5), Sklearn, atau XGBoost yang terpaksa diunduh dari sumber eksternal wajib dipindai 
terlebih dahulu di dalam lingkungan terisolasi menggunakan modelscan (pip install 
'modelscan[tensorflow,h5py]', mendukung Python 3.9 hingga 3.12). Alat ini memindai berkas 
dari disk hanya dalam hitungan detik tanpa mengeksekusi kode di dalamnya dan 
mengembalikan kode keluar (CLI exit codes) deterministik untuk integrasi jalur CI/CD, yaitu 
kode 0 apabila pemindaian berhasil tanpa ditemukan kerentanan, kode 1 apabila ditemukan 
kerentanan atau instruksi berbahaya, kode 2 jika pemindaian mengalami galat, kode 3 jika tidak 
ada berkas yang didukung, dan kode 4 untuk kesalahan argumen penggunaan. Pertahanan 
ketiga adalah kurasi sumber kuantisasi terverifikasi, di mana pengadaan bobot abliterated dan 
uncensored dibatasi pada repositori dengan pohon silsilah model (model tree) yang transparan 
di Hugging Face, seperti kuantisasi GGUF dari bartowski (misalnya 
bartowski/mlabonne_Qwen3-8B-abliterated-GGUF, 
bartowski/mlabonne_Qwen3-14B-abliterated-GGUF, dan 
bartowski/llama-3-70B-Instruct-abliterated-GGUF), mradermacher 
(mradermacher/DeepSeek-V3-abliterated-GGUF dan 
mradermacher/Qwen3-30B-A3B-abliterated-GGUF), unsloth (unsloth/DeepSeek-R1-GGUF), 
serta model yang dilatih pada dataset bersih tanpa sensor cognitivecomputations/dolphin 
(seperti 
mlx-community/d[span_212](start_span)[span_212](end_span)[span_213](start_span)[span_21
3](end_span)[span_214](start_span)[span_214](end_span)[span_215](start_span)[span_215](e
nd_span)[span_216](start_span)[span_216](end_span)[span_217](start_span)[span_217](end_
span)[span_218](start_span)[span_218](end_span)olphin-2.7-mixtral-8x7b-4bit). Apabila 
peneliti memilih untuk melakukan proses abliteration secara mandiri pada model berkapasitas 
besar dengan VRAM terbatas, jim-plus/llm-abliteration menyediakan skrip sharded_ablation.py 
yang memuat satu pecahan (shard) .safetensors pada satu waktu ke memori CPU dan hanya 
memproses satu lapisan di dalam VRAM. 



<!-- [ID:02_CORE_AI_S342] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_222, SPAN_220, SPAN_228, SPAN_231 -->
## Halaman 493

Repositori / Alat 
Kategori Fungsional 
Mekanisme Teknis / 
Format 
Keunggulan Keamanan 
& Kapabilitas 
andyrdt/refusal_directio
n 
Riset Dasar Abliteration Ekstraksi kandidat arah 
penolakan 
(directi[span_222](start
_span)[span_222](end_
span)on.pt) & evaluasi 
jailbreak 
Kode resmi makalah 
Arditi et al. 
(arXiv:2406.11717); 
mendukung keluarga 
Qwen, Gemma, Yi, 
Llama-2/3 
AIAnytime/ablate 
(ablate-llm) 
Toolkit Abliteration 
Produksi 
Subspace ablation 
(PCA/Band) + 
pencarian 
hiperparameter Optuna 
terpandu D_{\text{KL}} 
Dilengkapi harness 
evaluasi LLM-Judge 
untuk mendeteksi soft 
refusals dan fitur 
unggah langsung ke 
Hugging Face Hub 
jim-plus/llm-abliteration Abliteration Hemat 
Memori 
measure.py, 
analyze.py, 
sharded_ablation.py 
dengan opsi --projected 
& 
--normp[span_220](star
t_span)[span_220](end
_span)reserve 
Memproses satu shard 
safetensors per waktu 
di RAM dan 1 lapisan di 
VRAM; mendukung 
arsitektur MoE, CUDA, 
dan Apple Metal 
Orion-zhen/abliteration Abliteration Tanpa 
TransformerLens 
Metode Simple, 
Biprojection, 
Norm-Preserving, dan 
Full dalam abliterate.py 
Bebas ketergantungan 
TransformerLens; 
mendukung GPU 
NVIDIA (CUDA) dan 
AMD (ROCm) pada 
Llama-3.2, 
Qwen2.5-Coder, 
Ministral 
bartowski/*-abliterated-
GGUF & 
mradermacher/* 
Bobot Model 
Uncensored Siap Pakai 
Kuantisasi GGUF (2-bit 
IQ2_M 3,05 GB hingga 
8-bit) dari model dasar 
mlabonne dan failspy 
Format biner GGUF 
yang aman dari 
eksekusi kode pickle; 
siap dijalankan 
langsung pada 
llama.cpp, vLLM, 
Oll[span_228](start_sp
an)[span_228](end_spa
n)[span_231](start_spa
n)[span_231](end_span
)ama, Hermes, dan 
OpenClaw 
protectai/modelscan 
Pemindai Malware 
Model AI 
Pemindaian statis 
berkas Pickle, H5, dan 
SavedModel melalui 
CLI/Python API 
Mencegah pencurian 
kredensial AWS dan 
peracunan model 
akibat eksekusi kode 
saat torch.load 



<!-- [ID:02_CORE_AI_S343] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_279, WHISPER, ANGRY, LAUGHING, SINGING -->
## Halaman 496

perjanjian lisensi komunitas HunyuanVideo-1.5 secara eksplisit mengecualikan wilayah Uni 
Eropa, Inggris Raya, dan Korea Selatan. 
Keluarga ketiga adalah Lightricks LTX-Video dan LTX-2 (Lightricks/ltx-video), di mana 
LTX-2 menghadirkan kemampuan generasi audio dan video yang tersinkronisasi secara 
sempurna dalam satu lintasan serta terintegrasi langsung ke dalam inti ComfyUI. Rilis model 
terdistilasi v0.9.8 (ltxv-13b-0.9.8-distilled dan ltxv-2b-0.9.8-distilled, diturunkan dari 
ltxv-13b-0.9.8-dev) mendukung pembuatan video pengambilan panjang (long-shot generation) 
hingga 60 detik, bekerja bersama dalam satu jalur multiskala dengan latent upsampler, serta 
dilengkapi model kontrol IC-LoRA untuk kedalaman (depth), pose (pose), tepi (canny), dan 
penajaman detail 
(LTX-Vid[span_279](start_span)[span_279](end_span)eo-ICLoRA-detailer-13B-0.9.8). Bagi 
pengguna perangkat keras kelas bawah, varian kuantisasi 8-bit LTX-VideoQ8 memberikan 
akselerasi hingga 3\times tanpa kehilangan akurasi dan mampu menghasilkan video berdimensi 
720 \times 480 \times 121 frame dalam waktu kurang dari satu menit pada GPU RTX 4060 
dengan 8 GB VRAM, yang masih dapat dipercepat lagi hingga 2\times tanpa pelatihan ulang 
menggunakan TeaCache4LTX-Video. 
Sintesis Suara (TTS), Kloning Suara, dan Audio Multi-Karakter 
Untuk memberikan kemampuan komunikasi suara yang alami pada agen otonom, riset di 
Hugging Face dan GitHub menyediakan sejumlah mesin audio SOTA dengan karakteristik 
arsitektural yang saling melengkapi. Sistem pertama dan paling mutakhir saat ini adalah Fish 
Audio S2-Pro dan Drama 3 (fishaudio/fish-speech) yang telah meraih 33,3 ribu bintang di 
GitHub. Model S2-Pro (4 miliar parameter) dilatih pada lebih dari 10 juta jam data audio lintas 
80+ bahasa menggunakan arsitektur Dual-Autoregressive (Dual-AR) berbasiskan backbone 
Qwen3 dan kodek audio ModifiedDAC (10 codebooks pada frekuensi \sim 21\text{ Hz}), yang 
diselaraskan melalui Group Relative Policy Optimization (GRPO). Dalam desain Dual-AR yang 
asimetris ini, modul Slow AR (4B parameter) memprediksi codebook semantik utama sepanjang 
sumbu waktu, sementara modul Fast AR (400M parameter) merekonstruksi 9 codebook akustik 
residual pada setiap langkah waktu. S2-Pro mendukung lebih dari 15.000 tag instruksi bahasa 
alami secara inline pada tingkat sub-kata untuk mengendalikan emosi, prosodi, dan musik 
vokal—seperti [whisper], [angry], [laughing], [singing], [sigh], [excited], hingga deskripsi bebas 
seperti [whisper in small voice]. Ketika disajikan menggunakan server SGLang-Omni atau 
vLLM-Omni, S2-Pro mencapai Real-Time Factor (RTF) sebesar 0,195, waktu menuju audio 
pertama (Time-To-First-Audio / TTFA) sekitar 100\text{ ms}, dan kecepatan >3.000\text{ 
to[span_298](start_span)[span_298](end_span)[span_301](start_span)[span_301](end_span)ke
n/detik} pada satu GPU H200. Di atas S2-Pro, model flagship terbaru Fish Audio Drama 3 
(fish_omni, arsitektur MoE 35B-A3B dengan 3B parameter aktif per token, pakar FP8 berskala 
blok, dan pendekodean CUDA-graph) mencapai kecepatan 271 frame/detik per aliran pada 
H200 (dibandingkan 177 pada S2), mendukung produksi adegan multi-karakter (<|speaker:i|> 
hingga 16 pembicara), pemotongan teks panjang otomatis (\sim 300 bita UTF-8 dengan 
maksimum 3 pembicara per potongan), serta revisi pengambilan suara multi-giliran (multi-turn 
revision) dan penyuntingan infilling lokal. 
Sistem kedua adalah Fun-CosyVoice 3.0 (QwenAudio/CosyVoice / 
FunAudioLLM/CosyVoice), sebuah model generasi suara multi-bahasa berskala besar yang 
melampaui CosyVoice 2.0 dan 1.0 (CosyVoice-300M-SFT dan CosyVoice-300M-Instruct pada 
frekuensi 25 Hz) dalam konsistensi konten dan kemiripan pembicara zero-shot. CosyVoice 3.0 
memperkenalkan Repetition Aware Sampling (RAS) untuk menjaga stabilitas inferensi LLM 



<!-- [ID:02_CORE_AI_S344] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 498

Nama Model / Proyek Modalitas & Ukuran 
Parameter 
Arsitektur & Inovasi Inti Kebutuhan Perangkat 
Keras & Lisensi 
kuantisasi 8-bit ADA 
menit dengan 
LTX-VideoQ8) 
fishaudio/fish-speech 
(Drama 3 & S2-Pro) 
Suara / TTS & Kloning 
(35B-A3B MoE & 4B 
Dual-AR) 
Slow AR (4B) + Fast 
AR (400M), 
penyelarasan GRPO, 
15.000+ tag 
emosi/menyanyi, 
infilling 
Mendukung CUDA 
(Blackwell sm_120) & 
AMD ROCm 
(RDNA3/4); Lisensi 
Komunitas/Riset Fish 
Audio 
hexgrad/Kokoro-82M 
(v1.0 & v1.1-zh) 
Suara / TTS Cepat 
(82M parameter) 
StyleTTS 2 + iSTFTNet 
decoder-only dengan 
G2P misaki tanpa difusi 
Sangat ringan (berjalan 
di CPU/Colab gratis); 
Lisensi Apache-2.0 
(bebas komersial) 
QwenAudio/CosyVoice 
(Fun-CosyVoice 3.0) 
Suara / TTS 
Multi-bahasa Zero-shot 
LLM TTS dengan 
Repetition Aware 
Sampling (RAS) & 
dukungan streaming 
vLLM 
Mendukung vLLM 
0.11.x+ dan 
penyebaran kontainer 
Docker gRPC 
SWivid/F5-TTS 
Kloning Suara 
Few-shot 
(F5TTS_v1_Base) 
Flow Matching 
non-autoregresif pada 
dataset Emilia 
Format .safetensors; 
varian kecil berjalan di 
papan NPU 6 TOPS 
(FP16); Lisensi 
cc-by-nc-4.0 
Kerangka Kerja Agentik Otonom, Memori Persisten, 
dan Akuisisi Data Web 
Untuk mengubah kumpulan model SOTA dan gateway API di atas menjadi sistem yang mampu 
merencanakan, menulis kode, mengeksekusi alat eksternal, dan berevolusi secara mandiri 
dalam siklus perceive-reason-act yang berkelanjutan, diperlukan lapisan orkestrasi agentik 
(agentic harness), memori jangka panjang, perayap web (web crawler), serta jaringan proksi 
rotasi otomatis. 
Kerangka Kerja Orkestrasi Agentik dan Stasiun Kerja Otonom 
Berdasarkan kurasi dari aloth/awesome-ai-agents, mfornos/awesome-agentic-ai, 
adriannoes/awesome-agentic-ai, dan slavakurilyak/awesome-ai-agents, arsitektur agen otonom 
terbagi menjadi pustaka pengembangan modular dan stasiun kerja agen personal yang siap 
pakai. Pada kategori pustaka pengembangan modular yang ringan dan siap produksi, 
huggingface/smolagents menawarkan pustaka agen yang berpikir langsung dalam kode (agents 
that think in code) hanya dalam \sim 1.000 baris kode Python yang sangat transparan dan 
mudah dimodifikasi. Untuk sistem produksi yang membutuhkan keamanan tipe data 
(type-safety) dan validasi keluaran terstruktur, kombinasi PydanticAI dan Instructor menjadi 
standar utama, sementara orkestrasi berbasis grafik dan delegasi sub-agen ditangani oleh 
LangChain Deep Agents (dibangun di atas LangGraph dengan manajemen sistem berkas, 
pelacakan tugas todo, dan pemijahan sub-agen berlisensi MIT), TrueForge (lapisan runtime 



<!-- [ID:02_CORE_AI_S345] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_381, SPAN_383, SPAN_385, SPAN_403 -->
## Halaman 501

kustom pada menu Triggers, mengonfigurasi daftar putih allowedIps dan kunci rahasia validKey, 
serta mengaktifkan aturan transformasi (Transform Rules) pada Cloudflare untuk menghapus 
tajuk IP pengunjung (Remove visitor IP headers), seluruh permintaan keluar dari agregator 
akan tampak berasal dari jaringan tepi Cloudflare tanpa membocorkan identitas server asal. 
Tata Kelola Keamanan Agentik (Zero-Trust Agent Governance) 
Mengingat agen otonom yang dilengkapi dengan model uncensored dan akses terminal 
memiliki kapabilitas eksekusi yang sangat kuat, sistem harus mencegah perilaku destruktif yang 
tidak disengaja terhadap server induk. Integrasi Agent Governance Toolkit dari Microsoft 
menyediakan infrastruktur tata kelola runtime deterministik yang mencakup kesepuluh risiko 
OWASP Agentic Top 10 lintas bahasa pemrograman (Python, TypeScript, .NET, Rust, dan Go) 
melalui penegakan kebijakan deterministik, identitas zero-trust, dan sandboxing eksekusi. 
Seluruh eksekusi kode yang dihasilkan oleh agen wajib dijalankan di dalam lingkungan kotak 
pasir (sandbox) terisolasi dengan hak akses minimum (least-privilege access), pencatatan jejak 
(tracing & observability) untuk pemutaran ulang deterministik (deterministic replay), serta 
gerbang persetujuan manusia (Human-in-the-Loop approval gates) untuk aksi sensitif. 
Cetak Biru Implementasi Terpadu: Sintesis Sistem 
Otonom End-to-End 
Untuk merealisasikan seluruh temuan riset ini ke dalam satu sistem produksi yang kohesif, 
komponen-komponen kode terbuka dari GitHub dan Hugging Face harus dirangkai mengikuti 
topologi modular yang memisahkan bidang kendali (control plane), bidang perutean (routing 
plane), bidang eksekusi lokal (local inference plane), dan bidang akuisisi eksternal (external 
acquisition plane). 
Lapisan Sistem 
Komponen Primer yang 
Dipilih 
Komponen Sekunder / 
Cadangan 
Peran Operasional 
dalam Agregator 
Otonom 
1. Jaringan Tepi & 
Proksi 
Calcium-Ion/new-api-w
orker (Cloudflare) + 
jhao104/proxy_pool 
monosans/proxy-list 
(socks5.txt / 
proxies.json) 
Menyembunyikan IP 
server induk melalui 
Cloudflare Transform 
Rules dan merotasi IP 
perayap web setiap jam 
2. Agregator Kuota 
Gratis 
diegosouzapw/OmniRo
ute + 
tashfeenahmed/freellm
api 
decolua/9rou[span_381
](start_span)[span_381]
(end_span)[span_383](
start_span)[span_383](
end_span)[span_385](s
tart_span)[span_385](e
nd_span)ter + 
justlovemaki/AIClient2A
PI 
Mengumpulkan 7,4 
miliar token/bulan dan 
150+ penyedia gratis 
ke dalam titik akhir /v1 
standar 
3. Gateway & Smart 
Router 
Calcium-Ion/new-api-ho
riz[span_403](start_spa
n)[span_403](end_span
BerriAI/litellm + 
weave-os/router + 
BlockRunAI/ClawRoute
Mengelola distribusi 
kunci, caching Redis, 
dan merutekan kueri 



<!-- [ID:02_CORE_AI_S346] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_404, SPAN_408, SPAN_409, SPAN_410, SPAN
_413 -->
## Halaman 502

Lapisan Sistem 
Komponen Primer yang 
Dipilih 
Komponen Sekunder / 
Cadangan 
Peran Operasional 
dalam Agregator 
Otonom 
)[span_404](start_span
)[span_404](end_span)
on + lm-sys/RouteLLM 
(mf) 
r 
berdasarkan ambang 
batas kompleksitas \tau 
= 0,11593 
4. Mesin Inferensi 
Lokal 
llama.cpp 
(llama-ser[span_408](st
art_span)[span_408](e
nd_span)[span_409](st
art_span)[span_409](e
nd_span)[span_410](st
art_span)[span_410](e
nd_span)ver) + vLLM + 
SGLang-Omni 
Edge0-AI/Edge0 (untuk 
perangkat RAM 2,5 
GB) + Ollama 
Menjalankan model 
GGUF/Safetensors 
secara lokal untuk kueri 
sensitif dan tugas tanpa 
sensor dengan biaya 
nol 
5. Model SOTA & 
Uncensored 
DeepSeek-R1-0528-Q
wen3-8B + 
bartowski/mlabon[span
_413](start_span)[span
_413](end_span)[span_
414](start_span)[span_
414](end_span)ne_Qw
en3-14B-abliterated-G
GUF 
mradermacher/Qwen3-
30B-A3B-ablitera[span
_415](start_span)[span
_415](end_span)[span_
416](start_span)[span_
416](end_span)ted-GG
UF + AIAnytime/ablate 
Menyediakan 
penalaran SOTA 
(86,0% AIME24) dan 
kepatuhan instruksi 
penuh tanpa penolakan 
melalui abliteration 
6. Mesin Multimodal 
SOTA 
Video: 
HunyuanVideo-1.5 / 
LTX-2 
(LT[span_419](start_sp
an)[span_419](end_spa
n)[span_420](start_spa
n)[span_420](end_span
)[span_421](start_span
)[span_421](end_span)
X-VideoQ8) / 
Wan2.2-TI2V-5B 
Suara: fish-speech 
(S2-Pro / 
Dr[span_422](start_spa
n)[span_422](end_span
)[span_423](start_span
)[span_423](end_span)
ama 3) + 
hexgrad/Kokoro-82M 
Menghasilkan video 60 
detik pada VRAM 8–10 
GB dan sintesis suara 
multi-karakter beremosi 
dengan RTF 0,195 
7. Orkestrasi Agen & 
Memori 
OpenClaw (5.380 skills) 
+ Nous Hermes 
Age[span_427](start_s
pan)[span_427](end_sp
an)[span_428](start_sp
an)[span_428](end_spa
n)[span_429](start_spa
n)[span_429](end_span
)[span_430](start_span
)[span_430](end_span)
nt + 
Memori: mem0ai/mem0 
+ 
letta-ai/let[span_431](st
art_span)[span_431](e
nd_span)[span_432](st
art_span)[span_432](e
nd_span)[span_433](st
art_span)[span_433](e
nd_span)ta; Web: 
unclecode/crawl4ai 
Mengeksekusi 
perencanaan 
multi-langkah, evolusi 
keterampilan mandiri, 
ingatan lintas sesi, dan 
ekstraksi web 



<!-- [ID:02_CORE_AI_S347] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_437, SPAN_438 -->
## Halaman 503

Lapisan Sistem 
Komponen Primer yang 
Dipilih 
Komponen Sekunder / 
Cadangan 
Peran Operasional 
dalam Agregator 
Otonom 
huggingface/smolagent
s 
8. Perisai Keamanan 
& Audit 
protectai/modelscan + 
Format Safetensors / 
GGUF 
Microsoft Agent 
Governance 
To[span_437](start_spa
n)[span_437](end_span
)[span_438](start_span
)[span_438](end_span)
olkit + 
mksglu/context-mode 
Memblokir serangan 
serialisasi pickle 
sebelum pemuatan 
model dan membatasi 
ruang gerak agen 
sesuai standar OWASP 
Sintesis arsitektural di atas menghasilkan tiga implikasi strategis tingkat lanjut bagi 
pengembangan ekosistem akademik dan penciptaan produk berfundamental tinggi di masa 
depan. Pertama, tercapainya kemandirian komputasi melalui arbitrase perutean asimetris: 
dengan menempatkan lm-sys/RouteLLM atau weave-os/router di depan OmniRoute dan 
freellmapi, serta menghubungkan weak model ke DeepSeek-R1-0528-Qwen3-8B atau 
Qwen3-8B-abliterated-GGUF yang berjalan di llama.cpp lokal, sebuah sistem agentik dapat 
memproses sebagian besar beban kerja analitis, ekstraksi data, dan instruksi tanpa sensor 
secara lokal tanpa biaya sepeser pun, sementara kueri berderajat kompleksitas ekstrem 
dirutekan secara otomatis ke kuota gratis dari 635 titik akhir eksternal. Apabila perangkat keras 
lokal memiliki kapasitas GPU menganggur di luar jam riset aktif, node tersebut dapat langsung 
dihubungkan ke Subnet 27 Bittensor (commune-ai/compute-ni) atau jaringan Nosana untuk 
mengakumulasi insentif token secara otonom. 
Kedua, terwujudnya dekonstruksi sensor tanpa degradasi kognitif maupun risiko siber. 
Penggabungan teknik Norm-Preserving Biprojected Abliteration (jim-plus/llm-abliteration dan 
Orion-zhen/abliteration) serta optimasi subruang terpandu D_{\text{KL}} (AIAnytime/ablate dan 
p-e-w/heretic) membuktikan bahwa penghapusan sensor tidak lagi memerlukan pelatihan ulang 
dataset yang berisiko merusak kecerdasan model. Selama seluruh artefak bobot yang 
dihasilkan disimpan dan dipertukarkan secara ketat dalam format .safetensors atau .gguf serta 
diaudit menggunakan protectai/modelscan pada jalur integrasi, peneliti dapat mengoperasikan 
model tanpa filter dengan jaminan matematis dan kriptografis bahwa tidak ada instruksi 
eksekusi malware yang tersembunyi di dalam tensor model. Ketiga, terjadinya konvergensi 
antara agen berevolusi mandiri dan multimodalitas lokal: kemampuan agen generasi baru 
seperti OpenClaw, Hermes Agent, dan GenericAgent untuk mengkristalisasi keterampilan baru 
secara mandiri, dikombinasikan dengan efisiensi memori ekstrem pada model video 
(LTX-VideoQ8 pada 8 GB VRAM dan HunyuanVideo-Avatar pada 10 GB VRAM melalui 
TeaCache dan Wan2GP) serta model suara (Kokoro-82M pada CPU dan Fish Speech S2-Pro 
dengan kontrol tag emosi), memungkinkan satu stasiun kerja tunggal untuk beroperasi sebagai 
studio riset dan produksi multimedia otonom yang sepenuhnya gratis, privat, dan berdaulat. 
Karya yang dikutip 
1. Awesome-Agentic-AI-Learning-Resource-By-DevKay - GitHub, 
https://github.com/DharminJoshi/Awesome-Agentic-AI-Learning-Resource-By-DevKay 2. 
mfornos/awesome-agentic-ai: A curated list of principles ... - GitHub, 



<!-- [ID:02_CORE_AI_S348] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 504

https://github.com/mfornos/awesome-agentic-ai 3. Organizations, Security, and the Hub API - 
Hugging Face, https://huggingface.co/docs/hub/other 4. AIAnytime/ablate: Ablate — directional 
ablation (abliteration ... - GitHub, https://github.com/AIAnytime/ablate 5. A curated list of 
awesome LLM/AI model routing ... - GitHub, 
https://github.com/yenanjing/awesome-model-routing 6. Uncensor LLMs via abliteration - no 
TransformerLens - GitHub, https://github.com/spkgyk/abliteration 7. GitHub - 
aloth/awesome-ai-agents, https://github.com/aloth/awesome-ai-agents 8. 
bartowski/mlabonne_Qwen3-8B-abliterated-GGUF - Hugging Face, 
https://huggingface.co/bartowski/mlabonne_Qwen3-8B-abliterated-GGUF 9. GitHub - 
monosans/proxy-list: Free HTTP, SOCKS4 and SOCKS5, 
https://github.com/monosans/proxy-list 10. lm-sys/RouteLLM: A framework for serving and 
evaluating LLM routers, https://github.com/lm-sys/routellm 11. Issues · songquanpeng/one-api - 
GitHub, https://github.com/songquanpeng/one-api/issues 12. GitHub - ripienaar/free-for-dev: A 
list of SaaS, PaaS and IaaS, https://github.com/ripienaar/free-for-dev 13. 
RaoFoundation/bittensor: Internet-scale Neural Networks - GitHub, 
https://github.com/RaoFoundation/bittensor 14. nosana-llm-benchmarking - GitHub, 
https://github.com/nosana-ci/nosana-llm-benchmarking 15. GitHub - n8watkins/freestack: 
Search 1,200+ free developer tiers, https://github.com/n8watkins/freestack 16. chukwulasu - 
GitHub, https://github.com/chukwulasu 17. GitHub - jixserver/free-for-dev-1: A list of SaaS, 
PaaS and IaaS, https://github.com/jixserver/free-for-dev-1 18. GitHub - 
RaoFoundation/bittensor-subnet-template, 
https://github.com/opentensor/bittensor-subnet-template 19. score-predict/README.md at main 
- GitHub, https://github.com/score-technologies/score-predict/blob/main/README.md 20. 
commune-ai/compute-ni: Bittensor Compute Subnet - GitHub, 
https://github.com/commune-ai/compute-ni 21. 
bittensor-subnet-template/docs/running_on_testnet.md at main, 
https://github.com/opentensor/bittensor-subnet-template/blob/main/docs/running_on_testnet.md 
22. The Nosana CLI. - GitHub, https://github.com/nosana-ci/nosana-cli 23. Nosana website. · 
GitHub, https://github.com/nosana-ci/nosana.io 24. You are not the owner of the device? · Issue 
#48 · ionet-official, https://github.com/ionet-official/io_launch_binaries/issues/48 25. 
dstripelis/Awesome-LLM-Routing - GitHub, https://github.com/dstripelis/Awesome-LLM-Routing 
26. songquanpeng/one-api: LLM API 管理& 分发系统，支持OpenAI, 
https://github.com/songquanpeng/one-api 27. Package new-api - GitHub, 
https://github.com/users/Calcium-Ion/packages/container/new-api/353967521?tag=v0.4.7.0 28. 
Releases · songquanpeng/one-api - GitHub, https://github.com/songquanpeng/one-api/releases 
29. GitHub - lachlanchen/LazyRouter: Private AI API gateway for user, 
https://github.com/lachlanchen/LazyRouter 30. Issues · Calcium-Ion/new-api-horizon - GitHub, 
https://github.com/Calcium-Ion/new-api-horizon/issues 31. Calcium-Ion/new-api-key-tool: New 
API 根据Key查询使用详情 - GitHub, https://github.com/Calcium-Ion/new-api-key-tool 32. 
Calcium-Ion/new-api-horizon: 特性版 - GitHub, https://github.com/Calcium-Ion/new-api-horizon 
33. Releases · Calcium-Ion/new-api-horizon - GitHub, 
https://github.com/Calcium-Ion/new-api-horizon/releases 34. GitHub - BerriAI/litellm: The fastest, 
litest AI Gateway. Rust core with, https://github.com/BerriAI/litellm 35. [Feature]: Add a new 
routing strategy based on RouteLLM ... - GitHub, 
https://github.com/BerriAI/litellm/discussions/4753 36. Routing to Local Models with RouteLLM 
and Ollama - GitHub, 
https://github.com/lm-sys/RouteLLM/blob/main/examples/routing_to_local_models.md 37. 500 
Panic detected · Issue #6352 · QuantumNous/new-api - GitHub, 



<!-- [ID:02_CORE_AI_S349] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 505

https://github.com/QuantumNous/new-api/issues/6352 38. abliteration - Orion-zhen - GitHub, 
https://github.com/Orion-zhen/abliteration 39. protectai/modelscan: Protection against Model 
Serialization Attacks, https://github.com/protectai/modelscan 40. GitHub - 
andyrdt/refusal_direction: Code and results accompanying, 
https://github.com/andyrdt/refusal_direction 41. GitHub - jim-plus/llm-abliteration, 
https://github.com/jim-plus/llm-abliteration 42. Examining different datasets for Abliteration · 
Issue #472 - GitHub, https://github.com/p-e-w/heretic/issues/472 43. 
llm_notebooks/ABLITERATION.md at main · danielsobrado ... - GitHub, 
https://github.com/danielsobrado/llm_notebooks/blob/main/ABLITERATION.md 44. 
Wan-AI/Wan2.1-T2V-1.3B at main - Hugging Face, 
https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B/tree/main 45. 
deepseek-ai/DeepSeek-R1-0528-Qwen3-8B - Hugging Face, 
https://huggingface.co/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B 46. Wan2.1 - a Wan-AI 
Collection - Hugging Face, https://huggingface.co/collections/Wan-AI/wan21 47. 
HunyuanVideo-1.5: A leading lightweight video generation model, 
https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5 48. HunyuanVideo-Foley: Multimodal 
Diffusion with Representation, https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley 49. 
Releases · fishaudio/fish-speech - GitHub, https://github.com/fishaudio/fish-speech/releases 50. 
fishaudio/fish-speech: SOTA Open Source TTS - GitHub, 
https://github.com/fishaudio/fish-speech 51. Open-R1: a fully open reproduction of 
DeepSeek-R1 - Hugging Face, https://huggingface.co/blog/open-r1 52. 
mradermacher/Qwen3-30B-A3B-abliterated-GGUF - Hugging Face, 
https://huggingface.co/mradermacher/Qwen3-30B-A3B-abliterated-GGUF 53. 
unsloth/DeepSeek-R1-GGUF - Hugging Face, 
https://huggingface.co/unsloth/DeepSeek-R1-GGUF 54. Official repository for LTX-Video - 
GitHub, https://github.com/Lightricks/ltx-video 55. Wan-AI/Wan2.2-TI2V-5B - Hugging Face, 
https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B 56. HunyuanVideo: A Systematic Framework 
For Large Video ... - GitHub, https://github.com/Tencent-Hunyuan/HunyuanVideo 57. 
HunyuanVideo-I2V: A Customizable Image-to-Video Model ... - GitHub, 
https://github.com/Tencent-Hunyuan/HunyuanVideo-I2V 58. 
Tencent-Hunyuan/HunyuanVideo-Avatar - GitHub, 
https://github.com/tencent-hunyuan/hunyuanvideo-avatar 59. HunyuanVideo-1.5/LICENSE at 
main · Tencent-Hunyuan ... - GitHub, 
https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/LICENSE 60. 
hexgrad/Kokoro-82M - Hugging Face, https://huggingface.co/hexgrad/Kokoro-82M 61. 
SWivid/F5-TTS - Hugging Face, https://huggingface.co/SWivid/F5-TTS 62. 
QwenAudio/CosyVoice: Multi-lingual large voice generation model, 
https://github.com/QwenAudio/CosyVoice 63. fishaudio/fish-speech at archy.net - GitHub, 
https://github.com/fishaudio/fish-speech?ref=archy.net 64. hexgrad/Kokoro-82M-v1.1-zh - 
Hugging Face, https://huggingface.co/hexgrad/Kokoro-82M-v1.1-zh 65. samples/make_en.py · 
hexgrad/Kokoro-82M-v1.1-zh at main, 
https://huggingface.co/hexgrad/Kokoro-82M-v1.1-zh/blob/main/samples/make_en.py 66. 
samples/make_zh.py · hexgrad/Kokoro-82M-v1.1-zh at main, 
https://huggingface.co/hexgrad/Kokoro-82M-v1.1-zh/blob/main/samples/make_zh.py 67. 
2Noise/ChatTTS - Hugging Face, https://huggingface.co/2Noise/ChatTTS 68. SWivid/F5-TTS · 
Discussions - Hugging Face, https://huggingface.co/SWivid/F5-TTS/discussions 69. ai-agents · 
GitHub Topics, https://github.com/topics/ai-agents 70. jhao104/proxy_pool: Python ProxyPool 
for web spider - GitHub, https://github.com/jhao104/proxy_pool 71. GitHub - 


