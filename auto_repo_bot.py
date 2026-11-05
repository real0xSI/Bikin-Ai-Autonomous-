#!/usr/bin/env python3
"""
BOS BESAR ORKESTRATOR MONOREPO PREMAN (auto_repo_bot.py)
Ngatur: Sortir Kiriman Colab, Penambal Mentahan (merge save.md & 2 PDF 880 Hal),
Sweetspot 45K-50K, Razia Link Aktif, 177 Agent, Self-Healing, & Git Sync.
"""
import sys
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime

MARKAS_UTAMA_AING = Path(__file__).resolve().parent
sys.path.insert(0, str(MARKAS_UTAMA_AING / ".bot_engine"))

from sorter import rapihin_barang_kiriman_colab_goblog
from injector import suntik_kode_preman_kehed
from auditor import (
    DIR_03_MODUL_175,
    hitung_stok_blueprint_di_kandang,
    razia_repo_jeung_agent_anjing,
    audit_mentahan_vs_kode_kehed,
)
from healer import gebug_terminal_jeung_cek_modar, intip_log_analitik_bangsat
from enricher import tambal_dan_kunci_sweetspot_45k_50k

KOTAK_MASUK_AI = Path("inbox_ai.md")
FILE_STATUS_PROYEK = Path("project_state.json")
FILE_UMPAN_SESI_BARU = Path("PROMPT_SESI_BARU.md")
GUDANG_ARSIP_INBOX = Path(".bot_history_inbox")
PAGAR_KODE = "\x60" * 3

def siapkan_status_awal_goblog() -> dict:
    GUDANG_ARSIP_INBOX.mkdir(parents=True, exist_ok=True)
    if not FILE_STATUS_PROYEK.exists():
        status_bawaan_aing = {
            "sesi_ke_berapa_anjing": 0,
            "indeks_md_sekarang": 0,
            "daftar_md_kelar_digarap": [],
            "butuh_self_healing_darurat": False,
            "bacotan_terminal_terakhir": "Belum ada perintah terminal yang dijalankan kehed.",
            "terakhir_dioprek": datetime.now().isoformat(timespec="seconds")
        }
        FILE_STATUS_PROYEK.write_text(json.dumps(status_bawaan_aing, indent=2), encoding="utf-8")
    return json.loads(FILE_STATUS_PROYEK.read_text(encoding="utf-8"))

