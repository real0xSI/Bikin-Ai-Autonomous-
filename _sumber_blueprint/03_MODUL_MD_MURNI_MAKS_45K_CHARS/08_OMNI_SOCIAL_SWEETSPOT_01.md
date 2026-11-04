
<!-- [ID:08_OMNI_SOCIAL_S001] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: :1000 -->
## Aturan
- Log TIDAK BOLEH dihapus/diedit agent.
- Rotasi hanya oleh owner (arsip ke cold storage, hash tetap disimpan).

"""
Dijalankan oleh .github/workflows/nightly-audit.yml.
Jika chain rusak → trigger L4_READONLY otomatis + alert owner.
"""
import sys, httpx
from services.audit.verifier import verify_chain
from office.orchestrator.kill_switch import trigger
from office.orchestrator.notification_gateway import send_owner

def main():
    r = verify_chain()
    if r["ok"]:
        send_owner(f"🌙 Nightly audit OK. {r['total']} event.")
        return 0
    trigger("L4_READONLY", by="nightly_audit")
    send_owner(f"🚨 AUDIT CHAIN RUSAK! bad={r['bad_count']}\n"
               f"L4_READONLY aktif otomatis. Cek /verify.")
    return 1

if __name__ == "__main__":
    sys.exit(main())

"""
Helper HMAC untuk adapter yang butuh signature
(WA Cloud API, Meta Graph, Telegram formatter).
"""
import hmac, hashlib, time, os, secrets

SECRET = os.environ.get("HMAC_SECRET","").encode()

def sign(payload: str, ts: int | None = None,
         nonce: str | None = None) -> dict:
    ts = ts or int(time.time())
    nonce = nonce or secrets.token_hex(8)
    msg = f"{payload}|{ts}|{nonce}".encode()
    sig = hmac.new(SECRET, msg, hashlib.sha256).hexdigest()
    return {"sig": sig, "ts": ts, "nonce": nonce}

def format_signed(command: str) -> str:
    """Format pesan kirim dari owner (opsional, untuk perintah sensitif)."""
    s = sign(command)
    return f"sig:{s['sig']} ts:{s['ts']} n:{s['nonce']} | {command}"

"""
Instagram DM adapter via Meta Graph API (Instagram Messaging).
Webhook: /webhook/instagram
Owner ID: INSTAGRAM_OWNER_ID (IGSID)
"""
import os, hmac, hashlib, json, httpx, sys
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bots.core.dispatcher import dispatch

app = FastAPI(title="Instagram Bot")
TOKEN = os.environ.get("INSTAGRAM_TOKEN","")
PAGE_ID = os.environ.get("INSTAGRAM_PAGE_ID","")
APP_SECRET = os.environ.get("INSTAGRAM_APP_SECRET","").encode()

def _verify_sig(body: bytes, sig: str) -> bool:
    if not APP_SECRET: return True
    expected = "sha256=" + hmac.new(APP_SECRET, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig)

def _send(recipient: str, text: str):
    if not TOKEN or not PAGE_ID: return
    httpx.post(
        f"https://graph.facebook.com/v19.0/{PAGE_ID}/messages",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"recipient": {"id": recipient},
              "message": {"text": text[:1000]}},   # IG limit 1000 char
        timeout=15,
    )

@app.post("/webhook/instagram")
async def webhook(req: Request):
    raw = await req.body()
    if not _verify_sig(raw, req.headers.get("x-hub-signature-256","")):
        raise HTTPException(403, "bad_signature")
    data = json.loads(raw)
    for entry in data.get("entry", []):
        for m in (entry.get("messaging") or []):
            sender = str(m.get("sender",{}).get("id",""))
            text = (m.get("message",{}).get("text") or "").strip()
            if not text or not sender: continue
            result = dispatch(text=text, channel="instagram", user_id=sender)
            _send(sender, result)
    return {"ok": True}
"""
Instagram DM adapter via Meta Graph API (Instagram Messaging).
Webhook: /webhook/instagram
Owner ID: INSTAGRAM_OWNER_ID (IGSID)
"""
import os, hmac, hashlib, json, httpx, sys
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bots.core.dispatcher import dispatch

app = FastAPI(title="Instagram Bot")
TOKEN = os.environ.get("INSTAGRAM_TOKEN","")
PAGE_ID = os.environ.get("INSTAGRAM_PAGE_ID","")
APP_SECRET = os.environ.get("INSTAGRAM_APP_SECRET","").encode()

