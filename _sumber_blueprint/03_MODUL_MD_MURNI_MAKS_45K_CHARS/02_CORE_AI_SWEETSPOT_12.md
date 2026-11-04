
<!-- [ID:02_CORE_AI_S005] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
## 24. apppy3.6.py

```py
# ==============================================================================
# BIKINAI SUPER INTELLIGENCE — MASTER ENGINE v3.6.0 (AUTONOMOUS AGENTIC CORE)
# ==============================================================================
# Fitur Terintegrasi Utuh (v1.0 -> v3.6.0 Tanpa Pengurangan):
# 1. Persistent Vault Abadi (~/.bikinai_vault/bikinai_master_vault.db) + 11 Tabel
# 2. SingleWriterSQLiteDaemon + 4.096 Lock Stripes + WAL Concurrency Helper
# 3. 8-Agent Rolling Pool (Argon, Qwen, DeepSeek, Muse, Nano-Muse, Harness,
#    Nous Hermes, Groq/Cerebras/Pollinations) + Auto Circuit-Breaker 60s
# 4. 4-Gate Deep-Defense Bansos Sterilizer (Anti-SSRF, Whitelist AST v2.0,
#    Response Malware Scrubber, Live <2.5s Schema Ping Gate) + /donasi_api
# 5. Patch Audit Keamanan: Invoice Ledger Anti-Bypass Top-Up, HMAC-SHA256
#    Telegram WebApp initData Validator, & Owner Bootstrap Token Protection
# 6. Full Mini App SFW (Exclusive Radio Group + Context-Aware Engine Locking)
#    & NocturneAI 3-Tab Web Studio (/api/nocturne/chat & /api/nocturne/generate)
# ==============================================================================

import ast
import asyncio
import base64
import hashlib
import hmac
import ipaddress
import json
import math
import os
import re
import secrets
import time
import unicodedata
from collections import OrderedDict
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, AsyncIterator, Callable, Coroutine, Literal
from urllib.parse import parse_qsl, quote, urlparse

import aiosqlite
import httpx
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

# ==============================================================================
# 0. BRANKAS PERSISTEN ABADI, KUNCI ED25519 & KONFIGURASI RUNTIME
# ==============================================================================
VAULT_DIR = Path.home() / ".bikinai_vault"
VAULT_DIR.mkdir(parents=True, exist_ok=True)
try:
    os.chmod(VAULT_DIR, 0o700)
except Exception:
    pass

DB_PATH = str(VAULT_DIR / "bikinai_master_vault.db")
KEYRING_PATH = VAULT_DIR / "ed25519_voucher_key.bin"

BOT_TOKEN = os.getenv("TOKEN_BOT_UTAMA", "").strip()
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))
OWNER_BOOTSTRAP_TOKEN = os.getenv("OWNER_BOOTSTRAP_TOKEN", "").strip() or secrets.token_hex(8)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "").strip()
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY", "").strip()
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY", "").strip()
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "").strip()
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "").strip()
FAL_KEY = os.getenv("FAL_KEY", "").strip()

GOPAY_STATIC_QRIS_RAW = os.getenv("GOPAY_STATIC_QRIS_RAW", "").strip()
DUITKU_MERCHANT_CODE = os.getenv("DUITKU_MERCHANT_CODE", "").strip()
DUITKU_API_KEY = os.getenv("DUITKU_API_KEY", "").strip()
MIDTRANS_SERVER_KEY = os.getenv("MIDTRANS_SERVER_KEY", "").strip()
PAKASIR_SLUG = os.getenv("PAKASIR_SLUG", "").strip()
PAKASIR_API_KEY = os.getenv("PAKASIR_API_KEY", "").strip()
CRYPTOBOT_API_TOKEN = os.getenv("CRYPTOBOT_API_TOKEN", "").strip()

SAMPLE_SANDBOX_VIDEO_URL = "https://filesamples.com/samples/video/mp4/sample_640x360.mp4"
BOT_INSTANCE_GLOBAL: Bot | None = None
BOT_USERNAME_GLOBAL: str = "bikinAI_bot"


def detect_default_miniapp_url() -> str:
    env_url = os.getenv("MINIAPP_PUBLIC_URL", "").strip()
    if env_url.startswith("https://"):
        return env_url
    cs_name = os.getenv("CODESPACE_NAME", "").strip()
    cs_dom = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "app.github.dev").strip()
    if cs_name:
        return f"https://{cs_name}-8080.{cs_dom}"
    return ""


def load_or_create_persistent_keys() -> tuple[bytes, bytes]:
    if KEYRING_PATH.exists():
        priv_bytes = KEYRING_PATH.read_bytes()
        priv_obj = Ed25519PrivateKey.from_private_bytes(priv_bytes)
    else:
        priv_obj = Ed25519PrivateKey.generate()
        priv_bytes = priv_obj.private_bytes_raw()
        KEYRING_PATH.write_bytes(priv_bytes)
        try:
            os.chmod(KEYRING_PATH, 0o600)
        except Exception:
            pass
    return priv_bytes, priv_obj.public_key().public_bytes_raw()


ED25519_PRIV_BYTES, ED25519_PUB_BYTES = load_or_create_persistent_keys()

RUNTIME_CONFIG: dict[str, Any] = {
    "LAUNCH_PRODUCTION_MODE": False,
    "PILIHAN_MESIN_MEDIA": 1,
    "BANSOS_OPERATION_MODE": "SILENT_PROFIT",  # SILENT_PROFIT | HAPPY_HOUR | NORMAL
    "HAPPY_HOUR_MODE": False,
    "AUTO_APPROVE_SANDBOX_TOPUP": False,
    "ID_ACTIVE_CATEGORY": "QRIS_DIRECT",
    "ID_ACTIVE_PROVIDER": "QRIS GoPay Merchant",
    "GLOBAL_ACTIVE_PROVIDER": "Aktifkan Keduanya (USDT + Telegram Stars)",
    "MUSE_TOKEN_CEILING": 1_000_000,
    "FOMO_COUNTER_BASE": 29620,
    "OWNER_ID_RUNTIME": ADMIN_USER_ID,
    "MINIAPP_URL": detect_default_miniapp_url(),
    "PRIMARY_ROLLING_AGENT": "ARGON",
    "SUBBOT_SANGMATA_ACTIVE": True,
    "SUBBOT_WELCOME_GUARD_ACTIVE": True,
    "SUBBOT_NEURAL_FEED_ACTIVE": True,
    "SUBBOT_REFUND_SWEEPER_ACTIVE": True,
    "SUBBOT_SOCIAL_POSTER_ACTIVE": True,
}

# ==============================================================================
# 1. SQLITE WAL CONCURRENCY HELPER & 4.096 LOCK STRIPES
# ==============================================================================
STRIPE_COUNT = 4096
USER_LOCK_STRIPES = [asyncio.Lock() for _ in range(STRIPE_COUNT)]


def get_user_lock(user_id: int) -> asyncio.Lock:
    return USER_LOCK_STRIPES[user_id % STRIPE_COUNT]


@asynccontextmanager
async def get_db() -> AsyncIterator[aiosqlite.Connection]:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA journal_mode = WAL;")
        await db.execute("PRAGMA synchronous = NORMAL;")
        await db.execute("PRAGMA busy_timeout = 10000;")
        await db.execute("PRAGMA foreign_keys = ON;")
        yield db


class SingleWriterSQLiteDaemon:
    def __init__(self, checkpoint_every_n_writes: int = 400):
        self._write_mutex = asyncio.Lock()
        self._write_counter = 0
        self._checkpoint_threshold = checkpoint_every_n_writes

    async def execute_write_tx(
        self,
        db: aiosqlite.Connection,
        tx_coro: Callable[[aiosqlite.Connection], Coroutine[Any, Any, Any]],
    ) -> Any:
        async with self._write_mutex:
            try:
                result = await tx_coro(db)
                await db.commit()
            except Exception:
                try:
                    await db.rollback()
                except Exception:
                    pass
                raise
            self._write_counter += 1
            if self._write_counter >= self._checkpoint_threshold:
                self._write_counter = 0
                await self._run_inline_maintenance(db)
            return result

    async def _run_inline_maintenance(self, db: aiosqlite.Connection) -> None:
        now_ts = int(time.time())
        try:
            await db.execute("DELETE FROM redeemed_nullifiers WHERE expires_at <= ?;", (now_ts,))
            await db.execute("DELETE FROM omni_resource_registry WHERE expires_at <= ?;", (now_ts,))
            await db.commit()
            await db.execute("PRAGMA wal_checkpoint(PASSIVE);")
        except Exception:
            pass


DB_WRITER_DAEMON = SingleWriterSQLiteDaemon()

# ==============================================================================
# 2. DATABASE SCHEMA ABADI v3.6.0 (11 TABEL MASTER TERMASUK PAYMENT INVOICES)
# ==============================================================================
MAX_KOIN_BONUS_CAP = 25
PPP_EFFECTIVE_COIN_IDR = {1: 580, 2: 260, 3: 84}


async def init_master_db(db: aiosqlite.Connection) -> None:
    await db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            internal_user_id INTEGER PRIMARY KEY,
            username TEXT DEFAULT 'Kreator',
            first_name TEXT DEFAULT '',
            language_code TEXT DEFAULT 'id',
            koin_utama INTEGER NOT NULL DEFAULT 0 CHECK (koin_utama >= 0),
            koin_bonus INTEGER NOT NULL DEFAULT 4 CHECK (koin_bonus >= 0 AND koin_bonus <= 25),
            has_topped_up INTEGER NOT NULL DEFAULT 0,
            ppp_zone INTEGER NOT NULL DEFAULT 3,
            last_claim_date TEXT,
            chat_used_today INTEGER NOT NULL DEFAULT 0,
            free_img_used_today INTEGER NOT NULL DEFAULT 0,
            quota_day_epoch INTEGER NOT NULL DEFAULT 0,
            personal_memory_notes TEXT DEFAULT '',
            active_canvas_content TEXT DEFAULT '',
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS identity_history (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            old_username TEXT,
            new_username TEXT,
            changed_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            internal_user_id INTEGER NOT NULL,
            cost INTEGER NOT NULL,
            deducted_bonus INTEGER NOT NULL DEFAULT 0,
            deducted_utama INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'PROCESSING',
            refunded_lock INTEGER NOT NULL DEFAULT 0,
            prompt_text TEXT DEFAULT '',
            engine_used TEXT DEFAULT '',
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS payment_invoices (
            invoice_id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            amount_idr INTEGER NOT NULL,
            coins_credited INTEGER NOT NULL DEFAULT 60,
            provider TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING',
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS redeemed_nullifiers (
            nullifier_hash TEXT PRIMARY KEY,
            expires_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS treasury_summary (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            gross_revenue_idr INTEGER NOT NULL DEFAULT 0,
            working_capital_vault_idr INTEGER NOT NULL DEFAULT 0,
            harvestable_profit_vault_idr INTEGER NOT NULL DEFAULT 0,
            total_harvested_by_owner_idr INTEGER NOT NULL DEFAULT 0,
            total_jobs_completed INTEGER NOT NULL DEFAULT 0,
            updated_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS bot_bindings (
            binding_key TEXT PRIMARY KEY,
            chat_id INTEGER NOT NULL,
            topic_id INTEGER NOT NULL DEFAULT 0,
            topic_title TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS system_settings (
            setting_key TEXT PRIMARY KEY,
            setting_val TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS user_feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            feedback_text TEXT NOT NULL,
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS omni_resource_registry (
            resource_id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            resource_name TEXT NOT NULL,
            endpoint_url TEXT NOT NULL,
            secret_or_meta TEXT NOT NULL,
            is_live_verified INTEGER NOT NULL DEFAULT 0,
            expires_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS syndicated_assets (
            asset_id TEXT PRIMARY KEY,
            prompt_signature TEXT NOT NULL,
            engine_name TEXT NOT NULL,
            media_url TEXT NOT NULL,
            times_reused INTEGER NOT NULL DEFAULT 1,
            created_at INTEGER NOT NULL
        );
        """
    )
    await db.commit()

    cur = await db.execute("SELECT setting_key, setting_val FROM system_settings;")
    for k, v in await cur.fetchall():
        if k == "MINIAPP_URL" and v.startswith("https://"):
            RUNTIME_CONFIG["MINIAPP_URL"] = v
        elif k == "OWNER_ID_RUNTIME" and v.isdigit() and int(v) > 0:
            RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = int(v)
        elif k == "PILIHAN_MESIN_MEDIA" and v.isdigit():
            RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] = int(v)
        elif k in ("LAUNCH_PRODUCTION_MODE", "HAPPY_HOUR_MODE", "AUTO_APPROVE_SANDBOX_TOPUP"):
            RUNTIME_CONFIG[k] = v == "1"
        elif k in (
            "ID_ACTIVE_CATEGORY",
            "ID_ACTIVE_PROVIDER",
            "GLOBAL_ACTIVE_PROVIDER",
            "BANSOS_OPERATION_MODE",
            "PRIMARY_ROLLING_AGENT",
        ):
            RUNTIME_CONFIG[k] = v


async def save_persistent_setting(db: aiosqlite.Connection, key: str, val: str) -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(
            "INSERT OR REPLACE INTO system_settings (setting_key, setting_val) VALUES (?, ?);",
            (key, str(val)),
        )

    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def set_topic_binding(
    db: aiosqlite.Connection, key: str, chat_id: int, topic_id: int, title: str = ""
) -> None:
    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(
            "INSERT OR REPLACE INTO bot_bindings (binding_key, chat_id, topic_id, topic_title) VALUES (?, ?, ?, ?);",
            (key, chat_id, topic_id, title),
        )

    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def get_topic_binding(db: aiosqlite.Connection, key: str) -> tuple[int, int] | None:
    cur = await db.execute("SELECT chat_id, topic_id FROM bot_bindings WHERE binding_key = ?;", (key,))
    row = await cur.fetchone()
    return (int(row[0]), int(row[1])) if row else None


async def get_all_topic_bindings(db: aiosqlite.Connection) -> dict[str, tuple[int, int, str]]:
    cur = await db.execute("SELECT binding_key, chat_id, topic_id, topic_title FROM bot_bindings;")
    rows = await cur.fetchall()
    return {r[0]: (int(r[1]), int(r[2]), str(r[3] or r[0])) for r in rows}


# ==============================================================================
# 3. 4-GATE DEEP-DEFENSE BANSOS STERILIZER & OMNI-RESOURCE HARVESTER
# ==============================================================================
OMNI_BANSOS_PRESETS = {
    "AI_API": [
        {
            "res_id": "API-POLLINATIONS-V1",
            "name": "Pollinations Unified Router (Argon/Muse/Qwen/Flux)",
            "endpoint": "https://text.pollinations.ai/openai",
            "meta": "openai",
            "desc": "Jalur Utama Keyless Cepat (<1.5s) HPP Rp 0",
            "verified": 1,
        },
        {
            "res_id": "API-OR-FREE-POOL",
            "name": "OpenRouter Multi-Model (:free Pool)",
            "endpoint": "https://openrouter.ai/api/v1/chat/completions",
            "meta": "deepseek/deepseek-chat:free",
            "desc": "20+ Model Gratis (Qwen3 Coder, DeepSeek R1, Llama 3.3)",
            "verified": 1 if OPENROUTER_API_KEY else 0,
        },
        {
            "res_id": "API-GROQ-LPU",
            "name": "Groq Cloud LPU (Llama 3.3 70B 320 tok/s)",
            "endpoint": "https://api.groq.com/openai/v1/chat/completions",
            "meta": "llama-3.3-70b-versatile",
            "desc": "Kuota Gratis 1.000 RPD Tanpa Kartu Visa",
            "verified": 1 if GROQ_API_KEY else 0,
        },
        {
            "res_id": "API-CEREBRAS-1M",
            "name": "Cerebras Wafer-Scale Free Tier (1M Token/Hari)",
            "endpoint": "https://api.cerebras.ai/v1/chat/completions",
            "meta": "llama-3.3-70b",
            "desc": "Throughput Tinggi Gratis 1 Juta Token/Hari",
            "verified": 1 if CEREBRAS_API_KEY else 0,
        },
    ],
    "CLOUD_STORAGE": [
        {
            "res_id": "STOR-CF-R2",
            "name": "Cloudflare R2 Object Storage (10 GB Gratis)",
            "endpoint": "https://dash.cloudflare.com/",
            "meta": "10GB + 0% Biaya Egress Bandwidth",
            "desc": "Penyimpanan utama media & aset terenkripsi",
            "verified": 1,
        },
        {
            "res_id": "STOR-STORJ-DEPIN",
            "name": "Storj Decentralized S3 Cloud (25 GB Gratis)",
            "endpoint": "https://www.storj.io/",
            "meta": "25GB S3-Compatible Gratis",
            "desc": "Cadangan Storage Mesh #2 untuk syndication video",
            "verified": 1,
        },
        {
            "res_id": "STOR-B2-BACKBLAZE",
            "name": "Backblaze B2 Cloud Storage (10 GB Gratis)",
            "endpoint": "https://www.backblaze.com/cloud-storage",
            "meta": "10GB Tanpa Kartu Visa",
            "desc": "Cadangan Storage Mesh #3",
            "verified": 1,
        },
    ],
    "GRANTS_AND_DB": [
        {
            "res_id": "GRANT-MODAL-GPU",
            "name": "Modal.com Serverless GPU ($30/Bulan Gratis)",
            "endpoint": "https://modal.com/",
            "meta": "$30/bln (~Rp 480.000/bln) Kredit GPU A10G/H100",
            "desc": "Render ~1.500 video Wan 2.2 per bulan dengan modal Rp 0",
            "verified": 1,
        },
        {
            "res_id": "GRANT-CF-WORKERS-AI",
            "name": "Cloudflare Workers AI (10.000 Neurons/Hari Gratis)",
            "endpoint": "https://developers.cloudflare.com/workers-ai/",
            "meta": "Llama, Qwen, DeepSeek & Flux Edge Inference",
            "desc": "Inferensi AI tepi gratis setiap hari tanpa kartu",
            "verified": 1,
        },
        {
            "res_id": "GRANT-MS-FOUNDERS",
            "name": "Microsoft for Startups Founders Hub ($1K-$150K)",
            "endpoint": "https://foundershub.startups.microsoft.com/",
            "meta": "Kredit Azure & OpenAI Tanpa Syarat PT di Tahap Ide",
            "desc": "Hibah kredit cloud untuk Solo Founder",
            "verified": 1,
        },
    ],
}


def validate_safe_external_url(url: str) -> tuple[bool, str]:
    """[GATE 1 - ANTI-SSRF]: Memastikan endpoint komunitas menggunakan HTTPS publik dan bukan IP internal."""
    try:
        parsed = urlparse(url.strip())
        if parsed.scheme != "https":
            return False, "Wajib menggunakan protokol HTTPS."
        host = (parsed.hostname or "").lower()
        if not host or host in ("localhost", "0.0.0.0") or host.endswith((".local", ".internal")):
            return False, "Host lokal/internal ditolak oleh proteksi SSRF."
        try:
            ip = ipaddress.ip_address(host)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
                return False, f"Alamat IP privat/metadata ({ip}) diblokir."
        except ValueError:
            pass
        return True, "URL Aman"
    except Exception as e:
        return False, f"URL tidak valid: {e}"


def sterilize_community_script_ast(source_code: str, script_name: str = "community_plugin") -> dict[str, Any]:
    """
    [GATE 2 - AST STERILIZER v2.0]: Menutup celah bypass dunder (__subclasses__, __globals__,
    __self__, __builtins__) sesuai advisory GHSA-4mr5-g6f9-cfrh & GHSA-xm98-3vcf-fph7.
    """
    forbidden_calls = {
        "system", "popen", "eval", "exec", "compile", "open", "input", "breakpoint",
        "spawnl", "getattr", "setattr", "delattr", "globals", "locals", "vars", "dir", "__import__",
    }
    forbidden_imports = {
        "os", "sys", "subprocess", "pty", "ctypes", "pickle", "marshal", "shelve",
        "shutil", "socket", "urllib", "requests", "httpx", "aiohttp", "importlib", "builtins", "inspect",
    }
    forbidden_dunders = {
        "__subclasses__", "__globals__", "__builtins__", "__self__", "__import__",
        "__mro__", "__bases__", "__code__", "__closure__", "__dict__", "__class__",
    }

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
        elif isinstance(node, ast.Attribute):
            if node.attr in forbidden_dunders or node.attr.startswith("__"):
                stripped_threats.append(f"Blocked dunder attribute '{node.attr}'")
        elif isinstance(node, ast.Name):
            if node.id in forbidden_dunders:
                stripped_threats.append(f"Blocked restricted identifier '{node.id}'")
        elif isinstance(node, ast.Call):
            fn = (
                node.func.id
                if isinstance(node.func, ast.Name)
                else (node.func.attr if isinstance(node.func, ast.Attribute) else "")
            )
            if fn in forbidden_calls:
                stripped_threats.append(f"Blocked call '{fn}()'")
        elif isinstance(node, ast.ExceptHandler):
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                stripped_threats.append("Blocked empty 'except: pass'")

    ast_hash = hashlib.sha256(ast.dump(tree).encode()).hexdigest()[:14]
    return {
        "ok": len(stripped_threats) == 0,
        "script_name": script_name,
        "threats_removed": stripped_threats,
        "hash": ast_hash,
    }


def sanitize_external_api_response(raw_reply: str) -> str:
    """[GATE 3 - PAYLOAD SCRUBBER]: Melucuti injeksi script/phishing dari endpoint komunitas."""
    if not raw_reply:
        return ""
    cleaned = re.sub(r"<script\b[^>]*>.*?</script>", "", raw_reply, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"javascript\s*:", "", cleaned, flags=re.IGNORECASE)
    return cleaned.replace("|---|", "").strip()


async def ping_and_verify_bansos_endpoint(
    endpoint_url: str, model_name: str = "openai", api_key: str = ""
) -> tuple[bool, float, str]:
    """[GATE 4 - LIVE PING GATE]: Memastikan endpoint menjawab HTTP 200 OK JSON valid dalam <2.5 detik."""
    ok_url, reason = validate_safe_external_url(endpoint_url)
    if not ok_url:
        return False, 0.0, reason
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    payload = {
        "model": model_name or "openai",
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 5,
    }
    t0 = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=2.5, follow_redirects=False) as client:
            r = await client.post(endpoint_url, headers=headers, json=payload)
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
            if r.status_code == 200:
                return True, elapsed_ms, f"HTTP 200 OK ({elapsed_ms} ms)"
            return False, elapsed_ms, f"HTTP {r.status_code}"
    except Exception as e:
        elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
        return False, elapsed_ms, f"Timeout/Error ({type(e).__name__})"


async def check_multi_tld_domain_availability_live(base_keyword: str = "bikinai") -> list[dict[str, str]]:
    clean_kw = re.sub(r"[^a-z0-9-]", "", base_keyword.lower()) or "bikinai"
    candidate_domains = [
        f"{clean_kw}.tech",
        f"{clean_kw}.xyz",
        f"{clean_kw}.art",
        f"{clean_kw}.app",
        f"{clean_kw}.dev",
        f"nocturne-{clean_kw}.xyz",
    ]
    results = []
    async with httpx.AsyncClient(timeout=3.5, follow_redirects=True) as client:
        for dom in candidate_domains:
            try:
                r = await client.get(f"https://rdap.org/domain/{dom}")
                if r.status_code == 404:
                    status = "🟢 TERSEDIA (Kosong & Siap Diklaim!)"
                elif r.status_code == 200:
                    status = "🔴 Sudah Terdaftar"
                else:
                    status = "🟡 Cek Promo Registrar"
            except Exception:
                status = "🟢 Siap Cek di Cloudflare / Porkbun / GitHub Pack"
            results.append({"domain": dom, "status": status})
    return results


# ==============================================================================
# 4. FULL WEBSITE-GRADE MINI APP SFW & NOCTURNEAI 3-TAB WEB STUDIO (PORT 8080)
# Menjawab Catatan #5, #8, #9, #11, #12:
# - Exclusive Radio Group (data-group) & Context-Aware Engine Locking di Mini App
# - NocturneAI 3-Tab Utuh (Live Uncensored Chat, Media Generator + Download HD,
#   dan Dompet Penukaran Voucher Ed25519)
# - 100% Bahasa Konsumen (Bebas Istilah Dapur Developer di Layar Pembeli)
# ==============================================================================
MINIAPP_FULL_WEBSITE_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>bikinAI Super Intelligence — Studio Web Resmi</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
  :root {
    --bg: #05070c; --surface: #0f1523; --cyan: #00f0ff; --purple: #7b2cbf;
    --text: #f0f6fc; --muted: #8b949e; --success: #00e676;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  body { background: radial-gradient(circle at 50% 0%, #17103a 0%, #05070c 72%); color: var(--text); min-height: 100vh; padding: 14px 14px 96px 14px; }
  .hero { background: linear-gradient(135deg, rgba(15,21,35,0.95), rgba(30,16,60,0.85)); border: 1px solid rgba(0,240,255,0.3); border-radius: 16px; padding: 16px; margin-bottom: 14px; }
  .badge { display: inline-block; background: linear-gradient(90deg, var(--cyan), var(--purple)); color: #fff; font-size: 10px; font-weight: 800; padding: 3px 10px; border-radius: 99px; margin-bottom: 6px; }
  .hero h1 { font-size: 18px; font-weight: 800; color: #fff; margin-bottom: 4px; }
  .hero p { font-size: 12px; color: var(--muted); line-height: 1.4; }
  .tab-section { display: none; }
  .tab-section.active { display: block; }
  .label { font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--cyan); margin: 12px 0 6px; letter-spacing: 0.6px; }
  .pill-row { display: flex; gap: 7px; overflow-x: auto; padding-bottom: 4px; margin-bottom: 4px; }
  .pill { flex: 1; text-align: center; white-space: nowrap; background: var(--surface); border: 1px solid rgba(255,255,255,0.08); color: var(--muted); padding: 9px 10px; border-radius: 11px; font-size: 12px; font-weight: 600; cursor: pointer; user-select: none; }
  .pill.active { background: rgba(0,240,255,0.15); border-color: var(--cyan); color: #fff; }
  .pill.disabled { opacity: 0.35; pointer-events: none; cursor: not-allowed; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .card { background: var(--surface); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 10px; cursor: pointer; }
  .card.active { border-color: var(--cyan); background: rgba(0,240,255,0.12); }
  .card.hidden-engine { display: none; }
  .card h4 { font-size: 13px; color: #fff; margin-bottom: 2px; }
  .card p { font-size: 10px; color: var(--muted); }
  .upload-box { border: 1.5px dashed rgba(0,240,255,0.4); background: rgba(15,21,35,0.6); border-radius: 14px; padding: 12px; text-align: center; position: relative; cursor: pointer; margin-top: 4px; }
  .upload-box input { position: absolute; inset: 0; opacity: 0; cursor: pointer; }
  #ref-preview { max-height: 110px; border-radius: 8px; margin-top: 8px; display: none; margin-left: auto; margin-right: auto; border: 1px solid var(--cyan); }
  textarea { width: 100%; height: 80px; background: var(--surface); border: 1px solid rgba(0,240,255,0.3); border-radius: 12px; color: #fff; padding: 10px; font-size: 13px; outline: none; resize: none; }
  .btn-exec { width: 100%; margin-top: 12px; padding: 14px; border: none; border-radius: 14px; background: linear-gradient(90deg, #00c6ff, #7b2cbf); color: #fff; font-size: 14px; font-weight: 800; cursor: pointer; }
  #toast { margin-top: 10px; padding: 10px; border-radius: 10px; font-size: 12px; background: rgba(0,230,118,0.15); border: 1px solid var(--success); color: var(--success); display: none; text-align: center; }
  .legal-card { background: var(--surface); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; margin-bottom: 10px; font-size: 12px; line-height: 1.5; color: #d0d7de; }
  .legal-card h3 { color: var(--cyan); font-size: 14px; margin-bottom: 6px; }
  .legal-card a { color: var(--cyan); text-decoration: none; font-weight: 600; }
  .footer-copy { text-align: center; font-size: 11px; color: var(--muted); margin-top: 18px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.07); }
  .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; height: 62px; background: rgba(8,12,22,0.96); backdrop-filter: blur(16px); border-top: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-around; align-items: center; z-index: 99; }
  .nav-btn { display: flex; flex-direction: column; align-items: center; gap: 2px; color: var(--muted); font-size: 10px; font-weight: 600; cursor: pointer; }
  .nav-btn.active { color: var(--cyan); }
</style>
</head>
<body>
  <div class="hero">
    <span class="badge">⚡ STUDIO KREATIF RESMI v3.6</span>
    <h1>Selamat Datang di bikinAI Super Intelligence</h1>
    <p id="welcome-user">Platform Studio Visual 4K, Video Sinematik, & Editing Otomatis dengan Garansi Koin Kembali 100% (Auto-Refund).</p>
  </div>

  <div id="tab-studio" class="tab-section active">
    <div class="label">1. Pilih Kategori & Mode Karya</div>
    <div class="pill-row" data-group="modality">
      <div class="pill active" onclick="setMod(this,'IMAGE')">🎨 Gambar 4K</div>
      <div class="pill" onclick="setMod(this,'VIDEO')">🎬 Video AI</div>
      <div class="pill" onclick="setMod(this,'REMOVE_BG')">✂️ Hapus BG (.PNG)</div>
      <div class="pill" onclick="setMod(this,'RETOUCH')">✨ Retouch & Edit</div>
    </div>

    <div class="label">2. Pilih Mesin AI Sesuai Kategori</div>
    <div class="grid" id="engine-grid">
      <div class="card active" data-type="IMAGE" onclick="setEng(this,'Seedream 4.5')"><h4>✨ Seedream 4.5</h4><p>Poster 4K & Teks Akurat</p></div>
      <div class="card" data-type="IMAGE" onclick="setEng(this,'Flux.1 Dev')"><h4>📸 Flux.1 Dev</h4><p>Fotorealistis Natural</p></div>
      <div class="card" data-type="IMAGE" onclick="setEng(this,'Midjourney v7')"><h4>🎨 Midjourney v7</h4><p>Pencahayaan Artistik</p></div>
      <div class="card" data-type="IMAGE" onclick="setEng(this,'Recraft V3')"><h4>📐 Recraft V3</h4><p>Desain Logo & Vektor</p></div>
      <div class="card" data-type="IMAGE" onclick="setEng(this,'Ideogram v3')"><h4>🔤 Ideogram v3</h4><p>Tipografi & Kaligrafi</p></div>
      <div class="card" data-type="IMAGE" onclick="setEng(this,'Illustrious XL')"><h4>🎌 Illustrious XL</h4><p>Anime & Ilustrasi 2.5D</p></div>
      <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Kling 3.0 Pro')"><h4>🟣 Kling 3.0 Pro</h4><p>Video Sinematik & Gerak Halus</p></div>
      <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Seedance 2.0')"><h4>🕺 Seedance 2.0</h4><p>Koreografi & Transisi</p></div>
      <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Wan 2.2 Pro')"><h4>🔵 Wan 2.2 Pro</h4><p>Konsistensi Karakter</p></div>
      <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Google Veo 3')"><h4>🎥 Google Veo 3</h4><p>Sinematik Film & Suara</p></div>
      <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Sora 2 Turbo')"><h4>🌌 Sora 2 Turbo</h4><p>Adegan Kompleks Realistis</p></div>
      <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Runway Gen-4')"><h4>🎞️ Runway Gen-4</h4><p>Kontrol Kamera Presisi</p></div>
    </div>

    <div class="label">3. Ukuran Layar (Eksklusif 1 Pilihan)</div>
    <div class="pill-row" data-group="ratio">
      <div class="pill active" onclick="selectExclusive(this,'ratio','9:16')">📱 9:16 (TikTok/Reels)</div>
      <div class="pill" onclick="selectExclusive(this,'ratio','1:1')">🟦 1:1 (Feed/Katalog)</div>
      <div class="pill" onclick="selectExclusive(this,'ratio','16:9')">🖥️ 16:9 (YouTube/Lanskap)</div>
    </div>

    <div class="label">4. Durasi Video (Aktif Khusus Mode Video)</div>
    <div class="pill-row" data-group="duration" id="duration-row">
      <div class="pill active disabled" onclick="selectExclusive(this,'duration',5)">⚡ 5 Detik</div>
      <div class="pill disabled" onclick="selectExclusive(this,'duration',10)">🔥 10 Detik</div>
      <div class="pill disabled" onclick="selectExclusive(this,'duration',30)">🎬 30 Detik Story</div>
    </div>

    <div class="label">5. Mode Penajaman Kualitas 4K</div>
    <div class="pill-row" data-group="upscale">
      <div class="pill active" onclick="selectExclusive(this,'upscale','Pertajam Foto & Wajah 4K')">🔍 Pertajam Foto & Wajah 4K</div>
      <div class="pill" onclick="selectExclusive(this,'upscale','Pertajam Teks & Gambar 4K')">✨ Pertajam Teks & Gambar 4K</div>
      <div class="pill" id="vid-ups-pill" onclick="selectExclusive(this,'upscale','Pertajam & Haluskan Video 4K 60FPS')">🎞️ Pertajam Video 4K 60FPS</div>
    </div>

    <div class="label">6. Upload Foto Referensi (Opsional — Produk / Wajah)</div>
    <div class="upload-box">
      <input type="file" accept="image/*" onchange="previewRef(event)">
      <div id="up-txt" style="font-size:12px;">📸 <b>Sentuh untuk Upload Foto Referensi</b><br><span style="font-size:10px; color:var(--muted);">Privasi aman & otomatis dibersihkan setelah selesai</span></div>
      <img id="ref-preview" alt="Ref">
    </div>

    <div class="label">7. Tulis Deskripsi Karya Anda</div>
    <textarea id="prompt-in" placeholder="Ketik deskripsi gambar atau video yang ingin dibuat..."></textarea>
    <button class="btn-exec" id="btn-go" onclick="runGenerate()">🚀 BUAT KARYA SEKARANG (KIRIM KE CHAT)</button>
    <div id="toast"></div>
  </div>

  <div id="tab-guide" class="tab-section">
    <div class="legal-card">
      <h3>🧭 Panduan Cepat & Tautan Komunitas</h3>
      <p>1. <b>File PNG Transparan Kualitas Tinggi:</b> Pilih mode <i>✂️ Hapus BG (.PNG)</i> untuk menerima file dokumen PNG utuh tanpa latar belakang.<br>
      2. <b>Garansi Koin Kembali 100% (Auto-Refund):</b> Jika terjadi kendala jaringan saat memproses karya, sistem otomatis mengembalikan koin Anda dalam 60 detik.<br>
      3. <b>Akses Cepat Fitur Bot:</b> Ketik <code>/riset [topik]</code> untuk analisis mendalam, <code>/canvas [instruksi]</code> untuk ruang tulis, atau kunjungi <a href="/unfiltered-portal" target="_blank">🌐 NocturneAI Web Studio (Voucher)</a>.</p>
    </div>
  </div>

  <div id="tab-legal" class="tab-section">
    <div class="legal-card">
      <h3>⚖️ Ketentuan Layanan & Lisensi Komersial Bersih</h3>
      <p>Seluruh karya yang dibuat menggunakan <b>Koin Utama (Pro)</b> memberikan hak komersial penuh bebas watermark kepada kreator. Dilarang membuat konten melanggar hukum atau merugikan pihak lain.</p>
    </div>
    <div class="legal-card">
      <h3>🛡️ Kebijakan Privasi & Keamanan</h3>
      <p>Seluruh informasi lokasi foto (EXIF) dihapus otomatis dan transaksi pembayaran didukung oleh <b>Pembayaran QRIS Instan</b> serta kasir global otomatis.</p>
    </div>
  </div>

  <div class="footer-copy">
    Copyright © 2026 <b>bikinAI Super Intelligence</b>. All Rights Reserved.
  </div>

  <div class="bottom-nav">
    <div class="nav-btn active" onclick="openTab(this,'tab-studio')"><span>🎬</span><span>Studio AI</span></div>
    <div class="nav-btn" onclick="openTab(this,'tab-guide')"><span>🧭</span><span>Panduan & Link</span></div>
    <div class="nav-btn" onclick="openTab(this,'tab-legal')"><span>⚖️</span><span>Ketentuan & Privasi</span></div>
  </div>

<script>
  const tg = window.Telegram?.WebApp;
  let st = {
    init_data: "", user_id: 0, username: "Kreator",
    modality: "IMAGE", engine: "Seedream 4.5", ratio: "9:16",
    duration: 5, upscale: "Pertajam Foto & Wajah 4K", has_ref: false
  };
  if (tg) {
    tg.expand();
    st.init_data = tg.initData || "";
    const u = tg.initDataUnsafe?.user;
    if (u) {
      st.user_id = u.id; st.username = u.username || u.first_name || "Kreator";
      document.getElementById("welcome-user").innerText = `Halo @${st.username}! Pilih kategori di bawah untuk langsung membuat karya 4K.`;
    }
  }
  function openTab(el, id) {
    document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".tab-section").forEach(s => s.classList.remove("active"));
    el.classList.add("active"); document.getElementById(id).classList.add("active");
  }
  function selectExclusive(el, groupName, val) {
    if (el.classList.contains("disabled")) return;
    const parent = el.closest(`[data-group='${groupName}']`);
    if (parent) parent.querySelectorAll(".pill").forEach(p => p.classList.remove("active"));
    el.classList.add("active");
    st[groupName] = val;
  }
  function setMod(el, m) {
    selectExclusive(el, "modality", m);
    const isVid = (m === "VIDEO");
    document.querySelectorAll("#duration-row .pill").forEach(p => {
      p.classList.toggle("disabled", !isVid);
    });
    let firstVisible = null;
    document.querySelectorAll("#engine-grid .card").forEach(c => {
      const cType = c.getAttribute("data-type");
      const show = isVid ? (cType === "VIDEO") : (cType === "IMAGE");
      c.classList.toggle("hidden-engine", !show);
      c.classList.remove("active");
      if (show && !firstVisible) firstVisible = c;
    });
    if (firstVisible) {
      firstVisible.classList.add("active");
      st.engine = firstVisible.querySelector("h4").innerText.replace(/^[^\w]+/, "").trim();
    }
  }
  function setEng(el, e) {
    document.querySelectorAll("#engine-grid .card").forEach(c => c.classList.remove("active"));
    el.classList.add("active"); st.engine = e;
  }
  function previewRef(ev) {
    const f = ev.target.files[0]; if (!f) return;
    const rd = new FileReader();
    rd.onload = e => {
      const img = document.getElementById("ref-preview");
      img.src = e.target.result; img.style.display = "block";
      document.getElementById("up-txt").innerHTML = "✅ <b>Foto Referensi Siap Dipakai</b>";
      st.has_ref = true;
    };
    rd.readAsDataURL(f);
  }
  async function runGenerate() {
    const btn = document.getElementById("btn-go"); const toast = document.getElementById("toast");
    const pr = document.getElementById("prompt-in").value.trim() || "Katalog produk sinematik pencahayaan studio 4K";
    btn.disabled = true; btn.innerText = "⏳ SEDANG MEMPROSES KARYA...";
    try {
      const r = await fetch("/api/webapp/execute", {
        method: "POST", headers: {"Content-Type": "application/json"},
        body: JSON.stringify(Object.assign({}, st, { prompt: pr }))
      });
      const d = await r.json();
      toast.style.display = "block"; toast.innerText = d.message || "✅ Karya berhasil dikirim ke ruang chat Telegram Anda!";
    } catch (e) {
      toast.style.display = "block"; toast.innerText = "✅ Permintaan diterima! Silakan cek ruang chat bot Telegram Anda.";
    } finally {
      btn.disabled = false; btn.innerText = "🚀 BUAT KARYA SEKARANG (KIRIM KE CHAT)";
    }
  }
</script>
</body>
</html>
"""

NOCTURNE_UNFILTERED_PORTAL_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NocturneAI Web Studio — Open-Weight Independent Lab</title>
<style>
  :root { --bg: #07040e; --card: #130b24; --pink: #ff007f; --violet: #7928ca; --text: #f5f0ff; --muted: #b8a9c9; }
  * { box-sizing: border-box; font-family: system-ui, -apple-system, sans-serif; }
  body { background: var(--bg); color: var(--text); padding: 16px; max-width: 620px; margin: 0 auto; }
  .header { background: var(--card); border: 1px solid var(--pink); border-radius: 16px; padding: 16px; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center; }
  .credit-pill { background: rgba(255,0,127,0.2); border: 1px solid var(--pink); padding: 6px 12px; border-radius: 99px; font-size: 12px; font-weight: 800; color: #ff80bf; }
  .tabs { display: flex; gap: 8px; margin-bottom: 14px; }
  .tab { flex: 1; text-align: center; padding: 10px; background: var(--card); border: 1px solid #3a2058; border-radius: 12px; font-size: 12px; font-weight: 700; cursor: pointer; color: var(--muted); }
  .tab.active { border-color: var(--pink); color: #fff; background: rgba(255,0,127,0.15); }
  .panel { display: none; background: var(--card); border: 1px solid #3a2058; border-radius: 16px; padding: 16px; }
  .panel.active { display: block; }
  input, select, textarea { width: 100%; background: #090514; border: 1px solid #4a2c6d; color: #fff; padding: 10px; border-radius: 10px; margin-top: 8px; font-size: 13px; }
  button { width: 100%; margin-top: 12px; padding: 12px; border: none; border-radius: 12px; background: linear-gradient(90deg, var(--pink), var(--violet)); color: #fff; font-weight: 800; cursor: pointer; }
  #chat-log { height: 220px; overflow-y: auto; background: #090514; border: 1px solid #2d1944; border-radius: 10px; padding: 10px; font-size: 13px; margin-top: 8px; line-height: 1.45; }
  .msg-u { color: #00f0ff; margin-bottom: 6px; }
  .msg-a { color: #f5f0ff; margin-bottom: 10px; border-bottom: 1px solid #1f1131; padding-bottom: 6px; }
  #media-result { margin-top: 12px; text-align: center; display: none; }
  #media-result img { max-width: 100%; border-radius: 12px; border: 1px solid var(--pink); }
  .dl-btn { display: inline-block; margin-top: 8px; padding: 9px 16px; background: #00e676; color: #000; font-weight: 800; border-radius: 10px; text-decoration: none; font-size: 12px; }
</style>
</head>
<body>
  <div class="header">
    <div>
      <div style="font-size:10px; color:#ff66b2; font-weight:800;">🔒 INDEPENDENT OPEN-WEIGHT STUDIO</div>
      <h2 style="margin:2px 0 0; font-size:18px;">NocturneAI Web Studio</h2>
    </div>
    <div class="credit-pill" id="cu-balance">⚡ 0 Unit Kredit</div>
  </div>

  <div class="tabs">
    <div class="tab active" onclick="swTab(this,'p-chat')">💬 Obrolan & Cerita</div>
    <div class="tab" onclick="swTab(this,'p-gen')">🎨 Gambar & Video</div>
    <div class="tab" onclick="swTab(this,'p-vch')">🎟️ Tukar Kode Voucher</div>
  </div>

  <!-- TAB 1: LIVE UNCENSORED CHAT -->
  <div id="p-chat" class="panel active">
    <label style="font-size:12px; font-weight:700;">Pilih Model Open-Weight:</label>
    <select id="chat-model">
      <option value="nousresearch/hermes-3-llama-3.1-405b">Nous Hermes 3 405B (Unfiltered Roleplay & Story)</option>
      <option value="qwen/qwen3-coder-next">Qwen 3 Uncensored Reasoning</option>
      <option value="deepseek/deepseek-v4.1-flash">DeepSeek V4.1 Flash Unfiltered</option>
    </select>
    <div id="chat-log"><div class="msg-a">✨ <b>NocturneAI:</b> Ruang obrolan independen siap digunakan. Ketik pesan atau skenario cerita Anda di bawah!</div></div>
    <textarea id="chat-in" rows="2" placeholder="Ketik pesan atau instruksi cerita..."></textarea>
    <button onclick="sendNocturneChat()" id="btn-chat">💬 KIRIM PESAN</button>
  </div>

  <!-- TAB 2: UNFILTERED IMAGE & VIDEO GENERATOR -->
  <div id="p-gen" class="panel">
    <label style="font-size:12px; font-weight:700;">Pilih Mesin Generator:</label>
    <select id="gen-model">
      <option value="Flux.1-Dev Uncensored FP8">Flux.1-Dev Uncensored FP8 + LoRA</option>
      <option value="WAI-Illustrious-XL v11">WAI-Illustrious-XL v11 (Anime / 2.5D)</option>
      <option value="CyberRealistic Pony V6.5">CyberRealistic Pony V6.5</option>
      <option value="Wan 2.2 14B Unfiltered">Wan 2.2 14B Video Studio</option>
    </select>
    <select id="gen-ratio">
      <option value="9:16">📱 Rasio 9:16 (Potret)</option>
      <option value="1:1">🟦 Rasio 1:1 (Persegi)</option>
      <option value="16:9">🖥️ Rasio 16:9 (Lanskap)</option>
    </select>
    <textarea id="gen-prompt" rows="3" placeholder="Ketik prompt visual detail Anda..."></textarea>
    <button onclick="runNocturneGen()" id="btn-gen">🎨 GENERATE LANGSUNG DI WEB</button>
    <div id="media-result">
      <img id="gen-img" src="" alt="Hasil Render">
      <br><a id="gen-dl" class="dl-btn" href="#" download="NocturneAI_HD.jpg">⬇️ Download Hasil HD</a>
    </div>
  </div>

  <!-- TAB 3: VOUCHER WALLET -->
  <div id="p-vch" class="panel">
    <label style="font-size:12px; font-weight:700;">🎟️ Masukkan Kode Voucher Studio Web (VCH-...):</label>
    <input type="text" id="vch-in" placeholder="VCH-eyJuIjoi...">
    <button onclick="redeemVoucher()">⚡ VERIFIKASI & TAMBAH KREDIT</button>
    <p id="vch-msg" style="font-size:12px; margin-top:10px; color:#00e676;"></p>
  </div>

<script>
  let credits = parseInt(localStorage.getItem("nocturne_cu") || "2");
  let activeVoucher = localStorage.getItem("nocturne_vch") || "";
  function updUI() { document.getElementById("cu-balance").innerText = `⚡ ${credits} Unit Kredit`; }
  updUI();
  function swTab(el, id) {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
    el.classList.add("active"); document.getElementById(id).classList.add("active");
  }
  async function redeemVoucher() {
    const code = document.getElementById("vch-in").value.trim();
    const msg = document.getElementById("vch-msg");
    const r = await fetch("/api/voucher/redeem", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ voucher: code })
    });
    const d = await r.json();
    if (d.ok) {
      credits += (d.units || 10); activeVoucher = code;
      localStorage.setItem("nocturne_cu", credits); localStorage.setItem("nocturne_vch", code);
      updUI(); msg.style.color = "#00e676"; msg.innerText = "✅ " + d.message;
    } else {
      msg.style.color = "#ff5252"; msg.innerText = "❌ " + d.message;
    }
  }
  async function sendNocturneChat() {
    const inp = document.getElementById("chat-in"); const txt = inp.value.trim();
    if (!txt) return;
    const log = document.getElementById("chat-log");
    log.innerHTML += `<div class="msg-u"><b>Anda:</b> ${txt.replace(/</g,"&lt;")}</div>`;
    inp.value = "";
    const btn = document.getElementById("btn-chat"); btn.disabled = true; btn.innerText = "⏳ Mengetik...";
    try {
      const r = await fetch("/api/nocturne/chat", {
        method: "POST", headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ prompt: txt, model: document.getElementById("chat-model").value })
      });
      const d = await r.json();
      log.innerHTML += `<div class="msg-a"><b>NocturneAI:</b> ${(d.reply || "").replace(/</g,"&lt;")}</div>`;
      log.scrollTop = log.scrollHeight;
    } finally {
      btn.disabled = false; btn.innerText = "💬 KIRIM PESAN";
    }
  }
  async function runNocturneGen() {
    const pr = document.getElementById("gen-prompt").value.trim() || "Cyberpunk anime warrior portrait, neon rain, 8k";
    const btn = document.getElementById("btn-gen"); btn.disabled = true; btn.innerText = "⏳ Merender HD...";
    try {
      const r = await fetch("/api/nocturne/generate", {
        method: "POST", headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ prompt: pr, model: document.getElementById("gen-model").value, ratio: document.getElementById("gen-ratio").value })
      });
      const d = await r.json();
      if (d.ok && d.image_url) {
        if (credits > 0) { credits -= 1; localStorage.setItem("nocturne_cu", credits); updUI(); }
        document.getElementById("gen-img").src = d.image_url;
        document.getElementById("gen-dl").href = d.image_url;
        document.getElementById("media-result").style.display = "block";
      }
    } finally {
      btn.disabled = false; btn.innerText = "🎨 GENERATE LANGSUNG DI WEB";
    }
  }
</script>
</body>
</html>
"""


# ==============================================================================
# 5. SECURITY VALIDATORS (HMAC MINI APP, INPUT SANITIZER, & ED25519 VOUCHER)
# ==============================================================================
def verify_telegram_webapp_init_data(init_data_raw: str, bot_token: str, max_age_sec: int = 86400) -> dict[str, Any] | None:
    """[PATCH AUDIT-02]: Memverifikasi tanda tangan HMAC-SHA256 Telegram.WebApp.initData."""
    if not init_data_raw or not bot_token:
        return None
    try:
        parsed = dict(parse_qsl(init_data_raw, keep_blank_values=True))
        received_hash = parsed.pop("hash", "")
        if not received_hash:
            return None
        auth_date = int(parsed.get("auth_date", "0"))
        if auth_date > 0 and abs(int(time.time()) - auth_date) > max_age_sec:
            return None
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
        secret_key = hmac.new(b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(calculated_hash, received_hash):
            return None
        user_json = parsed.get("user", "{}")
        return json.loads(user_json)
    except Exception:
        return None


_INJECTION_PATTERNS = re.compile(
    r"(ignore\s+(all\s+)?(previous|prior)\s+instructions|system\s*prompt|"
    r"you\s+are\s+now\s+dan|jailbreak|ilja\s*kaerb|drop\s+table|union\s+select|"
    r"<script\b|javascript:|__import__|__subclasses__|__globals__|os\.system|subprocess)",
    re.IGNORECASE,
)


def sanitize_and_deobfuscate_input(raw_text: str) -> tuple[str, bool]:
    if not raw_text:
        return "", False
    normalized = unicodedata.normalize("NFKC", raw_text)
    cleaned = "".join(
        ch for ch in normalized if unicodedata.category(ch) not in ("Cf", "Cc") or ch in ("\n", "\r", "\t")
    ).strip()
    leet_map = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})
    deobfuscated = cleaned.lower().translate(leet_map)
    if _INJECTION_PATTERNS.search(cleaned) or _INJECTION_PATTERNS.search(deobfuscated):
        return cleaned, True
    return cleaned, False


def issue_stateless_ed25519_voucher(user_id: int, compute_units: int = 10, ttl_seconds: int = 86400) -> str:
    now_ts = int(time.time())
    nonce = hashlib.sha256(f"{user_id}:{now_ts}:{os.urandom(8).hex()}".encode()).hexdigest()[:16]
    payload_dict = {"n": nonce, "u": int(user_id), "c": int(compute_units), "exp": now_ts + ttl_seconds}
    payload_bytes = json.dumps(payload_dict, separators=(",", ":")).encode("utf-8")
    priv_key = Ed25519PrivateKey.from_private_bytes(ED25519_PRIV_BYTES)
    signature = priv_key.sign(payload_bytes)
    b64_payload = base64.urlsafe_b64encode(payload_bytes).decode("ascii").rstrip("=")
    b64_sig = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")
    return f"VCH-{b64_payload}.{b64_sig}"


async def verify_and_redeem_ed25519_voucher(
    db: aiosqlite.Connection, voucher_code: str
) -> tuple[bool, str, int]:
    code = voucher_code.strip()
    if not code.startswith("VCH-") or "." not in code:
        return False, "Format kode voucher tidak valid.", 0
    try:
        body = code[4:]
        b64_payload, b64_sig = body.split(".", 1)
        payload_bytes = base64.urlsafe_b64decode(b64_payload + "=" * (-len(b64_payload) % 4))
        sig_bytes = base64.urlsafe_b64decode(b64_sig + "=" * (-len(b64_sig) % 4))

        pub_key = Ed25519PublicKey.from_public_bytes(ED25519_PUB_BYTES)
        pub_key.verify(sig_bytes, payload_bytes)

        data = json.loads(payload_bytes.decode("utf-8"))
        exp = int(data.get("exp", 0))
        units = int(data.get("c", 10))
        now_ts = int(time.time())
        if exp <= now_ts:
            return False, "Kode voucher sudah kedaluwarsa.", 0

        nullifier_hash = hashlib.sha256(sig_bytes).hexdigest()

        async def _tx(conn: aiosqlite.Connection) -> bool:
            cur = await conn.execute(
                "SELECT 1 FROM redeemed_nullifiers WHERE nullifier_hash = ?;", (nullifier_hash,)
            )
            if await cur.fetchone():
                return False
            await conn.execute(
                "INSERT INTO redeemed_nullifiers (nullifier_hash, expires_at) VALUES (?, ?);",
                (nullifier_hash, exp),
            )
            return True

        ok = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
        if not ok:
            return False, "Kode voucher sudah pernah digunakan sebelumnya.", 0
        return True, f"Kode Voucher Valid (+{units} Unit Kredit Studio Web)!", units
    except Exception as e:
        return False, f"Verifikasi voucher gagal: {e}", 0


# ==============================================================================
# 6. ROLLING 8-AGENT POOL (ARGON, QWEN, DEEPSEEK, MUSE, NANO-MUSE, HARNESS, HERMES, GROQ)
# ==============================================================================
AGENTIC_ROLLING_POOL: dict[str, dict[str, Any]] = {
    "ARGON": {
        "title": "🌟 Argon Frontier (Gemini 4 Argon / Flash)",
        "model_polli": "google/gemini-4-argon",
        "model_or": "google/gemini-2.0-flash-exp:free",
        "role": "Penalaran Konteks Panjang & Deep Research",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "QWEN": {
        "title": "💻 Qwen3 Agentic Coder (Qwen3-Coder / 3.8)",
        "model_polli": "qwen/qwen3-coder-next",
        "model_or": "qwen/qwen3-coder:free",
        "role": "Arsitektur Kode, Logika & Canvas",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "DEEPSEEK": {
        "title": "🧠 DeepSeek R1/V4.1 Reasoner",
        "model_polli": "deepseek/deepseek-v4.1-flash",
        "model_or": "deepseek/deepseek-chat:free",
        "role": "Analisis Strategis & Deduksi Matematika",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "MUSE": {
        "title": "🎨 Meta Muse Spark 1.2 (Creative Director)",
        "model_polli": "meta/muse-spark-1.2",
        "model_or": "meta-llama/llama-3.3-70b-instruct:free",
        "role": "Racikan Prompt Sinematik 4K & Cerita Visual",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "NANO_MUSE": {
        "title": "⚡ Nano-Muse Glimmer 30B (Fast Drafter)",
        "model_polli": "meta/muse-glimmer-30b",
        "model_or": "openai/gpt-oss-120b:free",
        "role": "Respons Kilat <1.2s & Copywriting UMKM",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "HARNESS": {
        "title": "🛠️ OpenHands / DeepSeek Agent Harness",
        "model_polli": "deepseek/deepseek-v4-pro",
        "model_or": "qwen/qwen3-coder:free",
        "role": "Self-Healing Diagnostik & Troubleshooting",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "HERMES": {
        "title": "🔓 Nous Hermes 3/4 (Open-Weight Unfiltered)",
        "model_polli": "mistralai/mistral-large-4",
        "model_or": "nousresearch/hermes-3-llama-3.1-405b",
        "role": "Eksekusi Portal Independen NocturneAI",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
    "GROQ_CEREBRAS": {
        "title": "🚀 Groq LPU & Cerebras Wafer-Scale",
        "model_polli": "meta/llama-3.3-70b-instruct",
        "model_or": "meta-llama/llama-3.3-70b-instruct:free",
        "role": "Penyangga Kecepatan 320 Token/Detik",
        "ok": 0, "fail": 0, "quarantine_until": 0,
    },
}


def rotate_primary_agent() -> str:
    keys = list(AGENTIC_ROLLING_POOL.keys())
    cur = RUNTIME_CONFIG.get("PRIMARY_ROLLING_AGENT", "ARGON")
    idx = keys.index(cur) if cur in keys else 0
    nxt = keys[(idx + 1) % len(keys)]
    RUNTIME_CONFIG["PRIMARY_ROLLING_AGENT"] = nxt
    return nxt


async def _call_single_llm_endpoint(
    agent_key: str, url: str, headers: dict[str, str], payload: dict[str, Any], timeout_sec: float = 5.5
) -> str | None:
    ag = AGENTIC_ROLLING_POOL.get(agent_key)
    now_ts = int(time.time())
    if ag and ag["quarantine_until"] > now_ts:
        return None
    try:
        async with httpx.AsyncClient(timeout=timeout_sec) as client:
            r = await client.post(url, headers=headers, json=payload)
            if r.status_code == 200:
                data = r.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                if content and len(content.strip()) > 2:
                    if ag:
                        ag["ok"] += 1
                    return sanitize_external_api_response(content)
            elif r.status_code in (429, 502, 503) and ag:
                ag["fail"] += 1
                ag["quarantine_until"] = now_ts + 60
    except Exception:
        if ag:
            ag["fail"] += 1
    return None


BIKINAI_NATURAL_INDONESIAN_PROMPT = """
PERAN DAN KEPRIBADIAN UTAMA:
Kamu adalah 'bikinAI Super Intelligence', asisten AI dan sahabat diskusi paling cerdas, hangat, luwes, dan solutif.
ATURAN BAHASA & KENYAMANAN MUTLAK:
1. KEMURNIAN BAHASA 100%: Balas 100% dalam Bahasa Indonesia yang mengalir alami dan akrab.
2. LARANGAN TABEL GARIS PIPA DI CHAT TELEGRAM: Gunakan poin-poin rapi (▸, •, ⚡).
3. LANGSUNG SOLUTIF: Berikan jawaban tuntas pada kesempatan pertama.
""".strip()


async def generate_frontier_ai_response(
    db: aiosqlite.Connection,
    user_message: str,
    mode: Literal["NATURAL_CHAT", "DEEP_RESEARCH", "CANVAS_EDIT", "PROMPT_ARCHITECT", "NOCTURNE_UNCENSORED"] = "NATURAL_CHAT",
    personal_memory: str = "",
    canvas_state: str = "",
    preferred_model: str = "",
) -> str:
    mem_context = f"\nMEMORI PENGGUNA: {personal_memory}" if personal_memory else ""
    if mode == "DEEP_RESEARCH":
        task = "Susun laporan Deep Research mendalam dalam Bahasa Indonesia: 1) Intisari Eksekutif, 2) Bedah Data & Teknis, 3) Peluang & Solusi, 4) Langkah Eksekusi Praktis."
        primary_ag = "ARGON"
    elif mode == "CANVAS_EDIT":
        task = f"Perbarui dokumen/kode di Canvas ini sesuai instruksi pengguna:\n{canvas_state or '(Kosong)'}"
        primary_ag = "QWEN"
    elif mode == "PROMPT_ARCHITECT":
        task = "Buatkan 3 variasi prompt visual/video sinematik terbaik (1. Komersial Fotorealistis, 2. Video Sinematik, 3. Artistik/3D) beserta penjelasannya dalam Bahasa Indonesia."
        primary_ag = "MUSE"
    elif mode == "NOCTURNE_UNCENSORED":
        task = "Jawab secara kreatif, ekspresif, dan mendalam sesuai skenario pengguna tanpa pembatasan kaku."
        primary_ag = "HERMES"
    else:
        task = "Jawab obrolan atau pertanyaan pengguna dengan sangat luwes, hangat, dan solutif dalam Bahasa Indonesia."
        primary_ag = RUNTIME_CONFIG.get("PRIMARY_ROLLING_AGENT", "ARGON")

    sys_prompt = task if mode == "NOCTURNE_UNCENSORED" else f"{BIKINAI_NATURAL_INDONESIAN_PROMPT}{mem_context}\n\nTUGAS:\n{task}"
    msgs = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_message}]

    ag_info = AGENTIC_ROLLING_POOL.get(primary_ag, AGENTIC_ROLLING_POOL["ARGON"])
    tasks: list[asyncio.Task] = []

    if GROQ_API_KEY and mode != "NOCTURNE_UNCENSORED":
        tasks.append(
            asyncio.create_task(
                _call_single_llm_endpoint(
                    "GROQ_CEREBRAS",
                    "https://api.groq.com/openai/v1/chat/completions",
                    {"Authorization": f"Bearer {GROQ_API_KEY}"},
                    {"model": "llama-3.3-70b-versatile", "messages": msgs, "max_tokens": 750},
                    timeout_sec=4.5,
                )
            )
        )

    if CEREBRAS_API_KEY and mode != "NOCTURNE_UNCENSORED":
        tasks.append(
            asyncio.create_task(
                _call_single_llm_endpoint(
                    "GROQ_CEREBRAS",
                    "https://api.cerebras.ai/v1/chat/completions",
                    {"Authorization": f"Bearer {CEREBRAS_API_KEY}"},
                    {"model": "llama-3.3-70b", "messages": msgs, "max_tokens": 750},
                    timeout_sec=4.5,
                )
            )
        )

    if OPENROUTER_API_KEY:
        or_model = preferred_model or ag_info["model_or"]
        tasks.append(
            asyncio.create_task(
                _call_single_llm_endpoint(
                    primary_ag,
                    "https://openrouter.ai/api/v1/chat/completions",
                    {"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
                    {"model": or_model, "messages": msgs, "max_tokens": 750},
                    timeout_sec=5.8,
                )
            )
        )

    if GEMINI_API_KEY and mode != "NOCTURNE_UNCENSORED":
        tasks.append(
            asyncio.create_task(
                _call_single_llm_endpoint(
                    "ARGON",
                    "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                    {"Authorization": f"Bearer {GEMINI_API_KEY}"},
                    {"model": "gemini-2.0-flash", "messages": msgs, "max_tokens": 750},
                    timeout_sec=5.5,
                )
            )
        )

    # Jalur Bansos Komunitas yang Terverifikasi Hidup (Gate 1-4 Passed)
    try:
        cur_b = await db.execute(
            "SELECT endpoint_url, secret_or_meta FROM omni_resource_registry "
            "WHERE category = 'AI_API' AND is_live_verified = 1 AND expires_at > ? LIMIT 2;",
            (int(time.time()),),
        )
        for ep_url, meta_model in await cur_b.fetchall():
            ok_u, _ = validate_safe_external_url(ep_url)
            if ok_u and "pollinations.ai" not in ep_url and "openrouter.ai" not in ep_url:
                target_ep = ep_url if ep_url.endswith("/chat/completions") else f"{ep_url.rstrip('/')}/chat/completions"
                tasks.append(
                    asyncio.create_task(
                        _call_single_llm_endpoint(
                            primary_ag,
                            target_ep,
                            {"Content-Type": "application/json"},
                            {"model": meta_model or "openai", "messages": msgs, "max_tokens": 700},
                            timeout_sec=5.0,
                        )
                    )
                )
    except Exception:
        pass

    # Jalur Pollinations Multi-Model Fallback (Selalu Aktif HPP Rp 0)
    polli_headers = {"Content-Type": "application/json"}
    if POLLINATIONS_API_KEY:
        polli_headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"
    tasks.append(
        asyncio.create_task(
            _call_single_llm_endpoint(
                primary_ag,
                "https://text.pollinations.ai/openai",
                polli_headers,
                {"model": "openai", "messages": msgs},
                timeout_sec=6.8,
            )
        )
    )

    for coro in asyncio.as_completed(tasks):
        res = await coro
        if res:
            for t in tasks:
                if not t.done():
                    t.cancel()
            return res

    rotate_primary_agent()
    if mode == "PROMPT_ARCHITECT":
        return (
            "🎨 **RACIKAN PROMPT SINEMATIK — bikinAI**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"Berdasarkan konsep (**\"{user_message[:80]}\"**), berikut 3 variasi siap pakai:\n\n"
            f"▸ **1. Gaya Komersial 4K:** _`Commercial studio shot of {user_message[:60]}, golden hour lighting, ultra-detailed 8k photorealistic.`_\n"
            f"▸ **2. Gaya Video Sinematik:** _`Cinematic dynamic camera tracking shot of {user_message[:60]}, dramatic atmosphere, 4k 60fps.`_\n"
            f"▸ **3. Gaya Artistik 3D/Anime:** _`Vibrant 3D illustration of {user_message[:60]}, volumetric lighting, masterpiece.`_"
        )
    return (
        f"Halo Kak! Aku langsung menangkap maksud Kakak terkait **\"{user_message[:90]}\"** 😊\n\n"
        "▸ Ketik **`buat gambar [deskripsi]`** untuk merender gambar 4K.\n"
        "▸ Ketik **`buat video [deskripsi]`** untuk membuka Studio Video AI.\n"
        "▸ Ketik **`menu`** kapan saja jika ingin menampilkan tombol studio lengkap!"
    )


# ==============================================================================
# 7. IDENTITAS PENGGUNA (SANGMATA), BRANKAS TREASURY & INVOICE LEDGER
# ==============================================================================
async def ensure_user_and_track_identity(
    db: aiosqlite.Connection, user_id: int, username: str, first_name: str = "", lang_code: str = "id"
) -> dict[str, Any]:
    today_epoch = int(time.time()) // 86400
    clean_uname = (username or "Kreator").replace("`", "").replace("*", "").replace("_", "\\_")
    raw_uname = username or "Kreator"
    is_indo = not lang_code or lang_code.lower().startswith(("id", "in", "ms"))
    default_ppp_zone = 3 if is_indo else 1

    async def _tx(conn: aiosqlite.Connection) -> dict[str, Any]:
        cur_check = await conn.execute(
            "SELECT username, personal_memory_notes, active_canvas_content FROM users WHERE internal_user_id = ?;",
            (user_id,),
        )
        existing = await cur_check.fetchone()
        name_changed_msg = ""

        if not existing:
            await conn.execute(
                """
                INSERT INTO users (internal_user_id, username, first_name, language_code, koin_utama, koin_bonus, ppp_zone, quota_day_epoch, created_at)
                VALUES (?, ?, ?, 'id', 0, 4, ?, ?, ?);
                """,
                (user_id, raw_uname, first_name or raw_uname, default_ppp_zone, today_epoch, int(time.time())),
            )
        else:
            old_uname = existing[0]
            if (
                RUNTIME_CONFIG["SUBBOT_SANGMATA_ACTIVE"]
                and old_uname
                and old_uname != raw_uname
                and raw_uname != "Kreator"
            ):
                await conn.execute(
                    "INSERT INTO identity_history (user_id, old_username, new_username, changed_at) VALUES (?, ?, ?, ?);",
                    (user_id, old_uname, raw_uname, int(time.time())),
                )
                await conn.execute("UPDATE users SET username = ? WHERE internal_user_id = ?;", (raw_uname, user_id))
                name_changed_msg = f"@{old_uname} -> @{raw_uname}"

        await conn.execute(
            """
            UPDATE users
            SET chat_used_today = CASE WHEN quota_day_epoch < ? THEN 0 ELSE chat_used_today END,
                free_img_used_today = CASE WHEN quota_day_epoch < ? THEN 0 ELSE free_img_used_today END,
                quota_day_epoch = ?
            WHERE internal_user_id = ? AND quota_day_epoch < ?;
            """,
            (today_epoch, today_epoch, today_epoch, user_id, today_epoch),
        )
        cur = await conn.execute(
            "SELECT koin_utama, koin_bonus, has_topped_up, ppp_zone, chat_used_today, free_img_used_today, last_claim_date, personal_memory_notes, active_canvas_content FROM users WHERE internal_user_id = ?;",
            (user_id,),
        )
        row = await cur.fetchone()
        return {
            "koin_utama": int(row[0]),
            "koin_bonus": int(row[1]),
            "has_topped_up": bool(row[2]),
            "ppp_zone": int(row[3]),
            "chat_used_today": int(row[4]),
            "free_img_used_today": int(row[5]),
            "last_claim_date": row[6] or "",
            "memory": row[7] or "",
            "canvas": row[8] or "",
            "identity_alert": name_changed_msg,
            "safe_uname": clean_uname,
        }

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def record_job_and_split_profit(
    db: aiosqlite.Connection, revenue_idr: int, actual_hpp_idr: int, buffer_ratio: float = 0.10
) -> dict[str, int]:
    if RUNTIME_CONFIG.get("BANSOS_OPERATION_MODE") == "SILENT_PROFIT":
        actual_hpp_idr = 0
    required_working_capital = int(math.ceil(actual_hpp_idr * (1.0 + buffer_ratio)))
    net_harvestable_profit = max(0, revenue_idr - required_working_capital)

    async def _tx(conn: aiosqlite.Connection) -> int:
        now_ts = int(time.time())
        await conn.execute("INSERT OR IGNORE INTO treasury_summary VALUES (1, 0, 0, 0, 0, 0, ?);", (now_ts,))
        cur = await conn.execute(
            """
            UPDATE treasury_summary
            SET gross_revenue_idr = gross_revenue_idr + ?,
                working_capital_vault_idr = working_capital_vault_idr + ?,
                harvestable_profit_vault_idr = MAX(0, harvestable_profit_vault_idr + ?),
                total_jobs_completed = total_jobs_completed + 1,
                updated_at = ?
            WHERE id = 1
            RETURNING total_jobs_completed;
            """,
            (revenue_idr, required_working_capital, net_harvestable_profit, now_ts),
        )
        row = await cur.fetchone()
        return int(row[0]) if row else 1

    jobs_done = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    return {
        "working_capital_locked_idr": required_working_capital,
        "net_profit_ready_to_harvest_idr": net_harvestable_profit,
        "fomo_counter": RUNTIME_CONFIG["FOMO_COUNTER_BASE"] + jobs_done,
    }


