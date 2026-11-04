
<!-- [ID:02_CORE_AI_S018] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: TOPIK, IDX -->
# 9. WIZARD STATE, PRESET AWAM & CUSTOMER-FRIENDLY MENU BUILDERS
UPSCALER_WHITE_LABEL = {
    "PHOTO_FACE_4K": "🔍 Pertajam Foto & Wajah 4K",
    "TEXT_LINE_4K": "✨ Pertajam Teks & Gambar 4K",
    "VIDEO_4K_60FPS": "🎞️ Pertajam & Haluskan Video 4K 60FPS",
    "OFF": "Standar HD",
}

AWAM_VIDEO_MOTION_PRESETS = {
    "ZOOM_CINEMATIC": ("🎥 Kamera Zoom Sinematik", "smooth cinematic camera zoom-in, dramatic lighting, 60fps"),
    "ORBIT_360": ("🔄 Orbit Produk 360°", "360 degree orbital camera rotation around subject, studio spotlight"),
    "DANCE_FASHION": ("🕺 Gerakan Model & Dance", "fluid viral fashion model movement & natural choreography"),
    "SLOWMO_EPIC": ("🏃 Slow-Motion Epik", "epic slow-motion action, glowing atmosphere, high frame rate"),
}

AWAM_IMAGE_STYLE_PRESETS = {
    "UMKM_CATALOG": ("🛍️ Katalog Produk UMKM", "luxury commercial product photography, studio lighting, 8k"),
    "STUDIO_PORTRAIT": ("👔 Foto Profil Studio", "professional executive portrait, soft rim lighting, sharp focus"),
    "POSTER_THUMB": ("🎬 Poster & Thumbnail", "viral movie poster & YouTube thumbnail composition, vibrant colors"),
    "ANIME_PIXAR": ("🎌 Anime / 3D Pixar", "vibrant 3D Pixar & anime masterpiece illustration, volumetric light"),
}

IMAGE_EDITING_TOOLS = {
    "REMOVE_BG_PNG": ("✂️ Hapus Background (File PNG Transparan Kualitas Tinggi)", "Menghapus latar belakang foto dan mengirimkannya sebagai File Dokumen .PNG transparan utuh"),
    "IMG2VID_MOTION": ("🖼️➡️🎬 Gerakkan Foto Jadi Video (Image-to-Video)", "Menghidupkan foto produk atau potret wajah menjadi video sinematik bergerak"),
    "RETOUCH_FACE": ("✨ Retouch Wajah & Kulit Mulus", "Memperhalus tekstur kulit dan pencahayaan wajah secara alami"),
    "INPAINT_OBJ": ("🖌️ Ganti Baju / Ubah Objek", "Mengganti pakaian atau objek tertentu di dalam foto tanpa merusak latar"),
    "OUTPAINT_EXPAND": ("🖼️ Perluas Ukuran Foto", "Memperluas foto kotak 1:1 menjadi vertikal 9:16 atau melebar 16:9"),
    "PRODUCT_RELIGHT": ("📸 Studio Produk UMKM (Relighting)", "Mengubah foto produk rumahan menjadi foto katalog studio mewah"),
    "RESTORE_OLD": ("🕰️ Restorasi & Warnai Foto Lama", "Memperbaiki foto jadul yang buram menjadi tajam dan berwarna kembali"),
}

DYNAMIC_CHAT_FOOTERS = [
    "\n\n_💡 Tip: Kalau nanti ingin membuka menu tombol fitur, cukup ketik **\"menu\"** ya Kak 😊_",
    "\n\n_✨ Asik banget ngobrolnya! Kapan pun butuh tombol studio, tinggal ketik **\"tampilin tombol\"** ya._",
    "\n\n_📝 Tip: Kamu juga bisa ketik **`/riset [topik]`** untuk bedah mendalam atau **`/canvas`** untuk menyusun naskah panjang._",
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
        if self.modality in ("IMAGE", "EDIT_IMAGE") and self.edit_tool != "IMG2VID_MOTION":
            return 4, 0, True
        if RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] == 1 and not RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"]:
            return {5: 4, 10: 8, 30: 20}.get(self.duration_sec, 4), 0, True
        base_c = {5: 20, 10: 35, 30: 100}.get(self.duration_sec, 20)
        if self.video_engine in ("Kling 3.0 Pro", "Google Veo 3", "Sora 2 Turbo", "Runway Gen-4"):
            return int(base_c * 1.5), 950, False
        return base_c, 180, True


class BoundedSessionStore(OrderedDict):
    def __setitem__(self, key: Any, value: Any) -> None:
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if len(self) > 5000:
            self.popitem(last=False)


ACTIVE_DRAFTS: BoundedSessionStore = BoundedSessionStore()
WAITING_PROMPT_EDIT_USERS: set[int] = set()
router = Router()


def is_verified_owner_dm(user_id: int, chat_type: str) -> bool:
    return chat_type == "private" and int(RUNTIME_CONFIG.get("OWNER_ID_RUNTIME") or 0) > 0 and user_id == int(RUNTIME_CONFIG["OWNER_ID_RUNTIME"])


