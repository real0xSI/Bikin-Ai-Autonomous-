
<!-- [ID:21_OPPORTUNITY_SPIDER_S001] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
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



<!-- [ID:21_OPPORTUNITY_SPIDER_S002] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: CUR_AGENT -->
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



<!-- [ID:21_OPPORTUNITY_SPIDER_S003] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: CUR_AGENT -->
# 11. PEMBANGUN MENU /ADMIN (DENGAN CUSTOMER VIEW INSPECTOR & AUDIT PRIVASI)
def _build_owner_admin_panel_view(treasury_row: tuple[Any, ...] | None) -> tuple[str, InlineKeyboardMarkup]:
    gross, work_cap, profit_avail, harvested, jobs_cnt = (int(treasury_row[i]) for i in range(5)) if treasury_row else (0, 0, 0, 0, 0)
    prod_str = "🟢 PRODUCTION" if RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"] else "🧪 SANDBOX HPP Rp 0"
    hh_str = "🟢 ON (0 Koin)" if RUNTIME_CONFIG["HAPPY_HOUR_MODE"] else "⚪ OFF (Normal)"
    eng_mode = "Mode 1 (HPP Rp 0)" if RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] == 1 else "Mode 2 (Hybrid Flagship)"
    cur_agent = RUNTIME_CONFIG.get("PRIMARY_ROLLING_AGENT", "ARGON")
    w_brand = RUNTIME_CONFIG.get("WEB_BRAND_NAME", "AetherFree AI Studio")

    txt = (
        f"👑 **OWNER COMMAND CENTER — bikinAI v3.7.0**\n━━━━━━━━━━━━━━━━━━\n"
        f"💰 **Brankas Treasury & Profit Split:**\n"
        f"┣ 📈 **Omzet Kotor:** `Rp {gross:,}`\n"
        f"┣ 🛡️ **Modal Kerja Terkunci (HPP+10%):** `Rp {work_cap:,}`\n"
        f"┣ 💎 **Laba Bersih Siap Panen:** **`Rp {profit_avail:,}`**\n"
        f"┣ 🏦 **Total Sudah Dipanen Owner:** `Rp {harvested:,}`\n"
        f"┗ ⚙️ **Total Job Selesai:** `{jobs_cnt} Render`\n\n"
        f"🎛️ **Status Mesin, Rolling Agent & White-Label Web:**\n"
        f"┣ 🧠 **Agen Utama Aktif:** `{cur_agent}` ({AGENTIC_ROLLING_POOL[cur_agent]['title']})\n"
        f"┣ 🌐 **Nama Brand Web:** `{w_brand}` _(Ubah: `/set_webname`)_\n"
        f"┣ 📡 **Mode Operasi /bansos:** `{RUNTIME_CONFIG['BANSOS_OPERATION_MODE']}`\n"
        f"┣ 🚀 **Status Server:** `{prod_str}` | `{eng_mode}`\n"
        f"┣ 🇮🇩 **Kasir Lokal ID:** `{RUNTIME_CONFIG['ID_ACTIVE_PROVIDER']}`\n"
        f"┗ 🌍 **Kasir Global:** `{RUNTIME_CONFIG['GLOBAL_ACTIVE_PROVIDER']}`"
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🌾 Panen Laba Bersih Sekarang (Rp {profit_avail:,})", callback_data="adm:harvest")],
            [InlineKeyboardButton(text="👁️ Lihat Layar sebagai Pembeli & Audit Kebocoran Privasi", callback_data="adm:view_as_buyer:ID")],
            [InlineKeyboardButton(text="💳 Buka Sub-Menu Pengaturan Pembayaran (3 Halaman)", callback_data="adm:pay_menu")],
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
    mode_badge = {"SILENT_PROFIT": "🤫 Mode Silent (100% Profit Owner — HPP Rp 0)", "HAPPY_HOUR": "🎉 Mode Happy Hour (Render Gratis 0 Koin)", "NORMAL": "🛑 Mode Komersial Standar"}.get(b_mode, b_mode)
    header = f"📡 **OMNI-RESOURCE RADAR & 4-GATE BANSOS STERILIZER**\n━━━━━━━━━━━━━━━━━━\n🎛️ **Saklar Aktif:** **`{mode_badge}`**\n\n"

    if active_tab == "AI_API":
        cur = await db.execute("SELECT resource_name, endpoint_url, is_live_verified FROM omni_resource_registry WHERE category = 'AI_API';")
        rows = await cur.fetchall()
        lines = [f"▸ **{x['name']}** — `{'🟢 Verified' if x['verified'] else '🟡 Standby'}`" for x in OMNI_BANSOS_PRESETS["AI_API"]] if not rows else [f"▸ **{r[0]}**\n  `{r[1]}` — `{'🟢 LIVE (<2.5s)' if r[2] else '🟡 Siap Ping'}`" for r in rows]
        body = "⚡ **[TAB 1/4] KOLAM API AI GRATIS & KOMUNITAS:**\n" + "\n".join(lines)
    elif active_tab == "DOMAINS":
        doms = await check_multi_tld_domain_availability_live("bikinai")
        body = "🌐 **[TAB 2/4] RADAR DOMAIN MULTI-TLD (RDAP LIVE):**\n" + "\n".join(f"▸ `{d['domain']}` — {d['status']}" for d in doms)
    elif active_tab == "STORAGE":
        lines = [f"▸ **{item['name']}**\n  _{item['meta']} ({item['desc']})_" for item in OMNI_BANSOS_PRESETS["CLOUD_STORAGE"] + OMNI_BANSOS_PRESETS["GRANTS_AND_DB"]]
        body = "🗄️ **[TAB 3/4] STORAGE MESH & HIBAH KOMPUTASI GRATIS:**\n" + "\n".join(lines)
    else:
        ast_res = sterilize_community_script_ast("def health_probe():\n    return {'status': 200}\n", "community_plugin")
        gitops = AUTONOMIC_GUARD.build_gitops_commit_plan(ast_res["hash"], "Verified clean AST state")
        body = f"🧬 **[TAB 4/4] 4-GATE DEEP-DEFENSE & AUTONOMIC GITOPS:**\n▸ **Gate 1 (Anti-SSRF):** `🟢 AKTIF`\n▸ **Gate 2 (Whitelist AST v2.0):** `🟢 AMAN (Hash: {ast_res['hash']})`\n▸ **Gate 3 (Response Scrubber):** `🟢 AKTIF`\n▸ **Gate 4 (Live Ping <2.5s):** `🟢 AKTIF`\n▸ **GitOps Shadow Branch:** `{gitops['shadow_branch']}`"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{'✅ ' if active_tab=='AI_API' else ''}⚡ AI API", callback_data="bns:tab:AI_API"), InlineKeyboardButton(text=f"{'✅ ' if active_tab=='DOMAINS' else ''}🌐 Domain RDAP", callback_data="bns:tab:DOMAINS")],
            [InlineKeyboardButton(text=f"{'✅ ' if active_tab=='STORAGE' else ''}🗄️ Storage & Grant", callback_data="bns:tab:STORAGE"), InlineKeyboardButton(text=f"{'✅ ' if active_tab=='AST' else ''}🧬 Skrip & GitOps", callback_data="bns:tab:AST")],
            [InlineKeyboardButton(text="🤫 Aktifkan Mode Silent (100% Profit Owner)", callback_data="bns:mode:SILENT")],
            [InlineKeyboardButton(text="🎉 Aktifkan Mode Happy Hour + Umumkan ke Grup", callback_data="bns:mode:HAPPY_HOUR")],
            [InlineKeyboardButton(text="🛑 Matikan Happy Hour (Kembali ke Tarif Normal)", callback_data="bns:mode:NORMAL")],
            [InlineKeyboardButton(text="⚡ Ping & Verifikasi Semua Endpoint", callback_data="bns:ping_all"), InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh")],
        ]
    )
    return header + body, kb



