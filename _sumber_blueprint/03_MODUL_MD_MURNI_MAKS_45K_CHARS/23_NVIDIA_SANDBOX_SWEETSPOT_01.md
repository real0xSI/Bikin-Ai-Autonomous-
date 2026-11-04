
<!-- [ID:23_NVIDIA_SANDBOX_S001] SUMBER: MD:merged save.md | GRADE: PRIORITAS_1_KODE_DAN_SKEMA_LENGKAP | Tag Asli: FLOAT, SCANNER, STR, :20 -->
## Env
- INTERNAL_KEY (wajib, hanya orchestrator & payment yang pegang)

"""
Sandbox policy enforcement. Setiap scanner WAJIB panggil ini sebelum akses jaringan.
Memblokir: write, credential access, wallet signing, tx send.
"""
import os
from pathlib import Path

FORBIDDEN_ENV_VARS = [
    "PRIVATE_KEY","WALLET_PRIVATE_KEY","SEED_PHRASE","MNEMONIC",
    "BANK_API_SECRET","STRIPE_SECRET_KEY","OPENAI_API_KEY",
]

ALLOWED_HOSTS = {
    "airdrop": {"api.airdrops.io","defillama.com","dune.com","etherscan.io"},
    "bansos":  {"cek.dtsen.kemensos.go.id","kemensos.go.id","pkH.go.id"},
    "program": {"github.com","grants.gov","devpost.com","hackerone.com"},
    "nvidia":  {"nvidia.com","developer.nvidia.com","api.nvidia.com"},
}

class SandboxViolation(Exception): pass

def assert_clean_env():
    for var in FORBIDDEN_ENV_VARS:
        if os.environ.get(var):
            raise SandboxViolation(f"credential_leak: env {var} exposed to scanner")

def assert_host_allowed(scanner: str, host: str):
    allowed = ALLOWED_HOSTS.get(scanner, set())
    if host not in allowed:
        raise SandboxViolation(f"host_not_allowed: {host} for {scanner}")

def assert_read_only(method: str):
    if method.upper() in {"POST","PUT","PATCH","DELETE"}:
        raise SandboxViolation(f"write_method_blocked: {method}")

def enforce(scanner: str, host: str, method: str = "GET"):
    assert_clean_env()
    assert_host_allowed(scanner, host)
    assert_read_only(method)

import time
from collections import defaultdict

BUCKETS: dict[str, list[float]] = defaultdict(list)

def allow(scanner: str, max_per_min: int = 10) -> bool:
    now = time.time()
    window = [t for t in BUCKETS[scanner] if now - t < 60]
    if len(window) >= max_per_min:
        return False
    window.append(now)
    BUCKETS[scanner] = window
    return True

"""
Radar airdrop — READ ONLY.
Output: intel report. BUKAN klaim otomatis.
"""
import httpx
from services.scanner import sandbox, ratelimit
from services.scanner.report import IntelReport, write_report

async def scan(keywords: list[str] | None = None) -> dict:
    if not ratelimit.allow("airdrop", max_per_min=10):
        return {"ok": False, "reason": "rate_limited"}

    host = "api.airdrops.io"
    sandbox.enforce("airdrop", host, "GET")

    findings = []
    async with httpx.AsyncClient(timeout=15) as c:
        try:
            r = await c.get(f"https://{host}/v1/airdrops",
                            params={"status": "active"})
            for item in (r.json().get("data") or [])[:20]:
                findings.append({
                    "name": item.get("name"),
                    "chain": item.get("chain"),
                    "risk_flags": item.get("risk_flags", []),
                    "source": host,
                })
        except Exception as e:
            return {"ok": False, "reason": f"fetch_error: {e}"}

    report = IntelReport(
        scanner="airdrop",
        findings=findings,
        escalate_to=["S008_ThreatIntelAnalyst","S010_FraudDetectionEngineer"],
    )
    path = write_report(report)
    return {"ok": True, "report": str(path), "count": len(findings)}

"""
Radar bansos — READ ONLY. Jangan pernah submit form, jangan auto-claim.
"""
import httpx
from services.scanner import sandbox, ratelimit
from services.scanner.report import IntelReport, write_report

async def scan(region: str = "nasional") -> dict:
    if not ratelimit.allow("bansos", max_per_min=5):
        return {"ok": False, "reason": "rate_limited"}

    host = "cek.dtsen.kemensos.go.id"
    sandbox.enforce("bansos", host, "GET")

    findings = []
    async with httpx.AsyncClient(timeout=15) as c:
        try:
            r = await c.get(f"https://{host}/api/program",
                            params={"wilayah": region})
            for item in (r.json().get("program") or [])[:20]:
                findings.append({
                    "program": item.get("nama"),
                    "wilayah": item.get("wilayah"),
                    "deadline": item.get("deadline"),
                    "verified": item.get("verified", False),
                })
        except Exception as e:
            return {"ok": False, "reason": f"fetch_error: {e}"}

    report = IntelReport(
        scanner="bansos",
        findings=findings,
        escalate_to=["S010_FraudDetectionEngineer","H007_AbuseFraudAnalyst"],
    )
    return {"ok": True, "report": str(write_report(report)), "count": len(findings)}

"""
Bot pencari program (grant, hackathon, bounty) — READ ONLY.
Tidak boleh auto-apply. Hanya kumpulkan opportunity.
"""
import httpx
from services.scanner import sandbox, ratelimit
from services.scanner.report import IntelReport, write_report

async def scan(query: str = "ai grant") -> dict:
    if not ratelimit.allow("program", max_per_min=5):
        return {"ok": False, "reason": "rate_limited"}

    host = "github.com"
    sandbox.enforce("program", host, "GET")

    findings = []
    async with httpx.AsyncClient(timeout=15) as c:
        try:
            r = await c.get(
                "https://api.github.com/search/repositories",
                params={"q": query, "sort": "stars", "per_page": 10},
                headers={"Accept": "application/vnd.github+json"},
            )
            for item in (r.json().get("items") or []):
                findings.append({
                    "name": item.get("full_name"),
                    "url": item.get("html_url"),
                    "stars": item.get("stargazers_count"),
                    "license": (item.get("license") or {}).get("spdx_id"),
                    "tags": ["repo", "opportunity"],
                })
        except Exception as e:
            return {"ok": False, "reason": f"fetch_error: {e}"}

    report = IntelReport(
        scanner="program_finder",
        findings=findings,
        escalate_to=["B006_BusinessAnalyst"],
    )
    return {"ok": True, "report": str(write_report(report)), "count": len(findings)}

