import { defineConfig } from 'vite'
import path from 'path'
import Vue from '@vitejs/plugin-vue'
import Pages from 'vite-plugin-pages'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [Vue(), Pages()],
  resolve: {
    alias: {
      '~': path.resolve(__dirname, './src')
    }
  }
})
