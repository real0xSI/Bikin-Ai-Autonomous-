#!/usr/bin/env python3
"""
Bot Tukang Sapu Preman (Auto-Fixer Linter)
Kerjanya ngeberesin linter markdown & python yang bawel anjing.
Biar mata lu ga sepet liat 500+ problems di VSCode goblog.
"""
import time
import subprocess

def sikat_markdown_goblog() -> None:
    """Ngebantai error MD022, MD026, dll pake auto-fixer npx markdownlint-cli."""
    print("🧹 [TUKANG-SAPU] Ngepel markdown yang berantakan kehed...")
    try:
        # Install linter diem-diem kalo belum ada
        subprocess.run(["npm", "install", "-g", "markdownlint-cli"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Hajar auto-fix ke semua file .md
        subprocess.run(["markdownlint-cli", "--fix", "**/*.md"], check=False)
    except Exception as galat:
        print(f"⚠️ [TUKANG-SAPU] Gagal ngepel markdown sia: {galat}")

def sikat_python_bangsat() -> None:
    """Nge-fix kode Python biar kaga diomelin linter Ruff."""
    print("🧹 [TUKANG-SAPU] Rapiin kode Python pake Ruff anjing...")
    try:
        subprocess.run(["python3", "-m", "pip", "install", "-q", "ruff"], check=False)
        subprocess.run(["python3", "-m", "ruff", "check", "--fix", "."], stdout=subprocess.DEVNULL, check=False)
        subprocess.run(["python3", "-m", "ruff", "format", "."], stdout=subprocess.DEVNULL, check=False)
    except Exception as galat:
        print(f"⚠️ [TUKANG-SAPU] Gagal ngepel python anjing: {galat}")

def jaga_lilin_24jam() -> None:
    """Looping abadi, nongkrong 24 jam benerin spasi & typo linter."""
    print("🚬 [TUKANG-SAPU] Bot preman linter mulai nongkrong 24 jam...")
    while True:
        sikat_markdown_goblog()
        sikat_python_bangsat()
        print("💤 [TUKANG-SAPU] Beres ngepel, ngudud dulu 10 menit sebelum ronde maut selanjutnya...")
        time.sleep(600)  # Tidur 10 menit (600 detik) biar CPU lu kaga modar

if __name__ == "__main__":
    jaga_lilin_24jam()
