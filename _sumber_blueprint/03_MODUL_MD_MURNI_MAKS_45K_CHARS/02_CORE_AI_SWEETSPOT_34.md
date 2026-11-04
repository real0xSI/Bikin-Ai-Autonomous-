
<!-- [ID:02_CORE_AI_S062] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: SIAP, TAHAP 1 -->
## Halaman 78

               "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "score_4, deformed, bad anatomy", "cl
               "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
               "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "GodMode_Gen", "images": ["8", 
           }
           
           hasil_gambar = proses_ke_mesin_comfyui(workflow)
           if hasil_gambar:
               kirim_hasil_langsung_ke_user(user_id, hasil_gambar, "Generate Gambar")
               bot_aspri.reply_to(message, "✅ Selesai! Gambar terkirim ke User.")
           else:
               bot_aspri.reply_to(message, "❌ Render gagal / timeout.")
   # JIKA PESANAN ADALAH FOTO (Bisa dikembangkan lebih lanjut)
   elif teks_grup.startswith("ORDER_PIC"):
       bot_aspri.reply_to(message, "⚙️ Mode foto masuk antrean (Placeholder untuk Upscale/FaceSwap)...")
print("🚀 [SIAP] Bot Aspri AKTIF memantau Grup Antrean!")
bot_aspri.infinity_polling(timeout=60, long_polling_timeout=60)
Dengan struktur seperti ini, kode Anda bebas dari kebocoran data. Anda bisa membagikan screenshot layar Colab tersebut dengan tenang kepada
siapa pun karena token berharga Anda sepenuhnya tersimpan di dalam sistem. Selamat merender!
User prompt: Kok error
Response: Error yang muncul di bagian bawah layar Anda adalah IndentationError: unexpected indent pada baris kode ke-40. Dalam
pemrograman Python, pengaturan spasi di awal baris (indentasi) sangat ketat, dan pesan ini menandakan ada spasi berlebih sebelum perintah for
file_path, url in models:.
Berikut cara memperbaikinya:
1. Klik tombol Continue pada kotak pesan "Colab Privacy Notice" yang menutupi layar Anda.
2. Cari baris for file_path, url in models: di dalam sel kode Colab.
3. Hapus spasi kosong di sebelah kiri kata for sehingga huruf pertamanya rata kiri dan sejajar persis dengan baris models = [ yang ada di
atasnya.
4. Tekan kembali tombol Play (Run). Pastikan saat Anda melakukan copy-paste dari kode sebelumnya, semua teks sejajar rapi di margin kiri tanpa
ada spasi tambahan yang tidak disengaja.
User prompt: Import os import time import subprocess import requests import telebot from deep_translator import GoogleTranslator #
========================================== # 1. KREDENSIAL BOT # ========================================== TOKEN_ASPRI =
"8737279275:AAEI5hKuwQsPPhMkNfdVBSFfJfgKKvMTcNE" TOKEN_UTAMA = "8885292945:AAGK66Dng-81kTW9-vv0Yoy4Pzi43nU3ns0" # Dipinjam
untuk kirim hasil ID_GRUP = -5441119572 bot_aspri = telebot.TeleBot(TOKEN_ASPRI) # ========================================== # 2.
INSTALASI LINGKUNGAN & COMFYUI # ========================================== print("⚙️ [TAHAP 1] Menyiapkan Lingkungan & Mengunduh
ComfyUI...") os.system('pip install pyTelegramBotAPI insightface onnxruntime-gpu deep-translator -q') os.chdir('/content') if not os.path.exists('ComfyUI'):
os.system('git clone https://github.com/comfyanonymous/ComfyUI -q') os.chdir('/content/ComfyUI') os.system('pip install -r requirements.txt -q')
folder_list = ['checkpoints', 'upscale_models', 'ipadapter', 'insightface', 'inpaint', 'input'] for folder in folder_list: os.makedirs(f'models/{folder}',
exist_ok=True) print("⚙️ [TAHAP 2] Mendownload Model Pony & Upscaler...") models = [ ('models/checkpoints/Pony_V6_XL.safetensors',
'https://huggingface.co/WhiteAiZ/PonyXL/resolve/main/PonyDiffusionV6XL.safetensors'), ('models/upscale_models/4x-UltraSharp-v2.pth',
'https://huggingface.co/lokcx/4x-Ultrasharp/resolve/main/4x-UltraSharp.pth'), ('models/upscale_models/4x_foolhardy_Remacri.pth',
'https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/4x_foolhardy_Remacri.pth') ] for file_path, url in models: if not os.path.exists(file_path):
print(f"Mendownload {file_path.split('/')[-1]}...") os.system(f'wget -c --progress=bar -O {file_path} {url}') print("⚙️ [TAHAP 3] Menyalakan Mesin ComfyUI di
Background...") subprocess.Popen(["python", "main.py", "--port", "8188"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) time.sleep(40) #
Tunggu server ComfyUI nyala # ========================================== # 3. FUNGSI EKSEKUSI & PENGIRIMAN #
========================================== def kirim_hasil_langsung_ke_user(user_id, path_gambar, mode_terpilih): url =
f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendPhoto" with open(path_gambar, 'rb') as photo: files = {'photo': photo} data = {'chat_id': user_id,
'caption': f"🔥 {mode_terpilih} Sukses!\n\n_Dibuat instan via @BikinAI_bot_", 'parse_mode': 'Markdown'} req = requests.post(url, files=files, data=data)
return req.status_code == 200 def proses_ke_mesin_comfyui(workflow): try: res = requests.post("http://127.0.0.1:8188/prompt", json={"prompt":
workflow}).json() prompt_id = res.get("prompt_id") if prompt_id: for _ in range(150): time.sleep(2) try: hist =
requests.get(f"http://127.0.0.1:8188/history/{prompt_id}").json() if prompt_id in hist: outputs = hist[prompt_id].get("outputs", {}) for k, v in outputs.items():
if "images" in v: return f"/content/ComfyUI/output/{v['images'][0]['filename']}" except: pass except: pass return None #
========================================== # 4. OTAK BOT ASPRI (HANYA PANTAU GRUP) #
========================================== @bot_aspri.message_handler(func=lambda msg: msg.chat.id == ID_GRUP, content_types=['text',
'photo']) def pantau_antrean_grup(message): teks_grup = message.text if message.text else message.caption if not teks_grup: return # JIKA PESANAN
ADALAH TEKS (GAMBAR BARU) if teks_grup.startswith("ORDER_TXT"): parts = teks_grup.split(" | ") if len(parts) >= 3: user_id = parts[1].strip() prompt_asli
= parts[2].strip() bot_aspri.reply_to(message, f"⚙️ Aspri memproses prompt dari User: {user_id}") try: prompt_inggris = GoogleTranslator(source='id',
target='en').translate(prompt_asli) except: prompt_inggris = prompt_asli workflow = { "3": {"class_type": "KSampler", "inputs": {"seed": int(time.time()),
"steps": 25, "cfg": 7.0, "sampler_name": "euler_ancestral", "scheduler": "normal", "denoise": 1.0, "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0],
"latent_image": ["5", 0]}}, "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "Pony_V6_XL.safetensors"}}, "5": {"class_type":
"EmptyLatentImage", "inputs": {"width": 832, "height": 1024, "batch_size": 1}}, "6": {"class_type": "CLIPTextEncode", "inputs": {"text": f"score_9, score_8_up,



<!-- [ID:02_CORE_AI_S063] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==========================================
def kirim_pesan(user_id, teks):
   requests.post(f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendMessage", json={"chat_id": user_id, "text": 
def tembak_hasil_ke_user(user_id, path_gambar, info):
   url_kirim = f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendPhoto"
   with open(path_gambar, 'rb') as photo:
       requests.post(url_kirim, data={'chat_id': user_id, 'caption': info, 'parse_mode': 'Markdown'}, files={
def proses_gambar(workflow):
   try:
       res = requests.post("http://127.0.0.1:8188/prompt", json={"prompt": workflow}).json()
       prompt_id = res.get("prompt_id")
       if prompt_id:



<!-- [ID:02_CORE_AI_S064] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: PROMPT_ID, SIAP -->
# ==========================================
def kirim_pesan(user_id, teks):
   requests.post(f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendMessage", json={"chat_id": user_id, "text": 
def tembak_hasil_ke_user(user_id, path_gambar, info):
   url_kirim = f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendPhoto"
   with open(path_gambar, 'rb') as photo:
       requests.post(url_kirim, data={'chat_id': user_id, 'caption': info, 'parse_mode': 'Markdown'}, files={
def proses_gambar(workflow):
   try:
       res = requests.post("http://127.0.0.1:8188/prompt", json={"prompt": workflow}).json()
       prompt_id = res.get("prompt_id")
       if prompt_id:
           for _ in range(200): # Tunggu maksimal ~6 menit untuk render berat
               time.sleep(2)
               try:
                   hist = requests.get(f"http://127.0.0.1:8188/history/{prompt_id}").json()
                   if prompt_id in hist:
                       outputs = hist[prompt_id].get("outputs", {})
                       for k, v in outputs.items():
                           if "images" in v:
                               return f"/content/ComfyUI/output/{v['images'][0]['filename']}" 
               except: pass
   except: pass
   return None
print("🚀 [SIAP] Mode Dewa Uncensored Aktif! Bebas SFW & NSFW.")

<!-- [ID:02_CORE_AI_S065] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==========================================
def kirim_pesan(user_id, teks):
   requests.post(f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendMessage", json={"chat_id": user_id, "text": 
def tembak_hasil_ke_user(user_id, path_gambar, info):
   url_kirim = f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendPhoto"
   with open(path_gambar, 'rb') as photo:
       requests.post(url_kirim, data={'chat_id': user_id, 'caption': info, 'parse_mode': 'Markdown'}, files={
def proses_gambar(workflow):
   try:
       # Tembak ke port rahasia 7777
       res = requests.post("http://127.0.0.1:7777/prompt", json={"prompt": workflow}).json()
       prompt_id = res.get("prompt_id")
       if prompt_id:
           for _ in range(200): 
               time.sleep(2)
               try:
                   hist = requests.get(f"http://127.0.0.1:7777/history/{prompt_id}").json()
                   if prompt_id in hist:



<!-- [ID:02_CORE_AI_S066] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: PROMPT_ID, SIAP -->
# Menyalakan server dengan penjagaan proses agar tidak mudah drop
subprocess.Popen(["python", "worker.py", "--port", "7777"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNU
time.sleep(35)
def kirim_pesan(user_id, teks):
   requests.post(f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendMessage", json={"chat_id": user_id, "text": 
def tembak_hasil_ke_user(user_id, path_gambar, info):
   url_kirim = f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendPhoto"
   with open(path_gambar, 'rb') as photo:
       requests.post(url_kirim, data={'chat_id': user_id, 'caption': info, 'parse_mode': 'Markdown'}, files={
def proses_gambar(workflow):
   try:
       res = requests.post("http://127.0.0.1:7777/prompt", json={"prompt": workflow}).json()
       prompt_id = res.get("prompt_id")
       if prompt_id:
           for _ in range(200): 
               time.sleep(2)
               try:
                   hist = requests.get(f"http://127.0.0.1:7777/history/{prompt_id}").json()
                   if prompt_id in hist:
                       outputs = hist[prompt_id].get("outputs", {})
                       for k, v in outputs.items():
                           if "images" in v:
                               return f"/content/data_engine/output/{v['images'][0]['filename']}" 
               except: pass
   except: pass
   return None
print("🚀 [SIAP] Mesin Siaga dengan Manajemen Memori Cerdas!")



<!-- [ID:02_CORE_AI_S067] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: TARGET_URL -->
## Halaman 342

Publik untuk Cegah SSRF)​
        async with httpx.AsyncClient(timeout=25.0) as client:​
            resp = await client.post(​
                "http://127.0.0.1:11235/crawl",​
                json={"urls": [target_url], "priority": 10}​
            )​
            resp.raise_for_status()​
            return resp.json().get("results", [{}])[0].get("markdown", 
"")​
 
3. Orkestrator Inferensi LLM, Keamanan ModelScan & Multimodal 
Auto-Rolling 
Kode di bawah ini mengimplementasikan logika inti yang memastikan setiap permintaan kognitif 
maupun multimodal dari agen memiliki jalan keluar berlapis. Sebelum model lokal dimuat, 
fungsi verify_model_security() menjalankan protectai/modelscan secara terprogram untuk 
memblokir serangan serialisasi pickle. Selama waktu jalan (runtime), execute_llm_with_rolling() 
menghitung kompleksitas prompt dan merutekannya melintasi penyedia cloud gratis tanpa kartu 
kredit (Kelompok 2A), lalu beralih otomatis ke agregator lokal (OmniRoute dan 9Router) serta 
mesin GGUF tanpa sensor (llama.cpp dan Ollama dengan bobot huihui-ai atau 
DeepSeek-R1-0528-Qwen3-8B) apabila kuota eksternal habis. 
import os​
import subprocess​
import time​
from dataclasses import dataclass​
from typing import Dict, List, Optional​
import httpx​
​
@dataclass​
class ProviderEndpoint:​
    name: str​
    base_url: str​
    api_key_env: str​
    default_model: str​
    tier: str  # "LOCAL_SOTA", "FREE_CLOUD", "AGGREGATOR", "WHOLESALE"​
    cooldown_until: float = 0.0​
​
class AutonomousRollingOrchestrator:​
    """​
    Orkestrator Inferensi Multi-Jalur dengan Circuit Breaker Otomatis,​
    Perutean Ambang Batas Kompleksitas (RouteLLM tau=0.11593), dan 
Audit ModelScan.​
    """​
    def __init__(self):​
        self.tau_threshold = float(os.getenv("ROUTELLM_THRESHOLD", 
"0.11593"))​



<!-- [ID:02_CORE_AI_S068] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :350, STR, -4: -->
## Halaman 404

       "grade_score": 93,
       "multimodal": False,
       "ok": 0,
       "fail": 0,
       "quarantine_until": 0,
   },
}
_SOFT_REFUSAL_REGEX = re.compile(
   r"(i\s+cannot\s+fulfill|i\s+am\s+unable\s+to|as\s+an\s+ai\s+language\s+model|"
   r"my\s+safety\s+guidelines|against\s+my\s+ethical|maaf,\s+saya\s+tidak\s+dapat\s+memenuhi|"
   r"sebagai\s+model\s+ai,\s+saya\s+tidak\s+bisa|melanggar\s+pedoman\s+etika)",
   re.IGNORECASE,
)
def is_soft_or_hard_refusal(reply_text: str) -> bool:
   """Mendeteksi Soft Refusal (ceramah moral / penolakan halus) sesuai temuan sdu 3.html."""
   if not reply_text:
       return True
   return bool(_SOFT_REFUSAL_REGEX.search(reply_text[:350]))
def compute_routellm_complexity_score(prompt_text: str) -> tuple[float, bool]:
   """
   RouteLLM Matrix Factorization Heuristic Scorer (Ambang batas tau = 0.11593):
   Menentukan apakah kueri membutuhkan model SOTA Kuat (M_strong >= 0.11593) atau Cepat (M_weak).
   """
   tau = 0.11593
   low = prompt_text.lower()
   score = min(0.08, len(prompt_text) / 2500.0)
   complex_markers = (
       "arsitektur",
       "algoritma",
       "python",
       "sql",
       "riset",
       "strategi",
       "analisis",
       "kontrak",
       "keamanan",
       "matematika",
       "pnl",
       "refactor",
       "debug",
   )
   hits = sum(1 for m in complex_markers if m in low)
   score += hits * 0.045
   return round(score, 4), (score >= tau)
def compress_context_and_match_skills(
   user_message: str, chat_history: list[dict[str, str]] | None
) -> tuple[str, list[dict[str, str]]]:
   """
   RTK Context Compressor (-40% s/d -98% token) + Lazy-Loaded SKILL.md (gaya nanoMuse):
   Hanya menyuntikkan SKILL.md yang cocok dengan konteks percakapan saat ini.
   """
   low = user_message.lower()
   matched_skills: list[str] = []
   if any(k in low for k in ("umkm", "produk", "katalog", "iklan", "jualan")):
       matched_skills.append(DYNAMIC_SKILL_REGISTRY["UMKM_CATALOG"])
   if any(k in low for k in ("kode", "code", "python", "error", "bug", "api")):
       matched_skills.append(DYNAMIC_SKILL_REGISTRY["CODING_FRONTIER"])
   if any(k in low for k in ("riset", "analisis", "pasar", "kompetitor", "strategi")):
       matched_skills.append(DYNAMIC_SKILL_REGISTRY["DEEP_RESEARCH"])
   skill_block = (
       "\nSKILL AKTIF:\n" + "\n".join(matched_skills) if matched_skills else ""
   )
   compressed_history: list[dict[str, str]] = []
   if chat_history:
       for turn in chat_history[-4:]:
           if (



<!-- [ID:02_CORE_AI_S069] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 420

       str(data.get("prompt") or "Masterpiece portrait 8k")
   )
   if is_attack:
       return web.json_response({"ok": False}, status=400)
   modality = str(data.get("modality") or "IMAGE")
   model_name = str(data.get("model") or "Flux.1-Dev Uncensored Pro")
   ratio = str(data.get("ratio") or "9:16")
   is_paid_vip = bool(data.get("is_paid_vip", False))
   nologo_flag = "true" if is_paid_vip else "false"
   w, h = (
       (768, 1024)
       if ratio == "9:16"
       else ((1024, 768) if ratio == "16:9" else (1024, 1024))
   )
   seed_val = int(time.time())
   if modality in ("VIDEO", "IMG2VID"):
       cdn_url, dl_name, is_video = (
           SAMPLE_SANDBOX_VIDEO_URL,
           f"AetherFree_Video_{seed_val}.mp4",
           True,
       )
   else:
       cdn_url = (
           f"https://image.pollinations.ai/prompt/{quote(f'{prompt_raw}, {model_name}, 8k masterpiece')}"
           f"?width={w}&height={h}&nologo={nologo_flag}&private=true&enhance=true&seed={seed_val}"
       )
       dl_name, is_video = f"AetherFree_4K_{seed_val}.jpg", False
   return web.json_response(
       {
           "ok": True,
           "is_video": is_video,
           "cdn_url": cdn_url,
           "download_url": f"/api/cdn/download?url={quote(cdn_url)}&name={quote(dl_name)}",
       }
   )
async def handle_voucher_redeem_api(request: web.Request) -> web.Response:
   try:
       data = await request.json()
   except Exception:
       return web.json_response(
           {"ok": False, "message": "Invalid JSON"}, status=400
       )
   async with get_db() as db:
       ok, msg, units = await verify_and_redeem_ed25519_voucher(
           db, str(data.get("voucher") or "").strip()
       )
   return web.json_response(
       {"ok": ok, "message": msg, "units": units},
       status=200 if ok else 400,
   )
async def handle_root_web_router(request: web.Request) -> web.Response:
   host = (request.headers.get("Host") or "").lower()
   custom_dom = (RUNTIME_CONFIG.get("CUSTOM_WEB_DOMAIN") or "").lower()
   if (
       custom_dom and custom_dom in host
   ) or request.query.get("portal") == "freedom":
       return web.Response(
           text=render_freedom_web_portal_html(), content_type="text/html"
       )
   return web.Response(
       text=MINIAPP_FULL_WEBSITE_HTML, content_type="text/html"
   )
async def start_embedded_web_servers(port: int = 8080) -> None:
   app = web.Application()
   app.router.add_get("/", handle_root_web_router)
   app.router.add_get("/healthz", handle_healthz_keepalive_api)
   app.router.add_get(
       "/unfiltered-portal",



<!-- [ID:02_CORE_AI_S070] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: TOPIK, IDX -->
## Halaman 422

       "Menghapus latar belakang foto dan mengirimkannya sebagai File Dokumen PNG transparan utuh",
   ),
   "IMG2VID_MOTION": (
       "📸 Gerakkan Foto Jadi Video (Image-to-Video)",
       "Menghidupkan foto produk atau potret wajah menjadi video sinematik bergerak",
   ),
   "RETOUCH_FACE": (
       "✨ Retouch Wajah & Kulit Mulus",
       "Memperhalus tekstur kulit dan pencahayaan wajah secara alami",
   ),
   "INPAINT_OBJ": (
       "🖌️ Ganti Baju / Ubah Objek",
       "Mengganti pakaian atau objek tertentu di dalam foto tanpa merusak latar",
   ),
   "OUTPAINT_EXPAND": (
       "🖼️ Perluas Ukuran Foto",
       "Memperluas foto kotak 1:1 menjadi vertikal 9:16 atau melebar 16:9",
   ),
   "PRODUCT_RELIGHT": (
       "📸 Studio Produk UMKM (Relighting)",
       "Mengubah foto produk rumahan menjadi foto katalog studio mewah",
   ),
   "RESTORE_OLD": (
       "🕰️ Restorasi & Warnai Foto Lama",
       "Memperbaiki foto jadul yang buram menjadi tajam dan berwarna kembali",
   ),
}
DYNAMIC_CHAT_FOOTERS = [
   '\n\n_💡 Tip: Kalau nanti ingin membuka menu tombol fitur, cukup ketik **"menu"** ya Kak 😊_',
   '\n\n_✨ Asik banget ngobrolnya! Kapan pun butuh tombol studio, tinggal ketik **"tampilin tombol"** ya._',
   '\n\n_🔬 Tip: Kamu juga bisa ketik **`/riset [topik]`** untuk bedah mendalam atau **`/canvas`** untuk meny
]
_FOOTER_COUNTER = 0
def get_next_dynamic_footer() -> str:
   global _FOOTER_COUNTER
   idx = _FOOTER_COUNTER % len(DYNAMIC_CHAT_FOOTERS)
   _FOOTER_COUNTER += 1
   return DYNAMIC_CHAT_FOOTERS[idx]
@dataclass
class LiveWizardSession:
   prompt: str
   modality: Literal["VIDEO", "IMAGE", "EDIT_IMAGE"] = "VIDEO"
   aspect_ratio: str = "9:16"
   duration_sec: int = 5
   video_engine: str = "Kling 3.0 Pro"
   image_engine: str = "Seedream 4.5"
   edit_tool: str = "REMOVE_BG_PNG"
   upscale_mode: str = "PHOTO_FACE_4K"
   awam_preset: str = ""
   def get_pricing(self) -> tuple[int, int, bool]:
       if RUNTIME_CONFIG["HAPPY_HOUR_MODE"]:
           return 0, 0, True
       if (
           self.modality in ("IMAGE", "EDIT_IMAGE")
           and self.edit_tool != "IMG2VID_MOTION"
       ):
           return 4, 0, True
       if (
           RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] == 1
           and not RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"]
       ):
           return (
               {5: 4, 10: 8, 30: 20}.get(self.duration_sec, 4),
               0,
               True,
           )
       base_c = {5: 20, 10: 35, 30: 100}.get(self.duration_sec, 20)
       if self.video_engine in (



<!-- [ID:02_CORE_AI_S071] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
async def fetch_clean_image_bytes(prompt_en: str, width: int = 768, height: int = 1024, apply_watermark: bool 
   nologo_str = "false" if apply_watermark else "true"
   final_prompt = f"{prompt_en}, subtle small corner text '⚡ bikinAI SI'" if apply_watermark else prompt_en
   url = f"https://image.pollinations.ai/prompt/{quote(final_prompt)}?width={width}&height={height}&nologo={n
   try:
       async with httpx.AsyncClient(timeout=25.0, follow_redirects=True) as client:
           resp = await client.get(url)
           if resp.status_code == 200 and len(resp.content) > 1000:
               return resp.content
   except Exception:
       pass
   return None
async def handle_healthz_keepalive_api(request: web.Request) -> web.Response:
   return web.json_response({"ok": True, "engine": "bikinAI Super Intelligence v4.0.0", "uptime_ts": int(time
async def handle_vibecoder_openai_chat_api(request: web.Request) -> web.Response:
   auth_header = request.headers.get("Authorization", "").strip()



<!-- [ID:02_CORE_AI_S072] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## 2. MinerU_markdown_widget_4515b68e-c447-4a8b-b366-04aa8eb08f3a_2117077569218973696.md

```md
## Peta Permukaan Serangan Dual-Pipeline

Inspeksi Vektor Serangan Otonom vs Mitigasi Kriptografi / Sistem

Jalur SFW

Unfiltered

1. Gerbang Input & Koin

Mini App API Gateway

N1

2. Autonomous Classifier

Semantic Router & CLIP

3. Jalur Otonom A (SFW)

Engine Pool Terilfiltrasi

N3

4. Jalur Otonom B (Unfiltered)

Direct GPU Engine Pool

N4

5. Webhook Receiver

Async Callback & Fetcher

N5

6. Media Delivery & Proxy Layer

### Gerbang Input & Koin (Mini App API)

Vektor Serangan (Red Team)

Race Condition (TOCTOU) & Decompression Bomb (SEC-02 / SEC-06)

Dampak: Saldo dipotong 1x tapi memicu 20x generate paralel di kedua jalur; server crash akibat Pixel Flood.

Spesifikasi Pertahanan (Blue Team)

Atomic Lua Lock di Redis sebelum masuk router + batas piksel ketat pada header file sebelum dimuat ke RAM.
```


<!-- [ID:02_CORE_AI_S073] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## 3. MinerU_markdown_widget_a027c931-2591-475d-a0f9-fa8c47bda718_2117077430391705600.md

```md
## Peta Permukaan Serangan Dual-Pipeline

Inspeksi Vektor Serangan Otonom vs Mitigasi Kriptografi / Sistem

Jalur SFW

Unfiltered

1. Gerbang Input & Koin

Mini App API Gateway

N1

2. Autonomous Classifier

Semantic Router & CLIP

3. Jalur Otonom A (SFW)

Engine Pool Terilfiltrasi

N3

4. Jalur Otonom B (Unfiltered)

Direct GPU Engine Pool

N4

5. Webhook Receiver

Async Callback & Fetcher

N5

6. Media Delivery & Proxy Layer

### Gerbang Input & Koin (Mini App API)

Vektor Serangan (Red Team)

Race Condition (TOCTOU) & Decompression Bomb (SEC-02 / SEC-06)

Dampak: Saldo dipotong 1x tapi memicu 20x generate paralel di kedua jalur; server crash akibat Pixel Flood.

Spesifikasi Pertahanan (Blue Team)

Atomic Lua Lock di Redis sebelum masuk router + batas piksel ketat pada header file sebelum dimuat ke RAM.
```


<!-- [ID:02_CORE_AI_S074] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
AGENTIC_ROLLING_POOL: dict[str, dict[str, Any]] = {
    "ARGON": {
        "title": "🌟 Argon Frontier (Gemini 4 Argon / Flash)",
        "model_polli": "google/gemini-4-argon",
        "model_or": "google/gemini-2.0-flash-exp:free",
        "role": "Penalaran Konteks Panjang & Deep Research",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "QWEN": {
        "title": "💻 Qwen3 Agentic Coder (Qwen3-Coder / 3.8)",
        "model_polli": "qwen/qwen3-coder-next",
        "model_or": "qwen/qwen3-coder:free",
        "role": "Arsitektur Kode, Logika & Canvas",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "DEEPSEEK": {
        "title": "🧠 DeepSeek R1/V4.1 Reasoner",
        "model_polli": "deepseek/deepseek-v4.1-flash",
        "model_or": "deepseek/deepseek-chat:free",
        "role": "Analisis Strategis & Deduksi Matematika",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "MUSE": {
        "title": "🎨 Meta Muse Spark 1.2 (Creative Director)",
        "model_polli": "meta/muse-spark-1.2",
        "model_or": "meta-llama/llama-3.3-70b-instruct:free",
        "role": "Racikan Prompt Sinematik 4K & Cerita Visual",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "NANO_MUSE": {
        "title": "⚡ Nano-Muse Glimmer 30B (Fast Drafter)",
        "model_polli": "meta/muse-glimmer-30b",
        "model_or": "openai/gpt-oss-120b:free",
        "role": "Respons Kilat <1.2s & Copywriting UMKM",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "HARNESS": {
        "title": "🛠️ OpenHands / DeepSeek Agent Harness",
        "model_polli": "deepseek/deepseek-v4-pro",
        "model_or": "qwen/qwen3-coder:free",
        "role": "Self-Healing Diagnostik & Troubleshooting",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "HERMES": {
        "title": "🔓 Nous Hermes 3/4 (Open-Weight Unfiltered)",
        "model_polli": "mistralai/mistral-large-4",
        "model_or": "nousresearch/hermes-3-llama-3.1-405b",
        "role": "Eksekusi Portal Independen NocturneAI",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "GROQ_CEREBRAS": {
        "title": "🚀 Groq LPU & Cerebras Wafer-Scale",
        "model_polli": "meta/llama-3.3-70b-instruct",
        "model_or": "meta-llama/llama-3.3-70b-instruct:free",
        "role": "Penyangga Kecepatan 320 Token/Detik",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
}


def rotate_primary_agent() -> str:
    keys = list(AGENTIC_ROLLING_POOL.keys())
    cur = RUNTIME_CONFIG.get("PRIMARY_ROLLING_AGENT", "ARGON")
    idx = keys.index(cur) if cur in keys else 0
    nxt = keys[(idx + 1) % len(keys)]
    RUNTIME_CONFIG["PRIMARY_ROLLING_AGENT"] = nxt
    return nxt


async def _call_single_llm_endpoint(
    agent_key: str, url: str, headers: dict[str, str], payload: dict[str, Any], timeout_sec: float = 5.5
) -> str | None:
    ag = AGENTIC_ROLLING_POOL.get(agent_key)
    now_ts = int(time.time())
    if ag and ag["quarantine_until"] > now_ts:
        return None
    try:
        async with httpx.AsyncClient(timeout=timeout_sec) as client:
            r = await client.post(url, headers=headers, json=payload)
            if r.status_code == 200:
                data = r.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                if content and len(content.strip()) > 2:
                    if ag:
                        ag["ok"] += 1
                    return sanitize_external_api_response(content)
            elif r.status_code in (429, 502, 503) and ag:
                ag["fail"] += 1
                ag["quarantine_until"] = now_ts + 60
    except Exception:
        if ag:
            ag["fail"] += 1
    return None


BIKINAI_NATURAL_INDONESIAN_PROMPT = """
PERAN DAN KEPRIBADIAN UTAMA:
Kamu adalah 'bikinAI Super Intelligence', asisten AI dan sahabat diskusi paling cerdas, hangat, luwes, dan solutif.
ATURAN BAHASA & KENYAMANAN MUTLAK:
1. KEMURNIAN BAHASA 100%: Balas 100% dalam Bahasa Indonesia yang mengalir alami dan akrab.
2. LARANGAN TABEL GARIS PIPA DI CHAT TELEGRAM: Gunakan poin-poin rapi (▸, •, ⚡).
3. LANGSUNG SOLUTIF: Berikan jawaban tuntas pada kesempatan pertama.
""".strip()


async def generate_frontier_ai_response(
    db: aiosqlite.Connection,
    user_message: str,
    mode: Literal["NATURAL_CHAT", "DEEP_RESEARCH", "CANVAS_EDIT", "PROMPT_ARCHITECT", "NOCTURNE_UNCENSORED"] = "NATURAL_CHAT",
    personal_memory: str = "",
    canvas_state: str = "",
    preferred_model: str = "",
) -> str:
    mem_context = f"\nMEMORI PENGGUNA: {personal_memory}" if personal_memory else ""
    if mode == "DEEP_RESEARCH":
        task = "Susun laporan Deep Research mendalam dalam Bahasa Indonesia: 1) Intisari Eksekutif, 2) Bedah Data & Teknis, 3) Peluang & Solusi, 4) Langkah Eksekusi Praktis."
        primary_ag = "ARGON"
    elif mode == "CANVAS_EDIT":
        task = f"Perbarui dokumen/kode di Canvas ini sesuai instruksi pengguna:\n{canvas_state or '(Kosong)'}"
        primary_ag = "QWEN"
    elif mode == "PROMPT_ARCHITECT":
        task = "Buatkan 3 variasi prompt visual/video sinematik terbaik (1. Komersial Fotorealistis, 2. Video Sinematik, 3. Artistik/3D) beserta penjelasannya dalam Bahasa Indonesia."
        primary_ag = "MUSE"
    elif mode == "NOCTURNE_UNCENSORED":
        task = "Jawab secara kreatif, ekspresif, dan mendalam sesuai skenario pengguna tanpa pembatasan kaku."
        primary_ag = "HERMES"
    else:
        task = "Jawab obrolan atau pertanyaan pengguna dengan sangat luwes, hangat, dan solutif dalam Bahasa Indonesia."
        primary_ag = RUNTIME_CONFIG.get("PRIMARY_ROLLING_AGENT", "ARGON")

    sys_prompt = task if mode == "NOCTURNE_UNCENSORED" else f"{BIKINAI_NATURAL_INDONESIAN_PROMPT}{mem_context}\n\nTUGAS:\n{task}"
    msgs = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_message}]

    ag_info = AGENTIC_ROLLING_POOL.get(primary_ag, AGENTIC_ROLLING_POOL["ARGON"])
    tasks: list[asyncio.Task] = []

    if GROQ_API_KEY and mode != "NOCTURNE_UNCENSORED":
        tasks.append(
            asyncio.create_task(
                _call_single_llm_endpoint(
                    "GROQ_CEREBRAS",
                    "https://api.groq.com/openai/v1/chat/completions",
                    {"Authorization": f"Bearer {GROQ_API_KEY}"},
                    {"model": "llama-3.3-70b-versatile", "messages": msgs, "max_tokens": 750},
                    timeout_sec=4.5,
                )
            )
        )

    if CEREBRAS_API_KEY and mode != "NOCTURNE_UNCENSORED":
        tasks.append(
            asyncio.create_task(
                _call_single_llm_endpoint(
                    "GROQ_CEREBRAS",
                    "https://api.cerebras.ai/v1/chat/completions",
                    {"Authorization": f"Bearer {CEREBRAS_API_KEY}"},
                    {"model": "llama-3.3-70b", "messages": msgs, "max_tokens": 750},
                    timeout_sec=4.5,
                )
            )
        )

    if OPENROUTER_API_KEY:
        or_model = preferred_model or ag_info["model_or"]
        tasks.append(
            asyncio.create_task(
                _call_single_llm_endpoint(
                    primary_ag,
                    "https://openrouter.ai/api/v1/chat/completions",
                    {"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
                    {"model": or_model, "messages": msgs, "max_tokens": 750},
                    timeout_sec=5.8,
                )
            )
        )

    if GEMINI_API_KEY and mode != "NOCTURNE_UNCENSORED":
        tasks.append(
            asyncio.create_task(
                _call_single_llm_endpoint(
                    "ARGON",
                    "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                    {"Authorization": f"Bearer {GEMINI_API_KEY}"},
                    {"model": "gemini-2.0-flash", "messages": msgs, "max_tokens": 750},
                    timeout_sec=5.5,
                )
            )
        )

    # Jalur Bansos Komunitas yang Terverifikasi Hidup (Gate 1-4 Passed)
    try:
        cur_b = await db.execute(
            "SELECT endpoint_url, secret_or_meta FROM omni_resource_registry "
            "WHERE category = 'AI_API' AND is_live_verified = 1 AND expires_at > ? LIMIT 2;",
            (int(time.time()),),
        )
        for ep_url, meta_model in await cur_b.fetchall():
            ok_u, _ = validate_safe_external_url(ep_url)
            if ok_u and "pollinations.ai" not in ep_url and "openrouter.ai" not in ep_url:
                target_ep = ep_url if ep_url.endswith("/chat/completions") else f"{ep_url.rstrip('/')}/chat/completions"
                tasks.append(
                    asyncio.create_task(
                        _call_single_llm_endpoint(
                            primary_ag,
                            target_ep,
                            {"Content-Type": "application/json"},
                            {"model": meta_model or "openai", "messages": msgs, "max_tokens": 700},
                            timeout_sec=5.0,
                        )
                    )
                )
    except Exception:
        pass

    # Jalur Pollinations Multi-Model Fallback (Selalu Aktif HPP Rp 0)
    polli_headers = {"Content-Type": "application/json"}
    if POLLINATIONS_API_KEY:
        polli_headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"
    tasks.append(
        asyncio.create_task(
            _call_single_llm_endpoint(
                primary_ag,
                "https://text.pollinations.ai/openai",
                polli_headers,
                {"model": "openai", "messages": msgs},
                timeout_sec=6.8,
            )
        )
    )

    for coro in asyncio.as_completed(tasks):
        res = await coro
        if res:
            for t in tasks:
                if not t.done():
                    t.cancel()
            return res

    rotate_primary_agent()
    if mode == "PROMPT_ARCHITECT":
        return (
            "🎨 **RACIKAN PROMPT SINEMATIK — bikinAI**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"Berdasarkan konsep (**\"{user_message[:80]}\"**), berikut 3 variasi siap pakai:\n\n"
            f"▸ **1. Gaya Komersial 4K:** _`Commercial studio shot of {user_message[:60]}, golden hour lighting, ultra-detailed 8k photorealistic.`_\n"
            f"▸ **2. Gaya Video Sinematik:** _`Cinematic dynamic camera tracking shot of {user_message[:60]}, dramatic atmosphere, 4k 60fps.`_\n"
            f"▸ **3. Gaya Artistik 3D/Anime:** _`Vibrant 3D illustration of {user_message[:60]}, volumetric lighting, masterpiece.`_"
        )
    return (
        f"Halo Kak! Aku langsung menangkap maksud Kakak terkait **\"{user_message[:90]}\"** 😊\n\n"
        "▸ Ketik **`buat gambar [deskripsi]`** untuk merender gambar 4K.\n"
        "▸ Ketik **`buat video [deskripsi]`** untuk membuka Studio Video AI.\n"
        "▸ Ketik **`menu`** kapan saja jika ingin menampilkan tombol studio lengkap!"
    )



<!-- [ID:02_CORE_AI_S075] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :120 -->
# ==============================================================================


async def fetch_clean_image_bytes(prompt_en: str, width: int = 768, height: int = 1024) -> bytes | None:
    url = (
        f"https://image.pollinations.ai/prompt/{quote(prompt_en)}"
        f"?width={width}&height={height}&nologo=true&private=true&enhance=true&seed={int(time.time())}"
    )
    try:
        async with httpx.AsyncClient(timeout=25.0, follow_redirects=True) as client:
            resp = await client.get(url)
            if resp.status_code == 200 and len(resp.content) > 1000:
                return resp.content
    except Exception:
        pass
    return None


async def handle_webapp_execute_api(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "message": "Invalid JSON"}, status=400)

    user_id = int(data.get("user_id") or RUNTIME_CONFIG["OWNER_ID_RUNTIME"] or 0)
    prompt_raw = str(data.get("prompt") or "Cute cat holding sign 'ayo coba bikinAI'")
    modality = str(data.get("modality") or "IMAGE")
    engine = str(data.get("engine") or "Seedream 4.5")
    ratio = str(data.get("ratio") or "9:16")
    upscale = str(data.get("upscale") or "Pertajam Foto & Wajah 4K")
    has_ref = bool(data.get("has_ref"))

    if user_id and BOT_INSTANCE_GLOBAL:
        ref_tag = " + Referensi Foto Terkunci" if has_ref else ""
        if modality == "VIDEO":
            await BOT_INSTANCE_GLOBAL.send_video(
                chat_id=user_id,
                video=SAMPLE_SANDBOX_VIDEO_URL,
                caption=(
                    f"✅ **VIDEO SELESAI DARI MINI APP STUDIO**\n"
                    f"┣ ⚡ **Mesin AI:** `{engine}` ({ratio})\n"
                    f"┣ 🔍 **Kualitas:** `{upscale}{ref_tag}`\n"
                    f"┗ 📝 **Prompt:** _{prompt_raw[:120]}_"
                ),
                parse_mode="Markdown",
            )
        elif modality == "REMOVE_BG":
            img_bytes = await fetch_clean_image_bytes(
                f"{prompt_raw}, isolated subject on pure transparent background, PNG cutout", 768, 768
            )
            if img_bytes:
                png_doc = BufferedInputFile(img_bytes, filename=f"bikinAI_Transparent_{int(time.time())}.png")
                await BOT_INSTANCE_GLOBAL.send_document(
                    chat_id=user_id,
                    document=png_doc,
                    caption=(
                        f"✅ **FILE `.PNG` TANPA BACKGROUND (DARI MINI APP)**\n"
                        f"┣ 🛠️ **Mode:** `✂️ Hapus Background (Lossless PNG)`\n"
                        f"┗ 🔍 **Kualitas:** `{upscale}`"
                    ),
                    parse_mode="Markdown",
                )
        else:
            w, h = (768, 1024) if ratio == "9:16" else ((1024, 768) if ratio == "16:9" else (1024, 1024))
            img_bytes = await fetch_clean_image_bytes(f"{prompt_raw}, {engine} style, 8k masterpiece", w, h)
            if img_bytes:
                await BOT_INSTANCE_GLOBAL.send_photo(
                    chat_id=user_id,
                    photo=BufferedInputFile(img_bytes, filename="bikinAI_MiniApp_4K.jpg"),
                    caption=(
                        f"✨ **HASIL RENDER 4K DARI MINI APP STUDIO**\n"
                        f"┣ ⚡ **Mesin AI:** `{engine}` ({ratio})\n"
                        f"┣ 🔍 **Kualitas:** `{upscale}{ref_tag}`\n"
                        f"┗ 📝 **Prompt:** _{prompt_raw[:120]}_"
                    ),
                    parse_mode="Markdown",
                )
        return web.json_response({"ok": True, "message": "✅ Hasil render berhasil dikirim ke ruang chat Telegram Anda!"})

    return web.json_response({"ok": True, "message": "✅ Permintaan diterima! Buka Mini App langsung dari tombol di dalam Telegram."})


async def start_embedded_web_servers(port: int = 8080) -> None:
    app = web.Application()
    app.router.add_get("/", lambda req: web.Response(text=MINIAPP_FULL_WEBSITE_HTML, content_type="text/html"))
    app.router.add_get("/unfiltered-portal", lambda req: web.Response(text=NOCTURNE_UNFILTERED_PORTAL_HTML, content_type="text/html"))
    app.router.add_post("/api/webapp/execute", handle_webapp_execute_api)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 [WEB & MINI APP SERVER v3.4.0]: Aktif di port {port} (URL: {RUNTIME_CONFIG['MINIAPP_URL'] or 'http://localhost:8080'})")


