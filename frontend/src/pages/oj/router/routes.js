// all routes here.
import {
  AnnouncementList,
  Announcement,
  ContestDetail,
  ContestList,
  ContestProblemList,
  ContestRanking,
  ApplyResetPassword,
  EmailAuth,
  Register,
  Home,
  Logout,
  NotFound,
  Problem,
  ProblemList,
  ProblemSet,
  ResetPassword,
  ProfileSetting,
  LectureList,
  LectureDashboard,
  LectureAssignmentList,
  LectureAssignmentDetail,
  LectureQna,
  LectureQnaDetail
} from '../views'

export default [
  {
    name: 'home',
    path: '/',
    meta: { title: 'Home' },
    component: Home
  },
  {
    name: 'logout',
    path: '/logout',
    meta: { title: 'Logout' },
    component: Logout
  },
  {
    name: 'announcement-list',
    path: '/announcement',
    meta: { title: 'Announcement List' },
    component: AnnouncementList
  },
  {
    name: 'announcement-details',
    path: '/announcement/:announcementID',
    meta: { title: 'Announcement Detail' },
    component: Announcement
  },
  {
    name: 'apply-reset-password',
    path: '/apply-reset-password',
    meta: { title: 'Apply Reset Password' },
    component: ApplyResetPassword
  },
  {
    name: 'reset-password',
    path: '/reset-password/:token',
    meta: { title: 'Reset Password' },
    component: ResetPassword
  },
  {
    name: 'email-auth',
    path: '/email-auth/:token',
    meta: { title: 'Email Authentication' },
    component: EmailAuth
  },
  {
    name: 'register',
    path: '/register/:token',
    meta: { title: 'Register' },
    component: Register
  },
  {
    name: 'problem-list',
    path: '/problem',
    meta: { title: 'Problem List' },
    component: ProblemList
  },
  {
    name: 'problem-details',
    path: '/problem/:problemID',
    meta: { title: 'Problem Details' },
    component: Problem
  },
  {
    name: 'problem-set',
    path: '/problem-set/:problemSetGroupId/:problemSetId',
    meta: { title: 'Problem Set' },
    component: ProblemSet
  },
  {
    name: 'contest-list',
    path: '/contest',
    meta: { title: 'Contest List' },
    component: ContestList
  },
  {
    name: 'contest-problem-details',
    path: '/contest/:contestID/problem/:problemID/',
    component: Problem,
    meta: { title: 'Contest Problem Details' }
  },
  {
    name: 'contest-details',
    path: '/contest/:contestID/',
    component: ContestDetail,
    meta: { title: 'Contest Details' }
  },
  {
    name: 'contest-problems',
    path: '/contest/:contestID/problem',
    component: ContestProblemList,
    meta: { title: 'Contest Problems' }
  },
  {
    name: 'contest-ranking',
    path: '/contest/:contestID/rank/',
    component: ContestRanking,
    meta: { title: 'Contest Ranking' }
  },
  {
    name: 'profile-setting',
    path: '/setting',
    meta: { requiresAuth: true, title: 'Profile Settings' },
    component: ProfileSetting
  },
  {
    name: 'lecture-list',
    path: '/lecture',
    meta: { title: 'Lecture List' },
    component: LectureList
  },
  {
    name: 'lecture-dashboard',
    path: '/lecture/:courseID',
    meta: { title: 'Lecture Dashboard' },
    component: LectureDashboard
  },
  {
    name: 'lecture-assignment',
    path: '/lecture/:courseID/assignment',
    meta: { title: 'Lecture Assignment' },
    component: LectureAssignmentList
  },
  {
    name: 'lecture-assignment-detail',
    path: '/lecture/:courseID/assignment/:assignmentID',
    meta: { title: 'Lecture Assignment Detail' },
    component: LectureAssignmentDetail
  },
  {
    name: 'lecture-assignment-problem-details',
    path: '/lecture/:courseID/assignment/:assignmentID/problem/:problemID',
    component: Problem,
    meta: { title: 'Lecture Assignment Problem Details' }
  },
  {
    name: 'lecture-qna',
    path: '/lecture/:courseID/question',
    meta: { title: 'Lecture QnA' },
    component: LectureQna
  },
  {
    name: 'lecture-qna-detail',
    path: '/lecture/:courseID/question/:questionID',
    meta: { title: 'Lecture QnA Detail' },
    component: LectureQnaDetail
  },
  {
    path: '*',
    meta: { title: '404' },
    component: NotFound
  }
]
