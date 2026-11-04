
<!-- [ID:06_AGGREGATOR_S001] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 136

  overflow-x: hidden;​
}​
​
/* Custom Scrollbar */​
::-webkit-scrollbar {​
  width: 6px;​
  height: 6px;​
}​
::-webkit-scrollbar-track {​
  background: #030712;​
}​
::-webkit-scrollbar-thumb {​
  background: #1f2937;​
  border-radius: 9999px;​
}​
::-webkit-scrollbar-thumb:hover {​
  background: #374151;​
}​
 
app/layout.tsx 
Tata letak dasar dokumen Next.js: 
import type { Metadata } from "next";​
import "./globals.css";​
​
export const metadata: Metadata = {​
  title: "AETHEROS v3.0 | Autonomous Multi-Path AI Supercluster",​
  description: "Frontier Level AI Aggregator with 95% Margin Guard, Self-Evolving Open-Source 
Radar, and Zero-Cost Engine.",​
};​
​
export default function RootLayout({​
  children,​
}: {​
  children: React.ReactNode;​
}) {​
  return (​
    <html lang="id" className="dark">​
      <body className="min-h-screen bg-[#030712] text-slate-100 antialiased">​
        {children}​
      </body>​
    </html>​
  );​
}​
 



<!-- [ID:06_AGGREGATOR_S002] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 150

            <li className="flex items-center gap-2">✓ Kasir Telegram @CryptoBot Tanpa KYC 
Perbankan</li>​
            <li className="flex items-center gap-2">✓ Auto-Topup Grosir GPU: Novita AI, RunPod, 
Vast.ai</li>​
            <li className="flex items-center gap-2">✓ Dukungan Jaringan TRON, Solana, dan 
Base</li>​
          </ul>​
​
          <a​
            href="https://t.me/CryptoBot"​
            target="_blank"​
            rel="noreferrer"​
            className="flex items-center justify-center gap-2 w-full rounded-xl bg-gradient-to-r 
from-indigo-400 via-purple-500 to-pink-500 py-3 text-xs font-bold text-white shadow-lg 
shadow-indigo-500/25 hover:brightness-110"​
          >​
            <ArrowUpRight className="h-4 w-4" /> Bayar via @CryptoBot (USDT)​
          </a>​
        </div>​
      </div>​
    </div>​
  );​
}​
 
