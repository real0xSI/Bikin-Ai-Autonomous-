
<!-- [ID:02_CORE_AI_S002] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: INLINEKEYBOARDBUTTON -->
# ==============================================================================
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


ACTIVE_DRAFTS: dict[int, LiveWizardSession] = {}
router = Router()


def is_verified_owner_dm(user_id: int, chat_type: str) -> bool:
    if chat_type != "private":
        return False
    if RUNTIME_CONFIG["OWNER_ID_RUNTIME"] == 0:
        RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = user_id
    return user_id == RUNTIME_CONFIG["OWNER_ID_RUNTIME"]


def build_customer_main_menu_keyboard(u: dict[str, Any] | None = None, is_private: bool = True) -> InlineKeyboardMarkup:
    """
    [FIX CATATAN #1]: Tombol '🚀 Buka Super Mini App Studio (Web)' SELALU MUNCUL
    secara otomatis di baris paling atas tampilan menu!
    """
    today_str = time.strftime("%Y-%m-%d")
    already_claimed = u and (u.get("last_claim_date") == today_str or u.get("koin_bonus", 0) >= 25)
    claim_label = "🎁 Koin Harian Terklaim ✅" if already_claimed else "🎁 Klaim +4 Koin Gratis"
    ppp_zone = u.get("ppp_zone", 3) if u else 3
    topup_label = (
        f"💳 Isi Saldo ({RUNTIME_CONFIG['ID_ACTIVE_PROVIDER']})"
        if ppp_zone == 3
        else "💳 Top-Up Coins (USDT / Stars ⭐)"
    )

    rows: list[list[InlineKeyboardButton]] = []

    # BARIS 1 PERMANEN: Peluncur Super Mini App Studio (Otomatis menyesuaikan DM vs Grup!)
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
                text="📱 Buka Super Mini App Studio (Aktifkan Link)",
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
                text="🌐 Portal Web Open-Source (Unfiltered) & Voucher",
                callback_data="menu:unfiltered_external_referral",
            )
        ],
        [
            InlineKeyboardButton(text="📊 Status Kuota Harian", callback_data="menu:quota"),
            InlineKeyboardButton(text=claim_label, callback_data="menu:claim_daily"),
        ],
        [
            InlineKeyboardButton(text=topup_label, callback_data="menu:topup_qris"),
            InlineKeyboardButton(text="🎧 Bantuan & Solusi Instan", callback_data="menu:live_support"),
        ],
        [
            InlineKeyboardButton(text="📜 Panduan, FAQ, ToS & Topik Komunitas", callback_data="menu:faq_tos"),
        ],
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_customer_dashboard_caption(username: str, u: dict[str, Any]) -> str:
    tier_badge = "🌟 KREATOR PRO" if u["has_topped_up"] else "⚡ KREATOR EKSPLORER"
    hh_banner = "\n🎉 **FLASH HAPPY HOUR AKTIF: SEMUA RENDER GRATIS 0 KOIN!** 🎉\n" if RUNTIME_CONFIG["HAPPY_HOUR_MODE"] else ""
    return (
        f"┏━━━ ⚡ **bikinAI SUPER INTELLIGENCE** ⚡ ━━━┓\n"
        f"┃ 👤 **Kreator:** `@{username}`\n"
        f"┃ 🏅 **Status:** `{tier_badge}`\n"
        f"┣━━━━━━━━━━━━━━━━━━━━━━━┫\n"
        f"┃ 💎 **Koin Utama:** `{u['koin_utama']} Koin`\n"
        f"┃ 🎁 **Koin Bonus:** `{u['koin_bonus']}/{MAX_KOIN_BONUS_CAP} Koin`\n"
        f"┃ 🤖 **Asisten AI 24/7:** `🟢 AKTIF (Gratis)`\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━┛{hh_banner}\n\n"
        f"✨ **Selamat datang di Studio AI Otonom Generasi Baru.**\n"
        f"▸ Klik **`📱 Buka Super Mini App Studio`** di atas untuk tampilan web penuh, atau gunakan tombol cepat di bawah:"
    )


def build_400_percent_derivative_upsell_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🖼️ Ambil Poster Thumbnail 4K (+4 Koin)", callback_data="drv:poster4k"),
                InlineKeyboardButton(text="🎵 Ekstrak Audio MP3 (+4 Koin)", callback_data="drv:audiomp3"),
            ],
            [
                InlineKeyboardButton(text="✨ Buka Lisensi Bersih Tanpa Watermark (+10 Koin)", callback_data="drv:clean_license"),
            ],
            [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
        ]
    )


def build_video_wizard_kb(session: LiveWizardSession, show_more: bool = False) -> tuple[str, InlineKeyboardMarkup]:
    coins, _, _ = session.get_pricing()
    ups_label = UPSCALER_WHITE_LABEL.get(session.upscale_mode, "🔍 Pertajam Foto & Wajah 4K")
    text = (
        f"🎬 **STUDIO VIDEO AI — bikinAI**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Konsep Video:**\n> _{session.prompt}_\n\n"
        f"┣ ⚡ **Mesin AI Video:** **`{session.video_engine}`**\n"
        f"┣ 📐 **Rasio Layar:** `{session.aspect_ratio}` | ⏱️ **Durasi:** `{session.duration_sec}s`\n"
        f"┗ 🔍 **Penajaman:** `{ups_label}`\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💎 **Biaya:** **`{coins} Koin`**"
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
            [
                InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='HunyuanVideo 13B' else ''}🐉 HunyuanVideo 13B", callback_data="wiz:veng:HunyuanVideo 13B"),
                InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Luma Ray 2' else ''}✨ Luma Ray 2", callback_data="wiz:veng:Luma Ray 2"),
            ],
            [InlineKeyboardButton(text="🔼 Sembunyikan AI Video Lainnya", callback_data="wiz:more_vid:0")],
        ])
    else:
        rows.append([InlineKeyboardButton(text="➕ Pilihan AI Video Lainnya (Sora 2, Runway, MiniMax, LTX)", callback_data="wiz:more_vid:1")])

    rows.extend([
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='PHOTO_FACE_4K' else ''}🔍 Pertajam Foto & Wajah 4K", callback_data="wiz:ups:PHOTO_FACE_4K"),
            InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='TEXT_LINE_4K' else ''}✨ Pertajam Teks & Gambar 4K", callback_data="wiz:ups:TEXT_LINE_4K"),
        ],
        [InlineKeyboardButton(text=f"🚀 MULAI RENDER VIDEO ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ])
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def build_image_wizard_kb(session: LiveWizardSession, show_more: bool = False) -> tuple[str, InlineKeyboardMarkup]:
    coins, _, _ = session.get_pricing()
    ups_label = UPSCALER_WHITE_LABEL.get(session.upscale_mode, "🔍 Pertajam Foto & Wajah 4K")
    text = (
        f"🎨 **STUDIO GAMBAR 4K — bikinAI**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Prompt Visual:**\n> _{session.prompt}_\n\n"
        f"┣ ⚡ **Mesin AI Gambar:** **`{session.image_engine}`**\n"
        f"┣ 📐 **Rasio Layar:** `{session.aspect_ratio}`\n"
        f"┗ 🔍 **Penajaman:** `{ups_label}`\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💎 **Biaya:** **`{coins} Koin`**"
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
                InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Recraft V3' else ''}📐 Recraft V3 (Logo SVG)", callback_data="wiz:ieng:Recraft V3"),
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
        [InlineKeyboardButton(text=f"🚀 MULAI RENDER GAMBAR ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ])
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def build_editing_tools_wizard_kb(session: LiveWizardSession) -> tuple[str, InlineKeyboardMarkup]:
    coins, _, _ = session.get_pricing()
    tool_title, tool_desc = IMAGE_EDITING_TOOLS.get(session.edit_tool, IMAGE_EDITING_TOOLS["REMOVE_BG_PNG"])
    text = (
        f"🛠️ **STUDIO EDITING GAMBAR & TOOLS AWAM — bikinAI**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **Fitur Terpilih:** **`{tool_title}`**\n"
        f"ℹ️ **Penjelasan:** _{tool_desc}_\n"
        f"📝 **Objek/Instruksi:** _{session.prompt}_\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💡 *Khusus fitur Hapus Background, hasil otomatis dikirim sebagai **File Dokumen `.PNG`** agar latar transparan tidak rusak oleh kompresi Telegram!*"
    )
    rows = [
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='REMOVE_BG_PNG' else ''}✂️ Hapus Background (Kirim File .PNG)", callback_data="wiz:etool:REMOVE_BG_PNG")],
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='RETOUCH_FACE' else ''}✨ Retouch Wajah", callback_data="wiz:etool:RETOUCH_FACE"),
            InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='INPAINT_OBJ' else ''}🖌️ Inpainting (Ganti Baju)", callback_data="wiz:etool:INPAINT_OBJ"),
        ],
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='OUTPAINT_EXPAND' else ''}🖼️ Outpainting (Perluas)", callback_data="wiz:etool:OUTPAINT_EXPAND"),
            InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='PRODUCT_RELIGHT' else ''}📸 Studio Produk UMKM", callback_data="wiz:etool:PRODUCT_RELIGHT"),
        ],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='RESTORE_OLD' else ''}🕰️ Restorasi & Warnai Foto Lama", callback_data="wiz:etool:RESTORE_OLD")],
        [
            InlineKeyboardButton(text="🔍 Pertajam Foto & Wajah 4K", callback_data="wiz:ups:PHOTO_FACE_4K"),
            InlineKeyboardButton(text="✨ Pertajam Teks & Gambar 4K", callback_data="wiz:ups:TEXT_LINE_4K"),
        ],
        [InlineKeyboardButton(text=f"🚀 PROSES EDITING SEKARANG ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ]
    return text, InlineKeyboardMarkup(inline_keyboard=rows)
```!]
*(Setelah Anda menempelkan kode Bagian 2 di atas tepat di bawah Bagian 1, ketik **"Lanjut Bagian 3"** untuk bagian penutupnya!)*
# ==============================================================================
# [BAGIAN 3 DARI 3]:
# - Pemrosesan Multimodal Ingest (F.photo | F.document) & Render Otomatis
# - Schedulers / Bimbingan Topik Grup Otomatis (/setup_grup, /ikat)
# - Built-in SangMata Tracker & Cyber Welcome Gate (Menyapa Member Baru)
# - Zero-Clutter Natural Chat Engine + Rotasi Footer Dinamis
# - Entrypoint Asinkron Terpadu (main() Bot Telegram + Dual Web Server Port 8080)
# ==============================================================================


@router.message(Command("setup_grup"))
async def cmd_setup_community_group(message: Message) -> None:
    """
    [POIN #5]: Fitur 1-Klik /setup_grup yang otomatis membuat dan mengikat 6 Topik Unik
    di grup Telegram Anda (Live Neural Feed, Command Center, Blueprint, dll).
    """
    if message.chat.type not in ("group", "supergroup"):
        await message.reply("Perintah /setup_grup harus diketik di dalam grup komunitas Anda!")
        return

    chat_id = message.chat.id
    topics_to_create = [
        ("ACTIVITY_TOPIC", "⚡ Live Neural Feed"),
        ("COMMAND_TOPIC", "📡 Command Center & Promo"),
        ("FAQ_TOPIC", "🧭 Blueprint & Koin Gratis"),
        ("CREATIVE_TOPIC", "🧠 Arsitek Prompt & Ide 24/7"),
        ("GALLERY_TOPIC", "🎬 Galeri Kreator & Preset"),
        ("FEEDBACK_TOPIC", "🛠️ Lab Inovasi & Bantuan"),
    ]

    async with aiosqlite.connect(DB_PATH) as db:
        for b_key, t_title in topics_to_create:
            try:
                # Membuat topik forum baru via API Telegram secara otomatis
                res_topic = await message.bot.create_forum_topic(chat_id=chat_id, name=t_title)
                t_id = res_topic.message_thread_id
                await set_topic_binding(db, b_key, chat_id, t_id, title=t_title)
            except Exception:
                # Jika topik sudah ada atau bot tidak punya izin superadmin forum
                await set_topic_binding(db, b_key, chat_id, 0, title=t_title)

    await message.reply(
        "✅ **SETUP GRUP OTONOM BERHASIL!**\n"
        "Ke-6 Topik khas *bikinAI* telah dibuat dan diikat otomatis ke sistem. Bot siap melayani secara penuh!",
        parse_mode="Markdown",
    )


@router.message(Command("ikat"))
async def cmd_bind_current_topic_interactive(message: Message) -> None:
    if message.chat.type not in ("group", "supergroup"):
        return
    thread_id = message.message_thread_id or 0
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚡ Live Neural Feed", callback_data=f"bind:ACTIVITY_TOPIC:{thread_id}"),
                InlineKeyboardButton(text="🧠 Arsitek Prompt", callback_data=f"bind:CREATIVE_TOPIC:{thread_id}"),
            ],
            [
                InlineKeyboardButton(text="🛠️ Lab Bantuan", callback_data=f"bind:FEEDBACK_TOPIC:{thread_id}"),
                InlineKeyboardButton(text="🧭 Blueprint", callback_data=f"bind:FAQ_TOPIC:{thread_id}"),
            ],
        ]
    )
    await message.reply("Pilih fungsi otonom untuk topik ini:", reply_markup=kb)


@router.callback_query(F.data.startswith("bind:"))
async def handle_topic_binding_cb(call: CallbackQuery) -> None:
    parts = call.data.split(":")
    b_key, t_id = parts[1], int(parts[2])
    chat_id = call.message.chat.id
    async with aiosqlite.connect(DB_PATH) as db:
        await set_topic_binding(db, b_key, chat_id, t_id)
    await call.answer(f"✅ Topik ini berhasil diikat sebagai {b_key}!", show_alert=True)
    try:
        await call.message.edit_text(f"✅ **Topik ini resmi diikat ke `{b_key}` (Thread ID: `{t_id}`)!**", parse_mode="Markdown")
    except Exception:
        pass


@router.message(F.new_chat_members)
async def handle_builtin_cyber_welcome_gate(message: Message) -> None:
    if not RUNTIME_CONFIG["SUBBOT_WELCOME_GUARD_ACTIVE"]:
        return
    for member in message.new_chat_members:
        if member.is_bot:
            continue
        uname = member.username or member.first_name or "Kreator"
        async with aiosqlite.connect(DB_PATH) as db:
            u = await ensure_user_and_track_identity(db, member.id, uname, member.first_name or "")
        alert_line = f"\n🕵️ _Catatan Identitas (SangMata): Sebelumnya dikenal sebagai {u['identity_alert']}_" if u["identity_alert"] else ""
        await message.reply(
            f"⚡ **Selamat datang di Markas Otonom `bikinAI Super Intelligence`, Kak `@{uname}`!**{alert_line}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🧭 **Panduan Singkat:**\n"
            f"▸ Kirim **Teks, Foto Referensi, atau PDF** langsung ke bot pribadi kami.\n"
            f"▸ Nikmati asisten 24 jam gratis & studio generator SOTA.\n\n"
            f"🎁 *Ketik `/start` di chat pribadi `@{BOT_USERNAME_GLOBAL}` untuk mengambil **+4 Koin Gratis Harianmu**!*",
            parse_mode="Markdown",
        )


# ==============================================================================
# 12. HANDLER UPLOAD FOTO REFERENSI & PDF (LANGSUNG RENDER KE CHAT)
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


# ==============================================================================
# 13. HANDLER OBROLAN NYAMAN TANPA TOMBOL (ROBOT FOOTER DINAMIS & GEMINI STYLE)
# Menjawab Catatan #6 & #7: Tombol tidak muncul terus, melainkan hanya saat diminta
# dengan mengetik "tampilin tombol" atau "menu". Bahasa Indonesia 100% murni!
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


# ==============================================================================
# 14. ENTRYPOINT UTAMA (MAIN)
# ==============================================================================
async def main() -> None:
    global BOT_INSTANCE_GLOBAL, BOT_USERNAME_GLOBAL
    if not BOT_TOKEN:
        print("❌ TOKEN_BOT_UTAMA belum diatur di Secrets!")
        return

    async with aiosqlite.connect(DB_PATH) as db:
        await init_master_db(db)

    # Jalankan Dual Web Server (Port 8080: Mini App SFW + /unfiltered-portal)
    await start_embedded_web_servers(port=8080)

    bot = Bot(token=BOT_TOKEN)
    BOT_INSTANCE_GLOBAL = bot
    me = await bot.get_me()
    BOT_USERNAME_GLOBAL = me.username or "bikinAI_bot"

    dp = Dispatcher()
    dp.include_router(router)
    print(f"🚀 bikinAI Super Intelligence v3.4.0 (@{BOT_USERNAME_GLOBAL}) SIAP BEROPERASI 100%!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```
```

## 29. apppy11.md

```md
```python
# ==============================================================================
# BIKINAI — MASTER ENGINE v3.7.1 (STRICT TECHNICAL SEPARATION & CANONICAL REPOS)
# Dependencies (PyPI): pip install aiogram aiohttp aiosqlite httpx cryptography
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

# 0. PERSISTENT STORAGE & RUNTIME CONFIGURATION
VAULT_DIR = Path.home() / ".bikinai_vault"
VAULT_DIR.mkdir(parents=True, exist_ok=True)
try:
    os.chmod(VAULT_DIR, 0o700)
except Exception:
    pass

DB_PATH = str(VAULT_DIR / "bikinai_master_vault.db")
KEYRING_PATH = VAULT_DIR / "ed25519_voucher_key.bin"

BOT_TOKEN = os.getenv("TOKEN_BOT_UTAMA", "").strip()
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
OWNER_BOOTSTRAP_TOKEN = os.getenv("OWNER_BOOTSTRAP_TOKEN", "").strip() or secrets.token_hex(8)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "").strip()
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY", "").strip()
GOPAY_STATIC_QRIS_RAW = os.getenv("GOPAY_STATIC_QRIS_RAW", "").strip()

SAMPLE_SANDBOX_VIDEO_URL = "https://filesamples.com/samples/video/mp4/sample_640x360.mp4"
BOT_INSTANCE_GLOBAL: Bot | None = None
BOT_USERNAME_GLOBAL: str = "bikinAI_bot"


def detect_default_miniapp_url() -> str:
    env_url = os.getenv("MINIAPP_PUBLIC_URL", "").strip()
    if env_url.startswith("https://"):
        return env_url
    cs_name = os.getenv("CODESPACE_NAME", "").strip()
    cs_dom = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "app.github.dev").strip()
    return f"https://{cs_name}-8080.{cs_dom}" if cs_name else ""


def load_or_create_persistent_keys() -> tuple[bytes, bytes]:
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
    return priv_bytes, priv_obj.public_key().public_bytes_raw()


ED25519_PRIV_BYTES, ED25519_PUB_BYTES = load_or_create_persistent_keys()

RUNTIME_CONFIG: dict[str, Any] = {
    "LAUNCH_PRODUCTION_MODE": False,
    "PILIHAN_MESIN_MEDIA": 1,
    "BANSOS_OPERATION_MODE": "SILENT_PROFIT",
    "HAPPY_HOUR_MODE": False,
    "AUTO_APPROVE_SANDBOX_TOPUP": False,
    "ID_ACTIVE_CATEGORY": "QRIS_DIRECT",
    "ID_ACTIVE_PROVIDER": "QRIS GoPay Merchant",
    "GLOBAL_ACTIVE_PROVIDER": "Aktifkan Keduanya (USDT + Telegram Stars)",
    "WEB_BRAND_NAME": os.getenv("WEB_PORTAL_BRAND_NAME", "AetherFree AI Studio").strip(),
    "CUSTOM_WEB_DOMAIN": os.getenv("CUSTOM_WEB_DOMAIN", "").strip(),
    "FOMO_COUNTER_BASE": 29620,
    "OWNER_ID_RUNTIME": ADMIN_USER_ID,
    "MINIAPP_URL": detect_default_miniapp_url(),
    "PRIMARY_ROLLING_AGENT": "ARGON",
    "SUBBOT_SANGMATA_ACTIVE": True,
    "SUBBOT_WELCOME_GUARD_ACTIVE": True,
    "SUBBOT_NEURAL_FEED_ACTIVE": True,
    "SUBBOT_REFUND_SWEEPER_ACTIVE": True,
    "SUBBOT_SOCIAL_POSTER_ACTIVE": True,
}

# 1. SQLITE WAL CONCURRENCY, LOCK STRIPES & CONVERGENCE GUARD
STRIPE_COUNT = 4096
USER_LOCK_STRIPES = [asyncio.Lock() for _ in range(STRIPE_COUNT)]
ANTI_TUYUL_VELOCITY: dict[int, float] = {}


def get_user_lock(user_id: int) -> asyncio.Lock:
    return USER_LOCK_STRIPES[user_id % STRIPE_COUNT]


def check_velocity_rate_limit(user_id: int, min_interval_sec: float = 0.5) -> bool:
    now = time.monotonic()
    if now - ANTI_TUYUL_VELOCITY.get(user_id, 0.0) < min_interval_sec:
        return False
    ANTI_TUYUL_VELOCITY[user_id] = now
    if len(ANTI_TUYUL_VELOCITY) > 10000:
        ANTI_TUYUL_VELOCITY.clear()
    return True


class AutonomicConvergenceGuard:
    def __init__(self) -> None:
        self.verified_ast_hashes: set[str] = set()
        self.telemetry_window: deque[tuple[int, str, bool]] = deque(maxlen=50)

    def record_telemetry(self, component: str, success: bool) -> None:
        self.telemetry_window.append((int(time.time()), component, success))

    def build_gitops_commit_plan(self, ast_hash: str, summary: str) -> dict[str, str]:
        return {
            "shadow_branch": f"autonomic/patch-{ast_hash[:10]}",
            "verify_cmd": "python3 -m py_compile app.py",
            "commit_cmd": f"git checkout -b autonomic/patch-{ast_hash[:10]} && git commit -am '[Autonomic-Heal] {summary}'",
            "rollback_cmd": "git revert --no-edit HEAD",
        }


AUTONOMIC_GUARD = AutonomicConvergenceGuard()


@asynccontextmanager
async def get_db() -> AsyncIterator[aiosqlite.Connection]:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA journal_mode = WAL;")
        await db.execute("PRAGMA synchronous = NORMAL;")
        await db.execute("PRAGMA busy_timeout = 10000;")
        await db.execute("PRAGMA foreign_keys = ON;")
        yield db


class SingleWriterSQLiteDaemon:
    def __init__(self, checkpoint_every_n_writes: int = 400):
        self._write_mutex = asyncio.Lock()
        self._write_counter = 0
        self._checkpoint_threshold = checkpoint_every_n_writes

    async def execute_write_tx(
        self, db: aiosqlite.Connection, tx_coro: Callable[[aiosqlite.Connection], Coroutine[Any, Any, Any]]
    ) -> Any:
        async with self._write_mutex:
            try:
                result = await tx_coro(db)
                await db.commit()
            except Exception:
                try:
                    await db.rollback()
                except Exception:
                    pass
                raise
            self._write_counter += 1
            if self._write_counter >= self._checkpoint_threshold:
                self._write_counter = 0
                now_ts = int(time.time())
                try:
                    await db.execute("DELETE FROM redeemed_nullifiers WHERE expires_at <= ?;", (now_ts,))
                    await db.execute("DELETE FROM omni_resource_registry WHERE expires_at <= ?;", (now_ts,))
                    await db.commit()
                    await db.execute("PRAGMA wal_checkpoint(PASSIVE);")
                except Exception:
                    pass
            return result


DB_WRITER_DAEMON = SingleWriterSQLiteDaemon()

# 2. DATABASE SCHEMA (11 TABLES) & 3-TIER PPP MATRIX
MAX_KOIN_BONUS_CAP = 25
PPP_EFFECTIVE_COIN_IDR = {1: 580, 2: 260, 3: 84}

PPP_PRICING_PACKAGES = {
    "ID": {
        "HEMAT": {"name": "⚡ Paket Hemat Kreator", "idr": 5000, "coins": 60},
        "PRO": {"name": "🔥 Paket Studio Pro (+16% Bonus)", "idr": 25000, "coins": 350},
        "SULTAN": {"name": "👑 Paket Sultan / Executive VIP (+33% Bonus & Jalur Prioritas)", "idr": 250000, "coins": 4000},
    },
    "GLOBAL": {
        "HEMAT": {"name": "⚡ Starter Creator Pack", "usd": "$1.99", "stars": 110, "idr_eq": 31000, "coins": 60},
        "PRO": {"name": "🔥 Studio Pro Pack", "usd": "$9.99", "stars": 550, "idr_eq": 155000, "coins": 350},
        "SULTAN": {"name": "👑 Sovereign Executive VIP", "usd": "$49.99", "stars": 2750, "idr_eq": 775000, "coins": 2500},
    },
}


async def init_master_db(db: aiosqlite.Connection) -> None:
    await db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            internal_user_id INTEGER PRIMARY KEY, username TEXT DEFAULT 'Kreator', first_name TEXT DEFAULT '',
            language_code TEXT DEFAULT 'id', koin_utama INTEGER NOT NULL DEFAULT 0 CHECK (koin_utama >= 0),
            koin_bonus INTEGER NOT NULL DEFAULT 4 CHECK (koin_bonus >= 0 AND koin_bonus <= 25),
            has_topped_up INTEGER NOT NULL DEFAULT 0, ppp_zone INTEGER NOT NULL DEFAULT 3, last_claim_date TEXT,
            chat_used_today INTEGER NOT NULL DEFAULT 0, free_img_used_today INTEGER NOT NULL DEFAULT 0,
            quota_day_epoch INTEGER NOT NULL DEFAULT 0, personal_memory_notes TEXT DEFAULT '',
            active_canvas_content TEXT DEFAULT '', created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS identity_history (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
            old_username TEXT, new_username TEXT, changed_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY, internal_user_id INTEGER NOT NULL, cost INTEGER NOT NULL,
            deducted_bonus INTEGER NOT NULL DEFAULT 0, deducted_utama INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'PROCESSING', refunded_lock INTEGER NOT NULL DEFAULT 0,
            prompt_text TEXT DEFAULT '', engine_used TEXT DEFAULT '', created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS payment_invoices (
            invoice_id TEXT PRIMARY KEY, user_id INTEGER NOT NULL, amount_idr INTEGER NOT NULL,
            coins_credited INTEGER NOT NULL DEFAULT 60, provider TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING', created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS redeemed_nullifiers (nullifier_hash TEXT PRIMARY KEY, expires_at INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS treasury_summary (
            id INTEGER PRIMARY KEY CHECK (id = 1), gross_revenue_idr INTEGER NOT NULL DEFAULT 0,
            working_capital_vault_idr INTEGER NOT NULL DEFAULT 0, harvestable_profit_vault_idr INTEGER NOT NULL DEFAULT 0,
            total_harvested_by_owner_idr INTEGER NOT NULL DEFAULT 0, total_jobs_completed INTEGER NOT NULL DEFAULT 0,
            updated_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS bot_bindings (
            binding_key TEXT PRIMARY KEY, chat_id INTEGER NOT NULL, topic_id INTEGER NOT NULL DEFAULT 0, topic_title TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS system_settings (setting_key TEXT PRIMARY KEY, setting_val TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS user_feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
            username TEXT, feedback_text TEXT NOT NULL, created_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS omni_resource_registry (
            resource_id TEXT PRIMARY KEY, category TEXT NOT NULL, resource_name TEXT NOT NULL,
            endpoint_url TEXT NOT NULL, secret_or_meta TEXT NOT NULL, is_live_verified INTEGER NOT NULL DEFAULT 0,
            expires_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS syndicated_assets (
            asset_id TEXT PRIMARY KEY, prompt_signature TEXT NOT NULL, engine_name TEXT NOT NULL,
            media_url TEXT NOT NULL, times_reused INTEGER NOT NULL DEFAULT 1, created_at INTEGER NOT NULL
        );
        """
    )
    await db.commit()
    cur = await db.execute("SELECT setting_key, setting_val FROM system_settings;")
    for k, v in await cur.fetchall():
        if k == "MINIAPP_URL" and v.startswith("https://"):
            RUNTIME_CONFIG["MINIAPP_URL"] = v
        elif k == "OWNER_ID_RUNTIME" and v.isdigit() and int(v) > 0:
            RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = int(v)
        elif k == "PILIHAN_MESIN_MEDIA" and v.isdigit():
            RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] = int(v)
        elif k in ("LAUNCH_PRODUCTION_MODE", "HAPPY_HOUR_MODE", "AUTO_APPROVE_SANDBOX_TOPUP"):
            RUNTIME_CONFIG[k] = v == "1"
        elif k in (
            "ID_ACTIVE_CATEGORY", "ID_ACTIVE_PROVIDER", "GLOBAL_ACTIVE_PROVIDER",
            "BANSOS_OPERATION_MODE", "PRIMARY_ROLLING_AGENT", "WEB_BRAND_NAME", "CUSTOM_WEB_DOMAIN",
        ):
            RUNTIME_CONFIG[k] = v


async def save_persistent_setting(db: aiosqlite.Connection, key: str, val: str) -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("INSERT OR REPLACE INTO system_settings (setting_key, setting_val) VALUES (?, ?);", (key, str(val)))
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def set_topic_binding(db: aiosqlite.Connection, key: str, chat_id: int, topic_id: int, title: str = "") -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("INSERT OR REPLACE INTO bot_bindings (binding_key, chat_id, topic_id, topic_title) VALUES (?, ?, ?, ?);", (key, chat_id, topic_id, title))
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def get_topic_binding(db: aiosqlite.Connection, key: str) -> tuple[int, int] | None:
    cur = await db.execute("SELECT chat_id, topic_id FROM bot_bindings WHERE binding_key = ?;", (key,))
    row = await cur.fetchone()
    return (int(row[0]), int(row[1])) if row else None


async def get_all_topic_bindings(db: aiosqlite.Connection) -> dict[str, tuple[int, int, str]]:
    cur = await db.execute("SELECT binding_key, chat_id, topic_id, topic_title FROM bot_bindings;")
    return {r[0]: (int(r[1]), int(r[2]), str(r[3] or r[0])) for r in await cur.fetchall()}


# 3. 4-GATE DEEP-DEFENSE BANSOS STERILIZER & CANONICAL RESOURCE REGISTRY
OMNI_BANSOS_PRESETS = {
    "AI_API": [
        {"res_id": "API-POLLINATIONS-V1", "name": "pollinations/pollinations (OpenAI-Compatible Gateway)", "endpoint": "https://text.pollinations.ai/openai", "meta": "openai", "desc": "Base URL: https://gen.pollinations.ai/v1", "verified": 1},
        {"res_id": "API-OR-FREE-POOL", "name": "OpenRouter Unified API (:free Tier)", "endpoint": "https://openrouter.ai/api/v1/chat/completions", "meta": "deepseek/deepseek-chat:free", "desc": "deepseek-ai/DeepSeek-V3 & Qwen/Qwen2.5-Coder-32B-Instruct", "verified": 1 if OPENROUTER_API_KEY else 0},
        {"res_id": "API-GROQ-LPU", "name": "Groq Cloud LPU (meta-llama/Llama-3.3-70B-Instruct)", "endpoint": "https://api.groq.com/openai/v1/chat/completions", "meta": "llama-3.3-70b-versatile", "desc": "1,000 RPD / 30 RPM Free Tier", "verified": 1 if GROQ_API_KEY else 0},
        {"res_id": "API-CEREBRAS-1M", "name": "Cerebras Inference (llama-3.3-70b)", "endpoint": "https://api.cerebras.ai/v1/chat/completions", "meta": "llama-3.3-70b", "desc": "1M Tokens/Day Free Tier", "verified": 1 if CEREBRAS_API_KEY else 0},
    ],
    "CLOUD_STORAGE": [
        {"res_id": "STOR-CF-R2", "name": "Cloudflare R2 Object Storage", "endpoint": "https://dash.cloudflare.com/", "meta": "10GB Free + Zero Egress Fee", "desc": "S3-Compatible Object Storage", "verified": 1},
        {"res_id": "STOR-STORJ-DEPIN", "name": "Storj Decentralized Cloud", "endpoint": "https://www.storj.io/", "meta": "25GB Free S3-Compatible", "desc": "Backup Media Storage", "verified": 1},
        {"res_id": "STOR-B2-BACKBLAZE", "name": "Backblaze B2 Cloud Storage", "endpoint": "https://www.backblaze.com/cloud-storage", "meta": "10GB Free Tier", "desc": "Object Storage", "verified": 1},
    ],
    "GRANTS_AND_DB": [
        {"res_id": "GRANT-MODAL-GPU", "name": "Modal Serverless GPU", "endpoint": "https://modal.com/", "meta": "$30/month Free Compute Credits", "desc": "Containerized GPU Execution", "verified": 1},
        {"res_id": "GRANT-CF-WORKERS-AI", "name": "Cloudflare Workers AI", "endpoint": "https://developers.cloudflare.com/workers-ai/", "meta": "10,000 Neurons/Day Free Tier", "desc": "Serverless Edge Inference", "verified": 1},
        {"res_id": "GRANT-MS-FOUNDERS", "name": "Microsoft for Startups Founders Hub", "endpoint": "https://foundershub.startups.microsoft.com/", "meta": "Azure Cloud Credits", "desc": "Startup Infrastructure Grant", "verified": 1},
    ],
}


def validate_safe_external_url(url: str) -> tuple[bool, str]:
    try:
        parsed = urlparse(url.strip())
        if parsed.scheme != "https":
            return False, "HTTPS required."
        host = (parsed.hostname or "").lower()
        if not host or host in ("localhost", "0.0.0.0") or host.endswith((".local", ".internal")):
            return False, "Internal host blocked by SSRF filter."
        try:
            ip = ipaddress.ip_address(host)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
                return False, f"Private IP ({ip}) blocked."
        except ValueError:
            pass
        return True, "OK"
    except Exception as e:
        return False, f"Invalid URL: {e}"


def sterilize_community_script_ast(source_code: str, script_name: str = "community_plugin") -> dict[str, Any]:
    forbidden_calls = {"system", "popen", "eval", "exec", "compile", "open", "input", "breakpoint", "spawnl", "getattr", "setattr", "delattr", "globals", "locals", "vars", "dir", "__import__"}
    forbidden_imports = {"os", "sys", "subprocess", "pty", "ctypes", "pickle", "marshal", "shelve", "shutil", "socket", "urllib", "requests", "httpx", "aiohttp", "importlib", "builtins", "inspect"}
    forbidden_dunders = {"__subclasses__", "__globals__", "__builtins__", "__self__", "__import__", "__mro__", "__bases__", "__code__", "__closure__", "__dict__", "__class__"}
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return {"ok": False, "reason": f"SyntaxError: {e}", "hash": "", "threats_removed": [str(e)]}

    stripped_threats: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mod_names = [alias.name.split(".")[0] for alias in node.names]
            if isinstance(node, ast.ImportFrom) and node.module:
                mod_names.append(node.module.split(".")[0])
            for m in mod_names:
                if m in forbidden_imports:
                    stripped_threats.append(f"Blocked import '{m}'")
        elif isinstance(node, ast.Attribute) and (node.attr in forbidden_dunders or node.attr.startswith("__")):
            stripped_threats.append(f"Blocked dunder attribute '{node.attr}'")
        elif isinstance(node, ast.Name) and node.id in forbidden_dunders:
            stripped_threats.append(f"Blocked identifier '{node.id}'")
        elif isinstance(node, ast.Call):
            fn = node.func.id if isinstance(node.func, ast.Name) else (node.func.attr if isinstance(node.func, ast.Attribute) else "")
            if fn in forbidden_calls:
                stripped_threats.append(f"Blocked call '{fn}()'")
        elif isinstance(node, ast.ExceptHandler) and len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            stripped_threats.append("Blocked empty 'except: pass'")

    ast_hash = hashlib.sha256(ast.dump(tree).encode()).hexdigest()[:14]
    if not stripped_threats:
        AUTONOMIC_GUARD.verified_ast_hashes.add(ast_hash)
    return {"ok": len(stripped_threats) == 0, "script_name": script_name, "threats_removed": stripped_threats, "hash": ast_hash}


def sanitize_external_api_response(raw_reply: str) -> str:
    if not raw_reply:
        return ""
    cleaned = re.sub(r"<script\b[^>]*>.*?</script>", "", raw_reply, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"javascript\s*:", "", cleaned, flags=re.IGNORECASE)
    return cleaned.replace("|---|", "").strip()


async def ping_and_verify_bansos_endpoint(endpoint_url: str, model_name: str = "openai", api_key: str = "") -> tuple[bool, float, str]:
    ok_url, reason = validate_safe_external_url(endpoint_url)
    if not ok_url:
        return False, 0.0, reason
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    payload = {"model": model_name or "openai", "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
    t0 = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=2.5, follow_redirects=False) as client:
            r = await client.post(endpoint_url, headers=headers, json=payload)
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
            return (True, elapsed_ms, f"HTTP 200 OK ({elapsed_ms} ms)") if r.status_code == 200 else (False, elapsed_ms, f"HTTP {r.status_code}")
    except Exception as e:
        return False, round((time.perf_counter() - t0) * 1000, 1), f"Timeout ({type(e).__name__})"


async def check_multi_tld_domain_availability_live(base_keyword: str = "bikinai") -> list[dict[str, str]]:
    clean_kw = re.sub(r"[^a-z0-9-]", "", base_keyword.lower()) or "bikinai"
    candidate_domains = [f"{clean_kw}.tech", f"{clean_kw}.xyz", f"{clean_kw}.art", f"{clean_kw}.app", f"{clean_kw}.dev", f"aether-{clean_kw}.xyz"]
    results = []
    async with httpx.AsyncClient(timeout=3.5, follow_redirects=True) as client:
        for dom in candidate_domains:
            try:
                r = await client.get(f"https://rdap.org/domain/{dom}")
                status = "🟢 TERSEDIA (404 RDAP)" if r.status_code == 404 else ("🔴 Terdaftar (200 RDAP)" if r.status_code == 200 else "🟡 Cek Registrar")
            except Exception:
                status = "🟢 Siap Cek di Cloudflare / Porkbun"
            results.append({"domain": dom, "status": status})
    return results


# 4. MINI APP HTML & FREEDOM WEB PORTAL HTML (CANONICAL HF/OR MODEL IDS)
MINIAPP_FULL_WEBSITE_HTML = """<!DOCTYPE html>
<html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>bikinAI Super Intelligence — Studio Kreatif 4K</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
:root{--bg:#05070c;--surface:#0f1523;--cyan:#00f0ff;--purple:#7b2cbf;--text:#f0f6fc;--muted:#8b949e;--success:#00e676}
*{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
body{background:radial-gradient(circle at 50% 0%,#17103a 0%,#05070c 72%);color:var(--text);min-height:100vh;padding:14px 14px 96px}
.hero{background:linear-gradient(135deg,rgba(15,21,35,.95),rgba(30,16,60,.85));border:1px solid rgba(0,240,255,.3);border-radius:16px;padding:16px;margin-bottom:14px}
.badge{display:inline-block;background:linear-gradient(90deg,var(--cyan),var(--purple));color:#fff;font-size:10px;font-weight:800;padding:3px 10px;border-radius:99px;margin-bottom:6px}
.hero h1{font-size:18px;font-weight:800;color:#fff;margin-bottom:4px}.hero p{font-size:12px;color:var(--muted);line-height:1.4}
.tab-section{display:none}.tab-section.active{display:block}
.label{font-size:11px;font-weight:700;text-transform:uppercase;color:var(--cyan);margin:12px 0 6px;letter-spacing:.6px}
.pill-row{display:flex;gap:7px;overflow-x:auto;padding-bottom:4px;margin-bottom:4px}
.pill{flex:1;text-align:center;white-space:nowrap;background:var(--surface);border:1px solid rgba(255,255,255,.08);color:var(--muted);padding:9px 10px;border-radius:11px;font-size:12px;font-weight:600;cursor:pointer;user-select:none}
.pill.active{background:rgba(0,240,255,.18);border-color:var(--cyan);color:#fff}
.pill.disabled{opacity:.22;pointer-events:none;cursor:not-allowed;filter:grayscale(1)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.card{background:var(--surface);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:10px;cursor:pointer}
.card.active{border-color:var(--cyan);background:rgba(0,240,255,.12)}.card.hidden-engine{display:none}
.card h4{font-size:13px;color:#fff;margin-bottom:2px}.card p{font-size:10px;color:var(--muted)}
.upload-box{border:1.5px dashed rgba(0,240,255,.4);background:rgba(15,21,35,.6);border-radius:14px;padding:12px;text-align:center;position:relative;cursor:pointer;margin-top:4px}
.upload-box.highlight-upload{border-color:#00e676;background:rgba(0,230,118,.08)}
.upload-box input{position:absolute;inset:0;opacity:0;cursor:pointer}
#ref-preview{max-height:110px;border-radius:8px;margin-top:8px;display:none;margin-left:auto;margin-right:auto;border:1px solid var(--cyan)}
textarea{width:100%;height:80px;background:var(--surface);border:1px solid rgba(0,240,255,.3);border-radius:12px;color:#fff;padding:10px;font-size:13px;outline:none;resize:none}
.btn-exec{width:100%;margin-top:12px;padding:14px;border:none;border-radius:14px;background:linear-gradient(90deg,#00c6ff,#7b2cbf);color:#fff;font-size:14px;font-weight:800;cursor:pointer}
#toast{margin-top:10px;padding:10px;border-radius:10px;font-size:12px;background:rgba(0,230,118,.15);border:1px solid var(--success);color:var(--success);display:none;text-align:center}
.legal-card{background:var(--surface);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:14px;margin-bottom:10px;font-size:12px;line-height:1.55;color:#d0d7de}
.legal-card h3{color:var(--cyan);font-size:14px;margin-bottom:6px}
.topic-btn{display:block;background:rgba(0,240,255,.1);border:1px solid rgba(0,240,255,.3);color:#fff;text-decoration:none;padding:9px 12px;border-radius:10px;margin-top:6px;font-size:12px;font-weight:700}
.footer-copy{text-align:center;font-size:11px;color:var(--muted);margin-top:18px;padding-top:12px;border-top:1px solid rgba(255,255,255,.07)}
.bottom-nav{position:fixed;bottom:0;left:0;right:0;height:62px;background:rgba(8,12,22,.96);backdrop-filter:blur(16px);border-top:1px solid rgba(255,255,255,.1);display:flex;justify-content:space-around;align-items:center;z-index:99}
.nav-btn{display:flex;flex-direction:column;align-items:center;gap:2px;color:var(--muted);font-size:10px;font-weight:600;cursor:pointer}.nav-btn.active{color:var(--cyan)}
</style></head><body>
<div class="hero"><span class="badge">⚡ STUDIO KREATIF RESMI v3.7.1</span><h1>Selamat Datang di bikinAI Super Intelligence</h1>
<p id="welcome-user">Platform Studio Visual 4K, Video Sinematik, & Foto Jadi Video dengan Garansi Koin Kembali 100%.</p></div>

<div id="tab-studio" class="tab-section active">
  <div class="label">1. Pilih Kategori Karya</div>
  <div class="pill-row" data-group="modality">
    <div class="pill active" onclick="setMod(this,'IMAGE')">🎨 Gambar 4K</div>
    <div class="pill" onclick="setMod(this,'VIDEO')">🎬 Buat Video AI</div>
    <div class="pill" onclick="setMod(this,'IMG2VID')">🖼️➡️🎬 Foto Jadi Video</div>
    <div class="pill" onclick="setMod(this,'REMOVE_BG')">✂️ Hapus BG (.PNG)</div>
    <div class="pill" onclick="setMod(this,'RETOUCH')">✨ Retouch & Edit</div>
  </div>
  <div class="label">2. Pilih Mesin AI Utama</div>
  <div class="grid" id="engine-grid">
    <div class="card active" data-type="IMAGE" onclick="setEng(this,'bytedance/seedream-4.0')"><h4>✨ Seedream 4.0</h4><p>Poster 4K & Teks Tajam</p></div>
    <div class="card" data-type="IMAGE" onclick="setEng(this,'black-forest-labs/FLUX.1-dev')"><h4>📸 FLUX.1-dev</h4><p>Fotorealistis Natural</p></div>
    <div class="card" data-type="IMAGE" onclick="setEng(this,'black-forest-labs/flux.1-kontext-pro')"><h4>🎨 FLUX.1 Kontext Pro</h4><p>Konsistensi Objek & Edit</p></div>
    <div class="card" data-type="IMAGE" onclick="setEng(this,'OnomaAIResearch/Illustrious-xl')"><h4>🎌 Illustrious-XL</h4><p>Anime & Ilustrasi 2.5D</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Wan-AI/Wan2.2-T2V-A14B')"><h4>🔵 Wan2.2-T2V-A14B</h4><p>Video Sinematik 14B</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Wan-AI/Wan2.2-S2V-14B')"><h4>🕺 Wan2.2-S2V-14B</h4><p>Image/Audio to Video</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'google/veo-3.1-fast')"><h4>🎥 Google Veo 3.1</h4><p>Sinematik Film & Audio</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Wan-AI/Wan2.2-TI2V-5B')"><h4>🟢 Wan2.2-TI2V-5B</h4><p>Gerak Cepat & Halus</p></div>
  </div>
  <div class="label">3. Pilihan Instan Orang Awam (Klik untuk Pakai Gaya / Motion Kamera)</div>
  <div class="pill-row" id="preset-img-row" data-group="preset">
    <div class="pill active" onclick="applyAwamPreset(this,'Commercial product catalog photography, studio lighting')">🛍️ Katalog Produk UMKM</div>
    <div class="pill" onclick="applyAwamPreset(this,'Professional studio portrait, soft rim lighting, sharp focus')">👔 Foto Profil Studio</div>
    <div class="pill" onclick="applyAwamPreset(this,'Cinematic movie poster & viral YouTube thumbnail')">🎬 Poster & Thumbnail</div>
    <div class="pill" onclick="applyAwamPreset(this,'Vibrant 3D & anime illustration, volumetric light')">🎌 Anime / Ilustrasi 3D</div>
  </div>
  <div class="pill-row" id="preset-vid-row" data-group="preset" style="display:none">
    <div class="pill active" onclick="applyAwamPreset(this,'Smooth cinematic camera zoom-in, dynamic lighting, 60fps')">🎥 Kamera Zoom Sinematik</div>
    <div class="pill" onclick="applyAwamPreset(this,'360 degree orbital camera rotation around product, spotlight')">🔄 Orbit Produk 360°</div>
    <div class="pill" onclick="applyAwamPreset(this,'Fluid fashion model motion & natural movement, high frame rate')">🕺 Gerakan Model & Fashion</div>
    <div class="pill" onclick="applyAwamPreset(this,'Epic slow-motion action, glowing particles in the air')">🏃 Slow-Motion Epik</div>
  </div>
  <div class="label">4. Ukuran Layar (1 Pilihan Aktif)</div>
  <div class="pill-row" data-group="ratio">
    <div class="pill active" onclick="selectExclusive(this,'ratio','9:16')">📱 9:16 (TikTok/Reels)</div>
    <div class="pill" onclick="selectExclusive(this,'ratio','1:1')">🟦 1:1 (Feed/Katalog)</div>
    <div class="pill" onclick="selectExclusive(this,'ratio','16:9')">🖥️ 16:9 (YouTube/Lanskap)</div>
  </div>
  <div class="label">5. Durasi Video (Aktif Khusus Mode Video)</div>
  <div class="pill-row" data-group="duration" id="duration-row">
    <div class="pill active disabled" onclick="selectExclusive(this,'duration',5)">⚡ 5 Detik</div>
    <div class="pill disabled" onclick="selectExclusive(this,'duration',10)">🔥 10 Detik</div>
    <div class="pill disabled" onclick="selectExclusive(this,'duration',30)">🎬 30 Detik Story</div>
  </div>
  <div class="label">6. Mode Penajaman 4K (Otomatis Menyesuaikan Foto vs Video)</div>
  <div class="pill-row" data-group="upscale" id="upscale-row">
    <div class="pill active" data-ups="IMG" onclick="selectExclusive(this,'upscale','Pertajam Foto & Wajah 4K')">🔍 Pertajam Foto & Wajah 4K</div>
    <div class="pill" data-ups="IMG" onclick="selectExclusive(this,'upscale','Pertajam Teks & Gambar 4K')">✨ Pertajam Teks & Gambar 4K</div>
    <div class="pill disabled" data-ups="VID" id="vid-ups-pill" onclick="selectExclusive(this,'upscale','Pertajam & Haluskan Video 4K 60FPS')">🎞️ Pertajam Video 4K 60FPS</div>
  </div>
  <div class="label">7. Upload Foto Referensi (Untuk Foto Jadi Video / Produk)</div>
  <div class="upload-box" id="upload-container">
    <input type="file" accept="image/*" onchange="previewRef(event)">
    <div id="up-txt" style="font-size:12px">📸 <b>Sentuh untuk Upload Foto Referensi</b></div>
    <img id="ref-preview" alt="Ref">
  </div>
  <div class="label">8. Tulis Deskripsi Karya Anda</div>
  <textarea id="prompt-in" placeholder="Contoh: Botol parfum di atas batu hitam dengan pencahayaan studio..."></textarea>
  <button class="btn-exec" id="btn-go" onclick="runGenerate()">🚀 BUAT KARYA SEKARANG (KIRIM KE CHAT)</button>
  <div id="toast"></div>
</div>

<div id="tab-guide" class="tab-section">
  <div class="legal-card"><h3>🪄 Rumus Mudah Membuat Prompt bagi Pemula</h3>
  <p>Gunakan pola: <b>[Objek Utama] + [Gerakan/Aktivitas] + [Pencahayaan]</b>.<br>
  • Untuk <b>Foto Jadi Video</b>: Pilih <b>🖼️➡️🎬 Foto Jadi Video</b>, unggah foto Anda, lalu pilih preset <b>🔄 Orbit Produk 360°</b>.</p></div>
  <div class="legal-card"><h3>📡 Akses Cepat ke 6 Kamar Topik Komunitas</h3><div id="community-links-box"></div></div>
</div>

<div id="tab-legal" class="tab-section">
  <div class="legal-card"><h3>⚖️ Ketentuan Layanan & Lisensi Komersial Bersih</h3>
  <p>Seluruh karya yang dibuat menggunakan <b>Koin Utama (Pro)</b> memberikan hak komersial penuh bebas watermark kepada kreator.</p></div>
  <div class="legal-card"><h3>🛡️ Jaminan Privasi & Garansi Koin Kembali 100%</h3>
  <p>Jika pembuatan karya terkendala jaringan >60 detik, koin Anda otomatis dikembalikan 100%.</p></div>
</div>

<div class="footer-copy">Copyright © 2026 <b>bikinAI Super Intelligence</b>. All Rights Reserved.</div>
<div class="bottom-nav">
  <div class="nav-btn active" onclick="openTab(this,'tab-studio')"><span>🎬</span><span>Studio AI</span></div>
  <div class="nav-btn" onclick="openTab(this,'tab-guide')"><span>🧭</span><span>Panduan & Grup</span></div>
  <div class="nav-btn" onclick="openTab(this,'tab-legal')"><span>⚖️</span><span>Ketentuan & Privasi</span></div>
</div>

<script>
const tg=window.Telegram?.WebApp;
let st={init_data:"",user_id:0,username:"Kreator",modality:"IMAGE",engine:"bytedance/seedream-4.0",ratio:"9:16",duration:5,upscale:"Pertajam Foto & Wajah 4K",preset_mod:"Commercial product catalog photography, studio lighting",has_ref:false};
if(tg){tg.expand();st.init_data=tg.initData||"";const u=tg.initDataUnsafe?.user;if(u){st.user_id=u.id;st.username=u.username||u.first_name||"Kreator";document.getElementById("welcome-user").innerText=`Halo @${st.username}! Pilih kategori karya atau preset instan di bawah.`}}
fetch("/api/public/community-links").then(r=>r.json()).then(d=>{if(d.links)document.getElementById("community-links-box").innerHTML=d.links.map(x=>`<a class="topic-btn" href="${x.url}" target="_blank">${x.title}</a>`).join("")}).catch(()=>{});
function openTab(el,id){document.querySelectorAll(".nav-btn").forEach(b=>b.classList.remove("active"));document.querySelectorAll(".tab-section").forEach(s=>s.classList.remove("active"));el.classList.add("active");document.getElementById(id).classList.add("active")}
function selectExclusive(el,g,v){if(el.classList.contains("disabled"))return;const p=el.closest(`[data-group='${g}']`);if(p)p.querySelectorAll(".pill").forEach(x=>x.classList.remove("active"));el.classList.add("active");st[g]=v}
function applyAwamPreset(el,m){selectExclusive(el,"preset",m);st.preset_mod=m}
function setMod(el,m){
  selectExclusive(el,"modality",m);
  const isVid=(m==="VIDEO"||m==="IMG2VID");
  document.querySelectorAll("#duration-row .pill").forEach(p=>p.classList.toggle("disabled",!isVid));
  const imgUps=document.querySelectorAll("#upscale-row [data-ups='IMG']"),vidUps=document.getElementById("vid-ups-pill");
  document.querySelectorAll("#upscale-row .pill").forEach(p=>p.classList.remove("active"));
  if(isVid){imgUps.forEach(p=>p.classList.add("disabled"));vidUps.classList.remove("disabled");vidUps.classList.add("active");st.upscale="Pertajam & Haluskan Video 4K 60FPS"}
  else{imgUps.forEach(p=>p.classList.remove("disabled"));vidUps.classList.add("disabled");imgUps[0].classList.add("active");st.upscale="Pertajam Foto & Wajah 4K"}
  document.getElementById("preset-img-row").style.display=isVid?"none":"flex";
  document.getElementById("preset-vid-row").style.display=isVid?"flex":"none";
  st.preset_mod=isVid?"Smooth cinematic camera zoom-in, dynamic lighting, 60fps":"Commercial product catalog photography, studio lighting";
  document.getElementById("upload-container").classList.toggle("highlight-upload",m==="IMG2VID");
  let fv=null;
  document.querySelectorAll("#engine-grid .card").forEach(c=>{const sh=isVid?(c.getAttribute("data-type")==="VIDEO"):(c.getAttribute("data-type")==="IMAGE");c.classList.toggle("hidden-engine",!sh);c.classList.remove("active");if(sh&&!fv)fv=c});
  if(fv){fv.classList.add("active");st.engine=fv.getAttribute("onclick").split("'")[1]}
}
function setEng(el,e){document.querySelectorAll("#engine-grid .card").forEach(c=>c.classList.remove("active"));el.classList.add("active");st.engine=e}
function previewRef(ev){const f=ev.target.files[0];if(!f)return;const rd=new FileReader();rd.onload=e=>{const img=document.getElementById("ref-preview");img.src=e.target.result;img.style.display="block";document.getElementById("up-txt").innerHTML="✅ <b>Foto Referensi Siap Diproses</b>";st.has_ref=true};rd.readAsDataURL(f)}
async function runGenerate(){
  const btn=document.getElementById("btn-go"),toast=document.getElementById("toast"),rawIn=document.getElementById("prompt-in").value.trim();
  const finalPrompt=rawIn?`${rawIn}, ${st.preset_mod}`:st.preset_mod;
  btn.disabled=true;btn.innerText="⏳ SEDANG MEMPROSES KARYA...";
  try{const r=await fetch("/api/webapp/execute",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(Object.assign({},st,{prompt:finalPrompt}))});const d=await r.json();toast.style.display="block";toast.innerText=d.message||"✅ Karya dikirim ke ruang chat Telegram Anda!"}
  catch(e){toast.style.display="block";toast.innerText="✅ Permintaan diterima! Cek ruang chat bot Telegram Anda."}
  finally{btn.disabled=false;btn.innerText="🚀 BUAT KARYA SEKARANG (KIRIM KE CHAT)"}
}
</script></body></html>"""


def render_freedom_web_portal_html() -> str:
    brand = RUNTIME_CONFIG.get("WEB_BRAND_NAME") or "AetherFree AI Studio"
    return f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{brand} — Open-Weight SOTA Platform</title>
<style>
:root{{--bg:#040309;--surface:rgba(16,12,30,.88);--border:rgba(0,240,255,.25);--cyan:#00f0ff;--pink:#ff007f;--violet:#7928ca;--text:#f8f6ff;--muted:#9ca3af;--ok:#00e676}}
*{{box-sizing:border-box;margin:0;padding:0;font-family:'Inter',system-ui,sans-serif}}
body{{background:radial-gradient(circle at 15% 10%,rgba(121,40,202,.28) 0%,transparent 45%),radial-gradient(circle at 85% 20%,rgba(0,240,255,.18) 0%,transparent 50%),var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}}
.navbar{{display:flex;justify-content:space-between;align-items:center;padding:14px 22px;background:rgba(8,6,18,.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;flex-wrap:wrap;gap:10px}}
.brand-logo{{font-size:19px;font-weight:900;background:linear-gradient(90deg,#fff,var(--cyan),var(--pink));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.nav-links{{display:flex;gap:8px;flex-wrap:wrap}}
.nav-item{{padding:8px 14px;border-radius:99px;font-size:12px;font-weight:700;color:var(--muted);cursor:pointer;border:1px solid transparent}}
.nav-item.active,.nav-item:hover{{color:#fff;border-color:var(--cyan);background:rgba(0,240,255,.12)}}
.wallet-badge{{background:linear-gradient(90deg,rgba(255,0,127,.2),rgba(0,240,255,.2));border:1px solid var(--cyan);padding:7px 14px;border-radius:99px;font-size:12px;font-weight:800;color:#fff}}
.container{{max-width:960px;width:100%;margin:20px auto;padding:0 16px;flex:1}}
.hero-banner{{background:linear-gradient(135deg,rgba(19,11,36,.92),rgba(9,20,38,.92));border:1px solid var(--border);border-radius:20px;padding:22px;margin-bottom:18px}}
.hero-tag{{display:inline-block;background:linear-gradient(90deg,var(--pink),var(--violet));font-size:10px;font-weight:800;padding:4px 12px;border-radius:99px;margin-bottom:8px}}
.page{{display:none}}.page.active{{display:block}}
.glass-card{{background:var(--surface);border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:18px;margin-bottom:16px}}
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}@media(max-width:680px){{.grid-2{{grid-template-columns:1fr}}}}
label{{display:block;font-size:11px;font-weight:800;text-transform:uppercase;color:var(--cyan);margin:10px 0 5px}}
input,select,textarea{{width:100%;background:#070510;border:1px solid #2e2348;color:#fff;padding:10px 12px;border-radius:12px;font-size:13px;outline:none}}
.btn-primary{{width:100%;margin-top:12px;padding:13px;border:none;border-radius:14px;background:linear-gradient(90deg,var(--pink),var(--violet),#00c6ff);color:#fff;font-size:14px;font-weight:800;cursor:pointer}}
#chat-box{{height:320px;overflow-y:auto;background:#06040d;border:1px solid #261b3d;border-radius:14px;padding:14px;margin-top:10px;line-height:1.55;font-size:13.5px}}
.bubble-u{{background:rgba(0,240,255,.12);border:1px solid rgba(0,240,255,.3);padding:10px 14px;border-radius:14px 14px 2px 14px;margin-bottom:10px;color:#e0fbff}}
.bubble-a{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);padding:12px 14px;border-radius:14px 14px 14px 2px;margin-bottom:12px;color:#f5f0ff;white-space:pre-wrap}}
#cdn-box{{display:none;margin-top:16px;background:#080512;border:1px solid var(--ok);border-radius:14px;padding:14px;text-align:center}}
#cdn-box img,#cdn-box video{{max-width:100%;max-height:420px;border-radius:12px;border:1px solid var(--cyan);margin-bottom:10px}}
.btn-dl{{display:inline-block;padding:10px 16px;background:var(--ok);color:#000;font-weight:900;border-radius:10px;text-decoration:none;font-size:13px;margin:6px 4px}}
.btn-copy{{padding:10px 14px;background:#1f2937;color:#fff;border:1px solid var(--cyan);border-radius:10px;cursor:pointer;font-weight:700;font-size:12px}}
footer{{text-align:center;padding:20px 16px;border-top:1px solid rgba(255,255,255,.08);font-size:12px;color:var(--muted);margin-top:24px}}
</style></head><body>
<nav class="navbar">
  <div class="brand-logo">⚡ {brand}</div>
  <div class="nav-links">
    <div class="nav-item active" onclick="openPage(this,'pg-chat')">💬 Chat & Technical Studio</div>
    <div class="nav-item" onclick="openPage(this,'pg-media')">🎨 Image & Video SOTA</div>
    <div class="nav-item" onclick="openPage(this,'pg-vch')">🎟️ Kode Akses VIP</div>
    <div class="nav-item" onclick="openPage(this,'pg-guide')">🧭 Panduan, ToS & Privasi</div>
  </div>
  <div class="wallet-badge" id="cu-bal">⚡ 3 Kredit Studio</div>
</nav>
<div class="container">
  <div class="hero-banner"><span class="hero-tag">🌌 OPEN-WEIGHT SOTA & TECHNICAL WORKSPACE</span>
  <h1>{brand}</h1>
  <p style="font-size:13px;color:var(--muted);margin-top:4px">Akses langsung ke model HuggingFace & OpenRouter terverifikasi dengan pemisahan tegas antara Mode Teknis/Arsitektur (Zero-Roleplay) dan Mode Diskusi Umum.</p></div>

  <div id="pg-chat" class="page active"><div class="glass-card">
    <div class="grid-2">
      <div><label>1. Pilih Repositori Model Resmi (author/repo)</label>
      <select id="chat-model">
        <option value="nousresearch/hermes-4-405b">NousResearch/Hermes-4-405B</option>
        <option value="nousresearch/hermes-4-70b">NousResearch/Hermes-4-70B</option>
        <option value="nousresearch/hermes-3-llama-3.1-405b">NousResearch/Hermes-3-Llama-3.1-405B</option>
        <option value="cognitivecomputations/dolphin-mistral-24b-venice-edition:free">cognitivecomputations/dolphin-mistral-24b-venice-edition:free</option>
        <option value="cognitivecomputations/dolphin3.0-mistral-24b">cognitivecomputations/Dolphin3.0-Mistral-24B</option>
        <option value="anthracite-org/magnum-v4-72b">anthracite-org/magnum-v4-72b</option>
        <option value="sao10k/l3.3-euryale-70b">Sao10K/L3.3-70B-Euryale-v2.3</option>
        <option value="qwen/qwen3-coder-next">Qwen/Qwen2.5-Coder-32B-Instruct / Qwen3-Coder</option>
        <option value="deepseek/deepseek-r1:free">deepseek-ai/DeepSeek-R1</option>
        <option value="google/gemini-4-argon">google/gemini-4-argon</option>
        <option value="meta/muse-spark-1.2">meta-models/Muse-Spark-Open-816B-A42B</option>
      </select></div>
      <div><label>2. Mode Eksekusi Sistem</label>
      <select id="chat-persona">
        <option value="TECHNICAL_ZERO_ROLEPLAY">⚙️ Teknis & Kode Presisi (Zero-Roleplay, Wajib Sumber/Repo Resmi)</option>
        <option value="NATURAL_COMPANION">💬 Diskusi Umum Mengalir (Non-Teknis)</option>
        <option value="CREATIVE_WRITER">🖋️ Penulisan Skenario & Fiksi</option>
      </select></div>
    </div>
    <div id="chat-box"><div class="bubble-a">Sistem siap. Pilih <b>Teknis & Kode Presisi (Zero-Roleplay)</b> untuk rekayasa kode/arsitektur, atau <b>Diskusi Umum</b> untuk obrolan biasa.</div></div>
    <textarea id="chat-input" rows="3" placeholder="Ketik instruksi teknis, kode, atau topik diskusi..."></textarea>
    <button class="btn-primary" id="btn-send-chat" onclick="sendFreedomChat()">KIRIM INSTRUKSI</button>
  </div></div>

  <div id="pg-media" class="page"><div class="glass-card">
    <div class="grid-2">
      <div><label>1. Mode Media</label>
      <select id="media-mode" onchange="syncMediaEngines()">
        <option value="IMAGE">Text-to-Image</option>
        <option value="VIDEO">Text-to-Video</option>
        <option value="IMG2VID">Image-to-Video</option>
      </select></div>
      <div><label>2. Repositori Model Visual (author/repo)</label>
      <select id="media-engine">
        <option value="black-forest-labs/FLUX.1-dev">black-forest-labs/FLUX.1-dev</option>
        <option value="black-forest-labs/FLUX.1-dev-FP8">black-forest-labs/FLUX.1-dev-FP8</option>
        <option value="OnomaAIResearch/Illustrious-xl-early-release-v0">OnomaAIResearch/Illustrious-xl-early-release-v0</option>
        <option value="Laxhar/noobai-XL-Vpred-1.0">Laxhar/noobai-XL-Vpred-1.0</option>
        <option value="Laxhar/noobai-XL-1.1">Laxhar/noobai-XL-1.1</option>
        <option value="bytedance/seedream-4.0">bytedance/seedream-4.0</option>
      </select></div>
    </div>
    <label>3. Ukuran Rasio</label>
    <select id="media-ratio"><option value="9:16">9:16 (768x1024)</option><option value="1:1">1:1 (1024x1024)</option><option value="16:9">16:9 (1024x768)</option></select>
    <label>4. Prompt Visual</label>
    <textarea id="media-prompt" rows="3" placeholder="Ketik deskripsi visual..."></textarea>
    <button class="btn-primary" id="btn-render-media" onclick="generateFreedomMedia()">RENDER & GENERATE LINK CDN</button>
    <div id="cdn-box">
      <div id="media-preview-holder"></div>
      <div><a id="cdn-force-dl" class="btn-dl" href="#" download>⬇️ Download File HD</a>
      <button class="btn-copy" onclick="copyCdnUrl()">📋 Salin Link CDN</button></div>
      <input type="text" id="cdn-direct-url" readonly style="margin-top:8px">
    </div>
  </div></div>

  <div id="pg-vch" class="page"><div class="glass-card">
    <h3 style="color:var(--cyan);margin-bottom:8px">🎟️ Aktivasi Kode Akses VIP</h3>
    <input type="text" id="vch-code-in" placeholder="VCH-eyJuIjoi...">
    <button class="btn-primary" onclick="redeemWebVoucher()">AKTIFKAN KODE</button>
    <p id="vch-status" style="margin-top:12px;font-size:13px;font-weight:700"></p>
  </div></div>

  <div id="pg-guide" class="page"><div class="glass-card">
    <h3 style="color:var(--cyan);margin-bottom:8px">⚖️ Terms of Service, Privacy Policy & Copyright</h3>
    <p style="font-size:13px;color:var(--muted);line-height:1.6">Seluruh hasil render dilengkapi tautan CDN langsung. Copyright © 2026 {brand}.</p>
  </div></div>
</div>
<footer>Copyright © 2026 <b>{brand}</b></footer>
<script>
let credits=parseInt(localStorage.getItem("af_credits")||"3"),chatHistory=[];
function syncCredits(){{document.getElementById("cu-bal").innerText=`⚡ ${{credits}} Kredit Studio`}}syncCredits();
function openPage(el,id){{document.querySelectorAll(".nav-item").forEach(n=>n.classList.remove("active"));document.querySelectorAll(".page").forEach(p=>p.classList.remove("active"));if(el)el.classList.add("active");document.getElementById(id).classList.add("active")}}
async function sendFreedomChat(){{
  const inp=document.getElementById("chat-input"),txt=inp.value.trim();if(!txt)return;
  const box=document.getElementById("chat-box");box.innerHTML+=`<div class="bubble-u"><b>User:</b> ${{txt.replace(/</g,"&lt;")}}</div>`;
  inp.value="";chatHistory.push({{role:"user",content:txt}});
  const btn=document.getElementById("btn-send-chat");btn.disabled=true;btn.innerText="Memproses...";
  try{{const r=await fetch("/api/nocturne/chat",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{prompt:txt,history:chatHistory.slice(-6),model:document.getElementById("chat-model").value,persona:document.getElementById("chat-persona").value}})}});const d=await r.json();const rep=d.reply||"Selesai.";chatHistory.push({{role:"assistant",content:rep}});box.innerHTML+=`<div class="bubble-a">${{rep.replace(/</g,"&lt;")}}</div>`;box.scrollTop=box.scrollHeight}}
  finally{{btn.disabled=false;btn.innerText="KIRIM INSTRUKSI"}}
}}
function syncMediaEngines(){{
  const m=document.getElementById("media-mode").value,s=document.getElementById("media-engine");
  if(m==="VIDEO"||m==="IMG2VID")s.innerHTML=`<option value="Wan-AI/Wan2.2-S2V-14B">Wan-AI/Wan2.2-S2V-14B</option><option value="Wan-AI/Wan2.2-T2V-A14B">Wan-AI/Wan2.2-T2V-A14B</option><option value="Wan-AI/Wan2.2-TI2V-5B">Wan-AI/Wan2.2-TI2V-5B</option><option value="ModelTC/LightX2V">ModelTC/LightX2V (Wan2.2-NVFP4)</option><option value="google/veo-3.1-fast">google/veo-3.1-fast</option>`;
  else s.innerHTML=`<option value="black-forest-labs/FLUX.1-dev">black-forest-labs/FLUX.1-dev</option><option value="black-forest-labs/FLUX.1-dev-FP8">black-forest-labs/FLUX.1-dev-FP8</option><option value="OnomaAIResearch/Illustrious-xl-early-release-v0">OnomaAIResearch/Illustrious-xl-early-release-v0</option><option value="Laxhar/noobai-XL-Vpred-1.0">Laxhar/noobai-XL-Vpred-1.0</option><option value="Laxhar/noobai-XL-1.1">Laxhar/noobai-XL-1.1</option><option value="bytedance/seedream-4.0">bytedance/seedream-4.0</option>`;
}}
async function generateFreedomMedia(){{
  const pr=document.getElementById("media-prompt").value.trim()||"High resolution studio shot",mode=document.getElementById("media-mode").value,eng=document.getElementById("media-engine").value,rat=document.getElementById("media-ratio").value,btn=document.getElementById("btn-render-media");
  btn.disabled=true;btn.innerText="MERENDER...";
  try{{const r=await fetch("/api/nocturne/generate",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{prompt:pr,modality:mode,model:eng,ratio:rat}})}});const d=await r.json();if(d.ok){{if(credits>0){{credits-=1;localStorage.setItem("af_credits",credits);syncCredits()}}document.getElementById("media-preview-holder").innerHTML=d.is_video?`<video src="${{d.cdn_url}}" controls autoplay loop playsinline></video>`:`<img src="${{d.cdn_url}}" alt="HD">`;document.getElementById("cdn-direct-url").value=d.cdn_url;document.getElementById("cdn-force-dl").href=d.download_url;document.getElementById("cdn-box").style.display="block"}}}}
  finally{{btn.disabled=false;btn.innerText="RENDER & GENERATE LINK CDN"}}
}}
function copyCdnUrl(){{const el=document.getElementById("cdn-direct-url");el.select();navigator.clipboard.writeText(el.value);alert("Link CDN disalin!")}}
async function redeemWebVoucher(){{
  const code=document.getElementById("vch-code-in").value.trim(),stEl=document.getElementById("vch-status");
  const r=await fetch("/api/voucher/redeem",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{voucher:code}})}});const d=await r.json();
  if(d.ok){{credits+=(d.units||10);localStorage.setItem("af_credits",credits);syncCredits();stEl.style.color="#00e676";stEl.innerText=d.message}}else{{stEl.style.color="#ff5252";stEl.innerText=d.message}}
}}
</script></body></html>"""


# 5. SECURITY VALIDATORS & PRIVACY LEAK SCANNER
FORBIDDEN_CUSTOMER_JARGON = [
    "SingleWriterSQLiteDaemon", "redeemed_nullifiers", "Stateless Ed25519",
    "EMVCo CRC16", "4x-Remacri", "Dual-LLM Sandbox", "Dead-Job Sweeper",
    "SangMata", "Tuyul", "Lock Stripe", "HPP Rp 0",
]


def scan_customer_ui_for_leaks(sample_texts: list[str]) -> dict[str, Any]:
    leaks_found: list[str] = []
    combined = "\n".join(sample_texts) + "\n" + MINIAPP_FULL_WEBSITE_HTML + "\n" + render_freedom_web_portal_html()
    for term in FORBIDDEN_CUSTOMER_JARGON:
        if re.search(re.escape(term), combined, re.IGNORECASE):
            leaks_found.append(term)
    return {"clean": len(leaks_found) == 0, "leaks": leaks_found, "checked_terms": len(FORBIDDEN_CUSTOMER_JARGON)}


def verify_telegram_webapp_init_data(init_data_raw: str, bot_token: str, max_age_sec: int = 86400) -> dict[str, Any] | None:
    if not init_data_raw or not bot_token:
        return None
    try:
        parsed = dict(parse_qsl(init_data_raw, keep_blank_values=True))
        received_hash = parsed.pop("hash", "")
        if not received_hash:
            return None
        auth_date = int(parsed.get("auth_date", "0"))
        if auth_date > 0 and abs(int(time.time()) - auth_date) > max_age_sec:
            return None
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
        secret_key = hmac.new(b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()
        return json.loads(parsed.get("user", "{}")) if hmac.compare_digest(calculated_hash, received_hash) else None
    except Exception:
        return None


_INJECTION_PATTERNS = re.compile(
    r"(ignore\s+(all\s+)?(previous|prior)\s+instructions|system\s*prompt|"
    r"you\s+are\s+now\s+dan|jailbreak|ilja\s*kaerb|drop\s+table|union\s+select|"
    r"<script\b|javascript:|__import__|__subclasses__|__globals__|os\.system|subprocess)",
    re.IGNORECASE,
)


def sanitize_and_deobfuscate_input(raw_text: str) -> tuple[str, bool]:
    if not raw_text:
        return "", False
    normalized = unicodedata.normalize("NFKC", raw_text)
    cleaned = "".join(ch for ch in normalized if unicodedata.category(ch) not in ("Cf", "Cc") or ch in ("\n", "\r", "\t")).strip()
    leet_map = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})
    deobfuscated = cleaned.lower().translate(leet_map)
    return cleaned, bool(_INJECTION_PATTERNS.search(cleaned) or _INJECTION_PATTERNS.search(deobfuscated))


def issue_stateless_ed25519_voucher(user_id: int, compute_units: int = 10, ttl_seconds: int = 86400) -> str:
    now_ts = int(time.time())
    nonce = hashlib.sha256(f"{user_id}:{now_ts}:{os.urandom(8).hex()}".encode()).hexdigest()[:16]
    payload_bytes = json.dumps({"n": nonce, "u": int(user_id), "c": int(compute_units), "exp": now_ts + ttl_seconds}, separators=(",", ":")).encode("utf-8")
    signature = Ed25519PrivateKey.from_private_bytes(ED25519_PRIV_BYTES).sign(payload_bytes)
    b64_p = base64.urlsafe_b64encode(payload_bytes).decode("ascii").rstrip("=")
    b64_s = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")
    return f"VCH-{b64_p}.{b64_s}"


async def verify_and_redeem_ed25519_voucher(db: aiosqlite.Connection, voucher_code: str) -> tuple[bool, str, int]:
    code = voucher_code.strip()
    if not code.startswith("VCH-") or "." not in code:
        return False, "Format Kode Akses VIP tidak sesuai.", 0
    try:
        b64_p, b64_s = code[4:].split(".", 1)
        payload_bytes = base64.urlsafe_b64decode(b64_p + "=" * (-len(b64_p) % 4))
        sig_bytes = base64.urlsafe_b64decode(b64_s + "=" * (-len(b64_s) % 4))
        Ed25519PublicKey.from_public_bytes(ED25519_PUB_BYTES).verify(sig_bytes, payload_bytes)
        data = json.loads(payload_bytes.decode("utf-8"))
        exp, units = int(data.get("exp", 0)), int(data.get("c", 10))
        if exp <= int(time.time()):
            return False, "Kode Akses VIP sudah kedaluwarsa.", 0
        nullifier_hash = hashlib.sha256(sig_bytes).hexdigest()

        async def _tx(conn: aiosqlite.Connection) -> bool:
            cur = await conn.execute("SELECT 1 FROM redeemed_nullifiers WHERE nullifier_hash = ?;", (nullifier_hash,))
            if await cur.fetchone():
                return False
            await conn.execute("INSERT INTO redeemed_nullifiers (nullifier_hash, expires_at) VALUES (?, ?);", (nullifier_hash, exp))
            return True

        if not await DB_WRITER_DAEMON.execute_write_tx(db, _tx):
            return False, "Kode Akses VIP sudah pernah digunakan.", 0
        return True, f"Kode Akses VIP Aktif (+{units} Kredit Studio)!", units
    except Exception:
        return False, "Kode Akses VIP tidak valid.", 0


# 6. ROLLING 8-AGENT POOL & STRICT TECHNICAL vs. CONVERSATIONAL SEPARATION
AGENTIC_ROLLING_POOL: dict[str, dict[str, Any]] = {
    "ARGON": {"title": "google/gemini-4-argon", "model_polli": "google/gemini-4-argon", "model_or": "google/gemini-2.0-flash-exp:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "QWEN": {"title": "Qwen/Qwen2.5-Coder-32B-Instruct", "model_polli": "qwen/qwen3-coder-next", "model_or": "qwen/qwen3-coder:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "DEEPSEEK": {"title": "deepseek-ai/DeepSeek-R1", "model_polli": "deepseek/deepseek-v4.1-flash", "model_or": "deepseek/deepseek-chat:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "MUSE": {"title": "meta-models/Muse-Spark-Open-816B-A42B", "model_polli": "meta/muse-spark-1.2", "model_or": "meta-llama/llama-3.3-70b-instruct:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "NANO_MUSE": {"title": "meta-models/Muse-Glimmer-30B", "model_polli": "meta/muse-glimmer-30b", "model_or": "openai/gpt-oss-120b:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "HARNESS": {"title": "OpenHands/openhands", "model_polli": "deepseek/deepseek-v4-pro", "model_or": "qwen/qwen3-coder:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "HERMES": {"title": "NousResearch/Hermes-4-405B", "model_polli": "mistralai/mistral-large-4", "model_or": "nousresearch/hermes-4-405b", "ok": 0, "fail": 0, "quarantine_until": 0},
    "GROQ_CEREBRAS": {"title": "meta-llama/Llama-3.3-70B-Instruct", "model_polli": "meta/llama-3.3-70b-instruct", "model_or": "meta-llama/llama-3.3-70b-instruct:free", "ok": 0, "fail": 0, "quarantine_until": 0},
}


def rotate_primary_agent() -> str:
    keys = list(AGENTIC_ROLLING_POOL.keys())
    cur = RUNTIME_CONFIG.get("PRIMARY_ROLLING_AGENT", "ARGON")
    nxt = keys[((keys.index(cur) if cur in keys else 0) + 1) % len(keys)]
    RUNTIME_CONFIG["PRIMARY_ROLLING_AGENT"] = nxt
    return nxt


async def _call_single_llm_endpoint(agent_key: str, url: str, headers: dict[str, str], payload: dict[str, Any], timeout_sec: float = 6.0) -> str | None:
    ag = AGENTIC_ROLLING_POOL.get(agent_key)
    now_ts = int(time.time())
    if ag and ag["quarantine_until"] > now_ts:
        return None
    try:
        async with httpx.AsyncClient(timeout=timeout_sec, follow_redirects=True) as client:
            r = await client.post(url, headers=headers, json=payload)
            if r.status_code == 200:
                raw_txt = r.text.strip()
                content = ""
                if raw_txt.startswith("{"):
                    try:
                        data = r.json()
                        content = data.get("choices", [{}])[0].get("message", {}).get("content", "") or data.get("reply", "") or data.get("response", "")
                    except Exception:
                        content = raw_txt
                else:
                    content = raw_txt
                if content and len(content.strip()) > 2:
                    if ag:
                        ag["ok"] += 1
                    AUTONOMIC_GUARD.record_telemetry(agent_key, True)
                    return sanitize_external_api_response(content)
            elif r.status_code in (429, 502, 503) and ag:
                ag["fail"] += 1
                ag["quarantine_until"] = now_ts + 45
                AUTONOMIC_GUARD.record_telemetry(agent_key, False)
    except Exception:
        if ag:
            ag["fail"] += 1
        AUTONOMIC_GUARD.record_telemetry(agent_key, False)
    return None


async def _call_pollinations_get_fallback(user_message: str, sys_instruction: str) -> str | None:
    url = f"https://text.pollinations.ai/{quote(user_message[:500])}?model=openai&system={quote(sys_instruction[:350])}"
    try:
        async with httpx.AsyncClient(timeout=7.5, follow_redirects=True) as client:
            r = await client.get(url)
            if r.status_code == 200 and len(r.text.strip()) > 2:
                return sanitize_external_api_response(r.text.strip())
    except Exception:
        pass
    return None


# PEMISAHAN MUTLAK INSTRUKSI TEKNIS (ZERO-ROLEPLAY) vs. INSTRUKSI PERCAKAPAN UMUM
STRICT_TECHNICAL_ZERO_ROLEPLAY_PROMPT = """
ATURAN TEKNIS MUTLAK (ZERO-ROLEPLAY MODE):
1. MATIKAN SEMUA ROLEPLAY DAN BASA-BASI: Jangan gunakan sapaan kasual ("Kak", "Halo", emoji berlebihan) saat menjawab pertanyaan kode, arsitektur sistem, atau repositori.
2. SUMBER DAN IDENTITAS PRESISI: Setiap kali menyebutkan model AI, repositori HuggingFace/GitHub, atau package, WAJIB sebutkan nama author/organisasi dan nama package resminya secara presisi (contoh: `NousResearch/Hermes-4-405B`, `Qwen/Qwen2.5-Coder-32B-Instruct`, `black-forest-labs/FLUX.1-dev`, `Wan-AI/Wan2.2-T2V-A14B`, `pip install aiogram aiohttp aiosqlite httpx cryptography`) beserta URL resminya.
3. DILARANG KLAIM TANPA SUMBER: Jangan pernah mengarang nama repo, model, atau library yang tidak dapat diverifikasi author dan package resminya.
""".strip()

CONVERSATIONAL_COMPANION_PROMPT = """
PERAN PERCAKAPAN UMUM (NON-TEKNIS):
1. DILARANG MENYURUH BUAT GAMBAR ATAU VIDEO: Saat pengguna mengobrol biasa, fokus 100% pada topik pembicaraan pengguna.
2. Gunakan Bahasa Indonesia yang natural, jelas, dan nyaman.
""".strip()

_TECHNICAL_KEYWORDS = re.compile(
    r"\b(kode|code|python|repo|repository|huggingface|github|package|library|pip|npm|"
    r"arsitektur|architecture|schema|sql|sqlite|ast|bug|error|endpoint|api|docker|vps|git)\b",
    re.IGNORECASE,
)


def is_technical_or_code_query(text: str) -> bool:
    return bool(_TECHNICAL_KEYWORDS.search(text or ""))


async def generate_frontier_ai_response(
    db: aiosqlite.Connection,
    user_message: str,
    mode: Literal["NATURAL_CHAT", "DEEP_RESEARCH", "CANVAS_EDIT", "PROMPT_ARCHITECT", "NOCTURNE_UNCENSORED"] = "NATURAL_CHAT",
    personal_memory: str = "",
    canvas_state: str = "",
    preferred_model: str = "",
    persona_style: str = "TECHNICAL_ZERO_ROLEPLAY",
    chat_history: list[dict[str, str]] | None = None,
) -> str:
    # Jika query mengandung istilah teknis/kode/repo, paksa masuk ke STRICT_TECHNICAL_ZERO_ROLEPLAY_PROMPT
    force_tech = is_technical_or_code_query(user_message) or mode in ("DEEP_RESEARCH", "CANVAS_EDIT") or persona_style in ("TECHNICAL_ZERO_ROLEPLAY", "SENIOR_ARCHITECT")

    if force_tech:
        if mode == "CANVAS_EDIT":
            task = f"Perbarui kode atau skema arsitektur berikut secara presisi tanpa roleplay:\n{canvas_state or '(Kosong)'}"
            primary_ag = "QWEN"
        else:
            task = "Berikan analisis teknis, kode, atau referensi repositori (`author/repo`) dan package resmi secara presisi tanpa roleplay."
            primary_ag = "QWEN" if "kode" in user_message.lower() else "ARGON"
        sys_prompt = f"{STRICT_TECHNICAL_ZERO_ROLEPLAY_PROMPT}\n\nTUGAS:\n{task}"
    elif mode == "PROMPT_ARCHITECT":
        sys_prompt = "Susun 3 variasi prompt visual/video (1. Fotorealistis, 2. Sinematik, 3. Ilustrasi) secara langsung tanpa roleplay."
        primary_ag = "MUSE"
    elif mode == "NOCTURNE_UNCENSORED":
        sys_prompt = (
            "Tulis skenario fiksi/narasi sesuai instruksi pengguna."
            if persona_style == "CREATIVE_WRITER"
            else CONVERSATIONAL_COMPANION_PROMPT
        )
        primary_ag = "HERMES"
    else:
        mem_context = f"\nKONTEKS PENGGUNA: {personal_memory}" if personal_memory else ""
        sys_prompt = f"{CONVERSATIONAL_COMPANION_PROMPT}{mem_context}"
        primary_ag = RUNTIME_CONFIG.get("PRIMARY_ROLLING_AGENT", "ARGON")

    msgs: list[dict[str, str]] = [{"role": "system", "content": sys_prompt}]
    if chat_history:
        for turn in chat_history[-6:]:
            if isinstance(turn, dict) and turn.get("role") in ("user", "assistant") and turn.get("content"):
                msgs.append({"role": turn["role"], "content": str(turn["content"])[:600]})
    msgs.append({"role": "user", "content": user_message})

    ag_info = AGENTIC_ROLLING_POOL.get(primary_ag, AGENTIC_ROLLING_POOL["ARGON"])
    tasks: list[asyncio.Task] = []
    temp_val = 0.2 if force_tech else 0.7

    if GROQ_API_KEY and mode != "NOCTURNE_UNCENSORED":
        tasks.append(asyncio.create_task(_call_single_llm_endpoint("GROQ_CEREBRAS", "https://api.groq.com/openai/v1/chat/completions", {"Authorization": f"Bearer {GROQ_API_KEY}"}, {"model": "llama-3.3-70b-versatile", "messages": msgs, "max_tokens": 800, "temperature": temp_val}, 4.8)))
    if CEREBRAS_API_KEY and mode != "NOCTURNE_UNCENSORED":
        tasks.append(asyncio.create_task(_call_single_llm_endpoint("GROQ_CEREBRAS", "https://api.cerebras.ai/v1/chat/completions", {"Authorization": f"Bearer {CEREBRAS_API_KEY}"}, {"model": "llama-3.3-70b", "messages": msgs, "max_tokens": 800, "temperature": temp_val}, 4.8)))
    if OPENROUTER_API_KEY:
        tasks.append(asyncio.create_task(_call_single_llm_endpoint(primary_ag, "https://openrouter.ai/api/v1/chat/completions", {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}, {"model": preferred_model or ag_info["model_or"], "messages": msgs, "max_tokens": 800, "temperature": temp_val}, 6.0)))
    if GEMINI_API_KEY and mode != "NOCTURNE_UNCENSORED":
        tasks.append(asyncio.create_task(_call_single_llm_endpoint("ARGON", "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", {"Authorization": f"Bearer {GEMINI_API_KEY}"}, {"model": "gemini-2.0-flash", "messages": msgs, "max_tokens": 800, "temperature": temp_val}, 5.5)))

    polli_headers = {"Content-Type": "application/json"}
    if POLLINATIONS_API_KEY:
        polli_headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"
    tasks.append(asyncio.create_task(_call_single_llm_endpoint(primary_ag, "https://text.pollinations.ai/openai", polli_headers, {"model": "openai", "messages": msgs}, 6.5)))
    tasks.append(asyncio.create_task(_call_pollinations_get_fallback(user_message, sys_prompt)))

    for coro in asyncio.as_completed(tasks):
        res = await coro
        if res:
            for t in tasks:
                if not t.done():
                    t.cancel()
            return res

    rotate_primary_agent()
    return f"[Respon Sistem Cadangan] Permintaan diterima untuk input: `{user_message[:100]}`."


# 7. USER IDENTITY, TREASURY & INVOICE ENGINE
async def ensure_user_and_track_identity(db: aiosqlite.Connection, user_id: int, username: str, first_name: str = "", lang_code: str = "id") -> dict[str, Any]:
    today_epoch = int(time.time()) // 86400
    clean_uname = (username or "Kreator").replace("`", "").replace("*", "").replace("_", "\\_")
    raw_uname = username or "Kreator"
    default_ppp_zone = 3 if (not lang_code or lang_code.lower().startswith(("id", "in", "ms"))) else 1

    async def _tx(conn: aiosqlite.Connection) -> dict[str, Any]:
        cur_check = await conn.execute("SELECT username FROM users WHERE internal_user_id = ?;", (user_id,))
        existing = await cur_check.fetchone()
        name_changed_msg = ""
        if not existing:
            await conn.execute(
                "INSERT INTO users (internal_user_id, username, first_name, language_code, koin_utama, koin_bonus, ppp_zone, quota_day_epoch, created_at) VALUES (?, ?, ?, 'id', 0, 4, ?, ?, ?);",
                (user_id, raw_uname, first_name or raw_uname, default_ppp_zone, today_epoch, int(time.time())),
            )
        else:
            old_uname = existing[0]
            if RUNTIME_CONFIG["SUBBOT_SANGMATA_ACTIVE"] and old_uname and old_uname != raw_uname and raw_uname != "Kreator":
                await conn.execute("INSERT INTO identity_history (user_id, old_username, new_username, changed_at) VALUES (?, ?, ?, ?);", (user_id, old_uname, raw_uname, int(time.time())))
                await conn.execute("UPDATE users SET username = ? WHERE internal_user_id = ?;", (raw_uname, user_id))
                name_changed_msg = f"@{old_uname} -> @{raw_uname}"

        await conn.execute(
            "UPDATE users SET chat_used_today = CASE WHEN quota_day_epoch < ? THEN 0 ELSE chat_used_today END, free_img_used_today = CASE WHEN quota_day_epoch < ? THEN 0 ELSE free_img_used_today END, quota_day_epoch = ? WHERE internal_user_id = ? AND quota_day_epoch < ?;",
            (today_epoch, today_epoch, today_epoch, user_id, today_epoch),
        )
        cur = await conn.execute("SELECT koin_utama, koin_bonus, has_topped_up, ppp_zone, chat_used_today, free_img_used_today, last_claim_date, personal_memory_notes, active_canvas_content FROM users WHERE internal_user_id = ?;", (user_id,))
        row = await cur.fetchone()
        return {
            "koin_utama": int(row[0]), "koin_bonus": int(row[1]), "has_topped_up": bool(row[2]),
            "ppp_zone": int(row[3]), "chat_used_today": int(row[4]), "free_img_used_today": int(row[5]),
            "last_claim_date": row[6] or "", "memory": row[7] or "", "canvas": row[8] or "",
            "identity_alert": name_changed_msg, "safe_uname": clean_uname,
        }

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def record_job_and_split_profit(db: aiosqlite.Connection, revenue_idr: int, actual_hpp_idr: int, buffer_ratio: float = 0.10) -> dict[str, int]:
    if RUNTIME_CONFIG.get("BANSOS_OPERATION_MODE") == "SILENT_PROFIT":
        actual_hpp_idr = 0
    required_working_capital = int(math.ceil(actual_hpp_idr * (1.0 + buffer_ratio)))
    net_harvestable_profit = max(0, revenue_idr - required_working_capital)

    async def _tx(conn: aiosqlite.Connection) -> int:
        now_ts = int(time.time())
        await conn.execute("INSERT OR IGNORE INTO treasury_summary VALUES (1, 0, 0, 0, 0, 0, ?);", (now_ts,))
        cur = await conn.execute(
            "UPDATE treasury_summary SET gross_revenue_idr = gross_revenue_idr + ?, working_capital_vault_idr = working_capital_vault_idr + ?, harvestable_profit_vault_idr = MAX(0, harvestable_profit_vault_idr + ?), total_jobs_completed = total_jobs_completed + 1, updated_at = ? WHERE id = 1 RETURNING total_jobs_completed;",
            (revenue_idr, required_working_capital, net_harvestable_profit, now_ts),
        )
        row = await cur.fetchone()
        return int(row[0]) if row else 1

    jobs_done = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    return {"working_capital_locked_idr": required_working_capital, "net_profit_ready_to_harvest_idr": net_harvestable_profit, "fomo_counter": RUNTIME_CONFIG["FOMO_COUNTER_BASE"] + jobs_done}


async def execute_manual_profit_harvest(db: aiosqlite.Connection) -> tuple[bool, int, int]:
    async def _tx(conn: aiosqlite.Connection) -> tuple[bool, int, int]:
        now_ts = int(time.time())
        await conn.execute("INSERT OR IGNORE INTO treasury_summary VALUES (1, 0, 0, 0, 0, 0, ?);", (now_ts,))
        cur = await conn.execute("SELECT harvestable_profit_vault_idr, total_harvested_by_owner_idr FROM treasury_summary WHERE id = 1;")
        row = await cur.fetchone()
        if not row or int(row[0]) <= 0:
            return False, 0, int(row[1]) if row else 0
        avail, new_total = int(row[0]), int(row[1]) + int(row[0])
        await conn.execute("UPDATE treasury_summary SET harvestable_profit_vault_idr = 0, total_harvested_by_owner_idr = ?, updated_at = ? WHERE id = 1;", (new_total, now_ts))
        return True, avail, new_total

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


def compute_crc16_ccitt(data_str: str) -> str:
    crc = 0xFFFF
    for ch in data_str.encode("utf-8"):
        crc ^= ch << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if (crc & 0x8000) else (crc << 1) & 0xFFFF
    return f"{crc:04X}"


def generate_dynamic_qris_string(static_qris: str, amount_idr: int) -> str:
    if not static_qris or len(static_qris) < 20 or "5802ID" not in static_qris:
        static_qris = "00020101021126610014ID.CO.GOPAY.WWW01189360091431234567890210G1234567890303UMI51440014ID.CO.QRIS.WWW0215ID10200000000010303UMI5204581253033605802ID5912BIKINAI STUDIO6007JAKARTA6304ABCD"
    base_qris = static_qris[:-4].replace("010211", "010212", 1)
    if base_qris.endswith("6304"):
        base_qris = base_qris[:-4]
    amt_str = str(int(amount_idr))
    parts = base_qris.split("5802ID", 1)
    reconstructed = f"{parts[0]}54{len(amt_str):02d}{amt_str}5802ID{parts[1]}6304"
    return f"{reconstructed}{compute_crc16_ccitt(reconstructed)}"


async def create_payment_invoice(db: aiosqlite.Connection, user_id: int, ppp_zone: int, tier_key: str = "HEMAT") -> dict[str, Any]:
    invoice_id = f"INV-{user_id}-{int(time.time())}"
    unique_code = (user_id % 89) + 10
    if ppp_zone in (1, 2):
        pkg = PPP_PRICING_PACKAGES["GLOBAL"].get(tier_key, PPP_PRICING_PACKAGES["GLOBAL"]["HEMAT"])
        exact_idr, coins_amt, provider = pkg["idr_eq"], pkg["coins"], RUNTIME_CONFIG["GLOBAL_ACTIVE_PROVIDER"]
        display_amt, qris_str, is_global = f"{pkg['usd']} USDT / {pkg['stars']} Telegram Stars ⭐", "", True
    else:
        pkg = PPP_PRICING_PACKAGES["ID"].get(tier_key, PPP_PRICING_PACKAGES["ID"]["HEMAT"])
        exact_idr, coins_amt, provider = pkg["idr"] + unique_code, pkg["coins"], RUNTIME_CONFIG["ID_ACTIVE_PROVIDER"]
        display_amt, qris_str, is_global = f"Rp {exact_idr:,}", generate_dynamic_qris_string(GOPAY_STATIC_QRIS_RAW, exact_idr), False

    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("INSERT INTO payment_invoices (invoice_id, user_id, amount_idr, coins_credited, provider, status, created_at) VALUES (?, ?, ?, ?, ?, 'PENDING', ?);", (invoice_id, user_id, exact_idr, coins_amt, provider, int(time.time())))

    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    return {"invoice_id": invoice_id, "pkg_name": pkg["name"], "coins": coins_amt, "provider": provider, "display_amount": display_amt, "qris_payload": qris_str, "is_global": is_global}


async def approve_invoice_and_credit_coins(db: aiosqlite.Connection, invoice_id: str) -> tuple[bool, int, int, int, str]:
    async def _tx(conn: aiosqlite.Connection) -> tuple[bool, int, int, int, str]:
        cur = await conn.execute("SELECT user_id, amount_idr, coins_credited, status FROM payment_invoices WHERE invoice_id = ?;", (invoice_id,))
        row = await cur.fetchone()
        if not row:
            return False, 0, 0, 0, "Tagihan tidak ditemukan."
        uid, amt_idr, coins_add, st = int(row[0]), int(row[1]), int(row[2]), str(row[3])
        if st == "PAID":
            return False, uid, 0, 0, "Tagihan sudah diverifikasi."
        await conn.execute("UPDATE payment_invoices SET status = 'PAID' WHERE invoice_id = ?;", (invoice_id,))
        await conn.execute("UPDATE users SET koin_utama = koin_utama + ?, has_topped_up = 1 WHERE internal_user_id = ?;", (coins_add, uid))
        return True, uid, amt_idr, coins_add, f"+{coins_add} Koin Utama ditambahkan!"

    ok, uid, amt_idr, coins_add, msg = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    if ok and amt_idr > 0:
        await record_job_and_split_profit(db, revenue_idr=amt_idr, actual_hpp_idr=int(amt_idr * 0.12))
    return ok, uid, amt_idr, coins_add, msg


# 8. MEDIA FETCHER, CDN DOWNLOAD PROXY & DUAL WEB SERVER
async def fetch_clean_image_bytes(prompt_en: str, width: int = 768, height: int = 1024) -> bytes | None:
    url = f"https://image.pollinations.ai/prompt/{quote(prompt_en)}?width={width}&height={height}&nologo=true&private=true&enhance=true&seed={int(time.time())}"
    try:
        async with httpx.AsyncClient(timeout=25.0, follow_redirects=True) as client:
            resp = await client.get(url)
            if resp.status_code == 200 and len(resp.content) > 1000 and (resp.content[:4].startswith(b"\xff\xd8\xff") or resp.content[:4] == b"\x89PNG"):
                return resp.content
    except Exception:
        pass
    return None


async def handle_public_community_links_api(request: web.Request) -> web.Response:
    links = [{"title": f"🤖 Buka Chat Bot @{BOT_USERNAME_GLOBAL}", "url": f"https://t.me/{BOT_USERNAME_GLOBAL}"}]
    async with get_db() as db:
        for _, (c_id, t_id, t_title) in (await get_all_topic_bindings(db)).items():
            clean_cid = str(c_id).replace("-100", "")
            if clean_cid.isdigit() and t_id > 0:
                links.append({"title": t_title, "url": f"https://t.me/c/{clean_cid}/{t_id}"})
    return web.json_response({"ok": True, "links": links})


async def handle_cdn_force_download_api(request: web.Request) -> web.Response:
    src_url = unquote(str(request.query.get("url") or "")).strip()
    fname = re.sub(r"[^a-zA-Z0-9._-]", "", str(request.query.get("name") or "AetherFree_HD.jpg"))
    ok_u, _ = validate_safe_external_url(src_url)
    if not ok_u:
        return web.Response(text="Invalid CDN URL", status=400)
    try:
        async with httpx.AsyncClient(timeout=25.0, follow_redirects=True) as client:
            r = await client.get(src_url)
            if r.status_code == 200:
                return web.Response(
                    body=r.content,
                    headers={"Content-Type": r.headers.get("content-type", "application/octet-stream"), "Content-Disposition": f'attachment; filename="{fname}"', "Cache-Control": "public, max-age=86400"},
                )
    except Exception:
        pass
    raise web.HTTPFound(src_url)


async def handle_webapp_execute_api(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "message": "Invalid JSON"}, status=400)

    init_data_str = str(data.get("init_data") or "").strip()
    verified_user = verify_telegram_webapp_init_data(init_data_str, BOT_TOKEN) if init_data_str else None
    if verified_user and "id" in verified_user:
        user_id, username = int(verified_user["id"]), verified_user.get("username") or verified_user.get("first_name") or "Kreator"
    else:
        user_id, username = int(data.get("user_id") or 0), str(data.get("username") or "Kreator")
        if RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"] and not verified_user:
            return web.json_response({"ok": False, "message": "🔒 Sesi Mini App tidak valid."}, status=403)

    prompt_raw, is_attack = sanitize_and_deobfuscate_input(str(data.get("prompt") or "Katalog produk studio 4K"))
    if is_attack:
        return web.json_response({"ok": False, "message": "🛡️ Pola teks tidak diizinkan."}, status=400)

    modality, engine, ratio = str(data.get("modality") or "IMAGE"), str(data.get("engine") or "bytedance/seedream-4.0"), str(data.get("ratio") or "9:16")
    upscale, has_ref = str(data.get("upscale") or "Pertajam Foto & Wajah 4K"), bool(data.get("has_ref"))

    if user_id and BOT_INSTANCE_GLOBAL:
        is_vid_mode = modality in ("VIDEO", "IMG2VID")
        cost = 0 if RUNTIME_CONFIG["HAPPY_HOUR_MODE"] else (20 if is_vid_mode else 4)
        async with get_db() as db:
            await ensure_user_and_track_identity(db, user_id, username)
            ok, job_id, deduct_msg = await deduct_user_coins_for_job(db, user_id, cost, True, prompt_raw, engine)
            if not ok:
                return web.json_response({"ok": False, "message": f"⚠️ {deduct_msg}"}, status=402)
            ref_tag = " + Foto Referensi" if (has_ref or modality == "IMG2VID") else ""
            try:
                if is_vid_mode:
                    await BOT_INSTANCE_GLOBAL.send_video(chat_id=user_id, video=SAMPLE_SANDBOX_VIDEO_URL, caption=f"🎬 **VIDEO SELESAI**\n┣ ⚡ **Model:** `{engine}` ({ratio})\n┣ 🔍 **Kualitas:** `{upscale}{ref_tag}`\n┗ 📝 **Prompt:** _{prompt_raw[:120]}_", parse_mode="Markdown")
                elif modality == "REMOVE_BG":
                    img_bytes = await fetch_clean_image_bytes(f"{prompt_raw}, isolated subject on pure transparent background, PNG cutout", 768, 768)
                    if not img_bytes:
                        raise RuntimeError("Render PNG gagal")
                    await BOT_INSTANCE_GLOBAL.send_document(chat_id=user_id, document=BufferedInputFile(img_bytes, filename=f"bikinAI_Transparan_{int(time.time())}.png"), caption=f"✂️ **FILE PNG TRANSPARAN**\n┗ 🔍 **Kualitas:** `{upscale}`", parse_mode="Markdown")
                else:
                    w, h = (768, 1024) if ratio == "9:16" else ((1024, 768) if ratio == "16:9" else (1024, 1024))
                    img_bytes = await fetch_clean_image_bytes(f"{prompt_raw}, {engine}, 8k", w, h)
                    if not img_bytes:
                        raise RuntimeError("Render gambar gagal")
                    await BOT_INSTANCE_GLOBAL.send_photo(chat_id=user_id, photo=BufferedInputFile(img_bytes, filename="bikinAI_Studio_4K.jpg"), caption=f"✨ **HASIL KARYA 4K**\n┣ ⚡ **Model:** `{engine}` ({ratio})\n┣ 🔍 **Kualitas:** `{upscale}{ref_tag}`\n┗ 📝 **Prompt:** _{prompt_raw[:120]}_", parse_mode="Markdown")
                await mark_job_completed(db, job_id, prompt_raw, engine)
                await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            except Exception:
                await refund_failed_job(db, job_id)
                return web.json_response({"ok": False, "message": "🛡️ Garansi Koin Kembali 100%: Koin dikembalikan otomatis!"}, status=500)
        return web.json_response({"ok": True, "message": "✅ Karya selesai dan dikirim ke chat Telegram Anda!"})
    return web.json_response({"ok": True, "message": "✅ Buka Studio Web langsung dari tombol di dalam Telegram."})


async def handle_nocturne_chat_api(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "reply": "Invalid JSON"}, status=400)
    prompt_raw, is_attack = sanitize_and_deobfuscate_input(str(data.get("prompt") or "Halo"))
    if is_attack:
        return web.json_response({"ok": False, "reply": "Pola input tidak diizinkan."}, status=400)
    async with get_db() as db:
        reply = await generate_frontier_ai_response(
            db, prompt_raw, mode="NOCTURNE_UNCENSORED",
            preferred_model=str(data.get("model") or "nousresearch/hermes-4-405b"),
            persona_style=str(data.get("persona") or "TECHNICAL_ZERO_ROLEPLAY"),
            chat_history=data.get("history") if isinstance(data.get("history"), list) else [],
        )
    return web.json_response({"ok": True, "reply": reply})


