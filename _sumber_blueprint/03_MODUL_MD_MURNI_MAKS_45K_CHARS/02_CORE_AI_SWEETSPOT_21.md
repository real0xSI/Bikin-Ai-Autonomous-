
<!-- [ID:02_CORE_AI_S020] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# Daftar istilah teknis internal yang DILARANG bocor ke layar konsumen SFW
FORBIDDEN_TECHNICAL_LEAK_TERMS = [
    "pollinations",
    "chutes.ai",
    "bittensor",
    "subnet 27",
    "abliterated",
    "hermes 4 405b",
    "sqlite",
    "traceback",
    "singlewritersqlitedaemon",
    "nullifier_hash",
]


def scan_customer_ui_for_leaks(ui_text: str) -> Dict[str, Any]:
    """
    Memindai teks/HTML layar konsumen untuk memastikan 100% bahasa konsumen
    dan tidak ada kebocoran istilah teknis internal.
    """
    low = (ui_text or "").lower()
    leaks = [term for term in FORBIDDEN_TECHNICAL_LEAK_TERMS if term in low]
    return {
        "is_clean": len(leaks) == 0,
        "leaks_found": leaks,
        "checked_length": len(ui_text or ""),
    }


MINIAPP_FULL_WEBSITE_HTML: str = """\x3c!DOCTYPE html>
\x3chtml lang="id">
\x3chead>
  \x3cmeta charset="UTF-8" />
  \x3cmeta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  \x3ctitle>bikinAI Studio Kreatif — Foto, Video & Suara HD\x3c/title>
  \x3cscript src="https\x3a//telegram.org/js/telegram-web-app.js">\x3c/script>
  \x3cstyle>
    :root {
      --bg: #0b1020;
      --card: #151d36;
      --accent: #4f8cff;
      --accent-2: #00e5a3;
      --text: #f5f7ff;
      --muted: #9aa7c7;
      --border: rgba(255,255,255,0.12);
    }
    * { box-sizing: border-box; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    body { margin: 0; padding: 16px; background: var(--bg); color: var(--text); }
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
    .brand { font-size: 1.2rem; font-weight: 800; letter-spacing: -0.02em; }
    .badge { background: rgba(0,229,163,0.15); color: var(--accent-2); padding: 4px 10px; border-radius: 999px; font-size: 0.78rem; font-weight: 700; }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 14px; margin-bottom: 14px; }
    .section-title { font-size: 0.88rem; font-weight: 700; color: var(--muted); margin-bottom: 8px; text-transform: uppercase; }
    .pill-row { display: flex; flex-wrap: wrap; gap: 8px; }
    .pill {
      padding: 8px 13px; border-radius: 999px; border: 1px solid var(--border);
      background: rgba(255,255,255,0.04); color: var(--text); cursor: pointer;
      font-size: 0.85rem; font-weight: 600; transition: all 0.18s ease;
    }
    .pill.active { background: var(--accent); border-color: var(--accent); color: #fff; }
    .pill.locked { opacity: 0.38; pointer-events: none; filter: grayscale(1); }
    textarea {
      width: 100%; min-height: 92px; border-radius: 12px; border: 1px solid var(--border);
      background: rgba(0,0,0,0.28); color: var(--text); padding: 12px; font-size: 0.95rem;
    }
    .btn-primary {
      width: 100%; padding: 13px; border-radius: 12px; border: none;
      background: linear-gradient(135deg, var(--accent), #2b64e8);
      color: #fff; font-weight: 800; font-size: 0.98rem; cursor: pointer; margin-top: 10px;
    }
    .submenu { margin-top: 10px; padding-top: 10px; border-top: 1px dashed var(--border); }
    .community-list a { color: var(--accent-2); text-decoration: none; display: block; padding: 5px 0; font-size: 0.88rem; }
    .footer-links { font-size: 0.78rem; color: var(--muted); text-align: center; margin-top: 16px; }
  \x3c/style>
\x3c/head>
\x3cbody>
  \x3cdiv class="header">
    \x3cdiv class="brand">✨ bikinAI Studio Kreatif\x3c/div>
    \x3cdiv class="badge">Lisensi Bersih Tersedia\x3c/div>
  \x3c/div>

  \x3c!-- 1. Mode Utama (Exclusive Radio Group data-group="studio_mode") -->
  \x3cdiv class="card">
    \x3cdiv class="section-title">1. Pilih Mode Kreasi\x3c/div>
    \x3cdiv class="pill-row">
      \x3cbutton type="button" class="pill active" data-group="studio_mode" data-val="PHOTO_HD" onclick="selectExclusivePill(this)">📸 Buat Foto HD\x3c/button>
      \x3cbutton type="button" class="pill" data-group="studio_mode" data-val="VIDEO_CINEMATIC" onclick="selectExclusivePill(this)">🎬 Buat Video Sinematik\x3c/button>
      \x3cbutton type="button" class="pill" data-group="studio_mode" data-val="IMG2VID_MOTION" onclick="selectExclusivePill(this)">🖼️➡️🎞️ Gerakkan Foto (Img2Vid)\x3c/button>
      \x3cbutton type="button" class="pill" data-group="studio_mode" data-val="VOICE_STUDIO" onclick="selectExclusivePill(this)">🎙️ Suara Narator Jernih\x3c/button>
    \x3c/div>

    \x3c!-- Sub-Menu Preset Motion Awam (muncul otomatis saat Video / IMG2VID_MOTION aktif) -->
    \x3cdiv id="motionPresetBox" class="submenu" style="display:none;">
      \x3cdiv class="section-title">Gerakan Kamera & Subjek (Preset Mudah)\x3c/div>
      \x3cdiv class="pill-row">
        \x3cbutton type="button" class="pill active" data-group="motion_preset" data-val="SMOOTH_ZOOM" onclick="selectExclusivePill(this)">🔍 Kamera Maju Halus\x3c/button>
        \x3cbutton type="button" class="pill" data-group="motion_preset" data-val="CINEMATIC_PAN" onclick="selectExclusivePill(this)">🎥 Geser Sinematik\x3c/button>
        \x3cbutton type="button" class="pill" data-group="motion_preset" data-val="NATURAL_PORTRAIT" onclick="selectExclusivePill(this)">😊 Wajah Hidup & Tersenyum\x3c/button>
        \x3cbutton type="button" class="pill" data-group="motion_preset" data-val="PRODUCT_ORBIT" onclick="selectExclusivePill(this)">🛍️ Putar Produk 360°\x3c/button>
      \x3c/div>
    \x3c/div>
  \x3c/div>

  \x3c!-- 2. Peningkat Kualitas (Context-Aware Engine Locking) -->
  \x3cdiv class="card">
    \x3cdiv class="section-title">2. Peningkat Kualitas Otomatis\x3c/div>
    \x3cdiv class="pill-row">
      \x3cbutton type="button" id="pillPhotoSharpen" class="pill active" data-group="quality_enhancer" data-val="PHOTO_4K_HDR" onclick="selectExclusivePill(this)">✨ Pertajam Foto & Wajah 4K HDR\x3c/button>
      \x3cbutton type="button" id="pillPhotoRestore" class="pill" data-group="quality_enhancer" data-val="PHOTO_CLEANUP" onclick="selectExclusivePill(this)">🪄 Perbaiki Cahaya & Detail\x3c/button>
      \x3cbutton type="button" id="pillVideo4k60" class="pill locked" data-group="quality_enhancer" data-val="VIDEO_4K_60FPS" onclick="selectExclusivePill(this)">🎞️ Pertajam & Haluskan Video 4K 60FPS\x3c/button>
    \x3c/div>
  \x3c/div>

  \x3c!-- 3. Upload Foto Referensi & Ceritakan Ide -->
  \x3cdiv class="card">
    \x3cdiv class="section-title">3. Upload Foto Referensi (Opsional) & Tulis Ide\x3c/div>
    \x3cinput type="file" id="refImageInput" accept="image/*" style="margin-bottom: 10px; width: 100%; color: var(--muted);" />
    \x3ctextarea id="promptInput" placeholder="Contoh: Foto produk kopi susu kekinian di atas meja kayu hangat dengan cahaya pagi...">\x3c/textarea>
    \x3cbutton type="button" class="btn-primary" onclick="submitCreation()">🚀 Buat Karya Sekarang\x3c/button>
    \x3cdiv id="statusBox" style="margin-top:10px; font-size:0.88rem; color:var(--accent-2);">\x3c/div>
  \x3c/div>

  \x3c!-- 4. Panduan Cepat & Link Topik Komunitas -->
  \x3cdiv class="card">
    \x3cdiv class="section-title">📚 Panduan Singkat & Ruang Komunitas\x3c/div>
    \x3cp style="font-size:0.85rem; color:var(--muted); margin-top:0;">
      Gunakan Koin Utama mulai Rp 2.000 untuk hasil bersih 100% tanpa tanda air (watermark) dan siap dipakai jualan atau konten komersial.
    \x3c/p>
    \x3cdiv id="communityLinks" class="community-list">
      \x3ca href="https\x3a//t.me/bikinAI_komunitas" target="_blank">💬 Grup Diskusi & Inspirasi Kreator\x3c/a>
    \x3c/div>
  \x3c/div>

  \x3c!-- 5. Ketentuan Layanan (ToS) & Kebijakan Privasi -->
  \x3cdiv class="footer-links">
    \x3cstrong>Ketentuan Layanan & Privasi:\x3c/strong> Seluruh foto referensi dan dokumen pribadi Anda diproses melalui jalur terenkripsi pribadi dan tidak pernah dibagikan ke ruang publik.
  \x3c/div>

  \x3cscript>
    function selectExclusivePill(btn) {
      if (btn.classList.contains('locked')) return;
      const group = btn.getAttribute('data-group');
      document.querySelectorAll('.pill[data-group="' + group + '"]').forEach(el => el.classList.remove('active'));
      btn.classList.add('active');
      if (group === 'studio_mode') {
        applyContextAwareLocking(btn.getAttribute('data-val'));
      }
    }

    function applyContextAwareLocking(modeVal) {
      const isVideo = (modeVal === 'VIDEO_CINEMATIC' || modeVal === 'IMG2VID_MOTION');
      const motionBox = document.getElementById('motionPresetBox');
      const pSharpen = document.getElementById('pillPhotoSharpen');
      const pRestore = document.getElementById('pillPhotoRestore');
      const v4k60 = document.getElementById('pillVideo4k60');

      motionBox.style.display = isVideo ? 'block' : 'none';
      if (isVideo) {
        pSharpen.classList.add('locked');
        pSharpen.classList.remove('active');
        pRestore.classList.add('locked');
        pRestore.classList.remove('active');
        v4k60.classList.remove('locked');
        v4k60.classList.add('active');
      } else {
        pSharpen.classList.remove('locked');
        pRestore.classList.remove('locked');
        v4k60.classList.add('locked');
        v4k60.classList.remove('active');
        pSharpen.classList.add('active');
      }
    }

    async function submitCreation() {
      const modeEl = document.querySelector('.pill[data-group="studio_mode"].active');
      const qualEl = document.querySelector('.pill[data-group="quality_enhancer"].active');
      const motionEl = document.querySelector('.pill[data-group="motion_preset"].active');
      const prompt = document.getElementById('promptInput').value.trim();
      const statusBox = document.getElementById('statusBox');
      if (!prompt) {
        statusBox.textContent = 'Mohon tuliskan ide karya Anda terlebih dahulu.';
        return;
      }
      statusBox.textContent = 'Sedang menyiapkan karya terbaik untukmu...';
      const initData = (window.Telegram && window.Telegram.WebApp) ? window.Telegram.WebApp.initData : '';
      try {
        const res = await fetch('/api/webapp/execute', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            initData: initData,
            mode: modeEl ? modeEl.getAttribute('data-val') : 'PHOTO_HD',
            quality: qualEl ? qualEl.getAttribute('data-val') : 'PHOTO_4K_HDR',
            motion_preset: motionEl ? motionEl.getAttribute('data-val') : 'SMOOTH_ZOOM',
            prompt: prompt
          })
        });
        const data = await res.json();
        statusBox.textContent = data.message || 'Selesai! Silakan cek hasil di ruang obrolan Telegram.';
      } catch (e) {
        statusBox.textContent = 'Permintaan diterima. Silakan kembali ke layar utama Telegram.';
      }
    }

    fetch('/api/public/community-links').then(r => r.json()).then(d => {
      if (d.links && d.links.length) {
        const box = document.getElementById('communityLinks');
        box.innerHTML = d.links.map(l => `\x3ca href="${l.url}" target="_blank">📌 ${l.title}\x3c/a>`).join('');
      }
    }).catch(() => {});
  \x3c/script>
\x3c/body>
\x3c/html>
"""


