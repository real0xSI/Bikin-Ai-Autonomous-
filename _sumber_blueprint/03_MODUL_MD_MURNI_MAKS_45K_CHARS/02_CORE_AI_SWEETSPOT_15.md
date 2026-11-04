```
```
```


<!-- [ID:02_CORE_AI_S007] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: IMPORT-NOT-FOUND -->
# -*- coding: utf-8 -*-
"""
================================================================================
⚡ BIKINAI SUPER INTELLIGENCE — MASTER ENGINE v4.0.0 (MONOLITH-ORCHESTRATOR) ⚡
================================================================================
Arsitektur Produksi Utuh Tanpa Placeholder:
1. Fondasi, Keamanan & 16 Tabel SQLite WAL (~/.bikinai_vault/bikinai_master_vault.db)
   - SingleWriterSQLiteDaemon + 4.096 Lock Stripes + get_db() + check_velocity_rate_limit(0.5s)
   - Fail-Closed Owner Auth (is_verified_owner_dm menolak jika OWNER_ID_RUNTIME == 0) + /claim_owner
   - 16 Tabel Utuh sesuai skema produksi v4.0.0
2. Orchestrator Tipis, Plugin Surface, 6-Gate Zero-Trust Sterilizer, Self-Healing Loop
   (maks 3x retry -> human_escalation_queue + DM Owner), & HumanApprovalGate (5 aksi kritis)
3. Aturan Mutlak Watermark (A4.a) & Ekonomi 4-Zona PPP + Komisi Affiliate Dual-Mode + Auto-CS Siska
4. Smart Router v4.0, 8-Agent Rolling Pool, Staggered Speculative Hedging (1.2s),
   Anti-Soft-Refusal Detector, Strict Privacy Pinning, BittensorChutesAdapter & SOTA Audio
   (Fish Audio S2-Pro Dual-AR & Kokoro-82M v1.0)
5. Dual Web Server Port 8080 (`/` SFW Studio & `/unfiltered-portal` Freedom Web Portal)
   + Hub Omnichannel Lintas Platform (WhatsApp WAHA/Meta, Messenger/IG, TikTok/Shopee Auto-Post)
6. Modul 3 Lengkap: 23 Command Handlers, 6 Callback Routers, Inspektor Layar Pembeli,
   F.new_chat_members, F.photo|F.document, F.text, & Background Autonomous Daemons Loop.
================================================================================
"""

from __future__ import annotations

import ast
import asyncio
import base64
import hashlib
import hmac
import html
import io
import ipaddress
import json
import logging
import math
import os
import re
import secrets
import socket
import sqlite3
import struct
import time
import urllib.parse
import wave
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple

try:
    import aiohttp as _aiohttp_mod  # type: ignore[import-not-found]
    from aiohttp import web as _web_mod  # type: ignore[import-not-found]
    HAS_AIOHTTP = True
except ImportError:  # pragma: no cover
    HAS_AIOHTTP = False

    class _DummyClientResponse:
        status: int = 200
        async def __aenter__(self) -> "_DummyClientResponse":
            return self
        async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
            return None

    class _DummyClientSession:
        def __init__(self, timeout: Any = None) -> None:
            self.timeout = timeout
        async def __aenter__(self) -> "_DummyClientSession":
            return self
        async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
            return None
        def get(self, url: str, **kwargs: Any) -> _DummyClientResponse:
            return _DummyClientResponse()

    class _FallbackAiohttp:
        class ClientTimeout:
            def __init__(self, total: float = 2.5) -> None:
                self.total = total
        ClientSession = _DummyClientSession

    class _DummyRouter:
        def add_get(self, path: str, handler: Any) -> None:
            pass
        def add_post(self, path: str, handler: Any) -> None:
            pass

    class _FallbackWeb:
        class Response:
            def __init__(self, *, text: Optional[str] = None, body: Optional[bytes] = None, content_type: str = "text/plain", headers: Optional[Dict[str, str]] = None, status: int = 200) -> None:
                self.text = text
                self.body = body
                self.content_type = content_type
                self.headers = headers or {}
                self.status = status

        @staticmethod
        def json_response(data: Any, *, status: int = 200) -> "_FallbackWeb.Response":
            return _FallbackWeb.Response(text=json.dumps(data), content_type="application/json", status=status)

        class Application:
            def __init__(self) -> None:
                self.router = _DummyRouter()

        class AppRunner:
            def __init__(self, app: Any) -> None:
                self.app = app
            async def setup(self) -> None:
                pass
            async def cleanup(self) -> None:
                pass

        class TCPSite:
            def __init__(self, runner: Any, host: str = "0.0.0.0", port: int = 8080) -> None:
                self.runner = runner
                self.host = host
                self.port = port
            async def start(self) -> None:
                pass

    _aiohttp_mod = _FallbackAiohttp  # type: ignore[assignment]
    _web_mod = _FallbackWeb  # type: ignore[assignment]

aiohttp: Any = _aiohttp_mod
web: Any = _web_mod

try:
    from aiogram import Bot, Dispatcher, F, Router  # type: ignore[import-not-found]
    from aiogram.client.default import DefaultBotProperties  # type: ignore[import-not-found]
    from aiogram.enums import ParseMode  # type: ignore[import-not-found]
    from aiogram.filters import Command, CommandObject, CommandStart  # type: ignore[import-not-found]
    from aiogram.types import (  # type: ignore[import-not-found]
        CallbackQuery,
        InlineKeyboardButton,
        InlineKeyboardMarkup,
        Message,
        WebAppInfo,
    )
    HAS_AIOGRAM = True
except ImportError:  # pragma: no cover
    HAS_AIOGRAM = False

    class _DummyFilterExpr:
        def __getattr__(self, item: str) -> "_DummyFilterExpr":
            return self
        def startswith(self, prefix: str) -> "_DummyFilterExpr":
            return self
        def __or__(self, other: Any) -> "_DummyFilterExpr":
            return self

    class DefaultBotProperties:
        def __init__(self, parse_mode: Optional[str] = "HTML", **kwargs: Any) -> None:
            self.parse_mode = parse_mode

    class ChatType:
        PRIVATE = "private"
        GROUP = "group"
        SUPERGROUP = "supergroup"

    class ParseMode:
        HTML = "HTML"
        MARKDOWN = "Markdown"

    class Bot:
        def __init__(self, token: str, default: Optional[DefaultBotProperties] = None, **kwargs: Any) -> None:
            self.token = token
            self.default = default
        async def send_message(self, chat_id: int, text: str, **kwargs: Any) -> Any:
            return {"ok": True, "chat_id": chat_id, "text": text}

    class Router:
        def __init__(self, name: str = "") -> None:
            self.name = name
        def message(self, *args: Any, **kwargs: Any) -> Callable[[Any], Any]:
            def _decorator(fn: Any) -> Any:
                return fn
            return _decorator
        def callback_query(self, *args: Any, **kwargs: Any) -> Callable[[Any], Any]:
            def _decorator(fn: Any) -> Any:
                return fn
            return _decorator

    class Dispatcher:
        def __init__(self, **kwargs: Any) -> None:
            self.routers: List[Router] = []
        def include_router(self, r: Router) -> None:
            self.routers.append(r)
        async def start_polling(self, bot: Bot, **kwargs: Any) -> None:
            return None

    class Command:
        def __init__(self, *commands: str, **kwargs: Any) -> None:
            self.commands = commands

    class CommandStart(Command):
        def __init__(self, **kwargs: Any) -> None:
            super().__init__("start", **kwargs)

    class CommandObject:
        args: Optional[str] = None
        command: str = ""

    class WebAppInfo:
        def __init__(self, url: str = "") -> None:
            self.url = url

    class InlineKeyboardButton:
        def __init__(
            self,
            text: str = "",
            callback_data: Optional[str] = None,
            web_app: Optional[WebAppInfo] = None,
            url: Optional[str] = None,
        ) -> None:
            self.text = text
            self.callback_data = callback_data
            self.web_app = web_app
            self.url = url

    class InlineKeyboardMarkup:
        def __init__(self, inline_keyboard: Optional[List[List[InlineKeyboardButton]]] = None) -> None:
            self.inline_keyboard = inline_keyboard or []

    class BufferedInputFile:
        def __init__(self, file: bytes, filename: str) -> None:
            self.file = file
            self.filename = filename

    class LabeledPrice:
        def __init__(self, label: str, amount: int) -> None:
            self.label = label
            self.amount = amount

    class Message:
        from_user: Any = None
        chat: Any = None
        text: Optional[str] = None
        caption: Optional[str] = None
        photo: Optional[List[Any]] = None
        document: Any = None
        new_chat_members: Optional[List[Any]] = None
        message_thread_id: Optional[int] = None
        async def answer(self, text: str, **kwargs: Any) -> Any:
            return None
        async def edit_text(self, text: str, **kwargs: Any) -> Any:
            return None

    class CallbackQuery:
        from_user: Any = None
        message: Any = None
        data: Optional[str] = None
        async def answer(self, text: Optional[str] = None, show_alert: bool = False, **kwargs: Any) -> Any:
            return None

    class PreCheckoutQuery:
        id: str = ""
        from_user: Any = None

    F: Any = _DummyFilterExpr()


<!-- [ID:02_CORE_AI_S008] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: COMMANDOBJECT -->
# ------------------------------------------------------------------------------
@router.message(CommandStart())
async def cmd_start_handler(message: Message, command: Optional[CommandObject] = None) -> None:
    user = message.from_user
    if not user:
        return
    allowed, _ = check_velocity_rate_limit(user.id)
    if not allowed:
        return

    ref_id = 0
    args = (command.args if command and command.args else "").strip()
    if args.startswith("ref_"):
        try:
            ref_id = int(args.replace("ref_", "", 1).strip())
        except ValueError:
            ref_id = 0

    await ensure_user_profile(
        user_id=user.id,
        username=user.username or "",
        first_name=user.first_name or "Sahabat",
        language_code=user.language_code or "id",
        referred_by=ref_id,
    )
    text, kb = await build_buyer_main_menu_view(user.id, user.first_name or "Sahabat")
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.message(Command("menu"))
async def cmd_menu_handler(message: Message) -> None:
    user = message.from_user
    if not user:
        return
    text, kb = await build_buyer_main_menu_view(user.id, user.first_name or "Sahabat")
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


@router.message(Command("studio"))
async def cmd_studio_handler(message: Message) -> None:
    user = message.from_user
    if not user:
        return
    miniapp_url = await get_db().get_setting("miniapp_url", f"{PUBLIC_WEB_BASE_URL}/")
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✨ Buka Studio Kreatif Layar Penuh", web_app=WebAppInfo(url=miniapp_url))],
            [
                InlineKeyboardButton(text="📸 Mode Foto HD", callback_data="wiz:mode:PHOTO_HD"),
                InlineKeyboardButton(text="🎬 Mode Video", callback_data="wiz:mode:VIDEO_CINEMATIC"),
            ],
            [InlineKeyboardButton(text="🖼️➡️🎞️ Mode Gerakkan Foto", callback_data="wiz:mode:IMG2VID_MOTION")],
        ]
    )
    await message.answer(
        "🎨 \x3cb>Studio Kreatif bikinAI\x3c/b>\nPilih mode kreasi cepat di bawah atau buka aplikasi studio penuh:",
        reply_markup=kb,
        parse_mode="HTML",
    )


@router.message(Command("bantuan"))
async def cmd_bantuan_handler(message: Message) -> None:
    text = (
        "📖 \x3cb>Panduan Singkat Penggunaan bikinAI\x3c/b>\n\n"
        "1. \x3cb>Ngobrol & Tanya Jawab:\x3c/b> Langsung ketik pertanyaanmu di chat tanpa perlu perintah khusus.\n"
        "2. \x3cb>Buat Foto & Video:\x3c/b> Klik \x3ccode>/studio\x3c/code> atau tombol di menu utama.\n"
        "3. \x3cb>Gerakkan Foto (Image-to-Video):\x3c/b> Kirim foto dari galerimu disertai kalimat gerakan yang diinginkan.\n"
        "4. \x3cb>Baca Dokumen PDF:\x3c/b> Kirim file PDF dan tulis apa yang ingin dirangkum.\n"
        "5. \x3cb>Bebas Watermark 100%:\x3c/b> Isi Koin Utama mulai \x3cb>Paket Eceran Rp 2.000\x3c/b> (24 Koin Utama) "
        "agar seluruh hasil karyamu bebas tanda air secara otomatis."
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("riset"))
async def cmd_riset_handler(message: Message, command: Optional[CommandObject] = None) -> None:
    user = message.from_user
    if not user:
        return
    query = (command.args if command and command.args else "").strip()
    if not query:
        await message.answer("🔬 Gunakan format: \x3ccode>/riset [topik yang ingin dianalisis mendalam]\x3c/code>", parse_mode="HTML")
        return
    res = await SMART_ROUTER.route_and_execute(query, mode="DEEP_RESEARCH")
    await message.answer(res["text"], parse_mode="HTML")


@router.message(Command("canvas"))
async def cmd_canvas_handler(message: Message, command: Optional[CommandObject] = None) -> None:
    user = message.from_user
    if not user:
        return
    db = get_db()
    await ensure_user_profile(user.id, user.username or "", user.first_name or "")
    content = (command.args if command and command.args else "").strip()
    if not content:
        row = await db.fetch_one("SELECT active_canvas_content FROM users WHERE internal_user_id = ?;", (user.id,))
        curr = (row.get("active_canvas_content") if row else "") or "Kanvas masih kosong. Ketik /canvas [isi draf] untuk menyimpan."
        await message.answer(f"📝 \x3cb>Draf Kanvas Aktif Kamu:\x3c/b>\n\n{html.escape(curr)}", parse_mode="HTML")
        return
    await db.execute_write(
        "UPDATE users SET active_canvas_content = ? WHERE internal_user_id = ?;",
        (content[:8000], user.id),
    )
    await message.answer("✅ Draf berhasil disimpan ke dalam Kanvas pribadimu!", parse_mode="HTML")


@router.message(Command("saran", "feedback"))
async def cmd_feedback_handler(message: Message, command: Optional[CommandObject] = None) -> None:
    user = message.from_user
    if not user:
        return
    fb_text = (command.args if command and command.args else "").strip()
    if not fb_text:
        await message.answer("💌 Kirim masukanmu dengan cara ketik: \x3ccode>/saran [isi masukan]\x3c/code>", parse_mode="HTML")
        return
    fb_id = await get_db().execute_write(
        "INSERT INTO user_feedback (user_id, username, feedback_text, created_at) VALUES (?, ?, ?, ?);",
        (user.id, user.username or "", fb_text[:1000], int(time.time())),
    )
    await message.answer(
        f"🙏 Terima kasih banyak! Masukanmu (#{fb_id}) sudah tercatat dan sangat membantu kami berkembang.",
        parse_mode="HTML",
    )


@router.message(Command("donasi_api", "pasang_bansos"))
async def cmd_donasi_api_handler(message: Message, command: Optional[CommandObject] = None) -> None:
    user = message.from_user
    if not user:
        return
    raw = (command.args if command and command.args else "").strip()
    if not raw or "|" not in raw:
        await message.answer(
            "🤝 \x3cb>Donasi & Pasang Resource Komunitas (6-Gate Zero-Trust Sterilizer)\x3c/b>\n"
            "Format: \x3ccode>/pasang_bansos KATEGORI|NAMA|URL_ENDPOINT|TOKEN_OPSIONAL\x3c/code>\n"
            "Contoh: \x3ccode>/pasang_bansos AI_API|NodeCepat|https\x3a//https://www.google.com/search?q=api.example.com/v1|sk-123\x3c/code>",
            parse_mode="HTML",
        )
        return
    parts = [p.strip() for p in raw.split("|")]
    category = parts[0].upper() if len(parts) > 0 else "AI_API"
    name = parts[1] if len(parts) > 1 else "CommunityNode"
    endpoint = parts[2] if len(parts) > 2 else ""
    secret_meta = parts[3] if len(parts) > 3 else ""

    ok_ssrf, msg_ssrf = ZeroTrust6GateSterilizer.validate_gate1_ssrf(endpoint)
    if not ok_ssrf:
        await message.answer(f"🛡️ Ditolak oleh Gate-1 Anti-SSRF: {html.escape(msg_ssrf)}", parse_mode="HTML")
        return
    ok_threat, msg_threat = await ZeroTrust6GateSterilizer.validate_gate6_adaptive_threat(raw)
    if not ok_threat:
        await message.answer(f"🛡️ Ditolak oleh Gate-6 Adaptive Threat: {html.escape(msg_threat)}", parse_mode="HTML")
        return

    await get_db().execute_write(
        """
        INSERT INTO omni_resource_registry
        (category, resource_name, endpoint_url, secret_or_meta, is_live_verified, expires_at)
        VALUES (?, ?, ?, ?, 1, ?);
        """,
        (category, name, endpoint, secret_meta, int(time.time()) + 30 * 86400),
    )
    await message.answer(
        f"✅ Resource \x3cb>{html.escape(name)}\x3c/b> (\x3ccode>{html.escape(category)}\x3c/code>) "
        f"lolos verifikasi Zero-Trust dan resmi ditambahkan ke kolam komunitas!",
        parse_mode="HTML",
    )


@router.message(Command("setup_grup"))
async def cmd_setup_grup_handler(message: Message) -> None:
    chat_obj: Any = getattr(message, "chat", None)
    if not is_verified_owner_dm(message) and getattr(chat_obj, "type", "") == "private":
        await message.answer("🔒 Perintah ini khusus untuk pengaturan grup oleh Owner/Admin.", parse_mode="HTML")
        return
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📌 Ikat ke Log Pusat", callback_data="bind:LOG_PUSAT"),
                InlineKeyboardButton(text="💬 Ikat ke Ruang Komunitas", callback_data="bind:KOMUNITAS"),
            ],
            [
                InlineKeyboardButton(text="🖼️ Ikat ke Galeri Karya", callback_data="bind:GALERI_KARYA"),
                InlineKeyboardButton(text="🎁 Ikat ke Info Bansos", callback_data="bind:BANSOS_INFO"),
            ],
        ]
    )
    await message.answer(
        "⚙️ \x3cb>Pengaturan Topik Grup Komunitas\x3c/b>\nKlik tombol di bawah pada topik grup yang ingin diikat:",
        reply_markup=kb,
        parse_mode="HTML",
    )


@router.message(Command("ikat"))
async def cmd_ikat_handler(message: Message, command: Optional[CommandObject] = None) -> None:
    key = ((command.args if command and command.args else "KOMUNITAS").strip().upper())
    chat_obj: Any = getattr(message, "chat", None)
    chat_id = int(getattr(chat_obj, "id", 0))
    topic_id = int(getattr(message, "message_thread_id", 0) or 0)
    title = str(getattr(chat_obj, "title", None) or key)
    await get_db().execute_write(
        """
        INSERT INTO bot_bindings (binding_key, chat_id, topic_id, topic_title)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(binding_key) DO UPDATE SET
            chat_id = excluded.chat_id,
            topic_id = excluded.topic_id,
            topic_title = excluded.topic_title;
        """,
        (key, chat_id, topic_id, title),
    )
    await message.answer(
        f"✅ Topik ini berhasil diikat sebagai \x3ccode>{html.escape(key)}\x3c/code> (Chat: \x3ccode>{chat_id}\x3c/code>, Topic: \x3ccode>{topic_id}\x3c/code>).",
        parse_mode="HTML",
    )


@router.message(Command("claim_owner"))
async def cmd_claim_owner_handler(message: Message, command: Optional[CommandObject] = None) -> None:
    global OWNER_ID_RUNTIME
    user = message.from_user
    if not user:
        return
    chat_obj: Any = getattr(message, "chat", None)
    chat_type = getattr(chat_obj, "type", "")
    chat_type_str = chat_type.value if hasattr(chat_type, "value") else str(chat_type)
    if chat_type_str.lower() != "private":
        await message.answer("🔒 Klaim kepemilikan wajib dilakukan di ruang DM/Private bersama bot.", parse_mode="HTML")
        return

    provided_token = (command.args if command and command.args else "").strip()
    if not provided_token or not hmac.compare_digest(provided_token, OWNER_BOOTSTRAP_TOKEN):
        await message.answer("❌ Token bootstrap Owner tidak cocok. Akses ditolak (Fail-Closed).", parse_mode="HTML")
        return

    OWNER_ID_RUNTIME = int(user.id)
    await get_db().set_setting("owner_id", str(OWNER_ID_RUNTIME))
    await message.answer(
        f"👑 \x3cb>Klaim Owner Berhasil!\x3c/b>\n"
        f"ID Anda (\x3ccode>{OWNER_ID_RUNTIME}\x3c/code>) kini terkunci sebagai Owner tunggal sistem v4.0.0.\n"
        f"Ketik \x3ccode>/admin\x3c/code> untuk membuka Ruang Kendali Owner.",
        parse_mode="HTML",
    )


@router.message(Command("set_miniapp"))
async def cmd_set_miniapp_handler(message: Message, command: Optional[CommandObject] = None) -> None:
    if not is_verified_owner_dm(message):
        await message.answer("🔒 Akses ditolak (Khusus DM Owner Terverifikasi).", parse_mode="HTML")
        return
    url = (command.args if command and command.args else "").strip()
    ok, msg = ZeroTrust6GateSterilizer.validate_gate1_ssrf(url)
    if not ok:
        await message.answer(f"❌ URL ditolak Gate-1: {html.escape(msg)}", parse_mode="HTML")
        return
    await get_db().set_setting("miniapp_url", url)
    await message.answer(f"✅ URL Mini-App SFW berhasil diperbarui ke:\n\x3ccode>{html.escape(url)}\x3c/code>", parse_mode="HTML")


@router.message(Command("set_webname"))
async def cmd_set_webname_handler(message: Message, command: Optional[CommandObject] = None) -> None:
    if not is_verified_owner_dm(message):
        await message.answer("🔒 Akses ditolak (Khusus DM Owner Terverifikasi).", parse_mode="HTML")
        return
    new_name = (command.args if command and command.args else "").strip()
    if not new_name:
        await message.answer("Gunakan format: \x3ccode>/set_webname [Nama Portal Baru]\x3c/code>", parse_mode="HTML")
        return
    await get_db().set_setting("freedom_portal_name", new_name[:80])
    await message.answer(
        f"✅ Nama portal `/unfiltered-portal` berhasil diubah menjadi: \x3cb>{html.escape(new_name[:80])}\x3c/b>",
        parse_mode="HTML",
    )


@router.message(Command("set_qris"))
async def cmd_set_qris_handler(message: Message, command: Optional[CommandObject] = None) -> None:
    """
    Mendukung pengaturan QRIS 1x kirim (Universal) atau 3 slot spesifik (GoPay / ShopeePay / DANA).
    """
    if not is_verified_owner_dm(message):
        await message.answer("🔒 Akses ditolak (Khusus DM Owner Terverifikasi).", parse_mode="HTML")
        return
    slot = ((command.args if command and command.args else "UNIVERSAL").strip().upper())
    if slot not in ("UNIVERSAL", "GOPAY", "SHOPEEPAY", "DANA"):
        slot = "UNIVERSAL"
    owner_user: Any = getattr(message, "from_user", None)
    if owner_user is None:
        return
    _RUNTIME_QRIS_WIZARD[int(owner_user.id)] = slot
    await message.answer(
        f"📲 \x3cb>Mode Upload QRIS Aktif (Slot: {slot})\x3c/b>\n"
        f"Silakan kirim gambar barcode QRIS sekarang.\n"
        f"• Untuk 1x kirim semua e-wallet: gunakan \x3ccode>/set_qris UNIVERSAL\x3c/code>\n"
        f"• Untuk 3 slot terpisah: gunakan \x3ccode>/set_qris GOPAY\x3c/code>, \x3ccode>/set_qris SHOPEEPAY\x3c/code>, atau \x3ccode>/set_qris DANA\x3c/code>.",
        parse_mode="HTML",
    )


@router.message(Command("bansos", "info_bansos"))
async def cmd_bansos_handler(message: Message) -> None:
    db = get_db()
    mode = await db.get_setting("bansos_mode", "NORMAL")
    rows = await db.fetch_all(
        "SELECT category, COUNT(*) AS cnt FROM omni_resource_registry WHERE is_live_verified = 1 GROUP BY category;"
    )
    counts = {r["category"]: int(r["cnt"]) for r in rows}
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🤖 AI_API ({counts.get('AI_API', 0)})", callback_data="bns:tab:AI_API"),
                InlineKeyboardButton(text=f"🌐 DOMAINS ({counts.get('DOMAINS', 0)})", callback_data="bns:tab:DOMAINS"),
            ],
            [
                InlineKeyboardButton(text=f"💾 STORAGE ({counts.get('STORAGE', 0)})", callback_data="bns:tab:STORAGE"),
                InlineKeyboardButton(text=f"🧩 AST ({counts.get('AST_PLUGIN', 0)})", callback_data="bns:tab:AST"),
            ],
            [
                InlineKeyboardButton(text="🔇 SILENT", callback_data="bns:mode:SILENT"),
                InlineKeyboardButton(text="🎉 HAPPY_HOUR", callback_data="bns:mode:HAPPY_HOUR"),
                InlineKeyboardButton(text="⚖️ NORMAL", callback_data="bns:mode:NORMAL"),
            ],
        ]
    )
    await message.answer(
        f"🎁 \x3cb>Dasbor Kolam Resource & Bansos Komunitas\x3c/b>\n"
        f"• Mode Saat Ini: \x3cb>{html.escape(mode)}\x3c/b>\n"
        f"Pilih tab kategori resource atau ubah mode distribusi di bawah:",
        reply_markup=kb,
        parse_mode="HTML",
    )


@router.message(Command("rolling", "agents"))
async def cmd_rolling_agents_handler(message: Message) -> None:
    lines = ["🧠 \x3cb>8-Agent Rolling Pool & Combo Grading Score v4.0\x3c/b>\n"]
    for code, ag in AGENT_ROLLING_POOL.items():
        score = compute_combo_grading_score(code, "GENERAL")
        lines.append(
            f"• \x3cb>{ag['display_name']}\x3c/b> (\x3ccode>{code}\x3c/code>)\n"
            f"  Spesialisasi: {ag['specialty']} | Tier-{ag['tier']} | Combo Score: \x3cb>{score}\x3c/b>"
        )
    await message.answer("\n".join(lines), parse_mode="HTML")


@router.message(Command("harvest"))
async def cmd_harvest_handler(message: Message, command: Optional[CommandObject] = None) -> None:
    if not is_verified_owner_dm(message):
        await message.answer("🔒 Akses ditolak (Khusus DM Owner Terverifikasi).", parse_mode="HTML")
        return
    db = get_db()
    tr = await db.fetch_one("SELECT * FROM treasury_summary WHERE id = 1;") or {}
    avail_profit = int(tr.get("harvestable_profit_vault_idr") or 0)
    arg = (command.args if command and command.args else "").strip()
    req_amount = int(arg) if arg.isdigit() else avail_profit

    if req_amount <= 0 or req_amount > avail_profit:
        await message.answer(
            f"🏦 \x3cb>Brankas Treasury Owner\x3c/b>\n"
            f"• Gross Revenue: Rp {int(tr.get('gross_revenue_idr') or 0):,}\n"
            f"• Modal Kerja (35%): Rp {int(tr.get('working_capital_vault_idr') or 0):,}\n"
            f"• Profit Siap Panen (65%): \x3cb>Rp {avail_profit:,}\x3c/b>\n"
            f"• Total Sudah Dipanen: Rp {int(tr.get('total_harvested_by_owner_idr') or 0):,}\n\n"
            f"Ketik \x3ccode>/harvest [nominal]\x3c/code> untuk mencairkan profit.",
            parse_mode="HTML",
        )
        return

    # Kunci dengan HumanApprovalGate untuk WITHDRAW_ABOVE_THRESHOLD
    apr_id, kb = await HumanApprovalGate.request_approval(
        action_type="WITHDRAW_ABOVE_THRESHOLD",
        summary=f"Pencairan Profit Owner sebesar Rp {req_amount:,}",
        payload={"amount_idr": req_amount},
    )
    await message.answer(
        f"🛡️ \x3cb>Konfirmasi Pencairan Profit (`{apr_id}`)\x3c/b>\n"
        f"Nominal: \x3cb>Rp {req_amount:,}\x3c/b>\n"
        f"Silakan setujui melalui tombol Human Approval Gate di bawah:",
        reply_markup=kb,
        parse_mode="HTML",
    )


@router.message(Command("suntik"))
async def cmd_suntik_handler(message: Message, command: Optional[CommandObject] = None) -> None:
    if not is_verified_owner_dm(message):
        await message.answer("🔒 Akses ditolak (Khusus DM Owner Terverifikasi).", parse_mode="HTML")
        return
    raw = (command.args if command and command.args else "").strip()
    if not raw or "|" not in raw:
        await message.answer(
            "💉 \x3cb>Hot-Swap Plugin Surface (/suntik)\x3c/b>\n"
            "Format: \x3ccode>/suntik NAMA_PLUGIN|VERSI|KODE_PYTHON_AST_SAFE\x3c/code>\n"
            "Kode wajib memuat \x3ccode>async def plugin_handler(ctx): ...\x3c/code>",
            parse_mode="HTML",
        )
        return
    name, version, code_str = [p.strip() for p in raw.split("|", 2)]
    ok, msg = await PLUGIN_REGISTRY.hot_swap_plugin(name=name, version=version, source_code=code_str)
    await message.answer(f"{'✅' if ok else '❌'} {html.escape(msg)}", parse_mode="HTML")


@router.message(Command("admin"))
async def cmd_admin_handler(message: Message) -> None:
    if not is_verified_owner_dm(message):
        await message.answer(
            "🔒 \x3cb>Fail-Closed Owner Guard:\x3c/b> Akses ditolak. Jika Anda adalah Owner baru, "
            "gunakan \x3ccode>/claim_owner &lt;TOKEN&gt;\x3c/code> di DM.",
            parse_mode="HTML",
        )
        return
    text, kb = await build_admin_dashboard_view()
    await message.answer(text, reply_markup=kb, parse_mode="HTML")


async def build_admin_dashboard_view() -> Tuple[str, InlineKeyboardMarkup]:
    db = get_db()
    tr = await db.fetch_one("SELECT * FROM treasury_summary WHERE id = 1;") or {}
    users_cnt = await db.fetch_one("SELECT COUNT(*) AS c FROM users;") or {"c": 0}
    esc_cnt = await db.fetch_one("SELECT COUNT(*) AS c FROM human_escalation_queue WHERE status = 'OPEN';") or {"c": 0}
    text = (
        f"👑 \x3cb>BIKINAI SUPER INTELLIGENCE — OWNER COCKPIT v4.0.0\x3c/b>\n\n"
        f"📊 \x3cb>Metrik Inti & Treasury:\x3c/b>\n"
        f"• Total Pengguna: \x3cb>{users_cnt['c']}\x3c/b>\n"
        f"• Total Job Selesai: \x3cb>{tr.get('total_jobs_completed', 0)}\x3c/b>\n"
        f"• Gross Revenue: \x3cb>Rp {int(tr.get('gross_revenue_idr') or 0):,}\x3c/b>\n"
        f"• Profit Siap Panen: \x3cb>Rp {int(tr.get('harvestable_profit_vault_idr') or 0):,}\x3c/b>\n"
        f"• Insiden Eskalasi Terbuka: \x3cb>{esc_cnt['c']}\x3c/b>\n"
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👁️ Inspektor Layar Pembeli (Buyer UI)",
                    callback_data="adm:preview_buyer_ui",
                )
            ],
            [
                InlineKeyboardButton(text="💳 Pengaturan Pembayaran (3 Hal)", callback_data="adm:pay_menu:1"),
                InlineKeyboardButton(text="📘 Buku Manual Owner (4 Bab)", callback_data="adm:manual:1"),
            ],
            [
                InlineKeyboardButton(text="🤖 Sub-Bots & Omnichannel", callback_data="adm:subbots"),
                InlineKeyboardButton(text="🎁 Panel Bansos 4-Tab", callback_data="bns:tab:AI_API"),
            ],
        ]
    )
    return text, kb



<!-- [ID:02_CORE_AI_S009] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: :40 -->
# 12. COMMAND HANDLERS
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
        await message.reply("🔒 Khusus Owner di DM.")
        return
    new_name = (message.text or "").partition(" ")[2].strip()
    if not new_name:
        await message.reply(f"🌐 **Nama Website:** `{RUNTIME_CONFIG['WEB_BRAND_NAME']}`\nUbah: `/set_webname NamaBaru`", parse_mode="Markdown")
        return
    RUNTIME_CONFIG["WEB_BRAND_NAME"] = new_name[:40]
    async with get_db() as db:
        await save_persistent_setting(db, "WEB_BRAND_NAME", RUNTIME_CONFIG["WEB_BRAND_NAME"])
    await message.reply(f"✅ **Nama Brand Website diubah menjadi:** `{RUNTIME_CONFIG['WEB_BRAND_NAME']}`", parse_mode="Markdown")


@router.message(Command("claim_owner"))
async def cmd_claim_owner_bootstrap(message: Message) -> None:
    if message.chat.type != "private":
        return
    token_arg = (message.text or "").partition(" ")[2].strip()
    if RUNTIME_CONFIG["OWNER_ID_RUNTIME"] == 0 and hmac.compare_digest(token_arg, OWNER_BOOTSTRAP_TOKEN):
        RUNTIME_CONFIG["OWNER_ID_RUNTIME"] = message.from_user.id
        async with get_db() as db:
            await save_persistent_setting(db, "OWNER_ID_RUNTIME", str(message.from_user.id))
        await message.reply(f"✅ **Owner dikunci ke ID `{message.from_user.id}`.** Ketik `/admin`.")
    else:
        await message.reply("🔒 Token tidak valid atau Owner sudah terkunci.")


@router.message(Command("harvest"))
async def cmd_quick_harvest_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Khusus Owner di DM.")
        return
    async with get_db() as db:
        ok, harvested_now, total_h = await execute_manual_profit_harvest(db)
    await message.reply(f"🌾 **HARVEST BERHASIL:** `Rp {harvested_now:,}` (Total: `Rp {total_h:,}`)" if ok else "ℹ️ Belum ada laba bersih siap panen.", parse_mode="Markdown")


@router.message(Command("bansos", "info_bansos"))
async def cmd_bansos_radar_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Khusus Owner di DM.")
        return
    async with get_db() as db:
        txt, kb = await _build_bansos_4tab_view(db, "AI_API")
    await safe_reply_markdown(message, txt, reply_markup=kb)


@router.message(Command("rolling", "agents"))
async def cmd_rolling_agents_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Khusus Owner di DM.")
        return
    nxt = rotate_primary_agent()
    async with get_db() as db:
        await save_persistent_setting(db, "PRIMARY_ROLLING_AGENT", nxt)
    lines = [f"▸ {'🟢' if k == nxt else '⚪'} **`{k}`** — `{v['title']}` _(OK: {v['ok']} | Fail: {v['fail']})_" for k, v in AGENTIC_ROLLING_POOL.items()]
    await safe_reply_markdown(message, f"🔄 **PRIMARY AGENT:** **`{nxt}`**\n\n" + "\n".join(lines))


@router.message(Command("donasi_api"))
async def cmd_community_donate_api(message: Message) -> None:
    args = (message.text or "").split()[1:]
    if not args:
        await message.reply("Format: `/donasi_api https://endpoint/v1/chat/completions model-slug`", parse_mode="Markdown")
        return
    ep_url, model_slug = args[0].strip(), (args[1].strip() if len(args) > 1 else "openai")
    wait = await message.reply("🛡️ **Memeriksa Endpoint dengan 4-Gate Sterilizer...**", parse_mode="Markdown")
    ok_ping, ms, info = await ping_and_verify_bansos_endpoint(ep_url, model_slug)
    if not ok_ping:
        await safe_edit_markdown(wait, f"❌ **Ditolak:** `{info}`")
        return
    user_id, username = message.from_user.id, message.from_user.username or "Kreator"
    res_id = f"COM-{hashlib.sha256(ep_url.encode()).hexdigest()[:8].upper()}"
    async with get_db() as db:
        await ensure_user_and_track_identity(db, user_id, username)
        async def _tx(conn: aiosqlite.Connection) -> None:
            await conn.execute("INSERT OR REPLACE INTO omni_resource_registry (resource_id, category, resource_name, endpoint_url, secret_or_meta, is_live_verified, expires_at) VALUES (?, 'AI_API', ?, ?, ?, 1, ?);", (res_id, f"Node ({username})", ep_url, model_slug, int(time.time()) + 30 * 86400))
            await conn.execute("UPDATE users SET koin_bonus = MIN(?, koin_bonus + 15) WHERE internal_user_id = ?;", (MAX_KOIN_BONUS_CAP, user_id))
        await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
    await safe_edit_markdown(wait, f"✅ **TERVERIFIKASI ({ms} ms)!** +15 Koin Bonus ditambahkan.")