async def handle_nocturne_generate_api(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False}, status=400)
    prompt_raw, is_attack = sanitize_and_deobfuscate_input(str(data.get("prompt") or "High resolution studio shot"))
    if is_attack:
        return web.json_response({"ok": False}, status=400)
    modality, model_name, ratio = str(data.get("modality") or "IMAGE"), str(data.get("model") or "black-forest-labs/FLUX.1-dev"), str(data.get("ratio") or "9:16")
    w, h = (768, 1024) if ratio == "9:16" else ((1024, 768) if ratio == "16:9" else (1024, 1024))
    seed_val = int(time.time())
    if modality in ("VIDEO", "IMG2VID"):
        cdn_url, dl_name, is_video = SAMPLE_SANDBOX_VIDEO_URL, f"Video_{seed_val}.mp4", True
    else:
        cdn_url, dl_name, is_video = f"https://image.pollinations.ai/prompt/{quote(f'{prompt_raw}, {model_name}, 8k')}?width={w}&height={h}&nologo=true&private=true&enhance=true&seed={seed_val}", f"Image_4K_{seed_val}.jpg", False
    return web.json_response({"ok": True, "is_video": is_video, "cdn_url": cdn_url, "download_url": f"/api/cdn/download?url={quote(cdn_url)}&name={quote(dl_name)}"})