components/SelfEvolvingRadar.tsx 
Dashboard yang memantau repositori MIT/Apache-2.0, verifikasi keamanan ModelScan, dan 
status sintesis berkas keterampilan mandiri SKILL.md: 
"use client";​
​
import React from "react";​
import { Terminal, GitPullRequest, ShieldCheck, CheckCircle2, FileCode, RefreshCw } from 
"lucide-react";​
​
export default function SelfEvolvingRadar() {​
  const discoveredTools = [​
    { name: "thu-ml/SageAttention", license: "Apache-2.0", stars: "4.8k", benchmark: "+54% GPU 
Inference", status: "PROMOTED", skillFile: "sage_attention_SKILL.md" },​
    { name: "ali-vilab/TeaCache", license: "Apache-2.0", stars: "3.2k", benchmark: "2.8x Video 
Acceleration", status: "PROMOTED", skillFile: "teacache_diffusers_SKILL.md" },​
    { name: "D4Vinci/Scrapling", license: "BSD / MIT", stars: "6.9k", benchmark: "Cloudflare 
Turnstile Bypass", status: "PROMOTED", skillFile: "scrapling_crawler_SKILL.md" },​
    { name: "hexgrad/Kokoro-82M", license: "Apache-2.0", stars: "14.2k", benchmark: "Rp 1/Voice 
Script on CPU", status: "PROMOTED", skillFile: "kokoro_voice_SKILL.md" },​
    { name: "spider-rs/spider", license: "MIT", stars: "8.1k", benchmark: "Low-Latency Rust 
Scraper", status: "E2B SANDBOX TEST", skillFile: "spider_stream_SKILL.md" },​
  ];​



<!-- [ID:06_AGGREGATOR_S003] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 30

Omnichannel, Panel Server Mandiri & Direktori Free-Tier 
1.​ Stasiun Kerja Agen Otonom & Self-Evolving Harnesses — URL Polos OpenClaw 
(~385.000 Bintang & 5.380 Skills): https://github.com/openclaw/openclaw | URL Polos 
Nous Hermes Agent (~223.000 Bintang dengan Siklus Belajar Tertutup): 
https://github.com/NousResearch/hermes-agent | URL Polos Skrip Instalasi Langsung 
Hermes Agent: https://hermes-agent.nousresearch.com/install.sh | URL Polos HKUDS 
Nanobot: https://github.com/HKUDS/nanobot | URL Polos Hugging Face Smolagents 
(~1.000 Baris Python): https://github.com/huggingface/smolagents | URL Polos Aider: 
https://github.com/Aider-AI/aider | URL Polos OpenHands CLI Harness: 
https://github.com/All-Hands-AI/OpenHands | URL Polos Pi Terminal Coding Agent 
(~81.000 Bintang oleh Earendil): https://github.com/earendil-works/pi | URL Polos Portal 
Web Pi Coding Agent (npm install -g @earendil-works/pi-coding-agent): https://pi.dev | 
URL Polos OpenCode (Agen Koding Terminal TUI ~191.000 Bintang): 
https://github.com/anomalyco/opencode | URL Polos Buzz (Ruang Kerja Kolaborasi 
Manusia & Agen Berbasis Nostr/Rust): https://buzz.xyz | URL Polos Akash SDL Skill 
untuk Agen Koding: https://github.com/akash-network/akash-skill — Kegunaan & Aturan 
Terbaru: Stasiun kerja agen yang dapat langsung diarahkan ke server lokal 
(http://127.0.0.1:8080/v1) maupun router OmniRoute (http://localhost:20128/v1) dan 
9Router untuk mengeksekusi pemrograman, kontrol peramban, dan manajemen server 
tanpa henti. 
2.​ Pustaka Orkestrasi Agen Modular & Tata Kelola Runtime (Zero-Trust Governance) 
— URL Polos PydanticAI: https://github.com/pydantic/pydantic-ai | URL Polos Instructor: 
https://github.com/jxnl/instructor | URL Polos LangGraph: 
https://github.com/langchain-ai/langgraph | URL Polos Rig (Rust): 
https://github.com/0xPlaygrounds/rig | URL Polos Mastra (TypeScript): 
https://github.com/mastra-ai/mastra | URL Polos VoltAgent (TypeScript): 
https://github.com/voltagent/voltagent | URL Polos Microsoft Agent Governance Toolkit 
(OWASP Agentic Top 10): https://github.com/microsoft/agent-governance-toolkit — 
Kegunaan & Aturan Terbaru: Menjamin keluaran agen selalu patuh pada skema tipe data 
serta mengisolasi eksekusi kode agen dengan hak akses minimum (least-privilege). 
3.​ Mesin Perayap Web (Web Crawler) & Anti-Bot Adaptive Scrapers — URL Polos 
Crawl4AI: https://github.com/unclecode/crawl4ai | URL Polos Scrapling (Python Adaptive 
Scraper & Cloudflare Turnstile Bypass): https://github.com/D4Vinci/Scrapling | URL Polos 
Dokumentasi Resmi Scrapling: https://scrapling.readthedocs.io/en/latest/index.html | URL 
Polos Scrapling-RS (Port Rust Native dengan 135+ Profil TLS JA3/JA4): 
https://github.com/chrisabruce/scrapling-rs | URL Polos Spider-RS (Perayap Web 
Streaming Tercepat Berbasis Rust): https://github.com/spider-rs/spider | URL Polos 
Organisasi GitHub Spider-RS: https://github.com/spider-rs | URL Polos Portal 
Open-Source Spider Cloud: https://spider.cloud/open-source/ | URL Polos Spider Python 
Client: https://github.com/spider-rs/spider-py | URL Polos Spider Node.js Client: 
https://github.com/spider-rs/spider-nodejs | URL Polos Spider Multi-Language Clients: 
https://github.com/spider-rs/spider-clients | URL Polos Spider Cloud MCP Server v2: 
https://github.com/spider-rs/spider-cloud-mcp-v2 | URL Polos Spider Cloud MCP Server: 
https://github.com/spider-rs/spider-cloud-mcp-server | URL Polos Spider Headless 
Browser: https://github.com/spider-rs/headless-browser | URL Polos Spider Chromey 
(CDP Rust): https://github.com/spider-rs/chromey | URL Polos Spider HTML2MD: 



<!-- [ID:06_AGGREGATOR_S004] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 31

https://github.com/spider-rs/html2md | URL Polos Spider User-Agent Generator: 
https://github.com/spider-rs/ua_generator | URL Polos Spider Cloud Live Code Viewer: 
https://github.com/spider-rs/spider-cloud-live-code-viewer | URL Polos Spider Example 
Knowledge Base: https://github.com/spider-rs/spider-example-knowledge-base | URL 
Polos Scrapy Framework: https://github.com/scrapy/scrapy | URL Polos SeleniumBase: 
https://github.com/seleniumbase/SeleniumBase | URL Polos Botasaurus: 
https://github.com/omkarcloud/botasaurus | URL Polos Scrapfly Scrapers Reference: 
https://github.com/scrapfly/scrapfly-scrapers — Kegunaan & Aturan Terbaru: Rantai 
ekstraksi web 3-tingkat yang menggabungkan kecepatan HTTP-first spider-rs/spider, 
pelacakan elemen adaptif 12-faktor dan pembobol Cloudflare Turnstile otomatis pada 
Scrapling / scrapling-rs, serta layanan internal Crawl4AI (wajib dijalankan di jaringan lokal 
terisolasi tanpa ekspos publik untuk mencegah celah SSRF GHSA-wm69-2pc3-rmmf). 
4.​ Gateway Omnichannel Mandiri & Template Antarmuka Web — URL Polos WAHA — 
WhatsApp HTTP API: https://github.com/devlikeapro/waha | URL Polos Aceternity UI: 
https://ui.aceternity.com/ | URL Polos Magic UI: https://magicui.design/ — Kegunaan & 
Aturan Terbaru: Menghubungkan agen ke WhatsApp secara mandiri melalui kontainer 
Docker tanpa biaya langganan bulanan SaaS pihak ketiga serta merakit antarmuka web 
modern. 
5.​ Panel Manajemen Server VPS, Self-Hosted PaaS & AI Gateway Panels (Tambahan 
Baru 100% Gratis) — URL Polos 1Panel (Repositori Utama Panel Server Linux & AI 
Management Platform ~37.300 Bintang): https://github.com/1Panel-dev/1Panel | URL 
Polos Website Resmi 1Panel: https://1panel.pro | URL Polos Organisasi GitHub 
1Panel-dev: https://github.com/1Panel-dev | URL Polos 1Panel-Gateway (AI Gateway 
Terintegrasi untuk Rute & Audit): https://github.com/1Panel-dev/1Panel-Gateway | URL 
Polos MaxKB (Platform Agen Enterprise Open-Source dari 1Panel): 
https://github.com/1Panel-dev/MaxKB | URL Polos CordysCRM (Sistem AI CRM 
Open-Source Terintegrasi OpenClaw): https://github.com/1Panel-dev/CordysCRM | URL 
Polos Coolify (Self-Hosted PaaS Pengganti Vercel/Heroku ~63.000 Bintang, Rilis v4.4.6 
Okt 2026): https://github.com/coollabsio/coolify | URL Polos Website Resmi Coolify: 
https://coolify.io/ | URL Polos Dokploy (Self-Hosted PaaS Ringan Berbasis Docker Swarm 
& Traefik ~38.000 Bintang, Rilis v0.30.8 Sep 2026): https://github.com/Dokploy/dokploy | 
URL Polos Website Resmi Dokploy: https://dokploy.com/ | URL Polos CapRover 
(Self-Hosted PaaS Stabil Berbasis Nginx & Docker Swarm, Rilis v1.15.4 Agu 2026, Jalan 
di 1 GB RAM): https://caprover.com/ | URL Polos Temps (Self-Hosted PaaS dengan 
Observabilitas, Error Tracking & Analytics Bawaan): https://temps.sh/ | URL Polos Dokku 
(PaaS Berbasis Git Push Ringan via CLI): https://dokku.com/ | URL Polos aaPanel (Panel 
Kontrol Hosting Gratis dengan 400+ App 1-Klik, Idle <100 MB RAM): 
https://www.aapanel.com/ | URL Polos Direktori Perbandingan Panel Kontrol Web 
Hosting: https://github.com/mic7811/web-hosting-control-panels | URL Polos Indeks Topik 
Control Panel GitHub: https://github.com/topics/control-panel — Kegunaan & Aturan 
Terbaru: Panel web gratis berlisensi open-source (Apache-2.0 / GPL-3.0) untuk 
mengelola VPS (seperti Oracle Cloud Always Free atau VPS lokal), men-deploy kontainer 
Docker Compose, mengatur SSL Let's Encrypt otomatis, mencadangkan database ke 
S3/R2/Backblaze, serta mengelola model Ollama dan agen OpenClaw secara visual dari 
browser (khususnya pada 1Panel dan Coolify). 
6.​ Direktori Riset, Kurasi Agen & Katalog Pelacak Layanan Free-Tier (Automated 
Discovery Registries) — URL Polos Live Free LLM API Tracker (cheahjs - Induk): 
https://github.com/cheahjs/free-llm-api-resources | URL Polos Mirror SourceForge Free 



