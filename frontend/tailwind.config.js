/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        celonis: {
          dark: "#040B14",
          card: "#0A1628",
          border: "#1E293B",
          accent: "#0066FF",
          cyan: "#00F0FF",
          pass: "#10B981",
          review: "#F59E0B",
          reject: "#EF4444"
        }
      }
    },
  },
  plugins: [],
}
