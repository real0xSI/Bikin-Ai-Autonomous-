
<!-- [ID:02_CORE_AI_S041] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# 13. CALLBACK HANDLERS (/BANSOS, /ADMIN, CUSTOMER VIEW INSPECTOR, WIZARD & MENU)
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
                await call.answer("🤫 Mode Silent Aktif (100% Profit Owner)!", show_alert=True)
            elif val == "HAPPY_HOUR":
                RUNTIME_CONFIG["BANSOS_OPERATION_MODE"], RUNTIME_CONFIG["HAPPY_HOUR_MODE"] = "HAPPY_HOUR", True
                await save_persistent_setting(db, "BANSOS_OPERATION_MODE", "HAPPY_HOUR")
                await save_persistent_setting(db, "HAPPY_HOUR_MODE", "1")
                await broadcast_to_bound_topic(call.bot, db, "COMMAND_TOPIC", f"🎉 **FLASH HAPPY HOUR DIBUKA!** 🎉\nSeluruh pembuatan Gambar 4K & Video AI di `@{BOT_USERNAME_GLOBAL}` sedang **GRATIS 0 KOIN** sekarang juga!")
                await call.answer("🎉 Mode Happy Hour Aktif & Diumumkan ke Grup!", show_alert=True)
            else:
                RUNTIME_CONFIG["BANSOS_OPERATION_MODE"], RUNTIME_CONFIG["HAPPY_HOUR_MODE"] = "NORMAL", False
                await save_persistent_setting(db, "BANSOS_OPERATION_MODE", "NORMAL")
                await save_persistent_setting(db, "HAPPY_HOUR_MODE", "0")
                await call.answer("🛑 Kembali ke Mode Tarif Komersial Standar.", show_alert=True)
            txt, kb = await _build_bansos_4tab_view(db, "AI_API")
            await safe_edit_markdown(call.message, txt, reply_markup=kb)
            return

        if sub == "ping_all":
            await call.answer("⚡ Menguji kecepatan endpoint...")
            ok_p, ms_p, _ = await ping_and_verify_bansos_endpoint("https://text.pollinations.ai/openai", "openai")
            async def _upd_p(conn: aiosqlite.Connection) -> None:
                await conn.execute("UPDATE omni_resource_registry SET is_live_verified = ? WHERE resource_id = 'API-POLLINATIONS-V1';", (1 if ok_p else 0,))
            await DB_WRITER_DAEMON.execute_write_tx(db, _upd_p)
            txt, kb = await _build_bansos_4tab_view(db, "AI_API")
            await safe_edit_markdown(call.message, f"✅ **Hasil Live Ping Gate:** Pollinations `{ms_p} ms`\n\n{txt}", reply_markup=kb)
            return

        await call.answer()
        txt, kb = await _build_bansos_4tab_view(db, val if sub == "tab" else "AI_API")
        await safe_edit_markdown(call.message, txt, reply_markup=kb)


