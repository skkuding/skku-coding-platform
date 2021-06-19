import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from '@/store'
import i18n from '@/i18n'
import VueClipboard from 'vue-clipboard2'
import VueAnalytics from 'vue-analytics'
import VueSimpleAlert from 'vue-simple-alert'
import { GOOGLE_ANALYTICS_ID } from '@/utils/constants'

import iView from 'iview'
import 'iview/dist/styles/iview.css'

import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import Panel from '@oj/components/Panel.vue'
import VerticalMenu from '@oj/components/verticalMenu/verticalMenu.vue'
import VerticalMenuItem from '@oj/components/verticalMenu/verticalMenu-item.vue'
import '@/styles/bootstrap.scss'
import '@/styles/index.less'

import highlight from '@/plugins/highlight'
import katex from '@/plugins/katex'
import filters from '@/utils/filters.js'

// register global utility filters.
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

Vue.config.productionTip = false
Vue.use(iView, {
  i18n: (key, value) => i18n.t(key, value)
})

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)

Vue.use(VueClipboard)
Vue.use(highlight)
Vue.use(katex)
Vue.use(VueSimpleAlert)
Vue.use(VueAnalytics, {
  id: GOOGLE_ANALYTICS_ID,
  router
})

Vue.component(VerticalMenu.name, VerticalMenu)
Vue.component(VerticalMenuItem.name, VerticalMenuItem)
Vue.component(Panel.name, Panel)

Vue.config.devtools = process.env.NODE_ENV !== 'production'
// 注册全局消息提示

Vue.prototype.$Message.config({
  duration: 2
})

Vue.prototype.$info = (s, time = 1500) => {
  const len = s.length
  if (len <= 15) {
    Vue.prototype.$fire({
      toast: true,
      title: s,
      position: 'top',
      timer: 1500,
      width: '225px',
      type: 'info',
      showConfirmButton: false
    })
  } else {
    Vue.prototype.$fire({
      toast: true,
      title: s,
      position: 'top',
      timer: 1500,
      width: '350px',
      type: 'info',
      showConfirmButton: false
    })
  }
}
Vue.prototype.$error = (s, time = 1500) => {
  const len = s.length
  if (len <= 15) {
    Vue.prototype.$fire({
      toast: true,
      title: s,
      position: 'top',
      timer: 1500,
      width: '225px',
      type: 'error',
      showConfirmButton: false
    })
  } else {
    Vue.prototype.$fire({
      toast: true,
      title: s,
      position: 'top',
      timer: 1500,
      width: '350px',
      type: 'error',
      showConfirmButton: false
    })
  }
}
Vue.prototype.$success = (s, time = 1500) => {
  const len = s.length
  if (len <= 15) {
    Vue.prototype.$fire({
      toast: true,
      title: s,
      position: 'top',
      timer: time,
      width: '225px',
      type: 'success',
      showConfirmButton: false
    })
  } else {
    Vue.prototype.$fire({
      toast: true,
      title: s,
      position: 'top',
      timer: time,
      width: '350px',
      type: 'success',
      showConfirmButton: false
    })
  }
}

new Vue(Vue.util.extend({ router, store, i18n }, App)).$mount('#app')
