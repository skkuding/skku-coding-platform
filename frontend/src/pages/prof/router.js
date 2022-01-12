import Vue from 'vue'
import VueRouter from 'vue-router'

import {
  Login, Home, Dashboard, LectureDashboard, AssignmentList, Problem, ProblemGrade, QnA
} from './views'
Vue.use(VueRouter)

export default new VueRouter({
  mode: 'history',
  base: '/prof/',
  scrollBehavior: () => ({ y: 0 }),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/',
      component: Home,
      children: [
        {
          path: '',
          name: 'dashboard',
          component: Dashboard
        },
        {
          path: '/lecture/:lectureId/dashboard',
          name: 'lecture-dashboard',
          component: LectureDashboard
        },
        {
          path: '/lecture/:lectureId/assignment',
          name: 'lecture-assignment-list',
          component: AssignmentList
        },
        {
          path: '/lecture/:lectureId/assignment/:assignmentId/problem/:problemId/grade',
          name: 'lecture-problem-grade',
          component: ProblemGrade
        },
        {
          path: '/lecture/:lectureId/assignment/:assignmentId/problem/create',
          name: 'create-lecture-problem',
          component: Problem
        },
        {
          path: '/lecture/:lectureId/assignment/:assignmentId/problem/:problemId/edit',
          name: 'edit-lecture-problem',
          component: Problem
        },
        {
          path: '/lecture/:lectureId/QnA',
          name: 'create-contest',
          component: QnA
        }
      ]
    },
    {
      path: '*', redirect: '/login'
    }
  ]
})
