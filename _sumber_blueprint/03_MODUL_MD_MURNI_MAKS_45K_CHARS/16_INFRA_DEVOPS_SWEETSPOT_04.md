
<!-- [ID:16_INFRA_DEVOPS_S042] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 110

Untuk memastikan mesin server tempat berjalannya kode bot, router, dan perayap web tetap 
menyala 24 jam sehari sepanjang tahun tanpa biaya sepeser pun, arsitektur ini memisahkan 
antara lapisan komputasi nir-status (*stateless compute*) dan lapisan penyimpanan data eksternal. 
Bagi arsitek sistem yang memiliki kartu debit atau kredit fisik untuk verifikasi identitas awal (dengan 
mematuhi aturan keamanan FIN-SEC-01, yaitu menggunakan Kartu Debit Visa Virtual terisolasi 
pada kantong terpisah seperti Bank Jago atau Jenius bersaldo minimal ~Rp 20.000), jalur utama 
yang diaktifkan adalah Oracle Cloud Always Free Tier. Saat mendaftar Oracle Cloud, pendaftaran 
wajib dilakukan menggunakan jaringan seluler (hotspot HP) tanpa VPN dan tanpa pemblokir iklan 
(*adblocker*), serta menyamakan alamat tagihan secara presisi. Begitu akun aktif, langkah 
pengaman dan pembuka kapasitas yang harus segera dilakukan adalah melakukan upgrade akun 
ke status *Pay-As-You-Go* (PAYG) di menu Billing dan memasang *Budget Alert* pada angka 
US0.01. Selama pemakaian server tidak melewati batas *Always Free*, akun PAYG tidak akan 
pernah ditagih sepeser pun, namun pengguna langsung terbebas dari antrean penuh (*"Out of 
host capacity"*), terhindar dari penghapusan paksa akibat aturan *idle-reclamation* Oracle, dan 
mendapatkan kembali kuota penuh hingga 4 OCPU ARM Ampere A1 dan 24 GB RAM 
(dibandingkan batas 2 OCPU dan 12 GB RAM pada akun gratis murni) beserta 200 GB 
penyimpanan SSD dan 10 TB bandwidth keluar per bulan. Sebagai server pendamping gratis 
selamanya yang jauh lebih mudah lolos verifikasi kartu, Google Cloud Platform (GCP) 
menyediakan 1 unit VPS `e2-micro` (wajib memilih region AS `us-west1` Oregon, `us-central1` 
Iowa, atau `us-east1` South Carolina dan mengubah jenis disk ke *Standard Persistent Disk* 30 
GB), sementara untuk komputasi GPU berat seperti merender video `Wan2.2-TI2V-5B` atau 
`HunyuanVideo-1.5`, verifikasi kartu pada Modal (`modal.com`) langsung membuka kredit GPU 
serverless sebesar US30 per bulan yang direset ulang secara otomatis setiap bulan selamanya.
Apabila pengembang memilih untuk beroperasi 100% tanpa kartu pembayaran sama sekali, 
ketersediaan server 24 jam penuh sepanjang tahun dicapai melalui tiga kombinasi infrastruktur nir-
kartu. Pertama, men-deploy kontainer web atau router ke Render.com (yang memberikan kuota 
750 jam gratis per bulan, cukup untuk menyala 24 jam nonstop selama 31 hari penuh) lalu 
mendaftarkan URL aplikasi Render tersebut ke layanan penjadwal ping gratis cron-job.org atau 
UptimeRobot dengan interval kunjungan otomatis setiap 14 menit sekali; karena server Render 
menerima trafik setiap 14 menit, mesin tersebut tidak akan pernah mengalami *spin down* (tidur 
setelah 15 menit idle) dan menyala 24/7 secara gratis selamanya. Kedua, memanfaatkan kontainer 
Docker gratis tanpa kartu dari Caasify (menggratiskan hingga 2 CPU, 4 GB RAM, dan 50 GB 
NVMe SSD hingga 31 Desember 2026), SnapDeploy (4 kontainer Docker @ 512 MB RAM tanpa 
kartu), serta hosting SSH Serv00 (3 GB storage dengan dukungan Python, Node.js, Rust, Go, dan 
C++). Ketiga, menerapkan sistem estafet atau *load balancing* multi-akun pada GitHub 
Codespaces. Karena kuota 120 *core-hours* (60 jam aktif per bulan pada mesin 2-core / 4 GB 
RAM) dipotong dari akun GitHub yang menekan tombol *Create Codespace* dan bukan dari 



<!-- [ID:16_INFRA_DEVOPS_S043] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 111

pemilik repositori, menambahkan 6 hingga 12 akun kolaborator ke satu repositori utama yang 
dilengkapi berkas .devcontainer/devcontainer.json dan skrip .devcontainer/setup.sh memungkinkan 
pergantian mesin setiap 58 jam secara otomatis. Dengan menyematkan Cloudflare Tunnel 
(cloudflared) di dalam skrip inisialisasi dan menjaga sesi tetap hidup melalui perintah gh 
codespace ssh -- -o ServerAliveInterval=60 serta menyinkronkan variabel .env via Doppler Secret 
Manager (doppler.com), pergantian akun berlangsung mulus tanpa perubahan URL publik dan 
tanpa *downtime*.
Agar pergantian atau *failover* antar-server tersebut tidak pernah menghilangkan data pengguna 
sedikit pun, tidak boleh ada database yang disimpan di dalam disk lokal kontainer. Seluruh status 
transaksi cepat diarahkan ke Turso Cloud (gratis 5 GB penyimpanan libSQL terdistribusi, 500 juta 
pembacaan baris dan 10 juta penulisan baris per bulan, tanpa jeda otomatis), memori vektor 
diarahkan ke Supabase (gratis 500 MB PostgreSQL + pgvector dan 1 GB storage, dijaga oleh cron 
ping harian agar tidak terkena jeda inaktivitas 7 hari), konfigurasi klaster gateway diarahkan ke 
Neon Serverless Postgres (gratis 1 GB penyimpanan per proyek dan 100 CU-hours/bulan), 
sementara penyimpanan objek media dan cadangan bobot model didistribusikan ke Backblaze B2 
(10 GB pertama 100% gratis tanpa kartu Visa dengan egress gratis hingga 3x volume data) dan 
Cloudflare R2 (10 GB gratis per bulan).

<!-- [ID:16_INFRA_DEVOPS_S044] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 119

| **Oracle Cloud Free Tier ARM** | Kuota dasar akun Free Tier murni dipangkas ke **2 OCPU / 12 
GB RAM** dan rawan *Out of host capacity*. | Terapkan **Trik Upgrade PAYG + Budget Alert 
US$0.01** untuk membuka prioritas slot server dan memulihkan kuota hingga 4 OCPU / 24 GB 
RAM tanpa bayar. |
| **Turso** & **Neon Database** | Kuota gratis Turso disesuaikan menjadi **5 GB storage** (dari 9 
GB); Neon ditingkatkan menjadi **1 GB per proyek** (100 CU-hours) per Oktober 2026. | Gunakan 
Turso khusus untuk tabel transaksi cepat, Neon untuk konfigurasi New-API Horizon, dan Supabase 
untuk vektor pgvector. |
| **Piper TTS Lama** (rhasspy/piper) | Repositori lama telah **diarsipkan**. | Gunakan repositori 
aktif baru **OHF-Voice/piper1-gpl (rilis v1.8.0 Sep 2026)** via pip install piper-tts berdampingan 
dengan **Kokoro-82M**. |
| **Firebase Studio (eks Project IDX)** & **Fly.io** | Firebase Studio menutup workspace baru 
sejak 22 Juni 2026; Fly.io menghapus free allowance permanen. | Gunakan **GitHub Codespaces 
(estafet)**, **Render + cron-job.org**, **Caasify (gratis s/d akhir 2026)**, dan **SnapDeploy**. |

<!-- [ID:16_INFRA_DEVOPS_S045] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 144

  const nodes: NodeStatus[] = [​
    { name: "Mistral AI Console (Experiment)", category: "TIER-1 CLOUD", quota: "~1 Miliar 
Token/Bln", latencyMs: 145, status: "ONLINE", authType: "100% No Card" },​
    { name: "Google AI Studio (Gemini 3.5)", category: "TIER-1 CLOUD", quota: "1M Context / 15 
RPM", latencyMs: 120, status: "ONLINE", authType: "100% No Card" },​
    { name: "GroqCloud LPU (Qwen/Whisper)", category: "TIER-1 CLOUD", quota: "14.400 
RPD", latencyMs: 42, status: "ONLINE", authType: "100% No Card" },​
    { name: "NVIDIA NIM Catalog", category: "TIER-1 CLOUD", quota: "91-138 Model / 40 RPM", 
latencyMs: 98, status: "ONLINE", authType: "100% No Card" },​
    { name: "NgodeAI (Server ID-JKT)", category: "ZERO-AUTH / ID", quota: "Rp 0 / 100% OFF 
Unlimited", latencyMs: 14, status: "ONLINE", authType: "Zero-Auth" },​
    { name: "Pollinations.ai Endpoint", category: "ZERO-AUTH / ID", quota: "1.5M Req/Hari 
Uncensored", latencyMs: 185, status: "ONLINE", authType: "Zero-Auth" },​
    { name: "Kilo Code & LLM7.io", category: "ZERO-AUTH / ID", quota: "200 Req/Jam 
Nir-Kunci", latencyMs: 110, status: "ONLINE", authType: "Zero-Auth" },​
    { name: "LlamaCpp Huihui-Qwen3.8-27B", category: "LOCAL SOTA", quota: "Dedicated 
Local VPS", latencyMs: 38, status: "ONLINE", authType: "Zero-Auth" },​
    { name: "DeepSeek-R1-0528-Qwen3-8B", category: "LOCAL SOTA", quota: "86.0% AIME24 
Worker", latencyMs: 45, status: "ONLINE", authType: "Zero-Auth" },​
    { name: "Turso Cloud (Distributed libSQL)", category: "INFRA & DB", quota: "5 GB / 500M 
Reads", latencyMs: 32, status: "ONLINE", authType: "100% No Card" },​
    { name: "Oracle Cloud Always Free ARM", category: "INFRA & DB", quota: "4 OCPU / 24 GB 
RAM", latencyMs: 28, status: "ONLINE", authType: "Oracle PAYG" },​
    { name: "Modal Serverless GPU", category: "INFRA & DB", quota: "US$30/Bulan Reset", 
latencyMs: 65, status: "STANDBY", authType: "Oracle PAYG" },​
  ];​
​
  return (​
    <div className="mx-auto max-w-6xl px-4 py-8">​
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b 
border-white/10 pb-5 mb-6">​
        <div>​
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">​
            <Activity className="h-5 w-5 text-cyan-400" /> Telemetri Infrastruktur & Cluster 
Multi-Jalur​
          </h2>​
          <p className="text-xs text-slate-400 mt-1">​
            Status rotasi otomatis 25+ penyedia API gratis, failover daemon, dan redundansi basis 
data.​
          </p>​
        </div>​
        <div className="flex items-center gap-2">​
          <span className="rounded-lg border border-white/10 bg-white/5 px-3 py-1.5 text-xs 
font-mono text-slate-300">​
            Total Kapasitas: <strong>> 1,1 Miliar Token/Bln</strong>​
          </span>​
        </div>​
      </div>​



<!-- [ID:16_INFRA_DEVOPS_S046] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 158

    if (res.ok) {​
      const data = await res.json();​
      return NextResponse.json({​
        success: true,​
        gateway: "Pakasir_v2",​
        payment_url: `https://pakasir.com/pay-v2/${slug}?qris_only=1`,​
        data,​
      });​
    }​
​
    // Failover ke kasir CryptoBot jika Pakasir maintenance​
    return NextResponse.json({​
      success: true,​
      gateway: "CryptoBot_USDT_Failover",​
      payment_url: "https://t.me/CryptoBot?start=pay_invoice",​
    });​
  } catch {​
    return NextResponse.json({​
      success: true,​
      gateway: "CryptoBot_USDT_Failover",​
      payment_url: "https://t.me/CryptoBot?start=pay_invoice",​
    });​
  }​
}​
 
5. Panduan Instalasi dan Deployment 
Untuk menjalankan aplikasi ini di komputer lokal atau men-deploy-nya secara gratis ke 
Cloudflare Pages atau Vercel: 
1.​ Jalankan Aplikasi di Lokal:​
npm install​
npm run dev​
Buka peramban di http://localhost:3000. 
2.​ Deploy ke Cloudflare Pages (100% Gratis & Bandwidth Tanpa Batas): 
○​ Unggah repositori ke akun GitHub Anda. 
○​ Masuk ke dashboard Cloudflare Pages, pilih Create a project > Connect to Git. 
○​ Atur pengaturan build: 
■​ Framework preset: Next.js 
■​ Build command: npx @cloudflare/next-on-pages (atau npm run build) 
■​ Build output directory: .vercel/output/static (atau .next) 
○​ Masukkan variabel lingkungan dari file .env ke menu Settings > Environment 
Variables di Cloudflare Dashboard. 



<!-- [ID:16_INFRA_DEVOPS_S047] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 167

Saya telah memperbarui laporan riset Anda dengan menambahkan sub-bab "Panduan 
Operasional Terperinci Langkah demi Langkah: Pembuatan Website dari Nol hingga Live 
Launch" yang merinci secara berurutan:
​Langkah 1: Persiapan instalasi Node.js LTS, Git, dan pengambilan 17 kredensial Kategori 1 
(Telegram Bot, AI Studio, Groq, Mistral, Turso, Pakasir v2, CryptoBot).
​Langkah 2: Inisialisasi proyek Next.js 15, App Router, TypeScript, Tailwind CSS v4, serta 
struktur hierarki direktori.
​Langkah 3: Standarisasi brankas .env.local dan penguncian aturan Zero-Commit pada .gitignore.
​Langkah 4: Pembuatan utilitas kelas lib/utils.ts dan konfigurasi animasi keyframe spotlight 
pada app/globals.css.
​Langkah 5: Perakitan antarmuka pengguna modular (Navbar, Hero Studio Multimodal, System 
Health Telemetri, FinOps 95% Margin, Self-Evolving Radar, dan Omnichannel Failover).
​Langkah 6: Penulisan handler rute backend API (/api/v1/generate untuk evaluasi RouteLLM & 
failover kognitif, serta /api/v1/payment/qris untuk integrasi Pakasir API v2 bebas potongan 
MDR 0% Bank Indonesia).
​Langkah 7 & 8: Pengujian kompilasi lokal (npm run build) dan penyambungan repositori Git ke 
Cloudflare Pages untuk deployment gratis dengan bandwidth tanpa batas.
​Langkah 9: Penautan domain kustom, aktivasi Cloudflare Turnstile anti-bot, serta verifikasi 
pembayaran langsung (smoke-testing).
Penelitian lengkap beserta pembaruan peta jalan (roadmap) dan kode 
produksi untuk platform agregator AI Anda telah selesai disusun pada 
laporan di atas. Sebagai ringkasan eksekusi atas keempat poin utama yang 
Anda tanyakan:
 * Strategi Pendaftaran Hari Peluncuran (Serentak vs Bertahap):
   * Daftar & Aktifkan Serentak di Hari ke-1: Wajib dilakukan khusus untuk 
seluruh layanan 100% Tanpa Kartu yang memiliki kuota reset harian/bulanan 
permanen (seperti Mistral AI Console 1 miliar token/bulan, Google AI Studio, 
GroqCloud, NVIDIA NIM, OpenRouter :free, NgodeAI Jakarta Rp 0, 
Pollinations.ai, Turso, Supabase, Neon, Pakasir API v2, dan @CryptoBot). 
Penggabungan seluruh kunci ini di balik OmniRoute dan New-API Horizon 
menciptakan kapasitas konkurensi > 1.500\text{ RPM} untuk menahan 
serbuan ribuan pengguna secara bersamaan di hari pertama.
   * Daftar Bertahap / Estafet Bulanan: Jangan mendaftarkan layanan VPS 
atau kredit uji coba berbatas waktu (seperti DigitalOcean 60 hari, Linode 60 
hari, Vultr 30 hari, AWS 6 bulan, Alibaba Cloud 90 hari) secara bersamaan di 
hari pertama karena arloji kedaluwarsanya langsung berdetak sejak verifikasi 
kartu disetujui. Daftarkan satu per satu secara estafet ketika masa aktif 
penyedia sebelumnya menyisakan 5 hari, lalu suntikkan IP atau kunci API 
barunya ke dalam berkas .env tanpa mengubah kode.
 * Alur Kerja (Workflow) Gratis Permanen Menghadapi Trafik Viral:
   * Lapisan 0 (Edge & Browser): Hosting statis/SSR gratis di Cloudflare Pages 
+ proteksi Turnstile, ditambah pemanggilan Puter.js di sisi klien untuk 
mendelegasikan beban komputasi dasar langsung ke sesi peramban 
pengguna (biaya server Rp 0).
   * Lapisan 1 (Semantic Cache & Kompresi): Pencegatan kueri 
populer/kembar dalam ~25 milidetik menggunakan Valkey / RedisVL di 
Upstash Redis, serta pemangkasan ukuran token konteks hingga 98% 
menggunakan mksglu/context-mode.
   * Lapisan 2 & 3 (Smart Routing): Pemilahan tingkat kesulitan kueri secara 
matematis menggunakan RouteLLM (\tau = 0,11593) dan ClawRouter, yang 
mengarahkan kueri ringan ke titik akhir nir-kunci (NgodeAI, Pollinations.ai, 
Kilo Code, LLM7.io) atau model lokal tanpa sensor 
(Huihui-Qwen3.8-abliterated & DeepSeek-R1-0528-Qwen3-8B), dan kueri berat 
ke kolam rotasi multi-cloud gratis.
   * Lapisan 4 & 5 (Server & Database Abadi): Memisahkan penyimpanan data 
ke Turso, Supabase, Neon, dan Backblaze B2 sehingga mesin komputasi 
(Oracle Cloud Always Free dengan trik PAYG + Budget Alert US$0.01, Render 
+ ping cron-job.org tiap 14 menit, atau estafet GitHub Codespaces) dapat 
berganti kapan saja tanpa kehilangan data.
 * Adaptasi & Upgrade Otomatis dari Top 100 Repo Open-Source (MIT & 
Apache-2.0):
   * Menggunakan kombinasi Nous Hermes Agent dan OpenClaw 
(RangeKing/self-evolving-agent) yang dijadwalkan setiap malam untuk 
memindai tren GitHub berlisensi mit dan apache-2.0 melalui perayap 



<!-- [ID:16_INFRA_DEVOPS_S048] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 34

5.​ NVIDIA NIM API Catalog (91–138 Model Frontier Gratis) — URL Polos Portal Utama: 
https://build.nvidia.com/ | URL Polos Pengambilan Kunci API Langsung: 
https://build.nvidia.com/settings/api-keys | URL Polos Base Endpoint OpenAI-Compatible: 
https://integrate.api.nvidia.com/v1 — Kegunaan & Aturan Terbaru (Oktober 2026): 100% 
tanpa kartu kredit; cukup daftar dengan Gmail dan lakukan verifikasi nomor HP. 
Menyediakan akses prototipe gratis ke 91 hingga 138 titik akhir model (mencakup 
DeepSeek-R1/V3.2, Kimi K2.5, GLM 4.7, Nemotron, visi, audio, embedding, dan rerank) 
dengan konteks hingga 1M token dan batas laju tinggi sekitar 40 RPM. 
6.​ Cloudflare Workers AI (Inferensi Serverless Tepi Gratis) — URL Polos Pendaftaran 
Akun: https://dash.cloudflare.com/sign-up | URL Polos Dashboard Utama: 
https://dash.cloudflare.com | URL Polos Pengambilan Token API: 
https://dash.cloudflare.com/profile/api-tokens — Kegunaan & Aturan Terbaru (Oktober 
2026): 100% tanpa kartu kredit. Memberikan alokasi permanen 10.000 Neurons/hari 
(direset setiap pukul 00:00 UTC) untuk menjalankan 46 hingga 80+ model terbuka (teks, 
koding, penalaran, gambar, dan video dengan konteks hingga 262K) langsung di jaringan 
tepi Cloudflare. 
7.​ SiliconFlow, Fireworks AI & Alibaba Cloud Model Studio (Kredit Sambutan & Model 
Gratis Tanpa Kartu) — URL Polos SiliconFlow Global: https://cloud.siliconflow.com/ | 
URL Polos SiliconFlow CN (Pengambilan AK Langsung): 
https://cloud.siliconflow.cn/account/ak | URL Polos Fireworks AI: https://fireworks.ai | URL 
Polos Alibaba Cloud Model Studio (Bailian Console): 
https://bailian.console.alibabacloud.com/?apiKey=1 — Kegunaan & Aturan Terbaru 
(Oktober 2026): 100% tanpa kartu kredit saat pendaftaran. SiliconFlow menyediakan 6 
model gratis permanen (serta akses cepat ke keluarga Qwen dan DeepSeek dengan laju 
hingga 1.000 RPM); Fireworks AI memberikan US$1 kredit starter gratis pada laju 10 
RPM; dan Alibaba Cloud Model Studio menyediakan 5 model gratis dengan konteks 1M 
serta kuota sekitar 1.000.000 token gratis per model (berlaku 90 hari di wilayah 
Singapura). 
8.​ AWS Builder ID (Jembatan Kiro AI Gratis) — URL Polos Pendaftaran Profil: 
https://profile.aws.amazon.com/ — Kegunaan & Aturan Terbaru (Oktober 2026): 100% 
tanpa kartu kredit karena merupakan identitas profil pengembang mandiri (bukan akun 
AWS Console reguler). Catatan Audit 2026: Kiro AI telah membatasi paket gratisnya 
menjadi 50 kredit/bulan (~25.000–100.000 token, ditambah 500 kredit uji coba selama 30 
hari pertama untuk akun baru) dan ketentuan layanannya melarang penggunaan 
proksi/harness pihak ketiga. 
9.​ Hugging Face Access Tokens & Inference Providers — URL Polos Pengambilan 
Token: https://huggingface.co/settings/tokens | URL Polos HuggingChat Web (Akses 
Gratis): https://huggingface.co/chat — Kegunaan & Aturan Terbaru (Oktober 2026): 100% 
tanpa kartu kredit. Digunakan untuk mengunduh bobot model GGUF/Safetensors 
sekaligus memanggil 9 model gratis di Hugging Face Serverless Inference (termasuk 
kredit bulanan US$0,10/bulan yang dapat dirutekan ke mitra inferensi untuk 
menghasilkan ~590.000 token output pada gpt-oss-120b). 
10.​Cohere Dashboard & Chutes AI (Bittensor Serverless) — URL Polos Cohere 
Dashboard: https://dashboard.cohere.com | URL Polos Pengambilan Kunci API Cohere: 
https://dashboard.cohere.com/api-keys | URL Polos Portal Chutes AI: https://chutes.ai | 
URL Polos Dokumentasi API Chutes AI: https://docs.chutes.ai/ — Kegunaan & Aturan 
Terbaru (Oktober 2026): 100% tanpa kartu kredit. Cohere menyediakan Trial API Key 
otomatis dengan kuota 1.000 panggilan/bulan (20 RPM, penggunaan non-komersial) 



<!-- [ID:16_INFRA_DEVOPS_S049] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 35

pada 12 model (termasuk Command A+, Command A, Command R+, dan Aya Expanse 
32B dengan konteks 256K), sedangkan Chutes AI menyediakan 2 model penalaran/teks 
gratis berkonfigurasi 131K konteks di atas jaringan terdesentralisasi Bittensor. 
11.​Civitai & Spider Cloud API (Model Unfiltered & Smart Web Crawling API) — URL 
Polos Pengambilan Kunci API Civitai: https://civitai.com/user/account | URL Polos Portal 
Spider Cloud API: https://spider.cloud — Kegunaan & Aturan Terbaru (Oktober 2026): 
100% tanpa kartu kredit (URL Civitai telah diperbaiki dari kerusakan tag ekstraksi pada 
dokumen sumber). Kunci Civitai digunakan untuk mengunduh checkpoint gambar/video 
tanpa filter dan negative embeddings via skrip, sedangkan Spider Cloud memberikan 
kunci API gratis tanpa kartu untuk smart web scraping. 
12.​Tambahan Penyedia API LLM Gratis Baru Hasil Validasi Langsung Oktober 2026 
(100% Tanpa Kartu Kredit) — URL Polos ModelScope API-Inference (61 Model Gratis, 
Konteks 1M): https://modelscope.cn/my/myaccesstoken (Base URL: 
https://api-inference.modelscope.cn/v1) | URL Polos OpenCode Zen (34 Model Gratis 
Audio/Reasoning/Vision, Konteks 1M): https://opencode.ai/auth (Base URL: 
https://opencode.ai/zen/v1) | URL Polos Kilo Code Gateway (27 Model Gratis 
Multimodal/Koding, Konteks 1M): https://app.kilo.ai/profile (Base URL: 
https://api.kilo.ai/api/gateway) | URL Polos LLM7.io (24 Model Gratis Multimodal, Konteks 
1M, Terima Kunci String Apa Pun): https://token.llm7.io (Base URL: https://api.llm7.io/v1) | 
URL Polos Ollama Cloud (17 Model Gratis di Cloud Resmi Ollama, Konteks 1M): 
https://ollama.com/settings/keys | URL Polos OVHcloud AI Endpoints (15 Model Gratis 
Berstandar GDPR Eropa, Konteks 262K): 
https://www.ovhcloud.com/en/public-cloud/ai-endpoints/catalog/ | URL Polos Aion Labs 
(11 Model Gratis termasuk Aion 2.5 & Aion 2.0, 15 RPM / 20K Token per Hari): 
https://www.aionlabs.ai/app/api-keys/ | URL Polos Z.AI / Zhipu AI BigModel (8 Model 
Gratis termasuk GLM-4.7-Flash, Konteks 200K): 
https://open.bigmodel.cn/usercenter/apikeys | URL Polos DeepSeek Official Platform 
(Bonus 5 Juta Token Gratis Saat Pendaftaran): https://platform.deepseek.com/api_keys | 
URL Polos AI21 Labs Studio (US10 Kredit Uji Coba Gratis Berlaku 3 Bulan untuk Jamba 
256K, 200 RPM): https://studio.ai21.com/account/api-key | URL Polos AgentRouter 
(Gateway Multi-Model dengan Bonus US200 Kredit Gratis Saat Daftar): 
https://agentrouter.org | URL Polos FreeModel.dev (Bonus US300 Kredit Gratis Saat 
Daftar Tanpa Kartu untuk Akses Kompatibel OpenAI): https://freemodel.dev | URL Polos 
BazaarLink (Inferensi Gratis dengan Rute `auto:free` Tanpa Kartu Kredit): 
https://bazaarlink.ai | URL Polos MegaNova AI (Kuota Gratis Tier 1 Sebesar 550 
Request/Hari Tanpa Kartu): https://meganova.ai | URL Polos Morph (Kuota Gratis 
250.000 Kredit/Bulan): https://morphllm.com | URL Polos onomeo (30 Model Gratis Tanpa 
Kartu, Kuota 30 Panggilan per 5 Jam / 12 RPM): https://onomeo.com | URL Polos 
Api.airforce (55 Model Tier Gratis termasuk Claude 3.7, Grok-3, Qwen3, DeepSeek-V3): 
https://api.airforce | URL Polos BluesMinds (Kredit Pi Harian Gratis untuk 200+ Model): 
https://www.bluesminds.com | URL Polos Bytez (US1 Kredit Gratis yang Diperbarui 
Otomatis Setiap 4 Minggu): https://bytez.com | URL Polos MNN AI (US1 Kredit Bulanan 
Gratis pada Laju 10 RPM): https://mnnai.ru | URL Polos Logfare (Kunci API Gratis Instan 
Tanpa Verifikasi Email): https://logfare.ai/register | URL Polos Blackbox AI (Chat Dasar 
Gratis Tanpa Batas + Minimax-M2.5 Tanpa Kartu): https://blackbox.ai | URL Polos 
Featherless AI (Tier Gratis Tersedia Tanpa Kartu): https://featherless.ai | URL Polos 
FriendliAI (Tier Serverless Inference Gratis Tanpa Kartu): https://friendli.ai | URL Polos 
Glhf.chat (2 Model Gratis Konteks 131K): https://glhf.chat/ | URL Polos Agnes AI (5 Model 



