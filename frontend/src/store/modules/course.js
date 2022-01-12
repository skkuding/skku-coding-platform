import moment from 'moment'
import types from '../types'
import api from '@oj/api'
// import { CONTEST_STATUS, USER_TYPE, CONTEST_TYPE } from '@/utils/constants'

const state = {
  now: moment(),
  assignment: {},
  assignmentProblems: []
}

const getters = {
}

const mutations = {
  [types.CHANGE_ASSIGNMENT] (state, payload) {
    state.assignment = payload.assignment
  },
  [types.NOW] (state, payload) {
    state.now = payload.now
  },
  [types.CHANGE_ASSIGNMENT_PROBLEMS] (state, payload) {
    state.assignmentProblems = payload.assignmentProblems
  },
  [types.CHANGE_ASSIGNMENTLIST] (state, payload) {
    state.assignmentList = payload.assignmentList
  }
}

const actions = {
  async getLectureAssignmentList ({ rootState }) {
    const res = await api.getLectureAssignmentList(rootState.route.params.courseID)
    this.commit(types.CHANGE_ASSIGNMENTLIST, { assignmentList: res.data.data })
    return res
  },
  async getLectureAssignment ({ commit, rootState }) {
    const res = await api.getLectureAssignment(rootState.route.params.courseID, rootState.route.params.assignmentID)
    const assignment = res.data.data
    commit(types.CHANGE_ASSIGNMENT, { assignment: assignment })
    commit(types.NOW, { now: moment(assignment.now) })
    return res
  },
  async getLectureAssignmentProblems ({ commit, rootState }) {
    try {
      const res = await api.getLectureAssignmentProblems(rootState.route.params.courseID, rootState.route.params.assignmentID, rootState.route.params.problemID)
      commit(types.CHANGE_ASSIGNMENT_PROBLEMS, { assignmentProblems: res.data.data })
      return res
    } catch (err) {
      commit(types.CHANGE_ASSIGNMENT_PROBLEMS, { assignmentProblems: [] })
      throw err
    }
  }
}

export default {
  state,
  mutations,
  getters,
  actions
}