"""
NVIDIA Spectrum scan — READ ONLY.
Output: security report + evidence hash (sha256) untuk audit.
Tidak boleh: kirim payload, jalankan binary lokal, tanda tangan apa pun.
"""
import hashlib, json, httpx
from services.scanner import sandbox, ratelimit
from services.scanner.report import IntelReport, write_report

async def scan(target: str) -> dict:
    if not ratelimit.allow("nvidia", max_per_min=5):
        return {"ok": False, "reason": "rate_limited"}

    host = "api.nvidia.com"
    sandbox.enforce("nvidia", host, "GET")

    evidence = {"target": target, "scanner": "nvidia_spectrum"}
    findings = []
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.get(f"https://{host}/v1/spectrum/scan",
                            params={"target": target})
            data = r.json()
            findings = data.get("vulnerabilities", [])
            evidence["response_digest"] = hashlib.sha256(
                json.dumps(data, sort_keys=True).encode()
            ).hexdigest()
    except Exception as e:
        return {"ok": False, "reason": f"scan_error: {e}"}

    report = IntelReport(
        scanner="nvidia_spectrum",
        findings=findings,
        evidence=evidence,
        escalate_to=["S008_ThreatIntelAnalyst","S016_IncidentResponseEngineer"],
    )
    return {"ok": True, "report": str(write_report(report)),
            "count": len(findings), "evidence_hash": evidence["response_digest"]}

import json, time, hashlib
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List

OUT = Path("services/scanner/reports")
OUT.mkdir(parents=True, exist_ok=True)

@dataclass
class IntelReport:
    scanner: str
    findings: List[dict]
    escalate_to: List[str]
    evidence: dict = field(default_factory=dict)
    ts: float = field(default_factory=time.time)

def write_report(report: IntelReport) -> Path:
    payload = asdict(report)
    payload["hash"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()
    p = OUT / f"{report.scanner}_{int(report.ts)}.json"
    p.write_text(json.dumps(payload, indent=2))
    return p

from fastapi import FastAPI, Header, HTTPException
import os
from services.scanner import airdrop, bansos, program_finder, nvidia_spectrum

app = FastAPI(title="Scanner Service (READ-ONLY)")
INTERNAL_KEY = os.environ.get("INTERNAL_KEY", "")

def _auth(k: str):
    if not INTERNAL_KEY or k != INTERNAL_KEY:
        raise HTTPException(401, "unauthorized")

@app.get("/scan/airdrop")
async def s_airdrop(x_internal_key: str = Header(default="")):
    _auth(x_internal_key); return await airdrop.scan()

@app.get("/scan/bansos")
async def s_bansos(region: str = "nasional", x_internal_key: str = Header(default="")):
    _auth(x_internal_key); return await bansos.scan(region)

@app.get("/scan/program")
async def s_program(q: str = "ai grant", x_internal_key: str = Header(default="")):
    _auth(x_internal_key); return await program_finder.scan(q)

@app.get("/scan/nvidia")
async def s_nvidia(target: str, x_internal_key: str = Header(default="")):
    _auth(x_internal_key); return await nvidia_spectrum.scan(target) (skillspector)


<!-- [ID:23_NVIDIA_SANDBOX_S002] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
## Halaman 126

Setelah komponen terpasang, berkas app/globals.css dikonfigurasi menggunakan direktif @theme 
inline pada Tailwind CSS v4 untuk mendefinisikan animasi sorotan cahaya (*spotlight*) di atas 
kanvas gelap obsidian:
```css
@import "tailwindcss";
@theme inline {
  --animate-spotlight: spotlight 2s ease 0.75s 1 forwards;
}
@keyframes spotlight {
  0% {
    opacity: 0;
    transform: translate(-72%, -62%) scale(0.5);
  }
  100% {
    opacity: 1;
    transform: translate(-50%, -40%) scale(1);
  }
}
:root {
  color-scheme: dark;
}
body {
  background-color: #030712;
  color: #f9fafb;
  font-feature-settings: "cv02", "cv03", "cv04", "cv11";
  overflow-x: hidden;
}
```



<!-- [ID:23_NVIDIA_SANDBOX_S003] SUMBER: MD:merged save.md | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL -->
# Konfigurasi persisten memory & sandbox safety
openclaw config set sandbox.backend e2b
openclaw config set auto_upgrade.license_filter "MIT,Apache-2.0"
openclaw daemon start --cron "0 2 * * *" --task "
```
```


<!-- [ID:23_NVIDIA_SANDBOX_S004] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 135

    "postcss": "^8.5.2",​
    "tailwindcss": "^4.0.6",​
    "typescript": "^5.7.3"​
  }​
}​
 
lib/utils.ts 
Fungsi standar penggabungan kelas Tailwind CSS: 
import { ClassValue, clsx } from "clsx";​
import { twMerge } from "tailwind-merge";​
​
export function cn(...inputs: ClassValue[]) {​
  return twMerge(clsx(inputs));​
}​
 
app/globals.css 
Konfigurasi styling Tailwind CSS v4 dengan animasi custom spotlight dan efek sorotan neon: 
@import "tailwindcss";​
​
@theme inline {​
  --animate-spotlight: spotlight 2.5s ease 0.75s 1 forwards;​
  --animate-pulse-slow: pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;​
}​
​
@keyframes spotlight {​
  0% {​
    opacity: 0;​
    transform: translate(-72%, -62%) scale(0.6);​
  }​
  100% {​
    opacity: 1;​
    transform: translate(-50%, -40%) scale(1);​
  }​
}​
​
:root {​
  color-scheme: dark;​
}​
​
body {​
  background-color: #030712;​
  color: #f3f4f6;​
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
"Helvetica Neue", Arial, sans-serif;​



<!-- [ID:23_NVIDIA_SANDBOX_S005] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# [1] Mode Sandbox / Uji Coba Gratis Rp 0 (Pollinations + HF Free + 
Sample Video Cepat) -> PAKAI INI SAAT TESTING!​

<!-- [ID:23_NVIDIA_SANDBOX_S006] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# [1] Gaya "Sultan Super-App" (Banner Video Animasi + Kartu Saldo + 
Grid Lengkap)​

<!-- [ID:23_NVIDIA_SANDBOX_S007] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# [2] Gaya "Minimalis Cepat" (Fokus ruang chat bersih ala 
Gemini/ChatGPT)​

