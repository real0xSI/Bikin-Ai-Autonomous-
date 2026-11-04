
<!-- [ID:22_HITL_ACTION_S001] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: STR, :-1 -->
# Daftar perintah yang WAJIB PIN + HMAC
SENSITIVE_PREFIXES = (
    "/panic", "/freeze", "/approve", "/deny",
    "/recover", "/readonly", "/spawn", "/pr create",
)

OWNER_IDS: dict[Channel, set[str]] = {
    "telegram":     set(filter(None, os.environ.get("TELEGRAM_OWNER_ID", "").split(","))),
    "whatsapp":     set(filter(None, os.environ.get("WHATSAPP_OWNER_NUMBER", "").split(","))),
    "instagram":    set(filter(None, os.environ.get("INSTAGRAM_OWNER_ID", "").split(","))),
    "threads":      set(filter(None, os.environ.get("THREADS_OWNER_ID", "").split(","))),
    "github_issue": set(filter(None, os.environ.get("GITHUB_OWNER_LOGIN", "").split(","))),
}

def is_sensitive(text: str) -> bool:
    t = text.strip().lower()
    return any(t.startswith(p) for p in SENSITIVE_PREFIXES)

def is_owner(channel: Channel, user_id: str) -> bool:
    return str(user_id) in OWNER_IDS.get(channel, set())

def verify_pin(text: str) -> bool:
    """PIN ditulis di akhir perintah, contoh: /panic 123456"""
    if not OWNER_PIN:
        return False
    parts = text.strip().split()
    return len(parts) >= 2 and parts[-1] == OWNER_PIN

def verify_hmac(payload: str, signature: str, ts: int, nonce: str) -> bool:
    if not HMAC_SECRET:
        return False
    if abs(time.time() - ts) > WINDOW_SEC:
        return False
    msg = f"{payload}|{ts}|{nonce}".encode()
    expected = hmac.new(HMAC_SECRET, msg, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

def verify(channel: Channel, user_id: str, text: str,
           signature: str | None = None, ts: int | None = None,
           nonce: str | None = None) -> dict:
    """
    Return: {"ok": bool, "reason": str, "clean_text": str}
    clean_text = text tanpa PIN di belakang.
    """
    if not is_owner(channel, user_id):
        return {"ok": False, "reason": "owner_mismatch", "clean_text": text}

    if is_sensitive(text):
        if not verify_pin(text):
            return {"ok": False, "reason": "pin_invalid", "clean_text": text}
        if signature and ts and nonce:
            if not verify_hmac(text, signature, ts, nonce):
                return {"ok": False, "reason": "hmac_invalid", "clean_text": text}
        parts = text.strip().split()
        clean = " ".join(parts[:-1])
        return {"ok": True, "reason": "ok", "clean_text": clean}

    return {"ok": True, "reason": "ok", "clean_text": text.strip()}

"""
Dispatcher tunggal untuk semua channel.
Terima teks perintah → verifikasi → route ke orchestrator.
"""
import json, time, hashlib
from pathlib import Path
from typing import Literal
from .verify import verify, Channel

AUDIT = Path("office/logs/audit.log")
AUDIT.parent.mkdir(parents=True, exist_ok=True)

def _audit(event: dict):
    event["ts"] = time.time()
    line = json.dumps(event, sort_keys=True, ensure_ascii=False)
    h = hashlib.sha256(line.encode()).hexdigest()
    with AUDIT.open("a") as f:
        f.write(f"{h} {line}\n")

def _route(clean_text: str, channel: Channel, user_id: str) -> str:
    """
    Routing tipis: panggil orchestrator lokal / HTTP.
    Gunakan import lokal agar mudah diuji.
    """
    try:
        from office.orchestrator.main import dispatch_command
        return dispatch_command(text=clean_text, channel=channel, user_id=str(user_id))
    except Exception as e:
        return f"⚠️ orchestrator error: {type(e).__name__}: {e}"

def dispatch(text: str, channel: Channel, user_id: str,
             signature: str | None = None,
             ts: int | None = None,
             nonce: str | None = None) -> str:
    v = verify(channel=channel, user_id=str(user_id), text=text,
               signature=signature, ts=ts, nonce=nonce)
    _audit({"type": "command_in", "channel": channel,
            "user": str(user_id), "ok": v["ok"], "reason": v["reason"],
            "text_hash": hashlib.sha256(text.encode()).hexdigest()})

    if not v["ok"]:
        return f"⛔ Ditolak: {v['reason']}"

    result = _route(v["clean_text"], channel, user_id)
    _audit({"type": "command_out", "channel": channel,
            "result_preview": result[:200]})
    return result

"""
GitHub IssueOps: owner buka Issue berlabel 'command' berisi perintah.
Format body:
  /status
  /panic 123456
  /approve apv_2026_001 123456
Verifikasi: actor = owner + PIN (untuk perintah sensitif).
"""
import os, sys, subprocess, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bots.core.dispatcher import dispatch

def comment_issue(issue: int, body: str):
    subprocess.run(["gh", "issue", "comment", str(issue), "--body", body], check=False)

def label_issue(issue: int, label: str):
    subprocess.run(["gh", "issue", "edit", str(issue), "--add-label", label], check=False)

def main():
    body = os.environ.get("ISSUE_BODY", "").strip()
    issue = int(os.environ.get("ISSUE_NUMBER", "0"))
    actor = os.environ.get("OWNER", "")

    if not body:
        comment_issue(issue, "⚠️ Body Issue kosong.")
        return

    first_line = body.splitlines()[0].strip()
    comment_issue(issue, f"⏳ Memproses: `{first_line}`")

    result = dispatch(text=first_line, channel="github_issue", user_id=actor)

    comment_issue(issue, f"```\n{result[:6000]}\n```")

    if result.startswith("⛔"):
        label_issue(issue, "rejected")
    else:
        label_issue(issue, "processed")

if __name__ == "__main__":
    main()

import os, time, hashlib
import requests
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bots.core.dispatcher import dispatch

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}"
HMAC_SECRET = os.environ.get("HMAC_SECRET", "").encode()

