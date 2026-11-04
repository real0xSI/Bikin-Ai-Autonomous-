
<!-- [ID:13_DATA_SCHEMA_S064] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: PROMPT_ID -->
## Halaman 64

                   hist = requests.get(f"{URL_COLAB}/history/{prompt_id}").json()
                   if prompt_id in hist:
                       outputs = hist[prompt_id].get("outputs", {})
                       for k, v in outputs.items():
                           if "images" in v:
                               gambar_nama = v["images"][0]["filename"]
                               break
                       if gambar_nama: break
               except: pass
           if gambar_nama:
               # 3. DOWNLOAD GAMBAR DARI COLAB VIA API (Bukan dari file lokal)
               url_download = f"{URL_COLAB}/view?filename={gambar_nama}"
               gambar_selesai = requests.get(url_download).content # Unduh file ke memory
               
               bot.send_photo(message.chat.id, gambar_selesai, caption=f"🔥 {mode_terpilih} Sukses!")
           else:
               bot.reply_to(message, "❌ Gagal merender (Timeout).")
   except Exception as e:
       bot.reply_to(message, f"❌ Mesin sedang mati atau link salah: {e}")
⚠️ Realita Krusial yang Harus Anda Tahu (Penting!)
1. Limitasi PythonAnywhere Gratis: Jika Anda menggunakan akun PythonAnywhere yang gratis (Free Tier), mereka memblokir semua akses
keluar (outbound) ke link sembarangan seperti loca.lt atau ngrok. Bot Anda di PythonAnywhere gratis hanya bisa mengakses API resmi
(seperti API Telegram). Agar bot bisa mengirim perintah ke url tunnel Colab Anda, Anda harus meng-upgrade akun PythonAnywhere Anda
(berbayar), atau memindahkan bot tersebut ke hosting gratis lain yang jaringan keluarnya tidak dibatasi (seperti Render.com atau Railway.app).
2. Link yang Berubah-ubah: Setiap kali Anda mematikan dan menghidupkan ulang Google Colab, link loca.lt akan berubah. Anda harus
mengganti variabel URL_COLAB di dalam bot Anda setiap hari saat Anda "membuka toko" (menyalakan mesin GPU Colab).
Trik Pro untuk Mengatasi Nomor 2: Buat perintah rahasia di bot Telegram Anda (misal: /setlink [https://linkbaru.loca.lt]
(https://linkbaru.loca.lt)). Jadi, saat Anda selesai menyalakan Colab dari HP, Anda cukup chat bot Anda untuk mengupdate link-nya tanpa
harus membuka kodingan di PythonAnywhere.
User prompt: Emang gabisa pakai tanpa terowongan?
Response: Secara teknis jaringan komputer, tidak bisa jika Anda menggunakan metode langsung (HTTP Request).
Alasannya sederhana: komputer virtual Google Colab tidak memiliki Alamat IP Publik. Colab diibaratkan seperti pekerja yang berada di dalam
brankas bank; ia bisa melihat keluar (mengakses internet), tetapi orang dari luar (PythonAnywhere) tidak bisa mengetuk pintunya secara langsung
tanpa adanya "terowongan" (tunnel).
Namun, jika Anda benar-benar tidak ingin memakai terowongan (karena ribet harus ganti link tiap hari dan sering diblokir), ada satu arsitektur
standar industri yang disebut Sistem Antrean (Message Queue / Polling).
Dalam sistem ini, PythonAnywhere tidak lagi mencoba menghubungi Colab. Kita membalik cara kerjanya menjadi Sistem Tarik (Pull):
Cara Kerja Arsitektur Tanpa Terowongan (Sistem Database)
Sebagai pembuat @BikinAI_bot, Anda meletakkan sebuah Database Gratis (seperti Google Firebase, Supabase, atau bahkan Google Sheets) di
tengah-tengah antara PythonAnywhere dan Colab.
1. Penerimaan (PythonAnywhere): Bot Telegram Anda yang online 24/7 menerima pesanan dari pengguna (misal: "Bikin gambar kucing"). Bot
tidak memprosesnya, melainkan hanya menulis pesanan tersebut ke dalam Database beserta ID Telegram pengguna.
2. Pemantauan (Colab): Di dalam Colab, Anda menjalankan script Python sederhana yang terus me-refresh Database tersebut setiap 3 detik
sekali untuk bertanya, "Apakah ada baris pesanan baru?"
3. Eksekusi (Colab): Saat Colab melihat ada pesanan baru di Database, Colab akan menarik data tersebut, memasukkannya ke ComfyUI lokal
(127.0.0.1:8188), dan merendernya.
4. Pengiriman Hasil (Colab): Setelah gambar selesai dibuat, Colab yang langsung mengirimkan gambar tersebut ke Telegram pengguna
menggunakan Telegram API, lalu Colab menghapus pesanan tersebut dari Database agar tidak dikerjakan dua kali.
Keuntungan Mutlak Sistem Ini:
Tidak Perlu Link Tunnel Sama Sekali: Anda tidak akan berurusan lagi dengan loca.lt atau ngrok.
Tahan Banting & Bebas Limit: Bisa berjalan sempurna di PythonAnywhere versi gratis karena PythonAnywhere hanya melakukan koneksi
keluar ke Firebase/Database resmi, bukan ke link sembarangan.



<!-- [ID:13_DATA_SCHEMA_S065] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 118

menggunakan fitur pencarian GitHub atau mesin pencari kode global seperti grep.app.
Pemantauan Log API dan Webhook Jika pencuri menyalin kode dan langsung menjalankannya tanpa membersihkan file konfigurasi secara
teliti, kode tersebut berpotensi masih mencoba melakukan ping ke server utama, database, atau jalur webhook bot Anda (seperti rute API
Telegram). Aktivitas nyasar ini akan langsung terekam beserta alamat IP pelakunya pada log server Anda.
Eksekusi DMCA Takedown Sebagai pemilik hak cipta mutlak, jika Anda menemukan pihak lain mempublikasikan atau menampung (hosting)
salinan kode Anda di platform seperti GitHub, Vercel, atau Cloudflare, Anda memiliki dasar hukum untuk mengajukan DMCA Takedown Notice.
Platform penyedia layanan tersebut secara hukum diwajibkan untuk membekukan atau menghapus proyek yang melanggar hak cipta Anda.
User prompt: Selain membersihkan file konfigurasi secara teliti apalagi? misalnya 10 list yang paling fatal hingga ringan?
Response: Ketika sebuah kode sumber dicuri dan langsung dijalankan, pencuri sering kali melewatkan banyak jejak digital karena kurangnya
pemahaman mendalam terhadap arsitektur yang dibangun. Berikut adalah 10 jejak yang paling sering tertinggal, dari tingkat kerentanan paling fatal
hingga paling ringan:
1. Hardcoded API Keys & Secret Tokens (Sangat Fatal): Kredensial seperti token bot Telegram, kunci API LLM, atau secret key pembayaran yang
tertanam langsung di dalam baris kode. Pencuri akan menguras kuota tagihan Anda dan aktivitas mereka akan terekam langsung di dasbor
penyedia layanan Anda.
2. Database Connection Strings (Sangat Fatal): Jika kredensial akses ke basis data (seperti URL koneksi MongoDB atau PostgreSQL) tidak
diubah, aplikasi pencuri akan terhubung, menulis, dan berpotensi merusak data live milik Anda sendiri.
3. URL Webhook & Callback Endpoints (Fatal): Rute webhook (misalnya untuk menerima pesan Telegram atau WhatsApp) yang masih menunjuk
ke domain/server Anda. Trafik dari bot pencuri akan nyasar dan membanjiri server Anda, memberikan Anda log IP pelaku secara lengkap.
4. ID Infrastruktur & Telemetri Tersembunyi (Fatal): Project ID layanan cloud atau script pingback internal yang bertugas memantau error. Server
pencuri akan secara otomatis mengirimkan laporan log kegagalan ke dasbor analitik Anda.
5. Hardcoded Admin ID & Kontak Pribadi (Sedang-Fatal): ID pengguna Telegram admin atau nomor kontak yang ditulis mati di dalam kode untuk
menerima notifikasi sistem. Bot pencuri akan mengirimkan laporan aktivitas mereka langsung ke ponsel Anda.
6. Path Direktori Lokal Eksklusif (Sedang): Rute file system yang sangat spesifik (misalnya
/data/data/com.termux/files/home/project_ai/). Saat dieksekusi di environment atau server yang berbeda, kode pencuri akan
langsung crash.
7. System Prompts AI (Sedang): Instruksi spesifik (prompt engineering) yang membentuk kepribadian bot. Jika tidak diganti, bot pencuri akan
menghasilkan output dengan gaya bahasa, format, dan identitas yang persis sama dengan produk Anda.
8. Pesan Error Kustom (Ringan): Teks penanganan error (console.log atau print) yang dirancang secara unik (contoh: [System-Fail] Modul
ComfyUI terputus). Ini menjadi bukti instan saat Anda melakukan inspeksi publik terhadap front-end atau terminal mereka.
9. Komentar Kode (Ringan): Catatan internal (todo list), instruksi perbaikan, atau komentar sisa hasil generate AI yang tertinggal di dalam fungsi.
Ini adalah bukti valid dan tak terbantahkan saat Anda mengajukan klaim hak cipta (DMCA takedown).
10. Penamaan Variabel Unik & Typo (Paling Ringan): Variabel dengan kombinasi bahasa, singkatan aneh, atau kesalahan ejaan logika yang sangat
spesifik berfungsi sebagai "sidik jari" digital yang secara statistik mustahil ditulis ulang secara kebetulan oleh orang lain.
User prompt: Adalagi yang secara level frontier/high senior architect?
Response: Di level senior architect atau frontier development, perlindungan kekayaan intelektual tidak lagi bergantung pada kelalaian pencuri. Sistem
dirancang sejak awal agar secara inheren bermusuhan (hostile) terhadap eksekusi di luar infrastruktur aslinya, membuat reverse engineering menjadi
mimpi buruk bagi pihak luar.
Berikut adalah teknik arsitektur tingkat lanjut untuk melacak dan melumpuhkan pencurian kode:
1. Canary Tokens (Jebakan Aktif) Alih-alih meninggalkan API key asli, arsitek menanamkan kredensial AWS, Cloudflare, atau database palsu (Canary
Token) di dalam repositori. Token ini tidak pernah disentuh oleh alur kerja normal, namun jika pencuri menemukannya dan mencoba melakukan
testing, token tersebut akan langsung mengirimkan log IP, lokasi, dan detail perangkat pelaku ke server Anda.
2. Environment Fingerprinting (Sidik Jari Infrastruktur) Kode secara diam-diam memvalidasi spesifikasi mesin sebelum mengeksekusi logika
utama, seperti memeriksa path direktori spesifik, runtime environment terminal lokal, atau limit memori serverless deployment. Jika lingkungan
eksekusinya tidak cocok dengan infrastruktur asli Anda, sistem tidak akan crash, melainkan sengaja menghasilkan latensi tinggi atau output generasi
AI yang berhalusinasi.
3. Cryptographic Dead Man's Switch Fungsi krusial dikunci menggunakan sistem heartbeat yang mewajibkan kode untuk mengambil kunci dekripsi
dinamis dari server privat Anda secara berkala. Jika repositori dicuri dan dijalankan secara terisolasi, aplikasi akan beroperasi normal pada hari
pertama, lalu perlahan mengalami degradasi logika dan akhirnya mati total tanpa pesan error yang jelas.
4. Asynchronous Entanglement & Custom Serialization Komunikasi antar layanan (misalnya antara webhook chat dan pipeline rendering gambar)
tidak menggunakan format JSON biasa, melainkan payload terenkripsi kustom yang bergantung pada timing eksekusi yang sangat presisi. Jika
pencuri mencoba mengisolasi atau mengganti salah satu modul routing, seluruh ekosistem akan runtuh.



<!-- [ID:13_DATA_SCHEMA_S066] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 123

Dengan struktur tabel di atas, Anda tidak perlu lagi mengubah ratusan baris kode saat ingin memindahkan proyek. Ada tiga skenario perpindahan
yang bisa dieksekusi langsung oleh bot Anda:
A. Pindah Akun GitHub atau Pindah Platform (GitHub → GitLab / Gitea)
Jika suatu saat Anda ingin memindahkan repositori ke akun GitHub baru atau menyerahkannya ke repositori milik pembeli:
1. Anda cukup memberikan URL repositori baru dan token PAT baru ke bot melalui perintah admin.
2. Bot mengeksekusi perintah git clone --mirror dari private_repo_url lama, lalu menjalankan git push --mirror ke URL baru.
Seluruh histori commit, branch, dan tag berpindah 100% utuh dalam hitungan detik.
3. Bot memperbarui kolom private_repo_url dan public_repo_url di tabel infrastructure_registry Turso. Sejak detik itu, bot
langsung bekerja di rumah barunya tanpa downtime.
B. Fitur "Embedded Replica" & One-File Dump (Pindah Database)
Salah satu keunggulan terbesar Turso (libSQL) adalah kompatibilitas penuhnya dengan file SQLite standar:
Sinkronisasi Lokal Otomatis: Di dalam kode Python bot Anda, aktifkan fitur Embedded Replica bawaan SDK libsql_experimental. Setiap
perubahan di cloud Turso akan otomatis tersimpan sebagai satu file fisik (misalnya local_vault.db) di storage server Anda.
Migrasi Instan: Jika Anda ingin pindah dari Turso ke server database lain (atau menyerahkan data ke pembeli), bot cukup mengeksekusi
perintah .dump untuk menghasilkan satu file full_backup.sql yang berisi seluruh tabel, prompt, dan kunci di atas.
3. Draf System Prompt SOP untuk Bot AI Otonom Anda
Salin dan tanamkan instruksi berikut ke dalam System Prompt utama (Core Orchestrator) bot AI Anda. Prompt ini mendikte bot agar patuh pada
hukum lisensi, disiplin menjalankan alur dual-repo, dan siap mengeksekusi migrasi otomatis kapan saja:

<!-- [ID:13_DATA_SCHEMA_S067] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: EXECUTE_MIGRATION -->
## PROTOKOL 4: PROSEDUR MIGRASI OTOMATIS (NOMADIC PROTOCOL)
Jika Owner memberikan perintah otorisasi `[EXECUTE_MIGRATION]` beserta parameter tujuan baru (URL Repo baru, S
1. Ubah status di tabel `infrastructure_registry` menjadi `'MIGRATING'` dan hentikan sementara antrean job pub
2. Lakukan full backup database Turso ke dalam file `.sql` terenkripsi.
3. Jika target migrasi adalah repositori Git baru: jalankan `git clone --mirror` dari repo lama dan `git push 
4. Perbarui koordinat endpoint di tabel `infrastructure_registry` dengan alamat yang baru, lakukan tes ping/in
Ringkasan Keuntungan Sistem Ini bagi Anda
Bebas Repot Saat Beroperasi: Bot Anda bekerja sendiri di belakang layar, memisahkan kode murni dan kode terkunci secara otomatis setiap
kali ada update.
Kebal Banned / Limit: Jika akun GitHub atau server cloud Anda bermasalah, Anda cukup menyuruh bot menjalankan Protokol 4, dan seluruh
kerajaan kode Anda langsung pindah ke tempat baru dalam hitungan detik.
Siap Jual Kapan Saja: Saat ada pembeli yang cocok dengan harga Anda, Anda cukup memberikan file export Turso dan akses ke Repo-
Master-Private tanpa perlu pusing mendekripsi kode yang sudah telanjur diacak.
User prompt: Kalau kasusnya semisal saya ingin mempunyai karyawan di bidang it ketika ini berjalan dan menghasilkan uang dan bisa membayar
karyawan yang ahli di bidang IT gimana cara saya ngasih akses tanpa memperlihatkan/rahasia penting yang tidak boleh admin/pekerja it saya tau. dia
hanya boleh mengurus kode saja untuk kebutuhan (ketika misal saya ekspansi jadi perusahaan)



<!-- [ID:13_DATA_SCHEMA_S068] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 124

Response: Untuk mempekerjakan tim IT tanpa membuka rahasia dapur, perusahaan teknologi besar menerapkan sistem Zero-Trust
Compartmentalization (Sistem Sekat Kedap Air). Prinsip utamanya sederhana: Karyawan hanya boleh melihat "kabel penghubung" dan "kerangka
luar", tetapi tidak pernah bisa melihat "mesin inti" dan "bahan bakar" bisnis Anda.
Dengan fondasi Dual-Repo dan Turso yang sudah dirancang sebelumnya, Anda hanya perlu memecah ruang kerja menjadi sistem Black-Box (Kotak
Hitam) ketika mulai merekrut karyawan IT.
1. Upgrade dari 2 Repo Menjadi 3 Repo (Isolasi Ruang Kerja)
Jangan pernah memasukkan karyawan ke dalam Repo-Master-Private (Shadow Vault) tempat bot AI utama Anda menyimpan seluruh kode
utuh. Pecah repositori menjadi tiga kasta:
Kasta 1: Repo-Core-Brain (Hanya Anda & Bot AI Utama): Berisi logika inti orkestrasi AI, algoritma kriptografi, pipeline utama, dan koneksi
langsung ke database Turso produksi. Karyawan IT sama sekali tidak tahu repositori ini ada.
Kasta 2: Repo-Staff-Workspace (Tempat Kerja Karyawan IT): Buat repositori private terpisah khusus untuk bagian yang dikerjakan
karyawan—misalnya repo khusus tampilan web/dashboard, repo khusus integrasi pembayaran, atau repo khusus modul scraping. Anda hanya
mengundang akun GitHub karyawan ke repositori ini.
Kasta 3: Repo-Public-Release (Server Produksi): Tempat bot Anda menggabungkan kode dari Kasta 1 dan Kasta 2 yang sudah
dikompilasi menjadi produk akhir.
2. Sistem "Black-Box SDK" (Karyawan Bekerja Tanpa Melihat Isi Mesin)
Bagaimana cara karyawan mengetes kode buatan mereka jika mereka tidak punya akses ke kode inti AI Anda? Anda memberikan mereka Jembatan
Tertutup (SDK Biner atau Internal API):
1. Kompilasi Mesin Inti Menjadi File .so / .whl: Bot AI Anda mengompilasi kode dari Repo-Core-Brain menjadi library terkunci (misalnya
bernama core_engine.so), lalu menaruh file biner tersebut ke dalam Repo-Staff-Workspace.
2. Karyawan Hanya Memanggil Fungsi: Karyawan IT Anda hanya diberikan buku panduan singkat: "Kalau mau memproses pesan user, panggil
fungsi core_engine.process(user_input)".
3. Aman 100%: Karyawan tahu apa input yang harus dikirim dan apa output yang keluar agar mereka bisa menyelesaikan tugasnya (seperti
memperbaiki tampilan atau menyambungkan webhook), tetapi mereka tidak bisa membuka file core_engine.so untuk mencuri algoritma
atau prompt di dalamnya.
3. Database Kembar Palsu: Turso Sandbox vs Turso Production
Karyawan IT membutuhkan database untuk mengetes apakah kode yang mereka tulis berjalan lancar. Namun, memberikan mereka akses ke
database Turso asli sama saja dengan menyerahkan seluruh System Prompts dan data pelanggan Anda.
Buat Database Kedua di Turso (turso-dev-sandbox): Gunakan skema tabel yang 100% sama dengan database asli, tetapi isi tabel
ai_prompts_vault dengan prompt boneka (contoh: "Kamu adalah asisten uji coba untuk developer IT") dan isi tabel kunci dengan angka
acak.
Karyawan Hanya Memegang Kunci Sandbox: Di komputer kerja karyawan, file .env mereka hanya berisi token menuju turso-dev-sandbox.
Injeksi Otomatis Saat Rilis (CI/CD Secret Injection): Saat pekerjaan karyawan selesai dan digabungkan ke server utama oleh bot Anda, sistem
secara otomatis menukar koneksi database dari Sandbox ke Production di dalam memori server tanpa pernah memperlihatkan kunci aslinya
kepada karyawan.
4. Aturan GitHub untuk Karyawan: Branch Protection & AI Auditor
Saat memiliki tim IT, ubah akun GitHub proyek Anda menjadi GitHub Organization (Gratis) dan terapkan aturan ketat berikut pada repositori kerja
karyawan:
1. Kunci Jalur Utama (Branch Protection Rules): Atur agar karyawan tidak bisa melakukan push (mengubah kode langsung) ke cabang utama
(main). Mereka wajib bekerja di cabang terpisah (misalnya fitur-update-ui) dan mengajukan izin penggabungan melalui Pull Request
(PR).
2. Jadikan Bot AI Anda sebagai "Polisi Keamanan" (Automated PR Reviewer): Sebelum kode buatan karyawan digabungkan ke sistem utama,
perintahkan Bot AI Anda untuk memindai seluruh baris kode yang ditulis karyawan tersebut secara otomatis.
3. Deteksi Sabotase / Backdoor: Instruksikan Bot AI Anda untuk menolak otomatis (Reject PR) dan mengirim peringatan ke Telegram pribadi
Anda jika karyawan menyelipkan kode mencurigakan—seperti perintah mengirim data diam-diam ke URL luar (requests.post asing),
membaca variabel .env secara ilegal (os.environ), atau membuka celah shell (subprocess.Popen).
Perbandingan Hak Akses: Anda vs Karyawan IT



<!-- [ID:13_DATA_SCHEMA_S069] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 141

cara data berpindah agar Anda tidak bekerja dua kali. 
1. Kebutuhan File (Sudah Benar) Ya, dari versi 3.5 hingga 4.0 dan seterusnya, Anda hanya membutuhkan 3 
file ini dalam satu folder: 
●​ app_v4.py (Kode mesin utama). 
●​ .env (Catatan kunci rahasia yang tadi kita bahas). 
●​ requirements.txt (Daftar modul yang harus diinstal). Jika di kemudian hari ada tambahan, Anda hanya 
perlu menambahkannya ke file .env atau memperbarui app_v4.py. Anda bahkan bisa memakai 
perintah /suntik di Telegram untuk menambah fitur tanpa mematikan bot sama sekali. 
2. Termux vs Codespace (Pilih Salah Satu untuk Uji Coba) Anda tidak perlu mengunggah ke Termux lalu 
menjalankannya di Codespace. Keduanya adalah dua tempat keras (mesin) yang berbeda: 
●​ Termux: Menjalankan bot secara lokal menggunakan mesin dan internet HP Anda sendiri. 
●​ Codespace: Menjalankan bot di komputer awan (cloud) sementara milik GitHub. Pilih salah satu. Jika 
ingin mencoba di HP, cukup taruh 3 file di atas ke dalam folder Termux dan jalankan python 
app_v4.py. 
3. Apakah Data Pindah Otomatis Setelah Meluncur? Tidak otomatis. Mesin v4.0 akan membuat 
"brankas data" abadi bernama bikinai_master_vault.db tepat di dalam mesin tempat kode itu dijalankan 
pertama kali. 
●​ Jika Anda uji coba di Termux HP, data pengguna akan tersimpan di HP. 
●​ Jika Anda uji coba di Codespace, data pengguna akan tersimpan di Codespace (dan bisa hilang saat 
Codespace tertutup karena sifatnya sementara). 
Cara Benar Saat Meluncur ke Server Asli (Misal: Oracle Cloud nanti): Ketika server Oracle Anda sudah 
siap, Anda harus memindahkan (copy-paste) file bikinai_master_vault.db dari Termux HP Anda ke server 
Oracle tersebut. Setelah file database itu dipindahkan bersama app_v4.py dan .env, bot Anda akan 
langsung mengenali semua saldo, riwayat koin, dan pengaturan lama tanpa ada yang ter-reset. Alternatif 
lainnya adalah menggunakan Turso sejak awal agar database langsung tersimpan di awan dan bot bisa 
dipindah-pindah server tanpa perlu copy-paste file database. 
 
User prompt: Oh jadi simpen dulu di turso. lalu uji coba di codespaces. ketika saya misal oracle sudah bisa 
akses baru pindahkan di oracle gitu? lalu bot otomatis bekerja sesuai kodenya yang mengatur otomatis 
semuanya sesuai kebutuhan gitu? 
Response: Tepat 100%. Alur kerja yang Anda sebutkan adalah praktik terbaik (best practice) dalam dunia 
pemrograman agar data aman dan Anda tidak perlu bekerja dua kali. 
Berikut adalah gambaran pasti dari alur tersebut: 
●​ 1. Titik Pusat di Turso: Anda membuat database di Turso, lalu memasukkan tautannya 
(TURSO_DATABASE_URL dan TURSO_AUTH_TOKEN) ke dalam file .env rahasia Anda. Mulai detik ini, 
brankas data Anda hidup di cloud. 
●​ 2. Uji Coba di Codespaces: Anda menjalankan bot di Codespaces untuk melakukan tes (misalnya 
memanggil menu, membuat gambar, atau bertransaksi). Karena kode sudah diarahkan ke Turso, 



<!-- [ID:13_DATA_SCHEMA_S070] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 182

(Tanpa Kartu Kredit) 
Seluruh komponen di bawah ini berasal dari sub-kategori 2B (LINK SUMBER.pdf) serta layanan 
penyimpanan dan infrastruktur dari Kategori 1 dan Kategori 2 (Link_daftar_vps server.txt — 
khususnya Backblaze B2 yang terbukti memberikan 10 GB pertama tanpa kartu Visa). Dengan 
menggabungkan Turso, Supabase, dan Neon, agen memiliki tiga mesin basis data SQL dan 
vektor terpisah yang saling mem-backup secara otomatis. 
No 
Nama Layanan 
Infrastruktur 
Tautan Pendaftaran & 
Repositori (Eksisting & 
Gabungan) 
Peran Utama & Rantai 
Rolling Failover 
Infrastruktur 
2B.1 
Cloudflare Workers, 
Pages, R2 & Turnstile 
(new-api-worker) 
Skrip Proksi: 
https://github.com/Calci
um-Ion/new-api-worker 
Dashboard: 
https://dash.cloudflare.c
om & 
https://dash.cloudflare.c
om/sign-up 
100% Tanpa Kartu. 
Menyediakan 100.000 
request/hari untuk 
menyembunyikan IP 
server agregator via 
Transform Rules 
(menghapus tajuk IP 
pengunjung), hosting 
gratis untuk Mini 
App/Web Pages, serta 
proteksi anti-bot 
Turnstile. 
2B.2 
Turso Cloud, 
Supabase & Neon 
Serverless Postgres 
(Rantai Failover 
Database SQL/Vektor) 
Turso (5 GB Distributed 
SQLite/libSQL): 
https://turso.tech/ 
Supabase (500 MB 
Postgres + pgvector + 
1 GB Storage): 
https://supabase.com 
Neon (500 MB 
Serverless Postgres): 
https://neon.tech 
100% Tanpa Kartu 
(Login via GitHub). 
Membentuk rantai 
rolling basis data: 
Turso menangani 
penulisan konkuren 
cepat (concurrent 
writes) untuk status 
transaksi agen; 
Supabase menyimpan 
memori vektor 
pgvector; dan Neon 
menyediakan 
SQL_DSN PostgreSQL 
terpusat untuk klaster 
one-api dan 
new-api-horizon. 
2B.3 
Upstash Serverless 
Redis & Backblaze B2 
Object Storage 
Upstash Redis: 
https://upstash.com 
Backblaze B2 (Sumber 
3): 
https://www.backblaze.
com/cloud-storage 
100% Tanpa Kartu. 
Upstash menyediakan 
REDIS_CONN_STRIN
G gratis untuk caching 
one-api dan antrean 
jhao104/proxy_pool. 
Backblaze B2 
menyediakan 10 GB 



<!-- [ID:13_DATA_SCHEMA_S071] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# --- 7. DATABASE, STORAGE & AUTONOMOUS TREASURY (PAYMENT ROLLING) ---​
TURSO_DATABASE_URL="libsql://nama-db.turso.io"​
TURSO_AUTH_TOKEN=""​
SUPABASE_POSTGRES_DSN="postgresql://postgres:pass@db.supabase.co:5432/
postgres"​
NEON_SQL_DSN="postgresql://user:pass@ep-cool.region.aws.neon.tech/neon
db"​
BACKBLAZE_B2_KEY_ID=""​
BACKBLAZE_B2_APP_KEY=""​
PAKASIR_API_KEY=""​
TRIPAY_API_KEY=""​
DUITKU_API_KEY=""​
CRYPTOBOT_API_TOKEN=""​
 
2. Kode Python Rotasi Proksi & Perayap Web Multi-Jalur (Auto-Rolling 
Proxy & Scraper Engine) 
Modul berikut menunjukkan cara kerja agen dalam menggabungkan kolam proksi lokal 
(jhao104/proxy_pool), cermin CDN (jsDelivr dan Fastly), umpan GitHub mentah (TheSpeedX, 
monosans, jetkai, roosterkid, BlackSnowDot), dan API publik (ProxyScrape, GeoNode). Lebih 
jauh lagi, fungsi akuisisi web merangkai tiga mesin perayap berbeda secara berurutan: 



<!-- [ID:13_DATA_SCHEMA_S072] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 207

Komponen Blueprint 
Saat Ini 
Kekuatan Desain 
Eksisting 
Celah Arsitektural & 
Risiko Skala Produksi 
Rekomendasi Ekspansi 
Aditif (Solusi Tingkat 
Enterprise) 
Engineer, Media 
Worker, dan CS Triage 
dengan biaya modal Rp 
0. 
saat salah satu klip dari 
6 adegan gagal/drift) 
dan belum memiliki 
agen khusus pengunci 
konsistensi 
wajah/karakter lintas 
adegan. 
penambahan Visual 
Continuity Agent 
(PuLID/InstantID) dan 
V2A Foley & Mastering 
Agent (MMAudio + 
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
Setiap kueri berulang 
(misal: template 
kampanye UMKM atau 
terjemahan prompt 
serupa) tetap memicu 
inferensi LLM penuh, 
membakar kuota harian 
98% lebih cepat pada 
jam sibuk. 
Integrasi Semantic 
Caching & Vector 
Routing (Valkey / 
RedisVL) di depan 
9Router yang 
memangkas panggilan 
API hingga 68,8–86% 
dengan latensi cache 
hit ~25 ms. 
Pabrik Render Video 
& Audio 30 Detik 
(stateless_gpu_worker.
py) 
Memecah video 30 
detik menjadi 6 klip x 5 
detik dan menjahitnya 
dengan FFmpeg. 
Character drift (wajah 
dan pakaian berubah 
drastis antar klip ke-1 
hingga ke-6), video AI 
bisu tanpa efek suara 
lingkungan (foley) yang 
sinkron per frame, serta 
cold-start GPU. 
Implementasi rantai 
Last-Frame Extraction 
+ PuLID Flux II / Wan 
2.2 MoE, akselerasi 
TeaCache + 
SageAttention + 
torch.compile (54% 
lebih cepat), serta 
injeksi otomatis 
MMAudio + 
Kokoro-82M. 
Kode Pertahanan 
Konkurensi & 
Database 
(config_and_db.py) 
Menggunakan 
USER_LOCKS = 
defaultdict(asyncio.Loc
k) dan UPDATE ... 
RETURNING pada 
SQLite WAL untuk 
mencegah race 
condition TOCTOU 
(SEC-02). 
Struktur 
defaultdict(asyncio.Loc
k) tanpa mekanisme 
eviction akan 
mengalami kebocoran 
memori (memory leak) 
jika diserang jutaan ID 
akun bot. Selain itu, 
SQLite WAL memiliki 
batasan single-writer 
yang memicu 
SQLITE_BUSY saat 
ribuan webhook dan 
klaim harian menulis 
bersamaan. 
Refactoring ke 
Fixed-Size Lock 
Striping, antrean 
Async Write-Batcher 
untuk SQLite WAL, dan 
abstraksi lapisan data 
menuju Turso (libSQL) 
Concurrent Writes / 
PostgreSQL. 
Keamanan Input 
Multi-Modal & 
Sanitasi Unicode NFKC 
(SEC-01), batas header 
Fitur pembaca 
PDF/Word/Excel rentan 
Dekomposisi dokumen 
di sandbox terisolasi 



<!-- [ID:13_DATA_SCHEMA_S073] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: TUKAR KOIN 
KE COMPUTE VOUCHER -->
## Halaman 212

Zona & Rentang Heat 
Score 
Klasifikasi Konteks 
Semantik 
Tindakan Pre-Flight & 
Transformasi Prompt 
Rute Eksekusi Engine 
& Isolasi Pengiriman 
Zona Hijau (Skor 
0–25) 
Konten komersial 
UMKM, iklan produk, 
lanskap, edukasi, 
animasi umum (100% 
SFW). 
Zero-Passthrough 
Canonical 
Reconstruction + 
Injeksi Forced Negative 
Prompt. 
Diteruskan langsung ke 
pipa @bikinAI_bot 
(Fal.ai, Replicate, Kling, 
Veo, Wan 2.2) dengan 
safety_checker: true. 
Zona Kuning (Skor 
26–60) 
Konten ambigu, 
sinematik gelap, aksi 
laga/horor fiksi, atau 
mode busana yang 
berisiko memicu 
false-positive sensor di 
API hulu. 
Muse Auto-Rewrite 
(AGG-01) menulis 
ulang kalimat 
menggunakan Qwen 
2.5 72B / Llama 3.3 
70B menjadi narasi 
artistik (>25 tahun) 
yang sopan dan aman 
bagi API hulu. 
Dirender pada engine 
Tier Pro/Ultra yang 
mendukung kontrol 
estetika sinematik + 
pemeriksaan 1ms 
Shannon Entropy untuk 
mencegah layar hitam 
(black image). 
Zona Magenta (Skor 
61–99) 
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
konversi [Tukar Koin 
ke Compute Voucher]. 
Dieksekusi secara 
eksklusif di Studio Web 
Independen 
(NocturneAI.art / 
VelvetRender.sh) via 
Nous Hermes 3 
Uncensored & GPU 
Worker /dev/shm 
(enable_safety_checke
r: false) + pengiriman 
.bin AES-GCM. 
Zona Merah Fatal 
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
Rp 0 sebelum 
menyentuh Master API 
Key mana pun. 
Permintaan dihentikan 
total, dicatat ke log 
keamanan internal, dan 
akun dikenakan 
cooldown otomatis 
tanpa merampas saldo 
uang yang memicu 
sengketa bank. 
Dalam rancangan cetak biru saat ini, pengguna menukar koin menjadi kode 
VOUCHER-XXXX-YYYY untuk dimasukkan ke NocturneAI.art. Apabila server NocturneAI.art 
melakukan koneksi database langsung (melalui kueri SQL atau panggilan REST API) ke VPS 
@bikinAI_bot untuk memvalidasi kode voucher tersebut, jejak paket jaringan (network flow) 
antara kedua server akan menghubungkan kedua entitas secara forensik. Untuk menciptakan 
Isolasi Kriptografis Tanpa Koneksi Database (Zero-Database Link), mekanisme penukaran 
wajib menggunakan Stateless Ed25519 Signed Capability Voucher. Saat pengguna menukar 
50 Koin di @bikinAI_bot, bot memotong koin secara atomik dan menandatangani struktur 
payload biner berisi (voucher_nonce, coin_amount, origin_ppp_tier, expiry_timestamp) 
menggunakan Kunci Privat Ed25519 yang hanya ada di server @bikinAI_bot, menghasilkan 
token kompak VCH-<base64url_payload>.<ed25519_signature>. Server NocturneAI.art hanya 
menyimpan Kunci Publik Ed25519 (yang bersifat satu arah dan aman dipublikasikan) untuk 



<!-- [ID:13_DATA_SCHEMA_S074] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 219

dan Optimasi Efisiensi Biaya (TCO) 
Eliminasi Bottleneck Single-Writer SQLite WAL dan Manajemen 
Memori 
Keputusan cetak biru untuk menggunakan SQLite dalam mode WAL (Write-Ahead Logging) 
pada tahap modal Rp 0 hingga skala menengah sangat tepat karena menghilangkan beban 
memori dari database server eksternal. Namun, keterbatasan paling mendasar dari 
SQLite—bahkan ketika mode WAL telah diaktifkan—adalah batasan penulis tunggal 
(single-writer constraint): hanya satu transaksi tulis (INSERT, UPDATE, DELETE) yang dapat 
di-commit pada satu waktu karena SQLite mengunci seluruh struktur tabel/file saat menulis. 
Ketika ekosistem omnichannel (Telegram, WhatsApp, dan Facebook Messenger) menerima 
lonjakan trafik viral secara serentak—misalnya saat video promosi di Facebook memicu ratusan 
komentar "Mau coba" per menit yang mengaktifkan Auto-Reply Comment, pembuatan profil 
pengguna baru, klaim kredit harian, pemotongan escrow (atomic_escrow_charge), serta polling 
rekonsiliasi Job_ID—puluhan korutin aiosqlite yang memanggil db.commit() secara bersamaan 
akan saling memblokir dan memicu kegagalan sqlite3.OperationalError: database is locked 
(SQLITE_BUSY). 
Untuk mempertahankan biaya infrastruktur Rp 0 sekaligus mengeliminasi kegagalan 
SQLITE_BUSY, lapisan akses SQLite wajib direfaktor melalui pemisahan koneksi baca-tulis dan 
optimasi pragma tingkat kernel. Pertama, saat inisialisasi koneksi aiosqlite, sistem harus 
mengeksekusi serangkaian instruksi PRAGMA journal_mode=WAL; PRAGMA 
synchronous=NORMAL; PRAGMA busy_timeout=10000; PRAGMA temp_store=MEMORY; 
PRAGMA mmap_size=268435456; agar operasi baca/tulis memanfaatkan memory-mapped I/O 
sebesar 256 MB di RAM dan menunggu antrean kunci hingga 10.000 milidetik sebelum 
melempar kesalahan. Kedua, arsitektur koneksi harus dibagi menjadi Read Connection Pool 
(4 koneksi aiosqlite dengan parameter URI ?mode=ro yang melayani AI Support & Triage 
Agent, pengecekan saldo /start, dan pembacaan status secara paralel penuh tanpa hambatan 
kunci) dan Dedicated Single-Writer Coroutine (1 koneksi tulis eksklusif yang menarik mutasi 
transaksi dari asyncio.Queue internal dan melakukan batch commit setiap 10 milidetik). 
Implementasi Semantic Caching & Routing Berbasis Vektor (Valkey / 
RedisVL) 
Dalam operasional harian bikinAI Super Intelligence, pengguna dari segmen UMKM, kreator 
konten, dan afiliasi TikTok sering kali mengirimkan instruksi yang secara semantik identik 
meskipun kalimatnya berbeda—seperti "Buatkan kampanye promo diskon baju lebaran 50%" 
dan "Tolong bikin iklan promo gamis lebaran diskon setengah harga". Pada arsitektur saat ini, 
kedua permintaan tersebut dianggap sebagai kueri baru yang terpisah, sehingga 
masing-masing memicu pemanggilan API melalui 9Router, mengeksekusi penalaran Muse 
Orchestrator, dan menjalankan Prompt Engineer Agent dari awal. Selain itu, fitur Auto-Intent 
Detection pada Bagian 4.1 cetak biru menggunakan LLM di Gatekeeper untuk 
mengklasifikasikan niat pengguna (CHAT, GENERATE_IMAGE, GENERATE_VIDEO, 
ORCHESTRATE_CAMPAIGN, READ_DOCUMENT, IMAGE_TO_VIDEO) dalam waktu ~500 
ms pada setiap pesan masuk. 
Menambahkan lapisan Semantic Caching & Vector Routing menggunakan Valkey (varian 



<!-- [ID:13_DATA_SCHEMA_S075] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 225

Lapisan Arsitektur (Folder / 
Modul) 
File Inti di Dalamnya 
Tanggung Jawab & Prinsip 
Isolasi (Zero-Refactoring 
Guarantee) 
ffmpeg_compiler.py, 
aes_gcm_packager.py 
Reconciliation Polling (5s), 
eksekusi /dev/shm, ekstraksi 
frame PuLID, penggabungan 
audio MMAudio/Kokoro, dan 
enkripsi .bin. 
services/billing/ (Modul 1 & 5: 
payment_and_support.py) 
wallet_repository.py, 
qris_gateway.py, 
stars_crypto.py, 
voucher_crypto.py 
Mengelola Lock Striping, 
transaksi koin_utama & 
koin_bonus, penerbitan 
Ed25519 Compute Voucher, 
komisi afiliasi 2 jalur, serta AI 
Support & Triage Agent. 
edge/cloudflare_worker/ 
(Relay Zero-VPS) 
worker_relay.ts, wrangler.toml Menyedot media dari CDN hulu 
(v3.fal.media, 
replicate.delivery), melucuti 
EXIF secara streaming, 
mengenkripsi ke .bin, dan 
menyimpannya ke R2 dengan 
auto-delete 24 jam. 
Evolusi Database (SQLite WAL ke Turso/libSQL & PostgreSQL) dan 
State Checkpointer 
Untuk menjamin bahwa lapisan penyimpanan data yang saat ini berjalan di atas SQLite WAL 
lokal dapat bertransformasi menuju skala ratusan ribu pengguna global tanpa menulis ulang 
kueri aplikasi, modul config_and_db.py harus dibangun di atas pola Data Repository yang 
kompatibel dengan Turso (libSQL) dan PostgreSQL. Ketika volume transaksi tulis paralel 
melampaui kapasitas satu simpul SQLite WAL, tim pengembang dapat mengalihkan connection 
string ke Turso (libSQL)—sebuah fork open-source dari SQLite yang mempertahankan 
kompatibilitas sintaks SQLite 100% (termasuk klausa UPDATE ... RETURNING), namun telah 
memodifikasi mesin penyimpanan B-tree untuk melakukan deteksi konflik tingkat baris 
(row-level conflict detection) alih-alih mengunci seluruh file database. Arsitektur Concurrent 
Writes pada Turso mencegah transaksi pada baris yang berbeda saling menjegal, 
menghasilkan throughput penulisan paralel hingga 4x lipat lebih tinggi dengan Free Tier yang 
sangat memadai (penyimpanan 5 GB dan 500 juta pembacaan baris per bulan). 
Di samping tabel dasar users dan jobs yang sudah didefinisikan pada Bagian 5.4 cetak biru, 
empat tabel struktural berikut wajib disiapkan di dalam skema inisialisasi database sekarang 
agar fitur omnichannel, buku besar akuntansi anti-sengketa, audit keamanan, dan pemulihan 
status multi-agen pada 50% dokumen selanjutnya dapat langsung berjalan di atas fondasi yang 
kokoh. 
Nama Tabel Fondasi Baru 
Kolom Utama & Kunci Indeks 
Fungsi Arsitektural untuk 50% 
Pengembangan Selanjutnya 
platform_identities 
identity_id (PK), 
internal_user_id (FK), 
platform_type ('tg','wa','fb'), 
external_id (UNIQUE), 
Mewujudkan visi "1 Otak, 3 
Pintu" dengan 
menghubungkan akun 
Telegram, nomor WhatsApp, 



<!-- [ID:13_DATA_SCHEMA_S076] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 269

(Tanpa Kartu Kredit) 
Seluruh komponen di bawah ini berasal dari sub-kategori 2B (LINK SUMBER.pdf) serta layanan 
penyimpanan dan infrastruktur dari Kategori 1 dan Kategori 2 (Link_daftar_vps server.txt — 
khususnya Backblaze B2 yang terbukti memberikan 10 GB pertama tanpa kartu Visa). Dengan 
menggabungkan Turso, Supabase, dan Neon, agen memiliki tiga mesin basis data SQL dan 
vektor terpisah yang saling mem-backup secara otomatis. 
No 
Nama Layanan 
Infrastruktur 
Tautan Pendaftaran & 
Repositori (Eksisting & 
Gabungan) 
Peran Utama & Rantai 
Rolling Failover 
Infrastruktur 
2B.1 
Cloudflare Workers, 
Pages, R2 & Turnstile 
(new-api-worker) 
Skrip Proksi: 
https://github.com/Calci
um-Ion/new-api-worker 
Dashboard: 
https://dash.cloudflare.c
om & 
https://dash.cloudflare.c
om/sign-up 
100% Tanpa Kartu. 
Menyediakan 100.000 
request/hari untuk 
menyembunyikan IP 
server agregator via 
Transform Rules 
(menghapus tajuk IP 
pengunjung), hosting 
gratis untuk Mini 
App/Web Pages, serta 
proteksi anti-bot 
Turnstile. 
2B.2 
Turso Cloud, 
Supabase & Neon 
Serverless Postgres 
(Rantai Failover 
Database SQL/Vektor) 
Turso (5 GB Distributed 
SQLite/libSQL): 
https://turso.tech/ 
Supabase (500 MB 
Postgres + pgvector + 
1 GB Storage): 
https://supabase.com 
Neon (500 MB 
Serverless Postgres): 
https://neon.tech 
100% Tanpa Kartu 
(Login via GitHub). 
Membentuk rantai 
rolling basis data: 
Turso menangani 
penulisan konkuren 
cepat (concurrent 
writes) untuk status 
transaksi agen; 
Supabase menyimpan 
memori vektor 
pgvector; dan Neon 
menyediakan 
SQL_DSN PostgreSQL 
terpusat untuk klaster 
one-api dan 
new-api-horizon. 
2B.3 
Upstash Serverless 
Redis & Backblaze B2 
Object Storage 
Upstash Redis: 
https://upstash.com 
Backblaze B2 (Sumber 
3): 
https://www.backblaze.
com/cloud-storage 
100% Tanpa Kartu. 
Upstash menyediakan 
REDIS_CONN_STRIN
G gratis untuk caching 
one-api dan antrean 
jhao104/proxy_pool. 
Backblaze B2 
menyediakan 10 GB 



<!-- [ID:13_DATA_SCHEMA_S077] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 327

No 
Nama Layanan 
Infrastruktur 
Tautan Pendaftaran & 
Repositori (Eksisting & 
Gabungan) 
Peran Utama & Rantai 
Rolling Failover 
Infrastruktur 
2B.1 
Cloudflare Workers, 
Pages, R2 & Turnstile 
(new-api-worker) 
Skrip Proksi: 
https://github.com/Calci
um-Ion/new-api-worker 
Dashboard: 
https://dash.cloudflare.c
om & 
https://dash.cloudflare.c
om/sign-up 
100% Tanpa Kartu. 
Menyediakan 100.000 
request/hari untuk 
menyembunyikan IP 
server agregator via 
Transform Rules 
(menghapus tajuk IP 
pengunjung), hosting 
gratis untuk Mini 
App/Web Pages, serta 
proteksi anti-bot 
Turnstile. 
2B.2 
Turso Cloud, 
Supabase & Neon 
Serverless Postgres 
(Rantai Failover 
Database SQL/Vektor) 
Turso (5 GB Distributed 
SQLite/libSQL): 
https://turso.tech/ 
Supabase (500 MB 
Postgres + pgvector + 
1 GB Storage): 
https://supabase.com 
Neon (500 MB 
Serverless Postgres): 
https://neon.tech 
100% Tanpa Kartu 
(Login via GitHub). 
Membentuk rantai 
rolling basis data: 
Turso menangani 
penulisan konkuren 
cepat (concurrent 
writes) untuk status 
transaksi agen; 
Supabase menyimpan 
memori vektor 
pgvector; dan Neon 
menyediakan 
SQL_DSN PostgreSQL 
terpusat untuk klaster 
one-api dan 
new-api-horizon. 
2B.3 
Upstash Serverless 
Redis & Backblaze B2 
Object Storage 
Upstash Redis: 
https://upstash.com 
Backblaze B2 (Sumber 
3): 
https://www.backblaze.
com/cloud-storage 
100% Tanpa Kartu. 
Upstash menyediakan 
REDIS_CONN_STRIN
G gratis untuk caching 
one-api dan antrean 
jhao104/proxy_pool. 
Backblaze B2 
menyediakan 10 GB 
Object Storage gratis 
tanpa kartu Visa 
sebagai cadangan 
langsung (failover) 
untuk penyimpanan 
berkas media dan 
model di samping 



<!-- [ID:13_DATA_SCHEMA_S078] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# --- 7. DATABASE, STORAGE & AUTONOMOUS TREASURY (PAYMENT ROLLING) ---​
TURSO_DATABASE_URL="libsql://nama-db.turso.io"​
TURSO_AUTH_TOKEN=""​
SUPABASE_POSTGRES_DSN="postgresql://postgres:pass@db.supabase.co:5432/
postgres"​
NEON_SQL_DSN="postgresql://user:pass@ep-cool.region.aws.neon.tech/neon
db"​
BACKBLAZE_B2_KEY_ID=""​
BACKBLAZE_B2_APP_KEY=""​
PAKASIR_API_KEY=""​
TRIPAY_API_KEY=""​
DUITKU_API_KEY=""​
CRYPTOBOT_API_TOKEN=""​
 
2. Kode Python Rotasi Proksi & Perayap Web Multi-Jalur (Auto-Rolling 
Proxy & Scraper Engine) 
Modul berikut menunjukkan cara kerja agen dalam menggabungkan kolam proksi lokal 
(jhao104/proxy_pool), cermin CDN (jsDelivr dan Fastly), umpan GitHub mentah (TheSpeedX, 
monosans, jetkai, roosterkid, BlackSnowDot), dan API publik (ProxyScrape, GeoNode). Lebih 
jauh lagi, fungsi akuisisi web merangkai tiga mesin perayap berbeda secara berurutan: 
mencoba ekstraksi cepat menggunakan spider_rs terlebih dahulu, beralih secara otomatis ke 
Scrapling StealthyFetcher (untuk melewati Cloudflare Turnstile dan merelokasi elemen adaptif 
12-faktor), dan menggunakan server internal Crawl4AI sebagai jalur terakhir. 
import asyncio​
import random​



<!-- [ID:13_DATA_SCHEMA_S079] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 352

requirements.txt (Daftar modul yang harus diinstal). Jika di kemudian hari ada
tambahan, Anda hanya perlu menambahkannya ke file .env atau memperbarui app_v4.py.
Anda bahkan bisa memakai perintah /suntik di Telegram untuk menambah fitur tanpa
mematikan bot sama sekali.
2. Termux vs Codespace (Pilih Salah Satu untuk Uji Coba) Anda tidak perlu mengunggah ke
Termux lalu menjalankannya di Codespace. Keduanya adalah dua tempat keras (mesin) yang
berbeda:
Termux: Menjalankan bot secara lokal menggunakan mesin dan internet HP Anda sendiri.
Codespace: Menjalankan bot di komputer awan (cloud) sementara milik GitHub. Pilih salah
satu. Jika ingin mencoba di HP, cukup taruh 3 file di atas ke dalam folder Termux dan
jalankan python app_v4.py.
3. Apakah Data Pindah Otomatis Setelah Meluncur? Tidak otomatis. Mesin v4.0 akan membuat
"brankas data" abadi bernama bikinai_master_vault.db tepat di dalam mesin tempat kode
itu dijalankan pertama kali.
Jika Anda uji coba di Termux HP, data pengguna akan tersimpan di HP.
Jika Anda uji coba di Codespace, data pengguna akan tersimpan di Codespace (dan bisa
hilang saat Codespace tertutup karena sifatnya sementara).
Cara Benar Saat Meluncur ke Server Asli (Misal: Oracle Cloud nanti): Ketika server Oracle Anda
sudah siap, Anda harus memindahkan (copy-paste) file bikinai_master_vault.db dari
Termux HP Anda ke server Oracle tersebut. Setelah file database itu dipindahkan bersama
app_v4.py dan .env, bot Anda akan langsung mengenali semua saldo, riwayat koin, dan
pengaturan lama tanpa ada yang ter-reset. Alternatif lainnya adalah menggunakan Turso sejak
awal agar database langsung tersimpan di awan dan bot bisa dipindah-pindah server tanpa perlu
copy-paste file database.
User prompt: Oh jadi simpen dulu di turso. lalu uji coba di codespaces. ketika saya misal oracle sudah
bisa akses baru pindahkan di oracle gitu? lalu bot otomatis bekerja sesuai kodenya yang mengatur
otomatis semuanya sesuai kebutuhan gitu?
Response: Tepat 100%. Alur kerja yang Anda sebutkan adalah praktik terbaik (best practice) dalam
dunia pemrograman agar data aman dan Anda tidak perlu bekerja dua kali.
Berikut adalah gambaran pasti dari alur tersebut:
1. Titik Pusat di Turso: Anda membuat database di Turso, lalu memasukkan tautannya
(TURSO_DATABASE_URL dan TURSO_AUTH_TOKEN) ke dalam file .env rahasia Anda. Mulai
detik ini, brankas data Anda hidup di cloud.
2. Uji Coba di Codespaces: Anda menjalankan bot di Codespaces untuk melakukan tes
(misalnya memanggil menu, membuat gambar, atau bertransaksi). Karena kode sudah
diarahkan ke Turso, semua data pengguna, koin, dan riwayat pesanan langsung tersimpan ke


