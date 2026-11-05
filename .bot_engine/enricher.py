import os
import re
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime

try:
    import fitz  # PyMuPDF buat nyedot 880 halaman PDF tanpa kelewat 1 huruf pun
except ImportError:
    fitz = None

MARKAS_BP = Path("_sumber_blueprint")
DIR_00 = MARKAS_BP / "00_MENTAHAN_UTUH_3_86JUTA_MD_DAN_PDF"
DIR_01 = MARKAS_BP / "01_MINERU_RAW_DAN_GAMBAR"
DIR_02 = MARKAS_BP / "02_MASTER_1_SAMPAI_3_FILE_SWEETSPOT_45K"
DIR_03 = MARKAS_BP / "03_MODUL_MD_MURNI_MAKS_45K_CHARS"
DIR_04 = MARKAS_BP / "04_MODUL_PDF_MURNI_MAKS_20_HALAMAN"
DIR_05 = MARKAS_BP / "05_KOLEKSI_GAMBAR_DIAGRAM_PDF"

CACHE_MENTAHAN_FILE = Path(".bot_engine/cache_mentahan_utuh.json")
OVERFLOW_QUEUE_FILE = Path("antrean_tumpahan_mentahan.json")
ENV_FILE = Path(".env")

# Diturunkan ke 43.000 - 46.500 karakter supaya AMAN 100% di-copy dari browser HP tanpa kepotong di bawah!
BATAS_BAWAH_SWEETSPOT = 43000
BATAS_ATAS_SWEETSPOT  = 46500

# Kamus Layanan + Env Key + Guide Ringkas Padat buat Bos
KAMUS_LAYANAN_DAN_ENV = {
    "turso": (
        "Turso / LibSQL Database",
        ["TURSO_DATABASE_URL", "TURSO_AUTH_TOKEN"],
        "1. Buka app.turso.tech -> Klik 'Create Database' (kasih nama bebas, misal: `markas-preman`). "
        "2. Klik DB-nya -> Copy `libsql://...` ke `TURSO_DATABASE_URL` & klik 'Generate Token' (Read & Write) -> Copy ke `TURSO_AUTH_TOKEN` di `.env` Codespaces. "
        "3. Soal tabel masih kosong: TENANG BOS, kode Python yang dibuat AI di sesi ini wajib menyertakan fungsi Auto-Migrate (`CREATE TABLE IF NOT EXISTS`) + script seeder otomatis buat ngelempar isi `.env` ke Turso!"
    ),
    "supabase": (
        "Supabase Postgres/Auth/Storage",
        ["SUPABASE_URL", "SUPABASE_KEY"],
        "1. Login supabase.com -> 'New Project'. 2. Masuk Project Settings -> API -> Copy 'Project URL' & 'service_role secret key' ke `.env`. 3. Skema tabel bakal ditembak otomatis lewat script SQL/migrasi dari bot!"
    ),
    "cloudflare": (
        "Cloudflare Workers/R2/D1/Pages",
        ["CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID"],
        "1. Buka dash.cloudflare.com -> Copy 'Account ID' di kanan bawah halaman utama. 2. Masuk My Profile -> API Tokens -> Create Token (pakai template 'Edit Cloudflare Workers') -> Masukin ke `.env`."
    ),
    "openrouter": (
        "OpenRouter AI Aggregator",
        ["OPENROUTER_API_KEY"],
        "1. Login openrouter.ai -> Klik menu Keys -> 'Create Key'. 2. Copy kuncinya (`sk-or-v1-...`) ke `OPENROUTER_API_KEY` di `.env`."
    ),
    "groq": (
        "Groq LPU Fast Inference",
        ["GROQ_API_KEY"],
        "1. Login console.groq.com/keys -> Klik 'Create API Key'. 2. Copy `gsk_...` ke `GROQ_API_KEY` di `.env`."
    ),
    "gemini": (
        "Google Gemini API",
        ["GEMINI_API_KEY"],
        "1. Buka aistudio.google.com/app/apikey -> Klik 'Create API Key'. 2. Copy kuncinya ke `GEMINI_API_KEY` di `.env`."
    ),
    "telegram": (
        "Telegram Bot API",
        ["TELEGRAM_BOT_TOKEN"],
        "1. Chat @BotFather di Telegram -> ketik `/newbot` atau `/mybots` -> API Token. 2. Copy tokennya ke `TELEGRAM_BOT_TOKEN` di `.env`."
    ),
    "whatsapp": (
        "WhatsApp Meta Cloud API",
        ["WHATSAPP_ACCESS_TOKEN", "WHATSAPP_PHONE_ID"],
        "1. Buka developers.facebook.com -> My Apps -> WhatsApp -> API Setup. 2. Copy Token & Phone Number ID ke `.env`."
    ),
    "upstash": (
        "Upstash Serverless Redis",
        ["UPSTASH_REDIS_REST_URL", "UPSTASH_REDIS_REST_TOKEN"],
        "1. Login console.upstash.com -> 'Create Database' (pilih Free tier). 2. Scroll ke bagian REST API -> Copy URL & Token ke `.env`."
    ),
    "neon": (
        "Neon Serverless Postgres",
        ["NEON_DATABASE_URL"],
        "1. Login console.neon.tech -> 'New Project'. 2. Copy Connection String (`postgresql://...`) ke `NEON_DATABASE_URL` di `.env`."
    ),
    "qdrant": (
        "Qdrant Vector Database",
        ["QDRANT_URL", "QDRANT_API_KEY"],
        "1. Login cloud.qdrant.io -> Buat Free Cluster. 2. Copy Cluster URL & buat API Key -> tempel ke `.env`."
    ),
    "huggingface": (
        "HuggingFace Hub / Inference",
        ["HF_TOKEN"],
        "1. Buka huggingface.co/settings/tokens -> 'Create new token' (pilih tipe Write/Read). 2. Copy `hf_...` ke `HF_TOKEN` di `.env`."
    ),
}