<!-- [ID:06_AGGREGATOR_S005] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 171

No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis 
& Peran dalam 
Rantai Failover 
notebooks/blob/ma
in/ABLITERATION
.md 
1D.6 
Perisai 
Keamanan Bobot 
Model, Guardrails 
& Audit Celah 
Protect AI 
ModelScan: 
https://github.com/
protectai/modelsca
n HF Malware 
Docs: 
https://huggingface
.co/docs/hub/other 
Crawl4AI SSRF 
Advisory: 
https://github.com/
advisories/GHSA-
wm69-2pc3-rmmf 
NVIDIA NeMo 
Guardrails & 
Llama Prompt 
Guard 2 (86M) 
(Sumber 3): 
https://github.com/
NVIDIA/NeMo-Gu
ardrails 
Spider Firewall 
Utilities (Rust): 
https://github.com/
spider-rs/firewall 
modelscan 
memindai berkas 
Pickle, H5, dan 
SavedModel 
secara statis 
sebelum 
pemuatan untuk 
mencegah 
pencurian 
kredensial 
AWS/API, 
sedangkan 
NeMo-Guardrails 
dan Llama Prompt 
Guard 2 memfilter 
serangan prompt 
injection masuk. 
1E. Kerangka Kerja Agen Otonom, Crawler Adaptif, Gateway Omnichannel & 
Direktori Riset (Tanpa Pendaftaran) 
Pada lapisan akuisisi data web dan agen otonom, sumber induk mencantumkan 
unclecode/crawl4ai namun sekaligus memperingatkan adanya kerentanan keamanan tingkat 
tinggi GHSA-wm69-2pc3-rmmf (Unauthenticated Server-Side Request Forgery / SSRF pada 
jalur /crawl/stream di server Docker). Untuk memastikan agen memiliki jalur rolling yang bebas 
dari celah SSRF tersebut sekaligus mampu menembus proteksi Cloudflare Turnstile dan 
perubahan struktur HTML dinamis, riset menambahkan dua mesin perayap generasi baru yang 
jauh lebih tangguh: D4Vinci/Scrapling (beserta port Rust-nya chrisabruce/scrapling-rs) dan 
ekosistem perayap konkurensi tinggi berbasis Rust spider-rs/spider. Scrapling dan scrapling-rs 
menyimpan sidik jari struktural elemen di SQLite dan menghitung skor kemiripan 12-faktor untuk 
merelokasi elemen secara otomatis ketika situs web mengubah nama kelas CSS atau 
membungkus ulang struktur DOM, lengkap dengan emulasi 135+ profil sidik jari TLS 
(JA3/JA4/HTTP2) dan pemecah Cloudflare Turnstile bawaan. Di sisi lain, spider-rs/spider 
menerapkan arsitektur HTTP-first yang mengalirkan halaman secara real-time dan hanya 
meluncurkan peramban Chrome tanpa kepala (headless) melalui crawl_smart() ketika suatu 
halaman terbukti membutuhkan eksekusi JavaScript. 



<!-- [ID:06_AGGREGATOR_S006] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 173

No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Keunggulan 
Arsitektural & 
Peran Failover 
Microsoft Agent 
Governance 
Toolkit: 
https://github.com/
microsoft/agent-go
vernance-toolkit 
1E.3 
Mesin Perayap 
Web (Web 
Crawler) & 
Anti-Bot Adaptive 
Scrapers 
Crawl4AI (Utama 
di Sumber 1): 
https://github.com/
unclecode/crawl4a
i 
Scrapling 
(Python Adaptive 
Scraper & 
Turnstile 
Bypass): 
https://github.com/
D4Vinci/Scrapling 
(Docs: 
https://scrapling.re
adthedocs.io/en/lat
est/index.html, 
Docker: 
ghcr.io/d4vinci/scr
apling:latest) 
Scrapling-RS 
(Port Rust Native, 
135+ TLS 
Profiles): 
https://github.com/
chrisabruce/scrapli
ng-rs Spider-RS 
(Fastest Rust 
Crawler): 
https://github.com/
spider-rs/spider & 
Org: 
https://github.com/
spider-rs & Portal: 
https://spider.cloud
/open-source/ 
Spider 
Python/Node/Multi 
Clients: 
https://github.com/
spider-rs/spider-py
, 
https://github.com/
Mengatasi 
kelemahan SSRF 
pada Docker 
Crawl4AI dan 
kerapuhan 
selector CSS 
tradisional. 
Scrapling dan 
scrapling-rs 
menyimpan sidik 
jari struktural 
elemen di SQLite 
dan menggunakan 
algoritma 
kemiripan 
12-faktor untuk 
menemukan 
kembali elemen 
meski situs 
mengubah tata 
letak HTML, 
dilengkapi 
pemecah 
Cloudflare 
Turnstile otomatis, 
penyamaran sidik 
jari TLS JA3/JA4 
(wreq), DoH 
anti-bocor DNS, 
dan server MCP 
bawaan. 
spider-rs/spider 
menjalankan 
strategi HTTP-first 
dan hanya 
membuka Chrome 
tanpa kepala 



<!-- [ID:06_AGGREGATOR_S007] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 174

