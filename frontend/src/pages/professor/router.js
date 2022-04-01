import Vue from 'vue'
import VueRouter from 'vue-router'

import {
  Login, Home, Dashboard, CourseDashboard, CourseBookmark, AssignmentList, Problem, ProblemGrade, QnA
} from './views'
Vue.use(VueRouter)

export default new VueRouter({
  mode: 'history',
  base: '/professor/',
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
          path: '/course/:courseId/dashboard',
          name: 'course-dashboard',
          component: CourseDashboard
        },
        {
          path: '/course/professor/bookmark_course',
          name: 'course-bookmark',
          component: CourseBookmark
        },
        {
          path: '/course/:courseId/assignment',
          name: 'course-assignment-list',
          component: AssignmentList
        },
        {
          path: '/course/:courseId/assignment/:assignmentId/problem/:problemId/grade',
          name: 'course-problem-grade',
          component: ProblemGrade
        },
        {
          path: '/course/:courseId/assignment/:assignmentId/problem/create',
          name: 'create-course-problem',
          component: Problem
        },
        {
          path: '/course/:courseId/assignment/:assignmentId/problem/:problemId/edit',
          name: 'edit-course-problem',
          component: Problem
        },
        {
          path: '/course/:courseId/QnA',
          name: 'QnA',
          component: QnA
        }
      ]
    },
    {
      path: '*', redirect: '/login'
    }
  ]
})
