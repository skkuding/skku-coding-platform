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
        <h2 v-b-modal.clarifications-modal @click="getContestAnnouncementList">
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
            :current-page="clarifications_page"
            :fields="clarifications_table_fields">
            <template #cell(Clarifications)="data">
              <p v-html="data.value"/>
            </template>
            <template #cell(created_time)="data">
              {{ getTimeFormat(data.value) }}
            </template>
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
            <template #cell(submission_time)="data">
              {{ getTimeFormat(data.value) }}
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
            <template #cell(submission_time)="data">
              {{ getTimeFormat(data.value) }}
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
        <div id="submission-info-table">
          <b-table borderless class="align-center"
            :items="[submission_detail]"
            :fields="submission_info_table_fields">
          </b-table>
        </div>
        <div id="submssion-source-code">
          <h3>Source Code</h3>
          <p></p>
        </div>
        <div id="submission-detail-table">
          <b-table class="align-center"
            :items="my_submissions"
            :per-page="submission_detail_table_rows"
            :fields="submission_detail_table_fields">
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
      clarifications_table_fields: [
        'Title',
        'Clarifications',
        { label: 'Created Time', key: 'created_time' }
      ],
      submission_table_fields: [
        'Problem',
        { label: 'Submission Time', key: 'submission_time' },
        'Language',
        'User',
        'Result'
      ],

      formFilter: {
        myself: false,
        result: '',
        username: ''
      },

      table_rows: 8,

      submission_info_table_fields: [
        { label: 'Problem', key: 'problem' },
        { label: 'Submission Time', key: 'create_time' },
        { label: 'User', key: 'username' },
        { label: 'Language', key: 'language' },
        { label: 'Result', key: 'result' }
      ],
      submission_detail_table_rows: 5,
      submission_detail_table_fields: [
        { label: '#', key: 'id' },
        { label: 'Result', key: 'result' },
        { label: 'Exec time', key: 'time_cost' },
        { label: 'Memory', key: 'memory_cost' }
      ],
      clarifications_page: 1,
      my_submissions_page: 1,
      all_submissions_page: 1,

      submission_detail_modal_show: false
    }
  },
  async mounted () {
    if (this.$route.params.contestID) {
      await this.getContestProblems()
    }
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
    async getContestAnnouncementList () {
      const result = await api.getContestAnnouncementList(this.contestID)
      const data = result.data.data
      this.clarifications = data.map(v => {
        return {
          Title: v.title,
          Clarifications: v.content,
          created_time: v.create_time
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
          submission_time: v.create_time,
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
    async getSubmissionDetail (submissionID) {
      const res = await api.getSubmission(submissionID)
      let data = res.data.data
      data = {
        ...data,
        ...data.statistic_info,
        result: JUDGE_STATUS[data.result].name
      }

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

        #submission-info-table {
          table {
            color: white;
            font-size: 15px;
          }

          tr th:first-child,
          tr td:first-child {
            padding-left: 40px;
          }

          tr th:last-child,
          tr td:last-child {
            padding-right: 40px;
          }
        }

        #submission-detail-table {
          table {
            color: white;
            border-collapse: collapse;

            th {
              border: none;
            }

            td {
              border-color: #3B4F56;
            }

            tr th:first-child,
            tr td:first-child {
              padding-left: 70px;
            }

            tr th:last-child,
            tr td:last-child {
              padding-right: 70px;
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
