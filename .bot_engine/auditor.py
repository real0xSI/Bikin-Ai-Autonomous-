import os
import re
import json
from pathlib import Path
from datetime import datetime

MARKAS_BLUEPRINT = Path("_sumber_blueprint")
DIR_00_MENTAHAN = MARKAS_BLUEPRINT / "00_MENTAHAN_UTUH_3_86JUTA_MD_DAN_PDF"
DIR_01_MINERU = MARKAS_BLUEPRINT / "01_MINERU_RAW_DAN_GAMBAR"
DIR_02_MASTER = MARKAS_BLUEPRINT / "02_MASTER_1_SAMPAI_3_FILE_SWEETSPOT_45K"
DIR_03_MODUL_175 = MARKAS_BLUEPRINT / "03_MODUL_MD_MURNI_MAKS_45K_CHARS"
DIR_04_PDF_20HAL = MARKAS_BLUEPRINT / "04_MODUL_PDF_MURNI_MAKS_20_HALAMAN"
DIR_05_GAMBAR = MARKAS_BLUEPRINT / "05_KOLEKSI_GAMBAR_DIAGRAM_PDF"

FILE_LAPORAN_RAZIA = Path("AUDIT_IDE_MENTAHAN.md")
FILE_DAFTAR_PREMAN_AGENT = Path("agent_registry.json")

FOLDER_CUEKIN_AJG = {
    ".git", ".devcontainer", ".bot_engine", ".bot_history_inbox",
    "_sumber_blueprint", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".next"
}

PILAR_INTI_HARGA_MATI = [
    "turso", "libsql", "hotswap", "hot_swap", "failover", "key_rotation",
    "self_healing", "healing_loop", "aggregator", "orchestrator",
    "telemetry", "analytics", "circuit_breaker", "rate_limit", "webhook"
]

FILE_SKIP_KEHED = {
    "inbox_ai.md", "PROMPT_SESI_BARU.md", "auto_repo_bot.py",
    "project_state.json", "AUDIT_IDE_MENTAHAN.md", "agent_registry.json"
}

def hitung_stok_blueprint_di_kandang() -> dict:
    return {
        "00_MENTAHAN_UTUH (Target: 3 file [1 MD + 2 PDF 880 Hal])": len([p for p in DIR_00_MENTAHAN.glob("*") if p.name != ".gitkeep"]),
        "01_MINERU_RAW_DAN_GAMBAR (Target: 5 item)": len([p for p in DIR_01_MINERU.glob("*") if p.name != ".gitkeep"]),
        "02_MASTER_SWEETSPOT_45K (Target: 6 item)": len([p for p in DIR_02_MASTER.glob("*") if p.name != ".gitkeep"]),
        "03_MODUL_MD_MURNI_45K (Target: 175 file)": len(list(DIR_03_MODUL_175.glob("*.md"))),
        "04_MODUL_PDF_MAKS_20_HAL (Target: 47 file)": len(list(DIR_04_PDF_20HAL.glob("*.pdf"))),
        "05_KOLEKSI_GAMBAR_DIAGRAM (Target: 52 file)": len([p for p in DIR_05_GAMBAR.glob("*") if p.name != ".gitkeep"]),
    }

def razia_repo_jeung_agent_anjing() -> tuple[list[str], int, dict, str]:
    peta_file_goblog = []
    total_baris_kode_aing = 0
    kumpulan_kode_kecil_semua = []

    if FILE_DAFTAR_PREMAN_AGENT.exists():
        try:
            buku_besar_agent = json.loads(FILE_DAFTAR_PREMAN_AGENT.read_text(encoding="utf-8"))
        except Exception:
            buku_besar_agent = {"target_pasukan_agent": 177, "pasukan_agent_aktif": {}, "pilar_berdiri": []}
    else:
        buku_besar_agent = {"target_pasukan_agent": 177, "pasukan_agent_aktif": {}, "pilar_berdiri": []}

    pola_fungsi_kelas = re.compile(
        r"^(?:async\s+def|def|class|export\s+(?:default\s+)?(?:async\s+)?(?:function|class|const|interface))\s+([a-zA-Z0-9_]+)"
    )

    for akar, sub_folders, deretan_file in os.walk("."):
        sub_folders[:] = sorted([d for d in sub_folders if d not in FOLDER_CUEKIN_AJG])
        for nama_f in sorted(deretan_file):
            if nama_f in FILE_SKIP_KEHED or nama_f.startswith("."):
                continue
            lokasi_f = Path(akar) / nama_f
            jalur_relatif = str(lokasi_f).lstrip("./")
            try:
                isi_teks_sia = lokasi_f.read_text(encoding="utf-8", errors="ignore")
                baris_teks = isi_teks_sia.splitlines()
                jml_baris = len(baris_teks)
            except Exception:
                continue

            total_baris_kode_aing += jml_baris
            kumpulan_kode_kecil_semua.append(isi_teks_sia.lower())

            simbol_ditemukan = []
            for brs in baris_teks:
                cocok_simbol = pola_fungsi_kelas.match(brs.strip())
                if cocok_simbol:
                    simbol_ditemukan.append(cocok_simbol.group(1))

            if "agent" in jalur_relatif.lower() or any("agent" in s.lower() for s in simbol_ditemukan):
                buku_besar_agent.setdefault("pasukan_agent_aktif", {})[jalur_relatif] = {
                    "baris_kode": jml_baris,
                    "fungsi_preman": simbol_ditemukan[:10],
                    "diupdate_kapan": datetime.now().isoformat(timespec="seconds")
                }

            info_simbol = f" -> `{', '.join(simbol_ditemukan[:6])}`" if simbol_ditemukan else ""
            peta_file_goblog.append(f"- `{jalur_relatif}` ({jml_baris} baris){info_simbol}")

    gabungan_kode_lower = "\n".join(kumpulan_kode_kecil_semua)
    buku_besar_agent["pilar_berdiri"] = [p for p in PILAR_INTI_HARGA_MATI if p in gabungan_kode_lower]
    FILE_DAFTAR_PREMAN_AGENT.write_text(json.dumps(buku_besar_agent, indent=2), encoding="utf-8")

    return peta_file_goblog, total_baris_kode_aing, buku_besar_agent, gabungan_kode_lower

def audit_mentahan_vs_kode_kehed(gabungan_kode_lower: str) -> str:
    sumber_mentahan_aing = (
        list(DIR_00_MENTAHAN.rglob("*.md")) +
        list(DIR_00_MENTAHAN.rglob("*.txt")) +
        list(DIR_01_MINERU.rglob("*.md")) +
        list(DIR_02_MASTER.rglob("*.md")) +
        list(DIR_03_MODUL_175.rglob("*.md"))
    )

    komponen_belum_digarap_anjing = []
    pilar_ompong_goblog = [p for p in PILAR_INTI_HARGA_MATI if p not in gabungan_kode_lower]

    pola_komponen = re.compile(
        r"\b([A-Z][A-Za-z0-9_]{3,}(?:Agent|Router|Adapter|Provider|Engine|Worker|Swapper|Healer|Service|Controller|Dashboard))\b"
    )

    for file_mentah in sumber_mentahan_aing:
        try:
            isi_mentah = file_mentah.read_text(encoding="utf-8", errors="ignore")
            temuan_komponen = set(pola_komponen.findall(isi_mentah))
            for komp in temuan_komponen:
                if komp.lower() not in gabungan_kode_lower:
                    komponen_belum_digarap_anjing.append(f"`{komp}` (nyangkut di `{file_mentah.name}`)")
        except Exception:
            continue

    unik_belum_digarap = sorted(set(komponen_belum_digarap_anjing))
    stok_kandang = hitung_stok_blueprint_di_kandang()
    baris_stok = [f"- **{k}:** {v} item masuk" for k, v in stok_kandang.items()]

    baris_laporan_audit = [
        "# 🔍 RAZIA IDE MENTAHAN (3.86 JUTA CHARS & 880 HAL PDF) vs KODE PREMAN AKTIF",
        f"Dirazia otomatis pada: {datetime.now().isoformat(timespec='seconds')}\n",
        "## 📦 0. Status Isi Kandang `_sumber_blueprint/` Saat Ini:",
        *baris_stok,
        "\n## 🛠️ 1. Status Pilar Infrastruktur (Turso, Hot-Swap, Self-Healing, Analitik):",
        f"- **Pilar yang Belum Nongol di Kode Goblog:** {', '.join(pilar_ompong_goblog) if pilar_ompong_goblog else 'MANTAP ANJING! Semua pilar inti udah berdiri!'}",
        "\n## 📋 2. Daftar Modul / Agent di Mentahan yang Belum Dibikin Kodenya:"
    ]
    if unik_belum_digarap:
        baris_laporan_audit.extend([f"- [ ] {item}" for item in unik_belum_digarap[:100]])
    else:
        baris_laporan_audit.append("- ⚠️ Kandang `_sumber_blueprint/` masih kosong melompong atau semua komponen udah kelar digarap kehed!")

    FILE_LAPORAN_RAZIA.write_text("\n".join(baris_laporan_audit), encoding="utf-8")

    ringkasan_bacot = []
    if pilar_ompong_goblog:
        ringkasan_bacot.append(f"- Pilar Infrastruktur Belum Nongol: `{', '.join(pilar_ompong_goblog)}`")
    if unik_belum_digarap:
        ringkasan_bacot.append("- Sampel Komponen Mentahan Belum Digarap: " + ", ".join(unik_belum_digarap[:12]))
    return "\n".join(ringkasan_bacot) if ringkasan_bacot else "Semua komponen blueprint yang terdeteksi udah sinkron atau nunggu kiriman file dari Colab."
