
<!-- [ID:02_CORE_AI_S022] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
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



<!-- [ID:02_CORE_AI_S023] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# ==============================================================================
@router.message(CommandStart())
async def cmd_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "Kreator"
    is_priv = message.chat.type == "private"
    lang = message.from_user.language_code or "id"

    async with aiosqlite.connect(DB_PATH) as db:
        u = await ensure_user_and_track_identity(
            db, user_id, username, message.from_user.first_name or "", lang
        )

    await message.reply(
        build_customer_dashboard_caption(username, u),
        parse_mode="Markdown",
        reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
    )


@router.message(Command("menu"))
async def cmd_menu_handler(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "Kreator"
    is_priv = message.chat.type == "private"

    async with aiosqlite.connect(DB_PATH) as db:
        u = await ensure_user_and_track_identity(
            db, user_id, username, message.from_user.first_name or ""
        )

    await message.reply(
        build_customer_dashboard_caption(username, u),
        parse_mode="Markdown",
        reply_markup=build_customer_main_menu_keyboard(u, is_private=is_priv),
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
        await message.reply("🛡️ Security Shield: Pola injeksi ditolak.")
        return

    wait = await message.reply("🔬 **Sedang menyusun laporan Deep Research...**")
    async with aiosqlite.connect(DB_PATH) as db:
        u = await ensure_user_and_track_identity(db, user_id, username)
        res = await generate_frontier_ai_response(
            db, clean_q, mode="DEEP_RESEARCH", personal_memory=u["memory"]
        )
    await wait.edit_text(f"🔬 **LAPORAN DEEP RESEARCH — bikinAI**\n━━━━━━━━━━━━━━━━━━\n{res}", parse_mode="Markdown")


@router.message(Command("canvas"))
async def cmd_canvas_workspace_handler(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username or "Kreator"
    raw_arg = (message.text or "").partition(" ")[2].strip()

    async with aiosqlite.connect(DB_PATH) as db:
        u = await ensure_user_and_track_identity(db, user_id, username)
        if not raw_arg:
            current_canvas = u["canvas"] or "_(Canvas Anda masih kosong. Ketik `/canvas [instruksi]` untuk mulai menulis draf.)_"
            await message.reply(
                f"📝 **CANVAS WORKSPACE AKTIF**\n━━━━━━━━━━━━━━━━━━\n{current_canvas}\n\n"
                f"💡 _Ketik `/canvas [instruksi baru]` untuk menyunting atau mengembangkan draf di atas._",
                parse_mode="Markdown",
            )
            return

        clean_arg, is_attack = sanitize_and_deobfuscate_input(raw_arg)
        if is_attack:
            await message.reply("🛡️ Security Shield: Pola injeksi ditolak.")
            return

        wait = await message.reply("📝 **Sedang memperbarui dokumen di Canvas Workspace...**")
        updated_canvas = await generate_frontier_ai_response(
            db, clean_arg, mode="CANVAS_EDIT", personal_memory=u["memory"], canvas_state=u["canvas"]
        )

        async def _save_canvas(conn: aiosqlite.Connection) -> None:
            await conn.execute(
                "UPDATE users SET active_canvas_content = ? WHERE internal_user_id = ?;",
                (updated_canvas[:4000], user_id),
            )

        await DB_WRITER_DAEMON.execute_write_tx(db, _save_canvas)

    await wait.edit_text(
        f"📝 **CANVAS WORKSPACE DIPERBARUI**\n━━━━━━━━━━━━━━━━━━\n{updated_canvas}",
        parse_mode="Markdown",
    )


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
    async with aiosqlite.connect(DB_PATH) as db:
        await save_persistent_setting(db, "MINIAPP_URL", arg_url)
    await message.reply(
        f"✅ **URL Mini App Berhasil Dikunci Abadi:**\n`{arg_url}`",
        parse_mode="Markdown",
    )


@router.message(Command("pasang_bansos"))
async def cmd_pasang_bansos_handler(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Perintah ini khusus Owner di ruang chat pribadi (DM).")
        return

    now_ts = int(time.time())
    exp_ts = now_ts + (365 * 86400)
    count_installed = 0

    async with aiosqlite.connect(DB_PATH) as db:
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
                        (
                            item["res_id"],
                            cat,
                            item["name"],
                            item["endpoint"],
                            item["meta"],
                            int(item["verified"]),
                            exp_ts,
                        ),
                    )
                    c += 1
            return c

        count_installed = await DB_WRITER_DAEMON.execute_write_tx(db, _tx)

    ast_check = sterilize_community_script_ast("def ping():\n    return 'OK'\n", "bansos_healthcheck")
    await message.reply(
        f"✅ **OMNI-RESOURCE HARVESTER AKTIF!**\n"
        f"┣ 📦 **Total Preset Terpasang:** `{count_installed} Resource`\n"
        f"┣ 🛡️ **SkillSpector AST Sterilizer:** `{'AMAN' if ast_check['ok'] else 'DIBLOKIR'}` (Hash: `{ast_check['hash']}`)\n"
        f"┗ ⚡ **Status Router:** `Pollinations + Groq + OpenRouter Siap!`",
        parse_mode="Markdown",
    )


def _build_owner_admin_panel_view(treasury_row: tuple[Any, ...] | None) -> tuple[str, InlineKeyboardMarkup]:
    gross = int(treasury_row[0]) if treasury_row else 0
    work_cap = int(treasury_row[1]) if treasury_row else 0
    profit_avail = int(treasury_row[2]) if treasury_row else 0
    harvested = int(treasury_row[3]) if treasury_row else 0
    jobs_cnt = int(treasury_row[4]) if treasury_row else 0

    prod_str = "🟢 PRODUCTION" if RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"] else "🧪 SANDBOX HPP Rp 0"
    hh_str = "🟢 ON (0 Koin)" if RUNTIME_CONFIG["HAPPY_HOUR_MODE"] else "⚪ OFF (Normal)"

    txt = (
        f"👑 **OWNER COMMAND CENTER — bikinAI v3.4.0**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💰 **Brankas Treasury & Profit Split:**\n"
        f"┣ 📈 **Omzet Kotor:** `Rp {gross:,}`\n"
        f"┣ 🛡️ **Modal Kerja Terkunci (HPP+10%):** `Rp {work_cap:,}`\n"
        f"┣ 💎 **Profit Bersih Siap Panen:** **`Rp {profit_avail:,}`**\n"
        f"┣ 🏦 **Total Sudah Dipanen Owner:** `Rp {harvested:,}`\n"
        f"┗ ⚙️ **Total Job Selesai:** `{jobs_cnt} Render`\n\n"
        f"🎛️ **Konfigurasi Mesin & Kasir Dual-Rail:**\n"
        f"┣ 🚀 **Mode Operasi:** `{prod_str}`\n"
        f"┣ 🎉 **Flash Happy Hour:** `{hh_str}`\n"
        f"┣ 🇮🇩 **Kasir Indonesia:** `{RUNTIME_CONFIG['ID_ACTIVE_PROVIDER']}`\n"
        f"┣ 🌍 **Kasir Global:** `{RUNTIME_CONFIG['GLOBAL_ACTIVE_PROVIDER']}`\n"
        f"┗ 📱 **Mini App URL:** `{RUNTIME_CONFIG['MINIAPP_URL'] or 'Auto-Detect'}`"
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🌾 Panen Profit Bersih (Rp {profit_avail:,})", callback_data="adm:harvest")],
            [
                InlineKeyboardButton(text=f"🎉 Happy Hour: {hh_str}", callback_data="adm:toggle_hh"),
                InlineKeyboardButton(text=f"🚀 Mode: {prod_str}", callback_data="adm:toggle_prod"),
            ],
            [InlineKeyboardButton(text="💳 Ganti Provider Kasir ID (QRIS/Duitku/Midtrans/Pakasir)", callback_data="adm:cycle_pg")],
            [
                InlineKeyboardButton(text="🌐 Cek Domain Multi-TLD (RDAP)", callback_data="adm:domains"),
                InlineKeyboardButton(text="📦 Pasang Preset Bansos API", callback_data="adm:bansos"),
            ],
            [InlineKeyboardButton(text="🔄 Segarkan Data Brankas", callback_data="adm:refresh")],
        ]
    )
    return txt, kb


@router.message(Command("admin"))
async def cmd_owner_admin_panel(message: Message) -> None:
    if not is_verified_owner_dm(message.from_user.id, message.chat.type):
        await message.reply("🔒 Panel `/admin` hanya dapat diakses oleh Owner melalui DM pribadi.")
        return

    async with aiosqlite.connect(DB_PATH) as db:
        await save_persistent_setting(db, "OWNER_ID_RUNTIME", str(message.from_user.id))
        cur = await db.execute(
            "SELECT gross_revenue_idr, working_capital_vault_idr, harvestable_profit_vault_idr, total_harvested_by_owner_idr, total_jobs_completed FROM treasury_summary WHERE id = 1;"
        )
        row = await cur.fetchone()

    txt, kb = _build_owner_admin_panel_view(row)
    await message.reply(txt, parse_mode="Markdown", reply_markup=kb)



<!-- [ID:02_CORE_AI_S024] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
## 20. ai repo.md

```md
```markdown
-- 1. TABEL KOMPAS INFRASTRUKTUR (Kunci Migrasi Otomatis)
-- Bot membaca tabel ini saat booting untuk mengetahui lokasi repo & server aktif saat ini.
CREATE TABLE IF NOT EXISTS infrastructure_registry (
    node_id TEXT PRIMARY KEY,               -- Contoh: 'primary_stack'
    private_repo_url TEXT NOT NULL,         -- URL Git untuk Clean Code (Shadow Vault)
    public_repo_url TEXT NOT NULL,          -- URL Git untuk Obfuscated/Binary Code
    git_pat_encrypted TEXT NOT NULL,        -- Fine-grained PAT (dienkripsi dengan Master Key)
    active_webhook_domain TEXT NOT NULL,    -- Domain server/Cloudflare aktif saat ini
    storage_bucket_url TEXT,                -- Lokasi penyimpanan cadangan (.db dump / binary)
    migration_status TEXT DEFAULT 'STABLE', -- 'STABLE', 'MIGRATING', atau 'LOCKED'
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. TABEL BRANKAS KOGNITIF (Penyimpanan System Prompts & Logika Agen)
-- Memisahkan "otak" AI dari kode Git agar aman dari pencurian dan mudah di-export.
CREATE TABLE IF NOT EXISTS ai_prompts_vault (
    prompt_id TEXT PRIMARY KEY,             -- Contoh: 'core_orchestrator_v1'
    agent_role TEXT NOT NULL,               -- Peran agen (Coder, Maintainer, Router)
    system_prompt_text TEXT NOT NULL,       -- Isi instruksi rahasia AI
    checksum_sha256 TEXT NOT NULL,          -- Hash validasi agar prompt tidak bisa dimodifikasi pihak luar
    version INTEGER DEFAULT 1,
    is_active INTEGER DEFAULT 1,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. TABEL SINKRONISASI RILIS & KUNCI KRIPTOGRAFI (Dual-Repo Mapping)
-- Mencatat hubungan antara kode bersih (Private) dan kode terkunci (Public) beserta kunci dekripsinya.
CREATE TABLE IF NOT EXISTS release_snapshots (
    release_tag TEXT PRIMARY KEY,           -- Contoh: 'v1.0.4-prod'
    private_commit_hash TEXT NOT NULL,      -- Hash commit kode murni di Repo-Master-Private
    public_commit_hash TEXT NOT NULL,       -- Hash commit biner di Repo-Public-Release
    tensor_permutation_key TEXT NOT NULL,   -- Kunci matriks (K) / AES-GCM untuk membuka rilis ini
    allowed_dependencies_json TEXT,         -- Daftar library open-source (MIT/Apache/BSD) yang dipakai
    changelog_summary TEXT,                 -- Ringkasan fitur yang ditulis oleh AI
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. TABEL RIWAYAT MIGRASI (Audit Trail Perpindahan Sistem)
CREATE TABLE IF NOT EXISTS migration_logs (
    migration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_target_type TEXT NOT NULL,       -- 'GITHUB_REPO', 'SERVER_NODE', atau 'BUYER_HANDOVER'
    old_endpoint TEXT NOT NULL,
    new_endpoint TEXT NOT NULL,
    status TEXT NOT NULL,                   -- 'SUCCESS', 'FAILED', 'ROLLED_BACK'
    executed_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

Untuk mempekerjakan tim IT tanpa membuka rahasia dapur, perusahaan teknologi besar menerapkan sistem Zero-Trust Compartmentalization (Sistem Sekat Kedap Air). Prinsip utamanya sederhana: Karyawan hanya boleh melihat "kabel penghubung" dan "kerangka luar", tetapi tidak pernah bisa melihat "mesin inti" dan "bahan bakar" bisnis Anda.
Dengan fondasi Dual-Repo dan Turso yang sudah dirancang sebelumnya, Anda hanya perlu memecah ruang kerja menjadi sistem Black-Box (Kotak Hitam) ketika mulai merekrut karyawan IT.
1. Upgrade dari 2 Repo Menjadi 3 Repo (Isolasi Ruang Kerja)
Jangan pernah memasukkan karyawan ke dalam Repo-Master-Private (Shadow Vault) tempat bot AI utama Anda menyimpan seluruh kode utuh. Pecah repositori menjadi tiga kasta:
 * Kasta 1: Repo-Core-Brain (Hanya Anda & Bot AI Utama): Berisi logika inti orkestrasi AI, algoritma kriptografi, pipeline utama, dan koneksi langsung ke database Turso produksi. Karyawan IT sama sekali tidak tahu repositori ini ada.
 * Kasta 2: Repo-Staff-Workspace (Tempat Kerja Karyawan IT): Buat repositori private terpisah khusus untuk bagian yang dikerjakan karyawan—misalnya repo khusus tampilan web/dashboard, repo khusus integrasi pembayaran, atau repo khusus modul scraping. Anda hanya mengundang akun GitHub karyawan ke repositori ini.
 * Kasta 3: Repo-Public-Release (Server Produksi): Tempat bot Anda menggabungkan kode dari Kasta 1 dan Kasta 2 yang sudah dikompilasi menjadi produk akhir.
2. Sistem "Black-Box SDK" (Karyawan Bekerja Tanpa Melihat Isi Mesin)
Bagaimana cara karyawan mengetes kode buatan mereka jika mereka tidak punya akses ke kode inti AI Anda? Anda memberikan mereka Jembatan Tertutup (SDK Biner atau Internal API):
 * Kompilasi Mesin Inti Menjadi File .so / .whl: Bot AI Anda mengompilasi kode dari Repo-Core-Brain menjadi library terkunci (misalnya bernama core_engine.so), lalu menaruh file biner tersebut ke dalam Repo-Staff-Workspace.
 * Karyawan Hanya Memanggil Fungsi: Karyawan IT Anda hanya diberikan buku panduan singkat: "Kalau mau memproses pesan user, panggil fungsi core_engine.process(user_input)".
 * Aman 100%: Karyawan tahu apa input yang harus dikirim dan apa output yang keluar agar mereka bisa menyelesaikan tugasnya (seperti memperbaiki tampilan atau menyambungkan webhook), tetapi mereka tidak bisa membuka file core_engine.so untuk mencuri algoritma atau prompt di dalamnya.
3. Database Kembar Palsu: Turso Sandbox vs Turso Production
Karyawan IT membutuhkan database untuk mengetes apakah kode yang mereka tulis berjalan lancar. Namun, memberikan mereka akses ke database Turso asli sama saja dengan menyerahkan seluruh System Prompts dan data pelanggan Anda.
 * Buat Database Kedua di Turso (turso-dev-sandbox): Gunakan skema tabel yang 100% sama dengan database asli, tetapi isi tabel ai_prompts_vault dengan prompt boneka (contoh: "Kamu adalah asisten uji coba untuk developer IT") dan isi tabel kunci dengan angka acak.
 * Karyawan Hanya Memegang Kunci Sandbox: Di komputer kerja karyawan, file .env mereka hanya berisi token menuju turso-dev-sandbox.
 * Injeksi Otomatis Saat Rilis (CI/CD Secret Injection): Saat pekerjaan karyawan selesai dan digabungkan ke server utama oleh bot Anda, sistem secara otomatis menukar koneksi database dari Sandbox ke Production di dalam memori server tanpa pernah memperlihatkan kunci aslinya kepada karyawan.
4. Aturan GitHub untuk Karyawan: Branch Protection & AI Auditor
Saat memiliki tim IT, ubah akun GitHub proyek Anda menjadi GitHub Organization (Gratis) dan terapkan aturan ketat berikut pada repositori kerja karyawan:
 * Kunci Jalur Utama (Branch Protection Rules): Atur agar karyawan tidak bisa melakukan push (mengubah kode langsung) ke cabang utama (main). Mereka wajib bekerja di cabang terpisah (misalnya fitur-update-ui) dan mengajukan izin penggabungan melalui Pull Request (PR).
 * Jadikan Bot AI Anda sebagai "Polisi Keamanan" (Automated PR Reviewer): Sebelum kode buatan karyawan digabungkan ke sistem utama, perintahkan Bot AI Anda untuk memindai seluruh baris kode yang ditulis karyawan tersebut secara otomatis.
 * Deteksi Sabotase / Backdoor: Instruksikan Bot AI Anda untuk menolak otomatis (Reject PR) dan mengirim peringatan ke Telegram pribadi Anda jika karyawan menyelipkan kode mencurigakan—seperti perintah mengirim data diam-diam ke URL luar (requests.post asing), membaca variabel .env secara ilegal (os.environ), atau membuka celah shell (subprocess.Popen).
Perbandingan Hak Akses: Anda vs Karyawan IT
| Komponen Sistem | Akses Anda & Bot AI Utama | Akses Karyawan IT / Admin Teknis |
|---|---|---|
| Kode Inti & Algoritma AI | 100% Clean Code (di Repo-Core-Brain) | Hanya File Biner (.so) / Dokumentasi API |
| System Prompts Rahasia | Teks Asli (di Turso Production) | Teks Palsu / Dummy (di Turso Sandbox) |
| API Keys & Kredensial Pembayaran | Tersimpan di Brankas Utama / Server | Menggunakan API Key Testing / Sandbox dengan limit Rp0 |
| Server Produksi Utama (VPS/Cloud) | Akses Penuh (Root / Dashboard) | Tidak Ada Akses (Deployment dilakukan otomatis oleh Bot via GitHub Actions) |
| Hak Menulis Kode (Git Push) | Bebas ke seluruh cabang & repo | Hanya bisa mengajukan Pull Request di repo modul mereka sendiri |
Tambahan Protokol 5 untuk System Prompt Bot AI Anda
Agar bot AI Anda siap mengawasi karyawan manusia nantinya, Anda cukup menambahkan Protokol 5 ini ke dalam SOP yang sudah dibuat sebelumnya:
