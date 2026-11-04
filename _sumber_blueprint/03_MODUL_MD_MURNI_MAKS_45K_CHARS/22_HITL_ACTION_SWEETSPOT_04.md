
<!-- [ID:22_HITL_ACTION_S029] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER -->
## Halaman 362

sensitif, serta adaptor Bittensor-ready dan ModelScan/Safetensors Gate.
D2. ARSITEKTUR TARGET (Konsolidasi Utuh v3.7.0 + Patch v4.0 + Master Contract v1.0)
Tanpa menghapus satu pun fitur dari v1.0 hingga v3.7.0, struktur app.py akan disatukan menjadi Master Engine v4.0 (Frontier Autonomic Core)
dengan penambahan komponen kontrak berikut:
1. [FAKTA] [Bersumber] Orchestrator Tipis & Plugin Surface (PluginRegistry):
Mendukung dekorator/metode register_plugin(name, handler, version), pemeriksaan await plugin.health(), dan
hot_swap_plugin(name, new_source_code) yang otomatis melewati 4-Gate AST & Dunder Sterilizer sebelum dipasang di memori
tanpa mematikan bot.
2. [FAKTA] [Bersumber] Self-Healing Loop Level Orchestrator (SelfHealingOrchestrator):
Mengimplementasikan alur deterministik: classify_error(exc) → select_handler(err_type) → apply_fix() →
verify_health().
Jika perbaikan mandiri gagal 3 kali berturut-turut pada komponen/endpoint yang sama, sistem menghentikan retry berisiko,
mengarantina komponen, mencatat insiden ke tabel human_escalation_queue, dan mengirim notifikasi darurat ke DM Owner.
3. [FAKTA] [Bersumber] Human Approval Gate Eksplisit di Kode (HumanApprovalGate):
Menambahkan tabel pending_human_approvals dan fungsi pengunci di level kode untuk 5 aksi wajib persetujuan Owner:
1. DATA_MIGRATION (migrasi skema/ekspor database).
2. PRICE_PLAN_CHANGE (perubahan tarif koin/paket PPP).
3. DELETE_FEATURE_PLUGIN (penghapusan/penonaktifan plugin atau fitur).
4. WITHDRAW_ABOVE_THRESHOLD (penarikan/harvest laba bersih di atas ambang batas HARVEST_APPROVAL_THRESHOLD_IDR).
5. SECURITY_POLICY_CHANGE (perubahan mode produksi, whitelist AST, atau penguncian Owner).
Setiap aksi di atas menghasilkan tiket persetujuan dengan tombol [✅ Setujui Eksekusi] dan [❌ Batalkan] di DM Owner.
4. [FAKTA] [Bersumber] Penambalan Penuh VULN-01 s.d. VULN-08 & Ekosistem Sumber Daya:
Staggered Speculative Hedging (
) + RouteLLM Complexity Scorer (
): Menembak penyedia primer tercepat pada
 dan hanya memicu gelombang cadangan jika belum ada respons dalam 1,2 detik, ditambah dukungan rute Chutes AI (Bittensor
Serverless), Groq, Cerebras, OpenRouter, Gemini 2.5/3.8 Flash, Pollinations, serta Puter.js Client Bridge di Web Studio.
Blinded Ed25519 Voucher + Atomic Escrow Burn: Menghapus user_id dari payload JSON voucher (diganti komitmen hash buta 
)
dan memotong koin secara atomik.
Bittensor Subnet 27 & ModelScan/Safetensors Gate: Menyediakan adaptor kesiapan node Bittensor Compute (rumus skor 
 dengan timeout, retry, dan circuit breaker) serta pemindai ekstensi bobot model (.safetensors / .gguf & integrasi CLI
modelscan) di panel /bansos & /admin.
D3. RENCANA BERTAHAP (Kriteria Sukses & Rollback Trigger)
1. Fase 1 — Rekonstruksi Sintaksis Bersih, Fondasi SQLite Singleton WAL & Human Approval Gate:
Target: Membersihkan seluruh artefak OCR dari kode v3.7.0, menambahkan tabel pending_human_approvals &
human_escalation_queue, menerapkan koneksi SQLite WAL terkelola, serta mengunci is_verified_owner_dm (Fail-Closed +
Bootstrap Token) dan HumanApprovalGate.
Kriteria Sukses: python3 -m py_compile app.py menghasilkan exit code 0 (0 syntax error) dan pemeriksaan skema database
menciptakan 13 tabel utuh.
Rollback Trigger: Kegagalan kompilasi AST atau kegagalan transaksi SingleWriterSQLiteDaemon.
2. Fase 2 — Integrasi Plugin Surface, Self-Healing Loop (Max 3x Retry → Escalate), Staggered Router & Bittensor/ModelScan Adapter:
Target: Memasang PluginRegistry (register, health, hot_swap), SelfHealingOrchestrator, Two-Tier Staggered Hedging (
), RouteLLM Matrix Classifier, 4-Gate Bansos Sterilizer, ModelScan/Safetensors Validator, dan Bittensor Compute Adapter.
Kriteria Sukses: Uji simulasi matikan dependency memicu tepat 3x percobaan perbaikan lalu otomatis masuk ke
human_escalation_queue tanpa infinite loop; pemeriksaan sterilize_community_script_ast memblokir traversi dunder
(__subclasses__, __import__) 100%.
Rollback Trigger: Retry melebihi 3x atau lolosnya atribut dunder pada pengujian AST.
3. Fase 3 — Konsolidasi Penuh Antarmuka Bot, Mini App SFW v4.0, Freedom Web Studio & Verifikasi Privasi:
τ = 1, 2s
τ = 0, 11593
t = 0
H
​
blind
S
​ =
total
S
​ +
GPU
B
​
alloc
τ = 1, 2s



