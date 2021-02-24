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
      <b-row class="sidebar-row">
        <h2 v-b-modal.clarifications-modal>
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
            <b-icon icon="x" scale="4" shift-v="-15" shift-h="-10" @click="close()"/>
          </div>
        </template>
        <div id="clarifications-table">
          <b-table
            class="align-center"
            :items="clarifications"
            :per-page="table_rows"
            :current-page="clarifications_page">
          </b-table>
          <b-pagination class="pagination"
            v-model="clarifications_page"
            :total-rows="clarifications_rows"
            :per-page="table_rows"
          ></b-pagination>
        </div>
      </b-modal>
      <b-modal id="my-submissions-modal" class="modal" centered hide-backdrop hide-footer>
        <template #modal-header="{ close }">
          <div class="modal-title-close">
            <h1>My Submissions</h1>
            <b-icon icon="x" scale="4" shift-v="-15" shift-h="-10" @click="close()"/>
          </div>
        </template>
        <div id="my-submissions-table">
          <b-table
            class="align-center"
            :items="my_submissions"
            :per-page="table_rows"
            :current-page="my_submissions_page"
            :fields="submission_table_fields"
            @row-clicked="onMySubmissionClicked">
            <!-- Custom rendering for result text color -->
            <template #cell(result)="data">
              <span :style="'color: '+resultTextColor(data.item.Result)">{{data.item.Result}}</span>
            </template>
          </b-table>
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
            <b-icon icon="x" scale="4" shift-v="-15" shift-h="-10" @click="close()"/>
          </div>
        </template>
        <div id="all-submissions-table">
          <b-table
            class="align-center"
            :items="all_submissions"
            :per-page="table_rows"
            :current-page="all_submissions_page"
            :fields="submission_table_fields">
            <template #cell(result)="data">
              <span :style="'color: '+resultTextColor(data.item.Result)">{{data.item.Result}}</span>
            </template>
          </b-table>
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
            <b-icon icon="x" scale="4" shift-v="-15" shift-h="-10" @click="close()"/>
          </div>
        </template>
        <div>
          <span>{{submission_detail.problem_title}}</span>
          <span>{{submission_detail.submission_time}}</span>
          <span>{{submission_detail.username}}</span>
          <span>{{submission_detail.language}}</span>
          <span>{{submission_detail.result}}</span>
          <span>{{submission_detail.code_length}}</span>
          <span>{{submission_detail.code}}</span>
          <span></span>
        </div>
        <div id="submission-detail-table">
          <b-table class="align-center"
            :items="my_submissions"
            :per-page="submission_detail_table_rows"
            :fields="submission_table_fields">
            <template #cell(result)="data">
              <span :style="'color: '+resultTextColor(data.item.Result)">{{data.item.Result}}</span>
            </template>
          </b-table>
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

export default {
  name: 'ProblemSidebar',
  components: {

  },
  props: ['hide', 'contestID', 'problemID'],
  data () {
    return {
      clarifications: [],
      my_submissions: [],
      all_submissions: [],
      submission_detail: {
        id: '',
        code: '',
        language: ''
      },

      // Map (key: problem id, value: problem title)
      problem_titles: {},
      submission_table_fields: ['Problem', 'Submission Time', 'Language', 'User', 'Result'],

      formFilter: {
        myself: false,
        result: '',
        username: ''
      },

      // Modal table pagination
      table_rows: 8,
      submission_detail_table_rows: 5,
      clarifications_page: 1,
      my_submissions_page: 1,
      all_submissions_page: 1,

      submission_detail_modal_show: false
    }
  },
  async mounted () {
    await this.getContestProblems()
    this.initProblemTitles()
  },
  methods: {
    async getContestProblems () {
      const res = await this.$store.dispatch('getContestProblems')

      if (this.isAuthenticated) {
        if (this.contestRuleType === 'ACM') {
          this.addStatusColumn(this.ACMTableColumns, res.data.data)
        } else if (this.OIContestRealTimePermission) {
          this.addStatusColumn(this.ACMTableColumns, res.data.data)
        }
      }
    },
    initProblemTitles () {
      for (let i = 0; i < this.contestProblems.length; i++) {
        this.problem_titles[this.contestProblems[i]._id] = this.contestProblems[i].title
      }
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
        problem_id: this.problemID
      }
      params.contest_id = this.contestID
      params.problem_id = this.problemID
      const func = this.contestID ? 'getContestSubmissionList' : 'getSubmissionList'

      // offset, limit, params
      const result = await api[func](0, 1000, params)
      const data = result.data.data
      const submissions = data.results.map(v => {
        return {
          ID: v.id,
          Problem: this.problem_titles[v.problem],
          'Submission Time': time.utcToLocal(v.create_time),
          Language: v.language,
          User: v.username,
          Result: JUDGE_STATUS[v.result].name
        }
      })
      return submissions
    },
    goContestProblem (problemID) {
      this.$router.push({
        name: 'contest-problem-details',
        params: {
          contestID: this.$route.params.contestID,
          problemID: problemID
        }
      })
    },
    resultTextColor (result) {
      return result === 'Accepted' ? '#8DC63F' : '#FF4F28'
    },
    async onMySubmissionClicked (item, index, event) {
      await this.getSubmissionDetail(item.ID)
      this.submission_detail_modal_show = true
    },
    async getSubmissionDetail (problemID) {
      const res = await api.getSubmission(problemID)
      const data = res.data.data

      if (data.info && data.info.data) {
        // score exist means the submission is OI problem submission
        if (data.info.data[0].score !== undefined) {
          // TODO : 테이블에 Score field 추가
        }
        if (this.isAdminRole) {
          // TODO : 테이블에 Admin Column(Real time, Signal) 추가
        }
      }
      this.submissionDetail = data
    }
  },
  computed: {
    ...mapState({
      contestProblems: state => state.contest.contestProblems
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

<style lang="less" scoped>

#sidebar-container {
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

      li {
        list-style-type: none;
        margin-top: 10px;
        margin-bottom: 20px;
        font-size: 18px;
      }
    }
  }

  .bottom-border {
    border-bottom: 1px solid #3B4F56;
  }
}

/deep/ .modal {
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
        }
      }

      .modal-body {
        padding: 0;

        #clarifications-table {
          table {
            color: white;

            th {
              min-width: 230px;
              padding: 15px 25px;
              border: none;
            }

            td {
              min-width: 230px;
              padding: 15px 25px;
              border-top: 1px solid #3B4F56;
            }
          }
        }

        #my-submissions-table, #all-submissions-table {
          table {
            color: white;

            th {
              min-width: 100px;
              padding: 15px 25px;
              border: none;
            }

            td {
              min-width: 100px;
              padding: 15px 25px;
              border-top: 1px solid #3B4F56;
            }
          }
        }
      }
    }
  }
}

/deep/ .pagination {
  margin-left: 25px;

  .page-link {
    background: #24272D;
    border-color: #3B4F56;
    color: white;
  }
}
</style>