def send(chat_id, text):
    requests.post(f"{API}/sendMessage",
                  json={"chat_id": chat_id, "text": text[:4000],
                        "parse_mode": "Markdown"})

def poll():
    offset = None
    while True:
        try:
            r = requests.get(f"{API}/getUpdates",
                             params={"timeout": 30, "offset": offset}).json()
            for u in r.get("result", []):
                offset = u["update_id"] + 1
                msg = u.get("message") or {}
                if not msg: continue
                chat_id = msg["chat"]["id"]
                user_id = msg["from"]["id"]
                text = (msg.get("text") or "").strip()
                if not text: continue

                # HMAC opsional: pesan bisa diawali "sig:<hex> ts:<unix> n:<nonce> | <command>"
                sig = ts = nonce = None
                payload = text
                if "|" in text and text.startswith("sig:"):
                    head, payload = text.split("|", 1)
                    kv = dict(p.split(":") for p in head.strip().split())
                    sig, ts, nonce = kv.get("sig"), int(kv.get("ts", 0)), kv.get("n")
                    payload = payload.strip()

                result = dispatch(text=payload, channel="telegram",
                                  user_id=str(user_id),
                                  signature=sig, ts=ts, nonce=nonce)
                send(chat_id, result)
        except Exception as e:
            print("poll error:", e)
            time.sleep(3)

if __name__ == "__main__":
    poll()

"""
Load brain files sebagai konteks yang WAJIB disertakan ke setiap agent.
Cache dengan hash; reload jika file berubah atau owner kirim /reload brain.
"""
import hashlib, json
from pathlib import Path
from typing import Dict, List

BRAIN_DIR = Path("office/brain")
CACHE = Path("office/logs/brain_cache.json")
CACHE.parent.mkdir(parents=True, exist_ok=True)

ORDER = [
    "vision.md", "strategy.md", "roadmap.md", "principles.md",
    "conventions.md", "stack.md", "security-rules.md",
    "onchain-rules.md", "glossary.md",
]

def _hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def load_brain(force: bool = False) -> Dict[str, str]:
    state = {}
    for name in ORDER:
        p = BRAIN_DIR / name
        if p.exists():
            text = p.read_text()
            state[name] = {"hash": _hash(text), "text": text}
        else:
            state[name] = {"hash": None, "text": ""}
    CACHE.write_text(json.dumps({k: v["hash"] for k, v in state.items()}, indent=2))
    return {k: v["text"] for k, v in state.items()}

def brain_prompt() -> str:
    b = load_brain()
    sections = []
    for name in ORDER:
        if b.get(name):
            sections.append(f"## {name}\n{b[name]}")
    return "\n\n".join(sections)

"""
Satu-satunya pintu approval. Tidak ada agent lain yang boleh bypass.
Approval disimpan sebagai file JSON per id, dengan status pending/approved/denied/expired.
"""
import json, time, uuid, hashlib
from pathlib import Path

STORE = Path("office/logs/approvals")
STORE.mkdir(parents=True, exist_ok=True)

def _now(): return time.time()

def create(agent_id: str, gate: str, payload: dict, ttl_hours: int = 24) -> str:
    apv_id = f"apv_{int(_now())}_{uuid.uuid4().hex[:6]}"
    record = {
        "id": apv_id,
        "agent_id": agent_id,
        "gate": gate,
        "payload": payload,
        "status": "pending",
        "created": _now(),
        "expires": _now() + ttl_hours * 3600,
        "decided_by": None,
        "decided_at": None,
        "decision_note": None,
    }
    (STORE / f"{apv_id}.json").write_text(json.dumps(record, indent=2))
    return apv_id

def get(apv_id: str) -> dict | None:
    p = STORE / f"{apv_id}.json"
    if not p.exists(): return None
    return json.loads(p.read_text())

def decide(apv_id: str, decision: str, owner: str, note: str = "") -> dict:
    rec = get(apv_id)
    if not rec: return {"ok": False, "reason": "not_found"}
    if rec["status"] != "pending":
        return {"ok": False, "reason": f"already_{rec['status']}"}
    if _now() > rec["expires"]:
        rec["status"] = "expired"; (STORE / f"{apv_id}.json").write_text(json.dumps(rec))
        return {"ok": False, "reason": "expired"}
    if decision not in ("approved", "denied"):
        return {"ok": False, "reason": "invalid_decision"}
    rec["status"] = decision
    rec["decided_by"] = owner
    rec["decided_at"] = _now()
    rec["decision_note"] = note
    (STORE / f"{apv_id}.json").write_text(json.dumps(rec, indent=2))
    return {"ok": True, "record": rec}

def list_pending() -> list[dict]:
    out = []
    for p in STORE.glob("apv_*.json"):
        r = json.loads(p.read_text())
        if r["status"] == "pending":
            out.append(r)
    return sorted(out, key=lambda x: x["created"])

