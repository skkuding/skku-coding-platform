<template>
  <div id="sidebar-container">
    <b-container>
      <b-row class="sidebar-row bottom-border">
        <b-icon icon="x" scale="2.2" @click="hide"/>
      </b-row>
      <b-row class="sidebar-row bottom-border" v-if="$route.name && $route.name.indexOf('contest') != -1">
        <h2>
          <b-icon class="sidebar-icon" icon="hash" scale="1.3" shift-v="1"/>
          Problem List
        </h2>
        <ul id="problem-list">
          <li v-for="(contestProblem, index) of contestProblems" :key="index"
            @click="()=>goContestProblem(contestProblem._id)">
            {{contestProblem.title}}
          </li>
        </ul>
      </b-row>
      <b-row class="sidebar-row bottom-border" v-else-if="$route.name && $route.name.indexOf('assignment') != -1">
        <h2>
          <b-icon class="sidebar-icon" icon="hash" scale="1.3" shift-v="1"/>
          Problem List
        </h2>
        <ul id="problem-list">
          <li v-for="(assignmentProblem, index) of assignmentProblems" :key="index"
            @click="()=>goCourseAssignmentProblem(assignmentProblem._id)">
            {{assignmentProblem.title}}
          </li>
        </ul>
      </b-row>
      <b-row class="sidebar-row">
        <h2 v-if="contestID" v-b-modal.clarifications-modal @click="getContestAnnouncementList">
          <b-icon class="sidebar-icon" icon="question-circle" scale="1.2"/>
          Clarifications
        </h2>
        <h2 v-b-modal.my-submissions-modal @click="getMySubmissions">
          <b-icon class="sidebar-icon" icon="person" scale="1.2"/>
          My Submissions
        </h2>
        <h2 v-b-modal.all-submissions-modal @click="getAllSubmissions">
          <b-icon class="sidebar-icon" icon="people" scale="1.2"/>
          All Submissions
        </h2>
      </b-row>
    </b-container>

    <div id="modal-wrapper">
      <b-modal id="clarifications-modal" class="modal" centered hide-backdrop hide-footer>
        <template #modal-header="{ close }">
          <div class="modal-title-close">
            <h1>Clarifications</h1>
            <b-icon style="cursor: pointer" icon="x" class="close-icon" @click="close()"/>
          </div>
        </template>
        <Table
          lightStyle
          text="No Clarifications"
          :items="clarifications"
          :per-page="table_rows"
          :current-page="clarifications_page"
          :fields="clarifications_table_fields"
        >
          <template v-slot:Problem="data">
            {{ data.row.Problem }}
          </template>
          <template v-slot:Title="data">
            {{ data.row.Title }}
          </template>
          <template v-slot:Clarifications="data">
            <div v-katex>
              <p v-dompurify-html="data.row.Clarifications"/>
            </div>
          </template>
          <template v-slot:created_time="data">
            {{ getTimeFormat(data.row.create_time) }}
          </template>
        </Table>
        <b-pagination class="pagination"
          v-model="clarifications_page"
          :total-rows="clarifications_rows"
          :per-page="table_rows"
        ></b-pagination>
      </b-modal>
      <b-modal id="my-submissions-modal" class="modal" centered hide-backdrop hide-footer>
        <template #modal-header="{ close }">
          <div class="modal-title-close">
            <h1>My Submissions</h1>
            <b-icon style="cursor: pointer" icon="x" class="close-icon" @click="close()"/>
          </div>
        </template>
        <div id="my-submissions-table">
          <Table
            hover
            lightStyle
            :items="my_submissions"
            :per-page="table_rows"
            :current-page="my_submissions_page"
            :fields="submission_table_fields"
            @row-clicked="onMySubmissionClicked"
          >
            <template v-slot:Problem="data">
              {{ data.row.Problem }}
            </template>
            <template v-slot:Language="data">
              {{ data.row.Language }}
            </template>
            <template v-slot:User="data">
              {{ data.row.User }}
            </template>
            <template v-slot:Result="data">
              <span :style="'color: '+resultTextColor(data.row.Result)">{{data.row.Result}}</span>
            </template>
            <template v-slot:submission_time="data">
              {{ getTimeFormat(data.row.submission_time) }}
            </template>
          </Table>
          <b-pagination class="pagination"
            v-model="my_submissions_page"
            :total-rows="my_submissions_rows"
            :per-page="table_rows"
          ></b-pagination>
        </div>
      </b-modal>

      <b-modal id="all-submissions-modal" class="modal" centered hide-backdrop hide-footer>
        <template #modal-header="{ close }">
          <div class="modal-title-close">
            <h1>All Submissions</h1>
            <b-icon style="cursor: pointer" icon="x" class="close-icon" @click="close()"/>
          </div>
        </template>
        <div id="all-submissions-table">
          <Table
            lightStyle
            :items="all_submissions"
            :per-page="table_rows"
            :current-page="all_submissions_page"
            :fields="submission_table_fields">
            <template v-slot:Problem="data">
              {{ data.row.Problem }}
            </template>
            <template v-slot:Language="data">
              {{ data.row.Language }}
            </template>
            <template v-slot:User="data">
              {{ data.row.User }}
            </template>
            <template v-slot:Result="data">
              <span :style="'color: '+resultTextColor(data.row.Result)">{{data.row.Result}}</span>
            </template>
            <template v-slot:submission_time="data">
              {{ getTimeFormat(data.row.submission_time) }}
            </template>
          </Table>
          <b-pagination class="pagination"
            v-model="all_submissions_page"
            :total-rows="all_submissions_rows"
            :per-page="table_rows"
          ></b-pagination>
        </div>
      </b-modal>

      <b-modal id="submission-detail-modal" centered hide-backdrop hide-footer
        v-model="submission_detail_modal_show">
        <template #modal-header="{ close }">
          <div class="modal-title-close">
            <h1>Submission #{{submission_detail.id}}</h1>
            <b-icon style="cursor: pointer" icon="x" class="close-icon" @click="close()"/>
          </div>
        </template>
        <div id="submission-info-table">
          <Table
            lightStyle
            :items="[submission_detail]"
            :fields="submission_info_table_fields"
          >
            <template v-slot:Problem="data">
              {{data.row.Problem}}
            </template>
            <template v-slot:create_time="data">
              {{data.row.create_time}}
            </template>
            <template v-slot:username="data">
              {{data.row.username}}
            </template>
            <template v-slot:language="data">
              {{data.row.language}}
            </template>
            <template v-slot:result="data">
              <span :style="'color: '+resultTextColor(data.row.result)">{{data.row.result}}</span>
            </template>
          </Table>
        </div>
        <div id="submission-compile-error-message" v-if="compile_error_message_show">
          <p class="text-danger"> Compile error message: {{ submission_detail.statistic_info.err_info }} </p>
        </div>
        <div id="submission-source-code">
          <h3>Source Code</h3>
          <p>({{submission_detail.bytes}} Bytes)</p>
          <CodeMirror
            readOnly
            :key="codemirror_key"
            :value="submission_detail.code"
            :language="submission_detail.language"
            theme="material"/>
        </div>
        <div id="submission-detail-table">
          <Table
            :items="submission_detail.testcases"
            :per-page="submission_detail_table_rows"
            :fields="submission_detail_table_fields"
            v-show="submission_detail.testcases">
            <template v-slot:title="data">
              {{data.row.title}}
            </template>
            <template v-slot:exec_time="data">
              {{data.row.exec_time}}
            </template>
            <template v-slot:memory="data">
              {{data.row.memory}}
            </template>
            <template v-slot:result="data">
              <span :style="'color: '+resultTextColor(data.row.result)">{{data.row.result}}</span>
            </template>
          </Table>
        </div>
      </b-modal>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import api from '@oj/api'
