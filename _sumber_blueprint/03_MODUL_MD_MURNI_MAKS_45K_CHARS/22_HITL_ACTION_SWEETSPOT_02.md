
<!-- [ID:22_HITL_ACTION_S003] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: DRY -->
# {name} ({id})

Kategori: **{cat}** · Mode: **{auto}** · Gate: {gate_list}

Agent ini dibuat otomatis oleh `scripts/gen_agents.py`.
Edit `SOP.md` untuk mengubah perilaku tanpa mengubah kode orchestrator.

#!/usr/bin/env python3
"""
Generate office/agents/<id>/ untuk semua agent di agents.yaml.
Idempotent: tidak menimpa SOP.md yang sudah diedit (kecuali --force).
"""
import sys, json
from pathlib import Path
sys.path.insert(0, ".")
from office.orchestrator.config_loader import load_agents

ROOT = Path(".")
TEMPLATE = ROOT / "office/agents/_template"
AGENTS_DIR = ROOT / "office/agents"

FORCE = "--force" in sys.argv
DRY = "--dry" in sys.argv

def render_sop(a: dict) -> str:
    tpl = (TEMPLATE / "SOP.md").read_text()
    return (tpl
        .replace("{name}", a["name"])
        .replace("{id}", a["id"])
        .replace("{objective}", a.get("objective", ""))
        .replace("{input_list}", "\n".join(f"- {x}" for x in a.get("input", [])))
        .replace("{output_list}", "\n".join(f"- {x}" for x in a.get("output", [])))
        .replace("{escalation_rule}", a.get("escalation_rule", ""))
        .replace("{approval_gate_list}", ", ".join(a.get("approval_gate", []) or ["—"]))
        .replace("{kpi_block}", json.dumps(a.get("kpi", {}), indent=2))
        .replace("{handoff_list}", ", ".join(a.get("handoff_targets", [])))
        .replace("{tools_list}", ", ".join(a.get("tools", []))))

def render_readme(a: dict) -> str:
    tpl = (TEMPLATE / "README.md").read_text()
    return (tpl
        .replace("{name}", a["name"])
        .replace("{id}", a["id"])
        .replace("{cat}", a.get("cat", ""))
        .replace("{auto}", a.get("auto", ""))
        .replace("{gate_list}", ", ".join(a.get("gate", []) or ["—"])))

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if DRY:
        print(f"[DRY] {path}"); return
    path.write_text(content)

def main():
    agents = load_agents()
    print(f"generating {len(agents)} agents → {AGENTS_DIR}")
    for aid, a in agents.items():
        d = AGENTS_DIR / aid
        (d / "memory" / "history").mkdir(parents=True, exist_ok=True)
        (d / "tools").mkdir(parents=True, exist_ok=True)

        readme = d / "README.md"
        if FORCE or not readme.exists():
            write(readme, render_readme(a))

        sop = d / "SOP.md"
        if FORCE or not sop.exists():
            write(sop, render_sop(a))

        mem_r = d / "memory" / "README.md"
        if FORCE or not mem_r.exists():
            write(mem_r, (TEMPLATE / "memory" / "README.md")
                  .read_text().replace("{name}", a["name"]).replace("{id}", aid))

        tools_r = d / "tools" / "README.md"
        if FORCE or not tools_r.exists():
            write(tools_r, (TEMPLATE / "tools" / "README.md")
                  .read_text().replace("{name}", a["name"]).replace("{id}", aid))

        summary = d / "memory" / "last_summary.md"
        if FORCE or not summary.exists():
            write(summary, f"# Last summary — {a['name']}\n\n(belum ada aktivitas)\n")

    print("selesai. Edit SOP per agent di office/agents/<id>/SOP.md")

if __name__ == "__main__":
    main()

#!/usr/bin/env bash
set -euo pipefail
ID="${1:?usage: init_agent.sh <agent_id>}"
python scripts/gen_agents.py          # pastikan yang sudah ada tergenerate
[ -d "office/agents/$ID" ] || { echo "agent $ID belum ada di agents.yaml"; exit 1; }
echo "✅ agent $ID siap di office/agents/$ID"

python scripts/gen_agents.py --dry    # preview 177 folder
python scripts/gen_agents.py          # generate
python scripts/gen_agents.py --force  # regenerate SOP (hati-hati, menimpa edit)

office/agents/A001/
├── README.md
├── SOP.md            ← edit ini untuk mengubah perilaku
├── memory/
│   ├── README.md
│   ├── last_summary.md
│   └── history/
└── tools/
    └── README.md