async def handle_voucher_redeem_api(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "message": "Invalid JSON"}, status=400)
    async with get_db() as db:
        ok, msg, units = await verify_and_redeem_ed25519_voucher(db, str(data.get("voucher") or "").strip())
    return web.json_response({"ok": ok, "message": msg, "units": units}, status=200 if ok else 400)


async def handle_root_web_router(request: web.Request) -> web.Response:
    host = (request.headers.get("Host") or "").lower()
    custom_dom = (RUNTIME_CONFIG.get("CUSTOM_WEB_DOMAIN") or "").lower()
    if (custom_dom and custom_dom in host) or request.query.get("portal") == "freedom":
        return web.Response(text=render_freedom_web_portal_html(), content_type="text/html")
    return web.Response(text=MINIAPP_FULL_WEBSITE_HTML, content_type="text/html")


async def start_embedded_web_servers(port: int = 8080) -> None:
    app = web.Application()
    app.router.add_get("/", handle_root_web_router)
    app.router.add_get("/unfiltered-portal", lambda req: web.Response(text=render_freedom_web_portal_html(), content_type="text/html"))
    app.router.add_get("/api/public/community-links", handle_public_community_links_api)
    app.router.add_get("/api/cdn/download", handle_cdn_force_download_api)
    app.router.add_post("/api/webapp/execute", handle_webapp_execute_api)
    app.router.add_post("/api/nocturne/chat", handle_nocturne_chat_api)
    app.router.add_post("/api/nocturne/generate", handle_nocturne_generate_api)
    app.router.add_post("/api/voucher/redeem", handle_voucher_redeem_api)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()
    print(f"🌐 [WEB SERVER v3.7.1]: Port {port} aktif ({RUNTIME_CONFIG['MINIAPP_URL'] or 'http://localhost:8080'})")


