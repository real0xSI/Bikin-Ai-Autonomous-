
<!-- [ID:02_CORE_AI_S042] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
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
                RUNTIME_CONFIG["BANSOS_OPERATION_MODE"] = "SILENT_PROFIT"
                RUNTIME_CONFIG["HAPPY_HOUR_MODE"] = False
                await save_persistent_setting(db, "BANSOS_OPERATION_MODE", "SILENT_PROFIT")
                await save_persistent_setting(db, "HAPPY_HOUR_MODE", "0")
                await call.answer("🤫 Mode Silent Aktif: Memakai sumber daya gratis di balik layar (100% Profit Owner)!", show_alert=True)
            elif val == "HAPPY_HOUR":
                RUNTIME_CONFIG["BANSOS_OPERATION_MODE"] = "HAPPY_HOUR"
                RUNTIME_CONFIG["HAPPY_HOUR_MODE"] = True
                await save_persistent_setting(db, "BANSOS_OPERATION_MODE", "HAPPY_HOUR")
                await save_persistent_setting(db, "HAPPY_HOUR_MODE", "1")
                await broadcast_to_bound_topic(
                    call.bot,
                    db,
                    "COMMAND_TOPIC",
                    "🎉 **FLASH HAPPY HOUR DIBUKA!** 🎉\nSeluruh pembuatan Gambar 4K & Video AI di `@"
                    + BOT_USERNAME_GLOBAL
                    + "` sedang **GRATIS 0 KOIN** sekarang juga! Yuk langsung coba!",
                )
                await call.answer("🎉 Mode Happy Hour Aktif & Pengumuman telah dikirim ke Grup!", show_alert=True)
            else:
                RUNTIME_CONFIG["BANSOS_OPERATION_MODE"] = "NORMAL"
                RUNTIME_CONFIG["HAPPY_HOUR_MODE"] = False
                await save_persistent_setting(db, "BANSOS_OPERATION_MODE", "NORMAL")
                await save_persistent_setting(db, "HAPPY_HOUR_MODE", "0")
                await call.answer("🛑 Kembali ke Mode Tarif Komersial Standar.", show_alert=True)
            txt, kb = await _build_bansos_4tab_view(db, "AI_API")
            await safe_edit_markdown(call.message, txt, reply_markup=kb)
            return

        if sub == "ping_all":
            await call.answer("⚡ Menguji kecepatan & skema JSON seluruh endpoint...")
            ok_p, ms_p, _ = await ping_and_verify_bansos_endpoint("https://text.pollinations.ai/openai", "openai")

            async def _upd_p(conn: aiosqlite.Connection) -> None:
                await conn.execute(
                    "UPDATE omni_resource_registry SET is_live_verified = ? WHERE resource_id = 'API-POLLINATIONS-V1';",
                    (1 if ok_p else 0,),
                )

            await DB_WRITER_DAEMON.execute_write_tx(db, _upd_p)
            txt, kb = await _build_bansos_4tab_view(db, "AI_API")
            await safe_edit_markdown(call.message, f"✅ **Hasil Live Ping Gate:** Pollinations `{ms_p} ms`\n\n{txt}", reply_markup=kb)
            return

        tab_target = val if sub == "tab" else "AI_API"
        await call.answer()
        txt, kb = await _build_bansos_4tab_view(db, tab_target)
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
            if ok:
                await call.answer(f"🌾 Berhasil memanen laba bersih Rp {harvested_now:,}! Total: Rp {total_h:,}", show_alert=True)
            else:
                await call.answer("ℹ️ Belum ada laba bersih baru yang siap dipanen.", show_alert=True)

        elif act.startswith("acc_inv:") or act.startswith("rej_inv:"):
            inv_id = act.split(":", 1)[1]
            if act.startswith("acc_inv:"):
                ok, uid, amt_idr, msg = await approve_invoice_and_credit_coins(db, inv_id)
                await call.answer(msg, show_alert=True)
                if ok and BOT_INSTANCE_GLOBAL:
                    try:
                        await BOT_INSTANCE_GLOBAL.send_message(
                            chat_id=uid,
                            text=f"✅ **Pembayaran Tagihan `{inv_id}` (`Rp {amt_idr:,}`) Terverifikasi!**\nSaldo **+60 Koin Utama (Pro)** telah masuk ke akun Anda.",
                            parse_mode="Markdown",
                        )
                    except Exception:
                        pass
                await safe_edit_markdown(call.message, f"✅ **Tagihan `{inv_id}` telah di-ACC (+60 Koin Utama).**")
            else:
                await call.answer("❌ Tagihan ditolak.", show_alert=True)
                await safe_edit_markdown(call.message, f"❌ **Tagihan `{inv_id}` ditolak oleh Owner.**")
            return

        elif act == "pay_menu" or act.startswith("pay_sub:") or act.startswith("set_id_pg:") or act.startswith("set_gl_pg:"):
            if act.startswith("set_id_pg:"):
                _, cat, prov = act.split(":", 2)
                RUNTIME_CONFIG["ID_ACTIVE_CATEGORY"] = cat
                RUNTIME_CONFIG["ID_ACTIVE_PROVIDER"] = prov
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
                p_txt = (
                    "📲 **SUB-MENU A — KASIR LOKAL: QRIS DIRECT (0% BIAYA)**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"Kasir Lokal Aktif: **`{RUNTIME_CONFIG['ID_ACTIVE_PROVIDER']}`**\n"
                    "Pilih rekening QRIS statis/dinamis utama Anda:"
                )
                p_kb = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="🟢 QRIS GoPay Merchant (0% Fee)", callback_data="adm:set_id_pg:QRIS_DIRECT:QRIS GoPay Merchant")],
                        [InlineKeyboardButton(text="🟠 QRIS ShopeePay Merchant (0% Fee)", callback_data="adm:set_id_pg:QRIS_DIRECT:QRIS ShopeePay Merchant")],
                        [InlineKeyboardButton(text="🔵 QRIS DANA Bisnis (0% Fee)", callback_data="adm:set_id_pg:QRIS_DIRECT:QRIS DANA Bisnis")],
                        [
                            InlineKeyboardButton(text="➡️ Sub-Menu B (Payment Gateway)", callback_data="adm:pay_sub:B"),
                            InlineKeyboardButton(text="🌐 Sub-Menu C (Kasir Global)", callback_data="adm:pay_sub:C"),
                        ],
                        [InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
                    ]
                )
            elif sub_page == "B":
                p_txt = (
                    "🏦 **SUB-MENU B — KASIR LOKAL: PAYMENT GATEWAY RESMI**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"Kasir Lokal Aktif: **`{RUNTIME_CONFIG['ID_ACTIVE_PROVIDER']}`**\n"
                    "Gunakan saat QRIS Direct Anda mendekati batas limit harian/bulanan:"
                )
                p_kb = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="🏦 Duitku All-Payment (QRIS/VA)", callback_data="adm:set_id_pg:PG_DUITKU:Duitku All-Payment")],
                        [InlineKeyboardButton(text="🏦 Tripay Payment Gateway", callback_data="adm:set_id_pg:PG_TRIPAY:Tripay QRIS & VA")],
                        [InlineKeyboardButton(text="🏦 Pakasir QRIS Instan", callback_data="adm:set_id_pg:PG_PAKASIR:Pakasir QRIS Instan")],
                        [InlineKeyboardButton(text="🏦 Midtrans Snap QRIS/VA", callback_data="adm:set_id_pg:PG_MIDTRANS:Midtrans Snap QRIS/VA")],
                        [
                            InlineKeyboardButton(text="⬅️ Sub-Menu A (QRIS Direct)", callback_data="adm:pay_sub:A"),
                            InlineKeyboardButton(text="🌐 Sub-Menu C (Kasir Global)", callback_data="adm:pay_sub:C"),
                        ],
                        [InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
                    ]
                )
            else:
                p_txt = (
                    "🌐 **SUB-MENU C — KASIR GLOBAL (PEMBELI LUAR NEGERI)**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    f"Kasir Global Aktif: **`{RUNTIME_CONFIG['GLOBAL_ACTIVE_PROVIDER']}`**\n"
                    "Pilih metode yang ditampilkan otomatis kepada pembeli luar negeri:"
                )
                p_kb = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="₮ Hanya Crypto USDT (@CryptoBot)", callback_data="adm:set_gl_pg:Hanya Crypto USDT (@CryptoBot)")],
                        [InlineKeyboardButton(text="⭐ Hanya Telegram Stars", callback_data="adm:set_gl_pg:Hanya Telegram Stars")],
                        [InlineKeyboardButton(text="🌐 Aktifkan Keduanya Sekaligus (USDT + Telegram Stars)", callback_data="adm:set_gl_pg:Aktifkan Keduanya (USDT + Telegram Stars)")],
                        [
                            InlineKeyboardButton(text="📲 Sub-Menu A (QRIS Direct)", callback_data="adm:pay_sub:A"),
                            InlineKeyboardButton(text="🏦 Sub-Menu B (Payment Gateway)", callback_data="adm:pay_sub:B"),
                        ],
                        [InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
                    ]
                )
            await safe_edit_markdown(call.message, p_txt, reply_markup=p_kb)
            return

        elif act.startswith("manual:"):
            chap = act.split(":", 1)[1]
            await call.answer()
            manuals = {
                "1": (
                    "📖 **BUKU MANUAL DEVELOPER — BAB 1/4: SETUP & IKATAN GRUP**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "1. Masukkan bot ke Supergroup Telegram Anda dan jadikan Admin dengan izin **Manage Topics (Kelola Topik)**.\n"
                    "2. Ketik `/setup_grup` satu kali di dalam grup: bot otomatis membuat 6 kamar topik unik dan mengikat ID-nya ke database abadi.\n"
                    "3. Jika ingin mengganti nama topik atau mengikat topik lama secara manual, masuk ke topik tersebut lalu ketik `/ikat`."
                ),
                "2": (
                    "📖 **BUKU MANUAL DEVELOPER — BAB 2/4: KASIR & HARVEST**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "1. Pembeli Indonesia otomatis diarahkan ke **Kasir Lokal** (Sub-Menu A/B), sedangkan pembeli luar negeri otomatis melihat **Kasir Global** (Sub-Menu C).\n"
                    "2. Sistem memisahkan **Modal Kerja HPP+10%** dari **Laba Bersih Siap Panen**.\n"
                    "3. Klik tombol **🌾 Panen Laba Bersih** di paling atas `/admin` atau ketik `/harvest` kapan saja untuk menarik laba."
                ),
                "3": (
                    "📖 **BUKU MANUAL DEVELOPER — BAB 3/4: BANSOS & ROLLING AGENT**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "1. Ketik `/bansos` untuk membuka 4-Tab Radar Omni-Resource dan memilih saklar **🤫 Mode Silent (100% Profit)** atau **🎉 Mode Happy Hour**.\n"
                    "2. Ketik `/rolling` atau klik tombol **🔄 Rolling Agent** di `/admin` untuk memutar otak utama lintas 8 agen (Argon, Qwen, DeepSeek, Muse, Nano-Muse, Harness, Hermes, Groq).\n"
                    "3. Komunitas dapat menyumbang endpoint gratis lewat `/donasi_api` yang otomatis disaring oleh **4-Gate Malware Sterilizer**."
                ),
                "4": (
                    "📖 **BUKU MANUAL DEVELOPER — BAB 4/4: DATABASE & TROUBLESHOOTING**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "1. Lokasi database abadi terkunci di `~/.bikinai_vault/bikinai_master_vault.db` sehingga saldo & ikatan topik tidak pernah hilang saat update kode.\n"
                    "2. Port `8080` melayani dua aplikasi web sekaligus: `/` untuk **Super Mini App Studio (SFW)** dan `/unfiltered-portal` untuk **NocturneAI Web Studio (3-Tab)**.\n"
                    "3. Gunakan menu **🤖 Pusat 5 Sub-Bot** untuk memantau SangMata Tracker, Welcome Gate, dan Auto-Refund Watchdog."
                ),
            }
            m_kb = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text=f"{'✅ ' if chap=='1' else ''}Bab 1: Grup", callback_data="adm:manual:1"),
                        InlineKeyboardButton(text=f"{'✅ ' if chap=='2' else ''}Bab 2: Kasir", callback_data="adm:manual:2"),
                    ],
                    [
                        InlineKeyboardButton(text=f"{'✅ ' if chap=='3' else ''}Bab 3: Bansos/AI", callback_data="adm:manual:3"),
                        InlineKeyboardButton(text=f"{'✅ ' if chap=='4' else ''}Bab 4: Teknis", callback_data="adm:manual:4"),
                    ],
                    [InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
                ]
            )
            await safe_edit_markdown(call.message, manuals.get(chap, manuals["1"]), reply_markup=m_kb)
            return

        elif act == "rolling":
            nxt = rotate_primary_agent()
            await save_persistent_setting(db, "PRIMARY_ROLLING_AGENT", nxt)
            await call.answer(f"🔄 Otak utama diputar ke: {nxt} ({AGENTIC_ROLLING_POOL[nxt]['title']})", show_alert=True)

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
                ("SUBBOT_REFUND_SWEEPER_ACTIVE", "🔄 Auto-Refund Watchdog (60s)"),
                ("SUBBOT_SOCIAL_POSTER_ACTIVE", "📣 Social Viral Auto-Poster"),
            ]
            sb_rows = [
                [InlineKeyboardButton(text=f"{'🟢 ON' if RUNTIME_CONFIG[k] else '🔴 OFF'} — {label}", callback_data=f"adm:toggle_sb:{k}")]
                for k, label in sb_keys
            ]
            sb_rows.append([InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")])
            await safe_edit_markdown(
                call.message,
                "🤖 **PUSAT 5 SUB-BOT & GUARD OPERASIONAL — bikinAI**\n━━━━━━━━━━━━━━━━━━\nKlik untuk menyalakan/mematikan sub-bot otonom:",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=sb_rows),
            )
            return
        else:
            await call.answer("🔄 Data disegarkan.")

        cur = await db.execute(
            "SELECT gross_revenue_idr, working_capital_vault_idr, harvestable_profit_vault_idr, total_harvested_by_owner_idr, total_jobs_completed FROM treasury_summary WHERE id = 1;"
        )
        row = await cur.fetchone()

    txt, kb = _build_owner_admin_panel_view(row)
    await safe_edit_markdown(call.message, txt, reply_markup=kb)


@router.callback_query(F.data.startswith("menu:"))
async def handle_customer_menu_callbacks(call: CallbackQuery) -> None:
    action = call.data.split(":", 1)[1]
    user_id = call.from_user.id
    username = call.from_user.username or call.from_user.first_name or "Kreator"
    is_priv = call.message.chat.type == "private" if call.message else True

    async with get_db() as db:
        u = await ensure_user_and_track_identity(
            db, user_id, username, call.from_user.first_name or "", call.from_user.language_code or "id"
        )

        if action == "home":
            await call.answer()
            await safe_edit_markdown(
                call.message,
                build_customer_dashboard_caption(username, u),
                reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
            )
            return

        if action == "miniapp_guide":
            await call.answer()
            m_url = RUNTIME_CONFIG["MINIAPP_URL"] or "http://localhost:8080"
            await safe_edit_markdown(
                call.message,
                f"📱 **SUPER MINI APP STUDIO — bikinAI**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🌐 **Alamat Studio Web:** `{m_url}`\n\n"
                f"▸ Pastikan Port `8080` disetel ke **Public (HTTPS)** jika berjalan di Codespaces, atau gunakan `/set_miniapp https://domain-anda.app`.",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]
                ),
            )
            return

        if action == "wizard_video":
            await call.answer()
            sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(
                prompt="Suasana malam sinematik jalanan kota futuristik, pantulan lampu neon 4K", modality="VIDEO"
            )
            sess.modality = "VIDEO"
            ACTIVE_DRAFTS[user_id] = sess
            txt, kb = build_video_wizard_kb(sess)
            await safe_edit_markdown(call.message, txt, reply_markup=kb)
            return

        if action == "wizard_image":
            await call.answer()
            sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(
                prompt="Katalog produk kopi susu kekinian di atas meja kayu estetis, pencahayaan studio 4K",
                modality="IMAGE",
            )
            sess.modality = "IMAGE"
            ACTIVE_DRAFTS[user_id] = sess
            txt, kb = build_image_wizard_kb(sess)
            await safe_edit_markdown(call.message, txt, reply_markup=kb)
            return

        if action == "wizard_edit":
            await call.answer()
            sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(
                prompt="Katalog produk botol parfum mewah di atas meja marmer", modality="EDIT_IMAGE"
            )
            sess.modality = "EDIT_IMAGE"
            ACTIVE_DRAFTS[user_id] = sess
            txt, kb = build_editing_tools_wizard_kb(sess)
            await safe_edit_markdown(call.message, txt, reply_markup=kb)
            return

        if action == "prompt_helper":
            await call.answer("🪄 Meracik ide prompt sinematik...")
            await increment_user_usage_counter(db, user_id, is_render=False)
            sample = await generate_frontier_ai_response(
                db, "Produk kuliner dan fashion UMKM kualitas iklan televisi 4K", mode="PROMPT_ARCHITECT", personal_memory=u["memory"]
            )
            await safe_edit_markdown(
                call.message,
                f"{sample}\n\n💡 _Ketik langsung ide Anda di ruang chat dengan awalan **\"prompt [ide Anda]\"** untuk dibuatkan racikan baru!_",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]
                ),
            )
            return

        if action == "deep_research_hint":
            await call.answer()
            await safe_edit_markdown(
                call.message,
                "🔬 **DEEP RESEARCH — bikinAI**\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "Gunakan perintah `/riset [topik]` di ruang chat untuk membedah strategi bisnis, tren pasar, atau riset mendalam.\n\n"
                "▸ **Contoh:** `/riset strategi konten video pendek AI untuk UMKM kuliner 2026`",
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
                f"📝 **CANVAS WORKSPACE — bikinAI**\n━━━━━━━━━━━━━━━━━━\n{cur_c}\n\n"
                f"▸ Ketik `/canvas [instruksi]` di ruang chat untuk menulis atau merevisi naskah panjang, skrip iklan, atau kode program.",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]
                ),
            )
            return

        if action == "unfiltered_external_referral":
            base_url = RUNTIME_CONFIG["MINIAPP_URL"] or "http://localhost:8080"
            portal_url = f"{base_url.rstrip('/')}/unfiltered-portal"
            # Mengunci penerbitan voucher penuh bagi pemilik Koin Utama (atau 1 voucher uji coba)
            if u["koin_utama"] >= 4:
                ok_v, _, _ = await deduct_user_coins_for_job(
                    db, user_id, 4, allow_bonus=False, prompt_text="Penerbitan Kode Voucher Studio Web", engine_used="NOCTURNE_VOUCHER"
                )
                units_issued = 15 if ok_v else 5
            else:
                units_issued = 5
            await call.answer("🎟️ Menerbitkan Kode Voucher Studio Web...")
            voucher_str = issue_stateless_ed25519_voucher(user_id, compute_units=units_issued)
            await safe_edit_markdown(
                call.message,
                f"🌐 **NOCTURNE AI — STUDIO WEB OPEN-SOURCE INDEPENDEN**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🎟️ **Kode Voucher Studio Web Anda ({units_issued} Unit Kredit):**\n"
                f"`{voucher_str}`\n\n"
                f"🔗 **Buka Aplikasi Web Studio (3-Tab Live Chat & Render):**\n"
                f"{portal_url}\n\n"
                f"ℹ️ _Salin Kode Voucher di atas dan tukarkan pada Tab 3 di website NocturneAI untuk menggunakan ruang obrolan tanpa filter dan generator model open-weight._",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]
                ),
            )
            return

        if action == "quota":
            await call.answer()
            filled = min(10, int((u["koin_bonus"] / MAX_KOIN_BONUS_CAP) * 10))
            bar_visual = "█" * filled + "░" * (10 - filled)
            now_wib = (int(time.time()) + 7 * 3600) % 86400
            rem_sec = 86400 - now_wib
            rem_h, rem_m = rem_sec // 3600, (rem_sec % 3600) // 60
            ppp_rate = PPP_EFFECTIVE_COIN_IDR.get(u["ppp_zone"], 84)
            await safe_edit_markdown(
                call.message,
                f"📊 **STATUS KUOTA HARIAN & DOMPET KOIN**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"┣ 📈 **Bar Koin Bonus:** `[{bar_visual}]` (`{u['koin_bonus']}/{MAX_KOIN_BONUS_CAP}`)\n"
                f"┣ 💎 **Koin Utama (Pro):** `{u['koin_utama']} Koin`\n"
                f"┣ 💬 **Asisten Chat AI:** `🟢 24 Jam Gratis ({u['chat_used_today']} Pesan Hari Ini)`\n"
                f"┣ 🖼️ **Karya Visual Hari Ini:** `{u['free_img_used_today']} Karya`\n"
                f"┣ ⏳ **Reset Kuota Harian (00:00 WIB):** `{rem_h} Jam {rem_m} Menit Lagi`\n"
                f"┗ 🌏 **Tarif Wilayah:** `Zona {u['ppp_zone']} (~Rp {ppp_rate}/Koin)`",
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
                await call.answer(f"🎁 Koin Bonus Anda sudah penuh ({MAX_KOIN_BONUS_CAP} Koin)! Yuk pakai berkarya dulu.", show_alert=True)
                return

            async def _claim_tx(conn: aiosqlite.Connection) -> int:
                await conn.execute(
                    "UPDATE users SET koin_bonus = MIN(?, koin_bonus + 4), last_claim_date = ? WHERE internal_user_id = ?;",
                    (MAX_KOIN_BONUS_CAP, today_str, user_id),
                )
                cur = await conn.execute("SELECT koin_bonus FROM users WHERE internal_user_id = ?;", (user_id,))
                r = await cur.fetchone()
                return int(r[0]) if r else u["koin_bonus"]

            new_bonus = await DB_WRITER_DAEMON.execute_write_tx(db, _claim_tx)
            u["koin_bonus"] = new_bonus
            u["last_claim_date"] = today_str
            await call.answer(f"🎉 Berhasil klaim +4 Koin Gratis! Saldo Bonus: {new_bonus}/{MAX_KOIN_BONUS_CAP}", show_alert=True)
            await safe_edit_markdown(
                call.message,
                build_customer_dashboard_caption(username, u),
                reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
            )
            return

        if action == "topup_qris":
            await call.answer()
            inv = await create_payment_invoice(db, user_id, u["ppp_zone"])
            qris_block = f"\n📦 **Kode Pembayaran QRIS Instan:**\n`{inv['qris_payload']}`\n" if inv["qris_payload"] else ""
            pay_buttons = []
            if inv["is_global"]:
                gl_pref = RUNTIME_CONFIG["GLOBAL_ACTIVE_PROVIDER"]
                if "USDT" in gl_pref or "Keduanya" in gl_pref:
                    pay_buttons.append([InlineKeyboardButton(text="₮ Bayar via Crypto USDT (@CryptoBot)", url="https://t.me/CryptoBot")])
                if "Stars" in gl_pref or "Keduanya" in gl_pref:
                    pay_buttons.append([InlineKeyboardButton(text=f"⭐ Bayar via Telegram Stars ({inv['display_amount']})", callback_data=f"menu:topup_verify:{inv['invoice_id']}")])
            pay_buttons.append([InlineKeyboardButton(text="✅ Konfirmasi & Cek Status Pembayaran (+60 Koin)", callback_data=f"menu:topup_verify:{inv['invoice_id']}")])
            pay_buttons.append([InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")])

            await safe_edit_markdown(
                call.message,
                f"💳 **KASIR OTOMATIS — bikinAI**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"┣ 🧾 **Nomor Tagihan:** `{inv['invoice_id']}`\n"
                f"┣ 🏦 **Metode Pembayaran:** `{inv['provider']}`\n"
                f"┣ 💰 **Total Tagihan:** **`{inv['display_amount']}`**\n"
                f"┗ 💎 **Paket Pro:** `+60 Koin Utama (Aktifkan Lisensi Komersial Bersih)`\n"
                f"{qris_block}\n"
                f"⚡ _Setelah menyelesaikan pembayaran sesuai nominal unik di atas, klik tombol konfirmasi di bawah ini:_",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=pay_buttons),
            )
            return

        if action.startswith("topup_verify:"):
            inv_id = action.split(":", 1)[1]
            # [PATCH AUDIT-01]: Tidak mengizinkan klaim koin sepihak kecuali disetujui Owner / Webhook PG
            if RUNTIME_CONFIG.get("AUTO_APPROVE_SANDBOX_TOPUP", False) and not RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"]:
                ok, _, _, msg = await approve_invoice_and_credit_coins(db, inv_id)
                await call.answer(msg, show_alert=True)
                u = await ensure_user_and_track_identity(db, user_id, username)
                await safe_edit_markdown(
                    call.message,
                    build_customer_dashboard_caption(username, u),
                    reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
                )
                return

            owner_id = int(RUNTIME_CONFIG.get("OWNER_ID_RUNTIME") or 0)
            if owner_id > 0 and BOT_INSTANCE_GLOBAL:
                try:
                    await BOT_INSTANCE_GLOBAL.send_message(
                        chat_id=owner_id,
                        text=(
                            f"🔔 **PERMINTAAN VERIFIKASI TOP-UP BARU**\n"
                            f"┣ 👤 **Pembeli:** `@{username}` (ID: `{user_id}`)\n"
                            f"┣ 🧾 **Tagihan:** `{inv_id}`\n"
                            f"┗ 🏦 **Kasir:** `{RUNTIME_CONFIG['ID_ACTIVE_PROVIDER']}`"
                        ),
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text="✅ ACC (+60 Koin Utama)", callback_data=f"adm:acc_inv:{inv_id}"),
                                    InlineKeyboardButton(text="❌ Tolak", callback_data=f"adm:rej_inv:{inv_id}"),
                                ]
                            ]
                        ),
                    )
                except Exception:
                    pass
            await call.answer(
                "⏳ Permintaan konfirmasi pembayaran Anda telah dikirim ke sistem kasir! Saldo +60 Koin Utama akan otomatis masuk begitu mutasi terverifikasi.",
                show_alert=True,
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
            if stuck_row and await refund_failed_job(db, stuck_row[0]):
                refund_note = f"\n✅ **Garansi Koin Kembali 100%:** Koin dari pesanan `{stuck_row[0]}` yang tertunda telah dikembalikan utuh ke saldo Anda!\n"

            await safe_edit_markdown(
                call.message,
                f"🎧 **PUSAT BANTUAN & GARANSI KOIN KEMBALI 100%**\n"
                f"━━━━━━━━━━━━━━━━━━{refund_note}\n"
                f"▸ **Jaminan Auto-Refund 60 Detik:** Setiap pembuatan karya yang terkendala jaringan otomatis dikembalikan koinnya 100% tanpa perlu antre admin.\n"
                f"▸ **Kirim Saran Fitur:** Ketik `/saran [masukan Anda]`.\n"
                f"▸ **Butuh Bantuan Langsung?** Cukup ketik pertanyaan Anda di ruang chat ini dan asisten AI kami akan langsung menjawabnya dalam hitungan detik!",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")]]
                ),
            )
            return

        if action == "faq_tos":
            await call.answer()
            bindings = await get_all_topic_bindings(db)
            if bindings:
                lines_b = []
                for k, (c_id, t_id, t_title) in bindings.items():
                    clean_cid = str(c_id).replace("-100", "")
                    if clean_cid.isdigit() and t_id > 0:
                        lines_b.append(f"▸ [{t_title}](https://t.me/c/{clean_cid}/{t_id})")
                    else:
                        lines_b.append(f"▸ **{t_title}**")
                topic_info = "\n".join(lines_b)
            else:
                topic_info = "_(Gunakan `/setup_grup` di grup komunitas untuk mengaktifkan tautan langsung ke 6 kamar topik)_"

            m_url = RUNTIME_CONFIG["MINIAPP_URL"] or f"https://t.me/{BOT_USERNAME_GLOBAL}"
            await safe_edit_markdown(
                call.message,
                f"📜 **PANDUAN, FAQ, KETENTUAN & TAUTAN KOMUNITAS**\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"⚖️ **Lisensi Komersial Bersih:**\n"
                f"Seluruh karya yang dibuat dengan **Koin Utama (Pro)** memberikan hak komersial penuh tanpa watermark.\n\n"
                f"🛡️ **Garansi Koin Kembali 100% & Privasi:**\n"
                f"Informasi lokasi foto dihapus otomatis dan koin dijamin kembali 100% jika proses render gagal.\n\n"
                f"🔗 **Tautan Aktif Ekosistem bikinAI:**\n"
                f"▸ [📱 Peluncur Super Mini App Studio]({m_url})\n"
                f"▸ [🎧 Pusat Bantuan & Auto-Refund](https://t.me/{BOT_USERNAME_GLOBAL}?start=support)\n"
                f"{topic_info}",
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

    sess = ACTIVE_DRAFTS.get(user_id) or LiveWizardSession(
        prompt="Katalog produk sinematik pencahayaan studio 4K", modality="IMAGE"
    )
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
        await safe_edit_markdown(call.message, txt, reply_markup=kb)
        return
    elif sub_cmd == "more_img":
        await call.answer()
        txt, kb = build_image_wizard_kb(sess, show_more=(val == "1"))
        await safe_edit_markdown(call.message, txt, reply_markup=kb)
        return
    elif sub_cmd == "exec":
        coins, hpp_idr, allow_bonus = sess.get_pricing()
        engine_label = (
            sess.video_engine
            if sess.modality == "VIDEO"
            else (sess.image_engine if sess.modality == "IMAGE" else sess.edit_tool)
        )
        async with get_db() as db:
            await ensure_user_and_track_identity(db, user_id, username)
            ok, job_id, deduct_msg = await deduct_user_coins_for_job(
                db, user_id, coins, allow_bonus, sess.prompt, engine_label
            )
            if not ok:
                await call.answer(f"⚠️ {deduct_msg}", show_alert=True)
                return

            await call.answer("🚀 Memulai pembuatan karya...")
            await safe_edit_markdown(
                call.message,
                f"⏳ **SEDANG MEMPROSES KARYA ANDA...**\n"
                f"┣ 🆔 **Nomor Pesanan:** `{job_id}`\n"
                f"┣ ⚡ **Mesin AI:** `{engine_label}` ({sess.aspect_ratio})\n"
                f"┗ 💳 **Status Koin:** `{deduct_msg}`",
            )

            ups_label = UPSCALER_WHITE_LABEL.get(sess.upscale_mode, "🔍 Pertajam Foto & Wajah 4K")
            try:
                if sess.modality == "VIDEO":
                    await call.message.answer_video(
                        video=SAMPLE_SANDBOX_VIDEO_URL,
                        caption=(
                            f"🎬 **VIDEO AI SELESAI DIBUAT!**\n"
                            f"┣ ⚡ **Mesin AI:** `{sess.video_engine}` ({sess.aspect_ratio} • {sess.duration_sec} Detik)\n"
                            f"┣ 🔍 **Kualitas:** `{ups_label}`\n"
                            f"┗ 📝 **Konsep:** _{sess.prompt[:120]}_"
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
                    png_doc = BufferedInputFile(img_bytes, filename=f"bikinAI_Transparan_{int(time.time())}.png")
                    await call.message.answer_document(
                        document=png_doc,
                        caption=(
                            f"✂️ **FILE PNG TRANSPARAN KUALITAS TINGGI SELESAI!**\n"
                            f"┣ 🛠️ **Fitur:** `Hapus Background (File .PNG Utuh)`\n"
                            f"┗ 🔍 **Kualitas:** `{ups_label}`"
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
                            f"✨ **GAMBAR 4K SELESAI DIBUAT!**\n"
                            f"┣ ⚡ **Mesin AI:** `{engine_label}` ({sess.aspect_ratio})\n"
                            f"┣ 🔍 **Kualitas:** `{ups_label}`\n"
                            f"┗ 📝 **Deskripsi:** _{sess.prompt[:120]}_"
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
                    f"Kreator `@{username}` baru saja membuat karya baru dengan **`{engine_label}`** ({sess.aspect_ratio})!",
                )
            except Exception:
                await refund_failed_job(db, job_id)
                await safe_edit_markdown(
                    call.message,
                    f"🛡️ **Garansi Koin Kembali 100% (Auto-Refund):** Terjadi kendala jaringan saat memproses `{job_id}`. Koin Anda telah dikembalikan utuh ke saldo Anda!",
                )
        return

    await call.answer()
    if sess.modality == "VIDEO":
        txt, kb = build_video_wizard_kb(sess)
    elif sess.modality == "IMAGE":
        txt, kb = build_image_wizard_kb(sess)
    else:
        txt, kb = build_editing_tools_wizard_kb(sess)
    await safe_edit_markdown(call.message, txt, reply_markup=kb)


@router.callback_query(F.data.startswith("drv:"))
async def handle_derivative_upsell_callbacks(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    username = call.from_user.username or "Kreator"
    drv_type = call.data.split(":", 1)[1]
    sess = ACTIVE_DRAFTS.get(user_id)
    base_prompt = sess.prompt if sess else "Cinematic 4K YouTube & TikTok poster thumbnail"

    cost = 10 if drv_type == "clean_license" else 4
    async with get_db() as db:
        await ensure_user_and_track_identity(db, user_id, username)
        ok, job_id, deduct_msg = await deduct_user_coins_for_job(
            db, user_id, cost, allow_bonus=True, prompt_text=base_prompt, engine_used=f"DRV_{drv_type.upper()}"
        )
        if not ok:
            await call.answer(f"⚠️ {deduct_msg}", show_alert=True)
            return

        if drv_type == "poster4k":
            await call.answer("🖼️ Membuat Poster Thumbnail 4K...", show_alert=False)
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
