import "./globals.css";
import { HeaderNav } from "@/components/HeaderNav";

export const metadata = {
  title: "Celonis Marketing Asset Translation Studio",
  description: "Enterprise Agentic Localization Engine with AI Quality Gates",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen flex flex-col bg-celonis-dark text-slate-100">
        <HeaderNav />
        <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 space-y-6">
          {children}
        </main>
        <footer className="border-t border-slate-800 py-4 text-center text-xs text-slate-500">
          Celonis Marketing Applied AI Solutions • Enterprise Localization Engine v1.0
        </footer>
      </body>
    </html>
  );
}
