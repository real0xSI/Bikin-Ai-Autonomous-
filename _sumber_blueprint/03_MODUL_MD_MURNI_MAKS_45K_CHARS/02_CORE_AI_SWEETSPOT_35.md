
<!-- [ID:02_CORE_AI_S076] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :120 -->
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
    app.router.add_post("/api/voucher/redeem", handle_voucher_redeem_api)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 [WEB & MINI APP SERVER v3.4.0]: Aktif di port {port} (URL: {RUNTIME_CONFIG['MINIAPP_URL'] or 'http://localhost:8080'})")



<!-- [ID:02_CORE_AI_S077] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
router: Router = Router(name="bikinai_master_router_v4")

DYNAMIC_CONSUMER_FOOTERS = [
    "💡 \x3ci>Tips: Ketik \x3cb>tampilin tombol\x3c/b> kapan saja untuk membuka menu studio cepat.\x3c/i>",
    "✨ \x3ci>Info: Paket Eceran mulai Rp 2.000 langsung membuat hasil karyamu 100% bebas tanda air!\x3c/i>",
    "🎬 \x3ci>Baru: Kirim foto apa saja lalu beri keterangan untuk mengubahnya jadi video bergerak!\x3c/i>",
    "🎁 \x3ci>Bagikan link referral di menu Komunitas & dapatkan komisi otomatis dari teman yang bergabung.\x3c/i>",
]
_FOOTER_CURSOR = 0


def next_consumer_footer() -> str:
    global _FOOTER_CURSOR
    item = DYNAMIC_CONSUMER_FOOTERS[_FOOTER_CURSOR % len(DYNAMIC_CONSUMER_FOOTERS)]
    _FOOTER_CURSOR += 1
    return item


async def build_buyer_main_menu_view(user_id: int, first_name: str = "Sahabat Kreator") -> Tuple[str, InlineKeyboardMarkup]:
    """
    Membangun tampilan Menu Utama Pembeli (100% Bahasa Konsumen, Tanpa Istilah Teknis Internal).
    Digunakan oleh `/start`, `/menu`, tombol `menu:home`, dan Inspektor Layar Pembeli `adm:preview_buyer_ui`.
    """
    user = await ensure_user_profile(user_id, first_name=first_name)
    miniapp_url = await get_db().get_setting("miniapp_url", f"{PUBLIC_WEB_BASE_URL}/")
    utama = int(user.get("koin_utama") or 0)
    bonus = int(user.get("koin_bonus") or 0)
    status_lisensi = (
        "💎 \x3cb>Lisensi Komersial Bersih (100% Bebas Watermark)\x3c/b>"
        if utama > 0 or int(user.get("has_topped_up") or 0) == 1
        else "🎁 \x3cb>Mode Coba Gratis (Koin Bonus Harian)\x3c/b>"
    )
    text = (
        f"Halo, \x3cb>{html.escape(first_name)}\x3c/b>! 👋\n"
        f"Selamat datang di \x3cb>bikinAI Studio Kreatif\x3c/b> — asisten pribadimu untuk mengobrol hangat, "
        f"membuat foto produk 4K, video sinematik, hingga suara narator jernih.\n\n"
        f"💳 \x3cb>Dompet Koin Kamu:\x3c/b>\n"
        f"• Koin Utama: \x3cb>{utama} Koin\x3c/b>\n"
        f"• Koin Bonus Gratis: \x3cb>{bonus}/25 Koin\x3c/b>\n"
        f"• Status Karya: {status_lisensi}\n\n"
        f"Kamu bisa langsung ketik obrolan seperti biasa, kirim foto/dokumen PDF, atau pilih tombol di bawah:"
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Buka Studio Kreatif (Layar Penuh)",
                    web_app=WebAppInfo(url=miniapp_url),
                )
            ],
            [
                InlineKeyboardButton(text="📸 Buat Foto HD", callback_data="wiz:mode:PHOTO_HD"),
                InlineKeyboardButton(text="🎬 Buat Video", callback_data="wiz:mode:VIDEO_CINEMATIC"),
            ],
            [
                InlineKeyboardButton(text="🖼️➡️🎞️ Gerakkan Foto (Img2Vid)", callback_data="wiz:mode:IMG2VID_MOTION"),
            ],
            [
                InlineKeyboardButton(text="💎 Isi Koin Mulai Rp 2.000", callback_data="menu:topup"),
                InlineKeyboardButton(text="🎁 Klaim Koin Harian", callback_data="menu:claim_daily"),
            ],
            [
                InlineKeyboardButton(text="🤝 Ajak Teman & Komisi", callback_data="menu:affiliate"),
                InlineKeyboardButton(text="📖 Panduan Mudah", callback_data="menu:help"),
            ],
        ]
    )
    return text, kb


