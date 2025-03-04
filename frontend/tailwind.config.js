/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{ts,tsx}",
  ],
  theme: { extend: {} },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};