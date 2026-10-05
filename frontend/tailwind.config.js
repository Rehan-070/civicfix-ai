/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef2ff',
          100: '#e0e7ff',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          900: '#312e81',
        },
        civic: {
          emerald: '#10b981',
          amber: '#f59e0b',
          rose: '#f43f5e',
          cyan: '#06b6d4',
          slate: '#0f172a'
        }
      }
    },
  },
  plugins: [],
}