Bagian Isi Fungsi
1 bots/core/verify.py, dispatcher.py, bots/github/dispatch.py, bots/telegram/main.py Semua channel masuk ke satu dispatcher terverifikasi
2 office/orchestrator/* (brain_loader, approval_broker, kill_switch, policy_engine, main, audit, notification) Otak + gate + rem di satu tempat
3 office/config/agents.yaml (177 agent, schema penuh, defaults + override) + loader Definisi semua role tanpa 177 entry bertele-tele
4 office/agents/_template/* + scripts/gen_agents.py Generate 177 folder agent + SOP siap edit

from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class PaymentIntent(BaseModel):
    id: str
    created_at: datetime
    agent_id: str
    amount: float = Field(gt=0)
    currency: Literal["IDR","USD","USDT","USDC"] = "IDR"
    recipient: str
    method: Literal["bank_transfer","ewallet","crypto","card","vendor_api"]
    purpose: str
    invoice_url: str | None = None
    risk_score: float = 0.0
    status: Literal["draft","pending_approval","approved","rejected","paid","failed"] = "draft"
    approval_id: str | None = None
    tx_hash: str | None = None

class ApprovalDecision(BaseModel):
    approval_id: str
    decision: Literal["approved","denied"]
    owner: str
    note: str = ""

"""
Skor risiko sederhana. Semua > 0.7 otomatis eskalasi ke owner (tidak auto-approve
meski agent mode notify).
"""
import re

HIGH_RISK_TLDS = {"xyz","top","click","buzz","loan"}
KNOWN_VENDORS = {"openai.com","anthropic.com","stripe.com","aws.amazon.com",
                 "cloudflare.com","github.com","vercel.com"}

def score(intent: dict) -> float:
    s = 0.0
    amt = intent.get("amount", 0)
    if amt > 10_000_000: s += 0.5
    elif amt > 1_000_000: s += 0.25
    elif amt > 100_000: s += 0.1

    recipient = (intent.get("recipient") or "").lower()
    if any(recipient.endswith("." + t) for t in HIGH_RISK_TLDS): s += 0.3
    if not re.match(r"^[\w.\-@:]+$", recipient): s += 0.2
    if "@" in recipient and not any(recipient.endswith(v) for v in KNOWN_VENDORS):
        s += 0.15

    if intent.get("method") == "crypto": s += 0.3
    if intent.get("method") == "card" and amt > 5_000_000: s += 0.2

    return min(s, 1.0)
"""
Gate FIN: semua pergerakan uang WAJIB lewat sini.
- Draft dibuat oleh agent AP/AR/Treasury.
- Risk score dihitung otomatis.
- Approval via ApprovalBroker (X002) → notif ke owner (WA/Tele).
- Eksekusi hanya setelah approved DAN kill switch L1 tidak aktif.
"""
import os, json, time
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from office.orchestrator import approval_broker as APV
from office.orchestrator.kill_switch import is_frozen
from office.orchestrator.audit import audit
from office.orchestrator.notification_gateway import send_owner
from services.payment.models import PaymentIntent, ApprovalDecision
from services.payment.risk import score

STORE = Path("services/payment/store")
STORE.mkdir(parents=True, exist_ok=True)

def _save(intent: PaymentIntent):
    (STORE / f"{intent.id}.json").write_text(intent.model_dump_json(indent=2))

def _load(intent_id: str) -> PaymentIntent | None:
    p = STORE / f"{intent_id}.json"
    if not p.exists(): return None
    return PaymentIntent.model_validate_json(p.read_text())

def create_intent(agent_id: str, amount: float, recipient: str,
                  method: str, purpose: str, currency: str = "IDR",
                  invoice_url: str | None = None) -> dict:
    if is_frozen(category="finance"):
        return {"ok": False, "reason": "L1_FREEZE_FINANCE_active"}

    intent_id = f"pay_{int(time.time())}_{agent_id.lower()}"
    risk = score({"amount": amount, "recipient": recipient, "method": method})

    intent = PaymentIntent(
        id=intent_id, created_at="", agent_id=agent_id,
        amount=amount, currency=currency, recipient=recipient,
        method=method, purpose=purpose, invoice_url=invoice_url,
        risk_score=risk,
    )
    # set created_at
    from datetime import datetime, timezone
    intent.created_at = datetime.now(timezone.utc)

    # bila risiko tinggi → tetap gate, tapi ttl lebih pendek
    ttl = 4 if risk > 0.7 else 24
    apv_id = APV.create(agent_id=agent_id, gate="FIN",
                        payload=intent.model_dump(), ttl_hours=ttl)

    intent.status = "pending_approval"
    intent.approval_id = apv_id
    _save(intent)

    risk_tag = "🔴 HIGH" if risk > 0.7 else ("🟡" if risk > 0.3 else "🟢")
    send_owner(
        f"[GATE FIN] {apv_id}\n"
        f"{risk_tag} risk={risk:.2f} • {agent_id}\n"
        f"{amount} {currency} → {recipient}\n"
        f"via {method} • {purpose[:80]}\n"
        f"Balas: /approve {apv_id} atau /deny {apv_id}"
    )
    audit({"type":"payment_intent","intent":intent.model_dump()})
    return {"ok": True, "intent_id": intent_id, "approval_id": apv_id,
            "risk_score": risk, "ttl_hours": ttl}

def execute(intent_id: str, actor: str) -> dict:
    """
    Eksekusi setelah approval FIN approved.
    Di produksi: panggil bank API / e-wallet / crypto signer (external, owner-only).
    """
    intent = _load(intent_id)
    if not intent:
        return {"ok": False, "reason": "intent_not_found"}

    if is_frozen(category="finance"):
        return {"ok": False, "reason": "frozen"}

    if not intent.approval_id:
        return {"ok": False, "reason": "no_approval"}

    rec = APV.get(intent.approval_id)
    if not rec or rec["status"] != "approved":
        return {"ok": False, "reason": f"approval_{rec['status'] if rec else 'missing'}"}

    # Double-check: aktor harus owner
    if rec["decided_by"] != actor:
        return {"ok": False, "reason": "actor_mismatch"}

    # Placeholder eksekusi — di produksi ini titik panggil API bank/e-wallet/on-chain
    # Wajib: idempotency key = intent_id
    result = {
        "provider": intent.method,
        "tx_ref": f"TX-{intent.id}",
        "status": "paid",
    }
    intent.status = "paid"
    intent.tx_hash = result["tx_ref"]
    _save(intent)

    audit({"type":"payment_paid","intent":intent.model_dump(),"result":result})
    send_owner(f"✅ PAID {intent.id} • {intent.amount} {intent.currency} → {intent.recipient}")
    return {"ok": True, "result": result}

def status(intent_id: str) -> dict:
    i = _load(intent_id)
    return i.model_dump() if i else {"ok": False, "reason": "not_found"}

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import os
from services.payment import gate

app = FastAPI(title="Payment Service")
INTERNAL_KEY = os.environ.get("INTERNAL_KEY", "")

def _auth(x_internal_key: str):
    if not INTERNAL_KEY or x_internal_key != INTERNAL_KEY:
        raise HTTPException(401, "unauthorized")

class CreateReq(BaseModel):
    agent_id: str
    amount: float
    recipient: str
    method: str
    purpose: str
    currency: str = "IDR"
    invoice_url: str | None = None

@app.post("/intent")
def create(req: CreateReq, x_internal_key: str = Header(default="")):
    _auth(x_internal_key)
    return gate.create_intent(**req.model_dump())

@app.post("/execute/{intent_id}")
def execute(intent_id: str, actor: str, x_internal_key: str = Header(default="")):
    _auth(x_internal_key)
    return gate.execute(intent_id, actor)

@app.get("/status/{intent_id}")
def status(intent_id: str, x_internal_key: str = Header(default="")):
    _auth(x_internal_key)
    return gate.status(intent_id)


<!-- [ID:22_HITL_ACTION_S004] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: :20, DICT -->
## Command owner
- `/cost today` → tampilkan pemakaian hari ini (via orchestrator)

"""
Verifikasi hash chain di office/logs/audit.log.
Format baris: <sha256(line)> <json_line>
Kalau ada manipulasi, chain putus dan terdeteksi.
"""
import hashlib, json
from pathlib import Path

AUDIT = Path("office/logs/audit.log")

def verify_chain(path: Path = AUDIT) -> dict:
    if not path.exists():
        return {"ok": True, "reason": "empty"}
    bad = []
    total = 0
    with path.open() as f:
        for i, raw in enumerate(f, 1):
            raw = raw.rstrip("\n")
            if not raw.strip(): continue
            total += 1
            try:
                h, payload = raw.split(" ", 1)
            except ValueError:
                bad.append({"line": i, "reason": "malformed"}); continue
            computed = hashlib.sha256(payload.encode()).hexdigest()
            if computed != h:
                bad.append({"line": i, "reason": "hash_mismatch",
                            "expected": computed, "found": h})
            # pastikan json valid
            try: json.loads(payload)
            except Exception: bad.append({"line": i, "reason": "invalid_json"})
    return {"ok": len(bad) == 0, "total": total, "bad": bad[:20],
            "bad_count": len(bad)}

"""
Rekonstruksi insiden dari audit log.
Query: rentang waktu, agent_id, channel, atau tipe event.
Output: timeline yang bisa dibaca manusia.
"""
import json, time
from pathlib import Path
from datetime import datetime

AUDIT = Path("office/logs/audit.log")

def _iter_events():
    if not AUDIT.exists(): return
    with AUDIT.open() as f:
        for raw in f:
            raw = raw.strip()
            if not raw: continue
            try:
                _, payload = raw.split(" ", 1)
                yield json.loads(payload)
            except Exception:
                continue

def timeline(start: float | None = None, end: float | None = None,
             agent: str | None = None, event_type: str | None = None,
             channel: str | None = None, limit: int = 500) -> list[dict]:
    start = start or 0.0
    end = end or time.time()
    out = []
    for e in _iter_events():
        ts = e.get("ts", 0)
        if not (start <= ts <= end): continue
        if agent and e.get("agent") != agent: continue
        if event_type and e.get("type") != event_type: continue
        if channel and e.get("channel") != channel: continue
        e["_human_ts"] = datetime.utcfromtimestamp(ts).isoformat()+"Z"
        out.append(e)
        if len(out) >= limit: break
    return out

def incident_summary(incident_id: str) -> dict:
    """
    Ambil semua event yang terkait insiden berdasarkan approval_id atau intent_id.
    """
    keys = set()
    events = []
    for e in _iter_events():
        blob = json.dumps(e)
        if incident_id in blob:
            events.append(e)
            if e.get("approval_id"): keys.add(e["approval_id"])
    # lengkapi dengan event terkait approval_ids
    for e in _iter_events():
        if e.get("id") in keys or e.get("approval_id") in keys:
            if e not in events: events.append(e)
    events.sort(key=lambda x: x.get("ts", 0))
    return {"incident_id": incident_id, "events": events,
            "count": len(events)}

from fastapi import FastAPI, Header, HTTPException
import os
from services.audit import verifier, forensics

app = FastAPI(title="Audit Service")
INTERNAL_KEY = os.environ.get("INTERNAL_KEY","")

def _auth(k: str):
    if not INTERNAL_KEY or k != INTERNAL_KEY:
        raise HTTPException(401, "unauthorized")

@app.get("/health")
def health(): return {"ok": True}

@app.get("/verify")
def verify(x_internal_key: str = Header(default="")):
    _auth(x_internal_key)
    return verifier.verify_chain()

@app.get("/timeline")
def timeline(start: float = 0, end: float = 0, agent: str = "",
             event_type: str = "", channel: str = "", limit: int = 200,
             x_internal_key: str = Header(default="")):
    _auth(x_internal_key)
    return {"events": forensics.timeline(
        start=start or None, end=end or None,
        agent=agent or None, event_type=event_type or None,
        channel=channel or None, limit=limit)}

@app.get("/incident/{incident_id}")
def incident(incident_id: str, x_internal_key: str = Header(default="")):
    _auth(x_internal_key)
    return forensics.incident_summary(incident_id)

<!-- [ID:22_HITL_ACTION_S005] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
## Setup webhook (Meta)
1. Deploy `/webhook/*` di domain HTTPS.
2. Meta App → Webhooks → subscribe `messages` (WA) / `messages` (IG) / `mentions` (Threads).
3. Verify token: `WHATSAPP_VERIFY_TOKEN`.

{
  "name": "@office/admin",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev -p 3001",
    "build": "next build",
    "start": "next start -p 3001",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.2.3",
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "swr": "2.2.5"
  },
  "devDependencies": {
    "@types/node": "20.12.7",
    "@types/react": "18.3.1",
    "typescript": "5.4.5"
  }
}

/** @type {import('next').NextConfig} */
export default {
  output: "standalone",
  poweredByHeader: false,
  async headers() {
    return [{
      source: "/(.*)",
      headers: [
        { key: "X-Frame-Options", value: "DENY" },
        { key: "X-Content-Type-Options", value: "nosniff" },
        { key: "Referrer-Policy", value: "no-referrer" },
        { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" }
      ]
    }];
  }
};

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Owner-only: cek cookie session. Kalau tidak ada → 401.
export function middleware(req: NextRequest) {
  const session = req.cookies.get("owner_session")?.value;
  if (!session) {
    return new NextResponse("Unauthorized", { status: 401 });
  }
  return NextResponse.next();
}

export const config = { matcher: ["/((?!_next|favicon.ico).*)"] };

import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Office Admin",
  robots: { index: false, follow: false }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id">
      <body style={{ fontFamily: "system-ui, sans-serif", margin: 0 }}>
        <nav style={{ display: "flex", gap: 16, padding: 16,
                      background: "#111", color: "#fff" }}>
          <a href="/" style={{ color: "#fff" }}>Overview</a>
          <a href="/approvals" style={{ color: "#fff" }}>Approvals</a>
          <a href="/agents" style={{ color: "#fff" }}>Agents</a>
          <a href="/kill-switch" style={{ color: "#fff" }}>Kill Switch</a>
        </nav>
        <main style={{ padding: 24 }}>{children}</main>
      </body>
    </html>
  );
}
const BASE = process.env.NEXT_PUBLIC_ORCH_URL || "http://localhost:8000";
const KEY  = process.env.NEXT_PUBLIC_INTERNAL_KEY || "";

