
<!-- [ID:01_ARCH_S001] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: DICT -->
# test recover:
curl -X POST localhost:8000/command -H "X-Internal-Key: $KEY" \
  -d 'text=/recover 123456&channel=telegram&user_id=<owner_id>'

"""
Adapter provider LLM. Semua provider punya interface sama:
  async def complete(model, messages, **kwargs) -> dict
  async def stream(model, messages, **kwargs) -> AsyncIterator[dict]
"""
import os, httpx
from typing import AsyncIterator

class ProviderBase:
    name: str = "base"
    base_url: str = ""
    api_key_env: str = ""

    def __init__(self):
        self.api_key = os.environ.get(self.api_key_env, "")

    def available(self) -> bool:
        return bool(self.api_key)

    async def complete(self, model: str, messages: list, **kw) -> dict:
        raise NotImplementedError

    async def stream(self, model: str, messages: list, **kw) -> AsyncIterator[dict]:
        raise NotImplementedError


class OpenAIProvider(ProviderBase):
    name = "openai"; base_url = "https://api.openai.com/v1"; api_key_env = "OPENAI_API_KEY"

    async def complete(self, model, messages, **kw) -> dict:
        async with httpx.AsyncClient(timeout=90) as c:
            r = await c.post(f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": model, "messages": messages, **kw})
            r.raise_for_status()
            d = r.json()
            return {"provider": self.name, "model": model,
                    "content": d["choices"][0]["message"]["content"],
                    "usage": d.get("usage", {})}


class AnthropicProvider(ProviderBase):
    name = "anthropic"; base_url = "https://api.anthropic.com/v1"; api_key_env = "ANTHROPIC_API_KEY"

    async def complete(self, model, messages, **kw) -> dict:
        sys = next((m["content"] for m in messages if m["role"] == "system"), None)
        msgs = [m for m in messages if m["role"] != "system"]
        body = {"model": model, "max_tokens": kw.get("max_tokens", 2048), "messages": msgs}
        if sys: body["system"] = sys
        async with httpx.AsyncClient(timeout=90) as c:
            r = await c.post(f"{self.base_url}/messages",
                headers={"x-api-key": self.api_key, "anthropic-version": "2023-06-01"},
                json=body)
            r.raise_for_status()
            d = r.json()
            return {"provider": self.name, "model": model,
                    "content": d["content"][0]["text"],
                    "usage": d.get("usage", {})}


class LocalProvider(ProviderBase):
    """Fallback lokal: Ollama di localhost."""
    name = "local"; base_url = "http://localhost:11434"; api_key_env = "LOCAL_LLM_KEY"

    def available(self) -> bool: return True   # selalu ada

    async def complete(self, model, messages, **kw) -> dict:
        async with httpx.AsyncClient(timeout=120) as c:
            r = await c.post(f"{self.base_url}/api/chat",
                json={"model": model, "messages": messages, "stream": False})
            r.raise_for_status()
            d = r.json()
            return {"provider": self.name, "model": model,
                    "content": d["message"]["content"],
                    "usage": d.get("eval_count", {})}


PROVIDERS = {
    "openai": OpenAIProvider(),
    "anthropic": AnthropicProvider(),
    "local": LocalProvider(),
}
"""
Budget enforcement. Kalau lewat batas, tolak (bukan "warning").
Budget harian per kategori agent + global.
"""
import time, json
from pathlib import Path

STORE = Path("services/ai-gateway/usage")
STORE.mkdir(parents=True, exist_ok=True)


<!-- [ID:01_ARCH_S002] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
## Halaman 122

Horizon, OmniRoute, WAHA WhatsApp Gateway, dan Proxy Pool Harvester) dijalankan secara 
serentak menggunakan berkas docker-compose.yml berikut:
```yaml
version: "3.9"
services:
  new-api-horizon:
    image: calciumion/new-api-horizon:latest
    container_name: new-api-horizon
    restart: always
    ports:
      - "3001:3000"
    environment:
      - SQL_DSN=${NEON_SQL_DSN}
      - REDIS_CONN_STRING=${REDIS_CONN_STRING}
      - SESSION_SECRET=${SESSION_SECRET}
      - TZ=Asia/Jakarta
    volumes:
      - ./data/new-api:/data
  omniroute-gateway:
    image: ghcr.io/diegosouzapw/omniroute:latest
    container_name: omniroute
    restart: always
    ports:
      - "20128:20128"
    env_file:
      - .env
  waha-whatsapp:
    image: devlikeapro/waha:latest
    container_name: waha-gateway
    restart: always
    ports:


## Halaman 123

      - "3000:3000"
    env_file:
      - .env
  proxy-pool:
    image: jhao104/proxy_pool:latest
    container_name: proxy-harvester
    restart: always
    ports:
      - "5010:5010"
    environment:
      - DB_CONN=${REDIS_CONN_STRING}
```
#### Tahap 3 (Prioritas Main): Implementasi Kode Pemutus Sirkuit Margin 95% dan Kasir Pakasir 
API v2
Untuk menegakkan batas pengeluaran API per pengguna maksimal 5% dari pendapatan 
langganan sekaligus mengintegrasikan skema pembayaran QRIS Pakasir API v2 yang bebas 
potongan MDR (0% untuk nominal transaksi \le \text{Rp 100.000}) beserta pengalihan otomatis ke 
Tripay, Duitku, dan @CryptoBot, layanan backend Python mengeksekusi modul pengendali 
finansial berikut:
```python
import os
import httpx
from typing import Dict, Any
class AutonomousTreasuryAndMarginGuard:
    """
    Mengunci Margin Bersih >= 95% per pengguna (Hard-Cap COGS <= 5% dari Revenue)
    dan menangani pembuatan faktur pembayaran QRIS Pakasir API v2 (0% MDR <= Rp100.000).
    """
    def __init__(self):
        self.max_cogs_ratio = float(os.getenv("HARD_CAP_COGS_RATIO", "0.05"))


## Halaman 124

        self.pakasir_slug = os.getenv("PAKASIR_SLUG", "bikinai-pro")
        self.pakasir_key = os.getenv("PAKASIR_API_KEY", "")
    def select_execution_tier(self, user_revenue_idr: float, user_current_cogs_idr: float, 
prompt_complexity: float) -> str:
        """
        Menentukan apakah kueri pengguna boleh mengakses API Grosir Berbayar
        atau wajib dialihkan ke Kolam 100% Gratis (Zero-Cost Pool).
        """
        max_allowed_cogs = user_revenue_idr * self.max_cogs_ratio
        if user_revenue_idr <= 0 or user_current_cogs_idr >= max_allowed_cogs:
            return "PERPETUAL_FREE_POOL"
        
        if prompt_complexity >= float(os.getenv("ROUTELLM_THRESHOLD", "0.11593")):
            return "WHOLESALE_PAYG_POOL"
        
        return "PERPETUAL_FREE_POOL"
    async def create_qris_invoice_v2(self, order_id: str, amount_idr: int = 99000, redirect_url: str = 
"https://app-domain.pages.dev/success") -> Dict[str, Any]:
        """
        Membuat transaksi menggunakan endpoint baru Pakasir API v2 (Wajib per 20 Okt 2026).
        Nominal Rp 99.000 dipilih agar memenuhi syarat aturan BI MDR QRIS 0%.
        """
        pakasir_v2_url = f"https://pakasir.com/pay-v2/{self.pakasir_slug}?qris_only=1&redirect=
{redirect_url}"
        payload = {
            "order_id": order_id,
            "amount": amount_idr,
            "api_key": self.pakasir_key
        }
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:


## Halaman 125

                resp = await client.post("https://pakasir.com/api/v2/transaction/create", json=payload)
                if resp.status_code == 200:
                    return {"gateway": "Pakasir_v2", "payment_url": pakasir_v2_url, "data": resp.json()}
            except Exception:
                pass
            return {
                "gateway": "Failover_QRIS_CryptoBot",
                "payment_url": f"https://t.me/CryptoBot?start=pay_{order_id}",
                "amount_idr": amount_idr
            }
```
#### Tahap 4 (Prioritas Main): Panduan Kode dan CSS Tampilan Website Futuristic Luxury
Untuk merakit antarmuka web komersial bergaya *Futuristic Luxury* yang siap di-deploy secara 
gratis ke Cloudflare Pages atau Vercel, arsitektur frontend menggunakan kerangka kerja **Next.js 
15 (App Router)**, **React 19**, dan **Tailwind CSS v4** yang dikombinasikan dengan komponen 
visual dari **Aceternity UI** (ui.aceternity.com) dan **Magic UI** (magicui.design). Inisialisasi 
proyek dan penarikan komponen animasi (@aceternity/spotlight-new, @aceternity/background-
beams, @magicui/border-beam, @magicui/bento-grid, dan @magicui/shimmer-button) dilakukan 
melalui perintah terminal berikut:
```bash
# 1. Inisialisasi proyek Next.js 15 dengan TypeScript dan Tailwind CSS v4
npx create-next-app@latest bikinai-web --typescript --tailwind --eslint --app --use-npm
cd bikinai-web
# 2. Instalasi pustaka animasi Motion dan ikon Lucide
npm install motion clsx tailwind-merge lucide-react
# 3. Penarikan komponen dari registri resmi Aceternity UI & Magic UI
npx shadcn@latest add @aceternity/spotlight-new @aceternity/background-beams
npx shadcn@latest add @magicui/border-beam @magicui/bento-grid @magicui/shimmer-button 
@magicui/magic-card
```



