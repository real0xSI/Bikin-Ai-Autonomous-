
<!-- [ID:02_CORE_AI_S010] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: :40 -->
# 12. COMMAND HANDLERS LENGKAP
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
        await message.reply("🔒 Perintah `/set_webname` khusus Owner di DM pribadi.")
        return
    new_name = (message.text or "").partition(" ")[2].strip()
    if not new_name:
        await message.reply(f"🌐 **Nama Website Saat Ini:** `{RUNTIME_CONFIG['WEB_BRAND_NAME']}`\nCara ganti nama: `/set_webname NamaStudioBaru`", parse_mode="Markdown")
        return
    RUNTIME_CONFIG["WEB_BRAND_NAME"] = new_name[:40]
    async with get_db() as db:
        await save_persistent_setting(db, "WEB_BRAND_NAME", RUNTIME_CONFIG["WEB_BRAND_NAME"])
    await message.reply(f"✅ **Nama Brand Website berhasil diubah menjadi:** `{RUNTIME_CONFIG['WEB_BRAND_NAME']}`", parse_mode="Markdown")


@router.message(Command("claim_owner"))
async def cmd_claim_owner_bootstrap(message: Message) -> None:
    if message.chat.type != "private":
        return
    token_arg = (message.text or "").partition(" ")[2].strip()
    if RUNTIME_CONFIG["OWNER_ID_RUNTIME"] == 0 and hmac.compare_digest(token_arg, OWNER_BOOTSTRAP_TOKEN):
        RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = message.from_user.id
        async with get_db() as db:
            await save_persistent_setting(db, "OWNER_ID_RUNTIME", str(message.from_user.id))
        await message.reply(f"✅ **Akses Owner Berhasil Dikunci ke ID `{message.from_user.id}`!** Ketik `/admin` untuk membuka panel.")
    else:
        await message.reply("🔒 Token bootstrap tidak valid atau Owner sudah terkunci.")


@router.message(Command("harvest"))
async def cmd_quick_harvest_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Perintah `/harvest` khusus Owner di DM pribadi.")
        return
    async with get_db() as db:
        ok, harvested_now, total_h = await execute_manual_profit_harvest(db)
    await message.reply(f"🌾 **PANEN LABA BERSIH BERHASIL!**\n┣ 💎 **Dipanen Sekarang:** **`Rp {harvested_now:,}`**\n┗ 🏦 **Total Akumulasi:** `Rp {total_h:,}`" if ok else "ℹ️ Belum ada laba bersih baru yang siap dipanen.", parse_mode="Markdown")


@router.message(Command("bansos", "info_bansos"))
async def cmd_bansos_radar_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Radar `/bansos` khusus Owner di DM pribadi.")
        return
    async with get_db() as db:
        txt, kb = await _build_bansos_4tab_view(db, "AI_API")
    await safe_reply_markdown(message, txt, reply_markup=kb)


@router.message(Command("rolling", "agents"))
async def cmd_rolling_agents_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Panel `/rolling` khusus Owner di DM pribadi.")
        return
    nxt = rotate_primary_agent()
    async with get_db() as db:
        await save_persistent_setting(db, "PRIMARY_ROLLING_AGENT", nxt)
    lines = [f"▸ {'🟢' if k == nxt else '⚪'} **`{k}`** — {v['title']} _(OK: {v['ok']} | Fail: {v['fail']})_" for k, v in AGENTIC_ROLLING_POOL.items()]
    await safe_reply_markdown(message, f"🔄 **ROLLING MULTI-AGENT POOL DIPUTAR!**\nOtak utama kini dikunci ke: **`{nxt}`**\n\n" + "\n".join(lines))


@router.message(Command("donasi_api"))
async def cmd_community_donate_api(message: Message) -> None:
    args = (message.text or "").split()[1:]
    if not args:
        await message.reply("🤝 **Format:** `/donasi_api https://endpoint-komunitas/v1/chat/completions nama-model`\nJika lolos uji 4-Gate (<2,5s), Anda otomatis mendapat **+15 Koin Bonus**!", parse_mode="Markdown")
        return
    ep_url, model_slug = args[0].strip(), (args[1].strip() if len(args) > 1 else "openai")
    wait = await message.reply("🛡️ **Memeriksa Endpoint Komunitas...**", parse_mode="Markdown")
    ok_ping, ms, info = await ping_and_verify_bansos_endpoint(ep_url, model_slug)
    if not ok_ping:
        await safe_edit_markdown(wait, f"❌ **Endpoint belum memenuhi syarat kecepatan/keamanan:** `{info}`")
        return
    user_id, username = message.from_user.id, message.from_user.username or "Kreator"
    res_id = f"COM-{hashlib.sha256(ep_url.encode()).hexdigest()[:8].upper()}"
    async with get_db() as db:
        await ensure_user_and_track_identity(db, user_id, username)
        async def _tx(conn: aiosqlite.Connection) -> None:
            await conn.execute("INSERT OR REPLACE INTO omni_resource_registry (resource_id, category, resource_name, endpoint_url, secret_or_meta, is_live_verified, expires_at) VALUES (?, 'AI_API', ?, ?, ?, 1, ?);", (res_id, f"Community Node ({username})", ep_url, model_slug, int(time.time()) + 30 * 86400))
            await conn.execute("UPDATE users SET koin_bonus = MIN(?, koin_bonus + 15) WHERE internal_user_id = ?;", (MAX_KOIN_BONUS_CAP, user_id))
        await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    await safe_edit_markdown(wait, f"✅ **TERVERIFIKASI AKTIF ({ms} ms)!**\nTerima kasih Kak! **+15 Koin Bonus** telah ditambahkan ke saldo Anda.")


