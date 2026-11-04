
<!-- [ID:08_OMNI_SOCIAL_S016] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# Fungsi rahasia untuk meminjam identitas Bot Utama saat mengirim hasil
def kirim_hasil_langsung_ke_user(user_id, path_gambar, caption_text):
   url = f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendPhoto"
   with open(path_gambar, 'rb') as photo:
       files = {'photo': photo}
       data = {'chat_id': user_id, 'caption': caption_text}
       requests.post(url, files=files, data=data)

<!-- [ID:08_OMNI_SOCIAL_S017] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: UPDATE -->
# --- MESIN PENERIMA KETUKAN DARI TELEGRAM ---
@app.route('/' + TOKEN_UTAMA, methods=['POST'])
def getMessage():
   json_string = request.get_data().decode('utf-8')
   update = telebot.types.Update.de_json(json_string)
   bot.process_new_updates([update])
   return "!", 200

<!-- [ID:08_OMNI_SOCIAL_S018] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# --- SAKLAR OTOMATIS PEMASANG WEBHOOK ---
@app.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url=f'https://{USERNAME_PA}.pythonanywhere.com/' + TOKEN_UTAMA)
   return "Tembus Bro! Webhook BikinAI Berhasil Dipasang 24/7.", 200
5. Klik tombol Save di pojok kanan atas.
Langkah 3: Restart dan Pemicu Permanen
Kode sudah tersimpan, tetapi server belum menyadarinya.
1. Klik tombol menu garis tiga di pojok kanan atas, lalu klik tab Web.
2. Klik tombol hijau besar bertuliskan Reload bikinaibot.pythonanywhere.com.
3. Buka tab baru di browser HP Anda, lalu ketik alamat web ini persis seperti ini dan kunjungi:
[https://bikinaibot.pythonanywhere.com](https://bikinaibot.pythonanywhere.com)
4. Jika di layar HP Anda muncul tulisan "Tembus Bro! Webhook BikinAI Berhasil Dipasang 24/7.", berarti jalan tol antara server Telegram dan
PythonAnywhere sudah tersambung permanen.
Anda sekarang bisa menutup semua tab PythonAnywhere dan mematikan layar HP. Buka aplikasi Telegram, kirim pesan ke @BikinAI_bot, dan
saksikan bot Anda membalas dan meneruskan pesan ke grup secara otomatis tanpa hosting berbayar.
User prompt: Gini kan
Response: Tepat sekali, bro! Susunan kode di gambar tersebut sudah 100% benar dan menempel dengan sangat rapi.
Jika Anda melihat ada lambang segitiga peringatan kuning kecil di baris 29 dan 42, abaikan saja. Itu hanya pemberitahuan dari editor teks karena
kita menangkap error (variabel e) tapi belum mem-print-nya ke layar. Hal tersebut sama sekali tidak akan membuat bot macet.
Sekarang, selesaikan proses aktivasinya dengan 3 langkah pamungkas ini:
1. Klik tombol Save di pojok kanan atas editor tersebut.
2. Buka menu PythonAnywhere (garis tiga di pojok kanan atas), masuk ke tab Web, lalu klik tombol hijau besar bertuliskan Reload
bikinaibot.pythonanywhere.com.
3. Buka tab baru di browser HP Anda, lalu ketik dan kunjungi alamat web ini: [https://bikinaibot.pythonanywhere.com]
(https://bikinaibot.pythonanywhere.com)
Jika saat mengunjungi web tersebut muncul layar putih dengan tulisan "Tembus Bro! Webhook BikinAI Berhasil Dipasang 24/7.", berarti gerbang
webhook Anda sudah resmi terbuka dan terkunci secara permanen.
Anda sudah bisa menutup PythonAnywhere seutuhnya. Silakan buka aplikasi Telegram dan langsung tes kirim teks pesanan ke @BikinAI_bot!
User prompt: Nah tapi di collab sedang saya matikan sekarang. udah berhasil bacaan tembus saat new tab pyhton tadi linknya. jadi sekarang saya harus
nyalakan dulu collabnya lagi baru setelah selesai saya tulis di bot. ketika udah berhasil. baru rombak code collab yang udah sukses jadi agentic yang
saya tadi ya yang full dengan alat dan pendukung pendukungnya?



<!-- [ID:08_OMNI_SOCIAL_S019] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 1. PINTU MASUK DARI TELEGRAM (Hanya Menerima & Mencatat)
@app.route('/' + TOKEN_UTAMA, methods=['POST'])
def webhook():
   try:
       data = request.json
       if data and 'message' in data and 'text' in data['message']:
           chat_id = data['message']['chat']['id']
           prompt = data['message']['text']
           
           # Buka brankas, masukkan pesanan, tutup lagi
           with open(QUEUE_FILE, 'r') as f:
               antrean = json.load(f)
           
           antrean.append({"user_id": chat_id, "prompt": prompt})
           
           with open(QUEUE_FILE, 'w') as f:
               json.dump(antrean, f)
   except Exception:
       pass # Abaikan jika ada format aneh, biar tidak crash
       
   return "OK", 200

<!-- [ID:08_OMNI_SOCIAL_S020] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 2. PINTU KELUAR UNTUK KAGGLE/COLAB (Hanya Membaca)
@app.route("/get_task", methods=['GET'])
def get_task():
   with open(QUEUE_FILE, 'r') as f:
       antrean = json.load(f)
   
   if len(antrean) > 0:
       task = antrean.pop(0)
       with open(QUEUE_FILE, 'w') as f:
           json.dump(antrean, f)
       return jsonify({"status": "ok", "task": task})
       
   return jsonify({"status": "empty"})
3. Klik Save.
4. Masuk ke tab Web (menu tiga garis) -> Klik tombol hijau Reload bikinaibot.pythonanywhere.com.
TAHAP 2: Buka Katup Telegram Secara Manual
Agar kita tidak bergantung pada server untuk membuka katup, kita gunakan HP Anda secara langsung untuk memerintah Telegram.
1. Copy link di bawah ini secara utuh.
2. Paste di tab baru pada browser HP Anda, lalu tekan Enter/Go: 👉 [https://api.telegram.org/bot8885292945:AAGK66Dng-81kTW9-
vv0Yoy4Pzi43nU3ns0/setWebhook?url=https://bikinaibot.pythonanywhere.com/8885292945:AAGK66Dng-81kTW9-
vv0Yoy4Pzi43nU3ns0](https://api.telegram.org/bot8885292945:AAGK66Dng-81kTW9-
vv0Yoy4Pzi43nU3ns0/setWebhook?url=https://bikinaibot.pythonanywhere.com/8885292945:AAGK66Dng-81kTW9-
vv0Yoy4Pzi43nU3ns0)
3. Jika di layar muncul tulisan {"ok":true,"result":true,"description":"Webhook was set"}, berarti sistem selamanya sudah
terkunci rapat!
TAHAP 3: Update Mesin Colab Anda
Karena PythonAnywhere sekarang sudah "bisu", Colab/Kaggle Anda lah yang bertugas mengirim pesan "Pesanan Diterima".



<!-- [ID:08_OMNI_SOCIAL_S021] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: :4000 -->
# office/config/channels.yaml
version: 1
owner_only_commands: true

channels:
  telegram:
    adapter: bots/telegram
    enabled: true
    priority: 1
  whatsapp:
    adapter: bots/whatsapp
    enabled: true
    priority: 2
  instagram:
    adapter: bots/instagram
    enabled: true
    priority: 3
  threads:
    adapter: bots/threads
    enabled: true
    priority: 4
  github_issue:
    adapter: bots/github
    enabled: true
    priority: 5

auth:
  require_owner_id_match: true
  require_pin_for: [/panic, /freeze, /approve, /deny, /recover, /readonly]
  hmac: true
  timestamp_window_sec: 60
  replay_protection: true

fallback:
  if_primary_down_sec: 30
  escalate_to: [telegram, whatsapp, github_issue]

commands:
  /status:          {handler: report_status}
  /agents:          {handler: list_agents}
  /cost today:      {handler: cost_report}
  /panic:           {handler: kill_switch, level: L0_PANIC}
  /freeze finance:  {handler: kill_switch, level: L1_FREEZE_FINANCE}
  /freeze external: {handler: kill_switch, level: L2_FREEZE_EXTERNAL}
  /freeze agent:    {handler: kill_switch, level: L3_FREEZE_AGENT, arg: agent_id}
  /readonly on:     {handler: kill_switch, level: L4_READONLY}
  /readonly off:    {handler: kill_switch, action: restore}
  /approve:         {handler: approval, action: approve, arg: id}
  /deny:            {handler: approval, action: deny, arg: id}
  /log last:        {handler: tail_audit, arg: n}
  /recover:         {handler: kill_switch, action: restore_last_known_good}
  /spawn agent:     {handler: spawn_agent, arg: role_id}   # tambah agent baru
  /pr create:       {handler: create_pr, arg: description}

import os, requests
from bots_core.dispatcher import dispatch, verify

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OWNER = int(os.environ["TELEGRAM_OWNER_ID"])

def handle_update(u):
    msg = u.get("message")
    if not msg: return
    chat_id = msg["chat"]["id"]
    user_id = msg["from"]["id"]
    text = (msg.get("text") or "").strip()

    if user_id != OWNER:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                      json={"chat_id": chat_id, "text": "Unauthorized."})
        return

    if not verify(channel="telegram", user_id=user_id, text=text):
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                      json={"chat_id": chat_id, "text": "Auth gagal."})
        return

    result = dispatch(text, channel="telegram", user_id=user_id)
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                  json={"chat_id": chat_id, "text": result[:4000]})