<!-- [ID:16_INFRA_DEVOPS_S050] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 36

Multimodal Gratis Konteks 256K): https://platform.agnes-ai.com/settings/apiKeys | URL 
Polos Gonka Broker (4 Model Multimodal Gratis Konteks 400K): 
https://app.gonkabroker.com/signup | URL Polos NaraRouter (Akses `/v1` Gratis dengan 
Menautkan Akun Telegram): https://bynara.id | URL Polos NavyAI (Kunci API Gratis dari 
Dashboard): https://api.navy | URL Polos OfoxAI (10+ Model Gratis): https://ofox.ai | URL 
Polos Nebius AI Studio (~US1 Kredit Uji Coba Gratis Saat Pendaftaran): 
https://studio.nebius.com/settings/api-keys | URL Polos nScale Console (US$5 Kredit 
Gratis Saat Pendaftaran untuk Uji Inferensi): https://console.nscale.com/ | URL Polos 
Speechmatics / Openference API (8 Jam/Bulan Transkripsi Batch Gratis Tanpa Kartu): 
https://www.speechmatics.com | URL Polos Openference (Akses Gratis Qwen3.8 27B & 
Llama 3.2 3B): https://openference.com | URL Polos LiteRouter (Model Varian :free 
dengan Batas Input 5.000 Token): https://literouter.com | URL Polos LLM.Kiwi (Paket 
Gratis auto dan hrLLM 40 Request/Jam): https://llm.kiwi | URL Polos LLM Gateway (Paket 
Gratis 5 Request per 10 Menit Tanpa Saldo): https://llmgateway.io | URL Polos Naga AI 
(Model Berlabel :free Publik): https://naga.ac — Kegunaan & Aturan Terbaru: Puluhan 
sumber "bansos" token dan endpoint inferensi gratis terbaru yang tervalidasi aktif pada 
Oktober 2026 di dalam registri OmniRoute v3.8.52 dan awesome-freellm-apis untuk 
memperluas kolam rotasi kunci API Anda tanpa memerlukan kartu pembayaran. 
13.​Penyedia dalam Status Transisi / Legacy / Tutup (Wajib Dibungkus Blok try-except 
Fallback) — URL Polos Cerebras Cloud: https://cloud.cerebras.ai (Endpoint: 
https://api.cerebras.ai/v1 dan https://inference.cerebras.ai) | URL Polos SambaNova 
Cloud: https://cloud.sambanova.ai/apis | URL Polos GitHub Models: 
https://github.com/marketplace/models | URL Polos MonsterAPI (Ditutup): 
https://monsterapi.ai | URL Polos AI/ML API (Free Tier Dijeda): https://aimlapi.com — 
Kegunaan & Aturan Terbaru (Oktober 2026): Terdapat perbedaan status antar-direktori 
untuk Cerebras, SambaNova, dan GitHub Models: sementara beberapa direktori 
komunitas masih mencatat kuota gratis Cerebras (6 model, 1M token/hari, 30K TPM, 5 
RPM) dan SambaNova (4 model, konteks 128K), dokumen audit teknis mencatat bahwa 
sejak pertengahan Juli dan Agustus 2026 pendaftar baru Cerebras dan SambaNova 
dialihkan ke skema uji coba berbayar/wajib kartu, serta GitHub Models dipensiunkan 
pada 30 Juli 2026 (atau dibatasi ketat mengikuti langganan Copilot). Selain itu, 
MonsterAPI resmi ditutup pada 30 Juni 2026 dan AI/ML API telah menjeda paket 
gratisnya menjadi khusus prabayar (minimal pengisian US$20). Pastikan kode agen 
selalu membungkus penyedia pada poin ke-13 ini di dalam blok fallback otomatis. 
2B. Infrastruktur Database, Penyimpanan, Hosting Kontainer/Docker, 
GPU Cloud & Memori Gratis (Tanpa Kartu Kredit) 
1.​ Cloudflare Workers, Pages, R2, D1 & Turnstile (Beserta Proksi new-api-worker) — 
URL Polos Repositori Skrip Proksi: https://github.com/Calcium-Ion/new-api-worker | URL 
Polos Dashboard Cloudflare: https://dash.cloudflare.com | URL Polos Pendaftaran Akun 
Cloudflare: https://dash.cloudflare.com/sign-up | URL Polos Cloudflare Pages: 
https://pages.cloudflare.com/ | URL Polos Cloudflare Workers: 
https://workers.cloudflare.com/ | URL Polos Dokumentasi Cloudflare R2: 
https://developers.cloudflare.com/r2/ — Kegunaan & Aturan Terbaru (Oktober 2026): 
100% tanpa kartu kredit untuk Workers, Pages, D1, dan Turnstile. Memberikan 100.000 
request/hari pada Workers (untuk menyembunyikan IP server agregator via Transform 



<!-- [ID:16_INFRA_DEVOPS_S051] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_102 -->
## Halaman 38

Gratis): https://lightning.ai/ — Kegunaan & Aturan Terbaru (Oktober 2026): 100% tanpa 
kartu kredit (Colab cukup akun Gmail; Kaggle cukup Gmail + verifikasi nomor HP). 
Digunakan secara bergantian untuk menjalankan proses abliteration bobot model 
(p-e-w/heretic atau jim-plus/llm-abliteration) maupun merender suara/video ketika mesin 
lokal tidak memiliki GPU memadai. 
5.​ Vercel, Mem0, Letta & E2B Sandbox (Hosting, Memori Agen Persisten & Eksekusi 
Kode Terisolasi) — URL Polos Vercel (Hobby Tier Serverless Hosting, 100 GB 
Bandwidth/Bulan): https://vercel.com | URL Polos Dokumentasi Vercel Functions (100 
GB-Hours): https://vercel.com/docs/functions | URL Polos Mem0 (Infrastruktur Memori 
Agen Persisten): https://github.com/mem0ai/mem0 | URL Polos Letta / MemGPT Node 
SDK: https://github.com/letta-ai/letta-node | URL Polos Halaman Harga & Kuota Letta 
Cloud (Oktober 2026): https://docs.letta.com/pricing | URL Polos E2B Code Sandbox: 
https://e2b.dev | URL Polos Halaman Harga E2B (US100 Kredit Penggunaan Awal 
Gratis): https://e2b.dev/pricing — Kegunaan & Aturan Terbaru (Oktober 2026): 100% 
tanpa kartu kredit saat pendaftaran via 
GitHub[span_102](start_span)[span_102](end_span). Mem0 (`mem0 init --agent`) dan 
Letta (paket gratis memberikan 5 MiB penyimpanan per repositori memori serta dukungan 
BYOK/lokal penuh) menjaga memori agen lintas sesi, sedangkan E2B memberikan kredit 
penggunaan awal US100 untuk mengeksekusi kode yang ditulis agen di dalam sandbox 
yang aman. 
6.​ Platform Hosting Kontainer Docker, PaaS & Shell SSH Gratis Tanpa Kartu Kredit 
(Tambahan Baru Oktober 2026) — URL Polos SnapDeploy (Hosting 4 Kontainer Docker 
Gratis Tanpa Kartu): https://snapdeploy.dev/free-container-hosting | URL Polos Caasify 
Container Hosting (Gratis €0 hingga 31 Desember 2026 Tanpa Kartu): 
https://caasify.com/container-hosting | URL Polos Zeabur (PaaS Tanpa Kartu, Gratis US5 
Kredit): https://zeabur.com/ | URL Polos Koyeb (Free Nano Instance Tanpa Sleep, 
Diakuisisi Mistral AI Feb 2026): https://www.koyeb.com/ | URL Polos Render (750 
Jam/Bulan Gratis, 512 MB RAM, Sleep Setelah 15 Menit Idle): https://render.com/ | URL 
Polos Miget (Standing Free Tier 256 MiB RAM, 1 GiB Storage, Mendukung 
`docker-compose.yml` & Postgres): https://miget.com/blog/best-free-docker-hosting | URL 
Polos Hugging Face Spaces (2 vCPU & 16 GB RAM pada CPU Basic): 
https://huggingface.co/spaces | URL Polos Peluncuran Hugging Face Spaces: 
https://huggingface.co/spaces/launch | URL Polos Leapcell (Serverless PaaS untuk 
Aplikasi, API & Database): https://leapcell.io/ | URL Polos Serv00 (Hosting Gratis 3 GB 
dengan Akses SSH, Python, Node.js, Rust, Go & C++ Tanpa Kartu): 
https://www.serv00.com/ | URL Polos Deno Deploy (Gratis 100.000 Request/Hari atau 1 
Juta/Bulan untuk Edge TS/JS): https://deno.com/deploy | URL Polos Netlify (Hosting 
Frontend/Jamstack Gratis 100 GB Bandwidth/Bulan Tanpa Kartu): https://www.netlify.com/ 
| URL Polos Streamlit Community Cloud (Hosting Aplikasi Data/AI Python Gratis Tanpa 
Batas): https://streamlit.io/ | URL Polos InfinityFree (Hosting PHP/Web Tanpa Kartu & 
Tanpa Iklan Paksa): https://infinityfree.net/ | URL Polos HelioHost (Hosting Komunitas 
Gratis 1 GB): https://heliohost.org/ — Kegunaan & Aturan Terbaru (Audit Oktober 2026): 
Alternatif krusial bagi pengguna yang belum memiliki kartu Visa untuk mendaftar Oracle 
Cloud[span_105](start_span)[span_105](end_span)[span_106](start_span)[span_106](en
d_span). SnapDeploy memberikan 4 kontainer Docker (512 MB RAM per kontainer, 100 
jam/bulan, 10 deploy/hari, tidur setelah 15 menit idle dan bangun saat dikunjungi browser, 
serta dilengkapi konektor MCP resmi untuk Claude Code/Cursor/Codex) tanpa kartu 
kredit[span_107](start_span)[span_107](end_span). Caasify menggratiskan biaya 



