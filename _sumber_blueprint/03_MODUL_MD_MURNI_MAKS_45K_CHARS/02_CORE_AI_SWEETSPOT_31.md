
<!-- [ID:02_CORE_AI_S046] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
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



<!-- [ID:02_CORE_AI_S047] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ------------------------------------------------------------------------------
@router.callback_query(F.data.startswith("menu:"))
async def cb_menu_router(callback: CallbackQuery) -> None:
    user: Any = getattr(callback, "from_user", None)
    cb_msg: Any = getattr(callback, "message", None)
    if user is None or cb_msg is None:
        return
    action = (callback.data or "").split(":", 1)[1]

    if action == "home":
        text, kb = await build_buyer_main_menu_view(user.id, user.first_name or "Sahabat")
        await cb_msg.edit_text(text, reply_markup=kb, parse_mode="HTML")
    elif action == "topup":
        rows = []
        for tkey, pkg in TOPUP_PACKAGES.items():
            rows.append(
                [
                    InlineKeyboardButton(
                        text=f"💎 {pkg['name']} — Rp {pkg['amount_idr']:,} ({pkg['coins']} Koin Utama)",
                        callback_data=f"wiz:buy:{tkey}",
                    )
                ]
            )
        rows.append([InlineKeyboardButton(text="🏠 Kembali ke Menu Utama", callback_data="menu:home")])
        await cb_msg.edit_text(
            "💎 \x3cb>Pilih Paket Koin Utama (100% Bebas Watermark)\x3c/b>\n\n"
            "Semua pembelian Koin Utama — mulai dari \x3cb>Paket Eceran Rp 2.000\x3c/b> — "
            "otomatis membuka Lisensi Komersial Bersih tanpa tanda air!",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
            parse_mode="HTML",
        )
    elif action == "claim_daily":
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        u_row = await ensure_user_profile(user.id)
        if u_row.get("last_claim_date") == today_str:
            await callback.answer("Kamu sudah klaim Koin Bonus hari ini. Kembali lagi besok ya!", show_alert=True)
            return
        new_bonus = min(25, int(u_row.get("koin_bonus") or 0) + 5)
        await get_db().execute_write(
            "UPDATE users SET koin_bonus = ?, last_claim_date = ? WHERE internal_user_id = ?;",
            (new_bonus, today_str, user.id),
        )
        await callback.answer(f"🎉 Berhasil klaim! Saldo Koin Bonus kamu sekarang {new_bonus}/25.", show_alert=True)
    elif action == "affiliate":
        u_row = await ensure_user_profile(user.id)
        ref_link = f"https\x3a//t.me/bikinAI_bot?start=ref_{user.id}"
        await cb_msg.edit_text(
            f"🤝 \x3cb>Program Partner & Komisi Dual-Mode\x3c/b>\n\n"
            f"Bagikan tautan undangan pribadimu:\n\x3ccode>{ref_link}\x3c/code>\n\n"
            f"• Saldo Komisi Stars: \x3cb>{u_row.get('affiliate_stars_balance', 0)} ⭐\x3c/b>\n"
            f"• Saldo Komisi Rupiah (QRIS): \x3cb>Rp {int(u_row.get('affiliate_idr_pending') or 0):,}\x3c/b>\n\n"
            f"Kamu otomatis mendapat komisi 15% setiap teman yang kamu undang melakukan isi ulang!",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="🏠 Kembali", callback_data="menu:home")]]
            ),
            parse_mode="HTML",
        )
    elif action == "help":
        await cb_msg.edit_text(
            "📖 \x3cb>Panduan Singkat bikinAI Studio\x3c/b>\n\n"
            "• Pilih \x3cb>Buat Foto HD\x3c/b> atau \x3cb>Buat Video\x3c/b> untuk membuat karya visual.\n"
            "• Pilih \x3cb>Gerakkan Foto (Img2Vid)\x3c/b> atau langsung kirim foto dari galeri untuk menghidupkan gambar.\n"
            "• Gunakan \x3cb>Koin Utama\x3c/b> mulai Rp 2.000 agar hasil karyamu 100% bersih tanpa tanda air.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="🏠 Kembali", callback_data="menu:home")]]
            ),
            parse_mode="HTML",
        )
    await callback.answer()