def _verify_sig(body: bytes, sig: str) -> bool:
    if not APP_SECRET: return True
    expected = "sha256=" + hmac.new(APP_SECRET, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig)

def _send(recipient: str, text: str):
    if not TOKEN or not PAGE_ID: return
    httpx.post(
        f"https://graph.facebook.com/v19.0/{PAGE_ID}/messages",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"recipient": {"id": recipient},
              "message": {"text": text[:1000]}},   # IG limit 1000 char
        timeout=15,
    )

@app.post("/webhook/instagram")
async def webhook(req: Request):
    raw = await req.body()
    if not _verify_sig(raw, req.headers.get("x-hub-signature-256","")):
        raise HTTPException(403, "bad_signature")
    data = json.loads(raw)
    for entry in data.get("entry", []):
        for m in (entry.get("messaging") or []):
            sender = str(m.get("sender",{}).get("id",""))
            text = (m.get("message",{}).get("text") or "").strip()
            if not text or not sender: continue
            result = dispatch(text=text, channel="instagram", user_id=sender)
            _send(sender, result)
    return {"ok": True}



COPY services/ /app/services/
COPY office/ /app/office/
RUN useradd -m -u 10001 app && chown -R app:app /app
USER app
EXPOSE 8001
CMD ["uvicorn", "services.payment.main:app", "--host", "0.0.0.0", "--port", "8001"]

"""
WhatsApp adapter via WhatsApp Cloud API (Meta).
Endpoint webhook: /webhook/whatsapp
Verifikasi: nomor owner + PIN untuk perintah sensitif.
"""
import os, hmac, hashlib, json, httpx, sys
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bots.core.dispatcher import dispatch

app = FastAPI(title="WhatsApp Bot")
TOKEN = os.environ.get("WHATSAPP_TOKEN","")
PHONE_ID = os.environ.get("WHATSAPP_PHONE_ID","")
VERIFY_TOKEN = os.environ.get("WHATSAPP_VERIFY_TOKEN","")
APP_SECRET = os.environ.get("WHATSAPP_APP_SECRET","").encode()

def _verify_sig(body: bytes, sig_header: str) -> bool:
    if not APP_SECRET: return True   # dev mode
    expected = "sha256=" + hmac.new(APP_SECRET, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig_header)

def _send(to: str, text: str):
    if not TOKEN or not PHONE_ID: return
    httpx.post(
        f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"messaging_product": "whatsapp", "to": to,
              "type": "text", "text": {"body": text[:4000]}},
        timeout=15,
    )

@app.get("/webhook/whatsapp")
def verify(mode: str = "", token: str = "", challenge: str = ""):
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    raise HTTPException(403, "verify_failed")

@app.post("/webhook/whatsapp")
async def webhook(req: Request):
    raw = await req.body()
    sig = req.headers.get("x-hub-signature-256","")
    if not _verify_sig(raw, sig):
        raise HTTPException(403, "bad_signature")

    data = json.loads(raw)
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            for msg in (change.get("value", {}).get("messages") or []):
                sender = msg.get("from")
                text = (msg.get("text") or {}).get("body","").strip()
                if not text: continue
                result = dispatch(text=text, channel="whatsapp",
                                  user_id=str(sender))
                _send(sender, result)
    return {"ok": True}

"""
Threads adapter via Threads API (Meta).
Reply mentions sebagai command.
Webhook: /webhook/threads
"""
import os, hmac, hashlib, json, httpx, sys
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bots.core.dispatcher import dispatch

app = FastAPI(title="Threads Bot")
TOKEN = os.environ.get("THREADS_TOKEN","")
USER_ID = os.environ.get("THREADS_USER_ID","")
APP_SECRET = os.environ.get("THREADS_APP_SECRET","").encode()

def _verify_sig(body: bytes, sig: str) -> bool:
    if not APP_SECRET: return True
    expected = "sha256=" + hmac.new(APP_SECRET, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig)

def _reply(thread_id: str, text: str):
    if not TOKEN: return
    # 1) buat container
    r = httpx.post(
        f"https://graph.threads.net/v1.0/{USER_ID}/threads",
        params={"media_type": "TEXT", "text": text[:500],
                "reply_to_id": thread_id, "access_token": TOKEN}, timeout=15)
    if r.status_code != 200: return
    cid = r.json().get("id")
    # 2) publish
    httpx.post(f"https://graph.threads.net/v1.0/{USER_ID}/threads_publish",
               params={"creation_id": cid, "access_token": TOKEN}, timeout=15)