<!-- [ID:22_HITL_ACTION_S030] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 3. 15 Tabel Master (Termasuk Approval Gate, Escalation Queue, Hot-Patch, QRIS)

<!-- [ID:22_HITL_ACTION_S031] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
# 6. Human Approval Gate Eksplisit (5 Operasi Sensitif Wajib Persetujuan Owner)

<!-- [ID:22_HITL_ACTION_S032] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER -->
## Halaman 455

Mengimplementasikan alur deterministik: classify_error(exc) →
select_handler(err_type) → apply_fix() → verify_health().
Jika perbaikan mandiri gagal 3 kali berturut-turut pada komponen/endpoint yang
sama, sistem menghentikan retry berisiko, mengarantina komponen, mencatat insiden
ke tabel human_escalation_queue, dan mengirim notifikasi darurat ke DM Owner.
3. [FAKTA] [Bersumber] Human Approval Gate Eksplisit di Kode (HumanApprovalGate):
Menambahkan tabel pending_human_approvals dan fungsi pengunci di level kode
untuk 5 aksi wajib persetujuan Owner:
1. DATA_MIGRATION (migrasi skema/ekspor database).
2. PRICE_PLAN_CHANGE (perubahan tarif koin/paket PPP).
3. DELETE_FEATURE_PLUGIN (penghapusan/penonaktifan plugin atau fitur).
4. WITHDRAW_ABOVE_THRESHOLD (penarikan/harvest laba bersih di atas ambang
batas HARVEST_APPROVAL_THRESHOLD_IDR).
5. SECURITY_POLICY_CHANGE (perubahan mode produksi, whitelist AST, atau
penguncian Owner).
Setiap aksi di atas menghasilkan tiket persetujuan dengan tombol [✅ Setujui
Eksekusi] dan [❌ Batalkan] di DM Owner.
4. [FAKTA] [Bersumber] Penambalan Penuh VULN-01 s.d. VULN-08 & Ekosistem Sumber Daya:
Staggered Speculative Hedging (
) + RouteLLM Complexity Scorer (
): Menembak penyedia primer tercepat pada 
 dan hanya memicu
gelombang cadangan jika belum ada respons dalam 1,2 detik, ditambah dukungan rute
Chutes AI (Bittensor Serverless), Groq, Cerebras, OpenRouter, Gemini 2.5/3.8 Flash,
Pollinations, serta Puter.js Client Bridge di Web Studio.
Blinded Ed25519 Voucher + Atomic Escrow Burn: Menghapus user_id dari payload
JSON voucher (diganti komitmen hash buta 
) dan memotong koin secara atomik.
Bittensor Subnet 27 & ModelScan/Safetensors Gate: Menyediakan adaptor kesiapan
node Bittensor Compute (rumus skor 
 dengan timeout, retry,
dan circuit breaker) serta pemindai ekstensi bobot model (.safetensors / .gguf &
integrasi CLI modelscan) di panel /bansos & /admin.
D3. RENCANA BERTAHAP (Kriteria Sukses & Rollback Trigger)
1. Fase 1 — Rekonstruksi Sintaksis Bersih, Fondasi SQLite Singleton WAL & Human Approval
Gate:
Target: Membersihkan seluruh artefak OCR dari kode v3.7.0, menambahkan tabel
pending_human_approvals & human_escalation_queue, menerapkan koneksi
τ = 1, 2s
τ =
0, 11593
t = 0
H
​
blind
S
​ =
total
S
​ +
GPU
B
​
alloc



