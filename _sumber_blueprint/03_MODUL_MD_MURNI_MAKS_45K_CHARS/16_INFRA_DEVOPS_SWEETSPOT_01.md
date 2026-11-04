
<!-- [ID:16_INFRA_DEVOPS_S001] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## 11. trikcodespace.md

```md
Vultr dan Oracle Cloud (OCI) adalah dua perusahaan penyedia layanan cloud/VPS yang berbeda (kompetitor), bukan satu produk gabungan. Orang sering menyebut keduanya bersamaan saat membandingkan VPS murah atau berburu promo server gratis.
Perubahan besar pada kebijakan gratis Oracle Cloud berdampak langsung pada kuota spesifikasi dan cara pendaftarannya:

1. Perbedaan Vultr vs Oracle Cloud
  | Fitur / Aspek | Oracle Cloud (OCI) | Vultr |
  |---|---|---|
  | Fokus Layanan | Hyperscaler kelas enterprise (setara AWS/GCP) & database raksasa. | Penyedia VPS independen, bare metal, dan GPU yang ramah developer. |
  | Gratis Selamanya (Always Free) | Ada. Menyediakan VPS ARM dan AMD mikro gratis tanpa batas waktu. | Tidak ada (Program Free Tier mikro Vultr sudah dihentikan untuk umum). |
  | Promo Pendaftar Baru | Kredit US$300 (berlaku 30 hari) + akses layanan Always Free. | Kredit US200 – US300 (berlaku 30 hari dengan kode promo seperti FLY300VULTR atau 250VULTRFLY). |
2. Fakta Gratis Selamanya 12 GB di Oracle Cloud
  Benar, kuota gratis selamanya dari Oracle Cloud adalah 12 GB RAM.
  Oracle memangkas setengah jatah gratis untuk server berbasis ARM (Ampere A1):
- Aturan Lama: Gratis 4 OCPU dan 24 GB RAM (3.000 OCPU-jam & 18.000 GB-jam per bulan).
- Aturan Baru: Dipotong menjadi 2 OCPU dan 12 GB RAM (1.500 OCPU-jam & 9.000 GB-jam per bulan) yang aktif 24/7 tanpa kedaluwarsa.
  Rincian Promo & Paket Gratis Oracle Cloud:
- Free Trial (30 Hari): Saldo kredit US$300 selama 30 hari pertama untuk mencoba berbagai layanan berbayar.
- Always Free (Gratis Selamanya setelah/selama trial):
  - VPS ARM (Ampere A1 Compute): Total 2 OCPU dan 12 GB RAM (bisa dijadikan 1 VPS ukuran 2 OCPU/12 GB, atau dipecah jadi 2 VPS ukuran 1 OCPU/6 GB). (Catatan: Selain server komputasi/VPS, ada juga promo Oracle AI Database 26ai Free yang memberikan batas 12 GB storage dan 2 GB RAM).
  - VPS AMD (VM.Standard.E2.1.Micro): 2 unit VPS mikro (masing-masing 1/8 OCPU dan 1 GB RAM).
  - Storage: 200 GB Block Volume (penyimpanan SSD untuk VPS) + 20 GB Object Storage.
  - Bandwidth: Gratis kuota outbound transfer (egress) hingga 10 TB per bulan.
3. Apakah Masih Bisa Daftar? Bagaimana Caranya?
  Masih sangat bisa daftar, melalui halaman resmi cloud.oracle.com. Namun, ada dua rintangan besar yang sering dikeluhkan pendaftar baru beserta solusinya:
  A. Rintangan Verifikasi Pendaftaran ("The First Gate")
  Sistem anti-fraud Oracle sangat ketat dan otomatis menolak pendaftaran jika terdeteksi mencurigakan (sering muncul error "transaction could not be processed"). Agar lolos saat daftar:
- Wajib Kartu Kredit atau Debit Fisik (Visa/Mastercard): Kartu virtual (VCC), kartu prabayar, atau e-wallet hampir pasti ditolak oleh sistem verifikasi Oracle.
- Jangan Pakai VPN atau Wi-Fi Publik: Gunakan jaringan internet dari hotspot HP (data seluler) saat mendaftar, dan gunakan jendela browser bersih (matikan adblocker seperti uBlock Origin karena sering memblokir script verifikasi pembayaran).
- Samakan Alamat Tagihan: Pastikan nama dan alamat yang diketik di formulir Oracle sama persis dengan data tagihan kartu di bank.
  B. Rintangan "Out of Host Capacity" & Trik Upgrade PAYG
  Setelah akun aktif, pengguna berstatus Free Tier murni sering kesulitan membuat VPS ARM 12 GB karena slot server untuk akun gratis selalu penuh (Out of host capacity), atau slider di pengaturan terkunci di 1 OCPU / 6 GB.
  Cara mengatasinya (Trik Resmi Tanpa Bayar):
- Setelah akun Free Tier berhasil dibuat, masuk ke pengaturan Billing dan upgrade akun ke Pay-As-You-Go (PAYG).
- Apakah bakal ditagih? Tidak, selama pemakaian tidak melewati batas Always Free. Jatah gratis selamanya tetap berlaku di akun PAYG.
- Keuntungan Upgrade ke PAYG:
  - Antrean pembuatan server langsung diprioritaskan (bebas dari error Out of host capacity).
  - Pada banyak akun yang di-upgrade ke PAYG, batas kuota gratis ARM kembali terbuka hingga 4 OCPU / 24 GB RAM.
  - VPS tidak akan dihapus otomatis oleh sistem idle-reclamation Oracle (pada akun gratis murni, jika pemakaian CPU dan RAM di bawah 20% selama 7 hari berturut-turut, VPS akan dimatikan paksa oleh Oracle).
- Langkah Pengaman: Segera setelah upgrade ke PAYG, buka menu Billing - Budgets dan pasang Budget Alert di angka $0.01 (1 sen). Jadi jika tidak sengaja memilih fitur berbayar, email peringatan akan langsung masuk sebelum tagihan membengkak.

Daftar penyedia Cloud, VPS, dan PaaS (Platform as a Service) selain Oracle dan Vultr yang masih aktif memberikan Free Tier maupun Free Credit, lengkap dengan tautan resmi, spesifikasi riil, aturan pembaruan kebijakan, dan solusi pendaftaran tanpa kartu kredit:

1. Kategori "Always Free" (Gratis Selamanya Tanpa Batas Waktu)
  Selain Oracle Cloud, hanya ada satu penyedia hyperscaler yang masih memberikan VPS penuh gratis selamanya, ditambah beberapa platform container/serverless:
  | Penyedia | Spesifikasi Gratis | Syarat & Batasan Penting | Link Pendaftaran Resmi |
  |---|---|---|---|
  | Google Cloud Platform (GCP) | 1x VPS e2-micro (2 shared vCPU, 1 GB RAM) + 30 GB Standard Persistent Disk + saldo awal $300 (90 hari). | Wajib memilih region AS: Oregon (us-west1), Iowa (us-central1), atau South Carolina (us-east1). Disk wajib diubah ke Standard Persistent Disk (bukan Balanced SSD) saat pembuatan agar tidak kena tagihan. Gratis outbound transfer 1 GB/bulan. | cloud.google.com/free |
  | Google Cloud Run | 2 Juta request/bulan (360.000 GB-detik memori & 180.000 vCPU-detik gratis tiap bulan). | Berbasis Docker container (bukan VPS SSH penuh). Sangat cocok untuk backend API, bot Telegram/Discord, atau web app yang otomatis tidur saat tidak ada trafik. | cloud.google.com/run |
  | Render | 512 MB RAM, 0.1 CPU (Web Services / Docker) + 25 MB Redis gratis selamanya. | Tidak wajib kartu kredit untuk akun dasar. Server otomatis spin down (tidur) jika tidak ada trafik selama 15 menit dan butuh ~1 menit untuk bangun kembali. | render.com/pricing |
2. Kategori Gratis 6 – 12 Bulan & Kredit Saldo Besar (VPS Penuh)
  Jika membutuhkan VPS Linux/Windows utuh dengan akses root SSH untuk jangka menengah (belajar, testing, atau menjalankan proyek 2 hingga 12 bulan):
- Microsoft Azure (Gratis 12 Bulan + Kredit $200):
  - Apa yang didapat: Gratis 750 jam/bulan (aktif 24/7 selama setahun) untuk VPS tipe B1s, B2pts v2 (ARM), atau B2ats v2 (AMD) + 2x 64 GB SSD (P6) + 15 GB bandwidth keluar tiap bulan. Ditambah saldo $200 untuk 30 hari pertama.
  - Link Resmi: azure.microsoft.com/en-us/free
- Amazon Web Services / AWS (Sistem Baru: Kredit hingga $200 selama 6–12 Bulan):
  - Perubahan Aturan: AWS menghapus sistem lama (750 jam t2.micro 12 bulan) untuk pendaftar baru dan menggantinya dengan sistem Free Plan berbasis kredit.
  - Apa yang didapat: Pendaftar baru langsung mendapat $100 kredit awal, ditambah $100 kredit ekstra (total $200) dengan menyelesaikan 5 misi onboarding sederhana di konsol (seperti mencoba membuat instance EC2, RDS, Lambda, Bedrock, dan memasang Budget Alert—masing-masing bernilai $20). Jika memilih Free Plan, akun otomatis tertutup saat kredit habis atau setelah 6 bulan, sehingga mustahil terkena tagihan membengkak.
  - Link Resmi: aws.amazon.com/free
- DigitalOcean (Kredit $200 untuk 60 Hari):
  - Apa yang didapat: Saldo penuh $200 selama 2 bulan. Bebas dipakai membuat VPS (Droplets) spesifikasi besar di region Singapura.
  - Link Resmi: digitalocean.com/try/free-trial-offer
- Akamai Cloud / Linode (Kredit $100 untuk 60 Hari):
  - Apa yang didapat: Saldo $100 selama 2 bulan untuk mencoba VPS NVMe di berbagai lokasi termasuk Singapura dan Jepang.
  - Link Resmi: linode.com/lp/free-credit-100
- Kamatera (Kredit $100 untuk 30 Hari):
  - Apa yang didapat: 1 VPS gratis selama 1 bulan dengan konfigurasi bebas (bisa diatur hingga RAM dan CPU besar selama di bawah nilai kredit $100).
  - Link Resmi: kamatera.com
- Alibaba Cloud (Kredit ECS $90 untuk 3 Bulan):
  - Apa yang didapat: Memberikan kredit khusus Elastic Compute Service (ECS) sebesar $90 (berlaku 90 hari) ditambah kuota gratis untuk uji coba AI Model Studio (Qwen) dan database.
  - Link Resmi: alibabacloud.com/en/free
3. Solusi Tanpa Kartu Kredit (100% Tanpa Verifikasi Bank)
  Jika kendala utamanya adalah penolakan kartu debit/kredit saat mendaftar di Oracle atau Vultr, ini 3 jalur alternatif yang tidak meminta kartu pembayaran sama sekali:
- GitHub Codespaces (VM Linux 4 GB – 8 GB RAM Gratis Tiap Bulan):
  - Setiap akun GitHub gratis mendapatkan jatah 120 core-hours per bulan (setara 60 jam aktif menggunakan VM Linux 2-core / 4 GB RAM, atau 30 jam dengan 4-core / 8 GB RAM) + 15 GB storage.
  - Memiliki akses terminal root penuh, bisa menjalankan Docker, membuka port forwarding ke publik, dan diakses langsung dari browser atau VS Code Desktop tanpa kartu kredit.
  - Link Resmi: github.com/features/codespaces
- Azure for Students (Kredit $100 + VPS 1 Tahun Tanpa Kartu Kredit):
  - Jika memiliki email kampus/sekolah aktif (.ac.id, .edu, atau kartu pelajar/mahasiswa), Microsoft memberikan akses Azure for Students tanpa perlu memasukkan kartu kredit/debit.
  - Mendapatkan saldo $100 selama 12 bulan plus akses VPS gratis (B1s) yang bisa diperpanjang setiap tahun selama masih berstatus pelajar.
  - Link Resmi: azure.microsoft.com/en-us/free/students
- SnapDeploy & Back4App (Container Hosting Tanpa Kartu):
  - Untuk menjalankan aplikasi berbasis Docker atau backend tanpa kartu kredit sama sekali, SnapDeploy (snapdeploy.dev) dan Back4App Containers (back4app.com) menyediakan free tier berbasis kontainer langsung dari repositori GitHub.
4. Daftar Layanan yang Sudah Menghapus Free Tier (Jangan Buang Waktu Daftar)
  Banyak artikel lama di internet yang masih mencantumkan penyedia di bawah ini sebagai penyedia gratis, padahal sudah resmi ditutup atau dihapus:
- Firebase Studio (dulunya Google Project IDX): Google menutup pendaftaran workspace baru sejak 22 Juni 2026 dan layanan akan dimatikan total pada Maret 2027.
- Fly.io: Sudah menghapus free allowance untuk akun baru (sekarang hanya memberikan trial singkat 7 hari / 2 jam mesin dan wajib kartu).
- Heroku, Glitch, & Cyclic: Sudah tidak memiliki paket gratis umum (Glitch resmi menutup layanan hostingnya).
- Koyeb: Kini mewajibkan validasi kartu pembayaran sebelum bisa menjalankan free instance.
  Solusi Praktis: Mana yang Harus Dipilih?
- Jika punya kartu debit/kredit (seperti Jago Visa, Jenius m-Card fisik, atau kartu kredit bank lokal) dan butuh server nyala 24 jam selamanya: Daftar Google Cloud Platform (GCP) dan buat VM e2-micro di region us-west1 (Oregon) dengan Standard Persistent Disk 30 GB. Pendaftaran GCP jauh lebih mudah lolos dibandingkan sistem anti-fraud Oracle.
- Jika ingin bebas dari risiko tagihan kartu sama sekali tapi punya kartu untuk verifikasi awal: Daftar AWS dan pilih Free Plan saat registrasi. Klaim kredit $200 dari misi onboarding, lalu pakai untuk menjalankan server EC2 selama 6 bulan penuh tanpa risiko terpotong saldo sepeser pun.
- Jika tidak ingin memasukkan kartu pembayaran sama sekali: Gunakan GitHub Codespaces untuk kebutuhan coding/bot saat sesi aktif, atau gunakan Render untuk deploy aplikasi web/Docker secara gratis.

gh codespace ssh -- -o ServerAliveInterval=60

Ya, hampir semua penyedia cloud langsung menghitung mundur masa berlaku gratisnya detik itu juga saat pendaftaran dan verifikasi kartu disetujui, bukan saat pertama kali membuat server (VPS).
Jika proyek atau kodingan masih dalam tahap persiapan di laptop/PC, sangat disarankan untuk menahan diri dan jangan mendaftar dulu pada layanan berbasis batas waktu agar kuota harinya tidak terbuang sia-sia.
1. Kapan Waktu Gratis Mulai Dihitung? (Mana yang Harus Ditunda vs Daftar Sekarang) Berikut rincian kapan "arloji" masa gratis mulai berjalan di masing-masing platform:
| Penyedia | Kapan Hitungan Waktu Dimulai? | Strategi Terbaik untuk Kamu |
|---|---|---|
| DigitalOcean, Linode, Vultr (Masa aktif 30–60 hari) | Detik itu juga saat akun selesai diverifikasi. Meski tidak ada 1 pun VPS yang dibuat, saldo kredit akan hangus saat masa 30/60 hari berakhir. | Jangan daftar dulu. Selesaikan proyek di lokal sampai siap 100%, baru daftar saat siap deploy. |
| AWS & Microsoft Azure (Masa aktif 6–12 bulan) | Detik itu juga saat akun aktif. Masa berlaku 6 bulan (AWS Free Plan) atau 12 bulan (Azure) langsung berjalan sejak hari pertama registrasi. | Tunda pendaftaran sampai proyek siap diuji coba di server publik. |
| Google Cloud (GCP) & Oracle Cloud (Kredit $300 + Always Free) | Kredit awal $300 langsung dihitung mundur sejak daftar. Namun, jatah VPS Always Free (12 GB di Oracle / e2-micro di GCP) tidak punya batas waktu kedaluwarsa. | Oracle boleh dicicil daftar sekarang karena proses lolos verifikasi dan antrean servernya butuh waktu. GCP lebih baik tunggu proyek siap agar kredit $300-nya bisa dimanfaatkan maksimal selama 90 hari. |
| GitHub Codespaces & Render (Sistem Reset Bulanan) | Direset ulang setiap bulan (tidak ada masa kedaluwarsa akun). Kalau bulan ini tidak dipakai, bulan depan kuota penuh kembali. | Bebas daftar sekarang. Bisa langsung dipakai untuk tempat ngoding dan testing proyek. |
2. Apakah GitHub Codespaces Bisa Dibuat Menyala 24 Jam Nonstop?
Secara teknis bisa dijaga agar tidak tidur, tetapi ada batasan matematika pada kuota gratisnya yang wajib kamu ketahui sebelum mencobanya:
A. Hitungan Kuota (Kenapa Tidak Bisa 30 Hari Penuh)
 * Akun GitHub gratis mendapatkan jatah 120 core-hours per bulan.
 * Spesifikasi mesin paling kecil di GitHub Codespaces menggunakan 2-core CPU (4 GB RAM).
 * Jika dibagi: 120 \text{ core-hours} \div 2 \text{ core} = \mathbf{60 \text{ jam aktif per bulan}}.
 * Artinya, jika kamu memaksa Codespaces menyala 24 jam nonstop, kuota gratisnya akan langsung habis hanya dalam waktu 2,5 hari (60 jam). Setelah 60 jam, server akan otomatis dimatikan paksa oleh GitHub hingga tanggal reset bulan berikutnya.
B. Cara Membuat Codespaces Tidak Mati Saat Ditinggal (Selama Kuota Masih Ada) Secara bawaan, Codespaces akan otomatis mati (sleep) jika tidak ada aktivitas di layar selama 30 menit. Jika kamu butuh server tetap menyala berjam-jam saat ditinggal (misalnya untuk running script panjang atau testing bot):
 * Ubah Batas Waktu Tidur ke Maksimal (4 Jam):
   * Buka pengaturan akun GitHub di browser: Settings — Codespaces (di menu sebelah kiri).
   * Cari bagian Default idle timeout, lalu ubah dari 30 minutes menjadi 240 minutes (4 jam).
 * Gunakan Trik Koneksi SSH Keep-Alive (Agar Tidak Pernah Tidur):
   * GitHub menghitung waktu idle berdasarkan ada tidaknya koneksi aktif dari perangkatmu ke Codespaces (sekadar menjalankan script loop di dalam terminal web tidak akan mencegahnya tidur jika tab browser ditutup).
   * Agar tetap menyala selama perangkatmu terhubung, buka terminal di laptop atau aplikasi Termux di HP, install GitHub CLI (gh), lalu jalankan perintah SSH dengan pengirim sinyal otomatis setiap 60 detik:
   gh codespace ssh -- -o ServerAliveInterval=60

Selama jendela terminal kecil ini terbuka di latar belakang, Codespaces akan terus menyala 24 jam tanpa terputus sampai kuota 60 jam bulananmu habis.

3. Solusi Alternatif: Cara Dapat Server 24 Jam Penuh (Sebulan Nonstop) Tanpa Kartu Kredit
  Jika tujuan utamamu adalah menjalankan proyek (seperti bot Telegram/Discord, API, atau web) agar menyala 24 jam penuh sepanjang bulan tanpa kartu kredit, jangan gunakan kuota GitHub Codespaces untuk hosting. Gunakan kombinasi ini:
  Gunakan Render + Cron-job.org (750 Jam Gratis / Bulan)
  Berbeda dengan GitHub yang hanya memberi 60 jam mesin, Render.com memberikan kuota 750 jam gratis per bulan (1 bulan penuh = 720 hingga 744 jam, jadi cukup untuk 24 jam nonstop sebulan penuh).
  Kelemahan Render versi gratis hanyalah satu: servernya akan tidur (spin down) jika tidak ada pengunjung selama 15 menit. Cara mengakalinya agar menyala 24 jam nonstop:
- Deploy kodinganmu dari GitHub ke Render (pilih Web Service — Free). Pastikan kodinganmu memiliki satu halaman/rute web sederhana (misalnya rute / yang menampilkan tulisan "Server Aktif").
- Salin URL aplikasi Render milikmu (contoh: [[proyek-kamu.onrender.com](https://proyek-kamu.onrender.com)](https://proyek-kamu.onrender.com)).
- Daftar gratis di cron-job.org atau UptimeRobot (tidak butuh kartu kredit).
- Buat jadwal ping otomatis ke URL Render milikmu setiap 10 atau 14 menit sekali.
- Karena server Render menerima kunjungan otomatis setiap 14 menit, server tersebut tidak akan pernah tidur dan akan menyala 24 jam penuh secara gratis selamanya.

Kabar baiknya: strategi ini 100% bisa dilakukan dan sangat didukung oleh sistem GitHub.
Aturan kuota GitHub menetapkan bahwa untuk repositori milik akun pribadi (Personal Account), kuota 60 jam akan dipotong dari akun orang yang menekan tombol "Create Codespace", bukan dari pemilik repositori. Artinya, proyek dan kodingan tetap terpusat di akun utamamu, tetapi mesin servernya menggunakan jatah gratis dari akun teman-temanmu secara bergantian (sistem estafet) atau bersamaan (load balancing).
1. Hitungan Matematika: Berapa Akun Teman yang Dibutuhkan?
Sebelum menghubungkannya, hitung dulu ketersediaan kuota agar server tidak mati di tengah bulan:
| Jenis Akun GitHub | Kuota Gratis / Bulan | Durasi Nyala Nonstop (2-Core) | Jumlah Akun untuk 1 Bulan Penuh (720 Jam) |
|---|---|---|---|
| Akun Gratis Biasa | 120 core-hours | 60 jam (2,5 hari) per akun | 12 akun (dinyalakan bergantian tiap 2,5 hari) |
| Akun GitHub Student / Pro | 180 core-hours | 90 jam (3,75 hari) per akun | 8 akun (dinyalakan bergantian tiap 3,75 hari) |
> Catatan: Jika jumlah akun temanmu belum mencapai 12 akun (misalnya baru ada 4–5 akun), kamu bisa menghemat kuota dengan menyalakan server hanya pada jam aktif (misalnya 12 jam sehari dari jam 08.00 pagi sampai 20.00 malam), sehingga 6 akun saja sudah cukup untuk 1 bulan penuh.
>
2. Tiga Kunci Agar Pergantian Akun Tetap Stabil (Tidak Kehilangan Data) Karena setiap akun teman akan membuat mesin virtual (kontainer) sendiri-sendiri, kamu tidak boleh menyimpan database di dalam folder lokal Codespace. Gunakan arsitektur 3 lapis ini agar saat berpindah dari akunmu ke akun teman, pengguna tidak merasakan perubahan apa pun:
 * Kodingan Terpusat di Akun Utamamu: Semua kode berada di 1 repositori milikmu. Akun teman hanya dimasukkan sebagai Collaborator.
 * Database Cloud Eksternal (Satu Database untuk Semua Codespace): Jangan gunakan SQLite lokal atau menyimpan file upload di dalam disk Codespace karena datanya tidak akan ikut pindah saat ganti akun teman. Gunakan database cloud gratis selamanya seperti Supabase (PostgreSQL), Neon.tech (PostgreSQL), MongoDB Atlas, atau Turso. Semua Codespace temanmu cukup diarahkan ke URL database yang sama.
 * Satu Link / Jalur Koneksi Tetap:
   * Jika proyekmu adalah Bot (Telegram / Discord / WhatsApp): Kamu hanya perlu mematikan aplikasi di Codespace A, lalu menyalakannya di Codespace B.
   * Jika proyekmu adalah Website / API Backend: URL bawaan Codespace (*.app.github.dev) selalu berubah di setiap akun. Agar link publiknya tetap sama walau berganti-ganti akun teman, pasang Cloudflare Tunnel (cloudflared) gratis. Bahkan jika kamu menyalakan 2 Codespace teman sekaligus, Cloudflare Tunnel otomatis membagi beban trafik (load balancing) dan langsung mengalihkan trafik (failover) tanpa downtime saat salah satu Codespace habis kuotanya.
3. Langkah Demi Langkah Menghubungkan Akun Utama & Akun Teman
1. Undang Akun Teman sebagai Collaborator di Repo Utamamu Wajib jika repositori bersifat Private Buka repositori proyek di akun GitHub utamamu, lalu masuk ke menu Settings — Collaborators — klik Add people. Masukkan username GitHub teman-temanmu dan minta mereka menerima undangan tersebut. Dengan cara ini, mereka punya akses menjalankan proyekmu tanpa perlu memindahkan repositori.
2. Buat File Otomatisasi (.devcontainer) di Repo Utama Agar teman tidak perlu setting manual saat ganti giliran Buat folder bernama .devcontainer di dalam repositori utamamu, lalu isi dengan file devcontainer.json. File ini berfungsi menginstal semua paket dan menyalakan proyek secara otomatis begitu Codespace dibuat oleh akun siapa pun:
   {
  "name": "Server Proyek Utama",
"image": "mcr.microsoft.com/devcontainers/universal:2", "postCreateCommand": "npm install", "postStartCommand": "npm start" }

(Sesuaikan npm install dan npm start dengan bahasa pemrograman proyekmu, misalnya pip install -r requirements.txt dan python main.py untuk Python).

3. Buka Codespace Menggunakan Kuota Akun Teman
  Saat kuota akun utamamu hampir habis (mendekati 60 jam):
  - Login ke akun GitHub temanmu (atau minta temanmu yang melakukannya).
  - Buka halaman repositori proyek di akun utamamu (contoh: [github.com/akun-utamamu/nama-proyek](https://github.com/akun-utamamu/nama-proyek)).
  - Klik tombol hijau Code — pilih tab Codespaces — klik Create codespace on main.
  - Mesin baru akan langsung menyala dengan kodingan terbarumu, dan 100% memotong kuota dari akun teman yang sedang login tersebut.
4. Sinkronisasi Perubahan Kode Saat Berganti Giliran
  Jika ada perubahan kode saat server sedang berjalan di akun Teman 1, cukup jalankan git push ke repositori utamamu. Saat giliran Teman 2 menyalakan Codespace miliknya, dia hanya perlu mengetik git pull di terminal untuk mendapatkan pembaruan terbaru.
5. Jaga Koneksi Tetap Hidup (Estafet 60 Jam)
  Pada akun yang sedang mendapat giliran menyala, ubah pengaturan Default idle timeout ke 240 minutes, lalu jalankan perintah penahan tidur dari terminal laptop atau Termux HP yang login ke akun tersebut:
  gh codespace ssh -- -o ServerAliveInterval=60

   Saat waktu pemakaian akun pertama sudah menyentuh 58–59 jam (bisa dipantau di menu Settings — Billing and plans), nyalakan Codespace di akun teman berikutnya terlebih dahulu, baru matikan Codespace pertama agar server tidak mengalami jeda mati (zero downtime).
Tips Tambahan: Menyimpan Password / API Key Secara Aman Agar kamu tidak perlu mengetik ulang file .env (seperti koneksi database atau token bot) setiap kali berpindah ke akun teman, kamu punya dua opsi:
 * Jika kamu sendiri yang memegang login akun teman-temanmu: Simpan variabel .env di menu Settings — Codespaces — Codespaces secrets pada masing-masing akun dan beri akses ke repositori utamamu.
 * Jika temanmu yang menyalakan dari perangkat mereka sendiri (dan kamu tidak ingin mereka melihat isi password database secara telanjang): Gunakan layanan Secret Manager gratis seperti Doppler (doppler.com). Cukup berikan satu Service Token di perintah jalan, maka aplikasi akan menarik konfigurasi .env secara terenkripsi saat menyala.

Bisa, 100% bisa! Poin 3 (pembuatan Codespace dan proses handover ganti giliran) sangat bisa diotomatisasi, dan idemu untuk meletakkan skripnya langsung di dalam kode/terminal bawaan Codespace adalah langkah yang sangat cerdas.
Jika kamu menggunakan skrip otomatisasi di terminal, teman-temanmu tidak perlu lagi repot klik menu GitHub secara manual. Cukup jalankan satu perintah, atau bahkan bisa dijadwalkan otomatis.
Berikut adalah cara membuat proses estafet akun dan server berjalan otomatis langsung dari dalam kode dan terminal Codespace:
1. Otomatisasi 1: Menyalakan Aplikasi, Database, & Tunnel Sekali Jalan (postCreateCommand) Daripada temanmu harus mengetik perintah manual satu per satu setiap kali membuat Codespace baru, kita bisa memerintahkan file .devcontainer/devcontainer.json untuk menjalankan seluruh persiapannya secara otomatis detik itu juga saat Codespace terbuka.
Buat file .devcontainer/devcontainer.json di repo utamamu dengan format seperti ini:
{
  "name": "Estafet Auto Server",
  "image": "mcr.microsoft.com/devcontainers/universal:2",

  // Perintah yang otomatis berjalan saat Codespace pertama kali dibuat di akun teman:
"postCreateCommand": "bash .devcontainer/setup.sh" }

Lalu, buat file skrip .devcontainer/setup.sh di dalam foldermu untuk merangkap semua perintah terminal:
#!/bin/bash
echo "--- Memulai setup otomatis server proyek ---"

# 1. Install dependensi proyek (ubah sesuai bahasa, contoh: Node.js) npm install

# 2. Download otomatis Cloudflare Tunnel (cloudflared) agar URL permanen curl -L --output cloudflared [github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64) chmod +x cloudflared

# 3. Jalankan aplikasi di latar belakang
npm start &

# 4. Jalankan Cloudflare Tunnel secara otomatis (ganti PORT dengan port aplikasi kalian, misal 3000)
# Ini akan langsung menghasilkan URL publik permanen/random tanpa ribet ./cloudflared tunnel --url [localhost:3000](http://localhost:3000) &

echo "--- Server dan Tunnel Berhasil Aktif Otomatis! ---"

Dengan cara ini, begitu akun temanmu menekan tombol Create Codespace, semuanya langsung menyala sendiri tanpa mereka harus mengetik perintah di terminal.

2. Otomatisasi 2: Bisakah Pembuatan Codespace Akun Selanjutnya Dibuat Otomatis?
  Jika maksudmu adalah “Apakah akun Teman 1 bisa otomatis memerintahkan akun Teman 2 untuk membuat Codespace saat kuotanya hampir habis?”, jawabannya tidak bisa secara langsung karena alasan keamanan (GitHub melarang satu akun men-trigger pembuatan mesin di akun orang lain tanpa izin token OAuth).
  Namun, proses estafetnya bisa dipermudah menggunakan GitHub Actions + API Token:
- Kamu bisa membuat sebuah skrip Cron Job di GitHub Actions yang memantau sisa kuota (misalnya menggunakan GitHub CLI gh api user/billing/codespaces).
- Jika kuota akun Teman 1 tersisa 2 jam lagi, sistem bisa mengirimkan Webhook atau notifikasi otomatis (misalnya ke Discord/Telegram grup kalian) berupa satu link instan.
- Teman 2 tinggal klik link instan tersebut untuk langsung membuat Codespace baru dengan sekali klik, sementara server lama di akun Teman 1 dimatikan otomatis lewat terminal agar tidak terjadi bentrok double server.
3. Peringatan Penting Saat Menggunakan Multi-Akun di Repo yang Sama
  Karena kalian menggunakan banyak akun berbeda untuk satu repositori yang sama, perhatikan 2 hal ini agar tidak error:
- Jangan Commit File Konfigurasi Sensitif: Pastikan file .env atau Token Cloudflare/Database tidak ikut ter-push ke GitHub publik/private. Masukkan file .env ke dalam .gitignore. Gunakan Environment Variables di pengaturan Codespace masing-masing akun atau masukkan lewat skrip instalasi yang aman.
- Database Harus Eksternal: Karena setiap Codespace di akun teman adalah "komputer baru yang bersih", pastikan kodinganmu selalu terhubung ke database cloud (seperti Supabase atau MongoDB Atlas) agar data tidak hilang saat estafet akun dilakukan.
```


