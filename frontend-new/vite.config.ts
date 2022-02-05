import { defineConfig } from 'vite'
import path from 'path'
import Vue from '@vitejs/plugin-vue'
import Pages from 'vite-plugin-pages'
import Layouts from 'vite-plugin-vue-layouts'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'
import Components from 'unplugin-vue-components/vite'
import { imagetools } from 'vite-imagetools'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    Vue(),
    Pages(),
    Layouts(),
    Icons({
      // install iconset automatically
      autoInstall: true
    }),
    Components({
      resolvers: [
        // auto import icons
        IconsResolver({
          prefix: 'icon'
        })
      ],
      directoryAsNamespace: true,
      dts: 'src/components.d.ts'
    }),
    imagetools()
  ],
  optimizeDeps: {
    include: ['vue', 'vue-router', '@vueuse/head']
  },
  resolve: {
    alias: {
      '~': path.resolve(__dirname, './src')
    }
  },
  test: {
    environment: 'jsdom',
    watch: false
  },
  server: {
    hmr: {
      port: process.env.GITPOD_WORKSPACE_ID ? 443 : undefined
    },
    proxy: {
      '^/(api|public)': {
        target: process.env.API_PROXY_URL || 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  ssgOptions: {
    formatting: 'minify'
  }
})