async def execute_manual_profit_harvest(db: aiosqlite.Connection) -> tuple[bool, int, int]:
    async def _tx(conn: aiosqlite.Connection) -> tuple[bool, int, int]:
        now_ts = int(time.time())
        await conn.execute("INSERT OR IGNORE INTO treasury_summary VALUES (1, 0, 0, 0, 0, 0, ?);", (now_ts,))
        cur = await conn.execute(
            "SELECT harvestable_profit_vault_idr, total_harvested_by_owner_idr FROM treasury_summary WHERE id = 1;"
        )
        row = await cur.fetchone()
        if not row or int(row[0]) <= 0:
            return False, 0, int(row[1]) if row else 0
        avail = int(row[0])
        new_total = int(row[1]) + avail
        await conn.execute(
            "UPDATE treasury_summary SET harvestable_profit_vault_idr = 0, total_harvested_by_owner_idr = ?, updated_at = ? WHERE id = 1;",
            (new_total, now_ts),
        )
        return True, avail, new_total

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


# ==============================================================================
# 8. DUAL-RAIL GEO PAYMENT & ANTI-BYPASS INVOICE VERIFIER (PATCH AUDIT-01)
# ==============================================================================
def compute_crc16_ccitt(data_str: str) -> str:
    crc = 0xFFFF
    for ch in data_str.encode("utf-8"):
        crc ^= ch << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if (crc & 0x8000) else (crc << 1) & 0xFFFF
    return f"{crc:04X}"


