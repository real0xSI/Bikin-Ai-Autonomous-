import re
from pathlib import Path

FILE_KERAMAT_JANGAN_DISENTUH_GOBLOG = {
    "auto_repo_bot.py",
    "injector.py",
    "auditor.py",
    "healer.py",
    "sorter.py", "enricher.py",
}

def suntik_kode_preman_kehed(bacotan_ai_md: str) -> list[str]:
    file_diobok_obok = []

    # 1. Bikin folder baru (@MKDIR: path/ke/folder)
    for cocok_dir in re.finditer(r"^@MKDIR:\s*(.+)$", bacotan_ai_md, re.MULTILINE | re.IGNORECASE):
        jalur_kandang = Path(cocok_dir.group(1).strip().lstrip("/"))
        jalur_kandang.mkdir(parents=True, exist_ok=True)
        penjaga_kandang = jalur_kandang / ".gitkeep"
        if not any(jalur_kandang.iterdir()):
            penjaga_kandang.touch()
        print(f"📁 [BIKIN KANDANG ANJING] {jalur_kandang}/ siap dipake!")

    # 2. Bantai file sampah (@DELETE: path/ke/file)
    for cocok_hapus in re.finditer(r"^@DELETE:\s*(.+)$", bacotan_ai_md, re.MULTILINE | re.IGNORECASE):
        jalur_modar = Path(cocok_hapus.group(1).strip().lstrip("/"))
        if jalur_modar.exists() and jalur_modar.is_file() and jalur_modar.name not in FILE_KERAMAT_JANGAN_DISENTUH_GOBLOG:
            jalur_modar.unlink()
            print(f"🗑️ [BANTAI FILE TAI] {jalur_modar} udah dimusnahkan kehed!")

    # 3. Bedah blok kode (# FILE:, # APPEND:, atau # PATCH:)
    pola_blok_bangsat = re.compile(
        r"\x60{3}[a-zA-Z0-9_-]*(?:\s+(?:filepath:|file:|path:)?\s*([a-zA-Z0-9_./-]+))?\n(.*?)\x60{3}",
        re.DOTALL,
    )

    for tangkapan_asu in pola_blok_bangsat.finditer(bacotan_ai_md):
        jalur_kepala, jeroan_kode_anjing = tangkapan_asu.group(1), tangkapan_asu.group(2)
        target_operasi_sia = jalur_kepala
        mode_eksekusi_goblog = "TIMPA_TOTAL"

        baris_jeroan = jeroan_kode_anjing.splitlines()
        baris_pertama_kehed = baris_jeroan[0].strip() if baris_jeroan else ""

        cek_tag_dalam = re.search(
            r"^(?:#|//|--|/\*)\s*(?:FILE|PATH|FILEPATH|APPEND|PATCH)\s*:\s*([a-zA-Z0-9_./-]+)",
            baris_pertama_kehed,
            re.IGNORECASE,
        )
        if cek_tag_dalam:
            target_operasi_sia = cek_tag_dalam.group(1)
            tag_kapital_anjing = baris_pertama_kehed.upper()
            if "APPEND" in tag_kapital_anjing:
                mode_eksekusi_goblog = "SAMBUNG_BAWAH"
            elif "PATCH" in tag_kapital_anjing:
                mode_eksekusi_goblog = "TAMBAL_TENGAH"
            jeroan_kode_anjing = "\n".join(baris_jeroan[1:]) + ("\n" if jeroan_kode_anjing.endswith("\n") else "")

        if not target_operasi_sia:
            continue

        jalur_bersih_kontol = Path(target_operasi_sia.strip().lstrip("/"))
        if jalur_bersih_kontol.name in FILE_KERAMAT_JANGAN_DISENTUH_GOBLOG:
            continue

        jalur_bersih_kontol.parent.mkdir(parents=True, exist_ok=True)

        if mode_eksekusi_goblog == "SAMBUNG_BAWAH" and jalur_bersih_kontol.exists():
            with open(jalur_bersih_kontol, "a", encoding="utf-8") as f_asu:
                f_asu.write("\n" + jeroan_kode_anjing)
        elif mode_eksekusi_goblog == "TAMBAL_TENGAH" and jalur_bersih_kontol.exists():
            teks_asli_bangsat = jalur_bersih_kontol.read_text(encoding="utf-8")
            potongan_tambalan = re.findall(
                r"<<<SEARCH\n(.*?)\n===REPLACE\n(.*?)\n>>>END",
                jeroan_kode_anjing,
                re.DOTALL,
            )
            for blok_cari_tai, blok_ganti_anjing in potongan_tambalan:
                if blok_cari_tai in teks_asli_bangsat:
                    teks_asli_bangsat = teks_asli_bangsat.replace(blok_cari_tai, blok_ganti_anjing, 1)
            jalur_bersih_kontol.write_text(teks_asli_bangsat, encoding="utf-8")
        else:
            jalur_bersih_kontol.write_text(jeroan_kode_anjing, encoding="utf-8")

        file_diobok_obok.append(str(jalur_bersih_kontol))
        jumlah_baris_anjing = len(jalur_bersih_kontol.read_text(encoding="utf-8", errors="ignore").splitlines())
        print(f"🔥 [{mode_eksekusi_goblog}] {jalur_bersih_kontol} kelar disuntik kehed! (Total: {jumlah_baris_anjing:,} baris)")

    return file_diobok_obok