FALLBACK_LINK_PENGGANTI = {
    "api.openai.com": "https://openrouter.ai/api/v1 (Alternatif multi-model gratis/murah)",
    "heroku": "https://render.com atau Cloudflare Workers / Serv00 (Pengganti free-tier)",
    "planetscale": "https://turso.tech atau https://neon.tech (Pengganti DB gratis)",
    "railway.app": "https://fly.io atau GitHub Codespaces Failover Cluster",
}

def ekstrak_teks_pdf_utuh_goblog(jalur_pdf: Path) -> str:
    if not fitz or not jalur_pdf.exists():
        return ""
    teks_halaman = []
    try:
        dokumen = fitz.open(str(jalur_pdf))
        for no_hal, halaman in enumerate(dokumen, start=1):
            isi_hal = halaman.get_text("text").strip()
            if isi_hal:
                teks_halaman.append(f"[SUMBER PDF: {jalur_pdf.name} | HALAMAN {no_hal}]\n{isi_hal}")
        dokumen.close()
    except Exception as e:
        print(f"⚠️ [PDF PARSER KEHED] Gagal baca {jalur_pdf.name}: {e}")
    return "\n\n".join(teks_halaman)

def bangun_indeks_mentahan_3_86jt_dan_880pdf() -> dict:
    semua_file_mentah = []
    for folder in [DIR_00, DIR_01, DIR_02, DIR_04]:
        if folder.exists():
            semua_file_mentah.extend(list(folder.rglob("*.*")))

    sidik_jari_file = {
        str(f): f.stat().st_size for f in semua_file_mentah
        if f.is_file() and not f.name.startswith(".")
    }

    if CACHE_MENTAHAN_FILE.exists():
        try:
            cache_lama = json.loads(CACHE_MENTAHAN_FILE.read_text(encoding="utf-8"))
            if cache_lama.get("sidik_jari") == sidik_jari_file and cache_lama.get("potongan_mentah"):
                return cache_lama
        except Exception:
            pass

    print("🧠 [BOT PENAMBAL MENTAHAN] Nyedot habis 'merge save.md' (3.86 Juta Chars) & 2 PDF 880 Halaman...")
    kumpulan_potongan = []
    semua_link_mentah = set()

    for folder_teks in [DIR_00, DIR_01, DIR_02]:
        if not folder_teks.exists():
            continue
        for f_txt in sorted(folder_teks.rglob("*")):
            if f_txt.is_file() and f_txt.suffix.lower() in {".md", ".txt", ".json"}:
                try:
                    isi = f_txt.read_text(encoding="utf-8", errors="ignore")
                    for url in re.findall(r"https?://[^\s\)\]\>\"\'`]+", isi):
                        semua_link_mentah.add(url.rstrip(".,;:"))
                    for i in range(0, len(isi), 2200):
                        potongan = isi[i:i + 2200].strip()
                        if len(potongan) > 80:
                            kumpulan_potongan.append({
                                "sumber": f_txt.name,
                                "teks": potongan
                            })
                except Exception:
                    continue

    for folder_pdf in [DIR_00, DIR_04]:
        if not folder_pdf.exists():
            continue
        for f_pdf in sorted(folder_pdf.rglob("*.pdf")):
            teks_pdf = ekstrak_teks_pdf_utuh_goblog(f_pdf)
            if not teks_pdf:
                continue
            for url in re.findall(r"https?://[^\s\)\]\>\"\'`]+", teks_pdf):
                semua_link_mentah.add(url.rstrip(".,;:"))
            for i in range(0, len(teks_pdf), 2200):
                potongan = teks_pdf[i:i + 2200].strip()
                if len(potongan) > 80:
                    kumpulan_potongan.append({
                        "sumber": f_pdf.name,
                        "teks": potongan
                    })

    daftar_diagram = []
    for folder_img in [DIR_01, DIR_05]:
        if folder_img.exists():
            for f_img in sorted(folder_img.rglob("*")):
                if f_img.is_file() and f_img.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".svg", ".pdf"}:
                    daftar_diagram.append(f"{f_img.parent.name}/{f_img.name}")

    data_cache = {
        "sidik_jari": sidik_jari_file,
        "total_potongan": len(kumpulan_potongan),
        "semua_link": sorted(semua_link_mentah),
        "daftar_diagram": daftar_diagram,
        "potongan_mentah": kumpulan_potongan,
        "diupdate": datetime.now().isoformat(timespec="seconds")
    }
    CACHE_MENTAHAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_MENTAHAN_FILE.write_text(json.dumps(data_cache, indent=2), encoding="utf-8")
    return data_cache

