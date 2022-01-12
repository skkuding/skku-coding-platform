import Vue from 'vue'
import router from './router'
import axios from 'axios'

Vue.prototype.$http = axios
axios.defaults.baseURL = '/api'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

export default {
  login (username, password) {
    return ajax('login/', 'post', {
      data: {
        username,
        password
      }
    })
  },
  logout () {
    return ajax('logout/', 'get')
  },
  getProfile () {
    return ajax('profile/', 'get')
  },
  getLanguages () {
    return ajax('languages/', 'get')
  },
  getAssignmentSubmission (assignmentId, problemId, offset, limit) {
    return ajax('assignment_submissions_professor/', 'get', {
      params: {
        assignment_id: assignmentId,
        problem_id: problemId,
        offset: offset,
        limit: limit
      }
    })
  },
  getProblemTagList () {
    return ajax('problem/tags/', 'get')
  },
  compileSPJ (data) {
    return ajax('admin/compile_spj/', 'post', {
      data
    })
  },
  getSessions () {
    return ajax('sessions/', 'get')
  },
  createTestCase (data) {
    return ajax('admin/testcase_text/', 'post', {
      data
    })
  },
  getTestCase (id) {
    return ajax('admin/testcase_text/', 'get', {
      params: {
        id
      }
    })
  },
  uploadTestCase (data) {
    return ajax('admin/test_case/', 'post', {
      data
    })
  },
  uploadImage (data) {
    return ajax('admin/upload_image/', 'post', {
      data
    })
  },
  uploadFile (data) {
    return ajax('admin/upload_file/', 'post', {
      data
    })
  },
  getCourseList (courseId, limit, offset) {
    const params = { id: courseId, limit, offset }
    return ajax('lecture/professor/course/', 'get', {
      params
    })
  },
  getBookmarkCourseList (courseId, limit, offset) {
    const params = { id: courseId, limit, offset, bookmark: true }
    return ajax('lecture/professor/course/', 'get', {
      params
    })
  },
  setBookmark (courseID, bookmark) {
    return ajax('lecture/professor/bookmark_course/', 'put', {
      data: {
        course_id: courseID,
        bookmark: bookmark
      }
    })
  },
  createCourse (data) {
    return ajax('lecture/professor/course/', 'post', {
      data
    })
  },
  editCourse (data) {
    return ajax('lecture/professor/course/', 'put', {
      data
    })
  },
  deleteCourse (id) {
    const params = { id: id }
    return ajax('lecture/professor/course/', 'delete', {
      params: params
    })
  },
  getCourseStudents (courseId, limit, offset) {
    const params = { course_id: courseId, limit, offset }
    return ajax('lecture/professor/course/students/', 'get', {
      params: params
    })
  },
  registerStudent (data) {
    return ajax('lecture/professor/course/students/', 'post', {
      data
    })
  },
  deleteStudent (registrationId) {
    const params = { registration_id: registrationId }
    return ajax('lecture/professor/course/students/', 'delete', {
      params: params
    })
  },
  getAssignmentList (courseId, assignmentId, limit, offset) {
    const params = { course_id: courseId, assignment_id: assignmentId, limit, offset }
    return ajax('lecture/professor/course/assignment/', 'get', {
      params: params
    })
  },
  createAssignment (data) {
    return ajax('lecture/professor/course/assignment/', 'post', {
      data
    })
  },
  editAssignment (data) {
    return ajax('lecture/professor/course/assignment/', 'put', {
      data
    })
  },
  deleteAssignment (courseId, assignmentId) {
    const params = { course_id: courseId, assignment_id: assignmentId }
    return ajax('lecture/professor/course/assignment/', 'delete', {
      params: params
    })
  },
  // only assignmentId param => return problemList instead
  getAssignmentProblem (assignmentId, problemId) {
    const params = { problem_id: problemId, assignment_id: assignmentId }
    return ajax('lecture/professor/course/assignment/problem/', 'get', {
      params: params
    })
  },
  createAssignmentProblem (data) {
    return ajax('lecture/professor/course/assignment/problem/', 'post', {
      data
    })
  },
  editAssignmentProblem (data) {
    return ajax('lecture/professor/course/assignment/problem/', 'put', {
      data
    })
  },
  deleteAssignmentProblem (id) {
    const params = { id: id }
    return ajax('lecture/professor/course/assignment/problem/', 'delete', {
      params: params
    })
  },
  addProblemFromPublic (data) {
    return ajax('lecture/professor/course/assignment/add_problem_from_public/', 'post', {
      data
    })
  },
  getDashboardInfo (limit, offset) {
    const params = { limit, offset }
    return ajax('professor/professor_dashboard_info/', 'get', {
      params
    })
  },
  editSubmissionScore (data) {
    return ajax('edit_submission_score/', 'put', {
      data
    })
  }
}

/**
 * @param url
 * @param method get|post|put|delete...
 * @param params like queryString. if a url is index?a=1&b=2, params = {a: '1', b: '2'}
 * @param data post data, use for method put|post
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
        router.push({ name: 'login' })
      }
      throw res
    } else {
      if (method !== 'get' && url !== 'lecture/professor/course/students/') {
        Vue.prototype.$success('Succeeded')
      }
      return res
    }
  } catch (err) {
    Vue.prototype.$error(err.data.data)
    throw err
  }
}