@router.callback_query(F.data.startswith("adm:"))
async def handle_owner_admin_callbacks(call: CallbackQuery) -> None:
    if not call.message or not is_verified_owner_dm(call.from_user.id, call.message.chat.type):
        await call.answer("🔒 Akses khusus Owner.", show_alert=True)
        return
    act = call.data.split(":", 1)[1]

    async with get_db() as db:
        if act == "harvest":
            ok, harvested_now, total_h = await execute_manual_profit_harvest(db)
            await call.answer(f"🌾 Berhasil memanen Rp {harvested_now:,}! Total: Rp {total_h:,}" if ok else "ℹ️ Belum ada laba bersih baru.", show_alert=True)

        elif act.startswith("view_as_buyer:"):
            sim_zone = 3 if act.endswith(":ID") else 1
            sim_user = {"koin_utama": 60, "koin_bonus": 12, "has_topped_up": True, "ppp_zone": sim_zone, "last_claim_date": "", "safe_uname": "SimulasiPembeli"}
            sample_cap = build_customer_dashboard_caption("SimulasiPembeli", sim_user)
            sample_vid, _ = build_video_wizard_kb(LiveWizardSession(prompt="Contoh Video", modality="VIDEO"))
            sample_img, _ = build_image_wizard_kb(LiveWizardSession(prompt="Contoh Gambar", modality="IMAGE"))
            audit_res = scan_customer_ui_for_leaks([sample_cap, sample_vid, sample_img])
            leak_badge = f"🟢 **BERSIH 100%** (`0/{audit_res['checked_terms']}` istilah teknis bocor)" if audit_res["clean"] else f"🔴 **BOCOR:** `{', '.join(audit_res['leaks'])}`"
            zone_title = "🇮🇩 Pembeli Indonesia (Rupiah/QRIS)" if sim_zone == 3 else "🌍 Pembeli Global (USD/USDT/Stars)"
            buyer_kb = build_customer_main_menu_keyboard(sim_user, is_private=True)
            inspector_rows = list(buyer_kb.inline_keyboard) + [
                [InlineKeyboardButton(text="🇮🇩 Simulasi Pembeli ID", callback_data="adm:view_as_buyer:ID"), InlineKeyboardButton(text="🌍 Simulasi Pembeli Global", callback_data="adm:view_as_buyer:GL")],
                [InlineKeyboardButton(text="⬅️ Kembali ke Panel Rahasia /admin", callback_data="adm:refresh")],
            ]
            await call.answer("👁️ Menampilkan simulasi layar pembeli...")
            await safe_edit_markdown(
                call.message,
                f"👁️ **INSPEKTOR LAYAR PEMBELI & AUDIT PRIVASI**\n━━━━━━━━━━━━━━━━━━\n"
                f"┣ 🎭 **Mode Simulasi:** `{zone_title}`\n┗ 🛡️ **Audit Privasi UI:** {leak_badge}\n━━━━━━━━━━━━━━━━━━\n\n{sample_cap}",
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
                        await BOT_INSTANCE_GLOBAL.send_message(chat_id=uid, text=f"✅ **Pembayaran Tagihan `{inv_id}` (`Rp {amt_idr:,}`) Terverifikasi!**\nSaldo **+{coins_add} Koin Utama (Pro)** telah masuk ke akun Anda.", parse_mode="Markdown")
                    except Exception:
                        pass
                await safe_edit_markdown(call.message, f"✅ **Tagihan `{inv_id}` telah di-ACC (+{coins_add} Koin Utama).**")
            else:
                await call.answer("❌ Tagihan ditolak.", show_alert=True)
                await safe_edit_markdown(call.message, f"❌ **Tagihan `{inv_id}` ditolak oleh Owner.**")
            return

        elif act == "pay_menu" or act.startswith("pay_sub:") or act.startswith("set_id_pg:") or act.startswith("set_gl_pg:"):
            if act.startswith("set_id_pg:"):
                _, cat, prov = act.split(":", 2)
                RUNTIME_CONFIG["ID_ACTIVE_CATEGORY"], RUNTIME_CONFIG["ID_ACTIVE_PROVIDER"] = cat, prov
                await save_persistent_setting(db, "ID_ACTIVE_CATEGORY", cat)
                await save_persistent_setting(db, "ID_ACTIVE_PROVIDER", prov)
                await call.answer(f"🇮🇩 Kasir Lokal dikunci ke: {prov}", show_alert=True)
            elif act.startswith("set_gl_pg:"):
                prov = act.split(":", 1)[1]
                RUNTIME_CONFIG["GLOBAL_ACTIVE_PROVIDER"] = prov
                await save_persistent_setting(db, "GLOBAL_ACTIVE_PROVIDER", prov)
                await call.answer(f"🌍 Kasir Global dikunci ke: {prov}", show_alert=True)

            sub_page = act.split(":", 1)[1] if act.startswith("pay_sub:") else "A"
            await call.answer()
            if sub_page == "A":
                p_txt = f"📲 **SUB-MENU A — KASIR LOKAL: QRIS DIRECT (0% BIAYA)**\n━━━━━━━━━━━━━━━━━━\nAktif: **`{RUNTIME_CONFIG['ID_ACTIVE_PROVIDER']}`**"
                p_kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🟢 QRIS GoPay Merchant (0% Fee)", callback_data="adm:set_id_pg:QRIS_DIRECT:QRIS GoPay Merchant")],
                    [InlineKeyboardButton(text="🟠 QRIS ShopeePay Merchant (0% Fee)", callback_data="adm:set_id_pg:QRIS_DIRECT:QRIS ShopeePay Merchant")],
                    [InlineKeyboardButton(text="🔵 QRIS DANA Bisnis (0% Fee)", callback_data="adm:set_id_pg:QRIS_DIRECT:QRIS DANA Bisnis")],
                    [InlineKeyboardButton(text="➡️ Sub-Menu B (Payment Gateway)", callback_data="adm:pay_sub:B"), InlineKeyboardButton(text="🌐 Sub-Menu C (Kasir Global)", callback_data="adm:pay_sub:C")],
                    [InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
                ])
            elif sub_page == "B":
                p_txt = f"🏦 **SUB-MENU B — KASIR LOKAL: PAYMENT GATEWAY RESMI**\n━━━━━━━━━━━━━━━━━━\nAktif: **`{RUNTIME_CONFIG['ID_ACTIVE_PROVIDER']}`**"
                p_kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🏦 Duitku All-Payment (QRIS/VA)", callback_data="adm:set_id_pg:PG_DUITKU:Duitku All-Payment")],
                    [InlineKeyboardButton(text="🏦 Tripay Payment Gateway", callback_data="adm:set_id_pg:PG_TRIPAY:Tripay QRIS & VA")],
                    [InlineKeyboardButton(text="🏦 Pakasir QRIS Instan", callback_data="adm:set_id_pg:PG_PAKASIR:Pakasir QRIS Instan")],
                    [InlineKeyboardButton(text="🏦 Midtrans Snap QRIS/VA", callback_data="adm:set_id_pg:PG_MIDTRANS:Midtrans Snap QRIS/VA")],
                    [InlineKeyboardButton(text="⬅️ Sub-Menu A (QRIS Direct)", callback_data="adm:pay_sub:A"), InlineKeyboardButton(text="🌐 Sub-Menu C (Kasir Global)", callback_data="adm:pay_sub:C")],
                    [InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
                ])
            else:
                p_txt = f"🌐 **SUB-MENU C — KASIR GLOBAL (PEMBELI LUAR NEGERI)**\n━━━━━━━━━━━━━━━━━━\nAktif: **`{RUNTIME_CONFIG['GLOBAL_ACTIVE_PROVIDER']}`**"
                p_kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="₮ Hanya Crypto USDT (@CryptoBot)", callback_data="adm:set_gl_pg:Hanya Crypto USDT (@CryptoBot)")],
                    [InlineKeyboardButton(text="⭐ Hanya Telegram Stars", callback_data="adm:set_gl_pg:Hanya Telegram Stars")],
                    [InlineKeyboardButton(text="🌐 Aktifkan Keduanya Sekaligus (USDT + Telegram Stars)", callback_data="adm:set_gl_pg:Aktifkan Keduanya (USDT + Telegram Stars)")],
                    [InlineKeyboardButton(text="📲 Sub-Menu A (QRIS Direct)", callback_data="adm:pay_sub:A"), InlineKeyboardButton(text="🏦 Sub-Menu B (Payment Gateway)", callback_data="adm:pay_sub:B")],
                    [InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
                ])
            await safe_edit_markdown(call.message, p_txt, reply_markup=p_kb)
            return

        elif act.startswith("manual:"):
            chap = act.split(":", 1)[1]
            await call.answer()
            manuals = {
                "1": "📖 **BAB 1/4: SETUP & IKATAN GRUP**\n1. Masukkan bot ke Supergroup & beri izin **Manage Topics**.\n2. Ketik `/setup_grup` untuk otomatis membuat & mengikat 6 kamar topik.\n3. Gunakan `/ikat` jika ingin mengikat topik lama/mengganti nama topik.",
                "2": "📖 **BAB 2/4: KASIR 3-TIER PPP & INSPEKTOR PEMBELI**\n1. Kasir menyajikan 3 Tier: **Hemat (`Rp 5.000`)**, **Pro (`Rp 25.000`)**, dan **Sultan VIP (`Rp 250.000`)**.\n2. Gunakan tombol **👁️ Lihat Layar sebagai Pembeli** untuk mengaudit tampilan dan memastikan 0% kebocoran istilah teknis.\n3. Ketik `/harvest` untuk memanen laba bersih.",
                "3": "📖 **BAB 3/4: BANSOS, ROLLING AGENT & GANTI NAMA WEB**\n1. Ketik `/set_webname [Nama Baru]` untuk mengganti merek Website Freedom Anda.\n2. Ketik `/bansos` untuk mengatur saklar **Mode Silent** vs **Happy Hour**.\n3. Ketik `/rolling` untuk memutar 8 agen (Argon, Qwen, DeepSeek, Muse, Nano-Muse, Harness, Hermes, Groq).",
                "4": "📖 **BAB 4/4: CUSTOM DOMAIN & GITOPS OTONOM**\n1. Isi `CUSTOM_WEB_DOMAIN=domainanda.app` di `.env` agar pengunjung domain Anda langsung melihat Website Freedom utuh.\n2. Database abadi tersimpan aman di `~/.bikinai_vault/bikinai_master_vault.db`.",
            }
            m_kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f"{'✅ ' if chap=='1' else ''}Bab 1: Grup", callback_data="adm:manual:1"), InlineKeyboardButton(text=f"{'✅ ' if chap=='2' else ''}Bab 2: Kasir/VIP", callback_data="adm:manual:2")],
                [InlineKeyboardButton(text=f"{'✅ ' if chap=='3' else ''}Bab 3: Bansos/Web", callback_data="adm:manual:3"), InlineKeyboardButton(text=f"{'✅ ' if chap=='4' else ''}Bab 4: Domain/Git", callback_data="adm:manual:4")],
                [InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
            ])
            await safe_edit_markdown(call.message, manuals.get(chap, manuals["1"]), reply_markup=m_kb)
            return

        elif act == "rolling":
            nxt = rotate_primary_agent()
            await save_persistent_setting(db, "PRIMARY_ROLLING_AGENT", nxt)
            await call.answer(f"🔄 Otak utama diputar ke: {nxt}", show_alert=True)
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
                ("SUBBOT_SANGMATA_ACTIVE", "🕵️ Identity History Tracker (Silent Log)"),
                ("SUBBOT_WELCOME_GUARD_ACTIVE", "🛡️ Cyber Welcome Gate"),
                ("SUBBOT_NEURAL_FEED_ACTIVE", "⚡ Live Neural Feed Broadcaster"),
                ("SUBBOT_REFUND_SWEEPER_ACTIVE", "🔄 Auto-Refund Watchdog (60s)"),
                ("SUBBOT_SOCIAL_POSTER_ACTIVE", "📣 Social Viral Auto-Poster"),
            ]
            sb_rows = [[InlineKeyboardButton(text=f"{'🟢 ON' if RUNTIME_CONFIG[k] else '🔴 OFF'} — {label}", callback_data=f"adm:toggle_sb:{k}")] for k, label in sb_keys]
            sb_rows.append([InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")])
            await safe_edit_markdown(call.message, "🤖 **PUSAT 5 SUB-BOT & GUARD OPERASIONAL**", reply_markup=InlineKeyboardMarkup(inline_keyboard=sb_rows))
            return
        else:
            await call.answer("🔄 Data disegarkan.")

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
        await call.answer("⏳ Mohon tunggu sejenak...", show_alert=False)
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
            await safe_edit_markdown(call.message, f"📱 **SUPER MINI APP STUDIO**\n━━━━━━━━━━━━━━━━━━\n🌐 **Tautan Studio Web:** `{m_url}`", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]))
            return
        if action == "wizard_video":
            await call.answer()
            sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(prompt="Suasana malam sinematik jalanan kota futuristik, pantulan lampu neon 4K", modality="VIDEO", upscale_mode="VIDEO_4K_60FPS")
            sess.modality = "VIDEO"
            ACTIVE_DRAFTS[user_id] = sess
            txt, kb = build_video_wizard_kb(sess)
            await safe_edit_markdown(call.message, txt, reply_markup=kb)
            return
        if action == "wizard_image":
            await call.answer()
            sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(prompt="Katalog produk kopi susu kekinian di atas meja kayu estetis, pencahayaan studio 4K", modality="IMAGE", upscale_mode="PHOTO_FACE_4K")
            sess.modality = "IMAGE"
            ACTIVE_DRAFTS[user_id] = sess
            txt, kb = build_image_wizard_kb(sess)
            await safe_edit_markdown(call.message, txt, reply_markup=kb)
            return
        if action == "wizard_edit":
            await call.answer()
            sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(prompt="Katalog produk botol parfum mewah di atas meja marmer", modality="EDIT_IMAGE")
            sess.modality = "EDIT_IMAGE"
            ACTIVE_DRAFTS[user_id] = sess
            txt, kb = build_editing_tools_wizard_kb(sess)
            await safe_edit_markdown(call.message, txt, reply_markup=kb)
            return
        if action == "prompt_helper":
            await call.answer("🪄 Meracik ide prompt sinematik...")
            await increment_user_usage_counter(db, user_id, is_render=False)
            sample = await generate_frontier_ai_response(db, "Produk kuliner dan fashion UMKM kualitas iklan televisi 4K", mode="PROMPT_ARCHITECT", personal_memory=u["memory"])
            await safe_edit_markdown(call.message, f"{sample}\n\n💡 _Ketik langsung ide Anda di ruang chat dengan awalan **\"prompt [ide Anda]\"**!_", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]))
            return
        if action == "deep_research_hint":
            await call.answer()
            await safe_edit_markdown(call.message, "🔬 **DEEP RESEARCH — bikinAI**\nKetik `/riset [topik]` di ruang chat untuk membedah strategi bisnis atau tren pasar.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]))
            return
        if action == "canvas_hint":
            await call.answer()
            await safe_edit_markdown(call.message, f"📝 **CANVAS WORKSPACE — bikinAI**\n━━━━━━━━━━━━━━━━━━\n{u['canvas'] or '_(Belum ada draf aktif)_'}\n\n▸ Ketik `/canvas [instruksi]` di ruang chat.", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]))
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
            await call.answer(f"🎟️ Menyiapkan Kode Akses VIP {web_brand}...")
            voucher_str = issue_stateless_ed25519_voucher(user_id, compute_units=units_issued)
            await safe_edit_markdown(
                call.message,
                f"🌐 **{web_brand.upper()} — PLATFORM WEB CREATIVE FREEDOM**\n━━━━━━━━━━━━━━━━━━\n"
                f"🎟️ **Kode Akses VIP Anda (+{units_issued} Kredit Studio):**\n`{voucher_str}`\n\n"
                f"🔗 **Buka Website Studio Lengkap (Chat Bebas, Render & Download CDN):**\n{portal_url}\n\n"
                f"ℹ️ _Salin Kode Akses VIP di atas dan masukkan pada menu **Kode Akses VIP** di website untuk menggunakan seluruh koleksi SOTA dan mengunduh hasil via Link CDN._",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]),
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
                f"📊 **STATUS KUOTA HARIAN & DOMPET KOIN**\n━━━━━━━━━━━━━━━━━━\n"
                f"┣ 📈 **Bar Koin Bonus:** `[{bar_visual}]` (`{u['koin_bonus']}/{MAX_KOIN_BONUS_CAP}`)\n"
                f"┣ 💎 **Koin Utama (Pro):** `{u['koin_utama']} Koin`\n"
                f"┣ 💬 **Teman Diskusi AI:** `🟢 24 Jam Gratis ({u['chat_used_today']} Obrolan)`\n"
                f"┣ 🖼️ **Karya Visual Hari Ini:** `{u['free_img_used_today']} Karya`\n"
                f"┣ ⏳ **Reset Harian (00:00 WIB):** `{rem_sec // 3600} Jam {(rem_sec % 3600) // 60} Menit Lagi`\n"
                f"┗ 🌏 **Tarif Wilayah:** `Zona {u['ppp_zone']} (~Rp {ppp_rate}/Koin)`",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]),
            )
            return
        if action == "claim_daily":
            today_str = time.strftime("%Y-%m-%d")
            if u["last_claim_date"] == today_str:
                await call.answer("🎁 Koin harian sudah Anda klaim hari ini! Kembali lagi besok ya 😊", show_alert=True)
                return
            if u["koin_bonus"] >= MAX_KOIN_BONUS_CAP:
                await call.answer(f"🎁 Koin Bonus sudah penuh ({MAX_KOIN_BONUS_CAP} Koin)! Yuk pakai berkarya dulu.", show_alert=True)
                return
            async def _claim_tx(conn: aiosqlite.Connection) -> int:
                await conn.execute("UPDATE users SET koin_bonus = MIN(?, koin_bonus + 4), last_claim_date = ? WHERE internal_user_id = ?;", (MAX_KOIN_BONUS_CAP, today_str, user_id))
                cur = await conn.execute("SELECT koin_bonus FROM users WHERE internal_user_id = ?;", (user_id,))
                r = await cur.fetchone()
                return int(r[0]) if r else u["koin_bonus"]
            u["koin_bonus"] = await DB_WRITER_DAEMON.execute_write_tx(db, _claim_tx)
            u["last_claim_date"] = today_str
            await call.answer(f"🎉 Berhasil klaim +4 Koin Gratis! Saldo Bonus: {u['koin_bonus']}/{MAX_KOIN_BONUS_CAP}", show_alert=True)
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
                    pay_buttons.append([InlineKeyboardButton(text="₮ Bayar via Crypto USDT (@CryptoBot)", url="https://t.me/CryptoBot")])
                if "Stars" in gl_pref or "Keduanya" in gl_pref:
                    pay_buttons.append([InlineKeyboardButton(text=f"⭐ Bayar via Telegram Stars ({inv['display_amount']})", callback_data=f"menu:topup_verify:{inv['invoice_id']}")])
            pay_buttons.append([InlineKeyboardButton(text=f"✅ Konfirmasi Pembayaran (+{inv['coins']} Koin Utama)", callback_data=f"menu:topup_verify:{inv['invoice_id']}")])
            pay_buttons.append([InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")])

            await safe_edit_markdown(
                call.message,
                f"💳 **KASIR OTOMATIS & PAKET SULTAN VIP — bikinAI**\n━━━━━━━━━━━━━━━━━━\n"
                f"┣ 📦 **Paket Dipilih:** **`{inv['pkg_name']}`**\n"
                f"┣ 🧾 **Nomor Tagihan:** `{inv['invoice_id']}`\n"
                f"┣ 🏦 **Metode Aktif:** `{inv['provider']}`\n"
                f"┣ 💰 **Total Tagihan:** **`{inv['display_amount']}`**\n"
                f"┗ 💎 **Koin Diterima:** **`+{inv['coins']} Koin Utama (Lisensi Komersial Bersih)`**\n"
                f"{qris_block}\n⚡ _Pilih paket di bawah atau klik tombol konfirmasi setelah menyelesaikan pembayaran:_",
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
                        text=f"🔔 **PERMINTAAN VERIFIKASI TOP-UP BARU**\n┣ 👤 **Pembeli:** `@{username}` (ID: `{user_id}`)\n┗ 🧾 **Tagihan:** `{inv_id}`",
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ ACC Tagihan Ini", callback_data=f"adm:acc_inv:{inv_id}"), InlineKeyboardButton(text="❌ Tolak", callback_data=f"adm:rej_inv:{inv_id}")]]),
                    )
                except Exception:
                    pass
            await call.answer("⏳ Permintaan konfirmasi Anda telah dikirim ke sistem kasir! Koin Utama akan otomatis masuk begitu pembayaran terverifikasi.", show_alert=True)
            return

        if action == "live_support":
            await call.answer()
            cur = await db.execute("SELECT job_id FROM jobs WHERE internal_user_id = ? AND status = 'PROCESSING' AND refunded_lock = 0 ORDER BY created_at DESC LIMIT 1;", (user_id,))
            stuck_row = await cur.fetchone()
            refund_note = f"\n✅ **Garansi Koin Kembali 100%:** Koin dari pesanan `{stuck_row[0]}` telah dikembalikan utuh ke saldo Anda!\n" if (stuck_row and await refund_failed_job(db, stuck_row[0])) else ""
            await safe_edit_markdown(
                call.message,
                f"🎧 **PUSAT BANTUAN & GARANSI KOIN KEMBALI 100%**\n━━━━━━━━━━━━━━━━━━{refund_note}\n"
                f"▸ **Jaminan Auto-Refund 60 Detik:** Setiap pesanan yang terkendala jaringan otomatis dikembalikan koinnya 100%.\n"
                f"▸ **Kirim Saran Fitur:** Ketik `/saran [masukan Anda]`.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]),
            )
            return

        if action == "faq_tos":
            await call.answer()
            bindings = await get_all_topic_bindings(db)
            lines_b = []
            for _, (c_id, t_id, t_title) in bindings.items():
                clean_cid = str(c_id).replace("-100", "")
                lines_b.append(f"▸ [{t_title}](https://t.me/c/{clean_cid}/{t_id})" if (clean_cid.isdigit() and t_id > 0) else f"▸ **{t_title}**")
            topic_info = "\n".join(lines_b) if lines_b else "_(Gunakan `/setup_grup` di grup komunitas untuk mengaktifkan tautan langsung ke 6 kamar topik)_"
            m_url = RUNTIME_CONFIG["MINIAPP_URL"] or f"https://t.me/{BOT_USERNAME_GLOBAL}"
            await safe_edit_markdown(
                call.message,
                f"📜 **PANDUAN PROMPT AWAM, FAQ & TAUTAN KOMUNITAS**\n━━━━━━━━━━━━━━━━━━\n"
                f"🪄 **Rumus Prompt Mudah bagi Pemula:**\n"
                f"Gunakan pola: **[Objek] + [Gerakan/Gaya] + [Pencahayaan]**.\n"
                f"• _Contoh Foto Jadi Video:_ Kirim foto produk/wajah Anda langsung ke chat, lalu klik tombol **Gerakkan Gambar Ini Jadi Video 9:16**!\n\n"
                f"⚖️ **Lisensi Komersial Bersih & Garansi Koin 100%:**\n"
                f"Koin Utama memberikan hak komersial penuh bebas watermark, dan koin dijamin kembali 100% jika render gagal.\n\n"
                f"🔗 **Tautan Aktif Ekosistem bikinAI:**\n"
                f"▸ [📱 Peluncur Super Mini App Studio]({m_url})\n"
                f"{topic_info}",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]),
            )
            return