<!-- [ID:22_HITL_ACTION_S033] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 575

        ).hexdigest()​
        if 
VOUCHER_NULLIFIER_GUARD.is_replayed_or_register(nullifier_hash):​
            return None​
        return data​
    except Exception:​
        return None​
​
​
# 
======================================================================
========​

<!-- [ID:22_HITL_ACTION_S034] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER -->
## Halaman 615

sistem menghentikan retry berisiko, mengarantina komponen, mencatat insiden ke tabel 
human_escalation_queue, dan mengirim notifikasi darurat ke DM Owner. 
3.​ [FAKTA] [Bersumber] Human Approval Gate Eksplisit di Kode (HumanApprovalGate): 
○​ Menambahkan tabel pending_human_approvals dan fungsi pengunci di level kode untuk 5 aksi 
wajib persetujuan Owner: 
1.​ DATA_MIGRATION (migrasi skema/ekspor database). 
2.​ PRICE_PLAN_CHANGE (perubahan tarif koin/paket PPP). 
3.​ DELETE_FEATURE_PLUGIN (penghapusan/penonaktifan plugin atau fitur). 
4.​ WITHDRAW_ABOVE_THRESHOLD (penarikan/harvest laba bersih di atas ambang batas 
HARVEST_APPROVAL_THRESHOLD_IDR). 
5.​ SECURITY_POLICY_CHANGE (perubahan mode produksi, whitelist AST, atau penguncian 
Owner). 
○​ Setiap aksi di atas menghasilkan tiket persetujuan dengan tombol [✅ Setujui Eksekusi] dan [❌ 
Batalkan] di DM Owner. 
4.​ [FAKTA] [Bersumber] Penambalan Penuh VULN-01 s.d. VULN-08 & Ekosistem Sumber Daya: 
○​ Staggered Speculative Hedging (τ=1,2s) + RouteLLM Complexity Scorer (τ=0,11593): 
Menembak penyedia primer tercepat pada t=0 dan hanya memicu gelombang cadangan jika 
belum ada respons dalam 1,2 detik, ditambah dukungan rute Chutes AI (Bittensor Serverless), 
Groq, Cerebras, OpenRouter, Gemini 2.5/3.8 Flash, Pollinations, serta Puter.js Client Bridge di 
Web Studio. 
○​ Blinded Ed25519 Voucher + Atomic Escrow Burn: Menghapus user_id dari payload JSON 
voucher (diganti komitmen hash buta Hblind​) dan memotong koin secara atomik. 
○​ Bittensor Subnet 27 & ModelScan/Safetensors Gate: Menyediakan adaptor kesiapan node 
Bittensor Compute (rumus skor Stotal​=SGPU​+Balloc​ dengan timeout, retry, dan circuit breaker) serta 
pemindai ekstensi bobot model (.safetensors / .gguf & integrasi CLI modelscan) di panel 
/bansos & /admin. 
 
D3. RENCANA BERTAHAP (Kriteria Sukses & Rollback Trigger) 
 
1.​ Fase 1 — Rekonstruksi Sintaksis Bersih, Fondasi SQLite Singleton WAL & Human Approval Gate: 
○​ Target: Membersihkan seluruh artefak OCR dari kode v3.7.0, menambahkan tabel 
pending_human_approvals & human_escalation_queue, menerapkan koneksi SQLite WAL 
terkelola, serta mengunci is_verified_owner_dm (Fail-Closed + Bootstrap Token) dan 
HumanApprovalGate. 
○​ Kriteria Sukses: python3 -m py_compile app.py menghasilkan exit code 0 (0 syntax error) dan 
pemeriksaan skema database menciptakan 13 tabel utuh. 
○​ Rollback Trigger: Kegagalan kompilasi AST atau kegagalan transaksi 
SingleWriterSQLiteDaemon. 
2.​ Fase 2 — Integrasi Plugin Surface, Self-Healing Loop (Max 3x Retry → Escalate), Staggered 
Router & Bittensor/ModelScan Adapter: 
○​ Target: Memasang PluginRegistry (register, health, hot_swap), SelfHealingOrchestrator, 
Two-Tier Staggered Hedging (τ=1,2s), RouteLLM Matrix Classifier, 4-Gate Bansos Sterilizer, 
ModelScan/Safetensors Validator, dan Bittensor Compute Adapter. 
○​ Kriteria Sukses: Uji simulasi matikan dependency memicu tepat 3x percobaan perbaikan lalu 
otomatis masuk ke human_escalation_queue tanpa infinite loop; pemeriksaan 
sterilize_community_script_ast memblokir traversi dunder (__subclasses__, __import__) 100%. 
○​ Rollback Trigger: Retry melebihi 3x atau lolosnya atribut dunder pada pengujian AST. 



