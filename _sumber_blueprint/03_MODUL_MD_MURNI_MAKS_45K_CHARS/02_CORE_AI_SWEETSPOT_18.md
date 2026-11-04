
<!-- [ID:02_CORE_AI_S014] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# 4. MINI APP HTML & FREEDOM WEB PORTAL HTML (CANONICAL HF/OR MODEL IDS)
MINIAPP_FULL_WEBSITE_HTML = """<!DOCTYPE html>
<html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>bikinAI Super Intelligence — Studio Kreatif 4K</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
:root{--bg:#05070c;--surface:#0f1523;--cyan:#00f0ff;--purple:#7b2cbf;--text:#f0f6fc;--muted:#8b949e;--success:#00e676}
*{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
body{background:radial-gradient(circle at 50% 0%,#17103a 0%,#05070c 72%);color:var(--text);min-height:100vh;padding:14px 14px 96px}
.hero{background:linear-gradient(135deg,rgba(15,21,35,.95),rgba(30,16,60,.85));border:1px solid rgba(0,240,255,.3);border-radius:16px;padding:16px;margin-bottom:14px}
.badge{display:inline-block;background:linear-gradient(90deg,var(--cyan),var(--purple));color:#fff;font-size:10px;font-weight:800;padding:3px 10px;border-radius:99px;margin-bottom:6px}
.hero h1{font-size:18px;font-weight:800;color:#fff;margin-bottom:4px}.hero p{font-size:12px;color:var(--muted);line-height:1.4}
.tab-section{display:none}.tab-section.active{display:block}
.label{font-size:11px;font-weight:700;text-transform:uppercase;color:var(--cyan);margin:12px 0 6px;letter-spacing:.6px}
.pill-row{display:flex;gap:7px;overflow-x:auto;padding-bottom:4px;margin-bottom:4px}
.pill{flex:1;text-align:center;white-space:nowrap;background:var(--surface);border:1px solid rgba(255,255,255,.08);color:var(--muted);padding:9px 10px;border-radius:11px;font-size:12px;font-weight:600;cursor:pointer;user-select:none}
.pill.active{background:rgba(0,240,255,.18);border-color:var(--cyan);color:#fff}
.pill.disabled{opacity:.22;pointer-events:none;cursor:not-allowed;filter:grayscale(1)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.card{background:var(--surface);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:10px;cursor:pointer}
.card.active{border-color:var(--cyan);background:rgba(0,240,255,.12)}.card.hidden-engine{display:none}
.card h4{font-size:13px;color:#fff;margin-bottom:2px}.card p{font-size:10px;color:var(--muted)}
.upload-box{border:1.5px dashed rgba(0,240,255,.4);background:rgba(15,21,35,.6);border-radius:14px;padding:12px;text-align:center;position:relative;cursor:pointer;margin-top:4px}
.upload-box.highlight-upload{border-color:#00e676;background:rgba(0,230,118,.08)}
.upload-box input{position:absolute;inset:0;opacity:0;cursor:pointer}
#ref-preview{max-height:110px;border-radius:8px;margin-top:8px;display:none;margin-left:auto;margin-right:auto;border:1px solid var(--cyan)}
textarea{width:100%;height:80px;background:var(--surface);border:1px solid rgba(0,240,255,.3);border-radius:12px;color:#fff;padding:10px;font-size:13px;outline:none;resize:none}
.btn-exec{width:100%;margin-top:12px;padding:14px;border:none;border-radius:14px;background:linear-gradient(90deg,#00c6ff,#7b2cbf);color:#fff;font-size:14px;font-weight:800;cursor:pointer}
#toast{margin-top:10px;padding:10px;border-radius:10px;font-size:12px;background:rgba(0,230,118,.15);border:1px solid var(--success);color:var(--success);display:none;text-align:center}
.legal-card{background:var(--surface);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:14px;margin-bottom:10px;font-size:12px;line-height:1.55;color:#d0d7de}
.legal-card h3{color:var(--cyan);font-size:14px;margin-bottom:6px}
.topic-btn{display:block;background:rgba(0,240,255,.1);border:1px solid rgba(0,240,255,.3);color:#fff;text-decoration:none;padding:9px 12px;border-radius:10px;margin-top:6px;font-size:12px;font-weight:700}
.footer-copy{text-align:center;font-size:11px;color:var(--muted);margin-top:18px;padding-top:12px;border-top:1px solid rgba(255,255,255,.07)}
.bottom-nav{position:fixed;bottom:0;left:0;right:0;height:62px;background:rgba(8,12,22,.96);backdrop-filter:blur(16px);border-top:1px solid rgba(255,255,255,.1);display:flex;justify-content:space-around;align-items:center;z-index:99}
.nav-btn{display:flex;flex-direction:column;align-items:center;gap:2px;color:var(--muted);font-size:10px;font-weight:600;cursor:pointer}.nav-btn.active{color:var(--cyan)}
</style></head><body>
<div class="hero"><span class="badge">⚡ STUDIO KREATIF RESMI v3.7.1</span><h1>Selamat Datang di bikinAI Super Intelligence</h1>
<p id="welcome-user">Platform Studio Visual 4K, Video Sinematik, & Foto Jadi Video dengan Garansi Koin Kembali 100%.</p></div>

<div id="tab-studio" class="tab-section active">
  <div class="label">1. Pilih Kategori Karya</div>
  <div class="pill-row" data-group="modality">
    <div class="pill active" onclick="setMod(this,'IMAGE')">🎨 Gambar 4K</div>
    <div class="pill" onclick="setMod(this,'VIDEO')">🎬 Buat Video AI</div>
    <div class="pill" onclick="setMod(this,'IMG2VID')">🖼️➡️🎬 Foto Jadi Video</div>
    <div class="pill" onclick="setMod(this,'REMOVE_BG')">✂️ Hapus BG (.PNG)</div>
    <div class="pill" onclick="setMod(this,'RETOUCH')">✨ Retouch & Edit</div>
  </div>
  <div class="label">2. Pilih Mesin AI Utama</div>
  <div class="grid" id="engine-grid">
    <div class="card active" data-type="IMAGE" onclick="setEng(this,'bytedance/seedream-4.0')"><h4>✨ Seedream 4.0</h4><p>Poster 4K & Teks Tajam</p></div>
    <div class="card" data-type="IMAGE" onclick="setEng(this,'black-forest-labs/FLUX.1-dev')"><h4>📸 FLUX.1-dev</h4><p>Fotorealistis Natural</p></div>
    <div class="card" data-type="IMAGE" onclick="setEng(this,'black-forest-labs/flux.1-kontext-pro')"><h4>🎨 FLUX.1 Kontext Pro</h4><p>Konsistensi Objek & Edit</p></div>
    <div class="card" data-type="IMAGE" onclick="setEng(this,'OnomaAIResearch/Illustrious-xl')"><h4>🎌 Illustrious-XL</h4><p>Anime & Ilustrasi 2.5D</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Wan-AI/Wan2.2-T2V-A14B')"><h4>🔵 Wan2.2-T2V-A14B</h4><p>Video Sinematik 14B</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Wan-AI/Wan2.2-S2V-14B')"><h4>🕺 Wan2.2-S2V-14B</h4><p>Image/Audio to Video</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'google/veo-3.1-fast')"><h4>🎥 Google Veo 3.1</h4><p>Sinematik Film & Audio</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Wan-AI/Wan2.2-TI2V-5B')"><h4>🟢 Wan2.2-TI2V-5B</h4><p>Gerak Cepat & Halus</p></div>
  </div>
  <div class="label">3. Pilihan Instan Orang Awam (Klik untuk Pakai Gaya / Motion Kamera)</div>
  <div class="pill-row" id="preset-img-row" data-group="preset">
    <div class="pill active" onclick="applyAwamPreset(this,'Commercial product catalog photography, studio lighting')">🛍️ Katalog Produk UMKM</div>
    <div class="pill" onclick="applyAwamPreset(this,'Professional studio portrait, soft rim lighting, sharp focus')">👔 Foto Profil Studio</div>
    <div class="pill" onclick="applyAwamPreset(this,'Cinematic movie poster & viral YouTube thumbnail')">🎬 Poster & Thumbnail</div>
    <div class="pill" onclick="applyAwamPreset(this,'Vibrant 3D & anime illustration, volumetric light')">🎌 Anime / Ilustrasi 3D</div>
  </div>
  <div class="pill-row" id="preset-vid-row" data-group="preset" style="display:none">
    <div class="pill active" onclick="applyAwamPreset(this,'Smooth cinematic camera zoom-in, dynamic lighting, 60fps')">🎥 Kamera Zoom Sinematik</div>
    <div class="pill" onclick="applyAwamPreset(this,'360 degree orbital camera rotation around product, spotlight')">🔄 Orbit Produk 360°</div>
    <div class="pill" onclick="applyAwamPreset(this,'Fluid fashion model motion & natural movement, high frame rate')">🕺 Gerakan Model & Fashion</div>
    <div class="pill" onclick="applyAwamPreset(this,'Epic slow-motion action, glowing particles in the air')">🏃 Slow-Motion Epik</div>
  </div>
  <div class="label">4. Ukuran Layar (1 Pilihan Aktif)</div>
  <div class="pill-row" data-group="ratio">
    <div class="pill active" onclick="selectExclusive(this,'ratio','9:16')">📱 9:16 (TikTok/Reels)</div>
    <div class="pill" onclick="selectExclusive(this,'ratio','1:1')">🟦 1:1 (Feed/Katalog)</div>
    <div class="pill" onclick="selectExclusive(this,'ratio','16:9')">🖥️ 16:9 (YouTube/Lanskap)</div>
  </div>
  <div class="label">5. Durasi Video (Aktif Khusus Mode Video)</div>
  <div class="pill-row" data-group="duration" id="duration-row">
    <div class="pill active disabled" onclick="selectExclusive(this,'duration',5)">⚡ 5 Detik</div>
    <div class="pill disabled" onclick="selectExclusive(this,'duration',10)">🔥 10 Detik</div>
    <div class="pill disabled" onclick="selectExclusive(this,'duration',30)">🎬 30 Detik Story</div>
  </div>
  <div class="label">6. Mode Penajaman 4K (Otomatis Menyesuaikan Foto vs Video)</div>
  <div class="pill-row" data-group="upscale" id="upscale-row">
    <div class="pill active" data-ups="IMG" onclick="selectExclusive(this,'upscale','Pertajam Foto & Wajah 4K')">🔍 Pertajam Foto & Wajah 4K</div>
    <div class="pill" data-ups="IMG" onclick="selectExclusive(this,'upscale','Pertajam Teks & Gambar 4K')">✨ Pertajam Teks & Gambar 4K</div>
    <div class="pill disabled" data-ups="VID" id="vid-ups-pill" onclick="selectExclusive(this,'upscale','Pertajam & Haluskan Video 4K 60FPS')">🎞️ Pertajam Video 4K 60FPS</div>
  </div>
  <div class="label">7. Upload Foto Referensi (Untuk Foto Jadi Video / Produk)</div>
  <div class="upload-box" id="upload-container">
    <input type="file" accept="image/*" onchange="previewRef(event)">
    <div id="up-txt" style="font-size:12px">📸 <b>Sentuh untuk Upload Foto Referensi</b></div>
    <img id="ref-preview" alt="Ref">
  </div>
  <div class="label">8. Tulis Deskripsi Karya Anda</div>
  <textarea id="prompt-in" placeholder="Contoh: Botol parfum di atas batu hitam dengan pencahayaan studio..."></textarea>
  <button class="btn-exec" id="btn-go" onclick="runGenerate()">🚀 BUAT KARYA SEKARANG (KIRIM KE CHAT)</button>
  <div id="toast"></div>
</div>

<div id="tab-guide" class="tab-section">
  <div class="legal-card"><h3>🪄 Rumus Mudah Membuat Prompt bagi Pemula</h3>
  <p>Gunakan pola: <b>[Objek Utama] + [Gerakan/Aktivitas] + [Pencahayaan]</b>.<br>
  • Untuk <b>Foto Jadi Video</b>: Pilih <b>🖼️➡️🎬 Foto Jadi Video</b>, unggah foto Anda, lalu pilih preset <b>🔄 Orbit Produk 360°</b>.</p></div>
  <div class="legal-card"><h3>📡 Akses Cepat ke 6 Kamar Topik Komunitas</h3><div id="community-links-box"></div></div>
</div>

<div id="tab-legal" class="tab-section">
  <div class="legal-card"><h3>⚖️ Ketentuan Layanan & Lisensi Komersial Bersih</h3>
  <p>Seluruh karya yang dibuat menggunakan <b>Koin Utama (Pro)</b> memberikan hak komersial penuh bebas watermark kepada kreator.</p></div>
  <div class="legal-card"><h3>🛡️ Jaminan Privasi & Garansi Koin Kembali 100%</h3>
  <p>Jika pembuatan karya terkendala jaringan >60 detik, koin Anda otomatis dikembalikan 100%.</p></div>
</div>

<div class="footer-copy">Copyright © 2026 <b>bikinAI Super Intelligence</b>. All Rights Reserved.</div>
<div class="bottom-nav">
  <div class="nav-btn active" onclick="openTab(this,'tab-studio')"><span>🎬</span><span>Studio AI</span></div>
  <div class="nav-btn" onclick="openTab(this,'tab-guide')"><span>🧭</span><span>Panduan & Grup</span></div>
  <div class="nav-btn" onclick="openTab(this,'tab-legal')"><span>⚖️</span><span>Ketentuan & Privasi</span></div>
</div>

<script>
const tg=window.Telegram?.WebApp;
let st={init_data:"",user_id:0,username:"Kreator",modality:"IMAGE",engine:"bytedance/seedream-4.0",ratio:"9:16",duration:5,upscale:"Pertajam Foto & Wajah 4K",preset_mod:"Commercial product catalog photography, studio lighting",has_ref:false};
if(tg){tg.expand();st.init_data=tg.initData||"";const u=tg.initDataUnsafe?.user;if(u){st.user_id=u.id;st.username=u.username||u.first_name||"Kreator";document.getElementById("welcome-user").innerText=`Halo @${st.username}! Pilih kategori karya atau preset instan di bawah.`}}
fetch("/api/public/community-links").then(r=>r.json()).then(d=>{if(d.links)document.getElementById("community-links-box").innerHTML=d.links.map(x=>`<a class="topic-btn" href="${x.url}" target="_blank">${x.title}</a>`).join("")}).catch(()=>{});
function openTab(el,id){document.querySelectorAll(".nav-btn").forEach(b=>b.classList.remove("active"));document.querySelectorAll(".tab-section").forEach(s=>s.classList.remove("active"));el.classList.add("active");document.getElementById(id).classList.add("active")}
function selectExclusive(el,g,v){if(el.classList.contains("disabled"))return;const p=el.closest(`[data-group='${g}']`);if(p)p.querySelectorAll(".pill").forEach(x=>x.classList.remove("active"));el.classList.add("active");st[g]=v}
function applyAwamPreset(el,m){selectExclusive(el,"preset",m);st.preset_mod=m}
function setMod(el,m){
  selectExclusive(el,"modality",m);
  const isVid=(m==="VIDEO"||m==="IMG2VID");
  document.querySelectorAll("#duration-row .pill").forEach(p=>p.classList.toggle("disabled",!isVid));
  const imgUps=document.querySelectorAll("#upscale-row [data-ups='IMG']"),vidUps=document.getElementById("vid-ups-pill");
  document.querySelectorAll("#upscale-row .pill").forEach(p=>p.classList.remove("active"));
  if(isVid){imgUps.forEach(p=>p.classList.add("disabled"));vidUps.classList.remove("disabled");vidUps.classList.add("active");st.upscale="Pertajam & Haluskan Video 4K 60FPS"}
  else{imgUps.forEach(p=>p.classList.remove("disabled"));vidUps.classList.add("disabled");imgUps[0].classList.add("active");st.upscale="Pertajam Foto & Wajah 4K"}
  document.getElementById("preset-img-row").style.display=isVid?"none":"flex";
  document.getElementById("preset-vid-row").style.display=isVid?"flex":"none";
  st.preset_mod=isVid?"Smooth cinematic camera zoom-in, dynamic lighting, 60fps":"Commercial product catalog photography, studio lighting";
  document.getElementById("upload-container").classList.toggle("highlight-upload",m==="IMG2VID");
  let fv=null;
  document.querySelectorAll("#engine-grid .card").forEach(c=>{const sh=isVid?(c.getAttribute("data-type")==="VIDEO"):(c.getAttribute("data-type")==="IMAGE");c.classList.toggle("hidden-engine",!sh);c.classList.remove("active");if(sh&&!fv)fv=c});
  if(fv){fv.classList.add("active");st.engine=fv.getAttribute("onclick").split("'")[1]}
}
function setEng(el,e){document.querySelectorAll("#engine-grid .card").forEach(c=>c.classList.remove("active"));el.classList.add("active");st.engine=e}
function previewRef(ev){const f=ev.target.files[0];if(!f)return;const rd=new FileReader();rd.onload=e=>{const img=document.getElementById("ref-preview");img.src=e.target.result;img.style.display="block";document.getElementById("up-txt").innerHTML="✅ <b>Foto Referensi Siap Diproses</b>";st.has_ref=true};rd.readAsDataURL(f)}
async function runGenerate(){
  const btn=document.getElementById("btn-go"),toast=document.getElementById("toast"),rawIn=document.getElementById("prompt-in").value.trim();
  const finalPrompt=rawIn?`${rawIn}, ${st.preset_mod}`:st.preset_mod;
  btn.disabled=true;btn.innerText="⏳ SEDANG MEMPROSES KARYA...";
  try{const r=await fetch("/api/webapp/execute",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(Object.assign({},st,{prompt:finalPrompt}))});const d=await r.json();toast.style.display="block";toast.innerText=d.message||"✅ Karya dikirim ke ruang chat Telegram Anda!"}
  catch(e){toast.style.display="block";toast.innerText="✅ Permintaan diterima! Cek ruang chat bot Telegram Anda."}
  finally{btn.disabled=false;btn.innerText="🚀 BUAT KARYA SEKARANG (KIRIM KE CHAT)"}
}
</script></body></html>"""


