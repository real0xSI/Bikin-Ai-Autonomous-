
<!-- [ID:02_CORE_AI_S025] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
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



<!-- [ID:02_CORE_AI_S026] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# 8. MEDIA FETCHER, CDN DOWNLOAD PROXY & DUAL WEB APPLICATION HANDLERS
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
            return web.json_response({"ok": False, "message": "🔒 Sesi Mini App tidak valid. Buka ulang dari tombol di dalam Telegram."}, status=403)

    prompt_raw, is_attack = sanitize_and_deobfuscate_input(str(data.get("prompt") or "Katalog produk studio 4K"))
    if is_attack:
        return web.json_response({"ok": False, "message": "🛡️ Pola teks tidak diizinkan."}, status=400)

    modality, engine, ratio = str(data.get("modality") or "IMAGE"), str(data.get("engine") or "Seedream 4.5"), str(data.get("ratio") or "9:16")
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
                    mode_title = "FOTO JADI VIDEO (IMG2VID)" if modality == "IMG2VID" else "VIDEO AI SINEMATIK"
                    await BOT_INSTANCE_GLOBAL.send_video(chat_id=user_id, video=SAMPLE_SANDBOX_VIDEO_URL, caption=f"🎬 **{mode_title} SELESAI**\n┣ ⚡ **Mesin AI:** `{engine}` ({ratio})\n┣ 🔍 **Kualitas:** `{upscale}{ref_tag}`\n┗ 📝 **Konsep:** _{prompt_raw[:120]}_", parse_mode="Markdown")
                elif modality == "REMOVE_BG":
                    img_bytes = await fetch_clean_image_bytes(f"{prompt_raw}, isolated subject on pure transparent background, PNG cutout", 768, 768)
                    if not img_bytes:
                        raise RuntimeError("Render PNG gagal")
                    await BOT_INSTANCE_GLOBAL.send_document(chat_id=user_id, document=BufferedInputFile(img_bytes, filename=f"bikinAI_Transparan_{int(time.time())}.png"), caption=f"✂️ **FILE PNG TRANSPARAN KUALITAS TINGGI**\n┗ 🔍 **Kualitas:** `{upscale}`", parse_mode="Markdown")
                else:
                    w, h = (768, 1024) if ratio == "9:16" else ((1024, 768) if ratio == "16:9" else (1024, 1024))
                    img_bytes = await fetch_clean_image_bytes(f"{prompt_raw}, {engine} style, 8k masterpiece", w, h)
                    if not img_bytes:
                        raise RuntimeError("Render gambar gagal")
                    await BOT_INSTANCE_GLOBAL.send_photo(chat_id=user_id, photo=BufferedInputFile(img_bytes, filename="bikinAI_Studio_4K.jpg"), caption=f"✨ **HASIL KARYA 4K DARI STUDIO WEB**\n┣ ⚡ **Mesin AI:** `{engine}` ({ratio})\n┣ 🔍 **Kualitas:** `{upscale}{ref_tag}`\n┗ 📝 **Deskripsi:** _{prompt_raw[:120]}_", parse_mode="Markdown")
                await mark_job_completed(db, job_id, prompt_raw, engine)
                await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            except Exception:
                await refund_failed_job(db, job_id)
                return web.json_response({"ok": False, "message": "🛡️ Garansi Koin Kembali 100%: Koin Anda telah dikembalikan otomatis!"}, status=500)
        return web.json_response({"ok": True, "message": "✅ Karya selesai dan telah dikirim ke ruang chat Telegram Anda!"})
    return web.json_response({"ok": True, "message": "✅ Silakan buka Studio Web langsung dari tombol di dalam Telegram."})


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
            persona_style=str(data.get("persona") or "NATURAL_COMPANION"),
            chat_history=data.get("history") if isinstance(data.get("history"), list) else [],
        )
    return web.json_response({"ok": True, "reply": reply})


async def handle_nocturne_generate_api(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"ok": False}, status=400)
    prompt_raw, is_attack = sanitize_and_deobfuscate_input(str(data.get("prompt") or "Masterpiece portrait 8k"))
    if is_attack:
        return web.json_response({"ok": False}, status=400)
    modality, model_name, ratio = str(data.get("modality") or "IMAGE"), str(data.get("model") or "Flux.1-Dev Uncensored Pro"), str(data.get("ratio") or "9:16")
    w, h = (768, 1024) if ratio == "9:16" else ((1024, 768) if ratio == "16:9" else (1024, 1024))
    seed_val = int(time.time())
    if modality in ("VIDEO", "IMG2VID"):
        cdn_url, dl_name, is_video = SAMPLE_SANDBOX_VIDEO_URL, f"AetherFree_Video_{seed_val}.mp4", True
    else:
        cdn_url, dl_name, is_video = f"https://image.pollinations.ai/prompt/{quote(f'{prompt_raw}, {model_name}, 8k masterpiece')}?width={w}&height={h}&nologo=true&private=true&enhance=true&seed={seed_val}", f"AetherFree_4K_{seed_val}.jpg", False
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
    print(f"🌐 [WEB & FREEDOM STUDIO v3.7.0]: Aktif di port {port} ({RUNTIME_CONFIG['MINIAPP_URL'] or 'http://localhost:8080'})")



<!-- [ID:02_CORE_AI_S027] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: INLINEKEYBOARDBUTTON -->
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


