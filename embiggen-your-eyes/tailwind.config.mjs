import type { Config } from 'tailwindcss';
import plugin from 'tailwindcss/plugin';

export default {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  darkMode: ["class"],
  theme: {
    extend: {
      colors: {
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
      },
    },
  },
  plugins: [
    plugin(function({ addBase }) {
      addBase({
        ':root': {
          '--background': '0 0% 100%',
          '--foreground': '222.2 84% 4.9%',
          '--primary': '222.2 47.4% 11.2%',
          '--secondary': '210 40% 96.1%',
          '--border': '214.3 31.8% 91.4%',
        },
        '.dark': {
          '--background': '222.2 84% 4.9%',
          '--foreground': '210 40% 98%',
          '--primary': '210 40% 98%',
          '--secondary': '217.2 32.6% 17.5%',
          '--border': '217.2 32.6% 17.5%',
        },
      })
    })
  ],
} satisfies Config;