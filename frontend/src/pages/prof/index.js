import Vue from 'vue'
import App from './App.vue'
import store from '@/store'

import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import filters from '@/utils/filters'
import router from './router'
import 'katex/dist/katex.min.css'
import VueKatex from 'vue-katex'
import VueSimpleAlert from 'vue-simple-alert'
import VueDOMPurifyHTML from 'vue-dompurify-html'

import Panel from './components/Panel.vue'
import IconBtn from './components/btn/IconBtn.vue'
import Save from './components/btn/Save.vue'
import Cancel from './components/btn/Cancel.vue'

// register global utility filters.
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

Vue.use(VueKatex)
Vue.use(VueSimpleAlert)
Vue.use(VueDOMPurifyHTML)
Vue.component(IconBtn.name, IconBtn)
Vue.component(Panel.name, Panel)
Vue.component(Save.name, Save)
Vue.component(Cancel.name, Cancel)

Vue.config.devtools = true

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

new Vue(Vue.util.extend({ router, store }, App)).$mount('#app')
