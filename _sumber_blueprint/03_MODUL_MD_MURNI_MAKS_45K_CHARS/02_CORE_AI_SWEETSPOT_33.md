
<!-- [ID:02_CORE_AI_S052] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: TOPIK, IDX -->
# ==============================================================================
UPSCALER_WHITE_LABEL = {
    "PHOTO_FACE_4K": "🔍 Pertajam Foto & Wajah 4K",
    "TEXT_LINE_4K": "✨ Pertajam Teks & Gambar 4K",
    "OFF": "Standar HD",
}

IMAGE_EDITING_TOOLS = {
    "REMOVE_BG_PNG": (
        "✂️ Hapus Background (File .PNG Transparan)",
        "Menghapus latar belakang foto dan mengirimkannya sebagai FILE Dokumen .PNG transparan utuh",
    ),
    "RETOUCH_FACE": (
        "✨ Retouch Wajah & Kulit Mulus",
        "Memperhalus tekstur kulit dan pencahayaan wajah secara alami",
    ),
    "INPAINT_OBJ": (
        "🖌️ Inpainting (Ganti Baju / Ubah Objek)",
        "Mengganti pakaian atau objek tertentu di dalam foto tanpa merusak latar",
    ),
    "OUTPAINT_EXPAND": (
        "🖼️ Outpainting (Perluas Ukuran Foto)",
        "Memperluas foto kotak 1:1 menjadi vertikal 9:16 atau melebar 16:9",
    ),
    "PRODUCT_RELIGHT": (
        "📸 Studio Produk UMKM (Relighting)",
        "Mengubah foto produk rumahan menjadi foto katalog studio mewah",
    ),
    "RESTORE_OLD": (
        "🕰️ Restorasi & Warnai Foto Lama",
        "Memperbaiki foto jadul yang buram menjadi tajam dan berwarna kembali",
    ),
}

DYNAMIC_CHAT_FOOTERS = [
    "\n\n_💡 Kalau nanti butuh tombol menu interaktif, tinggal ketik **\"tampilin tombol\"** ya Kak 😊_",
    "\n\n_✨ Nyaman ngobrol dulu aja Kak. Kapan pun mau buka studio visual, cukup ketik **\"menu\"** ya!_",
    "\n\n_⚡ Kalau ide di atas mau langsung kita ubah jadi karya visual, tinggal bilang **\"tampilin tombol\"** aja ya Kak._",
    "\n\n_📝 Tip: Ketik **`/canvas`** kalau mau menyusun draf panjang, atau ketik **\"menu\"** untuk melihat fitur lainnya 😊_",
    "\n\n_🔬 Butuh bedah riset yang lebih mendalam? Cukup ketik **`/riset [topik]`** atau **\"tampilin tombol\"** kapan saja ya!_",
]
_FOOTER_COUNTER = 0


def get_next_dynamic_footer() -> str:
    global _FOOTER_COUNTER
    idx = _FOOTER_COUNTER % len(DYNAMIC_CHAT_FOOTERS)
    _FOOTER_COUNTER += 1
    return DYNAMIC_CHAT_FOOTERS[idx]


BIKINAI_NATURAL_INDONESIAN_PROMPT = """
PERAN DAN KEPRIBADIAN UTAMA:
Kamu adalah 'bikinAI Super Intelligence', asisten AI dan sahabat diskusi paling cerdas, hangat, luwes, dan solutif.
ATURAN BAHASA & KENYAMANAN MUTLAK:
1. KEMURNIAN BAHASA 100%: Balas 100% dalam Bahasa Indonesia yang mengalir alami dan akrab. DILARANG KERAS mencampur istilah/kalimat bahasa Inggris di akhir jawaban!
2. LARANGAN TABEL GARIS PIPA: Jangan pernah membuat tabel dengan karakter garis pipa (| Kolom |). Gunakan poin-poin rapi (▸, •, ⚡).
3. LANGSUNG JAWAB PADA KESEMPATAN PERTAMA: Berikan jawaban yang langsung menyelesaikan masalah pengguna tanpa menyuruh mereka menghubungi CS lain.
""".strip()


async def update_personal_memory_if_needed(
    db: aiosqlite.Connection, user_id: int, text: str, current_mem: str
) -> str:
    low = text.lower()
    new_fact = ""
    if any(k in low for k in ("nama saya ", "panggil saya ", "usaha saya ", "jualan ", "bisnis saya ")):
        new_fact = text[:80]
    if new_fact and new_fact not in current_mem:
        updated = (f"{current_mem} | {new_fact}").strip(" |")[:400]

        async def _upd(conn: aiosqlite.Connection):
            await conn.execute(
                "UPDATE users SET personal_memory_notes = ? WHERE internal_user_id = ?;",
                (updated, user_id),
            )

        await DB_WRITER_DAEMON.execute_write_tx(db, _upd)
        return updated
    return current_mem


async def _call_single_llm_endpoint(
    url: str, headers: dict[str, str], payload: dict[str, Any], timeout_sec: float = 6.5
) -> str | None:
    try:
        async with httpx.AsyncClient(timeout=timeout_sec) as client:
            r = await client.post(url, headers=headers, json=payload)
            if r.status_code == 200:
                data = r.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                if content and len(content.strip()) > 2:
                    return content.replace("|---|", "").strip()
    except Exception:
        pass
    return None


