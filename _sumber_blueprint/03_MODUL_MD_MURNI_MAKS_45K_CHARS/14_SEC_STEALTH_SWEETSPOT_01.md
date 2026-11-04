
<!-- [ID:14_SEC_STEALTH_S001] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: PLATFORMSPEC -->
# ── CLI Subcommands ─────────────────────────────────────────────────
def cmd_provision(args: argparse.Namespace) -> None:
    if args.category == "ALL":
        target_slugs = list(PLATFORM_REGISTRY.keys())
    else:
        target_slugs = [k for k, v in PLATFORM_REGISTRY.items() if v.category == args.category]

    if args.platforms:
        requested = [p.strip() for p in args.platforms.split(",") if p.strip() in PLATFORM_REGISTRY]
        if requested:
            target_slugs = requested

    print(f"== Provisioning {args.count} Account Bundles across {len(target_slugs)} Platforms ({args.workers} Workers) ==")
    t0 = time.time()
    all_profiles = []
    summary_rows = []

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {
            ex.submit(worker_provision_task, i, target_slugs, args): i
            for i in range(1, args.count + 1)
        }
        for fut in as_completed(futures):
            idx, prof, res = fut.result()
            all_profiles.append(prof)
            summary_rows.extend(res)

    PROFILES_FILE.write_text(json.dumps(all_profiles, indent=2), encoding="utf-8")
    elapsed = time.time() - t0
    print(f"\n=== COMPLETED: {len(all_profiles)} bundles x {len(target_slugs)} platforms in {elapsed:.2f}s ===")
    print(f"Saved master account profiles -> {PROFILES_FILE}")

    if args.tg_token and args.tg_chatid:
        msg = (
            f"<b>PROVISIONING SUMMARY</b>\n"
            f"Bundles: {len(all_profiles)}\n"
            f"Platforms: {len(target_slugs)}\n"
            f"Elapsed: {elapsed:.2f}s\n"
        )
        send_telegram_msg(args.tg_token, args.tg_chatid, msg)


def cmd_env_vault(args: argparse.Namespace) -> None:
    """Generates the standardized multi-path .env.master file with all registration keys."""
    lines = [
        "# ============================================================================",
        "# MASTER ENV VAULT — ALL REGISTRATION PLATFORMS & CREDENTIAL IDENTITIES",
        "# Rule: Add .env.master to .gitignore immediately (Zero-Commit Security)",
        "# ============================================================================",
        "",
        f"MASTER_USERNAME=\"{MASTER_CREDENTIAL_SEEDS['master_usernames'][0]}\"",
        f"MASTER_GITHUB_OAUTH=\"{MASTER_CREDENTIAL_SEEDS['oauth_identities']['github_primary']}\"",
        f"MASTER_GOOGLE_OAUTH=\"{MASTER_CREDENTIAL_SEEDS['oauth_identities']['google_primary']}\"",
        f"MASTER_AWS_BUILDER_ID=\"{MASTER_CREDENTIAL_SEEDS['oauth_identities']['aws_builder_id']}\"",
        ""
    ]
    by_cat: Dict[str, List[PlatformSpec]] = {}
    for spec in PLATFORM_REGISTRY.values():
        by_cat.setdefault(spec.category, []).append(spec)

    for cat, specs in by_cat.items():
        lines.append(f"# ── {cat} ──────────────────────────────────────────────")
        for s in specs:
            val = os.getenv(s.env_key_name, "")
            lines.append(f"# {s.name} | Signup: {s.signup_url}")
            lines.append(f"{s.env_key_name}=\"{val}\"")
        lines.append("")

    out_path = Path(args.out) if args.out else ENV_VAULT_FILE
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated master environment vault ({len(PLATFORM_REGISTRY)} platforms) -> {out_path}")


def cmd_list_links(args: argparse.Namespace) -> None:
    print(f"{'SLUG':20s} | {'CATEGORY':18s} | {'ENV KEY':24s} | {'SIGNUP URL'}")
    print("-" * 105)
    for slug, s in PLATFORM_REGISTRY.items():
        if args.category != "ALL" and s.category != args.category:
            continue
        print(f"{slug:20s} | {s.category:18s} | {s.env_key_name:24s} | {s.signup_url}")