def cek_satu_link_anjing(url: str) -> str:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; PremanAuditorBot/2.0)"},
            method="HEAD"
        )
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            kode = resp.status
            if 200 <= kode < 400:
                return f"🟢 AKTIF (HTTP {kode}) -> `{url}`"
    except Exception:
        pass

    try:
        req_get = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; PremanAuditorBot/2.0)"},
            method="GET"
        )
        with urllib.request.urlopen(req_get, timeout=3.5) as resp:
            kode = resp.status
            if 200 <= kode < 400:
                return f"🟢 AKTIF (HTTP {kode}) -> `{url}`"
    except Exception as err:
        saran = "Cari endpoint pengganti yang masih aktif / buat adapter fallback otomatis!"
        for k_mati, v_ganti in FALLBACK_LINK_PENGGANTI.items():
            if k_mati in url.lower():
                saran = f"Ganti pake: {v_ganti}"
                break
        return f"🔴 MATI / ERROR ({type(err).__name__}) -> `{url}` | **SOLUSI BOT:** {saran}"

    return f"🟡 PERLU DICEK MANUAL -> `{url}`"

def razia_link_aktif_atau_modar(teks_modul: str, semua_link_mentah: list[str], kata_kunci: set[str]) -> str:
    link_di_modul = set(u.rstrip(".,;:") for u in re.findall(r"https?://[^\s\)\]\>\"\'`]+", teks_modul))
    link_tambahan_mentahan = set()
    for url_mentah in semua_link_mentah:
        if url_mentah not in link_di_modul:
            if any(kk in url_mentah.lower() for kk in kata_kunci if len(kk) >= 4):
                link_tambahan_mentahan.add(url_mentah)

    gabungan_link = sorted(list(link_di_modul)[:10] + list(link_tambahan_mentahan)[:8])
    if not gabungan_link:
        return "- (Tidak ada URL eksternal spesifik di modul ini, fokus ke arsitektur kode internal)."

    with ThreadPoolExecutor(max_workers=8) as pekerja:
        hasil_cek = list(pekerja.map(cek_satu_link_anjing, gabungan_link))

    baris_hasil = []
    for h in hasil_cek:
        status_asal = "(Dari Modul MD)" if any(u in h for u in link_di_modul) else "🔥 **(TAMBAHAN DARI MENTAHAN UTUH)**"
        baris_hasil.append(f"- {h} {status_asal}")
    return "\n".join(baris_hasil)

