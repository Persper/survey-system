import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main'
import Entry from '@/components/Entry'
import QuestionView from '@/components/QuestionView'
import ReviewView from '@/components/ReviewView'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main
    },
    {
      path: '/entry/:token',
      name: 'Entry',
      component: Entry
    },
    {
      path: '/projects/:projectId/questions',
      name: 'QuestionView',
      component: QuestionView
    },
    {
      path: '/projects/:projectId/reviews',
      name: 'ReviewView',
      component: ReviewView
    }
  ]
})