<!-- [ID:16_INFRA_DEVOPS_S002] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# 3. 4-GATE DEEP-DEFENSE BANSOS STERILIZER & OMNI-RESOURCE HARVESTER
OMNI_BANSOS_PRESETS = {
    "AI_API": [
        {"res_id": "API-POLLINATIONS-V1", "name": "Pollinations Unified Router (Argon/Muse/Qwen/Flux)", "endpoint": "https://text.pollinations.ai/openai", "meta": "openai", "desc": "Jalur Utama Keyless Cepat (<1.5s) HPP Rp 0", "verified": 1},
        {"res_id": "API-OR-FREE-POOL", "name": "OpenRouter Multi-Model (:free Pool)", "endpoint": "https://openrouter.ai/api/v1/chat/completions", "meta": "deepseek/deepseek-chat:free", "desc": "20+ Model Gratis (Qwen3 Coder, DeepSeek R1, Dolphin 3.0)", "verified": 1 if OPENROUTER_API_KEY else 0},
        {"res_id": "API-GROQ-LPU", "name": "Groq Cloud LPU (Llama 3.3 70B 320 tok/s)", "endpoint": "https://api.groq.com/openai/v1/chat/completions", "meta": "llama-3.3-70b-versatile", "desc": "Kuota Gratis 1.000 RPD Tanpa Kartu Visa", "verified": 1 if GROQ_API_KEY else 0},
        {"res_id": "API-CEREBRAS-1M", "name": "Cerebras Wafer-Scale Free Tier (1M Token/Hari)", "endpoint": "https://api.cerebras.ai/v1/chat/completions", "meta": "llama-3.3-70b", "desc": "Throughput Tinggi Gratis 1 Juta Token/Hari", "verified": 1 if CEREBRAS_API_KEY else 0},
    ],
    "CLOUD_STORAGE": [
        {"res_id": "STOR-CF-R2", "name": "Cloudflare R2 Object Storage (10 GB Gratis)", "endpoint": "https://dash.cloudflare.com/", "meta": "10GB + 0% Biaya Egress Bandwidth", "desc": "Penyimpanan utama media & CDN", "verified": 1},
        {"res_id": "STOR-STORJ-DEPIN", "name": "Storj Decentralized S3 Cloud (25 GB Gratis)", "endpoint": "https://www.storj.io/", "meta": "25GB S3-Compatible Gratis", "desc": "Cadangan Storage Mesh #2", "verified": 1},
        {"res_id": "STOR-B2-BACKBLAZE", "name": "Backblaze B2 Cloud Storage (10 GB Gratis)", "endpoint": "https://www.backblaze.com/cloud-storage", "meta": "10GB Tanpa Kartu Visa", "desc": "Cadangan Storage Mesh #3", "verified": 1},
    ],
    "GRANTS_AND_DB": [
        {"res_id": "GRANT-MODAL-GPU", "name": "Modal.com Serverless GPU ($30/Bulan Gratis)", "endpoint": "https://modal.com/", "meta": "$30/bln Kredit GPU A10G/H100", "desc": "Render ~1.500 video Wan 2.2/bln modal Rp 0", "verified": 1},
        {"res_id": "GRANT-CF-WORKERS-AI", "name": "Cloudflare Workers AI (10.000 Neurons/Hari Gratis)", "endpoint": "https://developers.cloudflare.com/workers-ai/", "meta": "Llama, Qwen, DeepSeek & Flux Edge Inference", "desc": "Inferensi AI tepi gratis setiap hari", "verified": 1},
        {"res_id": "GRANT-MS-FOUNDERS", "name": "Microsoft for Startups Founders Hub ($1K-$150K)", "endpoint": "https://foundershub.startups.microsoft.com/", "meta": "Kredit Azure & OpenAI Tanpa Syarat PT", "desc": "Hibah kredit cloud untuk Solo Founder", "verified": 1},
    ],
}


