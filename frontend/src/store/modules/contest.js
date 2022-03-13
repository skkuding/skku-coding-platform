import moment from 'moment'
import types from '../types'
import api from '@oj/api'
import { CONTEST_STATUS, USER_TYPE, CONTEST_TYPE } from '@/utils/constants'

const state = {
  now: moment(),
  access: false,
  rankLimit: 30,
  forceUpdate: false,
  contest: {
    created_by: {},
    contest_type: CONTEST_TYPE.PUBLIC
  },
  contestProblems: [],
  itemVisible: {
    menu: true,
    chart: true,
    realName: false
  }
}

const getters = {
  contestLoaded: (state) => {
    return !!state.contest.status
  },
  contestStatus: (state, getters) => {
    if (!getters.contestLoaded) return null
    const startTime = moment(state.contest.start_time)
    const endTime = moment(state.contest.end_time)
    const now = state.now

    if (startTime > now) {
      return CONTEST_STATUS.NOT_START
    } else if (endTime < now) {
      return CONTEST_STATUS.ENDED
    } else {
      return CONTEST_STATUS.UNDERWAY
    }
  },
  contestRuleType: (state) => {
    return state.contest.rule_type || null
  },
  isContestAdmin: (state, getters, _, rootGetters) => {
    return rootGetters.isAuthenticated &&
      (state.contest.created_by.id === rootGetters.user.id || rootGetters.user.admin_type === USER_TYPE.SUPER_ADMIN)
  },
  contestMenuDisabled: (state, getters) => {
    if (getters.isContestAdmin) return false
    if (state.contest.contest_type === CONTEST_TYPE.PUBLIC) {
      return getters.contestStatus === CONTEST_STATUS.NOT_START
    }
    return !state.access
  },
  OIContestRealTimePermission: (state, getters, _, rootGetters) => {
    if (getters.contestStatus === CONTEST_STATUS.ENDED) {
      return true
    }
    return getters.isContestAdmin
  },
  problemSubmitDisabled: (state, getters, _, rootGetters) => {
    if (getters.contestStatus === CONTEST_STATUS.ENDED) {
      return true
    } else if (getters.contestStatus === CONTEST_STATUS.NOT_START) {
      return !getters.isContestAdmin
    }
    return !rootGetters.isAuthenticated
  },
  passwordFormVisible: (state, getters) => {
    return state.contest.contest_type !== CONTEST_TYPE.PUBLIC && !state.access && !getters.isContestAdmin
  },
  contestStartTime: (state) => {
    return moment(state.contest.start_time)
  },
  contestEndTime: (state) => {
    return moment(state.contest.end_time)
  },
  countdown: (state, getters) => {
    if (getters.contestStatus === CONTEST_STATUS.NOT_START) {
      const duration = moment.duration(getters.contestStartTime.diff(state.now, 'seconds'), 'seconds')
      // time is too long
      if (duration.weeks() > 0) {
        return 'Start At ' + duration.humanize()
      }
      const texts = [Math.floor(duration.asHours()), duration.minutes(), duration.seconds()]
      return '-' + texts.join(':')
    } else if (getters.contestStatus === CONTEST_STATUS.UNDERWAY) {
      const duration = moment.duration(getters.contestEndTime.diff(state.now, 'seconds'), 'seconds')
      const texts = [Math.floor(duration.asHours()), duration.minutes(), duration.seconds()]
      return '-' + texts.join(':')
    } else {
      return 'Ended'
    }
  }
}

const mutations = {
  [types.CHANGE_CONTEST] (state, payload) {
    state.contest = payload.contest
  },
  [types.CHANGE_CONTEST_ITEM_VISIBLE] (state, payload) {
    state.itemVisible = { ...state.itemVisible, ...payload }
  },
  [types.CHANGE_RANK_FORCE_UPDATE] (state, payload) {
    state.forceUpdate = payload.value
  },
  [types.CHANGE_CONTEST_PROBLEMS] (state, payload) {
    state.contestProblems = payload.contestProblems
  },
  [types.CHANGE_CONTEST_RANK_LIMIT] (state, payload) {
    state.rankLimit = payload.rankLimit
  },
  [types.CONTEST_ACCESS] (state, payload) {
    state.access = payload.access
  },
  [types.CLEAR_CONTEST] (state) {
    state.contest = { created_by: {} }
    state.contestProblems = []
    state.access = false
    state.itemVisible = {
      menu: true,
      chart: true,
      realName: false
    }
    state.forceUpdate = false
  },
  [types.NOW] (state, payload) {
    state.now = payload.now
  },
  [types.NOW_ADD_1S] (state) {
    state.now = moment(state.now.add(1, 's'))
  }
}

const actions = {
  async getContestList (query) {
    const res = await api.getContestList(0, 20, query)
    const data = res.data.data.results
    const underway = data.filter(contest => contest.status === '0')
    const notunderway = data.filter(contest => contest.status !== '0')
    const contestList = [...underway, ...notunderway]
    return contestList
  },
  async getContest ({ commit, rootState, dispatch }) {
    const res = await api.getContest(rootState.route.params.contestID)
    const contest = res.data.data
    commit(types.CHANGE_CONTEST, { contest: contest })
    commit(types.NOW, { now: moment(contest.now) })
    if (contest.contest_type === CONTEST_TYPE.PRIVATE) {
      dispatch('getContestAccess')
    }
    return res
  },
  async getContestProblems ({ commit, rootState }) {
    try {
      const res = await api.getContestProblemList(rootState.route.params.contestID)
      res.data.data.sort((a, b) => {
        const aId = isNaN(a._id) ? a._id : a._id * 1
        const bId = isNaN(b._id) ? b._id : b._id * 1
        if (aId === bId) {
          return 0
        } else if (aId > bId) {
          return 1
        }
        return -1
      })
      commit(types.CHANGE_CONTEST_PROBLEMS, { contestProblems: res.data.data })
      return res
    } catch (err) {
      commit(types.CHANGE_CONTEST_PROBLEMS, { contestProblems: [] })
      throw err
    }
  },
  async getProblemBankContestProblems ({ commit, rootState }) {
    try {
      const res = await api.getProblemBankContestProblem(rootState.route.params.contestID)
      res.data.data.sort((a, b) => {
        const aId = isNaN(a._id) ? a._id : a._id * 1
        const bId = isNaN(b._id) ? b._id : b._id * 1
        if (aId === bId) {
          return 0
        } else if (aId > bId) {
          return 1
        }
        return -1
      })
      commit(types.CHANGE_CONTEST_PROBLEMS, { contestProblems: res.data.data })
      return res
    } catch (err) {
      commit(types.CHANGE_CONTEST_PROBLEMS, { contestProblems: [] })
      throw err
    }
  },
  async getContestAccess ({ commit, rootState }) {
    const res = await api.getContestAccess(rootState.route.params.contestID)
    commit(types.CONTEST_ACCESS, { access: res.data.data.access })
    return res
  }
}

export default {
  state,
  mutations,
  getters,
  actions
}