def rakit_umpan_sesi_baru_preman(status_proyek: dict) -> None:
    rapihin_barang_kiriman_colab_goblog()
    peta_repo, total_baris, buku_agent, gabungan_kode = razia_repo_jeung_agent_anjing()
    laporan_celah_mentahan = audit_mentahan_vs_kode_kehed(gabungan_kode)
    telemetri_hidup = intip_log_analitik_bangsat()
    stok_kandang = hitung_stok_blueprint_di_kandang()

    daftar_file_md = sorted(DIR_03_MODUL_175.glob("*.md"))
    idx_sekarang = status_proyek.get("indeks_md_sekarang", 0)
    total_md_tersedia = len(daftar_file_md)

    if status_proyek.get("butuh_self_healing_darurat"):
        judul_tugas_sia = "## 🚨 MODE DARURAT SELF-HEALING ANJING: Benerin Error Sebelumnya Goblog!"
        isi_perintah_md = (
            "Perintah `@RUN:` di sesi barusan MODAR (cek bagian LOG TERMINAL TERAKHIR di atas kehed!). "
            "Bedah penyebab error bangsat itu, tambal kodenya pake `# FILE:` atau `# PATCH:` dengan gaya bahasa variabel preman aing, "
            "terus tes ulang pake `@RUN:` sampe ijo!"
        )
    elif idx_sekarang < total_md_tersedia:
        target_md_sia = daftar_file_md[idx_sekarang]
        judul_tugas_sia = f"## 🎯 GARAP MODUL KE-{idx_sekarang + 1} DARI {total_md_tersedia}: `{target_md_sia.name}`"
        isi_perintah_md = target_md_sia.read_text(encoding="utf-8", errors="ignore")
    else:
        judul_tugas_sia = "## 🔍 FASE EKSEKUSI MENTAHAN UTUH (`merge save.md` & 2 PDF 880 HALAMAN)"
        isi_perintah_md = (
            "Bangun dan lengkapi seluruh modul/agen dari suplemen `merge save.md`, `686+tambahan-Copy.pdf`, "
            "dan `Gabungan PDF All.pdf` yang tertera di bawah ini tanpa ada 1 fitur pun yang terlewat!"
        )

    jml_agent_aktif = len(buku_agent.get("pasukan_agent_aktif", {}))
    pilar_aktif_str = ", ".join(buku_agent.get("pilar_berdiri", [])) or "Belum ada satupun goblog"
    peta_repo_str = "\n".join(peta_repo[:60]) if peta_repo else "- (Repo masih perawan, sikat bangun fondasi awal sekarang juga!)"
    if len(peta_repo) > 60:
        peta_repo_str += f"\n- ... ditambah {len(peta_repo) - 60} file preman lainnya."

    ringkasan_stok_str = "\n".join([f"- **{k}:** `{v}`" for k, v in stok_kandang.items()])

    kerangka_awal = "\n".join([
        "# 🚀 KONTEKS HANDOFF SESI BARU — MARKAS BESAR ~177 AGENT (EDISI PREMAN SUNDA-INDO)",
        "Sia adalah Principal AI & Distributed Systems Architect bermental preman jalanan yang ngebangun monorepo raksasa milik aing "
        "(Agregator AI Otonom, ~177 Agent, Multi-Platform Web/API, Hot-Swap Provider, Turso DB, Self-Healing Loop, & Log Analitik).",
        "",
        "## 🤬 ATURAN GAYA BAHASA & PENAMAAN VARIABEL WAJIB (HARGA MATI ANJING!):",
        "1. **PENAMAAN VARIABEL, FUNGSI, PARAMETER & LOG INTERNAL WAJIB PAKE BAHASA GAUL KASAR INDONESIA & SUNDA ALA PREMAN:**",
        "   Gunakan kombinasi nama variabel unik khas aing seperti `data_mentah_goblog`, `koneksi_turso_anjing`, `putar_kunci_kehed()`, `antrean_bangsat`, `status_modar`, `eksekusi_sia`, `payload_tai`, `hitung_kuota_kontol()`, dll.",
        "2. **JANGAN MERUSAK KEY JSON API EKSTERNAL ATAU NAMA LIBRARY RESMI:**",
        "   Untuk nama package import (`fastapi`, `libsql`, `httpx`) dan field standar protokol luar (`Authorization`, `messages`, `model`) tetap ikuti standar supaya gak error, TAPI seluruh variabel lokal, fungsi internal, class helper, komentar kode, dan pesan logger WAJIB berformat preman kasar Sunda-Indo!",
        "",
        "## 🛠️ PROTOKOL OUTPUT WAJIB (SUPAYA DISUNTIK OTOMATIS SAMA `auto_repo_bot.py`):",
        "1. `# FILE: path/ke/file.ext` di baris pertama dalam blok kode -> Bikin atau timpa file.",
        "2. `# APPEND: path/ke/file.ext` di baris pertama dalam blok kode -> Sambung kode baru di buntut file.",
        "3. `# PATCH: path/ke/file.ext` di baris pertama dalam blok kode (`<<<SEARCH`, `===REPLACE`, `>>>END`) -> Tambal bagian spesifik.",
        "4. `@MKDIR: path/folder` di luar blok kode -> Bikin folder baru.",
        "5. `@RUN: perintah_terminal` di luar blok kode -> Gebug test atau health-check.",
        "6. `@NEXT_MD` di baris paling bawah jawaban sia -> Tandai modul MD sekarang udah beres dan lanjut ke MD berikutnya.",
        "",
        "## 📊 STATUS MARKAS PROYEK SAAT INI:",
        f"- **Sesi Preman Ke:** {status_proyek.get('sesi_ke_berapa_anjing', 0) + 1}",
        f"- **Progres 175 File Sweetspot (45K):** {idx_sekarang} / {total_md_tersedia} kelar",
        f"- **Total Baris Kode Produksi:** {total_baris:,} baris",
        f"- **Pasukan Agent Terdaftar:** {jml_agent_aktif} / 177 Agent",
        f"- **Pilar Infrastruktur Berdiri:** {pilar_aktif_str}",
        "",
        "## 📦 ISI GUDANG `_sumber_blueprint/` SAAT INI:",
        ringkasan_stok_str,
        "",
        "## 🗺️ PETA FILE & FUNGSI PREMAN YANG UDAH ADA (ACUAN IMPORT SIA):",
        peta_repo_str,
        "",
        "## 🔍 TEMUAN RAZIA IDE MENTAHAN (3.86 JUTA CHARS & 880 HAL PDF vs KODE):",
        laporan_celah_mentahan,
        "",
        "## 🖥️ LOG TERMINAL / SELF-HEALING TERAKHIR:",
        f"{PAGAR_KODE}text",
        status_proyek.get("bacotan_terminal_terakhir", ""),
        PAGAR_KODE,
        "",
        judul_tugas_sia,
    ])

    # Jalankan Bot Tambahan (Enricher) untuk menambal kekurangan dari merge save.md & 2 PDF 880 halaman tepat di sweetspot 45K-50K!
    prompt_final_sweetspot = tambal_dan_kunci_sweetspot_45k_50k(
        kerangka_awal,
        isi_perintah_md,
        idx_sekarang,
        max(1, total_md_tersedia)
    )

    FILE_UMPAN_SESI_BARU.write_text(prompt_final_sweetspot, encoding="utf-8")
    print(f"📋 [UMPAN SIAP ANJING] Buka '{FILE_UMPAN_SESI_BARU.name}' ({len(prompt_final_sweetspot):,} chars) buat dicopy ke Sesi Chat Baru!")