def validate_safe_external_url(url: str) -> tuple[bool, str]:
    try:
        parsed = urlparse(url.strip())
        if parsed.scheme != "https":
            return False, "Wajib protokol HTTPS."
        host = (parsed.hostname or "").lower()
        if not host or host in ("localhost", "0.0.0.0") or host.endswith((".local", ".internal")):
            return False, "Host internal ditolak oleh proteksi SSRF."
        try:
            ip = ipaddress.ip_address(host)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
                return False, f"Alamat IP privat ({ip}) diblokir."
        except ValueError:
            pass
        return True, "URL Aman"
    except Exception as e:
        return False, f"URL tidak valid: {e}"


def sterilize_community_script_ast(source_code: str, script_name: str = "community_plugin") -> dict[str, Any]:
    forbidden_calls = {"system", "popen", "eval", "exec", "compile", "open", "input", "breakpoint", "spawnl", "getattr", "setattr", "delattr", "globals", "locals", "vars", "dir", "__import__"}
    forbidden_imports = {"os", "sys", "subprocess", "pty", "ctypes", "pickle", "marshal", "shelve", "shutil", "socket", "urllib", "requests", "httpx", "aiohttp", "importlib", "builtins", "inspect"}
    forbidden_dunders = {"__subclasses__", "__globals__", "__builtins__", "__self__", "__import__", "__mro__", "__bases__", "__code__", "__closure__", "__dict__", "__class__"}
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return {"ok": False, "reason": f"SyntaxError: {e}", "hash": "", "threats_removed": [str(e)]}

    stripped_threats: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mod_names = [alias.name.split(".")[0] for alias in node.names]
            if isinstance(node, ast.ImportFrom) and node.module:
                mod_names.append(node.module.split(".")[0])
            for m in mod_names:
                if m in forbidden_imports:
                    stripped_threats.append(f"Blocked import '{m}'")
        elif isinstance(node, ast.Attribute) and (node.attr in forbidden_dunders or node.attr.startswith("__")):
            stripped_threats.append(f"Blocked dunder attribute '{node.attr}'")
        elif isinstance(node, ast.Name) and node.id in forbidden_dunders:
            stripped_threats.append(f"Blocked identifier '{node.id}'")
        elif isinstance(node, ast.Call):
            fn = node.func.id if isinstance(node.func, ast.Name) else (node.func.attr if isinstance(node.func, ast.Attribute) else "")
            if fn in forbidden_calls:
                stripped_threats.append(f"Blocked call '{fn}()'")
        elif isinstance(node, ast.ExceptHandler) and len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            stripped_threats.append("Blocked empty 'except: pass'")

    ast_hash = hashlib.sha256(ast.dump(tree).encode()).hexdigest()[:14]
    if not stripped_threats:
        AUTONOMIC_GUARD.verified_ast_hashes.add(ast_hash)
    return {"ok": len(stripped_threats) == 0, "script_name": script_name, "threats_removed": stripped_threats, "hash": ast_hash}