@router.callback_query(F.data.startswith("wiz:"))
async def handle_wizard_callbacks(call: CallbackQuery) -> None:
    user_id, username = call.from_user.id, call.from_user.username or "Kreator"
    parts = call.data.split(":", 2)
    if len(parts) < 3:
        await call.answer()
        return
    sub_cmd, val = parts[1], parts[2]

    sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(prompt="Katalog produk sinematik pencahayaan studio 4K", modality="IMAGE")
    ACTIVE_DRAFTS[user_id] = sess

    if sub_cmd == "prompt" and val == "edit":
        WAITING_PROMPT_EDIT_USERS.add(user_id)
        await call.answer("✏️ Silakan ketik konsep baru Anda di ruang chat!", show_alert=True)
        await call.message.reply("✏️ **Ketik dan kirimkan deskripsi / konsep baru Anda sekarang di ruang chat ini:**", parse_mode="Markdown")
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
        title_p, mod_p = AWAM_VIDEO_MOTION_PRESETS.get(val, ("Motion Sinematik", "smooth camera motion"))
        sess.awam_preset = title_p
        if mod_p not in sess.prompt:
            sess.prompt = f"{sess.prompt}, {mod_p}"[:180]
    elif sub_cmd == "ipre":
        title_p, mod_p = AWAM_IMAGE_STYLE_PRESETS.get(val, ("Gaya Studio", "luxury studio lighting"))
        sess.awam_preset = title_p
        if mod_p not in sess.prompt:
            sess.prompt = f"{sess.prompt}, {mod_p}"[:180]
    elif sub_cmd == "etool":
        sess.edit_tool, sess.modality = val, "EDIT_IMAGE"
        if val == "IMG2VID_MOTION":
            sess.upscale_mode = "VIDEO_4K_60FPS"
    elif sub_cmd == "ups":
        sess.upscale_mode = val
    elif sub_cmd == "more_vid":
        await call.answer()
        txt, kb = build_video_wizard_kb(sess, show_more=(val == "1"))
        await safe_edit_markdown(call.message, txt, reply_markup=kb)
        return
    elif sub_cmd == "more_img":
        await call.answer()
        txt, kb = build_image_wizard_kb(sess, show_more=(val == "1"))
        await safe_edit_markdown(call.message, txt, reply_markup=kb)
        return
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

            await call.answer("🚀 Memulai pembuatan karya...")
            await safe_edit_markdown(call.message, f"⏳ **SEDANG MEMPROSES KARYA ANDA...**\n┣ 🆔 **Pesanan:** `{job_id}`\n┣ ⚡ **Mesin AI:** `{engine_label}` ({sess.aspect_ratio})\n┗ 💳 **Status Koin:** `{deduct_msg}`")
            ups_label = UPSCALER_WHITE_LABEL.get(sess.upscale_mode, "🔍 Pertajam Foto & Wajah 4K")
            try:
                if is_vid_exec:
                    await call.message.answer_video(
                        video=SAMPLE_SANDBOX_VIDEO_URL,
                        caption=f"🎬 **VIDEO AI SELESAI DIBUAT!**\n┣ ⚡ **Mesin AI:** `{engine_label}` ({sess.aspect_ratio} • {sess.duration_sec} Detik)\n┣ 🔍 **Kualitas:** `{ups_label}`\n┗ 📝 **Konsep:** _{sess.prompt[:120]}_",
                        parse_mode="Markdown",
                        reply_markup=build_400_percent_derivative_upsell_kb(),
                    )
                elif sess.modality == "EDIT_IMAGE" and sess.edit_tool == "REMOVE_BG_PNG":
                    img_bytes = await fetch_clean_image_bytes(f"{sess.prompt}, isolated subject on pure transparent background, PNG cutout", 768, 768)
                    if not img_bytes:
                        raise RuntimeError("Gagal mengambil stream PNG.")
                    await call.message.answer_document(
                        document=BufferedInputFile(img_bytes, filename=f"bikinAI_Transparan_{int(time.time())}.png"),
                        caption=f"✂️ **FILE PNG TRANSPARAN KUALITAS TINGGI SELESAI!**\n┗ 🔍 **Kualitas:** `{ups_label}`",
                        parse_mode="Markdown",
                        reply_markup=build_400_percent_derivative_upsell_kb(),
                    )
                else:
                    w, h = (768, 1024) if sess.aspect_ratio == "9:16" else ((1024, 768) if sess.aspect_ratio == "16:9" else (1024, 1024))
                    img_bytes = await fetch_clean_image_bytes(f"{sess.prompt}, {engine_label} style, 8k photorealistic masterpiece", w, h)
                    if not img_bytes:
                        raise RuntimeError("Gagal merender gambar.")
                    await call.message.answer_photo(
                        photo=BufferedInputFile(img_bytes, filename="bikinAI_Studio_4K.jpg"),
                        caption=f"✨ **GAMBAR 4K SELESAI DIBUAT!**\n┣ ⚡ **Mesin AI:** `{engine_label}` ({sess.aspect_ratio})\n┣ 🔍 **Kualitas:** `{ups_label}`\n┗ 📝 **Deskripsi:** _{sess.prompt[:120]}_",
                        parse_mode="Markdown",
                        reply_markup=build_400_percent_derivative_upsell_kb(),
                    )
                await increment_user_usage_counter(db, user_id, is_render=True)
                await mark_job_completed(db, job_id, sess.prompt, engine_label)
                stats = await record_job_and_split_profit(db, revenue_idr=coins * 84, actual_hpp_idr=hpp_idr)
                await broadcast_to_bound_topic(call.bot, db, "ACTIVITY_TOPIC", f"⚡ **Live Neural Feed #{stats['fomo_counter']}**\nKreator `@{username}` baru saja membuat karya dengan **`{engine_label}`** ({sess.aspect_ratio})!")
            except Exception:
                await refund_failed_job(db, job_id)
                await safe_edit_markdown(call.message, f"🛡️ **Garansi Koin Kembali 100% (Auto-Refund):** Terjadi kendala jaringan saat memproses `{job_id}`. Koin Anda telah dikembalikan utuh!")
        return

    await call.answer()
    txt, kb = build_video_wizard_kb(sess) if sess.modality == "VIDEO" else (build_image_wizard_kb(sess) if sess.modality == "IMAGE" else build_editing_tools_wizard_kb(sess))
    await safe_edit_markdown(call.message, txt, reply_markup=kb)


