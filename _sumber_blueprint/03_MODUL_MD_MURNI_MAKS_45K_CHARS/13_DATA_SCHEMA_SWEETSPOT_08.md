
<!-- [ID:13_DATA_SCHEMA_S102] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: DOM -->
## Halaman 11

        domain_groups[dom].sort(key=lambda x: x["dna"]["score"], 
reverse=True)​
​
    # 5. Bangun File Laci Modul MD (DIKUNCI KETAT MAKSIMAL 45.000 
KARAKTER PER FILE)​
    #    Sekaligus kumpulkan entri untuk 1-3 File Master Peta Otak AI​
    master_catalog_entries = []​
    total_saved_chars = 0​
​
    for dom in sorted(domain_groups.keys()):​
        secs = domain_groups[dom]​
        part_no = 1​
        curr_bucket = []​
        curr_bucket_len = 0​
        curr_bucket_meta = []​
​
        for idx, s in enumerate(secs, 1):​
            img_info = f" | Gambar: {len(s['dna']['images'])} file 
({', '.join(s['dna']['images'][:3])})" if s['dna']['images'] else ""​
            tag_info = f" | Tag Asli: {', 
'.join(s['discovered_tags'][:5])}" if s['discovered_tags'] else ""​
            ​
            header_tag = (​
                f"\n<!-- [ID:{dom}_S{idx:03d}] SUMBER: {s['source']} | 
GRADE: {s['dna']['grade']}{tag_info}{img_info} -->\n"​
            )​
            full_block = header_tag + s["content"]​
            total_saved_chars += len(s["content"])​
​
            # Pastikan tidak ada 1 blok pun yang melebihi 45.000 
karakter​
            sub_blocks = slice_oversized_section_safely(full_block, 
MAX_MD_SWEETSPOT_CHARS - 1500)​
​
            for sub_i, sb in enumerate(sub_blocks, 1):​
                if curr_bucket_len + len(sb) > MAX_MD_SWEETSPOT_CHARS 
and curr_bucket:​
                    fname = f"{dom}_SWEETSPOT_{part_no:02d}.md"​
                    (MODUL_MD_45K_DIR / 
fname).write_text("".join(curr_bucket), encoding="utf-8")​
                    ​
                    # Catat ke Master Peta Otak AI​
                    master_catalog_entries.append({​
                        "file": fname,​
                        "domain": dom,​
                        "chars": curr_bucket_len,​
                        "items": curr_bucket_meta​
                    })​



<!-- [ID:13_DATA_SCHEMA_S103] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: :90 -->
## Halaman 12

                    part_no += 1​
                    curr_bucket = []​
                    curr_bucket_len = 0​
                    curr_bucket_meta = []​
​
                curr_bucket.append(sb)​
                curr_bucket_len += len(sb)​
                curr_bucket_meta.append({​
                    "id": f"{dom}_S{idx:03d}" + (f"_P{sub_i}" if 
len(sub_blocks) > 1 else ""),​
                    "title": re.sub(r"\s+", " ", s["title"])[:90],​
                    "grade": s["dna"]["grade"],​
                    "symbols": s["dna"]["symbols"],​
                    "images": [Path(p).name for p in 
s["dna"]["images"]],​
                    "tags": s["discovered_tags"][:4],​
                    "chars": len(sb)​
                })​
​
        if curr_bucket:​
            fname = f"{dom}_SWEETSPOT_{part_no:02d}.md"​
            (MODUL_MD_45K_DIR / 
fname).write_text("".join(curr_bucket), encoding="utf-8")​
            master_catalog_entries.append({​
                "file": fname,​
                "domain": dom,​
                "chars": curr_bucket_len,​
                "items": curr_bucket_meta​
            })​
​
    # 6. Cetak 1-3 FILE MASTER "PETA OTAK & KONTRAK TEKNIS" (KETAT <= 
45.000 KARAKTER PER FILE!)​
    master_header = (​
        "# MASTER BLUEPRINT & PETA OTAK ARSITEKTUR (SWEETSPOT <= 45K 
KARAKTER)\n"​
        "Dokumen ini memuat **100% daftar fitur, modul, fungsi kode, 
gambar diagram, dan hasil Auto-Discovery** "​
        "dari seluruh PDF (868 Halaman) & MD (3.8 Juta Karakter) tanpa 
1 pun fitur yang terlewat.\n\n"​
        "**CARA KERJA AI CODING:**\n"​
        "1. Baca peta utuh ini agar memahami keterkaitan seluruh 
sistem dan 26+ domain (termasuk `26_AUTO_DISCOVERY`).\n"​
        "2. Setiap fitur/kode mentah disimpan 100% lossless di file 
`nama_file_sweetspot.md` (<= 45k karakter).\n"​
        "3. Jangan pernah menghilangkan fitur apa pun yang tercatat di 
indeks Master ini!\n\n"​
    )​
​



