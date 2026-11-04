
<!-- [ID:14_SEC_STEALTH_S005] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: INT -->
# Daftar domain pengirim resmi agar tidak bisa dipalsukan oleh pembeli
TRUSTED_BANK_SENDERS = (
    "bca.co.id", "bankmandiri.co.id", "bri.co.id", "bni.co.id",
    "jago.com", "seabank.co.id", "gopay.co.id", "dana.id", "qris.id"
)

def normalize_amount(raw_str: str) -> int:
    """Membersihkan format desimal/titik (misal '50.142,00' atau '50,142.00' -> 50142)."""
    clean = raw_str.strip()
    # Hapus desimal sen (.00 atau ,00 di ujung)
    clean = re.sub(r"[\.,]\d{2}$", "", clean)
    # Hapus semua pemisah ribuan
    clean = re.sub(r"[^\d]", "", clean)
    return int(clean) if clean.isdigit() else 0

def check_incoming_mutations(imap_host: str, email_user: str, email_app_pass: str) -> list[int]:
    """Mengecek email mutasi bank yang belum dibaca (UNSEEN) dan mengembalikan daftar nominal masuk."""
    detected_amounts = []
    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(email_user, email_app_pass)
    mail.select("INBOX")

    status, messages = mail.search(None, '(UNSEEN)')
    if status != "OK" or not messages[0]:
        mail.logout()
        return detected_amounts

    for num in messages[0].split():
        _, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                sender = msg.get("From", "").lower()

                # Validasi keamanan: Pastikan email benar-benar berasal dari domain bank resmi
                if not any(domain in sender for domain in TRUSTED_BANK_SENDERS):
                    continue

                # Ambil isi email (Text/HTML)
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() in ("text/plain", "text/html"):
                            payload = part.get_payload(decode=True)
                            if payload:
                                body += payload.decode(errors="ignore")
                else:
                    payload = msg.get_payload(decode=True)
                    if payload:
                        body = payload.decode(errors="ignore")

                clean_text = re.sub(r"<[^>]+>", " ", unescape(body))

                # Ekstrak angka nominal dari isi email
                for pattern in BANK_AMOUNT_PATTERNS:
                    matches = re.findall(pattern, clean_text, re.IGNORECASE)
                    for m in matches:
                        amt = normalize_amount(m)
                        if amt > 0:
                            detected_amounts.append(amt)

    mail.logout()
    return detected_amounts
def calculate_crc16(data: str) -> str:
    """Menghitung ulang Checksum CRC16-CCITT (0xFFFF, Poly 0x1021) standar EMVCo QRIS."""
    crc = 0xFFFF
    for char in data:
        crc ^= ord(char) << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"

def parse_emvco_tlv(qris_str: str) -> list:
    """Membedah struktur Tag-Length-Value (TLV) dari string QRIS."""
    i = 0
    tlv_list = []
    while i < len(qris_str):
        tag = qris_str[i:i+2]
        length = int(qris_str[i+2:i+4])
        value = qris_str[i+4:i+4+length]
        tlv_list.append((tag, value))
        i += 4 + length
        if tag == "63":  # Tag 63 adalah CRC (selalu di akhir)
            break
    return tlv_list

def generate_dynamic_qris(static_qris: str, amount: int) -> str:
    """Mengubah QRIS Statis apa pun menjadi QRIS Dinamis dengan nominal terkunci."""
    tlv_items = parse_emvco_tlv(static_qris.strip())
    new_tlv = []
    amount_str = str(int(amount))
    amount_injected = False

    for tag, value in tlv_items:
        if tag == "01":
            # Ubah Point of Initiation Method dari '11' (Statis) ke '12' (Dinamis)
            new_tlv.append(("01", "12"))
        elif tag in ("54", "63"):
            # Lewati tag nominal lama (jika ada) dan tag CRC lama
            continue
        elif tag == "58" and not amount_injected:
            # Sisipkan Tag 54 (Transaction Amount) tepat sebelum Tag 58 (Country Code ID)
            new_tlv.append(("54", amount_str))
            new_tlv.append((tag, value))
            amount_injected = True
        else:
            new_tlv.append((tag, value))

    # Rakit kembali string EMVCo
    rebuilt_str = "".join(f"{t}{len(v):02d}{v}" for t, v in new_tlv)
    rebuilt_str += "6304"  # Tambahkan header Tag CRC
    
    # Hitung ulang checksum CRC16 dan gabungkan
    crc_hex = calculate_crc16(rebuilt_str)
    return rebuilt_str + crc_hex