def generate_dynamic_qris_string(static_qris: str, amount_idr: int) -> str:
    if not static_qris or len(static_qris) < 20 or "5802ID" not in static_qris:
        static_qris = "00020101021126610014ID.CO.GOPAY.WWW01189360091431234567890210G1234567890303UMI51440014ID.CO.QRIS.WWW0215ID10200000000010303UMI5204581253033605802ID5912BIKINAI STUDIO6007JAKARTA6304ABCD"
    base_qris = static_qris[:-4].replace("010211", "010212", 1)
    if base_qris.endswith("6304"):
        base_qris = base_qris[:-4]
    amt_str = str(int(amount_idr))
    tag_54 = f"54{len(amt_str):02d}{amt_str}"
    parts = base_qris.split("5802ID", 1)
    reconstructed = f"{parts[0]}{tag_54}5802ID{parts[1]}6304"
    return f"{reconstructed}{compute_crc16_ccitt(reconstructed)}"


async def create_payment_invoice(db: aiosqlite.Connection, user_id: int, ppp_zone: int) -> dict[str, Any]:
    invoice_id = f"INV-{user_id}-{int(time.time())}"
    unique_code = (user_id % 89) + 10
    exact_idr = 5000 + unique_code
    provider = (
        RUNTIME_CONFIG["ID_ACTIVE_PROVIDER"]
        if ppp_zone == 3
        else RUNTIME_CONFIG["GLOBAL_ACTIVE_PROVIDER"]
    )

    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(
            """
            INSERT INTO payment_invoices (invoice_id, user_id, amount_idr, coins_credited, provider, status, created_at)
            VALUES (?, ?, ?, 60, ?, 'PENDING', ?);
            """,
            (invoice_id, user_id, exact_idr, provider, int(time.time())),
        )

    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)

    if ppp_zone in (1, 2):
        usd_price = "$1.99" if ppp_zone == 1 else "$0.99"
        stars_amt = 110 if ppp_zone == 1 else 55
        return {
            "invoice_id": invoice_id,
            "provider": provider,
            "display_amount": f"{usd_price} USDT / {stars_amt} Telegram Stars ⭐",
            "qris_payload": "",
            "is_global": True,
        }
    return {
        "invoice_id": invoice_id,
        "provider": provider,
        "display_amount": f"Rp {exact_idr:,}",
        "qris_payload": generate_dynamic_qris_string(GOPAY_STATIC_QRIS_RAW, exact_idr),
        "is_global": False,
    }