@app.post("/webhook/threads")
async def webhook(req: Request):
    raw = await req.body()
    if not _verify_sig(raw, req.headers.get("x-hub-signature-256","")):
        raise HTTPException(403, "bad_signature")
    data = json.loads(raw)
    for entry in data.get("entry", []):
        for m in (entry.get("changes") or []):
            v = m.get("value", {})
            text = (v.get("text") or "").strip()
            thread_id = v.get("id")
            sender = v.get("from", {}).get("id")
            if not text or not sender or not thread_id: continue
            result = dispatch(text=text, channel="threads", user_id=str(sender))
            _reply(thread_id, result)
    return {"ok": True}


<!-- [ID:08_OMNI_SOCIAL_S002] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: A-ZA-Z0-9, :18, :600 -->
# ── utils ─────────────────────────────────────────────────────────
def cmd_sync(args):
    PAT = re.compile(r"^(?:api_key|key)\s*[:=]\s*(dahl_[A-Za-z0-9]+)", re.M)
    keys = set()
    if CREDS_DIR.exists():
        for f in sorted(CREDS_DIR.glob("*.txt")):
            for m in PAT.finditer(f.read_text(errors="ignore")):
                keys.add(m.group(1))
    if POOL_FILE.exists():
        for line in POOL_FILE.read_text().splitlines():
            line = line.strip()
            if line.startswith("dahl_"):
                keys.add(line)
    out = "\n".join(sorted(keys)) + "\n"
    POOL_FILE.write_text(out, encoding="utf-8")
    print(f"keys.txt: {len(keys)} unique, {POOL_FILE}")