def render_freedom_web_portal_html(portal_title: str = "NOCTURNE FREEDOM STUDIO v4.0") -> str:
    """
    Merender halaman `/unfiltered-portal` (Website futuristik profesional dengan nama yang
    dapat dikustomisasi via `/set_webname`):
    - Tab 1: Multi-Persona Unfiltered Chat dengan memori 12 giliran + ekspor .TXT
    - Tab 2: Direct Media Studio Image/Video/Img2Vid + tombol Download Langsung CDN `/api/cdn/download`
    - Tab 3: Dompet Voucher Ed25519 `VCH-...`
    - Tab 4: Vibe-Coder API Gateway & Dokumentasi Legal
    """
    safe_title = html.escape(portal_title or "NOCTURNE FREEDOM STUDIO v4.0")
    return f"""\x3c!DOCTYPE html>
\x3chtml lang="id">
\x3chead>
  \x3cmeta charset="UTF-8" />
  \x3cmeta name="viewport" content="width=device-width, initial-scale=1.0" />
  \x3ctitle>{safe_title}\x3c/title>
  \x3cstyle>
    :root {{
      --bg: #07060e;
      --panel: #121024;
      --neon: #c026d3;
      --cyan: #22d3ee;
      --text: #f8fafc;
      --muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; font-family: 'JetBrains Mono', 'Inter', sans-serif; }}
    body {{ margin: 0; padding: 20px; background: radial-gradient(circle at top, #1b1136, var(--bg)); color: var(--text); }}
    .top-bar {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.12); padding-bottom: 12px; margin-bottom: 18px; }}
    .tabs {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 18px; }}
    .tab-btn {{
      padding: 10px 16px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.15);
      background: var(--panel); color: var(--text); cursor: pointer; font-weight: 700;
    }}
    .tab-btn.active {{ background: linear-gradient(135deg, var(--neon), #4f46e5); border-color: var(--cyan); }}
    .tab-pane {{ display: none; background: var(--panel); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px; padding: 18px; }}
    .tab-pane.active {{ display: block; }}
    input, select, textarea {{
      width: 100%; padding: 10px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.16);
      background: rgba(0,0,0,0.35); color: var(--text); margin-bottom: 10px;
    }}
    .action-btn {{
      padding: 11px 18px; border-radius: 10px; border: none; cursor: pointer;
      background: linear-gradient(135deg, var(--cyan), #3b82f6); color: #050814; font-weight: 800;
    }}
    pre {{ background: #05050a; padding: 12px; border-radius: 10px; overflow-x: auto; color: #a5f3fc; }}
  \x3c/style>
\x3c/head>
\x3cbody>
  \x3cdiv class="top-bar">
    \x3ch2>🌌 {safe_title}\x3c/h2>
    \x3cspan>🔒 Strict Privacy Pinning (Encrypted POST Only)\x3c/span>
  \x3c/div>

  \x3cdiv class="tabs">
    \x3cbutton class="tab-btn active" onclick="switchTab('tab1', this)">1. Multi-Persona Unfiltered Chat (12-Turn + .TXT)\x3c/button>
    \x3cbutton class="tab-btn" onclick="switchTab('tab2', this)">2. Direct Media Studio (Img/Vid/Img2Vid + CDN)\x3c/button>
    \x3cbutton class="tab-btn" onclick="switchTab('tab3', this)">3. Dompet Voucher Ed25519 (VCH-...)\x3c/button>
    \x3cbutton class="tab-btn" onclick="switchTab('tab4', this)">4. Vibe-Coder API Gateway & Legal\x3c/button>
  \x3c/div>

  \x3c!-- TAB 1: Multi-Persona Unfiltered Chat -->
  \x3cdiv id="tab1" class="tab-pane active">
    \x3ch3>🎭 Multi-Persona Unfiltered Chat (Memori 12 Giliran)\x3c/h3>
    \x3cselect id="personaSelect">
      \x3coption value="Velvet Muse (Creative Uncensored)">Velvet Muse (Creative Uncensored)\x3c/option>
      \x3coption value="Shadow Architect (Cyberpunk Roleplay)">Shadow Architect (Cyberpunk Roleplay)\x3c/option>
      \x3coption value="Philosopher Zero (Unfiltered Analyst)">Philosopher Zero (Unfiltered Analyst)\x3c/option>
    \x3c/select>
    \x3cdiv id="chatHistoryBox" style="min-height:160px; max-height:300px; overflow-y:auto; padding:10px; background:#080711; border-radius:10px; margin-bottom:10px;">\x3c/div>
    \x3ctextarea id="nocturnePrompt" placeholder="Ketik dialog atau skenario bebas tanpa batas...">\x3c/textarea>
    \x3cbutton class="action-btn" onclick="sendNocturneChat()">Kirim Pesan\x3c/button>
    \x3cbutton class="action-btn" style="background:#f59e0b;" onclick="exportChatTxt()">📥 Ekspor Transkrip (.TXT)\x3c/button>
  \x3c/div>

  \x3c!-- TAB 2: Direct Media Studio -->
  \x3cdiv id="tab2" class="tab-pane">
    \x3ch3>🎬 Direct Media Studio (Image / Video / Img2Vid_Motion)\x3c/h3>
    \x3cselect id="mediaKind">
      \x3coption value="IMAGE_4K">Render Foto Unfiltered 4K\x3c/option>
      \x3coption value="VIDEO_HD">Render Video Sinematik HD\x3c/option>
      \x3coption value="IMG2VID_MOTION">Image-to-Video (IMG2VID_MOTION)\x3c/option>
    \x3c/select>
    \x3ctextarea id="mediaPrompt" placeholder="Deskripsikan adegan visual secara detail...">\x3c/textarea>
    \x3cbutton class="action-btn" onclick="generateNocturneMedia()">⚡ Render Sekarang\x3c/button>
    \x3cdiv id="mediaResultBox" style="margin-top:14px;">\x3c/div>
  \x3c/div>

  \x3c!-- TAB 3: Dompet Voucher Ed25519 -->
  \x3cdiv id="tab3" class="tab-pane">
    \x3ch3>🎟️ Klaim Kode Voucher Kriptografi Ed25519 (VCH-...)\x3c/h3>
    \x3cinput type="text" id="voucherUserId" placeholder="ID Telegram Anda (contoh: 123456789)" />
    \x3cinput type="text" id="voucherInput" placeholder="Masukkan kode VCH-..." />
    \x3cbutton class="action-btn" onclick="redeemVoucherWeb()">💎 Cairkan Voucher (Bebas Watermark)\x3c/button>
    \x3cdiv id="voucherStatus" style="margin-top:10px;">\x3c/div>
  \x3c/div>

  \x3c!-- TAB 4: Vibe-Coder API Gateway & Dokumentasi Legal -->
  \x3cdiv id="tab4" class="tab-pane">
    \x3ch3>⚡ Vibe-Coder OpenAI-Compatible API Gateway\x3c/h3>
    \x3cp>Endpoint Kompatibel: \x3ccode>POST /v1/chat/completions\x3c/code> dengan Header \x3ccode>Authorization: Bearer sk-bikinai-...\x3c/code>\x3c/p>
    \x3cpre>curl -X POST {PUBLIC_WEB_BASE_URL}/v1/chat/completions \\
  -H "Authorization: Bearer sk-bikinai-YOUR_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{{"model": "bikinai-v4-omni", "messages": [{{"role": "user", "content": "Halo!"}}]}}'\x3c/pre>
    \x3ch4>📜 Dokumentasi Legal & Kepatuhan\x3c/h4>
    \x3cp style="color:var(--muted); font-size:0.9rem;">
      Seluruh sesi di portal ini tunduk pada kebijakan Strict Privacy Pinning (tidak pernah disimpan ke log publik) dan wajib mematuhi hukum yang berlaku.
    \x3c/p>
  \x3c/div>

  \x3cscript>
    let chatTurns = [];
    function switchTab(id, btn) {{
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
      document.getElementById(id).classList.add('active');
      btn.classList.add('active');
    }}
    async function sendNocturneChat() {{
      const prompt = document.getElementById('nocturnePrompt').value.trim();
      const persona = document.getElementById('personaSelect').value;
      if (!prompt) return;
      const res = await fetch('/api/nocturne/chat', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{session_id: 'web-default', persona: persona, prompt: prompt}})
      }});
      const data = await res.json();
      chatTurns = data.history || [];
      const box = document.getElementById('chatHistoryBox');
      box.innerHTML = chatTurns.map(t => `\x3cdiv>\x3cb>${{t.role}}:\x3c/b> ${{t.content}}\x3c/div>\x3chr style="border-color:rgba(255,255,255,0.06)"/>`).join('');
      document.getElementById('nocturnePrompt').value = '';
    }}
    function exportChatTxt() {{
      const txt = chatTurns.map(t => `[${{t.role}}]\\n${{t.content}}\\n`).join('\\n---\\n');
      const blob = new Blob([txt || 'Belum ada riwayat obrolan.'], {{type: 'text/plain;charset=utf-8'}});
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'nocturne_chat_12turns.txt';
      a.click();
    }}
    async function generateNocturneMedia() {{
      const kind = document.getElementById('mediaKind').value;
      const prompt = document.getElementById('mediaPrompt').value.trim();
      const res = await fetch('/api/nocturne/generate', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{kind: kind, prompt: prompt}})
      }});
      const d = await res.json();
      document.getElementById('mediaResultBox').innerHTML =
        `\x3cp>✅ Render Selesai (${{d.license_label}})\x3c/p>` +
        `\x3ca class="action-btn" href="${{d.download_url}}" target="_blank">⬇️ Download Langsung CDN\x3c/a>`;
    }}
    async function redeemVoucherWeb() {{
      const uid = document.getElementById('voucherUserId').value.trim();
      const code = document.getElementById('voucherInput').value.trim();
      const res = await fetch('/api/voucher/redeem', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{user_id: parseInt(uid || '0', 10), voucher_code: code}})
      }});
      const d = await res.json();
      document.getElementById('voucherStatus').textContent = d.message || '';
    }}
  \x3c/script>
\x3c/body>
\x3c/html>
"""