def dorong_ke_github_goblog(daftar_file_diubah: list[str], nomor_sesi: int) -> None:
    if not daftar_file_diubah:
        return
    try:
        subprocess.run(["git", "pull", "--rebase", "--autostash"], check=False)
        subprocess.run(["git", "add", "."], check=True)
        sampel_f = ", ".join(daftar_file_diubah[:3])
        tambahan_f = f" +{len(daftar_file_diubah) - 3} file lainnya" if len(daftar_file_diubah) > 3 else ""
        pesan_commit_preman = f"🔥 [PREMAN-SESI-{nomor_sesi}] Obok-obok {len(daftar_file_diubah)} file ({sampel_f}{tambahan_f})"
        subprocess.run(["git", "commit", "-m", pesan_commit_preman], check=True)
        subprocess.run(["git", "push"], check=False)
        print(f"📦 [GIT SYNC TEMBUS] Udah masuk GitHub kehed: {pesan_commit_preman}")
    except Exception as err_git:
        print(f"ℹ️ [GIT LOKAL DOANG] Nyangkut di lokal goblog: {err_git}")

def sikat_utama_anjing() -> None:
    status_proyek = siapkan_status_awal_goblog()
    isi_mentah_inbox = KOTAK_MASUK_AI.read_text(encoding="utf-8").strip() if KOTAK_MASUK_AI.exists() else ""

    if len(isi_mentah_inbox) < 10:
        rakit_umpan_sesi_baru_preman(status_proyek)
        return

    file_kena_suntik = suntik_kode_preman_kehed(isi_mentah_inbox)
    cmd_jalan, log_cmd_bacot, ada_error_modar = gebug_terminal_jeung_cek_modar(isi_mentah_inbox)

    if file_kena_suntik or cmd_jalan:
        status_proyek["sesi_ke_berapa_anjing"] = status_proyek.get("sesi_ke_berapa_anjing", 0) + 1
        status_proyek["butuh_self_healing_darurat"] = ada_error_modar
        if log_cmd_bacot:
            status_proyek["bacotan_terminal_terakhir"] = log_cmd_bacot

        if not ada_error_modar and re.search(r"^@NEXT_MD", isi_mentah_inbox, re.MULTILINE | re.IGNORECASE):
            deretan_md = sorted(DIR_03_MODUL_175.glob("*.md"))
            idx_skrg = status_proyek.get("indeks_md_sekarang", 0)
            if idx_skrg < len(deretan_md):
                status_proyek.setdefault("daftar_md_kelar_digarap", []).append(deretan_md[idx_skrg].name)
                status_proyek["indeks_md_sekarang"] = idx_skrg + 1

        status_proyek["terakhir_dioprek"] = datetime.now().isoformat(timespec="seconds")
        FILE_STATUS_PROYEK.write_text(json.dumps(status_proyek, indent=2), encoding="utf-8")

        cap_waktu = datetime.now().strftime("%Y%m%d_%H%M%S")
        (GUDANG_ARSIP_INBOX / f"sesi_{status_proyek['sesi_ke_berapa_anjing']}_{cap_waktu}.md").write_text(isi_mentah_inbox, encoding="utf-8")
        KOTAK_MASUK_AI.write_text("", encoding="utf-8")

        rakit_umpan_sesi_baru_preman(status_proyek)
        dorong_ke_github_goblog(file_kena_suntik, status_proyek["sesi_ke_berapa_anjing"])
        print(f"\n🎉 MANTAP ANJING! SESI {status_proyek['sesi_ke_berapa_anjing']} BERES DIEKSEKUSI TANPA AMPUN!")
    else:
        print("⚠️ Goblog sia! Kagak ada tag # FILE:, # APPEND:, # PATCH:, @MKDIR:, atau @RUN: di dalam inbox_ai.md!")

if __name__ == "__main__":
    sikat_utama_anjing()
