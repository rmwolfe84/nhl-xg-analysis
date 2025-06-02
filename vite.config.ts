import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  root: 'frontend',  // ADD THIS LINE
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./frontend/src', import.meta.url))  // UPDATE PATH
    },
  },
})