<!-- [ID:13_DATA_SCHEMA_S104] SUMBER: PDF:Ya mau. kalau bisa karena tujuan akhir saya saat m....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 3. KAMUS 25 DOMAIN + MESIN AUTO-DISCOVERY (TANGKAP 100% LABEL LIAR)​
# 
======================================================================
========​
DOMAIN_SCHEMA = {​
    "01_ARCH": ["monorepo", "tech stack", "microservice", "env", "api 
gateway", "dependency", "arsitektur", "architecture"],​
    "02_CORE_AI": ["llm", "router", "sota", "rag", "memory", "fine 
tuning", "fine-tuning", "fallback", "embedding", "prompt"],​
    "03_V_OFFICE": ["177 agen", "kantor virtual", "virtual office", 
"org chart", "state machine", "message broker", "consensus", 
"handoff", "shift", "agent_"],​
    "04_PROMPT_LIB": ["system prompt", "few shot", "few-shot", "json 
schema", "negative prompt", "chain template"],​
    "05_TOOLS_ENGINE": ["playwright", "puppeteer", "ffmpeg", "mcp", 
"browser agent", "file converter", "search api"],​
    "06_AGGREGATOR": ["scraper", "scraping", "spider", "crawler", 
"aggregator", "social listener", "market spy", "deduplicator", 
"normalizer"],​
    "07_CONTENT_FACTORY": ["copywriting", "script director", "video 
assembler", "carousel", "localization", "quality gate", "pabrik 
aset"],​
    "08_OMNI_SOCIAL": ["whatsapp", "telegram", "instagram", 
"facebook", "threads", "tiktok", "comment bot", "sosial media", 
"auto-upload"],​
    "09_COMMERCE_AFF": ["affiliate", "marketplace", "cloaking", 
"autolist", "price sync", "crm", "offer hunter", "shopee", 
"tokopedia", "tiktok shop"],​
    "10_STOCK_ENGINE": ["microstock", "shutterstock", "adobe stock", 
"freepik", "upscaler", "vector", "exif", "iptc", "sftp", "artifact 
cleaner"],​
    "11_WEB_PLATFORM": ["frontend", "admin console", "dashboard", 
"cms", "seo", "client portal", "websocket"],​
    "12_FINANCE": ["pricing", "harga", "finansial", "token economics", 
"unit economics", "payment gateway", "revenue", "profit", "stripe", 
"midtrans", "rumus harga"],​
    "13_DATA_SCHEMA": ["postgresql", "mysql", "sql", "mongodb", 
"nosql", "vector db", "qdrant", "pinecone", "milvus", "neo4j", "graph 
db", "redis", "s3", "bucket", "database", "schema"],​



<!-- [ID:13_DATA_SCHEMA_S105] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Backend
- FastAPI (apps/api, services/*)
- Postgres + Redis


<!-- [ID:13_DATA_SCHEMA_S106] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# ==== Database ====
DATABASE_URL=postgres://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379


<!-- [ID:13_DATA_SCHEMA_S107] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 2. DATABASE STATE (MULTI-QRIS POOL, INVOICE, & CLOSED-LOOP TREASURY)

<!-- [ID:13_DATA_SCHEMA_S108] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# Dependencies (PyPI): pip install aiogram aiohttp aiosqlite httpx cryptography

<!-- [ID:13_DATA_SCHEMA_S109] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
#    Response Malware Scrubber, Live <2.5s Schema Ping Gate) + /donasi_api

<!-- [ID:13_DATA_SCHEMA_S110] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 2. DATABASE SCHEMA ABADI v3.6.0 (11 TABEL MASTER TERMASUK PAYMENT INVOICES)

<!-- [ID:13_DATA_SCHEMA_S111] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: EXECUTE_MIGRATION -->
## PROTOKOL 4: PROSEDUR MIGRASI OTOMATIS (NOMADIC PROTOCOL)
Jika Owner memberikan perintah otorisasi `[EXECUTE_MIGRATION]` beserta parameter tujuan baru (URL Repo baru, Server baru, atau Mode Handover Pembeli), jalankan urutan otomatis berikut:
1. Ubah status di tabel `infrastructure_registry` menjadi `'MIGRATING'` dan hentikan sementara antrean job publik.
2. Lakukan full backup database Turso ke dalam file `.sql` terenkripsi.
3. Jika target migrasi adalah repositori Git baru: jalankan `git clone --mirror` dari repo lama dan `git push --mirror` ke repo baru untuk memindahkan seluruh cabang, commit, dan tag tanpa kehilangan histori.
4. Perbarui koordinat endpoint di tabel `infrastructure_registry` dengan alamat yang baru, lakukan tes ping/integritas, lalu kembalikan status menjadi `'STABLE'` dan catat hasilnya di tabel `migration_logs`.

<!-- [ID:13_DATA_SCHEMA_S112] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# - Python 3.14 Compatible SingleWriterSQLiteDaemon & 10 Tabel Master

<!-- [ID:13_DATA_SCHEMA_S113] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 2. DATABASE SCHEMA ABADI v3.4.0 (TERMASUK PERSISTENT SETTINGS & SUB-BOT LOGS)

<!-- [ID:13_DATA_SCHEMA_S114] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 1. SINGLE-WRITER SQLITE WAL DAEMON & 16 TABEL UTUH