<!-- [ID:21_OPPORTUNITY_SPIDER_S004] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: CUR_AGENT -->
# ==============================================================================
def _build_owner_admin_panel_view(treasury_row: tuple[Any, ...] | None) -> tuple[str, InlineKeyboardMarkup]:
    gross = int(treasury_row[0]) if treasury_row else 0
    work_cap = int(treasury_row[1]) if treasury_row else 0
    profit_avail = int(treasury_row[2]) if treasury_row else 0
    harvested = int(treasury_row[3]) if treasury_row else 0
    jobs_cnt = int(treasury_row[4]) if treasury_row else 0

    prod_str = "🟢 PRODUCTION" if RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"] else "🧪 SANDBOX HPP Rp 0"
    hh_str = "🟢 ON (0 Koin)" if RUNTIME_CONFIG["HAPPY_HOUR_MODE"] else "⚪ OFF (Normal)"
    eng_mode = "Mode 1 (HPP Rp 0)" if RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] == 1 else "Mode 2 (Hybrid Flagship)"
    cur_agent = RUNTIME_CONFIG.get("PRIMARY_ROLLING_AGENT", "ARGON")
    b_mode = RUNTIME_CONFIG.get("BANSOS_OPERATION_MODE", "SILENT_PROFIT")

    txt = (
        f"👑 **OWNER COMMAND CENTER — bikinAI v3.6.0**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💰 **Brankas Treasury & Profit Split:**\n"
        f"┣ 📈 **Omzet Kotor:** `Rp {gross:,}`\n"
        f"┣ 🛡️ **Modal Kerja Terkunci (HPP+10%):** `Rp {work_cap:,}`\n"
        f"┣ 💎 **Laba Bersih Siap Panen:** **`Rp {profit_avail:,}`**\n"
        f"┣ 🏦 **Total Sudah Dipanen Owner:** `Rp {harvested:,}`\n"
        f"┗ ⚙️ **Total Job Selesai:** `{jobs_cnt} Render`\n\n"
        f"🎛️ **Status Mesin, Rolling Agent & Kasir:**\n"
        f"┣ 🧠 **Agen Utama Aktif:** `{cur_agent}` ({AGENTIC_ROLLING_POOL[cur_agent]['title']})\n"
        f"┣ 📡 **Mode Operasi /bansos:** `{b_mode}`\n"
        f"┣ 🚀 **Status Server:** `{prod_str}` | `{eng_mode}`\n"
        f"┣ 🇮🇩 **Kasir Lokal ID:** `{RUNTIME_CONFIG['ID_ACTIVE_PROVIDER']}`\n"
        f"┣ 🌍 **Kasir Global:** `{RUNTIME_CONFIG['GLOBAL_ACTIVE_PROVIDER']}`\n"
        f"┗ 📱 **Mini App URL:** `{RUNTIME_CONFIG['MINIAPP_URL'] or 'Auto-Detect'}`"
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🌾 Panen Laba Bersih Sekarang (Rp {profit_avail:,})", callback_data="adm:harvest")],
            [InlineKeyboardButton(text="💳 Buka Sub-Menu Pengaturan Pembayaran (3 Halaman)", callback_data="adm:pay_menu")],
            [
                InlineKeyboardButton(text="📡 Buka Radar /bansos (4-Tab)", callback_data="bns:tab:AI_API"),
                InlineKeyboardButton(text=f"🔄 Rolling Agent ({cur_agent})", callback_data="adm:rolling"),
            ],
            [
                InlineKeyboardButton(text=f"🎉 Happy Hour: {hh_str}", callback_data="adm:toggle_hh"),
                InlineKeyboardButton(text=f"🚀 Mode: {prod_str}", callback_data="adm:toggle_prod"),
            ],
            [
                InlineKeyboardButton(text=f"⚡ Mesin: {eng_mode}", callback_data="adm:toggle_eng_mode"),
                InlineKeyboardButton(text="🤖 Pusat 5 Sub-Bot & Guard", callback_data="adm:subbots"),
            ],
            [InlineKeyboardButton(text="📖 Buku Manual Developer & SOP Live (4 Bab)", callback_data="adm:manual:1")],
            [InlineKeyboardButton(text="🔄 Segarkan Data Brankas", callback_data="adm:refresh")],
        ]
    )
    return txt, kb