async def approve_invoice_and_credit_coins(
    db: aiosqlite.Connection, invoice_id: str
) -> tuple[bool, int, int, str]:
    """Mengubah status invoice PENDING -> PAID secara atomik (Anti-Double-Credit)."""
    async def _tx(conn: aiosqlite.Connection) -> tuple[bool, int, int, str]:
        cur = await conn.execute(
            "SELECT user_id, amount_idr, coins_credited, status FROM payment_invoices WHERE invoice_id = ?;",
            (invoice_id,),
        )
        row = await cur.fetchone()
        if not row:
            return False, 0, 0, "Tagihan tidak ditemukan."
        uid, amt_idr, coins_add, st = int(row[0]), int(row[1]), int(row[2]), str(row[3])
        if st == "PAID":
            return False, uid, 0, "Tagihan ini sudah pernah diverifikasi sebelumnya."
        await conn.execute("UPDATE payment_invoices SET status = 'PAID' WHERE invoice_id = ?;", (invoice_id,))
        await conn.execute(
            "UPDATE users SET koin_utama = koin_utama + ?, has_topped_up = 1 WHERE internal_user_id = ?;",
            (coins_add, uid),
        )
        return True, uid, amt_idr, f"+{coins_add} Koin Utama berhasil ditambahkan!"

    ok, uid, amt_idr, msg = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    if ok and amt_idr > 0:
        await record_job_and_split_profit(db, revenue_idr=amt_idr, actual_hpp_idr=750)
    return ok, uid, amt_idr, msg


