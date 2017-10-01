import Vue from 'vue'
import Router from 'vue-router'
import VueDoc from '@/components/VueDoc'
import Main from '@/components/Main'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/vue',
      name: 'Vue',
      component: VueDoc
    },
    {
      path: '/',
      name: 'Main',
      component: Main
    }
  ]
})