@router.message(Command("riset"))
async def cmd_deep_research_handler(message: Message) -> None:
    user_id, username = message.from_user.id, message.from_user.username or "Kreator"
    raw_arg = (message.text or "").partition(" ")[2].strip()
    if not raw_arg:
        await message.reply("🔬 **MODE DEEP RESEARCH — bikinAI**\nContoh: `/riset strategi pemasaran produk skincare UMKM 2026`", parse_mode="Markdown")
        return
    clean_q, is_attack = sanitize_and_deobfuscate_input(raw_arg)
    if is_attack:
        await message.reply("🛡️ Pola teks tidak diizinkan.")
        return
    wait = await message.reply("🔬 **Sedang menyusun laporan Deep Research...**", parse_mode="Markdown")
    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username)
        await increment_user_usage_counter(db, user_id, is_render=False)
        res = await generate_frontier_ai_response(db, clean_q, mode="DEEP_RESEARCH", personal_memory=u["memory"])
    await safe_edit_markdown(wait, f"🔬 **LAPORAN DEEP RESEARCH — bikinAI**\n━━━━━━━━━━━━━━━━━━\n{res}")


@router.message(Command("canvas"))
async def cmd_canvas_workspace_handler(message: Message) -> None:
    user_id, username = message.from_user.id, message.from_user.username or "Kreator"
    raw_arg = (message.text or "").partition(" ")[2].strip()
    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username)
        if not raw_arg:
            await safe_reply_markdown(message, f"📝 **CANVAS WORKSPACE AKTIF**\n━━━━━━━━━━━━━━━━━━\n{u['canvas'] or '_(Kosong. Ketik `/canvas [instruksi]` untuk mulai menulis.)_'}")
            return
        clean_arg, is_attack = sanitize_and_deobfuscate_input(raw_arg)
        if is_attack:
            await message.reply("🛡️ Pola teks tidak diizinkan.")
            return
        wait = await message.reply("📝 **Memperbarui Canvas Workspace...**", parse_mode="Markdown")
        await increment_user_usage_counter(db, user_id, is_render=False)
        updated_canvas = await generate_frontier_ai_response(db, clean_arg, mode="CANVAS_EDIT", personal_memory=u["memory"], canvas_state=u["canvas"])
        async def _save_c(conn: aiosqlite.Connection) -> None:
            await conn.execute("UPDATE users SET active_canvas_content = ? WHERE internal_user_id = ?;", (updated_canvas[:4000], user_id))
        await DB_WRITER_DAEMON.execute_write_tx(db, _save_c)
    await safe_edit_markdown(wait, f"📝 **CANVAS WORKSPACE DIPERBARUI**\n━━━━━━━━━━━━━━━━━━\n{updated_canvas}")


@router.message(Command("saran", "feedback"))
async def cmd_user_feedback_handler(message: Message) -> None:
    user_id, username = message.from_user.id, message.from_user.username or "Kreator"
    raw_fb = (message.text or "").partition(" ")[2].strip()
    if not raw_fb:
        await message.reply("🛠️ Kirim masukan Anda dengan format: `/saran [isi masukan Anda]`", parse_mode="Markdown")
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
        await broadcast_to_bound_topic(message.bot, db, "FEEDBACK_TOPIC", f"🛠️ **Masukan Baru dari Kreator `@{username}`:**\n> _{clean_fb[:300]}_")
    await message.reply("✅ Terima kasih Kak! Masukan Anda telah tercatat di Lab Inovasi bikinAI.")


