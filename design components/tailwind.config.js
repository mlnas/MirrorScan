/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "var(--border)",
        background: "var(--background)",
        foreground: "var(--foreground)",
        primary: {
          DEFAULT: "var(--primary)",
          hover: "var(--primary-hover)",
        },
        card: {
          DEFAULT: "var(--card-background)",
        },
        muted: {
          DEFAULT: "var(--muted)",
          foreground: "var(--muted-foreground)",
        },
        accent: {
          DEFAULT: "var(--accent)",
          foreground: "var(--accent-foreground)",
        },
        destructive: {
          DEFAULT: "var(--destructive)",
          foreground: "var(--destructive-foreground)",
        },
        warning: {
          DEFAULT: "var(--warning)",
        },
        success: {
          DEFAULT: "var(--success)",
        },
        terminal: {
          bg: "var(--terminal-bg)",
          text: "var(--terminal-text)",
          prompt: "var(--terminal-prompt)",
          warning: "var(--terminal-warning)",
        }
      },
      fontFamily: {
        mono: ["JetBrains Mono", "monospace"],
      },
      keyframes: {
        "glow": {
          "0%, 100%": { textShadow: "0 0 10px var(--primary)" },
          "50%": { textShadow: "0 0 20px var(--primary)" },
        }
      },
      animation: {
        "glow": "glow 2s ease-in-out infinite",
      }
    },
  },
  plugins: [require("tailwindcss-animate")],
} 