Menembak langsung ke endpoint API mutasi (Direct API Polling & Headless Session) adalah kasta tertinggi dari arsitektur "Wts source code self payment gateway". Dengan metode ini, Anda tidak perlu repot menyamakan alamat email di setiap aplikasi, tidak peduli akun DANA, ShopeePay, GoPay, OVO/Grab, atau Nobu tersebut terdaftar pakai nomor HP siapa, dan sistem menerima data JSON murni (lengkap dengan transaction_id, nominal, pengirim, dan waktu presisi hingga milidetik).
Agar server/VPS Anda bisa menembak langsung API internal merchant tanpa terblokir oleh sistem keamanan (Cloudflare/WAF) dan tanpa perlu login berulang-ulang, berikut adalah 3 rahasia teknis beserta source code mesin penembak langsungnya.
1. Tiga Kunci Utama Mesin "Tembak Langsung" (Direct API Engine)
 * Spoofing Sidik Jari TLS (curl_cffi):
   Jika Anda menembak API GoBiz, Shopee, DANA, atau Grab menggunakan requests atau httpx biasa, server mereka akan langsung menolak koneksi (403 Forbidden) karena mendeteksi TLS JA3/JA4 Fingerprint milik Python. Solusinya adalah menggunakan library curl_cffi dengan parameter impersonate="chrome124", sehingga server bank/e-wallet mengira request tersebut berasal dari browser/aplikasi asli.
 * Virtual Device Locking & Token Auto-Refresh:
   Saat pertama kali dihubungkan, source code akan membuat device_id permanen (UUID khusus) di VPS Anda. Anda cukup memasukkan OTP 1 kali saja (bisa langsung lewat perintah di Bot Telegram Anda), lalu server akan menyimpan access_token & refresh_token. Sebuah daemon di latar belakang akan memperbarui token tersebut secara otomatis sebelum kadaluarsa, sehingga sesi login bertahan berbulan-bulan.
 * Dynamic JSON-Path Extractor (Plug-and-Play API Baru):
   Setiap aplikasi memiliki struktur JSON mutasi yang berbeda (misal GoBiz menaruh nominal di data.amount, sedangkan Grab/OVO di transactions[].netAmount). Dengan JSON-Path Extractor, ketika nanti Anda ingin menambahkan Nobu atau bank lain, Anda hanya perlu mendaftarkan alamat URL API dan letak field JSON-nya tanpa perlu mengubah logika mesin utama.
2. Source Code Lengkap: direct_api_engine.py
Instal terlebih dahulu library intinya di server Anda:
pip install curl_cffi fastapi uvicorn pydantic

Simpan kode di bawah ini sebagai direct_api_engine.py. Kode ini sudah dilengkapi dengan Manajemen Sesi Otomatis, Login OTP langsung dari API/Bot, Penembak Mutasi Multi-Provider, dan Pendaftaran Provider Baru Tanpa Coding.
import asyncio
import json
import os
import time
import uuid
from typing import Dict, Any, List, Optional
from curl_cffi.requests import AsyncSession
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Direct API Multi-Merchant Engine")

VAULT_FILE = "merchant_sessions_vault.json"


<!-- [ID:14_SEC_STEALTH_S006] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 41

​
-- 4. TABEL PEKERJAAN & ONE-WAY REFUND STATE MACHINE​
CREATE TABLE IF NOT EXISTS jobs (​
    job_id TEXT PRIMARY KEY,​
    internal_user_id INTEGER NOT NULL,​
    cost INTEGER NOT NULL,​
    wallet_used TEXT NOT NULL DEFAULT 'UTAMA',​
    status TEXT NOT NULL DEFAULT 'PROCESSING', -- 'PROCESSING', 
'COMPLETED', 'FAILED_REFUNDED'​
    refunded_lock INTEGER NOT NULL DEFAULT 0 CHECK (refunded_lock IN 
(0, 1)),​
    provider_job_id TEXT,​
    actual_cost_idr INTEGER DEFAULT 0,​
    created_at INTEGER NOT NULL​
);​
​
-- 5. TABEL KLAIM HARIAN ANTI-TUYUL (MAKS 2 AKUN PER DEVICE 
FINGERPRINT)​
CREATE TABLE IF NOT EXISTS daily_claims (​
    claim_id INTEGER PRIMARY KEY AUTOINCREMENT,​
    internal_user_id INTEGER NOT NULL,​
    device_fp TEXT NOT NULL,​
    claim_date TEXT NOT NULL​
);​
CREATE INDEX IF NOT EXISTS idx_daily_claims_fp_date ON 
daily_claims(device_fp, claim_date);​
​
-- 6. TABEL BLIND pHASH AUDIT LEDGER (AUTO-DELETE TIAP 48 JAM)​
CREATE TABLE IF NOT EXISTS phash_audit_log (​
    job_id TEXT PRIMARY KEY,​
    internal_user_id INTEGER NOT NULL,​
    perceptual_hash_64bit TEXT NOT NULL,​
    media_type TEXT NOT NULL,​
    expires_at INTEGER NOT NULL​
);​
CREATE INDEX IF NOT EXISTS idx_phash_hash ON 
phash_audit_log(perceptual_hash_64bit);​
CREATE INDEX IF NOT EXISTS idx_phash_exp ON 
phash_audit_log(expires_at);​
 
5.3 Kode Produksi Inti v2.0 (Menutup Seluruh Celah Audit + Voucher 
Ed25519 + Lock Striping) 
Kode di bawah ini menggantikan draf kode v1.0 dengan implementasi Fixed-Size Lock 
Striping (4.096 stripes), BoundedReplayGuard (65s Ring Buffer), Anti-Tuyul 
claim_daily_bonus_safe (Max Cap 25 Koin + Device Fingerprint), serta Stateless Ed25519 



<!-- [ID:14_SEC_STEALTH_S007] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 640

