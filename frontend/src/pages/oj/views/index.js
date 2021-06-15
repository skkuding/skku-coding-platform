import ProblemList from './problem/ProblemList.vue'
import AnnouncementList from './announcement/AnnouncementList.vue'
import Announcement from './announcement/Announcement.vue'
import Logout from './user/Logout.vue'
import NotFound from './general/404.vue'
import Home from './general/Home.vue'

// Grouping Components in the Same Chunk
const Problem = () => import(/* webpackChunkName: "Problem" */ '@oj/views/problem/Problem.vue')

const SubmissionList = () => import(/* webpackChunkName: "submission" */ '@oj/views/submission/SubmissionList.vue')
const SubmissionDetails = () => import(/* webpackChunkName: "submission" */ '@oj/views/submission/SubmissionDetails.vue')

const ApplyResetPassword = () => import(/* webpackChunkName: "password" */ '@oj/views/user/ApplyResetPassword.vue')
const ResetPassword = () => import(/* webpackChunkName: "password" */ '@oj/views/user/ResetPassword.vue')

const EmailAuth = () => import(/* webpackChunkName: "emailAuth" */ '@oj/views/user/EmailAuth.vue')

export {
  Home, NotFound,
  Logout, ProblemList, Announcement, AnnouncementList, Problem,
  SubmissionList, SubmissionDetails,
  ApplyResetPassword, ResetPassword, EmailAuth
}
/* 组件导出分为两类, 一类常用的直接导出，另一类诸如Login, Logout等用懒加载,懒加载不在此处导出
 *   在对应的route内加载
 *   见https://router.vuejs.org/en/advanced/lazy-loading.html
 */
