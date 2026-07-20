import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { readFileSync } from "node:fs";

export default defineConfig(({ command }) => ({
  plugins: [react()],
  server: {
    port: 5173,
    https:
      command === "serve"
        ? {
            cert: readFileSync(new URL("../../.certs/localhost.pem", import.meta.url)),
            key: readFileSync(new URL("../../.certs/localhost-key.pem", import.meta.url)),
          }
        : undefined,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
}));