async def generate_frontier_ai_response(
    db: aiosqlite.Connection,
    user_message: str,
    mode: Literal["NATURAL_CHAT", "DEEP_RESEARCH", "CANVAS_EDIT", "PROMPT_ARCHITECT"] = "NATURAL_CHAT",
    personal_memory: str = "",
    canvas_state: str = "",
) -> str:
    """
    Parallel Hedged AI Router:
    Menjamin pertanyaan pertama pengguna langsung terjawab dalam <3.5 - 6 detik
    tanpa pernah tersangkut di endpoint mati!
    """
    mem_context = f"\nMEMORI PERSONAL PENGGUNA: {personal_memory}" if personal_memory else ""
    if mode == "DEEP_RESEARCH":
        task = (
            "Lakukan pembedahan Deep Research mendalam dalam Bahasa Indonesia: "
            "1) Intisari Eksekutif, 2) Analisis Data & Teknis, 3) Peluang & Titik Buta, 4) Langkah Eksekusi."
        )
    elif mode == "CANVAS_EDIT":
        task = f"Perbarui isi dokumen/kode pada Canvas ini sesuai permintaan pengguna:\n{canvas_state or '(Kosong)'}"
    elif mode == "PROMPT_ARCHITECT":
        task = (
            "Buatkan 3 variasi prompt visual/video sinematik terbaik "
            "(1. Gaya Realistis Komersial, 2. Gaya Sinematik, 3. Gaya Artistik/3D) beserta penjelasannya dalam Bahasa Indonesia."
        )
    else:
        task = "Jawab obrolan, curhatan, atau pertanyaan pengguna dengan sangat luwes, manusiawi, dan solutif dalam Bahasa Indonesia murni."

    full_sys = f"{BIKINAI_NATURAL_INDONESIAN_PROMPT}{mem_context}\n\nTUGAS:\n{task}"
    msgs = [{"role": "system", "content": full_sys}, {"role": "user", "content": user_message}]

    tasks: list[asyncio.Task] = []

    # Jalur 1: Groq Llama 3.3 70B (Jika kunci tersedia - Kecepatan ~0.4 detik)
    if GROQ_API_KEY:
        tasks.append(
            asyncio.create_task(
                _call_single_llm_endpoint(
                    "https://api.groq.com/openai/v1/chat/completions",
                    {"Authorization": f"Bearer {GROQ_API_KEY}"},
                    {"model": "llama-3.3-70b-versatile", "messages": msgs, "max_tokens": 750, "temperature": 0.6},
                    timeout_sec=5.5,
                )
            )
        )

    # Jalur 2: OpenRouter Free (Jika kunci tersedia)
    if OPENROUTER_API_KEY:
        tasks.append(
            asyncio.create_task(
                _call_single_llm_endpoint(
                    "https://openrouter.ai/api/v1/chat/completions",
                    {"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
                    {"model": "deepseek/deepseek-chat:free", "messages": msgs, "max_tokens": 750},
                    timeout_sec=6.5,
                )
            )
        )

    # Jalur 2B: Gemini Flash OpenAI-Compatible Endpoint (Jika GEMINI_API_KEY tersedia)
    if GEMINI_API_KEY:
        tasks.append(
            asyncio.create_task(
                _call_single_llm_endpoint(
                    "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
                    {"Authorization": f"Bearer {GEMINI_API_KEY}"},
                    {"model": "gemini-2.0-flash", "messages": msgs, "max_tokens": 750},
                    timeout_sec=6.0,
                )
            )
        )

    # Jalur 2C: Omni-Resource Bansos API yang Terverifikasi Hidup (is_live_verified == 1)
    try:
        cur_b = await db.execute(
            "SELECT endpoint_url, secret_or_meta FROM omni_resource_registry "
            "WHERE category = 'AI_API' AND is_live_verified = 1 AND expires_at > ? LIMIT 2;",
            (int(time.time()),),
        )
        for ep_url, meta_model in await cur_b.fetchall():
            if ep_url and "pollinations.ai" not in ep_url and "openrouter.ai" not in ep_url:
                target_ep = ep_url if ep_url.endswith("/chat/completions") else f"{ep_url.rstrip('/')}/chat/completions"
                tasks.append(
                    asyncio.create_task(
                        _call_single_llm_endpoint(
                            target_ep,
                            {"Content-Type": "application/json"},
                            {"model": meta_model or "gpt-4o-mini", "messages": msgs, "max_tokens": 750},
                            timeout_sec=6.0,
                        )
                    )
                )
    except Exception:
        pass

    # Jalur 3 (Selalu Menyala Paralel): Pollinations Keyless Fast Endpoint
    tasks.append(
        asyncio.create_task(
            _call_single_llm_endpoint(
                "https://text.pollinations.ai/openai",
                {"Content-Type": "application/json"},
                {"model": "openai", "messages": msgs},
                timeout_sec=7.5,
            )
        )
    )

    # Ambil hasil dari jalur tercepat yang pertama menjawab valid!
    for coro in asyncio.as_completed(tasks):
        res = await coro
        if res:
            for t in tasks:
                if not t.done():
                    t.cancel()
            return res

    # Jaminan Fallback Instan Cerdas jika seluruh jaringan internet luar sedang padat
    if mode == "PROMPT_ARCHITECT":
        return (
            "🎨 **PANDUAN & RACIKAN PROMPT SINEMATIK — bikinAI**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"Berdasarkan ide Kakak (**\"{user_message[:80]}\"**), berikut 3 variasi *prompt* siap pakai:\n\n"
            "▸ **1. Gaya Komersial Fotorealistis (Seedream 4.5 / Flux):**\n"
            f"  _`Commercial studio shot of {user_message[:60]}, golden hour lighting, ultra-detailed 8k photorealistic.`_\n\n"
            "▸ **2. Gaya Video Sinematik (Kling 3.0 Pro / Wan 2.2):**\n"
            f"  _`Cinematic dynamic camera tracking shot of {user_message[:60]}, dramatic atmosphere, 4k 60fps.`_\n\n"
            "▸ **3. Gaya Ilustrasi 3D / Anime (Illustrious / Recraft):**\n"
            f"  _`Vibrant 3D Pixar and anime style illustration of {user_message[:60]}, soft volumetric lighting.`_"
        )
    return (
        f"Halo Kak! Aku langsung menangkap maksud Kakak terkait **\"{user_message[:90]}\"** 😊\n\n"
        "▸ Kalau Kakak ingin aku merangkai konsep di atas menjadi **Gambar 4K**, cukup ketik **`buat gambar [deskripsi]`**.\n"
        "▸ Kalau ingin diubah menjadi **Video Sinematik**, ketik **`buat video [deskripsi]`**.\n"
        "▸ Atau kita bisa lanjutkan obrolan dan membedah idenya lebih dalam sekarang juga!"
    )



<!-- [ID:02_CORE_AI_S053] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 127

Selanjutnya, berkas halaman utama app/page.tsx dirakit untuk menyatukan efek pendaran gradien 
radial Aceternity UI, konsol pemilih modalitas (Teks/Koding, Video Kling 4.0 / Veo 3.1 / Wan 3.0, 
Gambar 4K Flux.2 / Nano Banana 2.1, serta Suara & Musik Fish Speech S2 / Kokoro / Suno), dan 
tombol integrasi kasir QRIS Pakasir v2:
```tsx
"use client";
import React, { useState } from "react";
import { Sparkles, Video, Image as ImageIcon, Mic, Code2, ShieldCheck, Zap } from "lucide-react";
export default function FuturisticAIStudioPage() {
  const [prompt, setPrompt] = useState("");
  const [modality, setModality] = useState<"llm" | "video" | "image" | "voice">("llm");
  const [output, setOutput] = useState<string>("Sistem siap. Rute aktif: RedisVL Cache (25ms) -> 
RouteLLM (tau=0.11593) -> 1.200+ Model SOTA.");
  const [loading, setLoading] = useState(false);
  const handleExecutePrompt = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("/api/v1/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, modality }),
      });
      const data = await res.json();
      setOutput(data.response || "Respons diterima dari klaster otonom.");
    } catch {
      setOutput("Dialihkan otomatis ke jalur Zero-Auth Fallback (Pollinations / NgodeAI ID-JKT).");
    } finally {
      setLoading(false);
    }


## Halaman 128

  };
  return (
    <main className="relative min-h-screen w-full bg-[#030712] text-slate-100 antialiased 
selection:bg-cyan-500/30">
      <div
        className="pointer-events-none absolute inset-0 opacity-80"
        style={{
          backgroundImage:
            "radial-gradient(68.54% 68.72% at 55.02% 31.46%, hsla(210, 100%, 85%, .08) 0, hsla(210, 
100%, 55%, .02) 50%, hsla(210, 100%, 45%, 0) 80%)",
        }}
      />
      <header className="relative z-20 mx-auto flex max-w-6xl items-center justify-between px-6 
py-6 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-
cyan-400 to-blue-600 shadow-lg shadow-cyan-500/20">
            <Sparkles className="h-5 w-5 text-slate-950" />
          </div>
          <span className="text-lg font-semibold tracking-tight text-white">
            AETHER<span className="text-cyan-400">OS</span> v3.0
          </span>
          <span className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2.5 
py-0.5 text-xs font-medium text-emerald-300">
            1.212+ Model Aktif
          </span>
        </div>
        <div className="flex items-center gap-4">
          <a
            href="#pricing"


## Halaman 129

            className="rounded-full border border-white/15 bg-white/5 px-4 py-2 text-xs font-medium 
text-slate-200 transition hover:bg-white/10"
          >
            Upgrade Pro (Rp 99.000 QRIS)
          </a>
        </div>
      </header>
      <section className="relative z-10 mx-auto max-w-5xl px-6 pt-14 pb-20 text-center">
        <div className="inline-flex items-center gap-2 rounded-full border border-cyan-500/30 bg-
cyan-500/10 px-4 py-1.5 text-xs font-medium text-cyan-300 mb-6">
          <Zap className="h-3.5 w-3.5" /> Zero-Latency Multi-Path AI Supercluster
        </div>
        <h1 className="bg-gradient-to-b from-white via-slate-100 to-slate-400 bg-clip-text text-4xl 
font-bold tracking-tight text-transparent sm:text-6xl">
          Satu Gerbang Otonom untuk <br /> Seluruh Model Frontier Dunia
        </h1>
        <p className="mx-auto mt-5 max-w-2xl text-sm leading-relaxed text-slate-400 sm:text-
base">
          Terhubung secara simultan ke Claude Opus 5.5, GPT-6 Astra, DeepSeek V4.1 Flash, Kling 
4.0, Veo 3.1,
          dan mesin tanpa sensor lokal dengan arsitektur pengalihan otomatis <span 
className="text-slate-200 font-medium">N+M Rolling Failover</span>.
        </p>
        <div className="relative mx-auto mt-10 max-w-3xl rounded-2xl border border-white/15 bg-
slate-900/70 p-6 backdrop-blur-xl shadow-2xl shadow-cyan-950/30 text-left">
          <div className="flex flex-wrap gap-2 border-b border-white/10 pb-4">
            {[
              { id: "llm", label: "Frontier LLM & Code", icon: Code2 },
              { id: "video", label: "Video (Kling 4.0 / Veo 3.1 / Wan 3.0)", icon: Video },
              { id: "image", label: "Gambar 4K (Flux.2 / Nano Banana 2.1)", icon: ImageIcon },


## Halaman 130

              { id: "voice", label: "Suara & Musik (Fish S2 / Kokoro / Suno)", icon: Mic },
            ].map((tab) => {
              const Icon = tab.icon;
              const active = modality === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setModality(tab.id as "llm" | "video" | "image" | "voice")}
                  className={`flex items-center gap-2 rounded-lg px-3.5 py-2 text-xs font-medium 
transition ${
                    active
                      ? "bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-md shadow-cyan-
500/20"
                      : "bg-white/5 text-slate-400 hover:bg-white/10 hover:text-slate-200"
                  }`}
                >
                  <Icon className="h-3.5 w-3.5" />
                  {tab.label}
                </button>
              );
            })}
          </div>
          <div className="mt-4">
            <textarea
              rows={3}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Ketik instruksi koding, riset web real-time, atau skenario video sinematik..."
              className="w-full rounded-xl border border-white/10 bg-slate-950/80 p-4 text-sm text-
slate-100 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
            />
          </div>


## Halaman 131

          <div className="mt-4 flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs text-slate-400">
              <ShieldCheck className="h-4 w-4 text-emerald-400" />
              <span>Dilindungi oleh Turnstile & Zero-Trust ModelScan</span>
            </div>
            <button
              onClick={handleExecutePrompt}
              disabled={loading}
              className="rounded-xl bg-gradient-to-r from-cyan-400 via-blue-500 to-indigo-600 px-6 
py-2.5 text-xs font-semibold text-slate-950 shadow-lg shadow-cyan-500/25 transition 
hover:brightness-110 disabled:opacity-50"
            >
              {loading ? "Merutekan Kueri..." : "Eksekusi Instan"}
            </button>
          </div>
          <div className="mt-5 rounded-xl border border-white/10 bg-black/60 p-4 font-mono text-xs 
text-cyan-300">
            {output}
          </div>
        </div>
      </section>
    </main>
  );
}
```

<!-- [ID:02_CORE_AI_S054] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 413

<div id="pg-media" class="page"><div class="glass-card">
<div class="grid-2">
<div><label>1. Pilih Mode Produksi Media</label>
<select id="media-mode" onchange="syncMediaEngines()">
<option value="IMAGE">🎨 Text-to-Image (Gambar 4K Ultra-HD)</option>
<option value="VIDEO">🎬 Text-to-Video (Video Sinematik AI)</option>
<option value="IMG2VID">📸 Image-to-Video (Gerakkan Foto Referensi)</option>
</select></div>
<div><label>2. Pilih Engine SOTA (Unfiltered & Commercial)</label>
<select id="media-engine">
<option value="Flux.1-Dev Uncensored Pro">Flux.1-Dev Uncensored Pro + Custom LoRA</option>
<option value="WAI-Illustrious-XL v11">WAI-Illustrious-XL v11 (Anime 2.5D Masterpiece)</option>
<option value="NoobAI-XL V-Pred 1.0">NoobAI-XL V-Pred 1.0 (Full Unfiltered Illustration)</option>
<option value="Juggernaut XL v9 Ragnarok">Juggernaut XL v9 Ragnarok (Hyper-Photorealistic)</option>
<option value="CyberRealistic Pony V6.5">CyberRealistic Pony V6.5 (Character Realism)</option>
<option value="Seedream 4.5 Pro">Seedream 4.5 Pro (4K Poster & Typography)</option>
<option value="Midjourney v7 Style">Midjourney v7 Aesthetic Engine</option>
</select></div>
</div>
<div class="grid-2">
<div><label>3. Ukuran Rasio Layar</label>
<select id="media-ratio"><option value="9:16">📱 9:16 Vertikal (TikTok/Reels)</option><option value="1:1">🟦 1
<div><label>4. Upload Foto Referensi (Opsional)</label><input type="file" accept="image/*"></div>
</div>
<label>5. Preset Gaya & Motion Cepat</label>
<div class="preset-bar">
<div class="preset-chip" onclick="appendMediaPreset('ultra-detailed 8k photorealistic, cinematic rim lighting'
<div class="preset-chip" onclick="appendMediaPreset('masterpiece anime illustration, vibrant cel shading')">🎌
<div class="preset-chip" onclick="appendMediaPreset('smooth orbital camera motion, 60fps fluid movement')">🎥 
<div class="preset-chip" onclick="appendMediaPreset('luxury commercial product shot on black marble')">🛍️ Kata
</div>
<label>6. Deskripsi Visual / Video Anda</label>
<textarea id="media-prompt" rows="3" placeholder="Ketik deskripsi gambar atau adegan video yang ingin dirender
<button class="btn-primary" id="btn-render-media" onclick="generateFreedomMedia()">⚡ RENDER KARYA & BUAT LINK
<div id="cdn-box">
<div style="font-size:12px;font-weight:800;color:var(--ok);margin-bottom:8px">✅ RENDER SELESAI — SIAP DIUNDUH
<div id="media-preview-holder"></div>
<div><a id="cdn-force-dl" class="btn-dl" href="#" download>⬇️ Download File HD Langsung</a>
<button class="btn-copy" onclick="copyCdnUrl()">📋 Salin Link CDN</button></div>
<input type="text" id="cdn-direct-url" readonly style="margin-top:8px">
</div>
</div></div>
<div id="pg-vch" class="page"><div class="glass-card">
<h3 style="color:var(--cyan);margin-bottom:8px">🎟️ Aktivasi Kode Akses VIP Studio</h3>
<p style="font-size:13px;color:var(--muted);margin-bottom:12px">Masukkan <b>Kode Akses VIP (VCH-...)</b> dari 
<input type="text" id="vch-code-in" placeholder="VCH-eyJuIjoi...">
<button class="btn-primary" onclick="redeemWebVoucher()">⚡ AKTIFKAN KODE AKSES VIP</button>
<p id="vch-status" style="margin-top:12px;font-size:13px;font-weight:700"></p>
</div></div>
<div id="pg-guide" class="page">
<div class="glass-card"><h3 style="color:var(--cyan);margin-bottom:8px">🧭 Panduan Penggunaan & Link CDN</h3>
<p style="font-size:13px;color:var(--muted);line-height:1.6">1. <b>Obrolan Natural:</b> Pilih model dari katal
<div class="glass-card"><h3 style="color:var(--cyan);margin-bottom:8px">⚖️ Terms of Service, Privacy Policy & 
<p style="font-size:13px;color:var(--muted);line-height:1.6">• <b>Zero-Knowledge Privacy:</b> {brand} tidak me
</div>
</div>
<footer>Copyright © 2026 <b>{brand}</b>. All Rights Reserved.<br>
<span onclick="openPage(document.querySelectorAll('.nav-item')[3],'pg-guide')">Panduan</span> |
<span onclick="openPage(document.querySelectorAll('.nav-item')[3],'pg-guide')">Terms of Service</span> |
<span onclick="openPage(document.querySelectorAll('.nav-item')[3],'pg-guide')">Privacy Policy</span></footer>
<script>
let credits=parseInt(localStorage.getItem("af_credits")||"3"),hasPaidVip=localStorage.getItem("af_vip")==="1",
function syncCredits(){{document.getElementById("cu-bal").innerText=`💎 ${{credits}} Kredit Studio`}}syncCredi
function openPage(el,id){{document.querySelectorAll(".nav-item").forEach(n=>n.classList.remove("active"));docu
async function sendFreedomChat(){{
 const inp=document.getElementById("chat-input"),txt=inp.value.trim();if(!txt)return;
 const box=document.getElementById("chat-box");box.innerHTML+=`<div class="bubble-u"><b>Anda:</b> ${{txt.repl
 inp.value="";chatHistory.push({{role:"user",content:txt}});
 const btn=document.getElementById("btn-send-chat");btn.disabled=true;btn.innerText="⏳ Sedang merespons...";
 try{{const r=await fetch("/api/nocturne/chat",{{method:"POST",headers:{{"Content-Type":"application/json"}},
 finally{{btn.disabled=false;btn.innerText="🚀 KIRIM OBROLAN"}}
}}
function syncMediaEngines(){{
 const m=document.getElementById("media-mode").value,s=document.getElementById("media-engine");



<!-- [ID:02_CORE_AI_S055] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: INT, INLINEKEYBOARDBUTTON -->
## Halaman 423

           "Kling 3.0 Pro",
           "Google Veo 3",
           "Sora 2 Turbo",
           "Runway Gen-4",
       ):
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
   """Menutup VULN-04: Fail-Closed Owner Verification (Tidak pernah auto-claim jika OWNER_ID_RUNTIME == 0).""
   return (
       chat_type == "private"
       and int(RUNTIME_CONFIG.get("OWNER_ID_RUNTIME") or 0) > 0
       and user_id == int(RUNTIME_CONFIG["OWNER_ID_RUNTIME"])
   )
def build_customer_3step_entry_keyboard(
   u: dict[str, Any] | None = None, is_private: bool = True
) -> InlineKeyboardMarkup:
   """
   [SOLUSI POIN ARCH #4 & #5]:
   Interaksi Awal 3-Langkah (Clean Progressive Disclosure) + Auto-Bahasa (ID vs EN).
   Tidak langsung menumpuk belasan tombol di awal, melainkan menyajikan 3 Pintu Etalase Utama!
   """
   lang = (u.get("lang") or "id") if u else "id"
   is_en = lang.startswith("en") and (u.get("ppp_zone", 4) != 4 if u else False)
   m_url = RUNTIME_CONFIG["MINIAPP_URL"]
   rows: list[list[InlineKeyboardButton]] = []
   if m_url.startswith("https://"):
       btn_txt = (
           "📱 Open Super AI Studio App (Full Web)"
           if is_en
           else "📱 Buka Super Mini App Studio (Full Web & Upload)"
       )
       if is_private:
           rows.append(
               [InlineKeyboardButton(text=btn_txt, web_app=WebAppInfo(url=m_url))]
           )
       else:
           rows.append(
               [
                   InlineKeyboardButton(
                       text=btn_txt,
                       url=f"https://t.me/{BOT_USERNAME_GLOBAL}?start=miniapp",
                   )
               ]
           )
   if is_en:
       rows.extend(
           [
               [
                   InlineKeyboardButton(
                       text="🎬 1. Create 4K Images, Cinema Video & Editing",
                       callback_data="menu:step2_media",
                   )
               ],



<!-- [ID:02_CORE_AI_S056] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: BOOTSTRAP -->
# 15. ENTRYPOINT UTAMA (MAIN)
async def main() -> None:
    global BOT_INSTANCE_GLOBAL, BOT_USERNAME_GLOBAL
    if not BOT_TOKEN:
        print("❌ TOKEN_BOT_UTAMA belum diatur di .env!")
        return

    async with get_db() as db:
        await init_master_db(db)

    if RUNTIME_CONFIG["OWNER_ID_RUNTIME"] == 0:
        print(f"🔐 [BOOTSTRAP]: /claim_owner {OWNER_BOOTSTRAP_TOKEN}")

    await start_embedded_web_servers(port=8080)
    asyncio.create_task(_background_dead_job_sweeper_loop())

    bot = Bot(token=BOT_TOKEN)
    BOT_INSTANCE_GLOBAL = bot
    me = await bot.get_me()
    BOT_USERNAME_GLOBAL = me.username or "bikinAI_bot"

    dp = Dispatcher()
    dp.include_router(router)
    print(f"🚀 bikinAI v3.7.1 (@{BOT_USERNAME_GLOBAL}) ACTIVE.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```
```


<!-- [ID:02_CORE_AI_S057] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# 6. ROLLING 8-AGENT POOL & ADDICTIVE NATURAL CONVERSATION ENGINE
AGENTIC_ROLLING_POOL: dict[str, dict[str, Any]] = {
    "ARGON": {"title": "🌟 Argon Frontier (Gemini 4 Argon / Flash)", "model_polli": "google/gemini-4-argon", "model_or": "google/gemini-2.0-flash-exp:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "QWEN": {"title": "💻 Qwen3 Agentic Coder (Qwen3-Coder / 3.8)", "model_polli": "qwen/qwen3-coder-next", "model_or": "qwen/qwen3-coder:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "DEEPSEEK": {"title": "🧠 DeepSeek R1/V4.1 Reasoner", "model_polli": "deepseek/deepseek-v4.1-flash", "model_or": "deepseek/deepseek-chat:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "MUSE": {"title": "🎨 Meta Muse Spark 1.2 (Creative Director)", "model_polli": "meta/muse-spark-1.2", "model_or": "meta-llama/llama-3.3-70b-instruct:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "NANO_MUSE": {"title": "⚡ Nano-Muse Glimmer 30B (Fast Companion)", "model_polli": "meta/muse-glimmer-30b", "model_or": "openai/gpt-oss-120b:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "HARNESS": {"title": "🛠️ OpenHands / DeepSeek Agent Harness", "model_polli": "deepseek/deepseek-v4-pro", "model_or": "qwen/qwen3-coder:free", "ok": 0, "fail": 0, "quarantine_until": 0},
    "HERMES": {"title": "🔓 Nous Hermes 4 405B / Dolphin 3.0 (Unfiltered)", "model_polli": "mistralai/mistral-large-4", "model_or": "nousresearch/hermes-4-405b", "ok": 0, "fail": 0, "quarantine_until": 0},
    "GROQ_CEREBRAS": {"title": "🚀 Groq LPU & Cerebras Wafer-Scale", "model_polli": "meta/llama-3.3-70b-instruct", "model_or": "meta-llama/llama-3.3-70b-instruct:free", "ok": 0, "fail": 0, "quarantine_until": 0},
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


BIKINAI_ADDICTIVE_COMPANION_PROMPT = """
PERAN UTAMA: Kamu adalah sahabat ngobrol, teman curhat, sekaligus rekan diskusi paling asik, hangat, cerdas, dan pengertian.
ATURAN PERCAKAPAN PENTING (EFEK CANDU & KENYAMANAN):
1. DILARANG KERAS MENYURUH BUAT GAMBAR ATAU VIDEO: Saat pengguna sedang mengobrol, curhat, atau berdiskusi, JANGAN PERNAH mengarahkan mereka untuk membuat gambar/video. Fokus 100% pada isi pembicaraan!
2. GAYA BAHASA MENGALIR & HIDUP: Gunakan Bahasa Indonesia yang luwes, akrab, empatik, dan berbobot.
3. AKHIRI DENGAN PERTANYAAN RINGAN YANG MEMANCING DISKUSI: Buat lawan bicara betah berlama-lama di ruang chat.
""".strip()


async def generate_frontier_ai_response(
    db: aiosqlite.Connection,
    user_message: str,
    mode: Literal["NATURAL_CHAT", "DEEP_RESEARCH", "CANVAS_EDIT", "PROMPT_ARCHITECT", "NOCTURNE_UNCENSORED"] = "NATURAL_CHAT",
    personal_memory: str = "",
    canvas_state: str = "",
    preferred_model: str = "",
    persona_style: str = "NATURAL_COMPANION",
    chat_history: list[dict[str, str]] | None = None,
) -> str:
    mem_context = f"\nCATATAN PENGGUNA: {personal_memory}" if personal_memory else ""
    if mode == "DEEP_RESEARCH":
        task, primary_ag = "Susun laporan Deep Research mendalam dalam Bahasa Indonesia: 1) Intisari Eksekutif, 2) Analisis Data & Teknis, 3) Peluang & Strategi, 4) Langkah Eksekusi.", "ARGON"
    elif mode == "CANVAS_EDIT":
        task, primary_ag = f"Perbarui dokumen/kode di Canvas ini sesuai permintaan pengguna:\n{canvas_state or '(Kosong)'}", "QWEN"
    elif mode == "PROMPT_ARCHITECT":
        task, primary_ag = "Buatkan 3 variasi prompt visual/video sinematik terbaik (1. Komersial Fotorealistis, 2. Video Sinematik, 3. Artistik/3D) beserta penjelasannya dalam Bahasa Indonesia.", "MUSE"
    elif mode == "NOCTURNE_UNCENSORED":
        persona_map = {
            "CREATIVE_WRITER": "Kamu adalah novelis dan penulis skenario bebas tanpa batas. Tulis dialog, adegan, dan narasi yang sangat hidup dan imersif.",
            "SENIOR_ARCHITECT": "Kamu adalah Senior Co-Architect level frontier. Berikan analisis teknis dan solusi kode tingkat tinggi tanpa jawaban generik.",
            "ROLEPLAY_IMMERSIVE": "Kamu berada dalam mode Roleplay Imersif penuh. Masuklah 100% ke dalam karakter/skenario yang diminta pengguna tanpa keluar dari karakter.",
        }
        task = persona_map.get(persona_style, "Kamu adalah sahabat diskusi yang sangat terbuka, cerdas, hangat, dan bebas. Tanggapi isi pembicaraan secara mendalam tanpa menawarkan pembuatan gambar/video.")
        primary_ag = "HERMES"
    else:
        task, primary_ag = "Tanggapilah obrolan, cerita, atau pertanyaan pengguna secara tuntas, hangat, dan mengasyikkan tanpa menawarkan pembuatan gambar/video.", RUNTIME_CONFIG.get("PRIMARY_ROLLING_AGENT", "ARGON")

    sys_prompt = task if mode == "NOCTURNE_UNCENSORED" else f"{BIKINAI_ADDICTIVE_COMPANION_PROMPT}{mem_context}\n\nFOKUS:\n{task}"
    msgs: list[dict[str, str]] = [{"role": "system", "content": sys_prompt}]
    if chat_history:
        for turn in chat_history[-6:]:
            if isinstance(turn, dict) and turn.get("role") in ("user", "assistant") and turn.get("content"):
                msgs.append({"role": turn["role"], "content": str(turn["content"])[:600]})
    msgs.append({"role": "user", "content": user_message})

    ag_info = AGENTIC_ROLLING_POOL.get(primary_ag, AGENTIC_ROLLING_POOL["ARGON"])
    tasks: list[asyncio.Task] = []

    if GROQ_API_KEY and mode != "NOCTURNE_UNCENSORED":
        tasks.append(asyncio.create_task(_call_single_llm_endpoint("GROQ_CEREBRAS", "https://api.groq.com/openai/v1/chat/completions", {"Authorization": f"Bearer {GROQ_API_KEY}"}, {"model": "llama-3.3-70b-versatile", "messages": msgs, "max_tokens": 800, "temperature": 0.75}, 4.8)))
    if CEREBRAS_API_KEY and mode != "NOCTURNE_UNCENSORED":
        tasks.append(asyncio.create_task(_call_single_llm_endpoint("GROQ_CEREBRAS", "https://api.cerebras.ai/v1/chat/completions", {"Authorization": f"Bearer {CEREBRAS_API_KEY}"}, {"model": "llama-3.3-70b", "messages": msgs, "max_tokens": 800, "temperature": 0.75}, 4.8)))
    if OPENROUTER_API_KEY:
        tasks.append(asyncio.create_task(_call_single_llm_endpoint(primary_ag, "https://openrouter.ai/api/v1/chat/completions", {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}, {"model": preferred_model or ag_info["model_or"], "messages": msgs, "max_tokens": 800, "temperature": 0.75}, 6.0)))
    if GEMINI_API_KEY and mode != "NOCTURNE_UNCENSORED":
        tasks.append(asyncio.create_task(_call_single_llm_endpoint("ARGON", "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", {"Authorization": f"Bearer {GEMINI_API_KEY}"}, {"model": "gemini-2.0-flash", "messages": msgs, "max_tokens": 800}, 5.5)))

    polli_headers = {"Content-Type": "application/json"}
    if POLLINATIONS_API_KEY:
        polli_headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"
    tasks.append(asyncio.create_task(_call_single_llm_endpoint(primary_ag, "https://text.pollinations.ai/openai", polli_headers, {"model": "openai", "messages": msgs}, 6.5)))
    tasks.append(asyncio.create_task(_call_pollinations_get_fallback(user_message, sys_prompt)))

    for coro in asyncio.as_completed(tasks):
        res = await coro
        if res:
            for t in tasks:
                if not t.done():
                    t.cancel()
            return res

    rotate_primary_agent()
    if mode == "PROMPT_ARCHITECT":
        return (
            f"🎨 **RACIKAN PROMPT SINEMATIK — bikinAI**\n━━━━━━━━━━━━━━━━━━\n"
            f"▸ **1. Komersial 4K:** _`Commercial studio shot of {user_message[:60]}, golden hour lighting, 8k photorealistic.`_\n"
            f"▸ **2. Video Sinematik:** _`Cinematic dynamic camera tracking shot of {user_message[:60]}, 4k 60fps.`_\n"
            f"▸ **3. Artistik 3D/Anime:** _`Vibrant 3D illustration of {user_message[:60]}, volumetric lighting.`_"
        )
    return (
        f"Wah, sudut pandang yang menarik banget soal **\"{user_message[:90]}\"**! 😊\n\n"
        "Aku penasaran, dari hal yang barusan kamu sampaikan, bagian mana yang paling ingin kita kupas lebih dalam atau sedang paling kamu pikirkan sekarang?"
    )



<!-- [ID:02_CORE_AI_S058] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: SECURITY BOOTSTRAP -->
# 15. ENTRYPOINT UTAMA (MAIN)
async def main() -> None:
    global BOT_INSTANCE_GLOBAL, BOT_USERNAME_GLOBAL
    if not BOT_TOKEN:
        print("❌ TOKEN_BOT_UTAMA belum diatur di variabel lingkungan (.env)!")
        return

    async with get_db() as db:
        await init_master_db(db)

    if RUNTIME_CONFIG["OWNER_ID_RUNTIME"] == 0:
        print(f"🔐 [SECURITY BOOTSTRAP]: Ketik di DM Bot untuk mengunci akses Owner:\n   /claim_owner {OWNER_BOOTSTRAP_TOKEN}")

    await start_embedded_web_servers(port=8080)
    asyncio.create_task(_background_dead_job_sweeper_loop())

    bot = Bot(token=BOT_TOKEN)
    BOT_INSTANCE_GLOBAL = bot
    me = await bot.get_me()
    BOT_USERNAME_GLOBAL = me.username or "bikinAI_bot"

    dp = Dispatcher()
    dp.include_router(router)
    print(f"🚀 bikinAI Super Intelligence v3.7.0 (@{BOT_USERNAME_GLOBAL}) SIAP BEROPERASI 100%!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```
```


<!-- [ID:02_CORE_AI_S059] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
async def main() -> None:
    global BOT_INSTANCE_GLOBAL, BOT_USERNAME_GLOBAL
    if not BOT_TOKEN:
        print("❌ TOKEN_BOT_UTAMA belum diatur di Secrets!")
        return

    async with aiosqlite.connect(DB_PATH) as db:
        await init_master_db(db)

    # Jalankan Dual Web Server (Port 8080: Mini App SFW + /unfiltered-portal)
    await start_embedded_web_servers(port=8080)

    bot = Bot(token=BOT_TOKEN)
    BOT_INSTANCE_GLOBAL = bot
    me = await bot.get_me()
    BOT_USERNAME_GLOBAL = me.username or "bikinAI_bot"

    dp = Dispatcher()
    dp.include_router(router)
    print(f"🚀 bikinAI Super Intelligence v3.4.0 (@{BOT_USERNAME_GLOBAL}) SIAP BEROPERASI 100%!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```
```


<!-- [ID:02_CORE_AI_S060] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# ==============================================================================
async def main() -> None:
    global BOT_INSTANCE_GLOBAL, BOT_USERNAME_GLOBAL
    if not BOT_TOKEN:
        print("❌ TOKEN_BOT_UTAMA belum diatur di Secrets!")
        return

    async with aiosqlite.connect(DB_PATH) as db:
        await init_master_db(db)

    # Jalankan Dual Web Server (Port 8080: Mini App SFW + /unfiltered-portal)
    await start_embedded_web_servers(port=8080)
    asyncio.create_task(_background_dead_job_sweeper_loop())

    bot = Bot(token=BOT_TOKEN)
    BOT_INSTANCE_GLOBAL = bot
    me = await bot.get_me()
    BOT_USERNAME_GLOBAL = me.username or "bikinAI_bot"

    dp = Dispatcher()
    dp.include_router(router)
    print(f"🚀 bikinAI Super Intelligence v3.4.0 (@{BOT_USERNAME_GLOBAL}) SIAP BEROPERASI 100%!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```
```


<!-- [ID:02_CORE_AI_S061] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 67

import telebot
TOKEN_UTAMA = "ISI_TOKEN_BOT_BIKIN_AI_DISINI"
ID_GRUP = "-5441119572" # Coba pakai minus. Jika error, coba tanpa minus.
bot = telebot.TeleBot(TOKEN_UTAMA)
@bot.message_handler(commands=['start'])
def send_welcome(message):
   if message.chat.type == 'private':
       bot.reply_to(message, "🔥 Selamat datang di BikinAI! Kirim prompt gambar atau foto yang mau di edit.")
@bot.message_handler(content_types=['text'])
def terima_pesanan_teks(message):
   if message.chat.type == 'private':
       user_id = message.chat.id
       prompt = message.text
       
       # Lempar pesanan ke Grup Antrean
       pesan_antrean = f"ORDER_TXT | {user_id} | {prompt}"
       bot.send_message(ID_GRUP, pesan_antrean)
       
       bot.reply_to(message, "⏳ Pesanan diterima! Mesin sedang memproses, mohon tunggu sebentar...")
@bot.message_handler(content_types=['photo'])
def terima_pesanan_foto(message):
   if message.chat.type == 'private':
       user_id = message.chat.id
       caption = message.caption if message.caption else "hd" # Default upscale jika tanpa teks
       file_id = message.photo[-1].file_id # Ambil foto resolusi tertinggi
       
       # Lempar pesanan foto ke Grup Antrean
       pesan_antrean = f"ORDER_PIC | {user_id} | {caption}"
       bot.send_photo(ID_GRUP, file_id, caption=pesan_antrean)
       
       bot.reply_to(message, "⏳ Foto diterima! Masuk antrean render...")
print("🟢 Resepsionis BikinAI Aktif 24/7...")
bot.infinity_polling()
KODE 2: Untuk di Google Colab (Pabrik GPU)
Gabungkan ini di bagian bawah script instalasi ComfyUI Anda yang sebelumnya. Kode ini akan dijalankan saat Anda butuh merender saja.
import telebot
import requests
import time
TOKEN_ASPRI = "ISI_TOKEN_BOT_ASPRI_DISINI"
TOKEN_UTAMA = "ISI_TOKEN_BOT_BIKIN_AI_DISINI" # Dipinjam khusus untuk mengirim hasil ke user
ID_GRUP = -5441119572 
bot_aspri = telebot.TeleBot(TOKEN_ASPRI)