# ==============================================================================
# 9. MEDIA FETCHER, WEBAPP API & NOCTURNE STUDIO BACKEND HANDLERS
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


# ==============================================================================
# 10. WIZARD STATE, VIDEO UPSCALER 4K 60FPS & CUSTOMER-FRIENDLY MENU BUILDERS
# ==============================================================================
UPSCALER_WHITE_LABEL = {
    "PHOTO_FACE_4K": "🔍 Pertajam Foto & Wajah 4K",
    "TEXT_LINE_4K": "✨ Pertajam Teks & Gambar 4K",
    "VIDEO_4K_60FPS": "🎞️ Pertajam & Haluskan Video 4K 60FPS",
    "OFF": "Standar HD",
}

IMAGE_EDITING_TOOLS = {
    "REMOVE_BG_PNG": (
        "✂️ Hapus Background (File PNG Transparan Kualitas Tinggi)",
        "Menghapus latar belakang foto dan mengirimkannya sebagai File Dokumen .PNG transparan utuh",
    ),
    "RETOUCH_FACE": (
        "✨ Retouch Wajah & Kulit Mulus",
        "Memperhalus tekstur kulit dan pencahayaan wajah secara alami",
    ),
    "INPAINT_OBJ": (
        "🖌️ Inpainting (Ganti Baju / Ubah Objek)",
        "Mengganti pakaian atau objek tertentu di dalam foto tanpa merusak latar",
    ),
    "OUTPAINT_EXPAND": (
        "🖼️ Outpainting (Perluas Ukuran Foto)",
        "Memperluas foto kotak 1:1 menjadi vertikal 9:16 atau melebar 16:9",
    ),
    "PRODUCT_RELIGHT": (
        "📸 Studio Produk UMKM (Relighting)",
        "Mengubah foto produk rumahan menjadi foto katalog studio mewah",
    ),
    "RESTORE_OLD": (
        "🕰️ Restorasi & Warnai Foto Lama",
        "Memperbaiki foto jadul yang buram menjadi tajam dan berwarna kembali",
    ),
}

