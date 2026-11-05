#!/usr/bin/env bash
# Script Pengawal 3 Bot Otonom Preman (Anti-Mati & Anti-Dobel)
MARKAS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$MARKAS_DIR" || exit 0
mkdir -p logs scripts

# 1. Watcher Inbox AI (Cek setiap 2 detik)
if ! pgrep -f "watcher_inbox_preman" > /dev/null 2>&1; then
    nohup bash -c '
        # Label unik: watcher_inbox_preman
        while true; do
            if [ -s inbox_ai.md ]; then
                python3 auto_repo_bot.py
            fi
            sleep 2
        done
    ' -- watcher_inbox_preman > logs/watcher_inbox.log 2>&1 &
fi

# 2. Bot Tukang Sapu Linter (Jika filenya sudah ada)
if [ -f "scripts/bot_tukang_sapu_preman.py" ] && ! pgrep -f "scripts/bot_tukang_sapu_preman.py" > /dev/null 2>&1; then
    nohup python3 scripts/bot_tukang_sapu_preman.py > logs/tukang_sapu.log 2>&1 &
fi

# 3. Bot Mandor Pukul Masalah (Jika filenya sudah ada)
if [ -f "scripts/mandor_pukul_masalah_preman.py" ] && ! pgrep -f "scripts/mandor_pukul_masalah_preman.py" > /dev/null 2>&1; then
    nohup python3 scripts/mandor_pukul_masalah_preman.py > logs/mandor_masalah.log 2>&1 &
fi
