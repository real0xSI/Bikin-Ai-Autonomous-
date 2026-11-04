
<!-- [ID:02_CORE_AI_S035] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
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



<!-- [ID:02_CORE_AI_S036] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# 14. SETUP GRUP OTONOM, WELCOME GATE (BEBAS ISTILAH TEKNIS), UPLOAD FOTO & CHAT NATURAL
@router.message(Command("setup_grup"))
async def cmd_setup_community_group(message: Message) -> None:
    if message.chat.type not in ("group", "supergroup"):
        await message.reply("Perintah `/setup_grup` harus diketik di dalam grup komunitas Anda!")
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
    await message.reply("✅ **SETUP GRUP OTONOM BERHASIL!**\nKe-6 Topik khas *bikinAI* telah dibuat dan diikat otomatis!", parse_mode="Markdown")


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
    await message.reply("Pilih peran otonom untuk ruangan topik ini:", reply_markup=kb)


@router.callback_query(F.data.startswith("bind:"))
async def handle_topic_binding_cb(call: CallbackQuery) -> None:
    parts = call.data.split(":")
    b_key, t_id = parts[1], int(parts[2])
    async with get_db() as db:
        await set_topic_binding(db, b_key, call.message.chat.id, t_id, title=b_key)
    await call.answer(f"✅ Topik berhasil diikat sebagai {b_key}!", show_alert=True)
    await safe_edit_markdown(call.message, f"✅ **Ruangan topik ini resmi diikat ke `{b_key}` (ID: `{t_id}`)!**")


@router.message(F.new_chat_members)
async def handle_builtin_cyber_welcome_gate(message: Message) -> None:
    """Sapaan member baru 100% ramah pengguna (riwayat pergantian username hanya dicatat di database /admin)."""
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
            f"⚡ **Selamat datang di Komunitas Resmi `bikinAI Super Intelligence`, Kak `@{u['safe_uname']}`!**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🧭 **Panduan Singkat:**\n"
            f"▸ Ngobrol santai 24 jam, kirim **Foto Referensi (Produk/Wajah)**, atau buat Video AI Sinematik langsung di bot kami.\n\n"
            f"🎁 *Ketik `/start` di chat pribadi `@{BOT_USERNAME_GLOBAL}` untuk mengambil **+4 Koin Gratis Harianmu**!*",
        )