import time from '@/utils/time'
import { JUDGE_STATUS } from '@/utils/constants'
import CodeMirror from '@oj/components/CodeMirror.vue'
import Table from '@oj/components/Table.vue'

export default {
  name: 'ProblemSidebar',
  components: {
    CodeMirror,
    Table
  },
  props: {
    hide: Boolean,
    contestID: Number,
    problemID: Number,
    bank: Boolean
  },
  data () {
    return {
      assignmentID: '',
      clarifications: [],
      my_submissions: [],
      all_submissions: [],
      submission_detail: {},

      // Map (key: problem id, value: problem title)
      assignmentProblems: [],
      problem_titles: {},
      clarifications_table_fields: [
        { key: 'Problem' },
        { key: 'Title' },
        { key: 'Clarifications' },
        { label: 'Create Time', key: 'created_time' }
      ],
      submission_table_fields: [
        { label: 'Submission Time', key: 'submission_time' },
        { key: 'Language' },
        { key: 'User' },
        { key: 'Result' }
      ],

      formFilter: {
        myself: false,
        result: '',
        username: ''
      },

      table_rows: 8,

      submission_info_table_fields: [
        { label: 'Submission Time', key: 'create_time' },
        { label: 'User', key: 'username' },
        { label: 'Language', key: 'language' },
        { label: 'Result', key: 'result' }
      ],
      submission_detail_table_rows: 5,
      submission_detail_table_fields: [
        { label: '#', key: 'title' },
        { label: 'Result', key: 'result' },
        { label: 'Exec time', key: 'exec_time' },
        { label: 'Memory', key: 'memory' }
      ],
      clarifications_page: 1,
      my_submissions_page: 1,
      all_submissions_page: 1,

      submission_detail_modal_show: false,
      compile_error_message_show: false,

      // for re-rendering when codemirror content is ready
      codemirror_key: 1
    }
  },
  async mounted () {
    if (this.$route.params.contestID) {
      await this.getContestProblems()
    } else if (this.$route.params.assignmentID) {
      this.assignmentID = this.$route.params.assignmentID
      await this.getCourseAssignmentProblemList()
    }
    if ((this.$route.params.contestID && !this.bank) || this.$route.params.assignmentID) {
      this.submission_table_fields.unshift({ key: 'Problem' })
      this.submission_info_table_fields.unshift({ label: 'Problem', key: 'problem' })
    }
    this.initProblemTitles()
  },
  methods: {
    async getContestProblems () {
      const res = await this.$store.dispatch(this.bank ? 'getProblemBankContestProblems' : 'getContestProblems')
      if (this.isAuthenticated) {
        if (this.contestRuleType === 'ACM') {
          this.addStatusColumn(this.ACMTableColumns, res.data.data)
        } else if (this.OIContestRealTimePermission) {
          this.addStatusColumn(this.ACMTableColumns, res.data.data)
        }
      }
    },
    async getCourseAssignmentProblemList () {
      try {
        const res = await this.$store.dispatch('getCourseAssignmentProblemList')
        this.assignmentProblems = res.data.data.results
      } catch (err) {
      }
    },
    initProblemTitles () {
      if (this.$route.params.contestID) {
        for (let i = 0; i < this.contestProblems.length; i++) {
          this.problem_titles[this.contestProblems[i]._id] = this.contestProblems[i].title
        }
      } else if (this.$route.params.assignmentID) {
        for (let i = 0; i < this.assignmentProblems.length; i++) {
          this.problem_titles[this.assignmentProblems[i]._id] = this.assignmentProblems[i].title
        }
      }
    },
    async getContestAnnouncementList () {
      const result = await api.getContestAnnouncementList(this.contestID)
      const data = result.data.data
      this.clarifications = data.map(v => {
        let problemInfo = ''
        for (const problem of this.contestProblems) {
          if (problem.id === v.problem) {
            problemInfo = problem._id + ' ' + problem.title
          }
        }
        return {
          Title: v.title,
          Clarifications: v.content,
          created_time: v.create_time,
          Problem: problemInfo
        }
      })
    },
    async getMySubmissions () {
      // Initialize problem id-title map
      this.my_submissions = await this.getSubmissions('my')
    },
    async getAllSubmissions () {
      this.all_submissions = await this.getSubmissions('all')
    },
    async getSubmissions (userType) {
      const params = {
        myself: userType === 'my' ? '1' : '0',
        result: '',
        username: '',
        page: 1,
        contest_id: this.contestID,
        problem_id: this.problemID,
        assignment_id: this.assignmentID
      }
      params.contest_id = this.contestID
      params.problem_id = this.problemID
      params.assignment_id = this.assignmentID
      var func
      if (this.contestID && !this.bank) {
        func = 'getContestSubmissionList'
      } else if (this.assignmentID) {
        func = 'getAssignmentSubmissionList'
      } else {
        delete params.contest_id // Problem Bank specified action
        func = 'getSubmissionList'
      }

      // offset, limit, params
      const result = await api[func](0, 100, params)
      const data = result.data.data
      const submissions = data.results.map(v => {
        var info = {
          ID: v.id,
          submission_time: v.create_time,
          Language: v.language,
          User: v.username,
          Result: JUDGE_STATUS[v.result].name
        }
        if (this.contestID || this.assignmentID) {
          this.$set(info, 'Problem', this.problem_titles[v.problem])
          // info.Problem = this.problem_titles[v.problem]
        }
        return info
      })
      return submissions
    },
    async goContestProblem (problemID) {
      await this.$router.push({
        name: 'contest-problem-details',
        params: {
          contestID: this.$route.params.contestID,
          problemID: problemID
        }
      })
    },
    async goCourseAssignmentProblem (problemID) {
      await this.$router.push({
        name: 'lecture-assignment-problem-details',
        params: {
          courseId: this.$route.params.courseID,
          assignmentID: this.$route.params.assignmentID,
          problemID: problemID
        }
      })
    },
    resultTextColor (result) {
      return result === 'Accepted' ? '#8DC63F' : '#FF4F28'
    },
    async onMySubmissionClicked (item) {
      await this.getSubmissionDetail(item.ID)
      this.submission_detail_modal_show = true
      await this.$nextTick()
      this.codemirror_key += 1
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
        result: JUDGE_STATUS[data.result].name,
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
      this.compile_error_message_show = data.result === 'Compile Error'

      if (data.info && data.info.data) {
        // score exist means the submission is OI problem submission
        if (data.info.data[0].score !== undefined) {
          // TODO : 테이블에 Score field 추가
        }
        if (this.isAdminRole) {
          // TODO : 테이블에 Admin Column(Real time, Signal) 추가
        }
      }
      this.submission_detail = data
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-MM-DD HH:mm')
    }
  },
  computed: {
    ...mapState({
      contestProblems: state => state.contest.contestProblems,
      assignmentProblems: state => state.contest.assignmentProblems
    }),
    // Modal table pagination variable
    clarifications_rows () {
      return this.clarifications.length
    },
    my_submissions_rows () {
      return this.my_submissions.length
    },
    all_submissions_rows () {
      return this.all_submissions.length
    }
  }
}
</script>

