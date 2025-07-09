import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://backend:3001'
    }
  },
  build: {
    outDir: 'build',
    sourcemap: true
  },
  resolve: {
    alias: {
      '@': '/src',
      '@shared': resolve(__dirname, 'shared')
    }
  },
  define: {
    'process.env': {}
  }
})