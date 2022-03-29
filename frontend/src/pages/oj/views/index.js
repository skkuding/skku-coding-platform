import ProblemList from './problem/ProblemList.vue'
import ProblemSet from './problem/ProblemSet.vue'
import AnnouncementList from './announcement/AnnouncementList.vue'
import Announcement from './announcement/Announcement.vue'
import Logout from './user/Logout.vue'
import NotFound from './general/404.vue'
import Home from './general/Home.vue'
import ContestRanking from './contest/ContestRanking.vue'
import ContestProblemList from './contest/ContestProblemList.vue'
import LectureList from './lecture/LectureList.vue'
import LectureDashboard from './lecture/LectureDashboard.vue'
import LectureAssignmentList from './lecture/LectureAssignmentList.vue'
import LectureAssignmentDetail from './lecture/LectureAssignmentDetail.vue'
import LectureQna from './lecture/LectureQnA.vue'
import LectureQnaDetail from './lecture/LectureQnADetail.vue'

// Grouping Components in the Same Chunk
const Problem = () => import(/* webpackChunkName: "Problem" */ '@oj/views/problem/Problem.vue')

const ApplyResetPassword = () => import(/* webpackChunkName: "password" */ '@oj/views/user/ApplyResetPassword.vue')
const ResetPassword = () => import(/* webpackChunkName: "password" */ '@oj/views/user/ResetPassword.vue')

const EmailAuth = () => import(/* webpackChunkName: "emailAuth" */ '@oj/views/user/EmailAuth.vue')
const Register = () => import('@oj/views/user/Register.vue')

const ProfileSetting = () => import(/* webpackChunckName: "setting" */ '@oj/views/user/ProfileSetting.vue')

const ContestList = () => import(/* webpackChunkName: "contest" */ '@oj/views/contest/ContestList.vue')
const ContestDetail = () => import(/* webpackChunkName: "contest" */ '@oj/views/contest/ContestDetail.vue')

export {
  Home, NotFound,
  Logout, ProblemList, Announcement, AnnouncementList, Problem, ProblemSet,
  ApplyResetPassword, ResetPassword, EmailAuth, ProfileSetting,
  ContestList, ContestDetail, ContestProblemList, ContestRanking, Register,
  LectureList, LectureDashboard, LectureAssignmentList, LectureAssignmentDetail, LectureQna, LectureQnaDetail
}
/* 구성 요소 내보내기는 두 가지 범주로 나뉩니다.
 *   하나는 일반적으로 직접 내보내기에 사용되며
 *   다른 하나는 로그인, 로그 아웃 등과 같은 lazy-loading이며
 *   여기서 lazy-loading은 내보내지지 않습니다.
 *   https://router.vuejs.org/en/advanced/lazy-loading.html
 */