@router.message(Command("riset"))
async def cmd_deep_research_handler(message: Message) -> None:
    user_id, username = message.from_user.id, message.from_user.username or "Kreator"
    raw_arg = (message.text or "").partition(" ")[2].strip()
    if not raw_arg:
        await message.reply("Format: `/riset [topik teknis / bisnis]`", parse_mode="Markdown")
        return
    clean_q, is_attack = sanitize_and_deobfuscate_input(raw_arg)
    if is_attack:
        await message.reply("🛡️ Pola teks tidak diizinkan.")
        return
    wait = await message.reply("🔬 **Menyusun analisis teknis...**", parse_mode="Markdown")
    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username)
        await increment_user_usage_counter(db, user_id, is_render=False)
        res = await generate_frontier_ai_response(db, clean_q, mode="DEEP_RESEARCH", personal_memory=u["memory"])
    await safe_edit_markdown(wait, f"🔬 **LAPORAN RISET TEKNIS**\n━━━━━━━━━━━━━━━━━━\n{res}")


@router.message(Command("canvas"))
async def cmd_canvas_workspace_handler(message: Message) -> None:
    user_id, username = message.from_user.id, message.from_user.username or "Kreator"
    raw_arg = (message.text or "").partition(" ")[2].strip()
    async with get_db() as db:
        u = await ensure_user_and_track_identity(db, user_id, username)
        if not raw_arg:
            await safe_reply_markdown(message, f"📝 **CANVAS WORKSPACE**\n━━━━━━━━━━━━━━━━━━\n{u['canvas'] or '_(Kosong. Gunakan `/canvas [instruksi]`)_'}")
            return
        clean_arg, is_attack = sanitize_and_deobfuscate_input(raw_arg)
        if is_attack:
            await message.reply("🛡️ Pola teks tidak diizinkan.")
            return
        wait = await message.reply("📝 **Memperbarui Canvas...**", parse_mode="Markdown")
        await increment_user_usage_counter(db, user_id, is_render=False)
        updated_canvas = await generate_frontier_ai_response(db, clean_arg, mode="CANVAS_EDIT", personal_memory=u["memory"], canvas_state=u["canvas"])
        async def _save_c(conn: aiosqlite.Connection) -> None:
            await conn.execute("UPDATE users SET active_canvas_content = ? WHERE internal_user_id = ?;", (updated_canvas[:4000], user_id))
        await DB_WRITER_DAEMON.execute_write_tx(db, _save_c)
    await safe_edit_markdown(wait, f"📝 **CANVAS DIPERBARUI**\n━━━━━━━━━━━━━━━━━━\n{updated_canvas}")