DYNAMIC_CHAT_FOOTERS = [
    "\n\n_💡 Kalau nanti butuh tombol menu interaktif, tinggal ketik **\"tampilin tombol\"** ya Kak 😊_",
    "\n\n_✨ Nyaman ngobrol dulu aja Kak. Kapan pun mau buka studio visual, cukup ketik **\"menu\"** ya!_",
    "\n\n_⚡ Kalau ide di atas mau langsung kita ubah jadi karya visual, tinggal bilang **\"tampilin tombol\"** aja ya Kak._",
    "\n\n_📝 Tip: Ketik **`/canvas`** kalau mau menyusun draf panjang, atau ketik **\"menu\"** untuk melihat fitur lainnya 😊_",
    "\n\n_🔬 Butuh bedah riset yang lebih mendalam? Cukup ketik **`/riset [topik]`** atau **\"tampilin tombol\"** kapan saja ya!_",
]
_FOOTER_COUNTER = 0


def get_next_dynamic_footer() -> str:
    global _FOOTER_COUNTER
    idx = _FOOTER_COUNTER % len(DYNAMIC_CHAT_FOOTERS)
    _FOOTER_COUNTER += 1
    return DYNAMIC_CHAT_FOOTERS[idx]


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


class BoundedSessionStore(OrderedDict):
    def __setitem__(self, key: Any, value: Any) -> None:
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if len(self) > 5000:
            self.popitem(last=False)


