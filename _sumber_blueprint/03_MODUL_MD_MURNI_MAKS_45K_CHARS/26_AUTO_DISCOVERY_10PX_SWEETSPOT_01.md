
<!-- [ID:26_AUTO_DISCOVERY_10PX_S001] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_2_STRUKTUR_DAN_VISUAL | Tag Asli: 10PX -->
## Halaman 137

2. Modul Antarmuka Pengguna (UI Components) 
components/Navbar.tsx 
Navigasi atas dengan pendaran kaca (frosted glass), indikator status node, dan tautan langsung 
ke kasir QRIS: 
"use client";​
​
import React from "react";​
import { Sparkles, Terminal, ShieldCheck, Zap } from "lucide-react";​
​
interface NavbarProps {​
  activeTab: string;​
  setActiveTab: (tab: string) => void;​
}​
​
export default function Navbar({ activeTab, setActiveTab }: NavbarProps) {​
  return (​
    <header className="sticky top-0 z-50 w-full border-b border-white/10 bg-[#030712]/80 
backdrop-blur-xl">​
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">​
        <div className="flex items-center gap-3">​
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br 
from-cyan-400 via-blue-600 to-indigo-700 shadow-lg shadow-cyan-500/25">​
            <Sparkles className="h-5 w-5 text-slate-950" />​
          </div>​
          <div>​
            <div className="flex items-center gap-2">​
              <span className="text-lg font-bold tracking-tight text-white">​
                AETHER<span className="text-cyan-400">OS</span>​
              </span>​
              <span className="rounded-md border border-cyan-500/30 bg-cyan-500/10 px-1.5 
py-0.5 text-[10px] font-mono text-cyan-300">​
                v3.0.8-PROD​
              </span>​
            </div>​
            <p className="text-[10px] text-slate-400">Autonomous Multi-Path Supercluster</p>​
          </div>​
        </div>​
​
        <nav className="hidden md:flex items-center gap-1 rounded-xl border border-white/10 
bg-white/5 p-1">​
          {[​
            { id: "studio", label: "Studio Studio", icon: Sparkles },​
            { id: "health", label: "Provider Health", icon: Zap },​
            { id: "finops", label: "FinOps 95% Margin", icon: ShieldCheck },​
            { id: "radar", label: "GitHub Scout Radar", icon: Terminal },​



<!-- [ID:26_AUTO_DISCOVERY_10PX_S002] SUMBER: PDF:686+tambahan-Copy.pdf | GRADE: PRIORITAS_3_LOGIKA_DAN_NARASI_FITUR | Tag Asli: 10PX -->
## Halaman 145

​
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">​
        {nodes.map((node, idx) => (​
          <div​
            key={idx}​
            className="rounded-xl border border-white/10 bg-slate-900/40 p-4 backdrop-blur-md 
hover:border-cyan-500/30 transition-all"​
          >​
            <div className="flex items-start justify-between">​
              <div>​
                <span className="text-[10px] font-mono text-cyan-400 uppercase 
tracking-wider">{node.category}</span>​
                <h3 className="text-sm font-semibold text-slate-100 mt-0.5">{node.name}</h3>​
              </div>​
              <span​
                className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] 
font-mono font-medium ${​
                  node.status === "ONLINE"​
                    ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"​
                    : "bg-amber-500/10 text-amber-400 border border-amber-500/20"​
                }`}​
              >​
                {node.status === "ONLINE" ? <CheckCircle2 className="h-3 w-3" /> : <AlertTriangle 
className="h-3 w-3" />}​
                {node.status}​
              </span>​
            </div>​
​
            <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between 
text-xs font-mono">​
              <span className="text-slate-400">{node.quota}</span>​
              <span className={`${node.latencyMs < 50 ? "text-emerald-400" : "text-cyan-400"}`}>​
                {node.latencyMs} ms​
              </span>​
            </div>​
​
            <div className="mt-2 text-[10px] text-slate-500 font-mono flex items-center 
justify-between">​
              <span>Auth: {node.authType}</span>​
              <span className="text-slate-400">Circuit Breaker: 120s</span>​
            </div>​
          </div>​
        ))}​
      </div>​
    </div>​
  );​
}​