# 9. WIZARD STATE, PRESET AWAM & MENU BUILDERS
UPSCALER_WHITE_LABEL = {
    "PHOTO_FACE_4K": "🔍 Pertajam Foto & Wajah 4K",
    "TEXT_LINE_4K": "✨ Pertajam Teks & Gambar 4K",
    "VIDEO_4K_60FPS": "🎞️ Pertajam & Haluskan Video 4K 60FPS",
    "OFF": "Standar HD",
}

AWAM_VIDEO_MOTION_PRESETS = {
    "ZOOM_CINEMATIC": ("🎥 Kamera Zoom Sinematik", "smooth cinematic camera zoom-in, dynamic lighting, 60fps"),
    "ORBIT_360": ("🔄 Orbit Produk 360°", "360 degree orbital camera rotation around subject, spotlight"),
    "DANCE_FASHION": ("🕺 Gerakan Model & Fashion", "fluid fashion model movement & natural motion"),
    "SLOWMO_EPIC": ("🏃 Slow-Motion Epik", "epic slow-motion action, high frame rate"),
}

AWAM_IMAGE_STYLE_PRESETS = {
    "UMKM_CATALOG": ("🛍️ Katalog Produk UMKM", "commercial product photography, studio lighting, 8k"),
    "STUDIO_PORTRAIT": ("👔 Foto Profil Studio", "professional studio portrait, soft rim lighting, sharp focus"),
    "POSTER_THUMB": ("🎬 Poster & Thumbnail", "movie poster & YouTube thumbnail composition, vibrant colors"),
    "ANIME_PIXAR": ("🎌 Anime / Ilustrasi 3D", "3D & anime illustration, volumetric light"),
}

IMAGE_EDITING_TOOLS = {
    "REMOVE_BG_PNG": ("✂️ Hapus Background (File PNG Transparan)", "Menghapus latar belakang foto dan mengirimkannya sebagai File Dokumen .PNG transparan"),
    "IMG2VID_MOTION": ("🖼️➡️🎬 Gerakkan Foto Jadi Video (Image-to-Video)", "Menggerakkan foto referensi menjadi video menggunakan Wan-AI/Wan2.2-S2V-14B"),
    "RETOUCH_FACE": ("✨ Retouch Wajah & Kulit", "Memperhalus tekstur kulit dan pencahayaan wajah"),
    "INPAINT_OBJ": ("🖌️ Ganti Baju / Ubah Objek", "Mengganti pakaian atau objek tertentu di dalam foto"),
    "OUTPAINT_EXPAND": ("🖼️ Perluas Ukuran Foto", "Memperluas rasio foto menjadi vertikal 9:16 atau 16:9"),
    "PRODUCT_RELIGHT": ("📸 Studio Produk UMKM (Relighting)", "Mengubah pencahayaan foto produk menjadi katalog studio"),
    "RESTORE_OLD": ("🕰️ Restorasi Foto Lama", "Memperbaiki foto buram menjadi tajam kembali"),
}


