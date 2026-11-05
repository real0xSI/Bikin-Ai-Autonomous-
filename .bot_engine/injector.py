import re
from pathlib import Path

FILE_KERAMAT_JANGAN_DISENTUH_GOBLOG = {
    "auto_repo_bot.py",
    "injector.py",
    "auditor.py",
    "healer.py",
    "sorter.py",
    "enricher.py",
}

POLA_HEADER_FILE = re.compile(
    r"^\s*(?:#|//|--|/\*)\s*(FILE|PATH|FILEPATH|APPEND|PATCH)\s*:\s*([a-zA-Z0-9_./-]+)",
    re.IGNORECASE,
)
POLA_PAGAR_MD = re.compile(r"^\s*\x60{3}[a-zA-Z0-9_-]*\s*$")

def _simpan_satu_file_preman(target_path: str, mode: str, baris_kode: list[str]) -> str | None:
    # Bersihkan pagar ``` di paling atas atau paling bawah blok kode jika ikut terbawa
    while baris_kode and POLA_PAGAR_MD.match(baris_kode[0]):
        baris_kode.pop(0)
    while baris_kode and POLA_PAGAR_MD.match(baris_kode[-1]):
        baris_kode.pop()

    jalur_bersih = Path(target_path.strip().lstrip("/"))
    if jalur_bersih.name in FILE_KERAMAT_JANGAN_DISENTUH_GOBLOG:
        return None

    jalur_bersih.parent.mkdir(parents=True, exist_ok=True)
    jeroan_kode = "\n".join(baris_kode).strip("\n") + "\n"

    if mode == "APPEND" and jalur_bersih.exists():
        with open(jalur_bersih, "a", encoding="utf-8") as f_asu:
            f_asu.write("\n" + jeroan_kode)
        label_mode = "SAMBUNG_BAWAH"
    elif mode == "PATCH" and jalur_bersih.exists():
        teks_asli = jalur_bersih.read_text(encoding="utf-8")
        potongan_tambalan = re.findall(
            r"<<<SEARCH\n(.*?)\n===REPLACE\n(.*?)\n>>>END",
            jeroan_kode,
            re.DOTALL,
        )
        for blok_cari, blok_ganti in potongan_tambalan:
            if blok_cari in teks_asli:
                teks_asli = teks_asli.replace(blok_cari, blok_ganti, 1)
        jalur_bersih.write_text(teks_asli, encoding="utf-8")
        label_mode = "TAMBAL_TENGAH"
    else:
        jalur_bersih.write_text(jeroan_kode, encoding="utf-8")
        label_mode = "TIMPA_TOTAL"

    jml_baris = len(jalur_bersih.read_text(encoding="utf-8", errors="ignore").splitlines())
    print(f"🔥 [{label_mode}] {jalur_bersih} kelar disuntik kehed! (Total: {jml_baris:,} baris)")
    return str(jalur_bersih)

def suntik_kode_preman_kehed(bacotan_ai_md: str) -> list[str]:
    file_diobok_obok = []

    # 1. Bikin folder baru (@MKDIR: path/ke/folder)
    for cocok_dir in re.finditer(r"^@MKDIR:\s*(.+)$", bacotan_ai_md, re.MULTILINE | re.IGNORECASE):
        jalur_kandang = Path(cocok_dir.group(1).strip().lstrip("/"))
        jalur_kandang.mkdir(parents=True, exist_ok=True)
        penjaga = jalur_kandang / ".gitkeep"
        if not any(jalur_kandang.iterdir()):
            penjaga.touch()
        print(f"📁 [BIKIN KANDANG ANJING] {jalur_kandang}/ siap dipake!")

    # 2. Bantai file sampah (@DELETE: path/ke/file)
    for cocok_hapus in re.finditer(r"^@DELETE:\s*(.+)$", bacotan_ai_md, re.MULTILINE | re.IGNORECASE):
        jalur_modar = Path(cocok_hapus.group(1).strip().lstrip("/"))
        if jalur_modar.exists() and jalur_modar.is_file() and jalur_modar.name not in FILE_KERAMAT_JANGAN_DISENTUH_GOBLOG:
            jalur_modar.unlink()
            print(f"🗑️ [BANTAI FILE TAI] {jalur_modar} udah dimusnahkan kehed!")

    # 3. Pemotong Baris-demi-Baris (Kebal copas tanpa backtick & kebal multi-# FILE dalam 1 blok!)
    target_aktif = None
    mode_aktif = "WRITE"
    keranjang_baris = []

    for brs in bacotan_ai_md.splitlines():
        cek_header = POLA_HEADER_FILE.match(brs)
        if cek_header:
            if target_aktif:
                hasil = _simpan_satu_file_preman(target_aktif, mode_aktif, keranjang_baris)
                if hasil and hasil not in file_diobok_obok:
                    file_diobok_obok.append(hasil)
            jenis_tag = cek_header.group(1).upper()
            target_aktif = cek_header.group(2).strip()
            mode_aktif = "APPEND" if "APPEND" in jenis_tag else ("PATCH" if "PATCH" in jenis_tag else "WRITE")
            keranjang_baris = []
            continue

        if target_aktif is not None:
            # Berhenti ngumpulin baris kode kalau ketemu tag komando bot atau akhir blok penjelasan
            if re.match(r"^(@RUN:|@MKDIR:|@DELETE:|@NEXT_MD|##\s+)", brs.strip(), re.IGNORECASE):
                hasil = _simpan_satu_file_preman(target_aktif, mode_aktif, keranjang_baris)
                if hasil and hasil not in file_diobok_obok:
                    file_diobok_obok.append(hasil)
                target_aktif = None
                keranjang_baris = []
            else:
                keranjang_baris.append(brs)

    if target_aktif:
        hasil = _simpan_satu_file_preman(target_aktif, mode_aktif, keranjang_baris)
        if hasil and hasil not in file_diobok_obok:
            file_diobok_obok.append(hasil)

    return file_diobok_obok
