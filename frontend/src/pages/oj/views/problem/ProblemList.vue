<template>
  <div class="problem-list-card">
    <h1 class="title">Problem List</h1>
    <div class="problem-list-table">
      <div class="category-container mb-2">
        <b-dropdown text="Difficulty">
          <b-dropdown-item @click="filterByDifficulty()">All</b-dropdown-item>
          <b-dropdown-item @click="filterByDifficulty('Level1')">Level1</b-dropdown-item>
          <b-dropdown-item @click="filterByDifficulty('Level2')">Level2</b-dropdown-item>
          <b-dropdown-item @click="filterByDifficulty('Level3')">Level3</b-dropdown-item>
          <b-dropdown-item @click="filterByDifficulty('Level4')">Level4</b-dropdown-item>
          <b-dropdown-item @click="filterByDifficulty('Level5')">Level5</b-dropdown-item>
          <b-dropdown-item @click="filterByDifficulty('Level6')">Level6</b-dropdown-item>
          <b-dropdown-item @click="filterByDifficulty('Level7')">Level7</b-dropdown-item>
        </b-dropdown>
        <div class="tags">
          <b-form-checkbox
            v-model="checked"
            name="check-button"
            switch
            class="mr-2"
          >
            Tags
          </b-form-checkbox>
        </div>
        <b-input-group class="col-4">
          <b-input-group-prepend is-text>
            <b-icon icon="search"></b-icon>
          </b-input-group-prepend>
          <b-form-input placeholder="keywords" v-model="query.keyword" @input="filterByKeyword"></b-form-input>
        </b-input-group>
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
        >
          <template #cell(title)="data">
            {{data.value}}
            <b-icon icon="check2-circle" style="color: #8DC63F;" v-if="data.item.accepted_number>=0"></b-icon>
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
          key: 'title',
          label: 'Title',
          tdClass: 'problem-title-field',
          thClass: 'problem-title-field'
        },
        {
          key: 'difficulty',
          label: 'Level',
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
      this.query.difficulty = item
      this.query.page = 1
      this.pushRouter()
    },
    filterByKeyword () {
      this.query.page = 1
      this.pushRouter()
    },
    levelCircle (value) {
      switch (value) {
        case 'Level2':
          return 'level2-circle'
        case 'Level3':
          return 'level3-circle'
        case 'Level4':
          return 'level4-circle'
        case 'Level5':
          return 'level5-circle'
        case 'Level6':
          return 'level6-circle'
        case 'Level7':
          return 'level7-circle'
        default:
          return 'level1-circle'
      }
    },
    pickone () {
      api.pickone().then(res => {
        this.$success('Good Luck')
        this.$router.push({ name: 'problem-details', params: { problemID: res.data.data } })
      })
    },
    test_keydown_handler (event) {
      if (event.which === 13) {
        this.filterByKeyword()
      }
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

<style>
  .title{
    margin-top: 100px;
  }
  .problem-list-card{
    margin:0 auto;
    width:90%;
  }
  .problem-list-card .problem-list-table{
    width: 95%;
    margin: 0 auto;
  }
  .pagination{
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
  }
  [type=checkbox]:checked+label:before{
    background-color: #8DC63F !important;
    border-color: #8DC63F !important;
  }
  .problem-title-field{
    width: 25%;
  }
  .level1-circle::before{
    content: '●';
    color: #CC99C9;
    margin-right: 10px;
    font-size: 25px;
  }
  .level2-circle::before{
    content: '●';
    color: #9EC1CF;
    margin-right: 10px;
    font-size: 25px;
  }
  .level3-circle::before{
    content: '●';
    color: #A1F2C2;
    margin-right: 10px;
    font-size: 25px;
  }
  .level4-circle::before{
    content: '●';
    color: #B8FF81;
    margin-right: 10px;
    font-size: 25px;
  }
  .level5-circle::before{
    content: '●';
    color: #F3EC53;
    margin-right: 10px;
    font-size: 25px;
  }
  .level6-circle::before{
    content: '●';
    color: #FEB144;
    margin-right: 10px;
    font-size: 25px;
  }
  .level7-circle::before{
    content: '●';
    color: #FF6663;
    margin-right: 10px;
    font-size: 25px;
  }
</style>

<!--
<template>
  <Row
    type="flex"
    :gutter="18"
  >
    <Col :span="19">
    <Panel shadow>
      <div slot="title">
        {{ $t('m.Problem_List') }}
      </div>
      <div slot="extra">
        <ul class="filter">
          <li>
            <Dropdown @on-click="filterByDifficulty">
              <span>{{ query.difficulty === '' ? this.$i18n.t('m.Difficulty') : this.$i18n.t('m.' + query.difficulty) }}
                <Icon type="arrow-down-b" />
              </span>
              <Dropdown-menu slot="list">
                <Dropdown-item name="">
                  {{ $t('m.All') }}
                </Dropdown-item>
                <Dropdown-item name="Level1">
                  {{ $t('m.Level1') }}
                </Dropdown-item>
                <Dropdown-item name="Level2">
                  {{ $t('m.Level2') }}
                </Dropdown-item>
                <Dropdown-item name="Level3">
                  {{ $t('m.Level3') }}
                </Dropdown-item>
                <Dropdown-item name="Level4">
                  {{ $t('m.Level4') }}
                </Dropdown-item>
                <Dropdown-item name="Level5">
                  {{ $t('m.Level5') }}
                </Dropdown-item>
                <Dropdown-item name="Level6">
                  {{ $t('m.Level6') }}
                </Dropdown-item>
                <Dropdown-item name="Level7">
                  {{ $t('m.Level7') }}
                </Dropdown-item>
              </Dropdown-menu>
            </Dropdown>
          </li>
          <li>
            <i-switch
              size="large"
              @on-change="handleTagsVisible"
            >
              <span slot="open">{{ $t('m.Tags') }}</span>
              <span slot="close">{{ $t('m.Tags') }}</span>
            </i-switch>
          </li>
          <li>
            <Input
              v-model="query.keyword"
              placeholder="keyword"
              icon="ios-search-strong"
              @on-enter="filterByKeyword"
              @on-click="filterByKeyword"
            />
          </li>
          <li>
            <Button
              type="info"
              @click="onReset"
            >
              <Icon type="refresh" />
              {{ $t('m.Reset') }}
            </Button>
          </li>
        </ul>
      </div>
      <Table
        style="width: 100%; font-size: 16px;"
        :columns="problemTableColumns"
        :data="problemList"
        :loading="loadings.table"
        disabled-hover
      />
    </Panel>
    <Pagination
      :total="total"
      :page-size="limit"
      :current.sync="query.page"
      @on-change="pushRouter"
    />
    </Col>

    <Col :span="5">
    <Panel :padding="10">
      <div
        slot="title"
        class="taglist-title"
      >
        {{ $t('m.Tags') }}
      </div>
      <Button
        v-for="tag in tagList"
        :key="tag.name"
        type="ghost"
        :disabled="query.tag === tag.name"
        shape="circle"
        class="tag-btn"
        @click="filterByTag(tag.name)"
      >
        {{ tag.name }}
      </Button>

      <Button
        id="pick-one"
        long
        @click="pickone"
      >
        <Icon type="shuffle" />
        {{ $t('m.Pick_One') }}
      </Button>
    </Panel>
    <Spin
      v-if="loadings.tag"
      fix
      size="large"
    />
    </Col>
  </Row>
</template>

<script>
import { mapGetters } from 'vuex'
import api from '@oj/api'
import utils from '@/utils/utils'
import { ProblemMixin } from '@oj/components/mixins'
import Pagination from '@oj/components/Pagination'

export default {
  name: 'ProblemList',
  components: {
    Pagination
  },
  mixins: [ProblemMixin],
  data () {
    return {
      tagList: [],
      problemTableColumns: [
        {
          title: '#',
          key: '_id',
          width: 80,
          render: (h, params) => {
            return h('Button', {
              props: {
                type: 'text',
                size: 'large'
              },
              on: {
                click: () => {
                  this.$router.push({ name: 'problem-details', params: { problemID: params.row._id } })
                }
              },
              style: {
                padding: '2px 0'
              }
            }, params.row._id)
          }
        },
        {
          title: this.$i18n.t('m.Title'),
          width: 200,
          render: (h, params) => {
            return h('Button', {
              props: {
                type: 'text',
                size: 'large'
              },
              on: {
                click: () => {
                  this.$router.push({ name: 'problem-details', params: { problemID: params.row._id } })
                }
              },
              style: {
                padding: '2px 0',
                overflowX: 'auto',
                textAlign: 'left',
                width: '100%'
              }
            }, params.row.title)
          }
        },
        {
          title: this.$i18n.t('m.Level'),
          render: (h, params) => {
            const t = params.row.difficulty
            let color = 'purple'
            if (t === 'Level2') color = 'blue'
            else if (t === 'Level3') color = 'green'
            else if (t === 'Level4') color = 'yellowgreen'
            else if (t === 'Level5') color = 'yellow'
            else if (t === 'Level6') color = 'orange'
            else if (t === 'Level7') color = 'red'
            return h('Tag', {
              props: {
                color: color
              }
            }, this.$i18n.t('m.' + params.row.difficulty))
          }
        },
        {
          title: this.$i18n.t('m.Total'),
          key: 'submission_number'
        },
        {
          title: this.$i18n.t('m.AC_Rate'),
          render: (h, params) => {
            return h('span', this.getACRate(params.row.accepted_number, params.row.submission_number))
          }
        }
      ],
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
      }
    }
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
    filterByTag (tagName) {
      this.query.tag = tagName
      this.query.page = 1
      this.pushRouter()
    },
    filterByDifficulty (difficulty) {
      this.query.difficulty = difficulty
      this.query.page = 1
      this.pushRouter()
    },
    filterByKeyword () {
      this.query.page = 1
      this.pushRouter()
    },
    handleTagsVisible (value) {
      if (value) {
        this.problemTableColumns.push(
          {
            title: this.$i18n.t('m.Tags'),
            align: 'center',
            render: (h, params) => {
              const tags = []
              params.row.tags.forEach(tag => {
                tags.push(h('Tag', {}, tag))
              })
              return h('div', {
                style: {
                  margin: '8px 0'
                }
              }, tags)
            }
          })
      } else {
        this.problemTableColumns.splice(this.problemTableColumns.length - 1, 1)
      }
    },
    onReset () {
      this.$router.push({ name: 'problem-list' })
    },
    pickone () {
      api.pickone().then(res => {
        this.$success('Good Luck')
        this.$router.push({ name: 'problem-details', params: { problemID: res.data.data } })
      })
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated'])
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

<style scoped lang="less">
  .taglist-title {
    margin-left: -10px;
    margin-bottom: -10px;
  }

  .tag-btn {
    margin-right: 5px;
    margin-bottom: 10px;
  }

  #pick-one {
    margin-top: 10px;
  }
</style>
-->
