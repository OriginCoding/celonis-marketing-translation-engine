"use client";

import { Terminal, Zap, DollarSign, Activity } from "lucide-react";

interface DebuggerProps {
  totalTokens: number;
  totalLatencyMs: number;
  costUsd: number;
  activeGlossaryCount: number;
  activeTmCount: number;
  selfCorrectionPasses: number;
}

export function AgentDebuggerConsole({
  totalTokens,
  totalLatencyMs,
  costUsd,
  activeGlossaryCount,
  activeTmCount,
  selfCorrectionPasses,
}: DebuggerProps) {
  return (
    <div className="glass-panel p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-slate-100 flex items-center gap-2">
          <Terminal className="w-5 h-5 text-cyan-400" />
          Agentic Observability & Telemetry Console
        </h3>
        <span className="px-2 py-0.5 text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded font-mono">
          Free Tier Engine Active
        </span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
        <div className="glass-card p-3 text-center">
          <div className="text-xs text-slate-400 flex items-center justify-center gap-1 mb-1">
            <Zap className="w-3.5 h-3.5 text-yellow-400" /> Total Tokens
          </div>
          <div className="text-lg font-bold text-slate-100 font-mono">
            {totalTokens.toLocaleString()}
          </div>
        </div>

        <div className="glass-card p-3 text-center">
          <div className="text-xs text-slate-400 flex items-center justify-center gap-1 mb-1">
            <Activity className="w-3.5 h-3.5 text-cyan-400" /> Latency
          </div>
          <div className="text-lg font-bold text-slate-100 font-mono">
            {totalLatencyMs.toFixed(0)} ms
          </div>
        </div>

        <div className="glass-card p-3 text-center">
          <div className="text-xs text-slate-400 flex items-center justify-center gap-1 mb-1">
            <DollarSign className="w-3.5 h-3.5 text-emerald-400" /> Estimated Cost
          </div>
          <div className="text-lg font-bold text-emerald-400 font-mono">
            ${costUsd.toFixed(4)}
          </div>
        </div>

        <div className="glass-card p-3 text-center">
          <div className="text-xs text-slate-400 mb-1">Reflexion Passes</div>
          <div className={`text-lg font-bold font-mono ${selfCorrectionPasses > 0 ? "text-amber-400" : "text-slate-100"}`}>
            {selfCorrectionPasses}
          </div>
        </div>
      </div>

      <div className="glass-card p-3 text-xs font-mono text-slate-300 space-y-1.5 bg-slate-950/80 border-slate-800">
        <div className="text-slate-400 border-b border-slate-800 pb-1 mb-1 flex items-center justify-between">
          <span>MCP TOOL INVOCATION AUDIT LOG</span>
          <span>Status: OK</span>
        </div>
        <div>[JiraMCP] fetchAssetBrief("LOC-4082") -&gt; Asset Payload: HTML Context Model Page</div>
        <div>[GlossaryMCP] lookupDNT(targetLanguage="es") -&gt; {activeGlossaryCount} active DNT terms loaded</div>
        <div>[TMVectorRAG] searchSimilarity(threshold=0.85) -&gt; {activeTmCount} TM segments scanned</div>
        <div>[QualityGateJudge] evaluateMetrics(Accuracy, DNT, Tone, Format) -&gt; Execution complete</div>
      </div>
    </div>
  );
}