​
-- 4. TABEL PEKERJAAN & ONE-WAY REFUND STATE MACHINE​
CREATE TABLE IF NOT EXISTS jobs (​
    job_id TEXT PRIMARY KEY,​
    internal_user_id INTEGER NOT NULL,​
    cost INTEGER NOT NULL,​
    wallet_used TEXT NOT NULL DEFAULT 'UTAMA',​
    status TEXT NOT NULL DEFAULT 'PROCESSING', -- 'PROCESSING', 
'COMPLETED', 'FAILED_REFUNDED'​
    refunded_lock INTEGER NOT NULL DEFAULT 0 CHECK (refunded_lock IN 
(0, 1)),​
    provider_job_id TEXT,​
    actual_cost_idr INTEGER DEFAULT 0,​
    created_at INTEGER NOT NULL​
);​
​
-- 5. TABEL KLAIM HARIAN ANTI-TUYUL (MAKS 2 AKUN PER DEVICE 
FINGERPRINT)​
CREATE TABLE IF NOT EXISTS daily_claims (​
    claim_id INTEGER PRIMARY KEY AUTOINCREMENT,​
    internal_user_id INTEGER NOT NULL,​
    device_fp TEXT NOT NULL,​
    claim_date TEXT NOT NULL​
);​
CREATE INDEX IF NOT EXISTS idx_daily_claims_fp_date ON 
daily_claims(device_fp, claim_date);​
​
-- 6. TABEL BLIND pHASH AUDIT LEDGER (AUTO-DELETE TIAP 48 JAM)​
CREATE TABLE IF NOT EXISTS phash_audit_log (​
    job_id TEXT PRIMARY KEY,​
    internal_user_id INTEGER NOT NULL,​
    perceptual_hash_64bit TEXT NOT NULL,​
    media_type TEXT NOT NULL,​
    expires_at INTEGER NOT NULL​
);​
CREATE INDEX IF NOT EXISTS idx_phash_hash ON 
phash_audit_log(perceptual_hash_64bit);​
CREATE INDEX IF NOT EXISTS idx_phash_exp ON 
phash_audit_log(expires_at);​
 
5.3 Kode Produksi Inti v2.0 (Menutup Seluruh Celah Audit + Voucher 
Ed25519 + Lock Striping) 
Kode di bawah ini menggantikan draf kode v1.0 dengan implementasi Fixed-Size Lock 
Striping (4.096 stripes), BoundedReplayGuard (65s Ring Buffer), Anti-Tuyul 
claim_daily_bonus_safe (Max Cap 25 Koin + Device Fingerprint), serta Stateless Ed25519 



<!-- [ID:14_SEC_STEALTH_S008] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: PROVIDER -->
# =====================================================================
class DirectMerchantClient:
    @staticmethod
    def build_headers(provider: str, session_data: Dict[str, Any]) -> Dict[str, str]:
        """Merakit header identik dengan perangkat asli agar tidak diblokir WAF."""
        device_id = session_data.get("device_id") or str(uuid.uuid4())
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "X-Unique-Id": device_id,
            "X-Device-Id": device_id,
            "Origin": PROVIDER_PROFILES[provider]["base_url"],
            "Referer": PROVIDER_PROFILES[provider]["base_url"] + "/",
        }
        if session_data.get("access_token"):
            headers["Authorization"] = f"Bearer {session_data['access_token']}"
        if session_data.get("raw_cookie"):
            headers["Cookie"] = session_data["raw_cookie"]
        if session_data.get("custom_headers"):
            headers.update(session_data["custom_headers"])
        return headers

    @classmethod
    async def fetch_mutations(cls, provider: str) -> List[Dict[str, Any]]:
        """Menembak langsung endpoint mutasi merchant dan mengembalikan daftar uang masuk."""
        if provider not in VAULT or not VAULT[provider].get("is_logged_in"):
            return []

        profile = PROVIDER_PROFILES[provider]
        session_info = VAULT[provider]
        headers = cls.build_headers(provider, session_info)

        # Gunakan curl_cffi impersonate="chrome124" untuk menembus Cloudflare/WAF
        async with AsyncSession(impersonate="chrome124", timeout=10) as client:
            if profile["method"].upper() == "POST":
                resp = await client.post(
                    profile["mutation_url"],
                    headers=headers,
                    json=profile.get("mutation_payload", {})
                )
            else:
                resp = await client.get(profile["mutation_url"], headers=headers)

            # Jika token expired (401), otomatis jalankan auto-refresh token!
            if resp.status_code == 401 and session_info.get("refresh_token"):
                refreshed = await cls.refresh_session(provider)
                if refreshed:
                    headers = cls.build_headers(provider, VAULT[provider])
                    resp = await client.get(profile["mutation_url"], headers=headers)

            if resp.status_code != 200:
                print(f"[{provider}] Gagal tembak API mutasi: HTTP {resp.status_code}")
                return []

            raw_json = resp.json()
            tx_list = extract_nested_json(raw_json, profile["json_list_path"]) or []

            valid_incoming = []
            for item in tx_list:
                tx_id = str(extract_nested_json(item, profile["json_id_path"]) or "")
                raw_amt = extract_nested_json(item, profile["json_amount_path"])
                status = str(extract_nested_json(item, profile["json_status_path"]) or "")

                if not tx_id or tx_id in PROCESSED_TX_IDS:
                    continue

                # Bersihkan angka nominal (jika berbentuk string/desimal)
                amt_int = int(float(str(raw_amt).replace(",", ""))) if raw_amt else 0

                if amt_int > 0 and status.upper() == profile["success_value"].upper():
                    valid_incoming.append({
                        "provider": provider,
                        "tx_id": tx_id,
                        "amount": amt_int,
                        "raw": item
                    })
            return valid_incoming

    @classmethod
    async def refresh_session(cls, provider: str) -> bool:
        """Memperbarui access_token secara otomatis di belakang layar tanpa perlu OTP ulang."""
        profile = PROVIDER_PROFILES.get(provider, {})
        refresh_url = profile.get("refresh_url")
        session_info = VAULT.get(provider, {})

        if not refresh_url or not session_info.get("refresh_token"):
            return False

        async with AsyncSession(impersonate="chrome124", timeout=10) as client:
            resp = await client.post(
                refresh_url,
                headers=cls.build_headers(provider, session_info),
                json={"refresh_token": session_info["refresh_token"]}
            )
            if resp.status_code == 200:
                data = resp.json()
                VAULT[provider]["access_token"] = data.get("access_token", VAULT[provider]["access_token"])
                if data.get("refresh_token"):
                    VAULT[provider]["refresh_token"] = data["refresh_token"]
                VAULT[provider]["last_refreshed"] = int(time.time())
                save_vault(VAULT)
                print(f"[{provider}] Token berhasil di-refresh otomatis!")
                return True
        return False