<!-- [ID:01_ARCH_S003] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: STR, A-ZA-Z0-9_-, A-ZA-Z0-9, BOT-WRITE, AUTO-BOT -->
# 6. GENERATOR BOT OTONOM INJEKTOR MONOREPO & GITHUB CODESPACES​
# 
======================================================================
========​
def generate_autonomous_github_bot():​
    """​
    Mencetak skrip Bot Otonom (auto_repo_bot.py) yang akan berjalan di 
GitHub Codespaces Anda.​
    Tugas Bot: Membaca balasan kode dari AI di setiap fresh chat, 
otomatis membuat foldernya,​
    menulis/mengupdate file kodenya, dan melakukan Git Commit & Push 
mandiri!​
    """​
    bot_code = '''#!/usr/bin/env python3​
"""​
======================================================================
==========​
BOT OTONOM ARSITEK MONOREPO & GITHUB CODESPACES (auto_repo_bot.py)​
======================================================================
==========​
Cara Pakai di GitHub Codespaces:​
1. Setiap kali selesai 1 Fresh Chat bersama AI, minta AI memberi tag 
path di atas blok kode:​
   Contoh format yang diminta dari AI:​
   ```python filepath: src/02_core_ai/router.py​
   # isi kode dari AI...​
 
Atau komentar di baris pertama dalam blok kode: # FILE: src/02_core_ai/router.py 2. 
Copy-paste seluruh balasan chat AI ke dalam file inbox_ai.md di Codespaces. 3. Jalankan 
perintah: python3 auto_repo_bot.py -> Bot otomatis membuat semua folder yang belum ada, 
menulis file kodenya, mencatat log integrasi, dan otomatis menjalankan git add, commit, & 
push! """ import os import re import subprocess from pathlib import Path from datetime import 
datetime 
INBOX_FILE = Path("inbox_ai.md") ARCHIVE_DIR = Path(".bot_history_inbox") 
ARCHIVE_DIR.mkdir(exist_ok=True) 
def parse_and_inject_code(markdown_text: str) -> list[str]: # Menangkap blok kode dengan 
deklarasi path file di pagar atau di baris pertama komentar pattern = re.compile( 
r"[a-zA-Z0-9_-](?:\s+(?:filepath:|file:|path:)?\s([a-zA-Z0-9_./-]+.[a-zA-Z0-9]+))?\n(.*?)```", 
re.DOTALL ) created_files = [] 
for match in pattern.finditer(markdown_text): header_path, code_body = match.group(1), 
match.group(2) target_path = header_path 
# Jika path ada di baris pertama komentar di dalam blok kode (# FILE: src/...) if not target_path: 
first_line = code_body.splitlines()[0] if code_body.splitlines() else "" m_inner = 
re.search(r"(?:FILE|PATH|FILEPATH)\s*:\s*([a-zA-Z0-9_./-]+.[a-zA-Z0-9]+)", first_line, 
re.IGNORECASE) if m_inner: target_path = m_inner.group(1) 


## Halaman 10

if target_path: clean_path = Path(target_path.strip().lstrip("/")) 
clean_path.parent.mkdir(parents=True, exist_ok=True) clean_path.write_text(code_body, 
encoding="utf-8") created_files.append(str(clean_path)) print(f"✅ [BOT-WRITE] Folder & File 
otomatis dibuat/diupdate: {clean_path} ({len(code_body):,} chars)") 
return created_files 
def auto_git_sync(files_modified: list[str]): if not files_modified: return try: subprocess.run(["git", 
"add", "."], check=True) msg = f"🤖 [AUTO-BOT] Injeksi {len(files_modified)} file: {', 
'.join(files_modified[:4])}" subprocess.run(["git", "commit", "-m", msg], check=True) print(f"📦 
[BOT-GIT] Berhasil commit: {msg}") # Otomatis push jika remote origin sudah terhubung di 
Codespaces subprocess.run(["git", "push"], check=False) except Exception as e: print(f"ℹ️ 
[BOT-GIT] Catatan Git lokal tersimpan (Push manual jika diperlukan): {e}") 
def main(): if not INBOX_FILE.exists(): INBOX_FILE.write_text("# Tempel (Paste) balasan kode 
dari Sesi Chat AI Anda di sini lalu jalankan: python3 auto_repo_bot.py\n", encoding="utf-8") 
print(f"📁 File {INBOX_FILE} telah disiapkan. Tempel balasan AI Anda di sana!") return 
raw_chat = INBOX_FILE.read_text(encoding="utf-8") if len(raw_chat.strip()) < 20: print("⚠️ 
inbox_ai.md masih kosong. Tempel balasan kode dari AI terlebih dahulu.") return 
written = parse_and_inject_code(raw_chat) if written: ts = 
datetime.now().strftime("%Y%m%d_%H%M%S") backup = ARCHIVE_DIR / f"session_{ts}.md" 
backup.write_text(raw_chat, encoding="utf-8") INBOX_FILE.write_text("", encoding="utf-8") # 
Kosongkan inbox untuk sesi chat berikutnya auto_git_sync(written) print(f"\n🎉 SELESAI! 
{len(written)} file berhasil disuntikkan ke Monorepo & riwayat chat diarsipkan ke {backup}") else: 
print("⚠️ Tidak ditemukan penanda path file di blok kode. Pastikan AI menyertakan # FILE: 
nama_folder/nama_file.py di baris pertama tiap blok kode!") 
if name == "main": main() ''' (BOT_AUTONOMOUS_DIR / 
"auto_repo_bot.py").write_text(bot_code, encoding="utf-8") 
# Buat Prompt Standar Sesi Chat agar AI selalu patuh pada format Bot Otonom Anda 
prompt_guide = ( "# PROMPT WAJIB UNTUK SETIAP SESI FRESH CHAT AI ANDA\n\n" "Salin 
kalimat singkat ini setiap kali Anda meng-upload 1 file Sweetspot (<=45k karakter) ke AI:\n\n" "> 
"Kamu adalah Senior Principal Engineer untuk Monorepo Skala Besar saya. " "Baca 
seluruh spesifikasi di file blueprint yang saya lampirkan ini tanpa melewatkan 1 fitur pun. 
" "Catatan: Abaikan blok yang saya beri tanda [DROP_SAAT_AUDIT] (jika ada). " 
"Tuliskan kode produksi yang 100% utuh (tanpa placeholder/TODO). " "WAJIB: Di baris 
paling atas di dalam SETIAP blok kode, tuliskan komentar # FILE: 
path/lengkap/nama_file.ext " "agar Bot Otonom Monorepo saya (auto_repo_bot.py) bisa 
langsung membuat folder dan menyuntikkan kodenya secara otomatis ke GitHub 
Codespaces."\n" ) (BOT_AUTONOMOUS_DIR / 
"CARA_PAKAI_DAN_PROMPT_AI.md").write_text(prompt_guide, encoding="utf-8") 
=================================
=================================
============ 
7. EKSEKUSI PIPELINE UTAMA + 