<style lang="scss" scoped>
  #sidebar-container {
    overflow: auto;
    height: 100%;
    background: #24272D;
    color: white;

    .sidebar-row {
      padding: 15px 15px;
      padding-left: 25px;

      .sidebar-icon {
        margin-right: 7px;
      }

      h2 {
        width: 100%;
        margin-top: 10px;
        margin-bottom: 20px;
        font-size: 18px;
      }

      #problem-list {
        margin-left: 30px;
        cursor: pointer;

        li {
          list-style-type: none;
          margin-top: 10px;
          margin-bottom: 20px;
          font-size: 18px;
          cursor: pointer;
        }
      }
    }

    .bottom-border {
      border-bottom: 1px solid #3B4F56;
    }
  }

  ::v-deep .modal {
    .modal-dialog {
      min-width: 1200px;

      .modal-content {
        color: white;
        border: none;
        border-radius: 10px;
        background: #24272D;
        box-shadow: 0px 0px 15px #000000;

        .modal-header {
          border-bottom: none;

          .modal-title-close {
            width: 100%;
            display: flex;
            flex-direction: row;
            justify-content: space-between;

            h1 {
              display: inline-block;
              margin-top: 10px;
              margin-left: 10px;
              font-size: 35px;
            }

            .close-icon {
              font-size: 60px;
            }
          }
        }

        .modal-body {
          padding: 0;

          #submission-compile-error-message {
            padding: 20px 50px;
          }

          #submission-source-code {
            padding: 20px 50px;
            padding-bottom: 40px;
            color: white;

            h3 {
              font-size: 30px;
              display: inline;
            }
            p {
              font-size: 25px;
            }
          }

          // occasional code indent css fix
          #submission-source-code::v-deep .CodeMirror-sizer {
            margin-left: 38px !important;
          }

          #submission-source-code::v-deep .CodeMirror-gutter-wrapper {
            left: -38px !important;
          }
        }
      }
    }
  }

  ::v-deep .pagination {
    margin-left: 25px;

    .page-link {
      background: #24272D;
      border-color: #3B4F56;
      color: white;
    }
  }
</style>
