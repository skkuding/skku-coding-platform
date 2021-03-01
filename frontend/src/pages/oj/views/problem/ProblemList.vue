<template>
  <div class="problem-list-card font-bold">
    <div class="top-bar mb-4" style="margin-top:4px;">
      <h2 class="title">Problem List</h2>
      <div class="problem-list-table">
        <div class="category-container">
          <b-dropdown :text="selectedDifficulty" class="mr-4">
            <b-dropdown-item @click="filterByDifficulty()">All</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level1')">Level1</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level2')">Level2</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level3')">Level3</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level4')">Level4</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level5')">Level5</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level6')">Level6</b-dropdown-item>
            <b-dropdown-item @click="filterByDifficulty('Level7')">Level7</b-dropdown-item>
          </b-dropdown>
            <div class="tags mr-4">
              tags
              <b-form-checkbox
                v-model="checked"
                name="check-button"
                switch
                class="ml-2"
              >
              </b-form-checkbox>
            </div>
          <div class="col-4">
            <b-icon icon="search" class="search-icon"/>
            <b-input placeholder="keywords" class="search-input"
              v-model="query.keyword" @input="filterByKeyword"/>
          </div>
        </div>
      </div>
    </div>
    <div class="table">
      <b-table
        hover
        :items="problemList"
        :fields="problemTableColumns"
        :per-page="perPage"
        :current-page="currentPage"
        head-variant="light"
        :loading="loadings.table"
        @row-clicked="goProblem"
      >
        <template #cell(title)="data">
          {{data.value}}
          <b-icon icon="check2-circle" style="color: #8DC63F;" font-scale="1.2" v-if="data.item.my_status===0"></b-icon>
        </template>
        <template #cell(AC_Rate)="data">
          {{ getACRate(data.item.accepted_number, data.item.submission_number) }}
        </template>
        <template v-slot:cell(tags)="data">
          <span v-show="checked" v-for="item in data.item.tags" :key="item.id">{{ item }}  </span>
        </template>
        <template v-slot:head(tags)="field">
          <div v-show="checked">{{ field.label }}</div>
        </template>
      </b-table>
    </div>
    <div class="pagination">
      <b-pagination
        aria-controls="notice-list"
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
import utils from '@/utils/utils'
import { ProblemMixin } from '@oj/components/mixins'

export default {
  name: 'problemList',
  mixins: [ProblemMixin],
  data () {
    return {
      selectedDifficulty: 'Difficulty',
      perPage: 10,
      currentPage: 1,
      checked: false,
      listVisible: true,
      problemList: [],
      limit: 20,
      total: 0,
      loadings: {
        table: true,
        tag: true
      },
      routeName: '',
      query: {
        keyword: '',
        difficulty: '',
        tag: '',
        page: 1
      },
      problemTableColumns: [
        {
          label: '#',
          key: '_id'
        },
        {
          label: 'Title',
          key: 'title',
          tdClass: 'problem-title-field',
          thClass: 'problem-title-field'
        },
        {
          label: 'Level',
          key: 'difficulty',
          tdClass: 'levelCircle'
        },
        {
          label: 'Submissions',
          key: 'submission_number'
        },
        'AC_Rate',
        {
          label: 'Tags',
          key: 'tags'
        }
      ]
    }
  },
  computed: {
    rows () {
      return this.problemList.length
    },
    ...mapGetters(['isAuthenticated'])
  },
  mounted () {
    this.init()
  },
  methods: {
    init (simulate = false) {
      this.routeName = this.$route.name
      const query = this.$route.query
      this.query.difficulty = query.difficulty || ''
      this.query.keyword = query.keyword || ''
      this.query.tag = query.tag || ''
      this.query.page = parseInt(query.page) || 1
      if (this.query.page < 1) {
        this.query.page = 1
      }
      if (!simulate) {
        this.getTagList()
      }
      this.getProblemList()
    },
    pushRouter () {
      this.$router.push({
        name: 'problem-list',
        query: utils.filterEmptyValue(this.query)
      })
    },
    getProblemList () {
      const offset = (this.query.page - 1) * this.limit
      this.loadings.table = true
      api.getProblemList(offset, this.limit, this.query).then(res => {
        this.loadings.table = false
        this.total = res.data.data.total
        this.problemList = res.data.data.results
        if (this.isAuthenticated) {
          this.addStatusColumn(this.problemTableColumns, res.data.data.results)
        }
      }, res => {
        this.loadings.table = false
      })
    },
    getTagList () {
      api.getProblemTagList().then(res => {
        this.tagList = res.data.data
        this.loadings.tag = false
      }, res => {
        this.loadings.tag = false
      })
    },
    filterByDifficulty (item) {
      if (item === undefined) {
        this.selectedDifficulty = 'All'
      } else {
        this.selectedDifficulty = item
      }
      this.query.difficulty = item
      this.query.page = 1
      this.pushRouter()
    },
    filterByKeyword () {
      this.query.page = 1
      this.pushRouter()
    },
    levelCircle (value) {
      return 'level' + value[5] + '-circle'
    },
    goProblem (item) {
      this.$router.push({ name: 'problem-details', params: { problemID: item._id } })
    }
  },
  watch: {
    '$route' (newVal, oldVal) {
      if (newVal !== oldVal) {
        this.init(true)
      }
    },
    'isAuthenticated' (newVal) {
      if (newVal === true) {
        this.init()
      }
    }
  }
}
</script>

<style lang="less" scoped>
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
    width:90%;
    font-family:Manrope;
  }
  .problem-list-card .problem-list-table{
    width: 95%;
    margin: 0 auto;
  }
  div.pagination{
    margin-right: 5%;
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
  .category-container{
    display:flex;
    justify-content:flex-end;
  }
  .dropdown-toggle{
    margin-right:2em;
  }
  .tags{
    display: flex;
    align-items: center;
    font-family: Manrope;
  }
  [type=checkbox]:checked+label:before{
    background-color: #8DC63F !important;
    border-color: #8DC63F !important;
  }
  .problem-title-field{
    width: 25%;
  }

  /deep/ .table {
    & .level1-circle::before {
      content: '●';
      color: #CC99C9;
      margin-right: 10px;
    }
    & .level2-circle::before{
      content: '●';
      color: #9EC1CF;
      margin-right: 10px;
    }
    & .level3-circle::before{
      content: '●';
      color: #A1F2C2;
      margin-right: 10px;
    }
    & .level4-circle::before{
      content: '●';
      color: #B8FF81;
      margin-right: 10px;
    }
    & .level5-circle::before{
      content: '●';
      color: #F3EC53;
      margin-right: 10px;
    }
    & .level6-circle::before{
      content: '●';
      color: #FEB144;
      margin-right: 10px;
    }
    & .level7-circle::before{
      content: '●';
      color: #FF6663;
      margin-right: 10px;
    }
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
  .tags {
    color:#767676;
  }
</style>
