import Vue from 'vue'
import router from './router'
import axios from 'axios'
import utils from '@/utils/utils'

Vue.prototype.$http = axios
axios.defaults.baseURL = '/api'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

export default {
  // 登录
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
  // 获取公告列表
  getAnnouncementList (offset, limit) {
    return ajax('admin/announcement/', 'get', {
      params: {
        paging: true,
        offset,
        limit
      }
    })
  },
  // 删除公告
  deleteAnnouncement (id) {
    return ajax('admin/announcement/', 'delete', {
      params: {
        id
      }
    })
  },
  // 修改公告
  updateAnnouncement (data) {
    return ajax('admin/announcement/', 'put', {
      data
    })
  },
  // 添加公告
  createAnnouncement (data) {
    return ajax('admin/announcement/', 'post', {
      data
    })
  },
  // 获取用户列表
  getUserList (offset, limit, keyword) {
    const params = { paging: true, offset, limit }
    if (keyword) {
      params.keyword = keyword
    }
    return ajax('admin/user/', 'get', {
      params: params
    })
  },
  // 获取单个用户信息
  getUser (id) {
    return ajax('admin/user/', 'get', {
      params: {
        id
      }
    })
  },
  // 编辑用户
  editUser (data) {
    return ajax('admin/user/', 'put', {
      data
    })
  },
  deleteUsers (id) {
    return ajax('admin/user/', 'delete', {
      params: {
        id
      }
    })
  },
  importUsers (users) {
    return ajax('admin/user/', 'post', {
      data: {
        users
      }
    })
  },
  generateUser (data) {
    return ajax('admin/generate_user/', 'post', {
      data
    })
  },
  getBannerImage (id) {
    return ajax('admin/banner/', 'get', {
      params: {
        id
      }
    })
  },
  createBannerImage (data) {
    return ajax('admin/banner/', 'post', { data })
  },
  editBannerImage (data) {
    return ajax('admin/banner/', 'put', { data })
  },
  deleteBannerImage (id) {
    return ajax('admin/banner/', 'delete', {
      params: {
        id
      }
    })
  },
  getLanguages () {
    return ajax('languages/', 'get')
  },
  getSMTPConfig () {
    return ajax('admin/smtp/', 'get')
  },
  createSMTPConfig (data) {
    return ajax('admin/smtp/', 'post', {
      data
    })
  },
  editSMTPConfig (data) {
    return ajax('admin/smtp/', 'put', {
      data
    })
  },
  testSMTPConfig (email) {
    return ajax('admin/smtp_test/', 'post', {
      data: {
        email
      }
    })
  },
  getWebsiteConfig () {
    return ajax('admin/website/', 'get')
  },
  editWebsiteConfig (data) {
    return ajax('admin/website/', 'post', {
      data
    })
  },
  getJudgeServer () {
    return ajax('admin/judge_server/', 'get')
  },
  deleteJudgeServer (hostname) {
    return ajax('admin/judge_server/', 'delete', {
      params: {
        hostname: hostname
      }
    })
  },
  updateJudgeServer (data) {
    return ajax('admin/judge_server/', 'put', {
      data
    })
  },
  getInvalidTestCaseList () {
    return ajax('admin/prune_test_case/', 'get')
  },
  pruneTestCase (id) {
    return ajax('admin/prune_test_case/', 'delete', {
      params: {
        id
      }
    })
  },
  createContest (data) {
    return ajax('admin/contest/', 'post', {
      data
    })
  },
  getContest (id) {
    return ajax('admin/contest/', 'get', {
      params: {
        id
      }
    })
  },
  editContest (data) {
    return ajax('admin/contest/', 'put', {
      data
    })
  },
  deleteContest (id) {
    return ajax('admin/contest/', 'delete', {
      params: {
        id
      }
    })
  },
  getContestList (offset, limit, keyword) {
    const params = { paging: true, offset, limit }
    if (keyword) {
      params.keyword = keyword
    }
    return ajax('admin/contest/', 'get', {
      params: params
    })
  },
  getContestAnnouncementList (contestID) {
    return ajax('admin/contest/announcement/', 'get', {
      params: {
        contest_id: contestID
      }
    })
  },
  createContestAnnouncement (data) {
    return ajax('admin/contest/announcement/', 'post', {
      data
    })
  },
  deleteContestAnnouncement (id) {
    return ajax('admin/contest/announcement/', 'delete', {
      params: {
        id
      }
    })
  },
  updateContestAnnouncement (data) {
    return ajax('admin/contest/announcement/', 'put', {
      data
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
  createProblem (data) {
    return ajax('admin/problem/', 'post', {
      data
    })
  },
  editProblem (data) {
    return ajax('admin/problem/', 'put', {
      data
    })
  },
  deleteProblem (id) {
    return ajax('admin/problem/', 'delete', {
      params: {
        id
      }
    })
  },
  getProblem (id) {
    return ajax('admin/problem/', 'get', {
      params: {
        id
      }
    })
  },
  getProblemList (params) {
    params = utils.filterEmptyValue(params)
    return ajax('admin/problem/', 'get', {
      params
    })
  },
  getContestProblemList (params) {
    params = utils.filterEmptyValue(params)
    return ajax('admin/contest/problem/', 'get', {
      params
    })
  },
  getContestProblem (id) {
    return ajax('admin/contest/problem/', 'get', {
      params: {
        id
      }
    })
  },
  createContestProblem (data) {
    return ajax('admin/contest/problem/', 'post', {
      data
    })
  },
  editContestProblem (data) {
    return ajax('admin/contest/problem/', 'put', {
      data
    })
  },
  deleteContestProblem (id) {
    return ajax('admin/contest/problem/', 'delete', {
      params: {
        id
      }
    })
  },
  makeContestProblemPublic (data) {
    return ajax('admin/contest_problem/make_public/', 'post', {
      data
    })
  },
  addProblemFromPublic (data) {
    return ajax('admin/contest/add_problem_from_public/', 'post', {
      data
    })
  },
  getReleaseNotes () {
    return ajax('admin/versions/', 'get')
  },
  getDashboardInfo () {
    return ajax('admin/dashboard_info/', 'get')
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
  getIPAddress () {
    return ajax('admin/ip_info/', 'get')
  },
  getGroupList () {
    return ajax('admin/group/', 'get')
  },
  getProblemLevelCount () {
    return ajax('admin/problem_level_count/')
  },
  getProblemBankContestProblem (contestID, problemID) {
    return ajax('bank/problem/', 'get', {
      params: {
        problem_id: problemID,
        contest_id: contestID
      }
    })
  },
  getProblemSetGroup (problemSetGroupID) {
    return ajax('admin/problemset/group/', 'get', {
      params: {
        id: problemSetGroupID
      }
    })
  },
  createProblemSetGroup (data) {
    return ajax('admin/problemset/group/', 'post', {
      data
    })
  },
  editProblemSetGroup (data) {
    return ajax('admin/problemset/group/', 'put', {
      data
    })
  },
  deleteProblemSetGroup (problemSetGroupID) {
    return ajax('admin/problemset/group/', 'delete', {
      params: {
        id: problemSetGroupID
      }
    })
  },
  getProblemSet (problemSetGroupID, problemSetID) {
    return ajax('admin/problemset/', 'get', {
      params: {
        problem_set_group_id: problemSetGroupID,
        id: problemSetID
      }
    })
  },
  createProblemSet (data) {
    return ajax('admin/problemset/', 'post', {
      data
    })
  },
  editProblemSet (data) {
    return ajax('admin/problemset/', 'put', {
      data
    })
  },
  deleteProblemSet (problemSetGroupID) {
    return ajax('admin/problemset/', 'delete', {
      params: {
        id: problemSetGroupID
      }
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
