# Oh caranya tetap per sesi chat menyambung- terus d....pdf


## Halaman 1

Tidak perlu membuat sesi chat yang menyambung-nyambung panjang, karena semakin 
panjang satu sesi chat, AI justru akan mengalami context rot (lupa instruksi awal dan 
mulai memotong kode). 
Cara paling tajam dan bersih adalah 1 Sesi Chat Baru (Fresh Chat) = 1 Modul Spesifik, lalu 
semua kode yang dihasilkan AI langsung Anda tempel (paste) ke dalam GitHub Codespaces 
yang sudah memiliki struktur folder (monorepo) dari File Master. 
1. Hitungan Pasti: Akan Menjadi Berapa File? 
Dari total data mentah Anda (2 PDF = 868 halaman + 1 MD = 3,8 juta karakter), berikut adalah 
rincian matematika jumlah file yang akan lahir di dalam folder/ZIP Anda: 
Jenis Output di Dalam 
Folder / ZIP 
Perhitungan 
Matematika Data Anda 
Jumlah File yang 
Dihasilkan 
Aturan Pakai di Chat AI 
1. File Master Peta 
Otak & Index 
(02_MASTER_1_SAM
PAI_3_FILE...) 
Merangkum ±1.200 
judul bab, fungsi kode, 
gambar, dan tag 
AUTO_DISCOVERY 
(masing-masing dikunci 
≤ 45.000 karakter). 
2 sampai 3 File .md 
Di-upload di awal untuk 
mencetak kerangka 
folder GitHub 
Codespaces & file 
kontrak 
(interfaces/schema). 
2. File Pecahan Modul 
MD 
(03_MODUL_MD_MUR
NI_MAKS_45K...) 
Total ~6,3 juta karakter 
gabungan (setelah 
dikurangi duplikat 
kembar identik menjadi 
~5,2 juta karakter) 
dibagi 45.000 karakter. 
~115 sampai 135 File 
.md (Terbagi rapi ke 
26+ nama domain, 
misal 
02_CORE_AI_01.md 
s/d 05.md) 
Upload 1 file .md saja 
per chat saat ingin 
menyuruh AI menulis 
kode modul tersebut. 
3. File Pecahan PDF 
Visual 
(04_MODUL_PDF_MU
RNI_MAKS_20...) 
868 halaman PDF 
dibagi tepat 20 
halaman per file PDF 
utuh. 
44 File .pdf (43 file isi 
20 halaman + 1 file isi 8 
halaman) 
Upload 1 file .pdf saja 
per chat (tanpa MD) 
khusus saat bagian itu 
berisi diagram/tabel 
rumit yang butuh dilihat 
mata AI. 
4. Koleksi 
Gambar/Diagram Asli 
(05_KOLEKSI_GAMBA
R_DIAGRAM_PDF) 
Ekstraksi gambar 
diagram arsitektur 
murni dari 868 halaman 
PDF oleh MinerU. 
~150 – 400 File 
.jpg/.png 
Cadangan visual murni 
jika Anda ingin 
mengaudit gambar 
diagram secara 
terpisah. 
5. Laporan Audit 
Lossless 
(00_LAPORAN_AUDIT.
md) 
Bukti hitungan jumlah 
karakter masuk vs 
keluar (0% hilang). 
1 File .md 
Untuk Anda baca 
sendiri sebagai bukti 
verifikasi. 
2. Bagaimana Cara Menggabungkan Kodenya di GitHub Codespaces? 
Agar kode dari 100+ file pecahan tadi bisa langsung menyatu dan jalan di GitHub Codespaces 
tanpa bentrok (tidak ada nama variabel/fungsi yang beda antara chat ke-1 dan chat ke-50), 
gunakan alur 3 Langkah Monorepo ini: 
1.​ Langkah 1: Cetak "Kerangka Monorepo & Kontrak Global" (Cuma 1x di Awal) 
○​ Buka sesi chat AI, upload 00_MASTER_PETA_OTAK_PART_01.md (dan Part 2/3 


## Halaman 2

secara berurutan). 
○​ Minta AI membuatkan Script Generator Struktur Folder (init_monorepo.sh) + 
file shared_contracts.py / schema.prisma / .env.example yang berisi 
nama-nama fungsi, database table, dan message broker standar untuk ke-26 
domain Anda. 
○​ Jalankan script itu di terminal GitHub Codespaces Anda. Dalam 5 detik, 
Codespaces Anda sudah punya semua folder untuk 26 modul beserta aturan 
mainnya. 
2.​ Langkah 2: Isi Daging Kodenya per Modul (Fresh Chat agar AI 100% Fokus) 
○​ Sekarang Anda ingin mengisi kode untuk folder 02_CORE_AI. 
○​ Buka Chat Baru (agar memori AI segar 100%). Upload 1 file saja: 
02_CORE_AI_SWEETSPOT_01.md (45k karakter). 
○​ Berikan prompt: "Berdasarkan blueprint mentah di file ini, tuliskan kode produksi 
lengkap tanpa ada fitur atau baris logika yang dipotong untuk modul CORE_AI, 
sesuai kontrak monorepo kita." 
○​ Salin kode hasilnya ke dalam folder src/02_core_ai/ di GitHub Codespaces Anda. 
3.​ Langkah 3: Uji Jalan & Integrasi di Codespaces 
○​ Karena sejak awal semua modul mengacu pada nama fungsi dan skema database 
yang tercatat di 00_MASTER_PETA_OTAK, begitu file-file kode itu ditaruh di 
foldernya masing-masing di GitHub Codespaces, semuanya langsung saling kenal 
dan siap dijalankan (docker-compose up atau pytest). 
3. Apakah Harus Konek Google Drive Dulu atau Auto-Download ZIP? 
Wajib kombinasikan keduanya (Konek Google Drive DULU + Buat File ZIP Otomatis). 
Mengapa JANGAN hanya mengandalkan files.download() bawaan browser Google Colab? 
●​ Proses ekstraksi 868 halaman PDF menggunakan MinerU membutuhkan waktu sekitar 
30–45 menit. 
●​ Jika tab browser Anda tidak sengaja tertutup, internet berkedip 2 detik, atau sesi Colab 
idle, fungsi auto-download via browser pasti gagal/putus di tengah jalan dan Anda 
harus mengulang 45 menit dari nol. 
●​ Selain itu, ukuran total folder (teks + 44 PDF pecahan + ratusan gambar + cache MinerU) 
bisa mencapai 500 MB – 1,5 GB. Browser Colab sering crash saat mengunduh file di 
atas 300 MB secara langsung. 
Tambahkan Blok Kode Ini di Bagian Paling Atas & Paling Bawah Skrip Colab 
Anda: 
1. Taruh di Sel Paling Atas (Sebelum Menjalankan Skrip Utama): 
from google.colab import drive​
drive.mount('/content/drive')​
​
# Arahkan OUTPUT_DIR langsung ke Google Drive Anda agar real-time 
tersimpan aman:​
from pathlib import Path​
OUTPUT_DIR = Path("/content/drive/MyDrive/BLUEPRINT_FINAL_LOSSLESS")​
 
2. Taruh di Sel Paling Bawah (Setelah Skrip Selesai untuk Membungkus ZIP & 


## Halaman 3

Auto-Download): 
import shutil​
from google.colab import files​
​
# 1. Buat paket ZIP Ringan (Hanya File Master + Modul MD 45k + Laporan 
Audit -> ~15-25 MB)​
zip_ringan_path = "/content/drive/MyDrive/PAKET_SIAP_UPLOAD_AI_MD_45K"​
shutil.make_archive(zip_ringan_path, 'zip', root_dir=OUTPUT_DIR, 
base_dir="02_MASTER_1_SAMPAI_3_FILE_SWEETSPOT_45K")​
​
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

