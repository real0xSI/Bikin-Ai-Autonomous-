
<!-- [ID:02_CORE_AI_S013] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP -->
# 4. MINI APP SFW v3.7 (FIXED UPSCALER LOCKING + IMG2VID + PRESET AWAM) & FREEDOM WEB v3.7
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
.hero h1{font-size:18px;font-weight:800;color:#fff;margin-bottom:4px}
.hero p{font-size:12px;color:var(--muted);line-height:1.4}
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
<div class="hero"><span class="badge">⚡ STUDIO KREATIF RESMI v3.7</span><h1>Selamat Datang di bikinAI Super Intelligence</h1>
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
    <div class="card active" data-type="IMAGE" onclick="setEng(this,'Seedream 4.5')"><h4>✨ Seedream 4.5</h4><p>Poster 4K & Teks Tajam</p></div>
    <div class="card" data-type="IMAGE" onclick="setEng(this,'Flux.1 Dev')"><h4>📸 Flux.1 Dev</h4><p>Fotorealistis Natural</p></div>
    <div class="card" data-type="IMAGE" onclick="setEng(this,'Midjourney v7')"><h4>🎨 Midjourney v7</h4><p>Pencahayaan Sinematik</p></div>
    <div class="card" data-type="IMAGE" onclick="setEng(this,'Recraft V3')"><h4>📐 Recraft V3</h4><p>Desain Logo & Vektor</p></div>
    <div class="card" data-type="IMAGE" onclick="setEng(this,'Ideogram v3')"><h4>🔤 Ideogram v3</h4><p>Tipografi & Kaligrafi</p></div>
    <div class="card" data-type="IMAGE" onclick="setEng(this,'Illustrious XL')"><h4>🎌 Illustrious XL</h4><p>Anime & Ilustrasi 2.5D</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Kling 3.0 Pro')"><h4>🟣 Kling 3.0 Pro</h4><p>Gerak Halus & Sinematik</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Seedance 2.0')"><h4>🕺 Seedance 2.0</h4><p>Koreografi & Model Fashion</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Wan 2.2 Pro')"><h4>🔵 Wan 2.2 Pro</h4><p>Konsistensi Wajah & Karakter</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Google Veo 3')"><h4>🎥 Google Veo 3</h4><p>Kualitas Film & Audio Hidup</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Sora 2 Turbo')"><h4>🌌 Sora 2 Turbo</h4><p>Adegan Realistis Kompleks</p></div>
    <div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Runway Gen-4')"><h4>🎞️ Runway Gen-4</h4><p>Kontrol Kamera Presisi</p></div>
  </div>
  <div class="label">3. Pilihan Instan Orang Awam (Klik untuk Pakai Gaya / Motion Kamera)</div>
  <div class="pill-row" id="preset-img-row" data-group="preset">
    <div class="pill active" onclick="applyAwamPreset(this,'Commercial product catalog photography, luxury studio lighting')">🛍️ Katalog Produk UMKM</div>
    <div class="pill" onclick="applyAwamPreset(this,'Professional studio portrait, soft rim lighting, sharp skin texture')">👔 Foto Profil Studio</div>
    <div class="pill" onclick="applyAwamPreset(this,'Cinematic movie poster & viral YouTube thumbnail, vibrant colors')">🎬 Poster & Thumbnail</div>
    <div class="pill" onclick="applyAwamPreset(this,'Vibrant 3D Pixar & anime masterpiece illustration, volumetric light')">🎌 Anime / 3D Pixar</div>
  </div>
  <div class="pill-row" id="preset-vid-row" data-group="preset" style="display:none">
    <div class="pill active" onclick="applyAwamPreset(this,'Smooth cinematic camera zoom-in, dynamic lighting, 60fps')">🎥 Kamera Zoom Sinematik</div>
    <div class="pill" onclick="applyAwamPreset(this,'360 degree orbital camera rotation around product, luxury spotlight')">🔄 Orbit Produk 360°</div>
    <div class="pill" onclick="applyAwamPreset(this,'Fluid viral fashion dance & natural body motion, high frame rate')">🕺 Gerakan Model & Dance</div>
    <div class="pill" onclick="applyAwamPreset(this,'Epic slow-motion action, wind & glowing particles in the air')">🏃 Slow-Motion Epik</div>
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
    <div id="up-txt" style="font-size:12px">📸 <b>Sentuh untuk Upload Foto Referensi</b><br><span style="font-size:10px;color:var(--muted)">Foto Anda langsung digerakkan atau dipercantik oleh AI</span></div>
    <img id="ref-preview" alt="Ref">
  </div>
  <div class="label">8. Tulis Deskripsi Karya Anda</div>
  <textarea id="prompt-in" placeholder="Contoh: Botol parfum mewah di atas batu hitam dengan percikan air emas..."></textarea>
  <button class="btn-exec" id="btn-go" onclick="runGenerate()">🚀 BUAT KARYA SEKARANG (KIRIM KE CHAT)</button>
  <div id="toast"></div>
