import re
import subprocess
from pathlib import Path

KANDANG_LOG = Path("logs")

def gebug_terminal_jeung_cek_modar(bacotan_ai_md: str) -> tuple[list[str], str, bool]:
    perintah_dieksekusi_anjing = []
    kumpulan_output_bacot = []
    ada_yang_modar_goblog = False

    for cocok_cmd in re.finditer(r"^@RUN:\s*(.+)$", bacotan_ai_md, re.MULTILINE | re.IGNORECASE):
        perintah_sia = cocok_cmd.group(1).strip()
        print(f"⚙️ [GEBUG TERMINAL KEHED] Njalanin: {perintah_sia}")
        try:
            hasil_gebug = subprocess.run(perintah_sia, shell=True, capture_output=True, text=True, timeout=180)
            perintah_dieksekusi_anjing.append(perintah_sia)
            if hasil_gebug.returncode != 0:
                ada_yang_modar_goblog = True
                status_bacot = f"❌ MODAR GOBLOG (Exit Code {hasil_gebug.returncode}) -> WAJIB SELF-HEALING SIA!"
            else:
                status_bacot = "✅ TEMBUS ANJING (Exit Code 0)"

            potongan_stdout = hasil_gebug.stdout.strip()[-400:] if hasil_gebug.stdout else "(kosong melompong)"
            potongan_stderr = hasil_gebug.stderr.strip()[-700:] if hasil_gebug.stderr else "(aman gak ada error tai)"
            kumpulan_output_bacot.append(
                f"$ {perintah_sia}\nStatus: {status_bacot}\nSTDOUT:\n{potongan_stdout}\nSTDERR:\n{potongan_stderr}"
            )
        except Exception as err_bangsat:
            ada_yang_modar_goblog = True
            kumpulan_output_bacot.append(f"$ {perintah_sia}\nStatus: ❌ MELEDAK EXCEPTION ANJING -> {str(err_bangsat)}")

    return perintah_dieksekusi_anjing, "\n---\n".join(kumpulan_output_bacot), ada_yang_modar_goblog

def intip_log_analitik_bangsat() -> str:
    if not KANDANG_LOG.exists():
        return "Belum ada folder `logs/` kehed."

    deretan_file_log = sorted(KANDANG_LOG.glob("*.*"))
    if not deretan_file_log:
        return "Folder `logs/` masih kosong melompong goblog."

    rangkuman_log_tai = []
    for f_log in deretan_file_log[-4:]:
        try:
            baris_log = f_log.read_text(encoding="utf-8", errors="ignore").splitlines()
            baris_penting_anjing = [
                ln for ln in baris_log
                if any(k in ln.upper() for k in ("ERROR", "CRITICAL", "MODAR", "GOBLOG", "HEAL", "HOTSWAP", "FAILOVER", "TURSO"))
            ]
            pilihan_baris = baris_penting_anjing[-10:] if baris_penting_anjing else baris_log[-6:]
            rangkuman_log_tai.append(f"[{f_log.name}]\n" + "\n".join(pilihan_baris))
        except Exception:
            continue

    return "\n\n".join(rangkuman_log_tai)[:2000]
