
<!-- [ID:08_OMNI_SOCIAL_S086] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 674

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



<!-- [ID:08_OMNI_SOCIAL_S087] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Bot
- grammY (Telegram)
- Baileys / WA Cloud API (WhatsApp)
- Meta Graph API (IG, Threads)


<!-- [ID:08_OMNI_SOCIAL_S088] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==== Bot ====
TELEGRAM_BOT_TOKEN=
TELEGRAM_OWNER_ID=
WHATSAPP_TOKEN=
WHATSAPP_OWNER_NUMBER=
INSTAGRAM_TOKEN=
THREADS_TOKEN=


<!-- [ID:08_OMNI_SOCIAL_S089] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# bots/core/__init__.py
__version__ = "0.1.0"

"""
Verifikasi perintah owner dari channel mana pun.
Aturan: owner match + PIN (untuk perintah sensitif) + HMAC + timestamp window.
"""
import os, hmac, hashlib, time
from typing import Literal

Channel = Literal["telegram", "whatsapp", "instagram", "threads", "github_issue"]

OWNER_PIN = os.environ.get("OWNER_PIN", "")
HMAC_SECRET = os.environ.get("HMAC_SECRET", "").encode()
WINDOW_SEC = int(os.environ.get("AUTH_WINDOW_SEC", "60"))


<!-- [ID:08_OMNI_SOCIAL_S090] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# test kill switch:
curl -X POST localhost:8000/command -H "X-Internal-Key: $KEY" \
  -d 'text=/panic 123456&channel=telegram&user_id=<owner_id>'

<!-- [ID:08_OMNI_SOCIAL_S091] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Env (ringkas)
- WA: `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_ID`, `WHATSAPP_VERIFY_TOKEN`, `WHATSAPP_APP_SECRET`
- IG: `INSTAGRAM_TOKEN`, `INSTAGRAM_PAGE_ID`, `INSTAGRAM_APP_SECRET`
- Threads: `THREADS_TOKEN`, `THREADS_USER_ID`, `THREADS_APP_SECRET`
- Owner IDs: `WHATSAPP_OWNER_NUMBER`, `INSTAGRAM_OWNER_ID`, `THREADS_OWNER_ID`


<!-- [ID:08_OMNI_SOCIAL_S092] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
#    Telegram WebApp initData Validator, & Owner Bootstrap Token Protection

<!-- [ID:08_OMNI_SOCIAL_S093] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# - Entrypoint Asinkron Terpadu (main() Bot Telegram + Dual Web Server Port 8080)