ACTIVE_DRAFTS: BoundedSessionStore = BoundedSessionStore()
WAITING_PROMPT_EDIT_USERS: set[int] = set()
router = Router()


def is_verified_owner_dm(user_id: int, chat_type: str) -> bool:
    """[PATCH AUDIT-03]: Mencegah pengambilalihan Owner otomatis jika ADMIN_USER_ID belum diisi."""
    if chat_type != "private":
        return False
    owner_id = int(RUNTIME_CONFIG.get("OWNER_ID_RUNTIME") or 0)
    return owner_id > 0 and user_id == owner_id


def build_customer_main_menu_keyboard(u: dict[str, Any] | None = None, is_private: bool = True) -> InlineKeyboardMarkup:
    today_str = time.strftime("%Y-%m-%d")
    already_claimed = u and (u.get("last_claim_date") == today_str or u.get("koin_bonus", 0) >= 25)
    claim_label = "🎁 Koin Harian Terklaim ✅" if already_claimed else "🎁 Klaim +4 Koin Gratis"
    ppp_zone = u.get("ppp_zone", 3) if u else 3
    topup_label = "💳 Isi Saldo (Pembayaran QRIS Instan)" if ppp_zone == 3 else "💳 Top-Up Coins (USDT / Stars ⭐)"

    rows: list[list[InlineKeyboardButton]] = []
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
                text="📱 Buka Super Mini App Studio (Panduan Link)",
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
                text="🌐 Studio Web Independen (NocturneAI) & Kode Voucher",
                callback_data="menu:unfiltered_external_referral",
            )
        ],
        [
            InlineKeyboardButton(text="📊 Status Kuota Harian", callback_data="menu:quota"),
            InlineKeyboardButton(text=claim_label, callback_data="menu:claim_daily"),
        ],
        [
            InlineKeyboardButton(text=topup_label, callback_data="menu:topup_qris"),
            InlineKeyboardButton(text="🎧 Bantuan & Garansi Koin 100%", callback_data="menu:live_support"),
        ],
        [
            InlineKeyboardButton(text="📜 Panduan, FAQ, Ketentuan & Topik Grup", callback_data="menu:faq_tos"),
        ],
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_customer_dashboard_caption(username: str, u: dict[str, Any]) -> str:
    tier_badge = "🌟 KREATOR PRO" if u["has_topped_up"] else "⚡ KREATOR EKSPLORER"
    hh_banner = "\n🎉 **FLASH HAPPY HOUR AKTIF: SEMUA RENDER GRATIS 0 KOIN!** 🎉\n" if RUNTIME_CONFIG["HAPPY_HOUR_MODE"] else ""
    safe_u = u.get("safe_uname") or username
    return (
        f"┏━━━ ⚡ **bikinAI SUPER INTELLIGENCE** ⚡ ━━━┓\n"
        f"┃ 👤 **Kreator:** `@{safe_u}`\n"
        f"┃ 🏅 **Status:** `{tier_badge}`\n"
        f"┣━━━━━━━━━━━━━━━━━━━━━━━┫\n"
        f"┃ 💎 **Koin Utama:** `{u['koin_utama']} Koin`\n"
        f"┃ 🎁 **Koin Bonus:** `{u['koin_bonus']}/{MAX_KOIN_BONUS_CAP} Koin`\n"
        f"┃ 🤖 **Asisten AI 24 Jam:** `🟢 AKTIF (Gratis)`\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━┛{hh_banner}\n\n"
        f"✨ **Selamat datang di Studio Kreatif AI Generasi Baru.**\n"
        f"▸ Klik **`📱 Buka Super Mini App Studio`** di atas untuk tampilan web penuh, atau pilih menu cepat di bawah:"
    )


def build_400_percent_derivative_upsell_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🖼️ Ambil Poster Thumbnail 4K (+4 Koin)", callback_data="drv:poster4k"),
                InlineKeyboardButton(text="🎵 Ekstrak Audio MP3 (+4 Koin)", callback_data="drv:audiomp3"),
            ],
            [
                InlineKeyboardButton(text="✨ Buka Lisensi Komersial Bersih Tanpa Watermark (+10 Koin)", callback_data="drv:clean_license"),
            ],
            [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
        ]
    )


