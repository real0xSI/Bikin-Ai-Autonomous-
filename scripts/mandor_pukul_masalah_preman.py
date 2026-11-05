#!/usr/bin/env python3
"""
Bot Mandor Darurat (Universal Auto-Healer)
Tugasnya nangkep error apapun (mau sepele atau berat), mikir pake AI, 
terus nge-generate dan jalanin patch/perintah buat ngebantai masalahnya!
"""
import os
import time
import subprocess
from typing import Optional

# Pake provider yang udah ada di sistem lu (fallback ke lokal kalo cloud modar)
try:
    from src.core_ai.providers_dan_budget_preman import AgentRouter
    router_preman = AgentRouter()
except ImportError:
    router_preman = None

def cek_sistem_goblog() -> Optional[str]:
    """Cari tau apa ada error atau proses yang modar."""
    try:
        # Contoh: ngecek status docker, git, atau error log terakhir
        hasil = subprocess.run(["journalctl", "-n", "20", "--no-pager", "-p", "3"], capture_output=True, text=True)
        if hasil.stdout.strip():
            return hasil.stdout[-500:] # Ambil buntut errornya aja
        return None
    except Exception:
        return "Gagal baca log anjing, butuh inspeksi manual."

async def hajar_pake_ai_kehed(pesan_error: str) -> None:
    """Nanya ke AI buat nyari bash command buat beresin errornya."""
    if not router_preman:
        print("⚠️ [MANDOR-PREMAN] Router AI kaga nyambung, aing pusing sendiri!")
        return

    prompt_sangar = (
        f"Bos nemu error ini:\n{pesan_error}\n"
        "Lu kan AI pinter, kasih gue command BASH murni (tanpa bacot, tanpa markdown) "
        "buat ngebenerin atau bypass ini masalah sekarang juga anjing!"
    )
    
    try:
        print("🧠 [MANDOR-PREMAN] Lagi mikir keras nyari wangsit buat benerin...")
        solusi = await router_preman.eksekusi_prompt_agent_sia(
            agent_id="agent_003_sweeper",
            messages=[{"role": "user", "content": prompt_sangar}],
            pilihan_provider="openai",
            model="gpt-4o-mini"
        )
        
        command_bersih = solusi["content"].replace("```bash", "").replace("```", "").strip()
        print(f"🔥 [MANDOR-PREMAN] Dapet wangsit! Ngeksekusi: {command_bersih[:50]}...")
        
        # Eksekusi command dari AI (Hati-hati, ini preman beneran!)
        subprocess.run(command_bersih, shell=True, check=False)
        print("✅ [MANDOR-PREMAN] Masalah udah aing bantai!")
        
    except Exception as e:
        print(f"💀 [MANDOR-PREMAN] AI-nya ikutan modar kehed: {e}")

def patroli_keliling_24jam() -> None:
    """Jalan terus nyari ribut sama error."""
    import asyncio
    print("🚬 [MANDOR-PREMAN] Mandor udah turun gunung. Siap ngebantai problem apapun...")
    while True:
        error_nemu = cek_sistem_goblog()
        if error_nemu:
            print("🚨 [MANDOR-PREMAN] Woy ada yang error anjing! Sini aing urus!")
            asyncio.run(hajar_pake_ai_kehed(error_nemu))
        else:
            print("💤 [MANDOR-PREMAN] Kondisi aman, markas tentram, ngudud dulu...")
        
        time.sleep(300) # Cek tiap 5 menit

if __name__ == "__main__":
    patroli_keliling_24jam()
