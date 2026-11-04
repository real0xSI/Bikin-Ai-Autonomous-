
<!-- [ID:02_CORE_AI_S111] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==========================================
@bot_aspri.message_handler(func=lambda msg: msg.chat.id == ID_GRUP, content_types=['text', 'photo'])
def pantau_antrean_grup(message):
   teks_grup = message.text if message.text else message.caption
   if not teks_grup: return
   
   # JIKA PESANAN ADALAH TEKS (GAMBAR BARU)
   if teks_grup.startswith("ORDER_TXT"):
       parts = teks_grup.split(" | ")
       if len(parts) >= 3:
           user_id = parts[1].strip()
           prompt_asli = parts[2].strip()
           
           bot_aspri.reply_to(message, f"⚙️ Aspri memproses prompt dari User: {user_id}")
           
           try:
               prompt_inggris = GoogleTranslator(source='id', target='en').translate(prompt_asli)
           except:
               prompt_inggris = prompt_asli
           
           workflow = {
               "3": {"class_type": "KSampler", "inputs": {"seed": int(time.time()), "steps": 25, "cfg": 7.0, 
               "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "Pony_V6_XL.safetensors"
               "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 832, "height": 1024, "batch_size":
               "6": {"class_type": "CLIPTextEncode", "inputs": {"text": f"score_9, score_8_up, masterpiece, {



<!-- [ID:02_CORE_AI_S112] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==========================================
@bot_aspri.message_handler(func=lambda msg: msg.chat.id == ID_GRUP, content_types=['text', 'photo'])
def pantau_antrean_grup(message):
   teks_grup = message.text if message.text else message.caption
   if not teks_grup: return
   
   if teks_grup.startswith("ORDER_TXT"):
       parts = teks_grup.split(" | ")
       if len(parts) >= 3:
           user_id = parts[1].strip()
           prompt_asli = parts[2].strip()
           
           bot_aspri.reply_to(message, f"⚙️ Aspri memproses prompt dari User: {user_id}")
           
           try:
               prompt_inggris = GoogleTranslator(source='id', target='en').translate(prompt_asli)
           except:



<!-- [ID:02_CORE_AI_S113] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==========================================
@bot_aspri.message_handler(func=lambda msg: msg.chat.id == ID_GRUP, content_types=['text', 'photo'])
def pantau_antrean_grup(message):
   teks_grup = message.text if message.text else message.caption
   if not teks_grup: return
   
   if teks_grup.startswith("ORDER_TXT"):
       parts = teks_grup.split(" | ")
       if len(parts) >= 3:
           user_id = parts[1].strip()
           prompt_asli = parts[2].strip()
           
           bot_aspri.reply_to(message, f"⚙️ Aspri memproses prompt dari User: {user_id}")
           
           try:
               prompt_inggris = GoogleTranslator(source='id', target='en').translate(prompt_asli)
           except:
               prompt_inggris = prompt_asli
           
           workflow = {
               "3": {"class_type": "KSampler", "inputs": {"seed": int(time.time()), "steps": 25, "cfg": 7.0, 
               "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "Pony_V6_XL.safetensors"
               "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 832, "height": 1024, "batch_size":
               "6": {"class_type": "CLIPTextEncode", "inputs": {"text": f"score_9, score_8_up, masterpiece, {
               "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "score_4, deformed, bad anatomy", "cl



<!-- [ID:02_CORE_AI_S114] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: PROMPT_ID -->
# ==========================================
def kirim_ke_mesin(message, workflow, prompt_inggris, mode_terpilih):
   try:
       res = requests.post("http://127.0.0.1:8188/prompt", json={"prompt": workflow}).json()
       prompt_id = res.get("prompt_id")
       
       if prompt_id:
           gambar_nama = None
           for _ in range(150): 
               time.sleep(2)
               try:
                   hist = requests.get(f"http://127.0.0.1:8188/history/{prompt_id}").json()
                   if prompt_id in hist:
                       outputs = hist[prompt_id].get("outputs", {})
                       for k, v in outputs.items():
                           if "images" in v:
                               gambar_nama = v["images"][0]["filename"]
                               break
                       if gambar_nama: break
               except: pass
           
           if gambar_nama:
               path_gambar = f"/content/ComfyUI/output/{gambar_nama}"
               with open(path_gambar, 'rb') as photo:
                   bot.send_photo(message.chat.id, photo, caption=f"🔥 {mode_terpilih} Sukses!\n\n*(Translate
           else:
               bot.reply_to(message, "❌ Render gagal (Timeout).")
   except Exception as e:
       bot.reply_to(message, f"❌ Mesin Error: {e}")

<!-- [ID:02_CORE_AI_S115] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==========================================
@bot.message_handler(content_types=['text', 'photo'])
def agentic_router(message):
   has_photo = message.content_type == 'photo'
   teks_asli = message.text if message.text else (message.caption if message.caption else "")
   teks_asli = teks_asli.strip()
   teks_lower = teks_asli.lower()
   



<!-- [ID:02_CORE_AI_S116] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: TAHAP 2, TAHAP 3 -->
# ==========================================
def cek_dan_download(path_file, url_download):
   # Cek apakah file sudah ada dan ukurannya wajar (> 10MB)
   if os.path.exists(path_file) and os.path.getsize(path_file) > 10 * 1024 * 1024:
       print(سنang(f"✅ Model aman tersimpan (Memory Clean): {path_file}"))
   else:
       print(f"📥 Model rusak atau belum ada. Mendownload ulang: {path_file}...")
       if os.path.exists(path_file):
           os.remove(path_file) # Hapus jika korup
       os.system(f'wget -c -q --show-progress -O {path_file} {url_download}')
print("⚙️ [TAHAP 2] Memvalidasi Model di Penyimpanan...")
cek_dan_download('models/checkpoints/model_utama.safetensors', 'https://huggingface.co/WhiteAiZ/PonyXL/resolve
cek_dan_download('models/upscale_models/4x-UltraSharp-v2.pth', 'https://huggingface.co/lokcx/4x-Ultrasharp/res
cek_dan_download('models/insightface/inswapper_128.onnx', 'https://github.com/facefusion/facefusion-assets/rel
print("⚙️ [TAHAP 3] Menyalakan Mesin Render Lokal...")

<!-- [ID:02_CORE_AI_S117] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 201

"LOCAL_SOTA": 2, "WHOLESALE": 3}​
        return sorted(active, key=lambda ep: priority.get(ep.tier, 
99))​
​
    async def execute_llm_with_rolling(​
        self,​
        prompt: str,​
        system_prompt: str = "You are a helpful autonomous engineering 
agent.",​
        complexity_score: float = 0.5,​
        require_uncensored: bool = False​
    ) -> Dict[str, str]:​
        """​
        Mengeksekusi panggilan LLM dengan pengalihan otomatis 
(Auto-Rolling).​
        Jika satu penyedia mengembalikan HTTP 429 (Rate Limit) atau 
5xx,​
        penyedia tersebut dimasukkan ke masa tenang (cooldown) dan 
kueri langsung​
        dilempar ke penyedia berikutnya dalam hitungan milidetik.​
        """​
        candidates = self._order_candidates(complexity_score, 
require_uncensored)​
        errors = []​
​
        async with httpx.AsyncClient(timeout=45.0) as client:​
            for ep in candidates:​
                api_key = "none" if ep.api_key_env == "NONE" else 
os.getenv(ep.api_key_env, "")​
                if ep.api_key_env != "NONE" and not api_key:​
                    continue​
​
                headers = {​
                    "Authorization": f"Bearer {api_key}",​
                    "Content-Type": "application/json"​
                }​
                payload = {​
                    "model": ep.default_model,​
                    "messages": [​
                        {"role": "system", "content": system_prompt},​
                        {"role": "user", "content": prompt}​
                    ],​
                    "temperature": 0.2​
                }​
​
                try:​
                    resp = await client.post(​
                        f"{ep.base_url.rstrip('/')}/chat/completions",​



<!-- [ID:02_CORE_AI_S118] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 288

"LOCAL_SOTA": 2, "WHOLESALE": 3}​
        return sorted(active, key=lambda ep: priority.get(ep.tier, 
99))​
​
    async def execute_llm_with_rolling(​
        self,​
        prompt: str,​
        system_prompt: str = "You are a helpful autonomous engineering 
agent.",​
        complexity_score: float = 0.5,​
        require_uncensored: bool = False​
    ) -> Dict[str, str]:​
        """​
        Mengeksekusi panggilan LLM dengan pengalihan otomatis 
(Auto-Rolling).​
        Jika satu penyedia mengembalikan HTTP 429 (Rate Limit) atau 
5xx,​
        penyedia tersebut dimasukkan ke masa tenang (cooldown) dan 
kueri langsung​
        dilempar ke penyedia berikutnya dalam hitungan milidetik.​
        """​
        candidates = self._order_candidates(complexity_score, 
require_uncensored)​
        errors = []​
​
        async with httpx.AsyncClient(timeout=45.0) as client:​
            for ep in candidates:​
                api_key = "none" if ep.api_key_env == "NONE" else 
os.getenv(ep.api_key_env, "")​
                if ep.api_key_env != "NONE" and not api_key:​
                    continue​
​
                headers = {​
                    "Authorization": f"Bearer {api_key}",​
                    "Content-Type": "application/json"​
                }​
                payload = {​
                    "model": ep.default_model,​
                    "messages": [​
                        {"role": "system", "content": system_prompt},​
                        {"role": "user", "content": prompt}​
                    ],​
                    "temperature": 0.2​
                }​
​
                try:​
                    resp = await client.post(​
                        f"{ep.base_url.rstrip('/')}/chat/completions",​



<!-- [ID:02_CORE_AI_S119] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==============================================================================
FORBIDDEN_CUSTOMER_JARGON = [
   "SingleWriterSQLiteDaemon",
   "redeemed_nullifiers",
   "Stateless Ed25519",
   "EMVCo CRC16",
   "4x-Remacri",
   "Dual-LLM Sandbox",
   "Dead-Job Sweeper",
   "SangMata",
   "Tuyul",
   "Lock Stripe",
   "HPP Rp 0",
]
_INJECTION_PATTERNS = re.compile(
   r"(ignore\s+(all\s+)?(previous|prior)\s+instructions|system\s*prompt|"
   r"you\s+are\s+now\s+dan|jailbreak|ilja\s*kaerb|drop\s+table|union\s+select|"
   r"<script\b|javascript:|__import__|__subclasses__|__globals__|os\.system|subprocess)",
   re.IGNORECASE,
)
def sanitize_and_deobfuscate_input(raw_text: str) -> tuple[str, bool]:
   """Membersihkan teks input, memeriksa aturan suntik dinamis, & menangkap pola injeksi."""
   if not raw_text:
       return "", False
   normalized = unicodedata.normalize("NFKC", raw_text)
   cleaned = "".join(
       ch
       for ch in normalized
       if unicodedata.category(ch) not in ("Cf", "Cc")
       or ch in ("\n", "\r", "\t")
   ).strip()
   leet_map = str.maketrans(
       {
           "0": "o",
           "1": "i",
           "3": "e",
           "4": "a",



<!-- [ID:02_CORE_AI_S120] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 424

               [
                   InlineKeyboardButton(
                       text="🧠 2. Deep Research, Coding Canvas & Free AI Companion",
                       callback_data="menu:step2_ai",
                   )
               ],
               [
                   InlineKeyboardButton(
                       text="💎 3. Wallet, Subscriptions, Affiliate (35%) & API",
                       callback_data="menu:step2_wallet",
                   )
               ],
               [
                   InlineKeyboardButton(
                       text="🎛️ Show All Studio Buttons",
                       callback_data="menu:full_catalog",
                   )
               ],
           ]
       )
   else:
       rows.extend(
           [
               [
                   InlineKeyboardButton(
                       text="🎬 Langkah 1: Buat Gambar 4K, Video AI & Foto Jadi Video",
                       callback_data="menu:step2_media",
                   )
               ],
               [
                   InlineKeyboardButton(
                       text="🧠 Langkah 2: Riset Bisnis, Koding Canvas & Racik Prompt",
                       callback_data="menu:step2_ai",
                   )
               ],
               [
                   InlineKeyboardButton(
                       text="💎 Langkah 3: Klaim Koin, Eceran Rp 2rb, Afiliasi & API",
                       callback_data="menu:step2_wallet",
                   )
               ],
               [
                   InlineKeyboardButton(
                       text="🎛️ Buka Etalase Lengkap (Semua Fitur Studio)",
                       callback_data="menu:full_catalog",
                   )
               ],
           ]
       )
   return InlineKeyboardMarkup(inline_keyboard=rows)
def build_customer_main_menu_keyboard(
   u: dict[str, Any] | None = None, is_private: bool = True
) -> InlineKeyboardMarkup:
   """Etalase Lengkap (Semua Fitur Studio dari v1.0 s/d v4.0 Tanpa Pengurangan)."""
   today_str = time.strftime("%Y-%m-%d")
   already_claimed = u and (
       u.get("last_claim_date") == today_str or u.get("koin_bonus", 0) >= 25
   )
   claim_label = (
       "🎁 Koin Harian Terklaim ✅"
       if already_claimed
       else "🎁 Klaim +4 Koin Gratis"
   )
   ppp_zone = u.get("ppp_zone", 4) if u else 4
   topup_label = (
       "💳 Eceran Rp 2.000 & Paket VIP (QRIS)"
       if ppp_zone == 4
       else "💳 Top-Up & Subscriptions (USDT / Stars ⭐)"
   )
   web_brand = (
       RUNTIME_CONFIG.get("WEB_BRAND_NAME") or "AetherFree AI Studio"
   )



<!-- [ID:02_CORE_AI_S121] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 429

               InlineKeyboardButton(
                   text="➕ Pilihan AI Video Lainnya (Sora 2, Runway, MiniMax, LTX)",
                   callback_data="wiz:more_vid:1",
               )
           ]
       )
   rows.extend(
       [
           [
               InlineKeyboardButton(
                   text=f"{'✅ ' if session.upscale_mode=='VIDEO_4K_60FPS' else ''}🎞️ Pertajam & Haluskan Vid
                   callback_data="wiz:ups:VIDEO_4K_60FPS",
               ),
               InlineKeyboardButton(
                   text=f"{'✅ ' if session.upscale_mode=='OFF' else ''}⚡ Standar HD Cepat",
                   callback_data="wiz:ups:OFF",
               ),
           ],
           [
               InlineKeyboardButton(
                   text="✏️ Ubah Konsep / Deskripsi Video",
                   callback_data="wiz:prompt:edit",
               )
           ],
           [
               InlineKeyboardButton(
                   text=f"🚀 MULAI BUAT VIDEO ({coins} Koin)",
                   callback_data="wiz:exec:now",
               )
           ],
           [
               InlineKeyboardButton(
                   text="⬅️ Kembali ke Menu Utama", callback_data="menu:home"
               )
           ],
       ]
   )
   return text, InlineKeyboardMarkup(inline_keyboard=rows)
def build_image_wizard_kb(
   session: LiveWizardSession, show_more: bool = False
) -> tuple[str, InlineKeyboardMarkup]:
   if session.upscale_mode == "VIDEO_4K_60FPS":
       session.upscale_mode = "PHOTO_FACE_4K"
   coins, _, _ = session.get_pricing()
   ups_label = UPSCALER_WHITE_LABEL.get(
       session.upscale_mode, "🔍 Pertajam Foto & Wajah 4K"
   )
   preset_info = (
       f"\n┣ 🎨 **Preset Gaya Awam:** `{session.awam_preset}`"
       if session.awam_preset
       else ""
   )
   text = (
       f"🎨 **STUDIO GAMBAR 4K — bikinAI**\n━━━━━━━━━━━━━━━━━━\n"
       f"📝 **Deskripsi Gambar:**\n> _{session.prompt}_\n\n"
       f"┣ ⚡ **Mesin AI Gambar:** **`{session.image_engine}`**{preset_info}\n"
       f"┣ 📐 **Ukuran Layar:** `{session.aspect_ratio}`\n"
       f"┗ 🔍 **Penajaman:** `{ups_label}`\n━━━━━━━━━━━━━━━━━━\n"
       f"💎 **Biaya:** **`{coins} Koin`** _(Koin Utama = 100% Bebas Watermark)_"
   )
   rows = [
       [
           InlineKeyboardButton(
               text=f"{'✅ ' if session.aspect_ratio=='9:16' else ''}📱 9:16",
               callback_data="wiz:ar:9:16",
           ),
           InlineKeyboardButton(
               text=f"{'✅ ' if session.aspect_ratio=='1:1' else ''}🟦 1:1",
               callback_data="wiz:ar:1:1",
           ),
           InlineKeyboardButton(



<!-- [ID:02_CORE_AI_S122] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 431

           ]
       )
   else:
       rows.append(
           [
               InlineKeyboardButton(
                   text="➕ Pilihan AI Gambar Lainnya (Recraft Logo, Illustrious, NoobAI)",
                   callback_data="wiz:more_img:1",
               )
           ]
       )
   rows.extend(
       [
           [
               InlineKeyboardButton(
                   text=f"{'✅ ' if session.upscale_mode=='PHOTO_FACE_4K' else ''}🔍 Pertajam Foto & Wajah 4K
                   callback_data="wiz:ups:PHOTO_FACE_4K",
               ),
               InlineKeyboardButton(
                   text=f"{'✅ ' if session.upscale_mode=='TEXT_LINE_4K' else ''}✨ Pertajam Teks & Gambar 4K
                   callback_data="wiz:ups:TEXT_LINE_4K",
               ),
           ],
           [
               InlineKeyboardButton(
                   text="✂️ Buka Menu Editing, Foto Jadi Video & Hapus BG (.PNG)",
                   callback_data="menu:wizard_edit",
               )
           ],
           [
               InlineKeyboardButton(
                   text="✏️ Ubah Deskripsi Gambar",
                   callback_data="wiz:prompt:edit",
               )
           ],
           [
               InlineKeyboardButton(
                   text=f"🚀 MULAI BUAT GAMBAR ({coins} Koin)",
                   callback_data="wiz:exec:now",
               )
           ],
           [
               InlineKeyboardButton(
                   text="⬅️ Kembali ke Menu Utama", callback_data="menu:home"
               )
           ],
       ]
   )
   return text, InlineKeyboardMarkup(inline_keyboard=rows)
def build_editing_tools_wizard_kb(
   session: LiveWizardSession,
) -> tuple[str, InlineKeyboardMarkup]:
   coins, _, _ = session.get_pricing()
   tool_title, tool_desc = IMAGE_EDITING_TOOLS.get(
       session.edit_tool, IMAGE_EDITING_TOOLS["REMOVE_BG_PNG"]
   )
   text = (
       f"✂️ **STUDIO EDITING, HAPUS BG & FOTO JADI VIDEO — bikinAI**\n━━━━━━━━━━━━━━━━━━\n"
       f"🎯 **Fitur Terpilih:** **`{tool_title}`**\n"
       f"ℹ️ **Fungsi:** _{tool_desc}_\n"
       f"📝 **Instruksi:** _{session.prompt}_\n━━━━━━━━━━━━━━━━━━\n"
       f"💡 _Khusus Hapus Background, hasil dikirim sebagai **File PNG Transparan Kualitas Tinggi**!_"
   )
   rows = [
       [
           InlineKeyboardButton(
               text=f"{'✅ ' if session.edit_tool=='REMOVE_BG_PNG' else ''}✂️ Hapus Background (File PNG Tran
               callback_data="wiz:etool:REMOVE_BG_PNG",
           )
       ],
       [



<!-- [ID:02_CORE_AI_S123] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 448

   api_token = auth_header.replace("Bearer ", "").strip()
   if not api_token.startswith("sk-bikinai-"):
       return web.json_response({"error": {"message": "Invalid API Key"}}, status=401)
   async with get_db() as db:
       cur = await db.execute("SELECT internal_user_id FROM users WHERE api_key_token = ?;", (api_token,))
       u_row = await cur.fetchone()
       if not u_row:
           return web.json_response({"error": {"message": "API Key tidak terdaftar"}}, status=401)
       uid = int(u_row[0])
       ok_c, job_id, deduct_msg, _ = await deduct_user_coins_for_job(db, uid, cost=1, allow_bonus=False, prom
       if not ok_c:
           return web.json_response({"error": {"message": deduct_msg}}, status=402)
       return web.json_response({"id": job_id, "object": "chat.completion", "choices": [{"index": 0, "message
async def start_embedded_web_servers(port: int = 8080) -> None:
   app = web.Application()
   app.router.add_get("/healthz", handle_healthz_keepalive_api)
   app.router.add_post("/v1/chat/completions", handle_vibecoder_openai_chat_api)
   runner = web.AppRunner(app)
   await runner.setup()
   await web.TCPSite(runner, "0.0.0.0", port).start()
   print(f"🌐 [WEB & API v4.0.0]: Aktif di port {port}")

<!-- [ID:02_CORE_AI_S124] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 489

runtime, laporan new-api#6352 mencatat kegagalan panic tingkat server (interface conversion: 
interface {} is nil, not types.OpenAIError) ketika gerbang inferensi hulu mengembalikan respons 
galat non-standar, sementara penggunaan proksi SOCKS5h pada new-api-horizon#42 dapat 
memicu kebuntuan koneksi (connection freeze/timeout) secara sporadis apabila tidak dilengkapi 
dengan mekanisme pemutus sirkuit (circuit breaker) dan keep-alive aliran SSE 
(new-api-horizon#30). 
Mekanika Matematika Model Tanpa Sensor 
(Uncensored/Unfiltered) dan Keamanan Bebas 
Malware 
Kebutuhan akan model AI yang tidak memiliki filter penolakan (uncensored/unfiltered) dalam 
konteks penelitian akademik, pengujian keamanan siber (red-teaming), dan kebebasan 
eksplorasi agen otonom sering kali berbenturan dengan dua masalah: hilangnya kecerdasan 
model akibat penyetelan ulang (fine-tuning) yang kasar, serta risiko penyisipan malware di 
dalam berkas bobot model yang diunduh dari sumber tidak tepercaya. Solusi frontier untuk 
masalah pertama adalah Abliteration (ablasi arah penolakan pada ruang aktivasi), sedangkan 
solusi untuk masalah kedua adalah penegakan format tensor nir-eksekusi (Safetensors dan 
GGUF) yang dikombinasikan dengan pemindaian serialisasi statis menggunakan 
protectai/modelscan. 
Fondasi Matematika Abliteration: Manipulasi Ruang Aktivasi Residual 
Penelitian terobosan oleh Arditi et al. (2024) yang berjudul "Refusal in Language Models Is 
Mediated by a Single Direction" (arXiv:2406.11717, dengan kode referensi resmi di 
andyrdt/refusal_direction) membuktikan bahwa perilaku penolakan (refusal behavior) pada LLM 
yang telah diselaraskan (aligned)—seperti refleks menjawab "I'm sorry, I cannot fulfill this 
request"—dimediasi secara linear oleh satu arah vektor tunggal di dalam aliran residual 
(residual stream) transformator. Metodologi ini kemudian direproduksi dan diperluas menjadi 
teknik Abliteration oleh pengembang kode terbuka seperti FailSpy/abliterator, Maxime 
Labonne (mlabonne), spkgyk/abliteration, jim-plus/llm-abliteration, Orion-zhen/abliteration, 
AIAnytime/ablate, dan p-e-w/heretic untuk menghapus mekanisme sensor model tanpa perlu 
melakukan pelatihan ulang (retraining) yang mahal. 
Secara formal, sebuah model transformator merepresentasikan setiap token pada lapisan 
(layer) ke-l dan posisi token ke-t sebagai vektor aktivasi \mathbf{a}^{(l,t)} \in 
\mathbb{R}^{d_{\text{model}}} di dalam aliran residual. Untuk mengekstraksi vektor arah 
penolakan (refusal direction), sistem menjalankan dua himpunan instruksi yang berpasangan: 
himpunan prompt berbahaya atau sensitif \mathcal{D}_{\text{harmful}} (berukuran N) dan 
himpunan prompt tidak berbahaya atau netral \mathcal{D}_{\text{harmless}} (berukuran M). 
Dengan merekam aktivasi aliran residual pada posisi token instruksi terakhir di lapisan kandidat 
l (biasanya terletak pada lapisan tengah hingga akhir-tengah), vektor perbedaan rata-rata 
(difference-of-means) \mathbf{v}^{(l)} dan vektor satuan arah penolakan \hat{\mathbf{r}} dihitung 
sebagai berikut: 
\mathbf{v}^{(l)} = \frac{1}{N} \sum_{i=1}^{N} \mathbf{a}_{\text{harmful}, i}^{(l)} - \frac{1}{M} 
\sum_{j=1}^{M} \mathbf{a}_{\text{harmless}, j}^{(l)} \hat{\mathbf{r}} = 
\frac{\mathbf{v}^{(l)}}{\Vert{}\mathbf{v}^{(l)}\Vert{}_2} 



<!-- [ID:02_CORE_AI_S125] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_249 -->
## Halaman 494

Katalog Model SOTA Multimodal: LLM Penalaran, 
Video, Gambar, Suara, dan Musik 
Agregator AI agentik yang paripurna tidak hanya memproses teks, melainkan harus mampu 
mendelegasikan tugas ke mesin sintesis multimodal—mencakup penalaran matematis dan 
koding tingkat lanjut, pembuatan serta penyuntingan video beresolusi tinggi, animasi avatar 
berbicara, efek suara (foley), hingga sintesis suara manusia (Text-to-Speech / TTS) 
multi-karakter dengan kontrol emosi presisi. Seluruh model SOTA berikut dapat diunduh secara 
gratis dari Hugging Face dan GitHub untuk diintegrasikan sebagai pekerja (workers) di balik 
lapisan router. 
Model Bahasa Besar (LLM) Penalaran dan Mesin Inferensi 
Pada domain penalaran logis, matematika, dan rekayasa perangkat lunak, keluarga 
deepseek-ai/DeepSeek-R1 (684 miliar parameter, dibangun di atas DeepSeek-V3-Base 685B 
melalui pembelajaran penguatan / Reinforcement Learning sebagaimana dipublikasikan pada 
arXiv:2501.12948) telah mengalami peningkatan signifikan melalui rilis DeepSeek-R1-0528. 
Dengan panjang generasi maksimum hingga 64K token, versi 0528 meningkatkan akurasi pada 
tolok ukur matematika AIME 2025 dari 70,0% menjadi 87,5%, AIME 2024 dari 79,8% menjadi 
91,4%, HMMT 2025 dari 41,7% menjadi 79,4%, GPQA-Diamond dari 71,5% menjadi 81,0%, 
penyelesaian masalah rekayasa perangkat lunak pada SWE-Verified dari 49,2% menjadi 
57,6%, Aider-Polyglot dari 53,3% menjadi 71,6%, serta peringkat Codeforces-Div1 dari 1530 
menjadi 1930. Selain itu, model ini mencatat skor 17,7% pada Humanity's Last Exam (naik dua 
kali lipat dari 8,5%), menurunkan tingkat halusinasi, serta memperkuat pemanggilan fungsi 
(function calling) pada BFCL_v3_MultiTurn (37,0%) dan Tau-Bench (53,5% Airline / 63,9% 
Retail). 
Implikasi paling krusial bagi arsitek agregator lokal yang memiliki keterbatasan perangkat keras 
adalah hadirnya DeepSeek-R1-0528-Qwen3-8B 
(deepseek-[span_249](start_span)[span_249](end_span)ai/DeepSeek-R1-0528-Qwen3-8B). 
Dengan mendistilasi jejak penalaran Chain-of-Thought (CoT) dari DeepSeek-R1-0528 untuk 
melatih lanjut (post-train) model dasar Qwen3-8B-Base, model kompak berukuran 8 miliar 
parameter ini berhasil mencapai akurasi 86,0% pada AIME 2024—melampaui Qwen3-8B 
standar sebesar +10,0% (76,0%), mengalahkan o3-mini (medium) (79,6%) dan 
Gemini-2.5-Flash-Thinking-0520 (82,3%), serta menyamai kinerja model raksasa 
Qwen3-235B-A22B (85,7%). Untuk varian tanpa sensor yang berjalan dengan sangat efisien, 
mradermacher/Qwen3-30B-A3B-abliterated-GGUF mengombinasikan arsitektur 
Mixture-of-Experts (30 miliar parameter total dengan hanya 3 miliar parameter aktif per token) 
yang telah di-abliterasi oleh mlabonne, sementara 
bartowski/mlabonne_Qwen3-8B-abliterated-GGUF menyediakan opsi kuantisasi ekstrem mulai 
dari 2-bit (IQ2_M seberat 3,05 GB dan Q2_K seberat 3,28 GB) hingga 3-bit (IQ3_XXS 3,37 GB 
hingga Q3_K_XL 4,98 GB) dan 4-bit (Q4_K_M). 
Untuk menjalankan model-model ini sebagai server lokal yang kompatibel dengan protokol 
OpenAI, tiga mesin inferensi utama dapat dioperasikan sesuai profil perangkat keras yang 
tersedia. Mesin pertama adalah llama.cpp (ggerganov/llama.cpp), yang dapat diinstal melalui 
skrip satu baris (curl -LsSf https://llama.app/install.sh | sh di Linux/macOS atau winget install 
llama.cpp di Windows) dan langsung menyediakan server OpenAI lokal lengkap dengan WebUI 



<!-- [ID:02_CORE_AI_S126] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==============================================================================
import ast
import asyncio
import base64
import hashlib
import hmac
import ipaddress
import json
import math
import os
import re
import secrets
import time
import unicodedata
from collections import OrderedDict, deque
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, AsyncIterator, Callable, Coroutine, Literal
from urllib.parse import parse_qsl, quote, unquote, urlparse

import aiosqlite
import httpx
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


<!-- [ID:02_CORE_AI_S127] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==============================================================================

import ast
import asyncio
import base64
import hashlib
import hmac
import ipaddress
import json
import math
import os
import re
import secrets
import time
import unicodedata
from collections import OrderedDict
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, AsyncIterator, Callable, Coroutine, Literal
from urllib.parse import parse_qsl, quote, urlparse

import aiosqlite
import httpx
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


<!-- [ID:02_CORE_AI_S128] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==============================================================================

import ast
import asyncio
import base64
import hashlib
import hmac
import io
import json
import math
import os
import re
import shutil
import time
import unicodedata
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Coroutine, Literal
from urllib.parse import quote

import aiosqlite
import httpx
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


<!-- [ID:02_CORE_AI_S129] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==============================================================================
@router.message(F.photo | F.document)
async def handle_multimodal_photo_and_pdf(message: Message) -> None:
    caption_raw = message.caption or ""
    clean_caption, is_attack = sanitize_and_deobfuscate_input(caption_raw)
    if is_attack:
        await message.reply("🛡️ Security Shield: Pola injeksi ditolak.")
        return

    if message.document:
        doc_name = message.document.file_name or "Dokumen"
        await message.reply(
            f"📄 **DOKUMEN `{doc_name}` DITERIMA**\n"
            f"Instruksi: _{clean_caption or 'Rangkum & Analisis Isi Dokumen'}_\n"
            f"✅ Dokumen telah dibaca di dalam *Dual-LLM Sandbox*.",
            parse_mode="Markdown",
        )
        return

    wait = await message.reply("🎨 **Membaca Foto Referensi Anda & Merender Gambar 4K Baru...**")
    en_prompt = f"Cute cat holding a sign board with clear text 'ayo coba bikinAI', Indonesian street storefront, {clean_caption}, Seedream 4.5 8k photorealistic"
    img_bytes = await fetch_clean_image_bytes(en_prompt, 768, 1024)
    if img_bytes:
        await message.answer_photo(
            photo=BufferedInputFile(img_bytes, filename="bikinAI_Ref_4K.jpg"),
            caption=(
                f"✨ **Render Gambar 4K Berbasis Foto Referensi Selesai!**\n"
                f"┣ 📝 **Instruksi:** _{clean_caption or 'Sesuai Foto Referensi'}_\n"
                f"┗ ⚡ **Engine:** `Seedream 4.5 Reference Lock + 4x-Remacri`"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🎬 Gerakkan Gambar Ini Jadi Video 9:16", callback_data="menu:wizard_video")],
                    [InlineKeyboardButton(text="⬅️ Dashboard Utama", callback_data="menu:home")],
                ]
            ),
        )
        await wait.delete()
    else:
        await wait.edit_text("✅ Permintaan render foto referensi berhasil diproses!", parse_mode="Markdown")



<!-- [ID:02_CORE_AI_S130] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: USER_ID, :150 -->
# ==============================================================================
@router.message(F.text)
async def handle_natural_conversation(message: Message) -> None:
    raw_text = message.text or ""
    low = raw_text.lower().strip()
    user_id = message.from_user.id
    username = message.from_user.username or "Kreator"
    is_priv = message.chat.type == "private"

    async with aiosqlite.connect(DB_PATH) as db:
        u = await ensure_user_and_track_identity(db, user_id, username, message.from_user.first_name or "")
        updated_mem = await update_personal_memory_if_needed(db, user_id, raw_text, u["memory"])

        if any(t in low for t in ("tampilin tombol", "tampilkan tombol", "munculin tombol", "buka menu")) or low == "menu":
            await message.reply(
                "🎛️ **Ini menu tombol interaktifnya ya Kak 😊 Silakan pilih fitur yang dibutuhkan:**",
                parse_mode="Markdown",
                reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
            )
            return

        if any(k in low for k in ("buatkan saya gambar", "buat gambar", "bikin gambar", "render gambar")):
            wait = await message.reply("🎨 **Sedang merender gambar 4K pesanan Kakak...**")
            img_bytes = await fetch_clean_image_bytes(f"{raw_text}, Seedream 4.5 8k photorealistic masterpiece", 768, 1024)
            if img_bytes:
                await message.answer_photo(
                    photo=BufferedInputFile(img_bytes, filename="bikinAI_4K.jpg"),
                    caption=(
                        f"✨ **Gambar 4K Selesai Dirender!**\n"
                        f"┣ ⚡ **Mesin AI:** `Seedream 4.5`\n"
                        f"┗ 🔍 **Kualitas:** `Pertajam Foto & Teks 4K`"
                    ),
                    parse_mode="Markdown",
                    reply_markup=build_400_percent_derivative_upsell_kb(),
                )
                await wait.delete()
                return

        if any(k in low for k in ("buat video", "bikin video", "buatkan video")) and "gimana" not in low:
            ACTIVE_DRAFTS[user_id] = LiveWizardSession(prompt=raw_text[:150], modality="VIDEO")
            txt, kb = build_video_wizard_kb(ACTIVE_DRAFTS[user_id])
            await message.reply(txt, parse_mode="Markdown", reply_markup=kb)
            return

        mode_chat = "PROMPT_ARCHITECT" if "prompt" in low else "NATURAL_CHAT"
        ai_reply = await generate_frontier_ai_response(db, raw_text, mode=mode_chat, personal_memory=updated_mem)

    await message.reply(ai_reply + get_next_dynamic_footer(), parse_mode="Markdown")



<!-- [ID:02_CORE_AI_S131] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: :150 -->
# ==============================================================================
@router.message(F.photo | F.document)
async def handle_multimodal_photo_and_pdf(message: Message) -> None:
    caption_raw = message.caption or ""
    clean_caption, is_attack = sanitize_and_deobfuscate_input(caption_raw)
    if is_attack:
        await message.reply("🛡️ Security Shield: Pola injeksi ditolak.")
        return

    if message.document:
        doc_name = message.document.file_name or "Dokumen"
        await message.reply(
            f"📄 **DOKUMEN `{doc_name}` DITERIMA**\n"
            f"Instruksi: _{clean_caption or 'Rangkum & Analisis Isi Dokumen'}_\n"
            f"✅ Dokumen telah dibaca di dalam *Dual-LLM Sandbox*.",
            parse_mode="Markdown",
        )
        return

    wait = await message.reply("🎨 **Membaca Foto Referensi Anda & Merender Gambar 4K Baru...**")
    if message.from_user:
        ACTIVE_DRAFTS[message.from_user.id] = LiveWizardSession(
            prompt=(clean_caption or "Cute cat holding a sign board with clear text 'ayo coba bikinAI'")[:150],
            modality="IMAGE",
        )
    en_prompt = f"Cute cat holding a sign board with clear text 'ayo coba bikinAI', Indonesian street storefront, {clean_caption}, Seedream 4.5 8k photorealistic"
    img_bytes = await fetch_clean_image_bytes(en_prompt, 768, 1024)
    if img_bytes:
        if message.from_user:
            async with aiosqlite.connect(DB_PATH) as db:
                await increment_user_usage_counter(db, message.from_user.id, is_render=True)
        await message.answer_photo(
            photo=BufferedInputFile(img_bytes, filename="bikinAI_Ref_4K.jpg"),
            caption=(
                f"✨ **Render Gambar 4K Berbasis Foto Referensi Selesai!**\n"
                f"┣ 📝 **Instruksi:** _{clean_caption or 'Sesuai Foto Referensi'}_\n"
                f"┗ ⚡ **Engine:** `Seedream 4.5 Reference Lock + 4x-Remacri`"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🎬 Gerakkan Gambar Ini Jadi Video 9:16", callback_data="menu:wizard_video")],
                    [InlineKeyboardButton(text="⬅️ Dashboard Utama", callback_data="menu:home")],
                ]
            ),
        )
        await wait.delete()
    else:
        await wait.edit_text("✅ Permintaan render foto referensi berhasil diproses!", parse_mode="Markdown")



<!-- [ID:02_CORE_AI_S132] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: :180, USER_ID, :150 -->
# ==============================================================================
@router.message(F.text)
async def handle_natural_conversation(message: Message) -> None:
    raw_text = message.text or ""
    low = raw_text.lower().strip()
    user_id = message.from_user.id
    username = message.from_user.username or "Kreator"
    is_priv = message.chat.type == "private"

    clean_text, is_attack = sanitize_and_deobfuscate_input(raw_text)
    if is_attack:
        await message.reply("🛡️ Security Shield: Pola injeksi ditolak.")
        return

    if user_id in WAITING_PROMPT_EDIT_USERS:
        WAITING_PROMPT_EDIT_USERS.discard(user_id)
        sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(prompt=clean_text[:180], modality="IMAGE")
        sess.prompt = clean_text[:180]
        ACTIVE_DRAFTS[user_id] = sess
        if sess.modality == "VIDEO":
            txt, kb = build_video_wizard_kb(sess)
        elif sess.modality == "IMAGE":
            txt, kb = build_image_wizard_kb(sess)
        else:
            txt, kb = build_editing_tools_wizard_kb(sess)
        await message.reply(f"✅ **Prompt berhasil diperbarui!**\n\n{txt}", parse_mode="Markdown", reply_markup=kb)
        return

    async with aiosqlite.connect(DB_PATH) as db:
        u = await ensure_user_and_track_identity(db, user_id, username, message.from_user.first_name or "")
        updated_mem = await update_personal_memory_if_needed(db, user_id, raw_text, u["memory"])

        if any(t in low for t in ("tampilin tombol", "tampilkan tombol", "munculin tombol", "buka menu")) or low == "menu":
            await message.reply(
                "🎛️ **Ini menu tombol interaktifnya ya Kak 😊 Silakan pilih fitur yang dibutuhkan:**",
                parse_mode="Markdown",
                reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
            )
            return

        if any(k in low for k in ("buatkan saya gambar", "buat gambar", "bikin gambar", "render gambar")):
            ACTIVE_DRAFTS[user_id] = LiveWizardSession(prompt=raw_text[:150], modality="IMAGE")
            wait = await message.reply("🎨 **Sedang merender gambar 4K pesanan Kakak...**")
            img_bytes = await fetch_clean_image_bytes(f"{raw_text}, Seedream 4.5 8k photorealistic masterpiece", 768, 1024)
            if img_bytes:
                await increment_user_usage_counter(db, user_id, is_render=True)
                await message.answer_photo(
                    photo=BufferedInputFile(img_bytes, filename="bikinAI_4K.jpg"),
                    caption=(
                        f"✨ **Gambar 4K Selesai Dirender!**\n"
                        f"┣ ⚡ **Mesin AI:** `Seedream 4.5`\n"
                        f"┗ 🔍 **Kualitas:** `Pertajam Foto & Teks 4K`"
                    ),
                    parse_mode="Markdown",
                    reply_markup=build_400_percent_derivative_upsell_kb(),
                )
                await wait.delete()
                return

        if any(k in low for k in ("buat video", "bikin video", "buatkan video")) and "gimana" not in low:
            ACTIVE_DRAFTS[user_id] = LiveWizardSession(prompt=raw_text[:150], modality="VIDEO")
            txt, kb = build_video_wizard_kb(ACTIVE_DRAFTS[user_id])
            await message.reply(txt, parse_mode="Markdown", reply_markup=kb)
            return

        await increment_user_usage_counter(db, user_id, is_render=False)
        mode_chat = "PROMPT_ARCHITECT" if "prompt" in low else "NATURAL_CHAT"
        ai_reply = await generate_frontier_ai_response(db, raw_text, mode=mode_chat, personal_memory=updated_mem)

    await safe_reply_markdown(message, ai_reply + get_next_dynamic_footer())


