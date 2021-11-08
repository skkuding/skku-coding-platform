<template>
  <div class="submission">
    <Panel :title="'Submission of ' + problemId + ' ' + problemTitle">
      <div v-if="!submissionList.length">
        No Submissions exists
      </div>
      <b-table
        v-else
        ref="table"
        :items="submissionList"
        :fields="field"
        :per-page="pageSize"
        style="width: 100%"
      >
        <template #cell(studentId)="row">
          {{row.item.student_id}}
        </template>

        <template #cell(name)="row">
          {{row.item.name}}
        </template>

        <template #cell(detail)="row">
          <b-button @click="showSubmissionDetail(row.item.id)" variant="outline-secondary" class="students-button" size="sm">
            <b-icon
              icon="code"
            />
          </b-button>
        </template>
      </b-table>
    </Panel>
    <submission-detail-modal :submission_detail="submissionDetail"/>
  </div>
</template>

<script>
import SubmissionDetailModal from './SubmissionDetail.vue'
import api from '../../api.js'
import time from '@/utils/time'
import { JUDGE_STATUS } from '@/utils/constants'

export default {
  name: 'SubmissionList',
  components: {
    SubmissionDetailModal
  },
  data () {
    return {
      problemId: 'A',
      assignmentId: 0,
      courseId: 0,
      problemTitle: 'Have to be changed',
      pageSize: 250,
      submissionList: [],
      field: [
        { key: 'user_id', label: 'Student ID' },
        { key: 'username', label: 'Name' },
        { key: 'detail', label: 'Detail' }
      ],
      downloadExcludeAdmin: false,
      downloadOnlyLastSubmissions: false,
      submissionDetail: {}
    }
  },
  watch: {
  },
  async created () {
    this.routeName = this.$route.name
    let res
    if (this.routeName === 'contest-problem-submission') {
      res = await api.getContestSubmissionList(this.$route.params.contestId, this.$route.params.problemDisplayId, 0, 250)
    } else {
      res = await api.getSubmissionList(this.$route.params.problemId, 0, 250)
    }
    this.submissionList = res.data.data.results
    for (const submission of this.submissionList) {
      this.$set(submission, 'press', false)
    }
  },
  mounted () {
    this.courseId = this.$route.params.courseId
    this.assignmentId = this.$route.params.assignmentId
    this.problemId = this.$route.params.problemId
    this.problemTitle = this.$route.params.problemTitle
  },
  methods: {
    async showSubmissionDetail (submissionId) {
      await this.getSubmissionDetail(submissionId)
      this.$nextTick(function () {
        this.$bvModal.show('submission-detail-modal')
      })
    },
    async getSubmissionDetail (submissionID) {
      const res = await api.getSubmission(submissionID)
      let data = res.data.data
      if (!this.contestID) {
        delete data.problem
      }
      data = {
        ...data,
        ...data.statistic_info,
        id: data.id.substring(0, 6),
        create_time: time.utcToLocal(data.create_time, 'YYYY-MM-DD HH:mm'),
        bytes: new Blob([data.code]).size,
        testcases: data.info && data.info.data && data.info.data.map(
          tc => {
            return {
              title: tc.test_case,
              result: JUDGE_STATUS[tc.result].name,
              exec_time: tc.real_time,
              memory: tc.memory
            }
          }
        )
      }
      this.submissionDetail = data
    }
  },
  computed: {
  }
}
</script>

<style  scoped lang="scss">
</style>
