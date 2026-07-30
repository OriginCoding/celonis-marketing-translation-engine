"use client";

import { Bug, RefreshCw, ShieldAlert } from "lucide-react";

interface ErrorSandboxProps {
  injectError: boolean;
  onToggleError: (val: boolean) => void;
  onRunPipeline: () => void;
  isLoading: boolean;
}

export function ErrorInjectionSandbox({
  injectError,
  onToggleError,
  onRunPipeline,
  isLoading,
}: ErrorSandboxProps) {
  return (
    <div className="glass-panel p-5 border-amber-500/30">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h3 className="text-base font-semibold text-slate-100 flex items-center gap-2">
            <Bug className="w-5 h-5 text-amber-400" />
            Live Error Injection & Reflexion Sandbox
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Simulate a bad LLM translation output (e.g. corrupting DNT term &quot;Agent C&quot; $\rightarrow$ &quot;Agente C&quot;) to test the 5-Layer Resilience Engine live.
          </p>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <label className="flex items-center gap-2 text-xs font-medium text-slate-300 cursor-pointer bg-slate-900/80 px-3 py-2 rounded-lg border border-slate-800 hover:border-slate-700">
            <input
              type="checkbox"
              checked={injectError}
              onChange={(e) => onToggleError(e.target.checked)}
              className="w-4 h-4 accent-amber-500 rounded cursor-pointer"
            />
            <span className={injectError ? "text-amber-400 font-bold" : ""}>
              Inject DNT Error Mode
            </span>
          </label>

          <button
            onClick={onRunPipeline}
            disabled={isLoading}
            className="px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white text-xs font-semibold rounded-lg shadow-lg shadow-blue-500/20 flex items-center gap-2 disabled:opacity-50 transition-all"
          >
            {isLoading ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <ShieldAlert className="w-4 h-4" />
            )}
            Run Pipeline Test
          </button>
        </div>
      </div>
    </div>
  );
}