No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Keunggulan 
Arsitektural & 
Peran Failover 
spider-rs/spider-no
dejs, 
https://github.com/
spider-rs/spider-cli
ents Spider MCP 
Servers: 
https://github.com/
spider-rs/spider-cl
oud-mcp-v2 & 
https://github.com/
spider-rs/spider-cl
oud-mcp-server 
Spider 
Browser/CDP/HT
ML2MD/UA: 
https://github.com/
spider-rs/headless
-browser, 
https://github.com/
spider-rs/chromey, 
https://github.com/
spider-rs/html2md, 
https://github.com/
spider-rs/ua_gener
ator Spider 
Reference Apps: 
https://github.com/
spider-rs/spider-cl
oud-live-code-view
er & 
https://github.com/
spider-rs/spider-ex
ample-knowledge-
base Alternatif 
Tambahan: 
https://github.com/
scrapy/scrapy, 
https://github.com/
seleniumbase/Sele
niumBase, 
https://github.com/
omkarcloud/botasa
urus, 
(headless) melalui 
crawl_smart() 
ketika halaman 
membutuhkan 
JavaScript. 



<!-- [ID:06_AGGREGATOR_S008] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 175

No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Keunggulan 
Arsitektural & 
Peran Failover 
https://github.com/
scrapfly/scrapfly-s
crapers 
1E.4 
Gateway 
Omnichannel 
Mandiri & 
Template 
Antarmuka Web 
WAHA — 
WhatsApp HTTP 
API (Sumber 3): 
https://github.com/
devlikeapro/waha 
Aceternity UI 
(Sumber 3): 
https://ui.aceternity
.com/ Magic UI 
(Sumber 3): 
https://magicui.des
ign/ 
Digunakan 
bersama Hermes 
Agent dan 
Nanobot untuk 
menghubungkan 
agen secara gratis 
ke WhatsApp, 
Telegram, Discord, 
Slack, Signal, dan 
Matrix, serta 
merakit antarmuka 
web bergaya 
Futuristic Luxury. 
Menghilangkan 
biaya langganan 
bulanan SaaS 
gateway pesan 
pihak ketiga 
melalui kontainer 
Docker mandiri. 
1E.5 
Direktori Riset, 
Kurasi Agen & 
Katalog Layanan 
Free-Tier 
Awesome Model 
Routing: 
https://github.com/
yenanjing/awesom
e-model-routing 
Awesome LLM 
Routing: 
https://github.com/
dstripelis/Awesom
e-LLM-Routing 
Awesome AI 
Agents (Aloth): 
https://github.com/
aloth/awesome-ai-
agents Awesome 
Agentic AI 
(Mfornos): 
https://github.com/
mfornos/awesome
-agentic-ai 
Awesome Agentic 
AI (Adriannoes): 
https://github.com/
adriannoes/aweso
me-agentic-ai 
Awesome AI 
Agents 
Topik Web 
Scraping Python: 
https://github.com/t
opics/web-scrapin
g-python Topik 
Spider Cloud: 
https://github.com/t
opics/spider-cloud 
Direktori Evaluasi 
API Agentik: 
https://apis.io/provi
ders/spider-cloud/ 
Berfungsi sebagai 
sumber penemuan 
otomatis 
(automated 
discovery 
registries) yang 
dapat dipindai 
secara berkala 
oleh agen perayap 
untuk menemukan 
layanan free-tier 
baru ketika 
penyedia lama 
mengubah 
ketentuan layanan. 



<!-- [ID:06_AGGREGATOR_S009] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# --- 6. LAYER 5: MULTIMODAL, WEB SCRAPING & WHOLESALE FALLBACKS ---​
SPIDER_CLOUD_API_KEY=""​
CRAWL4AI_INTERNAL_URL="http://127.0.0.1:11235"​
CIVITAI_API_KEY=""​
FAL_KEY=""​
NOVITA_API_KEY=""​
WAVESPEED_API_KEY=""​
REPLICATE_API_TOKEN=""​
PIAPI_KEY=""​
​

<!-- [ID:06_AGGREGATOR_S010] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 205

Zaeem20/FREE_PROXIES_LIST — GitHub trending stats & insights, 
https://trendshift.io/repositories/118339 12. Auto-Proxy-Fetcher/fetch_proxies.py at main - 
GitHub, https://github.com/VolkanSah/Auto-Proxy-Fetcher/blob/main/fetch_proxies.py 13. 
GitHub - WangYihang/Proxy-Verifier: A set of tools designed to, 
https://github.com/WangYihang/Proxy-Verifier 14. What Is huihui-ai (huihui AI)? Abliterated 
Models Guide, https://deepentresearch.com/en/journal/huihui-ai 15. Overview · 
cooper1637/SageAttention · GitHub, https://github.com/cooper1637/SageAttention/security 16. 
ali-vilab/TeaCache: Timestep Embedding Tells: It's Time to Cache, 
https://github.com/ali-vilab/TeaCache 17. InstantID: Zero-shot Identity-Preserving Generation in 
Seconds, https://github.com/instantx-research/instantid 18. rhasspy/piper: A fast, local neural 
text to speech system - GitHub, https://github.com/rhasspy/piper 19. Issue #2762 · 
k2-fsa/sherpa-onnx - tts模型推荐 - GitHub, https://github.com/k2-fsa/sherpa-onnx/issues/2762 
20. Releases · rhasspy/piper - GitHub, https://github.com/rhasspy/piper/releases 21. GitHub - 
Portkey-AI/gateway, https://github.com/portkey-ai/gateway 22. D4Vinci/Scrapling: 🕷️ A Web 
Scraping framework that ... - GitHub, https://github.com/d4vinci/Scrapling 23. GitHub - 
chrisabruce/scrapling-rs: Adaptive web scraping, built in, 
https://github.com/chrisabruce/scrapling-rs 24. Scrapling: Adaptive Python web scraping library 
that handles, https://www.scrapingbee.com/blog/scrapling-adaptive-python-web-scraping/ 25. 
Scrapling: Python Web Scraping Framework, 
https://scrapling.readthedocs.io/en/latest/index.html 26. Spider: a streaming Rust crawler that 
starts with HTTP - Hysen Labs, https://hysenlabs.com/projects/spider-rs-spider 27. 
ComfyUI-TeaCache - ComfyICU, https://comfy.icu/extension/welltop-cn__ComfyUI-TeaCache 
28. TeaCache/TeaCache4Wan2.1/README.md at main · ali ... - GitHub, 
https://github.com/ali-vilab/TeaCache/blob/main/TeaCache4Wan2.1/README.md 29. Akash 
Network - GitHub, https://github.com/akash-network 30. GitHub - akash-network/node: Source 
code for Akash node, a, https://github.com/akash-network/node 31. Node Architecture - Your 
Guide to Decentralized Cloud, https://akash.network/docs/node-operators/architecture/ 32. 
Releases · akash-network/node - GitHub, https://github.com/ovrclk/akash/releases 33. 
huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated - Hugging Face, 
https://huggingface.co/huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated 