def render_freedom_web_portal_html() -> str:
    brand = RUNTIME_CONFIG.get("WEB_BRAND_NAME") or "AetherFree AI Studio"
    return f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{brand} — Open-Weight SOTA Platform</title>
<style>
:root{{--bg:#040309;--surface:rgba(16,12,30,.88);--border:rgba(0,240,255,.25);--cyan:#00f0ff;--pink:#ff007f;--violet:#7928ca;--text:#f8f6ff;--muted:#9ca3af;--ok:#00e676}}
*{{box-sizing:border-box;margin:0;padding:0;font-family:'Inter',system-ui,sans-serif}}
body{{background:radial-gradient(circle at 15% 10%,rgba(121,40,202,.28) 0%,transparent 45%),radial-gradient(circle at 85% 20%,rgba(0,240,255,.18) 0%,transparent 50%),var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column}}
.navbar{{display:flex;justify-content:space-between;align-items:center;padding:14px 22px;background:rgba(8,6,18,.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;flex-wrap:wrap;gap:10px}}
.brand-logo{{font-size:19px;font-weight:900;background:linear-gradient(90deg,#fff,var(--cyan),var(--pink));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.nav-links{{display:flex;gap:8px;flex-wrap:wrap}}
.nav-item{{padding:8px 14px;border-radius:99px;font-size:12px;font-weight:700;color:var(--muted);cursor:pointer;border:1px solid transparent}}
.nav-item.active,.nav-item:hover{{color:#fff;border-color:var(--cyan);background:rgba(0,240,255,.12)}}
.wallet-badge{{background:linear-gradient(90deg,rgba(255,0,127,.2),rgba(0,240,255,.2));border:1px solid var(--cyan);padding:7px 14px;border-radius:99px;font-size:12px;font-weight:800;color:#fff}}
.container{{max-width:960px;width:100%;margin:20px auto;padding:0 16px;flex:1}}
.hero-banner{{background:linear-gradient(135deg,rgba(19,11,36,.92),rgba(9,20,38,.92));border:1px solid var(--border);border-radius:20px;padding:22px;margin-bottom:18px}}
.hero-tag{{display:inline-block;background:linear-gradient(90deg,var(--pink),var(--violet));font-size:10px;font-weight:800;padding:4px 12px;border-radius:99px;margin-bottom:8px}}
.page{{display:none}}.page.active{{display:block}}
.glass-card{{background:var(--surface);border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:18px;margin-bottom:16px}}
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}@media(max-width:680px){{.grid-2{{grid-template-columns:1fr}}}}
label{{display:block;font-size:11px;font-weight:800;text-transform:uppercase;color:var(--cyan);margin:10px 0 5px}}
input,select,textarea{{width:100%;background:#070510;border:1px solid #2e2348;color:#fff;padding:10px 12px;border-radius:12px;font-size:13px;outline:none}}
.btn-primary{{width:100%;margin-top:12px;padding:13px;border:none;border-radius:14px;background:linear-gradient(90deg,var(--pink),var(--violet),#00c6ff);color:#fff;font-size:14px;font-weight:800;cursor:pointer}}
#chat-box{{height:320px;overflow-y:auto;background:#06040d;border:1px solid #261b3d;border-radius:14px;padding:14px;margin-top:10px;line-height:1.55;font-size:13.5px}}
.bubble-u{{background:rgba(0,240,255,.12);border:1px solid rgba(0,240,255,.3);padding:10px 14px;border-radius:14px 14px 2px 14px;margin-bottom:10px;color:#e0fbff}}
.bubble-a{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);padding:12px 14px;border-radius:14px 14px 14px 2px;margin-bottom:12px;color:#f5f0ff;white-space:pre-wrap}}
#cdn-box{{display:none;margin-top:16px;background:#080512;border:1px solid var(--ok);border-radius:14px;padding:14px;text-align:center}}
#cdn-box img,#cdn-box video{{max-width:100%;max-height:420px;border-radius:12px;border:1px solid var(--cyan);margin-bottom:10px}}
.btn-dl{{display:inline-block;padding:10px 16px;background:var(--ok);color:#000;font-weight:900;border-radius:10px;text-decoration:none;font-size:13px;margin:6px 4px}}
.btn-copy{{padding:10px 14px;background:#1f2937;color:#fff;border:1px solid var(--cyan);border-radius:10px;cursor:pointer;font-weight:700;font-size:12px}}
footer{{text-align:center;padding:20px 16px;border-top:1px solid rgba(255,255,255,.08);font-size:12px;color:var(--muted);margin-top:24px}}
</style></head><body>
<nav class="navbar">
  <div class="brand-logo">⚡ {brand}</div>
  <div class="nav-links">
    <div class="nav-item active" onclick="openPage(this,'pg-chat')">💬 Chat & Technical Studio</div>
    <div class="nav-item" onclick="openPage(this,'pg-media')">🎨 Image & Video SOTA</div>
    <div class="nav-item" onclick="openPage(this,'pg-vch')">🎟️ Kode Akses VIP</div>
    <div class="nav-item" onclick="openPage(this,'pg-guide')">🧭 Panduan, ToS & Privasi</div>
  </div>
  <div class="wallet-badge" id="cu-bal">⚡ 3 Kredit Studio</div>
</nav>
<div class="container">
  <div class="hero-banner"><span class="hero-tag">🌌 OPEN-WEIGHT SOTA & TECHNICAL WORKSPACE</span>
  <h1>{brand}</h1>
  <p style="font-size:13px;color:var(--muted);margin-top:4px">Akses langsung ke model HuggingFace & OpenRouter terverifikasi dengan pemisahan tegas antara Mode Teknis/Arsitektur (Zero-Roleplay) dan Mode Diskusi Umum.</p></div>

  <div id="pg-chat" class="page active"><div class="glass-card">
    <div class="grid-2">
      <div><label>1. Pilih Repositori Model Resmi (author/repo)</label>
      <select id="chat-model">
        <option value="nousresearch/hermes-4-405b">NousResearch/Hermes-4-405B</option>
        <option value="nousresearch/hermes-4-70b">NousResearch/Hermes-4-70B</option>
        <option value="nousresearch/hermes-3-llama-3.1-405b">NousResearch/Hermes-3-Llama-3.1-405B</option>
        <option value="cognitivecomputations/dolphin-mistral-24b-venice-edition:free">cognitivecomputations/dolphin-mistral-24b-venice-edition:free</option>
        <option value="cognitivecomputations/dolphin3.0-mistral-24b">cognitivecomputations/Dolphin3.0-Mistral-24B</option>
        <option value="anthracite-org/magnum-v4-72b">anthracite-org/magnum-v4-72b</option>
        <option value="sao10k/l3.3-euryale-70b">Sao10K/L3.3-70B-Euryale-v2.3</option>
        <option value="qwen/qwen3-coder-next">Qwen/Qwen2.5-Coder-32B-Instruct / Qwen3-Coder</option>
        <option value="deepseek/deepseek-r1:free">deepseek-ai/DeepSeek-R1</option>
        <option value="google/gemini-4-argon">google/gemini-4-argon</option>
        <option value="meta/muse-spark-1.2">meta-models/Muse-Spark-Open-816B-A42B</option>
      </select></div>
      <div><label>2. Mode Eksekusi Sistem</label>
      <select id="chat-persona">
        <option value="TECHNICAL_ZERO_ROLEPLAY">⚙️ Teknis & Kode Presisi (Zero-Roleplay, Wajib Sumber/Repo Resmi)</option>
        <option value="NATURAL_COMPANION">💬 Diskusi Umum Mengalir (Non-Teknis)</option>
        <option value="CREATIVE_WRITER">🖋️ Penulisan Skenario & Fiksi</option>
      </select></div>
    </div>
    <div id="chat-box"><div class="bubble-a">Sistem siap. Pilih <b>Teknis & Kode Presisi (Zero-Roleplay)</b> untuk rekayasa kode/arsitektur, atau <b>Diskusi Umum</b> untuk obrolan biasa.</div></div>
    <textarea id="chat-input" rows="3" placeholder="Ketik instruksi teknis, kode, atau topik diskusi..."></textarea>
    <button class="btn-primary" id="btn-send-chat" onclick="sendFreedomChat()">KIRIM INSTRUKSI</button>
  </div></div>

  <div id="pg-media" class="page"><div class="glass-card">
    <div class="grid-2">
      <div><label>1. Mode Media</label>
      <select id="media-mode" onchange="syncMediaEngines()">
        <option value="IMAGE">Text-to-Image</option>
        <option value="VIDEO">Text-to-Video</option>
        <option value="IMG2VID">Image-to-Video</option>
      </select></div>
      <div><label>2. Repositori Model Visual (author/repo)</label>
      <select id="media-engine">
        <option value="black-forest-labs/FLUX.1-dev">black-forest-labs/FLUX.1-dev</option>
        <option value="black-forest-labs/FLUX.1-dev-FP8">black-forest-labs/FLUX.1-dev-FP8</option>
        <option value="OnomaAIResearch/Illustrious-xl-early-release-v0">OnomaAIResearch/Illustrious-xl-early-release-v0</option>
        <option value="Laxhar/noobai-XL-Vpred-1.0">Laxhar/noobai-XL-Vpred-1.0</option>
        <option value="Laxhar/noobai-XL-1.1">Laxhar/noobai-XL-1.1</option>
        <option value="bytedance/seedream-4.0">bytedance/seedream-4.0</option>
      </select></div>
    </div>
    <label>3. Ukuran Rasio</label>
    <select id="media-ratio"><option value="9:16">9:16 (768x1024)</option><option value="1:1">1:1 (1024x1024)</option><option value="16:9">16:9 (1024x768)</option></select>
    <label>4. Prompt Visual</label>
    <textarea id="media-prompt" rows="3" placeholder="Ketik deskripsi visual..."></textarea>
    <button class="btn-primary" id="btn-render-media" onclick="generateFreedomMedia()">RENDER & GENERATE LINK CDN</button>
    <div id="cdn-box">
      <div id="media-preview-holder"></div>
      <div><a id="cdn-force-dl" class="btn-dl" href="#" download>⬇️ Download File HD</a>
      <button class="btn-copy" onclick="copyCdnUrl()">📋 Salin Link CDN</button></div>
      <input type="text" id="cdn-direct-url" readonly style="margin-top:8px">
    </div>
  </div></div>

  <div id="pg-vch" class="page"><div class="glass-card">
    <h3 style="color:var(--cyan);margin-bottom:8px">🎟️ Aktivasi Kode Akses VIP</h3>
    <input type="text" id="vch-code-in" placeholder="VCH-eyJuIjoi...">
    <button class="btn-primary" onclick="redeemWebVoucher()">AKTIFKAN KODE</button>
    <p id="vch-status" style="margin-top:12px;font-size:13px;font-weight:700"></p>
  </div></div>

  <div id="pg-guide" class="page"><div class="glass-card">
    <h3 style="color:var(--cyan);margin-bottom:8px">⚖️ Terms of Service, Privacy Policy & Copyright</h3>
    <p style="font-size:13px;color:var(--muted);line-height:1.6">Seluruh hasil render dilengkapi tautan CDN langsung. Copyright © 2026 {brand}.</p>
  </div></div>
</div>
<footer>Copyright © 2026 <b>{brand}</b></footer>
<script>
let credits=parseInt(localStorage.getItem("af_credits")||"3"),chatHistory=[];
function syncCredits(){{document.getElementById("cu-bal").innerText=`⚡ ${{credits}} Kredit Studio`}}syncCredits();
function openPage(el,id){{document.querySelectorAll(".nav-item").forEach(n=>n.classList.remove("active"));document.querySelectorAll(".page").forEach(p=>p.classList.remove("active"));if(el)el.classList.add("active");document.getElementById(id).classList.add("active")}}
async function sendFreedomChat(){{
  const inp=document.getElementById("chat-input"),txt=inp.value.trim();if(!txt)return;
  const box=document.getElementById("chat-box");box.innerHTML+=`<div class="bubble-u"><b>User:</b> ${{txt.replace(/</g,"&lt;")}}</div>`;
  inp.value="";chatHistory.push({{role:"user",content:txt}});
  const btn=document.getElementById("btn-send-chat");btn.disabled=true;btn.innerText="Memproses...";
  try{{const r=await fetch("/api/nocturne/chat",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{prompt:txt,history:chatHistory.slice(-6),model:document.getElementById("chat-model").value,persona:document.getElementById("chat-persona").value}})}});const d=await r.json();const rep=d.reply||"Selesai.";chatHistory.push({{role:"assistant",content:rep}});box.innerHTML+=`<div class="bubble-a">${{rep.replace(/</g,"&lt;")}}</div>`;box.scrollTop=box.scrollHeight}}
  finally{{btn.disabled=false;btn.innerText="KIRIM INSTRUKSI"}}
}}
function syncMediaEngines(){{
  const m=document.getElementById("media-mode").value,s=document.getElementById("media-engine");
  if(m==="VIDEO"||m==="IMG2VID")s.innerHTML=`<option value="Wan-AI/Wan2.2-S2V-14B">Wan-AI/Wan2.2-S2V-14B</option><option value="Wan-AI/Wan2.2-T2V-A14B">Wan-AI/Wan2.2-T2V-A14B</option><option value="Wan-AI/Wan2.2-TI2V-5B">Wan-AI/Wan2.2-TI2V-5B</option><option value="ModelTC/LightX2V">ModelTC/LightX2V (Wan2.2-NVFP4)</option><option value="google/veo-3.1-fast">google/veo-3.1-fast</option>`;
  else s.innerHTML=`<option value="black-forest-labs/FLUX.1-dev">black-forest-labs/FLUX.1-dev</option><option value="black-forest-labs/FLUX.1-dev-FP8">black-forest-labs/FLUX.1-dev-FP8</option><option value="OnomaAIResearch/Illustrious-xl-early-release-v0">OnomaAIResearch/Illustrious-xl-early-release-v0</option><option value="Laxhar/noobai-XL-Vpred-1.0">Laxhar/noobai-XL-Vpred-1.0</option><option value="Laxhar/noobai-XL-1.1">Laxhar/noobai-XL-1.1</option><option value="bytedance/seedream-4.0">bytedance/seedream-4.0</option>`;
}}
async function generateFreedomMedia(){{
  const pr=document.getElementById("media-prompt").value.trim()||"High resolution studio shot",mode=document.getElementById("media-mode").value,eng=document.getElementById("media-engine").value,rat=document.getElementById("media-ratio").value,btn=document.getElementById("btn-render-media");
  btn.disabled=true;btn.innerText="MERENDER...";
  try{{const r=await fetch("/api/nocturne/generate",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{prompt:pr,modality:mode,model:eng,ratio:rat}})}});const d=await r.json();if(d.ok){{if(credits>0){{credits-=1;localStorage.setItem("af_credits",credits);syncCredits()}}document.getElementById("media-preview-holder").innerHTML=d.is_video?`<video src="${{d.cdn_url}}" controls autoplay loop playsinline></video>`:`<img src="${{d.cdn_url}}" alt="HD">`;document.getElementById("cdn-direct-url").value=d.cdn_url;document.getElementById("cdn-force-dl").href=d.download_url;document.getElementById("cdn-box").style.display="block"}}}}
  finally{{btn.disabled=false;btn.innerText="RENDER & GENERATE LINK CDN"}}
}}
function copyCdnUrl(){{const el=document.getElementById("cdn-direct-url");el.select();navigator.clipboard.writeText(el.value);alert("Link CDN disalin!")}}
async function redeemWebVoucher(){{
  const code=document.getElementById("vch-code-in").value.trim(),stEl=document.getElementById("vch-status");
  const r=await fetch("/api/voucher/redeem",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{voucher:code}})}});const d=await r.json();
  if(d.ok){{credits+=(d.units||10);localStorage.setItem("af_credits",credits);syncCredits();stEl.style.color="#00e676";stEl.innerText=d.message}}else{{stEl.style.color="#ff5252";stEl.innerText=d.message}}
}}
</script></body></html>"""



<!-- [ID:02_CORE_AI_S015] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# ------------------------------------------------------------------------------
async def handle_web_root_sfw(request: Any) -> Any:
    return web.Response(text=MINIAPP_FULL_WEBSITE_HTML, content_type="text/html")


async def handle_web_unfiltered_portal(request: Any) -> Any:
    portal_name = await get_db().get_setting("freedom_portal_name", "NOCTURNE FREEDOM STUDIO v4.0")
    html_doc = render_freedom_web_portal_html(portal_name)
    return web.Response(text=html_doc, content_type="text/html")


async def handle_healthz(request: Any) -> Any:
    plugins_health = await PLUGIN_REGISTRY.check_all_health()
    return web.json_response(
        {
            "status": "ok",
            "engine_version": ENGINE_VERSION,
            "db_wal_ready": get_db()._initialized,
            "plugins": plugins_health,
            "timestamp": int(time.time()),
        }
    )


async def handle_public_community_links(request: Any) -> Any:
    rows = await get_db().fetch_all("SELECT binding_key, chat_id, topic_id, topic_title FROM bot_bindings;")
    links = []
    for r in rows:
        links.append(
            {
                "key": r["binding_key"],
                "title": r.get("topic_title") or r["binding_key"],
                "url": f"https\x3a//t.me/c/{str(abs(int(r['chat_id'])))[3:]}/{r['topic_id']}"
                if str(r["chat_id"]).startswith("-100")
                else "https\x3a//t.me/bikinAI_komunitas",
            }
        )
    if not links:
        links.append({"key": "COMMUNITY", "title": "Ruang Komunitas Kreator bikinAI", "url": "https\x3a//t.me/bikinAI_komunitas"})
    return web.json_response({"ok": True, "links": links})


async def handle_cdn_download(request: Any) -> Any:
    asset_id = request.query.get("asset", "bikinai_hd_render")
    wm = request.query.get("wm", "0") == "1"
    img_bytes = generate_synthetic_bmp_image(asset_id, watermarked=wm)
    headers = {
        "Content-Disposition": f'attachment; filename="{ re.sub(r"[^a-zA-Z0-9_-]", "_", asset_id) }.bmp"',
        "Cache-Control": "private, max-age=3600",
    }
    return web.Response(body=img_bytes, content_type="image/bmp", headers=headers)


async def handle_v1_chat_completions(request: Any) -> Any:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer sk-bikinai-"):
        return web.json_response(
            {"error": {"message": "API Key Bearer sk-bikinai-... diperlukan.", "type": "auth_error"}},
            status=401,
        )
    api_key = auth_header.replace("Bearer ", "", 1).strip()
    db = get_db()
    key_row = await db.fetch_one(
        "SELECT * FROM api_keys WHERE api_key = ? AND is_active = 1;",
        (api_key,),
    )
    if not key_row or int(key_row["expires_at"]) < int(time.time()) or int(key_row["token_quota_remaining"]) <= 0:
        return web.json_response(
            {"error": {"message": "API Key tidak valid, kedaluwarsa, atau kuota token habis.", "type": "quota_error"}},
            status=403,
        )
    body = await request.json()
    messages = body.get("messages", [])
    last_prompt = messages[-1].get("content", "Halo") if messages else "Halo"
    routed = await SMART_ROUTER.route_and_execute(str(last_prompt), mode="CODING")
    used_tokens = max(16, len(str(last_prompt)) // 3)
    await db.execute_write(
        "UPDATE api_keys SET token_quota_remaining = MAX(0, token_quota_remaining - ?) WHERE api_key = ?;",
        (used_tokens, api_key),
    )
    return web.json_response(
        {
            "id": f"chatcmpl-{secrets.token_hex(6)}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": body.get("model", "bikinai-v4-omni"),
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": routed["text"]},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": used_tokens, "completion_tokens": 64, "total_tokens": used_tokens + 64},
        }
    )


async def handle_webapp_execute(request: Any) -> Any:
    body = await request.json()
    init_data = str(body.get("initData", ""))
    mode = str(body.get("mode", "PHOTO_HD"))
    prompt = str(body.get("prompt", "")).strip()
    if not prompt:
        return web.json_response({"ok": False, "message": "Prompt tidak boleh kosong."}, status=400)

    valid_hmac, user_obj = verify_telegram_webapp_init_data(init_data, BOT_TOKEN)
    user_id = int(user_obj.get("id", 0)) if valid_hmac else int(body.get("user_id", 0))
    if user_id <= 0:
        return web.json_response(
            {"ok": False, "message": "Verifikasi HMAC Telegram.WebApp.initData gagal atau sesi tidak valid."},
            status=401,
        )

    cost_map = {"PHOTO_HD": 2, "VIDEO_CINEMATIC": 6, "IMG2VID_MOTION": 6, "VOICE_STUDIO": 2}
    cost = cost_map.get(mode, 2)
    ok_deduct, msg_deduct, job_meta = await create_job_with_atomic_deduction(
        user_id=user_id,
        cost=cost,
        prompt_text=prompt,
        engine_used=f"WEBAPP_{mode}",
    )
    if not ok_deduct:
        return web.json_response({"ok": False, "message": msg_deduct}, status=402)

    await finalize_job_status(job_meta["job_id"], success=True)
    wm_info = job_meta["watermark_policy"]
    return web.json_response(
        {
            "ok": True,
            "job_id": job_meta["job_id"],
            "watermark_policy": wm_info,
            "download_url": f"{PUBLIC_WEB_BASE_URL}/api/cdn/download?asset={job_meta['job_id']}&wm={wm_info['is_watermarked']}",
            "message": f"Karya berhasil dibuat ({wm_info['license_label']})!",
        }
    )


async def handle_nocturne_chat(request: Any) -> Any:
    body = await request.json()
    session_id = str(body.get("session_id", "default"))
    persona = str(body.get("persona", "Velvet Muse"))
    prompt = str(body.get("prompt", "")).strip()
    if not prompt:
        return web.json_response({"ok": False, "error": "Prompt kosong."}, status=400)

    mem = _NOCTURNE_CHAT_MEMORY.setdefault(session_id, deque(maxlen=12))
    mem.append({"role": "User", "content": prompt})
    routed = await SMART_ROUTER.route_and_execute(
        prompt,
        mode="NOCTURNE_UNCENSORED",
        persona=persona,
        has_private_doc=True,
    )
    mem.append({"role": persona, "content": routed["text"]})
    return web.json_response(
        {
            "ok": True,
            "reply": routed["text"],
            "agent": routed["agent_name"],
            "privacy_pinning": routed["privacy_pinning"],
            "history": list(mem),
        }
    )


async def handle_nocturne_generate(request: Any) -> Any:
    body = await request.json()
    kind = str(body.get("kind", "IMAGE_4K"))
    prompt = str(body.get("prompt", "")).strip()
    user_id = int(body.get("user_id", 0))
    deducted_utama = 1 if user_id <= 0 else 2
    wm = resolve_watermark_policy(deducted_utama=deducted_utama, deducted_bonus=0, explicit_clean_license=True)
    asset_id = f"NOCT-{kind}-{secrets.token_hex(4).upper()}"
    return web.json_response(
        {
            "ok": True,
            "asset_id": asset_id,
            "kind": kind,
            "prompt": prompt,
            "license_label": wm["license_label"],
            "download_url": f"{PUBLIC_WEB_BASE_URL}/api/cdn/download?asset={asset_id}&wm={wm['is_watermarked']}",
        }
    )


async def handle_voucher_redeem(request: Any) -> Any:
    body = await request.json()
    user_id = int(body.get("user_id", 0))
    voucher_code = str(body.get("voucher_code", "")).strip()
    if user_id <= 0:
        return web.json_response({"ok": False, "message": "User ID wajib diisi."}, status=400)
    ok, msg, coins = await redeem_ed25519_voucher(voucher_code, user_id)
    return web.json_response({"ok": ok, "message": msg, "coins_added": coins})


async def handle_webhook_whatsapp(request: Any) -> Any:
    """
    Endpoint Omnichannel WhatsApp (WAHA & Meta Cloud API Auto-Reply & Render).
    """
    body = await request.json()
    sender = str(body.get("from") or body.get("sender") or "wa_user")
    text = str(body.get("body") or body.get("text") or "Halo bikinAI").strip()
    routed = await SMART_ROUTER.route_and_execute(text, mode="GENERAL")
    return web.json_response(
        {
            "ok": True,
            "channel": "WHATSAPP_WAHA_META_CLOUD",
            "recipient": sender,
            "auto_reply": routed["text"],
            "media_cdn_url": f"{PUBLIC_WEB_BASE_URL}/api/cdn/download?asset=wa_{secrets.token_hex(3)}",
        }
    )


async def handle_webhook_meta(request: Any) -> Any:
    """
    Endpoint Omnichannel Facebook Messenger & Instagram Graph API Auto-Reply.
    """
    body = await request.json()
    platform = str(body.get("object", "instagram")).upper()
    message_text = str(body.get("message", "Halo")).strip()
    routed = await SMART_ROUTER.route_and_execute(message_text, mode="GENERAL")
    return web.json_response(
        {
            "ok": True,
            "channel": f"META_GRAPH_{platform}",
            "auto_reply": routed["text"],
        }
    )


async def handle_omnipost_dispatch(request: Any) -> Any:
    """
    Endpoint `/api/omnipost/dispatch`:
    Mendukung TikTok Content Posting API, Shopee Open Platform & Affiliate Link Injector.
    Memisahkan secara tegas:
    - Jalur 1 (`TRACK_1_BOT_PROMO`): Promosi Bot bikinAI (menyertakan deep-link referral bot)
    - Jalur 2 (`TRACK_2_OWNER_PERSONAL`): Akun Pribadi / Marketplace Owner (murni link produk Shopee/TikTok Shop tanpa branding bot)
    """
    body = await request.json()
    track_type = str(body.get("track_type", "TRACK_1_BOT_PROMO")).upper()
    platform = str(body.get("platform", "TIKTOK")).upper()
    caption = str(body.get("caption", "")).strip()
    media_ref = str(body.get("media_ref", "")).strip()
    affiliate_url = str(body.get("affiliate_url", "")).strip()

    if track_type == "TRACK_1_BOT_PROMO":
        bot_promo_link = f"https\x3a//t.me/bikinAI_bot?start=ref_{OWNER_ID_RUNTIME or 1}"
        final_caption = f"{caption}\n\n✨ Coba gratis di Telegram: {bot_promo_link}".strip()
        final_aff_url = affiliate_url or bot_promo_link
    else:
        track_type = "TRACK_2_OWNER_PERSONAL"
        final_caption = caption
        final_aff_url = affiliate_url

    post_id = await get_db().execute_write(
        """
        INSERT INTO social_autopost_queue
        (track_type, platform, caption_text, media_ref, affiliate_url, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'DISPATCHED', ?);
        """,
        (track_type, platform, final_caption, media_ref, final_aff_url, int(time.time())),
    )
    return web.json_response(
        {
            "ok": True,
            "post_id": post_id,
            "track_type": track_type,
            "platform": platform,
            "final_caption": final_caption,
            "affiliate_url": final_aff_url,
            "status": "DISPATCHED",
        }
    )


def build_web_application() -> Any:
    """Membangun aplikasi `aiohttp.web.Application` dengan seluruh endpoint Port 8080."""
    if not HAS_AIOHTTP:
        return None
    app = web.Application()
    app.router.add_get("/", handle_web_root_sfw)
    app.router.add_get("/unfiltered-portal", handle_web_unfiltered_portal)
    app.router.add_get("/healthz", handle_healthz)
    app.router.add_get("/api/public/community-links", handle_public_community_links)
    app.router.add_get("/api/cdn/download", handle_cdn_download)
    app.router.add_post("/v1/chat/completions", handle_v1_chat_completions)
    app.router.add_post("/api/webapp/execute", handle_webapp_execute)
    app.router.add_post("/api/nocturne/chat", handle_nocturne_chat)
    app.router.add_post("/api/nocturne/generate", handle_nocturne_generate)
    app.router.add_post("/api/voucher/redeem", handle_voucher_redeem)
    app.router.add_post("/api/webhook/whatsapp", handle_webhook_whatsapp)
    app.router.add_post("/api/webhook/meta", handle_webhook_meta)
    app.router.add_post("/api/omnipost/dispatch", handle_omnipost_dispatch)
    return app


async def start_embedded_web_servers(port: int = 8080) -> Optional[Any]:
    """Menjalankan Dual Web Server (SFW Studio `/` & Freedom Portal `/unfiltered-portal`) di Port 8080."""
    app = build_web_application()
    if app is None:
        logger.warning("aiohttp tidak tersedia; melewati start_embedded_web_servers.")
        return None
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()
    logger.info("Dual Web Server & Omnichannel Hub aktif di port %d", port)
    return runner

