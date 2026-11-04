
<!-- [ID:02_CORE_AI_S028] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: INLINEKEYBOARDBUTTON -->
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
        [InlineKeyboardButton(text="✏️ Ubah Prompt / Konsep Video", callback_data="wiz:prompt:edit")],
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
        [InlineKeyboardButton(text="✏️ Ubah Prompt / Konsep Gambar", callback_data="wiz:prompt:edit")],
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
        [InlineKeyboardButton(text="✏️ Ubah Instruksi / Objek Editing", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 PROSES EDITING SEKARANG ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ]
    return text, InlineKeyboardMarkup(inline_keyboard=rows)



<!-- [ID:02_CORE_AI_S029] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: ANY -->
# ------------------------------------------------------------------------------
async def run_dead_job_refund_sweeper_once() -> int:
    """
    Menyapu job yang menggantung (`PROCESSING` lebih dari 60 detik) dan mengembalikan
    Koin Utama & Koin Bonus secara utuh dengan pengunci `refunded_lock = 1`.
    """
    db = get_db()
    cutoff = int(time.time()) - 60
    stale_jobs = await db.fetch_all(
        "SELECT job_id FROM jobs WHERE status = 'PROCESSING' AND refunded_lock = 0 AND created_at <= ?;",
        (cutoff,),
    )
    for j in stale_jobs:
        await finalize_job_status(j["job_id"], success=False)
    return len(stale_jobs)


async def run_auto_cs_siska_followup_once(bot: Optional[Any] = None) -> int:
    """
    Auto-CS "Siska" Follow-Up 20 menit (1.200 detik) untuk invoice `PENDING`
    yang belum dikirimkan pengingat ramah.
    """
    db = get_db()
    cutoff = int(time.time()) - 1200
    pending_list = await db.fetch_all(
        "SELECT * FROM payment_invoices WHERE status = 'PENDING' AND followup_sent = 0 AND created_at <= ?;",
        (cutoff,),
    )
    count = 0
    for inv in pending_list:
        await db.execute_write(
            "UPDATE payment_invoices SET followup_sent = 1 WHERE invoice_id = ?;",
            (inv["invoice_id"],),
        )
        count += 1
        if bot is not None:
            try:
                await bot.send_message(
                    chat_id=int(inv["user_id"]),
                    text=(
                        f"Halo Kak! 👋 Saya \x3cb>Siska\x3c/b> dari tim layanan sahabat \x3cb>bikinAI\x3c/b>.\n\n"
                        f"Saya melihat tagihan \x3ccode>{inv['invoice_id']}\x3c/code> (Rp {int(inv['amount_idr']):,}) "
                        f"untuk \x3cb>+{inv['coins_credited']} Koin Utama (100% Bebas Watermark)\x3c/b> belum selesai.\n"
                        f"Apakah ada kendala saat scan QRIS yang bisa Siska bantu? 😊"
                    ),
                    parse_mode="HTML",
                )
            except Exception as exc:
                logger.debug("Auto-CS Siska DM skipped for %s: %s", inv["user_id"], exc)
    return count


async def run_milestone_100_user_notifier_once(bot: Optional[Any] = None) -> bool:
    """Memberikan notifikasi perayaan ke grup komunitas setiap kelipatan 100 pengguna."""
    db = get_db()
    row = await db.fetch_one("SELECT COUNT(*) AS cnt FROM users;")
    total_users = int(row["cnt"]) if row else 0
    last_milestone = int(await db.get_setting("last_milestone_notified", "0") or "0")

    if total_users >= 100 and (total_users // 100) * 100 > last_milestone:
        new_milestone = (total_users // 100) * 100
        await db.set_setting("last_milestone_notified", str(new_milestone))
        binding = await db.fetch_one("SELECT * FROM bot_bindings WHERE binding_key = 'KOMUNITAS';")
        if bot is not None and binding:
            try:
                await bot.send_message(
                    chat_id=int(binding["chat_id"]),
                    message_thread_id=int(binding["topic_id"]) or None,
                    text=(
                        f"🎉 \x3cb>PERAYAAN MILESTONE KOMUNITAS!\x3c/b>\n"
                        f"Keluarga besar \x3cb>bikinAI Studio\x3c/b> kini telah mencapai \x3cb>{new_milestone} Kreator\x3c/b>! "
                        f"Terima kasih atas dukungan dan karya luar biasa kalian semua! 🚀"
                    ),
                    parse_mode="HTML",
                )
            except Exception as exc:
                logger.debug("Milestone group notification skipped: %s", exc)
        return True
    return False


async def _background_autonomous_daemons_loop(bot: Optional[Any] = None) -> None:
    """
    Loop daemon otonom latar belakang yang berjalan setiap 60 detik:
    1. Dead-Job Refund Sweeper (60s)
    2. Auto-CS "Siska" Follow-Up 20 menit untuk invoice PENDING
    3. Milestone 100 User Group Notifier
    """
    logger.info("Background Autonomous Daemons Loop diaktifkan (interval 60 detik).")
    while True:
        try:
            await run_dead_job_refund_sweeper_once()
            await run_auto_cs_siska_followup_once(bot=bot)
            await run_milestone_100_user_notifier_once(bot=bot)
        except asyncio.CancelledError:
            break
        except Exception as exc:
            logger.warning("Background daemon cycle warning: %s", exc)
        await asyncio.sleep(60.0)


async def main() -> None:
    """
    Entrypoint Utama `BIKINAI SUPER INTELLIGENCE — MASTER ENGINE v4.0.0`:
    1. Menginisialisasi SingleWriterSQLiteDaemon & 16 Tabel WAL.
    2. Menjalankan Dual Web Server di Port 8080 (`/` SFW Studio & `/unfiltered-portal` + REST/Omnichannel).
    3. Menjadwalkan `_background_autonomous_daemons_loop()`.
    4. Menyertakan `dp.include_router(router)` dan menjalankan polling Telegram Bot.
    """
    db = get_db()
    db.init_schema_sync()

    # Daftarkan plugin bawaan ke PluginRegistry
    async def _core_watermark_plugin(ctx: Dict[str, Any]) -> Dict[str, Any]:
        return resolve_watermark_policy(
            deducted_utama=int(ctx.get("deducted_utama", 0)),
            deducted_bonus=int(ctx.get("deducted_bonus", 0)),
            has_active_subscription=bool(ctx.get("has_active_subscription", False)),
            explicit_clean_license=bool(ctx.get("explicit_clean_license", False)),
        )

    PLUGIN_REGISTRY.register(
        name="core_watermark_enforcer_a4a",
        version="4.0.0",
        handler=_core_watermark_plugin,
    )

    web_runner = await start_embedded_web_servers(port=WEB_PORT)
    bot_instance: Optional[Any] = None
    daemon_task: Optional[asyncio.Task[Any]] = None

    try:
        if HAS_AIOGRAM and not BOT_TOKEN.startswith("0000000000:"):
            bot_instance = Bot(
                token=BOT_TOKEN,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            )
            dp = Dispatcher()
            dp.include_router(router)
            daemon_task = asyncio.create_task(_background_autonomous_daemons_loop(bot=bot_instance))
            logger.info("Memulai polling Telegram Bot v4.0.0...")
            await dp.start_polling(bot_instance)
        else:
            # Tetap sertakan wiring router standar untuk mode pengujian/staging
            dp_staging = Dispatcher()
            dp_staging.include_router(router)
            daemon_task = asyncio.create_task(_background_autonomous_daemons_loop(bot=None))
            logger.info("Mode Server Mandiri aktif di port %d.", WEB_PORT)
            await asyncio.Event().wait()
    finally:
        if daemon_task is not None:
            daemon_task.cancel()
        if web_runner is not None:
            await web_runner.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("BikinAI Master Engine v4.0.0 berhenti dengan aman.")
```

## 39. v4_0.txt

```txt
#!/usr/bin/env python3

<!-- [ID:02_CORE_AI_S030] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: ANY -->
# ------------------------------------------------------------------------------
async def run_dead_job_refund_sweeper_once() -> int:
    """
    Menyapu job yang menggantung (`PROCESSING` lebih dari 60 detik) dan mengembalikan
    Koin Utama & Koin Bonus secara utuh dengan pengunci `refunded_lock = 1`.
    """
    db = get_db()
    cutoff = int(time.time()) - 60
    stale_jobs = await db.fetch_all(
        "SELECT job_id FROM jobs WHERE status = 'PROCESSING' AND refunded_lock = 0 AND created_at <= ?;",
        (cutoff,),
    )
    for j in stale_jobs:
        await finalize_job_status(j["job_id"], success=False)
    return len(stale_jobs)


async def run_auto_cs_siska_followup_once(bot: Optional[Any] = None) -> int:
    """
    Auto-CS "Siska" Follow-Up 20 menit (1.200 detik) untuk invoice `PENDING`
    yang belum dikirimkan pengingat ramah.
    """
    db = get_db()
    cutoff = int(time.time()) - 1200
    pending_list = await db.fetch_all(
        "SELECT * FROM payment_invoices WHERE status = 'PENDING' AND followup_sent = 0 AND created_at <= ?;",
        (cutoff,),
    )
    count = 0
    for inv in pending_list:
        await db.execute_write(
            "UPDATE payment_invoices SET followup_sent = 1 WHERE invoice_id = ?;",
            (inv["invoice_id"],),
        )
        count += 1
        if bot is not None:
            try:
                await bot.send_message(
                    chat_id=int(inv["user_id"]),
                    text=(
                        f"Halo Kak! 👋 Saya \x3cb>Siska\x3c/b> dari tim layanan sahabat \x3cb>bikinAI\x3c/b>.\n\n"
                        f"Saya melihat tagihan \x3ccode>{inv['invoice_id']}\x3c/code> (Rp {int(inv['amount_idr']):,}) "
                        f"untuk \x3cb>+{inv['coins_credited']} Koin Utama (100% Bebas Watermark)\x3c/b> belum selesai.\n"
                        f"Apakah ada kendala saat scan QRIS yang bisa Siska bantu? 😊"
                    ),
                    parse_mode="HTML",
                )
            except Exception as exc:
                logger.debug("Auto-CS Siska DM skipped for %s: %s", inv["user_id"], exc)
    return count


async def run_milestone_100_user_notifier_once(bot: Optional[Any] = None) -> bool:
    """Memberikan notifikasi perayaan ke grup komunitas setiap kelipatan 100 pengguna."""
    db = get_db()
    row = await db.fetch_one("SELECT COUNT(*) AS cnt FROM users;")
    total_users = int(row["cnt"]) if row else 0
    last_milestone = int(await db.get_setting("last_milestone_notified", "0") or "0")

    if total_users >= 100 and (total_users // 100) * 100 > last_milestone:
        new_milestone = (total_users // 100) * 100
        await db.set_setting("last_milestone_notified", str(new_milestone))
        binding = await db.fetch_one("SELECT * FROM bot_bindings WHERE binding_key = 'KOMUNITAS';")
        if bot is not None and binding:
            try:
                await bot.send_message(
                    chat_id=int(binding["chat_id"]),
                    message_thread_id=int(binding["topic_id"]) or None,
                    text=(
                        f"🎉 \x3cb>PERAYAAN MILESTONE KOMUNITAS!\x3c/b>\n"
                        f"Keluarga besar \x3cb>bikinAI Studio\x3c/b> kini telah mencapai \x3cb>{new_milestone} Kreator\x3c/b>! "
                        f"Terima kasih atas dukungan dan karya luar biasa kalian semua! 🚀"
                    ),
                    parse_mode="HTML",
                )
            except Exception as exc:
                logger.debug("Milestone group notification skipped: %s", exc)
        return True
    return False


async def _background_autonomous_daemons_loop(bot: Optional[Any] = None) -> None:
    """
    Loop daemon otonom latar belakang yang berjalan setiap 60 detik:
    1. Dead-Job Refund Sweeper (60s)
    2. Auto-CS "Siska" Follow-Up 20 menit untuk invoice PENDING
    3. Milestone 100 User Group Notifier
    """
    logger.info("Background Autonomous Daemons Loop diaktifkan (interval 60 detik).")
    while True:
        try:
            await run_dead_job_refund_sweeper_once()
            await run_auto_cs_siska_followup_once(bot=bot)
            await run_milestone_100_user_notifier_once(bot=bot)
        except asyncio.CancelledError:
            break
        except Exception as exc:
            logger.warning("Background daemon cycle warning: %s", exc)
        await asyncio.sleep(60.0)


async def main() -> None:
    """
    Entrypoint Utama `BIKINAI SUPER INTELLIGENCE — MASTER ENGINE v4.0.0`:
    1. Menginisialisasi SingleWriterSQLiteDaemon & 16 Tabel WAL.
    2. Menjalankan Dual Web Server di Port 8080 (`/` SFW Studio & `/unfiltered-portal` + REST/Omnichannel).
    3. Menjadwalkan `_background_autonomous_daemons_loop()`.
    4. Menyertakan `dp.include_router(router)` dan menjalankan polling Telegram Bot.
    """
    db = get_db()
    db.init_schema_sync()

    # Daftarkan plugin bawaan ke PluginRegistry
    async def _core_watermark_plugin(ctx: Dict[str, Any]) -> Dict[str, Any]:
        return resolve_watermark_policy(
            deducted_utama=int(ctx.get("deducted_utama", 0)),
            deducted_bonus=int(ctx.get("deducted_bonus", 0)),
            has_active_subscription=bool(ctx.get("has_active_subscription", False)),
            explicit_clean_license=bool(ctx.get("explicit_clean_license", False)),
        )

    PLUGIN_REGISTRY.register(
        name="core_watermark_enforcer_a4a",
        version="4.0.0",
        handler=_core_watermark_plugin,
    )

    web_runner = await start_embedded_web_servers(port=WEB_PORT)
    bot_instance: Optional[Any] = None
    daemon_task: Optional[asyncio.Task[Any]] = None

    try:
        if HAS_AIOGRAM and not BOT_TOKEN.startswith("0000000000:"):
            bot_instance = Bot(
                token=BOT_TOKEN,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            )
            dp = Dispatcher()
            dp.include_router(router)
            daemon_task = asyncio.create_task(_background_autonomous_daemons_loop(bot=bot_instance))
            logger.info("Memulai polling Telegram Bot v4.0.0...")
            await dp.start_polling(bot_instance)
        else:
            # Tetap sertakan wiring router standar untuk mode pengujian/staging
            dp_staging = Dispatcher()
            dp_staging.include_router(router)
            daemon_task = asyncio.create_task(_background_autonomous_daemons_loop(bot=None))
            logger.info("Mode Server Mandiri aktif di port %d.", WEB_PORT)
            await asyncio.Event().wait()
    finally:
        if daemon_task is not None:
            daemon_task.cancel()
        if web_runner is not None:
            await web_runner.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("BikinAI Master Engine v4.0.0 berhenti dengan aman.")
```

## 40. converted (1).md

```md

<!-- [ID:02_CORE_AI_S031] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
## Halaman 40

PRAGMA synchronous = NORMAL;​
PRAGMA busy_timeout = 10000;​
PRAGMA temp_store = MEMORY;​
PRAGMA mmap_size = 268435456; -- 256 MB Memory-Mapped I/O​
​
-- 1. TABEL PENGGUNA UTAMA (DENGAN HARD-CAP KOIN BONUS & LOCK PPP 
ZONE)​
CREATE TABLE IF NOT EXISTS users (​
    internal_user_id INTEGER PRIMARY KEY AUTOINCREMENT,​
    koin_utama INTEGER NOT NULL DEFAULT 0 CHECK (koin_utama >= 0),​
    koin_bonus INTEGER NOT NULL DEFAULT 4 CHECK (koin_bonus >= 0 AND 
koin_bonus <= 25),​
    has_topped_up INTEGER NOT NULL DEFAULT 0,​
    ppp_zone INTEGER NOT NULL DEFAULT 3, -- 1: Global Premium, 2: 
Emerging, 3: Indonesia QRIS​
    referred_by INTEGER,​
    last_claim_date TEXT,​
    vouchers_minted_today INTEGER NOT NULL DEFAULT 0,​
    created_at INTEGER NOT NULL​
);​
​
-- 2. TABEL IDENTITAS LINTAS PLATFORM ("1 OTAK, 3 PINTU": TELEGRAM, 
WA, FB)​
CREATE TABLE IF NOT EXISTS platform_identities (​
    identity_id INTEGER PRIMARY KEY AUTOINCREMENT,​
    internal_user_id INTEGER NOT NULL,​
    platform_type TEXT NOT NULL CHECK (platform_type IN ('tg', 'wa', 
'fb')),​
    external_id TEXT NOT NULL UNIQUE,​
    language_code TEXT DEFAULT 'id',​
    device_fp_hash TEXT,​
    FOREIGN KEY (internal_user_id) REFERENCES users(internal_user_id)​
);​
​
-- 3. TABEL BUKU BESAR AKUNTANSI APPEND-ONLY (ANTI DOUBLE-CREDIT 
WEBHOOK)​
CREATE TABLE IF NOT EXISTS wallet_ledger (​
    tx_id INTEGER PRIMARY KEY AUTOINCREMENT,​
    internal_user_id INTEGER NOT NULL,​
    wallet_type TEXT NOT NULL CHECK (wallet_type IN ('UTAMA', 
'BONUS')),​
    delta_amount INTEGER NOT NULL,​
    balance_after INTEGER NOT NULL,​
    tx_type TEXT NOT NULL, -- 'TOPUP_QRIS', 'TOPUP_STARS', 
'ESCROW_HOLD', 'REFUND', 'DAILY_CLAIM', 'VOUCHER_MINT'​
    idempotency_key TEXT NOT NULL UNIQUE,​
    created_at INTEGER NOT NULL​
);​



<!-- [ID:02_CORE_AI_S032] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
### Tahap 4 dan 5: Sintesis Mandiri Berkas SKILL.md dan Hot-Swap Produksi
Apabila hasil pengujian di kotak pasir E2B membuktikan bahwa repositori baru dari Top 100 
GitHub tersebut memberikan peningkatan efisiensi atau akurasi yang terukur tanpa merusak 
pengujian regresi, modul refleksi pada Hermes Agent dan OpenClaw secara otomatis 
mengekstraksi langkah-langkah prosedural dari jejak eksekusi yang berhasil dan menyusunnya 
menjadi dokumen standar SKILL.md di dalam sistem berkas kognitif agen (bersanding dengan 
SOUL.md, USER.md, MEMORY.md, dan AGENTS.md) serta memperbarui buku besar 
.evolution/manifest.json. Pada tingkat integrasi kode, kerangka kerja Hugging Face Smolagents 
(CodeAgent yang menulis tindakan dalam bentuk kode Python langsung, bukan sekadar JSON) 
secara dinamis menghasilkan kelas pembungkus (*wrapper class* turunan Tool) yang 
menyamakan nama fungsi, tipe parameter masukan, dan skema keluaran dengan modul lama. 
Melalui mekanisme komposisi pipa keterampilan (|) pada OpenClaw dan pengaturan 
skills.write_approval: true pada Hermes Agent, ringkasan hasil benchmark dikirimkan ke ruang 
obrolan Telegram Admin untuk persetujuan satu klik (atau langsung dipromosikan secara otomatis 
untuk pembaruan minor non-destruktif), yang kemudian menerapkan *hot-patch* ke kontainer 
produksi dengan kecepatan iterasi hingga 37 kali lebih cepat dibandingkan pipa CI/CD tradisional.
```python
# Blueprint Daemon Python: Autonomous GitHub Top-100 MIT/Apache-2.0 Scout & E2B Evaluator
import os
import subprocess
import httpx
from typing import Dict, Any, List


## Halaman 114

class AutonomousRepoEvolutionEngine:
    """
    Mesin adaptasi otomatis harian yang memindai repo Top 100 berlisensi MIT/Apache-2.0,
    menguji keamanan bobot/relay, dan menjalankan benchmark terisolasi sebelum promosi.
    """
    def __init__(self):
        self.allowed_licenses = {"mit", "apache-2.0"}
        self.github_api = "https://api.github.com/search/repositories"
        self.skills_dir = os.path.expanduser("~/.openclaw/workspace/.evolution/skills")
        os.makedirs(self.skills_dir, exist_ok=True)
    async def discover_trending_permissive_repos(self, topic: str = "ai-agents", limit: int = 10) -> 
List[Dict[str, Any]]:
        query = f"topic:{topic} license:mit license:apache-2.0 stars:>500"
        params = {"q": query, "sort": "updated", "order": "desc", "per_page": limit}
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(self.github_api, params=params)
            resp.raise_for_status()
            items = resp.json().get("items", [])
            return [
                {
                    "full_name": repo["full_name"],
                    "clone_url": repo["clone_url"],
                    "stars": repo["stargazers_count"],
                    "license": (repo.get("license") or {}).get("key", "").lower(),
                    "description": repo.get("description", "")
                }
                for repo in items
                if (repo.get("license") or {}).get("key", "").lower() in self.allowed_licenses
            ]
    @staticmethod
    def enforce_modelscan_gate(artifact_path: str) -> bool:


## Halaman 115

        if artifact_path.endswith((".safetensors", ".gguf")):
            return True
        proc = subprocess.run(["modelscan", "-p", artifact_path], capture_output=True, text=True, 
check=False)
        return proc.returncode == 0
    def synthesize_hermes_skill_markdown(self, repo_info: Dict[str, Any], benchmark_gain_pct: 
float) -> str:
        slug = repo_info["full_name"].replace("/", "_")
        skill_path = os.path.join(self.skills_dir, f"{slug}_SKILL.md")
        content = (
            f"# SKILL: {repo_info['full_name']}\n"
            f"- **License Verified**: {repo_info['license'].upper()}\n"
            f"- **Benchmark Improvement**: +{benchmark_gain_pct:.1f}% vs Baseline\n"
            f"- **Repository**: {repo_info['clone_url']}\n\n"
            f"## Automated Execution Procedure\n"
            f"1. Instantiate isolated runner via E2B / Docker.\n"
            f"2. Invoke standardized Python wrapper for `{repo_info['full_name']}`.\n"
            f"3. Fallback to legacy module if latency exceeds 2000ms.\n"
        )
        with open(skill_path, "w", encoding="utf-8") as f:
            f.write(content)
        return skill_path
```

<!-- [ID:02_CORE_AI_S033] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: OBJEK UTAMA, PENCAHAYAAN -->
## Halaman 411

<div class="pill disabled" data-ups="VID" id="vid-ups-pill" onclick="selectExclusive(this,'upscale','Pertajam 
</div>
<div class="label">7. Upload Foto Referensi (Untuk Foto Jadi Video / Produk)</div>
<div class="upload-box" id="upload-container">
<input type="file" accept="image/*" onchange="previewRef(event)">
<div id="up-txt" style="font-size:12px">📸 <b>Sentuh untuk Upload Foto Referensi</b><br><span style="font-size
<img id="ref-preview" alt="Ref">
</div>
<div class="label">8. Tulis Deskripsi Karya Anda</div>
<textarea id="prompt-in" placeholder="Contoh: Botol parfum mewah di atas batu hitam dengan percikan air emas..
<button class="btn-exec" id="btn-go" onclick="runGenerate()">🚀 BUAT KARYA SEKARANG (KIRIM KE CHAT)</button>
<div id="toast"></div>
</div>
<div id="tab-guide" class="tab-section">
<div class="legal-card"><h3>🪄 Rumus Mudah Membuat Prompt bagi Pemula</h3>
<p>Gunakan rumus 3 langkah: <b>[Objek Utama] + [Gerakan/Aktivitas] + [Pencahayaan]</b>.<br>
• Untuk <b>Foto Jadi Video</b>: Pilih tombol <b>📸 Foto Jadi Video</b>, unggah foto Anda, lalu pilih preset <b
<div class="legal-card"><h3>📡 Akses Cepat ke 6 Kamar Topik Komunitas</h3><div id="community-links-box"></div>
</div>
<div id="tab-legal" class="tab-section">
<div class="legal-card"><h3>⚖️ Ketentuan Layanan & Kebijakan Watermark</h3>
<p>• Karya dari <b>Koin Gratisan/Bonus</b> menyertakan tanda air komunitas.<br>• Seluruh karya yang dibuat men
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
let st={init_data:"",user_id:0,username:"Kreator",modality:"IMAGE",engine:"Seedream 4.5",ratio:"9:16",duration
if(tg){tg.expand();st.init_data=tg.initData||"";const u=tg.initDataUnsafe?.user;if(u){st.user_id=u.id;st.usern
fetch("/api/public/community-links").then(r=>r.json()).then(d=>{if(d.links)document.getElementById("community-
function openTab(el,id){document.querySelectorAll(".nav-btn").forEach(b=>b.classList.remove("active"));documen
function selectExclusive(el,g,v){if(el.classList.contains("disabled"))return;const p=el.closest(`[data-group='
function applyAwamPreset(el,m){selectExclusive(el,"preset",m);st.preset_mod=m}
function setMod(el,m){
 selectExclusive(el,"modality",m);
 const isVid=(m==="VIDEO"||m==="IMG2VID");
 document.querySelectorAll("#duration-row .pill").forEach(p=>p.classList.toggle("disabled",!isVid));
 const imgUps=document.querySelectorAll("#upscale-row [data-ups='IMG']"),vidUps=document.getElementById("vid-
 document.querySelectorAll("#upscale-row .pill").forEach(p=>p.classList.remove("active"));
 if(isVid){imgUps.forEach(p=>p.classList.add("disabled"));vidUps.classList.remove("disabled");vidUps.classLis
 else{imgUps.forEach(p=>p.classList.remove("disabled"));vidUps.classList.add("disabled");imgUps[0].classList.
 document.getElementById("preset-img-row").style.display=isVid?"none":"flex";
 document.getElementById("preset-vid-row").style.display=isVid?"flex":"none";
 st.preset_mod=isVid?"Smooth cinematic camera zoom-in, dynamic lighting, 60fps":"Commercial product catalog p
 document.getElementById("upload-container").classList.toggle("highlight-upload",m==="IMG2VID");
 let fv=null;
 document.querySelectorAll("#engine-grid .card").forEach(c=>{const sh=isVid?(c.getAttribute("data-type")==="V
 if(fv){fv.classList.add("active");st.engine=fv.querySelector("h4").innerText.replace(/^[^\w]+/,"").trim()}
}
function setEng(el,e){document.querySelectorAll("#engine-grid .card").forEach(c=>c.classList.remove("active"))
function previewRef(ev){const f=ev.target.files[0];if(!f)return;const rd=new FileReader();rd.onload=e=>{const 
async function runGenerate(){
 const btn=document.getElementById("btn-go"),toast=document.getElementById("toast"),rawIn=document.getElement
 const finalPrompt=rawIn?`${rawIn}, ${st.preset_mod}`:st.preset_mod;
 btn.disabled=true;btn.innerText="⏳ [25%] MENYIAPKAN KLASTER GPU...";
 setTimeout(()=>{if(btn.disabled)btn.innerText="⚡ [65%] MERENDER KARYA 4K..."},900);
 try{const r=await fetch("/api/webapp/execute",{method:"POST",headers:{"Content-Type":"application/json"},bod
 catch(e){toast.style.display="block";toast.innerText="✅ Permintaan diterima! Cek ruang chat bot Telegram An
 finally{btn.disabled=false;btn.innerText="🚀 BUAT KARYA SEKARANG (KIRIM KE CHAT)"}
}
</script></body></html>"""
def render_freedom_web_portal_html() -> str:
   brand = RUNTIME_CONFIG.get("WEB_BRAND_NAME") or "AetherFree AI Studio"
   return f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"
<title>{brand} — Unrestricted Frontier AI & Creative Freedom Platform</title>



<!-- [ID:02_CORE_AI_S034] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
## Halaman 639

PRAGMA synchronous = NORMAL;​
PRAGMA busy_timeout = 10000;​
PRAGMA temp_store = MEMORY;​
PRAGMA mmap_size = 268435456; -- 256 MB Memory-Mapped I/O​
​
-- 1. TABEL PENGGUNA UTAMA (DENGAN HARD-CAP KOIN BONUS & LOCK PPP 
ZONE)​
CREATE TABLE IF NOT EXISTS users (​
    internal_user_id INTEGER PRIMARY KEY AUTOINCREMENT,​
    koin_utama INTEGER NOT NULL DEFAULT 0 CHECK (koin_utama >= 0),​
    koin_bonus INTEGER NOT NULL DEFAULT 4 CHECK (koin_bonus >= 0 AND 
koin_bonus <= 25),​
    has_topped_up INTEGER NOT NULL DEFAULT 0,​
    ppp_zone INTEGER NOT NULL DEFAULT 3, -- 1: Global Premium, 2: 
Emerging, 3: Indonesia QRIS​
    referred_by INTEGER,​
    last_claim_date TEXT,​
    vouchers_minted_today INTEGER NOT NULL DEFAULT 0,​
    created_at INTEGER NOT NULL​
);​
​
-- 2. TABEL IDENTITAS LINTAS PLATFORM ("1 OTAK, 3 PINTU": TELEGRAM, 
WA, FB)​
CREATE TABLE IF NOT EXISTS platform_identities (​
    identity_id INTEGER PRIMARY KEY AUTOINCREMENT,​
    internal_user_id INTEGER NOT NULL,​
    platform_type TEXT NOT NULL CHECK (platform_type IN ('tg', 'wa', 
'fb')),​
    external_id TEXT NOT NULL UNIQUE,​
    language_code TEXT DEFAULT 'id',​
    device_fp_hash TEXT,​
    FOREIGN KEY (internal_user_id) REFERENCES users(internal_user_id)​
);​
​
-- 3. TABEL BUKU BESAR AKUNTANSI APPEND-ONLY (ANTI DOUBLE-CREDIT 
WEBHOOK)​
CREATE TABLE IF NOT EXISTS wallet_ledger (​
    tx_id INTEGER PRIMARY KEY AUTOINCREMENT,​
    internal_user_id INTEGER NOT NULL,​
    wallet_type TEXT NOT NULL CHECK (wallet_type IN ('UTAMA', 
'BONUS')),​
    delta_amount INTEGER NOT NULL,​
    balance_after INTEGER NOT NULL,​
    tx_type TEXT NOT NULL, -- 'TOPUP_QRIS', 'TOPUP_STARS', 
'ESCROW_HOLD', 'REFUND', 'DAILY_CLAIM', 'VOUCHER_MINT'​
    idempotency_key TEXT NOT NULL UNIQUE,​
    created_at INTEGER NOT NULL​
);​