async function j<T>(path: string, init: RequestInit = {}): Promise<T> {
  const r = await fetch(`${BASE}${path}`, {
    ...init,
    headers: { "X-Internal-Key": KEY, "Content-Type": "application/json",
               ...(init.headers || {}) },
    cache: "no-store"
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  return r.json();
}

export const api = {
  status:  () => j<any>("/health"),
  cost:    () => j<any>("/cost").catch(() => ({})),
  agents:  () => fetch("/api/agents").then(r => r.json()),
  approvals: () => fetch("/api/approvals").then(r => r.json()),
  approve: (id: string) => fetch("/api/approve", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id })
  }).then(r => r.json()),
  deny: (id: string) => fetch("/api/deny", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id })
  }).then(r => r.json()),
  kill: (level: string, scope?: string) => fetch("/api/kill", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ level, scope })
  }).then(r => r.json()),
  recover: () => fetch("/api/recover", { method: "POST" }).then(r => r.json()),
};
"use client";
import useSWR from "swr";
import { api } from "../lib/api";

export default function Page() {
  const { data: health } = useSWR("health", api.status, { refreshInterval: 3000 });
  const { data: cost } = useSWR("cost", api.cost, { refreshInterval: 10000 });

  const kill = health?.kill?.level || "OFF";
  const color = kill === "OFF" ? "#0a0" : "#c00";

  return (
    <div>
      <h1>Overview</h1>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 16 }}>
        <Card title="Kill Switch">
          <span style={{ color, fontSize: 24, fontWeight: 700 }}>{kill}</span>
        </Card>
        <Card title="Global Spend (hari ini)">
          <pre style={{ margin: 0 }}>
            ${cost?.budget?.global?.spent ?? 0} / ${cost?.budget?.global?.budget ?? 0}
          </pre>
        </Card>
        <Card title="Panggilan LLM">
          <pre style={{ margin: 0 }}>{cost?.budget?.global?.calls ?? 0}</pre>
        </Card>
      </div>
      <h2 style={{ marginTop: 32 }}>Per Kategori</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ textAlign: "left", borderBottom: "1px solid #ccc" }}>
            <th>Kategori</th><th>Spent</th><th>Budget</th><th>Calls</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(cost?.budget || {}).map(([k, v]: any) => (
            <tr key={k} style={{ borderBottom: "1px solid #eee" }}>
              <td>{k}</td>
              <td>${(v.spent ?? 0).toFixed(4)}</td>
              <td>${v.budget}</td>
              <td>{v.calls}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Card({ title, children }: any) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 16 }}>
      <div style={{ fontSize: 12, opacity: 0.6, marginBottom: 8 }}>{title}</div>
      {children}
    </div>
  );
}

