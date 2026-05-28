const { fontFamily } = require("tailwindcss/defaultTheme");

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          /* Brand Teal — matches brand/BRAND_GUIDELINES.md #0b7272 */
          50: "#e6f4f4", 100: "#b3d9d9", 200: "#80bfbf", 300: "#4da4a4",
          400: "#1a9090", 500: "#0b7272", 600: "#095c5c", 700: "#074545",
          800: "#042e2e", 900: "#021717",
        },
        secondary: {
          50: "#FFF0F0", 100: "#FFD6D6", 200: "#FFBDBD", 300: "#FFA4A4",
          400: "#FF8B8B", 500: "#FF6B6B", 600: "#CC5656", 700: "#994040",
          800: "#662B2B", 900: "#331515",
        },
        accent: {
          50: "#FEF7E8", 100: "#FCEAB9", 200: "#FADF8A", 300: "#F8D45B",
          400: "#F6C92C", 500: "#F4A261", 600: "#C3824E", 700: "#92613A",
          800: "#614127", 900: "#302013",
        },
        success: {
          50: "#E8FCF8", 100: "#B8F5EA", 200: "#88EEDC", 300: "#58E7CE",
          400: "#28E0C0", 500: "#2EC4B6", 600: "#259D92", 700: "#1C766D",
          800: "#134E49", 900: "#0A2724",
        },
        neutral: {
          50: "#FAFAF9", 100: "#F5F5F4", 200: "#E7E5E4", 300: "#D6D3D1",
          400: "#A8A29E", 500: "#78716C", 600: "#57534E", 700: "#44403C",
          800: "#292524", 900: "#1C1917", 950: "#0C0A09",
        },
      },
      fontFamily: {
        heading: ["var(--font-inter)", "system-ui", "sans-serif"],
        body: ["var(--font-inter)", "system-ui", "sans-serif"],
        rounded: ["var(--font-nunito)", "system-ui", "sans-serif"],
      },
      boxShadow: {
        glow: "0 0 40px -10px rgba(13, 115, 119, 0.3)",
        "glow-lg": "0 0 60px -15px rgba(13, 115, 119, 0.4)",
        card: "0 4px 24px -4px rgba(0, 0, 0, 0.08)",
        "card-hover": "0 8px 40px -8px rgba(0, 0, 0, 0.12)",
      },
      animation: {
        "fade-in": "fadeIn 0.5s ease-out forwards",
        "fade-in-up": "fadeInUp 0.6s ease-out forwards",
        "pulse-soft": "pulseSoft 3s ease-in-out infinite",
        float: "float 6s ease-in-out infinite",
      },
      keyframes: {
        fadeIn: { "0%": { opacity: "0" }, "100%": { opacity: "1" } },
        fadeInUp: { "0%": { opacity: "0", transform: "translateY(20px)" }, "100%": { opacity: "1", transform: "translateY(0)" } },
        pulseSoft: { "0%, 100%": { opacity: "1" }, "50%": { opacity: "0.7" } },
        float: { "0%, 100%": { transform: "translateY(0)" }, "50%": { transform: "translateY(-10px)" } },
      },
    },
  },
  plugins: [],
};