def cmd_check_all(args: argparse.Namespace) -> None:
    """Checks connectivity/key status across all configured OpenAI-compatible platforms."""
    client = RotatingPlatformClient()
    for slug, spec in PLATFORM_REGISTRY.items():
        tok = os.getenv(spec.env_key_name, "")
        if not tok:
            continue
        st, body = client.request_json(
            "POST",
            f"{spec.api_base.rstrip('/')}/chat/completions",
            payload={
                "model": spec.default_model,
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 4
            },
            headers={"Authorization": f"Bearer {tok}"}
        )
        print(f"[{slug:20s}] HTTP {st} | model={spec.default_model} | resp={str(body)[:90]}")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="all_in_one_hub", description="Multi-Platform Registration & Credential Hub")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_prov = sub.add_parser("provision", help="Provision credentials & execute instant agent registrations")
    p_prov.add_argument("count", type=int, help="Number of credential bundles to generate/provision")
    p_prov.add_argument("--category", choices=["ALL", "INSTANT_API", "GONKA_BROKER", "OAUTH_CARDLESS", "WHOLESALE_OR_DEPIN"], default="ALL")
    p_prov.add_argument("--platforms", default="", help="Comma-separated platform slugs (optional)")
    p_prov.add_argument("--domain", default=None, help="Custom email domain for generated credentials")
    p_prov.add_argument("--proxy", default=None, help="Proxy URL (Bright Data or HTTP/SOCKS5)")
    p_prov.add_argument("--workers", type=int, default=8)
    p_prov.add_argument("--backoff", type=float, default=0.3)
    p_prov.add_argument("--skip-chat", action="store_true", default=True)
    p_prov.add_argument("--tg-token", default=TG_BOT_TOKEN)
    p_prov.add_argument("--tg-chatid", default=TG_CHAT_ID)
    p_prov.set_defaults(fn=cmd_provision)

    p_env = sub.add_parser("env", help="Export standardized .env.master vault with all registration links")
    p_env.add_argument("--out", default=None)
    p_env.set_defaults(fn=cmd_env_vault)

    p_list = sub.add_parser("links", help="List all registration links and categories")
    p_list.add_argument("--category", choices=["ALL", "INSTANT_API", "GONKA_BROKER", "OAUTH_CARDLESS", "WHOLESALE_OR_DEPIN"], default="ALL")
    p_list.set_defaults(fn=cmd_list_links)

    p_chk = sub.add_parser("check", help="Ping all platforms that have keys populated in environment")
    p_chk.set_defaults(fn=cmd_check_all)

    return ap


if __name__ == "__main__":
    parser = build_parser()
    parsed_args = parser.parse_args()
    parsed_args.fn(parsed_args)

#!/usr/bin/env python3
"""
Module 1: Master Registry of Registration Links, Embedded Username Pools & Thread-Safe Vault
"""

import json
import os
import random
import secrets
import string
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
CREDS_DIR = HERE / "creds"
POOL_FILE = HERE / "keys.txt"
ENV_VAULT_FILE = HERE / ".env.master"
FILE_LOCK = threading.Lock()

ADJ = [
    "swift", "quiet", "brave", "lucky", "cosmic", "rapid", "clever", "mellow",
    "crimson", "golden", "amber", "bright", "calm", "coral", "daring", "eager",
    "fierce", "gentle", "icy", "jolly", "kind", "lunar", "misty", "noble",
    "polar", "proud", "rusty", "silver", "solar", "tidy", "vivid", "wild"
]
NOUN = [
    "eagle", "otter", "falcon", "panda", "comet", "signal", "raven", "tiger",
    "nebula", "lynx", "badger", "birch", "bison", "cedar", "cloud", "crane",
    "dove", "ember", "fern", "finch", "fox", "heron", "maple", "mink"
]

EMBEDDED_USERNAMES = [
    "swift_falcon_901", "cosmic_raven_412", "lunar_lynx_778",
    "solar_tiger_304", "crimson_orca_552", "polar_eagle_819",
    "vivid_nebula_108", "nimble_heron_663", "amber_comet_227",
    "fierce_badger_940", "keen_otter_515", "noble_wolf_382"
]


@dataclass(frozen=True)
class PlatformNode:
    slug: str
    name: str
    category: str
    signup_url: str
    api_base: str
    auth_mode: str
    env_key: str
    default_model: str = "deepseek-v4.1-flash"


