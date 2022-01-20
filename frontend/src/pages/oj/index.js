import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from '@/store'
import VueClipboard from 'vue-clipboard2'
import VueSimpleAlert from 'vue-simple-alert'
import VueDOMPurifyHTML from 'vue-dompurify-html'

import iView from 'iview'
import 'iview/dist/styles/iview.css'

import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import '@/styles/bootstrap.scss'
import '@/styles/common.scss'
import '@/styles/tailwind.css'

import highlight from '@/plugins/highlight'
import 'katex/dist/katex.min.css'
import VueKatex from 'vue-katex'
import filters from '@/utils/filters.js'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// register global utility filters.
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

Vue.config.productionTip = false

Vue.use(iView)
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
library.add(fas, far)
Vue.component('icon', FontAwesomeIcon)

Vue.use(VueClipboard)
Vue.use(highlight)
Vue.use(VueKatex)
Vue.use(VueSimpleAlert)
Vue.use(VueDOMPurifyHTML)

Vue.config.devtools = process.env.NODE_ENV !== 'production'

Vue.prototype.$info = (s) => {
  s.length <= 15
    ? Vue.prototype.$fire({
      toast: true,
      title: s,
      position: 'top',
      timer: 1500,
      width: '225px',
      type: 'info',
      showConfirmButton: false
    })
    : Vue.prototype.$fire({
      toast: true,
      title: s,
      position: 'top',
      timer: 2500,
      width: '350px',
      type: 'info',
      showConfirmButton: false
    })
}
Vue.prototype.$error = (s) => {
  s.length <= 15
    ? Vue.prototype.$fire({
      toast: true,
      title: s,
      position: 'top',
      timer: 1500,
      width: '225px',
      type: 'error',
      showConfirmButton: false
    })
    : Vue.prototype.$fire({
      toast: true,
      title: s,
      position: 'top',
      timer: 2500,
      width: '350px',
      type: 'error',
      showConfirmButton: false
    })
}
Vue.prototype.$success = (s) => {
  s.length <= 15
    ? Vue.prototype.$fire({
      toast: true,
      title: s,
      position: 'top',
      timer: 1500,
      width: '225px',
      type: 'success',
      showConfirmButton: false
    })
    : Vue.prototype.$fire({
      toast: true,
      title: s,
      position: 'top',
      timer: 2500,
      width: '350px',
      type: 'success',
      showConfirmButton: false
    })
}

const app = new Vue(Vue.util.extend({ router, store }, App)).$mount('#app')

if (window.Cypress) {
  window.app = app
}