<!-- [ID:23_NVIDIA_SANDBOX_S008] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 84

Gelombang Prioritas 
Nama Layanan & 
Tautan Resmi 
Fungsi Utama dalam 
Sistem Kita 
Biaya 
9Router): 
[https://profile.aws.ama
zon.com/](https://profile
.aws.amazon.com/) 10. 
NVIDIA NIM (Kredit 
LLM Gratis): 
[https://build.nvidia.com
/](https://build.nvidia.co
m/) 
🔵 GELOMBANG 2 
(Daftar Saat Siap Buka 
Kasir QRIS & Mesin 
Komersial 
Pay-Per-Use) 
11. Pakasir (Gateway 
QRIS Kreator): 
[https://pakasir.com/](ht
tps://pakasir.com/) 12. 
Tripay / Duitku 
(Alternatif QRIS): 
[https://tripay.co.id/](htt
ps://tripay.co.id/) / 
[https://www.duitku.com
/](https://www.duitku.co
m/) 13. Fal.ai (API 
Kling, Veo, Wan, 
Flux): 
[https://fal.ai/dashboard
/keys](https://fal.ai/dash
board/keys) 14. Novita 
AI (API Unfiltered 
Murah): 
[https://novita.ai/](https:
//novita.ai/) 15. 
Replicate (Upscale 4K 
& Motion): 
[https://replicate.com/ac
count/api-tokens](https:
//replicate.com/account/
api-tokens) 16. PiAPI 
(API Musik Suno & 
Udio): 
[https://piapi.ai/](https://
piapi.ai/) 17. 
WaveSpeed AI 
(Render Cepat 
Wan/LTX): 
[https://wavespeed.ai/](
https://wavespeed.ai/) 
Menghidupkan kasir 
QRIS otomatis dan 
membuka seluruh 
mesin komersial Tier 
Pro & Tier Ultra pada 
saklar 
PILIHAN_MESIN_MED
IA = 2 tanpa risiko 
sewa GPU per jam. 
Deposit sesuai 
pemakaian pembeli 
🟣 GELOMBANG 3 
18. Vast.ai (Sewa GPU Mengalihkan saklar ke Sesuai skala ekspansi 



<!-- [ID:23_NVIDIA_SANDBOX_S009] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
### Tahap 3: Kurikulum Evaluasi Komparatif di Kotak Pasir E2B
Alih-alih langsung mengganti modul produksi dengan repositori baru yang belum teruji, sistem 
menerapkan paradigma empat lapis dari RangeKing/self-evolving-agent yang berjalan di atas 
OpenClaw, yakni *Diagnosis Layer* (menganalisis akar masalah kapabilitas saat ini), *Curriculum 
Layer* (menyusun skenario latihan dan kriteria kelulusan), *Evaluation Ladder* (memisahkan 
antara sekadar mencatat keberadaan alat baru dan benar-benar menguasainya), serta *Promotion 
Gate* (gerbang persetujuan promosi). Kandidat pustaka baru diinstal di dalam lingkungan kotak 
pasir awan terisolasi E2B Sandbox (@computesdk/e2b, yang menyediakan kredit penggunaan 
awal US$100 gratis tanpa kartu kredit) di bawah pembatasan hak akses minimum dari Microsoft 
Agent Governance Toolkit. Di dalam kotak pasir E2B tersebut, skrip evaluasi scripts/run-evals.py 
dan scripts/run-benchmark.py menjalankan pengujian *model-in-the-loop* yang mengadu performa 
kandidat repositori baru secara langsung melawan modul lama yang sedang berjalan di produksi 
berdasarkan kecepatan waktu respons, konsumsi memori RAM/VRAM, dan akurasi keluaran.

<!-- [ID:23_NVIDIA_SANDBOX_S010] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 13

Memverifikasi Keamanannya 
Dalam permintaan Anda, Anda menyebutkan bahwa "ratusan website bertebaran bisa 
didapatkan" dan membutuhkan daftar live terbaru dari ratusan situs tersebut. Berdasarkan 
pemetaan repositori komunitas dan sistem pemantauan endpoint aktif per Oktober 2026, 
ratusan situs tersebut terbagi ke dalam dua sumber utama: Indeks Direktori AI Gratis 
Terkurasi dan Ratusan Situs AI Relay / Reverse Proxy. 
1. Empat Direktori Induk yang Mengindeks Ratusan Website AI Gratis 
(Live Oktober 2026) 
Daripada mencari satu per satu secara acak, para pengembang merujuk pada empat indeks 
live berikut yang memetakan ratusan layanan dan model gratis: 
Pertama, No Cost AI (https://github.com/zebbern/no-cost-ai / Web: 
https://nocostai.vercel.app) mengindeks 80+ layanan AI gratis yang dipisahkan secara tegas 
antara layanan NO Signup (Tanpa Daftar Sama Sekali) dan layanan dengan registrasi cepat. 
Untuk kategori Chat, Riset & Coding Tanpa Login, direktori ini mencatat lmarena.ai (40+ model 
frontier tanpa batas), g4f.dev (200+ model), t3.chat, perplexity.ai (3 pencarian Pro/hari tanpa 
login menggunakan GPT-4.1 & Claude 4.0 Sonnet, ditambah pencarian dasar tak terbatas), 
heck.ai (50 kueri/hari + 5 pencarian web/hari untuk deepseek-r1-pro, gemini-2.5-flash, 
llama-4-scout), sur.pollinations.ai, sharedchat.cn (o3, o3-pro, o4-mini-high), chat2.free2gpt.com, 
chat4.free2gpt.com, free.netfly.top, chat.ai365vip.com, dan copilot.microsoft.com (gpt-5 teks tak 
terbatas + 1 gambar/hari tanpa login). Untuk kategori Gambar, Video, Suara & Musik, situs 
tanpa login mencakup vheer.com (gambar tanpa batas & tanpa watermark), 
perchance.org/wtr90dexsn (gambar tanpa batas via Pollinations API), runwayml.com (Gen-4), 
fotor.com, ttsmp3.com, voicegenerator.io, dan fakeyou.com. Sementara itu, situs media populer 
dengan kuota harian/bulanan gratis setelah login meliputi suno.com (suno-v4.5-all, gratis 50 
kredit atau 10 lagu/hari), udio.com (gratis 10 kredit atau 3–5 lagu/hari), app.pixverse.ai (gratis 
50–60 generasi video/hari), krea.ai (50 generasi/hari), ideogram.ai (40 gambar/minggu), pika.art 
(80 kredit/bulan), genmo.ai (mochi-1), elevenlabs.io (~10.000 karakter/bulan), stableaudio.com, 
dan riffusion.com, ditambah IDE coding Rovo Dev Agents (beta gratis 20 juta token Claude 4 
Sonnet/hari) dan anyapi.ai (200 req/hari tanpa kartu kredit). 
Kedua, AYAutomate Free AI Models (https://www.ayautomate.com/free-models) 
merupakan direktori interaktif yang memetakan 294 model dan API AI gratis lengkap dengan 
filter modalitas (Text, Code, Image, Video, Audio, Embeddings) serta penanda 🔓 No login dan 
✓ no card. Direktori ini mendokumentasikan penyedia dengan tier gratis tanpa kartu kredit 
seperti OpenCode Zen (MiMo-V2.5 Free, DeepSeek V4.1 Flash Free, Nemotron 3 Ultra Free, 
Big Pickle), Ollama Cloud (30+ model cloud termasuk Kimi K2.6, DeepSeek V4 Pro, MiniMax 
M3, Qwen3 Coder 480B, GLM 5.1), NVIDIA NIM (90+ model gratis ~40 RPM termasuk 
DeepSeek V4 Pro, MiniMax M3, Mistral Large 675B, Qwen3.5 400B VLM, Step 3.7 Flash), 
Google AI Studio / Gemini (Gemini 3.5 Flash 15 RPM / 1.500 RPD, Gemini 3.1 Pro Preview), 
Groq (Llama 3.3 70B, GPT OSS 120B), Cerebras, Cloudflare Workers AI (60+ model, 10.000 
Neurons/hari gratis termasuk @cf/moonshotai/kimi-k2.7-code), GitHub Models, Scaleway 
(GPT OSS 120B), dan OVHcloud AI Endpoints (Qwen3.6-27B gratis 2 RPM secara anonim 
tanpa kunci). 
Ketiga dan keempat, repositori Awesome Free LLM APIs 
(https://github.com/mnfst/awesome-free-llm-apis) (более 11.300 bintang di GitHub) dan 



<!-- [ID:23_NVIDIA_SANDBOX_S011] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 12. 3-Step Progressive UX (Auto ID/EN), Animasi Render, Wizard & Auto-CS Bot

<!-- [ID:23_NVIDIA_SANDBOX_S012] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 410

.pill.disabled{opacity:.22;pointer-events:none;cursor:not-allowed;filter:grayscale(1)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.card{background:var(--surface);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:10px;cursor:
.card.active{border-color:var(--cyan);background:rgba(0,240,255,.12)}.card.hidden-engine{display:none}
.card h4{font-size:13px;color:#fff;margin-bottom:2px}.card p{font-size:10px;color:var(--muted)}
.upload-box{border:1.5px dashed rgba(0,240,255,.4);background:rgba(15,21,35,.6);border-radius:14px;padding:12p
.upload-box.highlight-upload{border-color:#00e676;background:rgba(0,230,118,.08)}
.upload-box input{position:absolute;inset:0;opacity:0;cursor:pointer}
#ref-preview{max-height:110px;border-radius:8px;margin-top:8px;display:none;margin-left:auto;margin-right:auto
textarea{width:100%;height:80px;background:var(--surface);border:1px solid rgba(0,240,255,.3);border-radius:12
.btn-exec{width:100%;margin-top:12px;padding:14px;border:none;border-radius:14px;background:linear-gradient(90
#toast{margin-top:10px;padding:10px;border-radius:10px;font-size:12px;background:rgba(0,230,118,.15);border:1p
.legal-card{background:var(--surface);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:14px;m
.legal-card h3{color:var(--cyan);font-size:14px;margin-bottom:6px}
.topic-btn{display:block;background:rgba(0,240,255,.1);border:1px solid rgba(0,240,255,.3);color:#fff;text-dec
.footer-copy{text-align:center;font-size:11px;color:var(--muted);margin-top:18px;padding-top:12px;border-top:1
.bottom-nav{position:fixed;bottom:0;left:0;right:0;height:62px;background:rgba(8,12,22,.96);backdrop-filter:bl
.nav-btn{display:flex;flex-direction:column;align-items:center;gap:2px;color:var(--muted);font-size:10px;font-
</style></head><body>
<div class="hero"><span class="badge">⚡ STUDIO KREATIF RESMI v4.0</span><h1>Selamat Datang di bikinAI Super I
<p id="welcome-user">Platform Studio Visual 4K, Video Sinematik, & Foto Jadi Video. Koin Utama bebas watermark
<div id="tab-studio" class="tab-section active">
<div class="label">1. Pilih Kategori Karya</div>
<div class="pill-row" data-group="modality">
<div class="pill active" onclick="setMod(this,'IMAGE')">🎨 Gambar 4K</div>
<div class="pill" onclick="setMod(this,'VIDEO')">🎬 Buat Video AI</div>
<div class="pill" onclick="setMod(this,'IMG2VID')">📸 Foto Jadi Video</div>
<div class="pill" onclick="setMod(this,'REMOVE_BG')">✂️ Hapus BG (.PNG)</div>
<div class="pill" onclick="setMod(this,'RETOUCH')">✨ Retouch & Edit</div>
</div>
<div class="label">2. Pilih Mesin AI Utama</div>
<div class="grid" id="engine-grid">
<div class="card active" data-type="IMAGE" onclick="setEng(this,'Seedream 4.5')"><h4>✨ Seedream 4.5</h4><p>Po
<div class="card" data-type="IMAGE" onclick="setEng(this,'Flux.1 Dev')"><h4>📸 Flux.1 Dev</h4><p>Fotorealistis
<div class="card" data-type="IMAGE" onclick="setEng(this,'Midjourney v7')"><h4>🎨 Midjourney v7</h4><p>Pencaha
<div class="card" data-type="IMAGE" onclick="setEng(this,'Recraft V3')"><h4>📐 Recraft V3</h4><p>Desain Logo &
<div class="card" data-type="IMAGE" onclick="setEng(this,'Ideogram v3')"><h4>🔤 Ideogram v3</h4><p>Tipografi &
<div class="card" data-type="IMAGE" onclick="setEng(this,'Illustrious XL')"><h4>🎌 Illustrious XL</h4><p>Anime
<div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Kling 3.0 Pro')"><h4>🟣 Kling 3.0 Pro<
<div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Seedance 2.0')"><h4>🕺 Seedance 2.0</h
<div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Wan 2.2 Pro')"><h4>🔵 Wan 2.2 Pro</h4>
<div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Google Veo 3')"><h4>🎥 Google Veo 3</h
<div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Sora 2 Turbo')"><h4>🌌 Sora 2 Turbo</h
<div class="card hidden-engine" data-type="VIDEO" onclick="setEng(this,'Runway Gen-4')"><h4>🎞️ Runway Gen-4</h
</div>
<div class="label">3. Pilihan Instan Orang Awam (Klik untuk Pakai Gaya / Motion Kamera)</div>
<div class="pill-row" id="preset-img-row" data-group="preset">
<div class="pill active" onclick="applyAwamPreset(this,'Commercial product catalog photography, luxury studio 
<div class="pill" onclick="applyAwamPreset(this,'Professional studio portrait, soft rim lighting, sharp skin t
<div class="pill" onclick="applyAwamPreset(this,'Cinematic movie poster & viral YouTube thumbnail, vibrant col
<div class="pill" onclick="applyAwamPreset(this,'Vibrant 3D Pixar & anime masterpiece illustration, volumetric
</div>
<div class="pill-row" id="preset-vid-row" data-group="preset" style="display:none">
<div class="pill active" onclick="applyAwamPreset(this,'Smooth cinematic camera zoom-in, dynamic lighting, 60f
<div class="pill" onclick="applyAwamPreset(this,'360 degree orbital camera rotation around product, luxury spo
<div class="pill" onclick="applyAwamPreset(this,'Fluid viral fashion dance & natural body motion, high frame r
<div class="pill" onclick="applyAwamPreset(this,'Epic slow-motion action, wind & glowing particles in the air'
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
<div class="pill active" data-ups="IMG" onclick="selectExclusive(this,'upscale','Pertajam Foto & Wajah 4K')">🔍
<div class="pill" data-ups="IMG" onclick="selectExclusive(this,'upscale','Pertajam Teks & Gambar 4K')">✨ Pert



<!-- [ID:23_NVIDIA_SANDBOX_S013] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==============================================================================
UPSCALER_WHITE_LABEL = {
   "PHOTO_FACE_4K": "🔍 Pertajam Foto & Wajah 4K",
   "TEXT_LINE_4K": "✨ Pertajam Teks & Gambar 4K",
   "VIDEO_4K_60FPS": "🎞️ Pertajam & Haluskan Video 4K 60FPS",
   "OFF": "Standar HD",
}
AWAM_VIDEO_MOTION_PRESETS = {
   "ZOOM_CINEMATIC": (
       "🎥 Kamera Zoom Sinematik",
       "smooth cinematic camera zoom-in, dramatic lighting, 60fps",
   ),
   "ORBIT_360": (
       "🔄 Orbit Produk 360°",
       "360 degree orbital camera rotation around subject, studio spotlight",
   ),
   "DANCE_FASHION": (
       "💃 Gerakan Model & Dance",
       "fluid viral fashion model movement & natural choreography",
   ),
   "SLOWMO_EPIC": (
       "⚡ Slow-Motion Epik",
       "epic slow-motion action, glowing atmosphere, high frame rate",
   ),
}
AWAM_IMAGE_STYLE_PRESETS = {
   "UMKM_CATALOG": (
       "🛍️ Katalog Produk UMKM",
       "luxury commercial product photography, studio lighting, 8k",
   ),
   "STUDIO_PORTRAIT": (
       "👔 Foto Profil Studio",
       "professional executive portrait, soft rim lighting, sharp focus",
   ),
   "POSTER_THUMB": (
       "🎬 Poster & Thumbnail",
       "viral movie poster & YouTube thumbnail composition, vibrant colors",
   ),
   "ANIME_PIXAR": (
       "🎌 Anime / 3D Pixar",
       "vibrant 3D Pixar & anime masterpiece illustration, volumetric light",
   ),
}
IMAGE_EDITING_TOOLS = {
   "REMOVE_BG_PNG": (
       "✂️ Hapus Background (File PNG Transparan Kualitas Tinggi)",



<!-- [ID:23_NVIDIA_SANDBOX_S014] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 428

           InlineKeyboardButton(
               text="🎥 Motion: Zoom Sinematik",
               callback_data="wiz:vpre:ZOOM_CINEMATIC",
           ),
           InlineKeyboardButton(
               text="🔄 Motion: Orbit 360°",
               callback_data="wiz:vpre:ORBIT_360",
           ),
       ],
       [
           InlineKeyboardButton(
               text="💃 Motion: Model/Dance",
               callback_data="wiz:vpre:DANCE_FASHION",
           ),
           InlineKeyboardButton(
               text="⚡ Motion: Slow-Mo Epik",
               callback_data="wiz:vpre:SLOWMO_EPIC",
           ),
       ],
       [
           InlineKeyboardButton(
               text=f"{'✅ ' if session.video_engine=='Kling 3.0 Pro' else ''}🟣 Kling 3.0 Pro",
               callback_data="wiz:veng:Kling 3.0 Pro",
           ),
           InlineKeyboardButton(
               text=f"{'✅ ' if session.video_engine=='Seedance 2.0' else ''}🕺 Seedance 2.0",
               callback_data="wiz:veng:Seedance 2.0",
           ),
       ],
       [
           InlineKeyboardButton(
               text=f"{'✅ ' if session.video_engine=='Wan 2.2 Pro' else ''}🔵 Wan 2.2 Pro",
               callback_data="wiz:veng:Wan 2.2 Pro",
           ),
           InlineKeyboardButton(
               text=f"{'✅ ' if session.video_engine=='Google Veo 3' else ''}🎥 Google Veo 3",
               callback_data="wiz:veng:Google Veo 3",
           ),
       ],
   ]
   if show_more:
       rows.extend(
           [
               [
                   InlineKeyboardButton(
                       text=f"{'✅ ' if session.video_engine=='Sora 2 Turbo' else ''}🌌 Sora 2 Turbo",
                       callback_data="wiz:veng:Sora 2 Turbo",
                   ),
                   InlineKeyboardButton(
                       text=f"{'✅ ' if session.video_engine=='Runway Gen-4' else ''}🎞️ Runway Gen-4",
                       callback_data="wiz:veng:Runway Gen-4",
                   ),
               ],
               [
                   InlineKeyboardButton(
                       text=f"{'✅ ' if session.video_engine=='Hailuo MiniMax H3' else ''}🎭 Hailuo MiniMax H
                       callback_data="wiz:veng:Hailuo MiniMax H3",
                   ),
                   InlineKeyboardButton(
                       text=f"{'✅ ' if session.video_engine=='LTX-2.3 Fast' else ''}🟢 LTX-2.3 Fast",
                       callback_data="wiz:veng:LTX-2.3 Fast",
                   ),
               ],
               [
                   InlineKeyboardButton(
                       text="🔼 Sembunyikan AI Video Lainnya",
                       callback_data="wiz:more_vid:0",
                   )
               ],
           ]
       )
   else:
       rows.append(
           [



<!-- [ID:23_NVIDIA_SANDBOX_S015] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 430

               text=f"{'✅ ' if session.aspect_ratio=='16:9' else ''}🖥️ 16:9",
               callback_data="wiz:ar:16:9",
           ),
       ],
       [
           InlineKeyboardButton(
               text="🛍️ Gaya: Katalog UMKM",
               callback_data="wiz:ipre:UMKM_CATALOG",
           ),
           InlineKeyboardButton(
               text="👔 Gaya: Foto Studio",
               callback_data="wiz:ipre:STUDIO_PORTRAIT",
           ),
       ],
       [
           InlineKeyboardButton(
               text="🎬 Gaya: Poster/Thumb",
               callback_data="wiz:ipre:POSTER_THUMB",
           ),
           InlineKeyboardButton(
               text="🎌 Gaya: Anime/3D Pixar",
               callback_data="wiz:ipre:ANIME_PIXAR",
           ),
       ],
       [
           InlineKeyboardButton(
               text=f"{'✅ ' if session.image_engine=='Seedream 4.5' else ''}✨ Seedream 4.5",
               callback_data="wiz:ieng:Seedream 4.5",
           ),
           InlineKeyboardButton(
               text=f"{'✅ ' if session.image_engine=='Flux.1 Dev' else ''}📸 Flux.1 Dev",
               callback_data="wiz:ieng:Flux.1 Dev",
           ),
       ],
       [
           InlineKeyboardButton(
               text=f"{'✅ ' if session.image_engine=='Midjourney v7' else ''}🎨 Midjourney v7",
               callback_data="wiz:ieng:Midjourney v7",
           ),
           InlineKeyboardButton(
               text=f"{'✅ ' if session.image_engine=='Ideogram v3' else ''}🔤 Ideogram v3 (Teks)",
               callback_data="wiz:ieng:Ideogram v3",
           ),
       ],
   ]
   if show_more:
       rows.extend(
           [
               [
                   InlineKeyboardButton(
                       text=f"{'✅ ' if session.image_engine=='Recraft V3' else ''}📐 Recraft V3 (Logo)",
                       callback_data="wiz:ieng:Recraft V3",
                   ),
                   InlineKeyboardButton(
                       text=f"{'✅ ' if session.image_engine=='Illustrious XL' else ''}🎌 Illustrious XL",
                       callback_data="wiz:ieng:Illustrious XL",
                   ),
               ],
               [
                   InlineKeyboardButton(
                       text=f"{'✅ ' if session.image_engine=='NoobAI-XL' else ''}🔥 NoobAI-XL",
                       callback_data="wiz:ieng:NoobAI-XL",
                   ),
                   InlineKeyboardButton(
                       text=f"{'✅ ' if session.image_engine=='Juggernaut XL' else ''}🌟 Juggernaut XL",
                       callback_data="wiz:ieng:Juggernaut XL",
                   ),
               ],
               [
                   InlineKeyboardButton(
                       text="🔼 Sembunyikan AI Gambar Lainnya",
                       callback_data="wiz:more_img:0",
                   )
               ],



<!-- [ID:23_NVIDIA_SANDBOX_S016] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 514

Nama Entitas / 
Penyedia 
Model Unggulan 
dalam Rolling Pool 
(2026) 
Kuota Gratis & 
Batas Rate Limit 
Peran Spesifik 
dalam Arsitektur 
bikinAI 
Prioritas Rolling 
Groq Cloud (LPU) llama-3.3-70b, 
qwen/qwen3.6-27b
, 
openai/gpt-oss-12
0b, 
whisper-large-v3 
30 RPM, 1.000 
RPD, 6K–8K TPM, 
200K–500K TPD 
per model (Tanpa 
Kartu) 
Penjawab utama 
obrolan instan 
(<0,8s TTFT) & 
transkripsi suara. 
Tier 1 (Primer 
Cepat t=0) 
Cerebras & 
SambaNova 
llama-3.3-70b, 
llama-4-maverick, 
deepseek-r1 
Cerebras: 1M 
token/hari gratis; 
SambaNova: 
Kredit $5 + 20 
RPM permanen 
Cadangan 
berkecepatan 
tinggi 
(Wafer-Scale / 
RDU) saat Groq 
mengalami 
rate-limit. 
Tier 1 (Primer 
Rotasi t=0) 
Google AI Studio gemini-3.8-flash, 
gemini-2.5-pro, 
gemini-2.5-flash-lit
e (Konteks 1M) 
250.000 TPM, 
5–15 RPM gratis 
tanpa kartu 
(Catatan: 2.0-flash 
ditutup Juni 2026) 
Analisis 
multimodal 
(pembacaan 
PDF/Foto asli), 
/riset, dan /canvas 
panjang. 
Tier 2 (Hedged 
t=1,2\text{s}) 
Mistral AI (La 
Plateforme) 
mistral-large, 
codestral, 
mistral-small-2603 
1 Miliar 
token/bulan gratis 
permanen (1 
req/detik, 500K 
TPM, verifikasi 
SMS) 
Pengerjaan kode 
di /canvas, Prompt 
Architect, dan 
cadangan volume 
raksasa. 
Tier 2 (Hedged 
t=1,2\text{s}) 
OpenRouter 
(:free Pool) 
nvidia/nemotron-3-
ultra:free (1M), 
deepseek/deepsee
k-chat:free, 
hermes-3 
~21 model :free 
aktif (butuh saldo 
akun \ge \$0, 
tanpa biaya per 
token) 
Penalaran agen 
kompleks, coding, 
dan jalur unfiltered 
Hermes 3. 
Tier 2 (Hedged 
t=1,2\text{s}) 
Cloudflare 
Workers AI 
@cf/black-forest-la
bs/flux-1-schnell, 
qwen2.5-coder, 
gemma-sea 
10.000 
Neurons/hari gratis 
(reset 00:00 UTC, 
50+ model teks & 
gambar) 
Render gambar 4K 
gratis di edge & 
inferensi bahasa 
Asia Tenggara 
(gemma-sea). 
Tier 2 (Media & 
Teks Edge) 
NVIDIA NIM & 
SiliconFlow 
100+ model NIM 
(llama, mistral, 
gemma); 
SiliconFlow 
(Qwen-Image, 
Hunyuan-MT) 
NVIDIA: 40 RPM 
gratis permanen; 
SiliconFlow: 15+ 
model ¥0 tanpa 
kartu 
Cadangan 
inferensi korporat 
stabil, translasi 
prompt visual, dan 
reranking. 
Tier 3 (Rolling 
Pool) 
AnyAPI & 
InclusionAI 
15+ model dasar 
OpenAI-compatibl
e; Ant Group 
AnyAPI: 100K 
token/hari; 
InclusionAI: 500K 
Penyangga kuota 
harian tambahan 
untuk obrolan 
Tier 3 (Rolling 
Pool) 



<!-- [ID:23_NVIDIA_SANDBOX_S017] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 525

Urutan Penambalan 
Target Komponen pada 
App.py 
Spesifikasi Teknis 
Implementasi 
Indikator Keberhasilan 
Audit (Zero-Defect) 
19_voucher 
wasmtime berbatas 
fuel, hapus "u": user_id 
dari voucher, dan 
potong koin Pro. 
identitas Telegram dari 
NocturneAI. 
Tata Kelola Operasional Otonom Bersama Komunitas 
Setelah keenam penambalan di atas diterapkan, keseluruhan ekosistem berjalan secara 
otonom sebagai mesin kecerdasan buatan yang tumbuh bersama komunitas dengan 
pengawasan harian minimal dari pemilik proyek. Eksekusi satu perintah /setup_grup di dalam 
Supergroup Telegram secara otomatis membangun dan mengikat keenam ruangan topik 
komunitas (⚡ Live Neural Feed, 📡 Command Center & Promo, 🧭 Blueprint & Koin 
Gratis, 🧠 Arsitek Prompt & Ide 24/7, 🎬 Galeri Kreator & Preset, serta 🛠️ Lab Inovasi & 
Bantuan) ke dalam database persisten bikinai_master_vault.db berdasarkan nomor 
message_thread_id, sehingga pengelola bebas mengubah nama tampilan topik kapan saja 
tanpa memutuskan ikatan fungsi bot. Kelima Sub-Bot operasional bekerja secara terpadu di 
bawah satu induk untuk melacak riwayat pergantian identitas anggota baru melalui SangMata 
Identity Tracker, menyapa kreator baru sambil menangkal tautan spam, menyiarkan setiap 
keberhasilan render ke topik Live Neural Feed guna memicu efek psikologis Fear of Missing 
Out (FOMO), serta mengembalikan koin pengguna secara otomatis dalam 60 detik apabila 
terjadi gangguan jaringan di klaster GPU (Auto-Refund Watchdog). 
Melalui ruangan 🛠️ Lab Inovasi & Bantuan serta perintah /saran, anggota komunitas secara 
aktif menjadi mata dan telinga tambahan yang melaporkan kemunculan API gratis baru, 
promosi domain, maupun keterampilan agen SKILL.md. Daemon Omni-Resource Harvester 
kemudian memanen informasi tersebut, menyaringnya melewati pipa karantina enam lapis 
berbasis WebAssembly hingga terbukti bersih dari malware, dan menyajikannya di dalam panel 
/bansos milik pemilik proyek. Pengelola cukup memantau kesehatan brankas dari ruang pesan 
pribadi (/admin), mengalihkan penyedia kasir lokal apabila batas transaksi bulanan satu 
gerbang QRIS hampir penuh, menyalakan saklar Mode Silent atau Mode Happy Hour pada 
sumber daya /bansos, dan memanen akumulasi keuntungan bersih kapan saja melalui perintah 
/harvest. 
Karya yang dikutip 
1. Free, Unlimited AI API - Puter.js, https://developer.puter.com/tutorials/free-unlimited-ai-api/ 2. 
Free, Unlimited Google AI API - Puter.js, 
https://developer.puter.com/tutorials/free-unlimited-google-ai-api/ 3. nanoMuse: an open-source 
personal agent for every ... - GitHub, https://github.com/nano-muse/nanoMuse 4. Conditional 
Safe Harbor, Sistem SAMAN, dan - Journal UIN Jakarta, 
https://journal.uinjkt.ac.id/index.php/adalah/article/download/51883/19289 5. telegram-miniapps 
· Skills - MCP Field, https://mcpfield.com/en/skills/telegram-miniapps 6. API Documentation — 
OrbChain Crypto Payment Gateway, https://orbchain.io/docs 7. Code Injection / Sandbox 
Escape in PraisonAI Python Agent, 
https://codeant.ai/vulnerability-database/cve-2026-40158/copy 8. Escaping Python Sandboxes - 
Moshe Kaplan's Blog, https://moshekaplan.com/posts/2012-10-26-escaping-python-sandboxes/ 
9. Python Sandbox: Every Approach, Honestly Ranked - OpenComputer, 



<!-- [ID:23_NVIDIA_SANDBOX_S018] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_138, SPAN_141 -->
## Halaman 542

Teknologi Isolasi 
Sandbox 
Tingkat & 
Mekanisme Isolasi 
Waktu Boot (Cold / 
Snapshot) 
Overhead Memori 
& Performa 
Rekomendasi 
Penggunaan 
dalam Ekosistem 
bikinAI 
sandbox memiliki 
kernel Linux 
independen dan 
hanya 
mengemulasi 6 
perangkat virtual 
(~100K baris kode 
vs ~2 juta pada 
QEMU). 
hingga 150 
VM/detik per host. 
Bare-Metal untuk 
menguji patch 
kode otonom dan 
menjalankan skrip 
komunitas yang 
belum tepercaya. 
Firecracker + 
ZeroBoot / E2B 
Snapshot 
Isolasi perangkat 
keras KVM 
dengan teknik 
Copy-on-Write 
(CoW) KVM fork 
dari snapshot 
memori yang telah 
dipanaskan 
(pre-warmed). 
0,79\text{ ms} - 
150\text{ ms} 
Membutuhkan 
alokasi pool 
memori dasar, 
namun 
mengeliminasi 
waktu boot kernel 
dari nol. 
Skala Enterprise / 
Concurrency 
Tinggi untuk 
mengeksekusi 
kode Interactive 
Canvas (/canvas) 
milik ribuan 
pengguna secara 
bersamaan. 
Protokol Verifikasi Lima Gerbang di Dalam Sandbox (The 5-Gate 
Sandbox Verification) 
Setiap kali Remediation Agent menghasilkan kandidat perbaikan kode (app_candidate.py), 
sistem menyalakan instansiasi Firecracker MicroVM yang memiliki kernel Linux terpisah dan 
hanya mengemulasi enam perangkat virtual minimalis (virtio-net, virtio-blk, virtio-balloon, 
virtio-vsock, serial port, dan keyboard controller) dalam waktu kurang dari 125 milidetik. Di 
dalam lingkungan yang terputus dari jaringan publik 
(defaul[span_138](start_span)[span_138](end_span)[span_141](start_span)[span_141](end_sp
an)t-deny network) ini, kandidat kode wajib melintasi lima gerbang verifikasi sekuensial sebelum 
diizinkan menyentuh lalu lintas produksi. 
Gerbang pertama (AST & CST Structural Integrity) mengompilasi kandidat kode menjadi 
bytecode Python dan menjalankan pemeriksaan ruff serta tree-sitter guna memastikan 
ketiadaan kesalahan sintaksis. Gerbang kedua (Vault & Privilege Guard) mengaudit perubahan 
pada tingkat pohon sintaks untuk memastikan kode baru sama sekali tidak memodifikasi logika 
penguncian OWNER_ID pada /klaim_owner, tidak mengakses kunci rahasia di luar lingkupnya, 
dan tidak mengubah skema penyimpanan ~/.bikinai_vault/. Selanjutnya, gerbang ketiga 
(Synthetic Anomaly Replay) memutar ulang secara persis payload telemetri yang memicu 
insiden awal—seperti mengumpankan kembali dokumen PDF yang membuat bot diam—ke 
dalam instansiasi sandbox dan memverifikasi bahwa sistem merespons secara akurat di bawah 
batas waktu layanan. 
Setelah lulus uji fungsional spesifik, gerbang keempat (Core Directive Regression Suite) 
menjalankan pengujian otomatis menyeluruh menggunakan bantuan tiruan jaringan asinkron 
(aioresponses dan aiounittest) untuk menjamin tidak terjadinya kemunduran fungsi (regression) 
pada ke-14 pilar Master Blueprint v3.2.0. Pengujian ini memverifikasi bahwa pembungkusan 



<!-- [ID:23_NVIDIA_SANDBOX_S019] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 683

Gelombang Prioritas 
Nama Layanan & 
Tautan Resmi 
Fungsi Utama dalam 
Sistem Kita 
Biaya 
9Router): 
[https://profile.aws.ama
zon.com/](https://profile
.aws.amazon.com/) 10. 
NVIDIA NIM (Kredit 
LLM Gratis): 
[https://build.nvidia.com
/](https://build.nvidia.co
m/) 
🔵 GELOMBANG 2 
(Daftar Saat Siap Buka 
Kasir QRIS & Mesin 
Komersial 
Pay-Per-Use) 
11. Pakasir (Gateway 
QRIS Kreator): 
[https://pakasir.com/](ht
tps://pakasir.com/) 12. 
Tripay / Duitku 
(Alternatif QRIS): 
[https://tripay.co.id/](htt
ps://tripay.co.id/) / 
[https://www.duitku.com
/](https://www.duitku.co
m/) 13. Fal.ai (API 
Kling, Veo, Wan, 
Flux): 
[https://fal.ai/dashboard
/keys](https://fal.ai/dash
board/keys) 14. Novita 
AI (API Unfiltered 
Murah): 
[https://novita.ai/](https:
//novita.ai/) 15. 
Replicate (Upscale 4K 
& Motion): 
[https://replicate.com/ac
count/api-tokens](https:
//replicate.com/account/
api-tokens) 16. PiAPI 
(API Musik Suno & 
Udio): 
[https://piapi.ai/](https://
piapi.ai/) 17. 
WaveSpeed AI 
(Render Cepat 
Wan/LTX): 
[https://wavespeed.ai/](
https://wavespeed.ai/) 
Menghidupkan kasir 
QRIS otomatis dan 
membuka seluruh 
mesin komersial Tier 
Pro & Tier Ultra pada 
saklar 
PILIHAN_MESIN_MED
IA = 2 tanpa risiko 
sewa GPU per jam. 
Deposit sesuai 
pemakaian pembeli 
🟣 GELOMBANG 3 
18. Vast.ai (Sewa GPU Mengalihkan saklar ke Sesuai skala ekspansi 



<!-- [ID:23_NVIDIA_SANDBOX_S020] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Aturan keras (dijaga `sandbox.py`)
1. Hanya HTTP GET. POST/PUT/PATCH/DELETE ditolak.
2. Host wajib ada di allowlist per scanner.
3. Env kredensial (`PRIVATE_KEY`, `OPENAI_API_KEY`, dll) TIDAK BOLEH terbaca.
4. Rate limit: airdrop 10/min, bansos 5/min, program 5/min, nvidia 5/min.
5. Output → `IntelReport` + hash → audit. Bukan eksekusi.
6. Wallet signing / claim airdrop / auto-apply TIDAK ADA di service ini.
   Kalau butuh → gate CHAIN lewat payment/on-chain service, dan hanya owner.


<!-- [ID:23_NVIDIA_SANDBOX_S021] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# Opsional:
NVIDIA_SPECTRUM_API_KEY=

<!-- [ID:23_NVIDIA_SANDBOX_S022] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# === 2. ENAM SUMBER AI GRATIS (HPP Rp 0 - ISI MINIMAL 1 ATAU 2) ===
GEMINI_API_KEY=""
GROQ_API_KEY=""
OPENROUTER_API_KEY=""
CEREBRAS_API_KEY=""
POLLINATIONS_API_KEY=""
CLOUDFLARE_ACCOUNT_ID=""
CLOUDFLARE_API_TOKEN=""


<!-- [ID:23_NVIDIA_SANDBOX_S023] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# - Multi-TLD Domain RDAP Scanner & SkillSpector AST Sterilizer (Zero-Typo!)

<!-- [ID:23_NVIDIA_SANDBOX_S024] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 3. OMNI-RESOURCE HARVESTER & SKILLSPECTOR STERILIZER (FIXED ZERO-TYPO!)