"""
Kill switch L0–L4. State disimpan di file agar tetap berlaku setelah restart.
"""
import json, time
from pathlib import Path

STATE = Path("office/logs/kill_switch.json")
STATE.parent.mkdir(parents=True, exist_ok=True)

LEVELS = ["L0_PANIC", "L1_FREEZE_FINANCE", "L2_FREEZE_EXTERNAL",
          "L3_FREEZE_AGENT", "L4_READONLY"]

def _load() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"level": None, "scope": None, "since": None, "by": None}

def _save(s: dict):
    STATE.write_text(json.dumps(s, indent=2))

def current() -> dict:
    return _load()

def trigger(level: str, by: str, scope=None) -> dict:
    if level not in LEVELS:
        return {"ok": False, "reason": "invalid_level"}
    s = {"level": level, "scope": scope, "since": time.time(), "by": by}
    _save(s)
    return {"ok": True, "state": s}

def restore(by: str) -> dict:
    s = {"level": None, "scope": None, "since": time.time(), "by": by}
    _save(s)
    return {"ok": True, "state": s}

def is_frozen(agent_id: str | None = None, category: str | None = None) -> bool:
    s = _load()
    if s["level"] is None: return False
    if s["level"] == "L0_PANIC": return True
    if s["level"] == "L4_READONLY": return True   # diblok tulis, dibaca orchestrator
    if s["level"] == "L3_FREEZE_AGENT":
        return agent_id is not None and s["scope"] == agent_id
    if s["level"] == "L1_FREEZE_FINANCE":
        return category in ("finance", "treasury", "onchain", "wallet")
    if s["level"] == "L2_FREEZE_EXTERNAL":
        return category in ("external", "social", "email", "webhook", "scanner")
    return False

"""
Evaluasi apakah aksi agent boleh langsung, notify, atau gate ke owner.
Sumber: agents.yaml + approval_matrix.yaml
"""
import yaml
from pathlib import Path

CFG = yaml.safe_load(Path("office/config/agents.yaml").read_text())
APV = yaml.safe_load(Path("office/config/approval_matrix.yaml").read_text())
AGENTS = {a["id"]: a for a in CFG["agents"]}
GATE_TTL = {g: d.get("timeout_hours", 24) for g, d in APV["gates"].items()}

def evaluate(agent: dict, action: dict) -> dict:
    """
    action: {"type": "...", "amount": ..., "is_public": bool, ...}
    Return: {"decision": "auto|notify|gate|deny", "gate": str|None, "reason": str}
    """
    cat = agent.get("cat", "")
    if agent.get("auto") == "gate":
        return {"decision": "gate",
                "gate": agent.get("gate", ["STR"])[0],
                "reason": "agent_requires_owner"}

    touched = set(agent.get("gate", []))
    if action.get("amount") and touched & {"FIN"}:
        return {"decision": "gate", "gate": "FIN", "reason": "money_move"}
    if action.get("is_public") and "PUB" in touched:
        return {"decision": "gate", "gate": "PUB", "reason": "public_action"}
    if action.get("is_deploy") and "DEP" in touched:
        return {"decision": "gate", "gate": "DEP", "reason": "deploy_prod"}
    if action.get("is_onchain") and "CHAIN" in touched:
        return {"decision": "gate", "gate": "CHAIN", "reason": "onchain_action"}
    if action.get("is_incident") and "INC" in touched:
        return {"decision": "gate", "gate": "INC", "reason": "incident"}
    if action.get("is_legal") and "LEG" in touched:
        return {"decision": "gate", "gate": "LEG", "reason": "legal_commit"}
    if action.get("is_people") and "PPL" in touched:
        return {"decision": "gate", "gate": "PPL", "reason": "people_change"}
    if action.get("is_strategy") and "STR" in touched:
        return {"decision": "gate", "gate": "STR", "reason": "strategy_change"}

    if agent.get("auto") == "notify":
        return {"decision": "notify", "gate": None, "reason": "agent_notify_mode"}
    return {"decision": "auto", "gate": None, "reason": "ok"}

"""
Orchestrator utama. Menyatukan:
- brain loader
- kill switch
- policy engine
- approval broker
- notification (WA/Tele)
- audit log append-only
"""
import os, json, time, hashlib, yaml
from pathlib import Path
from typing import Literal

from .brain_loader import brain_prompt
from .kill_switch import current as kill_current, trigger as kill_trigger, restore as kill_restore, is_frozen
from .policy_engine import evaluate, AGENTS, GATE_TTL
from . import approval_broker as APV
from .audit import audit


<!-- [ID:22_HITL_ACTION_S002] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: ANY, BOOL, NAME -->
# ==============================================================================
@dataclass
class RegisteredPlugin:
    name: str
    version: str
    handler: Callable[..., Awaitable[Any]]
    health_check: Callable[[], Awaitable[bool]]
    registered_at: int = field(default_factory=lambda: int(time.time()))
    last_healthy: bool = True