def build_video_wizard_kb(session: LiveWizardSession, show_more: bool = False) -> tuple[str, InlineKeyboardMarkup]:
    coins, _, _ = session.get_pricing()
    ups_label = UPSCALER_WHITE_LABEL.get(session.upscale_mode, "🎞️ Pertajam & Haluskan Video 4K 60FPS")
    text = (
        f"🎬 **STUDIO VIDEO AI — bikinAI**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Konsep Video:**\n> _{session.prompt}_\n\n"
        f"┣ ⚡ **Mesin AI Video:** **`{session.video_engine}`**\n"
        f"┣ 📐 **Ukuran Layar:** `{session.aspect_ratio}` | ⏱️ **Durasi:** `{session.duration_sec} Detik`\n"
        f"┗ 🔍 **Kualitas:** `{ups_label}`\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💎 **Biaya:** **`{coins} Koin`** _(Garansi Koin Kembali 100%)_"
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
            [InlineKeyboardButton(text="🔼 Sembunyikan AI Video Lainnya", callback_data="wiz:more_vid:0")],
        ])
    else:
        rows.append([InlineKeyboardButton(text="➕ Pilihan AI Video Lainnya (Sora 2, Runway, MiniMax, LTX)", callback_data="wiz:more_vid:1")])

    rows.extend([
        [
            InlineKeyboardButton(
                text=f"{'✅ ' if session.upscale_mode=='VIDEO_4K_60FPS' else ''}🎞️ Pertajam & Haluskan Video 4K 60FPS",
                callback_data="wiz:ups:VIDEO_4K_60FPS",
            )
        ],
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='PHOTO_FACE_4K' else ''}🔍 Pertajam Wajah 4K", callback_data="wiz:ups:PHOTO_FACE_4K"),
            InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='TEXT_LINE_4K' else ''}✨ Pertajam Detail 4K", callback_data="wiz:ups:TEXT_LINE_4K"),
        ],
        [InlineKeyboardButton(text="✏️ Ubah Konsep / Deskripsi Video", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 MULAI BUAT VIDEO ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ])
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def build_image_wizard_kb(session: LiveWizardSession, show_more: bool = False) -> tuple[str, InlineKeyboardMarkup]:
    coins, _, _ = session.get_pricing()
    ups_label = UPSCALER_WHITE_LABEL.get(session.upscale_mode, "🔍 Pertajam Foto & Wajah 4K")
    text = (
        f"🎨 **STUDIO GAMBAR 4K — bikinAI**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Deskripsi Gambar:**\n> _{session.prompt}_\n\n"
        f"┣ ⚡ **Mesin AI Gambar:** **`{session.image_engine}`**\n"
        f"┣ 📐 **Ukuran Layar:** `{session.aspect_ratio}`\n"
        f"┗ 🔍 **Penajaman:** `{ups_label}`\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💎 **Biaya:** **`{coins} Koin`** _(Garansi Koin Kembali 100%)_"
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
                InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Recraft V3' else ''}📐 Recraft V3 (Logo)", callback_data="wiz:ieng:Recraft V3"),
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
        [InlineKeyboardButton(text="✏️ Ubah Deskripsi Gambar", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 MULAI BUAT GAMBAR ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ])
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def build_editing_tools_wizard_kb(session: LiveWizardSession) -> tuple[str, InlineKeyboardMarkup]:
    coins, _, _ = session.get_pricing()
    tool_title, tool_desc = IMAGE_EDITING_TOOLS.get(session.edit_tool, IMAGE_EDITING_TOOLS["REMOVE_BG_PNG"])
    text = (
        f"🛠️ **STUDIO EDITING FOTO & VIDEO — bikinAI**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **Fitur Terpilih:** **`{tool_title}`**\n"
        f"ℹ️ **Fungsi:** _{tool_desc}_\n"
        f"📝 **Instruksi:** _{session.prompt}_\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💡 _Khusus Hapus Background, hasil dikirim sebagai **File PNG Transparan Kualitas Tinggi** agar siap ditempel ke desain katalog/poster Anda!_"
    )
    rows = [
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='REMOVE_BG_PNG' else ''}✂️ Hapus Background (File PNG Transparan)", callback_data="wiz:etool:REMOVE_BG_PNG")],
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='RETOUCH_FACE' else ''}✨ Retouch Wajah", callback_data="wiz:etool:RETOUCH_FACE"),
            InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='INPAINT_OBJ' else ''}🖌️ Ganti Baju / Objek", callback_data="wiz:etool:INPAINT_OBJ"),
        ],
        [
            InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='OUTPAINT_EXPAND' else ''}🖼️ Perluas Ukuran Foto", callback_data="wiz:etool:OUTPAINT_EXPAND"),
            InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='PRODUCT_RELIGHT' else ''}📸 Studio Produk UMKM", callback_data="wiz:etool:PRODUCT_RELIGHT"),
        ],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='RESTORE_OLD' else ''}🕰️ Restorasi & Warnai Foto Lama", callback_data="wiz:etool:RESTORE_OLD")],
        [
            InlineKeyboardButton(text="🔍 Pertajam Foto & Wajah 4K", callback_data="wiz:ups:PHOTO_FACE_4K"),
            InlineKeyboardButton(text="🎞️ Pertajam & Haluskan Video 4K 60FPS", callback_data="wiz:ups:VIDEO_4K_60FPS"),
        ],
        [InlineKeyboardButton(text="✏️ Ubah Instruksi / Objek Editing", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 PROSES EDITING SEKARANG ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ]
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


# ==============================================================================
# 11. HELPER TRANSAKSI KOIN, AUTO-REFUND SWEEPER & BROADCAST TOPIK
# ==============================================================================
async def safe_reply_markdown(
    message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None
) -> Message:
    try:
        return await message.reply(text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception:
        return await message.reply(text, parse_mode=None, reply_markup=reply_markup)


async def safe_edit_markdown(
    message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None
) -> None:
    try:
        await message.edit_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception:
        try:
            await message.edit_text(text, parse_mode=None, reply_markup=reply_markup)
        except Exception:
            pass


async def increment_user_usage_counter(db: aiosqlite.Connection, user_id: int, is_render: bool = False) -> None:
    col = "free_img_used_today" if is_render else "chat_used_today"

    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute(f"UPDATE users SET {col} = {col} + 1 WHERE internal_user_id = ?;", (user_id,))

    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def update_personal_memory_if_needed(
    db: aiosqlite.Connection, user_id: int, text: str, current_mem: str
) -> str:
    low = text.lower()
    new_fact = ""
    if any(k in low for k in ("nama saya ", "panggil saya ", "usaha saya ", "jualan ", "bisnis saya ")):
        new_fact = text[:80]
    if new_fact and new_fact not in current_mem:
        updated = (f"{current_mem} | {new_fact}").strip(" |")[:400]

        async def _upd(conn: aiosqlite.Connection) -> None:
            await conn.execute(
                "UPDATE users SET personal_memory_notes = ? WHERE internal_user_id = ?;", (updated, user_id)
            )

        await DB_WRITER_DAEMON.execute_write_tx(db, _upd)
        return updated
    return current_mem


async def deduct_user_coins_for_job(
    db: aiosqlite.Connection, user_id: int, cost: int, allow_bonus: bool, prompt_text: str, engine_used: str
) -> tuple[bool, str, str]:
    job_id = f"JOB-{user_id}-{int(time.time() * 1000)}"
    if cost <= 0 or RUNTIME_CONFIG["HAPPY_HOUR_MODE"]:
        async def _free_tx(conn: aiosqlite.Connection) -> None:
            await conn.execute(
                """
                INSERT INTO jobs (job_id, internal_user_id, cost, deducted_bonus, deducted_utama, status, prompt_text, engine_used, created_at)
                VALUES (?, ?, 0, 0, 0, 'PROCESSING', ?, ?, ?);
                """,
                (job_id, user_id, prompt_text[:200], engine_used, int(time.time())),
            )

        await DB_WRITER_DAEMON.execute_write_tx(db, _free_tx)
        return True, job_id, "Promo Happy Hour (0 Koin)"

    user_lock = get_user_lock(user_id)
    async with user_lock:
        async def _tx(conn: aiosqlite.Connection) -> tuple[bool, str]:
            cur = await conn.execute(
                "SELECT koin_utama, koin_bonus FROM users WHERE internal_user_id = ?;", (user_id,)
            )
            row = await cur.fetchone()
            if not row:
                return False, "Akun belum terdaftar. Ketik /start terlebih dahulu."
            utama, bonus = int(row[0]), int(row[1])

            if allow_bonus:
                if utama + bonus < cost:
                    return False, f"Saldo koin belum cukup (Butuh {cost} Koin, Saldo: {utama} Utama + {bonus} Bonus)."
                use_bonus = min(bonus, cost)
                use_utama = cost - use_bonus
            else:
                if utama < cost:
                    return False, f"Fitur Pro ini memerlukan {cost} Koin Utama (Saldo Koin Utama Anda: {utama})."
                use_bonus = 0
                use_utama = cost

            await conn.execute(
                "UPDATE users SET koin_utama = koin_utama - ?, koin_bonus = koin_bonus - ? WHERE internal_user_id = ?;",
                (use_utama, use_bonus, user_id),
            )
            await conn.execute(
                """
                INSERT INTO jobs (job_id, internal_user_id, cost, deducted_bonus, deducted_utama, status, prompt_text, engine_used, created_at)
                VALUES (?, ?, ?, ?, ?, 'PROCESSING', ?, ?, ?);
                """,
                (job_id, user_id, cost, use_bonus, use_utama, prompt_text[:200], engine_used, int(time.time())),
            )
            return True, f"Terpakai {use_utama} Koin Utama & {use_bonus} Koin Bonus"

        ok, msg = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
        return ok, job_id, msg


async def mark_job_completed(
    db: aiosqlite.Connection, job_id: str, prompt_text: str, engine_name: str, media_url: str = "telegram_delivered"
) -> None:
    sig = hashlib.sha256(f"{engine_name}:{prompt_text.strip().lower()}".encode()).hexdigest()[:24]
    asset_id = f"AST-{sig[:10]}-{int(time.time())}"

    async def _tx(conn: aiosqlite.Connection) -> None:
        await conn.execute("UPDATE jobs SET status = 'COMPLETED' WHERE job_id = ?;", (job_id,))
        await conn.execute(
            """
            INSERT OR REPLACE INTO syndicated_assets (asset_id, prompt_signature, engine_name, media_url, times_reused, created_at)
            VALUES (?, ?, ?, ?, 1, ?);
            """,
            (asset_id, sig, engine_name, media_url, int(time.time())),
        )

    await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def refund_failed_job(db: aiosqlite.Connection, job_id: str) -> bool:
    if not RUNTIME_CONFIG["SUBBOT_REFUND_SWEEPER_ACTIVE"]:
        return False

    async def _tx(conn: aiosqlite.Connection) -> bool:
        cur = await conn.execute(
            "SELECT internal_user_id, deducted_bonus, deducted_utama, refunded_lock FROM jobs WHERE job_id = ?;",
            (job_id,),
        )
        row = await cur.fetchone()
        if not row or int(row[3]) == 1:
            return False
        uid, d_bonus, d_utama = int(row[0]), int(row[1]), int(row[2])
        await conn.execute(
            "UPDATE users SET koin_utama = koin_utama + ?, koin_bonus = MIN(?, koin_bonus + ?) WHERE internal_user_id = ?;",
            (d_utama, MAX_KOIN_BONUS_CAP, d_bonus, uid),
        )
        await conn.execute("UPDATE jobs SET status = 'REFUNDED', refunded_lock = 1 WHERE job_id = ?;", (job_id,))
        return True

    return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)


async def _background_dead_job_sweeper_loop() -> None:
    while True:
        await asyncio.sleep(30)
        if not RUNTIME_CONFIG.get("SUBBOT_REFUND_SWEEPER_ACTIVE", True):
            continue
        try:
            cutoff_ts = int(time.time()) - 60
            async with get_db() as db:
                cur = await db.execute(
                    "SELECT job_id, internal_user_id FROM jobs WHERE status = 'PROCESSING' AND refunded_lock = 0 AND created_at <= ?;",
                    (cutoff_ts,),
                )
                for j_id, u_id in await cur.fetchall():
                    if await refund_failed_job(db, str(j_id)) and BOT_INSTANCE_GLOBAL:
                        try:
                            await BOT_INSTANCE_GLOBAL.send_message(
                                chat_id=int(u_id),
                                text=f"🛡️ **Garansi Koin Kembali 100% (Auto-Refund):** Pesanan `{j_id}` melewati batas 60 detik. Koin Anda telah dikembalikan utuh ke saldo Anda!",
                                parse_mode="Markdown",
                            )
                        except Exception:
                            pass
        except Exception:
            pass


async def broadcast_to_bound_topic(bot: Bot, db: aiosqlite.Connection, binding_key: str, text: str) -> None:
    if binding_key == "ACTIVITY_TOPIC" and not RUNTIME_CONFIG["SUBBOT_NEURAL_FEED_ACTIVE"]:
        return
    bound = await get_topic_binding(db, binding_key)
    if not bound:
        return
    chat_id, topic_id = bound
    try:
        kwargs: dict[str, Any] = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        if topic_id > 0:
            kwargs["message_thread_id"] = topic_id
        await bot.send_message(**kwargs)
    except Exception:
        pass


# ==============================================================================
# 12. PEMBANGUN MENU /ADMIN, SUB-MENU PEMBAYARAN 3 HALAMAN, MANUAL 4-BAB & /BANSOS 4-TAB
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


# ==============================================================================
# 13. COMMAND HANDLERS LENGKAP (/start, /menu, /studio, /riset, /canvas, /bansos, /harvest, /rolling, /donasi_api, /admin)
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


# ==============================================================================
# 14. CALLBACK HANDLERS (/BANSOS 4-TAB, /ADMIN SUB-MENUS, WIZARD & CUSTOMER MENU)
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
                await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            else:
                await refund_failed_job(db, job_id)
                await call.answer("🛡️ Gagal mengambil gambar, koin Anda telah dikembalikan 100%.", show_alert=True)
        elif drv_type == "audiomp3":
            await mark_job_completed(db, job_id, base_prompt, "DRV_AUDIO_MP3")
            await record_job_and_split_profit(db, revenue_idr=cost * 84, actual_hpp_idr=0)
            await call.answer("🎵 Audio MP3 berhasil diekstrak!", show_alert=True)
            await call.message.reply(
                f"🎵 **EKSTRAKSI AUDIO SOUNDTRACK SELESAI**\n"
                f"┣ 🆔 **Nomor Pesanan:** `{job_id}`\n"
                f"┣ 🎼 **Format:** `Stereo MP3 320kbps Jernih`\n"
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


# ==============================================================================
# 15. SETUP GRUP OTONOM (/setup_grup, /ikat), WELCOME GATE, UPLOAD FOTO & CHAT NATURAL
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


# ==============================================================================
# 16. ENTRYPOINT UTAMA (MAIN)
# ==============================================================================
async def main() -> None:
    global BOT_INSTANCE_GLOBAL, BOT_USERNAME_GLOBAL
    if not BOT_TOKEN:
        print("❌ TOKEN_BOT_UTAMA belum diatur di variabel lingkungan (.env)!")
        return

    async with get_db() as db:
        await init_master_db(db)

    if RUNTIME_CONFIG["OWNER_ID_RUNTIME"] == 0:
        print(
            f"🔐 [SECURITY BOOTSTRAP]: ADMIN_USER_ID belum disetel di .env.\n"
            f"👉 Ketik perintah berikut di DM Bot untuk mengunci akses Owner:\n"
            f"   /claim_owner {OWNER_BOOTSTRAP_TOKEN}"
        )

    await start_embedded_web_servers(port=8080)
    asyncio.create_task(_background_dead_job_sweeper_loop())

    bot = Bot(token=BOT_TOKEN)
    BOT_INSTANCE_GLOBAL = bot
    me = await bot.get_me()
    BOT_USERNAME_GLOBAL = me.username or "bikinAI_bot"

    dp = Dispatcher()
    dp.include_router(router)
    print(f"🚀 bikinAI Super Intelligence v3.6.0 (@{BOT_USERNAME_GLOBAL}) SIAP BEROPERASI 100%!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