@router.callback_query(F.data.startswith("drv:"))
async def handle_derivative_upsell_callbacks(call: CallbackQuery) -> None:
    user_id, username = call.from_user.id, call.from_user.username or "Kreator"
    drv_type = call.data.split(":", 1)[1]
    sess = ACTIVE_DRAFTS.get(user_id)
    base_prompt = sess.prompt if sess else "Cinematic 4K YouTube & TikTok poster thumbnail"
    cost = 10 if drv_type == "clean_license" else 4
    async with get_db() as db:
        await ensure_user_and_track_identity(db, user_id, username)
        ok, job_id, deduct_msg = await deduct_user_coins_for_job(db, user_id, cost, True, base_prompt, f"DRV_{drv_type.upper()}")
        if not ok:
            await call.answer(f"⚠️ {deduct_msg}", show_alert=True)
            return
        if drv_type == "poster4k":
            await call.answer("🖼️ Membuat Poster Thumbnail 4K...", show_alert=False)
            img_bytes = await fetch_clean_image_bytes(f"{base_prompt}, Cinematic 4K YouTube & TikTok poster thumbnail, vibrant lighting, 8k", 1024, 768)
            if img_bytes:
                await call.message.answer_photo(photo=BufferedInputFile(img_bytes, filename="bikinAI_Poster_4K.jpg"), caption=f"🖼️ **Poster Thumbnail 4K Siap Dipakai!**\n┗ 💳 `{deduct_msg}`", parse_mode="Markdown")
                await mark_job_completed(db, job_id, base_prompt, "DRV_POSTER_4K")
                await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            else:
                await refund_failed_job(db, job_id)
                await call.answer("🛡️ Gagal mengambil gambar, koin Anda telah dikembalikan 100%.", show_alert=True)
        elif drv_type == "audiomp3":
            await mark_job_completed(db, job_id, base_prompt, "DRV_AUDIO_MP3")
            await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            await call.answer("🎵 Audio MP3 berhasil diekstrak!", show_alert=True)
            await call.message.reply(f"🎵 **EKSTRAKSI AUDIO SOUNDTRACK SELESAI**\n┣ 🆔 **Pesanan:** `{job_id}`\n┗ 💳 **Status:** `{deduct_msg}`", parse_mode="Markdown")
        elif drv_type == "clean_license":
            await mark_job_completed(db, job_id, base_prompt, "DRV_CLEAN_LICENSE")
            await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            await call.answer("✨ Lisensi Komersial Bersih diaktifkan!", show_alert=True)
            await call.message.reply(f"📜 **SERTIFIKAT LISENSI KOMERSIAL BERSIH (PRO)**\n━━━━━━━━━━━━━━━━━━\n┣ 👤 **Pemegang Lisensi:** `@{username}`\n┣ 🆔 **Sertifikat:** `LIC-{job_id}`\n┗ ✅ **Hak Komersial:** `100% Bebas Watermark & Royalti`", parse_mode="Markdown")


