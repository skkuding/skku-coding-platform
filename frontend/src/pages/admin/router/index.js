import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@admin/components/HelloWorld'

Vue.use(Router)

export default new Router({
  base: '/admin/',
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
})