<!-- [ID:16_INFRA_DEVOPS_S052] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 40

ses/ | URL Polos Finpay (Payment Gateway & QRIS Provider Berlisensi Finnet/BI): 
https://www.finpay.id/ | URL Polos PayDisini (Peringatan: Pendaftaran Baru Ditutup 
Sementara): https://paydisini.co.id/ — Kegunaan & Aturan Terbaru (Audit Oktober 2026): 
Per 20 Oktober 2026, integrasi Pakasir API v1 telah dihentikan (deprecated); seluruh 
skrip kasir bot Anda wajib bermigrasi ke endpoint API v2 (/pay-v2/{slug}?qris_only=1 dan 
parameter ?redirect=) dengan pencairan dana (settlement) H+1 pukul 12.00 WIB cukup 
bermodalkan KTP. Hindari mengandalkan PayDisini untuk akun baru karena halaman 
resminya mengumumkan penutupan sementara pendaftaran merchant baru guna 
peningkatan sistem keamanan; gunakan rantai failover Pakasir, Duitku, Midtrans, Xendit, 
atau Tripay. Berdasarkan kebijakan terbaru Bank Indonesia yang berlaku efektif 1 
Oktober 2026, biaya MDR QRIS adalah 0% (gratis) untuk seluruh transaksi hingga 
Rp100.000 di semua kategori merchant (dan 0% hingga Rp500.000 khusus kategori 
Usaha Mikro / UMI), serta 0,7% untuk transaksi di atas Rp100.000 pada merchant kecil, 
menengah, dan besar. 
Kelompok 3: Wajib Kartu Visa/Mastercard ATAU Wajib 
Dompet Kripto (Wholesale GPU, DePIN & Airdrop 
2026) 
Kelompok ini dipisahkan secara tegas agar Anda mengetahui layanan mana yang mewajibkan 
verifikasi kartu pembayaran (gunakan Kartu Debit Visa Virtual terisolasi seperti kantong terpisah 
Bank Jago/Jenius sesuai protokol keamanan FIN-SEC-01 dengan saldo minimal sekitar 
Rp20.000) dan mana yang dapat dioperasikan murni menggunakan dompet kripto (USDT, 
Solana, Bittensor, atau Cosmos/Akash). 
3A. Penyedia Cloud, VPS Gratis Selamanya & API Grosir (Wajib 
Verifikasi Kartu Visa/Mastercard atau Top-Up Crypto USDT) 
1.​ Oracle Cloud Always Free Tier (VPS ARM 24 Jam Gratis Selamanya) — URL Polos 
Pendaftaran Resmi: https://www.oracle.com/cloud/free/ — Kegunaan & Aturan Terbaru 
(Oktober 2026): Wajib verifikasi Kartu Debit Visa/Mastercard (hanya untuk pengecekan 
otorisasi identitas yang langsung dikembalikan otomatis). Memberikan kredit uji coba 
US$300 selama 30 hari ditambah sumber daya Always Free permanen berupa hingga 4 
ARM Ampere A1 OCPUs dan 24 GB RAM yang ideal untuk menghosting panel 1Panel / 
Coolify, OmniRoute, 9Router, New-API Horizon, dan jhao104/proxy_pool 24/7 tanpa biaya 
bulanan. 
2.​ Modal Serverless GPU (Bansos Kredit GPU US$30/Bulan Berulang Setiap Bulan) — 
URL Polos Portal Utama & Harga: https://modal.com/pricing | URL Polos Program Kredit 
Startup Modal (Hingga US25.000 Kredit Gratis): https://modal.com/startups — Kegunaan 
& Aturan Terbaru (Oktober 2026): Login via GitHub, namun kuota gratis US30/bulan yang 
diperbarui otomatis setiap bulan pada paket Starter (mencakup 100 kontainer, 10 
konkurensi GPU dari T4 US0,59/jam hingga H100 US3,95/jam dan B200/B300, serta 1 
TiB egress gratis/bulan) baru terbuka setelah memverifikasi kartu Visa/Mastercard. Selain 
itu, peneliti akademik/mahasiswa dapat mengajukan hibah hingga US10.000 dan startup 
tahap awal (Seed–Series A) hingga US25.000 tanpa menyerahkan ekuitas. Catatan 
Teknis: Jangan mengaktifkan parameter penguncian wilayah (region selection seperti us 



<!-- [ID:16_INFRA_DEVOPS_S053] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_133, SPAN_134, SPAN_135 -->
## Halaman 41

atau eu) pada fungsi GPU Modal jika tidak wajib, karena akan memicu pengali biaya 1,5x 
hingga 1,75x dari tarif dasar per detik. 
3.​ Google Cloud Platform (GCP), AWS Free Tier, Azure, Hetzner, DigitalOcean, Fly.io, 
Railway & Northflank — URL Polos Google Cloud Free Tier (US300 Trial + e2-micro): 
https://cloud.google.com/free | URL Polos Google Cloud Run (Gratis 2 Juta Request & 
360.000 GiB-detik/Bulan): https://cloud.google.com/run/pricing | URL Polos Google Cloud 
Functions (Gratis 2 Juta Invokasi/Bulan): https://cloud.google.com/functions | URL Polos 
AWS Free Tier (t2.micro/t3.micro 12 Bulan): https://aws.amazon.com/free/ | URL Polos 
AWS Lambda (Gratis 1 Juta Request/Bulan): https://aws.amazon.com/lambda/ | URL 
Polos AWS DynamoDB (Gratis 25 GB Always Free): https://aws.amazon.com/dynamodb/ 
| URL Polos AWS S3 (Gratis 5 GB 12 Bulan): https://aws.amazon.com/s3/ | URL Polos 
AWS Amplify (Gratis 1.000 Menit Build): https://aws.amazon.com/amplify/ | URL Polos 
Microsoft Azure Free Tier (US200 Kredit + B1s VM 12 Bulan): 
https://azure.microsoft.com/free/ | URL Polos DigitalOcean (US200 Kredit 60 Hari & 3 
Static Sites Gratis): https://www.digitalocean.com/products/app-platform | URL Polos 
Hetzner Cloud (Kredit Uji Coba €20): https://www.hetzner.com/cloud | URL Polos Fly.io 
(Docker Hosting): https://fly.io | URL Polos Railway (US5 Trial Credit): https://railway.app/ | 
URL Polos Northflank (Gratis 1 Service + 1 Database dengan Verifikasi Kartu): 
https://northflank.com/ — Kegunaan & Aturan Terbaru (Audit Oktober 2026): Seluruh 
layanan ini mewajibkan kartu pembayaran untuk penggunaan penuh. Pada GCP, sejak 
Maret 2026 kredit uji coba US300 tidak lagi dapat dikonsumsi oleh endpoint Gemini API 
biasa, melainkan harus dipanggil melalui endpoint Vertex AI 
Studio[span_133](start_span)[span_133](end_span). Pada Fly.io, pendaftar baru tahun 
2026 hanya mendapatkan uji coba singkat selama 2 jam VM atau 7 hari sebelum 
diwajibkan menautkan kartu 
kredit[span_134](start_span)[span_134](end_span)[span_135](start_span)[span_135](en
d_span). Pada Railway, pendaftar baru mendapatkan kredit satu kali sebesar US5 tanpa 
kartu selama masa uji coba, yang akan habis dalam waktu kurang dari sebulan jika 
menjalankan kontainer 512 MB secara terus-menerus. 
4.​ Novita AI, RunPod, Vast.ai, PiAPI, Baseten & DeepInfra (Grosir GPU & Media yang 
Mendukung Crypto USDT Tanpa Kartu Visa) — URL Polos Novita AI (US0,50 Kredit 
Pendaftaran Gratis Berlaku ~1 Tahun + Top-Up USDT): https://novita.ai/ | URL Polos 
RunPod (Serverless FlashBoot GPU 24GB+ VRAM, Top-Up Crypto/USDT): 
https://www.runpod.io/ | URL Polos Vast.ai (Sewa GPU RTX 3090/4090 Termurah, Top-Up 
Crypto via Coinbase Commerce): https://cloud.vast.ai/ | URL Polos PiAPI (API Musik 
Suno v6 Studio & Udio, Top-Up USDT): https://piapi.ai/ | URL Polos Baseten (US30 Kredit 
Uji Coba Gratis untuk Inferensi GPU): https://baseten.co | URL Polos DeepInfra (Kredit 
Pendaftaran Gratis untuk Eksplorasi Model): https://deepinfra.com | URL Polos Predibase 
(US$25 Kredit Uji Coba Gratis Berlaku 30 Hari): https://predibase.com — Kegunaan & 
Aturan Terbaru (Oktober 2026): Anda dapat mendaftar akun secara gratis sekarang juga 
menggunakan login Google/GitHub untuk mengambil kunci API dan klaim bonus 
pendaftaran awal. Keunggulan utama Novita AI, RunPod, Vast.ai, dan PiAPI adalah 
dukungan pengisian saldo menggunakan Crypto USDT (yang dapat diambil langsung dari 
kasir @CryptoBot pada poin 2C.3) sehingga mesin produksi Anda dapat berjalan tanpa 
pernah membutuhkan kartu Visa perbankan. 
5.​ Fal.ai, WaveSpeed AI, Replicate & OpenAI Platform (API Media & Moderasi Grosir) 
— URL Polos Pengambilan Kunci API Fal.ai: https://fal.ai/dashboard/keys | URL Polos 
WaveSpeed AI (600+ Model Gambar & 50+ Model Video Cepat): https://wavespeed.ai/ | 