<!-- [ID:06_AGGREGATOR_S011] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 258

No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis 
& Peran dalam 
Rantai Failover 
notebooks/blob/ma
in/ABLITERATION
.md 
1D.6 
Perisai 
Keamanan Bobot 
Model, Guardrails 
& Audit Celah 
Protect AI 
ModelScan: 
https://github.com/
protectai/modelsca
n HF Malware 
Docs: 
https://huggingface
.co/docs/hub/other 
Crawl4AI SSRF 
Advisory: 
https://github.com/
advisories/GHSA-
wm69-2pc3-rmmf 
NVIDIA NeMo 
Guardrails & 
Llama Prompt 
Guard 2 (86M) 
(Sumber 3): 
https://github.com/
NVIDIA/NeMo-Gu
ardrails 
Spider Firewall 
Utilities (Rust): 
https://github.com/
spider-rs/firewall 
modelscan 
memindai berkas 
Pickle, H5, dan 
SavedModel 
secara statis 
sebelum 
pemuatan untuk 
mencegah 
pencurian 
kredensial 
AWS/API, 
sedangkan 
NeMo-Guardrails 
dan Llama Prompt 
Guard 2 memfilter 
serangan prompt 
injection masuk. 
1E. Kerangka Kerja Agen Otonom, Crawler Adaptif, Gateway Omnichannel & 
Direktori Riset (Tanpa Pendaftaran) 
Pada lapisan akuisisi data web dan agen otonom, sumber induk mencantumkan 
unclecode/crawl4ai namun sekaligus memperingatkan adanya kerentanan keamanan tingkat 
tinggi GHSA-wm69-2pc3-rmmf (Unauthenticated Server-Side Request Forgery / SSRF pada 
jalur /crawl/stream di server Docker). Untuk memastikan agen memiliki jalur rolling yang bebas 
dari celah SSRF tersebut sekaligus mampu menembus proteksi Cloudflare Turnstile dan 
perubahan struktur HTML dinamis, riset menambahkan dua mesin perayap generasi baru yang 
jauh lebih tangguh: D4Vinci/Scrapling (beserta port Rust-nya chrisabruce/scrapling-rs) dan 
ekosistem perayap konkurensi tinggi berbasis Rust spider-rs/spider. Scrapling dan scrapling-rs 
menyimpan sidik jari struktural elemen di SQLite dan menghitung skor kemiripan 12-faktor untuk 
merelokasi elemen secara otomatis ketika situs web mengubah nama kelas CSS atau 
membungkus ulang struktur DOM, lengkap dengan emulasi 135+ profil sidik jari TLS 
(JA3/JA4/HTTP2) dan pemecah Cloudflare Turnstile bawaan. Di sisi lain, spider-rs/spider 
menerapkan arsitektur HTTP-first yang mengalirkan halaman secara real-time dan hanya 
meluncurkan peramban Chrome tanpa kepala (headless) melalui crawl_smart() ketika suatu 
halaman terbukti membutuhkan eksekusi JavaScript. 



<!-- [ID:06_AGGREGATOR_S012] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 260

No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Keunggulan 
Arsitektural & 
Peran Failover 
Microsoft Agent 
Governance 
Toolkit: 
https://github.com/
microsoft/agent-go
vernance-toolkit 
1E.3 
Mesin Perayap 
Web (Web 
Crawler) & 
Anti-Bot Adaptive 
Scrapers 
Crawl4AI (Utama 
di Sumber 1): 
https://github.com/
unclecode/crawl4a
i 
Scrapling 
(Python Adaptive 
Scraper & 
Turnstile 
Bypass): 
https://github.com/
D4Vinci/Scrapling 
(Docs: 
https://scrapling.re
adthedocs.io/en/lat
est/index.html, 
Docker: 
ghcr.io/d4vinci/scr
apling:latest) 
Scrapling-RS 
(Port Rust Native, 
135+ TLS 
Profiles): 
https://github.com/
chrisabruce/scrapli
ng-rs Spider-RS 
(Fastest Rust 
Crawler): 
https://github.com/
spider-rs/spider & 
Org: 
https://github.com/
spider-rs & Portal: 
https://spider.cloud
/open-source/ 
Spider 
Python/Node/Multi 
Clients: 
https://github.com/
spider-rs/spider-py
, 
https://github.com/
Mengatasi 
kelemahan SSRF 
pada Docker 
Crawl4AI dan 
kerapuhan 
selector CSS 
tradisional. 
Scrapling dan 
scrapling-rs 
menyimpan sidik 
jari struktural 
elemen di SQLite 
dan menggunakan 
algoritma 
kemiripan 
12-faktor untuk 
menemukan 
kembali elemen 
meski situs 
mengubah tata 
letak HTML, 
dilengkapi 
pemecah 
Cloudflare 
Turnstile otomatis, 
penyamaran sidik 
jari TLS JA3/JA4 
(wreq), DoH 
anti-bocor DNS, 
dan server MCP 
bawaan. 
spider-rs/spider 
menjalankan 
strategi HTTP-first 
dan hanya 
membuka Chrome 
tanpa kepala 



<!-- [ID:06_AGGREGATOR_S013] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 261

No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Keunggulan 
Arsitektural & 
Peran Failover 
spider-rs/spider-no
dejs, 
https://github.com/
spider-rs/spider-cli
ents Spider MCP 
Servers: 
https://github.com/
spider-rs/spider-cl
oud-mcp-v2 & 
https://github.com/
spider-rs/spider-cl
oud-mcp-server 
Spider 
Browser/CDP/HT
ML2MD/UA: 
https://github.com/
spider-rs/headless
-browser, 
https://github.com/
spider-rs/chromey, 
https://github.com/
spider-rs/html2md, 
https://github.com/
spider-rs/ua_gener
ator Spider 
Reference Apps: 
https://github.com/
spider-rs/spider-cl
oud-live-code-view
er & 
https://github.com/
spider-rs/spider-ex
ample-knowledge-
base Alternatif 
Tambahan: 
https://github.com/
scrapy/scrapy, 
https://github.com/
seleniumbase/Sele
niumBase, 
https://github.com/
omkarcloud/botasa
urus, 
(headless) melalui 
crawl_smart() 
ketika halaman 
membutuhkan 
JavaScript. 



