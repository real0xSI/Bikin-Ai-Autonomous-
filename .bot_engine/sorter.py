import shutil
from pathlib import Path

MARKAS_BLUEPRINT = Path("_sumber_blueprint")
KANDANG_TARGET = {
    "00_MENTAHAN_UTUH_3_86JUTA_MD_DAN_PDF": MARKAS_BLUEPRINT / "00_MENTAHAN_UTUH_3_86JUTA_MD_DAN_PDF",
    "01_MINERU_RAW_DAN_GAMBAR": MARKAS_BLUEPRINT / "01_MINERU_RAW_DAN_GAMBAR",
    "02_MASTER_1_SAMPAI_3_FILE_SWEETSPOT_45K": MARKAS_BLUEPRINT / "02_MASTER_1_SAMPAI_3_FILE_SWEETSPOT_45K",
    "03_MODUL_MD_MURNI_MAKS_45K_CHARS": MARKAS_BLUEPRINT / "03_MODUL_MD_MURNI_MAKS_45K_CHARS",
    "04_MODUL_PDF_MURNI_MAKS_20_HALAMAN": MARKAS_BLUEPRINT / "04_MODUL_PDF_MURNI_MAKS_20_HALAMAN",
    "05_KOLEKSI_GAMBAR_DIAGRAM_PDF": MARKAS_BLUEPRINT / "05_KOLEKSI_GAMBAR_DIAGRAM_PDF",
}

def rapihin_barang_kiriman_colab_goblog() -> int:
    """Nyeret folder yang nyasar di luar supaya masuk ke dalam _sumber_blueprint/ secara otomatis."""
    jumlah_digeser = 0
    for nama_kandang, lokasi_asli in KANDANG_TARGET.items():
        lokasi_asli.mkdir(parents=True, exist_ok=True)
        # Kalau ada folder bernama sama nyasar di root repo, seret isinya ke _sumber_blueprint
        nyasar_di_luar = Path(nama_kandang)
        if nyasar_di_luar.exists() and nyasar_di_luar.is_dir():
            for barang_tai in nyasar_di_luar.iterdir():
                tujuan_anjing = lokasi_asli / barang_tai.name
                if tujuan_anjing.exists():
                    if tujuan_anjing.is_dir():
                        shutil.rmtree(tujuan_anjing)
                    else:
                        tujuan_anjing.unlink()
                shutil.move(str(barang_tai), str(tujuan_anjing))
                jumlah_digeser += 1
            shutil.rmtree(nyasar_di_luar, ignore_errors=True)
            print(f"🚚 [SORTIR ANJING] Folder nyasar '{nama_kandang}' udah diseret masuk ke {lokasi_asli}!")
    return jumlah_digeser
