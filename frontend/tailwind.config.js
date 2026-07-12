/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        sage: {
          50: "#f3f6f2",
          100: "#e2e9de",
          500: "#5f7a56",
          600: "#4b6144",
          700: "#3b4d36",
          900: "#232e20",
        },
      },
    },
  },
  plugins: [],
};