<!-- [ID:22_HITL_ACTION_S035] SUMBER: PDF:Gabungan PDF All.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: FAKTA, BERSUMBER, CITE: 85 -->
## Halaman 623

●​ [FAKTA] [Bersumber] Seluruh kode v3.4.0 (App.py) dan v3.7.0 (audit update 1.pdf) tetap 
dipertahankan 100% tanpa ada fitur yang dihapus[cite: 37, 161, 191], dan diperluas dengan 10 
spesifikasi baru pada A4. 
D2. Arsitektur Target v4.0 (Modular, Suntik-Siap, & 3-Step UX) 
1.​ Lapisan Keamanan "Suntik" (HotPatchEngine + PluginRegistry + HumanApprovalGate): 
○​ app.py bertindak sebagai orchestrator tipis dengan PluginRegistry (register, health(), 
hot_swap()) dan perintah /suntik di DM /admin untuk menyuntikkan aturan keamanan, model 
baru, atau plugin tanpa restart. 
○​ HumanApprovalGate mengunci 5 operasi sensitif di kode: migrasi data, ubah harga/plan, 
hapus fitur/plugin, tarik saldo di atas threshold, dan ubah kebijakan keamanan. 
2.​ Interaksi 3-Langkah (3-Step Progressive Disclosure) & Auto-Bahasa (ID vs EN): 
○​ Deteksi otomatis language_code pengguna sejak detik pertama[cite: 72, 161]: 
■​ Langkah 1: Hanya menampilkan 3 Tombol Etalase Utama (1. Studio Visual/Video/Suara, 
2. Riset, Koding & Chat, 3. Dompet, Eceran/Sub, Afiliasi & API Mandiri) + peluncur Mini 
App[cite: 85]. 
■​ Langkah 2: Jika pengguna berbahasa Indonesia (id) mengklik kategori, muncul 
sub-menu rapi Preset Orang Awam (UMKM, Studio, Foto Jadi Video, Hapus BG). Untuk 
pengguna Global (en), antarmuka langsung menampilkan kontrol studio profesional yang 
bersih dalam bahasa Inggris. 
■​ Langkah 3: Eksekusi disertai Animasi Tunggu & Live Progress Bar (⏳ [25%]... → ⚡ 
[60%]... → ✨ [95%]...) + send_chat_action agar pengguna tahu persis proses berjalan 
lancar dan tidak mengira bot error. 
3.​ Auto-Grup Komunitas Lintas Negara (Ambang Batas ≥100 Pengguna): 
○​ Tabel geo_community_clusters mencatat jumlah pengguna per negara/bahasa. Saat suatu 
negara mencapai 100 pengguna, bot otomatis menyiapkan klaster/topik komunitas bahasa 
tersebut dan mengirim tombol aktivasi 1-klik ke Owner (lengkap dengan fitur /setup_grup 
otomatis 6 kamar topik dalam bahasa lokal mereka)[cite: 123, 185]. 
4.​ Self-Healing Loop & Router Cerdas (Combo Grading + Staggered Hedging 1.2s + 
Anti-Soft-Refusal): 
○​ Mengikuti alur: classify_error → pilih handler → apply_fix → verify → gagal 3x → escalate ke 
log + human_escalation_queue. 
○​ Menyediakan endpoint /v1/chat/completions dan /v1/images/generations dengan autentikasi 
sk-bikinai-... untuk melayani pasar vibecoders / pengguna mandiri. 
 
D3. Rencana Bertahap Revisi v4.0 (Kriteria Sukses & Rollback Trigger) 
 