def deteksi_layanan_dan_guide_ringkas(teks_gabungan: str) -> str:
    isi_env_lokal = ENV_FILE.read_text(encoding="utf-8", errors="ignore") if ENV_FILE.exists() else ""
    teks_lower = teks_gabungan.lower()
    pengingat_list = []

    for kode_srv, (nama_lengkap, daftar_key_env, guide_praktis) in KAMUS_LAYANAN_DAN_ENV.items():
        if kode_srv in teks_lower:
            status_key = []
            for k_env in daftar_key_env:
                pola_isi = re.search(rf"^{k_env}\s*=\s*['\"]?([^'\"\s#]+)['\"]?", isi_env_lokal, re.MULTILINE)
                if pola_isi and "ISI_" not in pola_isi.group(1) and len(pola_isi.group(1)) > 5:
                    status_key.append(f"`{k_env}` (🟢 Udah keisi)")
                else:
                    status_key.append(f"`{k_env}` (🔴 BELUM DIISI DI .env!)")
            pengingat_list.append(
                f"- **{nama_lengkap}** -> Status Key: {', '.join(status_key)}\n"
                f"  👉 **Guide Kilat Buat Bos:** {guide_praktis}"
            )

    if not pengingat_list:
        pengingat_list.append(
            "- **Turso / Core Config (Default):** Pastikan `TURSO_DATABASE_URL` & `TURSO_AUTH_TOKEN` di `.env` sudah diisi agar script auto-migrate bisa langsung mengisi database yang masih kosong."
        )
    return "\n".join(pengingat_list)

