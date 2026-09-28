import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx,mdx}", "./components/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        bg: "#08100d",
        panel: "#101916",
        panelSoft: "#16211e",
        line: "#273832",
        mint: "#58d68d",
        red: "#ff6b6b",
        amber: "#f8c471",
        ink: "#f5fff9",
        muted: "#9eb5aa"
      }
    }
  },
  plugins: []
};

export default config;