<!-- [ID:06_AGGREGATOR_S014] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 262

No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Keunggulan 
Arsitektural & 
Peran Failover 
https://github.com/
scrapfly/scrapfly-s
crapers 
1E.4 
Gateway 
Omnichannel 
Mandiri & 
Template 
Antarmuka Web 
WAHA — 
WhatsApp HTTP 
API (Sumber 3): 
https://github.com/
devlikeapro/waha 
Aceternity UI 
(Sumber 3): 
https://ui.aceternity
.com/ Magic UI 
(Sumber 3): 
https://magicui.des
ign/ 
Digunakan 
bersama Hermes 
Agent dan 
Nanobot untuk 
menghubungkan 
agen secara gratis 
ke WhatsApp, 
Telegram, Discord, 
Slack, Signal, dan 
Matrix, serta 
merakit antarmuka 
web bergaya 
Futuristic Luxury. 
Menghilangkan 
biaya langganan 
bulanan SaaS 
gateway pesan 
pihak ketiga 
melalui kontainer 
Docker mandiri. 
1E.5 
Direktori Riset, 
Kurasi Agen & 
Katalog Layanan 
Free-Tier 
Awesome Model 
Routing: 
https://github.com/
yenanjing/awesom
e-model-routing 
Awesome LLM 
Routing: 
https://github.com/
dstripelis/Awesom
e-LLM-Routing 
Awesome AI 
Agents (Aloth): 
https://github.com/
aloth/awesome-ai-
agents Awesome 
Agentic AI 
(Mfornos): 
https://github.com/
mfornos/awesome
-agentic-ai 
Awesome Agentic 
AI (Adriannoes): 
https://github.com/
adriannoes/aweso
me-agentic-ai 
Awesome AI 
Agents 
Topik Web 
Scraping Python: 
https://github.com/t
opics/web-scrapin
g-python Topik 
Spider Cloud: 
https://github.com/t
opics/spider-cloud 
Direktori Evaluasi 
API Agentik: 
https://apis.io/provi
ders/spider-cloud/ 
Berfungsi sebagai 
sumber penemuan 
otomatis 
(automated 
discovery 
registries) yang 
dapat dipindai 
secara berkala 
oleh agen perayap 
untuk menemukan 
layanan free-tier 
baru ketika 
penyedia lama 
mengubah 
ketentuan layanan. 



<!-- [ID:06_AGGREGATOR_S015] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 292

Zaeem20/FREE_PROXIES_LIST — GitHub trending stats & insights, 
https://trendshift.io/repositories/118339 12. Auto-Proxy-Fetcher/fetch_proxies.py at main - 
GitHub, https://github.com/VolkanSah/Auto-Proxy-Fetcher/blob/main/fetch_proxies.py 13. 
GitHub - WangYihang/Proxy-Verifier: A set of tools designed to, 
https://github.com/WangYihang/Proxy-Verifier 14. What Is huihui-ai (huihui AI)? Abliterated 
Models Guide, https://deepentresearch.com/en/journal/huihui-ai 15. Overview · 
cooper1637/SageAttention · GitHub, https://github.com/cooper1637/SageAttention/security 16. 
ali-vilab/TeaCache: Timestep Embedding Tells: It's Time to Cache, 
https://github.com/ali-vilab/TeaCache 17. InstantID: Zero-shot Identity-Preserving Generation in 
Seconds, https://github.com/instantx-research/instantid 18. rhasspy/piper: A fast, local neural 
text to speech system - GitHub, https://github.com/rhasspy/piper 19. Issue #2762 · 
k2-fsa/sherpa-onnx - tts模型推荐 - GitHub, https://github.com/k2-fsa/sherpa-onnx/issues/2762 
20. Releases · rhasspy/piper - GitHub, https://github.com/rhasspy/piper/releases 21. GitHub - 
Portkey-AI/gateway, https://github.com/portkey-ai/gateway 22. D4Vinci/Scrapling: 🕷️ A Web 
Scraping framework that ... - GitHub, https://github.com/d4vinci/Scrapling 23. GitHub - 
chrisabruce/scrapling-rs: Adaptive web scraping, built in, 
https://github.com/chrisabruce/scrapling-rs 24. Scrapling: Adaptive Python web scraping library 
that handles, https://www.scrapingbee.com/blog/scrapling-adaptive-python-web-scraping/ 25. 
Scrapling: Python Web Scraping Framework, 
https://scrapling.readthedocs.io/en/latest/index.html 26. Spider: a streaming Rust crawler that 
starts with HTTP - Hysen Labs, https://hysenlabs.com/projects/spider-rs-spider 27. 
ComfyUI-TeaCache - ComfyICU, https://comfy.icu/extension/welltop-cn__ComfyUI-TeaCache 
28. TeaCache/TeaCache4Wan2.1/README.md at main · ali ... - GitHub, 
https://github.com/ali-vilab/TeaCache/blob/main/TeaCache4Wan2.1/README.md 29. Akash 
Network - GitHub, https://github.com/akash-network 30. GitHub - akash-network/node: Source 
code for Akash node, a, https://github.com/akash-network/node 31. Node Architecture - Your 
Guide to Decentralized Cloud, https://akash.network/docs/node-operators/architecture/ 32. 
Releases · akash-network/node - GitHub, https://github.com/ovrclk/akash/releases 33. 
huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated - Hugging Face, 
https://huggingface.co/huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated 



<!-- [ID:06_AGGREGATOR_S016] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 316