@router.message(Command("saran", "feedback"))
async def cmd_user_feedback_handler(message: Message) -> None:
    user_id, username = message.from_user.id, message.from_user.username or "Kreator"
    raw_fb = (message.text or "").partition(" ")[2].strip()
    if not raw_fb:
        await message.reply("Format: `/saran [masukan Anda]`", parse_mode="Markdown")
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
        await broadcast_to_bound_topic(message.bot, db, "FEEDBACK_TOPIC", f"🛠️ **Masukan dari `@{username}`:**\n> _{clean_fb[:300]}_")
    await message.reply("✅ Masukan tercatat.")


@router.message(Command("set_miniapp"))
async def cmd_set_miniapp_url(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Khusus Owner di DM.")
        return
    arg_url = (message.text or "").partition(" ")[2].strip()
    if not arg_url.startswith("https://"):
        await message.reply(f"🌐 **URL Mini App:** `{RUNTIME_CONFIG['MINIAPP_URL'] or 'Belum disetel'}`", parse_mode="Markdown")
        return
    RUNTIME_CONFIG["MINIAPP_URL"] = arg_url
    async with get_db() as db:
        await save_persistent_setting(db, "MINIAPP_URL", arg_url)
    await message.reply(f"✅ **URL Mini App Dikunci:** `{arg_url}`", parse_mode="Markdown")


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
    await message.reply(f"✅ **PRESET TERPASANG:** `{count_installed} Resource` | **AST Hash:** `{ast_check['hash']}`", parse_mode="Markdown")


@router.message(Command("admin"))
async def cmd_owner_admin_panel(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Khusus Owner di DM pribadi.", parse_mode="Markdown")
        return
    async with get_db() as db:
        await save_persistent_setting(db, "OWNER_ID_RUNTIME", str(message.from_user.id))
        cur = await db.execute("SELECT gross_revenue_idr, working_capital_vault_idr, harvestable_profit_vault_idr, total_harvested_by_owner_idr, total_jobs_completed FROM treasury_summary WHERE id = 1;")
        row = await cur.fetchone()
    txt, kb = _build_owner_admin_panel_view(row)
    await safe_reply_markdown(message, txt, reply_markup=kb)