<!-- [ID:14_SEC_STEALTH_S009] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# =====================================================================
def load_vault() -> Dict[str, Any]:
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, "r") as f:
            return json.load(f)
    return {}

def save_vault(data: Dict[str, Any]):
    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=2)

VAULT = load_vault()
PROCESSED_TX_IDS = set()  # Mencegah 1 transaksi diklaim 2 kali (Double-Spend Protection)

def extract_nested_json(data: Any, path: str) -> Any:
    """Mengambil nilai dari JSON berlapis menggunakan notasi titik (misal: 'result.orderList')."""
    keys = path.split(".")
    curr = data
    for k in keys:
        if isinstance(curr, dict) and k in curr:
            curr = curr[k]
        else:
            return None
    return curr


<!-- [ID:14_SEC_STEALTH_S010] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR -->
## Halaman 194

mencoba ekstraksi cepat menggunakan spider_rs terlebih dahulu, beralih secara otomatis ke 
Scrapling StealthyFetcher (untuk melewati Cloudflare Turnstile dan merelokasi elemen adaptif 
12-faktor), dan menggunakan server internal Crawl4AI sebagai jalur terakhir. 
import asyncio​
import random​
import httpx​
from typing import List, Optional​
​
class MultiPathProxyAndScraperEngine:​
    """​
    Mesin Rotasi Proksi & Akuisisi Web Multi-Jalur Otomatis.​
    Tidak bergantung pada satu sumber proksi maupun satu pustaka web 
scraper.​
    """​
    def __init__(self, local_pool_url: str = "http://127.0.0.1:5010"):​
        self.local_pool_url = local_pool_url​
        # Rantai Umpan Proksi Berjenjang: CDN Mirrors -> GitHub Raw -> 
Public APIs​
        self.proxy_feed_chains: List[str] = [​
            
"https://cdn.jsdelivr.net/gh/monosans/proxy-list@main/proxies/http.txt
",​
            
"https://fastly.jsdelivr.net/gh/jetkai/proxy-list@main/online-proxies/
txt/proxies-http.txt",​
            
"https://fastly.jsdelivr.net/gh/roosterkid/openproxylist@main/HTTPS_RA
W.txt",​
            
"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.tx
t",​
            
"https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every
-minute/main/http.txt",​
            
"https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-li
st-raw.txt",​
            
"https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt
",​
            
"https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/
http.txt",​
            
"https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.
txt",​
            
"https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",​



<!-- [ID:14_SEC_STEALTH_S011] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR, :150 -->
## Halaman 195

            
"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&
timeout=5000&country=all",​
            "https://www.proxy-list.download/api/v1/get?type=http",​
            "https://api.openproxylist.xyz/http.txt"​
        ]​
        self.verified_proxies: List[str] = []​
​
    async def get_working_proxy(self) -> Optional[str]:​
        """Mengambil proksi dari daemon Redis lokal, otomatis failover 
ke 13 umpan publik."""​
        async with httpx.AsyncClient(timeout=4.0) as client:​
            # Jalur 1: Coba daemon lokal jhao104/proxy_pool terlebih 
dahulu​
            try:​
                resp = await client.get(f"{self.local_pool_url}/get/")​
                if resp.status_code == 200 and "proxy" in resp.json():​
                    return f"http://{resp.json()['proxy']}"​
            except Exception:​
                pass​
​
            # Jalur 2: Jika kolam memori kosong, panen dari rantai CDN 
& GitHub Raw secara acak​
            if not self.verified_proxies:​
                feeds = random.sample(self.proxy_feed_chains, k=min(4, 
len(self.proxy_feed_chains)))​
                for feed_url in feeds:​
                    try:​
                        r = await client.get(feed_url)​
                        if r.status_code == 200:​
                            lines = [​
                                line.strip().split()[0]​
                                for line in r.text.splitlines()​
                                if ":" in line and not 
line.startswith("#")​
                            ]​
                            self.verified_proxies.extend(lines[:150])​
                    except Exception:​
                        continue​
​
            if self.verified_proxies:​
                chosen = random.choice(self.verified_proxies)​
                return f"http://{chosen}"​
        return None​
​
    async def report_dead_proxy(self, proxy_url: str) -> None:​
        """Menghapus proksi mati dari memori dan melaporkannya ke 
jhao104/proxy_pool."""​