def verify_telegram_webapp_init_data(init_data_raw: str, bot_token: str = BOT_TOKEN) -> Tuple[bool, Dict[str, Any]]:
    """
    Memverifikasi tanda tangan kriptografi HMAC-SHA256 pada `Telegram.WebApp.initData`.
    """
    if not init_data_raw:
        return False, {}
    try:
        parsed = dict(urllib.parse.parse_qsl(init_data_raw, keep_blank_values=True))
        received_hash = parsed.pop("hash", "")
        if not received_hash:
            return False, {}
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
        secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(calculated_hash, received_hash):
            return False, {}
        user_obj = json.loads(parsed.get("user", "{}") or "{}")
        return True, user_obj
    except Exception:
        return False, {}


def generate_synthetic_bmp_image(title_text: str, watermarked: bool = False) -> bytes:
    """
    Menghasilkan gambar bitmap 24-bit valid secara deterministik di dalam memori
    untuk keperluan preview/download CDN tanpa ketergantungan jaringan eksternal.
    """
    width, height = 64, 64
    row_padded = (width * 3 + 3) & (~3)
    pixel_array_size = row_padded * height
    file_size = 54 + pixel_array_size

    header = bytearray(54)
    header[0:2] = b"BM"
    struct.pack_into("\x3cI", header, 2, file_size)
    struct.pack_into("\x3cI", header, 10, 54)
    struct.pack_into("\x3cI", header, 14, 40)
    struct.pack_into("\x3ci", header, 18, width)
    struct.pack_into("\x3ci", header, 22, height)
    struct.pack_into("\x3cH", header, 26, 1)
    struct.pack_into("\x3cH", header, 28, 24)
    struct.pack_into("\x3cI", header, 34, pixel_array_size)

    seed = sum(ord(c) for c in (title_text or "bikinAI")) % 255
    pixels = bytearray(pixel_array_size)
    for y in range(height):
        for x in range(width):
            idx = y * row_padded + x * 3
            pixels[idx] = (x * 4 + seed) % 256
            pixels[idx + 1] = (y * 4 + (40 if watermarked else 120)) % 256
            pixels[idx + 2] = ((x + y) * 2 + seed) % 256
    return bytes(header + pixels)



