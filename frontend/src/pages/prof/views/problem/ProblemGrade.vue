<template>
  <div class="flex-grow-1 mx-2" style="max-width: 1300px;">
    <b-breadcrumb :items="pageLocations" class="mt-3"></b-breadcrumb>
    <b-row
      type="flex"
      cols = "1"
      id="problem-grade"
    >
      <b-col>
        <Panel :title="'Assignment'+assignmentId+' - '+problemId+' '+problemTitle">
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

            <template #head(detail)="row">
              <span>
                {{row.label}}
                <b-button class="students-button" style="height: unset;" @click="$bvModal.show('download-submissions-option')">
                  <b-icon icon="download"/>
                </b-button>
              </span>
            </template>

            <template #cell(detail)="row">
              <b-button @click="showSubmissionDetail(row.item)" class="students-button">
                <b-icon
                  icon="code"
                />
              </b-button>
            </template>

            <template #cell(score)="row">
              <div v-if="!row.item.press">
                {{ row.item.statistic_info.score || ' - '}} / 100
                <b-button @click="$set(row.item, 'press', true)" class="students-button" variant="light" press="false" size="sm">
                  <b-icon icon="pencil"/>
                </b-button>
              </div>
              <b-form inline v-else >
                <b-form-input
                  v-model="row.item.newScore"
                  :id="'input-new-score' + row.item.student_id"
                  style="padding-left: 12px; width:53px"
                  size="sm"
                ></b-form-input>
                / 100
                <b-button @click="$set(row.item, 'press', false)" class="students-button"  variant="light" press="false">
                  <b-icon icon="x"/>
                </b-button>
                <b-button v-if="row.item.press" class="students-button" @click="editSubmissionScore(row.item.id, row.item.newScore, row)" variant="light">
                  <b-icon-check/>
                </b-button>
              </b-form>
            </template>
          </b-table>
        </Panel>
      </b-col>
    </b-row>
    <b-modal id="download-submissions-option" title="Download All Submissions" @ok="downloadAllSubmissions">
      Select download options and click ok to download All Submissions.
      <b-form-checkbox v-model="downloadExcludeAdmin">
        Exclude Admin submissions
      </b-form-checkbox>
      <b-form-checkbox v-model="downloadOnlyLastSubmissions">
        Get only last submissions
      </b-form-checkbox>
    </b-modal>
    <submission-detail-modal :submission_detail="submissionDetail"/>
  </div>
</template>

<script>
import SubmissionDetailModal from './SubmissionDetail.vue'
import api from '../../api.js'
import utils from '@/utils/utils'

export default {
  name: 'ProblemGrade',
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
        { key: 'detail', label: 'Detail' },
        { key: 'score', label: 'Score' }
      ],
      pageLocations: [
        {
          text: this.$route.params.courseInfo,
          to: '/course/' + this.$route.params.courseId + '/dashboard'
        },
        {
          text: this.$route.params.assignmentInfo,
          to: '/course/' + this.$route.params.courseId + '/assignment'
        },
        {
          text: this.$route.params.problemId + ' - '
        }
      ],
      downloadExcludeAdmin: false,
      downloadOnlyLastSubmissions: false,
      submissionDetail: {}
    }
  },
  watch: {
  },
  async created () {
    const res = await api.getAssignmentSubmission(this.$route.params.assignmentId, this.$route.params.problemId, 0, 250)
    this.submissionList = res.data.data.results
    for (const submission of this.submissionList) {
      this.$set(submission, 'press', false)
    }
  },
  mounted () {
    this.courseId = this.$route.params.courseId
    this.assignmentId = this.$route.params.assignmentId
    this.problemId = this.$route.params.problemId
    this.problemTitle = this.$route.params.problemInfo
    this.pageLocations[2].text += this.problemTitle
  },
  methods: {
    async downloadAllSubmissions () {
      const url = 'lecture/professor/download_submissions?problem_id=' + this.problemId + '&assignment_id=' + this.assignmentId + '&exclude_admin=' + Number(this.downloadExcludeAdmin) + '&last_submission=' + Number(this.downloadOnlyLastSubmissions)
      await utils.downloadFile(url)
      this.downloadOnlyLastSubmissions = false
      this.downloadExcludeAdmin = false
    },
    async editSubmissionScore (submissionId, newScore, row) {
      const data = {
        id: submissionId,
        score: newScore
      }
      const res = await api.editSubmissionScore(data)
      this.$set(row.item.statistic_info, 'score', res.data.data.statistic_info.score)
      this.$set(row.item, 'press', false)
    },
    showSubmissionDetail (submissionDetail) {
      this.submissionDetail = submissionDetail
      this.$nextTick(function () {
        this.$bvModal.show('submission-detail-modal')
      })
    }
  },
  computed: {
  }
}
</script>

<style  scoped lang="scss">
  #problem-grade {
    margin: auto;
    flex:1 0;
    max-width: 1300px;
  }
</style>
