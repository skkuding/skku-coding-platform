import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import generatedRoutes from 'virtual:generated-pages'
import { setupLayouts } from 'virtual:generated-layouts'
import NProgress from 'nprogress'
import App from './App.vue'
import './index.css'

const routes = setupLayouts(generatedRoutes)

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(() => { NProgress.start() })
router.afterEach(() => { NProgress.done() })

const app = createApp(App)

app.use(router)
app.mount('#app')
