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

import ECharts from 'vue-echarts/components/ECharts.vue'
import 'echarts/lib/chart/bar'
import 'echarts/lib/chart/line'
import 'echarts/lib/chart/pie'
import 'echarts/lib/component/title'
import 'echarts/lib/component/grid'
import 'echarts/lib/component/dataZoom'
import 'echarts/lib/component/legend'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/toolbox'
import 'echarts/lib/component/markPoint'

import { BootstrapVue, IconsPlugin, LayoutPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

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

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(LayoutPlugin)

Vue.component('ECharts', ECharts)
Vue.component(VerticalMenu.name, VerticalMenu)
Vue.component(VerticalMenuItem.name, VerticalMenuItem)
Vue.component(Panel.name, Panel)

Vue.config.devtools = process.env.NODE_ENV !== 'production'

// 注册全局消息提示
Vue.prototype.$Message.config({
  duration: 2
})
Vue.prototype.$error = (s) => Vue.prototype.$Message.error(s)
Vue.prototype.$info = (s) => Vue.prototype.$Message.info(s)
Vue.prototype.$success = (s) => Vue.prototype.$Message.success(s)

new Vue(Vue.util.extend({ router, store, i18n }, App)).$mount('#app')