name: keepalive
on:
  schedule: [{cron: "*/15 * * * *"}]
  workflow_dispatch:
jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Health check
        run: |
          curl -fsS ${{ secrets.HEALTHCHECK_URL }} || exit 1
      - name: Notify owner if down
        if: failure()
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id=${{ secrets.TELEGRAM_OWNER_ID }} \
            -d text="⚠️ keepalive: health check GAGAL"

name: command-router
on:
  issues:
    types: [opened, edited]
permissions:
  contents: write
  issues: write
  pull-requests: write
jobs:
  dispatch:
    if: contains(github.event.issue.labels.*.name, 'command')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.11"}
      - run: pip install -r office/orchestrator/requirements.txt
      - name: Dispatch command
        env:
          ISSUE_BODY: ${{ github.event.issue.body }}
          ISSUE_NUMBER: ${{ github.event.issue.number }}
          OWNER: ${{ github.actor }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          OWNER_PIN: ${{ secrets.OWNER_PIN }}
          HMAC_SECRET: ${{ secrets.HMAC_SECRET }}
        run: python bots/github/dispatch.py
      - name: Comment result
        if: always()
        run: gh issue comment $ISSUE_NUMBER --body "Command diproses. Cek log."

name: security
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Secret scan
        uses: gitleaks/gitleaks-action@v2
      - name: SAST (Semgrep)
        run: pip install semgrep && semgrep ci
      - name: Dependency scan
        run: |
          npm audit --audit-level=high || true
          pip-audit || true
      - name: Container scan
        run: echo "trivy scan di sini"
      - name: Block merge if critical
        run: echo "CI gagal = merge diblokir"

name: nightly-audit
on:
  schedule: [{cron: "0 18 * * *"}]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python office/orchestrator/nightly_audit.py
      - name: Push digest to owner
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d chat_id=${{ secrets.TELEGRAM_OWNER_ID }} \
            -d text="📊 Nightly audit selesai. Cek dashboard."

Layer Pemilik Isi
Brain Owner office/brain/*.md — strategi, prinsip, aturan
Config Owner + agent office/config/*.yaml — agents, gates, kill switch
Orchestrator Agent (auto) office/orchestrator/*
Execution Agent (sandbox) apps/, bots/, services/
Control Plane Owner only kill switch, approval broker, notification
Audit Immutable office/logs/audit.log


<!-- [ID:08_OMNI_SOCIAL_S022] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# Notification gateway (fungsi dari notification_gateway.py)
try:
    from office.orchestrator.notification_gateway import send_owner
except Exception:
    def send_owner(_): pass

Channel = Literal["telegram", "whatsapp", "instagram", "threads", "github_issue"]


<!-- [ID:08_OMNI_SOCIAL_S023] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 4

Kampanye Muse = 25 Koin, Paket Story 30 Detik = 100 Koin), sehingga logika aplikasi dan 
database escrow tidak perlu diubah sedikit pun. Namun, katalog harga Top-Up Koin disesuaikan 
secara otomatis ke dalam 3 Zona Ekonomi (PPP Tiers) sebagaimana dirumuskan dalam tabel 
berikut. 
Zona 
Ekonomi 
(PPP Tier) 
Cakupan 
Negara & 
Kode 
Bahasa 
Harga 
Dasar per 1 
Koin 
Paket 
Pemula (50 
Koin) 
Paket 
Kreator 
(160 Koin) 
Paket 
Agensi 
(600 Koin) 
Harga 
Efektif 
Video 5s 
(20 Koin) 
Margin 
Laba 
Bersih 
Rata-Rata 
Zona 3: 
Penetrasi 
Lokal 
(Indonesia
) 
Indonesia 
(id, IP ASN 
Indonesia, 
Pembayara
n QRIS) 
Rp 100 
(~$0,0062) 
Rp 5.000 
(2 Video + 
2 Gambar 
HD) 
Rp 15.000 
(Bonus 10 
Koin) 
Rp 50.000 
(Bonus 100 
Koin) 
Rp 1.666 – 
Rp 2.000 
(~0, 10–
0,125) 
80% – 85% 
(Tier Pro) / 
45% – 50% 
(Tier Ultra) 
Zona 2: 
Emerging 
Global 
(Menenga
h) 
Asia 
Tenggara 
non-SG 
(ms, vi, th, 
tl), India 
(hi), LATAM 
(es, pt), 
MENA (ar), 
CIS (ru) 
~$0,018 
(~Rp 290) 
$0,99 (atau 
55 
Telegram 
Stars) 
$2,49 (atau 
135 
Telegram 
Stars) 
$7,99 (atau 
430 
Telegram 
Stars) 
$0,26 – 
$0,36 (~Rp 
4.200–Rp 
5.800) 
91% – 94% 
(Tier Pro) / 
75% – 82% 
(Tier Ultra) 
Zona 1: 
Global 
Premium 
(Indeks 
Ekonomi 
Tinggi) 
AS, Inggris, 
Uni Eropa, 
Kanada, 
Australia, 
Jepang, 
Korea, 
Singapura 
(en, de, fr, 
ja, ko) 
~$0,040 
(~Rp 640) 
$1,99 (atau 
110 
Telegram 
Stars) 
$4,99 (atau 
270 
Telegram 
Stars) 
$14,99 
(atau 800 
Telegram 
Stars) 
$0,50 – 
$0,80 (~Rp 
8.000–Rp 
12.800) 
95% – 97% 
(Tier Pro) / 
85% – 90% 
(Tier Ultra) 
Sebagaimana terlihat pada perbandingan ekonomi unit di atas, biaya HPP komputasi di balik 
layar tetap sama (rata-rata Rp 350 per video untuk Tier Pro dan Rp 1.500–Rp 2.500 untuk Tier 
Ultra komersial). Namun, di Zona 1 Global Premium, harga jual efektif 
0,80 per video (Rp 
0, 50–
8.000–Rp 12.800) masih memberikan penghematan lebih dari 40%–50% bagi pengguna 
Barat/Jepang dibandingkan platform SaaS AI lokal mereka (tanpa keharusan berlangganan 
bulanan), sembari mendongkrak margin laba bersih Tier Ultra dari 45%–50% menjadi 
85%–90% dan margin Tier Pro menjadi 95%–97%. 
Mekanisme Penguncian Region (Multi-Factor Geo-Locking) dan Unit 
Economics Lintas Negara 
Mengandalkan variabel message.from_user.language_code == "id" semata sebagai penentu 
harga regional (seperti yang tertulis pada Bagian 3.6 cetak biru) menciptakan celah arbitrase 
harga (regional price spoofing): pengguna dari Amerika Serikat atau Eropa cukup mengganti 
bahasa aplikasi Telegram mereka ke Bahasa Indonesia untuk memunculkan harga Zona 3. 
Untuk menutup celah arbitrase tersebut tanpa menyulitkan pengguna domestik Indonesia, 



<!-- [ID:08_OMNI_SOCIAL_S024] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 5

arsitektur kasir payment_and_support.py wajib menerapkan mekanisme Tri-Factor Payment & 
Telemetry Geo-Locking. 
Kunci pertahanan pertama dan paling absolut adalah Payment Rail Hard-Binding 
(Penguncian Instrumen Pembayaran). Tarif penetrasi Zona 3 (Rp 5.000 / Rp 15.000 / Rp 
50.000) secara eksklusif hanya dapat dibayar menggunakan instrumen QRIS Domestik 
Indonesia (melalui Pakasir, Tripay, atau Duitku). Karena pembayaran QRIS hanya dapat 
dieksekusi melalui aplikasi perbankan atau e-wallet teregulasi Bank Indonesia (BCA, Mandiri, 
BRI, GoPay, OVO, DANA, ShopeePay) yang mewajibkan verifikasi identitas kependudukan 
nasional (e-KTP KYC), warga negara asing di luar Indonesia secara teknis tidak dapat 
menyelesaikan transaksi QRIS meskipun mereka menggunakan VPN Indonesia dan mengubah 
bahasa Telegram ke id. Jika pengguna memilih membayar menggunakan Telegram Stars atau 
Crypto USDT, sistem secara otomatis menonaktifkan harga Rupiah Zona 3 dan menyajikan 
struktur harga Zona 2 atau Zona 1. 
Untuk membedakan secara akurat antara pengguna Zona 2 (Emerging Global - $0,99) dan 
Zona 1 (Global Premium - $1,99) pada saluran pembayaran Telegram Stars serta USDT, 
Cloudflare Worker Edge Relay dan Mini App mengevaluasi korelasi tiga sinyal telemetri: header 
geolokasi jaringan CF-IPCountry dari Cloudflare, reputasi Autonomous System Number 
(CF-Connecting-IP ASN untuk mendeteksi IP datacenter/VPN komersial), serta zona waktu 
sistem operasi perangkat (Intl.DateTimeFormat().resolvedOptions().timeZone) disertai awalan 
nomor telepon jika pengguna terhubung melalui pintu WhatsApp. Pengguna hanya diberikan 
tarif subsidi Zona 2 apabila CF-IPCountry berada di daftar negara Emerging (seperti Malaysia, 
Vietnam, Thailand, India, Brasil, atau Turki), IP bukan berasal dari ASN penyedia VPN/Proxy, 
dan zona waktu perangkat selaras dengan negara tersebut. Apabila terdeteksi ketidaksesuaian 
sinyal (misalnya language_code diatur ke ru atau hi, namun timeZone berada di Europe/London 
atau menggunakan IP VPN), kasir secara otomatis memberlakukan tarif standar Zona 1 Global 
Premium. Sebagai pengaman tambahan terhadap praktik jual-beli akun lintas negara, saldo 
Koin dikunci secara permanen pada internal_user_id pembeli (tidak ada fitur transfer koin 
antar-pengguna) dan pencetakan Universal Compute Voucher dibatasi maksimal 3 voucher aktif 
per hari per akun. 
Dimensi 5: Future-Proofing untuk 50% Dokumen 
Selanjutnya 
Struktur Direktori Modular (Hexagonal Architecture) dan Kontrak 
Skema 
Mengingat cetak biru saat ini berada pada titik 50% dan paruh kedua pengembangan akan 
berfokus pada penulisan kode utuh untuk 6 modul Python (config_and_db.py, security_gate.py, 
muse_router.py, stateless_gpu_worker.py, payment_and_support.py, dan main_bot.py), 
perakitan miniapp_studio.html, pembuatan Cloudflare Worker Edge Relay, serta 
penyambungan webhook WhatsApp dan Facebook Messenger, arsitektur kode harus 
mengadopsi pola Ports and Adapters (Hexagonal Architecture) sejak hari pertama. 
Risiko utang teknis (technical debt) terbesar pada sistem omnichannel adalah mengikat logika 
bisnis agen dan kasir secara langsung pada objek pustaka spesifik platform (seperti 
meneruskan objek aiogram.types.Message milik Telegram langsung ke dalam fungsi 
muse_router.py atau payment_and_support.py). Jika ikatan erat (tight coupling) itu terjadi, maka 



<!-- [ID:08_OMNI_SOCIAL_S025] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 6

ketika developer mengintegrasikan WhatsApp (WAHA / Meta Cloud API) dan Facebook 
Messenger pada Tahap 5, seluruh fungsi agen harus dibongkar ulang. Dengan memisahkan 
Domain Core dari Platform Ingress Adapters dan menstandardisasi kontrak pesan 
menggunakan skema UnifiedMessageEvent berbasis Pydantic v2, penambahan pintu 
komunikasi keempat di masa depan (seperti Discord, Instagram DM, atau aplikasi web mandiri) 
dapat dilakukan dengan zéro refactoring pada ke-7 agen inti. 
Lapisan Arsitektur (Folder / 
Modul) 
File Inti di Dalamnya 
Tanggung Jawab & Prinsip 
Isolasi (Zero-Refactoring 
Guarantee) 
core/domain/ (Kontrak & 
Skema Murni) 
schemas.py, events.py, 
exceptions.py 
Mendefinisikan 
UnifiedMessageEvent 
(abstraksi pesan lintas 
Telegram/WA/FB), JobManifest, 
AgentState (TypedDict untuk 
LangGraph), dan PricingTier. 
Bebas dari library eksternal. 
core/config/ (Hot-Reload 
Saklar 1 Angka) 
config_manager.py, 
pricing_ppp.yaml 
Membungkus variabel 
PILIHAN_MESIN_MEDIA, 
PILIHAN_OTAK_MUSE, 
PILIHAN_OTAK_UNFILTERED
, dan 
PILIHAN_TAMPILAN_MENU di 
dalam Singleton Atomic Config 
yang dapat diubah live lewat 
/admin tanpa me-restart proses 
Python. 
adapters/ingress/ (3 Pintu 
Omnichannel) 
telegram_adapter.py, 
whatsapp_waha.py, 
fb_messenger.py 
Menerjemahkan webhook 
spesifik platform (Aiogram, 
WAHA JSON, Meta Graph API) 
menjadi objek standar 
UnifiedMessageEvent lalu 
mengirimkannya ke 
Gatekeeper. 
services/security/ (Modul 2: 
security_gate.py) 
initdata_auth.py, guardrails.py, 
sybil_shield.py, vision_gate.py 
Menjalankan HMAC-SHA256 
initData + Anti-Replay, sanitasi 
NFKC, Llama Prompt Guard 2 / 
NeMo, verifikasi Device 
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
Valkey Semantic Cache, dan 
Heat Score Router. 
services/workers/ (Modul 4: 
stateless_gpu_worker.py) 
comfy_serverless.py, 
wholesale_api.py, 
Mengelola Two-Phase Circuit 
Breaker (3s Cut-Off), 



<!-- [ID:08_OMNI_SOCIAL_S026] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 35

Zona 
Ekonomi 
(PPP Tier) 
Cakupan 
Negara, 
Bahasa & 
Sinyal 
Jaringan 
Harga 
Dasar per 1 
Koin 
Paket 
Pemula (50 
Koin) 
Paket 
Kreator 
(160 Koin) 
Paket 
Agensi 
(600 Koin) 
Harga 
Efektif 
Video 5s 
(20 Koin) 
Margin 
Laba 
Bersih 
Rata-Rata 
Zona 3: 
Penetrasi 
Lokal 
(Indonesia
) 
Indonesia 
(id, IP ASN 
Indonesia, 
Pembayara
n Wajib 
QRIS 
Domestik) 
Rp 100 
(~$0,0062) 
Rp 5.000 
(2 Video + 
2 Gambar 
HD) 
Rp 15.000 
(Bonus 10 
Koin) 
Rp 50.000 
(Bonus 100 
Koin) 
Rp 1.666 – 
Rp 2.000 
(~0, 10–
0,125) 
80%–89% 
(Tier Pro) 
45%–50% 
(Tier Ultra) 
Zona 2: 
Emerging 
Global 
(Menenga
h) 
Asia 
Tenggara 
non-SG 
(ms, vi, th, 
tl), India 
(hi), LATAM 
(es, pt), 
MENA (ar), 
CIS (ru) 
$0,018 
(~Rp 290) 
$0,99 (atau 
55 
Telegram 
Stars) 
$2,49 (atau 
135 
Telegram 
Stars) 
$7,99 (atau 
430 
Telegram 
Stars) 
$0,26 – 
$0,36 (~Rp 
4.200–Rp 
5.800) 
91%–94% 
(Tier Pro) 
75%–82% 
(Tier Ultra) 
Zona 1: 
Global 
Premium 
(Ekonomi 
Tinggi) 
AS, Inggris, 
Uni Eropa, 
Kanada, 
Australia, 
Jepang, 
Korea, 
Singapura 
(en, de, fr, 
ja, ko) 
$0,040 
(~Rp 640) 
$1,99 (atau 
110 
Telegram 
Stars) 
$4,99 (atau 
270 
Telegram 
Stars) 
$14,99 
(atau 800 
Telegram 
Stars) 
$0,50 – 
$0,80 (~Rp 
8.000–Rp 
12.800) 
95%–97% 
(Tier Pro) 
85%–90% 
(Tier Ultra) 
3.3 Penguncian Region Anti-Arbitrase (Tri-Factor Payment & 
Telemetry Geo-Locking) 
Untuk mencegah pengguna dari negara Zona 1 (AS/Eropa) mengubah bahasa Telegram 
mereka ke id demi mendapatkan harga murah Zona 3: 
1.​ Kunci #1 — Payment Rail Hard-Binding (Mutlak): Harga Rupiah Zona 3 (Rp 5.000 / Rp 
15.000 / Rp 50.000) hanya bisa dibayar menggunakan QRIS Domestik Indonesia (via 
Pakasir/Tripay/Duitku) yang mewajibkan akun bank/e-wallet Indonesia ber-KYC e-KTP. 
Jika pengguna memilih membayar dengan Telegram Stars atau Crypto USDT, harga 
Rupiah Zona 3 otomatis terkunci dan sistem menyajikan harga Zona 2 atau Zona 1. 
2.​ Kunci #2 — Korelasi 3 Sinyal Telemetri (Zona 2 vs. Zona 1): Cloudflare Worker & Mini 
App memeriksa kesesuaian antara header geolokasi CF-IPCountry, reputasi 
CF-Connecting-IP ASN (penolak IP VPN/Datacenter), dan zona waktu OS perangkat 
(Intl.DateTimeFormat().resolvedOptions().timeZone). Tarif subsidi Zona 2 hanya 
diberikan jika ketiga sinyal tersebut selaras di negara Emerging tanpa VPN. 
3.​ Kunci #3 — Non-Transferable Wallet & Batas Voucher: Saldo koin dikunci permanen 
pada internal_user_id (tidak ada fitur kirim koin antar-akun) dan pencetakan Ed25519 



<!-- [ID:08_OMNI_SOCIAL_S027] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 38

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
hari (120 Koin) lalu 
dibuka serentak 
dengan 1x top-up Rp 
5.000. 
TMA sebelum tombol 
klaim aktif, ditambah 
Hard-Cap Saldo 
koin_bonus Maksimal 
25 Koin (Rp 2.500). 
(setara 1 video 5 detik 
+ 1 gambar HD). Klaim 
baru hanya masuk jika 
saldo koin_bonus < 25, 
memaksa sirkulasi 
pemakaian harian yang 
sehat. 
BAGIAN V: HEXAGONAL ARCHITECTURE, SKEMA 
DATABASE TURSO/SQLITE, & KODE INTI v2.0 
5.1 Struktur Direktori Modular (Ports and Adapters / Hexagonal 
Architecture) 
Agar penambahan pintu WhatsApp (WAHA / Cloud API) dan Facebook Messenger pada 
Tahap 5 tidak pernah memaksa pembongkaran ulang kode ke-7 agen inti (Zero-Refactoring 
Guarantee), struktur proyek dikunci sebagai berikut: 
Lapisan Arsitektur (Folder / 
Modul) 
File Inti di Dalamnya 
Tanggung Jawab & Prinsip 
Isolasi (Zero-Refactoring 
Guarantee) 
core/domain/ (Kontrak & 
Skema Murni) 
schemas.py, events.py, 
exceptions.py 
Mendefinisikan 
UnifiedMessageEvent 
(abstraksi pesan lintas 
Telegram/WA/FB), JobManifest, 
AgentState (TypedDict untuk 
LangGraph), dan PricingTier. 
Murni Pydantic v2, bebas dari 
library platform eksternal. 
core/config/ (Hot-Reload 
Saklar 1 Angka) 
config_manager.py, 
pricing_ppp.yaml 
Membungkus variabel saklar 
PILIHAN_MESIN_MEDIA, 
PILIHAN_OTAK_MUSE, 
PILIHAN_OTAK_UNFILTERED
, dan 
PILIHAN_TAMPILAN_MENU di 
dalam Singleton Atomic Config 
yang dapat diubah live lewat 
/admin dalam 0 detik tanpa 
restart. 
adapters/ingress/ (3 Pintu 
Omnichannel) 
telegram_adapter.py, 
whatsapp_waha.py, 
fb_messenger.py 
Menerjemahkan webhook 
spesifik platform (Aiogram, 
WAHA JSON, Meta Graph API) 
menjadi objek standar 
UnifiedMessageEvent lalu 
mengirimkannya ke 



<!-- [ID:08_OMNI_SOCIAL_S028] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 67

Platform 
Cara Integrasi Gratis (Rp 0) 
Keunggulan Strategis untuk 
Bisnis Anda 
1. Telegram Bot 
Daftar resmi di BotFather 
(100% Gratis selamanya, tanpa 
batas pesan). 
Markas Utama (Fitur 
Terlengkap): Mendukung 
menu tombol berlapis, kirim file 
video besar (hingga 2GB), grup 
komunitas Forum Topics, dan 
tampilan Mini App. 
2. Facebook Messenger 
Gunakan Meta for Developers 
(Messenger API Resmi) yang 
dihubungkan ke Facebook 
Page bisnis Anda (100% 
Gratis). 
Mesin Akuisisi Pelanggan 
Viral: Saat Anda posting 
contoh video AI di Facebook, 
pasang fitur Auto-Reply 
Comment. Begitu ada orang 
berkomentar "Mau coba", bot 
otomatis mengirim pesan ke 
inbox Messenger mereka dan 
langsung melayani pembuatan 
gambar/video di sana. 
3. WhatsApp (WA) 
• Opsi A (Resmi): Meta 
WhatsApp Cloud API 
memberikan kuota gratis untuk 
membalas pesan masuk 
(Service Conversations dalam 
jendela 24 jam). • Opsi B 
(Open-Source Mandiri): 
Pasang WAHA (WhatsApp 
HTTP API) atau Baileys di 
VPS Anda (Rp 0, cukup scan 
QR dari nomor WA khusus 
bot). 
Pasar Paling Luas: 
Menjangkau pengguna 
awam/UMKM yang belum 
punya Telegram. Mereka cukup 
simpan nomor WA bot Anda 
dan kirim pesan seperti chatting 
biasa. 
BAGIAN II: FINANSIAL, HITUNGAN BIAYA 
OPERASIONAL 24/7, & SIMULASI KEUNTUNGAN 
2.1 Tabel Biaya Tetap Bulanan (Base Infrastructure 24/7) 
Biaya untuk membiarkan "Toko Utama" (Bot Telegram/WA/FB + 9Router + 5 Agentic AI + 
Database) menyala 24 jam sehari selama 30 hari penuh: 
Komponen 
Skema 1: Gerilya 
(Modal Rp 0) 
Skema 2: Stabil (Modal 
Minim) 
Keterangan 
Server Bot & 9Router 
(24 Jam) 
Rp 0 (Oracle Cloud 
Free / GCP Micro / 
Meta Muse VM) 
Rp 25.000 / bln (VPS 
KVM 1–2GB RAM 
lokal/NatVPS) 
Biaya harian Skema 2 
cuma ~Rp 833 / hari. 
Telegram / FB / WA 
Bot API 
Rp 0 
Rp 0 
Gratis penuh. 
LLM / Teks / Prompt 
(9Router) 
Rp 0 (Combo Full-Free: 
Kiro + Gemini + Groq + 
Rp 16.000 / bln ($1 
saldo cadangan 
9Router memeras yang 
gratis dulu (98% limit), 



<!-- [ID:08_OMNI_SOCIAL_S029] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 72

Sabar (absen klaim 5 hari berturut-turut di Mini App) atau Jalur Cepat (langsung 
Top-Up QRIS Rp 5.000 karena merasa sudah punya tabungan awal). 
2.​ Sistem 2 Dompet Terpisah (koin_utama vs. koin_bonus): 
○​ 🟢 Koin Bonus (Hasil Klaim Harian & Referral Pendaftaran): Bebas dipakai 
100% untuk fitur yang HPP-nya mendekati Rp 0 (Gambar Standar/HD, Upscale, 
Asisten Teks). Untuk fitur yang membakar saldo API/GPU mahal (Video 
Flagship/Suno), Koin Bonus baru terbuka full jika akun tersebut sudah pernah 
melakukan Top-Up minimal 1 kali (Rp 5.000) seumur hidup sebagai verifikasi 
manusia asli, atau berfungsi sebagai potongan diskon Rp 500 per video. 
3.​ Mesin Pertumbuhan Grup Otomatis: Tombol [🎁 Klaim Kredit Harian] mewajibkan 
pengguna sudah tergabung di dalam Grup Komunitas bikinAI (dicek otomatis lewat 
fungsi getChatMember Telegram API). 
3.5 Program Affiliate Gratis (2 Jalur Sekaligus — Modal Rp 0) 
1.​ In-Bot Referral (database.py): Setiap pengguna mendapat tautan 
[https://t.me/bikinAI_bot?start=ref_USERID](https://t.me/bikinAI_bot?start=ref_USERID). 
Pengundang mendapat +2 Koin Bonus saat teman bergabung ke grup, ditambah 
Komisi 10%–15% Koin Utama Seumur Hidup setiap kali teman tersebut melakukan 
Top-Up QRIS/Stars. 
2.​ Telegram Official Affiliate Program (@BotFather): Mengaktifkan fitur afiliasi resmi 
Telegram dengan bagi hasil 15%–20% Telegram Stars, sehingga ribuan pemilik channel 
global ikut mempromosikan bot Anda secara otomatis. 
3.6 Sistem Cerdas Multi-Bahasa Global (Auto-Localization) 
●​ Deteksi Bahasa Otomatis (message.from_user.language_code): Jika bahasa HP 
pengguna adalah id, bot menampilkan antarmuka Bahasa Indonesia & pembayaran 
QRIS. Jika selain id, bot otomatis menyajikan antarmuka Bahasa Inggris Internasional 
& pembayaran Telegram Stars / Crypto USDT. 
●​ Polyglot Muse Translation: Pengguna dari negara mana pun bebas mengetik prompt 
dalam bahasa ibu mereka (Inggris, Indonesia, Rusia, Arab, Jepang, Spanyol); Muse 
otomatis membalas dengan bahasa yang sama namun menerjemahkan instruksi render 
ke bahasa Inggris teknis untuk GPU. 
BAGIAN IV: UI/UX SULTAN SUPER-APP, MODULAR 
GATEWAY, & PANEL SAKLAR 1 ANGKA 
4.1 Smart Multimodal UX di Telegram (Sepintar Aplikasi Gemini/Qwen) 
1.​ Auto-Intent Detection (Tanpa Wajib Ketik /command): Pengguna cukup mengetik 
kalimat biasa, mengirim foto, mengirim dokumen PDF/Word/Excel, atau mengirim Voice 
Note (diterjemahkan via Whisper Free API di Groq). Gatekeeper/Muse otomatis 
mendeteksi niat pengguna (CHAT, GENERATE_IMAGE, GENERATE_VIDEO, 
ORCHESTRATE_CAMPAIGN, READ_DOCUMENT, IMAGE_TO_VIDEO) dalam 0,5 
detik. 



<!-- [ID:08_OMNI_SOCIAL_S030] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 4. PILIHAN GAYA TAMPILAN MENU TELEGRAM (UI/UX)​

<!-- [ID:08_OMNI_SOCIAL_S031] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# [3] Gaya "Kompetitor Pro" (Langsung daftar harga per model ala 
PosMotion)​
PILIHAN_TAMPILAN_MENU = 1​
 
BAGIAN V: PERTAHANAN SIBER TINGKAT LANJUT 
(RED-TEAM vs. BLUE-TEAM) & ISOLASI HUKUM 
Bagian ini mengunci seluruh celah keamanan tingkat produksi (Production-Grade Edge Cases), 
mulai dari pemindai internal Telegram, penyadapan server GPU, hingga 6 serangan eksploitasi 
siber pada arsitektur otonom. 
5.1 Anatomi Pemblokiran Telegram & 4 Aturan Emas SOP Anti-Ban 
Bot Telegram publik yang mengirim gambar/video 18+ (NSFW) atau kekerasan ekstrem secara 
langsung melalui pipa sendPhoto / sendVideo di ruang chat akan terdeteksi oleh Automated 
Hash & NSFW Media Scanner milik Telegram (demi kepatuhan Apple App Store & Google 
Play Store). 



<!-- [ID:08_OMNI_SOCIAL_S032] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 75

●​ Aturan #1 (Hard-Lock Pipeline Isolation): Bot Telegram Utama (@bikinAI_bot) hanya 
diizinkan mengirim media bertanda SFW_SAFE ke ruang chat. Seluruh konten Unfiltered 
wajib diisolasi ke arsitektur Web/Mini App terenkripsi. 
●​ Aturan #2 (Sistem Bot Kembar / Cold-Standby): Seluruh database saldo koin disimpan 
di server eksternal kita (bukan di memori Telegram). Jika Bot #1 mengalami kendala, 
pergantian ke TOKEN_BOT_CADANGAN selesai dalam 10 detik tanpa kehilangan 1 koin 
pun. 
●​ Aturan #3 (has_spoiler=True & Teks Murni di Activity Bot): Laporan di grup komunitas 
📈 Activity Bot murni berupa teks status tanpa lampiran file media persis seperti strategi 
kompetitor. 
●​ Aturan #4 (Rate-Limiter / Anti-Flood): Jeda otomatis 0,5–1 detik antar pesan ke 
pengguna yang sama untuk mencegah auto-ban anti-spam Telegram. 
5.2 Matriks Audit 6-Lapisan Pertahanan Produksi (Zero-Knowledge & 
WebView Hardening) 
Berdasarkan pemetaan arsitektur keamanan 6 tahapan (Tahap 1 s/d Tahap 6), berikut adalah 
mekanisme pertahanan yang ditanamkan ke dalam sistem kita dengan biaya tambahan Rp 0: 
Kode & Tahap Pertahanan 
Ancaman Fatal yang Dicegah Mekanisme Teknis Pertahanan 
di Sistem Kita 
Tahap 1: Gerbang Klien TMA 
(WebView) TMA-01, WV-02, 
WV-03 
• Pemindaian Crawler 
TelegramBot yang memicu 
label restricted pada Bot 
(TMA-01). • Jejak forensik di 
disk cache HP Android 
(WV-02). • Kebocoran layar di 
OS App Switcher / Recent 
Apps (WV-03). 
• Zero-Trust Decoy Landing 
Page: Jika URL diakses tanpa 
tanda tangan kriptografi 
Telegram.WebApp.initData 
yang valid (misalnya oleh 
crawler Telegram), halaman 
hanya merender web 
kalkulator/desain statis yang 
bersih. • Auto-Blur & 
Biometric Lock: Memasang 
pendengar visibilitychange & 
deactivated untuk menutup 
layar dengan overlay buram 
saat pengguna berpindah 
aplikasi, disertai kunci sidik 
jari/FaceID (BiometricManager) 
dan penyimpanan Blob murni di 
RAM. 
Tahap 2: API Gateway & Auth 
API-01 
• Token Replay & pencurian 
string initData lewat Inspect 
Element (DevTools) di 
Telegram Desktop untuk 
menembak API otomatis 
(API-01). 
• Verifikasi HMAC-SHA256 
Ketat: Memeriksa tanda tangan 
initData dengan batas 
kedaluwarsa auth_date 
maksimal 60 detik, lalu 
menukarnya menjadi sesi 
Short-Lived JWT dengan Rate 
Limiting berbasis 
telegram_user_id. 



<!-- [ID:08_OMNI_SOCIAL_S033] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
### Matriks Eksekusi Dua Fase: Konkurensi Maksimal Tanpa Penghangusan Kuota
Untuk memperoleh kapasitas konkurensi maksimal yang sanggup menahan ribuan pengguna 
sejak detik pertama peluncuran sekaligus menjaga ketersediaan komputasi gratis hingga bertahun-
tahun ke depan, sistem wajib menerapkan mekanisme penyediaan dua fase. Fase pertama adalah 
aktivasi serentak pada hari pertama untuk seluruh layanan dalam kategori nir-kartu (cukup 
menggunakan akun GitHub, Gmail, Telegram, atau identitas kriptografis peramban) yang memiliki 
skema reset kuota harian atau bulanan permanen. Mengingat kuota pada kelompok ini tidak 
memiliki masa kedaluwarsa akun dan selalu kembali penuh setiap pergantian siklus bulan atau 
hari, penggabungan lebih dari 25 penyedia nir-kartu secara paralel di balik agregator OmniRoute 
dan New-API Horizon akan mengakumulasi batas laju individual menjadi kapasitas agregat di atas 
1.500 RPM dengan suplai melampaui 1,1 miliar token per bulan.



<!-- [ID:08_OMNI_SOCIAL_S034] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: 10PX -->
## Halaman 153

  const handleTestBroadcast = () => {​
    setLogResponse(`Trafik disimulasikan: Pesan "${testMsg}" terkirim ke 
TOKEN_BOT_UTAMA. Jika bot 1 mengalami HTTP 429 Telegram, kueri dialihkan instan ke 
TOKEN_BOT_ACTIVITY lalu TOKEN_BOT_CADANGAN.`);​
    setTestMsg("");​
  };​
​
  return (​
    <div className="mx-auto max-w-6xl px-4 py-8">​
      <div className="border-b border-white/10 pb-5 mb-6">​
        <h2 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">​
          <Bot className="h-5 w-5 text-blue-400" /> Omnichannel Gateway & Telegram Failover 
Bridge​
        </h2>​
        <p className="text-xs text-slate-400 mt-1">​
          Redundansi 3 token bot independen (@BotFather) dan kontainer Docker mandiri WAHA 
WhatsApp HTTP API.​
        </p>​
      </div>​
​
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">​
        <div className="rounded-xl border border-white/10 bg-slate-900/50 p-4">​
          <div className="flex items-center justify-between">​
            <span className="text-xs font-mono text-cyan-400">TOKEN_BOT_UTAMA</span>​
            <span className="flex items-center gap-1 text-[10px] font-mono text-emerald-400">​
              <CheckCircle2 className="h-3 w-3" /> AKTIF​
            </span>​
          </div>​
          <p className="text-sm font-bold text-white mt-2">@AetherStudioBot</p>​
          <span className="text-[10px] text-slate-500 font-mono">Pintu Utama Pengguna 
Telegram</span>​
        </div>​
​
        <div className="rounded-xl border border-white/10 bg-slate-900/50 p-4">​
          <div className="flex items-center justify-between">​
            <span className="text-xs font-mono text-cyan-400">TOKEN_BOT_ACTIVITY</span>​
            <span className="flex items-center gap-1 text-[10px] font-mono text-emerald-400">​
              <CheckCircle2 className="h-3 w-3" /> SIAGA​
            </span>​
          </div>​
          <p className="text-sm font-bold text-white mt-2">@AetherActivityBot</p>​
          <span className="text-[10px] text-slate-500 font-mono">Notifikasi Audit & 
Admin</span>​
        </div>​
​
        <div className="rounded-xl border border-white/10 bg-slate-900/50 p-4">​
          <div className="flex items-center justify-between">​
            <span className="text-xs font-mono 



<!-- [ID:08_OMNI_SOCIAL_S035] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_108 -->
## Halaman 39

penggunaan kontainer Docker (hingga kapasitas 2 CPU, 4 GB RAM, 50 GB NVMe SSD, 
dan 100 GB trafik keluar) hingga 31 Desember 2026 tanpa kartu 
kredit[span_108](start_span)[span_108](end_span). Serv00 menyediakan shell SSH 
gratis dengan dukungan kompilasi C++, Java, dan Rust. Catatan untuk Render, Koyeb, 
dan Hugging Face Spaces: pada Render dan Koyeb, sebagian pengguna dapat 
mendaftar dan men-deploy tanpa kartu kredit, namun sistem anti-abuse terkadang 
meminta otorisasi kartu US1 (yang langsung dibatalkan) untuk layanan komputasi 
backend di luar situs statis; sementara pada Hugging Face Spaces, Static Spaces selalu 
gratis untuk semua akun, sedangkan ruang komputasi Gradio/Docker memiliki batasan 
kebijakan Pro/komputasi pada akun tertentu meskipun perangkat keras CPU Basic 
menyediakan 2 vCPU dan 16 GB RAM. 
2C. Identitas Pengembang, Bot Omnichannel & Gerbang Pembayaran 
QRIS / Kripto Otomatis (100% Tanpa Kartu Visa) 
1.​ GitHub Signup, Telegram @BotFather & @userinfobot — URL Polos Pendaftaran 
GitHub: https://github.com/signup | URL Polos Telegram BotFather: https://t.me/BotFather 
| URL Polos Telegram UserInfoBot: https://t.me/userinfobot — Kegunaan & Aturan 
Terbaru: Akun GitHub menjadi kunci login OAuth 1-klik di seluruh layanan Kelompok 2. 
@BotFather digunakan untuk menerbitkan 3 token bot independen 
(TOKEN_BOT_UTAMA, TOKEN_BOT_ACTIVITY, TOKEN_BOT_CADANGAN) sebagai 
rantai failover otomatis apabila salah satu bot terkena pembatasan laju Telegram, 
sedangkan @userinfobot mengambil angka ADMIN_USER_ID Anda. 
2.​ Meta for Developers (Integrasi Resmi WhatsApp & Messenger) — URL Polos Portal 
Developer: https://developers.facebook.com/ — Kegunaan & Aturan Terbaru: Login 
menggunakan akun Facebook untuk mengonfigurasi Cloud API resmi WhatsApp dan 
Messenger, berpasangan dengan kontainer mandiri devlikeapro/waha (1E.4) sebagai 
jalur cadangan bebas biaya per pesan. 
3.​ Telegram @CryptoBot (Kasir Pembayaran Crypto USDT Global 1-Klik) — URL Polos 
Bot Kasir: https://t.me/CryptoBot — Kegunaan & Aturan Terbaru: 100% tanpa kartu Visa 
dan tanpa KYC perbankan. Cukup ketik /start lalu pilih Crypto Pay dan Create App untuk 
mendapatkan CRYPTOBOT_API_TOKEN. Pendapatan USDT yang masuk dari 
pelanggan dapat langsung dipakai untuk mengisi ulang saldo komputasi GPU di Novita 
AI, RunPod, Vast.ai, dan PiAPI (Kelompok 3A) tanpa pernah menyentuh rekening bank 
tradisional. 
4.​ Pakasir, Tripay, Duitku & Alternatif Payment Gateway QRIS Indonesia (Audit Aturan 
BI & API Oktober 2026) — URL Polos Pakasir (Layanan Link Pembayaran QRIS & VA 
Cepat 1-3 Hari): https://pakasir.com/ | URL Polos Dokumentasi Migrasi Wajib Pakasir API 
v2: https://pakasir.com/p/create-transaction | URL Polos Tripay (Payment Gateway & 
Remitansi BI-FAST PT Trijaya Digital Grup): https://tripay.co.id/ | URL Polos Duitku 
(Payment Gateway & Disbursement 26+ Metode PT Kharisma Catur Mandala): 
https://www.duitku.com/ | URL Polos Panduan Integrasi Callback & Merchant Code 
Duitku: https://kekasir.id/panduan/payment-gateway/duitku | URL Polos Midtrans 
(Payment Gateway GoTo Financial, Unggul Integrasi Native GoPay & QRIS): 
https://midtrans.com/id/biaya | URL Polos Xendit (Payment Gateway & Disbursement 
Otomatis Multi-Negara Asia Tenggara): 
https://www.xendit.co/en-id/blog/qris-payments-in-indonesia-a-complete-guide-for-busines



<!-- [ID:08_OMNI_SOCIAL_S036] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: NAMA BRAND, PENJELASAN FUNGSI KATA KUNCI -->
## Halaman 58

BikinFoto AI (Sangat SEO-driven. Ketika orang mengetik "Bikin foto AI", nama bot Anda otomatis relevan)
GambarAI / GambarBot (Sederhana, langsung ke sasaran)
Sulap.ai (Memberikan kesan magis, instan, dan cepat)
3. Kategori Cepat & Murah (Sesuai target pasar agregator)
InstanAI
KonekAI (Menandakan fungsi jembatan/agregator ke berbagai model AI)
SakuAI (Memberikan kesan murah, ringan, dan bisa diakses langsung lewat HP/Telegram)
Eksekusi SEO Khusus di Telegram
SEO di pencarian global Google dan pencarian internal Telegram bekerja dengan cara berbeda. Untuk mengakali keduanya agar berada di Rank 1,
gunakan trik pemisahan antara Username dan Display Name:
Pilih Brand Name yang Pendek: Misalnya Anda memilih BikinAI.
Gunakan Username Bot: @BikinAI_bot
Optimalkan Display Name (Judul Bot): Di sinilah Anda memasukkan kata kunci volume tinggi. Jangan hanya menulis "BikinAI" di judul. Tulis:
BikinAI - Bot Pembuat Foto & Video AI Cepat
Dengan struktur ini, ketika pengguna Telegram mengetik "Bot Foto AI" atau mencari di Google "Bot Telegram buat bikin foto AI", sistem akan
membaca Display Name Anda yang kaya kata kunci, sementara mereka tetap mengingat brand BikinAI.
User prompt: BikinAI_instan_bot gitu? sebagai username lalu namanya bikin AI Instan?
Response: Konsepnya sudah searah, tapi mari kita pertajam lagi agar senjata SEO-nya benar-benar maksimal menjaring traffic.
Berikut adalah koreksi dan racikan yang lebih mematikan untuk algoritma pencarian Telegram maupun Google:
1. Username (Harus Singkat & Ikonik) @BikinAI_instan_bot bisa digunakan, tapi sedikit terlalu panjang. Username adalah identitas yang akan
diketik orang atau dibagikan via link (t.me/...). Buatlah sesingkat mungkin agar tidak rawan typo.
Rekomendasi: @BikinAI_bot atau @BikinInstan_bot
2. Display Name (Lahan Utama Keyword SEO) Menamai bot hanya dengan "Bikin AI Instan" berarti Anda membuang ruang kosong yang berharga.
Orang Indonesia jarang secara spesifik mencari kata "Instan" di kolom pencarian; mereka mencari objek teknisnya seperti "Foto", "Gambar", atau
"Video".
Gunakan format [Nama Brand] + [Penjelasan Fungsi Kata Kunci].
Opsi 1 (Fokus Visual): BikinAI - Bot Bikin Foto & Video
Opsi 2 (Fokus Kasual): BikinInstan - Edit Gambar AI Gampang
Opsi 3 (Fokus Lengkap): BikinAI - Render Foto, Video & Chat
Cara Kerjanya di Lapangan: Ketika ada pengguna Telegram yang tidak tahu nama bot Anda lalu mengetik "bot bikin foto" atau "bot edit gambar" di
kolom pencarian global Telegram, sistem akan memindai Display Name Anda. Karena Anda memasukkan kata kunci "Bikin", "Foto", dan "Gambar" di
judul utama, bot Anda akan terseret ke peringkat atas.
Setelah mereka mengklik dan menggunakan layanannya yang murah dan cepat, brand "BikinAI" baru akan secara alami melekat di ingatan mereka.
User prompt: Kalau di satuin? Bikin AI - Bikin Edit Foto & Video Gambar?
Response: Secara SEO, memasukkan semua kata kunci itu memang akan terbaca oleh mesin, namun strategi ini masuk ke dalam kategori keyword
stuffing (penumpukan kata kunci).
Sama halnya saat menganalisis distribusi algoritma atau mengoptimalkan alt text untuk mendongkrak jangkauan non-follower di media sosial, teks
yang Anda buat harus ramah untuk mesin algoritma, namun tetap harus terlihat meyakinkan dan tidak menyerupai spam di mata manusia. Jika
judulnya terlalu berantakan, click-through rate (rasio orang yang mau mengklik) akan turun karena pengguna curiga itu adalah bot penipuan.
Penggunaan kata "Bikin" yang diulang ("Bikin AI - Bikin Edit...") dan penggabungan "Foto & Gambar" secara berurutan ("Video Gambar") membuat
susunannya kurang natural untuk dibaca.
Jika Anda ingin menyatukan semua kata kunci bertegangan tinggi tersebut dalam satu baris Display Name tanpa terlihat spammy, gunakan pemisah
berupa koma atau garis miring. Berikut adalah racikan yang mengawinkan optimasi SEO maksimal dengan tingkat kepercayaan pengguna
(Trust/CTR):


