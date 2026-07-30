"use client";

import { ShieldCheck, AlertOctagon, Info } from "lucide-react";

interface QualityProps {
  accuracy: number;
  glossaryDnt: number;
  brandTone: number;
  htmlStructure: number;
  overallConfidence: number;
  dntViolations: string[];
  glossaryViolations: string[];
  formattingIssues: string[];
  critiqueFeedback: string;
}

export function QualityGateMatrix({
  accuracy,
  glossaryDnt,
  brandTone,
  htmlStructure,
  overallConfidence,
  dntViolations,
  glossaryViolations,
  critiqueFeedback,
}: QualityProps) {
  const isPass = overallConfidence >= 88 && dntViolations.length === 0;

  return (
    <div className="glass-panel p-5">
      {/* Result Status Banner */}
      <div
        className={`mb-5 p-4 rounded-xl border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 ${
          isPass
            ? "bg-emerald-950/20 border-emerald-500/30 text-emerald-300"
            : "bg-amber-950/20 border-amber-500/30 text-amber-300"
        }`}
      >
        <div className="flex items-center gap-3">
          <div
            className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg ${
              isPass ? "bg-emerald-500/20 text-emerald-400" : "bg-amber-500/20 text-amber-400"
            }`}
          >
            {isPass ? "✓" : "⚠️"}
          </div>
          <div>
            <div className="text-base font-bold">
              {isPass
                ? `Document Passed Quality Check (Score: ${overallConfidence}%)`
                : `Human Review Required (Brand Score: ${glossaryDnt}%)`}
            </div>
            <p className="text-xs opacity-90 mt-0.5">
              {isPass
                ? "Zero brand name violations found. Ready for immediate publishing."
                : "Brand term 'Agent C' was altered. Review required before publishing."}
            </p>
          </div>
        </div>
      </div>

      {/* 4 Plain-English Badges */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
        <div className="glass-card p-4 text-center">
          <div className="text-xs text-slate-400 mb-1">🎯 Meaning Preserved</div>
          <div className="text-xl font-bold text-slate-100 font-mono">{accuracy}%</div>
        </div>

        <div className="glass-card p-4 text-center">
          <div className="text-xs text-slate-400 mb-1">🔒 Brand Names Kept</div>
          <div
            className={`text-xl font-bold font-mono ${
              glossaryDnt < 80 ? "text-amber-400" : "text-emerald-400"
            }`}
          >
            {glossaryDnt}%
          </div>
        </div>

        <div className="glass-card p-4 text-center">
          <div className="text-xs text-slate-400 mb-1">📣 Tone of Voice</div>
          <div className="text-xl font-bold text-slate-100 font-mono">{brandTone}%</div>
        </div>

        <div className="glass-card p-4 text-center">
          <div className="text-xs text-slate-400 mb-1">📐 Page Formatting</div>
          <div className="text-xl font-bold text-slate-100 font-mono">{htmlStructure}%</div>
        </div>
      </div>

      {/* Critique Feedback */}
      <div className="space-y-2 text-xs">
        <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-300">
          <strong className="text-slate-100">Evaluator Feedback:</strong> {critiqueFeedback}
        </div>

        {dntViolations.length > 0 && (
          <div className="p-3 rounded-lg bg-red-950/40 border border-red-800/40 text-red-300 flex items-start gap-2">
            <AlertOctagon className="w-4 h-4 text-red-400 mt-0.5 shrink-0" />
            <div>
              <strong>Critical Brand Name Violations ({dntViolations.length}):</strong> {dntViolations.join("; ")}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
