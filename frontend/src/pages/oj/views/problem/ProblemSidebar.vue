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
          Clarification
        </h2>
        <h2 v-b-modal.my-submissions-modal @click="getMySubmissions">
          <b-icon class="sidebar-icon" icon="person" scale="1.2"/>
          My Submissions
        </h2>
        <h2 v-b-modal.all-submissions-modal @click="getAllSubmissions">
          <b-icon class="sidebar-icon" icon="people" scale="1.2"/>
          All Submissions
        </h2>
        <h2>
          <b-icon class="sidebar-icon" icon="bar-chart-line" scale="1.2"/>
          Standings
        </h2>
      </b-row>
    </b-container>

    <div id="modal-wrapper">
      <b-modal id="clarifications-modal" centered hide-backdrop hide-footer>
        <template #modal-header="{ close }">
          <div class="modal-title-close">
            <h1>Clarifications</h1>
            <b-icon icon="x" scale="3" shift-v="-3" @click="close()"/>
          </div>
        </template>
        <div id="clarifications-table">
          <b-table :items="clarifications"></b-table>
        </div>
      </b-modal>
      <b-modal id="my-submissions-modal" centered hide-backdrop hide-footer>
        <template #modal-header="{ close }">
          <div class="modal-title-close">
            <h1>My Submissions</h1>
            <b-icon icon="x" scale="3" shift-v="-3" @click="close()"/>
          </div>
        </template>
        <div id="my-submissions-table">
          <b-table class="align-center" :items="my_submissions"></b-table>
        </div>
      </b-modal>

      <b-modal id="all-submissions-modal" centered hide-backdrop hide-footer>
        <template #modal-header="{ close }">
          <div class="modal-title-close">
            <h1>All Submissions</h1>
            <b-icon icon="x" scale="3" shift-v="-3" @click="close()"/>
          </div>
        </template>
        <div id="all-submissions-table">
          <b-table class="align-center" :items="all_submissions"></b-table>
        </div>
      </b-modal>

      <b-modal id="submission-detail-modal" centered hide-backdrop hide-footer>
        <template #modal-header="{ close }">
          <div class="modal-title-close">
            <h1>All Submissions</h1>
            <b-icon icon="x" scale="3" shift-v="-3" @click="close()"/>
          </div>
        </template>
        <div id="submission-detail-table">
          <b-table class="align-center" :items="all_submissions"></b-table>
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
  props: {
    hide: Function,
    contestID: String,
    problemID: String
  },
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

      formFilter: {
        myself: false,
        result: '',
        username: ''
      }
    }
  },
  mounted () {
    this.getContestProblems()
  },
  methods: {
    getContestProblems () {
      this.$store.dispatch('getContestProblems').then(res => {
        if (this.isAuthenticated) {
          if (this.contestRuleType === 'ACM') {
            this.addStatusColumn(this.ACMTableColumns, res.data.data)
          } else if (this.OIContestRealTimePermission) {
            this.addStatusColumn(this.ACMTableColumns, res.data.data)
          }
        }
      })
    },
    async getMySubmissions () {
      this.my_submissions = await this.getSubmissions('my')
      console.log(this.my_submissions)
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
      console.log(params)

      // offset, limit, params
      const result = await api[func](0, 1000, params)
      const data = result.data.data
      console.log(result)
      const submissions = data.results.map(v => {
        return {
          ID: v.id,
          Problem: v.problem,
          'Submission Time': time.utcToLocal(v.create_time),
          Language: v.language,
          User: v.username,
          Result: JUDGE_STATUS[v.result].name
        }
      })
      console.log(submissions)
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
    }
  },
  computed: {
    ...mapState({
      contestProblems: state => state.contest.contestProblems
    })
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
      border-radius: 10px;
      background: #24272D;
      color: white;

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
</style>