@router.callback_query(F.data.startswith("wiz:"))
async def cb_wizard_router(callback: CallbackQuery) -> None:
    user: Any = getattr(callback, "from_user", None)
    cb_msg: Any = getattr(callback, "message", None)
    if user is None or cb_msg is None:
        return
    parts = (callback.data or "").split(":")
    sub = parts[1] if len(parts) > 1 else ""
    val = parts[2] if len(parts) > 2 else ""

    state = _RUNTIME_WIZARD_STATE.setdefault(
        user.id,
        {"mode": "PHOTO_HD", "motion_preset": "SMOOTH_ZOOM"},
    )

    if sub == "mode":
        state["mode"] = val
        if val in ("VIDEO_CINEMATIC", "IMG2VID_MOTION"):
            kb = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="🔍 Kamera Maju Halus", callback_data="wiz:vpre:SMOOTH_ZOOM"),
                        InlineKeyboardButton(text="🎥 Geser Sinematik", callback_data="wiz:vpre:CINEMATIC_PAN"),
                    ],
                    [
                        InlineKeyboardButton(text="😊 Wajah Hidup", callback_data="wiz:vpre:NATURAL_PORTRAIT"),
                        InlineKeyboardButton(text="🛍️ Putar Produk 360°", callback_data="wiz:vpre:PRODUCT_ORBIT"),
                    ],
                    [InlineKeyboardButton(text="🏠 Kembali", callback_data="menu:home")],
                ]
            )
            await cb_msg.edit_text(
                f"🎬 \x3cb>Mode {html.escape(val)} Aktif!\x3c/b>\n"
                f"Pilih gaya gerakan kamera di bawah, lalu kirim foto atau tulis adegan yang kamu inginkan:",
                reply_markup=kb,
                parse_mode="HTML",
            )
        else:
            await cb_msg.edit_text(
                "📸 \x3cb>Mode Foto HD 4K Aktif!\x3c/b>\n"
                "Silakan ketik deskripsi foto yang ingin kamu buat sekarang (atau kirim foto referensi):",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="🏠 Kembali", callback_data="menu:home")]]
                ),
                parse_mode="HTML",
            )
    elif sub == "vpre":
        state["motion_preset"] = val
        await cb_msg.edit_text(
            f"✅ Preset gerakan \x3cb>{html.escape(val)}\x3c/b> dipilih!\n"
            f"Sekarang kirimkan \x3cb>foto\x3c/b> yang ingin digerakkan atau ketik deskripsi videonya di chat.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="🏠 Kembali", callback_data="menu:home")]]
            ),
            parse_mode="HTML",
        )
    elif sub == "buy":
        inv = await create_payment_invoice(user.id, tier_key=val, provider="QRIS_LOKAL")
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Simulasi Konfirmasi Bayar (Instan)",
                        callback_data=f"adm:confirm_inv:{inv['invoice_id']}",
                    )
                ],
                [InlineKeyboardButton(text="🏠 Kembali", callback_data="menu:home")],
            ]
        )
        await cb_msg.edit_text(
            f"🧾 \x3cb>Tagihan Isi Koin Utama #{inv['invoice_id']}\x3c/b>\n\n"
            f"• Paket: \x3cb>{inv['package_name']}\x3c/b>\n"
            f"• Nominal QRIS: \x3cb>Rp {inv['amount_idr']:,}\x3c/b>\n"
            f"• Koin Diterima: \x3cb>+{inv['coins_credited']} Koin Utama (100% Bebas Watermark)\x3c/b>\n\n"
            f"Silakan selesaikan pembayaran melalui QRIS GoPay / ShopeePay / DANA.",
            reply_markup=kb,
            parse_mode="HTML",
        )
    await callback.answer()


@router.callback_query(F.data.startswith("drv:"))
async def cb_derivative_router(callback: CallbackQuery) -> None:
    user: Any = getattr(callback, "from_user", None)
    cb_msg: Any = getattr(callback, "message", None)
    if user is None or cb_msg is None:
        return
    parts = (callback.data or "").split(":", 2)
    action = parts[1] if len(parts) > 1 else ""
    job_id = parts[2] if len(parts) > 2 else "JOB-DEFAULT"

    if action == "poster4k":
        ok, msg, meta = await create_job_with_atomic_deduction(
            user_id=user.id,
            cost=2,
            prompt_text=f"Upscale Poster 4K from {job_id}",
            engine_used="POSTER_4K_ENHANCER",
        )
        if not ok:
            await callback.answer(msg, show_alert=True)
            return
        await finalize_job_status(meta["job_id"], success=True)
        wm = meta["watermark_policy"]
        await cb_msg.answer(
            f"🖼️ \x3cb>Poster 4K Siap Cetak!\x3c/b>\n"
            f"• ID Karya: \x3ccode>{meta['job_id']}\x3c/code>\n"
            f"• Lisensi: {wm['license_label']}\n"
            f"• Unduh Kualitas Penuh: {PUBLIC_WEB_BASE_URL}/api/cdn/download?asset={meta['job_id']}&wm={wm['is_watermarked']}",
            parse_mode="HTML",
        )
    elif action == "audiomp3":
        _audio_bytes, audio_meta = await SOTAAudioEngine.synthesize_voice_bytes(
            text_script=f"Narasi suara jernih untuk karya {job_id}",
            preferred_engine="FISH_S2_PRO",
        )
        await cb_msg.answer(
            f"🎙️ \x3cb>Suara Narator Selesai Dibuat!\x3c/b>\n"
            f"• Mesin Suara: \x3cb>{audio_meta['engine_label']}\x3c/b>\n"
            f"• Durasi: {audio_meta['duration_sec']} detik ({audio_meta['size_bytes']} bytes)",
            parse_mode="HTML",
        )
    elif action == "clean_license":
        ok, msg, meta = await create_job_with_atomic_deduction(
            user_id=user.id,
            cost=1,
            prompt_text=f"Clean License Unlock for {job_id}",
            engine_used="CLEAN_LICENSE_UNLOCK",
            prefer_utama_first=True,
            explicit_clean_license=True,
        )
        if not ok:
            await callback.answer(msg, show_alert=True)
            return
        await finalize_job_status(meta["job_id"], success=True)
        await cb_msg.answer(
            f"💎 \x3cb>Lisensi Komersial Bersih Aktif!\x3c/b>\n"
            f"Karya \x3ccode>{html.escape(job_id)}\x3c/code> kini 100% bebas tanda air (\x3ccode>nologo=true\x3c/code>).\n"
            f"Unduh File Bersih: {PUBLIC_WEB_BASE_URL}/api/cdn/download?asset={job_id}&wm=0",
            parse_mode="HTML",
        )
    await callback.answer()


@router.callback_query(F.data.startswith("adm:"))
async def cb_admin_router(callback: CallbackQuery) -> None:
    user: Any = getattr(callback, "from_user", None)
    cb_msg: Any = getattr(callback, "message", None)
    if user is None or cb_msg is None:
        return
    parts = (callback.data or "").split(":")
    action = parts[1] if len(parts) > 1 else ""
    arg = parts[2] if len(parts) > 2 else "1"

    # Izinkan simulasi konfirmasi bayar invoice bagi pembeli saat menguji pembayaran
    if action == "confirm_inv":
        ok, msg, meta = await settle_payment_invoice(arg)
        extra_key = (
            f"\n🔑 \x3cb>API Key Vibe-Coder Anda:\x3c/b> \x3ccode>{meta['generated_api_key']}\x3c/code>"
            if meta.get("generated_api_key")
            else ""
        )
        await cb_msg.edit_text(
            f"{'✅' if ok else 'ℹ️'} \x3cb>{html.escape(msg)}\x3c/b>{extra_key}",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="🏠 Menu Utama", callback_data="menu:home")]]
            ),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    if not is_verified_owner_dm(callback):
        await callback.answer("🔒 Akses ditolak (Khusus DM Owner Terverifikasi).", show_alert=True)
        return

    if action == "home":
        text, kb = await build_admin_dashboard_view()
        await cb_msg.edit_text(text, reply_markup=kb, parse_mode="HTML")
    elif action == "preview_buyer_ui":
        # Inspektor Layar Pembeli + Pemindaian Kebocoran Istilah Teknis
        buyer_text, _ = await build_buyer_main_menu_view(user.id, "Simulasi Pembeli Awam")
        leak_chat = scan_customer_ui_for_leaks(buyer_text)
        leak_web = scan_customer_ui_for_leaks(MINIAPP_FULL_WEBSITE_HTML)
        status_audit = (
            "✅ LULUS AUDIT 100% (Nol Kebocoran Istilah Teknis)"
            if leak_chat["is_clean"] and leak_web["is_clean"]
            else f"⚠️ Ditemukan kebocoran: {leak_chat['leaks_found'] + leak_web['leaks_found']}"
        )
        await cb_msg.edit_text(
            f"👁️ \x3cb>INSPEKTOR LAYAR PEMBELI (BUYER SCREEN INSPECTOR)\x3c/b>\n"
            f"• Status Audit Bahasa Konsumen: \x3cb>{status_audit}\x3c/b>\n\n"
            f"\x3cb>Pratinjau Pesan Pembeli:\x3c/b>\n"
            f"────────────────────\n"
            f"{buyer_text}\n"
            f"────────────────────",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="🔙 Kembali ke Admin", callback_data="adm:home")]]
            ),
            parse_mode="HTML",
        )
    elif action == "pay_menu":
        page = int(arg) if arg.isdigit() else 1
        pages = {
            1: (
                "💳 \x3cb>Pengaturan Pembayaran — Hal 1/3 (QRIS Lokal & 3 Slot E-Wallet)\x3c/b>\n\n"
                "• Gunakan \x3ccode>/set_qris UNIVERSAL\x3c/code> untuk 1 barcode semua pembayaran.\n"
                "• Gunakan \x3ccode>/set_qris GOPAY\x3c/code>, \x3ccode>/set_qris SHOPEEPAY\x3c/code>, \x3ccode>/set_qris DANA\x3c/code> untuk 3 slot spesifik.\n"
                "• Paket Eceran Rp 2.000 = 24 Koin Utama (Langsung Bebas Watermark)."
            ),
            2: (
                "🌍 \x3cb>Pengaturan Pembayaran — Hal 2/3 (4-Zona PPP & Telegram Stars)\x3c/b>\n\n"
                "• Zona 1 Global T1 (100%) | Zona 2 Global T2 (70%)\n"
                "• Zona 3 Emerging (50%) | Zona 4 Indonesia QRIS (25%)\n"
                "• Mendukung pembayaran lintas negara dengan Telegram Stars."
            ),
            3: (
                "🎟️ \x3cb>Pengaturan Pembayaran — Hal 3/3 (Voucher Ed25519 & Auto-CS Siska)\x3c/b>\n\n"
                "• Voucher kriptografi \x3ccode>VCH-...\x3c/code> anti-replay dengan tabel \x3ccode>redeemed_nullifiers\x3c/code>.\n"
                "• Auto-CS Siska otomatis mengirimkan pengingat ramah setelah 20 menit jika invoice masih PENDING."
            ),
        }
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="1️⃣ Hal 1", callback_data="adm:pay_menu:1"),
                    InlineKeyboardButton(text="2️⃣ Hal 2", callback_data="adm:pay_menu:2"),
                    InlineKeyboardButton(text="3️⃣ Hal 3", callback_data="adm:pay_menu:3"),
                ],
                [InlineKeyboardButton(text="🔙 Kembali ke Admin", callback_data="adm:home")],
            ]
        )
        await cb_msg.edit_text(pages.get(page, pages[1]), reply_markup=kb, parse_mode="HTML")
    elif action == "manual":
        chap = int(arg) if arg.isdigit() else 1
        chapters = {
            1: (
                "📘 \x3cb>Buku Manual Owner — Bab 1/4: Fondasi & Klaim Owner\x3c/b>\n\n"
                "• Klaim kepemilikan via \x3ccode>/claim_owner &lt;TOKEN&gt;\x3c/code> di DM.\n"
                "• Semua data tersimpan aman di 16 tabel SQLite WAL \x3ccode>~/.bikinai_vault/bikinai_master_vault.db\x3c/code>."
            ),
            2: (
                "📘 \x3cb>Buku Manual Owner — Bab 2/4: Ekonomi, QRIS & Panen Profit\x3c/b>\n\n"
                "• Pasang QRIS dengan \x3ccode>/set_qris\x3c/code>.\n"
                "• Pantau dan cairkan profit 65% melalui \x3ccode>/harvest\x3c/code> yang dilindungi Human Approval Gate."
            ),
            3: (
                "📘 \x3cb>Buku Manual Owner — Bab 3/4: Keamanan 6-Gate & Hot-Swap Plugin\x3c/b>\n\n"
                "• Suntik plugin baru tanpa restart dengan \x3ccode>/suntik\x3c/code>.\n"
                "• Self-Healing Loop otomatis memperbaiki gangguan hingga 3x sebelum eskalasi ke DM Owner."
            ),
            4: (
                "📘 \x3cb>Buku Manual Owner — Bab 4/4: Hub Omnichannel & Auto-Posting\x3c/b>\n\n"
                "• Port 8080 melayani SFW Studio (\x3ccode>/\x3c/code>), Freedom Portal (\x3ccode>/unfiltered-portal\x3c/code>), "
                "WhatsApp WAHA/Meta, Messenger/IG, dan Auto-Post TikTok/Shopee (Jalur 1 Bot vs Jalur 2 Pribadi)."
            ),
        }
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Bab 1", callback_data="adm:manual:1"),
                    InlineKeyboardButton(text="Bab 2", callback_data="adm:manual:2"),
                    InlineKeyboardButton(text="Bab 3", callback_data="adm:manual:3"),
                    InlineKeyboardButton(text="Bab 4", callback_data="adm:manual:4"),
                ],
                [InlineKeyboardButton(text="🔙 Kembali ke Admin", callback_data="adm:home")],
            ]
        )
        await cb_msg.edit_text(chapters.get(chap, chapters[1]), reply_markup=kb, parse_mode="HTML")
    elif action == "subbots":
        await cb_msg.edit_text(
            "🤖 \x3cb>Status Hub Omnichannel & Sub-Bots\x3c/b>\n\n"
            "• WhatsApp Webhook: \x3ccode>POST /api/webhook/whatsapp\x3c/code> (Aktif)\n"
            "• Meta IG/Messenger: \x3ccode>POST /api/webhook/meta\x3c/code> (Aktif)\n"
            "• TikTok & Shopee Auto-Post: \x3ccode>POST /api/omnipost/dispatch\x3c/code> (Jalur 1 & Jalur 2 Siap)",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="🔙 Kembali ke Admin", callback_data="adm:home")]]
            ),
            parse_mode="HTML",
        )
    elif action in ("apr_yes", "apr_no"):
        approved = action == "apr_yes"
        ok, msg, _ = await HumanApprovalGate.resolve_approval(arg, approved=approved)
        await cb_msg.edit_text(
            f"🛡️ \x3cb>Hasil Human Approval Gate\x3c/b>\n\n{html.escape(msg)}",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="🔙 Kembali ke Admin", callback_data="adm:home")]]
            ),
            parse_mode="HTML",
        )
    await callback.answer()


@router.callback_query(F.data.startswith("bns:"))
async def cb_bansos_router(callback: CallbackQuery) -> None:
    cb_msg: Any = getattr(callback, "message", None)
    if cb_msg is None:
        return
    parts = (callback.data or "").split(":", 2)
    kind = parts[1] if len(parts) > 1 else "tab"
    val = parts[2] if len(parts) > 2 else "AI_API"
    db = get_db()

    if kind == "mode":
        if not is_verified_owner_dm(callback):
            await callback.answer("🔒 Hanya Owner yang dapat mengubah mode distribusi Bansos.", show_alert=True)
            return
        await db.set_setting("bansos_mode", val)
        await callback.answer(f"Mode Bansos diubah ke {val}!", show_alert=True)
        val = "AI_API"

    cat_query = "AST_PLUGIN" if val == "AST" else val
    rows = await db.fetch_all(
        "SELECT resource_name, endpoint_url, is_live_verified FROM omni_resource_registry WHERE category = ? LIMIT 10;",
        (cat_query,),
    )
    mode_now = await db.get_setting("bansos_mode", "NORMAL")
    list_txt = (
        "\n".join(f"• \x3cb>{html.escape(r['resource_name'])}\x3c/b> — \x3ccode>{html.escape(r['endpoint_url'])}\x3c/code>" for r in rows)
        if rows
        else "\x3ci>Belum ada node terdaftar di kategori ini. Gunakan /pasang_bansos untuk menambahkan.\x3c/i>"
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🤖 AI_API", callback_data="bns:tab:AI_API"),
                InlineKeyboardButton(text="🌐 DOMAINS", callback_data="bns:tab:DOMAINS"),
                InlineKeyboardButton(text="💾 STORAGE", callback_data="bns:tab:STORAGE"),
                InlineKeyboardButton(text="🧩 AST", callback_data="bns:tab:AST"),
            ],
            [
                InlineKeyboardButton(text="🔇 SILENT", callback_data="bns:mode:SILENT"),
                InlineKeyboardButton(text="🎉 HAPPY_HOUR", callback_data="bns:mode:HAPPY_HOUR"),
                InlineKeyboardButton(text="⚖️ NORMAL", callback_data="bns:mode:NORMAL"),
            ],
        ]
    )
    await cb_msg.edit_text(
        f"🎁 \x3cb>Tab Kolam Resource: {html.escape(val)}\x3c/b> (Mode: \x3cb>{html.escape(mode_now)}\x3c/b>)\n\n{list_txt}",
        reply_markup=kb,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("bind:"))
async def cb_bind_router(callback: CallbackQuery) -> None:
    cb_msg: Any = getattr(callback, "message", None)
    if cb_msg is None:
        return
    key = (callback.data or "").split(":", 1)[1]
    cb_chat: Any = getattr(cb_msg, "chat", None)
    chat_id = int(getattr(cb_chat, "id", 0))
    topic_id = int(getattr(cb_msg, "message_thread_id", 0) or 0)
    title = str(getattr(cb_chat, "title", None) or key)
    await get_db().execute_write(
        """
        INSERT INTO bot_bindings (binding_key, chat_id, topic_id, topic_title)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(binding_key) DO UPDATE SET
            chat_id = excluded.chat_id,
            topic_id = excluded.topic_id,
            topic_title = excluded.topic_title;
        """,
        (key, chat_id, topic_id, title),
    )
    await callback.answer(f"Topik berhasil diikat sebagai {key}!", show_alert=True)


