"use client";

import { useState } from "react";
import { UserCheck, CheckCircle, XCircle } from "lucide-react";

interface HitlProps {
  jobId: string;
  assignedTo: string;
  reasoning: string;
  recommendedAction: string;
  translatedHtml: string;
  onApprove: (notes: string) => void;
  onReject: (notes: string) => void;
}

export function HitlReviewPortal({
  jobId,
  assignedTo,
  reasoning,
  recommendedAction,
  translatedHtml,
  onApprove,
  onReject,
}: HitlProps) {
  const [reviewerNotes, setReviewerNotes] = useState("");
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const handleApprove = () => {
    onApprove(reviewerNotes);
    setStatusMessage("✅ Asset Approved! Queued for Staging CMS & Segment Saved to Translation Memory.");
  };

  const handleReject = () => {
    onReject(reviewerNotes);
    setStatusMessage("❌ Asset Rejected. Quality critique returned to Translation Agent feedback loop.");
  };

  return (
    <div className="glass-panel p-5 border-blue-500/30">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-base font-semibold text-slate-100 flex items-center gap-2">
          <UserCheck className="w-5 h-5 text-blue-400" />
          Language Champion HITL Review Portal
        </h3>
        <span className="text-xs font-mono text-blue-400 bg-blue-500/10 px-2.5 py-1 rounded border border-blue-500/20">
          Assigned to: {assignedTo}
        </span>
      </div>

      <div className="glass-card p-3 mb-4 text-xs space-y-1.5 border-slate-800">
        <div>
          <strong className="text-slate-200">Gating Reasoning:</strong> {reasoning}
        </div>
        <div>
          <strong className="text-slate-200">Recommended Action:</strong> {recommendedAction}
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-xs font-medium text-slate-300 mb-1">
          Reviewer Notes / Spanish Phrasing Guidance
        </label>
        <textarea
          value={reviewerNotes}
          onChange={(e) => setReviewerNotes(e.target.value)}
          placeholder="e.g. Verified Spanish phrasing for Celonis Process Intelligence. Approved for production."
          rows={2}
          className="w-full bg-slate-950/80 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
        />
      </div>

      {statusMessage && (
        <div className="mb-4 p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-medium">
          {statusMessage}
        </div>
      )}

      <div className="flex items-center justify-end gap-3">
        <button
          onClick={handleReject}
          className="px-4 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-300 border border-red-500/30 text-xs font-semibold rounded-lg flex items-center gap-1.5 transition-all"
        >
          <XCircle className="w-4 h-4" /> Send Back for Re-Translation
        </button>

        <button
          onClick={handleApprove}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg shadow-lg shadow-emerald-600/20 flex items-center gap-1.5 transition-all"
        >
          <CheckCircle className="w-4 h-4" /> Approve & Deploy to Staging
        </button>
      </div>
    </div>
  );
}