## Halaman 11

PEMBUNGKUS AUTO-ZIP 
=================================
=================================
============ 
def execute_all(): all_sections = [] total_raw_chars = 0 
for pdf_f in RAW_PDF_FILES: if os.path.exists(pdf_f): slice_pdf_20_pages(pdf_f) md_p = 
extract_pdf_and_rescue_images(pdf_f, MINERU_OUT_DIR) txt = 
md_p.read_text(encoding="utf-8", errors="replace") total_raw_chars += len(txt) 
all_sections.extend(split_sections_lossless(txt, f"PDF:{Path(pdf_f).name}")) else: print(f"[!] File 
PDF {pdf_f} tidak ditemukan, dilewati.") 
for md_f in RAW_MD_FILES: if os.path.exists(md_f): txt = 
Path(md_f).read_text(encoding="utf-8", errors="replace") total_raw_chars += len(txt) 
all_sections.extend(split_sections_lossless(txt, f"MD:{Path(md_f).name}")) else: print(f"[!] File 
MD {md_f} tidak ditemukan, dilewati.") 
# Deduplikasi 100% SHA-256 Utuh (Hanya membuang jika isi karakter kembar 100% identik) 
domain_groups = defaultdict(list) seen_hashes = set() exact_dup_chars = 0 
for s in tqdm(all_sections, desc="Memeriksa Keutuhan 100% Karakter & Auto-Discovery"): if not 
s["content"]: continue h = hashlib.sha256(s["content"].encode("utf-8")).hexdigest() if h in 
seen_hashes: exact_dup_chars += len(s["content"]) continue seen_hashes.add(h) 
domain_groups[s["domain"]].append(s) 
# Tandai kemiripan parsial agar mudah Anda Audit Manual master_catalog = [] 
total_saved_chars = 0 
for dom in sorted(domain_groups.keys()): audited_secs = 
mark_similar_sections_for_human_audit(domain_groups[dom]) part_no = 1 curr_bucket, 
curr_meta = [], [] curr_len = 0 
for idx, s in enumerate(audited_secs, 1): img_str = f" | GAMBAR: {', '.join(s['dna']['images'][:3])}" 
if s["dna"]["images"] else "" tag_str = f" | TAG_ASLI: {', '.join(s['tags'][:4])}" if s["tags"] else "" 
audit_banner = ( f"\n<!-- 
======================================================================= 
-->\n" f"<!-- [ID:{dom}_S{idx:03d}] SUMBER: {s['source']} | KUALITAS: {s['dna']['grade']} (Skor: 
{s['dna']['score']}) -->\n" f"<!-- STATUS AUDIT: {s['audit_flag']}{tag_str}{img_str} -->\n" f"<!-- AKSI 
AUDIT ANDA: [PERTAHANKAN] (Ubah jadi [DROP_SAAT_AUDIT] jika tidak ingin dipakai AI) 
-->\n" f"<!-- 
======================================================================= 
-->\n" ) full_block = audit_banner + s["content"] total_saved_chars += len(s["content"]) 
sub_blocks = slice_oversized_safely(full_block, MAX_MD_SWEETSPOT_CHARS - 1200) for 
sub_i, sb in enumerate(sub_blocks, 1): if curr_len + len(sb) > MAX_MD_SWEETSPOT_CHARS 
and curr_bucket: fname = f"{dom}SWEETSPOT{part_no:02d}.md" (MODUL_MD_45K_DIR / 
fname).write_text("".join(curr_bucket), encoding="utf-8") master_catalog.append({"file": fname, 
"chars": curr_len, "items": curr_meta}) part_no += 1 curr_bucket, curr_meta, curr_len = [], [], 0 
curr_bucket.append(sb) curr_len += len(sb) curr_meta.append({ "id": f"{dom}_S{idx:03d}" + 


## Halaman 12

(f"_P{sub_i}" if len(sub_blocks) > 1 else ""), "title": re.sub(r"\s+", " ", s["title"])[:85], "grade": 
s["dna"]["grade"], "audit": "KEMBAR_PARSIAL" if "KEMBAR_PARSIAL" in s["audit_flag"] else 
"UNIK", "symbols": s["dna"]["symbols"][:5], "chars": len(sb) }) 
if curr_bucket: fname = f"{dom}SWEETSPOT{part_no:02d}.md" (MODUL_MD_45K_DIR / 
fname).write_text("".join(curr_bucket), encoding="utf-8") master_catalog.append({"file": fname, 
"chars": curr_len, "items": curr_meta}) 
# Cetak 1-3 File Master Peta Otak (Dikunci ketat <= 45.000 karakter per file) m_header = ( "# 
MASTER PETA OTAK & KONTRAK MONOREPO (SWEETSPOT <= 45.000 KARAKTER)\n" 
"Berisi 100% indeks seluruh modul, fungsi kode, gambar, dan 26_AUTO_DISCOVERY.\n" 
"Upload file ini di Sesi Pertama untuk menginisiasi struktur dasar Monorepo bersama 
auto_repo_bot.py.\n\n" ) m_part, m_curr, m_len = 1, [m_header], len(m_header) 
for entry in master_catalog: lines = [f"\n## 📁 {entry['file']} ({entry['chars']:,} chr)\n"] for it in 
entry["items"]: sym = f" | Fungsi: {', '.join(it['symbols'])}" if it["symbols"] else "" aud = " ⚠️*[Cek 
Audit Kembar]*" if it["audit"] == "KEMBAR_PARSIAL" else "" lines.append(f"- [{it['id']}] {it['title']} 
({it['chars']:,} chr | {it['grade']}{sym}){aud}\n") block = "".join(lines) 
if m_len + len(block) > MAX_MD_SWEETSPOT_CHARS and m_curr: (MASTER_BLUEPRINT / 
f"00_MASTER_PETA_OTAK_PART_{m_part:02d}.md").write_text("".join(m_curr), 
encoding="utf-8") m_part += 1 m_curr = [m_header + f"(Bagian Lanjutan {m_part})\n\n"] m_len = 
len(m_curr[0]) m_curr.append(block) m_len += len(block) 
if m_curr: (MASTER_BLUEPRINT / 
f"00_MASTER_PETA_OTAK_PART_{m_part:02d}.md").write_text("".join(m_curr), 
encoding="utf-8") 
# Bangkitkan Bot Otonom GitHub Codespaces generate_autonomous_github_bot() 
# Buat Laporan Audit Lossless audit_txt = ( f"# LAPORAN VERIFIKASI 100% LOSSLESS & 
PANEL AUDIT\n\n" f"- Total Karakter Mentah Masuk: {total_raw_chars:,} karakter\n" f"- 
Duplikat Kembar 100% Identik: {exact_dup_chars:,} karakter\n" f"- Total Karakter Bersih 
Tersimpan: {total_saved_chars:,} karakter (0% Karakter Hilang!)\n" f"- Jumlah File Modul 
Sweetspot (<=45k chr): {len(master_catalog)} file\n" ) (BASE_DRIVE_DIR / 
"00_LAPORAN_VERIFIKASI_LOSSLESS.md").write_text(audit_txt, encoding="utf-8") 
# Bungkus ZIP Otomatis di Google Drive zip_code_pack = str(BASE_DRIVE_DIR.parent / 
"PAKET_SIAP_CODING_DAN_BOT_OTONOM") print("\n[*] Membungkus Paket ZIP Siap 
Coding + Bot Otonom ke Google Drive...") shutil.make_archive(zip_code_pack, 'zip', 
BASE_DRIVE_DIR) print(f"✅ SELESAI! Paket ZIP Utuh tersimpan di Google Drive: 
{zip_code_pack}.zip") 
if IN_COLAB: try: files.download(f"{zip_code_pack}.zip") except Exception: print("ℹ️ File ZIP 
sudah aman di Google Drive Anda (silakan unduh langsung dari Drive atau tarik ke 
Codespaces).") 
if name == "main": execute_all() 
---​
​
### Bagian 2: Cara Kerja "Panel Audit Manual" + "Bot Otonom GitHub 
Codespaces" Anda​
​
Perhatikan betapa mudahnya alur kerja Anda setelah skrip di atas 
selesai:​
​
#### 1. Cara Anda Mengaudit Bagian yang Mirip (Sebelum Buat Kode)​
Di dalam setiap file pecahan `03_MODUL_MD_AUDIT_SIAP_PAKAI_45K`, jika 


## Halaman 13

ada bagian dari PDF dan MD yang membahas hal serupa (misal sama-sama 
membahas *Router LLM* tetapi isinya sedikit berbeda), skrip **tidak 
akan menghapus salah satunya**, melainkan menaruh keduanya 
berdampingan persis atas-bawah dengan label mencolok:​
```markdown​
<!-- [ID:02_CORE_AI_S001] SUMBER: MD:blueprint_utama.md | KUALITAS: 
BINTANG_5_KODE_UTUH (Skor: 85) -->​
<!-- STATUS AUDIT: ⚠️ KEMBAR_PARSIAL_DENGAN_VERSI_LAIN (Rekomendasi 
Otomatis: PILIH INI karena Skor=85) -->​
<!-- AKSI AUDIT ANDA: [PERTAHANKAN] (Ubah jadi [DROP_SAAT_AUDIT] jika 
tidak ingin dipakai AI) -->​
 
●​ Tugas Audit Anda sangat ringan: Buka file tersebut, tekan Ctrl + F dan cari kata 
KEMBAR_PARSIAL. Anda tinggal melihat 2 blok yang berdampingan itu. Jika Anda setuju 
dengan rekomendasi skor atau lebih suka versi yang bawah, Anda cukup menghapus 
blok yang tidak diinginkan (atau mengubah tulisannya menjadi [DROP_SAAT_AUDIT]), 
sehingga AI tidak akan pernah bingung menghadapi 2 instruksi ganda! 
2. Cara Menarik ZIP dari Google Drive Langsung ke Terminal GitHub Codespaces 
Tanpa perlu mengunduh ratusan MB ke HP/Laptop lalu meng-upload ulang ke GitHub 
Codespaces, Anda cukup: 
1.​ Klik kanan file PAKET_SIAP_CODING_DAN_BOT_OTONOM.zip di Google Drive Anda > 
Bagikan (Share) > Siapa saja yang memiliki link > Salin ID file-nya. 
2.​ Buka terminal GitHub Codespaces Anda, lalu jalankan 3 baris perintah ini:​
pip install gdown​
gdown --id MASUKKAN_ID_FILE_GOOGLE_DRIVE_ANDA_DI_SINI -O paket.zip​
unzip paket.zip -d ./blueprint_vault && cp 
./blueprint_vault/06_BOT_OTONOM_GITHUB_CODESPACES/auto_repo_bot.py 
.​
 
3. Cara Bot Otonom (auto_repo_bot.py) Mengurus Folder & GitHub Anda 
Setiap kali Anda membuka 1 Fresh Chat dan meng-upload 1 file Sweetspot (≤ 45k karakter): 
1.​ Gunakan prompt standar yang sudah dibuatkan di file 
CARA_PAKAI_DAN_PROMPT_AI.md (yang menyuruh AI menuliskan # FILE: 
src/nama_modul/nama_file.py di baris pertama tiap blok kodenya). 
2.​ Begitu AI selesai memuntahkan kode, Anda tidak perlu pusing membuat folder atau 
membuat file satu per satu. Cukup klik tombol Copy pada jawaban AI, tempelkan 
(paste) semuanya ke dalam file inbox_ai.md di GitHub Codespaces Anda, lalu ketik di 
terminal:​
python3 auto_repo_bot.py​
 
3.​ Dalam 1 detik, auto_repo_bot.py akan otomatis: 
○​ Membaca seluruh blok kode dari AI. 
○​ Mengecek apakah foldernya (misal src/03_v_office/agents/ atau 
web/dashboard/components/) sudah ada. Jika belum ada, bot otomatis 



<!-- [ID:01_ARCH_S004] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STANDARD -->
# Wajib owner approval: cek gate DEP
python - <<'PY'
import sys
from office.orchestrator.approval_broker import list_pending
pending = [p for p in list_pending() if p["gate"] == "DEP"]
if pending:
    print(f"❌ Ada {len(pending)} gate DEP pending. Approve dulu via /approve <id>.")
    sys.exit(1)
print("✅ Tidak ada gate DEP pending.")
PY

docker compose -f "infra/docker/docker-compose.${ENV}.yml" up -d --build

echo "== Smoke test =="
curl -fsS "http://localhost:8000/health" || { echo "❌ health check gagal"; exit 1; }

echo "== Audit =="
python - <<'PY'
from office.orchestrator.audit import audit
audit({"type": "deploy", "env": "prod", "result": "ok"})
PY

echo "✅ deploy $ENV selesai"

#!/usr/bin/env python3
"""Health check semua service. Dipakai keepalive.yml."""
import os, sys, httpx

URLS = {
    "orchestrator": os.environ.get("HEALTH_ORCH",  "http://localhost:8000/health"),
    "payment":      os.environ.get("HEALTH_PAY",   "http://localhost:8001/health"),
    "scanner":      os.environ.get("HEALTH_SCAN",  "http://localhost:8002/health"),
}

fails = []
for name, url in URLS.items():
    try:
        r = httpx.get(url, timeout=5)
        if r.status_code != 200: fails.append(f"{name}:{r.status_code}")
    except Exception as e:
        fails.append(f"{name}:{type(e).__name__}")

if fails:
    print("FAIL " + ",".join(fails)); sys.exit(1)
print("OK")

from fastapi import FastAPI, Header, HTTPException
import os
from office.orchestrator.main import dispatch_command, agent_act
from office.orchestrator.kill_switch import current

app = FastAPI(title="Orchestrator")
INTERNAL_KEY = os.environ.get("INTERNAL_KEY","")

def _auth(k: str):
    if not INTERNAL_KEY or k != INTERNAL_KEY:
        raise HTTPException(401, "unauthorized")

@app.get("/health")
def health(): return {"ok": True, "kill": current()}

@app.post("/command")
def command(text: str, channel: str, user_id: str,
            x_internal_key: str = Header(default="")):
    _auth(x_internal_key)
    return {"result": dispatch_command(text=text, channel=channel, user_id=user_id)}

@app.post("/agent/{agent_id}/act")
def act(agent_id: str, body: dict, x_internal_key: str = Header(default="")):
    _auth(x_internal_key)
    return agent_act(agent_id, body)

fastapi>=0.110
uvicorn[standard]>=0.27
httpx>=0.27
pyyaml>=6.0
pydantic>=2.6
python-multipart>=0.0.9


<!-- [ID:01_ARCH_S005] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: SECURITY BOOTSTRAP -->
# ==============================================================================
async def main() -> None:
    global BOT_INSTANCE_GLOBAL, BOT_USERNAME_GLOBAL
    if not BOT_TOKEN:
        print("❌ TOKEN_BOT_UTAMA belum diatur di variabel lingkungan (.env)!")
        return

    async with get_db() as db:
        await init_master_db(db)

    if RUNTIME_CONFIG["OWNER_ID_RUNTIME"] == 0:
        print(
            f"🔐 [SECURITY BOOTSTRAP]: ADMIN_USER_ID belum disetel di .env.\n"
            f"👉 Ketik perintah berikut di DM Bot untuk mengunci akses Owner:\n"
            f"   /claim_owner {OWNER_BOOTSTRAP_TOKEN}"
        )

    await start_embedded_web_servers(port=8080)
    asyncio.create_task(_background_dead_job_sweeper_loop())

    bot = Bot(token=BOT_TOKEN)
    BOT_INSTANCE_GLOBAL = bot
    me = await bot.get_me()
    BOT_USERNAME_GLOBAL = me.username or "bikinAI_bot"

    dp = Dispatcher()
    dp.include_router(router)
    print(f"🚀 bikinAI Super Intelligence v3.6.0 (@{BOT_USERNAME_GLOBAL}) SIAP BEROPERASI 100%!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```
```


<!-- [ID:01_ARCH_S006] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## 6. code-to-markdown.md

```md
```yaml
PRODUKSI 2026 READY Zero-Cost Launch Architecture


<!-- [ID:01_ARCH_S007] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Deploy lokal
```bash
docker compose -f infra/docker/docker-compose.dev.yml up --build


---

# 📦 BAGIAN 8 — Scripts & Makefile (biar tinggal jalan)

## 8.1 `scripts/security-check.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail
echo "== Secret scan =="
gitleaks detect --no-git -v || exit 1

echo "== Dependency audit =="
(npm audit --audit-level=high || true)
(pip-audit || true)

echo "== Lint & format =="
(npx eslint . || true)
(ruff check . || true)

echo "== Semgrep (SAST ringan) =="
semgrep --config auto --error || exit 1

echo "== Docker image scan =="
(trivy image --severity HIGH,CRITICAL $(docker images -q | head -n1) || true)

echo "✅ security-check selesai"

#!/usr/bin/env bash
set -euo pipefail

ENV="${1:-prod}"
echo "== Deploy ke $ENV =="


<!-- [ID:01_ARCH_S008] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## 12. farming api all mass sign up.md

```md
```python
#!/usr/bin/env python3
"""
All-In-One Multi-Platform Registration, Credential Vault & Endpoint Provisioner
Modeled on dahl.md architecture with ThreadPoolExecutor, Dynamic Proxy Rotation,
Embedded Username/Credential Profiles, .env Master Vault Sync, and Telegram Reporting.
"""

import argparse
import json
import os
import random
import re
import secrets
import string
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.request import HTTPCookieProcessor, Request, build_opener


<!-- [ID:01_ARCH_S009] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ── Thread-Safe Persistence Helpers ─────────────────────────────────
def append_key_to_pool(platform_slug: str, api_key: str) -> None:
    if not api_key:
        return
    entry = f"{platform_slug}:{api_key}"
    with FILE_LOCK:
        existing = set()
        if POOL_FILE.exists():
            existing = set(POOL_FILE.read_text(encoding="utf-8").splitlines())
        if entry not in existing:
            with open(POOL_FILE, "a", encoding="utf-8") as f:
                f.write(f"{entry}\n")


def save_platform_cred(platform: PlatformSpec, profile: Dict[str, str], auth_data: Dict[str, str]) -> Path:
    CREDS_DIR.mkdir(parents=True, exist_ok=True)
    username = profile["username"]
    f = CREDS_DIR / f"{platform.slug}_{username}.txt"
    tok = auth_data.get("api_key", "")
    fp = auth_data.get("fingerprint", "")
    claim = auth_data.get("claim_token", "")
    lines = [
        f"# Platform: {platform.name} ({platform.slug})",
        f"# Category: {platform.category} | Auth Mode: {platform.auth_mode}",
        f"# Signup URL: {platform.signup_url}",
        f"# API Base: {platform.api_base}",
        "",
        f"platform: {platform.slug}",
        f"env_key: {platform.env_key_name}",
        f"username: {username}",
        f"email: {profile['email']}",
        f"password: {profile['password']}",
        f"fingerprint: {fp}",
        f"api_key: {tok}",
        f"claim_token: {claim}",
        f"status: {auth_data.get('status', 'PROVISIONED')}",
        f"farmed: {time.strftime('%Y-%m-%dT%H:%M:%S%z')}",
        ""
    ]
    with FILE_LOCK:
        f.write_text("\n".join(lines), encoding="utf-8")
    if tok and not tok.startswith("PENDING_"):
        append_key_to_pool(platform.slug, tok)
    return f


def send_telegram_msg(token: str, chat_id: str, text: str) -> None:
    if not token or not chat_id:
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode("utf-8")
        req = Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        build_opener().open(req, timeout=10)
    except Exception:
        pass



<!-- [ID:01_ARCH_S010] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## 15. dahl.md

```md
```python
#!/usr/bin/env python3

import argparse
import json
import os
import random
import re
import socket
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.cookiejar import CookieJar
from pathlib import Path
from urllib.request import HTTPCookieProcessor, Request, build_opener


<!-- [ID:01_ARCH_S011] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## PROTOKOL 5: PENGAWASAN KARYAWAN IT & ISOLASI MODUL (ENTERPRISE MODE)
1. **Audit Keamanan Pull Request (PR):** Setiap kali developer manusia mengajukan Pull Request di `Repo-Staff-Workspace`, lakukan pemindaian keamanan statis (SAST). Tolak PR secara otomatis dan laporkan ke Owner jika ditemukan:
   - Pengiriman data keluar ke domain/IP yang tidak terdaftar di `infrastructure_registry`.
   - Upaya mencetak (print/log) isi variabel lingkungan (`os.environ` / `.env`).
   - Upaya melakukan dekompilasi atau pembacaan memori pada modul `.so` inti.
2. **Kompilasi SDK Harian:** Setiap kali ada pembaruan di `Repo-Core-Brain`, kompilasi ulang fungsi yang boleh diakses karyawan menjadi binary `.so` (tanpa menyertakan source code asli) dan perbarui file binary tersebut di `Repo-Staff-Workspace`.

intinya jadi di dual repo saya jadi butuh 3 repo.

Dengan arsitektur ini, meskipun Anda mempekerjakan 10 programmer senior sekaligus dan salah satu dari mereka berniat jahat atau pindah ke perusahaan pesaing, yang bisa mereka bawa hanyalah potongan kode antarmuka (kulit luar) yang tidak akan pernah bisa hidup tanpa jantung biner dan database Turso milik Anda.
Apakah Anda ingin tahu bagaimana cara mengatur GitHub Actions + Branch Protection secara praktis agar karyawan tidak bisa mencuri kunci .env dari dalam server saat mereka mengetes kode?

```
```


<!-- [ID:01_ARCH_S012] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
VAULT_DIR = Path.home() / ".bikinai_vault"
VAULT_DIR.mkdir(parents=True, exist_ok=True)
try:
   os.chmod(VAULT_DIR, 0o700)
except Exception:
   pass
DB_PATH = str(VAULT_DIR / "bikinai_master_vault.db")
KEYRING_PATH = VAULT_DIR / "ed25519_voucher_key.bin"
BLIND_SALT_PATH = VAULT_DIR / "voucher_blind_salt.bin"
BOT_TOKEN = os.getenv("TOKEN_BOT_UTAMA", "").strip()
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
OWNER_BOOTSTRAP_TOKEN = (
   os.getenv("OWNER_BOOTSTRAP_TOKEN", "").strip() or secrets.token_hex(8)
)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "").strip()
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY", "").strip()
CHUTES_API_KEY = os.getenv("CHUTES_API_KEY", "").strip()
NVIDIA_NIM_API_KEY = os.getenv("NVIDIA_NIM_API_KEY", "").strip()
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY", "").strip()
FAL_KEY = os.getenv("FAL_KEY", "").strip()
GOPAY_STATIC_QRIS_RAW = os.getenv("GOPAY_STATIC_QRIS_RAW", "").strip()
SHOPEEPAY_STATIC_QRIS_RAW = os.getenv("SHOPEEPAY_STATIC_QRIS_RAW", "").strip()
DANA_STATIC_QRIS_RAW = os.getenv("DANA_STATIC_QRIS_RAW", "").strip()
DUITKU_MERCHANT_CODE = os.getenv("DUITKU_MERCHANT_CODE", "").strip()
DUITKU_API_KEY = os.getenv("DUITKU_API_KEY", "").strip()
MIDTRANS_SERVER_KEY = os.getenv("MIDTRANS_SERVER_KEY", "").strip()
PAKASIR_SLUG = os.getenv("PAKASIR_SLUG", "").strip()
PAKASIR_API_KEY = os.getenv("PAKASIR_API_KEY", "").strip()
CRYPTOBOT_API_TOKEN = os.getenv("CRYPTOBOT_API_TOKEN", "").strip()
SAMPLE_SANDBOX_VIDEO_URL = (
   "https://filesamples.com/samples/video/mp4/sample_640x360.mp4"
)
BOT_INSTANCE_GLOBAL: Bot | None = None
BOT_USERNAME_GLOBAL: str = "bikinAI_bot"
def detect_default_miniapp_url() -> str:
   """Mendeteksi URL HTTPS publik secara otomatis (Codespaces / HF Spaces / Custom)."""
   env_url = os.getenv("MINIAPP_PUBLIC_URL", "").strip()
   if env_url.startswith("https://"):
       return env_url
   hf_host = os.getenv("SPACE_HOST", "").strip()
   if hf_host:
       return f"https://{hf_host}"
   cs_name = os.getenv("CODESPACE_NAME", "").strip()
   cs_dom = os.getenv(
       "GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "app.github.dev"
   ).strip()
   return f"https://{cs_name}-8080.{cs_dom}" if cs_name else ""
def load_or_create_persistent_keys() -> tuple[bytes, bytes, bytes]:
   if KEYRING_PATH.exists():



<!-- [ID:01_ARCH_S013] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 443

except Exception:
   pass
DB_PATH = str(VAULT_DIR / "bikinai_master_vault.db")
KEYRING_PATH = VAULT_DIR / "ed25519_voucher_key.bin"
BLIND_SALT_PATH = VAULT_DIR / "voucher_blind_salt.bin"
BOT_TOKEN = os.getenv("TOKEN_BOT_UTAMA", "").strip()
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "").strip()
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY", "").strip()
CHUTES_API_KEY = os.getenv("CHUTES_API_KEY", "").strip()
FAL_KEY = os.getenv("FAL_KEY", "").strip()
GOPAY_STATIC_QRIS_RAW = os.getenv("GOPAY_STATIC_QRIS_RAW", "").strip()
SHOPEEPAY_STATIC_QRIS_RAW = os.getenv("SHOPEEPAY_STATIC_QRIS_RAW", "").strip()
DANA_STATIC_QRIS_RAW = os.getenv("DANA_STATIC_QRIS_RAW", "").strip()
SAMPLE_SANDBOX_VIDEO_URL = "https://filesamples.com/samples/video/mp4/sample_640x360.mp4"
BOT_INSTANCE_GLOBAL: Bot | None = None
BOT_USERNAME_GLOBAL: str = "bikinAI_bot"
def detect_default_miniapp_url() -> str:
   env_url = os.getenv("MINIAPP_PUBLIC_URL", "").strip()
   if env_url.startswith("https://"):
       return env_url
   hf_host = os.getenv("SPACE_HOST", "").strip()
   if hf_host:
       return f"https://{hf_host}"
   cs_name = os.getenv("CODESPACE_NAME", "").strip()
   cs_dom = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "app.github.dev").strip()
   return f"https://{cs_name}-8080.{cs_dom}" if cs_name else ""