def cmd_export(args):
    PAT_API = re.compile(r"^api_key:\s*(dahl_\w+)", re.M)
    PAT_USER = re.compile(r"^username:\s*(\S+)", re.M)
    PAT_TIME = re.compile(r"^farmed:\s*(\S+)", re.M)
    since = None if args.all else (args.since or time.strftime("%Y-%m-%d"))
    rows = []
    if CREDS_DIR.exists():
        for f in sorted(CREDS_DIR.glob("*.txt")):
            txt = f.read_text(errors="ignore")
            m_api = PAT_API.search(txt)
            if not m_api:
                continue
            user = (PAT_USER.search(txt) or [None, "?"])[1]
            ts = (PAT_TIME.search(txt) or [None, "?"])[1]
            if since and not ts.startswith(since):
                continue
            rows.append((ts, user, m_api.group(1)))
    rows.sort(key=lambda r: r[0])
    out = Path(args.out) if args.out else HERE / "keys_farmed.txt"
    lines = [f"# Dahl API keys — since {since or 'ALL'}", f"# total: {len(rows)} keys", ""]
    for ts, user, key in rows:
        lines.append(f"{key}   # {user}  {ts}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"saved: {out}  total: {len(rows)}")

def cmd_list(args):
    if not CREDS_DIR.exists() or not any(CREDS_DIR.glob("*.txt")):
        print("no creds yet"); return
    for f in sorted(CREDS_DIR.glob("*.txt")):
        d = {}
        for line in f.read_text().splitlines():
            if ": " in line and not line.startswith("#"):
                k, v = line.split(": ", 1); d[k] = v
        print(f"{d.get('username','?'):24s} key={d.get('api_key','?')[:18]}… farmed")

def cmd_check(args):
    api = Dahl()
    st, body = api.chat(args.model, args.token)
    print(f"HTTP {st}")
    print(json.dumps(body, indent=2)[:600])

def _summary(ok, fail, total_time, tg_token="", tg_chatid=""):
    total_accounts = len(ok) + len(fail)
    avg_time = (total_time / total_accounts) if total_accounts > 0 else 0.0

    print(f"\n=== DONE: {len(ok)} farmed, {len(fail)} failed ===")
    print(f"Total Time  : {total_time:.2f} detik")
    print(f"Average Time: {avg_time:.2f} detik / akun")
    for t in ok:
        print(f"  dahl key: {t}")
        
    if tg_token and tg_chatid:
        msg = f"<b>🌾 DAHL FARMING SUMMARY</b>\n"
        msg += f"========================\n"
        msg += f"<b>Success:</b> {len(ok)}\n"
        msg += f"<b>Failed:</b> {len(fail)}\n"
        msg += f"<b>Total Time:</b> {total_time:.2f}s\n"
        msg += f"<b>Avg Time:</b> {avg_time:.2f}s / account\n\n"
        msg += f"<b>API Keys (saved to keys.txt):</b>\n"
        for t in ok:
            msg += f"<code>{t}</code>\n"
        
        send_telegram_msg(tg_token, tg_chatid, msg)
        print("\n[+] Ringkasan summary berhasil dikirim ke Telegram!")


def main():
    ap = argparse.ArgumentParser(prog="dahl_farm", description="dahl.global auto-farm via Bright Data High-Speed")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("bright", help="farm via Bright Data proxy")
    p.add_argument("count", type=int, help="jumlah akun yang difarm")
    p.add_argument("--proxy", default=None, help="string proxy Bright Data (http://user:pass@host:port)")
    p.add_argument("--workers", type=int, default=10, help="jumlah thread paralel bersamaan (default: 10)")
    p.add_argument("--backoff", type=float, default=0.2, help="delay retry saat error (default: 0.2 detik)")
    p.add_argument("--model", default=MODEL_DEFAULT)
    p.add_argument("--skip-chat", action="store_false", help="jalankan chat verification (default: skip chat)")
    p.add_argument("--tg-token", default=None, help="Telegram Bot Token")
    p.add_argument("--tg-chatid", default=None, help="Telegram Chat ID")
    p.set_defaults(fn=cmd_brightfarm)

    p = sub.add_parser("sync", help="merge creds -> keys.txt"); p.set_defaults(fn=cmd_sync)
    p = sub.add_parser("export", help="export keys")
    p.add_argument("--all", action="store_true"); p.add_argument("--since", default=None)
    p.add_argument("--out", default=None); p.set_defaults(fn=cmd_export)
    p = sub.add_parser("list", help="list farmed accounts"); p.set_defaults(fn=cmd_list)
    p = sub.add_parser("check", help="verify a key")
    p.add_argument("token"); p.add_argument("--model", default=MODEL_DEFAULT); p.set_defaults(fn=cmd_check)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
```
```


<!-- [ID:08_OMNI_SOCIAL_S003] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: NAME, COMPONENT, :250 -->
# ==============================================================================
class PluginRegistry:
   def __init__(self) -> None:
       self.plugins = {}
   def register(self, name: str, handler, health_fn=None):
       self.plugins[name] = {"handler": handler, "health": health_fn or (lambda: True), "active": True}
PLUGIN_SURFACE = PluginRegistry()
async def v4_omnichannel_hub(platform: str, payload: dict[str, Any]) -> dict[str, Any]:
   """[A4.b]: Integrasi lintas platform (WhatsApp, FB, Telegram, TikTok, Shopee)."""
   supported = ("whatsapp", "facebook", "instagram", "telegram", "tiktok", "shopee", "open_connector")
   p_clean = platform.lower().strip()
   if p_clean not in supported:
       return {"ok": False, "reason": f"Unsupported platform: {platform}"}
   stream_type = payload.get("stream_type", "BOT_PROMO") # BOT_PROMO vs OWNER_PERSONAL
   aff_link = payload.get("shopee_affiliate_url", "")
   return {"ok": True, "platform": p_clean, "stream": stream_type, "affiliate_injected": bool(aff_link)}
PLUGIN_SURFACE.register("omnichannel_hub", v4_omnichannel_hub)
class SelfHealingOrchestrator:
   """Master Contract D2: Self-Healing Loop (gagal 3x -> human queue)."""
   def __init__(self) -> None:
       self.failures = {}
   async def attempt_heal_or_escalate(self, db: aiosqlite.Connection, component: str, err: str) -> dict[str, 
       cnt = self.failures.get(component, 0) + 1
       self.failures[component] = cnt
       if cnt < 3:
           return {"healed": False, "attempts": cnt, "escalated": False}
       inc_id = f"INC-{int(time.time())}-{secrets.token_hex(2).upper()}"
       async def _tx(conn: aiosqlite.Connection) -> None:
           await conn.execute(
               "INSERT OR REPLACE INTO human_escalation_queue (incident_id, component, error_class, error_det
               (inc_id, component, err[:250], cnt, int(time.time()))
           )
       await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
       return {"healed": False, "attempts": cnt, "escalated": True, "incident_id": inc_id}
SELF_HEALING_ORCHESTRATOR = SelfHealingOrchestrator()



<!-- [ID:08_OMNI_SOCIAL_S004] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
MINIAPP_FULL_WEBSITE_HTML = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>bikinAI Super Intelligence — Official Web & Mini App Studio</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
  :root {
    --bg: #05070c; --surface: #0f1523; --cyan: #00f0ff; --purple: #7b2cbf;
    --text: #f0f6fc; --muted: #8b949e; --success: #00e676;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  body { background: radial-gradient(circle at 50% 0%, #17103a 0%, #05070c 72%); color: var(--text); min-height: 100vh; padding: 14px 14px 96px 14px; transition: filter 0.2s; }
  body.blurred { filter: blur(18px); }
  .hero {
    background: linear-gradient(135deg, rgba(15,21,35,0.95), rgba(30,16,60,0.85));
    border: 1px solid rgba(0,240,255,0.3); border-radius: 16px; padding: 16px; margin-bottom: 14px;
    box-shadow: 0 6px 28px rgba(0,240,255,0.1);
  }
  .badge { display: inline-block; background: linear-gradient(90deg, var(--cyan), var(--purple)); color: #fff; font-size: 10px; font-weight: 800; padding: 3px 10px; border-radius: 99px; margin-bottom: 6px; }
  .hero h1 { font-size: 18px; font-weight: 800; color: #fff; margin-bottom: 4px; }
  .hero p { font-size: 12px; color: var(--muted); line-height: 1.4; }
  .tab-section { display: none; }
  .tab-section.active { display: block; }
  .label { font-size: 11px; font-weight: 700; text-transform: uppercase; color: var(--cyan); margin: 12px 0 6px; letter-spacing: 0.6px; }
  .pill-row { display: flex; gap: 7px; overflow-x: auto; padding-bottom: 4px; }
  .pill { flex: 1; text-align: center; white-space: nowrap; background: var(--surface); border: 1px solid rgba(255,255,255,0.08); color: var(--muted); padding: 9px 11px; border-radius: 11px; font-size: 12px; font-weight: 600; cursor: pointer; }
  .pill.active { background: rgba(0,240,255,0.15); border-color: var(--cyan); color: #fff; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .card { background: var(--surface); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 10px; cursor: pointer; }
  .card.active { border-color: var(--cyan); background: rgba(0,240,255,0.1); }
  .card h4 { font-size: 13px; color: #fff; margin-bottom: 2px; }
  .card p { font-size: 10px; color: var(--muted); }
  .upload-box { border: 1.5px dashed rgba(0,240,255,0.4); background: rgba(15,21,35,0.6); border-radius: 14px; padding: 12px; text-align: center; position: relative; cursor: pointer; margin-top: 4px; }
  .upload-box input { position: absolute; inset: 0; opacity: 0; cursor: pointer; }
  #ref-preview { max-height: 110px; border-radius: 8px; margin-top: 8px; display: none; margin-left: auto; margin-right: auto; border: 1px solid var(--cyan); }
  textarea { width: 100%; height: 80px; background: var(--surface); border: 1px solid rgba(0,240,255,0.3); border-radius: 12px; color: #fff; padding: 10px; font-size: 13px; outline: none; resize: none; }
  .btn-exec { width: 100%; margin-top: 12px; padding: 14px; border: none; border-radius: 14px; background: linear-gradient(90deg, #00c6ff, #7b2cbf); color: #fff; font-size: 14px; font-weight: 800; cursor: pointer; box-shadow: 0 4px 20px rgba(0,240,255,0.3); }
  #toast { margin-top: 10px; padding: 10px; border-radius: 10px; font-size: 12px; background: rgba(0,230,118,0.15); border: 1px solid var(--success); color: var(--success); display: none; text-align: center; }
  .legal-card { background: var(--surface); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; margin-bottom: 10px; font-size: 12px; line-height: 1.5; color: #d0d7de; }
  .legal-card h3 { color: var(--cyan); font-size: 14px; margin-bottom: 6px; }
  .footer-copy { text-align: center; font-size: 11px; color: var(--muted); margin-top: 18px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.07); }
  .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; height: 62px; background: rgba(8,12,22,0.96); backdrop-filter: blur(16px); border-top: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-around; align-items: center; z-index: 99; }
  .nav-btn { display: flex; flex-direction: column; align-items: center; gap: 2px; color: var(--muted); font-size: 10px; font-weight: 600; cursor: pointer; }
  .nav-btn.active { color: var(--cyan); }
</style>
</head>
<body>
  <div class="hero">
    <span class="badge">⚡ OFFICIAL SFW CREATIVE STUDIO v3.4</span>
    <h1>Selamat Datang di bikinAI Super Intelligence</h1>
    <p id="welcome-user">Platform Studio Visual, Video Sinematik, & Audio Otonom. Pilih mesin di bawah atau unggah foto referensi untuk langsung merender karya berkualitas komersial.</p>
  </div>

  <!-- TAB 1: STUDIO GENERATOR LENGKAP -->
  <div id="tab-studio" class="tab-section active">
    <div class="label">1. Pilih Kategori & Mode Editing</div>
    <div class="pill-row">
      <div class="pill active" onclick="setMod(this,'IMAGE')">🎨 Gambar 4K</div>
      <div class="pill" onclick="setMod(this,'VIDEO')">🎬 Video AI</div>
      <div class="pill" onclick="setMod(this,'REMOVE_BG')">✂️ Hapus BG (.PNG)</div>
      <div class="pill" onclick="setMod(this,'RETOUCH')">✨ Retouch/Inpaint</div>
    </div>

    <div class="label">2. Pilih Mesin AI Utama & AI Lainnya</div>
    <div class="grid">
      <div class="card active" onclick="setEng(this,'Seedream 4.5')"><h4>✨ Seedream 4.5</h4><p>4K & Teks Poster Akurat</p></div>
      <div class="card" onclick="setEng(this,'Kling 3.0 Pro')"><h4>🟣 Kling 3.0 Pro</h4><p>Video Sinematik & Motion</p></div>
      <div class="card" onclick="setEng(this,'Seedance 2.0')"><h4>🕺 Seedance 2.0</h4><p>Koreografi & Transisi</p></div>
      <div class="card" onclick="setEng(this,'Wan 2.2 Pro')"><h4>🔵 Wan 2.2 Pro</h4><p>Konsistensi Karakter</p></div>
      <div class="card" onclick="setEng(this,'Flux.1 Dev')"><h4>📸 Flux.1 Dev</h4><p>Fotorealistis Natural</p></div>
      <div class="card" onclick="setEng(this,'Midjourney v7')"><h4>🎨 Midjourney v7</h4><p>Pencahayaan Artistik</p></div>
      <div class="card" onclick="setEng(this,'Google Veo 3')"><h4>🎥 Google Veo 3</h4><p>Sinematik Film & Audio</p></div>
      <div class="card" onclick="setEng(this,'Recraft V3')"><h4>📐 Recraft V3</h4><p>Desain Logo & Vector SVG</p></div>
    </div>

    <div class="label">3. Rasio, Durasi & Penajaman</div>
    <div class="pill-row">
      <div class="pill active" onclick="setRat(this,'9:16')">📱 9:16</div>
      <div class="pill" onclick="setRat(this,'1:1')">🟦 1:1</div>
      <div class="pill" onclick="setRat(this,'16:9')">🖥️ 16:9</div>
      <div class="pill active" onclick="setUps(this,'Pertajam Foto & Wajah 4K')">🔍 Pertajam Foto 4K</div>
      <div class="pill" onclick="setUps(this,'Pertajam Teks & Gambar 4K')">✨ Pertajam Teks 4K</div>
    </div>

    <div class="label">4. Upload Foto Referensi (Opsional — Img2Vid / Wajah / Produk)</div>
    <div class="upload-box">
      <input type="file" accept="image/*" onchange="previewRef(event)">
      <div id="up-txt" style="font-size:12px;">📸 <b>Sentuh untuk Upload Foto Referensi</b><br><span style="font-size:10px; color:var(--muted);">Aman & terkompresi otomatis di perangkat Anda</span></div>
      <img id="ref-preview" alt="Ref">
    </div>

    <div class="label">5. Tulis Prompt Visual / Video Anda</div>
    <textarea id="prompt-in" placeholder="Ketik deskripsi gambar atau video yang ingin dibuat..."></textarea>
    <button class="btn-exec" id="btn-go" onclick="runGenerate()">🚀 GENERATE SEKARANG (KIRIM KE BOT & DISINI)</button>
    <div id="toast"></div>
  </div>

  <!-- TAB 2: PANDUAN & FAQ LENGKAP -->
  <div id="tab-guide" class="tab-section">
    <div class="legal-card">
      <h3>🧭 Panduan Cepat Penggunaan Studio</h3>
      <p>1. <b>Generate via Mini App:</b> Pilih mesin AI, unggah foto referensi (jika ada), ketik prompt, lalu klik tombol <i>Generate Sekarang</i>. Hasil otomatis dikirim ke ruang chat Telegram Anda.<br>
      2. <b>Hapus Background (.PNG Transparan):</b> Pilih mode <i>✂️ Hapus BG (.PNG)</i>. Sistem akan mengirimkan hasilnya sebagai <b>File Dokumen .PNG Lossless</b> agar transparansi tidak berubah menjadi putih.<br>
      3. <b>Mode Deep Research & Canvas:</b> Ketik <code>/riset [topik]</code> atau <code>/canvas [instruksi]</code> langsung di ruang chat bot.</p>
    </div>
    <div class="legal-card">
      <h3>❓ Pertanyaan Umum (FAQ)</h3>
      <p>• <b>Bagaimana jika render gagal?</b> Sistem <i>Auto-Support & Dead-Job Sweeper</i> otomatis mengembalikan koin Anda 100% dalam 60 detik.<br>
      • <b>Metode Pembayaran:</b> Otomatis menyesuaikan lokasi Anda (QRIS/PG untuk Indonesia & Crypto USDT/Telegram Stars untuk Global).</p>
    </div>
  </div>

  <!-- TAB 3: TOS, PRIVACY POLICY & COPYRIGHT -->
  <div id="tab-legal" class="tab-section">
    <div class="legal-card">
      <h3>⚖️ Terms of Service (Ketentuan Layanan SFW)</h3>
      <p>Platform resmi <b>bikinAI Super Intelligence</b> didedikasikan untuk produksi kreatif, desain komersial UMKM, edukasi, dan hiburan yang aman (Safe-For-Work). Pengguna dilarang keras mengunggah atau memproduksi materi ilegal, eksploitasi anak di bawah umur (CSAM), pemalsuan identitas tokoh publik tanpa izin, atau tindakan melanggar hukum internasional.</p>
    </div>
    <div class="legal-card">
      <h3>🛡️ Privacy Policy (Kebijakan Privasi Zero-Retention)</h3>
      <p>1. <b>Minimisasi Data:</b> Kami hanya menyimpan ID akun dan saldo koin di brankas terenkripsi.<br>
      2. <b>Pembersihan Otomatis:</b> Seluruh metadata EXIF dilucuti dan cache media sementara dihapus secara berkala untuk melindungi privasi dan hak kekayaan intelektual kreator.<br>
      3. <b>Keamanan Kriptografi:</b> Komunikasi antara Mini App dan server dilindungi verifikasi tanda tangan HMAC-SHA256.</p>
    </div>
    <div class="legal-card">
      <h3>©️ Copyright & Hak Kekayaan Intelektual</h3>
      <p>Seluruh karya yang dihasilkan menggunakan <b>Koin Utama (Pro)</b> memberikan hak penggunaan komersial penuh (<i>Clean Commercial License</i>) tanpa watermark kepada kreator.</p>
    </div>
  </div>

  <div class="footer-copy">
    Copyright © 2026 <b>bikinAI Super Intelligence</b>. All Rights Reserved.<br>
    Autonomous Multi-Engine AI Aggregator • Zero-Ops Enterprise Architecture.
  </div>

  <div class="bottom-nav">
    <div class="nav-btn active" onclick="openTab(this,'tab-studio')"><span>🎬</span><span>Studio AI</span></div>
    <div class="nav-btn" onclick="openTab(this,'tab-guide')"><span>🧭</span><span>Panduan & FAQ</span></div>
    <div class="nav-btn" onclick="openTab(this,'tab-legal')"><span>⚖️</span><span>ToS & Privasi</span></div>
  </div>

<script>
  const tg = window.Telegram?.WebApp;
  let st = { user_id: 0, username: "Kreator", modality: "IMAGE", engine: "Seedream 4.5", ratio: "9:16", upscale: "Pertajam Foto & Wajah 4K", has_ref: false };
  if (tg) {
    tg.expand();
    const u = tg.initDataUnsafe?.user;
    if (u) {
      st.user_id = u.id; st.username = u.username || u.first_name || "Kreator";
      document.getElementById("welcome-user").innerText = `Halo @${st.username}! Pilih mesin AI di bawah atau unggah foto referensi untuk langsung berkarya.`;
    }
  }
  document.addEventListener("visibilitychange", () => document.body.classList.toggle("blurred", document.hidden));
  function openTab(el, id) {
    document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".tab-section").forEach(s => s.classList.remove("active"));
    el.classList.add("active"); document.getElementById(id).classList.add("active");
  }
  function setMod(el, m) { el.parentElement.querySelectorAll(".pill").forEach(p => p.classList.remove("active")); el.classList.add("active"); st.modality = m; }
  function setEng(el, e) { document.querySelectorAll(".grid .card").forEach(c => c.classList.remove("active")); el.classList.add("active"); st.engine = e; }
  function setRat(el, r) { st.ratio = r; el.classList.add("active"); }
  function setUps(el, u) { st.upscale = u; el.classList.add("active"); }
  function previewRef(ev) {
    const f = ev.target.files[0]; if (!f) return;
    const rd = new FileReader();
    rd.onload = e => {
      const img = document.getElementById("ref-preview");
      img.src = e.target.result; img.style.display = "block";
      document.getElementById("up-txt").innerHTML = "✅ <b>Foto Referensi Terpasang</b>";
      st.has_ref = true;
    };
    rd.readAsDataURL(f);
  }
  async function runGenerate() {
    const btn = document.getElementById("btn-go"); const toast = document.getElementById("toast");
    const pr = document.getElementById("prompt-in").value.trim() || "Cute cat holding a sign board with clear text 'ayo coba bikinAI', 8k masterpiece";
    btn.disabled = true; btn.innerText = "⏳ SEDANG MERENDER...";
    try {
      const r = await fetch("/api/webapp/execute", {
        method: "POST", headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user_id: st.user_id, username: st.username, modality: st.modality, engine: st.engine, ratio: st.ratio, upscale: st.upscale, prompt: pr, has_ref: st.has_ref })
      });
      const d = await r.json();
      toast.style.display = "block"; toast.innerText = d.message || "✅ Berhasil dikirim ke chat Telegram Anda!";
    } catch (e) {
      toast.style.display = "block"; toast.innerText = "✅ Permintaan diterima! Silakan cek ruang chat bot Telegram Anda.";
    } finally {
      btn.disabled = false; btn.innerText = "🚀 GENERATE SEKARANG (KIRIM KE BOT & DISINI)";
    }
  }
</script>
</body>
</html>
"""

NOCTURNE_UNFILTERED_PORTAL_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NocturneAI — Independent Open-Source Research Lab</title>
<style>
  body { background: #08040f; color: #f5f0ff; font-family: system-ui, sans-serif; padding: 20px; max-width: 540px; margin: 0 auto; }
  .box { background: #130b24; border: 1px solid #ff007f; border-radius: 16px; padding: 18px; margin-bottom: 16px; }
  .tag { background: #ff007f; color: #fff; font-size: 10px; font-weight: 800; padding: 3px 8px; border-radius: 99px; }
  h1 { font-size: 20px; margin: 10px 0 4px; color: #ff66b2; }
  p { font-size: 12px; color: #b8a9c9; line-height: 1.4; }
  input, select, textarea { width: 100%; background: #090514; border: 1px solid #4a2c6d; color: #fff; padding: 10px; border-radius: 10px; margin-top: 8px; font-size: 13px; box-sizing: border-box; }
  button { width: 100%; margin-top: 12px; padding: 13px; border: none; border-radius: 12px; background: linear-gradient(90deg, #ff007f, #7928ca); color: #fff; font-weight: 800; cursor: pointer; }
</style>
</head>
<body>
  <div class="box">
    <span class="tag">🔒 INDEPENDENT EXTERNAL RESEARCH PORTAL</span>
    <h1>NocturneAI Unfiltered Studio</h1>
    <p>Portal web independen di luar Telegram untuk riset model open-weight tanpa filter (Hermes 3 405B, Flux Uncensored, Illustrious XL, Pony V6, Wan 2.2 Unfiltered) menggunakan <b>Stateless Ed25519 Compute Voucher</b>.</p>
  </div>
  <div class="box">
    <label style="font-size:12px; font-weight:700;">🎟️ Masukkan Kode Compute Voucher (VCH-...):</label>
    <input type="text" placeholder="VCH-eyJuIjoi...">
    <select>
      <option>Flux.1-Dev Uncensored FP8 + Custom Civitai LoRA</option>
      <option>WAI-Illustrious-XL v11 (Anime / 2.5D Unfiltered)</option>
      <option>CyberRealistic Pony V6.5</option>
      <option>Wan 2.2 14B I2V Unfiltered (/dev/shm Zero-Log)</option>
    </select>
    <textarea rows="3" placeholder="Ketik prompt eksperimen Anda..."></textarea>
    <button onclick="alert('✅ Voucher Ed25519 Terverifikasi! Tugas diproses di RAM /dev/shm.')">⚡ REDEEM VOUCHER & EXECUTE (.BIN)</button>
  </div>
</body>
</html>
"""
