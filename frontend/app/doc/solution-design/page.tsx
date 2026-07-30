"use client";

import { FileText, ArrowLeft, ShieldCheck, Cpu, CheckCircle2, Layers } from "lucide-react";
import Link from "next/link";

export default function SolutionDesignDocPage() {
  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <Link
          href="/"
          className="text-xs text-cyan-400 hover:underline flex items-center gap-1 font-medium"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Marketing Studio
        </Link>
        <span className="px-3 py-1 bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 rounded-full text-xs font-mono">
          Solution Design Doc v1.1.0
        </span>
      </div>

      <div className="glass-panel p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <FileText className="w-6 h-6 text-cyan-400" />
            Solution Design Document: Marketing Asset Translation Engine
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Author: Sr. Applied AI Engineer Candidate • Celonis Marketing Applied AI Solutions
          </p>
        </div>

        <div className="space-y-6 text-sm text-slate-300 leading-relaxed border-t border-slate-800 pt-5">
          <div>
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-2">
              <Cpu className="w-5 h-5 text-blue-400" /> 1. Problem Framing & System Scope
            </h2>
            <p>
              Celonis localizes 400+ marketing deliverables annually across 7 target languages, coordinated through 6+ disconnected platforms. Language Champions spend 334 hours per year manually reviewing localized assets line-by-line due to invisible and inconsistent quality checks.
            </p>
          </div>

          <div>
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-2">
              <Layers className="w-5 h-5 text-cyan-400" /> 2. 4-Step Guided Stepper Architecture
            </h2>
            <ul className="list-disc pl-5 space-y-1">
              <li><strong>Step 1 (Ingestion & Upload)</strong>: Drag-and-drop HTML file uploader or sample scenario selector.</li>
              <li><strong>Step 2 (Visual Preview)</strong>: Side-by-side visual rendered cards comparing original English copy vs Spanish localized output.</li>
              <li><strong>Step 3 (AI Quality Check)</strong>: LLM-as-a-Judge scoring across Accuracy (35%), Brand DNT (30%), Tone (20%), and Format (15%).</li>
              <li><strong>Step 4 (Publishing Decision)</strong>: Auto-Pass ($\ge 88\%$) for direct CMS staging or Human-in-the-Loop review box ($70-87\%$).</li>
            </ul>
          </div>

          <div>
            <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-2">
              <ShieldCheck className="w-5 h-5 text-emerald-400" /> 3. Do-Not-Translate (DNT) Penalty Override
            </h2>
            <p>
              Product terms (<code className="text-cyan-400 font-mono">Celonis</code>, <code className="text-cyan-400 font-mono">Agent C</code>, <code className="text-cyan-400 font-mono">Celonis Process Intelligence</code>, <code className="text-cyan-400 font-mono">MCP</code>, <code className="text-cyan-400 font-mono">CTA</code>, <code className="text-cyan-400 font-mono">ROI</code>, <code className="text-cyan-400 font-mono">Skill</code>) are protected by a zero-trust guardrail. Any unapproved alteration applies an immediate <strong>-25 point penalty</strong>, dropping the brand score to <strong>30/100</strong> and requiring human approval.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