def build_customer_main_menu_keyboard(u: dict[str, Any] | None = None, is_private: bool = True) -> InlineKeyboardMarkup:
    today_str = time.strftime("%Y-%m-%d")
    already_claimed = u and (u.get("last_claim_date") == today_str or u.get("koin_bonus", 0) >= 25)
    claim_label = "🎁 Koin Harian Terklaim ✅" if already_claimed else "🎁 Klaim +4 Koin Gratis"
    ppp_zone = u.get("ppp_zone", 3) if u else 3
    topup_label = "💳 Isi Saldo & Paket VIP (QRIS Instan)" if ppp_zone == 3 else "💳 Top-Up & VIP Packs (USDT / Stars ⭐)"
    web_brand = RUNTIME_CONFIG.get("WEB_BRAND_NAME") or "AetherFree AI Studio"

    rows: list[list[InlineKeyboardButton]] = []
    m_url = RUNTIME_CONFIG["MINIAPP_URL"]
    if m_url.startswith("https://"):
        if is_private:
            rows.append([InlineKeyboardButton(text="📱 Buka Super Mini App Studio (Full Web & Upload)", web_app=WebAppInfo(url=m_url))])
        else:
            rows.append([InlineKeyboardButton(text="📱 Buka Super Mini App Studio (via DM Bot)", url=f"https://t.me/{BOT_USERNAME_GLOBAL}?start=miniapp")])
    else:
        rows.append([InlineKeyboardButton(text="📱 Buka Super Mini App Studio (Panduan Link)", callback_data="menu:miniapp_guide")])

    rows.extend([
        [InlineKeyboardButton(text="🎬 Studio Video & Img2Vid", callback_data="menu:wizard_video"), InlineKeyboardButton(text="🎨 Studio Gambar 4K", callback_data="menu:wizard_image")],
        [InlineKeyboardButton(text="🛠️ Editing & Hapus BG (.PNG)", callback_data="menu:wizard_edit"), InlineKeyboardButton(text="🪄 Arsitek Prompt AI", callback_data="menu:prompt_helper")],
        [InlineKeyboardButton(text="🔬 Deep Research (/riset)", callback_data="menu:deep_research_hint"), InlineKeyboardButton(text="📝 Canvas Workspace (/canvas)", callback_data="menu:canvas_hint")],
        [InlineKeyboardButton(text=f"🌐 Buka {web_brand} (Web Bebas & Kode VIP)", callback_data="menu:unfiltered_external_referral")],
        [InlineKeyboardButton(text="📊 Status Kuota Harian", callback_data="menu:quota"), InlineKeyboardButton(text=claim_label, callback_data="menu:claim_daily")],
        [InlineKeyboardButton(text=topup_label, callback_data="menu:topup_qris"), InlineKeyboardButton(text="🎧 Bantuan & Garansi Koin 100%", callback_data="menu:live_support")],
        [InlineKeyboardButton(text="📜 Panduan Prompt, FAQ, Ketentuan & Grup", callback_data="menu:faq_tos")],
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_customer_dashboard_caption(username: str, u: dict[str, Any]) -> str:
    tier_badge = "🌟 KREATOR PRO" if u["has_topped_up"] else "⚡ KREATOR EKSPLORER"
    hh_banner = "\n🎉 **FLASH HAPPY HOUR AKTIF: SEMUA PEMBUATAN KARYA GRATIS 0 KOIN!** 🎉\n" if RUNTIME_CONFIG["HAPPY_HOUR_MODE"] else ""
    safe_u = u.get("safe_uname") or username
    return (
        f"┏━━━ ⚡ **bikinAI SUPER INTELLIGENCE** ⚡ ━━━┓\n"
        f"┃ 👤 **Kreator:** `@{safe_u}`\n"
        f"┃ 🏅 **Status:** `{tier_badge}`\n"
        f"┣━━━━━━━━━━━━━━━━━━━━━━━┫\n"
        f"┃ 💎 **Koin Utama:** `{u['koin_utama']} Koin`\n"
        f"┃ 🎁 **Koin Bonus:** `{u['koin_bonus']}/{MAX_KOIN_BONUS_CAP} Koin`\n"
        f"┃ 💬 **Teman Diskusi AI 24 Jam:** `🟢 AKTIF (Gratis)`\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━┛{hh_banner}\n\n"
        f"✨ **Selamat datang di Studio Kreatif AI Generasi Baru.**\n"
        f"▸ Ketik apa saja di ruang chat untuk mengobrol santai, atau gunakan tombol studio di bawah ini:"
    )


def build_400_percent_derivative_upsell_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🖼️ Ambil Poster Thumbnail 4K (+4 Koin)", callback_data="drv:poster4k"), InlineKeyboardButton(text="🎵 Ekstrak Audio MP3 (+4 Koin)", callback_data="drv:audiomp3")],
            [InlineKeyboardButton(text="✨ Buka Lisensi Komersial Bersih Tanpa Watermark (+10 Koin)", callback_data="drv:clean_license")],
            [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
        ]
    )


def build_video_wizard_kb(session: LiveWizardSession, show_more: bool = False) -> tuple[str, InlineKeyboardMarkup]:
    if session.upscale_mode in ("PHOTO_FACE_4K", "TEXT_LINE_4K"):
        session.upscale_mode = "VIDEO_4K_60FPS"
    coins, _, _ = session.get_pricing()
    ups_label = UPSCALER_WHITE_LABEL.get(session.upscale_mode, "🎞️ Pertajam & Haluskan Video 4K 60FPS")
    preset_info = f"\n┣ 🎬 **Preset Gerakan (Motion):** `{session.awam_preset}`" if session.awam_preset else ""
    text = (
        f"🎬 **STUDIO VIDEO AI & FOTO JADI VIDEO — bikinAI**\n━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Konsep Video:**\n> _{session.prompt}_\n\n"
        f"┣ ⚡ **Mesin AI Video:** **`{session.video_engine}`**{preset_info}\n"
        f"┣ 📐 **Ukuran Layar:** `{session.aspect_ratio}` | ⏱️ **Durasi:** `{session.duration_sec} Detik`\n"
        f"┗ 🔍 **Kualitas Video:** `{ups_label}`\n━━━━━━━━━━━━━━━━━━\n"
        f"💡 _Tip: Kirim **Foto Produk/Wajah** langsung ke ruang chat jika ingin mengubah foto menjadi video!_\n"
        f"💎 **Biaya:** **`{coins} Koin`** _(Garansi Koin Kembali 100%)_"
    )
    rows = [
        [InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='9:16' else ''}📱 9:16 TikTok", callback_data="wiz:ar:9:16"), InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='16:9' else ''}🖥️ 16:9 YouTube", callback_data="wiz:ar:16:9"), InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='1:1' else ''}🟦 1:1 Feed", callback_data="wiz:ar:1:1")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.duration_sec==5 else ''}⚡ 5 Detik", callback_data="wiz:dur:5"), InlineKeyboardButton(text=f"{'✅ ' if session.duration_sec==10 else ''}🔥 10 Detik", callback_data="wiz:dur:10"), InlineKeyboardButton(text=f"{'✅ ' if session.duration_sec==30 else ''}🎬 30s Story", callback_data="wiz:dur:30")],
        [InlineKeyboardButton(text="🎥 Motion: Zoom Sinematik", callback_data="wiz:vpre:ZOOM_CINEMATIC"), InlineKeyboardButton(text="🔄 Motion: Orbit 360°", callback_data="wiz:vpre:ORBIT_360")],
        [InlineKeyboardButton(text="🕺 Motion: Model/Dance", callback_data="wiz:vpre:DANCE_FASHION"), InlineKeyboardButton(text="🏃 Motion: Slow-Mo Epik", callback_data="wiz:vpre:SLOWMO_EPIC")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Kling 3.0 Pro' else ''}🟣 Kling 3.0 Pro", callback_data="wiz:veng:Kling 3.0 Pro"), InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Seedance 2.0' else ''}🕺 Seedance 2.0", callback_data="wiz:veng:Seedance 2.0")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Wan 2.2 Pro' else ''}🔵 Wan 2.2 Pro", callback_data="wiz:veng:Wan 2.2 Pro"), InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Google Veo 3' else ''}🎥 Google Veo 3", callback_data="wiz:veng:Google Veo 3")],
    ]
    if show_more:
        rows.extend([
            [InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Sora 2 Turbo' else ''}🌌 Sora 2 Turbo", callback_data="wiz:veng:Sora 2 Turbo"), InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Runway Gen-4' else ''}🎞️ Runway Gen-4", callback_data="wiz:veng:Runway Gen-4")],
            [InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Hailuo MiniMax H3' else ''}🎭 Hailuo MiniMax H3", callback_data="wiz:veng:Hailuo MiniMax H3"), InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='LTX-2.3 Fast' else ''}🟢 LTX-2.3 Fast", callback_data="wiz:veng:LTX-2.3 Fast")],
            [InlineKeyboardButton(text="🔼 Sembunyikan AI Video Lainnya", callback_data="wiz:more_vid:0")],
        ])
    else:
        rows.append([InlineKeyboardButton(text="➕ Pilihan AI Video Lainnya (Sora 2, Runway, MiniMax, LTX)", callback_data="wiz:more_vid:1")])

    rows.extend([
        [InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='VIDEO_4K_60FPS' else ''}🎞️ Pertajam & Haluskan Video 4K 60FPS", callback_data="wiz:ups:VIDEO_4K_60FPS"), InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='OFF' else ''}⚡ Standar HD Cepat", callback_data="wiz:ups:OFF")],
        [InlineKeyboardButton(text="✏️ Ubah Konsep / Deskripsi Video", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 MULAI BUAT VIDEO ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ])
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def build_image_wizard_kb(session: LiveWizardSession, show_more: bool = False) -> tuple[str, InlineKeyboardMarkup]:
    if session.upscale_mode == "VIDEO_4K_60FPS":
        session.upscale_mode = "PHOTO_FACE_4K"
    coins, _, _ = session.get_pricing()
    ups_label = UPSCALER_WHITE_LABEL.get(session.upscale_mode, "🔍 Pertajam Foto & Wajah 4K")
    preset_info = f"\n┣ 🎨 **Preset Gaya Awam:** `{session.awam_preset}`" if session.awam_preset else ""
    text = (
        f"🎨 **STUDIO GAMBAR 4K — bikinAI**\n━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Deskripsi Gambar:**\n> _{session.prompt}_\n\n"
        f"┣ ⚡ **Mesin AI Gambar:** **`{session.image_engine}`**{preset_info}\n"
        f"┣ 📐 **Ukuran Layar:** `{session.aspect_ratio}`\n"
        f"┗ 🔍 **Penajaman:** `{ups_label}`\n━━━━━━━━━━━━━━━━━━\n"
        f"💎 **Biaya:** **`{coins} Koin`** _(Garansi Koin Kembali 100%)_"
    )
    rows = [
        [InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='9:16' else ''}📱 9:16", callback_data="wiz:ar:9:16"), InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='1:1' else ''}🟦 1:1", callback_data="wiz:ar:1:1"), InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='16:9' else ''}🖥️ 16:9", callback_data="wiz:ar:16:9")],
        [InlineKeyboardButton(text="🛍️ Gaya: Katalog UMKM", callback_data="wiz:ipre:UMKM_CATALOG"), InlineKeyboardButton(text="👔 Gaya: Foto Studio", callback_data="wiz:ipre:STUDIO_PORTRAIT")],
        [InlineKeyboardButton(text="🎬 Gaya: Poster/Thumb", callback_data="wiz:ipre:POSTER_THUMB"), InlineKeyboardButton(text="🎌 Gaya: Anime/3D Pixar", callback_data="wiz:ipre:ANIME_PIXAR")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Seedream 4.5' else ''}✨ Seedream 4.5", callback_data="wiz:ieng:Seedream 4.5"), InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Flux.1 Dev' else ''}📸 Flux.1 Dev", callback_data="wiz:ieng:Flux.1 Dev")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Midjourney v7' else ''}🎨 Midjourney v7", callback_data="wiz:ieng:Midjourney v7"), InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Ideogram v3' else ''}🔤 Ideogram v3 (Teks)", callback_data="wiz:ieng:Ideogram v3")],
    ]
    if show_more:
        rows.extend([
            [InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Recraft V3' else ''}📐 Recraft V3 (Logo)", callback_data="wiz:ieng:Recraft V3"), InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Illustrious XL' else ''}🎌 Illustrious XL", callback_data="wiz:ieng:Illustrious XL")],
            [InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='NoobAI-XL' else ''}🌟 NoobAI-XL", callback_data="wiz:ieng:NoobAI-XL"), InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Juggernaut XL' else ''}📷 Juggernaut XL", callback_data="wiz:ieng:Juggernaut XL")],
            [InlineKeyboardButton(text="🔼 Sembunyikan AI Gambar Lainnya", callback_data="wiz:more_img:0")],
        ])
    else:
        rows.append([InlineKeyboardButton(text="➕ Pilihan AI Gambar Lainnya (Recraft Logo, Illustrious, NoobAI)", callback_data="wiz:more_img:1")])

    rows.extend([
        [InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='PHOTO_FACE_4K' else ''}🔍 Pertajam Foto & Wajah 4K", callback_data="wiz:ups:PHOTO_FACE_4K"), InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='TEXT_LINE_4K' else ''}✨ Pertajam Teks & Gambar 4K", callback_data="wiz:ups:TEXT_LINE_4K")],
        [InlineKeyboardButton(text="🛠️ Buka Menu Editing, Foto Jadi Video & Hapus BG (.PNG)", callback_data="menu:wizard_edit")],
        [InlineKeyboardButton(text="✏️ Ubah Deskripsi Gambar", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 MULAI BUAT GAMBAR ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ])
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def build_editing_tools_wizard_kb(session: LiveWizardSession) -> tuple[str, InlineKeyboardMarkup]:
    coins, _, _ = session.get_pricing()
    tool_title, tool_desc = IMAGE_EDITING_TOOLS.get(session.edit_tool, IMAGE_EDITING_TOOLS["REMOVE_BG_PNG"])
    text = (
        f"🛠️ **STUDIO EDITING, HAPUS BG & FOTO JADI VIDEO — bikinAI**\n━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **Fitur Terpilih:** **`{tool_title}`**\n"
        f"ℹ️ **Fungsi:** _{tool_desc}_\n"
        f"📝 **Instruksi:** _{session.prompt}_\n━━━━━━━━━━━━━━━━━━\n"
        f"💡 _Khusus Hapus Background, hasil dikirim sebagai **File PNG Transparan Kualitas Tinggi**!_"
    )
    rows = [
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='REMOVE_BG_PNG' else ''}✂️ Hapus Background (File PNG Transparan)", callback_data="wiz:etool:REMOVE_BG_PNG")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='IMG2VID_MOTION' else ''}🖼️➡️🎬 Gerakkan Foto Jadi Video (Image-to-Video)", callback_data="wiz:etool:IMG2VID_MOTION")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='RETOUCH_FACE' else ''}✨ Retouch Wajah", callback_data="wiz:etool:RETOUCH_FACE"), InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='INPAINT_OBJ' else ''}🖌️ Ganti Baju / Objek", callback_data="wiz:etool:INPAINT_OBJ")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='OUTPAINT_EXPAND' else ''}🖼️ Perluas Ukuran Foto", callback_data="wiz:etool:OUTPAINT_EXPAND"), InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='PRODUCT_RELIGHT' else ''}📸 Studio Produk UMKM", callback_data="wiz:etool:PRODUCT_RELIGHT")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='RESTORE_OLD' else ''}🕰️ Restorasi & Warnai Foto Lama", callback_data="wiz:etool:RESTORE_OLD")],
        [InlineKeyboardButton(text="✏️ Ubah Instruksi / Objek Editing", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 PROSES SEKARANG ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ]
    return text, InlineKeyboardMarkup(inline_keyboard=rows)



<!-- [ID:02_CORE_AI_S019] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: TOPIK, IDX -->
# ==============================================================================
UPSCALER_WHITE_LABEL = {
    "PHOTO_FACE_4K": "🔍 Pertajam Foto & Wajah 4K",
    "TEXT_LINE_4K": "✨ Pertajam Teks & Gambar 4K",
    "VIDEO_4K_60FPS": "🎞️ Pertajam & Haluskan Video 4K 60FPS",
    "OFF": "Standar HD",
}

IMAGE_EDITING_TOOLS = {
    "REMOVE_BG_PNG": (
        "✂️ Hapus Background (File PNG Transparan Kualitas Tinggi)",
        "Menghapus latar belakang foto dan mengirimkannya sebagai File Dokumen .PNG transparan utuh",
    ),
    "RETOUCH_FACE": (
        "✨ Retouch Wajah & Kulit Mulus",
        "Memperhalus tekstur kulit dan pencahayaan wajah secara alami",
    ),
    "INPAINT_OBJ": (
        "🖌️ Inpainting (Ganti Baju / Ubah Objek)",
        "Mengganti pakaian atau objek tertentu di dalam foto tanpa merusak latar",
    ),
    "OUTPAINT_EXPAND": (
        "🖼️ Outpainting (Perluas Ukuran Foto)",
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
    "\n\n_💡 Kalau nanti butuh tombol menu interaktif, tinggal ketik **\"tampilin tombol\"** ya Kak 😊_",
    "\n\n_✨ Nyaman ngobrol dulu aja Kak. Kapan pun mau buka studio visual, cukup ketik **\"menu\"** ya!_",
    "\n\n_⚡ Kalau ide di atas mau langsung kita ubah jadi karya visual, tinggal bilang **\"tampilin tombol\"** aja ya Kak._",
    "\n\n_📝 Tip: Ketik **`/canvas`** kalau mau menyusun draf panjang, atau ketik **\"menu\"** untuk melihat fitur lainnya 😊_",
    "\n\n_🔬 Butuh bedah riset yang lebih mendalam? Cukup ketik **`/riset [topik]`** atau **\"tampilin tombol\"** kapan saja ya!_",
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

    def get_pricing(self) -> tuple[int, int, bool]:
        if RUNTIME_CONFIG["HAPPY_HOUR_MODE"]:
            return 0, 0, True
        if self.modality in ("IMAGE", "EDIT_IMAGE"):
            return 4, 0, True
        if RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] == 1 and not RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"]:
            base_c = {5: 4, 10: 8, 30: 20}.get(self.duration_sec, 4)
            return base_c, 0, True
        base_c = {5: 20, 10: 35, 30: 100}.get(self.duration_sec, 20)
        if self.video_engine in ("Kling 3.0 Pro", "Google Veo 3", "Sora 2 Turbo", "Runway Gen-4"):
            return int(base_c * 1.5), 950, False
        return base_c, 180, True


class BoundedSessionStore(OrderedDict):
    def __setitem__(self, key: Any, value: Any) -> None:
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if len(self) > 5000:
            self.popitem(last=False)


ACTIVE_DRAFTS: BoundedSessionStore = BoundedSessionStore()
WAITING_PROMPT_EDIT_USERS: set[int] = set()
router = Router()


def is_verified_owner_dm(user_id: int, chat_type: str) -> bool:
    """[PATCH AUDIT-03]: Mencegah pengambilalihan Owner otomatis jika ADMIN_USER_ID belum diisi."""
    if chat_type != "private":
        return False
    owner_id = int(RUNTIME_CONFIG.get("OWNER_ID_RUNTIME") or 0)
    return owner_id > 0 and user_id == owner_id


def build_customer_main_menu_keyboard(u: dict[str, Any] | None = None, is_private: bool = True) -> InlineKeyboardMarkup:
    today_str = time.strftime("%Y-%m-%d")
    already_claimed = u and (u.get("last_claim_date") == today_str or u.get("koin_bonus", 0) >= 25)
    claim_label = "🎁 Koin Harian Terklaim ✅" if already_claimed else "🎁 Klaim +4 Koin Gratis"
    ppp_zone = u.get("ppp_zone", 3) if u else 3
    topup_label = "💳 Isi Saldo (Pembayaran QRIS Instan)" if ppp_zone == 3 else "💳 Top-Up Coins (USDT / Stars ⭐)"

    rows: list[list[InlineKeyboardButton]] = []
    m_url = RUNTIME_CONFIG["MINIAPP_URL"]
    if m_url.startswith("https://"):
        if is_private:
            rows.append([
                InlineKeyboardButton(
                    text="📱 Buka Super Mini App Studio (Full Web & Upload)",
                    web_app=WebAppInfo(url=m_url),
                )
            ])
        else:
            rows.append([
                InlineKeyboardButton(
                    text="📱 Buka Super Mini App Studio (via DM Bot)",
                    url=f"https://t.me/{BOT_USERNAME_GLOBAL}?start=miniapp",
                )
            ])
    else:
        rows.append([
            InlineKeyboardButton(
                text="📱 Buka Super Mini App Studio (Panduan Link)",
                callback_data="menu:miniapp_guide",
            )
        ])

    rows.extend([
        [
            InlineKeyboardButton(text="🎬 Studio Video AI", callback_data="menu:wizard_video"),
            InlineKeyboardButton(text="🎨 Studio Gambar 4K", callback_data="menu:wizard_image"),
        ],
        [
            InlineKeyboardButton(text="🛠️ Editing & Hapus BG (.PNG)", callback_data="menu:wizard_edit"),
            InlineKeyboardButton(text="🪄 Arsitek Prompt AI", callback_data="menu:prompt_helper"),
        ],
        [
            InlineKeyboardButton(text="🔬 Deep Research (/riset)", callback_data="menu:deep_research_hint"),
            InlineKeyboardButton(text="📝 Canvas Workspace (/canvas)", callback_data="menu:canvas_hint"),
        ],
        [
            InlineKeyboardButton(
                text="🌐 Studio Web Independen (NocturneAI) & Kode Voucher",
                callback_data="menu:unfiltered_external_referral",
            )
        ],
        [
            InlineKeyboardButton(text="📊 Status Kuota Harian", callback_data="menu:quota"),
            InlineKeyboardButton(text=claim_label, callback_data="menu:claim_daily"),
        ],
        [
            InlineKeyboardButton(text=topup_label, callback_data="menu:topup_qris"),
            InlineKeyboardButton(text="🎧 Bantuan & Garansi Koin 100%", callback_data="menu:live_support"),
        ],
        [
            InlineKeyboardButton(text="📜 Panduan, FAQ, Ketentuan & Topik Grup", callback_data="menu:faq_tos"),
        ],
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_customer_dashboard_caption(username: str, u: dict[str, Any]) -> str:
    tier_badge = "🌟 KREATOR PRO" if u["has_topped_up"] else "⚡ KREATOR EKSPLORER"
    hh_banner = "\n🎉 **FLASH HAPPY HOUR AKTIF: SEMUA RENDER GRATIS 0 KOIN!** 🎉\n" if RUNTIME_CONFIG["HAPPY_HOUR_MODE"] else ""
    safe_u = u.get("safe_uname") or username
    return (
        f"┏━━━ ⚡ **bikinAI SUPER INTELLIGENCE** ⚡ ━━━┓\n"
        f"┃ 👤 **Kreator:** `@{safe_u}`\n"
        f"┃ 🏅 **Status:** `{tier_badge}`\n"
        f"┣━━━━━━━━━━━━━━━━━━━━━━━┫\n"
        f"┃ 💎 **Koin Utama:** `{u['koin_utama']} Koin`\n"
        f"┃ 🎁 **Koin Bonus:** `{u['koin_bonus']}/{MAX_KOIN_BONUS_CAP} Koin`\n"
        f"┃ 🤖 **Asisten AI 24 Jam:** `🟢 AKTIF (Gratis)`\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━┛{hh_banner}\n\n"
        f"✨ **Selamat datang di Studio Kreatif AI Generasi Baru.**\n"
        f"▸ Klik **`📱 Buka Super Mini App Studio`** di atas untuk tampilan web penuh, atau pilih menu cepat di bawah:"
    )


def build_400_percent_derivative_upsell_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🖼️ Ambil Poster Thumbnail 4K (+4 Koin)", callback_data="drv:poster4k"),
                InlineKeyboardButton(text="🎵 Ekstrak Audio MP3 (+4 Koin)", callback_data="drv:audiomp3"),
            ],
            [
                InlineKeyboardButton(text="✨ Buka Lisensi Komersial Bersih Tanpa Watermark (+10 Koin)", callback_data="drv:clean_license"),
            ],
            [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
        ]
    )


def build_video_wizard_kb(session: LiveWizardSession, show_more: bool = False) -> tuple[str, InlineKeyboardMarkup]:
    coins, _, _ = session.get_pricing()
    ups_label = UPSCALER_WHITE_LABEL.get(session.upscale_mode, "🎞️ Pertajam & Haluskan Video 4K 60FPS")
    text = (
        f"🎬 **STUDIO VIDEO AI — bikinAI**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Konsep Video:**\n> _{session.prompt}_\n\n"
        f"┣ ⚡ **Mesin AI Video:** **`{session.video_engine}`**\n"
        f"┣ 📐 **Ukuran Layar:** `{session.aspect_ratio}` | ⏱️ **Durasi:** `{session.duration_sec} Detik`\n"
        f"┗ 🔍 **Kualitas:** `{ups_label}`\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💎 **Biaya:** **`{coins} Koin`** _(Garansi Koin Kembali 100%)_"
    )
    rows = [
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='9:16' else ''}📱 9:16 TikTok", callback_data="wiz:ar:9:16"),
            InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='16:9' else ''}🖥️ 16:9 YouTube", callback_data="wiz:ar:16:9"),
            InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='1:1' else ''}🟦 1:1 Feed", callback_data="wiz:ar:1:1"),
        ],
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.duration_sec==5 else ''}⚡ 5 Detik", callback_data="wiz:dur:5"),
            InlineKeyboardButton(text=f"{'✅ ' if session.duration_sec==10 else ''}🔥 10 Detik", callback_data="wiz:dur:10"),
            InlineKeyboardButton(text=f"{'✅ ' if session.duration_sec==30 else ''}🎬 30s Story", callback_data="wiz:dur:30"),
        ],
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Kling 3.0 Pro' else ''}🟣 Kling 3.0 Pro", callback_data="wiz:veng:Kling 3.0 Pro"),
            InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Seedance 2.0' else ''}🕺 Seedance 2.0", callback_data="wiz:veng:Seedance 2.0"),
        ],
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Wan 2.2 Pro' else ''}🔵 Wan 2.2 Pro", callback_data="wiz:veng:Wan 2.2 Pro"),
            InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Google Veo 3' else ''}🎥 Google Veo 3", callback_data="wiz:veng:Google Veo 3"),
        ],
    ]
    if show_more:
        rows.extend([
            [
                InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Sora 2 Turbo' else ''}🌌 Sora 2 Turbo", callback_data="wiz:veng:Sora 2 Turbo"),
                InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Runway Gen-4' else ''}🎞️ Runway Gen-4", callback_data="wiz:veng:Runway Gen-4"),
            ],
            [
                InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Hailuo MiniMax H3' else ''}🎭 Hailuo MiniMax H3", callback_data="wiz:veng:Hailuo MiniMax H3"),
                InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='LTX-2.3 Fast' else ''}🟢 LTX-2.3 Fast", callback_data="wiz:veng:LTX-2.3 Fast"),
            ],
            [InlineKeyboardButton(text="🔼 Sembunyikan AI Video Lainnya", callback_data="wiz:more_vid:0")],
        ])
    else:
        rows.append([InlineKeyboardButton(text="➕ Pilihan AI Video Lainnya (Sora 2, Runway, MiniMax, LTX)", callback_data="wiz:more_vid:1")])

    rows.extend([
        [
            InlineKeyboardButton(
                text=f"{'✅ ' if session.upscale_mode=='VIDEO_4K_60FPS' else ''}🎞️ Pertajam & Haluskan Video 4K 60FPS",
                callback_data="wiz:ups:VIDEO_4K_60FPS",
            )
        ],
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='PHOTO_FACE_4K' else ''}🔍 Pertajam Wajah 4K", callback_data="wiz:ups:PHOTO_FACE_4K"),
            InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='TEXT_LINE_4K' else ''}✨ Pertajam Detail 4K", callback_data="wiz:ups:TEXT_LINE_4K"),
        ],
        [InlineKeyboardButton(text="✏️ Ubah Konsep / Deskripsi Video", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 MULAI BUAT VIDEO ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ])
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def build_image_wizard_kb(session: LiveWizardSession, show_more: bool = False) -> tuple[str, InlineKeyboardMarkup]:
    coins, _, _ = session.get_pricing()
    ups_label = UPSCALER_WHITE_LABEL.get(session.upscale_mode, "🔍 Pertajam Foto & Wajah 4K")
    text = (
        f"🎨 **STUDIO GAMBAR 4K — bikinAI**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Deskripsi Gambar:**\n> _{session.prompt}_\n\n"
        f"┣ ⚡ **Mesin AI Gambar:** **`{session.image_engine}`**\n"
        f"┣ 📐 **Ukuran Layar:** `{session.aspect_ratio}`\n"
        f"┗ 🔍 **Penajaman:** `{ups_label}`\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💎 **Biaya:** **`{coins} Koin`** _(Garansi Koin Kembali 100%)_"
    )
    rows = [
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='9:16' else ''}📱 9:16", callback_data="wiz:ar:9:16"),
            InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='1:1' else ''}🟦 1:1", callback_data="wiz:ar:1:1"),
            InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='16:9' else ''}🖥️ 16:9", callback_data="wiz:ar:16:9"),
        ],
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Seedream 4.5' else ''}✨ Seedream 4.5", callback_data="wiz:ieng:Seedream 4.5"),
            InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Flux.1 Dev' else ''}📸 Flux.1 Dev", callback_data="wiz:ieng:Flux.1 Dev"),
        ],
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Midjourney v7' else ''}🎨 Midjourney v7", callback_data="wiz:ieng:Midjourney v7"),
            InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Ideogram v3' else ''}🔤 Ideogram v3 (Teks)", callback_data="wiz:ieng:Ideogram v3"),
        ],
    ]
    if show_more:
        rows.extend([
            [
                InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Recraft V3' else ''}📐 Recraft V3 (Logo)", callback_data="wiz:ieng:Recraft V3"),
                InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Illustrious XL' else ''}🎌 Illustrious XL (Anime)", callback_data="wiz:ieng:Illustrious XL"),
            ],
            [
                InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Pony V6 Realism' else ''}🌟 Pony V6 Realism", callback_data="wiz:ieng:Pony V6 Realism"),
                InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='SD 3.5 Large' else ''}🖼️ SD 3.5 Large", callback_data="wiz:ieng:SD 3.5 Large"),
            ],
            [InlineKeyboardButton(text="🔼 Sembunyikan AI Gambar Lainnya", callback_data="wiz:more_img:0")],
        ])
    else:
        rows.append([InlineKeyboardButton(text="➕ Pilihan AI Gambar Lainnya (Recraft Logo, Illustrious, Pony)", callback_data="wiz:more_img:1")])

    rows.extend([
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='PHOTO_FACE_4K' else ''}🔍 Pertajam Foto & Wajah 4K", callback_data="wiz:ups:PHOTO_FACE_4K"),
            InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='TEXT_LINE_4K' else ''}✨ Pertajam Teks & Gambar 4K", callback_data="wiz:ups:TEXT_LINE_4K"),
        ],
        [InlineKeyboardButton(text="🛠️ Buka Menu Editing & Hapus Background (File .PNG)", callback_data="menu:wizard_edit")],
        [InlineKeyboardButton(text="✏️ Ubah Deskripsi Gambar", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 MULAI BUAT GAMBAR ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ])
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def build_editing_tools_wizard_kb(session: LiveWizardSession) -> tuple[str, InlineKeyboardMarkup]:
    coins, _, _ = session.get_pricing()
    tool_title, tool_desc = IMAGE_EDITING_TOOLS.get(session.edit_tool, IMAGE_EDITING_TOOLS["REMOVE_BG_PNG"])
    text = (
        f"🛠️ **STUDIO EDITING FOTO & VIDEO — bikinAI**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **Fitur Terpilih:** **`{tool_title}`**\n"
        f"ℹ️ **Fungsi:** _{tool_desc}_\n"
        f"📝 **Instruksi:** _{session.prompt}_\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💡 _Khusus Hapus Background, hasil dikirim sebagai **File PNG Transparan Kualitas Tinggi** agar siap ditempel ke desain katalog/poster Anda!_"
    )
    rows = [
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='REMOVE_BG_PNG' else ''}✂️ Hapus Background (File PNG Transparan)", callback_data="wiz:etool:REMOVE_BG_PNG")],
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='RETOUCH_FACE' else ''}✨ Retouch Wajah", callback_data="wiz:etool:RETOUCH_FACE"),
            InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='INPAINT_OBJ' else ''}🖌️ Ganti Baju / Objek", callback_data="wiz:etool:INPAINT_OBJ"),
        ],
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='OUTPAINT_EXPAND' else ''}🖼️ Perluas Ukuran Foto", callback_data="wiz:etool:OUTPAINT_EXPAND"),
            InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='PRODUCT_RELIGHT' else ''}📸 Studio Produk UMKM", callback_data="wiz:etool:PRODUCT_RELIGHT"),
        ],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='RESTORE_OLD' else ''}🕰️ Restorasi & Warnai Foto Lama", callback_data="wiz:etool:RESTORE_OLD")],
        [
            InlineKeyboardButton(text="🔍 Pertajam Foto & Wajah 4K", callback_data="wiz:ups:PHOTO_FACE_4K"),
            InlineKeyboardButton(text="🎞️ Pertajam & Haluskan Video 4K 60FPS", callback_data="wiz:ups:VIDEO_4K_60FPS"),
        ],
        [InlineKeyboardButton(text="✏️ Ubah Instruksi / Objek Editing", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 PROSES EDITING SEKARANG ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ]
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


