<template>
  <div class="problem-list-card font-bold">
    <div class="top-bar mb-4" style="margin-top:4px;">
      <h2 class="title">Submission List</h2>
      <div class="problem-list-table">
        <div class="category-container">
          <b-dropdown :text="difficulty" class="mr-4">
            <b-dropdown-item @click="filterByDifficulty('All')">All</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level1')">Level1</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level2')">Level2</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level3')">Level3</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level4')">Level4</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level5')">Level5</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level6')">Level6</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level7')">Level7</b-dropdown-item>
          </b-dropdown>
          <div class="col-4">
            <b-icon icon="search" class="search-icon"/>
            <b-input placeholder="keywords" class="search-input"
              v-model="keyword" @input="filterByKeyword"/>
          </div>
        </div>
      </div>
    </div>
    <div class="table">
      <b-table
        hover
        :items="testItemsList"
        :fields="problemTableColumns"
        :per-page="perPage"
        :current-page="currentPage"
        head-variant="light"
        @row-clicked="goProblem"
      >
        <template #cell(result)="data">
          <span style="color: #8DC63F;" v-if="data.item.result==='Accepted'"> {{ data.value }} </span>
          <span style="color: #FF4F28;" v-else> {{ data.value }} </span>
        </template>
        <template #cell(execution)="data">
          <div v-if="data.item.result==='Accepted'">
            <span>{{ data.item.memory }}KB</span> / <span>{{ data.item.time }}ms</span>
          </div>
          <div v-else>
            -
          </div>
        </template>
        <template #cell(code)="data">
          <span>{{ data.item.language }}</span> / <span>{{ data.item.length }}B</span>
        </template>
      </b-table>
    </div>
    <div class="pagination">
      <b-pagination
        v-model="currentPage"
        :total-rows="rows"
        :per-page="perPage"
        limit="3"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import api from '@oj/api'
import { ProblemMixin } from '@oj/components/mixins'
import { DIFFICULTY_COLOR } from '@/utils/constants'

export default {
  name: 'ProfileSubmission',
  mixins: [ProblemMixin],
  data () {
    return {
      perPage: 20,
      currentPage: 1,
      checked: false,
      submissionList: [],
      testItemsList: [
        { title: 'problem1', result: 'Accepted', memory: '30864', time: '68', language: 'Python3', length: '219', date: '2021.1.23' },
        { title: 'problem2', result: 'Wrong Answer', memory: '2024', time: '12', language: 'C++17', length: '718', date: '2021.1.22' },
        { title: 'problem3', result: 'Time Limit Exceed', memory: '2024', time: '12', language: 'C++17', length: '718', date: '2021.1.22' },
        { title: 'problem4', result: 'Runtime Error', memory: '2024', time: '12', language: 'C++17', length: '718', date: '2021.1.21' },
        { title: 'problem5', result: 'Accepted', memory: '2024', time: '12', language: 'C++17', length: '718', date: '2021.1.20' }
      ],
      limit: 50,
      total: 0,
      keyword: '',
      difficulty: 'All',
      tag: '',
      page: 1,
      problemTableColumns: [
        {
          label: 'Title',
          key: 'title',
          tdClass: 'problem-title-field',
          thClass: 'problem-title-field'
        },
        {
          label: 'Result',
          key: 'result',
          tdClass: 'result'
        },
        {
          label: 'Execution',
          key: 'execution'
        },
        {
          label: 'Code',
          key: 'code'
        },
        {
          label: 'Date',
          key: 'date'
        }
      ]
    }
  },
  computed: {
    rows () {
      return this.submissionList.length
    },
    ...mapGetters(['isAuthenticated'])
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      await this.getTagList()
      await this.getSubmissionList()
    },
    async getTagList () {
      const res = await api.getProblemTagList()
      this.tagList = res.data.data
    },
    async getSubmissionList () {
      const offset = (this.page - 1) * this.limit
      const res = await api.getSubmissionList(offset, this.limit,
        {
          difficulty: this.difficulty === 'All' ? '' : this.difficulty,
          keyword: this.keyword,
          tag: this.tag,
          page: this.page
        }
      )
      this.total = res.data.data.total
      this.submissionList = res.data.data.results
      if (this.isAuthenticated) {
        this.addStatusColumn(this.problemTableColumns, res.data.data.results)
      }
    },
    async filterByDifficulty (item) {
      this.difficulty = item
      this.page = 1
      await this.getSubmissionList()
    },
    async filterByKeyword () {
      this.page = 1
      await this.getSubmissionList()
    },
    difficultyColor (value) {
      return DIFFICULTY_COLOR[value]
    },
    async goProblem (item) {
      await this.$router.push({ name: 'problem-details', params: { problemID: item._id } })
    }
  },
  watch: {
    async 'isAuthenticated' (newVal) {
      await this.init()
    }
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .top-bar {
    margin-top: 40px;
    margin-left: 68px;
  }
  .title{
    margin-bottom:0;
    color: #7C7A7B;
    display:inline;
    position:relative;
    top:36px;
  }
  .problem-list-card{
    margin:0 auto;
    width:95%;
    font-family:Manrope;
    .problem-list-table{
      width: 95%;
      margin: 0 auto;
      cursor: pointer;
    }
  }
  div {
    &.pagination{
      margin-right: 5%;
      margin-top: 20px;
      display: flex;
      justify-content: flex-end;
    }
  }
  .category-container{
    display:flex;
    justify-content:flex-end;
  }
  .dropdown-toggle{
    margin-right:2em;
  }

  [type=checkbox]:checked+label:before{
    background-color: #8DC63F !important;
    border-color: #8DC63F !important;
  }
  .problem-title-field{
    width: 25%;
  }
  .dropdown-item{
    font-family: Manrope;
  }
  .search-icon {
    position:absolute;
    top: 11px;
    left: 23px;
  }
  .search-input {
    margin-left: -5px;
    padding-left: 37px;
  }
  .font-bold {
    font-family: manrope_bold;
  }
  .table {
    width:95% !important;
    margin-left:auto;
    margin-right:auto;
  }
</style>