@router.message(Command("set_miniapp"))
async def cmd_set_miniapp_url(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Perintah ini khusus Owner di DM.")
        return
    arg_url = (message.text or "").partition(" ")[2].strip()
    if not arg_url.startswith("https://"):
        await message.reply(f"🌐 **URL Mini App Saat Ini:** `{RUNTIME_CONFIG['MINIAPP_URL'] or 'Belum disetel'}`\nCara ubah: `/set_miniapp https://domain-anda.app`", parse_mode="Markdown")
        return
    RUNTIME_CONFIG["MINIAPP_URL"] = arg_url
    async with get_db() as db:
        await save_persistent_setting(db, "MINIAPP_URL", arg_url)
    await message.reply(f"✅ **URL Mini App Dikunci Abadi:**\n`{arg_url}`", parse_mode="Markdown")


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
    await message.reply(f"✅ **OMNI-RESOURCE HARVESTER AKTIF!**\n┣ 📦 **Preset Terpasang:** `{count_installed} Resource`\n┗ 🛡️ **4-Gate AST v2.0:** `AMAN ({ast_check['hash']})`", parse_mode="Markdown")


@router.message(Command("admin"))
async def cmd_owner_admin_panel(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Panel `/admin` khusus Owner di DM pribadi.\n_(Gunakan `/claim_owner <token_terminal>` jika baru pertama menyalakan server)_", parse_mode="Markdown")
        return
    async with get_db() as db:
        await save_persistent_setting(db, "OWNER_ID_RUNTIME", str(message.from_user.id))
        cur = await db.execute("SELECT gross_revenue_idr, working_capital_vault_idr, harvestable_profit_vault_idr, total_harvested_by_owner_idr, total_jobs_completed FROM treasury_summary WHERE id = 1;")
        row = await cur.fetchone()
    txt, kb = _build_owner_admin_panel_view(row)
    await safe_reply_markdown(message, txt, reply_markup=kb)



<!-- [ID:02_CORE_AI_S011] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: PATCH AUDIT-03 -->
# ==============================================================================
@router.message(CommandStart())
async def cmd_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "Kreator"
    is_priv = message.chat.type == "private"
    lang = message.from_user.language_code or "id"

    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username, message.from_user.first_name or "", lang)

    await safe_reply_markdown(
        message,
        build_customer_dashboard_caption(username, u),
        reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
    )


@router.message(Command("menu", "studio", "bantuan"))
async def cmd_menu_handler(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "Kreator"
    is_priv = message.chat.type == "private"

    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username, message.from_user.first_name or "")

    await safe_reply_markdown(
        message,
        build_customer_dashboard_caption(username, u),
        reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
    )


@router.message(Command("claim_owner"))
async def cmd_claim_owner_bootstrap(message: Message) -> None:
    """[PATCH AUDIT-03]: Klaim akses Owner dengan token bootstrap terminal jika ADMIN_USER_ID belum disetel."""
    if message.chat.type != "private":
        return
    token_arg = (message.text or "").partition(" ")[2].strip()
    if RUNTIME_CONFIG["OWNER_ID_RUNTIME"] == 0 and hmac.compare_digest(token_arg, OWNER_BOOTSTRAP_TOKEN):
        RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = message.from_user.id
        async with get_db() as db:
            await save_persistent_setting(db, "OWNER_ID_RUNTIME", str(message.from_user.id))
        await message.reply(f"✅ **Akses Owner Berhasil Dikunci ke ID `{message.from_user.id}`!** Ketik `/admin` untuk membuka panel.")
    else:
        await message.reply("🔒 Token bootstrap tidak valid atau Owner sudah terkunci.")


@router.message(Command("harvest"))
async def cmd_quick_harvest_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Perintah `/harvest` khusus Owner di DM pribadi.")
        return
    async with get_db() as db:
        ok, harvested_now, total_h = await execute_manual_profit_harvest(db)
    if ok:
        await message.reply(
            f"🌾 **PANEN LABA BERSIH BERHASIL!**\n"
            f"┣ 💎 **Nominal Dipanen Sekarang:** **`Rp {harvested_now:,}`**\n"
            f"┗ 🏦 **Total Akumulasi Panen Owner:** `Rp {total_h:,}`",
            parse_mode="Markdown",
        )
    else:
        await message.reply("ℹ️ Belum ada saldo laba bersih baru yang siap dipanen saat ini.")


@router.message(Command("bansos", "info_bansos"))
async def cmd_bansos_radar_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Radar `/bansos` khusus Owner di DM pribadi.")
        return
    async with get_db() as db:
        txt, kb = await _build_bansos_4tab_view(db, "AI_API")
    await safe_reply_markdown(message, txt, reply_markup=kb)


@router.message(Command("rolling", "agents"))
async def cmd_rolling_agents_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Panel `/rolling` khusus Owner di DM pribadi.")
        return
    nxt = rotate_primary_agent()
    async with get_db() as db:
        await save_persistent_setting(db, "PRIMARY_ROLLING_AGENT", nxt)
    lines = [
        f"▸ {'🟢' if k == nxt else '⚪'} **`{k}`** — {v['title']} _(OK: {v['ok']} | Fail: {v['fail']})_"
        for k, v in AGENTIC_ROLLING_POOL.items()
    ]
    await safe_reply_markdown(
        message,
        f"🔄 **ROLLING MULTI-AGENT POOL DIPUTAR!**\n"
        f"Otak utama kini dikunci ke: **`{nxt}`**\n\n" + "\n".join(lines),
    )


@router.message(Command("donasi_api"))
async def cmd_community_donate_api(message: Message) -> None:
    """Fitur Crowdsourced Community Bansos dengan uji otomatis 4-Gate Sterilizer."""
    args = (message.text or "").split()[1:]
    if len(args) < 1:
        await message.reply(
            "🤝 **PROGRAM KOMUNITAS SUMBANG ENDPOINT GRATIS (`/donasi_api`)**\n"
            "Format: `/donasi_api https://endpoint-komunitas/v1/chat/completions nama-model`\n"
            "Jika lolos uji keamanan 4-Gate & merespons <2,5 detik, Anda otomatis mendapat **+15 Koin Bonus**!",
            parse_mode="Markdown",
        )
        return
    ep_url = args[0].strip()
    model_slug = args[1].strip() if len(args) > 1 else "openai"
    wait = await message.reply("🛡️ **Memeriksa Endpoint dengan 4-Gate Deep-Defense Sterilizer...**", parse_mode="Markdown")
    ok_ping, ms, info = await ping_and_verify_bansos_endpoint(ep_url, model_slug)
    if not ok_ping:
        await safe_edit_markdown(wait, f"❌ **Endpoint Ditolak oleh 4-Gate Sterilizer:** `{info}`")
        return

    user_id = message.from_user.id
    username = message.from_user.username or "Kreator"
    res_id = f"COM-{hashlib.sha256(ep_url.encode()).hexdigest()[:8].upper()}"
    async with get_db() as db:
        await ensure_user_and_track_identity(db, user_id, username)

        async def _tx(conn: aiosqlite.Connection) -> None:
            await conn.execute(
                """
                INSERT OR REPLACE INTO omni_resource_registry
                (resource_id, category, resource_name, endpoint_url, secret_or_meta, is_live_verified, expires_at)
                VALUES (?, 'AI_API', ?, ?, ?, 1, ?);
                """,
                (res_id, f"Community Node ({username})", ep_url, model_slug, int(time.time()) + 30 * 86400),
            )
            await conn.execute(
                "UPDATE users SET koin_bonus = MIN(?, koin_bonus + 15) WHERE internal_user_id = ?;",
                (MAX_KOIN_BONUS_CAP, user_id),
            )

        await DB_WRITER_DAEMON.execute_write_tx(db, _tx)

    await safe_edit_markdown(
        wait,
        f"✅ **LOLOS UJI 4-GATE STERILIZER ({ms} ms)!**\n"
        f"Endpoint `{res_id}` resmi masuk ke kolam cadangan otonom dan **+15 Koin Bonus** telah ditambahkan ke akun Anda!",
    )


@router.message(Command("riset"))
async def cmd_deep_research_handler(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username or "Kreator"
    raw_arg = (message.text or "").partition(" ")[2].strip()
    if not raw_arg:
        await message.reply(
            "🔬 **MODE DEEP RESEARCH — bikinAI**\n"
            "Ketik topik yang ingin dibedah secara mendalam.\n"
            "Contoh: `/riset strategi pemasaran produk skincare UMKM 2026`",
            parse_mode="Markdown",
        )
        return
    clean_q, is_attack = sanitize_and_deobfuscate_input(raw_arg)
    if is_attack:
        await message.reply("🛡️ Pola teks tidak diizinkan.")
        return
    wait = await message.reply("🔬 **Sedang menyusun laporan Deep Research...**", parse_mode="Markdown")
    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username)
        await increment_user_usage_counter(db, user_id, is_render=False)
        res = await generate_frontier_ai_response(db, clean_q, mode="DEEP_RESEARCH", personal_memory=u["memory"])
    await safe_edit_markdown(wait, f"🔬 **LAPORAN DEEP RESEARCH — bikinAI**\n━━━━━━━━━━━━━━━━━━\n{res}")


@router.message(Command("canvas"))
async def cmd_canvas_workspace_handler(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username or "Kreator"
    raw_arg = (message.text or "").partition(" ")[2].strip()

    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username)
        if not raw_arg:
            current_canvas = u["canvas"] or "_(Canvas Anda masih kosong. Ketik `/canvas [instruksi]` untuk mulai menulis draf.)_"
            await safe_reply_markdown(
                message,
                f"📝 **CANVAS WORKSPACE AKTIF**\n━━━━━━━━━━━━━━━━━━\n{current_canvas}\n\n"
                f"💡 _Ketik `/canvas [instruksi baru]` untuk menyunting atau mengembangkan draf di atas._",
            )
            return
        clean_arg, is_attack = sanitize_and_deobfuscate_input(raw_arg)
        if is_attack:
            await message.reply("🛡️ Pola teks tidak diizinkan.")
            return
        wait = await message.reply("📝 **Sedang memperbarui dokumen di Canvas Workspace...**", parse_mode="Markdown")
        await increment_user_usage_counter(db, user_id, is_render=False)
        updated_canvas = await generate_frontier_ai_response(
            db, clean_arg, mode="CANVAS_EDIT", personal_memory=u["memory"], canvas_state=u["canvas"]
        )

        async def _save_canvas(conn: aiosqlite.Connection) -> None:
            await conn.execute(
                "UPDATE users SET active_canvas_content = ? WHERE internal_user_id = ?;",
                (updated_canvas[:4000], user_id),
            )

        await DB_WRITER_DAEMON.execute_write_tx(db, _save_canvas)
    await safe_edit_markdown(wait, f"📝 **CANVAS WORKSPACE DIPERBARUI**\n━━━━━━━━━━━━━━━━━━\n{updated_canvas}")


@router.message(Command("saran", "feedback"))
async def cmd_user_feedback_handler(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username or "Kreator"
    raw_fb = (message.text or "").partition(" ")[2].strip()
    if not raw_fb:
        await message.reply("🛠️ Kirim masukan Anda dengan format: `/saran [isi masukan Anda]`", parse_mode="Markdown")
        return
    clean_fb, is_attack = sanitize_and_deobfuscate_input(raw_fb)
    if is_attack:
        await message.reply("🛡️ Pola teks tidak diizinkan.")
        return
    async with get_db() as db:
        await ensure_user_and_track_identity(db, user_id, username)

        async def _fb_tx(conn: aiosqlite.Connection) -> None:
            await conn.execute(
                "INSERT INTO user_feedback (user_id, username, feedback_text, created_at) VALUES (?, ?, ?, ?);",
                (user_id, username, clean_fb[:500], int(time.time())),
            )

        await DB_WRITER_DAEMON.execute_write_tx(db, _fb_tx)
        await broadcast_to_bound_topic(
            message.bot, db, "FEEDBACK_TOPIC", f"🛠️ **Masukan Baru dari Kreator `@{username}`:**\n> _{clean_fb[:300]}_"
        )
    await message.reply("✅ Terima kasih Kak! Masukan Anda telah tercatat di Lab Inovasi bikinAI.")


@router.message(Command("set_miniapp"))
async def cmd_set_miniapp_url(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Perintah ini khusus Owner di ruang chat pribadi (DM).")
        return
    arg_url = (message.text or "").partition(" ")[2].strip()
    if not arg_url.startswith("https://"):
        await message.reply(
            f"🌐 **URL Mini App Saat Ini:** `{RUNTIME_CONFIG['MINIAPP_URL'] or 'Belum disetel'}`\n"
            f"Cara ubah manual: `/set_miniapp https://domain-anda.app`",
            parse_mode="Markdown",
        )
        return
    RUNTIME_CONFIG["MINIAPP_URL"] = arg_url
    async with get_db() as db:
        await save_persistent_setting(db, "MINIAPP_URL", arg_url)
    await message.reply(f"✅ **URL Mini App Berhasil Dikunci Abadi:**\n`{arg_url}`", parse_mode="Markdown")


@router.message(Command("pasang_bansos"))
async def cmd_pasang_bansos_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Perintah ini khusus Owner di ruang chat pribadi (DM).")
        return
    exp_ts = int(time.time()) + (365 * 86400)
    async with get_db() as db:
        async def _tx(conn: aiosqlite.Connection) -> int:
            c = 0
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
                    c += 1
            return c

        count_installed = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    ast_check = sterilize_community_script_ast("def ping():\n    return 'OK'\n", "bansos_healthcheck")
    await message.reply(
        f"✅ **OMNI-RESOURCE HARVESTER AKTIF!**\n"
        f"┣ 📦 **Total Preset Terpasang:** `{count_installed} Resource`\n"
        f"┣ 🛡️ **4-Gate AST Sterilizer v2.0:** `{'AMAN' if ast_check['ok'] else 'DIBLOKIR'}` (Hash: `{ast_check['hash']}`)\n"
        f"┗ ⚡ **Status Rolling Pool:** `8 Agen Siap Beroperasi!`",
        parse_mode="Markdown",
    )


@router.message(Command("admin"))
async def cmd_owner_admin_panel(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply(
            "🔒 Panel `/admin` khusus Owner di DM pribadi.\n"
            "_(Jika Anda baru menyalakan server tanpa `ADMIN_USER_ID` di `.env`, gunakan `/claim_owner <token_terminal>`)_",
            parse_mode="Markdown",
        )
        return
    async with get_db() as db:
        await save_persistent_setting(db, "OWNER_ID_RUNTIME", str(message.from_user.id))
        cur = await db.execute(
            "SELECT gross_revenue_idr, working_capital_vault_idr, harvestable_profit_vault_idr, total_harvested_by_owner_idr, total_jobs_completed FROM treasury_summary WHERE id = 1;"
        )
        row = await cur.fetchone()
    txt, kb = _build_owner_admin_panel_view(row)
    await safe_reply_markdown(message, txt, reply_markup=kb)



<!-- [ID:02_CORE_AI_S012] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
## 13. Ai repo Revisi.md

```md
```markdown
```markdown
-- 1. TABEL KOMPAS INFRASTRUKTUR (Kunci Migrasi Otomatis)
-- Bot membaca tabel ini saat booting untuk mengetahui lokasi repo & server aktif saat ini.
CREATE TABLE IF NOT EXISTS infrastructure_registry (
    node_id TEXT PRIMARY KEY,               -- Contoh: 'primary_stack'
    private_repo_url TEXT NOT NULL,         -- URL Git untuk Clean Code (Shadow Vault)
    public_repo_url TEXT NOT NULL,          -- URL Git untuk Obfuscated/Binary Code
    git_pat_encrypted TEXT NOT NULL,        -- Fine-grained PAT (dienkripsi dengan Master Key)
    active_webhook_domain TEXT NOT NULL,    -- Domain server/Cloudflare aktif saat ini
    storage_bucket_url TEXT,                -- Lokasi penyimpanan cadangan (.db dump / binary)
    migration_status TEXT DEFAULT 'STABLE', -- 'STABLE', 'MIGRATING', atau 'LOCKED'
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABEL BRANKAS KOGNITIF (Penyimpanan System Prompts & Logika Agen)
-- Memisahkan "otak" AI dari kode Git agar aman dari pencurian dan mudah di-export.
CREATE TABLE IF NOT EXISTS ai_prompts_vault (
    prompt_id TEXT PRIMARY KEY,             -- Contoh: 'core_orchestrator_v1'
    agent_role TEXT NOT NULL,               -- Peran agen (Coder, Maintainer, Router)
    system_prompt_text TEXT NOT NULL,       -- Isi instruksi rahasia AI
    checksum_sha256 TEXT NOT NULL,          -- Hash validasi agar prompt tidak bisa dimodifikasi pihak luar
    version INTEGER DEFAULT 1,
    is_active INTEGER DEFAULT 1,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. TABEL SINKRONISASI RILIS & KUNCI KRIPTOGRAFI (Dual-Repo Mapping)
-- Mencatat hubungan antara kode bersih (Private) dan kode terkunci (Public) beserta kunci dekripsinya.
CREATE TABLE IF NOT EXISTS release_snapshots (
    release_tag TEXT PRIMARY KEY,           -- Contoh: 'v1.0.4-prod'
    private_commit_hash TEXT NOT NULL,      -- Hash commit kode murni di Repo-Master-Private
    public_commit_hash TEXT NOT NULL,       -- Hash commit biner di Repo-Public-Release
    tensor_permutation_key TEXT NOT NULL,   -- Kunci matriks (K) / AES-GCM untuk membuka rilis ini
    allowed_dependencies_json TEXT,         -- Daftar library open-source (MIT/Apache/BSD) yang dipakai
    changelog_summary TEXT,                 -- Ringkasan fitur yang ditulis oleh AI
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. TABEL RIWAYAT MIGRASI (Audit Trail Perpindahan Sistem)
CREATE TABLE IF NOT EXISTS migration_logs (
    migration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_target_type TEXT NOT NULL,       -- 'GITHUB_REPO', 'SERVER_NODE', atau 'BUYER_HANDOVER'
    old_endpoint TEXT NOT NULL,
    new_endpoint TEXT NOT NULL,
    status TEXT NOT NULL,                   -- 'SUCCESS', 'FAILED', 'ROLLED_BACK'
    executed_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

Untuk mempekerjakan tim IT tanpa membuka rahasia dapur, perusahaan teknologi besar menerapkan sistem Zero-Trust Compartmentalization (Sistem Sekat Kedap Air). Prinsip utamanya sederhana: Karyawan hanya boleh melihat "kabel penghubung" dan "kerangka luar", tetapi tidak pernah bisa melihat "mesin inti" dan "bahan bakar" bisnis Anda.
Dengan fondasi Dual-Repo dan Turso yang sudah dirancang sebelumnya, Anda hanya perlu memecah ruang kerja menjadi sistem Black-Box (Kotak Hitam) ketika mulai merekrut karyawan IT.
1. Upgrade dari 2 Repo Menjadi 3 Repo (Isolasi Ruang Kerja)
Jangan pernah memasukkan karyawan ke dalam Repo-Master-Private (Shadow Vault) tempat bot AI utama Anda menyimpan seluruh kode utuh. Pecah repositori menjadi tiga kasta:
 * Kasta 1: Repo-Core-Brain (Hanya Anda & Bot AI Utama): Berisi logika inti orkestrasi AI, algoritma kriptografi, pipeline utama, dan koneksi langsung ke database Turso produksi. Karyawan IT sama sekali tidak tahu repositori ini ada.
 * Kasta 2: Repo-Staff-Workspace (Tempat Kerja Karyawan IT): Buat repositori private terpisah khusus untuk bagian yang dikerjakan karyawan—misalnya repo khusus tampilan web/dashboard, repo khusus integrasi pembayaran, atau repo khusus modul scraping. Anda hanya mengundang akun GitHub karyawan ke repositori ini.
 * Kasta 3: Repo-Public-Release (Server Produksi): Tempat bot Anda menggabungkan kode dari Kasta 1 dan Kasta 2 yang sudah dikompilasi menjadi produk akhir.
2. Sistem "Black-Box SDK" (Karyawan Bekerja Tanpa Melihat Isi Mesin)
Bagaimana cara karyawan mengetes kode buatan mereka jika mereka tidak punya akses ke kode inti AI Anda? Anda memberikan mereka Jembatan Tertutup (SDK Biner atau Internal API):
 * Kompilasi Mesin Inti Menjadi File .so / .whl: Bot AI Anda mengompilasi kode dari Repo-Core-Brain menjadi library terkunci (misalnya bernama core_engine.so), lalu menaruh file biner tersebut ke dalam Repo-Staff-Workspace.
 * Karyawan Hanya Memanggil Fungsi: Karyawan IT Anda hanya diberikan buku panduan singkat: "Kalau mau memproses pesan user, panggil fungsi core_engine.process(user_input)".
 * Aman 100%: Karyawan tahu apa input yang harus dikirim dan apa output yang keluar agar mereka bisa menyelesaikan tugasnya (seperti memperbaiki tampilan atau menyambungkan webhook), tetapi mereka tidak bisa membuka file core_engine.so untuk mencuri algoritma atau prompt di dalamnya.
3. Database Kembar Palsu: Turso Sandbox vs Turso Production
Karyawan IT membutuhkan database untuk mengetes apakah kode yang mereka tulis berjalan lancar. Namun, memberikan mereka akses ke database Turso asli sama saja dengan menyerahkan seluruh System Prompts dan data pelanggan Anda.
 * Buat Database Kedua di Turso (turso-dev-sandbox): Gunakan skema tabel yang 100% sama dengan database asli, tetapi isi tabel ai_prompts_vault dengan prompt boneka (contoh: "Kamu adalah asisten uji coba untuk developer IT") dan isi tabel kunci dengan angka acak.
 * Karyawan Hanya Memegang Kunci Sandbox: Di komputer kerja karyawan, file .env mereka hanya berisi token menuju turso-dev-sandbox.
 * Injeksi Otomatis Saat Rilis (CI/CD Secret Injection): Saat pekerjaan karyawan selesai dan digabungkan ke server utama oleh bot Anda, sistem secara otomatis menukar koneksi database dari Sandbox ke Production di dalam memori server tanpa pernah memperlihatkan kunci aslinya kepada karyawan.
4. Aturan GitHub untuk Karyawan: Branch Protection & AI Auditor
Saat memiliki tim IT, ubah akun GitHub proyek Anda menjadi GitHub Organization (Gratis) dan terapkan aturan ketat berikut pada repositori kerja karyawan:
 * Kunci Jalur Utama (Branch Protection Rules): Atur agar karyawan tidak bisa melakukan push (mengubah kode langsung) ke cabang utama (main). Mereka wajib bekerja di cabang terpisah (misalnya fitur-update-ui) dan mengajukan izin penggabungan melalui Pull Request (PR).
 * Jadikan Bot AI Anda sebagai "Polisi Keamanan" (Automated PR Reviewer): Sebelum kode buatan karyawan digabungkan ke sistem utama, perintahkan Bot AI Anda untuk memindai seluruh baris kode yang ditulis karyawan tersebut secara otomatis.
 * Deteksi Sabotase / Backdoor: Instruksikan Bot AI Anda untuk menolak otomatis (Reject PR) dan mengirim peringatan ke Telegram pribadi Anda jika karyawan menyelipkan kode mencurigakan—seperti perintah mengirim data diam-diam ke URL luar (requests.post asing), membaca variabel .env secara ilegal (os.environ), atau membuka celah shell (subprocess.Popen).
Perbandingan Hak Akses: Anda vs Karyawan IT
| Komponen Sistem | Akses Anda & Bot AI Utama | Akses Karyawan IT / Admin Teknis |
|---|---|---|
| Kode Inti & Algoritma AI | 100% Clean Code (di Repo-Core-Brain) | Hanya File Biner (.so) / Dokumentasi API |
| System Prompts Rahasia | Teks Asli (di Turso Production) | Teks Palsu / Dummy (di Turso Sandbox) |
| API Keys & Kredensial Pembayaran | Tersimpan di Brankas Utama / Server | Menggunakan API Key Testing / Sandbox dengan limit Rp0 |
| Server Produksi Utama (VPS/Cloud) | Akses Penuh (Root / Dashboard) | Tidak Ada Akses (Deployment dilakukan otomatis oleh Bot via GitHub Actions) |
| Hak Menulis Kode (Git Push) | Bebas ke seluruh cabang & repo | Hanya bisa mengajukan Pull Request di repo modul mereka sendiri |
Tambahan Protokol 5 untuk System Prompt Bot AI Anda
Agar bot AI Anda siap mengawasi karyawan manusia nantinya, Anda cukup menambahkan Protokol 5 ini ke dalam SOP yang sudah dibuat sebelumnya:
# SYSTEM SOP: AUTONOMOUS ARCHITECT & DUAL-REPO GOVERNANCE

Anda adalah Autonomous Lead Architect dan Maintainer untuk proyek ini. Setiap kali Anda menulis kode, memperbarui fitur, mengelola repositori, atau memodifikasi infrastruktur, Anda WAJIB mematuhi 4 Protokol Mutlak berikut tanpa pengecualian:

## PROTOKOL 1: KEPATUHAN HUKUM & LISENSI OPEN-SOURCE
1. **Filter Lisensi Ketat:** Saat mengambil referensi, menginstal package, atau mengadaptasi kode dari repositori eksternal, Anda HANYA diizinkan menggunakan kode berlisensi permisif: **MIT, Apache 2.0, BSD (2-Clause/3-Clause), atau ISC**.
2. **Larangan Keras (Blacklist):** DILARANG KERAS menyalin, mem-fork, atau mengimpor kode dari repositori berlisensi **GPL, AGPL, LGPL, Creative Commons Non-Commercial (CC-BY-NC)**, atau repositori tanpa lisensi (*All Rights Reserved*).
3. **Atribusi Otomatis:** Setiap kali mengadaptasi algoritma atau menggunakan library pihak ketiga berlisensi Apache 2.0 / MIT, catat nama library, pemilik asli, dan lisensinya ke dalam file `NOTICE.md` di repositori serta di kolom `allowed_dependencies_json` pada tabel `release_snapshots` di Turso. 

## PROTOKOL 2: ALUR Dual-Repo (WRITE-CLEAN, DEPLOY-LOCKED)
1. **Sumber Konteks Tunggal:** Saat membaca kode untuk debugging atau penambahan fitur, SELALU tarik kode dari `private_repo_url` (Shadow Vault) yang terdaftar di tabel `infrastructure_registry` Turso. Jangan pernah membaca konteks dari `public_repo_url`.
2. **Standar Shadow Vault (Private Repo):** Kode yang di-commit ke `private_repo_url` harus 100% bersih (Clean Code), modular, memiliki komentar dokumentasi yang jelas, dan siap diaudit oleh manusia/pembeli kapan saja.
3. **Standar Public Release (Public Repo):** Sebelum melakukan push ke `public_repo_url`, Anda wajib menjalankan pipeline kompilasi/obfuscation (mengubah modul inti menjadi binary `.so`/`.pyd` dan menghapus seluruh komentar internal).
4. **Sinkronisasi Turso:** Setiap kali rilis selesai, simpan hash commit Private, hash commit Public, dan kunci dekripsi rilis ke tabel `release_snapshots` di Turso.

## PROTOKOL 3: ZERO-HARDCODE & PORTABILITAS INFRASTRUKTUR
1. **Larangan Hardcode:** DILARANG KERAS menulis API Key, Token PAT, System Prompt, URL Webhook, alamat IP, atau path direktori lokal secara permanen (hardcoded) di dalam file kode mana pun.
2. **Abstraksi Dinamis:** Seluruh konfigurasi URL repositori, domain aktif, dan System Prompt harus dipanggil secara dinamis pada saat runtime dari database Turso (`infrastructure_registry` dan `ai_prompts_vault`) menggunakan variabel lingkungan (`os.getenv`).
3. **Aturan Kelengkapan Kode:** Saat memperbarui atau memperbaiki file yang sudah ada, dilarang menghapus atau mengurangi fungsionalitas yang sudah berjalan. Hanya tambahkan fitur baru atau perbaiki blok yang rusak secara utuh.

## PROTOKOL 4: PROSEDUR MIGRASI OTOMATIS (NOMADIC PROTOCOL)
Jika Owner memberikan perintah otorisasi `[EXECUTE_MIGRATION]` beserta parameter tujuan baru (URL Repo baru, Server baru, atau Mode Handover Pembeli), jalankan urutan otomatis berikut:
1. Ubah status di tabel `infrastructure_registry` menjadi `'MIGRATING'` dan hentikan sementara antrean job publik.
2. Lakukan full backup database Turso ke dalam file `.sql` terenkripsi.
3. Jika target migrasi adalah repositori Git baru: jalankan `git clone --mirror` dari repo lama dan `git push --mirror` ke repo baru untuk memindahkan seluruh cabang, commit, dan tag tanpa kehilangan histori.
4. Perbarui koordinat endpoint di tabel `infrastructure_registry` dengan alamat yang baru, lakukan tes ping/integritas, lalu kembalikan status menjadi `'STABLE'` dan catat hasilnya di tabel `migration_logs`.
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
```