def sanitize_external_api_response(raw_reply: str) -> str:
    if not raw_reply:
        return ""
    cleaned = re.sub(r"<script\b[^>]*>.*?</script>", "", raw_reply, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"javascript\s*:", "", cleaned, flags=re.IGNORECASE)
    return cleaned.replace("|---|", "").strip()


async def ping_and_verify_bansos_endpoint(endpoint_url: str, model_name: str = "openai", api_key: str = "") -> tuple[bool, float, str]:
    ok_url, reason = validate_safe_external_url(endpoint_url)
    if not ok_url:
        return False, 0.0, reason
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    payload = {"model": model_name or "openai", "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
    t0 = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=2.5, follow_redirects=False) as client:
            r = await client.post(endpoint_url, headers=headers, json=payload)
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
            return (True, elapsed_ms, f"HTTP 200 OK ({elapsed_ms} ms)") if r.status_code == 200 else (False, elapsed_ms, f"HTTP {r.status_code}")
    except Exception as e:
        return False, round((time.perf_counter() - t0) * 1000, 1), f"Timeout ({type(e).__name__})"


async def check_multi_tld_domain_availability_live(base_keyword: str = "bikinai") -> list[dict[str, str]]:
    clean_kw = re.sub(r"[^a-z0-9-]", "", base_keyword.lower()) or "bikinai"
    candidate_domains = [f"{clean_kw}.tech", f"{clean_kw}.xyz", f"{clean_kw}.art", f"{clean_kw}.app", f"{clean_kw}.dev", f"aether-{clean_kw}.xyz"]
    results = []
    async with httpx.AsyncClient(timeout=3.5, follow_redirects=True) as client:
        for dom in candidate_domains:
            try:
                r = await client.get(f"https://rdap.org/domain/{dom}")
                status = "🟢 TERSEDIA (Siap Diklaim!)" if r.status_code == 404 else ("🔴 Terdaftar" if r.status_code == 200 else "🟡 Cek Promo")
            except Exception:
                status = "🟢 Siap Cek di Cloudflare / Porkbun / GitHub Pack"
            results.append({"domain": dom, "status": status})
    return results


