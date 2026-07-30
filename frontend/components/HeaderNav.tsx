"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Cpu, FileText, Calculator, ShieldCheck } from "lucide-react";

export function HeaderNav() {
  const pathname = usePathname();

  const links = [
    { href: "/", label: "Marketing Studio", icon: Cpu },
    { href: "/doc/solution-design", label: "Solution Design Doc", icon: FileText },
    { href: "/doc/tco-model", label: "TCO & ROI Model", icon: Calculator },
  ];

  return (
    <header className="border-b border-slate-800 bg-celonis-dark/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center font-bold text-white shadow-lg shadow-cyan-500/20">
            ⚡
          </div>
          <div>
            <div className="font-bold text-slate-100 flex items-center gap-2">
              Celonis Marketing Agent
              <span className="px-2 py-0.5 text-xs bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 rounded-full font-mono">
                es-ES
              </span>
            </div>
            <p className="text-xs text-slate-400">Applied AI Localization & Quality Gate Engine</p>
          </div>
        </div>

        <nav className="flex items-center gap-2">
          {links.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all flex items-center gap-2 ${
                  isActive
                    ? "bg-blue-600/20 text-blue-400 border border-blue-500/30"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                }`}
              >
                <Icon className="w-4 h-4" />
                {link.label}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-2">
          <div className="px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold flex items-center gap-1.5 shadow-sm">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            ⚡ Enterprise AI Stack Active
          </div>
        </div>
      </div>
    </header>
  );
}
