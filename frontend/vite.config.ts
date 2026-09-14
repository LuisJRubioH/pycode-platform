/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    css: false,
    exclude: ['node_modules', 'dist', 'e2e', 'tests/e2e', '**/*.spec.ts'],
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  worker: {
    format: 'es',
  },
  build: {
    rollupOptions: {
      output: {
        // Las paginas ya se cargan con React.lazy (App.tsx). Aqui solo se
        // agrupan dos cosas que Rollup repartia mal:
        // - React y el router cambian casi nunca: en su propio chunk, el
        //   navegador los conserva en cache entre deploys.
        // - lucide-react: cada icono salia como un chunk de ~0,3 kB compartido
        //   entre paginas (mas de 20 peticiones); juntos pesan poco.
        manualChunks(id) {
          if (!id.includes('node_modules')) return undefined
          if (/[\\/]node_modules[\\/](react|react-dom|scheduler|react-router|react-router-dom|@remix-run)[\\/]/.test(id)) {
            return 'react'
          }
          if (id.includes('lucide-react')) return 'iconos'
          return undefined
        },
      },
    },
  },
})