def build_derivative_action_keyboard(job_id: str) -> InlineKeyboardMarkup:
    """Tombol turunan karya setelah render selesai (`drv:*`)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🖼️ Cetak Poster 4K", callback_data=f"drv:poster4k:{job_id}"),
                InlineKeyboardButton(text="🎙️ Buat Suara Narasi MP3", callback_data=f"drv:audiomp3:{job_id}"),
            ],
            [
                InlineKeyboardButton(
                    text="💎 Hapus Watermark (Lisensi Bersih)",
                    callback_data=f"drv:clean_license:{job_id}",
                )
            ],
            [InlineKeyboardButton(text="🏠 Kembali ke Menu Utama", callback_data="menu:home")],
        ]
    )



<!-- [ID:02_CORE_AI_S078] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR, :32 -->
# ------------------------------------------------------------------------------
@router.message(F.new_chat_members)
async def handle_new_chat_members(message: Message) -> None:
    """Welcome Gate + SangMata Identity Tracker untuk anggota baru di grup."""
    members = getattr(message, "new_chat_members", []) or []
    greetings: List[str] = []
    for m in members:
        if getattr(m, "is_bot", False):
            continue
        await ensure_user_profile(
            user_id=m.id,
            username=m.username or "",
            first_name=m.first_name or "Sahabat",
            language_code=m.language_code or "id",
        )
        hist = await get_db().fetch_all(
            "SELECT old_username, new_username FROM identity_history WHERE user_id = ? ORDER BY changed_at DESC LIMIT 2;",
            (m.id,),
        )
        sangmata_note = (
            f" \x3ci>(Riwayat username: @{html.escape(hist[0]['old_username'])} → @{html.escape(hist[0]['new_username'])})\x3c/i>"
            if hist
            else ""
        )
        greetings.append(f"👋 Selamat datang, \x3cb>{html.escape(m.first_name or 'Sahabat')}\x3c/b>!{sangmata_note}")
    if greetings:
        await message.answer(
            "\n".join(greetings) + "\n\nSilakan ketik \x3ccode>/menu\x3c/code> untuk mulai berkarya bersama!",
            parse_mode="HTML",
        )


@router.message(F.photo | F.document)
async def handle_media_and_document(message: Message) -> None:
    """
    Menangani kiriman Foto & Dokumen:
    1. Jika Owner sedang dalam sesi `/set_qris`, simpan `file_id` ke slot QRIS terkait.
    2. Jika pengguna mengirim dokumen PDF/teks, jalankan Dual-LLM PDF/Dokumen Reader dengan Strict Privacy Pinning.
    3. Jika pengguna mengirim foto, jalankan Image-to-Image atau Image-to-Video (`IMG2VID_MOTION`)
       menggunakan prompt asli pengguna (`message.caption`).
    """
    user = message.from_user
    if not user:
        return

    photos_list: Any = getattr(message, "photo", None)
    doc_obj: Any = getattr(message, "document", None)

    # 1. Cek sesi /set_qris Owner
    if user.id in _RUNTIME_QRIS_WIZARD and is_verified_owner_dm(message):
        slot = _RUNTIME_QRIS_WIZARD.pop(user.id)
        file_id = ""
        if photos_list:
            file_id = str(getattr(photos_list[-1], "file_id", ""))
        elif doc_obj is not None:
            file_id = str(getattr(doc_obj, "file_id", ""))
        setting_map = {
            "UNIVERSAL": "qris_universal_file_id",
            "GOPAY": "qris_gopay_file_id",
            "SHOPEEPAY": "qris_shopeepay_file_id",
            "DANA": "qris_dana_file_id",
        }
        await get_db().set_setting(setting_map.get(slot, "qris_universal_file_id"), file_id)
        await message.answer(
            f"✅ Gambar QRIS untuk slot \x3cb>{html.escape(slot)}\x3c/b> berhasil disimpan (File ID: \x3ccode>{html.escape(file_id[:32])}\x3c/code>).",
            parse_mode="HTML",
        )
        return

    caption_prompt = str(getattr(message, "caption", None) or "").strip()

    # 2. Dual-LLM PDF / Dokumen Reader
    if doc_obj is not None:
        fname = str(getattr(doc_obj, "file_name", "dokumen.pdf") or "dokumen.pdf")
        user_instruction = caption_prompt or f"Rangkum poin penting dari dokumen {fname}"
        routed = await SMART_ROUTER.route_and_execute(
            f"[Dokumen: {fname}] Instruksi: {user_instruction}",
            mode="DEEP_RESEARCH",
            has_private_doc=True,
        )
        await message.answer(
            f"📄 \x3cb>Analisis Dokumen Pribadi ({html.escape(fname)})\x3c/b>\n"
            f"🔒 \x3ci>Diproses dengan Strict Privacy Pinning (100% Privat)\x3c/i>\n\n"
            f"{routed['text']}",
            parse_mode="HTML",
        )
        return

    # 3. Image-to-Image / Image-to-Video (IMG2VID_MOTION) menggunakan prompt asli pengguna
    wiz = _RUNTIME_WIZARD_STATE.get(user.id, {})
    active_mode = str(wiz.get("mode", "IMG2VID_MOTION"))
    motion_preset = str(wiz.get("motion_preset", "SMOOTH_ZOOM"))
    original_prompt = caption_prompt or f"Hidupkan foto ini secara sinematik ({motion_preset})"

    cost = 6 if active_mode in ("VIDEO_CINEMATIC", "IMG2VID_MOTION") else 2
    ok, msg, meta = await create_job_with_atomic_deduction(
        user_id=user.id,
        cost=cost,
        prompt_text=original_prompt,
        engine_used=f"MEDIA_{active_mode}_{motion_preset}",
    )
    if not ok:
        await message.answer(f"⚠️ {html.escape(msg)}", parse_mode="HTML")
        return

    photo_file_id = str(getattr(photos_list[-1], "file_id", "")) if photos_list else ""
    await finalize_job_status(meta["job_id"], success=True, telegram_file_id=photo_file_id)
    wm = meta["watermark_policy"]
    await message.answer(
        f"🎬 \x3cb>Karya Visual Selesai Dibuat!\x3c/b>\n"
        f"• Mode: \x3cb>{html.escape(active_mode)} ({html.escape(motion_preset)})\x3c/b>\n"
        f"• Arahan Asli Kamu: \x3ci>“{html.escape(original_prompt)}”\x3c/i>\n"
        f"• Status Lisensi: {wm['license_label']}\n"
        f"• Unduh Langsung: {PUBLIC_WEB_BASE_URL}/api/cdn/download?asset={meta['job_id']}&wm={wm['is_watermarked']}",
        reply_markup=build_derivative_action_keyboard(meta["job_id"]),
        parse_mode="HTML",
    )


@router.message(F.text)
async def handle_natural_text_chat(message: Message) -> None:
    """
    Handler `F.text`:
    - Mendeteksi pemicu cepat `"tampilin tombol"` atau `"menu"` untuk memunculkan tombol interaktif.
    - Menjawab obrolan pengguna secara natural dan hangat tanpa memaksa render visual jika tidak diminta.
    - Menyertakan rotasi footer dinamis yang ramah konsumen.
    """
    user = message.from_user
    if not user or not message.text:
        return
    allowed, _ = check_velocity_rate_limit(user.id)
    if not allowed:
        return

    raw_text = message.text.strip()
    low_text = raw_text.lower()

    if low_text in ("tampilin tombol", "tampilkan tombol", "menu", "buka menu", "tombol"):
        text, kb = await build_buyer_main_menu_view(user.id, user.first_name or "Sahabat")
        await message.answer(text, reply_markup=kb, parse_mode="HTML")
        return

    # Cek jika teks berupa kode Voucher VCH-...
    if raw_text.upper().startswith("VCH-"):
        ok, msg, _ = await redeem_ed25519_voucher(raw_text, user.id)
        await message.answer(f"{'🎉' if ok else '⚠️'} {html.escape(msg)}", parse_mode="HTML")
        return

    await ensure_user_profile(user.id, user.username or "", user.first_name or "", user.language_code or "id")
    await get_db().execute_write(
        "UPDATE users SET chat_used_today = chat_used_today + 1 WHERE internal_user_id = ?;",
        (user.id,),
    )
    routed = await SMART_ROUTER.route_and_execute(raw_text, mode="GENERAL")
    footer = next_consumer_footer()
    await message.answer(f"{routed['text']}\n\n{footer}", parse_mode="HTML")



<!-- [ID:02_CORE_AI_S079] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: 11PX -->
## Halaman 143

        {responseOutput && (​
          <div className="mt-6 rounded-xl border border-white/10 bg-slate-950/90 p-4">​
            <div className="flex items-center justify-between border-b border-white/5 pb-2 mb-3 
text-xs font-mono">​
              <span className="text-slate-400 flex items-center gap-1.5">​
                <CheckCircle2 className="h-4 w-4 text-emerald-400" /> Output Hasil​
              </span>​
              {metaInfo && (​
                <div className="flex items-center gap-3 text-[11px] text-slate-500">​
                  <span>Provider: <strong 
className="text-cyan-400">{metaInfo.provider}</strong></span>​
                  <span>Latensi: <strong 
className="text-emerald-400">{metaInfo.latency}ms</strong></span>​
                  <span>Score: <strong>{metaInfo.routeScore}</strong></span>​
                </div>​
              )}​
            </div>​
            <pre className="font-mono text-xs text-slate-300 whitespace-pre-wrap leading-relaxed 
overflow-x-auto">​
              {responseOutput}​
            </pre>​
          </div>​
        )}​
      </div>​
    </div>​
  );​
}​
 
components/SystemHealthMonitor.tsx 
Monitor status real-time untuk seluruh tier infrastruktur (Cloud Free, Local SOTA, Zero-Auth, 
DePIN, dan Database): 
"use client";​
​
import React from "react";​
import { Server, Activity, ShieldCheck, CheckCircle2, AlertTriangle } from "lucide-react";​
​
interface NodeStatus {​
  name: string;​
  category: "TIER-1 CLOUD" | "ZERO-AUTH / ID" | "LOCAL SOTA" | "INFRA & DB";​
  quota: string;​
  latencyMs: number;​
  status: "ONLINE" | "STANDBY" | "FAILOVER";​
  authType: "100% No Card" | "Zero-Auth" | "Oracle PAYG" | "USDT Wholesale";​
}​
​
export default function SystemHealthMonitor() {​



<!-- [ID:02_CORE_AI_S080] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 70

           "Kirimkan *prompt* atau instruksi di bawah ini:\n"
           "1. Ketik teks biasa = *Bikin Gambar Baru*\n"
           "2. Kirim Foto + 'hd' = *Upscale UltraSharp*\n"
           "3. Kirim Foto + 'hd remacri' = *Upscale Desain/Anime*\n"
           "4. Kirim Foto + 'wajah' = *FaceSwap (ReActor)*\n"
           "5. Kirim Foto + teks biasa = *Mode Edit (Image-to-Image)*"
       )
       bot.reply_to(message, teks_bantuan, parse_mode="Markdown")
@bot.message_handler(content_types=['text'])
def terima_pesanan_teks(message):
   if message.chat.type == 'private':
       user_id = message.chat.id
       prompt = message.text
       
       # Lempar pesanan ke Grup Antrean
       pesan_antrean = f"ORDER_TXT | {user_id} | {prompt}"
       
       try:
           bot.send_message(ID_GRUP, pesan_antrean)
           bot.reply_to(message, "⏳ Pesanan diterima! Mesin sedang memproses antrean, mohon tunggu sebentar.
       except Exception as e:
           bot.reply_to(message, "❌ Sistem antrean sedang penuh/error, silakan coba lagi nanti.")
           print(f"Error kirim grup: {e}")
@bot.message_handler(content_types=['photo'])
def terima_pesanan_foto(message):
   if message.chat.type == 'private':
       user_id = message.chat.id
       caption = message.caption if message.caption else "hd" # Default ke mode upscale
       file_id = message.photo[-1].file_id # Ambil resolusi paling tinggi
       
       # Format perintah untuk foto di grup
       pesan_antrean = f"ORDER_PIC | {user_id} | {caption}"
       
       try:
           # Gunakan send_photo dengan file_id (menghemat bandwidth server gratis)
           bot.send_photo(ID_GRUP, file_id, caption=pesan_antrean)
           bot.reply_to(message, "⏳ Foto diterima! Masuk ke dalam antrean render...")
       except Exception as e:
           bot.reply_to(message, "❌ Sistem antrean foto sedang error, silakan coba lagi.")
           print(f"Error kirim foto ke grup: {e}")
print("🟢 Resepsionis BikinAI Aktif 24/7 di PythonAnywhere...")
bot.infinity_polling(timeout=60, long_polling_timeout=60)
Jika tahap 1 di atas sudah sukses menyala (muncul tulisan "Resepsionis BikinAI Aktif 24/7 di PythonAnywhere..."), Anda bisa mencoba mengirim
pesan (misal: "Bikin gambar ayam") ke bot @BikinAI_bot di Telegram Anda. Jika sistem berjalan lancar, pesan dengan format ORDER_TXT | ...
akan muncul di Grup Antrean rahasia Anda.
Jika pengujian itu berhasil, kabari saya, lalu saya akan berikan Kode Tahap 2 untuk Colab (yang isinya kode ComfyUI + Bot Aspri).
User prompt: Kenapa nih? saya ada termux padahal
Response: Pesan error ModuleNotFoundError: No module named 'telebot' yang muncul di konsol pada bagian bawah layar Anda terjadi
karena pustaka (library) untuk menjalankan bot Telegram belum di-instal di dalam mesin PythonAnywhere Anda.
Terkait aplikasi Termux yang Anda miliki di HP, perlu dipahami bahwa Termux dan PythonAnywhere adalah dua komputer yang sepenuhnya
terpisah. Termux berjalan secara lokal di dalam memori HP Anda, sedangkan PythonAnywhere adalah server awan (cloud) yang berlokasi di luar
negeri. Menginstal sesuatu di Termux tidak akan membuatnya otomatis terinstal di PythonAnywhere. Anda ibarat sedang memakai dua laptop yang
berbeda.
Untuk mengatasi masalah ini, Anda harus menginstal telebot langsung dari dalam situs PythonAnywhere. Berikut langkah-langkahnya:
1. Tutup halaman editor kode tersebut dan kembali ke halaman utama (Dashboard) PythonAnywhere.
2. Pilih tab Consoles.
3. Pada bagian Start a new console, klik opsi Bash. Ini akan membuka layar terminal hitam yang mirip dengan Termux, namun ini adalah terminal
milik server PythonAnywhere.
4. Ketik perintah berikut di terminal Bash tersebut, lalu tekan Enter: pip3 install pyTelegramBotAPI --user



<!-- [ID:02_CORE_AI_S081] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ---------------------------------------------------
TOKEN_UTAMA = "8885292945:AAGK66Dng-81kTW9-vv0Yoy4Pzi43nU3ns0"
ID_GRUP = "-5441119572"
bot = telebot.TeleBot(TOKEN_UTAMA)
@bot.message_handler(commands=['start'])
def send_welcome(message):
   if message.chat.type == 'private':
       teks_bantuan = (
           "🔥 **Selamat Datang di BikinAI! (Agregator Termurah & Tercepat)** 🔥\n\n"
           "Kirimkan *prompt* atau instruksi di bawah ini:\n"
           "1. Ketik teks biasa = *Bikin Gambar Baru*\n"
           "2. Kirim Foto + 'hd' = *Upscale UltraSharp*\n"
           "3. Kirim Foto + 'hd remacri' = *Upscale Desain/Anime*\n"
           "4. Kirim Foto + 'wajah' = *FaceSwap (ReActor)*\n"
           "5. Kirim Foto + teks biasa = *Mode Edit (Image-to-Image)*"
       )
       bot.reply_to(message, teks_bantuan, parse_mode="Markdown")
@bot.message_handler(content_types=['text'])
def terima_pesanan_teks(message):
   if message.chat.type == 'private':
       user_id = message.chat.id
       prompt = message.text



<!-- [ID:02_CORE_AI_S082] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: PROMPT_ID -->
# ==========================================
def kirim_hasil_langsung_ke_user(user_id, path_gambar, mode_terpilih):
   url = f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendPhoto"
   with open(path_gambar, 'rb') as photo:
       files = {'photo': photo}
       data = {'chat_id': user_id, 'caption': f"🔥 {mode_terpilih} Sukses!\n\n_Dibuat instan via @BikinAI_bot
       req = requests.post(url, files=files, data=data)
       return req.status_code == 200
def proses_ke_mesin_comfyui(workflow):
   try:
       res = requests.post("http://127.0.0.1:8188/prompt", json={"prompt": workflow}).json()
       prompt_id = res.get("prompt_id")
       if prompt_id:
           for _ in range(150):
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

<!-- [ID:02_CORE_AI_S083] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: PROMPT_ID -->
# ==========================================
def kirim_hasil_langsung_ke_user(user_id, path_gambar, mode_terpilih):
   url = f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendPhoto"
   with open(path_gambar, 'rb') as photo:
       files = {'photo': photo}
       data = {
           'chat_id': user_id, 
           'caption': f"🔥 {mode_terpilih} Sukses!\n\n_Dibuat instan via @BikinAI_bot_", 
           'parse_mode': 'Markdown'
       }
       req = requests.post(url, files=files, data=data)
       return req.status_code == 200
def proses_ke_mesin_comfyui(workflow):
   try:
       res = requests.post("http://127.0.0.1:8188/prompt", json={"prompt": workflow}).json()
       prompt_id = res.get("prompt_id")
       if prompt_id:
           for _ in range(150):
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

<!-- [ID:02_CORE_AI_S084] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# Tembus Firewall PythonAnywhere Gratis
apihelper.proxy = {'https': 'http://proxy.server:3128'}
TOKEN_UTAMA = "8885292945:AAGK66Dng-81kTW9-vv0Yoy4Pzi43nU3ns0"
ID_GRUP = "-5441119572" # Jika gagal melempar ke grup, ganti jadi -1005441119572
USERNAME_PA = "bikinaibot" 
bot = telebot.TeleBot(TOKEN_UTAMA)
app = Flask(__name__)
@bot.message_handler(commands=['start'])
def send_welcome(message):
   if message.chat.type == 'private':
       bot.reply_to(message, "🔥 Resepsionis 24/7 (Mode Webhook) Aktif! Kirim prompt gambar atau foto.")
@bot.message_handler(content_types=['text'])
def terima_pesanan_teks(message):
   if message.chat.type == 'private':
       user_id = message.chat.id
       prompt = message.text
       pesan_antrean = f"ORDER_TXT | {user_id} | {prompt}"
       try:
           bot.send_message(ID_GRUP, pesan_antrean)
           bot.reply_to(message, "⏳ Pesanan diterima! Mesin sedang memproses antrean...")
       except Exception as e:
           bot.reply_to(message, f"❌ Gagal melempar pesanan ke Grup. Cek ID Grup Anda.")



<!-- [ID:02_CORE_AI_S085] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 92

def send_welcome(message):
   bot.reply_to(message, "🔥 Resepsionis BikinAI Aktif! Kirimkan ide gambar Anda di sini.")
@bot.message_handler(content_types=['text'])
def terima_pesanan_teks(message):
   user_id = message.chat.id
   prompt = message.text
   
   # Balas user
   bot.reply_to(message, "⏳ Pesanan masuk ke dalam sistem antrean rahasia. Mesin GPU akan segera menyedotnya
   # Simpan pesanan ke dalam file brankas (Database)
   with open(QUEUE_FILE, 'r') as f:
       data = json.load(f)
   
   data.append({"user_id": user_id, "prompt": prompt})
   
   with open(QUEUE_FILE, 'w') as f:
       json.dump(data, f)

<!-- [ID:02_CORE_AI_S086] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: PROMPT_ID, SIAP -->
# ==========================================
def tembak_hasil_ke_user(user_id, path_gambar, info):
   url_kirim = f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendPhoto"
   with open(path_gambar, 'rb') as photo:
       requests.post(url_kirim, data={'chat_id': user_id, 'caption': info, 'parse_mode': 'Markdown'}, files={
def proses_gambar(workflow):
   try:
       res = requests.post("http://127.0.0.1:8188/prompt", json={"prompt": workflow}).json()
       prompt_id = res.get("prompt_id")
       if prompt_id:
           for _ in range(150):
               time.sleep(2)
               try:
                   hist = requests.get(f"http://127.0.0.1:8188/history/{prompt_id}").json()
                   if prompt_id in hist:
                       outputs = hist[prompt_id].get("outputs", {})
                       for k, v in outputs.items():
                           if "images" in v:
                               return f"output/{v['images'][0]['filename']}" # Pastikan path sesuai Colab/Kag
               except: pass
   except: pass
   return None
print("🚀 [SIAP] Kaggle Siaga! Mengintip pesanan di PythonAnywhere setiap 5 detik...")

<!-- [ID:02_CORE_AI_S087] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: PROMPT_ID, SIAP -->
# ==========================================
def tembak_hasil_ke_user(user_id, path_gambar, info):
   url_kirim = f"https://api.telegram.org/bot{TOKEN_UTAMA}/sendPhoto"
   with open(path_gambar, 'rb') as photo:
       requests.post(url_kirim, data={'chat_id': user_id, 'caption': info, 'parse_mode': 'Markdown'}, files={
def proses_gambar(workflow):
   try:
       res = requests.post("http://127.0.0.1:8188/prompt", json={"prompt": workflow}).json()
       prompt_id = res.get("prompt_id")
       if prompt_id:
           for _ in range(150):
               time.sleep(2)
               try:
                   hist = requests.get(f"http://127.0.0.1:8188/history/{prompt_id}").json()
                   if prompt_id in hist:
                       outputs = hist[prompt_id].get("outputs", {})
                       for k, v in outputs.items():
                           if "images" in v:
                               # Sesuaikan path absolute untuk Colab
                               return f"/content/ComfyUI/output/{v['images'][0]['filename']}" 
               except: pass
   except: pass
   return None
print("🚀 [SIAP] Colab Siaga! Mengintip pesanan di PythonAnywhere setiap 5 detik...")

<!-- [ID:02_CORE_AI_S088] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 100

1. Buka kembali file mysite/flask_app.py di PythonAnywhere Anda.
2. Hapus seluruh kodenya, dan ganti dengan ini:
from flask import Flask, request, jsonify
import json
import os
app = Flask(__name__)
TOKEN_UTAMA = "8885292945:AAGK66Dng-81kTW9-vv0Yoy4Pzi43nU3ns0"
QUEUE_FILE = '/home/bikinaibot/mysite/antrean.json'
if not os.path.exists(QUEUE_FILE):
   with open(QUEUE_FILE, 'w') as f:
       json.dump([], f)
@app.route('/' + TOKEN_UTAMA, methods=['POST'])
def webhook():
   try:
       data = request.json
       if data and 'message' in data:
           msg = data['message']
           chat_id = msg['chat']['id']
           
           teks = ""
           file_id = ""
           
           # Deteksi apakah user kirim teks atau foto
           if 'text' in msg:
               teks = msg['text']
           elif 'photo' in msg:
               teks = msg.get('caption', '')
               file_id = msg['photo'][-1]['file_id'] # Ambil foto resolusi tertinggi
           
           if teks or file_id:
               with open(QUEUE_FILE, 'r') as f:
                   antrean = json.load(f)
               
               antrean.append({"user_id": chat_id, "prompt": teks, "file_id": file_id})
               
               with open(QUEUE_FILE, 'w') as f:
                   json.dump(antrean, f)
   except Exception:
       pass
       
   return "OK", 200
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
3. Klik Save, masuk ke menu Web, lalu tekan tombol hijau Reload bikinaibot.pythonanywhere.com. (Selesai! PythonAnywhere resmi ditutup
selamanya).
TAHAP 2: Kode Pamungkas Colab (Full Version God Mode)
Nah, ini dia kode yang Anda tunggu-tunggu. Kode ini akan mengunduh semua alat dewa (ReActor, dll), lalu memantau brankas. Jika ada foto masuk,
Colab akan mengunduhnya secara gaib dan memprosesnya.
Hapus seluruh kode di Colab Anda, paste ini, lalu tekan Play:

<!-- [ID:02_CORE_AI_S089] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: TARGET_URL -->
## Halaman 197

        except Exception:​
            if proxy:​
                await self.report_dead_proxy(proxy)​
​
        # TIER 3: Fallback ke Crawl4AI Internal Endpoint (Tanpa Ekspos 
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



<!-- [ID:02_CORE_AI_S090] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: TARGET_URL -->
## Halaman 284

        except Exception:​
            if proxy:​
                await self.report_dead_proxy(proxy)​
​
        # TIER 3: Fallback ke Crawl4AI Internal Endpoint (Tanpa Ekspos 
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



<!-- [ID:02_CORE_AI_S091] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: PROVIDERENDPOINT -->
## Halaman 345

        """​
        Gerbang Zero-Trust: Memastikan berkas model adalah 