1.​ Fase 1 — Fondasi 15 Tabel SQLite WAL, HotPatchEngine (/suntik), HumanApprovalGate, & 
SelfHealingOrchestrator: 
○​ Kriteria Sukses: python3 -m py_compile app.py lulus 100% (exit code 0), uji suntik aturan baru 
berhasil tanpa restart, dan simulasi matikan dependency berhenti tepat pada retry ke-3 lalu 
masuk ke human_escalation_queue[cite: 40, 191]. 
○​ Rollback Trigger: Kegagalan kompilasi AST atau kegagalan isolasi plugin[cite: 47, 191]. 
2.​ Fase 2 — Router Combo Grading, Staggered Hedging, Anti-Soft-Refusal, & 
AutonomousResourceHarvester (Auto-Test vs Owner Control): 
○​ Kriteria Sukses: Endpoint gratis diuji mandiri (<2,0s) sebelum masuk antrean aktif, sedangkan 



<!-- [ID:22_HITL_ACTION_S036] SUMBER: PDF:Wah kamu ada yang terlewat nih. auto discovery lab....pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman 10

    total_input_chars = 0​
​
    # 1. Ekstrak PDF dengan MinerU + Potong PDF Asli per 20 Halaman​
    for pdf_f in RAW_PDF_FILES:​
        if os.path.exists(pdf_f):​
            slice_raw_pdf_into_20_page_sweetspots(pdf_f)​
            mineru_md = extract_pdf_and_rescue_images(pdf_f, 
MINERU_OUT_DIR)​
            txt = mineru_md.read_text(encoding="utf-8", 
errors="replace")​
            total_input_chars += len(txt)​
            all_sections.extend(split_lossless_sections(txt, 
f"PDF:{Path(pdf_f).name}"))​
        else:​
            print(f"[!] File PDF {pdf_f} tidak ditemukan, 
melewati...")​
​
    # 2. Baca File MD Mentah 3.8 Juta Karakter​
    for md_f in RAW_MD_FILES:​
        if os.path.exists(md_f):​
            txt = Path(md_f).read_text(encoding="utf-8", 
errors="replace")​
            total_input_chars += len(txt)​
            all_sections.extend(split_lossless_sections(txt, 
f"MD:{Path(md_f).name}"))​
        else:​
            print(f"[!] File MD {md_f} tidak ditemukan, melewati...")​
​
    # 3. Deduplikasi 100% SHA-256 Utuh (Hanya membuang jika isi teks 
100% kembar identik)​
    domain_groups = defaultdict(list)​
    seen_hashes = set()​
    exact_dup_chars = 0​
​
    for sec in tqdm(all_sections, desc="Memeriksa Keutuhan Karakter & 
Auto-Discovery"):​
        if not sec["content"]:​
            continue​
        h = hashlib.sha256(sec["content"].encode("utf-8")).hexdigest()​
        if h in seen_hashes:​
            exact_dup_chars += len(sec["content"])​
            continue​
        seen_hashes.add(h)​
        domain_groups[sec["domain"]].append(sec)​
​
    # 4. Urutkan di setiap domain: Prioritaskan yang paling kaya kode 
& gambar di atas​
    for dom in domain_groups:​



<!-- [ID:22_HITL_ACTION_S037] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Gate owner
{approval_gate_list}


<!-- [ID:22_HITL_ACTION_S038] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Aturan keras
1. Agent tidak pernah sign transaksi / panggil bank API langsung.
2. Semua intent → gate FIN (ApprovalBroker X002).
3. Kill switch L1 aktif → semua intent ditolak.
4. Eksekusi hanya setelah owner approve + actor match.
5. Idempotency key = intent_id (tidak boleh dobel bayar).


<!-- [ID:22_HITL_ACTION_S039] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Alur
Agent → create_intent() → risk score → ApprovalBroker (X002) → notif owner
→ owner /approve → execute() → provider (bank/ewallet/crypto) → paid → audit.


<!-- [ID:22_HITL_ACTION_S040] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: :20 -->
## Endpoint
- `GET /verify` — cek hash chain, return `{ok, total, bad_count, bad[:20]}`
- `GET /timeline?start=&end=&agent=&event_type=&channel=&limit=`
- `GET /incident/{approval_id|intent_id}` — rekonstruksi insiden


<!-- [ID:22_HITL_ACTION_S041] SUMBER: MD:merged save.md | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR -->
## Halaman
- `/` — overview (kill switch, spend, calls)
- `/approvals` — queue approval pending, tombol approve/deny
- `/agents` — list agent + mode + gate
- `/kill-switch` — tombol L0/L1/L2/L4 + recover

