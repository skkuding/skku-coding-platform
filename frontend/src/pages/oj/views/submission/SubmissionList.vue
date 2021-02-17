<template>
  <div>
    <b-button @click="show_my=true; formFilter.myself=true; getSubmissions()" variant="primary">My Submission</b-button>
    <b-button @click="show_all=true; formFilter.myself=false; getSubmissions()" variant="primary">All Submission</b-button>
    <b-modal
      modal-class="my-submission"
      size="xl"
      v-model="show_my"
      title="My Submissions"
      hide-footer="true"
    >
    <b-table class="my-submission-table"
      @row-clicked="rowClicked"
      :items="my_sub" />
    </b-modal>
    <b-modal
      modal-class="all-submission"
      size="xl"
      v-model="show_all"
      title="All Submissions"
      hide-footer="true"
    >
    <b-table class="all-submission-table" :items="all_sub" />
    </b-modal>
    <b-modal
      modal-class="submission-detail"
      size="lg"
      v-model="show_detail"
      title="Submissions Detail"
      hide-footer="true"
    >
      <Highlight :language="language">{{ code }}</Highlight>
      <b-table class="submission-table" :items="sub_detail"></b-table>
    </b-modal>
  </div>
</template>

<script>
import api from '@oj/api'
import hljs from 'highlight.js'
import time from '@/utils/time'
import { JUDGE_STATUS } from '@/utils/constants'
import Highlight from 'vue-highlight-component'

hljs.registerLanguage('cpp', require('highlight.js/lib/languages/cpp'))

export default {
  components: {
    Highlight
  },
  data () {
    return {
      my_sub: [],
      all_sub: [],
      show_my: false,
      show_all: false,
      show_detail: false,
      loadingTable: false,
      total: 30,
      limit: 12,
      page: 1,
      contestID: '',
      problemID: '',
      routeName: '',
      rejudge_column: false,
      formFilter: {
        myself: false,
        result: '',
        username: ''
      },
      code: '',
      language: ''
    }
  },
  mounted () {
    this.init()
  },
  methods: {
    init () {
      this.contestID = this.$route.params.contestID
      const query = this.$route.query
      this.problemID = query.problemID
      this.formFilter.myself = query.myself === '1'
      this.formFilter.result = query.result || ''
      this.formFilter.username = query.username || ''
      this.page = parseInt(query.page) || 1
      if (this.page < 1) {
        this.page = 1
      }
      this.routeName = this.$route.name
      this.getSubmissions()
    },
    rowClicked (record) {
      this.show_detail = true
      api.getSubmission(record.ID).then(res => {
        const data = res.data.data
        this.code = data.code
        this.language = data.language
      })
    },
    buildQuery () {
      return {
        myself: this.formFilter.myself === true ? '1' : '0',
        result: this.formFilter.result,
        username: this.formFilter.username,
        page: this.page
      }
    },
    getSubmissions () {
      const params = this.buildQuery()
      params.contest_id = this.contestID
      params.problem_id = this.problemID
      const offset = (this.page - 1) * this.limit
      const func = this.contestID ? 'getContestSubmissionList' : 'getSubmissionList'
      this.loadingTable = true
      api[func](offset, this.limit, params).then(res => {
        const data = res.data.data
        const refined = []
        for (const v of data.results) {
          refined.push({
            ID: v.id,
            Problem: v.problem,
            'Submission Time': time.utcToLocal(v.create_time),
            Language: v.language,
            User: v.username,
            Result: JUDGE_STATUS[v.result].name
          })
        }
        this.loadingTable = false
        if (this.formFilter.myself === true) {
          this.my_sub = refined
        } else {
          this.all_sub = refined
        }
        this.total = data.total
      }).catch(() => {
        this.loadingTable = false
      })
    }
  }
}
</script>
<style lang="scss">

.modal-content{
  background-color: #24272d !important;
}
.modal-body{
  padding: 0 !important;
}
.modal-header{
  border-bottom: 0 !important;
  padding-left: 30px !important;
}
.modal-title{
  font-family: 'Manrope', sans-serif;
  font-weight: bolder;
  font-size: 35px;
  color: #d2d2d2;
}
.table{
  margin: 0;
  color:#d2d2d2;
}
button.close{
  color: white;
  font-size: 50px;
  font-weight: lighter;
}
th {
  font-family: 'Manrope', sans-serif;
  font-weight: bold;
  font-size: 20px;
  color: #d2d2d2;
  border-top: 0 !important;
  border-bottom: 0 !important;
  vertical-align: middle !important;
  text-align: center !important;
}
td {
  font-family: 'Manrope', sans-serif;
  font-weight: lighter;
  font-size: 20px;
  color: #d2d2d2;
  border-top-color: #3b4f56 !important;
  height: 70px;
  vertical-align: middle !important;
  text-align: center !important;
}
.hljs{
  background: #24272d !important;
}
</style>
<style src="highlight.js/styles/night-owl.css"></style>
