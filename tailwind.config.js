/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html, htm, js}", "./templates/*.{html, htm, js}"],
  daisyui: {
    themes: [
      {
        mytheme: {
          primary: "#386641",
          "primary-content": "#020e07",
          secondary: "#52ce8a",
          "secondary-content": "#111827",
          accent: "#1aad75",
          "accent-content": "#001616",
          neutral: "#fde047",
          "neutral-content": "#161202",
          "base-100": "#ffffff",
          "base-200": "#d1fae5",
          "base-300": "#dcfce7",
          "base-content": "#161616",
          info: "#0ea5e9",
          "info-content": "#000a13",
          success: "#00ff00",
          "success-content": "#001600",
          warning: "#fef08a",
          "warning-content": "#161407",
          error: "#ff0000",
          "error-content": "#f3f4f6",
        },
      },
    ],
  },
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/aspect-ratio"),
    require("daisyui"),
    require("@tailwindcss/typography"),
    require("tailwind-scrollbar-hide"),
    require("tailwindcss-animate"),
  ],
};