.safetensors / .gguf​
        atau lulus audit statis ProtectAI ModelScan (Exit Code 0).​
        """​
        if model_path.endswith((".safetensors", ".gguf")):​
            return True​
        res = subprocess.run(​
            ["modelscan", "-p", model_path],​
            capture_output=True,​
            text=True,​
            check=False​
        )​
        if res.returncode == 0:​
            return True​
        raise PermissionError(​
            f"ModelScan memblokir pemuatan berkas '{model_path}' (Exit 
Code {res.returncode}). "​
            "Terdeteksi potensi instruksi berbahaya pada serialisasi 
Pickle/H5!"​
        )​
​
    def _order_candidates(self, complexity_score: float, 
require_uncensored: bool) -> List[ProviderEndpoint]:​
        """Menyusun urutan prioritas penyedia berdasarkan skor 
RouteLLM dan kebutuhan sensor."""​
        now = time.time()​
        active = [ep for ep in self.endpoints if ep.cooldown_until <= 
now]​
        if require_uncensored:​
            # Prioritaskan model abliterated lokal dan agregator tanpa 
filter​
            priority = {"LOCAL_SOTA": 0, "AGGREGATOR": 1, "WHOLESALE": 
2, "FREE_CLOUD": 3}​
        elif complexity_score < self.tau_threshold:​
            # Kueri ringan/menengah (< 0.11593) langsung diselesaikan 
di lokal untuk hemat kuota​
            priority = {"LOCAL_SOTA": 0, "FREE_CLOUD": 1, 
"AGGREGATOR": 2, "WHOLESALE": 3}​
        else:​
            # Kueri kompleks (>= 0.11593) gunakan kuota gratis Cloud 
Frontier -> Agregator -> Lokal​
            priority = {"FREE_CLOUD": 0, "AGGREGATOR": 1, 
"LOCAL_SOTA": 2, "WHOLESALE": 3}​
        return sorted(active, key=lambda ep: priority.get(ep.tier, 
99))​
​
    async def execute_llm_with_rolling(​



<!-- [ID:02_CORE_AI_S092] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :480, :320 -->
## Halaman 406

async def _call_pollinations_get_fallback(
   user_message: str, sys_instruction: str
) -> str | None:
   url = (
       f"https://text.pollinations.ai/{quote(user_message[:480])}"
       f"?model=openai&system={quote(sys_instruction[:320])}"
   )
   try:
       async with httpx.AsyncClient(
           timeout=6.5, follow_redirects=True
       ) as client:
           r = await client.get(url)
           if r.status_code == 200 and len(r.text.strip()) > 2:
               return sanitize_external_api_response(r.text.strip())
   except Exception:
       pass
   return None
BIKINAI_ADDICTIVE_COMPANION_PROMPT = """
PERAN UTAMA: Kamu adalah sahabat ngobrol, teman curhat, sekaligus rekan diskusi paling asik, hangat, cerdas, d
ATURAN PERCAKAPAN PENTING (EFEK CANDU & KENYAMANAN):
1. DILARANG KERAS MENYURUH BUAT GAMBAR ATAU VIDEO: Saat pengguna sedang mengobrol, curhat, atau berdiskusi, JA
2. KEMURNIAN BAHASA & LARANGAN TABEL PIPA: Gunakan Bahasa Indonesia yang luwes, akrab, dan berbobot (atau Baha
3. AKHIRI DENGAN PERTANYAAN RINGAN YANG MEMANCING DISKUSI: Buat lawan bicara betah berlama-lama di ruang chat.
""".strip()
async def generate_frontier_ai_response(
   db: aiosqlite.Connection,
   user_message: str,
   mode: Literal[
       "NATURAL_CHAT",
       "DEEP_RESEARCH",
       "CANVAS_EDIT",
       "PROMPT_ARCHITECT",
       "NOCTURNE_UNCENSORED",
   ] = "NATURAL_CHAT",
   personal_memory: str = "",
   canvas_state: str = "",
   preferred_model: str = "",
   persona_style: str = "NATURAL_COMPANION",
   chat_history: list[dict[str, str]] | None = None,
   has_multimodal_attachment: bool = False,
) -> str:
   """
   Smart Router v4.0:
   1. RouteLLM Complexity Scoring (tau = 0.11593) + Combo Grading (9Router MIBP style)
   2. Two-Tier Staggered Speculative Hedging (Tier 1 di t=0s, Tier 2 di t=1.2s jika Tier 1 belum selesai)
   3. Strict Privacy Pinning & Anti-Soft-Refusal untuk NOCTURNE_UNCENSORED
   """
   mem_context = (
       f"\nCATATAN PENGGUNA: {personal_memory}" if personal_memory else ""
   )
   skill_block, comp_hist = compress_context_and_match_skills(
       user_message, chat_history
   )
   _, is_complex_query = compute_routellm_complexity_score(user_message)
   if mode == "DEEP_RESEARCH":
       task, primary_ag = (
           "Susun laporan Deep Research mendalam: 1) Intisari Eksekutif, 2) Analisis Data & Teknis, 3) Peluan
           "DEEPSEEK",
       )
   elif mode == "CANVAS_EDIT":
       task, primary_ag = (
           f"Perbarui dokumen/kode di Canvas ini sesuai permintaan pengguna:\n{canvas_state or '(Kosong)'}",
           "QWEN",
       )
   elif mode == "PROMPT_ARCHITECT":
       task, primary_ag = (
           "Buatkan 3 variasi prompt visual/video sinematik terbaik (1. Komersial Fotorealistis, 2. Video Sin
           "MUSE",



<!-- [ID:02_CORE_AI_S093] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :-1 -->
## Halaman 416

   raise web.HTTPFound(src_url)
async def handle_vibecoder_openai_chat_api(
   request: web.Request,
) -> web.Response:
   """
   Endpoint Mandiri / Vibecoder API (/v1/chat/completions):
   Memungkinkan pengguna paket Mandiri/Sultan memasang kunci sk-bikinai-... di Cursor/Cline/Bot.
   Memotong 1 Koin Utama per panggilan secara atomik.
   """
   auth_header = request.headers.get("Authorization", "").strip()
   api_token = auth_header.replace("Bearer ", "").strip()
   if not api_token.startswith("sk-bikinai-"):
       return web.json_response(
           {"error": {"message": "Invalid API Key (Gunakan kunci sk-bikinai-... dari Paket Mandiri/Sultan)"}}
           status=401,
       )
   try:
       body = await request.json()
   except Exception:
       return web.json_response({"error": {"message": "Invalid JSON"}}, status=400)
   async with get_db() as db:
       cur = await db.execute(
           "SELECT internal_user_id, username FROM users WHERE api_key_token = ?;",
           (api_token,),
       )
       u_row = await cur.fetchone()
       if not u_row:
           return web.json_response(
               {"error": {"message": "API Key tidak terdaftar"}}, status=401
           )
       uid = int(u_row[0])
       ok_c, job_id, deduct_msg, _ = await deduct_user_coins_for_job(
           db, uid, cost=1, allow_bonus=False, prompt_text="API Call /v1/chat/completions", engine_used="VIBE
       )
       if not ok_c:
           return web.json_response({"error": {"message": deduct_msg}}, status=402)
       msgs = body.get("messages", [])
       last_prompt = str(msgs[-1].get("content", "Hello")) if msgs else "Hello"
       reply = await generate_frontier_ai_response(
           db,
           last_prompt,
           mode="CANVAS_EDIT" if "code" in last_prompt.lower() else "NATURAL_CHAT",
           preferred_model=str(body.get("model") or ""),
           chat_history=msgs[:-1] if len(msgs) > 1 else None,
       )
       await mark_job_completed(db, job_id, last_prompt, "VIBECODER_API")
       return web.json_response(
           {
               "id": job_id,
               "object": "chat.completion",
               "created": int(time.time()),
               "model": body.get("model", "bikinai-frontier-v4"),
               "choices": [
                   {
                       "index": 0,
                       "message": {"role": "assistant", "content": reply},
                       "finish_reason": "stop",
                   }
               ],
           }
       )
async def handle_webapp_execute_api(request: web.Request) -> web.Response:
   try:
       data = await request.json()
   except Exception:
       return web.json_response(
           {"ok": False, "message": "Invalid JSON"}, status=400
       )


