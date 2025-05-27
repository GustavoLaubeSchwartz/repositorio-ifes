import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0',    // Necessário para funcionar com Docker
    port: 5173,          // Porta que o app utiliza (garantindo que bata com a exposta)
    watch: {
      usePolling: true,  // Habilita o polling para detectar mudanças
    },
  }
})
