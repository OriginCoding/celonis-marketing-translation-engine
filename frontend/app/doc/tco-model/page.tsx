"use client";

import { Calculator, ArrowLeft, DollarSign, TrendingUp, Clock } from "lucide-react";
import Link from "next/link";

export default function TcoModelDocPage() {
  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <Link
          href="/"
          className="text-xs text-cyan-400 hover:underline flex items-center gap-1 font-medium"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Marketing Studio
        </Link>
        <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-mono">
          Financial Model v1.3.0
        </span>
      </div>

      <div className="glass-panel p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Calculator className="w-6 h-6 text-emerald-400" />
            Total Cost of Ownership (TCO) & ROI Model
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Financial Analysis & Token Economics • Celonis Marketing Applied AI Solutions
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 border-t border-slate-800 pt-5">
          <div className="glass-card p-4 text-center">
            <div className="text-xs text-slate-400 flex items-center justify-center gap-1 mb-1">
              <DollarSign className="w-4 h-4 text-emerald-400" /> Annual LLM API Cost
            </div>
            <div className="text-2xl font-bold text-slate-100 font-mono">$5.04 / yr</div>
            <div className="text-[10px] text-slate-400 mt-1">2,800 annual localization runs</div>
          </div>

          <div className="glass-card p-4 text-center">
            <div className="text-xs text-slate-400 flex items-center justify-center gap-1 mb-1">
              <TrendingUp className="w-4 h-4 text-cyan-400" /> Direct Labor Savings
            </div>
            <div className="text-2xl font-bold text-cyan-400 font-mono">$19,890 / yr</div>
            <div className="text-[10px] text-slate-400 mt-1">234 hours saved @ $85/hr</div>
          </div>

          <div className="glass-card p-4 text-center">
            <div className="text-xs text-slate-400 flex items-center justify-center gap-1 mb-1">
              <Clock className="w-4 h-4 text-emerald-400" /> Net Direct ROI & Payback
            </div>
            <div className="text-2xl font-bold text-emerald-400 font-mono">373% ROI</div>
            <div className="text-[10px] text-slate-400 mt-1">Payback period &lt; 2.5 months</div>
          </div>
        </div>
      </div>
    </div>
  );
}