<!-- [ID:02_CORE_AI_S021] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# 9. WIZARD STATE, PRESET AWAM & MENU BUILDERS
UPSCALER_WHITE_LABEL = {
    "PHOTO_FACE_4K": "🔍 Pertajam Foto & Wajah 4K",
    "TEXT_LINE_4K": "✨ Pertajam Teks & Gambar 4K",
    "VIDEO_4K_60FPS": "🎞️ Pertajam & Haluskan Video 4K 60FPS",
    "OFF": "Standar HD",
}

AWAM_VIDEO_MOTION_PRESETS = {
    "ZOOM_CINEMATIC": ("🎥 Kamera Zoom Sinematik", "smooth cinematic camera zoom-in, dynamic lighting, 60fps"),
    "ORBIT_360": ("🔄 Orbit Produk 360°", "360 degree orbital camera rotation around subject, spotlight"),
    "DANCE_FASHION": ("🕺 Gerakan Model & Fashion", "fluid fashion model movement & natural motion"),
    "SLOWMO_EPIC": ("🏃 Slow-Motion Epik", "epic slow-motion action, high frame rate"),
}

AWAM_IMAGE_STYLE_PRESETS = {
    "UMKM_CATALOG": ("🛍️ Katalog Produk UMKM", "commercial product photography, studio lighting, 8k"),
    "STUDIO_PORTRAIT": ("👔 Foto Profil Studio", "professional studio portrait, soft rim lighting, sharp focus"),
    "POSTER_THUMB": ("🎬 Poster & Thumbnail", "movie poster & YouTube thumbnail composition, vibrant colors"),
    "ANIME_PIXAR": ("🎌 Anime / Ilustrasi 3D", "3D & anime illustration, volumetric light"),
}