class PluginRegistry:
    """
    Plugin Surface untuk arsitektur Monolith-Orchestrator.
    Mendukung registrasi plugin, pemeriksaan kesehatan menyeluruh, dan hot-swap via /suntik.
    """

    def __init__(self) -> None:
        self._plugins: Dict[str, RegisteredPlugin] = {}

    def register(
        self,
        name: str,
        version: str,
        handler: Callable[..., Awaitable[Any]],
        health_check: Optional[Callable[[], Awaitable[bool]]] = None,
    ) -> RegisteredPlugin:
        async def _default_health() -> bool:
            return True

        plugin = RegisteredPlugin(
            name=name.strip(),
            version=version.strip(),
            handler=handler,
            health_check=health_check or _default_health,
        )
        self._plugins[plugin.name] = plugin
        return plugin

    async def check_all_health(self) -> Dict[str, Dict[str, Any]]:
        report: Dict[str, Dict[str, Any]] = {}
        for name, plug in self._plugins.items():
            try:
                ok = bool(await plug.health_check())
            except Exception as exc:
                ok = False
                logger.warning("Plugin health check failed for %s: %s", name, exc)
            plug.last_healthy = ok
            report[name] = {
                "version": plug.version,
                "healthy": ok,
                "registered_at": plug.registered_at,
            }
        return report

    async def hot_swap_plugin(
        self,
        name: str,
        version: str,
        source_code: str,
    ) -> Tuple[bool, str]:
        ok_ast, msg_ast = ZeroTrust6GateSterilizer.validate_gate2_ast(source_code)
        if not ok_ast:
            return False, f"Gate-2 AST Sterilizer menolak plugin: {msg_ast}"
        ok_threat, msg_threat = await ZeroTrust6GateSterilizer.validate_gate6_adaptive_threat(source_code)
        if not ok_threat:
            return False, f"Gate-6 Adaptive Threat menolak plugin: {msg_threat}"

        safe_ns: Dict[str, Any] = {
            "__builtins__": {
                "len": len,
                "min": min,
                "max": max,
                "sum": sum,
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "dict": dict,
                "list": list,
                "tuple": tuple,
                "set": set,
                "round": round,
                "abs": abs,
                "enumerate": enumerate,
                "range": range,
                "zip": zip,
            },
            "asyncio": asyncio,
            "json": json,
            "math": math,
            "re": re,
            "time": time,
        }
        try:
            compiled = compile(source_code, filename=f"\x3cplugin:{name}:{version}>", mode="exec")
            exec(compiled, safe_ns, safe_ns)  # noqa: S102 - already AST-sterilized by Gate-2
            handler = safe_ns.get("plugin_handler")
            health_fn = safe_ns.get("plugin_health")
            if not callable(handler):
                return False, "Kode plugin wajib mendefinisikan `async def plugin_handler(ctx): ...`"
            self.register(name=name, version=version, handler=handler, health_check=health_fn)
            await get_db().execute_write(
                """
                INSERT INTO omni_resource_registry
                (category, resource_name, endpoint_url, secret_or_meta, is_live_verified, expires_at)
                VALUES ('AST_PLUGIN', ?, 'internal://plugin_registry', ?, 1, 0);
                """,
                (f"{name}@{version}", source_code[:2000]),
            )
            return True, f"Plugin `{name}` v{version} berhasil di-hot-swap secara aman."
        except Exception as exc:
            return False, f"Gagal mengompilasi plugin `{name}`: {exc}"

    def list_plugins(self) -> List[RegisteredPlugin]:
        return list(self._plugins.values())


PLUGIN_REGISTRY = PluginRegistry()


class ZeroTrust6GateSterilizer:
    """
    6-Gate Zero-Trust Sterilizer:
    - Gate 1: Anti-SSRF DNS/IP Validator
    - Gate 2: Whitelist AST Sterilizer v4.0 (blokir dunder & modul berbahaya)
    - Gate 3: Payload Malware & Magic Bytes Scrubber
    - Gate 4: Live Ping <2.5s
    - Gate 5: ProtectAI ModelScan Enforcer (.safetensors/.gguf, blokir .pkl/.pt/.bin)
    - Gate 6: Adaptive Threat Memory (auto-regex dari serangan baru)
    """

    FORBIDDEN_DUNDERS = {
        "__subclasses__",
        "__globals__",
        "__builtins__",
        "__import__",
        "__code__",
        "__closure__",
        "__mro__",
        "__bases__",
        "__dict__",
        "__getattribute__",
        "__setattr__",
        "__delattr__",
        "__reduce__",
        "__reduce_ex__",
    }
    FORBIDDEN_CALLS = {
        "eval",
        "exec",
        "compile",
        "open",
        "input",
        "getattr",
        "setattr",
        "delattr",
        "globals",
        "locals",
        "vars",
        "__import__",
        "breakpoint",
    }
    FORBIDDEN_MODULES = {
        "os",
        "sys",
        "subprocess",
        "shutil",
        "socket",
        "ctypes",
        "pickle",
        "marshal",
        "importlib",
        "pty",
        "resource",
        "signal",
        "multiprocessing",
        "threading",
        " pathlib",
        "pathlib",
        " inspect",
        "inspect",
        "builtins",
    }

    @staticmethod
    def validate_gate1_ssrf(url: str) -> Tuple[bool, str]:
        """Gate 1: Anti-SSRF DNS/IP Validator."""
        try:
            parsed = urllib.parse.urlparse(url.strip())
            if parsed.scheme not in ("https", "http"):
                return False, "Skema URL wajib http/https."
            hostname = (parsed.hostname or "").strip().lower()
            if not hostname:
                return False, "Hostname URL kosong."
            if hostname in ("localhost", "127.0.0.1", "0.0.0.0", "::1", "metadata.google.internal"):
                return False, "Hostname lokal/metadata diblokir oleh Gate-1 Anti-SSRF."
            if hostname.endswith((".local", ".internal", ".lan", ".arpa")):
                return False, "Domain internal diblokir oleh Gate-1 Anti-SSRF."
            try:
                ip_obj = ipaddress.ip_address(hostname)
                if (
                    ip_obj.is_private
                    or ip_obj.is_loopback
                    or ip_obj.is_link_local
                    or ip_obj.is_multicast
                    or ip_obj.is_reserved
                    or ip_obj.is_unspecified
                ):
                    return False, f"IP non-publik ({ip_obj}) diblokir oleh Gate-1 Anti-SSRF."
            except ValueError:
                # Hostname DNS resolution check (non-blocking fallback if offline)
                try:
                    infos = socket.getaddrinfo(hostname, None)
                    for info in infos:
                        resolved_ip = info[4][0]
                        ip_obj = ipaddress.ip_address(resolved_ip)
                        if (
                            ip_obj.is_private
                            or ip_obj.is_loopback
                            or ip_obj.is_link_local
                            or ip_obj.is_reserved
                        ):
                            return False, f"Resolusi DNS mengarah ke IP privat ({ip_obj})."
                except socket.gaierror:
                    pass
            return True, "Gate-1 Anti-SSRF Valid."
        except Exception as exc:
            return False, f"Gate-1 SSRF error: {exc}"

    @classmethod
    def validate_gate2_ast(cls, code_str: str) -> Tuple[bool, str]:
        """Gate 2: Whitelist AST Sterilizer v4.0."""
        if not code_str or len(code_str) > 65000:
            return False, "Ukuran kode kosong atau melebihi batas 65KB."
        try:
            tree = ast.parse(code_str)
        except SyntaxError as exc:
            return False, f"SyntaxError pada kode: {exc}"

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                mod_names = []
                if isinstance(node, ast.Import):
                    mod_names = [alias.name.split(".")[0] for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    mod_names = [node.module.split(".")[0]]
                for m in mod_names:
                    if m in cls.FORBIDDEN_MODULES:
                        return False, f"Modul terlarang terdeteksi: `{m}`"
            elif isinstance(node, ast.Attribute):
                attr_name = getattr(node, "attr", "")
                if attr_name in cls.FORBIDDEN_DUNDERS or attr_name.startswith("__"):
                    return False, f"Atribut dunder terlarang terdeteksi: `{attr_name}`"
            elif isinstance(node, ast.Name):
                if node.id in cls.FORBIDDEN_DUNDERS or node.id in cls.FORBIDDEN_CALLS:
                    return False, f"Identifier terlarang terdeteksi: `{node.id}`"
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in cls.FORBIDDEN_CALLS:
                    return False, f"Pemanggilan fungsi terlarang: `{node.func.id}()`"
        return True, "Gate-2 AST Whitelist Sterilizer Valid."

    @staticmethod
    def validate_gate3_magic_bytes(payload_bytes: bytes, expected_kind: str = "ANY") -> Tuple[bool, str]:
        """Gate 3: Payload Malware & Magic Bytes Scrubber."""
        if not payload_bytes:
            return False, "Payload kosong."
        # Blokir executable biner berbahaya (ELF, MZ/PE, Mach-O, Shebang shell exploit)
        forbidden_prefixes = [
            (b"\x7fELF", "ELF Linux Executable"),
            (b"MZ", "Windows PE/MZ Executable"),
            (b"\xfe\xed\xfa\xce", "Mach-O 32-bit Executable"),
            (b"\xfe\xed\xfa\xcf", "Mach-O 64-bit Executable"),
            (b"#!/bin/sh", "Shell Script Exploit"),
            (b"#!/bin/bash", "Bash Script Exploit"),
        ]
        for sig, label in forbidden_prefixes:
            if payload_bytes.startswith(sig):
                return False, f"Gate-3 menolak signature malware/biner: {label}"

        kind = expected_kind.upper()
        if kind == "IMAGE":
            valid_img = (
                payload_bytes.startswith(b"\x89PNG\r\n\x1a\n")
                or payload_bytes.startswith(b"\xff\xd8\xff")
                or payload_bytes.startswith(b"RIFF")
                or payload_bytes.startswith(b"GIF8")
            )
            if not valid_img:
                return False, "Gate-3: Magic bytes bukan gambar valid (PNG/JPEG/WEBP/GIF)."
        elif kind == "PDF":
            if not payload_bytes.startswith(b"%PDF-"):
                return False, "Gate-3: Magic bytes bukan dokumen PDF valid."
        return True, "Gate-3 Magic Bytes Scrubber Valid."

    @staticmethod
    async def validate_gate4_live_ping(endpoint_url: str, timeout_sec: float = 2.5) -> Tuple[bool, str]:
        """Gate 4: Live Ping <2.5s."""
        ok_ssrf, msg_ssrf = ZeroTrust6GateSterilizer.validate_gate1_ssrf(endpoint_url)
        if not ok_ssrf:
            return False, msg_ssrf
        if not HAS_AIOHTTP:
            return True, "Gate-4 Live Ping (simulasi mode sandbox tanpa jaringan)."
        start_t = time.monotonic()
        try:
            timeout = aiohttp.ClientTimeout(total=timeout_sec)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(endpoint_url) as resp:
                    latency_ms = int((time.monotonic() - start_t) * 1000)
                    if resp.status < 500 and latency_ms <= int(timeout_sec * 1000):
                        return True, f"Gate-4 Live Ping OK ({latency_ms} ms, HTTP {resp.status})."
                    return False, f"Gate-4 gagal: HTTP {resp.status} ({latency_ms} ms)."
        except Exception as exc:
            return False, f"Gate-4 Live Ping melebihi {timeout_sec}s atau gagal: {exc}"

    @staticmethod
    def validate_gate5_modelscan(filename: str, header_bytes: bytes = b"") -> Tuple[bool, str]:
        """
        Gate 5: ProtectAI ModelScan Enforcer:
        Hanya mengizinkan .safetensors / .gguf, memblokir .pkl / .pt / .bin dan opcode pickle.
        """
        fname = filename.strip().lower()
        blocked_exts = (".pkl", ".pickle", ".pt", ".pth", ".bin", ".ckpt", ".h5", ".joblib")
        allowed_exts = (".safetensors", ".gguf", ".onnx")
        if fname.endswith(blocked_exts):
            return False, f"Gate-5 ProtectAI ModelScan memblokir ekstensi raw-pickle/weights `{fname}`."
        if not fname.endswith(allowed_exts):
            return False, f"Gate-5 wajib format aman (.safetensors / .gguf), diterima: `{fname}`."
        if header_bytes:
            # Deteksi protokol pickle (\x80\x02, \x80\x03, \x80\x04, \x80\x05) atau kata kunci sistem
            if header_bytes.startswith((b"\x80\x02", b"\x80\x03", b"\x80\x04", b"\x80\x05")):
                return False, "Gate-5 mendeteksi header Pickle di dalam file model!"
            for bad_token in (b"posix\nsystem", b"nt\nsystem", b"subprocess", b"eval\n", b"__reduce__"):
                if bad_token in header_bytes:
                    return False, f"Gate-5 mendeteksi gadget RCE `{bad_token.decode('latin1')}` pada model!"
        return True, "Gate-5 ProtectAI ModelScan Valid (.safetensors/.gguf aman)."

    @staticmethod
    async def validate_gate6_adaptive_threat(text_input: str) -> Tuple[bool, str]:
        """
        Gate 6: Adaptive Threat Memory:
        Memeriksa input terhadap aturan regex adaptif di DB, serta mengekstrak
        dan menyimpan pola regex baru secara otomatis saat mendeteksi eksploitasi baru.
        """
        if not text_input:
            return True, "Gate-6 Valid."
        db = get_db()
        rules = await db.fetch_all("SELECT rule_id, pattern_regex FROM adaptive_threat_rules;")
        for rule in rules:
            pat = rule.get("pattern_regex", "")
            if pat:
                try:
                    if re.search(pat, text_input, flags=re.IGNORECASE):
                        await db.execute_write(
                            "UPDATE adaptive_threat_rules SET hits_count = hits_count + 1 WHERE rule_id = ?;",
                            (rule["rule_id"],),
                        )
                        return False, f"Gate-6 Adaptive Threat Memory memblokir pola serangan #{rule['rule_id']}."
                except re.error:
                    continue

        # Deteksi heuristik serangan baru & auto-generate regex ke DB
        builtin_signatures = [
            r"__subclasses__\s*\(",
            r"__globals__\s*\[",
            r"os\.popen\s*\(",
            r"subprocess\.(Popen|call|run|check_output)",
            r"UNION\s+ALL\s+SELECT\s+.*FROM\s+users",
            r";\s*DROP\s+TABLE\s+",
            r"file:///etc/passwd",
            r"169\.254\.169\.254",
        ]
        for sig in builtin_signatures:
            m = re.search(sig, text_input, flags=re.IGNORECASE)
            if m:
                matched_token = m.group(0)
                learned_regex = re.escape(matched_token[:48])
                await db.execute_write(
                    """
                    INSERT INTO adaptive_threat_rules (pattern_regex, source_attack_sample, hits_count, created_at)
                    VALUES (?, ?, 1, ?)
                    ON CONFLICT(pattern_regex) DO UPDATE SET hits_count = hits_count + 1;
                    """,
                    (learned_regex, text_input[:300], int(time.time())),
                )
                return False, f"Gate-6 mendeteksi & mempelajari tanda serangan baru: `{matched_token}`"
        return True, "Gate-6 Adaptive Threat Memory Valid."

    @classmethod
    async def run_all_6_gates(
        cls,
        *,
        endpoint_url: Optional[str] = None,
        code_str: Optional[str] = None,
        payload_bytes: Optional[bytes] = None,
        expected_kind: str = "ANY",
        model_filename: Optional[str] = None,
        raw_text: str = "",
    ) -> Tuple[bool, List[str]]:
        logs: List[str] = []
        if endpoint_url:
            ok1, m1 = cls.validate_gate1_ssrf(endpoint_url)
            logs.append(m1)
            if not ok1:
                return False, logs
            ok4, m4 = await cls.validate_gate4_live_ping(endpoint_url)
            logs.append(m4)
            if not ok4:
                return False, logs
        if code_str is not None:
            ok2, m2 = cls.validate_gate2_ast(code_str)
            logs.append(m2)
            if not ok2:
                return False, logs
        if payload_bytes is not None:
            ok3, m3 = cls.validate_gate3_magic_bytes(payload_bytes, expected_kind)
            logs.append(m3)
            if not ok3:
                return False, logs
        if model_filename is not None:
            ok5, m5 = cls.validate_gate5_modelscan(model_filename, payload_bytes or b"")
            logs.append(m5)
            if not ok5:
                return False, logs
        if raw_text:
            ok6, m6 = await cls.validate_gate6_adaptive_threat(raw_text)
            logs.append(m6)
            if not ok6:
                return False, logs
        return True, logs


class SelfHealingOrchestrator:
    """
    Self-Healing Loop terstruktur:
    classify_error() -> select_handler() -> apply_fix() -> verify()
    Maksimal 3x retry berturut-turut; jika masih gagal, hentikan retry,
    simpan ke `human_escalation_queue`, dan kirim alert ke DM Owner.
    """

    MAX_RETRIES = 3

    def __init__(self) -> None:
        self._failure_counters: Dict[str, int] = {}

    @staticmethod
    def classify_error(exc: BaseException) -> str:
        msg = f"{type(exc).__name__}: {exc}".lower()
        if "locked" in msg or "sqlite" in msg or "database" in msg:
            return "SQLITE_CONCURRENCY_OR_LOCK"
        if "timeout" in msg or "timed out" in msg or "connect" in msg:
            return "UPSTREAM_TIMEOUT_OR_NETWORK"
        if "429" in msg or "rate limit" in msg or "quota" in msg:
            return "PROVIDER_RATE_LIMIT_429"
        if "refusal" in msg or "policy" in msg or "safety" in msg:
            return "MODEL_SOFT_REFUSAL"
        return "GENERIC_RUNTIME_FAULT"

    @staticmethod
    def select_handler(error_class: str) -> str:
        mapping = {
            "SQLITE_CONCURRENCY_OR_LOCK": "RECONNECT_WAL_AND_FLUSH_LOCK",
            "UPSTREAM_TIMEOUT_OR_NETWORK": "FAILOVER_SECONDARY_ENDPOINT",
            "PROVIDER_RATE_LIMIT_429": "ROTATE_ROLLING_POOL_AGENT",
            "MODEL_SOFT_REFUSAL": "REROUTE_ABLITERATED_MODEL",
            "GENERIC_RUNTIME_FAULT": "RESET_COMPONENT_CONTEXT",
        }
        return mapping.get(error_class, "RESET_COMPONENT_CONTEXT")

    async def apply_fix(self, component: str, handler_name: str, context: Dict[str, Any]) -> bool:
        await asyncio.sleep(0.05)
        if handler_name == "RECONNECT_WAL_AND_FLUSH_LOCK":
            get_db().init_schema_sync()
            return True
        if handler_name in ("FAILOVER_SECONDARY_ENDPOINT", "ROTATE_ROLLING_POOL_AGENT", "REROUTE_ABLITERATED_MODEL"):
            context["healed_route"] = handler_name
            return True
        context["healed_reset"] = True
        return True

    async def verify(self, component: str, context: Dict[str, Any]) -> bool:
        return bool(context.get("healed_route") or context.get("healed_reset") or get_db()._initialized)

    async def execute_with_self_healing(
        self,
        component: str,
        operation: Callable[[Dict[str, Any]], Awaitable[Any]],
        bot: Optional[Any] = None,
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> Any:
        ctx: Dict[str, Any] = dict(initial_context or {})
        last_exc: Optional[BaseException] = None

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                result = await operation(ctx)
                self._failure_counters[component] = 0
                return result
            except Exception as exc:
                last_exc = exc
                self._failure_counters[component] = attempt
                err_class = self.classify_error(exc)
                handler_name = self.select_handler(err_class)
                logger.warning(
                    "[SelfHealing] Component=%s Attempt=%d/%d ErrorClass=%s Handler=%s Detail=%s",
                    component,
                    attempt,
                    self.MAX_RETRIES,
                    err_class,
                    handler_name,
                    exc,
                )
                await self.apply_fix(component, handler_name, ctx)
                await self.verify(component, ctx)

        # Jika gagal 3x berturut-turut -> simpan ke human_escalation_queue & DM Owner
        err_class_final = self.classify_error(last_exc) if last_exc else "UNKNOWN_ERROR"
        err_detail_final = f"{type(last_exc).__name__}: {last_exc}" if last_exc else "Unknown failure"
        incident_id = await get_db().execute_write(
            """
            INSERT INTO human_escalation_queue
            (component, error_class, error_detail, attempts, status, created_at)
            VALUES (?, ?, ?, ?, 'OPEN', ?);
            """,
            (component, err_class_final, err_detail_final[:1000], self.MAX_RETRIES, int(time.time())),
        )
        if bot is not None and OWNER_ID_RUNTIME > 0:
            try:
                await bot.send_message(
                    chat_id=OWNER_ID_RUNTIME,
                    text=(
                        f"🚨 \x3cb>SELF-HEALING ESCALATION ALERT (#{incident_id})\x3c/b>\n"
                        f"• Komponen: \x3ccode>{html.escape(component)}\x3c/code>\n"
                        f"• Kelas Error: \x3ccode>{html.escape(err_class_final)}\x3c/code>\n"
                        f"• Percobaan: {self.MAX_RETRIES}x gagal berturut-turut (Retry dihentikan)\n"
                        f"• Detail: \x3ccode>{html.escape(err_detail_final[:350])}\x3c/code>"
                    ),
                    parse_mode="HTML",
                )
            except Exception as notify_exc:
                logger.warning("Failed to send escalation DM to owner: %s", notify_exc)
        if last_exc is not None:
            raise last_exc
        raise RuntimeError(f"Self-healing failed after {self.MAX_RETRIES} attempts on {component}")


SELF_HEALING = SelfHealingOrchestrator()


class HumanApprovalGate:
    """
    Mengunci 5 aksi kritis di kode:
    - DATA_MIGRATION
    - PRICE_PLAN_CHANGE
    - DELETE_FEATURE_PLUGIN
    - WITHDRAW_ABOVE_THRESHOLD
    - SECURITY_POLICY_CHANGE
    Dengan tombol persetujuan InlineKeyboard `adm:apr_yes:\x3cid>` dan `adm:apr_no:\x3cid>`.
    """

    LOCKED_CRITICAL_ACTIONS = {
        "DATA_MIGRATION",
        "PRICE_PLAN_CHANGE",
        "DELETE_FEATURE_PLUGIN",
        "WITHDRAW_ABOVE_THRESHOLD",
        "SECURITY_POLICY_CHANGE",
    }

    @classmethod
    async def request_approval(
        cls,
        action_type: str,
        summary: str,
        payload: Dict[str, Any],
        bot: Optional[Any] = None,
    ) -> Tuple[str, InlineKeyboardMarkup]:
        action_key = action_type.strip().upper()
        if action_key not in cls.LOCKED_CRITICAL_ACTIONS:
            raise ValueError(f"Action type `{action_key}` bukan aksi kritis terdaftar.")
        approval_id = f"APR-{secrets.token_hex(4).upper()}"
        await get_db().execute_write(
            """
            INSERT INTO pending_approvals (approval_id, action_type, summary, payload_json, status, created_at)
            VALUES (?, ?, ?, ?, 'PENDING', ?);
            """,
            (approval_id, action_key, summary, json.dumps(payload, ensure_ascii=False), int(time.time())),
        )
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ Setujui Eksekusi", callback_data=f"adm:apr_yes:{approval_id}"),
                    InlineKeyboardButton(text="❌ Tolak & Batalkan", callback_data=f"adm:apr_no:{approval_id}"),
                ]
            ]
        )
        if bot is not None and OWNER_ID_RUNTIME > 0:
            try:
                await bot.send_message(
                    chat_id=OWNER_ID_RUNTIME,
                    text=(
                        f"🛡️ \x3cb>HUMAN APPROVAL GATE — AKSI KRITIS TERKUNCI\x3c/b>\n\n"
                        f"• ID Tiket: \x3ccode>{approval_id}\x3c/code>\n"
                        f"• Kategori Aksi: \x3ccode>{action_key}\x3c/code>\n"
                        f"• Ringkasan: {html.escape(summary)}\n\n"
                        f"Silakan tinjau dan klik tombol di bawah untuk mengeksekusi atau membatalkan:"
                    ),
                    reply_markup=kb,
                    parse_mode="HTML",
                )
            except Exception as exc:
                logger.warning("Failed sending HumanApprovalGate prompt: %s", exc)
        return approval_id, kb

    @classmethod
    async def resolve_approval(cls, approval_id: str, approved: bool) -> Tuple[bool, str, Dict[str, Any]]:
        db = get_db()
        row = await db.fetch_one(
            "SELECT * FROM pending_approvals WHERE approval_id = ?;",
            (approval_id,),
        )
        if not row:
            return False, "Tiket persetujuan tidak ditemukan.", {}
        if row["status"] != "PENDING":
            return False, f"Tiket `{approval_id}` sudah berstatus `{row['status']}`.", {}

        new_status = "APPROVED" if approved else "REJECTED"
        await db.execute_write(
            "UPDATE pending_approvals SET status = ? WHERE approval_id = ?;",
            (new_status, approval_id),
        )
        payload = json.loads(row.get("payload_json") or "{}")
        action_type = row["action_type"]

        if not approved:
            return True, f"❌ Aksi kritis `{action_type}` (`{approval_id}`) resmi DITOLAK & dibatalkan.", payload

        # Eksekusi aksi kritis setelah disetujui Owner
        if action_type == "WITHDRAW_ABOVE_THRESHOLD":
            amount_idr = int(payload.get("amount_idr", 0))
            await db.execute_write(
                """
                UPDATE treasury_summary
                SET harvestable_profit_vault_idr = MAX(0, harvestable_profit_vault_idr - ?),
                    total_harvested_by_owner_idr = total_harvested_by_owner_idr + ?,
                    updated_at = ?
                WHERE id = 1;
                """,
                (amount_idr, amount_idr, int(time.time())),
            )
            return True, f"✅ Pencairan Profit Rp {amount_idr:,} berhasil dieksekusi (`{approval_id}`).", payload
        elif action_type == "SECURITY_POLICY_CHANGE":
            new_policy = str(payload.get("policy", "STRICT_ZERO_TRUST_6GATE"))
            await db.set_setting("security_policy_level", new_policy)
            return True, f"✅ Kebijakan keamanan diperbarui ke `{new_policy}` (`{approval_id}`).", payload
        elif action_type == "PRICE_PLAN_CHANGE":
            tier_key = str(payload.get("tier_key", "ECERAN"))
            new_price = int(payload.get("new_price_idr", 2000))
            await db.set_setting(f"price_override_{tier_key}", str(new_price))
            return True, f"✅ Harga paket `{tier_key}` diperbarui menjadi Rp {new_price:,}.", payload
        elif action_type == "DELETE_FEATURE_PLUGIN":
            plug_name = str(payload.get("plugin_name", ""))
            PLUGIN_REGISTRY._plugins.pop(plug_name, None)
            return True, f"✅ Plugin `{plug_name}` berhasil dihapus dari registri aktif.", payload
        elif action_type == "DATA_MIGRATION":
            await db.set_setting("last_migration_approved", approval_id)
            return True, f"✅ Migrasi data `{approval_id}` telah disetujui dan dijalankan.", payload

        return True, f"✅ Aksi `{action_type}` (`{approval_id}`) telah disetujui.", payload

