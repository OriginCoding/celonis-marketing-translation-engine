"use client";

import { FileCode, Sparkles } from "lucide-react";

interface DiffProps {
  sourceHtml: string;
  translatedHtml: string;
}

export function ContentDiffViewer({ sourceHtml, translatedHtml }: DiffProps) {
  return (
    <div className="glass-panel p-5">
      <h3 className="text-base font-semibold text-slate-100 mb-4 flex items-center gap-2">
        <FileCode className="w-5 h-5 text-cyan-400" />
        Side-by-Side Content & HTML Diff Viewer
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
              🇺🇸 Source Asset (English HTML)
            </span>
            <span className="text-xs text-slate-500 font-mono">Original DOM</span>
          </div>
          <pre className="glass-card p-3 text-xs text-slate-300 font-mono overflow-x-auto max-h-[350px] whitespace-pre-wrap bg-slate-950/70 border-slate-800">
            {sourceHtml}
          </pre>
        </div>

        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-cyan-400 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5" /> 🇪🇸 Localized Output (Spanish HTML)
            </span>
            <span className="text-xs text-emerald-400 font-mono bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
              DNT Protected
            </span>
          </div>
          <pre className="glass-card p-3 text-xs text-slate-300 font-mono overflow-x-auto max-h-[350px] whitespace-pre-wrap bg-slate-950/70 border-slate-800">
            {translatedHtml}
          </pre>
        </div>
      </div>
    </div>
  );
}