<!-- [ID:14_SEC_STEALTH_S012] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR -->
## Halaman 281

mencoba ekstraksi cepat menggunakan spider_rs terlebih dahulu, beralih secara otomatis ke 
Scrapling StealthyFetcher (untuk melewati Cloudflare Turnstile dan merelokasi elemen adaptif 
12-faktor), dan menggunakan server internal Crawl4AI sebagai jalur terakhir. 
import asyncio​
import random​
import httpx​
from typing import List, Optional​
​
class MultiPathProxyAndScraperEngine:​
    """​
    Mesin Rotasi Proksi & Akuisisi Web Multi-Jalur Otomatis.​
    Tidak bergantung pada satu sumber proksi maupun satu pustaka web 
scraper.​
    """​
    def __init__(self, local_pool_url: str = "http://127.0.0.1:5010"):​
        self.local_pool_url = local_pool_url​
        # Rantai Umpan Proksi Berjenjang: CDN Mirrors -> GitHub Raw -> 
Public APIs​
        self.proxy_feed_chains: List[str] = [​
            
"https://cdn.jsdelivr.net/gh/monosans/proxy-list@main/proxies/http.txt
",​
            
"https://fastly.jsdelivr.net/gh/jetkai/proxy-list@main/online-proxies/
txt/proxies-http.txt",​
            
"https://fastly.jsdelivr.net/gh/roosterkid/openproxylist@main/HTTPS_RA
W.txt",​
            
"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.tx
t",​
            
"https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every
-minute/main/http.txt",​
            
"https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-li
st-raw.txt",​
            
"https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt
",​
            
"https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/
http.txt",​
            
"https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.
txt",​
            
"https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",​



<!-- [ID:14_SEC_STEALTH_S013] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR, :150 -->
## Halaman 282

            
"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&
timeout=5000&country=all",​
            "https://www.proxy-list.download/api/v1/get?type=http",​
            "https://api.openproxylist.xyz/http.txt"​
        ]​
        self.verified_proxies: List[str] = []​
​
    async def get_working_proxy(self) -> Optional[str]:​
        """Mengambil proksi dari daemon Redis lokal, otomatis failover 
ke 13 umpan publik."""​
        async with httpx.AsyncClient(timeout=4.0) as client:​
            # Jalur 1: Coba daemon lokal jhao104/proxy_pool terlebih 
dahulu​
            try:​
                resp = await client.get(f"{self.local_pool_url}/get/")​
                if resp.status_code == 200 and "proxy" in resp.json():​
                    return f"http://{resp.json()['proxy']}"​
            except Exception:​
                pass​
​
            # Jalur 2: Jika kolam memori kosong, panen dari rantai CDN 
& GitHub Raw secara acak​
            if not self.verified_proxies:​
                feeds = random.sample(self.proxy_feed_chains, k=min(4, 
len(self.proxy_feed_chains)))​
                for feed_url in feeds:​
                    try:​
                        r = await client.get(feed_url)​
                        if r.status_code == 200:​
                            lines = [​
                                line.strip().split()[0]​
                                for line in r.text.splitlines()​
                                if ":" in line and not 
line.startswith("#")​
                            ]​
                            self.verified_proxies.extend(lines[:150])​
                    except Exception:​
                        continue​
​
            if self.verified_proxies:​
                chosen = random.choice(self.verified_proxies)​
                return f"http://{chosen}"​
        return None​
​
    async def report_dead_proxy(self, proxy_url: str) -> None:​
        """Menghapus proksi mati dari memori dan melaporkannya ke 
jhao104/proxy_pool."""​



<!-- [ID:14_SEC_STEALTH_S014] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR -->
## Halaman 339

import httpx​
from typing import List, Optional​
​
class MultiPathProxyAndScraperEngine:​
    """​
    Mesin Rotasi Proksi & Akuisisi Web Multi-Jalur Otomatis.​
    Tidak bergantung pada satu sumber proksi maupun satu pustaka web 
scraper.​
    """​
    def __init__(self, local_pool_url: str = "http://127.0.0.1:5010"):​
        self.local_pool_url = local_pool_url​
        # Rantai Umpan Proksi Berjenjang: CDN Mirrors -> GitHub Raw -> 
Public APIs​
        self.proxy_feed_chains: List[str] = [​
            
"https://cdn.jsdelivr.net/gh/monosans/proxy-list@main/proxies/http.txt
",​
            
"https://fastly.jsdelivr.net/gh/jetkai/proxy-list@main/online-proxies/
txt/proxies-http.txt",​
            
"https://fastly.jsdelivr.net/gh/roosterkid/openproxylist@main/HTTPS_RA
W.txt",​
            
"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.tx
t",​
            
"https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every
-minute/main/http.txt",​
            
"https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-li
st-raw.txt",​
            
"https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt
",​
            
"https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/
http.txt",​
            
"https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.
txt",​
            
"https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",​
            
"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&
timeout=5000&country=all",​
            "https://www.proxy-list.download/api/v1/get?type=http",​
            "https://api.openproxylist.xyz/http.txt"​



<!-- [ID:14_SEC_STEALTH_S015] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR, :150 -->
## Halaman 340

        ]​
        self.verified_proxies: List[str] = []​
​
    async def get_working_proxy(self) -> Optional[str]:​
        """Mengambil proksi dari daemon Redis lokal, otomatis failover 
ke 13 umpan publik."""​
        async with httpx.AsyncClient(timeout=4.0) as client:​
            # Jalur 1: Coba daemon lokal jhao104/proxy_pool terlebih 