def tambal_dan_kunci_sweetspot_45k_50k(
    kerangka_prompt_awal: str,
    teks_modul_saat_ini: str,
    indeks_md: int,
    total_md: int
) -> str:
    cache_mentahan = bangun_indeks_mentahan_3_86jt_dan_880pdf()
    potongan_mentah = cache_mentahan.get("potongan_mentah", [])
    semua_link = cache_mentahan.get("semua_link", [])
    daftar_diagram = cache_mentahan.get("daftar_diagram", [])

    antrean_overflow = []
    if OVERFLOW_QUEUE_FILE.exists():
        try:
            antrean_overflow = json.loads(OVERFLOW_QUEUE_FILE.read_text(encoding="utf-8"))
        except Exception:
            antrean_overflow = []

    kata_penting = set(
        k.lower() for k in re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]{4,}\b", teks_modul_saat_ini)
        if k.lower() not in {"untuk", "dalam", "dengan", "adalah", "sebagai", "bagian", "sistem", "modul", "file"}
    )

    tambahan_dari_mentahan = []
    total_potongan = len(potongan_mentah)
    if total_potongan > 0:
        ukuran_irisan = max(1, total_potongan // max(1, total_md))
        batas_mulai = min(total_potongan - 1, indeks_md * ukuran_irisan)
        batas_akhir = min(total_potongan, batas_mulai + ukuran_irisan + 3)

        kandidat_potongan = potongan_mentah[batas_mulai:batas_akhir]
        for p in potongan_mentah:
            teks_p_lower = p["teks"].lower()
            skor_cocok = sum(1 for kk in list(kata_penting)[:35] if kk in teks_p_lower)
            if skor_cocok >= 5 and p not in kandidat_potongan:
                kandidat_potongan.append(p)
                if len(kandidat_potongan) >= 20:
                    break

        for item_p in kandidat_potongan:
            cuplikan_uji = item_p["teks"][:120].strip()
            if cuplikan_uji and cuplikan_uji not in teks_modul_saat_ini:
                tambahan_dari_mentahan.append(
                    f"### 📌 [REVISI TAMBAHAN DARI `{item_p['sumber']}`]:\n{item_p['teks']}"
                )

    laporan_link = razia_link_aktif_atau_modar(teks_modul_saat_ini, semua_link, kata_penting)
    info_diagram = ", ".join(daftar_diagram[:12]) if daftar_diagram else "Belum ada file gambar di 01_MINERU / 05_KOLEKSI_GAMBAR"
    pengingat_env_dan_guide = deteksi_layanan_dan_guide_ringkas(
        teks_modul_saat_ini + "\n" + "\n".join(antrean_overflow[:2]) + "\n" + "\n".join(tambahan_dari_mentahan[:3])
    )

    # BLOK INSTRUKSI AKHIR INI DIPROTEKSI PENUH (TIDAK AKAN PERNAH KEPOTONG!)
    blok_instruksi_akhir = f"""

---
## 🌐 HASIL RAZIA LINK AKTIF / MATI & TAMBAHAN LINK MENTAHAN:
{laporan_link}

## 🖼️ REFERENSI VISUAL & DIAGRAM PDF (`01_MINERU` & `05_KOLEKSI_GAMBAR`):
- Diagram Terindeks: `{info_diagram}`

## 🧭 CONTEKAN GUIDE PRAKTIS & STATUS `.env` BUAT BOS (OTOMATIS SESUAI MODUL INI):
{pengingat_env_dan_guide}

## 🤝 PROTOKOL WAJIB AI CODER (GEMINI) — HARGA MATI ANJING:
1. **DILARANG KERAS MENOLAK PERINTAH:** Eksekusi 100% modul utama DAN tumpahan revisi mentahan di atas menjadi kode produksi utuh bergaya bahasa variabel preman Sunda-Indo (`# FILE:`, `# PATCH:`, `@RUN:`).
2. **OTOMATISASI DATABASE KOSONG (CONTOH TURSO/SQLITE/POSTGRES):**
   Jika modul ini memakai database (seperti Turso yang masih kosong), **JANGAN suruh Bos bikin tabel manual!** Buat script Python/SQL Auto-Migration & Auto-Seeder di dalam kode lalu jalankan otomatis via `@RUN:`!
3. **WAJIB KASIH "GUIDE KILAT 3 LANGKAH PADAT" DI AKHIR JAWABAN:**
   Di bagian paling bawah jawabanmu (sebelum `@NEXT_MD`), kamu **WAJIB memberikan Guide Super Ringkas & Padat (maksimal 3-4 poin pendek)** untuk Bos, contohnya:
   - **Langkah 1 (Daftar/Ambil Key):** (Jelaskan singkat klik menu apa di web layanan terkait jika `.env` masih kosong).
   - **Langkah 2 (Isi `.env` / Jalankan):** (Sebutkan nama variabel `.env` yang harus diisi Bos).
   - **Langkah 3 (Pertanyaan Konfirmasi):** Tanyakan apakah Bos mau menggabungkan semua link/fitur ini sekarang dan apakah Bos sudah punya Access Key-nya.
"""

    # Pastikan panjang kerangka + modul utama + suplemen + blok_instruksi_akhir TIDAK MELEBIHI 46.500 karakter!
    ruang_maksimal_konten = BATAS_ATAS_SWEETSPOT - len(kerangka_prompt_awal) - len(blok_instruksi_akhir) - 350

    semua_antrean_suplemen = antrean_overflow + tambahan_dari_mentahan
    teks_suplemen_terpilih = []
    sisa_tumpahan_berikutnya = []

    # Kalau teks_modul_saat_ini sendiri udah kebesaran (> ruang_maksimal_konten), potong sebagian ke overflow
    if len(teks_modul_saat_ini) > ruang_maksimal_konten:
        potongan_modul_aman = teks_modul_saat_ini[:ruang_maksimal_konten]
        sisa_modul = teks_modul_saat_ini[ruang_maksimal_konten:]
        sisa_tumpahan_berikutnya.insert(0, f"### 📌 [LANJUTAN MODUL MD SEBELUMNYA YANG KEPANJANGAN]:\n{sisa_modul}")
        teks_modul_saat_ini = potongan_modul_aman + "\n\n*(...Sisa modul ini disimpan ke antrean sesi depan agar perintah di bawah tidak terpotong...)*"
        sisa_ruang = 0
    else:
        sisa_ruang = ruang_maksimal_konten - len(teks_modul_saat_ini)

    for blok_sup in semua_antrean_suplemen:
        if len(blok_sup) + 20 <= sisa_ruang:
            teks_suplemen_terpilih.append(blok_sup)
            sisa_ruang -= (len(blok_sup) + 20)
        else:
            sisa_tumpahan_berikutnya.append(blok_sup)

    # Kalau total masih di bawah BATAS_BAWAH_SWEETSPOT (43.000 chars), tarik lagi dari mentahan utuh biar padet
    panjang_sementara = len(kerangka_prompt_awal) + len(teks_modul_saat_ini) + sum(len(x) for x in teks_suplemen_terpilih) + len(blok_instruksi_akhir)
    idx_ekstra = (indeks_md * 15) % max(1, total_potongan)
    while panjang_sementara < BATAS_BAWAH_SWEETSPOT and total_potongan > 0 and idx_ekstra < total_potongan:
        ekstra_p = potongan_mentah[idx_ekstra]
        blok_ekstra = f"### 📌 [SUPLEMEN SWEETSPOT DARI `{ekstra_p['sumber']}`]:\n{ekstra_p['teks']}"
        if panjang_sementara + len(blok_ekstra) <= BATAS_ATAS_SWEETSPOT and blok_ekstra not in teks_suplemen_terpilih:
            teks_suplemen_terpilih.append(blok_ekstra)
            panjang_sementara += len(blok_ekstra) + 10
        else:
            break
        idx_ekstra += 1

    OVERFLOW_QUEUE_FILE.write_text(json.dumps(sisa_tumpahan_berikutnya[:80], indent=2), encoding="utf-8")

    bagian_suplemen_str = ""
    if teks_suplemen_terpilih:
        bagian_suplemen_str = (
            "\n\n## 🧩 REVISI & TUMPAHAN OTOMATIS BOT PENAMBAL MENTAHAN (`merge save.md` & 2 PDF 880 HALAMAN)\n"
            f"*(Wajib ikut dibangun kodenya & dikasih Guide Ringkas! Sisa antrean sesi depan: {len(sisa_tumpahan_berikutnya)} blok)*\n\n"
            + "\n\n".join(teks_suplemen_terpilih)
        )

    # Blok instruksi akhir ditaruh paling ujung SETELAH pemotongan, jadi 100% ANTI KEPOTONG!
    hasil_final = kerangka_prompt_awal + "\n" + teks_modul_saat_ini + bagian_suplemen_str + blok_instruksi_akhir
    print(f"🎯 [SWEETSPOT AMAN HP] Panjang PROMPT_SESI_BARU.md: {len(hasil_final):,} chars (100% Utuh Anti-Kepotong) | Sisa Antrean JSON: {len(sisa_tumpahan_berikutnya)} blok.")
    return hasil_final