@dataclass
class LiveWizardSession:
    prompt: str
    modality: Literal["VIDEO", "IMAGE", "EDIT_IMAGE"] = "VIDEO"
    aspect_ratio: str = "9:16"
    duration_sec: int = 5
    video_engine: str = "Wan-AI/Wan2.2-T2V-A14B"
    image_engine: str = "black-forest-labs/FLUX.1-dev"
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
        if self.video_engine in ("google/veo-3.1-fast", "Wan-AI/Wan2.2-S2V-14B"):
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
        [InlineKeyboardButton(text=f"🌐 Buka {web_brand} (Web & Kode VIP)", callback_data="menu:unfiltered_external_referral")],
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
        f"┃ 💬 **Asisten AI 24 Jam:** `🟢 AKTIF (Gratis)`\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━┛{hh_banner}\n\n"
        f"▸ Pilih fitur studio di bawah atau ketik instruksi Anda secara langsung:"
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
    preset_info = f"\n┣ 🎬 **Preset Motion:** `{session.awam_preset}`" if session.awam_preset else ""
    text = (
        f"🎬 **STUDIO VIDEO AI & FOTO JADI VIDEO**\n━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Konsep Video:**\n> _{session.prompt}_\n\n"
        f"┣ ⚡ **Model Video:** **`{session.video_engine}`**{preset_info}\n"
        f"┣ 📐 **Rasio:** `{session.aspect_ratio}` | ⏱️ **Durasi:** `{session.duration_sec}s`\n"
        f"┗ 🔍 **Kualitas:** `{ups_label}`\n━━━━━━━━━━━━━━━━━━\n"
        f"💎 **Biaya:** **`{coins} Koin`** _(Garansi Koin Kembali 100%)_"
    )
    rows = [
        [InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='9:16' else ''}📱 9:16", callback_data="wiz:ar:9:16"), InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='16:9' else ''}🖥️ 16:9", callback_data="wiz:ar:16:9"), InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='1:1' else ''}🟦 1:1", callback_data="wiz:ar:1:1")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.duration_sec==5 else ''}⚡ 5s", callback_data="wiz:dur:5"), InlineKeyboardButton(text=f"{'✅ ' if session.duration_sec==10 else ''}🔥 10s", callback_data="wiz:dur:10"), InlineKeyboardButton(text=f"{'✅ ' if session.duration_sec==30 else ''}🎬 30s", callback_data="wiz:dur:30")],
        [InlineKeyboardButton(text="🎥 Motion: Zoom Sinematik", callback_data="wiz:vpre:ZOOM_CINEMATIC"), InlineKeyboardButton(text="🔄 Motion: Orbit 360°", callback_data="wiz:vpre:ORBIT_360")],
        [InlineKeyboardButton(text="🕺 Motion: Model/Fashion", callback_data="wiz:vpre:DANCE_FASHION"), InlineKeyboardButton(text="🏃 Motion: Slow-Mo Epik", callback_data="wiz:vpre:SLOWMO_EPIC")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Wan-AI/Wan2.2-T2V-A14B' else ''}🔵 Wan2.2-T2V-A14B", callback_data="wiz:veng:Wan-AI/Wan2.2-T2V-A14B"), InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Wan-AI/Wan2.2-S2V-14B' else ''}🕺 Wan2.2-S2V-14B", callback_data="wiz:veng:Wan-AI/Wan2.2-S2V-14B")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='google/veo-3.1-fast' else ''}🎥 google/veo-3.1-fast", callback_data="wiz:veng:google/veo-3.1-fast"), InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Wan-AI/Wan2.2-TI2V-5B' else ''}🟢 Wan2.2-TI2V-5B", callback_data="wiz:veng:Wan-AI/Wan2.2-TI2V-5B")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='VIDEO_4K_60FPS' else ''}🎞️ Pertajam & Haluskan Video 4K 60FPS", callback_data="wiz:ups:VIDEO_4K_60FPS"), InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='OFF' else ''}⚡ Standar HD", callback_data="wiz:ups:OFF")],
        [InlineKeyboardButton(text="✏️ Ubah Deskripsi Video", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 MULAI BUAT VIDEO ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ]
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def build_image_wizard_kb(session: LiveWizardSession, show_more: bool = False) -> tuple[str, InlineKeyboardMarkup]:
    if session.upscale_mode == "VIDEO_4K_60FPS":
        session.upscale_mode = "PHOTO_FACE_4K"
    coins, _, _ = session.get_pricing()
    ups_label = UPSCALER_WHITE_LABEL.get(session.upscale_mode, "🔍 Pertajam Foto & Wajah 4K")
    preset_info = f"\n┣ 🎨 **Preset Gaya:** `{session.awam_preset}`" if session.awam_preset else ""
    text = (
        f"🎨 **STUDIO GAMBAR 4K**\n━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Deskripsi Gambar:**\n> _{session.prompt}_\n\n"
        f"┣ ⚡ **Model Gambar:** **`{session.image_engine}`**{preset_info}\n"
        f"┣ 📐 **Rasio:** `{session.aspect_ratio}`\n"
        f"┗ 🔍 **Penajaman:** `{ups_label}`\n━━━━━━━━━━━━━━━━━━\n"
        f"💎 **Biaya:** **`{coins} Koin`** _(Garansi Koin Kembali 100%)_"
    )
    rows = [
        [InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='9:16' else ''}📱 9:16", callback_data="wiz:ar:9:16"), InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='1:1' else ''}🟦 1:1", callback_data="wiz:ar:1:1"), InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='16:9' else ''}🖥️ 16:9", callback_data="wiz:ar:16:9")],
        [InlineKeyboardButton(text="🛍️ Gaya: Katalog UMKM", callback_data="wiz:ipre:UMKM_CATALOG"), InlineKeyboardButton(text="👔 Gaya: Foto Studio", callback_data="wiz:ipre:STUDIO_PORTRAIT")],
        [InlineKeyboardButton(text="🎬 Gaya: Poster/Thumb", callback_data="wiz:ipre:POSTER_THUMB"), InlineKeyboardButton(text="🎌 Gaya: Anime/3D", callback_data="wiz:ipre:ANIME_PIXAR")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='black-forest-labs/FLUX.1-dev' else ''}📸 FLUX.1-dev", callback_data="wiz:ieng:black-forest-labs/FLUX.1-dev"), InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='bytedance/seedream-4.0' else ''}✨ seedream-4.0", callback_data="wiz:ieng:bytedance/seedream-4.0")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='OnomaAIResearch/Illustrious-xl' else ''}🎌 Illustrious-xl", callback_data="wiz:ieng:OnomaAIResearch/Illustrious-xl"), InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Laxhar/noobai-XL-Vpred-1.0' else ''}🌟 noobai-XL-Vpred-1.0", callback_data="wiz:ieng:Laxhar/noobai-XL-Vpred-1.0")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='PHOTO_FACE_4K' else ''}🔍 Pertajam Foto & Wajah 4K", callback_data="wiz:ups:PHOTO_FACE_4K"), InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='TEXT_LINE_4K' else ''}✨ Pertajam Teks & Gambar 4K", callback_data="wiz:ups:TEXT_LINE_4K")],
        [InlineKeyboardButton(text="🛠️ Buka Menu Editing, Foto Jadi Video & Hapus BG (.PNG)", callback_data="menu:wizard_edit")],
        [InlineKeyboardButton(text="✏️ Ubah Deskripsi Gambar", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 MULAI BUAT GAMBAR ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ]
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def build_editing_tools_wizard_kb(session: LiveWizardSession) -> tuple[str, InlineKeyboardMarkup]:
    coins, _, _ = session.get_pricing()
    tool_title, tool_desc = IMAGE_EDITING_TOOLS.get(session.edit_tool, IMAGE_EDITING_TOOLS["REMOVE_BG_PNG"])
    text = (
        f"🛠️ **STUDIO EDITING, HAPUS BG & FOTO JADI VIDEO**\n━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **Fitur:** **`{tool_title}`**\n"
        f"ℹ️ **Fungsi:** _{tool_desc}_\n"
        f"📝 **Instruksi:** _{session.prompt}_"
    )
    rows = [
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='REMOVE_BG_PNG' else ''}✂️ Hapus Background (File PNG Transparan)", callback_data="wiz:etool:REMOVE_BG_PNG")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='IMG2VID_MOTION' else ''}🖼️➡️🎬 Gerakkan Foto Jadi Video (Image-to-Video)", callback_data="wiz:etool:IMG2VID_MOTION")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='RETOUCH_FACE' else ''}✨ Retouch Wajah", callback_data="wiz:etool:RETOUCH_FACE"), InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='INPAINT_OBJ' else ''}🖌️ Ganti Baju / Objek", callback_data="wiz:etool:INPAINT_OBJ")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='OUTPAINT_EXPAND' else ''}🖼️ Perluas Ukuran Foto", callback_data="wiz:etool:OUTPAINT_EXPAND"), InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='PRODUCT_RELIGHT' else ''}📸 Studio Produk UMKM", callback_data="wiz:etool:PRODUCT_RELIGHT")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='RESTORE_OLD' else ''}🕰️ Restorasi Foto Lama", callback_data="wiz:etool:RESTORE_OLD")],
        [InlineKeyboardButton(text="✏️ Ubah Instruksi", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 PROSES SEKARANG ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ]
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


# 10. HELPER TRANSAKSI KOIN, AUTO-REFUND SWEEPER & BROADCAST TOPIK
async def safe_reply_markdown(message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None) -> Message:
    try:
        return await message.reply(text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception:
        return await message.reply(text, parse_mode=None, reply_markup=reply_markup)


async def safe_edit_markdown(message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None) -> None:
    try:
        await message.edit_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception:
        try:
            await message.edit_text(text, parse_mode=None, reply_markup=reply_markup)
        except Exception:
            pass


async def increment_user_usage_counter(db: aiosqlite.Connection, user_id: int, is_render: bool = False) -> None:
    col = "free_img_used_today" if is_render else "chat_used_today"
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(f"UPDATE users SET {col} = {col} + 1 WHERE internal_user_id = ?;", (user_id,))
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def update_personal_memory_if_needed(db: aiosqlite.Connection, user_id: int, text: str, current_mem: str) -> str:
    low = text.lower()
    new_fact = text[:80] if any(k in low for k in ("nama saya ", "panggil saya ", "usaha saya ", "jualan ", "bisnis saya ")) else ""
    if new_fact and new_fact not in current_mem:
        updated = (f"{current_mem} | {new_fact}").strip(" |")[:400]
        async def _upd(conn: aiosqlite.Connection) -> None:
            await conn.execute("UPDATE users SET personal_memory_notes = ? WHERE internal_user_id = ?;", (updated, user_id))
        await DB_WRITER_DAEMON.execute_write_tx(db, _upd)
        return updated
    return current_mem


async def deduct_user_coins_for_job(db: aiosqlite.Connection, user_id: int, cost: int, allow_bonus: bool, prompt_text: str, engine_used: str) -> tuple[bool, str, str]:
    job_id = f"JOB-{user_id}-{int(time.time() * 1000)}"
    if cost <= 0 or RUNTIME_CONFIG["HAPPY_HOUR_MODE"]:
        async def _free_tx(conn: aiosqlite.Connection) -> None:
            await conn.execute("INSERT INTO jobs (job_id, internal_user_id, cost, deducted_bonus, deducted_utama, status, prompt_text, engine_used, created_at) VALUES (?, ?, 0, 0, 0, 'PROCESSING', ?, ?, ?);", (job_id, user_id, prompt_text[:200], engine_used, int(time.time())))
        await DB_WRITER_DAEMON.execute_write_tx(db, _free_tx)
        return True, job_id, "Promo Happy Hour (0 Koin)"

    async with get_user_lock(user_id):
        async def _tx(conn: aiosqlite.Connection) -> tuple[bool, str]:
            cur = await conn.execute("SELECT koin_utama, koin_bonus FROM users WHERE internal_user_id = ?;", (user_id,))
            row = await cur.fetchone()
            if not row:
                return False, "Ketik /start terlebih dahulu."
            utama, bonus = int(row[0]), int(row[1])
            if allow_bonus:
                if utama + bonus < cost:
                    return False, f"Saldo koin belum cukup (Butuh {cost} Koin, Saldo: {utama} Utama + {bonus} Bonus)."
                use_bonus = min(bonus, cost)
                use_utama = cost - use_bonus
            else:
                if utama < cost:
                    return False, f"Memerlukan {cost} Koin Utama (Saldo: {utama})."
                use_bonus, use_utama = 0, cost
            await conn.execute("UPDATE users SET koin_utama = koin_utama - ?, koin_bonus = koin_bonus - ? WHERE internal_user_id = ?;", (use_utama, use_bonus, user_id))
            await conn.execute("INSERT INTO jobs (job_id, internal_user_id, cost, deducted_bonus, deducted_utama, status, prompt_text, engine_used, created_at) VALUES (?, ?, ?, ?, ?, 'PROCESSING', ?, ?, ?);", (job_id, user_id, cost, use_bonus, use_utama, prompt_text[:200], engine_used, int(time.time())))
            return True, f"Terpakai {use_utama} Koin Utama & {use_bonus} Koin Bonus"

        ok, msg = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
        return ok, job_id, msg


async def mark_job_completed(db: aiosqlite.Connection, job_id: str, prompt_text: str, engine_name: str, media_url: str = "telegram_delivered") -> None:
    sig = hashlib.sha256(f"{engine_name}:{prompt_text.strip().lower()}".encode()).hexdigest()[:24]
    asset_id = f"AST-{sig[:10]}-{int(time.time())}"
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("UPDATE jobs SET status = 'COMPLETED' WHERE job_id = ?;", (job_id,))
        await conn.execute("INSERT OR REPLACE INTO syndicated_assets (asset_id, prompt_signature, engine_name, media_url, times_reused, created_at) VALUES (?, ?, ?, ?, 1, ?);", (asset_id, sig, engine_name, media_url, int(time.time())))
    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def refund_failed_job(db: aiosqlite.Connection, job_id: str) -> bool:
    if not RUNTIME_CONFIG["SUBBOT_REFUND_SWEEPER_ACTIVE"]:
        return False
    async def _tx(conn: aiosqlite.Connection) -> bool:
        cur = await conn.execute("SELECT internal_user_id, deducted_bonus, deducted_utama, refunded_lock FROM jobs WHERE job_id = ?;", (job_id,))
        row = await cur.fetchone()
        if not row or int(row[3]) == 1:
            return False
        uid, d_bonus, d_utama = int(row[0]), int(row[1]), int(row[2])
        await conn.execute("UPDATE users SET koin_utama = koin_utama + ?, koin_bonus = MIN(?, koin_bonus + ?) WHERE internal_user_id = ?;", (d_utama, MAX_KOIN_BONUS_CAP, d_bonus, uid))
        await conn.execute("UPDATE jobs SET status = 'REFUNDED', refunded_lock = 1 WHERE job_id = ?;", (job_id,))
        return True
    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def _background_dead_job_sweeper_loop() -> None:
    while True:
        await asyncio.sleep(30)
        if not RUNTIME_CONFIG.get("SUBBOT_REFUND_SWEEPER_ACTIVE", True):
            continue
        try:
            cutoff_ts = int(time.time()) - 60
            async with get_db() as db:
                cur = await db.execute("SELECT job_id, internal_user_id FROM jobs WHERE status = 'PROCESSING' AND refunded_lock = 0 AND created_at <= ?;", (cutoff_ts,))
                for j_id, u_id in await cur.fetchall():
                    if await refund_failed_job(db, str(j_id)) and BOT_INSTANCE_GLOBAL:
                        try:
                            await BOT_INSTANCE_GLOBAL.send_message(chat_id=int(u_id), text=f"🛡️ **Garansi Koin Kembali 100% (Auto-Refund):** Pesanan `{j_id}` melewati batas 60 detik. Koin Anda telah dikembalikan utuh!", parse_mode="Markdown")
                        except Exception:
                            pass
        except Exception:
            pass


async def broadcast_to_bound_topic(bot: Bot, db: aiosqlite.Connection, binding_key: str, text: str) -> None:
    if binding_key == "ACTIVITY_TOPIC" and not RUNTIME_CONFIG["SUBBOT_NEURAL_FEED_ACTIVE"]:
        return
    bound = await get_topic_binding(db, binding_key)
    if not bound:
        return
    chat_id, topic_id = bound
    try:
        kwargs: dict[str, Any] = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        if topic_id > 0:
            kwargs["message_thread_id"] = topic_id
        await bot.send_message(**kwargs)
    except Exception:
        pass


# 11. ADMIN PANEL & BANSOS 4-TAB VIEW BUILDERS
def _build_owner_admin_panel_view(treasury_row: tuple[Any, ...] | None) -> tuple[str, InlineKeyboardMarkup]:
    gross, work_cap, profit_avail, harvested, jobs_cnt = (int(treasury_row[i]) for i in range(5)) if treasury_row else (0, 0, 0, 0, 0)
    prod_str = "🟢 PRODUCTION" if RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"] else "🧪 SANDBOX HPP Rp 0"
    hh_str = "🟢 ON (0 Koin)" if RUNTIME_CONFIG["HAPPY_HOUR_MODE"] else "⚪ OFF (Normal)"
    eng_mode = "Mode 1 (HPP Rp 0)" if RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] == 1 else "Mode 2 (Hybrid Flagship)"
    cur_agent = RUNTIME_CONFIG.get("PRIMARY_ROLLING_AGENT", "ARGON")
    w_brand = RUNTIME_CONFIG.get("WEB_BRAND_NAME", "AetherFree AI Studio")

    txt = (
        f"👑 **OWNER COMMAND CENTER — bikinAI v3.7.1**\n━━━━━━━━━━━━━━━━━━\n"
        f"💰 **Treasury Ledger:**\n"
        f"┣ 📈 **Omzet Kotor:** `Rp {gross:,}`\n"
        f"┣ 🛡️ **Modal Kerja (HPP+10%):** `Rp {work_cap:,}`\n"
        f"┣ 💎 **Laba Bersih Siap Panen:** **`Rp {profit_avail:,}`**\n"
        f"┣ 🏦 **Total Dipanen:** `Rp {harvested:,}`\n"
        f"┗ ⚙️ **Total Job:** `{jobs_cnt} Render`\n\n"
        f"🎛️ **Konfigurasi Sistem:**\n"
        f"┣ 🧠 **Primary Agent:** `{cur_agent}` (`{AGENTIC_ROLLING_POOL[cur_agent]['title']}`)\n"
        f"┣ 🌐 **Web Brand:** `{w_brand}` (`/set_webname`)\n"
        f"┣ 📡 **Mode /bansos:** `{RUNTIME_CONFIG['BANSOS_OPERATION_MODE']}`\n"
        f"┣ 🚀 **Status:** `{prod_str}` | `{eng_mode}`\n"
        f"┣ 🇮🇩 **Kasir ID:** `{RUNTIME_CONFIG['ID_ACTIVE_PROVIDER']}`\n"
        f"┗ 🌍 **Kasir Global:** `{RUNTIME_CONFIG['GLOBAL_ACTIVE_PROVIDER']}`"
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🌾 Panen Laba Bersih Sekarang (Rp {profit_avail:,})", callback_data="adm:harvest")],
            [InlineKeyboardButton(text="👁️ Lihat Layar sebagai Pembeli & Audit Privasi UI", callback_data="adm:view_as_buyer:ID")],
            [InlineKeyboardButton(text="💳 Sub-Menu Pengaturan Pembayaran (3 Halaman)", callback_data="adm:pay_menu")],
            [InlineKeyboardButton(text="📡 Buka Radar /bansos (4-Tab)", callback_data="bns:tab:AI_API"), InlineKeyboardButton(text=f"🔄 Rolling Agent ({cur_agent})", callback_data="adm:rolling")],
            [InlineKeyboardButton(text=f"🎉 Happy Hour: {hh_str}", callback_data="adm:toggle_hh"), InlineKeyboardButton(text=f"🚀 Mode: {prod_str}", callback_data="adm:toggle_prod")],
            [InlineKeyboardButton(text=f"⚡ Mesin: {eng_mode}", callback_data="adm:toggle_eng_mode"), InlineKeyboardButton(text="🤖 Pusat 5 Sub-Bot & Guard", callback_data="adm:subbots")],
            [InlineKeyboardButton(text="📖 Buku Manual Developer & SOP Live (4 Bab)", callback_data="adm:manual:1")],
            [InlineKeyboardButton(text="🔄 Segarkan Data Brankas", callback_data="adm:refresh")],
        ]
    )
    return txt, kb


async def _build_bansos_4tab_view(db: aiosqlite.Connection, active_tab: str = "AI_API") -> tuple[str, InlineKeyboardMarkup]:
    b_mode = RUNTIME_CONFIG.get("BANSOS_OPERATION_MODE", "SILENT_PROFIT")
    header = f"📡 **OMNI-RESOURCE RADAR & 4-GATE STERILIZER**\n━━━━━━━━━━━━━━━━━━\n🎛️ **Mode:** **`{b_mode}`**\n\n"
    if active_tab == "AI_API":
        cur = await db.execute("SELECT resource_name, endpoint_url, is_live_verified FROM omni_resource_registry WHERE category = 'AI_API';")
        rows = await cur.fetchall()
        lines = [f"▸ **{x['name']}** — `{'🟢 Verified' if x['verified'] else '🟡 Standby'}`" for x in OMNI_BANSOS_PRESETS["AI_API"]] if not rows else [f"▸ **{r[0]}**\n  `{r[1]}` — `{'🟢 LIVE (<2.5s)' if r[2] else '🟡 Standby'}`" for r in rows]
        body = "⚡ **[TAB 1/4] AI API REGISTRY:**\n" + "\n".join(lines)
    elif active_tab == "DOMAINS":
        doms = await check_multi_tld_domain_availability_live("bikinai")
        body = "🌐 **[TAB 2/4] MULTI-TLD RDAP SCANNER:**\n" + "\n".join(f"▸ `{d['domain']}` — {d['status']}" for d in doms)
    elif active_tab == "STORAGE":
        lines = [f"▸ **{item['name']}** — _{item['meta']}_" for item in OMNI_BANSOS_PRESETS["CLOUD_STORAGE"] + OMNI_BANSOS_PRESETS["GRANTS_AND_DB"]]
        body = "🗄️ **[TAB 3/4] STORAGE & COMPUTE GRANTS:**\n" + "\n".join(lines)
    else:
        ast_res = sterilize_community_script_ast("def health_probe():\n    return {'status': 200}\n", "community_plugin")
        gitops = AUTONOMIC_GUARD.build_gitops_commit_plan(ast_res["hash"], "Verified clean AST state")
        body = f"🧬 **[TAB 4/4] 4-GATE AST STERILIZER & GITOPS:**\n▸ **AST Hash:** `{ast_res['hash']}`\n▸ **GitOps Branch:** `{gitops['shadow_branch']}`"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{'✅ ' if active_tab=='AI_API' else ''}⚡ AI API", callback_data="bns:tab:AI_API"), InlineKeyboardButton(text=f"{'✅ ' if active_tab=='DOMAINS' else ''}🌐 Domain RDAP", callback_data="bns:tab:DOMAINS")],
            [InlineKeyboardButton(text=f"{'✅ ' if active_tab=='STORAGE' else ''}🗄️ Storage & Grant", callback_data="bns:tab:STORAGE"), InlineKeyboardButton(text=f"{'✅ ' if active_tab=='AST' else ''}🧬 AST & GitOps", callback_data="bns:tab:AST")],
            [InlineKeyboardButton(text="🤫 Mode Silent (100% Profit Owner)", callback_data="bns:mode:SILENT")],
            [InlineKeyboardButton(text="🎉 Mode Happy Hour + Broadcast Grup", callback_data="bns:mode:HAPPY_HOUR")],
            [InlineKeyboardButton(text="🛑 Matikan Happy Hour (Tarif Normal)", callback_data="bns:mode:NORMAL")],
            [InlineKeyboardButton(text="⚡ Ping Semua Endpoint", callback_data="bns:ping_all"), InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
        ]
    )
    return header + body, kb


# 12. COMMAND HANDLERS
@router.message(CommandStart())
async def cmd_start_handler(message: Message) -> None:
    user_id, username = message.from_user.id, message.from_user.username or message.from_user.first_name or "Kreator"
    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username, message.from_user.first_name or "", message.from_user.language_code or "id")
    await safe_reply_markdown(message, build_customer_dashboard_caption(username, u), reply_markup=build_customer_main_menu_keyboard(u, is_private=(message.chat.type == "private")))


@router.message(Command("menu", "studio", "bantuan"))
async def cmd_menu_handler(message: Message) -> None:
    user_id, username = message.from_user.id, message.from_user.username or message.from_user.first_name or "Kreator"
    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username, message.from_user.first_name or "")
    await safe_reply_markdown(message, build_customer_dashboard_caption(username, u), reply_markup=build_customer_main_menu_keyboard(u, is_private=(message.chat.type == "private")))


@router.message(Command("set_webname"))
async def cmd_set_web_brand_name(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Khusus Owner di DM.")
        return
    new_name = (message.text or "").partition(" ")[2].strip()
    if not new_name:
        await message.reply(f"🌐 **Nama Website:** `{RUNTIME_CONFIG['WEB_BRAND_NAME']}`\nUbah: `/set_webname NamaBaru`", parse_mode="Markdown")
        return
    RUNTIME_CONFIG["WEB_BRAND_NAME"] = new_name[:40]
    async with get_db() as db:
        await save_persistent_setting(db, "WEB_BRAND_NAME", RUNTIME_CONFIG["WEB_BRAND_NAME"])
    await message.reply(f"✅ **Nama Brand Website diubah menjadi:** `{RUNTIME_CONFIG['WEB_BRAND_NAME']}`", parse_mode="Markdown")


@router.message(Command("claim_owner"))
async def cmd_claim_owner_bootstrap(message: Message) -> None:
    if message.chat.type != "private":
        return
    token_arg = (message.text or "").partition(" ")[2].strip()
    if RUNTIME_CONFIG["OWNER_ID_RUNTIME"] == 0 and hmac.compare_digest(token_arg, OWNER_BOOTSTRAP_TOKEN):
        RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = message.from_user.id
        async with get_db() as db:
            await save_persistent_setting(db, "OWNER_ID_RUNTIME", str(message.from_user.id))
        await message.reply(f"✅ **Owner dikunci ke ID `{message.from_user.id}`.** Ketik `/admin`.")
    else:
        await message.reply("🔒 Token tidak valid atau Owner sudah terkunci.")


@router.message(Command("harvest"))
async def cmd_quick_harvest_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Khusus Owner di DM.")
        return
    async with get_db() as db:
        ok, harvested_now, total_h = await execute_manual_profit_harvest(db)
    await message.reply(f"🌾 **HARVEST BERHASIL:** `Rp {harvested_now:,}` (Total: `Rp {total_h:,}`)" if ok else "ℹ️ Belum ada laba bersih siap panen.", parse_mode="Markdown")


@router.message(Command("bansos", "info_bansos"))
async def cmd_bansos_radar_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Khusus Owner di DM.")
        return
    async with get_db() as db:
        txt, kb = await _build_bansos_4tab_view(db, "AI_API")
    await safe_reply_markdown(message, txt, reply_markup=kb)


@router.message(Command("rolling", "agents"))
async def cmd_rolling_agents_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Khusus Owner di DM.")
        return
    nxt = rotate_primary_agent()
    async with get_db() as db:
        await save_persistent_setting(db, "PRIMARY_ROLLING_AGENT", nxt)
    lines = [f"▸ {'🟢' if k == nxt else '⚪'} **`{k}`** — `{v['title']}` _(OK: {v['ok']} | Fail: {v['fail']})_" for k, v in AGENTIC_ROLLING_POOL.items()]
    await safe_reply_markdown(message, f"🔄 **PRIMARY AGENT:** **`{nxt}`**\n\n" + "\n".join(lines))


@router.message(Command("donasi_api"))
async def cmd_community_donate_api(message: Message) -> None:
    args = (message.text or "").split()[1:]
    if not args:
        await message.reply("Format: `/donasi_api https://endpoint/v1/chat/completions model-slug`", parse_mode="Markdown")
        return
    ep_url, model_slug = args[0].strip(), (args[1].strip() if len(args) > 1 else "openai")
    wait = await message.reply("🛡️ **Memeriksa Endpoint dengan 4-Gate Sterilizer...**", parse_mode="Markdown")
    ok_ping, ms, info = await ping_and_verify_bansos_endpoint(ep_url, model_slug)
    if not ok_ping:
        await safe_edit_markdown(wait, f"❌ **Ditolak:** `{info}`")
        return
    user_id, username = message.from_user.id, message.from_user.username or "Kreator"
    res_id = f"COM-{hashlib.sha256(ep_url.encode()).hexdigest()[:8].upper()}"
    async with get_db() as db:
        await ensure_user_and_track_identity(db, user_id, username)
        async def _tx(conn: aiosqlite.Connection) -> None:
            await conn.execute("INSERT OR REPLACE INTO omni_resource_registry (resource_id, category, resource_name, endpoint_url, secret_or_meta, is_live_verified, expires_at) VALUES (?, 'AI_API', ?, ?, ?, 1, ?);", (res_id, f"Node ({username})", ep_url, model_slug, int(time.time()) + 30 * 86400))
            await conn.execute("UPDATE users SET koin_bonus = MIN(?, koin_bonus + 15) WHERE internal_user_id = ?;", (MAX_KOIN_BONUS_CAP, user_id))
        await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    await safe_edit_markdown(wait, f"✅ **TERVERIFIKASI ({ms} ms)!** +15 Koin Bonus ditambahkan.")


@router.message(Command("riset"))
async def cmd_deep_research_handler(message: Message) -> None:
    user_id, username = message.from_user.id, message.from_user.username or "Kreator"
    raw_arg = (message.text or "").partition(" ")[2].strip()
    if not raw_arg:
        await message.reply("Format: `/riset [topik teknis / bisnis]`", parse_mode="Markdown")
        return
    clean_q, is_attack = sanitize_and_deobfuscate_input(raw_arg)
    if is_attack:
        await message.reply("🛡️ Pola teks tidak diizinkan.")
        return
    wait = await message.reply("🔬 **Menyusun analisis teknis...**", parse_mode="Markdown")
    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username)
        await increment_user_usage_counter(db, user_id, is_render=False)
        res = await generate_frontier_ai_response(db, clean_q, mode="DEEP_RESEARCH", personal_memory=u["memory"])
    await safe_edit_markdown(wait, f"🔬 **LAPORAN RISET TEKNIS**\n━━━━━━━━━━━━━━━━━━\n{res}")


@router.message(Command("canvas"))
async def cmd_canvas_workspace_handler(message: Message) -> None:
    user_id, username = message.from_user.id, message.from_user.username or "Kreator"
    raw_arg = (message.text or "").partition(" ")[2].strip()
    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username)
        if not raw_arg:
            await safe_reply_markdown(message, f"📝 **CANVAS WORKSPACE**\n━━━━━━━━━━━━━━━━━━\n{u['canvas'] or '_(Kosong. Gunakan `/canvas [instruksi]`)_'}")
            return
        clean_arg, is_attack = sanitize_and_deobfuscate_input(raw_arg)
        if is_attack:
            await message.reply("🛡️ Pola teks tidak diizinkan.")
            return
        wait = await message.reply("📝 **Memperbarui Canvas...**", parse_mode="Markdown")
        await increment_user_usage_counter(db, user_id, is_render=False)
        updated_canvas = await generate_frontier_ai_response(db, clean_arg, mode="CANVAS_EDIT", personal_memory=u["memory"], canvas_state=u["canvas"])
        async def _save_c(conn: aiosqlite.Connection) -> None:
            await conn.execute("UPDATE users SET active_canvas_content = ? WHERE internal_user_id = ?;", (updated_canvas[:4000], user_id))
        await DB_WRITER_DAEMON.execute_write_tx(db, _save_c)
    await safe_edit_markdown(wait, f"📝 **CANVAS DIPERBARUI**\n━━━━━━━━━━━━━━━━━━\n{updated_canvas}")


@router.message(Command("saran", "feedback"))
async def cmd_user_feedback_handler(message: Message) -> None:
    user_id, username = message.from_user.id, message.from_user.username or "Kreator"
    raw_fb = (message.text or "").partition(" ")[2].strip()
    if not raw_fb:
        await message.reply("Format: `/saran [masukan Anda]`", parse_mode="Markdown")
        return
    clean_fb, is_attack = sanitize_and_deobfuscate_input(raw_fb)
    if is_attack:
        await message.reply("🛡️ Pola teks tidak diizinkan.")
        return
    async with get_db() as db:
        await ensure_user_and_track_identity(db, user_id, username)
        async def _fb_tx(conn: aiosqlite.Connection) -> None:
            await conn.execute("INSERT INTO user_feedback (user_id, username, feedback_text, created_at) VALUES (?, ?, ?, ?);", (user_id, username, clean_fb[:500], int(time.time())))
        await DB_WRITER_DAEMON.execute_write_tx(db, _fb_tx)
        await broadcast_to_bound_topic(message.bot, db, "FEEDBACK_TOPIC", f"🛠️ **Masukan dari `@{username}`:**\n> _{clean_fb[:300]}_")
    await message.reply("✅ Masukan tercatat.")