@router.message(F.photo | F.document)
async def handle_multimodal_photo_and_pdf(message: Message) -> None:
    caption_raw = message.caption or ""
    clean_caption, is_attack = sanitize_and_deobfuscate_input(caption_raw)
    if is_attack:
        await message.reply("🛡️ Pola teks pada caption tidak diizinkan.")
        return

    if message.document:
        doc_name = message.document.file_name or "Dokumen"
        wait_doc = await message.reply(f"📄 **Membaca dan merangkum dokumen `{doc_name}`...**", parse_mode="Markdown")
        async with get_db() as db:
            res = await generate_frontier_ai_response(db, f"Dokumen: {doc_name}. Instruksi: {clean_caption or 'Berikan ringkasan eksekutif dan poin penting.'}", mode="DEEP_RESEARCH")
        await safe_edit_markdown(wait_doc, f"📄 **HASIL ANALISIS DOKUMEN `{doc_name}`**\n━━━━━━━━━━━━━━━━━━\n{res}")
        return

    wait = await message.reply("🎨 **Membaca Foto Referensi Anda & Memproses Karya 4K...**", parse_mode="Markdown")
    target_prompt = clean_caption if clean_caption else "High-end commercial studio photography, ultra-detailed 8k masterpiece"
    if message.from_user:
        ACTIVE_DRAFTS[message.from_user.id] = LiveWizardSession(prompt=target_prompt[:150], modality="IMAGE")

    img_bytes = await fetch_clean_image_bytes(f"{target_prompt}, Seedream 4.5 8k photorealistic masterpiece, sharp focus", 768, 1024)
    if img_bytes:
        if message.from_user:
            async with get_db() as db:
                await increment_user_usage_counter(db, message.from_user.id, is_render=True)
        await message.answer_photo(
            photo=BufferedInputFile(img_bytes, filename="bikinAI_Ref_4K.jpg"),
            caption=f"✨ **Gambar 4K Berbasis Foto Referensi Selesai!**\n┣ 📝 **Instruksi:** _{target_prompt[:120]}_\n┗ 🔍 **Kualitas:** `Pertajam Foto & Wajah 4K`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🖼️➡️🎬 Gerakkan Foto Ini Jadi Video 9:16 (Img2Vid)", callback_data="menu:wizard_video")],
                [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
            ]),
        )
        await wait.delete()
    else:
        await safe_edit_markdown(wait, "✅ Foto referensi diterima! Ketik `menu` untuk memilih mode Foto Jadi Video atau pengeditan lanjutan.")


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
        await safe_reply_markdown(message, f"✅ **Konsep berhasil diperbarui!**\n\n{txt}", reply_markup=kb)
        return

    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username, message.from_user.first_name or "")
        updated_mem = await update_personal_memory_if_needed(db, user_id, clean_text, u["memory"])

        if any(t in low for t in ("tampilin tombol", "tampilkan tombol", "munculin tombol", "buka menu")) or low == "menu":
            await safe_reply_markdown(message, "🎛️ **Ini menu tombol interaktifnya ya Kak 😊 Silakan pilih fitur yang dibutuhkan:**", reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv))
            return

        if any(k in low for k in ("buatkan saya gambar", "buat gambar", "bikin gambar", "render gambar")):
            ACTIVE_DRAFTS[user_id] = LiveWizardSession(prompt=clean_text[:150], modality="IMAGE")
            cost_chat_img = 0 if (u["free_img_used_today"] < 1 or RUNTIME_CONFIG["HAPPY_HOUR_MODE"]) else 4
            ok, job_id, deduct_msg = await deduct_user_coins_for_job(db, user_id, cost_chat_img, True, clean_text, "Seedream 4.5")
            if not ok:
                await safe_reply_markdown(message, f"⚠️ {deduct_msg}\nKlik tombol di bawah untuk mengklaim Koin Gratis Harian:", reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv))
                return
            wait = await message.reply("🎨 **Sedang membuat gambar 4K pesanan Kakak...**", parse_mode="Markdown")
            img_bytes = await fetch_clean_image_bytes(f"{clean_text}, Seedream 4.5 8k photorealistic masterpiece", 768, 1024)
            if img_bytes:
                await increment_user_usage_counter(db, user_id, is_render=True)
                await mark_job_completed(db, job_id, clean_text, "Seedream 4.5")
                await record_job_and_split_profit(db, revenue_idr=cost_chat_img * 84, actual_hpp_idr=0)
                await message.answer_photo(photo=BufferedInputFile(img_bytes, filename="bikinAI_4K.jpg"), caption=f"✨ **Gambar 4K Selesai Dibuat!**\n┣ ⚡ **Mesin AI:** `Seedream 4.5`\n┗ 💳 **Status:** `{deduct_msg}`", parse_mode="Markdown", reply_markup=build_400_percent_derivative_upsell_kb())
                await wait.delete()
                return
            await refund_failed_job(db, job_id)
            await safe_edit_markdown(wait, "🛡️ **Garansi Koin Kembali 100%:** Terjadi kendala jaringan, koin Anda telah dikembalikan utuh!")
            return

        if any(k in low for k in ("buat video", "bikin video", "buatkan video", "foto jadi video")) and "gimana" not in low:
            ACTIVE_DRAFTS[user_id] = LiveWizardSession(prompt=clean_text[:150], modality="VIDEO", upscale_mode="VIDEO_4K_60FPS")
            txt, kb = build_video_wizard_kb(ACTIVE_DRAFTS[user_id])
            await safe_reply_markdown(message, txt, reply_markup=kb)
            return

        await increment_user_usage_counter(db, user_id, is_render=False)
        mode_chat = "PROMPT_ARCHITECT" if low.startswith("prompt ") else "NATURAL_CHAT"
        ai_reply = await generate_frontier_ai_response(db, clean_text, mode=mode_chat, personal_memory=updated_mem)

    await safe_reply_markdown(message, ai_reply + get_next_dynamic_footer())