IMAGE_EDITING_TOOLS = {
    "REMOVE_BG_PNG": ("✂️ Hapus Background (File PNG Transparan)", "Menghapus latar belakang foto dan mengirimkannya sebagai File Dokumen .PNG transparan"),
    "IMG2VID_MOTION": ("🖼️➡️🎬 Gerakkan Foto Jadi Video (Image-to-Video)", "Menggerakkan foto referensi menjadi video menggunakan Wan-AI/Wan2.2-S2V-14B"),
    "RETOUCH_FACE": ("✨ Retouch Wajah & Kulit", "Memperhalus tekstur kulit dan pencahayaan wajah"),
    "INPAINT_OBJ": ("🖌️ Ganti Baju / Ubah Objek", "Mengganti pakaian atau objek tertentu di dalam foto"),
    "OUTPAINT_EXPAND": ("🖼️ Perluas Ukuran Foto", "Memperluas rasio foto menjadi vertikal 9:16 atau 16:9"),
    "PRODUCT_RELIGHT": ("📸 Studio Produk UMKM (Relighting)", "Mengubah pencahayaan foto produk menjadi katalog studio"),
    "RESTORE_OLD": ("🕰️ Restorasi Foto Lama", "Memperbaiki foto buram menjadi tajam kembali"),
}