def get_master_registry() -> Dict[str, PlatformNode]:
    nodes = [
        # Instant / Cryptographic Token / Self-Register Platforms
        PlatformNode("dahl_global", "Dahl Global", "INSTANT_API", "https://inference.dahl.global/account", "https://inference.dahl.global/v1", "dahl_fp", "DAHL_API_KEY", "deepseek-ai/DeepSeek-V4-Flash-0731"),
        PlatformNode("bazaarlink", "BazaarLink Agent API", "INSTANT_API", "https://bazaarlink.ai/api/v1/agents/register", "https://api.bazaarlink.ai/v1", "bazaar_post", "BAZAARLINK_API_KEY", "auto:free"),
        PlatformNode("bazaarlink_x402", "BazaarLink x402", "INSTANT_API", "https://bazaarlink.ai/api/v1/agents/register/x402", "https://api.bazaarlink.ai/v1", "bazaar_post", "BAZAARLINK_X402_KEY", "deepseek/deepseek-v4.1-flash-1017"),
        PlatformNode("nanogpt", "NanoGPT Studio", "INSTANT_API", "https://nano-gpt.com", "https://nano-gpt.com/api/v1", "session_token", "NANOGPT_API_KEY", "claude-opus-5.5"),
        PlatformNode("payperq", "PayPerQ Credit ID", "INSTANT_API", "https://ppq.ai", "https://api.ppq.ai/v1", "session_token", "PPQ_API_KEY", "gemini-4-argon"),
        PlatformNode("pollinations_enter", "Pollinations Pollen", "INSTANT_API", "https://enter.pollinations.ai", "https://gen.pollinations.ai/v1", "session_token", "POLLINATIONS_API_KEY", "deepseek-v4.1-flash"),
        PlatformNode("venice_ai", "Venice AI", "INSTANT_API", "https://venice.ai", "https://api.venice.ai/api/v1", "session_token", "VENICE_API_KEY", "kimi-k3.1-pro"),
        PlatformNode("llm7_token", "LLM7.io Token", "INSTANT_API", "https://token.llm7.io", "https://api.llm7.io/v1", "session_token", "LLM7_API_KEY", "deepseek-v4-flash"),

        # Gonka Ecosystem Brokers
        PlatformNode("gonka_proxy", "Proxy by Gonka.gg", "GONKA_BROKER", "https://proxy.gonka.gg", "https://api.proxy.gonka.gg/v1", "gonka_key", "GONKA_PROXY_API_KEY", "minimax-m2.7"),
        PlatformNode("gonka_openbroker", "OpenBroker Gonka", "GONKA_BROKER", "https://openbroker.gonka.gg", "https://api.openbroker.gonka.gg/v1", "crypto_wallet", "OPENBROKER_API_KEY", "deepseek-v4-flash"),
        PlatformNode("easy_gonka", "Easy GonkaAI API", "GONKA_BROKER", "https://gonka-api.org", "https://hkyauefqcgbvgvxkluj.supabase.co/functions/v1/gonka", "gonka_key", "EASY_GONKA_API_KEY", "glm-5.3-flash"),
        PlatformNode("gonkarouter", "GonkaRouter", "GONKA_BROKER", "https://gonkarouter.io", "https://api.gonkarouter.io/v1", "gonka_key", "GONKAROUTER_API_KEY", "glm-5.3-flash"),
        PlatformNode("joingonka", "JoinGonka Gateway", "GONKA_BROKER", "https://gate.joingonka.ai", "https://gate.joingonka.ai/v1", "gonka_key", "JOINGONKA_API_KEY", "minimax-m2.7"),
        PlatformNode("gonka24", "Gonka24", "GONKA_BROKER", "https://gonka24.com", "https://api.gonka24.com/v1", "gonka_key", "GONKA24_API_KEY", "kimi-k2.6"),
        PlatformNode("gonkagate", "GonkaGate", "GONKA_BROKER", "https://gonkagate.com", "https://api.gonkagate.com/v1", "gonka_key", "GONKAGATE_API_KEY", "deepseek-v4-flash"),

        # Group 2: Cardless OAuth / Email Registration Platforms
        PlatformNode("ngodeai", "NgodeAI ID-JKT", "OAUTH_CARDLESS", "https://ngodeai.net", "https://llm.ngodeai.net/v1", "oauth_portal", "NGODEAI_API_KEY", "deepseek-v4.1-flash"),
        PlatformNode("google_ai_studio", "Google AI Studio", "OAUTH_CARDLESS", "https://aistudio.google.com/app/apikey", "https://generativelanguage.googleapis.com/v1beta/openai", "oauth_portal", "GEMINI_API_KEY", "gemini-3.5-flash"),
        PlatformNode("mistral_console", "Mistral Console", "OAUTH_CARDLESS", "https://console.mistral.ai", "https://api.mistral.ai/v1", "oauth_portal", "MISTRAL_API_KEY", "mistral-large-latest"),
        PlatformNode("groq_cloud", "GroqCloud", "OAUTH_CARDLESS", "https://console.groq.com/keys", "https://api.groq.com/openai/v1", "oauth_portal", "GROQ_API_KEY", "qwen-qwq-32b"),
        PlatformNode("openrouter", "OpenRouter", "OAUTH_CARDLESS", "https://openrouter.ai/settings/keys", "https://openrouter.ai/api/v1", "oauth_portal", "OPENROUTER_API_KEY", "openrouter/free"),
        PlatformNode("nvidia_nim", "NVIDIA NIM", "OAUTH_CARDLESS", "https://build.nvidia.com/", "https://integrate.api.nvidia.com/v1", "oauth_portal", "NVIDIA_NIM_API_KEY", "deepseek-ai/deepseek-r1"),
        PlatformNode("cloudflare_dash", "Cloudflare Workers AI", "OAUTH_CARDLESS", "https://dash.cloudflare.com/sign-up", "https://api.cloudflare.com/client/v4", "oauth_portal", "CLOUDFLARE_AI_TOKEN", "@cf/moonshotai/kimi-k2.7-code"),
        PlatformNode("siliconflow", "SiliconFlow", "OAUTH_CARDLESS", "https://cloud.siliconflow.com/", "https://api.siliconflow.cn/v1", "oauth_portal", "SILICONFLOW_API_KEY", "deepseek-ai/DeepSeek-V3"),
        PlatformNode("fireworks_ai", "Fireworks AI", "OAUTH_CARDLESS", "https://fireworks.ai", "https://api.fireworks.ai/inference/v1", "oauth_portal", "FIREWORKS_API_KEY", "accounts/fireworks/models/deepseek-r1"),
        PlatformNode("aws_builder_id", "AWS Builder ID", "OAUTH_CARDLESS", "https://profile.aws.amazon.com/", "http://127.0.0.1:4001/v1", "oauth_portal", "AWS_BUILDER_TOKEN", "claude-code-free"),
        PlatformNode("huggingface", "Hugging Face Tokens", "OAUTH_CARDLESS", "https://huggingface.co/settings/tokens", "https://router.huggingface.co/v1", "oauth_portal", "HF_ACCESS_TOKEN", "Qwen/Qwen3-235B-A22B"),
        PlatformNode("cohere", "Cohere Trial", "OAUTH_CARDLESS", "https://dashboard.cohere.com", "https://api.cohere.com/compatibility/v1", "oauth_portal", "COHERE_API_KEY", "command-r-plus"),
        PlatformNode("chutes_ai", "Chutes AI", "OAUTH_CARDLESS", "https://chutes.ai", "https://llm.chutes.ai/v1", "oauth_portal", "CHUTES_API_KEY", "deepseek-ai/DeepSeek-R1"),
        PlatformNode("civitai", "Civitai API", "OAUTH_CARDLESS", "https://civitai.com/user/account", "https://civitai.com/api/v1", "oauth_portal", "CIVITAI_API_KEY", "flux-1"),
        PlatformNode("spider_cloud", "Spider Cloud", "OAUTH_CARDLESS", "https://spider.cloud", "https://api.spider.cloud/v1", "oauth_portal", "SPIDER_CLOUD_API_KEY", "crawler"),
        PlatformNode("turso_cloud", "Turso libSQL", "OAUTH_CARDLESS", "https://turso.tech/", "https://api.turso.tech/v1", "oauth_portal", "TURSO_AUTH_TOKEN", "libsql"),
        PlatformNode("supabase", "Supabase", "OAUTH_CARDLESS", "https://supabase.com", "https://api.supabase.com/v1", "oauth_portal", "SUPABASE_POSTGRES_DSN", "pgvector"),
        PlatformNode("neon_db", "Neon Postgres", "OAUTH_CARDLESS", "https://neon.tech", "https://console.neon.tech/api/v2", "oauth_portal", "NEON_SQL_DSN", "postgres"),
        PlatformNode("upstash", "Upstash Redis", "OAUTH_CARDLESS", "https://upstash.com", "https://api.upstash.com/v2", "oauth_portal", "REDIS_CONN_STRING", "redis"),
        PlatformNode("backblaze_b2", "Backblaze B2", "OAUTH_CARDLESS", "https://www.backblaze.com/cloud-storage", "https://api.backblazeb2.com/b2api/v2", "oauth_portal", "BACKBLAZE_B2_APP_KEY", "b2"),
        PlatformNode("vercel", "Vercel", "OAUTH_CARDLESS", "https://vercel.com", "https://api.vercel.com", "oauth_portal", "VERCEL_TOKEN", "edge"),
        PlatformNode("e2b_sandbox", "E2B Sandbox", "OAUTH_CARDLESS", "https://e2b.dev", "https://api.e2b.dev", "oauth_portal", "E2B_API_KEY", "sandbox"),
        PlatformNode("pakasir", "Pakasir QRIS", "OAUTH_CARDLESS", "https://pakasir.com/", "https://pakasir.com/api", "oauth_portal", "PAKASIR_API_KEY", "qris"),
        PlatformNode("tripay", "Tripay QRIS", "OAUTH_CARDLESS", "https://tripay.co.id/", "https://tripay.co.id/api", "oauth_portal", "TRIPAY_API_KEY", "qris"),
        PlatformNode("duitku", "Duitku QRIS", "OAUTH_CARDLESS", "https://www.duitku.com/", "https://passport.duitku.com/webapi", "oauth_portal", "DUITKU_API_KEY", "qris"),
        PlatformNode("telegram_botfather", "Telegram @BotFather", "OAUTH_CARDLESS", "https://t.me/BotFather", "https://api.telegram.org", "oauth_portal", "TOKEN_BOT_UTAMA", "bot"),
        PlatformNode("telegram_cryptobot", "Telegram @CryptoBot", "OAUTH_CARDLESS", "https://t.me/CryptoBot", "https://pay.crypt.bot/api", "oauth_portal", "CRYPTOBOT_API_TOKEN", "usdt"),

        # Group 3: Wholesale & Multimodal Supermarkets
        PlatformNode("wavespeed_ai", "WaveSpeed AI", "WHOLESALE_OR_DEPIN", "https://wavespeed.ai/", "https://api.wavespeed.ai/api/v2", "oauth_portal", "WAVESPEED_API_KEY", "wan-3.0"),
        PlatformNode("cometapi", "CometAPI", "WHOLESALE_OR_DEPIN", "https://www.cometapi.com/", "https://api.cometapi.com/v1", "oauth_portal", "COMETAPI_KEY", "suno-v4"),
        PlatformNode("ai_302", "302.AI Supermarket", "WHOLESALE_OR_DEPIN", "https://302.ai/anonymous", "https://api.302.ai/v1", "oauth_portal", "AI302_API_KEY", "kling-4.0"),
        PlatformNode("fal_ai", "Fal.ai", "WHOLESALE_OR_DEPIN", "https://fal.ai/dashboard/keys", "https://fal.run", "oauth_portal", "FAL_KEY", "kling-3.0"),
        PlatformNode("novita_ai", "Novita AI", "WHOLESALE_OR_DEPIN", "https://novita.ai/", "https://api.novita.ai/v3/openai", "oauth_portal", "NOVITA_API_KEY", "deepseek/deepseek-r1"),
        PlatformNode("runpod", "RunPod", "WHOLESALE_OR_DEPIN", "https://www.runpod.io/", "https://api.runpod.ai/v2", "oauth_portal", "RUNPOD_API_KEY", "serverless"),
        PlatformNode("vast_ai", "Vast.ai", "WHOLESALE_OR_DEPIN", "https://cloud.vast.ai/", "https://console.vast.ai/api/v0", "oauth_portal", "VAST_API_KEY", "gpu"),
        PlatformNode("replicate", "Replicate", "WHOLESALE_OR_DEPIN", "https://replicate.com/account/api-tokens", "https://api.replicate.com/v1", "oauth_portal", "REPLICATE_API_TOKEN", "esrgan"),
        PlatformNode("piapi", "PiAPI", "WHOLESALE_OR_DEPIN", "https://piapi.ai/", "https://api.piapi.ai/api/v1", "oauth_portal", "PIAPI_KEY", "suno-v6"),
        PlatformNode("oracle_cloud_free", "Oracle Cloud Free ARM", "WHOLESALE_OR_DEPIN", "https://www.oracle.com/cloud/free/", "https://iaas.us-ashburn-1.oraclecloud.com", "oauth_portal", "OCI_TENANCY_OCID", "ampere-a1"),
        PlatformNode("modal_gpu", "Modal GPU", "WHOLESALE_OR_DEPIN", "https://modal.com", "https://api.modal.com", "oauth_portal", "MODAL_TOKEN_ID", "serverless-gpu")
    ]
    return {n.slug: n for n in nodes}


