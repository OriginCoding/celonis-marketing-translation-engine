"use client";

import { CheckCircle2, AlertTriangle, Info, Clock, Cpu } from "lucide-react";

interface TraceEvent {
  id: string;
  timestamp: string;
  stage: string;
  agent_name: string;
  tool_name?: string;
  message: string;
  status: "INFO" | "SUCCESS" | "WARNING" | "ERROR";
  tokens_used?: number;
  latency_ms?: number;
}

export function AgentTimeline({ events }: { events: TraceEvent[] }) {
  if (!events || events.length === 0) {
    return (
      <div className="glass-panel p-6 text-center text-slate-400">
        <Clock className="w-8 h-8 mx-auto mb-2 opacity-50" />
        <p>No agent execution trace events recorded yet. Run the pipeline to view real-time agent reasoning.</p>
      </div>
    );
  }

  return (
    <div className="glass-panel p-5">
      <h3 className="text-base font-semibold text-slate-100 mb-4 flex items-center gap-2">
        <Cpu className="w-5 h-5 text-cyan-400" />
        Real-Time Agentic Execution Trace
      </h3>
      <div className="space-y-3 relative before:absolute before:left-3.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800">
        {events.map((evt) => {
          const isSuccess = evt.status === "SUCCESS";
          const isWarning = evt.status === "WARNING";
          return (
            <div key={evt.id} className="relative pl-9 text-sm">
              <div className={`absolute left-0 top-0.5 w-7 h-7 rounded-full flex items-center justify-center border ${
                isSuccess
                  ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
                  : isWarning
                  ? "bg-amber-500/10 border-amber-500/30 text-amber-400"
                  : "bg-blue-500/10 border-blue-500/30 text-blue-400"
              }`}>
                {isSuccess ? (
                  <CheckCircle2 className="w-4 h-4" />
                ) : isWarning ? (
                  <AlertTriangle className="w-4 h-4" />
                ) : (
                  <Info className="w-4 h-4" />
                )}
              </div>
              <div className="glass-card p-3">
                <div className="flex items-center justify-between gap-2 mb-1">
                  <span className="font-semibold text-slate-200">{evt.stage}</span>
                  <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
                    <span>{evt.agent_name}</span>
                    {evt.latency_ms && <span>• {evt.latency_ms.toFixed(0)}ms</span>}
                  </div>
                </div>
                <p className="text-slate-300 text-xs">{evt.message}</p>
                {evt.tool_name && (
                  <div className="mt-2 text-xs font-mono text-cyan-400 bg-cyan-950/40 px-2 py-1 rounded inline-block border border-cyan-800/40">
                    🛠️ {evt.tool_name}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