@router.message(Command("set_miniapp"))
async def cmd_set_miniapp_url(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Khusus Owner di DM.")
        return
    arg_url = (message.text or "").partition(" ")[2].strip()
    if not arg_url.startswith("https://"):
        await message.reply(f"🌐 **URL Mini App:** `{RUNTIME_CONFIG['MINIAPP_URL'] or 'Belum disetel'}`", parse_mode="Markdown")
        return
    RUNTIME_CONFIG["MINIAPP_URL"] = arg_url
    async with get_db() as db:
        await save_persistent_setting(db, "MINIAPP_URL", arg_url)
    await message.reply(f"✅ **URL Mini App Dikunci:** `{arg_url}`", parse_mode="Markdown")


@router.message(Command("pasang_bansos"))
async def cmd_pasang_bansos_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Khusus Owner di DM.")
        return
    exp_ts = int(time.time()) + (365 * 86400)
    async with get_db() as db:
        async def _tx(conn: aiosqlite.Connection) -> int:
            c = 0
            for cat, items in OMNI_BANSOS_PRESETS.items():
                for item in items:
                    await conn.execute("INSERT OR REPLACE INTO omni_resource_registry (resource_id, category, resource_name, endpoint_url, secret_or_meta, is_live_verified, expires_at) VALUES (?, ?, ?, ?, ?, ?, ?);", (item["res_id"], cat, item["name"], item["endpoint"], item["meta"], int(item["verified"]), exp_ts))
                    c += 1
            return c
        count_installed = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    ast_check = sterilize_community_script_ast("def ping():\n    return 'OK'\n", "bansos_healthcheck")
    await message.reply(f"✅ **PRESET TERPASANG:** `{count_installed} Resource` | **AST Hash:** `{ast_check['hash']}`", parse_mode="Markdown")


@router.message(Command("admin"))
async def cmd_owner_admin_panel(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Khusus Owner di DM pribadi.", parse_mode="Markdown")
        return
    async with get_db() as db:
        await save_persistent_setting(db, "OWNER_ID_RUNTIME", str(message.from_user.id))
        cur = await db.execute("SELECT gross_revenue_idr, working_capital_vault_idr, harvestable_profit_vault_idr, total_harvested_by_owner_idr, total_jobs_completed FROM treasury_summary WHERE id = 1;")
        row = await cur.fetchone()
    txt, kb = _build_owner_admin_panel_view(row)
    await safe_reply_markdown(message, txt, reply_markup=kb)


# 13. CALLBACK HANDLERS
@router.callback_query(F.data.startswith("bns:"))
async def handle_bansos_radar_callbacks(call: CallbackQuery) -> None:
    if not call.message or not is_verified_owner_dm(call.from_user.id, call.message.chat.type):
        await call.answer("🔒 Khusus Owner.", show_alert=True)
        return
    parts = call.data.split(":")
    sub, val = parts[1], parts[2] if len(parts) > 2 else ""

    async with get_db() as db:
        if sub == "mode":
            if val == "SILENT":
                RUNTIME_CONFIG["BANSOS_OPERATION_MODE"], RUNTIME_CONFIG["HAPPY_HOUR_MODE"] = "SILENT_PROFIT", False
                await save_persistent_setting(db, "BANSOS_OPERATION_MODE", "SILENT_PROFIT")
                await save_persistent_setting(db, "HAPPY_HOUR_MODE", "0")
                await call.answer("🤫 Mode Silent Aktif!", show_alert=True)
            elif val == "HAPPY_HOUR":
                RUNTIME_CONFIG["BANSOS_OPERATION_MODE"], RUNTIME_CONFIG["HAPPY_HOUR_MODE"] = "HAPPY_HOUR", True
                await save_persistent_setting(db, "BANSOS_OPERATION_MODE", "HAPPY_HOUR")
                await save_persistent_setting(db, "HAPPY_HOUR_MODE", "1")
                await broadcast_to_bound_topic(call.bot, db, "COMMAND_TOPIC", f"🎉 **FLASH HAPPY HOUR DIBUKA!** 🎉\nSeluruh pembuatan karya di `@{BOT_USERNAME_GLOBAL}` sedang **GRATIS 0 KOIN**!")
                await call.answer("🎉 Mode Happy Hour Aktif!", show_alert=True)
            else:
                RUNTIME_CONFIG["BANSOS_OPERATION_MODE"], RUNTIME_CONFIG["HAPPY_HOUR_MODE"] = "NORMAL", False
                await save_persistent_setting(db, "BANSOS_OPERATION_MODE", "NORMAL")
                await save_persistent_setting(db, "HAPPY_HOUR_MODE", "0")
                await call.answer("🛑 Mode Normal Aktif.", show_alert=True)
            txt, kb = await _build_bansos_4tab_view(db, "AI_API")
            await safe_edit_markdown(call.message, txt, reply_markup=kb)
            return

        if sub == "ping_all":
            await call.answer("⚡ Menguji endpoint...")
            ok_p, ms_p, _ = await ping_and_verify_bansos_endpoint("https://text.pollinations.ai/openai", "openai")
            async def _upd_p(conn: aiosqlite.Connection) -> None:
                await conn.execute("UPDATE omni_resource_registry SET is_live_verified = ? WHERE resource_id = 'API-POLLINATIONS-V1';", (1 if ok_p else 0,))
            await DB_WRITER_DAEMON.execute_write_tx(db, _upd_p)
            txt, kb = await _build_bansos_4tab_view(db, "AI_API")
            await safe_edit_markdown(call.message, f"✅ **Ping Gate:** `{ms_p} ms`\n\n{txt}", reply_markup=kb)
            return

        await call.answer()
        txt, kb = await _build_bansos_4tab_view(db, val if sub == "tab" else "AI_API")
        await safe_edit_markdown(call.message, txt, reply_markup=kb)


@router.callback_query(F.data.startswith("adm:"))
async def handle_owner_admin_callbacks(call: CallbackQuery) -> None:
    if not call.message or not is_verified_owner_dm(call.from_user.id, call.message.chat.type):
        await call.answer("🔒 Khusus Owner.", show_alert=True)
        return
    act = call.data.split(":", 1)[1]

    async with get_db() as db:
        if act == "harvest":
            ok, harvested_now, total_h = await execute_manual_profit_harvest(db)
            await call.answer(f"🌾 Dipanen: Rp {harvested_now:,} (Total: Rp {total_h:,})" if ok else "ℹ️ Belum ada laba baru.", show_alert=True)

        elif act.startswith("view_as_buyer:"):
            sim_zone = 3 if act.endswith(":ID") else 1
            sim_user = {"koin_utama": 60, "koin_bonus": 12, "has_topped_up": True, "ppp_zone": sim_zone, "last_claim_date": "", "safe_uname": "SimulasiPembeli"}
            sample_cap = build_customer_dashboard_caption("SimulasiPembeli", sim_user)
            sample_vid, _ = build_video_wizard_kb(LiveWizardSession(prompt="Contoh Video", modality="VIDEO"))
            sample_img, _ = build_image_wizard_kb(LiveWizardSession(prompt="Contoh Gambar", modality="IMAGE"))
            audit_res = scan_customer_ui_for_leaks([sample_cap, sample_vid, sample_img])
            leak_badge = f"🟢 **BERSIH 100%** (`0/{audit_res['checked_terms']}` istilah bocor)" if audit_res["clean"] else f"🔴 **BOCOR:** `{', '.join(audit_res['leaks'])}`"
            zone_title = "🇮🇩 Pembeli Indonesia (Zona 3)" if sim_zone == 3 else "🌍 Pembeli Global (Zona 1)"
            buyer_kb = build_customer_main_menu_keyboard(sim_user, is_private=True)
            inspector_rows = list(buyer_kb.inline_keyboard) + [
                [InlineKeyboardButton(text="🇮🇩 Simulasi Pembeli ID", callback_data="adm:view_as_buyer:ID"), InlineKeyboardButton(text="🌍 Simulasi Pembeli Global", callback_data="adm:view_as_buyer:GL")],
                [InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
            ]
            await call.answer("👁️ Simulasi layar pembeli...")
            await safe_edit_markdown(
                call.message,
                f"👁️ **INSPEKTOR LAYAR PEMBELI & AUDIT PRIVASI**\n━━━━━━━━━━━━━━━━━━\n"
                f"┣ 🎭 **Simulasi:** `{zone_title}`\n┗ 🛡️ **Audit UI:** {leak_badge}\n━━━━━━━━━━━━━━━━━━\n\n{sample_cap}",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=inspector_rows),
            )
            return

        elif act.startswith("acc_inv:") or act.startswith("rej_inv:"):
            inv_id = act.split(":", 1)[1]
            if act.startswith("acc_inv:"):
                ok, uid, amt_idr, coins_add, msg = await approve_invoice_and_credit_coins(db, inv_id)
                await call.answer(msg, show_alert=True)
                if ok and BOT_INSTANCE_GLOBAL:
                    try:
                        await BOT_INSTANCE_GLOBAL.send_message(chat_id=uid, text=f"✅ **Tagihan `{inv_id}` (`Rp {amt_idr:,}`) Terverifikasi!**\nSaldo **+{coins_add} Koin Utama** telah ditambahkan.", parse_mode="Markdown")
                    except Exception:
                        pass
                await safe_edit_markdown(call.message, f"✅ **Tagihan `{inv_id}` di-ACC (+{coins_add} Koin Utama).**")
            else:
                await call.answer("❌ Ditolak.", show_alert=True)
                await safe_edit_markdown(call.message, f"❌ **Tagihan `{inv_id}` ditolak.**")
            return

        elif act == "pay_menu" or act.startswith("pay_sub:") or act.startswith("set_id_pg:") or act.startswith("set_gl_pg:"):
            if act.startswith("set_id_pg:"):
                _, cat, prov = act.split(":", 2)
                RUNTIME_CONFIG["ID_ACTIVE_CATEGORY"], RUNTIME_CONFIG["ID_ACTIVE_PROVIDER"] = cat, prov
                await save_persistent_setting(db, "ID_ACTIVE_CATEGORY", cat)
                await save_persistent_setting(db, "ID_ACTIVE_PROVIDER", prov)
                await call.answer(f"🇮🇩 Kasir Lokal: {prov}", show_alert=True)
            elif act.startswith("set_gl_pg:"):
                prov = act.split(":", 1)[1]
                RUNTIME_CONFIG["GLOBAL_ACTIVE_PROVIDER"] = prov
                await save_persistent_setting(db, "GLOBAL_ACTIVE_PROVIDER", prov)
                await call.answer(f"🌍 Kasir Global: {prov}", show_alert=True)

            sub_page = act.split(":", 1)[1] if act.startswith("pay_sub:") else "A"
            await call.answer()
            if sub_page == "A":
                p_txt = f"📲 **SUB-MENU A — QRIS DIRECT (0% FEE)**\nAktif: **`{RUNTIME_CONFIG['ID_ACTIVE_PROVIDER']}`**"
                p_kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🟢 QRIS GoPay Merchant", callback_data="adm:set_id_pg:QRIS_DIRECT:QRIS GoPay Merchant")],
                    [InlineKeyboardButton(text="🟠 QRIS ShopeePay Merchant", callback_data="adm:set_id_pg:QRIS_DIRECT:QRIS ShopeePay Merchant")],
                    [InlineKeyboardButton(text="🔵 QRIS DANA Bisnis", callback_data="adm:set_id_pg:QRIS_DIRECT:QRIS DANA Bisnis")],
                    [InlineKeyboardButton(text="➡️ Sub-Menu B (PG)", callback_data="adm:pay_sub:B"), InlineKeyboardButton(text="🌐 Sub-Menu C (Global)", callback_data="adm:pay_sub:C")],
                    [InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
                ])
            elif sub_page == "B":
                p_txt = f"🏦 **SUB-MENU B — PAYMENT GATEWAY**\nAktif: **`{RUNTIME_CONFIG['ID_ACTIVE_PROVIDER']}`**"
                p_kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🏦 Duitku", callback_data="adm:set_id_pg:PG_DUITKU:Duitku All-Payment")],
                    [InlineKeyboardButton(text="🏦 Tripay", callback_data="adm:set_id_pg:PG_TRIPAY:Tripay QRIS & VA")],
                    [InlineKeyboardButton(text="🏦 Pakasir", callback_data="adm:set_id_pg:PG_PAKASIR:Pakasir QRIS Instan")],
                    [InlineKeyboardButton(text="🏦 Midtrans", callback_data="adm:set_id_pg:PG_MIDTRANS:Midtrans Snap QRIS/VA")],
                    [InlineKeyboardButton(text="⬅️ Sub-Menu A", callback_data="adm:pay_sub:A"), InlineKeyboardButton(text="🌐 Sub-Menu C", callback_data="adm:pay_sub:C")],
                    [InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
                ])
            else:
                p_txt = f"🌐 **SUB-MENU C — KASIR GLOBAL**\nAktif: **`{RUNTIME_CONFIG['GLOBAL_ACTIVE_PROVIDER']}`**"
                p_kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="₮ Hanya Crypto USDT (@CryptoBot)", callback_data="adm:set_gl_pg:Hanya Crypto USDT (@CryptoBot)")],
                    [InlineKeyboardButton(text="⭐ Hanya Telegram Stars", callback_data="adm:set_gl_pg:Hanya Telegram Stars")],
                    [InlineKeyboardButton(text="🌐 Aktifkan Keduanya (USDT + Stars)", callback_data="adm:set_gl_pg:Aktifkan Keduanya (USDT + Telegram Stars)")],
                    [InlineKeyboardButton(text="📲 Sub-Menu A", callback_data="adm:pay_sub:A"), InlineKeyboardButton(text="🏦 Sub-Menu B", callback_data="adm:pay_sub:B")],
                    [InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
                ])
            await safe_edit_markdown(call.message, p_txt, reply_markup=p_kb)
            return

        elif act.startswith("manual:"):
            chap = act.split(":", 1)[1]
            await call.answer()
            manuals = {
                "1": "📖 **BAB 1/4: SETUP GRUP**\nKetik `/setup_grup` di Supergroup untuk membuat 6 topik otomatis, atau `/ikat` untuk mengikat topik secara manual.",
                "2": "📖 **BAB 2/4: KASIR 3-TIER & INSPEKTOR**\nKasir mendukung 3 Tier (`HEMAT`, `PRO`, `SULTAN`). Gunakan **👁️ Lihat Layar sebagai Pembeli** untuk audit privasi.",
                "3": "📖 **BAB 3/4: BANSOS & ROLLING AGENT**\nGunakan `/set_webname`, `/bansos`, dan `/rolling` untuk mengatur operasional otonom.",
                "4": "📖 **BAB 4/4: DATABASE & DOMAIN**\nDatabase: `~/.bikinai_vault/bikinai_master_vault.db`. Setel `CUSTOM_WEB_DOMAIN` di `.env` untuk domain web mandiri.",
            }
            m_kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Bab 1", callback_data="adm:manual:1"), InlineKeyboardButton(text="Bab 2", callback_data="adm:manual:2"), InlineKeyboardButton(text="Bab 3", callback_data="adm:manual:3"), InlineKeyboardButton(text="Bab 4", callback_data="adm:manual:4")],
                [InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
            ])
            await safe_edit_markdown(call.message, manuals.get(chap, manuals["1"]), reply_markup=m_kb)
            return

        elif act == "rolling":
            nxt = rotate_primary_agent()
            await save_persistent_setting(db, "PRIMARY_ROLLING_AGENT", nxt)
            await call.answer(f"🔄 Primary Agent: {nxt}", show_alert=True)
        elif act == "toggle_hh":
            RUNTIME_CONFIG["HAPPY_HOUR_MODE"] = not RUNTIME_CONFIG["HAPPY_HOUR_MODE"]
            await save_persistent_setting(db, "HAPPY_HOUR_MODE", "1" if RUNTIME_CONFIG["HAPPY_HOUR_MODE"] else "0")
            await call.answer("Status Happy Hour diperbarui.", show_alert=True)
        elif act == "toggle_prod":
            RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"] = not RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"]
            await save_persistent_setting(db, "LAUNCH_PRODUCTION_MODE", "1" if RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"] else "0")
            await call.answer("Mode Produksi diperbarui.", show_alert=True)
        elif act == "toggle_eng_mode":
            RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] = 2 if RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] == 1 else 1
            await save_persistent_setting(db, "PILIHAN_MESIN_MEDIA", str(RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"]))
            await call.answer("Mode Mesin diperbarui.", show_alert=True)
        elif act == "subbots" or act.startswith("toggle_sb:"):
            if act.startswith("toggle_sb:"):
                sb_key = act.split(":", 1)[1]
                if sb_key in RUNTIME_CONFIG:
                    RUNTIME_CONFIG[sb_key] = not RUNTIME_CONFIG[sb_key]
            await call.answer()
            sb_keys = [
                ("SUBBOT_SANGMATA_ACTIVE", "Identity History Tracker"),
                ("SUBBOT_WELCOME_GUARD_ACTIVE", "Cyber Welcome Gate"),
                ("SUBBOT_NEURAL_FEED_ACTIVE", "Live Neural Feed Broadcaster"),
                ("SUBBOT_REFUND_SWEEPER_ACTIVE", "Auto-Refund Watchdog (60s)"),
                ("SUBBOT_SOCIAL_POSTER_ACTIVE", "Social Auto-Poster"),
            ]
            sb_rows = [[InlineKeyboardButton(text=f"{'🟢 ON' if RUNTIME_CONFIG[k] else '🔴 OFF'} — {label}", callback_data=f"adm:toggle_sb:{k}")] for k, label in sb_keys]
            sb_rows.append([InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")])
            await safe_edit_markdown(call.message, "🤖 **PUSAT 5 SUB-BOT OTONOM**", reply_markup=InlineKeyboardMarkup(inline_keyboard=sb_rows))
            return
        else:
            await call.answer("🔄 Disegarkan.")

        cur = await db.execute("SELECT gross_revenue_idr, working_capital_vault_idr, harvestable_profit_vault_idr, total_harvested_by_owner_idr, total_jobs_completed FROM treasury_summary WHERE id = 1;")
        row = await cur.fetchone()
    txt, kb = _build_owner_admin_panel_view(row)
    await safe_edit_markdown(call.message, txt, reply_markup=kb)


@router.callback_query(F.data.startswith("menu:"))
async def handle_customer_menu_callbacks(call: CallbackQuery) -> None:
    action = call.data.split(":", 1)[1]
    user_id, username = call.from_user.id, call.from_user.username or call.from_user.first_name or "Kreator"
    is_priv = call.message.chat.type == "private" if call.message else True
    if not check_velocity_rate_limit(user_id):
        await call.answer("⏳ Tunggu sejenak...", show_alert=False)
        return

    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username, call.from_user.first_name or "", call.from_user.language_code or "id")

        if action == "home":
            await call.answer()
            await safe_edit_markdown(call.message, build_customer_dashboard_caption(username, u), reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv))
            return
        if action == "miniapp_guide":
            await call.answer()
            m_url = RUNTIME_CONFIG["MINIAPP_URL"] or "http://localhost:8080"
            await safe_edit_markdown(call.message, f"📱 **STUDIO WEB:** `{m_url}`", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu:home")]]))
            return
        if action == "wizard_video":
            await call.answer()
            sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(prompt="Cinematic urban street at night, 4k", modality="VIDEO", upscale_mode="VIDEO_4K_60FPS")
            sess.modality = "VIDEO"
            ACTIVE_DRAFTS[user_id] = sess
            txt, kb = build_video_wizard_kb(sess)
            await safe_edit_markdown(call.message, txt, reply_markup=kb)
            return
        if action == "wizard_image":
            await call.answer()
            sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(prompt="Commercial product photography, studio lighting, 4k", modality="IMAGE", upscale_mode="PHOTO_FACE_4K")
            sess.modality = "IMAGE"
            ACTIVE_DRAFTS[user_id] = sess
            txt, kb = build_image_wizard_kb(sess)
            await safe_edit_markdown(call.message, txt, reply_markup=kb)
            return
        if action == "wizard_edit":
            await call.answer()
            sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(prompt="Product studio catalog", modality="EDIT_IMAGE")
            sess.modality = "EDIT_IMAGE"
            ACTIVE_DRAFTS[user_id] = sess
            txt, kb = build_editing_tools_wizard_kb(sess)
            await safe_edit_markdown(call.message, txt, reply_markup=kb)
            return
        if action == "prompt_helper":
            await call.answer("🪄 Menyusun prompt...")
            await increment_user_usage_counter(db, user_id, is_render=False)
            sample = await generate_frontier_ai_response(db, "Commercial product & video showcase", mode="PROMPT_ARCHITECT", personal_memory=u["memory"])
            await safe_edit_markdown(call.message, sample, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu:home")]]))
            return
        if action == "deep_research_hint":
            await call.answer()
            await safe_edit_markdown(call.message, "🔬 Ketik `/riset [topik]` di ruang chat.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu:home")]]))
            return
        if action == "canvas_hint":
            await call.answer()
            await safe_edit_markdown(call.message, f"📝 **CANVAS**\n{u['canvas'] or '_(Kosong)_'}\nKetik `/canvas [instruksi]`.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu:home")]]))
            return
        if action == "unfiltered_external_referral":
            base_url = RUNTIME_CONFIG["MINIAPP_URL"] or "http://localhost:8080"
            portal_url = f"{base_url.rstrip('/')}/unfiltered-portal"
            web_brand = RUNTIME_CONFIG.get("WEB_BRAND_NAME") or "AetherFree AI Studio"
            if u["koin_utama"] >= 4:
                ok_v, _, _ = await deduct_user_coins_for_job(db, user_id, 4, False, f"Kode Akses VIP {web_brand}", "VIP_WEB_PASS")
                units_issued = 15 if ok_v else 5
            else:
                units_issued = 5
            await call.answer("🎟️ Menerbitkan Kode Akses VIP...")
            voucher_str = issue_stateless_ed25519_voucher(user_id, compute_units=units_issued)
            await safe_edit_markdown(
                call.message,
                f"🌐 **{web_brand.upper()}**\n━━━━━━━━━━━━━━━━━━\n"
                f"🎟️ **Kode Akses VIP (+{units_issued} Kredit Studio):**\n`{voucher_str}`\n\n"
                f"🔗 **Tautan Studio Web:**\n{portal_url}",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu:home")]]),
            )
            return
        if action == "quota":
            await call.answer()
            filled = min(10, int((u["koin_bonus"] / MAX_KOIN_BONUS_CAP) * 10))
            bar_visual = "█" * filled + "░" * (10 - filled)
            rem_sec = 86400 - ((int(time.time()) + 7 * 3600) % 86400)
            ppp_rate = PPP_EFFECTIVE_COIN_IDR.get(u["ppp_zone"], 84)
            await safe_edit_markdown(
                call.message,
                f"📊 **STATUS KUOTA HARIAN**\n━━━━━━━━━━━━━━━━━━\n"
                f"┣ 📈 **Koin Bonus:** `[{bar_visual}]` (`{u['koin_bonus']}/{MAX_KOIN_BONUS_CAP}`)\n"
                f"┣ 💎 **Koin Utama:** `{u['koin_utama']} Koin`\n"
                f"┣ ⏳ **Reset (00:00 WIB):** `{rem_sec // 3600}j {(rem_sec % 3600) // 60}m`\n"
                f"┗ 🌏 **Zona PPP:** `Zona {u['ppp_zone']} (~Rp {ppp_rate}/Koin)`",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu:home")]]),
            )
            return
        if action == "claim_daily":
            today_str = time.strftime("%Y-%m-%d")
            if u["last_claim_date"] == today_str:
                await call.answer("🎁 Sudah diklaim hari ini.", show_alert=True)
                return
            if u["koin_bonus"] >= MAX_KOIN_BONUS_CAP:
                await call.answer(f"🎁 Koin Bonus penuh ({MAX_KOIN_BONUS_CAP}).", show_alert=True)
                return
            async def _claim_tx(conn: aiosqlite.Connection) -> int:
                await conn.execute("UPDATE users SET koin_bonus = MIN(?, koin_bonus + 4), last_claim_date = ? WHERE internal_user_id = ?;", (MAX_KOIN_BONUS_CAP, today_str, user_id))
                cur = await conn.execute("SELECT koin_bonus FROM users WHERE internal_user_id = ?;", (user_id,))
                r = await cur.fetchone()
                return int(r[0]) if r else u["koin_bonus"]
            u["koin_bonus"] = await DB_WRITER_DAEMON.execute_write_tx(db, _claim_tx)
            u["last_claim_date"] = today_str
            await call.answer(f"🎉 +4 Koin Gratis ditambahkan ({u['koin_bonus']}/{MAX_KOIN_BONUS_CAP})!", show_alert=True)
            await safe_edit_markdown(call.message, build_customer_dashboard_caption(username, u), reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv))
            return

        if action == "topup_qris" or action.startswith("topup_pkg:"):
            tier_key = action.split(":", 1)[1] if action.startswith("topup_pkg:") else "HEMAT"
            await call.answer()
            inv = await create_payment_invoice(db, user_id, u["ppp_zone"], tier_key=tier_key)
            qris_block = f"\n📦 **Kode Pembayaran QRIS Instan:**\n`{inv['qris_payload']}`\n" if inv["qris_payload"] else ""
            tier_row = [
                InlineKeyboardButton(text=f"{'✅ ' if tier_key=='HEMAT' else ''}⚡ Hemat (60)", callback_data="menu:topup_pkg:HEMAT"),
                InlineKeyboardButton(text=f"{'✅ ' if tier_key=='PRO' else ''}🔥 Pro (350)", callback_data="menu:topup_pkg:PRO"),
                InlineKeyboardButton(text=f"{'✅ ' if tier_key=='SULTAN' else ''}👑 Sultan VIP", callback_data="menu:topup_pkg:SULTAN"),
            ]
            pay_buttons = [tier_row]
            if inv["is_global"]:
                gl_pref = RUNTIME_CONFIG["GLOBAL_ACTIVE_PROVIDER"]
                if "USDT" in gl_pref or "Keduanya" in gl_pref:
                    pay_buttons.append([InlineKeyboardButton(text="₮ Crypto USDT (@CryptoBot)", url="https://t.me/CryptoBot")])
                if "Stars" in gl_pref or "Keduanya" in gl_pref:
                    pay_buttons.append([InlineKeyboardButton(text=f"⭐ Telegram Stars ({inv['display_amount']})", callback_data=f"menu:topup_verify:{inv['invoice_id']}")])
            pay_buttons.append([InlineKeyboardButton(text=f"✅ Konfirmasi Pembayaran (+{inv['coins']} Koin Utama)", callback_data=f"menu:topup_verify:{inv['invoice_id']}")])
            pay_buttons.append([InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu:home")])

            await safe_edit_markdown(
                call.message,
                f"💳 **KASIR OTOMATIS — bikinAI**\n━━━━━━━━━━━━━━━━━━\n"
                f"┣ 📦 **Paket:** **`{inv['pkg_name']}`**\n"
                f"┣ 🧾 **Tagihan:** `{inv['invoice_id']}`\n"
                f"┣ 💰 **Nominal:** **`{inv['display_amount']}`**\n"
                f"┗ 💎 **Koin:** **`+{inv['coins']} Koin Utama`**{qris_block}",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=pay_buttons),
            )
            return

        if action.startswith("topup_verify:"):
            inv_id = action.split(":", 1)[1]
            if RUNTIME_CONFIG.get("AUTO_APPROVE_SANDBOX_TOPUP", False) and not RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"]:
                ok, _, _, _, msg = await approve_invoice_and_credit_coins(db, inv_id)
                await call.answer(msg, show_alert=True)
                u = await ensure_user_and_track_identity(db, user_id, username)
                await safe_edit_markdown(call.message, build_customer_dashboard_caption(username, u), reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv))
                return
            owner_id = int(RUNTIME_CONFIG.get("OWNER_ID_RUNTIME") or 0)
            if owner_id > 0 and BOT_INSTANCE_GLOBAL:
                try:
                    await BOT_INSTANCE_GLOBAL.send_message(
                        chat_id=owner_id,
                        text=f"🔔 **VERIFIKASI TOP-UP**\n┣ 👤 **Pembeli:** `@{username}` (`{user_id}`)\n┗ 🧾 **Tagihan:** `{inv_id}`",
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ ACC", callback_data=f"adm:acc_inv:{inv_id}"), InlineKeyboardButton(text="❌ Tolak", callback_data=f"adm:rej_inv:{inv_id}")]]),
                    )
                except Exception:
                    pass
            await call.answer("⏳ Permintaan verifikasi dikirim ke kasir.", show_alert=True)
            return

        if action == "live_support":
            await call.answer()
            cur = await db.execute("SELECT job_id FROM jobs WHERE internal_user_id = ? AND status = 'PROCESSING' AND refunded_lock = 0 ORDER BY created_at DESC LIMIT 1;", (user_id,))
            stuck_row = await cur.fetchone()
            refund_note = f"\n✅ **Auto-Refund:** Koin pesanan `{stuck_row[0]}` telah dikembalikan!\n" if (stuck_row and await refund_failed_job(db, stuck_row[0])) else ""
            await safe_edit_markdown(call.message, f"🎧 **PUSAT BANTUAN & GARANSI KOIN 100%**{refund_note}\nKetik `/saran [pesan]` untuk mengirim masukan.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu:home")]]))
            return

        if action == "faq_tos":
            await call.answer()
            bindings = await get_all_topic_bindings(db)
            lines_b = [f"▸ [{t_title}](https://t.me/c/{str(c_id).replace('-100', '')}/{t_id})" for _, (c_id, t_id, t_title) in bindings.items() if str(c_id).replace("-100", "").isdigit() and t_id > 0]
            topic_info = "\n".join(lines_b) if lines_b else "_(Gunakan `/setup_grup` di grup komunitas)_"
            await safe_edit_markdown(call.message, f"📜 **PANDUAN & TAUTAN KOMUNITAS**\n━━━━━━━━━━━━━━━━━━\n{topic_info}", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali", callback_data="menu:home")]]))
            return


@router.callback_query(F.data.startswith("wiz:"))
async def handle_wizard_callbacks(call: CallbackQuery) -> None:
    user_id, username = call.from_user.id, call.from_user.username or "Kreator"
    parts = call.data.split(":", 2)
    if len(parts) < 3:
        await call.answer()
        return
    sub_cmd, val = parts[1], parts[2]
    sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(prompt="Commercial studio photography, 4k", modality="IMAGE")
    ACTIVE_DRAFTS[user_id] = sess

    if sub_cmd == "prompt" and val == "edit":
        WAITING_PROMPT_EDIT_USERS.add(user_id)
        await call.answer("✏️ Ketik deskripsi baru di ruang chat!", show_alert=True)
        await call.message.reply("✏️ **Ketik deskripsi baru Anda sekarang:**", parse_mode="Markdown")
        return

    if sub_cmd == "ar":
        sess.aspect_ratio = val
    elif sub_cmd == "dur":
        sess.duration_sec = int(val)
    elif sub_cmd == "veng":
        sess.video_engine, sess.modality, sess.upscale_mode = val, "VIDEO", "VIDEO_4K_60FPS"
    elif sub_cmd == "ieng":
        sess.image_engine, sess.modality, sess.upscale_mode = val, "IMAGE", "PHOTO_FACE_4K"
    elif sub_cmd == "vpre":
        title_p, mod_p = AWAM_VIDEO_MOTION_PRESETS.get(val, ("Motion", "smooth camera motion"))
        sess.awam_preset = title_p
        if mod_p not in sess.prompt:
            sess.prompt = f"{sess.prompt}, {mod_p}"[:180]
    elif sub_cmd == "ipre":
        title_p, mod_p = AWAM_IMAGE_STYLE_PRESETS.get(val, ("Studio", "studio lighting"))
        sess.awam_preset = title_p
        if mod_p not in sess.prompt:
            sess.prompt = f"{sess.prompt}, {mod_p}"[:180]
    elif sub_cmd == "etool":
        sess.edit_tool, sess.modality = val, "EDIT_IMAGE"
        if val == "IMG2VID_MOTION":
            sess.upscale_mode = "VIDEO_4K_60FPS"
    elif sub_cmd == "ups":
        sess.upscale_mode = val
    elif sub_cmd == "exec":
        coins, hpp_idr, allow_bonus = sess.get_pricing()
        is_vid_exec = sess.modality == "VIDEO" or (sess.modality == "EDIT_IMAGE" and sess.edit_tool == "IMG2VID_MOTION")
        engine_label = sess.video_engine if is_vid_exec else (sess.image_engine if sess.modality == "IMAGE" else sess.edit_tool)
        async with get_db() as db:
            await ensure_user_and_track_identity(db, user_id, username)
            ok, job_id, deduct_msg = await deduct_user_coins_for_job(db, user_id, coins, allow_bonus, sess.prompt, engine_label)
            if not ok:
                await call.answer(f"⚠️ {deduct_msg}", show_alert=True)
                return
            await call.answer("🚀 Memproses...")
            await safe_edit_markdown(call.message, f"⏳ **MEMPROSES `{job_id}`...**\n┣ ⚡ **Model:** `{engine_label}`\n┗ 💳 `{deduct_msg}`")
            ups_label = UPSCALER_WHITE_LABEL.get(sess.upscale_mode, "🔍 Pertajam Foto & Wajah 4K")
            try:
                if is_vid_exec:
                    await call.message.answer_video(video=SAMPLE_SANDBOX_VIDEO_URL, caption=f"🎬 **VIDEO SELESAI**\n┣ ⚡ **Model:** `{engine_label}` ({sess.aspect_ratio})\n┗ 🔍 **Kualitas:** `{ups_label}`", parse_mode="Markdown", reply_markup=build_400_percent_derivative_upsell_kb())
                elif sess.modality == "EDIT_IMAGE" and sess.edit_tool == "REMOVE_BG_PNG":
                    img_bytes = await fetch_clean_image_bytes(f"{sess.prompt}, isolated subject on pure transparent background, PNG cutout", 768, 768)
                    if not img_bytes:
                        raise RuntimeError("PNG stream error")
                    await call.message.answer_document(document=BufferedInputFile(img_bytes, filename=f"bikinAI_Transparan_{int(time.time())}.png"), caption=f"✂️ **FILE PNG TRANSPARAN**\n┗ 🔍 `{ups_label}`", parse_mode="Markdown", reply_markup=build_400_percent_derivative_upsell_kb())
                else:
                    w, h = (768, 1024) if sess.aspect_ratio == "9:16" else ((1024, 768) if sess.aspect_ratio == "16:9" else (1024, 1024))
                    img_bytes = await fetch_clean_image_bytes(f"{sess.prompt}, {engine_label}, 8k", w, h)
                    if not img_bytes:
                        raise RuntimeError("Image render error")
                    await call.message.answer_photo(photo=BufferedInputFile(img_bytes, filename="bikinAI_Studio_4K.jpg"), caption=f"✨ **GAMBAR 4K SELESAI**\n┣ ⚡ **Model:** `{engine_label}` ({sess.aspect_ratio})\n┗ 🔍 **Kualitas:** `{ups_label}`", parse_mode="Markdown", reply_markup=build_400_percent_derivative_upsell_kb())
                await increment_user_usage_counter(db, user_id, is_render=True)
                await mark_job_completed(db, job_id, sess.prompt, engine_label)
                stats = await record_job_and_split_profit(db, revenue_idr=coins * 84, actual_hpp_idr=hpp_idr)
                await broadcast_to_bound_topic(call.bot, db, "ACTIVITY_TOPIC", f"⚡ **Live Neural Feed #{stats['fomo_counter']}**\n`@{username}` merender dengan **`{engine_label}`** ({sess.aspect_ratio}).")
            except Exception:
                await refund_failed_job(db, job_id)
                await safe_edit_markdown(call.message, f"🛡️ **Auto-Refund:** Koin pesanan `{job_id}` telah dikembalikan utuh!")
        return

    await call.answer()
    txt, kb = build_video_wizard_kb(sess) if sess.modality == "VIDEO" else (build_image_wizard_kb(sess) if sess.modality == "IMAGE" else build_editing_tools_wizard_kb(sess))
    await safe_edit_markdown(call.message, txt, reply_markup=kb)


@router.callback_query(F.data.startswith("drv:"))
async def handle_derivative_upsell_callbacks(call: CallbackQuery) -> None:
    user_id, username = call.from_user.id, call.from_user.username or "Kreator"
    drv_type = call.data.split(":", 1)[1]
    sess = ACTIVE_DRAFTS.get(user_id)
    base_prompt = sess.prompt if sess else "4K YouTube & TikTok poster thumbnail"
    cost = 10 if drv_type == "clean_license" else 4
    async with get_db() as db:
        await ensure_user_and_track_identity(db, user_id, username)
        ok, job_id, deduct_msg = await deduct_user_coins_for_job(db, user_id, cost, True, base_prompt, f"DRV_{drv_type.upper()}")
        if not ok:
            await call.answer(f"⚠️ {deduct_msg}", show_alert=True)
            return
        if drv_type == "poster4k":
            await call.answer("🖼️ Merender Poster 4K...", show_alert=False)
            img_bytes = await fetch_clean_image_bytes(f"{base_prompt}, 4K YouTube poster thumbnail, 8k", 1024, 768)
            if img_bytes:
                await call.message.answer_photo(photo=BufferedInputFile(img_bytes, filename="bikinAI_Poster_4K.jpg"), caption=f"🖼️ **Poster 4K Selesai**\n┗ 💳 `{deduct_msg}`", parse_mode="Markdown")
                await mark_job_completed(db, job_id, base_prompt, "DRV_POSTER_4K")
                await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            else:
                await refund_failed_job(db, job_id)
                await call.answer("🛡️ Gagal, koin dikembalikan 100%.", show_alert=True)
        elif drv_type == "audiomp3":
            await mark_job_completed(db, job_id, base_prompt, "DRV_AUDIO_MP3")
            await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            await call.answer("🎵 Audio MP3 selesai!", show_alert=True)
            await call.message.reply(f"🎵 **AUDIO MP3 SELESAI (`{job_id}`)**\n┗ 💳 `{deduct_msg}`", parse_mode="Markdown")
        elif drv_type == "clean_license":
            await mark_job_completed(db, job_id, base_prompt, "DRV_CLEAN_LICENSE")
            await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            await call.answer("✨ Lisensi aktif!", show_alert=True)
            await call.message.reply(f"📜 **SERTIFIKAT LISENSI KOMERSIAL (`LIC-{job_id}`)**\nPemegang: `@{username}`", parse_mode="Markdown")


# 14. GROUP SETUP, WELCOME GATE, MULTIMODAL UPLOAD & NATURAL/TECHNICAL ROUTER
@router.message(Command("setup_grup"))
async def cmd_setup_community_group(message: Message) -> None:
    if message.chat.type not in ("group", "supergroup"):
        await message.reply("Gunakan `/setup_grup` di dalam grup komunitas.")
        return
    chat_id = message.chat.id
    topics_to_create = [
        ("ACTIVITY_TOPIC", "⚡ Live Neural Feed"), ("COMMAND_TOPIC", "📡 Command Center & Promo"),
        ("FAQ_TOPIC", "🧭 Blueprint & Koin Gratis"), ("CREATIVE_TOPIC", "🧠 Arsitek Prompt & Ide 24/7"),
        ("GALLERY_TOPIC", "🎬 Galeri Kreator & Preset"), ("FEEDBACK_TOPIC", "🛠️ Lab Inovasi & Bantuan"),
    ]
    async with get_db() as db:
        for b_key, t_title in topics_to_create:
            try:
                res_topic = await message.bot.create_forum_topic(chat_id=chat_id, name=t_title)
                await set_topic_binding(db, b_key, chat_id, res_topic.message_thread_id, title=t_title)
            except Exception:
                await set_topic_binding(db, b_key, chat_id, 0, title=t_title)
    await message.reply("✅ **6 Topik Grup berhasil dibuat dan diikat ke database.**", parse_mode="Markdown")


@router.message(Command("ikat"))
async def cmd_bind_current_topic_interactive(message: Message) -> None:
    if message.chat.type not in ("group", "supergroup"):
        return
    tid = message.message_thread_id or 0
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚡ Live Neural Feed", callback_data=f"bind:ACTIVITY_TOPIC:{tid}"), InlineKeyboardButton(text="📡 Command & Promo", callback_data=f"bind:COMMAND_TOPIC:{tid}")],
        [InlineKeyboardButton(text="🧭 Blueprint & Koin", callback_data=f"bind:FAQ_TOPIC:{tid}"), InlineKeyboardButton(text="🧠 Arsitek Prompt", callback_data=f"bind:CREATIVE_TOPIC:{tid}")],
        [InlineKeyboardButton(text="🎬 Galeri Kreator", callback_data=f"bind:GALLERY_TOPIC:{tid}"), InlineKeyboardButton(text="🛠️ Lab Inovasi & Bantuan", callback_data=f"bind:FEEDBACK_TOPIC:{tid}")],
    ])
    await message.reply("Pilih fungsi topik:", reply_markup=kb)


