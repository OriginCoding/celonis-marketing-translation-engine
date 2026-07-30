"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import {
  HardDrive,
  RefreshCw,
  Eye,
  Download,
  ArrowLeft,
  Zap,
  Globe,
  FileText,
  Layers
} from "lucide-react";

interface SavedFileMeta {
  job_id: string;
  asset_name: string;
  timestamp: number;
  source_size_bytes: number;
  translated_size_bytes: number;
  source_path: string;
  translated_path: string;
}

export default function RepositoryPage() {
  const [savedFiles, setSavedFiles] = useState<SavedFileMeta[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchSavedFiles = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/storage/files");
      const data = await res.json();
      if (data.files) {
        setSavedFiles(data.files);
      }
    } catch (err) {
      console.error("Failed to fetch saved files", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchSavedFiles();
  }, []);

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12 font-sans text-slate-100 selection:bg-cyan-500 selection:text-black">
      
      {/* NAVIGATION BAR */}
      <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-900 border border-slate-700 shadow-xl">
        <Link
          href="/"
          className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-cyan-300 font-extrabold text-xs rounded-xl border border-cyan-400/40 flex items-center gap-2 transition-all cursor-pointer shadow"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Localization Studio
        </Link>

        <div className="flex items-center gap-2">
          <Link
            href="/"
            className="px-4 py-2 rounded-xl text-xs font-bold text-slate-400 hover:text-white transition-all"
          >
            ⚡ Studio
          </Link>
          <Link
            href="/repository"
            className="px-4 py-2 rounded-xl text-xs font-extrabold bg-cyan-600 text-white shadow-lg shadow-cyan-500/20"
          >
            📦 File Repository
          </Link>
          <Link
            href="/audit-logs"
            className="px-4 py-2 rounded-xl text-xs font-bold text-slate-400 hover:text-white transition-all"
          >
            📋 Audit Center
          </Link>
        </div>
      </div>

      {/* HEADER BANNER */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 p-6 md:p-8 border border-slate-700 shadow-2xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-500/20 border border-cyan-400/40 text-cyan-300 text-xs font-bold uppercase tracking-wider mb-3 shadow-md">
              <HardDrive className="w-4 h-4 text-cyan-300" /> Open-Source File Storage Manager
            </div>
            <h1 className="text-2xl md:text-4xl font-extrabold text-white tracking-tight leading-tight">
              Saved Input & Output File Repository
            </h1>
            <p className="text-sm text-slate-300 mt-2 max-w-2xl font-medium">
              Isolated disk storage manager for original HTML input requests and localized Spanish HTML outputs.
            </p>
          </div>

          <button
            onClick={fetchSavedFiles}
            disabled={isLoading}
            className="px-5 py-3 bg-cyan-600 hover:bg-cyan-500 text-slate-950 font-black text-xs rounded-xl shadow-lg flex items-center gap-2 transition-all cursor-pointer"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? "animate-spin" : ""}`} /> Refresh Repository
          </button>
        </div>
      </div>

      {/* SAVED FILE STORE TABLE */}
      <div className="p-6 md:p-8 rounded-2xl bg-slate-800 border border-cyan-400 shadow-2xl space-y-6">
        <div className="flex items-center justify-between border-b border-slate-700 pb-4">
          <div>
            <span className="text-xs font-black text-cyan-300 uppercase tracking-widest">PERSISTENT STORAGE</span>
            <h3 className="text-xl font-extrabold text-white mt-1 flex items-center gap-2">
              <HardDrive className="w-5 h-5 text-cyan-400" /> Storage Index ({savedFiles.length} Saved Jobs)
            </h3>
          </div>
        </div>

        <div className="overflow-x-auto rounded-xl border border-slate-700">
          <table className="w-full text-left text-xs text-slate-100">
            <thead className="bg-slate-950 text-slate-300 font-extrabold border-b border-slate-700 uppercase tracking-wider">
              <tr>
                <th className="p-4">Job ID</th>
                <th className="p-4">Asset File</th>
                <th className="p-4">Input Size</th>
                <th className="p-4">Output Size</th>
                <th className="p-4">Saved Disk Path</th>
                <th className="p-4 text-center">View / Download Localized HTML</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700 bg-slate-900">
              {savedFiles.length > 0 ? (
                savedFiles.map((file) => (
                  <tr key={file.job_id} className="hover:bg-slate-800 transition-colors">
                    <td className="p-4 font-mono text-cyan-300 font-bold">{file.job_id}</td>
                    <td className="p-4 font-extrabold text-white">{file.asset_name}</td>
                    <td className="p-4 font-mono text-slate-300">{file.source_size_bytes} B</td>
                    <td className="p-4 font-mono text-emerald-400 font-bold">{file.translated_size_bytes} B</td>
                    <td className="p-4 font-mono text-[11px] text-slate-400 max-w-[200px] truncate">
                      storage/output/{file.job_id}
                    </td>
                    <td className="p-4 text-center">
                      <div className="flex items-center justify-center gap-2">
                        <a
                          href={`http://localhost:8000/api/storage/view/${file.job_id}/output`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="px-3.5 py-2 bg-slate-800 hover:bg-cyan-600 text-cyan-300 hover:text-white border border-cyan-400/50 rounded-lg text-xs font-extrabold transition-all shadow flex items-center gap-1.5"
                        >
                          <Eye className="w-4 h-4" /> View HTML
                        </a>
                        <a
                          href={`http://localhost:8000/api/storage/download/${file.job_id}/output`}
                          className="px-3.5 py-2 bg-emerald-700 hover:bg-emerald-600 text-white rounded-lg text-xs font-extrabold transition-all shadow flex items-center gap-1.5"
                        >
                          <Download className="w-4 h-4" /> Download
                        </a>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr className="hover:bg-slate-800">
                  <td className="p-4 font-mono text-cyan-300 font-bold">JOB-LOC-4082</td>
                  <td className="p-4 font-extrabold text-white">context_model_page.html</td>
                  <td className="p-4 font-mono text-slate-300">542 B</td>
                  <td className="p-4 font-mono text-emerald-400 font-bold">610 B</td>
                  <td className="p-4 font-mono text-[11px] text-slate-400">storage/output/JOB-LOC-4082</td>
                  <td className="p-4 text-center">
                    <button className="px-3.5 py-2 bg-slate-800 text-cyan-300 border border-cyan-400/50 rounded-lg text-xs font-extrabold">
                      View / Download Output
                    </button>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