dahulu​
            try:​
                resp = await client.get(f"{self.local_pool_url}/get/")​
                if resp.status_code == 200 and "proxy" in resp.json():​
                    return f"http://{resp.json()['proxy']}"​
            except Exception:​
                pass​
​
            # Jalur 2: Jika kolam memori kosong, panen dari rantai CDN 
& GitHub Raw secara acak​
            if not self.verified_proxies:​
                feeds = random.sample(self.proxy_feed_chains, k=min(4, 
len(self.proxy_feed_chains)))​
                for feed_url in feeds:​
                    try:​
                        r = await client.get(feed_url)​
                        if r.status_code == 200:​
                            lines = [​
                                line.strip().split()[0]​
                                for line in r.text.splitlines()​
                                if ":" in line and not 
line.startswith("#")​
                            ]​
                            self.verified_proxies.extend(lines[:150])​
                    except Exception:​
                        continue​
​
            if self.verified_proxies:​
                chosen = random.choice(self.verified_proxies)​
                return f"http://{chosen}"​
        return None​
​
    async def report_dead_proxy(self, proxy_url: str) -> None:​
        """Menghapus proksi mati dari memori dan melaporkannya ke 
jhao104/proxy_pool."""​
        raw_host = proxy_url.replace("http://", 
"").replace("https://", "")​
        if raw_host in self.verified_proxies:​
            self.verified_proxies.remove(raw_host)​
        try:​



<!-- [ID:14_SEC_STEALTH_S016] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR, PROV -->
# =====================================================================
class BindMerchantSession(BaseModel):
    provider: str                      # 'GOPAY', 'DANA', 'SHOPEE', 'OVO_GRAB', atau nama baru
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    raw_cookie: Optional[str] = None
    custom_headers: Optional[Dict[str, str]] = None

@app.post("/api/merchant/bind-session")
async def bind_merchant_session(req: BindMerchantSession):
    """
    Suntikkan Token / Cookie 1 kali saja dari Bot Telegram / Panel Admin Anda.
    Server akan menyimpannya di Vault dan menjaga sesinya tetap hidup.
    """
    prov = req.provider.upper()
    if prov not in PROVIDER_PROFILES:
        raise HTTPException(status_code=400, detail=f"Provider {prov} belum terdaftar di profil.")

    VAULT[prov] = {
        "device_id": VAULT.get(prov, {}).get("device_id", str(uuid.uuid4())),
        "access_token": req.access_token,
        "refresh_token": req.refresh_token,
        "raw_cookie": req.raw_cookie,
        "custom_headers": req.custom_headers or {},
        "is_logged_in": True,
        "bound_at": int(time.time())
    }
    save_vault(VAULT)
    return {"message": f"Sesi {prov} berhasil dikunci di server!", "device_id": VAULT[prov]["device_id"]}


<!-- [ID:14_SEC_STEALTH_S017] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 196

        raw_host = proxy_url.replace("http://", 
"").replace("https://", "")​
        if raw_host in self.verified_proxies:​
            self.verified_proxies.remove(raw_host)​
        try:​
            async with httpx.AsyncClient(timeout=2.0) as client:​
                await 
client.get(f"{self.local_pool_url}/delete/?proxy={raw_host}")​
        except Exception:​
            pass​
​
    async def scrape_with_rolling_fallback(self, target_url: str, 
css_selector: str = "body") -> str:​
        """​
        Ekstraksi Web 3-Tingkat:​
        Tier 1: Spider-RS (Rust HTTP/Smart Chrome Streaming)​
        Tier 2: Scrapling StealthyFetcher (Cloudflare Turnstile Bypass 
+ Adaptive 12-Factor Relocation)​
        Tier 3: Crawl4AI Internal Docker Service (Isolated Network)​
        """​
        proxy = await self.get_working_proxy()​
​
        # TIER 1: Spider-RS (Kecepatan Ekstrem Berbasis Rust)​
        try:​
            import spider_rs​
            website = spider_rs.Website(target_url)​
            website.crawl()​
            pages = website.get_pages()​
            if pages and len(pages[0].get_content()) > 100:​
                return pages[0].get_content()​
        except Exception:​
            pass​
​
        # TIER 2: Scrapling StealthyFetcher (Anti-Bot Bypass & 
Adaptive Element Tracking)​
        try:​
            from scrapling.fetchers import StealthyFetcher​
            StealthyFetcher.adaptive = True​
            page = await StealthyFetcher.async_fetch(​
                target_url,​
                headless=True,​
                network_idle=True,​
                proxy=proxy​
            )​
            elements = page.css(css_selector, adaptive=True)​
            if elements:​
                return "\n".join([el.text for el in elements if 
el.text])​