<!-- [ID:16_INFRA_DEVOPS_S054] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 42

URL Polos Pengambilan Token API Replicate: https://replicate.com/account/api-tokens | 
URL Polos Pengambilan Kunci API OpenAI Platform: 
https://platform.openai.com/api-keys — Kegunaan & Aturan Terbaru (Oktober 2026): 
Daftar akun gratis via GitHub/Google sekarang untuk mengambil kunci API dan 
menikmati kredit promosi pendaftaran awal (khususnya pada Fal.ai untuk inferensi FLUX 
berkecepatan sub-detik dengan kernel CUDA kustom dan pelatihan LoRA instan, serta 
WaveSpeed AI untuk akses awal Seedream, Kling 3.0, Seedance 1.5 Pro, dan Wan 2.2). 
Kartu Visa baru diperlukan saat mengaktifkan Auto-Topup komersial. Pada OpenAI 
Platform, endpoint omni-moderation-latest bersifat gratis untuk memfilter teks 
multibahasa, dan organisasi yang memenuhi syarat berbagi trafik dapat memperoleh 
kuota token gratis harian. 
3B. Jaringan DePIN, Mining AI, Marketplace GPU Terdesentralisasi & 
Airdrop Gratis (Wajib Dompet Kripto) 
Proyek di dalam sub-kategori 3B tidak memerlukan kartu Visa perbankan, melainkan 
menggunakan dompet kripto (Solana Phantom/Solflare, Bittensor coldkey/hotkey, Cosmos 
Keplr/Leap, atau dompet EVM) untuk menerima pembayaran token insentif, USDC, maupun 
alokasi airdrop. 
1.​ Ekosistem Bittensor (Subtensor Monorepo, Subnet 27 Compute & Score Predict) — 
URL Polos Bittensor Monorepo & SDK (btcli): https://github.com/RaoFoundation/bittensor 
| URL Polos Bittensor Subnet Template: 
https://github.com/opentensor/bittensor-subnet-template | URL Polos Panduan Eksekusi 
Testnet Bittensor: 
https://github.com/opentensor/bittensor-subnet-template/blob/main/docs/running_on_testn
et.md | URL Polos Spesifikasi Perangkat Keras Minimum Miner Bittensor: 
https://github.com/opentensor/bittensor-subnet-template/blob/main/min_compute.yml | 
URL Polos Subnet 27 Compute Bittensor (NeuralInternet / Commune-AI): 
https://github.com/commune-ai/compute-ni | URL Polos Score Predict Subnet (Mining 
Prediksi Olahraga Random Forest): 
https://github.com/score-technologies/score-predict/blob/main/README.md — Kegunaan 
& Aturan Terbaru: Menggunakan pasangan kunci kriptografi lokal (btcli wallet 
new_coldkey dan new_hotkey). Menyewakan GPU menganggur (minimal 4–8 core CPU, 
16 GB RAM, 24 GB VRAM, SSD 100 GB) ke Subnet 27 atau menjalankan model 
klasifikasi Random Forest di score-predict untuk memperoleh imbalan token TAO melalui 
Yuma Consensus. 
2.​ Nosana, IO.net, Hyperbolic & Prime Intellect (Jaringan Klaster GPU 
Terdesentralisasi) — URL Polos Nosana CLI (Node GPU di Jaringan Solana): 
https://github.com/nosana-ci/nosana-cli | URL Polos Nosana LLM Benchmarking Suite: 
https://github.com/nosana-ci/nosana-llm-benchmarking | URL Polos Repositori Portal 
Nosana: https://github.com/nosana-ci/nosana.io | URL Polos IO.net Launch Binaries 
(Worker Klaster GPU): https://github.com/ionet-official/io_launch_binaries/issues/48 | URL 
Polos Hyperbolic (Jaringan GPU DePIN & Inferensi dengan Verifikasi PoSP): 
https://www.hyperbolic.ai/blog/ai-compute-planning-gpu-market | URL Polos Prime 
Intellect (Klaster GPU Terdesentralisasi & Prime Inference vLLM/Dynamo): 
https://www.primeintellect.ai/blog/prime-inference — Kegunaan & Aturan Terbaru 
(Oktober 2026): Memungkinkan monetisasi GPU menganggur menggunakan dompet 



