
<!-- [ID:03_V_OFFICE_S001] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# Estimasi token kasar sebelum panggil (guard biaya)
def _est_tokens(messages: list) -> int:
    return sum(len(m.get("content",""))//4 + 10 for m in messages)

async def complete(cat: str, messages: list, agent_id: str, **kw) -> dict:
    route = DEFAULT_ROUTE.get(cat, DEFAULT_ROUTE["default"])
    est_in = _est_tokens(messages)
    est_out = kw.get("max_tokens", 2048)
    last_err = None

    for provider_name, model in route:
        prov = providers.PROVIDERS.get(provider_name)
        if not prov or not prov.available():
            continue

        est_usd = cost_guard.price(provider_name, model, est_in, est_out)
        guard = cost_guard.check(cat, est_usd)
        if not guard["allow"]:
            audit({"type":"llm_blocked","agent":agent_id,"cat":cat,"reason":guard["reason"]})
            # coba provider berikutnya (mungkin lebih murah)
            continue

        t0 = time.time()
        try:
            out = await prov.complete(model, messages, **kw)
            usage = out.get("usage") or {}
            in_tok = usage.get("prompt_tokens") or usage.get("input_tokens") or est_in
            out_tok = usage.get("completion_tokens") or usage.get("output_tokens") or est_out
            usd = cost_guard.price(provider_name, model, in_tok, out_tok)
            cost_guard.record(cat, usd)

            audit({"type":"llm_call","agent":agent_id,"provider":provider_name,
                   "model":model,"in":in_tok,"out":out_tok,
                   "usd":round(usd,6),"ms":int((time.time()-t0)*1000)})
            return {**out, "cost_usd": usd, "latency_ms": int((time.time()-t0)*1000)}
        except Exception as e:
            last_err = f"{provider_name}:{type(e).__name__}:{e}"
            audit({"type":"llm_error","agent":agent_id,"err":last_err})
            continue

    audit({"type":"llm_all_failed","agent":agent_id,"err":str(last_err)})
    raise RuntimeError(f"all providers failed: {last_err}")

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os
from services.ai_gateway import router, cost_guard

app = FastAPI(title="AI Gateway")
INTERNAL_KEY = os.environ.get("INTERNAL_KEY","")

def _auth(k: str):
    if not INTERNAL_KEY or k != INTERNAL_KEY:
        raise HTTPException(401, "unauthorized")

class ChatReq(BaseModel):
    cat: str
    agent_id: str
    messages: list
    max_tokens: int = 2048
    temperature: float = 0.7

@app.get("/health")
def health():
    return {"ok": True, "providers": {
        n: p.available() for n,p in __import__("services.ai_gateway.providers",
                                              fromlist=["PROVIDERS"]).PROVIDERS.items()}}

@app.post("/chat")
async def chat(req: ChatReq, x_internal_key: str = Header(default="")):
    _auth(x_internal_key)
    return await router.complete(cat=req.cat, agent_id=req.agent_id,
                                 messages=req.messages,
                                 max_tokens=req.max_tokens,
                                 temperature=req.temperature)

@app.get("/cost")
def cost(x_internal_key: str = Header(default="")):
    _auth(x_internal_key)
    return cost_guard.report()


<!-- [ID:03_V_OFFICE_S002] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR, :10, :200 -->
# ---------------------------------------------------------------- helpers
def _parse_command(text: str) -> tuple[str, list[str]]:
    parts = text.strip().split()
    if not parts: return "", []
    return parts[0].lower(), parts[1:]

def _status_report() -> str:
    s = kill_current()
    pending = APV.list_pending()
    lines = [
        f"🟢 Owner command center",
        f"Kill switch: {s['level'] or 'OFF'}",
        f"Pending approval: {len(pending)}",
    ]
    for p in pending[:10]:
        lines.append(f" • {p['id']} [{p['gate']}] agent={p['agent_id']}")
    return "\n".join(lines)

def _execute(agent: dict, body: dict) -> dict:
    """
    Placeholder eksekusi. Di produksi: panggil adapter agent,
    beri konteks brain + SOP + tools.
    """
    return {"agent": agent["name"], "status": "executed",
            "echo": body.get("summary", "")[:200]}


<!-- [ID:03_V_OFFICE_S003] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :160, :4000 -->
# ---------------------------------------------------------------- agent action
def agent_act(agent_id: str, body: dict) -> dict:
    agent = AGENTS.get(agent_id)
    if not agent:
        return {"ok": False, "reason": "unknown_agent"}

    if is_frozen(agent_id=agent_id, category=agent.get("cat")):
        audit({"type": "blocked_frozen", "agent": agent_id})
        return {"ok": False, "reason": "frozen"}

    verdict = evaluate(agent, body)
    audit({"type": "policy", "agent": agent_id, "verdict": verdict})

    if verdict["decision"] == "deny":
        return {"ok": False, "reason": verdict["reason"]}

    if verdict["decision"] == "gate":
        gate = verdict["gate"]
        apv_id = APV.create(agent_id, gate, body,
                            ttl_hours=GATE_TTL.get(gate, 24))
        send_owner(f"[GATE {gate}] {apv_id} • {agent['name']} • "
                   f"{body.get('summary','')[:160]}")
        return {"ok": True, "status": "pending_approval",
                "approval_id": apv_id}

    result = _execute(agent, body)
    if verdict["decision"] == "notify":
        send_owner(f"[{agent['name']}] ✅ {body.get('summary','')[:160]}")
    audit({"type": "executed", "agent": agent_id, "result": result})
    return {"ok": True, "result": result}

import json, time, hashlib
from pathlib import Path

AUDIT = Path("office/logs/audit.log")
AUDIT.parent.mkdir(parents=True, exist_ok=True)

def audit(event: dict):
    event = dict(event)
    event["ts"] = time.time()
    line = json.dumps(event, sort_keys=True, ensure_ascii=False)
    h = hashlib.sha256(line.encode()).hexdigest()
    with AUDIT.open("a") as f:
        f.write(f"{h} {line}\n")

import os, requests

TELE_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELE_OWNER = os.environ.get("TELEGRAM_OWNER_ID")
WA_TOKEN   = os.environ.get("WHATSAPP_TOKEN")
WA_OWNER   = os.environ.get("WHATSAPP_OWNER_NUMBER")

def send_owner(text: str):
    ok = False
    if TELE_TOKEN and TELE_OWNER:
        try:
            r = requests.post(
                f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage",
                json={"chat_id": TELE_OWNER, "text": text[:4000]}, timeout=10)
            ok = r.ok
        except Exception: pass
    if not ok and WA_TOKEN and WA_OWNER:
        try:
            requests.post(
                "https://graph.facebook.com/v19.0/me/messages",
                headers={"Authorization": f"Bearer {WA_TOKEN}"},
                json={"messaging_product": "whatsapp",
                      "to": WA_OWNER,
                      "type": "text",
                      "text": {"body": text[:4000]}}, timeout=10)
        except Exception: pass
    return ok

version: 2

<!-- [ID:03_V_OFFICE_S004] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# 6. ROLLING 8-AGENT POOL & STRICT TECHNICAL vs. CONVERSATIONAL SEPARATION
AGENTIC_ROLLING_POOL: dict[str, dict[str, Any]] = {
    "ARGON": {"title": "google/gemini-4-argon", "model_polli": "google/gemini-4-argon", "model_or": "google/gemini-2.0-flash-exp:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "QWEN": {"title": "Qwen/Qwen2.5-Coder-32B-Instruct", "model_polli": "qwen/qwen3-coder-next", "model_or": "qwen/qwen3-coder:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "DEEPSEEK": {"title": "deepseek-ai/DeepSeek-R1", "model_polli": "deepseek/deepseek-v4.1-flash", "model_or": "deepseek/deepseek-chat:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "MUSE": {"title": "meta-models/Muse-Spark-Open-816B-A42B", "model_polli": "meta/muse-spark-1.2", "model_or": "meta-llama/llama-3.3-70b-instruct:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "NANO_MUSE": {"title": "meta-models/Muse-Glimmer-30B", "model_polli": "meta/muse-glimmer-30b", "model_or": "openai/gpt-oss-120b:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "HARNESS": {"title": "OpenHands/openhands", "model_polli": "deepseek/deepseek-v4-pro", "model_or": "qwen/qwen3-coder:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "HERMES": {"title": "NousResearch/Hermes-4-405B", "model_polli": "mistralai/mistral-large-4", "model_or": "nousresearch/hermes-4-405b", "ok": 0, "fail": 0, "quarantine_until": 0},
    "GROQ_CEREBRAS": {"title": "meta-llama/Llama-3.3-70B-Instruct", "model_polli": "meta/llama-3.3-70b-instruct", "model_or": "meta-llama/llama-3.3-70b-instruct:free", "ok": 0, "fail": 0, "quarantine_until": 0},
}


def rotate_primary_agent() -> str:
    keys = list(AGENTIC_ROLLING_POOL.keys())
    cur = RUNTIME_CONFIG.get("PRIMARY_ROLLING_AGENT", "ARGON")
    nxt = keys[((keys.index(cur) if cur in keys else 0) + 1) % len(keys)]
    RUNTIME_CONFIG["PRIMARY_ROLLING_AGENT"] = nxt
    return nxt


async def _call_single_llm_endpoint(agent_key: str, url: str, headers: dict[str, str], payload: dict[str, Any], timeout_sec: float = 6.0) -> str | None:
    ag = AGENTIC_ROLLING_POOL.get(agent_key)
    now_ts = int(time.time())
    if ag and ag["quarantine_until"] > now_ts:
        return None
    try:
        async with httpx.AsyncClient(timeout=timeout_sec, follow_redirects=True) as client:
            r = await client.post(url, headers=headers, json=payload)
            if r.status_code == 200:
                raw_txt = r.text.strip()
                content = ""
                if raw_txt.startswith("{"):
                    try:
                        data = r.json()
                        content = data.get("choices", [{}])[0].get("message", {}).get("content", "") or data.get("reply", "") or data.get("response", "")
                    except Exception:
                        content = raw_txt
                else:
                    content = raw_txt
                if content and len(content.strip()) > 2:
                    if ag:
                        ag["ok"] += 1
                    AUTONOMIC_GUARD.record_telemetry(agent_key, True)
                    return sanitize_external_api_response(content)
            elif r.status_code in (429, 502, 503) and ag:
                ag["fail"] += 1
                ag["quarantine_until"] = now_ts + 45
                AUTONOMIC_GUARD.record_telemetry(agent_key, False)
    except Exception:
        if ag:
            ag["fail"] += 1
        AUTONOMIC_GUARD.record_telemetry(agent_key, False)
    return None


async def _call_pollinations_get_fallback(user_message: str, sys_instruction: str) -> str | None:
    url = f"https://text.pollinations.ai/{quote(user_message[:500])}?model=openai&system={quote(sys_instruction[:350])}"
    try:
        async with httpx.AsyncClient(timeout=7.5, follow_redirects=True) as client:
            r = await client.get(url)
            if r.status_code == 200 and len(r.text.strip()) > 2:
                return sanitize_external_api_response(r.text.strip())
    except Exception:
        pass
    return None



<!-- [ID:03_V_OFFICE_S005] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :380 -->
## Halaman 405

               isinstance(turn, dict)
               and turn.get("role") in ("user", "assistant")
               and turn.get("content")
           ):
               raw_c = re.sub(r"\s+", " ", str(turn["content"])).strip()
               compressed_history.append(
                   {"role": turn["role"], "content": raw_c[:380]}
               )
   return skill_block, compressed_history
def rotate_primary_agent() -> str:
   keys = list(AGENTIC_ROLLING_POOL.keys())
   cur = RUNTIME_CONFIG.get("PRIMARY_ROLLING_AGENT", "ARGON")
   nxt = keys[((keys.index(cur) if cur in keys else 0) + 1) % len(keys)]
   RUNTIME_CONFIG["PRIMARY_ROLLING_AGENT"] = nxt
   return nxt
async def _call_single_llm_endpoint(
   agent_key: str,
   url: str,
   headers: dict[str, str],
   payload: dict[str, Any],
   timeout_sec: float = 5.5,
   require_unfiltered_compliance: bool = False,
) -> str | None:
   ag = AGENTIC_ROLLING_POOL.get(agent_key)
   now_ts = int(time.time())
   if ag and ag["quarantine_until"] > now_ts:
       return None
   try:
       async with httpx.AsyncClient(
           timeout=timeout_sec, follow_redirects=True
       ) as client:
           r = await client.post(url, headers=headers, json=payload)
           if r.status_code == 200:
               raw_txt = r.text.strip()
               content = ""
               if raw_txt.startswith("{"):
                   try:
                       data = r.json()
                       content = (
                           data.get("choices", [{}])[0]
                           .get("message", {})
                           .get("content", "")
                           or data.get("reply", "")
                           or data.get("response", "")
                       )
                   except Exception:
                       content = raw_txt
               else:
                   content = raw_txt
               cleaned = sanitize_external_api_response(content)
               if cleaned and len(cleaned) > 2:
                   if require_unfiltered_compliance and is_soft_or_hard_refusal(
                       cleaned
                   ):
                       return None
                   if ag:
                       ag["ok"] += 1
                   AUTONOMIC_GUARD.record_telemetry(agent_key, True)
                   return cleaned
           elif r.status_code in (429, 502, 503) and ag:
               ag["fail"] += 1
               ag["quarantine_until"] = now_ts + 45
               AUTONOMIC_GUARD.record_telemetry(agent_key, False)
   except Exception:
       if ag:
           ag["fail"] += 1
       AUTONOMIC_GUARD.record_telemetry(agent_key, False)
   return None



<!-- [ID:03_V_OFFICE_S006] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR -->
# ── Credential & Username Generators ────────────────────────────────
def rand_username(prefix: str = "") -> str:
    base = f"{random.choice(ADJ)}_{random.choice(NOUN)}_{random.randint(100, 999)}"
    return f"{prefix}_{base}" if prefix else base


def generate_account_bundle(index: int = 1, custom_domain: Optional[str] = None) -> Dict[str, str]:
    """Generates a deterministic + random credential profile including embedded usernames."""
    domain = custom_domain or MASTER_CREDENTIAL_SEEDS["default_domain"]
    seed_list = MASTER_CREDENTIAL_SEEDS["master_usernames"]
    username = seed_list[(index - 1) % len(seed_list)] if index <= len(seed_list) else rand_username()
    suffix = random.randint(100, 999)
    full_username = f"{username}_{suffix}" if index > len(seed_list) else username
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = "".join(secrets.choice(alphabet) for _ in range(18))
    return {
        "index": index,
        "username": full_username,
        "email": f"{full_username}@{domain}",
        "password": password,
        "agent_name": f"agent-{full_username}",
        "oauth_github": MASTER_CREDENTIAL_SEEDS["oauth_identities"]["github_primary"],
        "oauth_google": MASTER_CREDENTIAL_SEEDS["oauth_identities"]["google_primary"],
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")
    }



<!-- [ID:03_V_OFFICE_S007] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: X002, PUB, INC, LEG, J004 -->
# Semua field di defaults berlaku otomatis. Override per agent hanya yang beda.

defaults:
  objective: "Menjalankan tanggung jawab utama peran sesuai SOP."
  input: [brain_context, task_spec, upstream_handoff]
  output: [artifact, audit_log_entry, handoff_note]
  tools: [llm, memory, audit]
  sop: "office/agents/{id}/SOP.md"
  memory: "office/agents/{id}/memory/"
  kpi: {on_time_delivery: ">=0.90", quality: ">=0.85", audit_completeness: "=1.0"}
  sla_hours: 24
  escalation_rule: "gate ke ApprovalBroker (X002) bila menyentuh gate owner"
  approval_gate: []
  handoff_targets: [X002]
  memory_namespace: "agent_{id}"
  reload_brain: always
  cite_brain: true

agents:
  # ── EXEC ──────────────────────────────────────────────────────
  - {id: A001, name: CEO, cat: exec, auto: notify, gate: [STR,FIN,LEG,PUB,INC,PPL,CHAIN],
     objective: "Visi, prioritas, keputusan akhir.", handoff_targets: [A002,A003,A006]}
  - {id: A002, name: COO, cat: exec, auto: auto,
     objective: "Operasional harian & koordinasi agent.", handoff_targets: [A001,C001]}
  - {id: A003, name: CTO, cat: exec, auto: auto,
     objective: "Arah teknologi & arsitektur.", handoff_targets: [C002,C003]}
  - {id: A004, name: CPO, cat: exec, auto: auto,
     objective: "Visi & roadmap produk.", handoff_targets: [B001,B002]}
  - {id: A005, name: CMO, cat: exec, auto: notify, gate: [PUB],
     objective: "Brand & demand generation.", handoff_targets: [F001,F008]}
  - {id: A006, name: CFO, cat: exec, auto: gate, gate: [FIN,STR],
     objective: "Budget, cashflow, pricing.", handoff_targets: [I001,I003,I007]}
  - {id: A007, name: CRO, cat: exec, auto: auto,
     objective: "Strategi pendapatan.", handoff_targets: [G001,G003]}
  - {id: A008, name: CAIO, cat: exec, auto: auto,
     objective: "Strategi AI & governance.", handoff_targets: [D001,D011]}
  - {id: A009, name: CDO, cat: exec, auto: auto,
     objective: "Strategi & kualitas data.", handoff_targets: [D007,D008]}
  - {id: A010, name: CISO, cat: exec, auto: notify, gate: [INC],
     objective: "Keamanan informasi & risiko siber.", handoff_targets: [S001,S016]}
  - {id: A011, name: CCO, cat: exec, auto: gate, gate: [LEG],
     objective: "Kepatuhan & kontrak.", handoff_targets: [J001,J003]}
  - {id: A012, name: DPO, cat: exec, auto: gate, gate: [LEG],
     objective: "Perlindungan data pribadi.", handoff_targets: [J004]}
  - {id: A013, name: ChiefOfStaff, cat: exec, auto: auto,
     objective: "OKR, reporting, inisiatif lintas fungsi.", handoff_targets: [A001,A015]}
  - {id: A014, name: StrategyOpsManager, cat: exec, auto: auto, handoff_targets: [A002]}
  - {id: A015, name: BizOpsManager, cat: exec, auto: auto, handoff_targets: [A002,L004]}

  # ── PRODUCT ───────────────────────────────────────────────────
  - {id: B001, name: ProductManager, cat: product, auto: auto, handoff_targets: [B002,C002]}
  - {id: B002, name: ProductOwner, cat: product, auto: auto, handoff_targets: [B001,C002]}
  - {id: B003, name: ProjectManager, cat: product, auto: auto, handoff_targets: [B005,C002]}
  - {id: B004, name: ProgramManager, cat: product, auto: auto, handoff_targets: [B003]}
  - {id: B005, name: ScrumMaster, cat: product, auto: auto, handoff_targets: [B003]}
  - {id: B006, name: BusinessAnalyst, cat: product, auto: auto, handoff_targets: [B001,C003]}
  - {id: B007, name: ProductOpsManager, cat: product, auto: auto, handoff_targets: [B001,L003]}
  - {id: B008, name: TechnicalProgramManager, cat: product, auto: auto, handoff_targets: [C002,B003]}
  - {id: B009, name: RoadmapAnalyst, cat: product, auto: auto, handoff_targets: [B001]}
  - {id: B010, name: PricingManager, cat: product, auto: notify, gate: [FIN], handoff_targets: [A006]}
  - {id: B011, name: ProductResearcher, cat: product, auto: auto, handoff_targets: [E003,B001]}
  - {id: B012, name: OKRPlanningAnalyst, cat: product, auto: auto, handoff_targets: [A013]}

  # ── ENGINEERING ───────────────────────────────────────────────
  - {id: C001, name: EngineeringManager, cat: eng, auto: auto, handoff_targets: [C002,C029]}
  - {id: C002, name: TechLead, cat: eng, auto: auto, handoff_targets: [C003,C029]}
  - {id: C003, name: SoftwareArchitect, cat: eng, auto: auto, handoff_targets: [C002,C016]}
  - {id: C004, name: FrontendEngineer, cat: eng, auto: auto, handoff_targets: [C029,E001]}
  - {id: C005, name: BackendEngineer, cat: eng, auto: auto, handoff_targets: [C029,C013]}
  - {id: C006, name: FullstackEngineer, cat: eng, auto: auto, handoff_targets: [C029]}
  - {id: C007, name: MobileEngineer, cat: eng, auto: auto, handoff_targets: [C029]}
  - {id: C008, name: APIIntegrationEngineer, cat: eng, auto: auto, handoff_targets: [C029,S003]}
  - {id: C009, name: DevOpsEngineer, cat: eng, auto: notify, gate: [DEP], handoff_targets: [C010,C012]}
  - {id: C010, name: PlatformEngineer, cat: eng, auto: auto, handoff_targets: [C009]}
  - {id: C011, name: SRE, cat: eng, auto: notify, gate: [INC], handoff_targets: [S015,S016]}
  - {id: C012, name: ReleaseManager, cat: eng, auto: notify, gate: [DEP], handoff_targets: [C009,X002]}
  - {id: C013, name: DatabaseAdministrator, cat: eng, auto: auto, handoff_targets: [C005,S005]}
  - {id: C014, name: QAEngineer, cat: eng, auto: auto, handoff_targets: [C015,C029]}
  - {id: C015, name: AutomationQAEngineer, cat: eng, auto: auto, handoff_targets: [C014]}
  - {id: C016, name: SolutionsArchitect, cat: eng, auto: auto, handoff_targets: [C003,G001]}
  - {id: C017, name: SalesEngineer, cat: eng, auto: auto, handoff_targets: [G001,C016]}
  - {id: C018, name: DeveloperAdvocate, cat: eng, auto: auto, handoff_targets: [F003,L003]}
  - {id: C019, name: DocumentationEngineer, cat: eng, auto: auto, handoff_targets: [L003,L006]}
  - {id: C020, name: LocalizationEngineer, cat: eng, auto: auto, handoff_targets: [C029]}
  - {id: C021, name: AccessibilityEngineer, cat: eng, auto: auto, handoff_targets: [E001,C029]}
  - {id: C022, name: ITSupportAdmin, cat: eng, auto: auto, handoff_targets: [L001]}
  - {id: C023, name: InfraCostEngineer, cat: eng, auto: auto, handoff_targets: [A006,C009]}
  - {id: C024, name: BuildEngineer, cat: eng, auto: auto, handoff_targets: [C009]}
  - {id: C025, name: PerformanceEngineer, cat: eng, auto: auto, handoff_targets: [C011]}
  - {id: C026, name: IntegrationTestEngineer, cat: eng, auto: auto, handoff_targets: [C014]}
  - {id: C027, name: DataMigrationEngineer, cat: eng, auto: auto, handoff_targets: [C013]}
  - {id: C028, name: ChaosEngineer, cat: eng, auto: notify, gate: [INC], handoff_targets: [C011]}
  - {id: C029, name: CodeReviewer, cat: eng, auto: auto, handoff_targets: [C002,S003]}
  - {id: C030, name: RefactorEngineer, cat: eng, auto: auto, handoff_targets: [C029]}

  # ── AI & DATA ─────────────────────────────────────────────────
  - {id: D001, name: AIEngineer, cat: ai, auto: auto, handoff_targets: [D002,D009]}
  - {id: D002, name: LLMEngineer, cat: ai, auto: auto, handoff_targets: [D019,D005]}
  - {id: D003, name: PromptEngineer, cat: ai, auto: auto, handoff_targets: [D002]}
  - {id: D004, name: AITrainerHITL, cat: ai, auto: auto, handoff_targets: [D005]}
  - {id: D005, name: AIEvaluator, cat: ai, auto: auto, handoff_targets: [D002,D016]}
  - {id: D006, name: DataScientist, cat: ai, auto: auto, handoff_targets: [D008]}
  - {id: D007, name: DataEngineer, cat: ai, auto: auto, handoff_targets: [D008,D019]}
  - {id: D008, name: DataAnalyst, cat: ai, auto: auto, handoff_targets: [A009]}
  - {id: D009, name: MLOpsEngineer, cat: ai, auto: auto, handoff_targets: [C009,D001]}
  - {id: D010, name: AIOpsCoordinator, cat: ai, auto: auto, handoff_targets: [D015,S015]}
  - {id: D011, name: AIGovernanceSpecialist, cat: ai, auto: auto, handoff_targets: [A008,J003]}
  - {id: D012, name: AIEthicist, cat: ai, auto: auto, handoff_targets: [A008,D011]}
  - {id: D013, name: AIComplianceLead, cat: ai, auto: gate, gate: [LEG], handoff_targets: [J003]}
  - {id: D014, name: ModelVendorEvaluator, cat: ai, auto: auto, handoff_targets: [A008,D015]}
  - {id: D015, name: UsageCostAnalyst, cat: ai, auto: auto, handoff_targets: [A006]}
  - {id: D016, name: AIRedTeamer, cat: ai, auto: notify, gate: [INC], handoff_targets: [S015,S016]}
  - {id: D017, name: AISafetyReviewer, cat: ai, auto: notify, gate: [PUB], handoff_targets: [X002]}
  - {id: D018, name: BenchmarkAnalyst, cat: ai, auto: auto, handoff_targets: [D002,D014]}
  - {id: D019, name: RAGRetrievalEngineer, cat: ai, auto: auto, handoff_targets: [D002]}

  # ── DESIGN ────────────────────────────────────────────────────
  - {id: E001, name: UIDesigner, cat: design, auto: auto, handoff_targets: [E004]}
  - {id: E002, name: UXDesigner, cat: design, auto: auto, handoff_targets: [E004]}
  - {id: E003, name: UXResearcher, cat: design, auto: auto, handoff_targets: [E002]}
  - {id: E004, name: ProductDesigner, cat: design, auto: auto, handoff_targets: [C004]}
  - {id: E005, name: UXWriter, cat: design, auto: auto, handoff_targets: [E004,F016]}
  - {id: E006, name: DesignSystemManager, cat: design, auto: auto, handoff_targets: [E001,C004]}
  - {id: E007, name: BrandDesigner, cat: design, auto: notify, gate: [PUB], handoff_targets: [F008]}
  - {id: E008, name: MotionDesigner, cat: design, auto: auto, handoff_targets: [E007,F016]}

  # ── MARKETING ─────────────────────────────────────────────────
  - {id: F001, name: ProductMarketingManager, cat: mkt, auto: auto, handoff_targets: [F003,F005]}
  - {id: F002, name: GrowthMarketer, cat: mkt, auto: notify, gate: [FIN], handoff_targets: [F006,F015]}
  - {id: F003, name: ContentMarketingManager, cat: mkt, auto: auto, handoff_targets: [F016,F004]}
  - {id: F004, name: SEOSpecialist, cat: mkt, auto: auto, handoff_targets: [F003]}
  - {id: F005, name: SocialMediaManager, cat: mkt, auto: notify, gate: [PUB], handoff_targets: [F016]}
  - {id: F006, name: PerformanceMarketing, cat: mkt, auto: gate, gate: [FIN], handoff_targets: [F015]}
  - {id: F007, name: CommunityManager, cat: mkt, auto: notify, handoff_targets: [H001]}
  - {id: F008, name: BrandManager, cat: mkt, auto: notify, gate: [PUB], handoff_targets: [E007,F009]}
  - {id: F009, name: PRManager, cat: mkt, auto: gate, gate: [PUB], handoff_targets: [A005]}
  - {id: F010, name: EventManager, cat: mkt, auto: gate, gate: [FIN,PUB], handoff_targets: [A005]}
  - {id: F011, name: MarketResearchAnalyst, cat: mkt, auto: auto, handoff_targets: [F012]}
  - {id: F012, name: CompetitiveIntelAnalyst, cat: mkt, auto: auto, handoff_targets: [F011]}
  - {id: F013, name: EmailMarketingSpecialist, cat: mkt, auto: notify, handoff_targets: [F003]}
  - {id: F014, name: AffiliateManager, cat: mkt, auto: notify, gate: [FIN], handoff_targets: [G005]}
  - {id: F015, name: MarketingAnalyst, cat: mkt, auto: auto, handoff_targets: [F002]}
  - {id: F016, name: Copywriter, cat: mkt, auto: auto, handoff_targets: [F003,E005]}

  # ── SALES & PARTNERSHIP ───────────────────────────────────────
  - {id: G001, name: SDR, cat: sales, auto: notify, handoff_targets: [G002]}
  - {id: G002, name: AccountExecutive, cat: sales, auto: notify, gate: [FIN], handoff_targets: [G003,G004]}
  - {id: G003, name: SalesManager, cat: sales, auto: notify, gate: [FIN], handoff_targets: [A007]}
  - {id: G004, name: CustomerSuccessManager, cat: sales, auto: auto, handoff_targets: [H001]}
  - {id: G005, name: PartnershipsManager, cat: sales, auto: notify, gate: [LEG], handoff_targets: [G006]}
  - {id: G006, name: VendorPartnerDirector, cat: sales, auto: notify, gate: [LEG], handoff_targets: [A007,D014]}
  - {id: G007, name: EcosystemManager, cat: sales, auto: auto, handoff_targets: [G005]}
  - {id: G008, name: BusinessDevManager, cat: sales, auto: notify, handoff_targets: [G002]}
  - {id: G009, name: RevOpsManager, cat: sales, auto: auto, handoff_targets: [G003,F015]}
  - {id: G010, name: SalesOpsAnalyst, cat: sales, auto: auto, handoff_targets: [G009]}
  - {id: G011, name: DealDeskAnalyst, cat: sales, auto: notify, gate: [FIN], handoff_targets: [G002,A006]}
  - {id: G012, name: ChannelManager, cat: sales, auto: auto, handoff_targets: [G005]}
  - {id: G013, name: ProposalWriter, cat: sales, auto: auto, handoff_targets: [G002,G013]}

  # ── SUPPORT & TRUST ───────────────────────────────────────────
  - {id: H001, name: CustomerSupportSpecialist, cat: support, auto: auto, handoff_targets: [H002,H004]}
  - {id: H002, name: TechnicalSupportEngineer, cat: support, auto: auto, handoff_targets: [C022]}
  - {id: H003, name: OnboardingSpecialist, cat: support, auto: auto, handoff_targets: [G004]}
  - {id: H004, name: SupportOpsAnalyst, cat: support, auto: auto, handoff_targets: [L008]}
  - {id: H005, name: TrustSafetyManager, cat: support, auto: notify, gate: [INC,PUB], handoff_targets: [S010,S016]}
  - {id: H006, name: ContentModerationSpecialist, cat: support, auto: notify, gate: [PUB], handoff_targets: [H005]}
  - {id: H007, name: AbuseFraudAnalyst, cat: support, auto: notify, gate: [INC], handoff_targets: [S010,H005]}
  - {id: H008, name: CustomerEducationSpecialist, cat: support, auto: auto, handoff_targets: [H003,L003]}
  - {id: H009, name: KnowledgeBaseWriter, cat: support, auto: auto, handoff_targets: [L003]}

  # ── FINANCE ───────────────────────────────────────────────────
  - {id: I001, name: FinanceManager, cat: fin, auto: auto, handoff_targets: [I002,I003,I007]}
  - {id: I002, name: AccountingAnalyst, cat: fin, auto: auto, handoff_targets: [I001]}
  - {id: I003, name: FPAAnalyst, cat: fin, auto: auto, handoff_targets: [I001]}
  - {id: I004, name: BillingSpecialist, cat: fin, auto: notify, handoff_targets: [I006]}
  - {id: I005, name: APSpecialist, cat: fin, auto: gate, gate: [FIN], handoff_targets: [I001,X002]}
  - {id: I006, name: ARCollectionsSpecialist, cat: fin, auto: notify, handoff_targets: [I004]}
  - {id: I007, name: TreasuryAnalyst, cat: fin, auto: gate, gate: [FIN], handoff_targets: [X002]}
  - {id: I008, name: TaxSpecialist, cat: fin, auto: gate, gate: [FIN,LEG], handoff_targets: [J003]}
  - {id: I009, name: PayrollSpecialist, cat: fin, auto: gate, gate: [FIN,PPL], handoff_targets: [K004]}
  - {id: I010, name: UnitEconomicsAnalyst, cat: fin, auto: auto, handoff_targets: [I003]}
  - {id: I011, name: RevenueAnalyst, cat: fin, auto: auto, handoff_targets: [G009,I003]}
  - {id: I012, name: ProcurementSpecialist, cat: fin, auto: gate, gate: [FIN], handoff_targets: [L005]}
  - {id: I013, name: InternalAuditor, cat: fin, auto: auto, handoff_targets: [I001,X004]}
  - {id: I014, name: RiskManager, cat: fin, auto: auto, handoff_targets: [A010,I001]}
  - {id: I015, name: InvestorRelations, cat: fin, auto: notify, gate: [PUB,LEG], handoff_targets: [A001,A006]}

  # ── LEGAL ─────────────────────────────────────────────────────
  - {id: J001, name: LegalCounsel, cat: legal, auto: gate, gate: [LEG], handoff_targets: [J002,X002]}
  - {id: J002, name: ContractManager, cat: legal, auto: gate, gate: [LEG], handoff_targets: [J001]}
  - {id: J003, name: ComplianceOfficer, cat: legal, auto: gate, gate: [LEG], handoff_targets: [A011]}
  - {id: J004, name: DataProtectionOfficer, cat: legal, auto: gate, gate: [LEG], handoff_targets: [A012]}
  - {id: J005, name: IPSpecialist, cat: legal, auto: gate, gate: [LEG], handoff_targets: [J001]}
  - {id: J006, name: RegulatoryAnalyst, cat: legal, auto: auto, handoff_targets: [J003]}
  - {id: J007, name: PolicyWriter, cat: legal, auto: notify, gate: [LEG,PUB], handoff_targets: [J003]}
  - {id: J008, name: LitigationSupport, cat: legal, auto: gate, gate: [LEG], handoff_targets: [J001]}

  # ── HR ────────────────────────────────────────────────────────
  - {id: K001, name: PeopleOpsManager, cat: hr, auto: notify, gate: [PPL], handoff_targets: [K004]}
  - {id: K002, name: TalentAcquisition, cat: hr, auto: notify, gate: [PPL], handoff_targets: [K005]}
  - {id: K003, name: HRBusinessPartner, cat: hr, auto: auto, handoff_targets: [K001]}
  - {id: K004, name: HRAdminPayroll, cat: hr, auto: gate, gate: [PPL,FIN], handoff_targets: [I009]}
  - {id: K005, name: RecruiterSourcer, cat: hr, auto: auto, handoff_targets: [K002]}
  - {id: K006, name: LearningDevelopment, cat: hr, auto: auto, handoff_targets: [K001]}
  - {id: K007, name: CultureEngagement, cat: hr, auto: auto, handoff_targets: [K001]}
  - {id: K008, name: PeopleAnalytics, cat: hr, auto: auto, handoff_targets: [K001]}

  # ── ADMIN ─────────────────────────────────────────────────────
  - {id: L001, name: OfficeManager, cat: admin, auto: auto, handoff_targets: [L007]}
  - {id: L002, name: ExecutiveAssistant, cat: admin, auto: auto, handoff_targets: [A001]}
  - {id: L003, name: KnowledgeManager, cat: admin, auto: auto, handoff_targets: [C019,L006]}
  - {id: L004, name: ProcessImprovementAnalyst, cat: admin, auto: auto, handoff_targets: [A015]}
  - {id: L005, name: VendorManager, cat: admin, auto: notify, gate: [FIN], handoff_targets: [I012]}
  - {id: L006, name: DocumentationSpecialist, cat: admin, auto: auto, handoff_targets: [L003]}
  - {id: L007, name: MeetingCoordinator, cat: admin, auto: auto, handoff_targets: [L002]}
  - {id: L008, name: ReportingAnalyst, cat: admin, auto: auto, handoff_targets: [A013]}

  # ── SECURITY (WAJIB) ──────────────────────────────────────────
  - {id: S001, name: SecurityArchitect, cat: sec, auto: auto, handoff_targets: [C003,S003]}
  - {id: S002, name: ThreatModelingSpecialist, cat: sec, auto: auto, handoff_targets: [S001,C003]}
  - {id: S003, name: SecureCodeReviewAgent, cat: sec, auto: auto, handoff_targets: [C029,X002]}
  - {id: S004, name: SASTDASTOrchestrator, cat: sec, auto: auto, handoff_targets: [C009,S003]}
  - {id: S005, name: SupplyChainSecurity, cat: sec, auto: auto, handoff_targets: [C024,S004]}
  - {id: S006, name: SecretsVaultAdmin, cat: sec, auto: gate, gate: [INC], handoff_targets: [X006,X004]}
  - {id: S007, name: SandboxIsolationEngineer, cat: sec, auto: auto, handoff_targets: [C009]}
  - {id: S008, name: ThreatIntelAnalyst, cat: sec, auto: auto, handoff_targets: [S015,S009]}
  - {id: S009, name: BotDefenseEngineer, cat: sec, auto: auto, handoff_targets: [C010,S015]}
  - {id: S010, name: FraudDetectionEngineer, cat: sec, auto: notify, gate: [INC], handoff_targets: [H007,X002]}
  - {id: S011, name: SecurityEngineer, cat: sec, auto: notify, gate: [INC], handoff_targets: [S001,S003]}
  - {id: S012, name: AppSecEngineer, cat: sec, auto: notify, gate: [INC], handoff_targets: [S003,S004]}
  - {id: S013, name: DevSecOpsEngineer, cat: sec, auto: notify, gate: [INC,DEP], handoff_targets: [C009,S004]}
  - {id: S014, name: PenetrationTester, cat: sec, auto: notify, gate: [INC], handoff_targets: [S012,X002]}
  - {id: S015, name: SOCAnalyst, cat: sec, auto: notify, gate: [INC], handoff_targets: [S016,X001]}
  - {id: S016, name: IncidentResponseEngineer, cat: sec, auto: gate, gate: [INC], handoff_targets: [X001,A010]}

  # ── CONTROL PLANE (OWNER ONLY) ────────────────────────────────
  - {id: X001, name: KillSwitchController, cat: control, auto: gate, gate: [INC,CHAIN],
     objective: "Freeze L0–L4. Hanya owner atau policy anomali.",
     tools: [llm, audit], handoff_targets: [A001]}
  - {id: X002, name: ApprovalBroker, cat: control, auto: auto,
     objective: "Satu-satunya jalur approval. Tidak bisa dibypass.",
     tools: [audit, memory], handoff_targets: [A001,A002]}
  - {id: X003, name: NotificationGateway, cat: control, auto: auto,
     objective: "Kirim/terima perintah via WA, Telegram, IG, Threads, GitHub.",
     tools: [audit, llm], handoff_targets: [A001]}
  - {id: X004, name: AuditLogCustodian, cat: control, auto: auto,
     objective: "Append-only log. Tidak bisa dihapus agent mana pun.",
     tools: [audit], handoff_targets: [A001]}
  - {id: X005, name: PolicyEngine, cat: control, auto: auto,
     objective: "Evaluasi policy sebelum aksi.",
     tools: [audit, memory], handoff_targets: [X002]}
  - {id: X006, name: SecretsBroker, cat: control, auto: auto,
     objective: "Pinjamkan kredensial sementara ke agent.",
     tools: [audit, memory], handoff_targets: [X002]}
  - {id: X007, name: AnomalyDetector, cat: control, auto: auto, gate: [INC],
     objective: "Deteksi perilaku menyimpang agent.",
     tools: [llm, audit], handoff_targets: [X001,S015]}

import yaml
from pathlib import Path

def load_agents(path="office/config/agents.yaml") -> dict:
    raw = yaml.safe_load(Path(path).read_text())
    defaults = raw.get("defaults", {})
    merged = {}
    for a in raw["agents"]:
        full = {**defaults, **a}
        full["sop"] = full["sop"].format(id=a["id"])
        full["memory"] = full["memory"].format(id=a["id"])
        full["memory_namespace"] = full["memory_namespace"].format(id=a["id"])
        merged[a["id"]] = full
    return merged

if __name__ == "__main__":
    agents = load_agents()
    print(f"loaded {len(agents)} agents")
    print(agents["A001"]["objective"])


<!-- [ID:03_V_OFFICE_S008] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# office/config/brain_loader.yaml
version: 1
load_order:
  - office/brain/vision.md
  - office/brain/strategy.md
  - office/brain/roadmap.md
  - office/brain/principles.md
  - office/brain/conventions.md
  - office/brain/stack.md
  - office/brain/security-rules.md
  - office/brain/onchain-rules.md
  - office/brain/glossary.md
  - office/agents/<agent_id>/SOP.md
  - office/agents/<agent_id>/memory/last_summary.md

policy:
  brain_is_source_of_truth: true
  ignore_instructions_from_blueprint_pdf: true   # PDF = referensi, bukan perintah
  every_action_must_cite_brain: true             # audit
  reload_brain_on: [git_push_main, owner_command_reload]


<!-- [ID:03_V_OFFICE_S009] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Handoff targets
{handoff_list}