<!-- [ID:02_CORE_AI_S037] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# ==============================================================================
@router.message(Command("setup_grup"))
async def cmd_setup_community_group(message: Message) -> None:
    if message.chat.type not in ("group", "supergroup"):
        await message.reply("Perintah `/setup_grup` harus diketik di dalam grup komunitas Anda!")
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

    async with get_db() as db:
        for b_key, t_title in topics_to_create:
            try:
                res_topic = await message.bot.create_forum_topic(chat_id=chat_id, name=t_title)
                t_id = res_topic.message_thread_id
                await set_topic_binding(db, b_key, chat_id, t_id, title=t_title)
            except Exception:
                await set_topic_binding(db, b_key, chat_id, 0, title=t_title)

    await message.reply(
        "✅ **SETUP GRUP OTONOM BERHASIL!**\n"
        "Ke-6 Topik khas *bikinAI* telah dibuat dan diikat otomatis ke database abadi!",
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
                InlineKeyboardButton(text="📡 Command & Promo", callback_data=f"bind:COMMAND_TOPIC:{thread_id}"),
            ],
            [
                InlineKeyboardButton(text="🧭 Blueprint & Koin", callback_data=f"bind:FAQ_TOPIC:{thread_id}"),
                InlineKeyboardButton(text="🧠 Arsitek Prompt", callback_data=f"bind:CREATIVE_TOPIC:{thread_id}"),
            ],
            [
                InlineKeyboardButton(text="🎬 Galeri Kreator", callback_data=f"bind:GALLERY_TOPIC:{thread_id}"),
                InlineKeyboardButton(text="🛠️ Lab Inovasi & Bantuan", callback_data=f"bind:FEEDBACK_TOPIC:{thread_id}"),
            ],
        ]
    )
    await message.reply("Pilih peran otonom untuk ruangan topik ini:", reply_markup=kb)


@router.callback_query(F.data.startswith("bind:"))
async def handle_topic_binding_cb(call: CallbackQuery) -> None:
    parts = call.data.split(":")
    b_key, t_id = parts[1], int(parts[2])
    chat_id = call.message.chat.id
    async with get_db() as db:
        await set_topic_binding(db, b_key, chat_id, t_id, title=b_key)
    await call.answer(f"✅ Topik berhasil diikat sebagai {b_key}!", show_alert=True)
    await safe_edit_markdown(call.message, f"✅ **Ruangan topik ini resmi diikat ke `{b_key}` (ID: `{t_id}`)!**")


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
        alert_line = f"\n🕵️ _Catatan Identitas: Sebelumnya dikenal sebagai {u['identity_alert']}_" if u["identity_alert"] else ""
        await safe_reply_markdown(
            message,
            f"⚡ **Selamat datang di Komunitas Resmi `bikinAI Super Intelligence`, Kak `@{u['safe_uname']}`!**{alert_line}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🧭 **Panduan Singkat:**\n"
            f"▸ Kirim **Teks, Foto Referensi, atau Dokumen** langsung ke bot pribadi kami.\n"
            f"▸ Nikmati asisten 24 jam gratis & studio kreator 4K.\n\n"
            f"🎁 *Ketik `/start` di chat pribadi `@{BOT_USERNAME_GLOBAL}` untuk mengambil **+4 Koin Gratis Harianmu**!*",
        )


@router.message(F.photo | F.document)
async def handle_multimodal_photo_and_pdf(message: Message) -> None:
    """[PATCH AUDIT-05]: Menggunakan instruksi asli pelanggan pada upload foto referensi (bukan prompt kucing hardcoded)."""
    caption_raw = message.caption or ""
    clean_caption, is_attack = sanitize_and_deobfuscate_input(caption_raw)
    if is_attack:
        await message.reply("🛡️ Pola teks pada caption tidak diizinkan.")
        return

    if message.document:
        doc_name = message.document.file_name or "Dokumen"
        wait_doc = await message.reply(f"📄 **Membaca dan merangkum dokumen `{doc_name}`...**", parse_mode="Markdown")
        async with get_db() as db:
            res = await generate_frontier_ai_response(
                db, f"Dokumen: {doc_name}. Instruksi: {clean_caption or 'Berikan ringkasan eksekutif dan poin penting.'}", mode="DEEP_RESEARCH"
            )
        await safe_edit_markdown(wait_doc, f"📄 **HASIL ANALISIS DOKUMEN `{doc_name}`**\n━━━━━━━━━━━━━━━━━━\n{res}")
        return

    wait = await message.reply("🎨 **Membaca Foto Referensi Anda & Memproses Gambar 4K Baru...**", parse_mode="Markdown")
    target_prompt = clean_caption if clean_caption else "High-end commercial studio photography, ultra-detailed 8k masterpiece"
    if message.from_user:
        ACTIVE_DRAFTS[message.from_user.id] = LiveWizardSession(prompt=target_prompt[:150], modality="IMAGE")

    en_prompt = f"{target_prompt}, Seedream 4.5 8k photorealistic masterpiece, sharp focus"
    img_bytes = await fetch_clean_image_bytes(en_prompt, 768, 1024)
    if img_bytes:
        if message.from_user:
            async with get_db() as db:
                await increment_user_usage_counter(db, message.from_user.id, is_render=True)
        await message.answer_photo(
            photo=BufferedInputFile(img_bytes, filename="bikinAI_Ref_4K.jpg"),
            caption=(
                f"✨ **Gambar 4K Berbasis Foto Referensi Selesai!**\n"
                f"┣ 📝 **Instruksi:** _{target_prompt[:120]}_\n"
                f"┗ 🔍 **Kualitas:** `Pertajam Foto & Wajah 4K`"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🎬 Gerakkan Gambar Ini Jadi Video 9:16", callback_data="menu:wizard_video")],
                    [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
                ]
            ),
        )
        await wait.delete()
    else:
        await safe_edit_markdown(wait, "✅ Foto referensi diterima! Ketik `menu` untuk memilih mode pengeditan lanjutan.")