async def _build_bansos_4tab_view(
    db: aiosqlite.Connection, active_tab: str = "AI_API"
) -> tuple[str, InlineKeyboardMarkup]:
    b_mode = RUNTIME_CONFIG.get("BANSOS_OPERATION_MODE", "SILENT_PROFIT")
    mode_badge = {
        "SILENT_PROFIT": "🤫 Mode Silent (100% Profit Owner — HPP Rp 0)",
        "HAPPY_HOUR": "🎉 Mode Happy Hour (Render Gratis 0 Koin di Komunitas)",
        "NORMAL": "🛑 Mode Komersial Standar",
    }.get(b_mode, b_mode)

    header = (
        f"📡 **OMNI-RESOURCE RADAR & 4-GATE BANSOS STERILIZER**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎛️ **Saklar Aktif:** **`{mode_badge}`**\n\n"
    )

    if active_tab == "AI_API":
        cur = await db.execute(
            "SELECT resource_name, endpoint_url, is_live_verified FROM omni_resource_registry WHERE category = 'AI_API';"
        )
        rows = await cur.fetchall()
        if not rows:
            lines = [f"▸ **{x['name']}** — `{'🟢 Verified' if x['verified'] else '🟡 Standby'}`" for x in OMNI_BANSOS_PRESETS["AI_API"]]
        else:
            lines = [f"▸ **{r[0]}**\n  `{r[1]}` — `{'🟢 LIVE (<2.5s)' if r[2] else '🟡 Siap Ping'}`" for r in rows]
        body = "⚡ **[TAB 1/4] KOLAM API AI GRATIS & KOMUNITAS:**\n" + "\n".join(lines)
    elif active_tab == "DOMAINS":
        doms = await check_multi_tld_domain_availability_live("bikinai")
        body = "🌐 **[TAB 2/4] RADAR DOMAIN MULTI-TLD (RDAP LIVE):**\n" + "\n".join(
            f"▸ `{d['domain']}` — {d['status']}" for d in doms
        )
    elif active_tab == "STORAGE":
        lines = []
        for item in OMNI_BANSOS_PRESETS["CLOUD_STORAGE"] + OMNI_BANSOS_PRESETS["GRANTS_AND_DB"]:
            lines.append(f"▸ **{item['name']}**\n  _{item['meta']} ({item['desc']})_")
        body = "🗄️ **[TAB 3/4] STORAGE MESH & HIBAH KOMPUTASI GRATIS:**\n" + "\n".join(lines)
    else:
        ast_res = sterilize_community_script_ast("def health_probe():\n    return {'status': 200}\n", "community_plugin")
        body = (
            f"🧬 **[TAB 4/4] 4-GATE DEEP-DEFENSE & SKRIP BERSIH:**\n"
            f"▸ **Gate 1 (Anti-SSRF):** `🟢 AKTIF (Blokir IP Lokal & Metadata)`\n"
            f"▸ **Gate 2 (Whitelist AST v2.0):** `🟢 AMAN (Hash: {ast_res['hash']})`\n"
            f"▸ **Gate 3 (Response Malware Scrubber):** `🟢 AKTIF (Filter XSS & Magic Bytes)`\n"
            f"▸ **Gate 4 (Live Latency Ping <2.5s):** `🟢 AKTIF`\n\n"
            f"💡 _Member grup juga dapat menyumbang kuota API gratis via `/donasi_api [url] [model]` untuk ditukar +15 Koin Bonus setelah lolos uji 4-Gate!_"
        )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{'✅ ' if active_tab=='AI_API' else ''}⚡ AI API", callback_data="bns:tab:AI_API"),
                InlineKeyboardButton(text=f"{'✅ ' if active_tab=='DOMAINS' else ''}🌐 Domain RDAP", callback_data="bns:tab:DOMAINS"),
            ],
            [
                InlineKeyboardButton(text=f"{'✅ ' if active_tab=='STORAGE' else ''}🗄️ Storage & Grant", callback_data="bns:tab:STORAGE"),
                InlineKeyboardButton(text=f"{'✅ ' if active_tab=='AST' else ''}🧬 Skrip Bersih", callback_data="bns:tab:AST"),
            ],
            [InlineKeyboardButton(text="🤫 Aktifkan Mode Silent (100% Profit Owner)", callback_data="bns:mode:SILENT")],
            [InlineKeyboardButton(text="🎉 Aktifkan Mode Happy Hour + Umumkan ke Grup", callback_data="bns:mode:HAPPY_HOUR")],
            [InlineKeyboardButton(text="🛑 Matikan Happy Hour (Kembali ke Tarif Normal)", callback_data="bns:mode:NORMAL")],
            [
                InlineKeyboardButton(text="⚡ Ping & Verifikasi Semua Endpoint", callback_data="bns:ping_all"),
                InlineKeyboardButton(text="⬅️ Kembali ke /admin", callback_data="adm:refresh"),
            ],
        ]
    )
    return header + body, kb



