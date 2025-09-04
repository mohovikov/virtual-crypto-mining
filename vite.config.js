import { defineConfig } from "vite"
import { resolve } from "path"

export default defineConfig({
  build: {
    outDir: resolve(__dirname, "static/js"),
    emptyOutDir: true,
    minify: "esbuild",
    rollupOptions: {
      input: "./src/main.js",
      output: {
        entryFileNames: "bundle.min.js",
        assetFileNames: "assets/[name].[ext]"
      }
    }
  }
})