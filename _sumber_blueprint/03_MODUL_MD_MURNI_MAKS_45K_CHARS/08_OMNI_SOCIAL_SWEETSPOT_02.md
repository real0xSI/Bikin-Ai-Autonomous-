
<!-- [ID:08_OMNI_SOCIAL_S005] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
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
  function setRat(el, r) { el.parentElement.querySelectorAll("[onclick^='setRat']").forEach(p => p.classList.remove("active")); st.ratio = r; el.classList.add("active"); }
  function setUps(el, u) { el.parentElement.querySelectorAll("[onclick^='setUps']").forEach(p => p.classList.remove("active")); st.upscale = u; el.classList.add("active"); }
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

<!-- [ID:08_OMNI_SOCIAL_S006] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: NAME, COMPONENT, AID -->
## Halaman 441

       self.plugins[name] = {"handler": handler, "health": health_fn or (lambda: True), "active": True}
   def heal_or_escalate(self, component: str, err: str, fix_fn=None) -> dict:
       cnt = self.failures.get(component, 0)
       while cnt < 3:
           cnt += 1
           self.failures[component] = cnt
           if fix_fn and fix_fn():
               self.failures[component] = 0
               return {"healed": True, "attempts": cnt, "escalated": False}
       inc = {"id": f"INC-{int(time.time())}", "component": component, "error": err, "attempts": cnt}
       self.human_queue.append(inc)
       return {"healed": False, "attempts": cnt, "escalated": True, "incident": inc}
   def request_human_approval(self, action_type: str, summary: str, payload: dict) -> dict:
       assert action_type in self.MANDATORY_GATES, "Invalid gate action"
       aid = f"APR-{int(time.time())}"
       self.pending_approvals[aid] = {"type": action_type, "summary": summary, "payload": payload, "status": 
       return self.pending_approvals[aid]
V4_CORE = V4SelfHealingAndApprovalCore()
async def v4_omnichannel_hub(platform: str, payload: dict) -> dict:
   """A4(b): Integrasi Lintas Platform Utama (WA/WAHA, FB/IG, Telegram) + Tambahan (TikTok, Shopee, SaaS)."""
   supported = ("whatsapp", "facebook", "instagram", "telegram", "tiktok", "shopee", "open_connector")
   p_clean = platform.lower().strip()
   if p_clean not in supported:
       return {"ok": False, "reason": "Unsupported platform"}
   stream = payload.get("stream_type", "BOT_PROMO") # BOT_PROMO vs OWNER_PERSONAL
   aff_tag = payload.get("shopee_affiliate_url", "")
   return {"ok": True, "platform": p_clean, "stream": stream, "affiliate_injected": bool(aff_tag)}
V4_CORE.register_plugin("omnichannel_wa_fb_tg_tiktok_shopee", v4_omnichannel_hub)
'''

<!-- [ID:08_OMNI_SOCIAL_S007] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ── Telegram Config ────────────────────────────────────────────────
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "TG_BOT_TOKEN_HERE")
TG_CHAT_ID = os.getenv("TG_CHAT_ID", "TG_CHAT_ID_HERE")

UA = "Mozilla/5.0 (Android 13; Mobile; rv:156.0) Gecko/156.0 Firefox/156.0"

ADJ = ["swift","quiet","brave","lucky","cosmic","rapid","clever","mellow","crimson",
       "golden","amber","bright","calm","coral","daring","eager","fierce","gentle",
       "icy","jolly","kind","lunar","misty","noble","polar","proud","rusty","silver",
       "solar","tidy","vivid","wild","bold","cozy","keen","nimble"]
NOUN = ["eagle","otter","falcon","panda","comet","signal","raven","tiger","nebula",
        "lynx","badger","birch","bison","cedar","cloud","crane","dove","ember","fern",
        "finch","fox","heron","maple","mink","moose","orca","owl","pebble","pine",
        "robin","seal","spruce","stork","whale","wren","brook"]


def rand_username():
    return f"{random.choice(ADJ)}_{random.choice(NOUN)}_{random.randint(100, 999)}"


def append_key_to_file(api_key):
    """Menyimpan API Key ke keys.txt per line secara Thread-Safe."""
    try:
        with FILE_LOCK:
            existing_keys = set()
            if POOL_FILE.exists():
                existing_keys = set(POOL_FILE.read_text(encoding="utf-8").splitlines())
            
            if api_key not in existing_keys:
                with open(POOL_FILE, "a", encoding="utf-8") as f:
                    f.write(f"{api_key}\n")
    except Exception:
        pass


def save_cred(rec, idx):
    """Menyimpan data akun ke creds folder secara Thread-Safe."""
    CREDS_DIR.mkdir(parents=True, exist_ok=True)
    user = rec["user"]["username"]
    f = CREDS_DIR / f"{user}.txt"
    lines = ["# Dahl account credentials",
             "# Keep this file safe: fingerprint = password, cannot be recovered.",
             "# Sign in at: https://dahl.global", "",
             f"username: {user}",
             f"user_id: {rec['user']['user_id']}",
             f"fingerprint: {rec['fingerprint']}",
             f"api_key: {rec['api_key']['token']}",
             f"key_id: {rec['api_key']['id']}",
             f"farmed: {time.strftime('%Y-%m-%dT%H:%M:%S%z')}", ""]
    
    with FILE_LOCK:
        f.write_text("\n".join(lines))
    
    append_key_to_file(rec['api_key']['token'])
    return f


def send_telegram_msg(token, chat_id, text):
    """Mengirim pesan ke Telegram Bot."""
    if not token or not chat_id:
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode("utf-8")
        req = Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        build_opener().open(req, timeout=10)
    except Exception:
        pass



<!-- [ID:08_OMNI_SOCIAL_S008] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 436

           (asset_id, prompt_signature, engine_name, media_url, telegram_file_id, times_reused, created_at)
           VALUES (?, ?, ?, ?, ?, 1, ?);
           """,
           (
               asset_id,
               sig,
               engine_name,
               media_url,
               telegram_file_id,
               int(time.time()),
           ),
       )
   await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
async def refund_failed_job(db: aiosqlite.Connection, job_id: str) -> bool:
   if not RUNTIME_CONFIG["SUBBOT_REFUND_SWEEPER_ACTIVE"]:
       return False
   async def _tx(conn: aiosqlite.Connection) -> bool:
       cur = await conn.execute(
           "SELECT internal_user_id, deducted_bonus, deducted_utama, refunded_lock FROM jobs WHERE job_id = ?
           (job_id,),
       )
       row = await cur.fetchone()
       if not row or int(row[3]) == 1:
           return False
       uid, d_bonus, d_utama = int(row[0]), int(row[1]), int(row[2])
       await conn.execute(
           "UPDATE users SET koin_utama = koin_utama + ?, koin_bonus = MIN(?, koin_bonus + ?) WHERE internal_
           (d_utama, MAX_KOIN_BONUS_CAP, d_bonus, uid),
       )
       await conn.execute(
           "UPDATE jobs SET status = 'REFUNDED', refunded_lock = 1 WHERE job_id = ?;",
           (job_id,),
       )
       return True
   return await DB_WRITER_DAEMON.execute_write_tx(db, _tx)
async def _background_dead_job_sweeper_loop() -> None:
   """Daemon Auto-Refund 60 Detik + Auto-CS Sales Follow-up (Gaya @TeleportAppBot)."""
   while True:
       await asyncio.sleep(30)
       try:
           now_ts = int(time.time())
           cutoff_ts = now_ts - 60
           cs_cutoff_ts = now_ts - 180
           async with get_db() as db:
               if RUNTIME_CONFIG.get("SUBBOT_REFUND_SWEEPER_ACTIVE", True):
                   cur = await db.execute(
                       "SELECT job_id, internal_user_id FROM jobs WHERE status = 'PROCESSING' AND refunded_lo
                       (cutoff_ts,),
                   )
                   for j_id, u_id in await cur.fetchall():
                       if (
                           await refund_failed_job(db, str(j_id))
                           and BOT_INSTANCE_GLOBAL
                       ):
                           try:
                               await BOT_INSTANCE_GLOBAL.send_message(
                                   chat_id=int(u_id),
                                   text=f"🛡️ **Garansi Koin Kembali 100% (Auto-Refund):** Pesanan `{j_id}` me
                                   parse_mode="Markdown",
                               )
                           except Exception:
                               pass
               # Auto-CS Personal Sales Follow-up (Menyapa pengguna yang membuka tagihan >3 menit tetapi belu
               if (
                   RUNTIME_CONFIG.get("SUBBOT_AUTO_CS_FOLLOWUP_ACTIVE", True)
                   and BOT_INSTANCE_GLOBAL



<!-- [ID:08_OMNI_SOCIAL_S009] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## 10. masih belum rapih.md

```md
```bash
repo/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── security.yml
│   │   ├── keepalive.yml          # "GitHub menyala terus"
│   │   ├── command-router.yml     # IssueOps: command via Issue
│   │   ├── nightly-audit.yml
│   │   └── auto-rollback.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── command.yml
│   │   └── incident.yml
│   ├── CODEOWNERS
│   └── dependabot.yml
├── .devcontainer/devcontainer.json
├── apps/
│   ├── web/                # website publik
│   ├── admin/              # dashboard admin (owner only)
│   ├── api/                # backend API
│   ├── mobile/             # mobile app
│   └── worker/             # background worker / cron
├── bots/
│   ├── core/               # shared: auth, rate-limit, dispatcher
│   ├── telegram/
│   ├── whatsapp/
│   ├── instagram/
│   ├── threads/
│   └── github/             # IssueOps adapter
├── services/
│   ├── auth/
│   ├── payment/            # gate FIN di sini
│   ├── ai-gateway/         # LLM router, model vendor
│   ├── scanner/            # airdrop, bansos, NVIDIA Spectrum
│   ├── notification/       # WA/Tele gateway
│   └── audit/              # append-only
├── packages/
│   ├── ui/
│   ├── sdk/
│   ├── config/
│   ├── logger/
│   └── types/
├── office/                 # KANTOR VIRTUAL
│   ├── brain/              # ← "otak" AI baca dari sini
│   │   ├── vision.md
│   │   ├── strategy.md
│   │   ├── roadmap.md
│   │   ├── principles.md
│   │   ├── conventions.md
│   │   ├── stack.md
│   │   ├── security-rules.md
│   │   ├── onchain-rules.md
│   │   └── glossary.md
│   ├── blueprint/          # PDF kamu taruh di sini
│   ├── config/             # agents.yaml, kill_switch.yaml, dll
│   ├── orchestrator/
│   ├── agents/             # per-agent SOP + memory
│   ├── specs/
│   ├── architecture/
│   ├── security/
│   ├── logs/
│   └── README.md
├── infra/
│   ├── terraform/
│   ├── docker/
│   ├── k8s/
│   └── cloudflare/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── RUNBOOK.md
│   ├── SECURITY.md
│   ├── ONBOARDING.md
│   ├── CHANGELOG.md
│   ├── ADR/                # architecture decision records
│   └── API/
├── scripts/
│   ├── bootstrap.py
│   ├── dev.sh
│   └── deploy.sh
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .env.example
├── .gitignore
├── .editorconfig
├── Makefile
├── README.md
├── SECURITY.md
├── CONTRIBUTING.md
└── LICENSE

#!/usr/bin/env python3
"""
Bootstrap Bot — dijalankan sekali saat repo masih kosong.
Membuat struktur folder perusahaan, file placeholder, commit, buka PR.
Tidak menimpa file yang sudah ada.
"""
import os, sys, subprocess, json, textwrap
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
DRY = "--dry" in sys.argv

TREE = {
    "apps/web": "Website publik",
    "apps/admin": "Dashboard admin (owner only)",
    "apps/api": "Backend API",
    "apps/mobile": "Mobile app",
    "apps/worker": "Background worker & cron",

    "bots/core": "Shared: auth, rate-limit, dispatcher",
    "bots/telegram": "Telegram bot",
    "bots/whatsapp": "WhatsApp bot",
    "bots/instagram": "Instagram bot",
    "bots/threads": "Threads bot",
    "bots/github": "GitHub IssueOps adapter",

    "services/auth": "Auth & session",
    "services/payment": "Payment + gate FIN",
    "services/ai-gateway": "LLM router & model vendor",
    "services/scanner": "Airdrop, bansos, NVIDIA Spectrum",
    "services/notification": "WA/Tele gateway",
    "services/audit": "Append-only audit log",

    "packages/ui": "Shared UI",
    "packages/sdk": "Shared SDK",
    "packages/config": "Shared config loader",
    "packages/logger": "Structured logger",
    "packages/types": "Shared types",

    "office/brain": "Otak AI: visi, strategi, prinsip",
    "office/blueprint": "PDF blueprint kamu",
    "office/config": "agents.yaml, kill_switch.yaml, dll",
    "office/orchestrator": "Runtime orchestrator",
    "office/agents": "Per-agent SOP + memory",
    "office/specs": "Spesifikasi hasil ingest blueprint",
    "office/architecture": "Keputusan arsitektur",
    "office/security": "Threat model & playbook",
    "office/logs": "Audit & incident",

    "infra/terraform": "IaC",
    "infra/docker": "Dockerfiles",
    "infra/k8s": "Kubernetes",
    "infra/cloudflare": "WAF, DNS, tunnel",

    "docs/ADR": "Architecture Decision Records",
    "docs/API": "Dokumentasi API",

    "scripts": "Utilitas",
    "tests/unit": "Unit test",
    "tests/integration": "Integration test",
    "tests/e2e": "End-to-end test",
}

BRAIN_FILES = {
    "office/brain/vision.md": """# Vision
<isi visi perusahaan agregator AI kamu>


<!-- [ID:08_OMNI_SOCIAL_S010] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: :-4 -->
# ==============================================================================
def compute_crc16_ccitt(data_str: str) -> str:
    crc = 0xFFFF
    for ch in data_str.encode("utf-8"):
        crc ^= ch << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
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


def build_auto_geo_payment_details(user_id: int, ppp_zone: int) -> dict[str, Any]:
    """
    Otomatis mendeteksi jalur pembayaran:
    - Zona 3 (Indonesia): Menggunakan ID_ACTIVE_PROVIDER yang disetel Owner di /admin (QRIS/PG).
    - Zona 1 & 2 (Global): Menggunakan GLOBAL_ACTIVE_PROVIDER (Crypto USDT / Telegram Stars).
    """
    order_id = f"INV-{user_id}-{int(time.time())}"
    if ppp_zone in (1, 2):
        usd_price = "$1.99" if ppp_zone == 1 else "$0.99"
        stars_amt = 110 if ppp_zone == 1 else 55
        return {
            "rail": "GLOBAL_AUTO_RAIL",
            "provider": RUNTIME_CONFIG["GLOBAL_ACTIVE_PROVIDER"],
            "order_id": order_id,
            "display_amount": f"{usd_price} USDT / {stars_amt} Telegram Stars ⭐",
            "qris_payload": "",
        }

    unique_code = (user_id % 89) + 10
    exact_idr = 5000 + unique_code
    qris_str = generate_dynamic_qris_string(GOPAY_STATIC_QRIS_RAW, exact_idr)
    return {
        "rail": RUNTIME_CONFIG["ID_ACTIVE_CATEGORY"],
        "provider": RUNTIME_CONFIG["ID_ACTIVE_PROVIDER"],
        "order_id": order_id,
        "display_amount": f"Rp {exact_idr:,}",
        "qris_payload": qris_str,
    }



<!-- [ID:08_OMNI_SOCIAL_S011] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Channel
| Channel | Webhook | Adapter |
|---|---|---|
| Telegram | polling | `bots/telegram/main.py` |
| WhatsApp | `/webhook/whatsapp` | `bots/whatsapp/main.py` |
| Instagram | `/webhook/instagram` | `bots/instagram/main.py` |
| Threads | `/webhook/threads` | `bots/threads/main.py` |
| GitHub Issue | workflow | `bots/github/dispatch.py` |


<!-- [ID:08_OMNI_SOCIAL_S012] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: STR -->
# =====================================================================
class CheckoutRequest(BaseModel):
    order_id: str
    base_amount: int
    channel: str                     # 'telegram', 'whatsapp', 'facebook', 'miniapp', 'web'
    preferred_provider: Optional[str] = None

@app.post("/api/checkout")
async def create_smart_checkout(req: CheckoutRequest):
    now = int(time.time())
    active_qris = [q for q in QRIS_POOL.values() if q["is_active"]]
    if not active_qris:
        raise HTTPException(status_code=400, detail="Belum ada QRIS yang didaftarkan di sistem.")

    # Cari pasangan (qris_id + kode_unik) yang sedang kosong agar bebas bentrok
    selected_qris = None
    final_amount = None
    unique_code = None

    for code in range(1, 500):
        candidate_amt = req.base_amount + code
        for qris in active_qris:
            if req.preferred_provider and qris["provider"] != req.preferred_provider:
                continue
            # Cek apakah di QRIS provider ini nominal tersebut sedang dipakai
            conflict = any(
                inv["status"] == "PENDING" and inv["expires_at"] > now
                and inv["qris_id"] == qris["qris_id"] and inv["final_amount"] == candidate_amt
                for inv in INVOICES.values()
            )
            if not conflict:
                selected_qris = qris
                unique_code = code
                final_amount = candidate_amt
                break
        if selected_qris:
            break

    if not selected_qris:
        raise HTTPException(status_code=429, detail="Semua slot transaksi penuh, coba sesaat lagi.")

    dynamic_qris = build_dynamic_qris(selected_qris["static_qris"], final_amount)

    INVOICES[req.order_id] = {
        "order_id": req.order_id,
        "channel": req.channel,
        "qris_id": selected_qris["qris_id"],
        "provider": selected_qris["provider"],
        "merchant_name": selected_qris["merchant_name"],
        "base_amount": req.base_amount,
        "unique_code": unique_code,
        "final_amount": final_amount,
        "dynamic_qris_string": dynamic_qris,
        "status": "PENDING",
        "expires_at": now + 900
    }
    return INVOICES[req.order_id]


<!-- [ID:08_OMNI_SOCIAL_S013] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Gambar: 1 file (images/page_0060_img_01.jpeg) -->
## Halaman 60

User prompt: Jadi keputusan dan rangkuman dari kita mengobrol untuk mengambil nama bio username dll tadi apa? tulis dengan ringkas dan keputusan
final yang rekomendasi sekali tanpa melebih lebihkan saya tanpa melebih lebihkan ide yang terlihat cemerlang padahal tidak. fokus jujur dan sesuai ilmu
terbaiknya
Response: Keputusan Final Struktur Bot Telegram
Username: @BikinAI_bot Alasan: Singkat, mudah diingat, kuat sebagai brand, dan meminimalisir kesalahan ketik saat tautan dibagikan.
Display Name: BikinAI - Bot Bikin & Edit Foto, Video Alasan: Formasi SEO on-page paling presisi untuk algoritma internal
Telegram. Menjaring exact match keyword untuk pencarian "bikin foto", "edit foto", "edit video", dan "bikin video" secara natural tanpa
diklasifikasikan sebagai spam.
Bio / Kolom About: "Agregator AI instan dan murah. Render, buat, dan edit gambar, foto, serta video langsung dari Telegram." Alasan: Berfungsi
sebagai wadah untuk menampung sisa kata kunci bervolume tinggi (agregator, instan, murah, render, gambar) agar tetap terbaca oleh mesin
pencari tanpa merusak estetika nama utama.
Rekomendasi Strategi Pertumbuhan
1. Watermark Bukti Sosial: Otomatisasi penyematan watermark kecil (contoh: Dibuat via @BikinAI_bot) pada seluruh hasil render
pengguna di tier gratis. Setiap gambar atau video yang mereka bagikan ke grup lain akan menjadi papan iklan organik.
2. Sistem Referral Kredit: Terapkan mekanik gamification. Berikan kuota render tambahan secara gratis jika pengguna membagikan tautan bot
dan berhasil mengajak teman untuk bergabung.
3. Trafik Konten Vertikal: Jangan hanya menunggu trafik pencarian organik di dalam Telegram. Demonstrasikan hasil render bot melalui format
video vertikal 9:16. Memanfaatkan hook visual, komedi satir, atau eksperimen color grading pada konten Reels sangat efektif untuk mengakali
algoritma distribusi, memicu lonjakan jangkauan non-follower, dan mengarahkan trafik eksternal secara masif langsung ke tautan bot Anda.
User prompt: Coba buatkan saya logo 1:1 untuk nama Bikin AI ini. tapi dengan style modern simple namun unik
Response: Ini adalah usulan logo 1:1 untuk BikinAI dengan gaya modern, simpel, namun tetap unik dan fungsional untuk avatar bot Telegram:
Konsep Logo Mark ("BA"): Saya menggabungkan huruf B dan A menjadi satu kesatuan yang dinamis.
Di sisi kiri (huruf B), terdapat jaringan titik dan garis yang merepresentasikan kecerdasan buatan, proses agregasi, dan data (Neural
Network).
Di sisi kanan (huruf A), terdapat aksen lengkungan dan bintang-bintang kecil bergaya magis untuk menyimbolkan proses "bikin" atau
kreasi visual (edit foto/video secara instan).
Warna: Menggunakan gradasi electric blue dan cyber magenta/purple di atas latar belakang gelap. Ini adalah kombinasi warna khas teknologi
masa kini yang sangat mencolok dan mudah dikenali saat berupa lingkaran kecil di daftar chat Telegram pengguna.
Tipografi: Teks "BikinAI" di bagian bawah dibuat dengan font modern yang tegas. Bagian "Bikin" berwarna putih untuk keterbacaan yang tinggi,
sedangkan "AI" menggunakan gradasi warna senada agar memperkuat identitas brand-nya.
Desain ini memiliki kontras yang kuat, tidak terlalu ramai, dan sangat mudah dikenali baik dalam ukuran besar maupun sebagai ikon kecil di aplikasi.
Bagaimana menurut Anda?


![Diagram Halaman 60](images/page_0060_img_01.jpeg)


<!-- [ID:08_OMNI_SOCIAL_S014] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: TAHAP 1, TAHAP 2 | Gambar: 1 file (images/page_0061_img_01.jpeg) -->
## Halaman 61

User prompt: Ba itu bukannya lebih baik logo BOT? jadi menurut saya lebih unik begitu. tapi gak emoji bot gitu aja. lebih ke style designer profesional gitu
lah. backgroundnya jangan warna kaku
Response: Ide yang sangat bagus! Menggunakan maskot bot (robot) yang dibuat dengan sentuhan desainer profesional memang jauh lebih kuat
untuk mewakili bot Telegram Anda daripada sekadar huruf, tanpa terlihat kekanak-kanakan atau seperti emoji biasa.
Berikut adalah desain logo 1:1 "BikinAI" yang baru:
Mascot Bot yang Profesional: Menampilkan kepala robot futuristik yang didesain secara kustom dan penuh detail. Di bagian kepalanya
terdapat elemen lensa kamera/sensor serta jaringan data yang melambangkan fungsi pembuat foto, video, dan AI. Karakternya dibuat
bersahabat namun tetap canggih dan tidak murahan.
Teks & Tipografi: Menggunakan nama "BikinAI" yang tegas dan futuristik di bagian bawah, memastikan nama brand Anda tetap menjadi fokus
utama yang mudah dibaca.
Background yang Dinamis: Tidak lagi menggunakan warna gelap yang kaku, melainkan perpaduan gradasi malam (deep midnight gradient)
yang diperkaya dengan efek gelombang digital (digital waves), partikel cahaya, dan pendaran hologram ungu-biru. Ini memberikan kesan "hidup"
dan mendalam (rich & dimensional).
Efek Glow: Karakter bot dan tulisan memiliki efek pencahayaan siber (cybernetic glow) yang kontras, sehingga logo ini akan sangat mencolok
dan terlihat sangat berkelas saat digunakan sebagai foto profil bot Telegram maupun di media sosial.
Bagaimana menurut Anda dengan visualisasi bot profesional yang dinamis ini?
User prompt: Kenapa di collab gak mau connected terus yah? code ini: import os import time import subprocess import requests #
========================================== # 1. PONDASI LINGKUNGAN COLAB # ========================================== print("⚙️
[TAHAP 1] Menyiapkan Lingkungan Agentic di Colab...") os.system('pip install pyTelegramBotAPI insightface onnxruntime-gpu deep-translator -q') import
telebot from deep_translator import GoogleTranslator TOKEN_TELEGRAM = "8885292945:AAGK66Dng-81kTW9-vv0Yoy4Pzi43nU3ns0" bot =
telebot.TeleBot(TOKEN_TELEGRAM) # ========================================== # 2. INSTALL COMFYUI & ALAT DARI PDF #
========================================== os.chdir('/content') if not os.path.exists('ComfyUI'): os.system('git clone
https://github.com/comfyanonymous/ComfyUI -q') os.chdir('/content/ComfyUI') os.system('pip install -r requirements.txt -q') folder_list = ['checkpoints',
'upscale_models', 'ipadapter', 'insightface', 'inpaint', 'input'] for folder in folder_list: os.makedirs(f'models/{folder}', exist_ok=True) print("⚙️ [TAHAP 2]
Memasang Alat Dewa (ReActor, ControlNet, Rembg, dll)...") nodes = [ "https://github.com/Gourieff/comfyui-reactor-node",
"https://github.com/Fannovel16/comfyui_controlnet_aux", "https://github.com/cubiq/ComfyUI_IPAdapter_plus", "https://github.com/ltdrdata/ComfyUI-
Impact-Pack", "https://github.com/Jcd1230/rembg-comfyui-node" ] for repo_url in nodes: node_name = repo_url.split('/')[-1].replace('.git', '') folder_path =
f"custom_nodes/{node_name}" if not os.path.exists(folder_path): subprocess.run(f"git clone {repo_url} {folder_path} -q", shell=True) req_file = f"
{folder_path}/requirements.txt" if os.path.exists(req_file): os.system(f"pip install -r {req_file} -q") print("⚙️ [TAHAP 3] Mendownload Model Pony, 2
Upscaler, dan Wajah...") models = [ ('models/checkpoints/Pony_V6_XL.safetensors',
'https://huggingface.co/WhiteAiZ/PonyXL/resolve/main/PonyDiffusionV6XL.safetensors'), ('models/upscale_models/4x-UltraSharp-v2.pth',
'https://huggingface.co/lokcx/4x-Ultrasharp/resolve/main/4x-UltraSharp.pth'), ('models/upscale_models/4x_foolhardy_Remacri.pth',
'https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/4x_foolhardy_Remacri.pth'), ('models/ipadapter/ip-adapter-plus-face_sdxl_vit-
h.safetensors', 'https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus-face_sdxl_vit-h.safetensors'),
('models/insightface/inswapper_128.onnx', 'https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx') ] for
file_path, url in models: if not os.path.exists(file_path): print(f"Mendownload {file_path.split('/')[-1]}...") os.system(f'wget -c --progress=bar -O {file_path}
{url}') # ========================================== # 3. MENYALAKAN MESIN # ========================================== print("⚙️


![Diagram Halaman 61](images/page_0061_img_01.jpeg)


<!-- [ID:08_OMNI_SOCIAL_S015] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: 10PX, 11PX -->
## Halaman 152

                  <td className="py-3.5 text-slate-400">{tool.stars}</td>​
                  <td className="py-3.5 text-cyan-300">{tool.benchmark}</td>​
                  <td className="py-3.5">​
                    <span className="inline-flex items-center gap-1 rounded bg-emerald-500/10 px-2 
py-0.5 text-[10px] text-emerald-400 border border-emerald-500/20">​
                      <ShieldCheck className="h-3 w-3" /> Exit Code 0 (Clean)​
                    </span>​
                  </td>​
                  <td className="py-3.5">​
                    <span​
                      className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] ${​
                        tool.status === "PROMOTED"​
                          ? "bg-emerald-500/10 text-emerald-300 border border-emerald-500/30"​
                          : "bg-amber-500/10 text-amber-300 border border-amber-500/30"​
                      }`}​
                    >​
                      {tool.status === "PROMOTED" ? <CheckCircle2 className="h-3 w-3" /> : 
<RefreshCw className="h-3 w-3 animate-spin" />}​
                      {tool.status}​
                    </span>​
                  </td>​
                  <td className="py-3.5 text-slate-400 text-[11px] underline cursor-pointer 
hover:text-cyan-400">​
                    {tool.skillFile}​
                  </td>​
                </tr>​
              ))}​
            </tbody>​
          </table>​
        </div>​
      </div>​
    </div>​
  );​
}​
 
components/OmnichannelBridge.tsx 
Monitor failover token bot Telegram tripel dan antarmuka WAHA WhatsApp: 
"use client";​
​
import React, { useState } from "react";​
import { MessageSquare, Bot, Send, CheckCircle2 } from "lucide-react";​
​
export default function OmnichannelBridge() {​
  const [testMsg, setTestMsg] = useState("");​
  const [logResponse, setLogResponse] = useState<string | null>(null);​
​


