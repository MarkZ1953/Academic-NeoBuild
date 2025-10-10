import react from "@vitejs/plugin-react-swc";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";
import path from "path";

/**
 * Vite configuration for the frontend project.
 *
 * - Integrates React and Tailwind CSS plugins.
 * - Sets up a path alias "@" to resolve to the "./src" directory for cleaner imports.
 *
 * @see https://vitejs.dev/config/
 * @see https://vitejs.dev/guide/features.html#aliasing
 */
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