@dataclass
class LiveWizardSession:
    prompt: str
    modality: Literal["VIDEO", "IMAGE", "EDIT_IMAGE"] = "VIDEO"
    aspect_ratio: str = "9:16"
    duration_sec: int = 5
    video_engine: str = "Wan-AI/Wan2.2-T2V-A14B"
    image_engine: str = "black-forest-labs/FLUX.1-dev"
    edit_tool: str = "REMOVE_BG_PNG"
    upscale_mode: str = "PHOTO_FACE_4K"
    awam_preset: str = ""

    def get_pricing(self) -> tuple[int, int, bool]:
        if RUNTIME_CONFIG["HAPPY_HOUR_MODE"]:
            return 0, 0, True
        if self.modality in ("IMAGE", "EDIT_IMAGE") and self.edit_tool != "IMG2VID_MOTION":
            return 4, 0, True
        if RUNTIME_CONFIG["PILIHAN_MESIN_MEDIA"] == 1 and not RUNTIME_CONFIG["LAUNCH_PRODUCTION_MODE"]:
            return {5: 4, 10: 8, 30: 20}.get(self.duration_sec, 4), 0, True
        base_c = {5: 20, 10: 35, 30: 100}.get(self.duration_sec, 20)
        if self.video_engine in ("google/veo-3.1-fast", "Wan-AI/Wan2.2-S2V-14B"):
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
    return chat_type == "private" and int(RUNTIME_CONFIG.get("OWNER_ID_RUNTIME") or 0) > 0 and user_id == int(RUNTIME_CONFIG["OWNER_ID_RUNTIME"])


