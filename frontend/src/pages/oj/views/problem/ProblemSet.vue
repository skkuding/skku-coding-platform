<template>
  <div class="problem-list-card font-bold">
    <button class="mt-8" @click="goProblemList">&lt;&lt; Back</button>
    <div class="text-2xl flex items-center mt-6" :style="`color: ${problemSet.color}`">
      <div class="ellipse" :style="`background-color: ${problemSet.color}`"></div>
      <h4 class="-ml-10 text-stroke-white">{{ problemSetGroup.title }} - {{ problemSet.title }}</h4>
    </div>
    <div class="mb-4 flex justify-between flex-row-reverse">
      <div class="my-auto">
        <div class="category-container">
          <div class="tags">
            tags
            <b-form-checkbox
              v-model="checked"
              name="check-button"
              switch
              class="ml-2"
            >
            </b-form-checkbox>
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
        @row-clicked="goProblem"
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
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import api from '@oj/api'
import { ProblemMixin } from '@oj/components/mixins'
import { DIFFICULTY_COLOR } from '@/utils/constants'

export default {
  name: 'ProblemSetGroup',
  mixins: [ProblemMixin],
  props: {
  },
  components: {
  },
  data () {
    return {
      perPage: 20,
      currentPage: 1,
      checked: false,
      problemList: [],
      limit: 50,
      total: 0,
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
      ],
      problemSetId: 0,
      problemSet: [],
      problemSetGroup: {}
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
      this.problemSetId = this.$route.params.problemSetId
      this.problemSetGroupId = this.$route.params.problemSetGroupId
      await this.getProblemSetGroup()
      await this.getProblemSet()
      await this.getTagList()
      await this.getProblemList()
    },
    async getProblemSetGroup () {
      const res = await api.getProblemSetGroup(this.problemSetGroupId)
      this.problemSetGroup = res.data.data
    },
    async getProblemSet () {
      const res = await api.getProblemSet(this.problemSetGroupId, this.problemSetId)
      this.problemSet = res.data.data
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
          page: this.page,
          problem_set_id: this.problemSetId
        }
      )
      this.total = res.data.data.total
      this.problemList = res.data.data.results
      if (this.isAuthenticated) {
        this.addStatusColumn(this.problemTableColumns, res.data.data.results)
      }
    },
    difficultyColor (value) {
      return DIFFICULTY_COLOR[value]
    },
    async goProblem (item) {
      await this.$router.push({ name: 'problem-details', params: { problemID: item._id } })
    },
    async goProblemList () {
      await this.$router.push({ name: 'problem-list' })
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
  .problem-list-card{
    margin:0 auto;
    width:70%;
    font-family:Manrope;
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
    justify-content: flex-end;
  }
  .dropdown-toggle{
    margin-right:2em;
  }
  .tags{
    display: flex;
    align-items: center;
    font-family: Manrope;
    cursor: default;
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
  ::v-deep .table {
    width:100%
    td {
      cursor: pointer;
    }
  }
  .ellipse {
    height: 60px;
    width: 60px;
    margin: auto 10px;
    border-radius: 50%;
    align-items: center;
    justify-content: center;
  }
  .text-stroke-white {
     text-shadow:
      -1.5px -1.5px 0 white,
      1.5px -1.5px 0 white,
      -1.5px 1.5px 0 white,
      1.5px 1.5px 0 white;
  }
</style>