@router.message(F.text)
async def handle_natural_conversation(message: Message) -> None:
    raw_text = message.text or ""
    low = raw_text.lower().strip()
    user_id = message.from_user.id
    username = message.from_user.username or "Kreator"
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
        if sess.modality == "VIDEO":
            txt, kb = build_video_wizard_kb(sess)
        elif sess.modality == "IMAGE":
            txt, kb = build_image_wizard_kb(sess)
        else:
            txt, kb = build_editing_tools_wizard_kb(sess)
        await safe_reply_markdown(message, f"✅ **Konsep berhasil diperbarui!**\n\n{txt}", reply_markup=kb)
        return

    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username, message.from_user.first_name or "")
        updated_mem = await update_personal_memory_if_needed(db, user_id, clean_text, u["memory"])

        if any(t in low for t in ("tampilin tombol", "tampilkan tombol", "munculin tombol", "buka menu")) or low == "menu":
            await safe_reply_markdown(
                message,
                "🎛️ **Ini menu tombol interaktifnya ya Kak 😊 Silakan pilih fitur yang dibutuhkan:**",
                reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
            )
            return

        if any(k in low for k in ("buatkan saya gambar", "buat gambar", "bikin gambar", "render gambar")):
            ACTIVE_DRAFTS[user_id] = LiveWizardSession(prompt=clean_text[:150], modality="IMAGE")
            # [PATCH AUDIT-06]: Sampel gratis di chat 1x/hari; selebihnya memotong 4 Koin secara adil
            cost_chat_img = 0 if (u["free_img_used_today"] < 1 or RUNTIME_CONFIG["HAPPY_HOUR_MODE"]) else 4
            ok, job_id, deduct_msg = await deduct_user_coins_for_job(
                db, user_id, cost_chat_img, allow_bonus=True, prompt_text=clean_text, engine_used="Seedream 4.5"
            )
            if not ok:
                await safe_reply_markdown(
                    message,
                    f"⚠️ {deduct_msg}\nKlik tombol di bawah untuk mengklaim Koin Gratis Harian atau membuka Studio:",
                    reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
                )
                return

            wait = await message.reply("🎨 **Sedang membuat gambar 4K pesanan Kakak...**", parse_mode="Markdown")
            img_bytes = await fetch_clean_image_bytes(f"{clean_text}, Seedream 4.5 8k photorealistic masterpiece", 768, 1024)
            if img_bytes:
                await increment_user_usage_counter(db, user_id, is_render=True)
                await mark_job_completed(db, job_id, clean_text, "Seedream 4.5")
                await record_job_and_split_profit(db, revenue_idr=cost_chat_img * 84, actual_hpp_idr=0)
                await message.answer_photo(
                    photo=BufferedInputFile(img_bytes, filename="bikinAI_4K.jpg"),
                    caption=(
                        f"✨ **Gambar 4K Selesai Dibuat!**\n"
                        f"┣ ⚡ **Mesin AI:** `Seedream 4.5`\n"
                        f"┣ 🔍 **Kualitas:** `Pertajam Foto & Teks 4K`\n"
                        f"┗ 💳 **Status:** `{deduct_msg}`"
                    ),
                    parse_mode="Markdown",
                    reply_markup=build_400_percent_derivative_upsell_kb(),
                )
                await wait.delete()
                return
            else:
                await refund_failed_job(db, job_id)
                await safe_edit_markdown(
                    wait,
                    "🛡️ **Garansi Koin Kembali 100%:** Terjadi kendala jaringan, koin Anda telah dikembalikan utuh!",
                )
                return

        if any(k in low for k in ("buat video", "bikin video", "buatkan video")) and "gimana" not in low:
            ACTIVE_DRAFTS[user_id] = LiveWizardSession(prompt=clean_text[:150], modality="VIDEO")
            txt, kb = build_video_wizard_kb(ACTIVE_DRAFTS[user_id])
            await safe_reply_markdown(message, txt, reply_markup=kb)
            return

        await increment_user_usage_counter(db, user_id, is_render=False)
        mode_chat = "PROMPT_ARCHITECT" if "prompt" in low else "NATURAL_CHAT"
        ai_reply = await generate_frontier_ai_response(db, clean_text, mode=mode_chat, personal_memory=updated_mem)

    await safe_reply_markdown(message, ai_reply + get_next_dynamic_footer())



