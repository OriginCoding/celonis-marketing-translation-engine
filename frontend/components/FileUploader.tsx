"use client";

import { UploadCloud, FilePlus } from "lucide-react";

interface FileUploaderProps {
  onFileUpload: (file: File) => void;
  fileName: string | null;
}

export function FileUploader({ onFileUpload, fileName }: FileUploaderProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onFileUpload(e.target.files[0]);
    }
  };

  return (
    <div
      onClick={() => document.getElementById("file-picker")?.click()}
      className="glass-card p-6 border-dashed border-2 border-slate-700 hover:border-cyan-400 cursor-pointer flex flex-col items-center justify-center text-center transition-all"
    >
      <UploadCloud className="w-8 h-8 text-cyan-400 mb-2 opacity-80" />
      <div className="text-xs font-bold text-slate-200">
        {fileName ? `📄 Uploaded: ${fileName}` : "Click or Drag & Drop HTML File Here"}
      </div>
      <p className="text-[11px] text-slate-500 mt-1">
        Supports .html and .htm marketing documents
      </p>
      <input
        type="file"
        id="file-picker"
        accept=".html,.htm"
        onChange={handleChange}
        className="hidden"
      />
    </div>
  );
}