</div>

<div id="tab-guide" class="tab-section">
  <div class="legal-card"><h3>🪄 Rumus Mudah Membuat Prompt bagi Pemula</h3>
  <p>Gunakan rumus 3 langkah: <b>[Objek Utama] + [Gerakan/Aktivitas] + [Pencahayaan]</b>.<br>
  • Untuk <b>Foto Jadi Video</b>: Pilih tombol <b>🖼️➡️🎬 Foto Jadi Video</b>, unggah foto Anda, lalu pilih preset <b>🔄 Orbit Produk 360°</b> atau <b>🎥 Kamera Zoom Sinematik</b>!</p></div>
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
let st={init_data:"",user_id:0,username:"Kreator",modality:"IMAGE",engine:"Seedream 4.5",ratio:"9:16",duration:5,upscale:"Pertajam Foto & Wajah 4K",preset_mod:"Commercial product catalog photography, luxury studio lighting",has_ref:false};
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
  st.preset_mod=isVid?"Smooth cinematic camera zoom-in, dynamic lighting, 60fps":"Commercial product catalog photography, luxury studio lighting";
  document.getElementById("upload-container").classList.toggle("highlight-upload",m==="IMG2VID");
  let fv=null;
  document.querySelectorAll("#engine-grid .card").forEach(c=>{const sh=isVid?(c.getAttribute("data-type")==="VIDEO"):(c.getAttribute("data-type")==="IMAGE");c.classList.toggle("hidden-engine",!sh);c.classList.remove("active");if(sh&&!fv)fv=c});
  if(fv){fv.classList.add("active");st.engine=fv.querySelector("h4").innerText.replace(/^[^\w]+/,"").trim()}
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
<title>{brand} — Unrestricted Frontier AI & Creative Freedom Platform</title>
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
.preset-bar{{display:flex;gap:7px;overflow-x:auto;padding:4px 0 8px}}
.preset-chip{{white-space:nowrap;background:#140d26;border:1px solid #3a2660;color:#d8c8ff;font-size:11px;padding:7px 12px;border-radius:99px;cursor:pointer;font-weight:600}}
#cdn-box{{display:none;margin-top:16px;background:#080512;border:1px solid var(--ok);border-radius:14px;padding:14px;text-align:center}}
#cdn-box img,#cdn-box video{{max-width:100%;max-height:420px;border-radius:12px;border:1px solid var(--cyan);margin-bottom:10px}}
.btn-dl{{display:inline-block;padding:10px 16px;background:var(--ok);color:#000;font-weight:900;border-radius:10px;text-decoration:none;font-size:13px;margin:6px 4px}}
.btn-copy{{padding:10px 14px;background:#1f2937;color:#fff;border:1px solid var(--cyan);border-radius:10px;cursor:pointer;font-weight:700;font-size:12px}}
footer{{text-align:center;padding:20px 16px;border-top:1px solid rgba(255,255,255,.08);font-size:12px;color:var(--muted);margin-top:24px}}
footer span{{color:var(--cyan);cursor:pointer;margin:0 8px;font-weight:600}}
</style></head><body>
<nav class="navbar">
  <div class="brand-logo">⚡ {brand}</div>
  <div class="nav-links">
    <div class="nav-item active" onclick="openPage(this,'pg-chat')">💬 Deep Chat & Roleplay</div>
    <div class="nav-item" onclick="openPage(this,'pg-media')">🎨 Studio Gambar & Video SOTA</div>
    <div class="nav-item" onclick="openPage(this,'pg-vch')">🎟️ Kode Akses VIP</div>
    <div class="nav-item" onclick="openPage(this,'pg-guide')">🧭 Panduan, ToS & Privasi</div>
  </div>
  <div class="wallet-badge" id="cu-bal">⚡ 3 Kredit Studio</div>
</nav>
<div class="container">
  <div class="hero-banner"><span class="hero-tag">🌌 CREATIVE FREEDOM & OPEN-WEIGHT FRONTIER</span>
  <h1>Ekspresi Tanpa Batas di {brand}</h1>
  <p style="font-size:13px;color:var(--muted);margin-top:4px">Nikmati kebebasan berdiskusi, skenario roleplay, pemrograman, hingga merender karya 4K & video sinematik menggunakan koleksi lengkap SOTA Open-Weight kelas dunia.</p></div>

  <div id="pg-chat" class="page active"><div class="glass-card">
    <div class="grid-2">
      <div><label>1. Pilih Otak AI SOTA (Unfiltered & Agentic Catalog)</label>
      <select id="chat-model">
        <option value="nousresearch/hermes-4-405b">Nous Hermes 4 405B Frontier (Unfiltered Reasoning & Story)</option>
        <option value="nousresearch/hermes-4-70b">Nous Hermes 4 70B Hybrid (Fast Creative & Roleplay)</option>
        <option value="nousresearch/hermes-3-llama-3.1-405b">Nous Hermes 3 405B Instruct (Open-Weight Flagship)</option>
        <option value="cognitivecomputations/dolphin-mistral-24b-venice-edition:free">Dolphin 3.0 R1 Venice Edition (100% Uncensored)</option>
        <option value="cognitivecomputations/dolphin3.0-mistral-24b">Dolphin 3.0 Mistral 24B Instruct</option>
        <option value="anthracite-org/magnum-v4-72b">Magnum v4 72B (Prose & Immersive Storytelling)</option>
        <option value="sao10k/l3.3-euryale-70b">Sao10K Llama 3.3 Euryale 70B (Deep Character Roleplay)</option>
        <option value="google/gemini-4-argon">Argon Frontier (Deep Analysis & 1M Context)</option>
        <option value="qwen/qwen3-coder-next">Qwen 3 Coder Next (Full-Stack Architecture)</option>
        <option value="deepseek/deepseek-v4.1-flash">DeepSeek V4.1 Flash Unfiltered</option>
        <option value="meta/muse-spark-1.2">Meta Muse Spark 1.2 (Creative Ideation)</option>
      </select></div>
      <div><label>2. Mode Kepribadian & Gaya Diskusi</label>
      <select id="chat-persona">
        <option value="NATURAL_COMPANION">💫 Sahabat Diskusi Luwes, Hangat & Mendalam (Efek Candu)</option>
        <option value="CREATIVE_WRITER">🖋️ Novelis & Sutradara Skenario Tanpa Batas</option>
        <option value="SENIOR_ARCHITECT">💻 Senior Co-Architect & Strategist</option>
        <option value="ROLEPLAY_IMMERSIVE">🎭 Roleplay Karakter Imersif (100% Mengikuti Skenario)</option>
      </select></div>
    </div>
    <div id="chat-box"><div class="bubble-a">✨ Selamat datang di ruang diskusi bebas <b>{brand}</b>. Di sini kamu bebas mengobrolkan topik apa saja secara mengalir dan nyaman. Apa yang ingin kita obrolkan hari ini?</div></div>
    <textarea id="chat-input" rows="3" placeholder="Ketik obrolan, curhatan, skenario cerita, atau pertanyaanmu di sini..."></textarea>
    <button class="btn-primary" id="btn-send-chat" onclick="sendFreedomChat()">💬 KIRIM OBROLAN</button>
  </div></div>

  <div id="pg-media" class="page"><div class="glass-card">
    <div class="grid-2">
      <div><label>1. Pilih Mode Produksi Media</label>
      <select id="media-mode" onchange="syncMediaEngines()">
        <option value="IMAGE">🎨 Text-to-Image (Gambar 4K Ultra-HD)</option>
        <option value="VIDEO">🎬 Text-to-Video (Video Sinematik AI)</option>
        <option value="IMG2VID">🖼️➡️🎬 Image-to-Video (Gerakkan Foto Referensi)</option>
      </select></div>
      <div><label>2. Pilih Engine SOTA (Unfiltered & Commercial)</label>
      <select id="media-engine">
        <option value="Flux.1-Dev Uncensored Pro">Flux.1-Dev Uncensored Pro + Custom LoRA</option>
        <option value="WAI-Illustrious-XL v11">WAI-Illustrious-XL v11 (Anime / 2.5D Masterpiece)</option>
        <option value="NoobAI-XL V-Pred 1.0">NoobAI-XL V-Pred 1.0 (Full Unfiltered Illustration)</option>
        <option value="Juggernaut XL v9 Ragnarok">Juggernaut XL v9 Ragnarok (Hyper-Photorealistic)</option>
        <option value="CyberRealistic Pony V6.5">CyberRealistic Pony V6.5 (Character Realism)</option>
        <option value="Seedream 4.5 Pro">Seedream 4.5 Pro (4K Poster & Typography)</option>
        <option value="Midjourney v7 Style">Midjourney v7 Aesthetic Engine</option>
      </select></div>
    </div>
    <div class="grid-2">
      <div><label>3. Ukuran Rasio Layar</label>
      <select id="media-ratio"><option value="9:16">📱 9:16 Vertikal (TikTok/Reels)</option><option value="1:1">🟦 1:1 Persegi (Katalog)</option><option value="16:9">🖥️ 16:9 Sinematik (YouTube)</option></select></div>
      <div><label>4. Upload Foto Referensi (Opsional)</label><input type="file" accept="image/*"></div>
    </div>
    <label>5. Preset Gaya & Motion Cepat</label>
    <div class="preset-bar">
      <div class="preset-chip" onclick="appendMediaPreset('ultra-detailed 8k photorealistic, cinematic rim lighting')">📸 Fotorealistis 8K</div>
      <div class="preset-chip" onclick="appendMediaPreset('masterpiece anime illustration, vibrant cel shading')">🎌 Anime Masterpiece</div>
      <div class="preset-chip" onclick="appendMediaPreset('smooth orbital camera motion, 60fps fluid movement')">🎥 Motion 60FPS</div>
      <div class="preset-chip" onclick="appendMediaPreset('luxury commercial product shot on black marble')">🛍️ Katalog Mewah</div>
    </div>
    <label>6. Deskripsi Visual / Video Anda</label>
    <textarea id="media-prompt" rows="3" placeholder="Ketik deskripsi gambar atau adegan video yang ingin dirender..."></textarea>
    <button class="btn-primary" id="btn-render-media" onclick="generateFreedomMedia()">⚡ RENDER KARYA & BUAT LINK CDN HD</button>
    <div id="cdn-box">
      <div style="font-size:12px;font-weight:800;color:var(--ok);margin-bottom:8px">✅ RENDER SELESAI — SIAP DIUNDUH DARI CDN</div>
      <div id="media-preview-holder"></div>
      <div><a id="cdn-force-dl" class="btn-dl" href="#" download>⬇️ Download File HD Langsung</a>
      <button class="btn-copy" onclick="copyCdnUrl()">📋 Salin Link CDN</button></div>
      <input type="text" id="cdn-direct-url" readonly style="margin-top:8px">
    </div>
  </div></div>

  <div id="pg-vch" class="page"><div class="glass-card">
    <h3 style="color:var(--cyan);margin-bottom:8px">🎟️ Aktivasi Kode Akses VIP Studio</h3>
    <p style="font-size:13px;color:var(--muted);margin-bottom:12px">Masukkan <b>Kode Akses VIP (VCH-...)</b> dari Bot untuk menambahkan Kredit Studio secara instan.</p>
    <input type="text" id="vch-code-in" placeholder="VCH-eyJuIjoi...">
    <button class="btn-primary" onclick="redeemWebVoucher()">⚡ AKTIFKAN KODE AKSES VIP</button>
    <p id="vch-status" style="margin-top:12px;font-size:13px;font-weight:700"></p>
  </div></div>

  <div id="pg-guide" class="page">
    <div class="glass-card"><h3 style="color:var(--cyan);margin-bottom:8px">🧭 Panduan Penggunaan & Link CDN</h3>
    <p style="font-size:13px;color:var(--muted);line-height:1.6">1. <b>Obrolan Natural:</b> Pilih model dari katalog <i>Nous Hermes 4</i>, <i>Dolphin 3.0</i>, atau <i>Euryale</i> untuk diskusi bebas.<br>2. <b>Download via Link CDN:</b> Setiap karya dilengkapi tombol <b>Download File HD Langsung</b> beserta tautan CDN langsung.</p></div>
    <div class="glass-card"><h3 style="color:var(--cyan);margin-bottom:8px">⚖️ Terms of Service, Privacy Policy & Copyright</h3>
    <p style="font-size:13px;color:var(--muted);line-height:1.6">• <b>Zero-Knowledge Privacy:</b> {brand} tidak menyimpan identitas pribadi pengguna.<br>• <b>Ketentuan Hukum:</b> Dilarang keras membuat materi eksploitasi anak (CSAM) atau kejahatan siber.<br>• <b>Copyright © 2026 {brand}:</b> Hak cipta penuh atas hasil karya berada di tangan kreator.</p></div>
  </div>
</div>
<footer>Copyright © 2026 <b>{brand}</b> • All Rights Reserved.<br>
<span onclick="openPage(document.querySelectorAll('.nav-item')[3],'pg-guide')">Panduan</span> |
<span onclick="openPage(document.querySelectorAll('.nav-item')[3],'pg-guide')">Terms of Service</span> |
<span onclick="openPage(document.querySelectorAll('.nav-item')[3],'pg-guide')">Privacy Policy</span></footer>
<script>
let credits=parseInt(localStorage.getItem("af_credits")||"3"),chatHistory=[];
function syncCredits(){{document.getElementById("cu-bal").innerText=`⚡ ${{credits}} Kredit Studio`}}syncCredits();
function openPage(el,id){{document.querySelectorAll(".nav-item").forEach(n=>n.classList.remove("active"));document.querySelectorAll(".page").forEach(p=>p.classList.remove("active"));if(el)el.classList.add("active");document.getElementById(id).classList.add("active")}}
async function sendFreedomChat(){{
  const inp=document.getElementById("chat-input"),txt=inp.value.trim();if(!txt)return;
  const box=document.getElementById("chat-box");box.innerHTML+=`<div class="bubble-u"><b>Anda:</b> ${{txt.replace(/</g,"&lt;")}}</div>`;
  inp.value="";chatHistory.push({{role:"user",content:txt}});
  const btn=document.getElementById("btn-send-chat");btn.disabled=true;btn.innerText="⏳ Sedang merespons...";
  try{{const r=await fetch("/api/nocturne/chat",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{prompt:txt,history:chatHistory.slice(-6),model:document.getElementById("chat-model").value,persona:document.getElementById("chat-persona").value}})}});const d=await r.json();const rep=d.reply||"Ceritakan lebih lanjut!";chatHistory.push({{role:"assistant",content:rep}});box.innerHTML+=`<div class="bubble-a"><b>AI:</b> ${{rep.replace(/</g,"&lt;")}}</div>`;box.scrollTop=box.scrollHeight}}
  finally{{btn.disabled=false;btn.innerText="💬 KIRIM OBROLAN"}}
}}
function syncMediaEngines(){{
  const m=document.getElementById("media-mode").value,s=document.getElementById("media-engine");
  if(m==="VIDEO"||m==="IMG2VID")s.innerHTML=`<option value="Wan 2.2 S2V-14B Unfiltered">Wan 2.2 S2V-14B Unfiltered (Cinematic Video & Audio)</option><option value="Wan2.2-NVFP4-Sparse Fast">Wan 2.2 NVFP4 Ultra-Fast Motion</option><option value="Kling 3.0 Pro / Omni O3">Kling 3.0 Pro / Omni O3</option><option value="Seedance 2.0 Pro">Seedance 2.0 Pro</option><option value="HunyuanVideo 13B Uncensored">HunyuanVideo 13B Open-Weight</option><option value="Google Veo 3.1 Cinema">Google Veo 3.1 Cinema</option><option value="Grok Imagine Video 1.5">Grok Imagine Video 1.5</option>`;
  else s.innerHTML=`<option value="Flux.1-Dev Uncensored Pro">Flux.1-Dev Uncensored Pro + Custom LoRA</option><option value="WAI-Illustrious-XL v11">WAI-Illustrious-XL v11 (Anime / 2.5D)</option><option value="NoobAI-XL V-Pred 1.0">NoobAI-XL V-Pred 1.0 (Unfiltered Illustration)</option><option value="Juggernaut XL v9 Ragnarok">Juggernaut XL v9 Ragnarok</option><option value="CyberRealistic Pony V6.5">CyberRealistic Pony V6.5</option><option value="Seedream 4.5 Pro">Seedream 4.5 Pro</option><option value="Midjourney v7 Style">Midjourney v7 Aesthetic</option>`;
}}
function appendMediaPreset(p){{const el=document.getElementById("media-prompt");el.value=el.value.trim()?`${{el.value.trim()}}, ${{p}}`:p}}
async function generateFreedomMedia(){{
  const pr=document.getElementById("media-prompt").value.trim()||"Masterpiece futuristic portrait, neon lighting, 8k",mode=document.getElementById("media-mode").value,eng=document.getElementById("media-engine").value,rat=document.getElementById("media-ratio").value,btn=document.getElementById("btn-render-media");
  btn.disabled=true;btn.innerText="⏳ MERENDER & MENYIAPKAN LINK CDN...";
  try{{const r=await fetch("/api/nocturne/generate",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{prompt:pr,modality:mode,model:eng,ratio:rat}})}});const d=await r.json();if(d.ok){{if(credits>0){{credits-=1;localStorage.setItem("af_credits",credits);syncCredits()}}document.getElementById("media-preview-holder").innerHTML=d.is_video?`<video src="${{d.cdn_url}}" controls autoplay loop playsinline></video>`:`<img src="${{d.cdn_url}}" alt="HD">`;document.getElementById("cdn-direct-url").value=d.cdn_url;document.getElementById("cdn-force-dl").href=d.download_url;document.getElementById("cdn-box").style.display="block"}}}}
  finally{{btn.disabled=false;btn.innerText="⚡ RENDER KARYA & BUAT LINK CDN HD"}}
}}
function copyCdnUrl(){{const el=document.getElementById("cdn-direct-url");el.select();navigator.clipboard.writeText(el.value);alert("✅ Link CDN berhasil disalin!")}}
async function redeemWebVoucher(){{
  const code=document.getElementById("vch-code-in").value.trim(),stEl=document.getElementById("vch-status");
  const r=await fetch("/api/voucher/redeem",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{voucher:code}})}});const d=await r.json();
  if(d.ok){{credits+=(d.units||10);localStorage.setItem("af_credits",credits);syncCredits();stEl.style.color="#00e676";stEl.innerText="✅ "+d.message}}else{{stEl.style.color="#ff5252";stEl.innerText="❌ "+d.message}}
}}
</script></body></html>"""