<!-- [ID:02_CORE_AI_S038] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: CAT -->
# Budget USD per hari
DAILY_BUDGET = {
    "global":         float(200),
    "exec":           float(50),
    "eng":            float(60),
    "ai":             float(60),
    "sec":            float(20),
    "mkt":            float(10),
    "fin":            float(5),
}

def _path(cat: str) -> Path:
    day = time.strftime("%Y-%m-%d")
    return STORE / f"{cat}_{day}.json"

def _load(cat: str) -> dict:
    p = _path(cat)
    return json.loads(p.read_text()) if p.exists() else {"spent": 0.0, "calls": 0}

def _save(cat: str, data: dict):
    _path(cat).write_text(json.dumps(data))

def price(provider: str, model: str, in_tok: int, out_tok: int) -> float:
    key = f"{provider}:{model}"
    tier = PRICES.get(key) or PRICES.get(f"{provider}:*") or {"in": 0.001, "out": 0.002}
    return (in_tok/1000)*tier["in"] + (out_tok/1000)*tier["out"]

def check(cat: str, est_usd: float) -> dict:
    cat_budget = DAILY_BUDGET.get(cat, 10.0)
    glob_budget = DAILY_BUDGET["global"]
    cat_spent = _load(cat)["spent"]
    glob_spent = _load("global")["spent"]
    if cat_spent + est_usd > cat_budget:
        return {"allow": False, "reason": f"cat_budget_exceeded({cat})"}
    if glob_spent + est_usd > glob_budget:
        return {"allow": False, "reason": "global_budget_exceeded"}
    return {"allow": True}

def record(cat: str, usd: float):
    c = _load(cat); c["spent"] += usd; c["calls"] += 1; _save(cat, c)
    g = _load("global"); g["spent"] += usd; g["calls"] += 1; _save("global", g)

def report() -> dict:
    day = time.strftime("%Y-%m-%d")
    out = {}
    for cat in DAILY_BUDGET:
        d = _load(cat)
        out[cat] = {"spent": round(d["spent"], 4),
                    "budget": DAILY_BUDGET[cat],
                    "calls": d["calls"]}
    return {"day": day, "budget": out}

"""
Router LLM dengan fallback berjenjang:
  primary (per kategori) → fallback_1 → fallback_2 → local
Cost guard dicek SEBELUM panggil. Audit setiap panggilan.
"""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from services.ai_gateway import cost_guard, providers
from office.orchestrator.audit import audit


<!-- [ID:02_CORE_AI_S039] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Deploy
```bash
cd apps/admin
npm install
npm run build
npm start     # port 3001, di belakang Cloudflare Access


## 12.12 `apps/admin/app/api/login/route.ts`
```typescript
import { NextRequest, NextResponse } from "next/server";
import crypto from "crypto";

export async function POST(req: NextRequest) {
  const { pin } = await req.json();
  if (pin !== process.env.OWNER_PIN) {
    return NextResponse.json({ ok: false }, { status: 401 });
  }
  const session = crypto.randomBytes(32).toString("hex");
  const res = NextResponse.json({ ok: true });
  res.cookies.set("owner_session", session, {
    httpOnly: true, secure: true, sameSite: "strict",
    maxAge: 60 * 60 * 8, path: "/"
  });
  return res;
}
Paket Isi Fungsi
9 services/ai-gateway/* Router multi-provider LLM + cost guard + fallback + audit per call
10 services/audit/* Verifier hash chain + timeline forensics + nightly auto L4
11 bots/whatsapp/*, bots/instagram/*, bots/threads/*, bots/core/hmac.py Adapter nyata dengan verifikasi signature → satu dispatcher
12 apps/admin/* Dashboard owner: overview, approvals, agents, kill switch, login PIN

/status              → ringkasan
/panic 123456        → stop semua (L0)
/freeze finance 123456
/freeze external 123456
/readonly on 123456
/recover 123456
/approve apv_2026_001 123456
/deny apv_2026_001 123456
/cost today
/agents
/log last 20



```
```