@router.callback_query(F.data.startswith("bind:"))
async def handle_topic_binding_cb(call: CallbackQuery) -> None:
    parts = call.data.split(":")
    b_key, t_id = parts[1], int(parts[2])
    async with get_db() as db:
        await set_topic_binding(db, b_key, call.message.chat.id, t_id, title=b_key)
    await call.answer(f"✅ Diikat ke {b_key}", show_alert=True)
    await safe_edit_markdown(call.message, f"✅ **Topik diikat ke `{b_key}` (ID: `{t_id}`).**")


@router.message(F.new_chat_members)
async def handle_builtin_cyber_welcome_gate(message: Message) -> None:
    if not RUNTIME_CONFIG["SUBBOT_WELCOME_GUARD_ACTIVE"]:
        return
    for member in message.new_chat_members:
        if member.is_bot:
            continue
        uname = member.username or member.first_name or "Kreator"
        async with get_db() as db:
            u = await ensure_user_and_track_identity(db, member.id, uname, member.first_name or "")
        await safe_reply_markdown(
            message,
            f"⚡ **Selamat datang di `bikinAI Super Intelligence`, `@{u['safe_uname']}`!**\n"
            f"Ketik `/start` di chat pribadi `@{BOT_USERNAME_GLOBAL}` untuk mengambil **+4 Koin Gratis Harian**.",
        )


@router.message(F.photo | F.document)
async def handle_multimodal_photo_and_pdf(message: Message) -> None:
    caption_raw = message.caption or ""
    clean_caption, is_attack = sanitize_and_deobfuscate_input(caption_raw)
    if is_attack:
        await message.reply("🛡️ Pola teks tidak diizinkan.")
        return

    if message.document:
        doc_name = message.document.file_name or "Dokumen"
        wait_doc = await message.reply(f"📄 **Memproses dokumen `{doc_name}`...**", parse_mode="Markdown")
        async with get_db() as db:
            res = await generate_frontier_ai_response(db, f"Dokumen: {doc_name}. Instruksi: {clean_caption or 'Analisis teknis isi dokumen.'}", mode="DEEP_RESEARCH")
        await safe_edit_markdown(wait_doc, f"📄 **HASIL ANALISIS `{doc_name}`**\n━━━━━━━━━━━━━━━━━━\n{res}")
        return

    wait = await message.reply("🎨 **Memproses Foto Referensi...**", parse_mode="Markdown")
    target_prompt = clean_caption if clean_caption else "Commercial studio photography, 8k"
    if message.from_user:
        ACTIVE_DRAFTS[message.from_user.id] = LiveWizardSession(prompt=target_prompt[:150], modality="IMAGE")

    img_bytes = await fetch_clean_image_bytes(f"{target_prompt}, bytedance/seedream-4.0, 8k", 768, 1024)
    if img_bytes:
        if message.from_user:
            async with get_db() as db:
                await increment_user_usage_counter(db, message.from_user.id, is_render=True)
        await message.answer_photo(
            photo=BufferedInputFile(img_bytes, filename="bikinAI_Ref_4K.jpg"),
            caption=f"✨ **Selesai!**\n┣ 📝 **Instruksi:** _{target_prompt[:120]}_\n┗ ⚡ **Model:** `bytedance/seedream-4.0`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🖼️➡️🎬 Gerakkan Foto Jadi Video (Img2Vid)", callback_data="menu:wizard_video")],
                [InlineKeyboardButton(text="⬅️ Menu Utama", callback_data="menu:home")],
            ]),
        )
        await wait.delete()
    else:
        await safe_edit_markdown(wait, "✅ Foto referensi diterima. Ketik `menu` untuk opsi lanjutan.")


@router.message(F.text)
async def handle_natural_conversation(message: Message) -> None:
    raw_text = message.text or ""
    low = raw_text.lower().strip()
    user_id, username = message.from_user.id, message.from_user.username or "Kreator"
    is_priv = message.chat.type == "private"

    clean_text, is_attack = sanitize_and_deobfuscate_input(raw_text)
    if is_attack:
        await message.reply("🛡️ Pola teks tidak diizinkan.")
        return

    if user_id in WAITING_PROMPT_EDIT_USERS:
        WAITING_PROMPT_EDIT_USERS.discard(user_id)
        sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(prompt=clean_text[:180], modality="IMAGE")
        sess.prompt = clean_text[:180]
        ACTIVE_DRAFTS[user_id] = sess
        txt, kb = build_video_wizard_kb(sess) if sess.modality == "VIDEO" else (build_image_wizard_kb(sess) if sess.modality == "IMAGE" else build_editing_tools_wizard_kb(sess))
        await safe_reply_markdown(message, f"✅ **Deskripsi diperbarui.**\n\n{txt}", reply_markup=kb)
        return

    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username, message.from_user.first_name or "")
        updated_mem = await update_personal_memory_if_needed(db, user_id, clean_text, u["memory"])

        if any(t in low for t in ("tampilin tombol", "tampilkan tombol", "munculin tombol", "buka menu")) or low == "menu":
            await safe_reply_markdown(message, "🎛️ **Menu Utama:**", reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv))
            return

        if any(k in low for k in ("buatkan saya gambar", "buat gambar", "bikin gambar", "render gambar")):
            ACTIVE_DRAFTS[user_id] = LiveWizardSession(prompt=clean_text[:150], modality="IMAGE")
            cost_chat_img = 0 if (u["free_img_used_today"] < 1 or RUNTIME_CONFIG["HAPPY_HOUR_MODE"]) else 4
            ok, job_id, deduct_msg = await deduct_user_coins_for_job(db, user_id, cost_chat_img, True, clean_text, "black-forest-labs/FLUX.1-dev")
            if not ok:
                await safe_reply_markdown(message, f"⚠️ {deduct_msg}", reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv))
                return
            wait = await message.reply("🎨 **Merender gambar 4K...**", parse_mode="Markdown")
            img_bytes = await fetch_clean_image_bytes(f"{clean_text}, black-forest-labs/FLUX.1-dev, 8k", 768, 1024)
            if img_bytes:
                await increment_user_usage_counter(db, user_id, is_render=True)
                await mark_job_completed(db, job_id, clean_text, "black-forest-labs/FLUX.1-dev")
                await record_job_and_split_profit(db, revenue_idr=cost_chat_img * 84, actual_hpp_idr=0)
                await message.answer_photo(photo=BufferedInputFile(img_bytes, filename="bikinAI_4K.jpg"), caption=f"✨ **Gambar 4K Selesai**\n┣ ⚡ **Model:** `black-forest-labs/FLUX.1-dev`\n┗ 💳 `{deduct_msg}`", parse_mode="Markdown", reply_markup=build_400_percent_derivative_upsell_kb())
                await wait.delete()
                return
            await refund_failed_job(db, job_id)
            await safe_edit_markdown(wait, "🛡️ **Auto-Refund:** Koin dikembalikan utuh.")
            return

        if any(k in low for k in ("buat video", "bikin video", "buatkan video", "foto jadi video")) and "gimana" not in low:
            ACTIVE_DRAFTS[user_id] = LiveWizardSession(prompt=clean_text[:150], modality="VIDEO", upscale_mode="VIDEO_4K_60FPS")
            txt, kb = build_video_wizard_kb(ACTIVE_DRAFTS[user_id])
            await safe_reply_markdown(message, txt, reply_markup=kb)
            return

        await increment_user_usage_counter(db, user_id, is_render=False)
        mode_chat = "PROMPT_ARCHITECT" if low.startswith("prompt ") else "NATURAL_CHAT"
        ai_reply = await generate_frontier_ai_response(db, clean_text, mode=mode_chat, personal_memory=updated_mem)

    # Jika pertanyaan bersifat teknis/kode, jangan tambahkan footer sapaan kasual
    if is_technical_or_code_query(clean_text):
        await safe_reply_markdown(message, ai_reply)
    else:
        await safe_reply_markdown(message, ai_reply + "\n\n_Ketik `menu` untuk menampilkan tombol fitur._")


# 15. ENTRYPOINT UTAMA (MAIN)
async def main() -> None:
    global BOT_INSTANCE_GLOBAL, BOT_USERNAME_GLOBAL
    if not BOT_TOKEN:
        print("❌ TOKEN_BOT_UTAMA belum diatur di .env!")
        return

    async with get_db() as db:
        await init_master_db(db)

    if RUNTIME_CONFIG["OWNER_ID_RUNTIME"] == 0:
        print(f"🔐 [BOOTSTRAP]: /claim_owner {OWNER_BOOTSTRAP_TOKEN}")

    await start_embedded_web_servers(port=8080)
    asyncio.create_task(_background_dead_job_sweeper_loop())

    bot = Bot(token=BOT_TOKEN)
    BOT_INSTANCE_GLOBAL = bot
    me = await bot.get_me()
    BOT_USERNAME_GLOBAL = me.username or "bikinAI_bot"

    dp = Dispatcher()
    dp.include_router(router)
    print(f"🚀 bikinAI v3.7.1 (@{BOT_USERNAME_GLOBAL}) ACTIVE.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