No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Spesifikasi Teknis 
& Peran dalam 
Rantai Failover 
.co/docs/hub/other 
Crawl4AI SSRF 
Advisory: 
https://github.com/
advisories/GHSA-
wm69-2pc3-rmmf 
NVIDIA NeMo 
Guardrails & 
Llama Prompt 
Guard 2 (86M) 
(Sumber 3): 
https://github.com/
NVIDIA/NeMo-Gu
ardrails 
mencegah 
pencurian 
kredensial 
AWS/API, 
sedangkan 
NeMo-Guardrails 
dan Llama Prompt 
Guard 2 memfilter 
serangan prompt 
injection masuk. 
1E. Kerangka Kerja Agen Otonom, Crawler Adaptif, Gateway Omnichannel & 
Direktori Riset (Tanpa Pendaftaran) 
Pada lapisan akuisisi data web dan agen otonom, sumber induk mencantumkan 
unclecode/crawl4ai namun sekaligus memperingatkan adanya kerentanan keamanan tingkat 
tinggi GHSA-wm69-2pc3-rmmf (Unauthenticated Server-Side Request Forgery / SSRF pada 
jalur /crawl/stream di server Docker). Untuk memastikan agen memiliki jalur rolling yang bebas 
dari celah SSRF tersebut sekaligus mampu menembus proteksi Cloudflare Turnstile dan 
perubahan struktur HTML dinamis, riset menambahkan dua mesin perayap generasi baru yang 
jauh lebih tangguh: D4Vinci/Scrapling (beserta port Rust-nya chrisabruce/scrapling-rs) dan 
ekosistem perayap konkurensi tinggi berbasis Rust spider-rs/spider. Scrapling dan scrapling-rs 
menyimpan sidik jari struktural elemen di SQLite dan menghitung skor kemiripan 12-faktor untuk 
merelokasi elemen secara otomatis ketika situs web mengubah nama kelas CSS atau 
membungkus ulang struktur DOM, lengkap dengan emulasi 135+ profil sidik jari TLS 
(JA3/JA4/HTTP2) dan pemecah Cloudflare Turnstile bawaan. Di sisi lain, spider-rs/spider 
menerapkan arsitektur HTTP-first yang mengalirkan halaman secara real-time dan hanya 
meluncurkan peramban Chrome tanpa kepala (headless) melalui crawl_smart() ketika suatu 
halaman terbukti membutuhkan eksekusi JavaScript. 
No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Keunggulan 
Arsitektural & 
Peran Failover 
1E.1 
Stasiun Kerja 
Agen Otonom & 
Self-Evolving 
Harnesses 
OpenClaw (5.380 
Skills): 
https://github.com/
openclaw/opencla
w Nous Hermes 
Agent: 
https://github.com/
Hermes Install 
Script: 
https://hermes-age
nt.nousresearch.c
om/install.sh Pi 
Terminal Coding 
Agent: npm install 
OpenClaw, 
Hermes Agent, 
OpenHands, dan 
Pi dapat langsung 
diarahkan ke 
server lokal 
(http://127.0.0.1:80



<!-- [ID:06_AGGREGATOR_S017] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 318

No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Keunggulan 
Arsitektural & 
Peran Failover 
Web (Web 
Crawler) & 
Anti-Bot Adaptive 
Scrapers 
di Sumber 1): 
https://github.com/
unclecode/crawl4a
i 
(Python Adaptive 
Scraper & 
Turnstile 
Bypass): 
https://github.com/
D4Vinci/Scrapling 
(Docs: 
https://scrapling.re
adthedocs.io/en/lat
est/index.html, 
Docker: 
ghcr.io/d4vinci/scr
apling:latest) 
Scrapling-RS 
(Port Rust Native, 
135+ TLS 
Profiles): 
https://github.com/
chrisabruce/scrapli
ng-rs Spider-RS 
(Fastest Rust 
Crawler): 
https://github.com/
spider-rs/spider & 
Org: 
https://github.com/
spider-rs & Portal: 
https://spider.cloud
/open-source/ 
Spider 
Python/Node/Multi 
Clients: 
https://github.com/
spider-rs/spider-py
, 
https://github.com/
spider-rs/spider-no
dejs, 
https://github.com/
spider-rs/spider-cli
ents Spider MCP 
Servers: 
https://github.com/
kelemahan SSRF 
pada Docker 
Crawl4AI dan 
kerapuhan 
selector CSS 
tradisional. 
Scrapling dan 
scrapling-rs 
menyimpan sidik 
jari struktural 
elemen di SQLite 
dan menggunakan 
algoritma 
kemiripan 
12-faktor untuk 
menemukan 
kembali elemen 
meski situs 
mengubah tata 
letak HTML, 
dilengkapi 
pemecah 
Cloudflare 
Turnstile otomatis, 
penyamaran sidik 
jari TLS JA3/JA4 
(wreq), DoH 
anti-bocor DNS, 
dan server MCP 
bawaan. 
spider-rs/spider 
menjalankan 
strategi HTTP-first 
dan hanya 
membuka Chrome 
tanpa kepala 
(headless) melalui 
crawl_smart() 
ketika halaman 
membutuhkan 
JavaScript. 



<!-- [ID:06_AGGREGATOR_S018] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 319

No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Keunggulan 
Arsitektural & 
Peran Failover 
spider-rs/spider-cl
oud-mcp-v2 & 
https://github.com/
spider-rs/spider-cl
oud-mcp-server 
Spider 
Browser/CDP/HT
ML2MD/UA: 
https://github.com/
spider-rs/headless
-browser, 
https://github.com/
spider-rs/chromey, 
https://github.com/
spider-rs/html2md, 
https://github.com/
spider-rs/ua_gener
ator Spider 
Reference Apps: 
https://github.com/
spider-rs/spider-cl
oud-live-code-view
er & 
https://github.com/
spider-rs/spider-ex
ample-knowledge-
base Alternatif 
Tambahan: 
https://github.com/
scrapy/scrapy, 
https://github.com/
seleniumbase/Sele
niumBase, 
https://github.com/
omkarcloud/botasa
urus, 
https://github.com/
scrapfly/scrapfly-s
crapers 
1E.4 
Gateway 
Omnichannel 
Mandiri & 
Template 
WAHA — 
WhatsApp HTTP 
API (Sumber 3): 
https://github.com/
Digunakan 
bersama Hermes 
Agent dan 
Nanobot untuk 
Menghilangkan 
biaya langganan 
bulanan SaaS 
gateway pesan 



<!-- [ID:06_AGGREGATOR_S019] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 320