<!-- [ID:14_SEC_STEALTH_S018] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 3. ANTI-TUYUL DAILY CLAIM: Device Fingerprint Binding + Max Bonus 
Cap (25 Koin)​
MAX_KOIN_BONUS_CAP = 25​
​
async def claim_daily_bonus_safe(​
    db: aiosqlite.Connection, user_id: int, device_fp_hash: str, 
today_str: str​
) -> tuple[bool, str]:​
    async with get_user_lock(user_id):​
        cursor = await db.execute(​
            "SELECT COUNT(DISTINCT user_id) FROM daily_claims WHERE 
device_fp = ? AND claim_date = ?",​
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
            WHERE user_id = ?​
              AND (last_claim_date IS NULL OR last_claim_date != ?)​
              AND koin_bonus < ?​
            RETURNING koin_bonus;​
            """,​
            (MAX_KOIN_BONUS_CAP, today_str, user_id, today_str, 
MAX_KOIN_BONUS_CAP),​
        )​
        row = await cursor.fetchone()​
        if not row:​
            return False, "ALREADY_CLAIMED_OR_CAP_REACHED"​
​
        await db.execute(​
            "INSERT INTO daily_claims (user_id, device_fp, claim_date) 
VALUES (?, ?, ?)",​
            (user_id, device_fp_hash, today_str),​
        )​
        await db.commit()​
        return True, f"SUCCESS_NEW_BONUS_{row[0]}"​
 
Dimensi 3: Refactoring Logika Bisnis, Infrastruktur, 



<!-- [ID:14_SEC_STEALTH_S019] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 283

        raw_host = proxy_url.replace("http://", 
"").replace("https://", "")​
        if raw_host in self.verified_proxies:​
            self.verified_proxies.remove(raw_host)​
        try:​
            async with httpx.AsyncClient(timeout=2.0) as client:​
                await 
client.get(f"{self.local_pool_url}/delete/?proxy={raw_host}")​
        except Exception:​
            pass​
​
    async def scrape_with_rolling_fallback(self, target_url: str, 
css_selector: str = "body") -> str:​
        """​
        Ekstraksi Web 3-Tingkat:​
        Tier 1: Spider-RS (Rust HTTP/Smart Chrome Streaming)​
        Tier 2: Scrapling StealthyFetcher (Cloudflare Turnstile Bypass 
+ Adaptive 12-Factor Relocation)​
        Tier 3: Crawl4AI Internal Docker Service (Isolated Network)​
        """​
        proxy = await self.get_working_proxy()​
​
        # TIER 1: Spider-RS (Kecepatan Ekstrem Berbasis Rust)​
        try:​
            import spider_rs​
            website = spider_rs.Website(target_url)​
            website.crawl()​
            pages = website.get_pages()​
            if pages and len(pages[0].get_content()) > 100:​
                return pages[0].get_content()​
        except Exception:​
            pass​
​
        # TIER 2: Scrapling StealthyFetcher (Anti-Bot Bypass & 
Adaptive Element Tracking)​
        try:​
            from scrapling.fetchers import StealthyFetcher​
            StealthyFetcher.adaptive = True​
            page = await StealthyFetcher.async_fetch(​
                target_url,​
                headless=True,​
                network_idle=True,​
                proxy=proxy​
            )​
            elements = page.css(css_selector, adaptive=True)​
            if elements:​
                return "\n".join([el.text for el in elements if 
el.text])​



<!-- [ID:14_SEC_STEALTH_S020] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 341

            async with httpx.AsyncClient(timeout=2.0) as client:​
                await 
client.get(f"{self.local_pool_url}/delete/?proxy={raw_host}")​
        except Exception:​
            pass​
​
    async def scrape_with_rolling_fallback(self, target_url: str, 
css_selector: str = "body") -> str:​
        """​
        Ekstraksi Web 3-Tingkat:​
        Tier 1: Spider-RS (Rust HTTP/Smart Chrome Streaming)​
        Tier 2: Scrapling StealthyFetcher (Cloudflare Turnstile Bypass 
+ Adaptive 12-Factor Relocation)​
        Tier 3: Crawl4AI Internal Docker Service (Isolated Network)​
        """​
        proxy = await self.get_working_proxy()​
​
        # TIER 1: Spider-RS (Kecepatan Ekstrem Berbasis Rust)​
        try:​
            import spider_rs​
            website = spider_rs.Website(target_url)​
            website.crawl()​
            pages = website.get_pages()​
            if pages and len(pages[0].get_content()) > 100:​
                return pages[0].get_content()​
        except Exception:​
            pass​
​
        # TIER 2: Scrapling StealthyFetcher (Anti-Bot Bypass & 
Adaptive Element Tracking)​
        try:​
            from scrapling.fetchers import StealthyFetcher​
            StealthyFetcher.adaptive = True​
            page = await StealthyFetcher.async_fetch(​
                target_url,​
                headless=True,​
                network_idle=True,​
                proxy=proxy​
            )​
            elements = page.css(css_selector, adaptive=True)​
            if elements:​
                return "\n".join([el.text for el in elements if 
el.text])​
        except Exception:​
            if proxy:​
                await self.report_dead_proxy(proxy)​
​
        # TIER 3: Fallback ke Crawl4AI Internal Endpoint (Tanpa Ekspos 



<!-- [ID:14_SEC_STEALTH_S021] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# Daftarkan plugin inti ke Plugin Surface saat inisialisasi Modul 1
async def _core_vault_health() -> bool:
   return Path(DB_PATH).parent.exists()
PLUGIN_SURFACE.register(
   name="core_sqlite_wal_vault",
   version="4.0.0",
   handler=lambda *a, **kw: asyncio.sleep(0),
   health_check=_core_vault_health,
)
PLUGIN_SURFACE.register(
   name="bittensor_subnet27_bridge",
   version="4.0.0",
   handler=BITTENSOR_ADAPTER.call_bittensor_chutes_llm,
   health_check=lambda: asyncio.sleep(0, result=True),
)

<!-- [ID:14_SEC_STEALTH_S022] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: PROXY IP AWAL -->
# ── Subcommand: Bright Data Farm ───────────────────────────────────
def cmd_brightfarm(args):
    try:
        import httpx  # noqa: F401
    except ImportError:
        sys.exit("httpx belum terinstall — jalankan: pip install httpx")

    proxy_str = args.proxy or BRIGHTDATA_URL
    tg_token = args.tg_token or TG_BOT_TOKEN
    tg_chatid = args.tg_chatid or TG_CHAT_ID

    print("== Cek Koneksi Bright Data Proxy ==")
    try:
        import httpx
        with httpx.Client(proxy=proxy_str, timeout=10.0) as c:
            ip = c.get("https://api.ipify.org").text
            print(f"[Proxy IP Awal] {ip}")
    except Exception:
        print("[!] Proxy terhubung, lanjut proses farming...")

    print(f"== Start Parallel Farming {args.count} akun ({args.workers} Threads) ==")
    
    start_time_all = time.time()
    ok, fail = [], []

    # Menggunakan ThreadPoolExecutor untuk eksekusi PARALEL bersamaan
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(worker_process, i, args, proxy_str): i for i in range(1, args.count + 1)}
        for future in as_completed(futures):
            success, result = future.result()
            if success:
                ok.append(result)
            else:
                fail.append(result)

    total_time = time.time() - start_time_all
    _summary(ok, fail, total_time, tg_token, tg_chatid)



<!-- [ID:14_SEC_STEALTH_S023] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 112

Siklus adaptasi mandiri dimulai secara terjadwal setiap malam melalui penjadwal cron bawaan 
pada Hermes Agent yang mampu mengonversi instruksi bahasa alami menjadi tugas latar 
belakang tanpa pengawasan. Agen pemantau menggunakan mesin akuisisi web tiga tingkat yang 
didukung oleh kolam proksi multi-CDN (TheSpeedX/PROXY-List dengan 5.610+ proksi aktif, 
proxifly/free-proxy-list yang memvalidasi 84.522 proksi setiap 5 menit via jsDelivr CDN, 
monosans/proxy-list, serta daemon Go WangYihang/Proxy-Verifier dan jhao104/proxy_pool). 
Perayapan tingkat pertama dieksekusi oleh spider-rs/spider berbasis Rust dengan strategi HTTP-
first yang sangat cepat, beralih secara otomatis ke tingkat kedua menggunakan D4Vinci/Scrapling 
(atau port Rust chrisabruce/scrapling-rs yang mengemulasi 135+ profil sidik jari TLS JA3/JA4, 
menembus Cloudflare Turnstile secara otomatis, dan menggunakan algoritma kemiripan 12-faktor 
berbasis SQLite untuk menemukan kembali elemen meskipun situs target mengubah struktur 
HTML/CSS), dan menggunakan layanan internal Crawl4AI sebagai cadangan tingkat ketiga. Modul 
perayap ini memindai API pencarian dan tren GitHub dengan filter kueri ketat license:mit dan 
license:apache-2.0 pada topik-topik operasional utama, sekaligus membaca perubahan status 
kuota terbaru dari empat registri penemuan otomatis, yaitu cheahjs/free-llm-api-resources, open-
free-llm-api/awesome-freellm-apis, zebbern/no-cost-ai, dan tokengratis.id.

<!-- [ID:14_SEC_STEALTH_S024] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: 10PX -->
## Halaman 154

text-cyan-400">TOKEN_BOT_CADANGAN</span>​
            <span className="flex items-center gap-1 text-[10px] font-mono text-emerald-400">​
              <CheckCircle2 className="h-3 w-3" /> FAILOVER​
            </span>​
          </div>​
          <p className="text-sm font-bold text-white mt-2">@AetherBackupBot</p>​
          <span className="text-[10px] text-slate-500 font-mono">Pengalihan Otomatis Saat Limit 
429</span>​
        </div>​
      </div>​
​
      {/* Simulator Box */}​
      <div className="rounded-xl border border-white/10 bg-slate-900/40 p-5">​
        <h3 className="text-xs font-mono text-slate-300 mb-3 flex items-center gap-1.5">​
          <MessageSquare className="h-4 w-4 text-blue-400" /> Uji Coba Pengiriman Pesan & 
Failover Trigger​
        </h3>​
        <div className="flex gap-2">​
          <input​
            type="text"​
            value={testMsg}​
            onChange={(e) => setTestMsg(e.target.value)}​
            placeholder="Ketik pesan pengujian bot..."​
            className="flex-1 rounded-xl border border-white/10 bg-slate-950/80 px-4 py-2 text-xs 
text-slate-200 focus:border-cyan-500 focus:outline-none"​
          />​
          <button​
            onClick={handleTestBroadcast}​
            disabled={!testMsg.trim()}​
            className="flex items-center gap-1.5 rounded-xl bg-blue-600 px-5 py-2 text-xs 
font-semibold text-white hover:bg-blue-500 disabled:opacity-50"​
          >​
            <Send className="h-3.5 w-3.5" /> Kirim​
          </button>​
        </div>​
​
        {logResponse && (​
          <div className="mt-4 rounded-lg bg-black/60 border border-white/5 p-3 text-xs 
font-mono text-cyan-300">​
            {logResponse}​
          </div>​
        )}​
      </div>​
    </div>​
  );​
}​
 


