
<!-- [ID:02_CORE_AI_S040] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
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


