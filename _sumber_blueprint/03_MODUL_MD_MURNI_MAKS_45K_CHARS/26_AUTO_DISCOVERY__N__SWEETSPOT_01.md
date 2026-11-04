
<!-- [ID:26_AUTO_DISCOVERY__N__S001] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: -N:, :200 -->
# ---------------------------------------------------------------- core
def dispatch_command(text: str, channel: Channel, user_id: str) -> str:
    cmd, args = _parse_command(text)
    audit({"type": "cmd", "cmd": cmd, "channel": channel, "user": user_id})

    # Owner-only commands
    if cmd == "/status":         return _status_report()
    if cmd == "/agents":
        return "\n".join(f"{a['id']} {a['name']} ({a['cat']}/{a['auto']})"
                         for a in AGENTS.values())
    if cmd == "/cost today":
        return "Biaya: (hubungkan services/ai-gateway)"
    if cmd == "/panic":
        s = kill_trigger("L0_PANIC", by=user_id)
        return f"🛑 L0 PANIC aktif. {json.dumps(s['state'])}"
    if cmd == "/freeze" and args and args[0] == "finance":
        kill_trigger("L1_FREEZE_FINANCE", by=user_id); return "❄️ Finance frozen."
    if cmd == "/freeze" and args and args[0] == "external":
        kill_trigger("L2_FREEZE_EXTERNAL", by=user_id); return "❄️ External frozen."
    if cmd == "/freeze" and args and args[0] == "agent" and len(args) > 1:
        kill_trigger("L3_FREEZE_AGENT", by=user_id, scope=args[1])
        return f"❄️ Agent {args[1]} frozen."
    if cmd == "/readonly" and args and args[0] == "on":
        kill_trigger("L4_READONLY", by=user_id); return "📖 Read-only aktif."
    if cmd == "/readonly" and args and args[0] == "off":
        kill_restore(by=user_id); return "▶️ Restored."
    if cmd == "/recover":
        kill_restore(by=user_id); return "♻️ Restore ke state normal."
    if cmd == "/log" and args and args[0] == "last":
        n = int(args[1]) if len(args) > 1 else 20
        return "\n".join(open("office/logs/audit.log").read().splitlines()[-n:])
    if cmd == "/approve" and args:
        r = APV.decide(args[0], "approved", owner=user_id)
        return f"✅ {args[0]}" if r["ok"] else f"❌ {r.get('reason')}"
    if cmd == "/deny" and args:
        r = APV.decide(args[0], "denied", owner=user_id,
                       note=" ".join(args[1:])[:200])
        return f"❌ {args[0]}" if r["ok"] else f"❌ {r.get('reason')}"
    if cmd == "/spawn" and len(args) >= 2 and args[0] == "agent":
        return f"🛠️ Spawn agent {args[1]} (hubungkan scripts/gen_agents.py)"
    if cmd == "/pr" and len(args) >= 1 and args[0] == "create":
        return "📝 PR create (hubungkan GitHub API)"

    return f"❓ Perintah tidak dikenal: {cmd}. Coba /status"

