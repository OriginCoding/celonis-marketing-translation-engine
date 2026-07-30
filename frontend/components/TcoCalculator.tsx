"use client";

import { useState } from "react";
import { Calculator, TrendingUp, DollarSign, Clock } from "lucide-react";

export function TcoCalculator() {
  const [annualAssets, setAnnualAssets] = useState(400);
  const [targetLanguages, setTargetLanguages] = useState(7);
  const [hourlyRate, setHourlyRate] = useState(85);
  const [tokenCostPerRun, setTokenCostPerRun] = useState(0.0018);

  const totalRuns = annualAssets * targetLanguages;
  const baselineManualHours = 334;
  const baselineManualCost = baselineManualHours * hourlyRate;

  // 70% review time reduction savings
  const hoursSaved = baselineManualHours * 0.70;
  const directLaborSavings = hoursSaved * hourlyRate;

  // Annual engine OPEX (LLM API + Serverless + Maintenance)
  const annualLlmCost = totalRuns * tokenCostPerRun;
  const annualOpex = annualLlmCost + 1200 + 3000;

  const netAnnualSavings = directLaborSavings - annualOpex;
  const roiPercentage = ((netAnnualSavings / annualOpex) * 100).toFixed(0);
  const paybackMonths = ((annualOpex / directLaborSavings) * 12).toFixed(1);

  return (
    <div className="glass-panel p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-slate-100 flex items-center gap-2">
          <Calculator className="w-5 h-5 text-cyan-400" />
          Interactive TCO & ROI Financial Calculator
        </h3>
        <span className="text-xs font-mono text-cyan-400 bg-cyan-500/10 px-2.5 py-1 rounded border border-cyan-500/20">
          Financial Model
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="space-y-4 glass-card p-4">
          <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
            Operational Input Parameters
          </h4>

          <div>
            <div className="flex justify-between text-xs text-slate-300 mb-1">
              <span>Annual Deliverables</span>
              <span className="font-mono text-cyan-400">{annualAssets} assets/yr</span>
            </div>
            <input
              type="range"
              min={100}
              max={1000}
              step={50}
              value={annualAssets}
              onChange={(e) => setAnnualAssets(Number(e.target.value))}
              className="w-full accent-cyan-500 cursor-pointer"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs text-slate-300 mb-1">
              <span>Target Languages</span>
              <span className="font-mono text-cyan-400">{targetLanguages} languages</span>
            </div>
            <input
              type="range"
              min={1}
              max={15}
              step={1}
              value={targetLanguages}
              onChange={(e) => setTargetLanguages(Number(e.target.value))}
              className="w-full accent-cyan-500 cursor-pointer"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs text-slate-300 mb-1">
              <span>Language Champion Rate</span>
              <span className="font-mono text-cyan-400">${hourlyRate}/hr</span>
            </div>
            <input
              type="range"
              min={50}
              max={150}
              step={5}
              value={hourlyRate}
              onChange={(e) => setHourlyRate(Number(e.target.value))}
              className="w-full accent-cyan-500 cursor-pointer"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div className="glass-card p-4 text-center flex flex-col justify-center">
            <div className="text-xs text-slate-400 flex items-center justify-center gap-1 mb-1">
              <TrendingUp className="w-4 h-4 text-emerald-400" /> Net Annual ROI
            </div>
            <div className="text-2xl font-bold text-emerald-400 font-mono">
              {roiPercentage}%
            </div>
            <div className="text-[10px] text-slate-400 mt-1">Direct ROI</div>
          </div>

          <div className="glass-card p-4 text-center flex flex-col justify-center">
            <div className="text-xs text-slate-400 flex items-center justify-center gap-1 mb-1">
              <Clock className="w-4 h-4 text-cyan-400" /> Payback Period
            </div>
            <div className="text-2xl font-bold text-cyan-400 font-mono">
              {paybackMonths} Mo
            </div>
            <div className="text-[10px] text-slate-400 mt-1">Breakeven Time</div>
          </div>

          <div className="glass-card p-4 text-center flex flex-col justify-center">
            <div className="text-xs text-slate-400 flex items-center justify-center gap-1 mb-1">
              <DollarSign className="w-4 h-4 text-emerald-400" /> Net Savings
            </div>
            <div className="text-xl font-bold text-slate-100 font-mono">
              ${netAnnualSavings.toLocaleString()}/yr
            </div>
            <div className="text-[10px] text-slate-400 mt-1">Direct Labor Savings</div>
          </div>

          <div className="glass-card p-4 text-center flex flex-col justify-center">
            <div className="text-xs text-slate-400 mb-1">LLM API Cost</div>
            <div className="text-xl font-bold text-slate-100 font-mono">
              ${annualLlmCost.toFixed(2)}/yr
            </div>
            <div className="text-[10px] text-slate-400 mt-1">{totalRuns.toLocaleString()} runs</div>
          </div>
        </div>
      </div>
    </div>
  );
}
