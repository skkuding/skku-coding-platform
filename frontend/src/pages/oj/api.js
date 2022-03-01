import Vue from 'vue'
import store from '@/store'
import axios from 'axios'

Vue.prototype.$http = axios
axios.defaults.baseURL = '/api'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

export default {
  getWebsiteConf (params) {
    return ajax('website/', 'get', {
      params
    })
  },
  getAnnouncementList (offset, limit) {
    const params = {
      offset: offset,
      limit: limit
    }
    return ajax('announcement/', 'get', {
      params
    })
  },
  getAnnouncementDetail (id) {
    return ajax('announcement_detail/', 'get', {
      params: {
        id
      }
    })
  },
  login (data) {
    return ajax('login/', 'post', {
      data
    })
  },
  checkUsernameOrEmail (username, email) {
    return ajax('check_username_or_email/', 'post', {
      data: {
        username,
        email
      }
    })
  },
  register (data) {
    return ajax('register/', 'post', {
      data
    })
  },
  deleteAccount (data) {
    return ajax('delete_account/', 'post', {
      data
    })
  },
  logout () {
    return ajax('logout/', 'get')
  },
  getCaptcha () {
    return ajax('captcha/', 'get')
  },
  getUserInfo (username = undefined) {
    return ajax('profile/', 'get', {
      params: {
        username
      }
    })
  },
  updateProfile (profile) {
    return ajax('profile/', 'put', {
      data: profile
    })
  },
  updateUser (info) {
    return ajax('user/', 'put', {
      data: info
    })
  },
  getUser (username = undefined) {
    return ajax('user/', 'get', {
      params: {
        username
      }
    })
  },
  getSessions () {
    return ajax('sessions/', 'get')
  },
  applyResetPassword (data) {
    return ajax('apply_reset_password/', 'post', {
      data
    })
  },
  resetPassword (data) {
    return ajax('reset_password/', 'post', {
      data
    })
  },
  emailAuth (data) {
    return ajax('email_auth/', 'post', {
      data
    })
  },
  changePassword (data) {
    return ajax('change_password/', 'post', {
      data
    })
  },
  changeEmail (data) {
    return ajax('change_email/', 'post', {
      data
    })
  },
  getLanguages () {
    return ajax('languages/', 'get')
  },
  getProblemTagList () {
    return ajax('problem/tags/', 'get')
  },
  getProblemList (offset, limit, searchParams) {
    const params = {
      paging: true,
      offset,
      limit
    }
    Object.keys(searchParams).forEach(element => {
      if (searchParams[element]) {
        params[element] = searchParams[element]
      }
    })
    return ajax('problem/', 'get', {
      params: params
    })
  },
  getProblem (problemID) {
    return ajax('problem/', 'get', {
      params: {
        problem_id: problemID
      }
    })
  },
  getContestList (offset, limit, searchParams) {
    const params = {
      offset,
      limit
    }
    if (searchParams !== undefined) {
      Object.keys(searchParams).forEach(element => {
        if (searchParams[element]) {
          params[element] = searchParams[element]
        }
      })
    }
    return ajax('contests/', 'get', {
      params
    })
  },
  getContest (id) {
    return ajax('contest/', 'get', {
      params: {
        id
      }
    })
  },
  getContestAccess (contestID) {
    return ajax('contest/access/', 'get', {
      params: {
        contest_id: contestID
      }
    })
  },
  checkContestPassword (contestID, password) {
    return ajax('contest/password/', 'post', {
      data: {
        contest_id: contestID,
        password
      }
    })
  },
  getContestAnnouncementList (contestId) {
    return ajax('contest/announcement/', 'get', {
      params: {
        contest_id: contestId
      }
    })
  },
  getContestProblemList (contestId) {
    return ajax('contest/problem/', 'get', {
      params: {
        contest_id: contestId
      }
    })
  },
  getContestProblem (problemID, contestID) {
    return ajax('contest/problem/', 'get', {
      params: {
        contest_id: contestID,
        problem_id: problemID
      }
    })
  },
  getContestRanking (contestID, forceRefresh, offset, limit) {
    return ajax('contest/rank/', 'get', {
      params: {
        contest_id: contestID,
        force_refresh: forceRefresh,
        offset,
        limit
      }
    })
  },
  submitCode (data) {
    return ajax('submission/', 'post', {
      data
    })
  },
  getSubmissionList (offset, limit, params) {
    params.limit = limit
    params.offset = offset
    return ajax('submissions/', 'get', {
      params
    })
  },
  getContestSubmissionList (offset, limit, params) {
    params.limit = limit
    params.offset = offset
    return ajax('contest_submissions/', 'get', {
      params
    })
  },
  getSubmission (id) {
    return ajax('submission/', 'get', {
      params: {
        id
      }
    })
  },
  submissionExists (problemID) {
    return ajax('submission_exists/', 'get', {
      params: {
        problem_id: problemID
      }
    })
  },
  updateSubmission (data) {
    return ajax('submission/', 'put', {
      data
    })
  },
  getBannerImage () {
    return ajax('banner/', 'get')
  },
  getCourseList () {
    return ajax('lecture/course/', 'get')
  },
  getCourse (courseID) {
    return ajax('lecture/course/', 'get', {
      params: {
        course_id: courseID
      }
    })
  },
  getBookmarkCourseList () {
    return ajax('lecture/course/', 'get', {
      params: {
        bookmark: true
      }
    })
  },
  setBookmark (courseID, bookmark) {
    return ajax('lecture/bookmark_course/', 'put', {
      data: {
        course_id: courseID,
        bookmark: bookmark
      }
    })
  },
  getCourseAssignmentList (courseID, offset, limit) {
    return ajax('lecture/course/assignment/', 'get', {
      params: {
        course_id: courseID,
        paging: true,
        offset,
        limit
      }
    })
  },
  getCourseAssignment (courseID, assignmentID) {
    return ajax('lecture/course/assignment/', 'get', {
      params: {
        course_id: courseID,
        assignment_id: assignmentID
      }
    })
  },
  getCourseAssignmentProblemList (courseID, assignmentID) {
    return ajax('lecture/course/assignment/problem/', 'get', {
      params: {
        course_id: courseID,
        assignment_id: assignmentID
      }
    })
  },
  getCourseAssignmentProblem (assignmentID, problemID) {
    return ajax('lecture/course/assignment/problem/', 'get', {
      params: {
        assignment_id: assignmentID,
        problem_id: problemID
      }
    })
  },
  getAssignmentSubmissionList (offset, limit, params) {
    params.limit = limit
    params.offset = offset
    return ajax('assignment_submissions/', 'get', {
      params
    })
  },
  getGroupList () {
    return ajax('group/', 'get', {
    })
  },
  startProblemBankContest (contestID) {
    return ajax('contest/bank/', 'post', {
      data: {
        contest_id: contestID
      }
    })
  },
  getProblemBankContestProblem (contestID, problemID) {
    return ajax('bank/problem/', 'get', {
      params: {
        problem_id: problemID,
        contest_id: contestID
      }
    })
  },
  getProblemBankParticipation (contestID) {
    return ajax('contest/bank/', 'get', {
      params: {
        contest_id: contestID
      }
    })
  },
  getProblemSetGroup (problemSetGroupID) {
    return ajax('problemset/group/', 'get', {
      params: {
        id: problemSetGroupID
      }
    })
  },
  getProblemSet (problemSetGroupID, problemSetID) {
    return ajax('problemset/', 'get', {
      params: {
        problem_set_group_id: problemSetGroupID,
        id: problemSetID
      }
    })
  },
  createQuestion (data) {
    return ajax('lecture/course/question/', 'post', {
      data
    })
  },
  updateQuestion (data) {
    return ajax('lecture/course/question/', 'put', {
      data
    })
  },
  getQuestionList (params) {
    return ajax('lecture/course/question/', 'get', {
      params
    })
  },
  deleteQuestion (params) {
    return ajax('lecture/course/question/', 'delete', {
      params
    })
  },
  createAnswer (data) {
    return ajax('lecture/course/question/answer/', 'post', {
      data
    })
  },
  updateAnswer (data) {
    return ajax('lecture/course/question/answer/', 'put', {
      data
    })
  },
  getAnswerList (params) {
    return ajax('lecture/course/question/answer/', 'get', {
      params
    })
  },
  deleteAnswer (params) {
    return ajax('lecture/course/question/answer/', 'delete', {
      params
    })
  }
}

/**
 * @param url
 * @param method get|post|put|delete...
 * @param options params: like queryString. if a url is index?a=1&b=2, params = {a: '1', b: '2'}
 * data: post data, use for method put|post
 * @returns {Promise}
 */
async function ajax (url, method, options) {
  if (options !== undefined) {
    var { params = {}, data = {} } = options
  } else {
    params = data = {}
  }
  try {
    const res = await axios({
      url,
      method,
      params,
      data
    })
    if (res.data.error !== null) {
      Vue.prototype.$error(res.data.data)
      if (res.data.data.startsWith('Please login')) {
        store.dispatch('changeModalStatus', { mode: 'login', visible: true })
      }
      throw res
    } else {
      if (method !== 'get') {
        Vue.prototype.$success('Succeeded')
      }
      return res
    }
  } catch (err) {
    Vue.prototype.$error(err.data.data)
    throw err
  }
}