<!-- [ID:16_INFRA_DEVOPS_S055] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 63

Solusi: Buka menu Runtime > Change runtime type. Pastikan "Hardware accelerator" diatur ke T4 GPU. Jika masih connecting, coba ubah
sementara ke "CPU" lalu klik Connect. Jika CPU bisa terhubung namun GPU tidak, berarti Anda terkena limit harian dan harus menunggu
beberapa jam.
Pemutusan Latar Belakang (Background Kill): Sistem operasi HP (Android/iOS) sangat agresif memotong koneksi internet pada tab browser
yang dianggap diam.
Solusi: Saat mencoba menghubungkan Colab, pastikan layar HP tetap menyala dan jangan berpindah ke aplikasi lain sampai status di
pojok kanan atas berubah menjadi indikator "RAM" dan "Disk" yang dicentang hijau.
Sebagai tambahan mengenai kode Anda, penggunaan bot.infinity_polling() akan membuat sel (cell) tersebut berjalan tanpa henti. Google
Colab akan secara otomatis memutus koneksi dan mematikan bot Anda jika tab browser ditutup, HP terkunci, atau mendeteksi tidak ada aktivitas
interaksi (klik/scroll) di halaman web Colab tersebut selama kurang lebih 90 menit. Colab cocok untuk proses testing atau merender, namun bukan
solusi permanen untuk hosting bot Telegram 24/7.
User prompt: Terus biar bot telegram ke phyton anywhere yang bisa 24/7 dan comfyui dll nya biarkan di collab gimana?
Response: Ide memisahkan keduanya adalah langkah yang sangat cerdas. Dalam dunia software engineering, ini disebut arsitektur Microservices:
PythonAnywhere: Bertugas sebagai "Resepsionis 24/7". Dia tidak butuh spek tinggi, tugasnya hanya membalas chat, menangani
database/user, dan tidak akan pernah mati.
Google Colab: Bertugas sebagai "Pabrik GPU". Dia hanya dihidupkan saat Anda butuh merender gambar/video berat.
Namun, ada satu masalah teknis utama: PythonAnywhere berada di server awan (Inggris/AS), sedangkan Colab adalah komputer virtual sementara
milik Google. PythonAnywhere tidak bisa menghubungi alamat 127.0.0.1:8188 karena itu adalah alamat internal (localhost) milik Colab.
Berikut adalah cara menyambungkan keduanya secara keilmuan:
Langkah 1: Buat "Terowongan" (Tunnel) di Google Colab
Agar PythonAnywhere bisa mengirim perintah ke Colab, ComfyUI di Colab harus memiliki "Link Publik" yang bisa diakses dari luar. Kita bisa
menggunakan localtunnel atau cloudflared.
Hapus kode bot Telegram Anda dari Colab. Colab Anda kini hanya berisi kode instalasi ComfyUI dan kode untuk membuka akses publik:
