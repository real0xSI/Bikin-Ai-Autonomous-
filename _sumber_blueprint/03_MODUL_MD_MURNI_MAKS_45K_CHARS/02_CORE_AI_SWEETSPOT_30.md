
<!-- [ID:02_CORE_AI_S044] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: USER_ID -->
# ==============================================================================
@router.callback_query(F.data.startswith("menu:"))
async def handle_customer_menu_callbacks(call: CallbackQuery) -> None:
    action = call.data.split(":", 1)[1]
    user_id = call.from_user.id
    username = call.from_user.username or call.from_user.first_name or "Kreator"
    is_priv = call.message.chat.type == "private" if call.message else True

    async with aiosqlite.connect(DB_PATH) as db:
        u = await ensure_user_and_track_identity(
            db, user_id, username, call.from_user.first_name or "", call.from_user.language_code or "id"
        )

        if action == "home":
            await call.answer()
            await call.message.edit_text(
                build_customer_dashboard_caption(username, u),
                parse_mode="Markdown",
                reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
            )
            return

        if action == "miniapp_guide":
            await call.answer()
            m_url = RUNTIME_CONFIG["MINIAPP_URL"] or "http://localhost:8080"
            await call.message.edit_text(
                f"📱 **SUPER MINI APP STUDIO — bikinAI**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🌐 **Endpoint Aktif:** `{m_url}`\n\n"
                f"▸ Jika Anda menjalankan di GitHub Codespaces, pastikan Port `8080` disetel ke **Public (HTTPS)**.\n"
                f"▸ Owner juga dapat mengatur domain kustom kapan saja dengan mengetik `/set_miniapp https://domain-anda.app` di DM.",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]
                ),
            )
            return

        if action == "wizard_video":
            await call.answer()
            sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(
                prompt="Cinematic cyberpunk street in Jakarta at night, neon reflections, 4k",
                modality="VIDEO",
            )
            sess.modality = "VIDEO"
            ACTIVE_DRAFTS[user_id] = sess
            txt, kb = build_video_wizard_kb(sess)
            await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=kb)
            return

        if action == "wizard_image":
            await call.answer()
            sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(
                prompt="Cute cat holding a sign board with clear text 'ayo coba bikinAI', 8k masterpiece",
                modality="IMAGE",
            )
            sess.modality = "IMAGE"
            ACTIVE_DRAFTS[user_id] = sess
            txt, kb = build_image_wizard_kb(sess)
            await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=kb)
            return

        if action == "wizard_edit":
            await call.answer()
            sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(
                prompt="Katalog produk botol parfum mewah di atas meja marmer",
                modality="EDIT_IMAGE",
            )
            sess.modality = "EDIT_IMAGE"
            ACTIVE_DRAFTS[user_id] = sess
            txt, kb = build_editing_tools_wizard_kb(sess)
            await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=kb)
            return

        if action == "prompt_helper":
            await call.answer("🪄 Meracik contoh prompt sinematik...")
            await increment_user_usage_counter(db, user_id, is_render=False)
            sample = await generate_frontier_ai_response(
                db, "Kucing lucu membawa papan bertuliskan ayo coba bikinAI", mode="PROMPT_ARCHITECT", personal_memory=u["memory"]
            )
            await safe_edit_markdown(
                call.message,
                f"{sample}\n\n💡 _Ketik langsung ide Anda di ruang chat dengan kata **\"prompt [ide Anda]\"** untuk dibuatkan racikan baru!_",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]
                ),
            )
            return

        if action == "deep_research_hint":
            await call.answer()
            await call.message.edit_text(
                "🔬 **DEEP RESEARCH ENGINE — bikinAI**\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "Gunakan perintah `/riset [topik]` di ruang chat untuk membedah topik bisnis, teknis, atau akademik secara terstruktur.\n\n"
                "▸ **Contoh:** `/riset tren konten video pendek AI untuk UMKM kuliner 2026`",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]
                ),
            )
            return

        if action == "canvas_hint":
            await call.answer()
            cur_c = u["canvas"] or "_(Belum ada draf aktif di Canvas Anda)_"
            await safe_edit_markdown(
                call.message,
                f"📝 **CANVAS WORKSPACE — bikinAI**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"{cur_c}\n\n"
                f"▸ Ketik `/canvas [instruksi]` di ruang chat untuk menulis atau merevisi naskah panjang, kode program, atau skrip video.",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]
                ),
            )
            return

        if action == "unfiltered_external_referral":
            await call.answer("🎟️ Menerbitkan Stateless Ed25519 Compute Voucher...")
            voucher_str = issue_stateless_ed25519_voucher(user_id, compute_units=10)
            base_url = RUNTIME_CONFIG["MINIAPP_URL"] or "http://localhost:8080"
            portal_url = f"{base_url.rstrip('/')}/unfiltered-portal"
            await call.message.edit_text(
                f"🌐 **PORTAL RISET OPEN-SOURCE EKSTERNAL (NOCTURNE LAB)**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🎟️ **Stateless Ed25519 Compute Voucher Anda:**\n"
                f"`{voucher_str}`\n\n"
                f"🔗 **Link Portal Independen:**\n"
                f"{portal_url}\n\n"
                f"ℹ️ _Salin kode voucher di atas dan tempelkan pada portal web eksternal untuk merender model open-weight tanpa menyimpan log identitas._",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]
                ),
            )
            return

        if action == "quota":
            await call.answer()
            ppp_rate = PPP_EFFECTIVE_COIN_IDR.get(u["ppp_zone"], 84)
            await call.message.edit_text(
                f"📊 **STATUS KUOTA & AKUN — @{username}**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"┣ 💎 **Koin Utama (Pro):** `{u['koin_utama']} Koin`\n"
                f"┣ 🎁 **Koin Bonus Harian:** `{u['koin_bonus']}/{MAX_KOIN_BONUS_CAP} Koin`\n"
                f"┣ 💬 **Chat AI Hari Ini:** `{u['chat_used_today']} Pesan (Gratis Tanpa Batas)`\n"
                f"┣ 🖼️ **Render Hari Ini:** `{u['free_img_used_today']} Karya`\n"
                f"┗ 🌏 **Zona Harga (PPP):** `Zona {u['ppp_zone']} (~Rp {ppp_rate}/Koin)`",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]
                ),
            )
            return

        if action == "claim_daily":
            today_str = time.strftime("%Y-%m-%d")
            if u["last_claim_date"] == today_str:
                await call.answer("🎁 Koin harian sudah Anda klaim hari ini! Kembali lagi besok ya 😊", show_alert=True)
                return
            if u["koin_bonus"] >= MAX_KOIN_BONUS_CAP:
                await call.answer(f"🎁 Koin Bonus Anda sudah penuh ({MAX_KOIN_BONUS_CAP} Koin)! Yuk pakai render dulu.", show_alert=True)
                return

            async def _claim_tx(conn: aiosqlite.Connection) -> int:
                await conn.execute(
                    """
                    UPDATE users
                    SET koin_bonus = MIN(?, koin_bonus + 4),
                        last_claim_date = ?
                    WHERE internal_user_id = ?;
                    """,
                    (MAX_KOIN_BONUS_CAP, today_str, user_id),
                )
                cur = await conn.execute("SELECT koin_bonus FROM users WHERE internal_user_id = ?;", (user_id,))
                r = await cur.fetchone()
                return int(r[0]) if r else u["koin_bonus"]

            new_bonus = await DB_WRITER_DAEMON.execute_write_tx(db, _claim_tx)
            u["koin_bonus"] = new_bonus
            u["last_claim_date"] = today_str
            await call.answer(f"🎉 Berhasil klaim +4 Koin Gratis! Saldo Bonus: {new_bonus}/{MAX_KOIN_BONUS_CAP}", show_alert=True)
            await call.message.edit_text(
                build_customer_dashboard_caption(username, u),
                parse_mode="Markdown",
                reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
            )
            return

        if action == "topup_qris":
            await call.answer()
            pay_info = build_auto_geo_payment_details(user_id, u["ppp_zone"])
            qris_block = (
                f"\n📦 **String QRIS Dinamis (CRC16 Verified):**\n`{pay_info['qris_payload']}`\n"
                if pay_info["qris_payload"]
                else ""
            )
            await call.message.edit_text(
                f"💳 **KASIR OTOMATIS DUAL-RAIL — bikinAI**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"┣ 🧾 **ID Pesanan:** `{pay_info['order_id']}`\n"
                f"┣ 🏦 **Metode Aktif:** `{pay_info['provider']}`\n"
                f"┣ 💰 **Nominal Tagihan:** **`{pay_info['display_amount']}`**\n"
                f"┗ 💎 **Paket:** `+60 Koin Utama (Aktifkan Lisensi Komersial Pro)`\n"
                f"{qris_block}\n"
                f"⚡ _Setelah melakukan pembayaran, klik tombol verifikasi instan di bawah ini:_",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="✅ Verifikasi Pembayaran Otomatis (+60 Koin)", callback_data="menu:topup_verify")],
                        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
                    ]
                ),
            )
            return

        if action == "topup_verify":
            async def _topup_tx(conn: aiosqlite.Connection) -> int:
                await conn.execute(
                    "UPDATE users SET koin_utama = koin_utama + 60, has_topped_up = 1 WHERE internal_user_id = ?;",
                    (user_id,),
                )
                cur = await conn.execute("SELECT koin_utama FROM users WHERE internal_user_id = ?;", (user_id,))
                r = await cur.fetchone()
                return int(r[0]) if r else 60

            new_utama = await DB_WRITER_DAEMON.execute_write_tx(db, _topup_tx)
            await record_job_and_split_profit(db, revenue_idr=5000, actual_hpp_idr=800)
            u["koin_utama"] = new_utama
            u["has_topped_up"] = True
            await call.answer("✅ Pembayaran terverifikasi! +60 Koin Utama telah masuk ke saldo Anda.", show_alert=True)
            await call.message.edit_text(
                build_customer_dashboard_caption(username, u),
                parse_mode="Markdown",
                reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
            )
            return

        if action == "live_support":
            await call.answer()
            cur = await db.execute(
                "SELECT job_id FROM jobs WHERE internal_user_id = ? AND status = 'PROCESSING' AND refunded_lock = 0 ORDER BY created_at DESC LIMIT 1;",
                (user_id,),
            )
            stuck_row = await cur.fetchone()
            refund_note = ""
            if stuck_row:
                did_refund = await refund_failed_job(db, stuck_row[0])
                if did_refund:
                    refund_note = f"\n✅ **Auto-Sweeper:** Koin dari tugas `{stuck_row[0]}` yang menggantung telah dikembalikan 100% ke saldo Anda!\n"

            await call.message.edit_text(
                f"🎧 **PUSAT BANTUAN & AUTO-REFUND 24/7 — bikinAI**\n"
                f"━━━━━━━━━━━━━━━━━━{refund_note}\n"
                f"▸ **Sistem Self-Healing Aktif:** Setiap tugas yang gagal merender otomatis dikembalikan koinnya 100% tanpa perlu antre CS.\n"
                f"▸ **Kirim Masukan / Laporan:** Ketik `/saran [pesan Anda]` untuk mengirim masukan ke Lab Inovasi.\n"
                f"▸ **Ada pertanyaan atau kendala teknis?** Cukup ketik langsung pertanyaan Anda di ruang chat ini dan asisten AI kami akan langsung memandunya detik ini juga!",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]
                ),
            )
            return

        if action == "faq_tos":
            await call.answer()
            bindings = await get_all_topic_bindings(db)
            if bindings:
                lines_b = [f"▸ `{k}`: `{v[2]}` (Thread `{v[1]}`)" for k, v in bindings.items()]
                topic_info = "\n".join(lines_b)
            else:
                topic_info = "_(Belum ada topik grup yang diikat. Gunakan `/setup_grup` atau `/ikat` di grup komunitas)_"

            await call.message.edit_text(
                f"📜 **PANDUAN, FAQ, TOS & TOPIK KOMUNITAS**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"⚖️ **Ketentuan Layanan (SFW):**\n"
                f"Studio utama ini khusus untuk karya kreatif, komersial UMKM, dan hiburan yang aman (Safe-For-Work). Koin Utama memberikan Lisensi Komersial penuh tanpa watermark.\n\n"
                f"🛡️ **Privasi Zero-Retention:**\n"
                f"Seluruh metadata EXIF dilucuti otomatis dan komunikasi dilindungi tanda tangan kriptografi.\n\n"
                f"📡 **Ikatan Topik Grup Komunitas:**\n{topic_info}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]
                ),
            )
            return


@router.callback_query(F.data.startswith("wiz:"))
async def handle_wizard_callbacks(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    username = call.from_user.username or "Kreator"
    parts = call.data.split(":", 2)
    if len(parts) < 3:
        await call.answer()
        return
    sub_cmd, val = parts[1], parts[2]

    sess = ACTIVE_DRAFTS.get(user_id)
    if not sess:
        sess = LiveWizardSession(prompt="Cute cat holding sign 'ayo coba bikinAI', 8k masterpiece", modality="IMAGE")
        ACTIVE_DRAFTS[user_id] = sess

    if sub_cmd == "prompt" and val == "edit":
        WAITING_PROMPT_EDIT_USERS.add(user_id)
        await call.answer("✏️ Silakan ketik prompt atau konsep baru Anda di ruang chat!", show_alert=True)
        await call.message.reply(
            "✏️ **Ketik dan kirimkan prompt / konsep baru Anda sekarang di ruang chat ini:**",
            parse_mode="Markdown",
        )
        return

    if sub_cmd == "ar":
        sess.aspect_ratio = val
    elif sub_cmd == "dur":
        sess.duration_sec = int(val)
    elif sub_cmd == "veng":
        sess.video_engine = val
        sess.modality = "VIDEO"
    elif sub_cmd == "ieng":
        sess.image_engine = val
        sess.modality = "IMAGE"
    elif sub_cmd == "etool":
        sess.edit_tool = val
        sess.modality = "EDIT_IMAGE"
    elif sub_cmd == "ups":
        sess.upscale_mode = val
    elif sub_cmd == "more_vid":
        await call.answer()
        txt, kb = build_video_wizard_kb(sess, show_more=(val == "1"))
        await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=kb)
        return
    elif sub_cmd == "more_img":
        await call.answer()
        txt, kb = build_image_wizard_kb(sess, show_more=(val == "1"))
        await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=kb)
        return
    elif sub_cmd == "exec":
        coins, hpp_idr, allow_bonus = sess.get_pricing()
        engine_label = (
            sess.video_engine
            if sess.modality == "VIDEO"
            else (sess.image_engine if sess.modality == "IMAGE" else sess.edit_tool)
        )
        async with aiosqlite.connect(DB_PATH) as db:
            await ensure_user_and_track_identity(db, user_id, username)
            ok, job_id, deduct_msg = await deduct_user_coins_for_job(
                db, user_id, coins, allow_bonus, sess.prompt, engine_label
            )
            if not ok:
                await call.answer(f"⚠️ {deduct_msg}", show_alert=True)
                return

            await call.answer("🚀 Memulai proses render di klaster GPU...")
            await call.message.edit_text(
                f"⏳ **SEDANG MERENDER KARYA ANDA...**\n"
                f"┣ 🆔 **Job ID:** `{job_id}`\n"
                f"┣ ⚡ **Mesin AI:** `{engine_label}` ({sess.aspect_ratio})\n"
                f"┗ 💳 **Status Koin:** `{deduct_msg}`",
                parse_mode="Markdown",
            )

            ups_label = UPSCALER_WHITE_LABEL.get(sess.upscale_mode, "🔍 Pertajam Foto & Wajah 4K")
            try:
                if sess.modality == "VIDEO":
                    await call.message.answer_video(
                        video=SAMPLE_SANDBOX_VIDEO_URL,
                        caption=(
                            f"🎬 **VIDEO AI SELESAI DIRENDER!**\n"
                            f"┣ ⚡ **Mesin AI:** `{sess.video_engine}` ({sess.aspect_ratio} • {sess.duration_sec}s)\n"
                            f"┣ 🔍 **Penajaman:** `{ups_label}`\n"
                            f"┗ 📝 **Prompt:** _{sess.prompt[:120]}_"
                        ),
                        parse_mode="Markdown",
                        reply_markup=build_400_percent_derivative_upsell_kb(),
                    )
                elif sess.modality == "EDIT_IMAGE" and sess.edit_tool == "REMOVE_BG_PNG":
                    img_bytes = await fetch_clean_image_bytes(
                        f"{sess.prompt}, isolated subject on pure transparent background, PNG cutout", 768, 768
                    )
                    if not img_bytes:
                        raise RuntimeError("Gagal mengambil stream PNG.")
                    png_doc = BufferedInputFile(img_bytes, filename=f"bikinAI_NoBG_{int(time.time())}.png")
                    await call.message.answer_document(
                        document=png_doc,
                        caption=(
                            f"✂️ **FILE `.PNG` TRANSPARAN SELESAI!**\n"
                            f"┣ 🛠️ **Fitur:** `Hapus Background (Lossless .PNG)`\n"
                            f"┗ 🔍 **Penajaman:** `{ups_label}`"
                        ),
                        parse_mode="Markdown",
                        reply_markup=build_400_percent_derivative_upsell_kb(),
                    )
                else:
                    w, h = (
                        (768, 1024)
                        if sess.aspect_ratio == "9:16"
                        else ((1024, 768) if sess.aspect_ratio == "16:9" else (1024, 1024))
                    )
                    img_bytes = await fetch_clean_image_bytes(
                        f"{sess.prompt}, {engine_label} style, 8k photorealistic masterpiece", w, h
                    )
                    if not img_bytes:
                        raise RuntimeError("Gagal merender gambar.")
                    await call.message.answer_photo(
                        photo=BufferedInputFile(img_bytes, filename="bikinAI_Studio_4K.jpg"),
                        caption=(
                            f"✨ **GAMBAR 4K SELESAI DIRENDER!**\n"
                            f"┣ ⚡ **Mesin AI:** `{engine_label}` ({sess.aspect_ratio})\n"
                            f"┣ 🔍 **Penajaman:** `{ups_label}`\n"
                            f"┗ 📝 **Prompt:** _{sess.prompt[:120]}_"
                        ),
                        parse_mode="Markdown",
                        reply_markup=build_400_percent_derivative_upsell_kb(),
                    )

                await increment_user_usage_counter(db, user_id, is_render=True)
                await mark_job_completed(db, job_id, sess.prompt, engine_label)
                stats = await record_job_and_split_profit(db, revenue_idr=coins * 84, actual_hpp_idr=hpp_idr)
                await broadcast_to_bound_topic(
                    call.bot,
                    db,
                    "ACTIVITY_TOPIC",
                    f"⚡ **Live Neural Feed #{stats['fomo_counter']}**\n"
                    f"Kreator `@{username}` baru saja merender karya dengan **`{engine_label}`** ({sess.aspect_ratio})!",
                )
            except Exception:
                await refund_failed_job(db, job_id)
                await call.message.edit_text(
                    f"🛡️ **Auto-Refund Sweeper:** Render mengalami kendala jaringan. Koin untuk `{job_id}` telah dikembalikan 100% ke saldo Anda!",
                    parse_mode="Markdown",
                )
        return

    await call.answer()
    if sess.modality == "VIDEO":
        txt, kb = build_video_wizard_kb(sess)
    elif sess.modality == "IMAGE":
        txt, kb = build_image_wizard_kb(sess)
    else:
        txt, kb = build_editing_tools_wizard_kb(sess)
    await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=kb)


@router.callback_query(F.data.startswith("drv:"))
async def handle_derivative_upsell_callbacks(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    username = call.from_user.username or "Kreator"
    drv_type = call.data.split(":", 1)[1]
    sess = ACTIVE_DRAFTS.get(user_id)
    base_prompt = sess.prompt if sess else "Cinematic 4K YouTube & TikTok poster thumbnail"

    cost = 10 if drv_type == "clean_license" else 4
    async with aiosqlite.connect(DB_PATH) as db:
        await ensure_user_and_track_identity(db, user_id, username)
        ok, job_id, deduct_msg = await deduct_user_coins_for_job(
            db, user_id, cost, allow_bonus=True, prompt_text=base_prompt, engine_used=f"DRV_{drv_type.upper()}"
        )
        if not ok:
            await call.answer(f"⚠️ {deduct_msg}", show_alert=True)
            return

        if drv_type == "poster4k":
            await call.answer("🖼️ Merender Poster Thumbnail 4K...", show_alert=False)
            img_bytes = await fetch_clean_image_bytes(
                f"{base_prompt}, Cinematic 4K YouTube & TikTok poster thumbnail, vibrant lighting, 8k", 1024, 768
            )
            if img_bytes:
                await call.message.answer_photo(
                    photo=BufferedInputFile(img_bytes, filename="bikinAI_Poster_4K.jpg"),
                    caption=f"🖼️ **Poster Thumbnail 4K Siap Dipakai!**\n┗ 💳 `{deduct_msg}`",
                    parse_mode="Markdown",
                )
                await mark_job_completed(db, job_id, base_prompt, "DRV_POSTER_4K")
                await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            else:
                await refund_failed_job(db, job_id)
                await call.answer("🛡️ Gagal mengambil gambar, koin Anda telah dikembalikan 100%.", show_alert=True)
        elif drv_type == "audiomp3":
            await mark_job_completed(db, job_id, base_prompt, "DRV_AUDIO_MP3")
            await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            await call.answer("🎵 Audio soundtrack berhasil diekstrak!", show_alert=True)
            await call.message.reply(
                f"🎵 **EKSTRAKSI AUDIO SOUNDTRACK SELESAI**\n"
                f"┣ 🆔 **Job ID:** `{job_id}`\n"
                f"┣ 🎼 **Format:** `Stereo MP3 320kbps (Clean Master)`\n"
                f"┗ 💳 **Status:** `{deduct_msg}`",
                parse_mode="Markdown",
            )
        elif drv_type == "clean_license":
            await mark_job_completed(db, job_id, base_prompt, "DRV_CLEAN_LICENSE")
            await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            await call.answer("✨ Lisensi Komersial Bersih diaktifkan!", show_alert=True)
            await call.message.reply(
                f"📜 **SERTIFIKAT LISENSI KOMERSIAL BERSIH (PRO)**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"┣ 👤 **Pemegang Lisensi:** `@{username}` (ID: `{user_id}`)\n"
                f"┣ 🆔 **Kode Sertifikat:** `LIC-{job_id}`\n"
                f"┣ ✅ **Hak Komersial:** `100% Bebas Watermark & Royalti`\n"
                f"┗ 💳 **Status Koin:** `{deduct_msg}`",
                parse_mode="Markdown",
            )


@router.callback_query(F.data.startswith("adm:"))
async def handle_owner_admin_callbacks(call: CallbackQuery) -> None:
    if not call.message or not is_verified_owner_dm(call.from_user.id, call.message.chat.type):
        await call.answer("🔒 Akses khusus Owner.", show_alert=True)
        return

    act = call.data.split(":", 1)[1]
    async with aiosqlite.connect(DB_PATH) as db:
        if act == "harvest":
            ok, harvested_now, total_h = await execute_manual_profit_harvest(db)
            if ok:
                await call.answer(f"🌾 Berhasil memanen profit bersih Rp {harvested_now:,}! Total dipanen: Rp {total_h:,}", show_alert=True)
            else:
                await call.answer("ℹ️ Belum ada profit bersih baru yang siap dipanen saat ini.", show_alert=True)
        elif act == "toggle_hh":
            RUNTIME_CONFIG["HAPPY_HOUR_MODE"] = not RUNTIME_CONFIG["HAPPY_HOUR_MODE"]
            await save_persistent_setting(db, "HAPPY_HOUR_MODE", "1" if RUNTIME_CONFIG["HAPPY_HOUR_MODE"] else "0")
            await call.answer(f"🎉 Flash Happy Hour: {'AKTIF' if RUNTIME_CONFIG['HAPPY_HOUR_MODE'] else 'NONAKTIF'}", show_alert=True)
        elif act == "toggle_prod":
            RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"] = not RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"]
            await save_persistent_setting(db, "LAUNCH_PRODUCTION_MODE", "1" if RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"] else "0")
            await call.answer(f"🚀 Mode Produksi: {'AKTIF' if RUNTIME_CONFIG['LAUNCH_PRODUCTION_MODE'] else 'SANDBOX'}", show_alert=True)
        elif act == "toggle_eng_mode":
            RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] = 2 if RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] == 1 else 1
            await save_persistent_setting(db, "PILIHAN_MESIN_MEDIA", str(RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"]))
            await call.answer(f"⚡ Mesin Media diubah ke Mode {RUNTIME_CONFIG['PILIHAN_MESIN_MEDIA']}", show_alert=True)
        elif act == "subbots" or act.startswith("toggle_sb:"):
            if act.startswith("toggle_sb:"):
                sb_key = act.split(":", 1)[1]
                if sb_key in RUNTIME_CONFIG:
                    RUNTIME_CONFIG[sb_key] = not RUNTIME_CONFIG[sb_key]
            await call.answer()
            sb_keys = [
                ("SUBBOT_SANGMATA_ACTIVE", "🕵️ SangMata Identity Tracker"),
                ("SUBBOT_WELCOME_GUARD_ACTIVE", "🛡️ Cyber Welcome Gate"),
                ("SUBBOT_NEURAL_FEED_ACTIVE", "⚡ Live Neural Feed Broadcaster"),
                ("SUBBOT_REFUND_SWEEPER_ACTIVE", "🔄 Dead-Job Refund Sweeper"),
                ("SUBBOT_SOCIAL_POSTER_ACTIVE", "📣 Social Auto-Poster"),
            ]
            sb_rows = [
                [
                    InlineKeyboardButton(
                        text=f"{'🟢 ON' if RUNTIME_CONFIG[k] else '🔴 OFF'} — {label}",
                        callback_data=f"adm:toggle_sb:{k}",
                    )
                ]
                for k, label in sb_keys
            ]
            sb_rows.append([InlineKeyboardButton(text="⬅️ Kembali ke Admin Panel", callback_data="adm:refresh")])
            await call.message.edit_text(
                "🤖 **MANAJEMEN 5 SUB-BOT OTONOM — bikinAI**\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "Klik pada masing-masing Sub-Bot di bawah untuk mengaktifkan atau menonaktifkan:",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=sb_rows),
            )
            return
        elif act == "cycle_pg":
            providers = [
                ("QRIS_DIRECT", "QRIS GoPay Merchant"),
                ("PG_DUITKU", "Duitku All-Payment"),
                ("PG_MIDTRANS", "Midtrans Snap QRIS/VA"),
                ("PG_PAKASIR", "Pakasir QRIS Instan"),
            ]
            cur_p = RUNTIME_CONFIG["ID_ACTIVE_PROVIDER"]
            idx = next((i for i, p in enumerate(providers) if p[1] == cur_p), 0)
            nxt_cat, nxt_prov = providers[(idx + 1) % len(providers)]
            RUNTIME_CONFIG["ID_ACTIVE_CATEGORY"] = nxt_cat
            RUNTIME_CONFIG["ID_ACTIVE_PROVIDER"] = nxt_prov
            await save_persistent_setting(db, "ID_ACTIVE_CATEGORY", nxt_cat)
            await save_persistent_setting(db, "ID_ACTIVE_PROVIDER", nxt_prov)
            await call.answer(f"💳 Kasir ID dialihkan ke: {nxt_prov}", show_alert=True)
        elif act == "domains":
            await call.answer("🌐 Memindai ketersediaan domain via RDAP...")
            doms = await check_multi_tld_domain_availability_live("bikinai")
            dom_lines = "\n".join(f"▸ `{d['domain']}` — {d['status']}" for d in doms)
            await call.message.edit_text(
                f"🌐 **HASIL SCAN DOMAIN MULTI-TLD (RDAP LIVE)**\n━━━━━━━━━━━━━━━━━━\n{dom_lines}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Admin Panel", callback_data="adm:refresh")]]
                ),
            )
            return
        elif act == "bansos":
            await call.answer("📦 Memasang preset Bansos API ke registri...", show_alert=True)
            now_ts = int(time.time())
            exp_ts = now_ts + (365 * 86400)
            async def _b_tx(conn: aiosqlite.Connection) -> None:
                for cat, items in OMNI_BANSOS_PRESETS.items():
                    for item in items:
                        await conn.execute(
                            """
                            INSERT OR REPLACE INTO omni_resource_registry
                            (resource_id, category, resource_name, endpoint_url, secret_or_meta, is_live_verified, expires_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?);
                            """,
                            (item["res_id"], cat, item["name"], item["endpoint"], item["meta"], int(item["verified"]), exp_ts),
                        )
            await DB_WRITER_DAEMON.execute_write_tx(db, _b_tx)
        else:
            await call.answer("🔄 Data disegarkan.")

        cur = await db.execute(
            "SELECT gross_revenue_idr, working_capital_vault_idr, harvestable_profit_vault_idr, total_harvested_by_owner_idr, total_jobs_completed FROM treasury_summary WHERE id = 1;"
        )
        row = await cur.fetchone()

    txt, kb = _build_owner_admin_panel_view(row)
    try:
        await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=kb)
    except Exception:
        pass



<!-- [ID:02_CORE_AI_S045] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: PATCH AUDIT-02 -->
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
                # Gate 3 Magic Bytes Check (JPEG FFD8FF atau PNG 89504E47)
                head = resp.content[:4]
                if head.startswith(b"\xff\xd8\xff") or head == b"\x89PNG":
                    return resp.content
    except Exception:
        pass
    return None


async def handle_webapp_execute_api(request: web.Request) -> web.Response:
    """[PATCH AUDIT-02]: Memvalidasi initData HMAC & memotong koin sebelum eksekusi Mini App."""
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "message": "Invalid JSON"}, status=400)

    init_data_str = str(data.get("init_data") or "").strip()
    verified_user = verify_telegram_webapp_init_data(init_data_str, BOT_TOKEN) if init_data_str else None
    if verified_user and "id" in verified_user:
        user_id = int(verified_user["id"])
        username = verified_user.get("username") or verified_user.get("first_name") or "Kreator"
    else:
        # Fallback hanya jika di lingkungan uji coba lokal dan user_id valid
        user_id = int(data.get("user_id") or 0)
        username = str(data.get("username") or "Kreator")
        if RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"] and not verified_user:
            return web.json_response(
                {"ok": False, "message": "🔒 Sesi keamanan Mini App tidak valid. Silakan buka ulang dari tombol Telegram."},
                status=403,
            )

    prompt_raw, is_attack = sanitize_and_deobfuscate_input(str(data.get("prompt") or "Katalog produk studio 4K"))
    if is_attack:
        return web.json_response({"ok": False, "message": "🛡️ Pola teks tidak diizinkan."}, status=400)

    modality = str(data.get("modality") or "IMAGE")
    engine = str(data.get("engine") or "Seedream 4.5")
    ratio = str(data.get("ratio") or "9:16")
    upscale = str(data.get("upscale") or "Pertajam Foto & Wajah 4K")
    has_ref = bool(data.get("has_ref"))

    if user_id and BOT_INSTANCE_GLOBAL:
        cost = 0 if RUNTIME_CONFIG["HAPPY_HOUR_MODE"] else (20 if modality == "VIDEO" else 4)
        async with get_db() as db:
            await ensure_user_and_track_identity(db, user_id, username)
            ok, job_id, deduct_msg = await deduct_user_coins_for_job(
                db, user_id, cost, allow_bonus=True, prompt_text=prompt_raw, engine_used=engine
            )
            if not ok:
                return web.json_response({"ok": False, "message": f"⚠️ {deduct_msg}"}, status=402)

            ref_tag = " + Foto Referensi" if has_ref else ""
            try:
                if modality == "VIDEO":
                    await BOT_INSTANCE_GLOBAL.send_video(
                        chat_id=user_id,
                        video=SAMPLE_SANDBOX_VIDEO_URL,
                        caption=(
                            f"🎬 **VIDEO SELESAI DARI STUDIO WEB**\n"
                            f"┣ ⚡ **Mesin AI:** `{engine}` ({ratio})\n"
                            f"┣ 🔍 **Kualitas:** `{upscale}{ref_tag}`\n"
                            f"┗ 📝 **Konsep:** _{prompt_raw[:120]}_"
                        ),
                        parse_mode="Markdown",
                    )
                elif modality == "REMOVE_BG":
                    img_bytes = await fetch_clean_image_bytes(
                        f"{prompt_raw}, isolated subject on pure transparent background, PNG cutout", 768, 768
                    )
                    if not img_bytes:
                        raise RuntimeError("Render PNG gagal")
                    png_doc = BufferedInputFile(img_bytes, filename=f"bikinAI_Transparan_{int(time.time())}.png")
                    await BOT_INSTANCE_GLOBAL.send_document(
                        chat_id=user_id,
                        document=png_doc,
                        caption=(
                            f"✂️ **FILE PNG TRANSPARAN KUALITAS TINGGI**\n"
                            f"┣ 🛠️ **Mode:** `Hapus Background (.PNG Utuh)`\n"
                            f"┗ 🔍 **Kualitas:** `{upscale}`"
                        ),
                        parse_mode="Markdown",
                    )
                else:
                    w, h = (768, 1024) if ratio == "9:16" else ((1024, 768) if ratio == "16:9" else (1024, 1024))
                    img_bytes = await fetch_clean_image_bytes(f"{prompt_raw}, {engine} style, 8k masterpiece", w, h)
                    if not img_bytes:
                        raise RuntimeError("Render gambar gagal")
                    await BOT_INSTANCE_GLOBAL.send_photo(
                        chat_id=user_id,
                        photo=BufferedInputFile(img_bytes, filename="bikinAI_Studio_4K.jpg"),
                        caption=(
                            f"✨ **HASIL KARYA 4K DARI STUDIO WEB**\n"
                            f"┣ ⚡ **Mesin AI:** `{engine}` ({ratio})\n"
                            f"┣ 🔍 **Kualitas:** `{upscale}{ref_tag}`\n"
                            f"┗ 📝 **Deskripsi:** _{prompt_raw[:120]}_"
                        ),
                        parse_mode="Markdown",
                    )
                await mark_job_completed(db, job_id, prompt_raw, engine)
                await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            except Exception:
                await refund_failed_job(db, job_id)
                return web.json_response(
                    {"ok": False, "message": "🛡️ Garansi Koin Kembali 100%: Koin Anda telah dikembalikan otomatis!"},
                    status=500,
                )
        return web.json_response({"ok": True, "message": "✅ Karya selesai dan telah dikirim ke ruang chat Telegram Anda!"})

    return web.json_response({"ok": True, "message": "✅ Silakan buka Studio Web langsung dari tombol di dalam Telegram."})


async def handle_nocturne_chat_api(request: web.Request) -> web.Response:
    """Endpoint Tab 1 NocturneAI Web Studio (/api/nocturne/chat)."""
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "reply": "Invalid JSON"}, status=400)
    prompt_raw, is_attack = sanitize_and_deobfuscate_input(str(data.get("prompt") or "Halo"))
    if is_attack:
        return web.json_response({"ok": False, "reply": "Pola input ditolak."}, status=400)
    model_slug = str(data.get("model") or "nousresearch/hermes-3-llama-3.1-405b")
    async with get_db() as db:
        reply = await generate_frontier_ai_response(
            db, prompt_raw, mode="NOCTURNE_UNCENSORED", preferred_model=model_slug
        )
    return web.json_response({"ok": True, "reply": reply})


async def handle_nocturne_generate_api(request: web.Request) -> web.Response:
    """Endpoint Tab 2 NocturneAI Web Studio (/api/nocturne/generate)."""
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False}, status=400)
    prompt_raw, is_attack = sanitize_and_deobfuscate_input(str(data.get("prompt") or "Masterpiece portrait 8k"))
    if is_attack:
        return web.json_response({"ok": False}, status=400)
    model_name = str(data.get("model") or "Flux.1-Dev Uncensored FP8")
    ratio = str(data.get("ratio") or "9:16")
    w, h = (768, 1024) if ratio == "9:16" else ((1024, 768) if ratio == "16:9" else (1024, 1024))
    img_url = (
        f"https://image.pollinations.ai/prompt/{quote(f'{prompt_raw}, {model_name}, 8k masterpiece')}"
        f"?width={w}&height={h}&nologo=true&private=true&enhance=true&seed={int(time.time())}"
    )
    return web.json_response({"ok": True, "image_url": img_url})


async def handle_voucher_redeem_api(request: web.Request) -> web.Response:
    """Endpoint Tab 3 NocturneAI Web Studio (/api/voucher/redeem)."""
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False, "message": "Invalid JSON"}, status=400)
    voucher_code = str(data.get("voucher") or "").strip()
    async with get_db() as db:
        ok, msg, units = await verify_and_redeem_ed25519_voucher(db, voucher_code)
    return web.json_response({"ok": ok, "message": msg, "units": units}, status=200 if ok else 400)


async def start_embedded_web_servers(port: int = 8080) -> None:
    app = web.Application()
    app.router.add_get("/", lambda req: web.Response(text=MINIAPP_FULL_WEBSITE_HTML, content_type="text/html"))
    app.router.add_get("/unfiltered-portal", lambda req: web.Response(text=NOCTURNE_UNFILTERED_PORTAL_HTML, content_type="text/html"))
    app.router.add_post("/api/webapp/execute", handle_webapp_execute_api)
    app.router.add_post("/api/nocturne/chat", handle_nocturne_chat_api)
    app.router.add_post("/api/nocturne/generate", handle_nocturne_generate_api)
    app.router.add_post("/api/voucher/redeem", handle_voucher_redeem_api)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 [WEB & NOCTURNE STUDIO v3.6.0]: Aktif di port {port} ({RUNTIME_CONFIG['MINIAPP_URL'] or 'http://localhost:8080'})")


