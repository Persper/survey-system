import Vue from 'vue'
import Router from 'vue-router'
import VueDoc from '@/components/VueDoc'
import Main from '@/components/Main'
import QuestionView from '@/components/QuestionView'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main
    },
    {
      path: '/vue',
      name: 'Vue',
      component: VueDoc
    },
    {
      path: '/projects/:projectId/questions',
      name: 'QuestionView',
      component: QuestionView
    }
  ]
})
