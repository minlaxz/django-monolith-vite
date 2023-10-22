import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import { dependencies } from './package.json'

const inclVendors = ['lottie-react']
function renderChunks(deps) {
  let chunks = {}
  Object.keys(deps).forEach((key) => {
    if (inclVendors.includes(key)) chunks[key] = [key]
    return
  })
  return chunks
}


export default defineConfig({
  plugins: [
    react({
    babel: {
      babelrc: true
    }
    })
  ],
  optimizeDeps: {
    include: ['@emotion/styled'],
  },
  root: resolve('./src'),
  base: '/static/',
  server: {
    host: 'localhost',
    port: 3000,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    extensions: ['.js', '.json', '.jsx'],
    alias: {
      '@': resolve(__dirname, './src')
    },
  },
  build: {
    outDir: resolve('./_dist'),
    assetsDir: '',
    manifest: true,
    emptyOutDir: true,
    target: 'es2022',
    rollupOptions: {
      input: {
        main: resolve('./src/main.jsx'),
      },
      output: {
        manualChunks: {
          ...renderChunks(dependencies),
        },
        chunkFileNames: "[name]-[hash].js",
        compact: true
      },
    },
  },
})
