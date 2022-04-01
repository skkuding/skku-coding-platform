<template>
  <b-modal id="import-public-problem-modal" @ok="goCreateProblem" title="Add problem from SKKU coding platform" size="xl" class="font-bold">
    <div class="top-bar mb-4" style="margin-top:4px;">
      <h2 class="title">Problem List</h2>
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
              v-model="keyword" @input="filterByKeyword"/>
          </div>
        </div>
      </div>
    </div>
    <div class="table">
      <b-table
        select-mode="single"
        selectable
        hover
        :items="problemList"
        :fields="problemTableColumns"
        :per-page="perPage"
        :current-page="currentPage"
        head-variant="light"
        @row-clicked="selectProblem"
      >
        <template #cell(title)="data">
          {{data.value}}
          <b-icon icon="check2-circle" style="color: #8DC63F;" font-scale="1.2" v-if="data.item.my_status===0"></b-icon>
        </template>
        <template #cell(difficulty)="data">
          <b-icon
            icon="circle-fill"
            class="mr-2"
            :style="'color:' + difficultyColor(data.value)"
          />
          {{ data.value }}
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
        v-model="currentPage"
        :total-rows="rows"
        :per-page="perPage"
        limit="3"
      ></b-pagination>
    </div>
    <template #modal-footer="{ ok }">
      <b-form-input v-model="form.displayId" placeholder="Enter display ID"></b-form-input>
      <b-button size="md" variant="success" @click="ok()">
        Add
      </b-button>
    </template>
  </b-modal>
</template>

<script>
import { mapGetters } from 'vuex'
import api from '@oj/api'
import profApi from '@professor/api'
import { ProblemMixin } from '@oj/components/mixins'
import { DIFFICULTY_COLOR } from '@/utils/constants'

export default {
  name: 'ImportPublicProblem',
  mixins: [ProblemMixin],
  props: ['assignmentId'],
  data () {
    return {
      form: {
        selectedProblemId: null,
        displayId: ''
      },
      perPage: 7,
      currentPage: 1,
      checked: false,
      problemList: [],
      limit: 50,
      total: 0,
      keyword: '',
      difficulty: 'All',
      tag: '',
      page: 1,
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
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      await this.getTagList()
      await this.getProblemList()
    },
    async getTagList () {
      const res = await api.getProblemTagList()
      this.tagList = res.data.data
    },
    async getProblemList () {
      const offset = (this.page - 1) * this.limit
      const res = await api.getProblemList(offset, this.limit,
        {
          difficulty: this.difficulty === 'All' ? '' : this.difficulty,
          keyword: this.keyword,
          tag: this.tag,
          page: this.page
        }
      )
      this.total = res.data.data.total
      this.problemList = res.data.data.results
      if (this.isAuthenticated) {
        this.addStatusColumn(this.problemTableColumns, res.data.data.results)
      }
    },
    async filterByDifficulty (item) {
      this.difficulty = item
      this.page = 1
      await this.getProblemList()
    },
    async filterByKeyword () {
      this.page = 1
      await this.getProblemList()
    },
    difficultyColor (value) {
      return DIFFICULTY_COLOR[value]
    },
    async goProblem (item) {
      await this.$router.push({ name: 'problem-details', params: { problemID: item._id } })
    },
    selectProblem (item) {
      this.form.selectedProblemId = item.id
    },
    async goCreateProblem () {
      if (this.form.selectedProblemId === null || this.form.displayId === '') {
        this.$error('Select Problem and enter display ID!')
        return
      }
      const data = {
        assignment_id: this.assignmentId,
        problem_id: this.form.selectedProblemId,
        display_id: this.form.displayId
      }
      try {
        await profApi.addProblemFromPublic(data)
      } catch (err) {
      }
      this.$set(this.form, 'selectedProblemId', null)
      this.$set(this.form, 'displayId', '')
      this.$emit('update')
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
    float: left;
  }
  .problem-list-card{
    font-family:Manrope;
    .problem-list-table{
      width: 95%;
      margin: 0 auto;
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