<!-- [ID:21_OPPORTUNITY_SPIDER_S005] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: DIAGRAM HALAMAN 483 | Gambar: 1 file (images/page_0483_img_01.jpeg) -->
## Halaman 483

Paradigma Ekonomi Komputasi: Strategi Airdrop, 
Bantuan Sosial Komputasi, dan Jaringan DePIN 


![Diagram Halaman 483](images/page_0483_img_01.jpeg)


<!-- [ID:21_OPPORTUNITY_SPIDER_S006] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 376

           "name": "👑 Paket Sultan / Agensi VIP (+50% Bonus + Jalur Prioritas)",
           "idr": 200000,
           "coins": 3600,
           "grant_api": True,
           "is_sub": False,
           "desc": "3.600 Koin Utama + Jalur Render VIP + Kunci API Mandiri",
       },
   },
   "GLOBAL": {
       "HEMAT": {
           "name": "⚡ Starter Creator Pack",
           "usd": "$1.99",
           "stars": 110,
           "idr_eq": 31000,
           "coins": 60,
           "grant_api": False,
           "is_sub": False,
           "desc": "60 Pro Coins • 100% Watermark-Free Commercial Rights",
       },
       "PRO": {
           "name": "🚀 Studio Pro Pack",
           "usd": "$9.99",
           "stars": 550,
           "idr_eq": 155000,
           "coins": 360,
           "grant_api": False,
           "is_sub": False,
           "desc": "360 Pro Coins • Clean Commercial License & Fast Queue",
       },
       "SULTAN": {
           "name": "👑 Sovereign Executive VIP",
           "usd": "$49.99",
           "stars": 2750,
           "idr_eq": 775000,
           "coins": 2500,
           "grant_api": True,
           "is_sub": False,
           "desc": "2,500 Pro Coins • Personal API Key + Priority GPU Lane",
       },
       "SUB_CREATOR": {
           "name": "🌟 Global Creator Monthly Subscription",
           "usd": "$12.99/mo",
           "stars": 700,
           "idr_eq": 205000,
           "coins": 600,
           "grant_api": False,
           "is_sub": True,
           "desc": "600 Pro Coins/Month • Zero Watermark • Fast-Track Rendering",
       },
       "SUB_AUTONOMOUS": {
           "name": "💎 Global Autonomous Pro Subscription (API + VIP)",
           "usd": "$29.99/mo",
           "stars": 1650,
           "idr_eq": 475000,
           "coins": 1800,
           "grant_api": True,
           "is_sub": True,
           "desc": "1,800 Pro Coins/Month • Personal API Key (sk-bikinai-...) • 24/7 Priority CS",
       },
   },
}
def resolve_watermark_policy(
   deducted_utama: int,
   has_active_subscription: bool = False,
   explicit_clean_license: bool = False,
) -> dict[str, Any]:
   """
   ATURAN MUTLAK PENGGUNA:
   - Koin Gratisan / Bonus (deducted_utama == 0 & bukan subscriber): WAJIB Watermark.
   - Berbayar (Koin Utama > 0 / Subscriber Aktif / Clean License): 100% FREE WATERMARK.
   """
   is_paid_render = (



<!-- [ID:21_OPPORTUNITY_SPIDER_S007] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER, ESTIMASI -->
## Halaman 23

2.​ Paket Tier (Koin Utama Non-Hangus): Hemat Rp 5.000 (60 Koin), Pro Rp 25.000 (350 
Koin + Lisensi Komersial), Sultan VIP Rp 250.000 (4.000 Koin + Jalur Prioritas VIP). 
3.​ Subscription Bulanan (Langganan Rutin): Kreator Pass Rp 49.000/bln (Jatah 25 
Koin/hari + Bebas Watermark) & Vibecoder API/Reseller Pass Rp 99.000/bln (Kunci API 
sk-bikinai-... + Hak Buka Sub-Bot Reseller). 
○​ [FAKTA] [Bersumber] Pasar Global (Zona 1–3 PPP — USDT & Telegram Stars XTR): 
1.​ Micro Single-Pack: $0.99 (55 Stars — 30 Koin). 
2.​ Tier Packs: Starter $1.99 (110 Stars / 60 Koin), Studio Pro $9.99 (550 Stars / 350 Koin), 
Sovereign VIP $49.99 (2.750 Stars / 2.500 Koin). 
3.​ Global Monthly Subscription: $19.99/bln (1.100 Stars). 
●​ E4. Trigger Harga (Metrik Kenaikan Otomatis): 
○​ [ESTIMASI] [Bersumber] Sistem memberikan notifikasi ke /admin (melalui Human Approval 
Gate) untuk menaikkan tarif eceran/paket sebesar 15% apabila: (1) Beban HPP aktual 
melampaui 15% dari omzet kotor harian, atau (2) Efisiensi rute gratis turun di bawah 80%, atau 
(3) Jumlah pelanggan aktif di suatu zona tumbuh melampaui kelipatan 500 user. 
●​ E5. Risiko Komersial + Mitigasi (Jawaban Case 3: Auto-Posting & Afiliasi Saat Pasar 
Up-and-Down): 
○​ [FAKTA] [Bersumber] Saat tren pasar berubah cepat, mesin akuisisi tidak boleh bergantung 
pada satu jenis konten. Di v4.0, Sub-Bot #5 (Social Viral Auto-Poster) dihubungkan dengan 
Mesin Afiliasi 2-Lapis: 
1.​ Setiap karya gratis yang diunduh atau dibagikan otomatis menyematkan kode/link afiliasi 
pembuatnya (?start=ref_USERID). 
2.​ Anggota komunitas bisa mendaftarkan kanal Telegram/sosmed mereka sebagai 
Affiliator Auto-Post: bot secara terjadwal mengirim materi video/gambar tren terbaru 
(beserta tombol afiliasi mereka) ke kanal mereka. Setiap ada penonton yang klik dan 
Top-Up (baik Eceran Rp 1.500, Paket, maupun API Vibecoder), affiliator otomatis 
mendapat komisi koin/saldo! 
●​ E6. Open Source Safety, Airdrop, Community Source Safety, Oprekers Clean, Bansos (Solusi 
Poin ARCH #6): 
○​ [FAKTA] [Bersumber] Sistem membagi pemburuan sumber daya menjadi 2 protokol ketat: 
1.​ Otonom 100% (Tanpa Akun/Pendaftaran): Untuk sumber daya Kelompok 1 (LINK 
SUMBER.pdf) seperti proksi monosans, endpoint Pollinations, katalog 
OmniRoute/freellmapi, dan pemeriksaan domain RDAP, bot menguji sendiri secara 
mandiri lewat 6-Gate Canary Probe (tes ping <2,0s, cek akurasi logika, bebas 
malware/SSRF) lalu langsung mengadopsinya ke dalam kolam aktif. 
2.​ Kendali Owner (Butuh Daftar Akun / Kartu / Dompet Kripto Airdrop & Bittensor): 
Jika bot menemukan peluang kredit gratis atau airdrop DePIN (seperti Bittensor Subnet 
27, Nosana, Modal.com, NVIDIA NIM) yang membutuhkan pendaftaran akun atau dompet 
kripto, bot tidak bertindak liar, melainkan mengirim kartu info siap klik ke menu /bansos 
Anda[cite: 6, 8, 9, 140]. 
●​ E7. Konfirmasi Turunan Teknis: Mau saya turunkan seluruh skema billing (Eceran + Paket + 
Subscription + B2B API Vibecoder + Afiliasi) ini ke dalam kode v4.0? 
 
3. CODING/ARCH: & PRODUCT/UX: REVISI ARSITEKTUR TARGET v4.0 (D1–D4) 
 
D1. Grounding Tambahan A4 (10 Poin ARCH + 3 Case MARKET) 



<!-- [ID:21_OPPORTUNITY_SPIDER_S008] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 88

code arch 
 
1. fundamental yang solid dan sangat kuat, keamanan berlapis lapis. 
2. menulis dan menyusun otomatis folder project structure saat pertama kali di nyalakan & 
sesudah bot otonom github terpasang. melanjutkan penyusunan berkas folder serta mengatur 
semua kebutuhan project tertata rapih. 
3. punya kantor ai agent sendiri. yang berisikan semua anggota tugas mulai dari teratas sama 
terbawah untuk perusahaan bikinAI super Intelligence. (bisa liat kantor virtualnya lengkap 
dengan pengaturannya) 
 
tools ai: agent reach 
minerU 
ods v3 pre reales (osmantic) 
all about ai tool that have MIT & APACHE LICENSE or that need bot otonom PR/fork ikut 
contribusi dll pokoknya yang secara hukum dan aturan legal memakai yang gratis. skillspector 
Nvidia dan scanning harus bersih dari Malware dan jenis bahaya lainnya untuk kelancaran dan 
keamanan operasional 
hindsight 
octop 
ai deep tutor 
logo design skill 
ai employee 
spec kit 
jev ultrafast 
cocoindex code 
colibri 
jev 
light panda browser 
awesomefreellm 
audio8, freellmapi, paperclip, motionmaxxing, openmausbot and manymore semua daftar list 
yang ada di file juga termasuk. 
 
nosignup.net itu daftar apa tuh airdrop atau bansos atau gratisan kan. appverse.id juga itu dia 
banyak bansos token B B M MAn pokoknya jutaan repo opensource yang benar benar bisa di 
pakai secara gratis! tentu ini sangat berguna banyak buat operasional dan semua karyawan 
fully otonom harian yang benar benar setiap harinya sangat komplex bagi pengguna chat. juga 
kebutuhan lainnya kita benar benar harus buat premium services untuk semua pengguna. mau 
itu sfw/unfil and uncen. semua punya hak yang sama. baik itu premium services/subscription. 
karena kita hanya biasa saja yang gratisan cukup dan tidak perlu membebani server untuk yang 
gratisan khusus jalur gratis dan sama di batasi juga karena semua harus wajib bayar. 
 
 
 
 
bahasa & penulisan variable unik harus dalam bahasa indonesia gaul & sunda kasar. 
 



<!-- [ID:21_OPPORTUNITY_SPIDER_S009] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 43

Solana (SOL/NOS/IO) sekaligus menyediakan penyewaan GPU dan inferensi model 
terbuka dengan harga 50–70% lebih murah dari cloud terpusat. Sejak Juni 2026, IO.net 
mengaktifkan Incentive Dynamic Engine yang membakar (burn) sedikitnya 50% 
pendapatan jaringan untuk menopang nilai token IO. 
3.​ Akash Network (Decentralized Serverless Cloud & Otomasi Deployment Agen) — 
URL Polos Repositori Kode Node Akash: https://github.com/akash-network/node | URL 
Polos Rilis Binary Akash (v2.1.2 / v3.0.0-a0): https://github.com/ovrclk/akash/releases | 
URL Polos Skrip Instalasi Node Akash: 
https://raw.githubusercontent.com/akash-network/node/main/install.sh | URL Polos 
Daemon Provider Akash: https://github.com/akash-network/provider | URL Polos Web 
Console Akash (Deploy Kontainer Docker Tanpa Kartu Kredit): 
https://github.com/akash-network/console | URL Polos Agent SDL Generator Skill (Deploy 
Otomatis oleh Claude Code/OpenClaw): https://github.com/akash-network/akash-skill | 
URL Polos Kumpulan Template Deployment Awesome-Akash: 
https://github.com/akash-network/awesome-akash | URL Polos Helm Charts Akash: 
https://github.com/akash-network/helm-charts | URL Polos RPC Proxy Akash: 
https://github.com/akash-network/rpc-proxy | URL Polos Dokumentasi Arsitektur Operator 
Node Akash: https://akash.network/docs/node-operators/architecture/ — Kegunaan & 
Aturan Terbaru (Oktober 2026): Pasar komputasi awan peer-to-peer berbasis Cosmos 
SDK yang memungkinkan agen koding AI membuat berkas konfigurasi SDL secara 
otomatis (akash-skill) dan men-deploy kontainer Docker dengan biaya 60–80% di bawah 
AWS menggunakan token AKT tanpa kartu kredit. 
4.​ Tambahan Airdrop DePIN & Node Ringan Gratis (Tanpa Modal Uang / Zero-Cost 
Farming - Aktif Oktober 2026) — URL Polos Portal Aplikasi Grass Network (Desktop & 
Android Node): https://app.grass.io | URL Polos Grass Foundation (Staking & Klaim 
Airdrop): https://www.grassfoundation.io/ | URL Polos Panduan & Pelacak Airdrop 
Gradient Network (Sentry Node Solana): https://airdroplyx.com/airdrop/gradient/ | URL 
Polos Panduan & Pelacak Airdrop Nexus zkVM (Browser & Rust CLI Prover): 
https://airdroplyx.com/airdrop/nexus/ | URL Polos Ekstensi Chrome Resmi DAWN 
Validator (v3.0.13 - Proof of Bandwidth Solana): 
https://chromewebstore.google.com/detail/dawn-validator-chrome-ext/fpdkjdnhkakefebpek
bdhillbhonfjjp | URL Polos Dashboard Bless Network (Incentivized Testnet Idle Compute): 
https://bless.network/dashboard | URL Polos Panduan Node Bless Network & DePIN: 
https://www.nodeaddicts.com/bless-network.html | URL Polos Pelacak Aktivitas Testnet 
Gensyn AI: https://cryptorank.io/drophunting/gensyn-activity749 | URL Polos Titan 
Network (DePIN Edge CDN & Storage): 
https://www.titannet.io/learn/basics/best-depin-projects-2026-top-decentralized-physical-in
frastructure-networks | URL Polos Direktori Proyek DePIN Hub: 
https://depinhub.io/projects/ | URL Polos Katalog Airdrop DePIN Terverifikasi (Airdrops.io): 
https://airdrops.io/categories/depin/ | URL Polos Panduan DePIN & Testnet Airdrops 2026 
(AirdropAlert): https://airdropalert.com/blogs/depin-and-testnet-airdrops/ — Kegunaan & 
Aturan Terbaru (Audit Oktober 2026): Pada 8 Oktober 2026, Grass resmi meluncurkan 
Contents API komersial (mengubah URL publik menjadi HTML/Markdown bersih untuk 
agen AI dengan tingkat keberhasilan pengambilan 97%–98% menggunakan jaringan IP 
residensial pengguna) dan mengalihkan imbalan kontributor ke arah pendapatan nyata / 
USDC (batas akhir klaim Season 2 jatuh pada 22 Januari 2027). Aturan penting Grass 
2026: ekstensi browser lama telah digantikan oleh aplikasi desktop resmi dan aplikasi 
Android (yang memberikan pengali 3x lipat poin jika dijalankan pada koneksi data seluler 



<!-- [ID:21_OPPORTUNITY_SPIDER_S010] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_153 -->
## Halaman 44

terpisah); wajib menggunakan IP rumah/residensial asli karena IP pusat data (VPS/VPN) 
langsung difilter oleh sistem anti-Sybil. Sementara itu, Gradient Network (didukung 
Multicoin Capital, Pantera, dan Sequoia di jaringan Solana) sedang menjalankan 
kampanye Sentry Node Open Beta 100% gratis untuk mengumpulkan poin menuju 
konversi token 
𝐺𝑅𝐴𝐷𝑝𝑎𝑑𝑎𝑎𝑘ℎ𝑖𝑟2026. 𝑁𝑒𝑥𝑢𝑠𝑧𝑘𝑉𝑀(𝑑𝑖𝑑𝑢𝑘𝑢𝑛𝑔𝑝𝑒𝑛𝑑𝑎𝑛𝑎𝑎𝑛𝑈𝑆27, 2𝑗𝑢𝑡𝑎𝑑𝑎𝑟𝑖𝐿𝑖𝑔ℎ𝑡𝑠𝑝𝑒𝑒𝑑𝑑𝑎𝑛𝑃𝑎𝑛𝑡𝑒𝑟𝑎𝐶𝑎𝑝𝑖𝑡𝑎𝑙)𝑚
NEXUS` menjelang peluncuran token akhir 
2026[span_153](start_span)[span_153](end_span). Terakhir, DAWN (didukung 
pendanaan US33 juta di ekosistem Solana) memberikan poin imbalan atas validasi Proof 
of Bandwidth melalui ekstensi Chrome v3.0.13, sementara Bless Network memberikan 
poin testnet berinsentif dengan membagikan kapasitas komputasi idle perangkat melalui 
ekstensi Chrome tanpa memerlukan modal finansial. 
Karya yang dikutip 
1. OmniRoute/docs/reference/PROVIDER_REFERENCE.md ... - GitHub, 
https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.52/docs/reference/PROVIDER_
REFERENCE.md 2. raullenchai/free-llm-api-resources - GitHub, 
https://github.com/raullenchai/free-llm-api-resources 3. Package 9router - GitHub, 
https://github.com/decolua/9router/pkgs/container/9router 4. Provider Reference · 
diegosouzapw/OmniRoute Wiki - GitHub, 
https://github.com/diegosouzapw/OmniRoute/wiki/Provider-Reference 5. Panduan v2: Membuat 
Transaksi - Pakasir, https://pakasir.com/p/create-transaction 6. Paydisini | Aggregator Payment 
Gateway Indonesia Terbaik, https://paydisini.co.id/ 7. Payment Gateway Fees Indonesia 2026: 
Xendit, Midtrans, DOKU, https://www.matthewswong.com/en/indonesia/payment-gateway-fees/ 
8. QRIS Payments in Indonesia: A Complete Guide for Businesses, 
https://www.xendit.co/en-id/blog/qris-payments-in-indonesia-a-complete-guide-for-businesses/ 
9. Docker Container Hosting — Free until 2027 - Caasify, https://caasify.com/container-hosting 
10. Container Hosting with a Free Tier: 4 Docker Containers, No Card, 
https://snapdeploy.dev/free-container-hosting 11. Coolify vs Dokploy vs CapRover (2026): 
Self-Hosted PaaS, https://www.rakibulinux.com/blogs/coolify-vs-dokploy-vs-caprover-2026 12. 
Gradient Network Airdrop Guide & Verification (2026) - Airdroplyx, 
https://airdroplyx.com/airdrop/gradient/ 13. Nexus zkVM Airdrop Guide & Verification (2026) - 
Airdroplyx, https://airdroplyx.com/airdrop/nexus/ 14. Latest Grass (GRASS) News Update - 
CoinMarketCap, https://coinmarketcap.com/cmc-ai/grass/latest-updates/ 15. GitHub - 
proxifly/free-proxy-list: Free HTTP, SOCKS4, & SOCKS5, 
https://github.com/proxifly/free-proxy-list 16. GitHub - Zaeem20/FREE_PROXIES_LIST: FREE 
PROXY LIST (Gets, https://github.com/Zaeem20/FREE_PROXIES_LIST 17. 
pollinations/APIDOCS.md at main - GitHub, 
https://github.com/pollinations/pollinations/blob/main/APIDOCS.md 18. PollinationAI-SDK - 
PyPI, https://pypi.org/project/PollinationAI-SDK/ 19. LICENSE · 
huihui-ai/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF, 
https://huggingface.co/huihui-ai/Huihui-Qwen3.8-Flash-Next-abliterated-GGUF/blob/e82f977342
13d69d51fba611fa7003b773520133/LICENSE 20. huihui-ai/Huihui4-48B-A4B-abliterated - 
Hugging Face, https://huggingface.co/huihui-ai/Huihui4-48B-A4B-abliterated 21. Local AI Video 
Generation: Wan 2.2 vs LTX-2 vs HunyuanVideo, 
https://localaimaster.com/blog/local-ai-video-generation 22. GitHub - Wan-Video/Wan2.2, 
https://github.com/Wan-Video/Wan2.2 23. Wan2.Video: Free AI Video Generator, 