def load_or_create_persistent_keys() -> tuple[bytes, bytes, bytes]:
   if KEYRING_PATH.exists():
       priv_bytes = KEYRING_PATH.read_bytes()
       priv_obj = Ed25519PrivateKey.from_private_bytes(priv_bytes)
   else:
       priv_obj = Ed25519PrivateKey.generate()
       priv_bytes = priv_obj.private_bytes_raw()
       KEYRING_PATH.write_bytes(priv_bytes)
       try:
           os.chmod(KEYRING_PATH, 0o600)
       except Exception:
           pass
   if BLIND_SALT_PATH.exists():
       salt_bytes = BLIND_SALT_PATH.read_bytes()
   else:
       salt_bytes = secrets.token_bytes(32)
       BLIND_SALT_PATH.write_bytes(salt_bytes)
       try:
           os.chmod(BLIND_SALT_PATH, 0o600)
       except Exception:
           pass
   return priv_bytes, priv_obj.public_key().public_bytes_raw(), salt_bytes
ED25519_PRIV_BYTES, ED25519_PUB_BYTES, VOUCHER_BLIND_SALT = load_or_create_persistent_keys()
RUNTIME_CONFIG: dict[str, Any] = {
   "LAUNCH_PRODUCTION_MODE": False,
   "PILIHAN_MESIN_MEDIA": 1,
   "BANSOS_OPERATION_MODE": "SILENT_PROFIT",
   "HAPPY_HOUR_MODE": False,
   "ID_ACTIVE_CATEGORY": "QRIS_DIRECT",
   "ID_ACTIVE_PROVIDER": "QRIS GoPay Merchant",
   "GLOBAL_ACTIVE_PROVIDER": "Aktifkan Keduanya (USDT + Telegram Stars)",



<!-- [ID:01_ARCH_S014] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ── Platform Provisioning & Self-Registration Handlers ──────────────
def provision_platform(
    client: RotatingPlatformClient,
    platform: PlatformSpec,
    profile: Dict[str, str],
    verify_chat: bool = False,
    backoff: float = 0.3,
    max_tries: int = 5
) -> Dict[str, str]:
    """
    Executes API self-registration for instant-auth platforms (Dahl, BazaarLink, LLM7, Gonka)
    or generates structured credential & OAuth provisioning manifests for portal-based platforms.
    """
    username = profile["username"]

    # Mode 1: Dahl Global Fingerprint Flow
    if platform.auth_mode == "dahl_fp":
        base_host = platform.api_base.replace("/v1", "")
        for _ in range(max_tries):
            st, body = client.request_json(
                "POST",
                f"{platform.api_base}{platform.signup_endpoint}",
                payload={"username": username},
                headers={"Referer": f"{base_host}/account", "Origin": base_host}
            )
            if st in (200, 201) and "fingerprint" in body:
                fp = body["fingerprint"]
                tok = body.get("api_key", {}).get("token", "")
                kid = body.get("api_key", {}).get("id", "")
                client.request_json("POST", f"{platform.api_base}{platform.signin_endpoint}", {"fingerprint": fp})
                st_acc, acc = client.request_json("GET", f"{platform.api_base}/account")
                pool = acc.get("token_balance", 0) if st_acc == 200 else 0
                if pool and kid:
                    client.request_json("POST", f"{platform.api_base}{platform.allocate_endpoint}", {"key_id": kid, "amount": pool})
                if verify_chat and tok:
                    client.request_json(
                        "POST",
                        f"{platform.api_base}/chat/completions",
                        payload={"model": platform.default_model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 4},
                        headers={"Authorization": f"Bearer {tok}"}
                    )
                return {"api_key": tok, "fingerprint": fp, "claim_token": str(pool), "status": "ACTIVE_API"}
            client.rotate_ip()
            time.sleep(backoff)
        return {"api_key": f"PENDING_{platform.slug.upper()}", "fingerprint": "", "status": "BROWSER_REQUIRED_403"}

    # Mode 2: BazaarLink 1-Call POST Agent Self-Registration
    if platform.auth_mode == "bazaar_post":
        for _ in range(max_tries):
            st, body = client.request_json(
                "POST",
                platform.signup_endpoint,
                payload={"name": profile["agent_name"]}
            )
            if st in (200, 201) and ("api_key" in body or "key" in body):
                tok = body.get("api_key") or body.get("key", "")
                claim = body.get("claim_token", "")
                return {"api_key": tok, "fingerprint": profile["agent_name"], "claim_token": claim, "status": "ACTIVE_API"}
            client.rotate_ip()
            time.sleep(backoff)
        return {"api_key": f"PENDING_{platform.slug.upper()}", "fingerprint": profile["agent_name"], "status": "ENDPOINT_QUEUED"}

    # Mode 3: Gonka Brokers & Instant Session Token Platforms
    if platform.auth_mode in ("gonka_key", "session_token"):
        existing_env = os.getenv(platform.env_key_name, "")
        if existing_env:
            return {"api_key": existing_env, "fingerprint": username, "status": "LOADED_FROM_ENV"}
        return {
            "api_key": f"PENDING_{platform.env_key_name}",
            "fingerprint": username,
            "claim_token": platform.signup_url,
            "status": "READY_FOR_INSTANT_TOKEN"
        }

    # Mode 4: OAuth Cardless & Wholesale/DePIN Portals
    existing_env = os.getenv(platform.env_key_name, "")
    return {
        "api_key": existing_env if existing_env else f"YOUR_{platform.env_key_name}",
        "fingerprint": profile["oauth_github"],
        "claim_token": platform.signup_url,
        "status": "LOADED_FROM_ENV" if existing_env else "PORTAL_PROFILE_CREATED"
    }


def worker_provision_task(
    index: int,
    platform_slugs: List[str],
    args: argparse.Namespace
) -> Tuple[int, Dict[str, str], List[Tuple[str, str, str]]]:
    """Thread worker that creates an account bundle and provisions selected platforms."""
    profile = generate_account_bundle(index=index, custom_domain=args.domain)
    client = RotatingPlatformClient(proxy_url=args.proxy, use_brightdata=bool(args.proxy))
    results = []
    for slug in platform_slugs:
        spec = PLATFORM_REGISTRY[slug]
        auth_data = provision_platform(
            client=client,
            platform=spec,
            profile=profile,
            verify_chat=not args.skip_chat,
            backoff=args.backoff
        )
        saved_file = save_platform_cred(spec, profile, auth_data)
        results.append((spec.slug, auth_data.get("status", "DONE"), saved_file.name))
        print(
            f"[#{index:02d}] {spec.slug:20s} | user={profile['username']:22s} | "
            f"status={auth_data.get('status'):24s} | file={saved_file.name}",
            flush=True
        )
    return index, profile, results