No 
Nama Sumber & 
Kategori 
Tautan Primer 
(Eksisting dari 
Sumber Induk) 
Tautan Alternatif & 
Superior Baru 
(Hasil Riset untuk 
Auto-Rolling) 
Keunggulan 
Arsitektural & 
Peran Failover 
Antarmuka Web devlikeapro/waha 
Aceternity UI 
(Sumber 3): 
https://ui.aceternity
.com/ Magic UI 
(Sumber 3): 
https://magicui.des
ign/ 
menghubungkan 
agen secara gratis 
ke WhatsApp, 
Telegram, Discord, 
Slack, Signal, dan 
Matrix, serta 
merakit antarmuka 
web bergaya 
Futuristic Luxury. 
pihak ketiga 
melalui kontainer 
Docker mandiri. 
1E.5 
Direktori Riset, 
Kurasi Agen & 
Katalog Layanan 
Free-Tier 
Awesome Model 
Routing: 
https://github.com/
yenanjing/awesom
e-model-routing 
Awesome LLM 
Routing: 
https://github.com/
dstripelis/Awesom
e-LLM-Routing 
Awesome AI 
Agents (Aloth): 
https://github.com/
aloth/awesome-ai-
agents Awesome 
Agentic AI 
(Mfornos): 
https://github.com/
mfornos/awesome
-agentic-ai 
Awesome Agentic 
AI (Adriannoes): 
https://github.com/
adriannoes/aweso
me-agentic-ai 
Awesome AI 
Agents 
(Slavakurilyak): 
https://github.com/
slavakurilyak/awes
ome-ai-agents 
Awesome AI 
Agents (E2B): 
https://github.com/
Topik Web 
Scraping Python: 
https://github.com/t
opics/web-scrapin
g-python Topik 
Spider Cloud: 
https://github.com/t
opics/spider-cloud 
Direktori Evaluasi 
API Agentik: 
https://apis.io/provi
ders/spider-cloud/ 
Berfungsi sebagai 
sumber penemuan 
otomatis 
(automated 
discovery 
registries) yang 
dapat dipindai 
secara berkala 
oleh agen perayap 
untuk menemukan 
layanan free-tier 
baru ketika 
penyedia lama 
mengubah 
ketentuan layanan. 



<!-- [ID:06_AGGREGATOR_S020] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: SPAN_4 -->
## Halaman 325

No 
Nama Penyedia 
Layanan 
Tautan 
Pendaftaran & 
Konsol Kunci 
(Eksisting & 
Gabungan) 
Alternatif / 
Endpoint Spesifik 
& Status Audit 
2026 
Kapasitas Kuota 
Gratis, Batas Laju 
& Peran Rolling 
hanya 
membutuhkan 
email untuk 
membuka akses 
kuota koding 
Claude dan Kiro 
gratis di 9Router. 
2A.9 
Hugging Face 
Access Tokens & 
Inference 
Providers 
Token: 
https://huggingface
.co/settings/tokens 
Dapat digunakan 
untuk menarik 
model 
GGUF/Safetensor
s 
(Wan/Flux/Kokoro) 
sekaligus 
memanggil 
Hugging Face 
Inference 
Providers. 
100% Tanpa 
Kartu. 
Menyertakan 
kredit bulanan 
$0,10/bulan yang 
dapat dirutekan ke 
mitra (Cerebras, 
Groq, Together, 
Fireworks, Novita, 
Scaleway, Z.ai), 
setara ~590.000 
token output pada 
gpt-oss-120b. 
2A.10 
Cohere 
Dashboard & 
Chutes AI 
(Bittensor 
Serverless) 
Cohere: 
https://dashboard.
cohere.com 
Chutes AI: 
https://chutes.ai 
Dokumentasi API 
Chutes: 
https://docs.chutes
.ai/ 
100% Tanpa 
Kartu. Cohere 
menyediakan Trial 
API Key otomatis 
dengan kuota 
1.000 
panggilan/bulan, 
sedangkan Chutes 
AI menyajikan 
inferensi 
serverless 
berbiaya nol atau 
rendah di atas 
jaringan 
terdesentralisasi 
Bittensor. 
2A.11 
Civitai & Spider 
Cloud API (Model 
Unfiltered & Web 
Crawling API) 
Civitai Account 
(Sumber 3): 
https://c[span_4](st
art_span)[span_4](
end_span)ivitai.co
m/user/account 
Spider Cloud API 
(Tanpa Kartu): 
https://spider.cloud 
100% Tanpa 
Kartu. Kunci API 
Civitai digunakan 
untuk menarik 
checkpoint gambar 
tanpa filter dan 



<!-- [ID:06_AGGREGATOR_S021] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 350

Models Guide, https://deepentresearch.com/en/journal/huihui-ai 15. Overview · 
cooper1637/SageAttention · GitHub, https://github.com/cooper1637/SageAttention/security 16. 
ali-vilab/TeaCache: Timestep Embedding Tells: It's Time to Cache, 
https://github.com/ali-vilab/TeaCache 17. InstantID: Zero-shot Identity-Preserving Generation in 
Seconds, https://github.com/instantx-research/instantid 18. rhasspy/piper: A fast, local neural 
text to speech system - GitHub, https://github.com/rhasspy/piper 19. Issue #2762 · 
k2-fsa/sherpa-onnx - tts模型推荐 - GitHub, https://github.com/k2-fsa/sherpa-onnx/issues/2762 
20. Releases · rhasspy/piper - GitHub, https://github.com/rhasspy/piper/releases 21. GitHub - 
Portkey-AI/gateway, https://github.com/portkey-ai/gateway 22. D4Vinci/Scrapling: 🕷️ A Web 
Scraping framework that ... - GitHub, https://github.com/d4vinci/Scrapling 23. GitHub - 
chrisabruce/scrapling-rs: Adaptive web scraping, built in, 
https://github.com/chrisabruce/scrapling-rs 24. Scrapling: Adaptive Python web scraping library 
that handles, https://www.scrapingbee.com/blog/scrapling-adaptive-python-web-scraping/ 25. 
Scrapling: Python Web Scraping Framework, 
https://scrapling.readthedocs.io/en/latest/index.html 26. Spider: a streaming Rust crawler that 
starts with HTTP - Hysen Labs, https://hysenlabs.com/projects/spider-rs-spider 27. 
ComfyUI-TeaCache - ComfyICU, https://comfy.icu/extension/welltop-cn__ComfyUI-TeaCache 
28. TeaCache/TeaCache4Wan2.1/README.md at main · ali ... - GitHub, 
https://github.com/ali-vilab/TeaCache/blob/main/TeaCache4Wan2.1/README.md 29. Akash 
Network - GitHub, https://github.com/akash-network 30. GitHub - akash-network/node: Source 
code for Akash node, a, https://github.com/akash-network/node 31. Node Architecture - Your 
Guide to Decentralized Cloud, https://akash.network/docs/node-operators/architecture/ 32. 
Releases · akash-network/node - GitHub, https://github.com/ovrclk/akash/releases 33. 
huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated - Hugging Face, 
https://huggingface.co/huihui-ai/Huihui-Qwen3.6-35B-A3B-abliterated 