def create_credential_identity(idx: int, domain: str = "dev-node.io") -> Dict[str, str]:
    if idx <= len(EMBEDDED_USERNAMES):
        uname = EMBEDDED_USERNAMES[idx - 1]
    else:
        uname = f"{random.choice(ADJ)}_{random.choice(NOUN)}_{random.randint(100, 999)}"
    pw_chars = string.ascii_letters + string.digits + "!@#$%"
    return {
        "index": str(idx),
        "username": uname,
        "email": f"{uname}@{domain}",
        "password": "".join(secrets.choice(pw_chars) for _ in range(16)),
        "agent_name": f"agent_{uname}",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")
    }


def persist_credential_record(node: PlatformNode, ident: Dict[str, str], result: Dict[str, str]) -> Path:
    CREDS_DIR.mkdir(parents=True, exist_ok=True)
    path = CREDS_DIR / f"{node.slug}_{ident['username']}.txt"
    tok = result.get("api_key", "")
    text = (
        f"# {node.name} Credential File\n"
        f"platform: {node.slug}\n"
        f"signup_url: {node.signup_url}\n"
        f"api_base: {node.api_base}\n"
        f"env_key: {node.env_key}\n"
        f"username: {ident['username']}\n"
        f"email: {ident['email']}\n"
        f"password: {ident['password']}\n"
        f"fingerprint: {result.get('fingerprint', '')}\n"
        f"api_key: {tok}\n"
        f"status: {result.get('status', 'SAVED')}\n"
        f"farmed: {ident['timestamp']}\n"
    )
    with FILE_LOCK:
        path.write_text(text, encoding="utf-8")
        if tok and not tok.startswith("PENDING_") and not tok.startswith("YOUR_"):
            existing = set(POOL_FILE.read_text(encoding="utf-8").splitlines()) if POOL_FILE.exists() else set()
            line = f"{node.slug}:{tok}"
            if line not in existing:
                with open(POOL_FILE, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
    return path

#!/usr/bin/env python3
"""
Module 2: Multi-Path Proxy Harvester (jsDelivr/Fastly/GitHub Raw + Local Redis Pool)
and Dynamic Session IP Rotator.
"""

import json
import random
import re
from http.cookiejar import CookieJar
from typing import Dict, List, Optional, Tuple
from urllib.request import HTTPCookieProcessor, Request, build_opener

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"

PUBLIC_PROXY_FEEDS: List[str] = [
    "https://cdn.jsdelivr.net/gh/monosans/proxy-list@main/proxies/http.txt",
    "https://fastly.jsdelivr.net/gh/jetkai/proxy-list@main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all"
]


class MultiPathHttpSession:
    def __init__(self, brightdata_url: Optional[str] = None, local_pool_api: str = "http://127.0.0.1:5010"):
        self.brightdata_url = brightdata_url
        self.local_pool_api = local_pool_api
        self.session_id = random.randint(100000, 999999)
        self.harvested_proxies: List[str] = []
        self.jar = CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(self.jar))
        self.httpx = None
        self.client = None
        try:
            import httpx
            self.httpx = httpx
            self._rebuild_client()
        except ImportError:
            pass

    def _resolve_proxy(self) -> Optional[str]:
        if self.brightdata_url and "BRD_USER" not in self.brightdata_url:
            if "@" in self.brightdata_url:
                auth, host = self.brightdata_url.split("@", 1)
                if ":" in auth:
                    u, p = auth.rsplit(":", 1)
                    u = re.sub(r"-session-\d+", "", u)
                    return f"{u}-session-{self.session_id}:{p}@{host}"
            return self.brightdata_url
        if self.harvested_proxies:
            return f"http://{random.choice(self.harvested_proxies)}"
        return None

    def harvest_public_proxies(self) -> int:
        if not self.httpx:
            return 0
        with self.httpx.Client(timeout=5.0) as c:
            try:
                r = c.get(f"{self.local_pool_api}/get/")
                if r.status_code == 200 and "proxy" in r.json():
                    self.harvested_proxies.append(r.json()["proxy"])
            except Exception:
                pass
            for feed in random.sample(PUBLIC_PROXY_FEEDS, k=min(2, len(PUBLIC_PROXY_FEEDS))):
                try:
                    resp = c.get(feed)
                    if resp.status_code == 200:
                        items = [
                            ln.strip().split()[0]
                            for ln in resp.text.splitlines()
                            if ":" in ln and not ln.startswith("#")
                        ]
                        self.harvested_proxies.extend(items[:100])
                except Exception:
                    continue
        return len(self.harvested_proxies)

    def _rebuild_client(self) -> None:
        if not self.httpx:
            return
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass
        self.client = self.httpx.Client(
            proxy=self._resolve_proxy(),
            timeout=self.httpx.Timeout(12.0, connect=5.0),
            follow_redirects=True
        )

    def rotate_ip(self) -> None:
        self.session_id = random.randint(100000, 999999)
        self._rebuild_client()

    def request(
        self,
        method: str,
        url: str,
        payload: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Tuple[int, Dict]:
        hdrs = {"User-Agent": UA, "Accept": "application/json"}
        if payload is not None:
            hdrs["Content-Type"] = "application/json"
        if headers:
            hdrs.update(headers)

        if self.client:
            try:
                r = self.client.request(method, url, json=payload, headers=hdrs)
                try:
                    return r.status_code, r.json()
                except Exception:
                    return r.status_code, {"_raw": r.text[:250]}
            except Exception as exc:
                return 500, {"error": str(exc)}

        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = Request(url, data=data, headers=hdrs, method=method)
        try:
            r = self.opener.open(req, timeout=12)
            raw = r.read()
            return r.status, json.loads(raw) if raw else {}
        except Exception as exc:
            return getattr(exc, "code", 500), {"error": str(exc)}

#!/usr/bin/env python3
"""
Module 3: Protocol-Specific Self-Registration, Token Allocation & Verification Engine
"""

import os
import time
from typing import Dict
from module_1_registry_and_creds import PlatformNode
from module_2_network_and_proxy import MultiPathHttpSession


class PlatformProvisioner:
    def __init__(self, session: MultiPathHttpSession, backoff: float = 0.25, max_attempts: int = 5):
        self.session = session
        self.backoff = backoff
        self.max_attempts = max_attempts

    def provision(self, node: PlatformNode, identity: Dict[str, str], verify: bool = False) -> Dict[str, str]:
        if node.auth_mode == "dahl_fp":
            return self._provision_dahl(node, identity, verify)
        if node.auth_mode == "bazaar_post":
            return self._provision_bazaarlink(node, identity)
        return self._provision_env_or_portal(node, identity)

    def _provision_dahl(self, node: PlatformNode, identity: Dict[str, str], verify: bool) -> Dict[str, str]:
        origin = node.api_base.replace("/v1", "")
        hdrs = {"Referer": f"{origin}/account", "Origin": origin}
        for _ in range(self.max_attempts):
            st, body = self.session.request(
                "POST",
                f"{node.api_base}/auth/signup",
                payload={"username": identity["username"]},
                headers=hdrs
            )
            if st in (200, 201) and "fingerprint" in body:
                fp = body["fingerprint"]
                tok = body.get("api_key", {}).get("token", "")
                kid = body.get("api_key", {}).get("id", "")
                self.session.request("POST", f"{node.api_base}/auth/signin", {"fingerprint": fp}, hdrs)
                st_acc, acc = self.session.request("GET", f"{node.api_base}/account", headers=hdrs)
                pool = acc.get("token_balance", 0) if st_acc == 200 else 0
                if pool and kid:
                    self.session.request(
                        "POST",
                        f"{node.api_base}/account/allocate",
                        {"key_id": kid, "amount": pool},
                        hdrs
                    )
                if verify and tok:
                    self.session.request(
                        "POST",
                        f"{node.api_base}/chat/completions",
                        {"model": node.default_model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 4},
                        {"Authorization": f"Bearer {tok}"}
                    )
                return {"api_key": tok, "fingerprint": fp, "status": f"OK_POOL_{pool}"}
            self.session.rotate_ip()
            time.sleep(self.backoff)
        return {"api_key": f"PENDING_{node.env_key}", "fingerprint": identity["username"], "status": "BROWSER_GATE_403"}

    def _provision_bazaarlink(self, node: PlatformNode, identity: Dict[str, str]) -> Dict[str, str]:
        for _ in range(self.max_attempts):
            st, body = self.session.request(
                "POST",
                node.signup_url,
                payload={"name": identity["agent_name"]}
            )
            if st in (200, 201) and ("api_key" in body or "key" in body):
                return {
                    "api_key": body.get("api_key") or body.get("key", ""),
                    "fingerprint": body.get("claim_token", identity["agent_name"]),
                    "status": "OK_AGENT_REGISTERED"
                }
            self.session.rotate_ip()
            time.sleep(self.backoff)
        return {"api_key": f"PENDING_{node.env_key}", "fingerprint": identity["agent_name"], "status": "RETRY_LATER"}

    @staticmethod
    def _provision_env_or_portal(node: PlatformNode, identity: Dict[str, str]) -> Dict[str, str]:
        env_val = os.getenv(node.env_key, "")
        return {
            "api_key": env_val if env_val else f"PENDING_{node.env_key}",
            "fingerprint": identity["username"],
            "status": "ENV_ACTIVE" if env_val else "CREDENTIALS_GENERATED"
        }

#!/usr/bin/env python3
"""
Module 4: Parallel ThreadPool Orchestrator, Key Sync & Telegram Notifier CLI
"""

import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple
from module_1_registry_and_creds import (
    CREDS_DIR,
    ENV_VAULT_FILE,
    POOL_FILE,
    create_credential_identity,
    get_master_registry,
    persist_credential_record,
)
from module_2_network_and_proxy import MultiPathHttpSession
from module_3_provisioner_and_auth import PlatformProvisioner


def run_worker(idx: int, slugs: List[str], proxy: str, backoff: float) -> Tuple[int, int]:
    registry = get_master_registry()
    ident = create_credential_identity(idx)
    session = MultiPathHttpSession(brightdata_url=proxy)
    provisioner = PlatformProvisioner(session=session, backoff=backoff)
    ok_count = 0
    for slug in slugs:
        node = registry[slug]
        res = provisioner.provision(node, ident)
        persist_credential_record(node, ident, res)
        ok_count += 1
    return idx, ok_count


def main() -> None:
    ap = argparse.ArgumentParser(prog="module_4_orchestrator_cli")
    ap.add_argument("count", type=int, help="Number of account identities to provision")
    ap.add_argument("--category", default="ALL", choices=["ALL", "INSTANT_API", "GONKA_BROKER", "OAUTH_CARDLESS", "WHOLESALE_OR_DEPIN"])
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--proxy", default=None)
    ap.add_argument("--backoff", type=float, default=0.25)
    args = ap.parse_args()

    registry = get_master_registry()
    slugs = [k for k, v in registry.items() if args.category == "ALL" or v.category == args.category]

    t0 = time.time()
    total_records = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = [pool.submit(run_worker, i, slugs, args.proxy, args.backoff) for i in range(1, args.count + 1)]
        for f in as_completed(futs):
            idx, c = f.result()
            total_records += c
            print(f"[Worker #{idx:02d}] Provisioned {c} platform records", flush=True)

    print(f"Done: {total_records} records saved in {CREDS_DIR} ({time.time() - t0:.2f}s) | Pool: {POOL_FILE} | Vault: {ENV_VAULT_FILE}")


if __name__ == "__main__":
    main()
```
```


<!-- [ID:14_SEC_STEALTH_S002] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: :200 -->
# ── Klien Proxy Bright Data (HTTPX dengan Dynamic Rotating IP) ─────
class DahlBrightData:
    def __init__(self, proxy_url=None):
        import httpx
        self.httpx = httpx
        self.base_proxy = proxy_url or BRIGHTDATA_URL
        self.current_session = random.randint(100000, 999999)
        self._build_client()

    def _get_proxy_url(self):
        if "@" in self.base_proxy:
            auth_part, host_part = self.base_proxy.split("@", 1)
            if ":" in auth_part:
                user_part, pass_part = auth_part.rsplit(":", 1)
                user_part = re.sub(r"-session-\d+", "", user_part)
                auth_part = f"{user_part}-session-{self.current_session}:{pass_part}"
            else:
                auth_part = re.sub(r"-session-\d+", "", auth_part)
                auth_part = f"{auth_part}-session-{self.current_session}"
                
            return f"{auth_part}@{host_part}"
        return self.base_proxy

    def rotate_ip(self):
        """Memaksa ganti IP dengan meregenerasi Session ID Bright Data."""
        self.current_session = random.randint(100000, 999999)
        self._build_client()

    def _build_client(self):
        proxy = self._get_proxy_url()
        # Fast Timeout Settings: Connect 5s, Read 12s
        self.c = self.httpx.Client(
            proxy=proxy,
            timeout=self.httpx.Timeout(12.0, connect=5.0),
            follow_redirects=True
        )

    def _req(self, method, path, payload=None, extra=None, timeout=12):
        hdrs = {"User-Agent": UA, "Accept": "application/json",
                "Referer": f"{BASE}/account", "Origin": BASE}
        if payload is not None:
            hdrs["Content-Type"] = "application/json"
        if extra:
            hdrs.update(extra)

        try:
            r = self.c.request(method, BASE + path, json=payload, headers=hdrs, timeout=timeout)
            try:
                body = r.json()
            except Exception:
                body = {"_raw": r.text[:200]}
            return r.status_code, body
        except Exception:
            return 500, {}

    def signup(self, u):        return self._req("POST", "/v1/auth/signup", {"username": u})
    def signin(self, fp):       return self._req("POST", "/v1/auth/signin", {"fingerprint": fp})
    def account(self):          return self._req("GET", "/v1/account")
    def allocate(self, kid, a): return self._req("POST", "/v1/account/allocate", {"key_id": kid, "amount": a})
    def signout(self):          return self._req("POST", "/v1/auth/signout", {})
    def chat(self, model, tok):
        return self._req("POST", "/v1/chat/completions",
                         {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 4},
                         extra={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})


def do_signup(api, index, tag, backoff=0.5, max_tries=1000):
    """Signup terus menerus tanpa log error, merotasi IP hanya saat error/429."""
    attempt = 0
    while attempt < max_tries:
        attempt += 1
        need_rotate = False
        try:
            st, body = api.signup(rand_username())
            
            if st in (200, 201) and "fingerprint" in body:
                return body, st
            
            if st == 429 or st >= 400:
                need_rotate = True

        except Exception:
            need_rotate = True

        if need_rotate:
            if hasattr(api, "rotate_ip"):
                api.rotate_ip()
            if backoff > 0:
                time.sleep(backoff)

    raise RuntimeError("signup exhausted")


def finish_account(api, body, index, tag, model, skip_chat):
    """Signin -> allocate pool -> verify -> save."""
    fp, tok, kid = body["fingerprint"], body["api_key"]["token"], body["api_key"]["id"]
    st, _ = api.signin(fp)
    if st != 200:
        raise RuntimeError(f"signin HTTP {st}")
    pool = 0
    st, acc = api.account()
    if st == 200:
        pool = acc.get("token_balance", 0)
    if pool:
        try:
            api.allocate(kid, pool)
        except Exception:
            pass
    if not skip_chat:
        try:
            api.chat(model, tok)
        except Exception:
            pass
    try:
        api.signout()
    except Exception:
        pass
    f = save_cred(body, index)
    print(f"[{index:02d}{tag}] OK tok={tok[:12]}… pool={pool} SAVED {f.name}", flush=True)
    return tok


def worker_process(index, args, proxy_str):
    """Fungsi pembantu yang dijalankan oleh tiap Thread Worker."""
    try:
        api = DahlBrightData(proxy_url=proxy_str)
        body, st = do_signup(api, index, "[bright]", backoff=args.backoff)
        tok = finish_account(api, body, index, "[bright]", args.model, args.skip_chat)
        return True, tok
    except Exception:
        print(f"[{index:02d}] FAILED", flush=True)
        return False, index



<!-- [ID:14_SEC_STEALTH_S003] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# ── Klien Sequential Direct (Urllib) ─────────────────────────────
class Dahl:
    def __init__(self):
        self.jar = CookieJar()
        self.op = build_opener(HTTPCookieProcessor(self.jar))

    def _req(self, method, path, payload=None, extra=None, timeout=15):
        url = BASE + path
        data = json.dumps(payload).encode() if payload is not None else None
        hdrs = {"User-Agent": UA, "Accept": "application/json",
                "Referer": f"{BASE}/account", "Origin": BASE}
        if data is not None:
            hdrs["Content-Type"] = "application/json"
        if extra:
            hdrs.update(extra)
        req = Request(url, data=data, headers=hdrs, method=method)
        try:
            r = self.op.open(req, timeout=timeout)
            status, raw = r.status, r.read()
        except Exception as e:
            code = getattr(e, "code", None)
            raw = getattr(e, "read", lambda: b"")() if code else b""
            if code:
                status, raw = code, raw
            else:
                raise RuntimeError(f"network error {url}: {e}")
        try:
            body = json.loads(raw) if raw else {}
        except Exception:
            body = {"_raw": raw.decode(errors="replace")}
        return status, body

    def signup(self, u):            return self._req("POST", "/v1/auth/signup", {"username": u})
    def signin(self, fp):           return self._req("POST", "/v1/auth/signin", {"fingerprint": fp})
    def account(self):              return self._req("GET", "/v1/account")
    def allocate(self, kid, amt):   return self._req("POST", "/v1/account/allocate", {"amount": amt, "key_id": kid})
    def signout(self):              return self._req("POST", "/v1/auth/signout")
    def chat(self, model, tok, content="ping"):
        return self._req("POST", "/v1/chat/completions",
                         {"model": model, "messages": [{"role": "user", "content": content}], "max_tokens": 4},
                         extra={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})



<!-- [ID:14_SEC_STEALTH_S004] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR, DICT, :300 -->
# ── Multi-Path Rotating HTTP Client ─────────────────────────────────
class RotatingPlatformClient:
    """Supports Bright Data dynamic session rotation, local proxy_pool (5010), or direct HTTPX/Urllib."""
    def __init__(self, proxy_url: Optional[str] = None, use_brightdata: bool = False):
        self.base_proxy = proxy_url or (BRIGHTDATA_URL if use_brightdata else None)
        self.current_session = random.randint(100000, 999999)
        self.jar = CookieJar()
        self.urllib_opener = build_opener(HTTPCookieProcessor(self.jar))
        self.httpx_mod = None
        self.client = None
        try:
            import httpx
            self.httpx_mod = httpx
            self._build_httpx()
        except ImportError:
            pass

    def _format_proxy(self) -> Optional[str]:
        if not self.base_proxy or "BRD_USER" in self.base_proxy:
            return None
        if "@" in self.base_proxy:
            auth_part, host_part = self.base_proxy.split("@", 1)
            if ":" in auth_part:
                user_part, pass_part = auth_part.rsplit(":", 1)
                user_part = re.sub(r"-session-\d+", "", user_part)
                auth_part = f"{user_part}-session-{self.current_session}:{pass_part}"
            return f"{auth_part}@{host_part}"
        return self.base_proxy

    def _build_httpx(self) -> None:
        if not self.httpx_mod:
            return
        proxy = self._format_proxy()
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass
        self.client = self.httpx_mod.Client(
            proxy=proxy,
            timeout=self.httpx_mod.Timeout(15.0, connect=6.0),
            follow_redirects=True
        )

    def rotate_ip(self) -> None:
        self.current_session = random.randint(100000, 999999)
        self._build_httpx()

    def request_json(
        self,
        method: str,
        url: str,
        payload: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 12
    ) -> Tuple[int, Dict]:
        hdrs = {
            "User-Agent": UA,
            "Accept": "application/json",
        }
        if payload is not None:
            hdrs["Content-Type"] = "application/json"
        if headers:
            hdrs.update(headers)

        if self.client:
            try:
                r = self.client.request(method, url, json=payload, headers=hdrs, timeout=timeout)
                try:
                    return r.status_code, r.json()
                except Exception:
                    return r.status_code, {"_raw": r.text[:300]}
            except Exception as e:
                return 500, {"error": str(e)}

        # Fallback to standard library urllib
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = Request(url, data=data, headers=hdrs, method=method)
        try:
            r = self.urllib_opener.open(req, timeout=timeout)
            raw = r.read()
            return r.status, json.loads(raw) if raw else {}
        except Exception as e:
            code = getattr(e, "code", 500)
            return code, {"error": str(e)}