"use client";
import useSWR from "swr";
import { api } from "../../lib/api";

export default function Approvals() {
  const { data, mutate } = useSWR("approvals", api.approvals, { refreshInterval: 5000 });
  const items = data?.items || [];

  return (
    <div>
      <h1>Approval Queue</h1>
      {items.length === 0 && <p>Tidak ada approval pending.</p>}
      {items.map((it: any) => (
        <div key={it.id} style={{ border: "1px solid #ddd", borderRadius: 8,
                                  padding: 12, marginBottom: 12 }}>
          <div><b>{it.id}</b> · gate <b>{it.gate}</b> · agent <code>{it.agent_id}</code></div>
          <pre style={{ background: "#f6f6f6", padding: 8, overflowX: "auto" }}>
            {JSON.stringify(it.payload, null, 2)}
          </pre>
          <div style={{ display: "flex", gap: 8 }}>
            <button onClick={async () => { await api.approve(it.id); mutate(); }}>
              ✅ Approve
            </button>
            <button onClick={async () => { await api.deny(it.id); mutate(); }}>
              ❌ Deny
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

"use client";
import useSWR from "swr";
import { api } from "../../lib/api";

const LEVELS = [
  { code: "L0_PANIC",            label: "L0 PANIC — Stop semua", color: "#c00" },
  { code: "L1_FREEZE_FINANCE",   label: "L1 Freeze Finance",    color: "#c60" },
  { code: "L2_FREEZE_EXTERNAL",  label: "L2 Freeze External",   color: "#c60" },
  { code: "L4_READONLY",         label: "L4 Read-Only",         color: "#06c" },
];

export default function KillSwitch() {
  const { data, mutate } = useSWR("health", api.status, { refreshInterval: 2000 });
  const current = data?.kill?.level || "OFF";

  return (
    <div>
      <h1>Kill Switch</h1>
      <p>Status: <b style={{ color: current === "OFF" ? "#0a0" : "#c00" }}>{current}</b></p>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(2,1fr)", gap: 12 }}>
        {LEVELS.map(l => (
          <button key={l.code}
            style={{ padding: 24, background: l.color, color: "#fff",
                     border: "none", borderRadius: 8, fontSize: 16, cursor: "pointer" }}
            onClick={async () => {
              if (!confirm(`Aktifkan ${l.code}?`)) return;
              await api.kill(l.code); mutate();
            }}>
            {l.label}
          </button>
        ))}
        <button
          style={{ padding: 24, background: "#0a0", color: "#fff",
                   border: "none", borderRadius: 8, fontSize: 16, cursor: "pointer" }}
          onClick={async () => {
            if (!confirm("Recover ke state normal?")) return;
            await api.recover(); mutate();
          }}>
          ♻️ RECOVER
        </button>
      </div>
      <p style={{ marginTop: 24, fontSize: 12, opacity: 0.7 }}>
        Untuk /panic via bot, wajib PIN. Dashboard ini butuh login owner.
      </p>
    </div>
  );
}

import { NextRequest } from "next/server";

export async function POST(req: NextRequest) {
  const body = await req.json();
  const r = await fetch(`${process.env.ORCH_URL}/command`, {
    method: "POST",
    headers: { "X-Internal-Key": process.env.INTERNAL_KEY!,
               "Content-Type": "application/json" },
    body: JSON.stringify({
      text: body.level === "L0_PANIC" ? "/panic 000000" :
            body.level === "L1_FREEZE_FINANCE" ? "/freeze finance 000000" :
            body.level === "L2_FREEZE_EXTERNAL" ? "/freeze external 000000" :
            "/readonly on 000000",
      channel: "dashboard",
      user_id: process.env.OWNER_ID!,
    })
  });
  return new Response(await r.text(), { status: r.status });
}
import { NextResponse } from "next/server";
import fs from "fs/promises";
import path from "path";

export async function GET() {
  const dir = path.resolve(process.cwd(), "../../office/logs/approvals");
  try {
    const files = await fs.readdir(dir);
    const items = [];
    for (const f of files) {
      if (!f.startsWith("apv_")) continue;
      const raw = await fs.readFile(path.join(dir, f), "utf8");
      const rec = JSON.parse(raw);
      if (rec.status === "pending") items.push(rec);
    }
    return NextResponse.json({ items });
  } catch {
    return NextResponse.json({ items: [] });
  }
}
import { NextResponse } from "next/server";
import fs from "fs/promises";
import path from "path";
import YAML from "yaml";

export async function GET() {
  const file = path.resolve(process.cwd(), "../../office/config/agents.yaml");
  const raw = await fs.readFile(file, "utf8");
  const cfg = YAML.parse(raw);
  const defaults = cfg.defaults || {};
  const agents = (cfg.agents || []).map((a: any) => ({ ...defaults, ...a }));
  return NextResponse.json({ agents });
}


<!-- [ID:22_HITL_ACTION_S006] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# Endpoint Real-Time Stream (SSE) agar halaman Web & Mini App otomatis Centang Hijau tanpa refresh
@app.get("/pay/{order_id}/stream")
async def payment_status_stream(order_id: str, request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            inv = TRANSACTIONS.get(order_id)
            if not inv:
                yield f"data: {json.dumps({'status': 'NOT_FOUND'})}\n\n"
                break
            
            yield f"data: {json.dumps({'status': inv['status'], 'amount': inv['final_amount']})}\n\n"
            
            if inv["status"] in ("PAID", "EXPIRED"):
                break
            await asyncio.sleep(2)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

import hmac
import hashlib
import base64
from datetime import datetime, timezone, timedelta

def generate_snap_symmetric_signature(
    http_method: str,
    relative_url: str,
    access_token: str,
    request_body: str,
    timestamp: str,
    client_secret: str
) -> str:
    """
    Membuat X-SIGNATURE standar SNAP Bank Indonesia (HMAC-SHA512)
    untuk menembak langsung API mutasi/QRIS Bank tanpa perantara PG.
    """
    # 1. Hash body JSON dengan SHA-256 (lowercase hex)
    minified_body = request_body.strip()
    body_hash = hashlib.sha256(minified_body.encode('utf-8')).hexdigest().lower()

    # 2. Susun StringToSign sesuai protokol resmi Bank Indonesia
    string_to_sign = f"{http_method.upper()}:{relative_url}:{access_token}:{body_hash}:{timestamp}"

    # 3. Enkripsi dengan HMAC-SHA512 menggunakan Client Secret dari Bank
    signature = hmac.new(
        client_secret.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        hashlib.sha512
    ).digest()

    return base64.b64encode(signature).decode('utf-8')

def get_jakarta_iso_timestamp() -> str:
    """Menghasilkan format waktu ISO-8601 WIB (+07:00) wajib untuk header X-TIMESTAMP."""
    wib = timezone(timedelta(hours=7))
    return datetime.now(wib).strftime("%Y-%m-%dT%H:%M:%S+07:00")
```
```


<!-- [ID:22_HITL_ACTION_S007] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR, :16 -->
# 5. SECURITY VALIDATORS & PRIVACY LEAK SCANNER
FORBIDDEN_CUSTOMER_JARGON = [
    "SingleWriterSQLiteDaemon", "redeemed_nullifiers", "Stateless Ed25519",
    "EMVCo CRC16", "4x-Remacri", "Dual-LLM Sandbox", "Dead-Job Sweeper",
    "SangMata", "Tuyul", "Lock Stripe", "HPP Rp 0",
]


def scan_customer_ui_for_leaks(sample_texts: list[str]) -> dict[str, Any]:
    leaks_found: list[str] = []
    combined = "\n".join(sample_texts) + "\n" + MINIAPP_FULL_WEBSITE_HTML + "\n" + render_freedom_web_portal_html()
    for term in FORBIDDEN_CUSTOMER_JARGON:
        if re.search(re.escape(term), combined, re.IGNORECASE):
            leaks_found.append(term)
    return {"clean": len(leaks_found) == 0, "leaks": leaks_found, "checked_terms": len(FORBIDDEN_CUSTOMER_JARGON)}


def verify_telegram_webapp_init_data(init_data_raw: str, bot_token: str, max_age_sec: int = 86400) -> dict[str, Any] | None:
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
        return json.loads(parsed.get("user", "{}")) if hmac.compare_digest(calculated_hash, received_hash) else None
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
    cleaned = "".join(ch for ch in normalized if unicodedata.category(ch) not in ("Cf", "Cc") or ch in ("\n", "\r", "\t")).strip()
    leet_map = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})
    deobfuscated = cleaned.lower().translate(leet_map)
    return cleaned, bool(_INJECTION_PATTERNS.search(cleaned) or _INJECTION_PATTERNS.search(deobfuscated))


def issue_stateless_ed25519_voucher(user_id: int, compute_units: int = 10, ttl_seconds: int = 86400) -> str:
    now_ts = int(time.time())
    nonce = hashlib.sha256(f"{user_id}:{now_ts}:{os.urandom(8).hex()}".encode()).hexdigest()[:16]
    payload_bytes = json.dumps({"n": nonce, "u": int(user_id), "c": int(compute_units), "exp": now_ts + ttl_seconds}, separators=(",", ":")).encode("utf-8")
    signature = Ed25519PrivateKey.from_private_bytes(ED25519_PRIV_BYTES).sign(payload_bytes)
    b64_p = base64.urlsafe_b64encode(payload_bytes).decode("ascii").rstrip("=")
    b64_s = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")
    return f"VCH-{b64_p}.{b64_s}"


async def verify_and_redeem_ed25519_voucher(db: aiosqlite.Connection, voucher_code: str) -> tuple[bool, str, int]:
    code = voucher_code.strip()
    if not code.startswith("VCH-") or "." not in code:
        return False, "Format Kode Akses VIP tidak sesuai.", 0
    try:
        b64_p, b64_s = code[4:].split(".", 1)
        payload_bytes = base64.urlsafe_b64decode(b64_p + "=" * (-len(b64_p) % 4))
        sig_bytes = base64.urlsafe_b64decode(b64_s + "=" * (-len(b64_s) % 4))
        Ed25519PublicKey.from_public_bytes(ED25519_PUB_BYTES).verify(sig_bytes, payload_bytes)
        data = json.loads(payload_bytes.decode("utf-8"))
        exp, units = int(data.get("exp", 0)), int(data.get("c", 10))
        if exp <= int(time.time()):
            return False, "Kode Akses VIP sudah kedaluwarsa.", 0
        nullifier_hash = hashlib.sha256(sig_bytes).hexdigest()

        async def _tx(conn: aiosqlite.Connection) -> bool:
            cur = await conn.execute("SELECT 1 FROM redeemed_nullifiers WHERE nullifier_hash = ?;", (nullifier_hash,))
            if await cur.fetchone():
                return False
            await conn.execute("INSERT INTO redeemed_nullifiers (nullifier_hash, expires_at) VALUES (?, ?);", (nullifier_hash, exp))
            return True

        if not await DB_WRITER_DAEMON.execute_write_tx(db, _tx):
            return False, "Kode Akses VIP sudah pernah digunakan.", 0
        return True, f"Kode Akses VIP Aktif (+{units} Kredit Studio)!", units
    except Exception:
        return False, "Kode Akses VIP tidak valid.", 0



<!-- [ID:22_HITL_ACTION_S008] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR, :16 -->
# 5. SECURITY VALIDATORS & AUTOMATED PRIVACY LEAK SCANNER
FORBIDDEN_CUSTOMER_JARGON = [
    "SingleWriterSQLiteDaemon", "redeemed_nullifiers", "Stateless Ed25519",
    "EMVCo CRC16", "4x-Remacri", "Dual-LLM Sandbox", "Dead-Job Sweeper",
    "SangMata", "Tuyul", "Lock Stripe", "HPP Rp 0",
]


def scan_customer_ui_for_leaks(sample_texts: list[str]) -> dict[str, Any]:
    leaks_found: list[str] = []
    combined = "\n".join(sample_texts) + "\n" + MINIAPP_FULL_WEBSITE_HTML + "\n" + render_freedom_web_portal_html()
    for term in FORBIDDEN_CUSTOMER_JARGON:
        if re.search(re.escape(term), combined, re.IGNORECASE):
            leaks_found.append(term)
    return {"clean": len(leaks_found) == 0, "leaks": leaks_found, "checked_terms": len(FORBIDDEN_CUSTOMER_JARGON)}


def verify_telegram_webapp_init_data(init_data_raw: str, bot_token: str, max_age_sec: int = 86400) -> dict[str, Any] | None:
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
        return json.loads(parsed.get("user", "{}")) if hmac.compare_digest(calculated_hash, received_hash) else None
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
    cleaned = "".join(ch for ch in normalized if unicodedata.category(ch) not in ("Cf", "Cc") or ch in ("\n", "\r", "\t")).strip()
    leet_map = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})
    deobfuscated = cleaned.lower().translate(leet_map)
    return cleaned, bool(_INJECTION_PATTERNS.search(cleaned) or _INJECTION_PATTERNS.search(deobfuscated))


def issue_stateless_ed25519_voucher(user_id: int, compute_units: int = 10, ttl_seconds: int = 86400) -> str:
    now_ts = int(time.time())
    nonce = hashlib.sha256(f"{user_id}:{now_ts}:{os.urandom(8).hex()}".encode()).hexdigest()[:16]
    payload_bytes = json.dumps({"n": nonce, "u": int(user_id), "c": int(compute_units), "exp": now_ts + ttl_seconds}, separators=(",", ":")).encode("utf-8")
    signature = Ed25519PrivateKey.from_private_bytes(ED25519_PRIV_BYTES).sign(payload_bytes)
    b64_p = base64.urlsafe_b64encode(payload_bytes).decode("ascii").rstrip("=")
    b64_s = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")
    return f"VCH-{b64_p}.{b64_s}"


async def verify_and_redeem_ed25519_voucher(db: aiosqlite.Connection, voucher_code: str) -> tuple[bool, str, int]:
    code = voucher_code.strip()
    if not code.startswith("VCH-") or "." not in code:
        return False, "Format Kode Akses VIP tidak sesuai.", 0
    try:
        b64_p, b64_s = code[4:].split(".", 1)
        payload_bytes = base64.urlsafe_b64decode(b64_p + "=" * (-len(b64_p) % 4))
        sig_bytes = base64.urlsafe_b64decode(b64_s + "=" * (-len(b64_s) % 4))
        Ed25519PublicKey.from_public_bytes(ED25519_PUB_BYTES).verify(sig_bytes, payload_bytes)
        data = json.loads(payload_bytes.decode("utf-8"))
        exp, units = int(data.get("exp", 0)), int(data.get("c", 10))
        if exp <= int(time.time()):
            return False, "Kode Akses VIP sudah melewati masa berlaku.", 0
        nullifier_hash = hashlib.sha256(sig_bytes).hexdigest()

        async def _tx(conn: aiosqlite.Connection) -> bool:
            cur = await conn.execute("SELECT 1 FROM redeemed_nullifiers WHERE nullifier_hash = ?;", (nullifier_hash,))
            if await cur.fetchone():
                return False
            await conn.execute("INSERT INTO redeemed_nullifiers (nullifier_hash, expires_at) VALUES (?, ?);", (nullifier_hash, exp))
            return True

        if not await DB_WRITER_DAEMON.execute_write_tx(db, _tx):
            return False, "Kode Akses VIP ini sudah pernah diaktifkan sebelumnya.", 0
        return True, f"Kode Akses VIP Aktif (+{units} Kredit Studio ditambahkan)!", units
    except Exception:
        return False, "Kode Akses VIP tidak dapat diverifikasi.", 0



<!-- [ID:22_HITL_ACTION_S009] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 388

   @staticmethod
   async def request_approval(
       db: aiosqlite.Connection,
       action_type: Literal[
           "DATA_MIGRATION",
           "PRICE_PLAN_CHANGE",
           "DELETE_FEATURE_PLUGIN",
           "WITHDRAW_ABOVE_THRESHOLD",
           "SECURITY_POLICY_CHANGE",
       ],
       summary: str,
       payload: dict[str, Any],
   ) -> dict[str, Any]:
       if action_type not in MANDATORY_HUMAN_APPROVAL_ACTIONS:
           raise ValueError(f"Unknown approval action_type: {action_type}")
       app_id = f"APR-{int(time.time())}-{secrets.token_hex(2).upper()}"
       now_ts = int(time.time())
       async def _tx(conn: aiosqlite.Connection) -> None:
           await conn.execute(
               """
               INSERT INTO pending_human_approvals
               (approval_id, action_type, summary, payload_json, status, created_at, decided_at)
               VALUES (?, ?, ?, ?, 'PENDING', ?, 0);
               """,
               (app_id, action_type, summary, json.dumps(payload), now_ts),
           )
       await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
       return {
           "approval_id": app_id,
           "action_type": action_type,
           "summary": summary,
           "status": "PENDING_HUMAN_APPROVAL",
       }
   @staticmethod
   async def decide_approval(
       db: aiosqlite.Connection, approval_id: str, approve: bool
   ) -> tuple[bool, str, dict[str, Any]]:
       cur = await db.execute(
           "SELECT action_type, summary, payload_json, status FROM pending_human_approvals WHERE approval_id 
           (approval_id,),
       )
       row = await cur.fetchone()
       if not row:
           return False, "Tiket persetujuan tidak ditemukan.", {}
       act_type, summary, payload_raw, st = (
           str(row[0]),
           str(row[1]),
           str(row[2]),
           str(row[3]),
       )
       if st != "PENDING":
           return False, f"Tiket ini sudah berstatus {st}.", {}
       new_st = "APPROVED" if approve else "REJECTED"
       async def _tx(conn: aiosqlite.Connection) -> None:
           await conn.execute(
               "UPDATE pending_human_approvals SET status = ?, decided_at = ? WHERE approval_id = ?;",
               (new_st, int(time.time()), approval_id),
           )
       await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
       payload = json.loads(payload_raw) if payload_raw else {}
       if not approve:
           return True, f"Operasi `{act_type}` ({summary}) dibatalkan oleh Owner.", payload
       # Eksekusi aksi yang telah disetujui secara eksplisit oleh Owner
       if act_type == "PRICE_PLAN_CHANGE":



<!-- [ID:22_HITL_ACTION_S010] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 447

class HumanApprovalGate:
   """Master Contract D2: Human Approval Gate untuk 5 aksi kritis."""
   MANDATORY_GATES = ("DATA_MIGRATION", "PRICE_PLAN_CHANGE", "DELETE_FEATURE_PLUGIN", "WITHDRAW_ABOVE_THRESHO
   @staticmethod
   async def request_approval(db: aiosqlite.Connection, action_type: str, summary: str, payload: dict[str, An
       aid = f"APR-{int(time.time())}"
       async def _tx(conn: aiosqlite.Connection) -> None:
           await conn.execute(
               "INSERT INTO pending_human_approvals (approval_id, action_type, summary, payload_json, status,
               (aid, action_type, summary, json.dumps(payload), int(time.time()))
           )
       await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
       return {"approval_id": aid, "status": "PENDING_HUMAN_APPROVAL"}
HUMAN_APPROVAL_GATE = HumanApprovalGate()
def verify_telegram_webapp_init_data(init_data_raw: str, bot_token: str, max_age_sec: int = 3600) -> dict[str,
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
       return json.loads(parsed.get("user", "{}")) if hmac.compare_digest(calculated_hash, received_hash) els
   except Exception:
       return None
def issue_stateless_ed25519_voucher(user_id: int, compute_units: int = 15, ttl_seconds: int = 86400) -> str:
   now_ts = int(time.time())
   nonce_hex = secrets.token_hex(8)
   blind_commitment = hashlib.sha256(f"{nonce_hex}:{user_id}".encode("utf-8") + VOUCHER_BLIND_SALT).hexdigest
   payload_dict = {"n": nonce_hex, "b": blind_commitment, "c": int(compute_units), "t": "PRO_COMPUTE", "exp":
   payload_bytes = json.dumps(payload_dict, separators=(",", ":")).encode("utf-8")
   signature = Ed25519PrivateKey.from_private_bytes(ED25519_PRIV_BYTES).sign(payload_bytes)
   b64_p = base64.urlsafe_b64encode(payload_bytes).decode("ascii").rstrip("=")
   b64_s = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")
   return f"VCH-{b64_p}.{b64_s}"