def build_customer_main_menu_keyboard(u: dict[str, Any] | None = None, is_private: bool = True) -> InlineKeyboardMarkup:
    today_str = time.strftime("%Y-%m-%d")
    already_claimed = u and (u.get("last_claim_date") == today_str or u.get("koin_bonus", 0) >= 25)
    claim_label = "🎁 Koin Harian Terklaim ✅" if already_claimed else "🎁 Klaim +4 Koin Gratis"
    ppp_zone = u.get("ppp_zone", 3) if u else 3
    topup_label = "💳 Isi Saldo & Paket VIP (QRIS Instan)" if ppp_zone == 3 else "💳 Top-Up & VIP Packs (USDT / Stars ⭐)"
    web_brand = RUNTIME_CONFIG.get("WEB_BRAND_NAME") or "AetherFree AI Studio"

    rows: list[list[InlineKeyboardButton]] = []
    m_url = RUNTIME_CONFIG["MINIAPP_URL"]
    if m_url.startswith("https://"):
        if is_private:
            rows.append([InlineKeyboardButton(text="📱 Buka Super Mini App Studio (Full Web & Upload)", web_app=WebAppInfo(url=m_url))])
        else:
            rows.append([InlineKeyboardButton(text="📱 Buka Super Mini App Studio (via DM Bot)", url=f"https://t.me/{BOT_USERNAME_GLOBAL}?start=miniapp")])
    else:
        rows.append([InlineKeyboardButton(text="📱 Buka Super Mini App Studio (Panduan Link)", callback_data="menu:miniapp_guide")])

    rows.extend([
        [InlineKeyboardButton(text="🎬 Studio Video & Img2Vid", callback_data="menu:wizard_video"), InlineKeyboardButton(text="🎨 Studio Gambar 4K", callback_data="menu:wizard_image")],
        [InlineKeyboardButton(text="🛠️ Editing & Hapus BG (.PNG)", callback_data="menu:wizard_edit"), InlineKeyboardButton(text="🪄 Arsitek Prompt AI", callback_data="menu:prompt_helper")],
        [InlineKeyboardButton(text="🔬 Deep Research (/riset)", callback_data="menu:deep_research_hint"), InlineKeyboardButton(text="📝 Canvas Workspace (/canvas)", callback_data="menu:canvas_hint")],
        [InlineKeyboardButton(text=f"🌐 Buka {web_brand} (Web & Kode VIP)", callback_data="menu:unfiltered_external_referral")],
        [InlineKeyboardButton(text="📊 Status Kuota Harian", callback_data="menu:quota"), InlineKeyboardButton(text=claim_label, callback_data="menu:claim_daily")],
        [InlineKeyboardButton(text=topup_label, callback_data="menu:topup_qris"), InlineKeyboardButton(text="🎧 Bantuan & Garansi Koin 100%", callback_data="menu:live_support")],
        [InlineKeyboardButton(text="📜 Panduan Prompt, FAQ, Ketentuan & Grup", callback_data="menu:faq_tos")],
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_customer_dashboard_caption(username: str, u: dict[str, Any]) -> str:
    tier_badge = "🌟 KREATOR PRO" if u["has_topped_up"] else "⚡ KREATOR EKSPLORER"
    hh_banner = "\n🎉 **FLASH HAPPY HOUR AKTIF: SEMUA PEMBUATAN KARYA GRATIS 0 KOIN!** 🎉\n" if RUNTIME_CONFIG["HAPPY_HOUR_MODE"] else ""
    safe_u = u.get("safe_uname") or username
    return (
        f"┏━━━ ⚡ **bikinAI SUPER INTELLIGENCE** ⚡ ━━━┓\n"
        f"┃ 👤 **Kreator:** `@{safe_u}`\n"
        f"┃ 🏅 **Status:** `{tier_badge}`\n"
        f"┣━━━━━━━━━━━━━━━━━━━━━━━┫\n"
        f"┃ 💎 **Koin Utama:** `{u['koin_utama']} Koin`\n"
        f"┃ 🎁 **Koin Bonus:** `{u['koin_bonus']}/{MAX_KOIN_BONUS_CAP} Koin`\n"
        f"┃ 💬 **Asisten AI 24 Jam:** `🟢 AKTIF (Gratis)`\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━┛{hh_banner}\n\n"
        f"▸ Pilih fitur studio di bawah atau ketik instruksi Anda secara langsung:"
    )


def build_400_percent_derivative_upsell_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🖼️ Ambil Poster Thumbnail 4K (+4 Koin)", callback_data="drv:poster4k"), InlineKeyboardButton(text="🎵 Ekstrak Audio MP3 (+4 Koin)", callback_data="drv:audiomp3")],
            [InlineKeyboardButton(text="✨ Buka Lisensi Komersial Bersih Tanpa Watermark (+10 Koin)", callback_data="drv:clean_license")],
            [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
        ]
    )


def build_video_wizard_kb(session: LiveWizardSession, show_more: bool = False) -> tuple[str, InlineKeyboardMarkup]:
    if session.upscale_mode in ("PHOTO_FACE_4K", "TEXT_LINE_4K"):
        session.upscale_mode = "VIDEO_4K_60FPS"
    coins, _, _ = session.get_pricing()
    ups_label = UPSCALER_WHITE_LABEL.get(session.upscale_mode, "🎞️ Pertajam & Haluskan Video 4K 60FPS")
    preset_info = f"\n┣ 🎬 **Preset Motion:** `{session.awam_preset}`" if session.awam_preset else ""
    text = (
        f"🎬 **STUDIO VIDEO AI & FOTO JADI VIDEO**\n━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Konsep Video:**\n> _{session.prompt}_\n\n"
        f"┣ ⚡ **Model Video:** **`{session.video_engine}`**{preset_info}\n"
        f"┣ 📐 **Rasio:** `{session.aspect_ratio}` | ⏱️ **Durasi:** `{session.duration_sec}s`\n"
        f"┗ 🔍 **Kualitas:** `{ups_label}`\n━━━━━━━━━━━━━━━━━━\n"
        f"💎 **Biaya:** **`{coins} Koin`** _(Garansi Koin Kembali 100%)_"
    )
    rows = [
        [InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='9:16' else ''}📱 9:16", callback_data="wiz:ar:9:16"), InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='16:9' else ''}🖥️ 16:9", callback_data="wiz:ar:16:9"), InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='1:1' else ''}🟦 1:1", callback_data="wiz:ar:1:1")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.duration_sec==5 else ''}⚡ 5s", callback_data="wiz:dur:5"), InlineKeyboardButton(text=f"{'✅ ' if session.duration_sec==10 else ''}🔥 10s", callback_data="wiz:dur:10"), InlineKeyboardButton(text=f"{'✅ ' if session.duration_sec==30 else ''}🎬 30s", callback_data="wiz:dur:30")],
        [InlineKeyboardButton(text="🎥 Motion: Zoom Sinematik", callback_data="wiz:vpre:ZOOM_CINEMATIC"), InlineKeyboardButton(text="🔄 Motion: Orbit 360°", callback_data="wiz:vpre:ORBIT_360")],
        [InlineKeyboardButton(text="🕺 Motion: Model/Fashion", callback_data="wiz:vpre:DANCE_FASHION"), InlineKeyboardButton(text="🏃 Motion: Slow-Mo Epik", callback_data="wiz:vpre:SLOWMO_EPIC")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Wan-AI/Wan2.2-T2V-A14B' else ''}🔵 Wan2.2-T2V-A14B", callback_data="wiz:veng:Wan-AI/Wan2.2-T2V-A14B"), InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Wan-AI/Wan2.2-S2V-14B' else ''}🕺 Wan2.2-S2V-14B", callback_data="wiz:veng:Wan-AI/Wan2.2-S2V-14B")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='google/veo-3.1-fast' else ''}🎥 google/veo-3.1-fast", callback_data="wiz:veng:google/veo-3.1-fast"), InlineKeyboardButton(text=f"{'✅ ' if session.video_engine=='Wan-AI/Wan2.2-TI2V-5B' else ''}🟢 Wan2.2-TI2V-5B", callback_data="wiz:veng:Wan-AI/Wan2.2-TI2V-5B")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='VIDEO_4K_60FPS' else ''}🎞️ Pertajam & Haluskan Video 4K 60FPS", callback_data="wiz:ups:VIDEO_4K_60FPS"), InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='OFF' else ''}⚡ Standar HD", callback_data="wiz:ups:OFF")],
        [InlineKeyboardButton(text="✏️ Ubah Deskripsi Video", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 MULAI BUAT VIDEO ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ]
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def build_image_wizard_kb(session: LiveWizardSession, show_more: bool = False) -> tuple[str, InlineKeyboardMarkup]:
    if session.upscale_mode == "VIDEO_4K_60FPS":
        session.upscale_mode = "PHOTO_FACE_4K"
    coins, _, _ = session.get_pricing()
    ups_label = UPSCALER_WHITE_LABEL.get(session.upscale_mode, "🔍 Pertajam Foto & Wajah 4K")
    preset_info = f"\n┣ 🎨 **Preset Gaya:** `{session.awam_preset}`" if session.awam_preset else ""
    text = (
        f"🎨 **STUDIO GAMBAR 4K**\n━━━━━━━━━━━━━━━━━━\n"
        f"📝 **Deskripsi Gambar:**\n> _{session.prompt}_\n\n"
        f"┣ ⚡ **Model Gambar:** **`{session.image_engine}`**{preset_info}\n"
        f"┣ 📐 **Rasio:** `{session.aspect_ratio}`\n"
        f"┗ 🔍 **Penajaman:** `{ups_label}`\n━━━━━━━━━━━━━━━━━━\n"
        f"💎 **Biaya:** **`{coins} Koin`** _(Garansi Koin Kembali 100%)_"
    )
    rows = [
        [InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='9:16' else ''}📱 9:16", callback_data="wiz:ar:9:16"), InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='1:1' else ''}🟦 1:1", callback_data="wiz:ar:1:1"), InlineKeyboardButton(text=f"{'✅ ' if session.aspect_ratio=='16:9' else ''}🖥️ 16:9", callback_data="wiz:ar:16:9")],
        [InlineKeyboardButton(text="🛍️ Gaya: Katalog UMKM", callback_data="wiz:ipre:UMKM_CATALOG"), InlineKeyboardButton(text="👔 Gaya: Foto Studio", callback_data="wiz:ipre:STUDIO_PORTRAIT")],
        [InlineKeyboardButton(text="🎬 Gaya: Poster/Thumb", callback_data="wiz:ipre:POSTER_THUMB"), InlineKeyboardButton(text="🎌 Gaya: Anime/3D", callback_data="wiz:ipre:ANIME_PIXAR")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='black-forest-labs/FLUX.1-dev' else ''}📸 FLUX.1-dev", callback_data="wiz:ieng:black-forest-labs/FLUX.1-dev"), InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='bytedance/seedream-4.0' else ''}✨ seedream-4.0", callback_data="wiz:ieng:bytedance/seedream-4.0")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='OnomaAIResearch/Illustrious-xl' else ''}🎌 Illustrious-xl", callback_data="wiz:ieng:OnomaAIResearch/Illustrious-xl"), InlineKeyboardButton(text=f"{'✅ ' if session.image_engine=='Laxhar/noobai-XL-Vpred-1.0' else ''}🌟 noobai-XL-Vpred-1.0", callback_data="wiz:ieng:Laxhar/noobai-XL-Vpred-1.0")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='PHOTO_FACE_4K' else ''}🔍 Pertajam Foto & Wajah 4K", callback_data="wiz:ups:PHOTO_FACE_4K"), InlineKeyboardButton(text=f"{'✅ ' if session.upscale_mode=='TEXT_LINE_4K' else ''}✨ Pertajam Teks & Gambar 4K", callback_data="wiz:ups:TEXT_LINE_4K")],
        [InlineKeyboardButton(text="🛠️ Buka Menu Editing, Foto Jadi Video & Hapus BG (.PNG)", callback_data="menu:wizard_edit")],
        [InlineKeyboardButton(text="✏️ Ubah Deskripsi Gambar", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 MULAI BUAT GAMBAR ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ]
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


def build_editing_tools_wizard_kb(session: LiveWizardSession) -> tuple[str, InlineKeyboardMarkup]:
    coins, _, _ = session.get_pricing()
    tool_title, tool_desc = IMAGE_EDITING_TOOLS.get(session.edit_tool, IMAGE_EDITING_TOOLS["REMOVE_BG_PNG"])
    text = (
        f"🛠️ **STUDIO EDITING, HAPUS BG & FOTO JADI VIDEO**\n━━━━━━━━━━━━━━━━━━\n"
        f"🎯 **Fitur:** **`{tool_title}`**\n"
        f"ℹ️ **Fungsi:** _{tool_desc}_\n"
        f"📝 **Instruksi:** _{session.prompt}_"
    )
    rows = [
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='REMOVE_BG_PNG' else ''}✂️ Hapus Background (File PNG Transparan)", callback_data="wiz:etool:REMOVE_BG_PNG")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='IMG2VID_MOTION' else ''}🖼️➡️🎬 Gerakkan Foto Jadi Video (Image-to-Video)", callback_data="wiz:etool:IMG2VID_MOTION")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='RETOUCH_FACE' else ''}✨ Retouch Wajah", callback_data="wiz:etool:RETOUCH_FACE"), InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='INPAINT_OBJ' else ''}🖌️ Ganti Baju / Objek", callback_data="wiz:etool:INPAINT_OBJ")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='OUTPAINT_EXPAND' else ''}🖼️ Perluas Ukuran Foto", callback_data="wiz:etool:OUTPAINT_EXPAND"), InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='PRODUCT_RELIGHT' else ''}📸 Studio Produk UMKM", callback_data="wiz:etool:PRODUCT_RELIGHT")],
        [InlineKeyboardButton(text=f"{'✅ ' if session.edit_tool=='RESTORE_OLD' else ''}🕰️ Restorasi Foto Lama", callback_data="wiz:etool:RESTORE_OLD")],
        [InlineKeyboardButton(text="✏️ Ubah Instruksi", callback_data="wiz:prompt:edit")],
        [InlineKeyboardButton(text=f"🚀 PROSES SEKARANG ({coins} Koin)", callback_data="wiz:exec:now")],
        [InlineKeyboardButton(text="⬅️ Kembali ke Menu Utama", callback_data="menu:home")],
    ]
    return text, InlineKeyboardMarkup(inline_keyboard=rows)


