<template>
  <div>
    <b-card
      title="Problem list"
      class="border-0"
      bg-variant="transparent"
    >
      <div class="category-container mb-2">
        <b-dropdown @on-click="filterByDifficulty" text="Difficulty">
          <b-dropdown-item name="Level1">{{ $t('Level1') }}</b-dropdown-item>
          <b-dropdown-item name="Level2">{{ $t('Level2') }}</b-dropdown-item>
          <b-dropdown-item name="Level3">{{ $t('Level3') }}</b-dropdown-item>
          <b-dropdown-item name="Level4">{{ $t('Level4') }}</b-dropdown-item>
          <b-dropdown-item name="Level5">{{ $t('Level5') }}</b-dropdown-item>
          <b-dropdown-item name="Level6">{{ $t('Level6') }}</b-dropdown-item>
          <b-dropdown-item name="Level7">{{ $t('Level7') }}</b-dropdown-item>
        </b-dropdown>
        <div>
          <b-form-checkbox v-model="checked" name="check-button" switch class="mr-2" @on-change="handleTagsVisible">
            {{ $t('m.Tags') }}
          </b-form-checkbox>
        </div>
        <b-input-group
          class="col-4"
          @on-enter="filterByKeyword"
          @on-click="filterByKeyword"
        >
          <b-input-group-prepend @on-click="filterByKeyword" is-text>
            <b-icon icon="search"></b-icon>
          </b-input-group-prepend>
          <b-form-input placeholder="keywords"></b-form-input>
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
        </b-table>
      </div>
      <div class="pagination">
        <b-pagination
          aria-controls="notice-list"
          v-model="currentPage"
          :total-rows=100
          :per-page="perPage"
          limit="3"
        ></b-pagination>
      </div>
    </b-card>
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
      problemTableColumns: [
        {
          label: '#',
          key: '_id',
          width: 50,
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
              }
            }, params.row._id)
          }
        },
        {
          key: 'title',
          label: this.$i18n.t('m.Title'),
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
              }
            }, params.row.title)
          }
        },
        {
          key: 'difficulty',
          label: this.$i18n.t('m.Level'),
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
          label: this.$i18n.t('m.Total'),
          key: 'submission_number'
        },
        {
          key: 'AC_Rate',
          label: this.$i18n.t('m.AC_Rate'),
          // formatter: params => {
          //   return this.getACRate(params.row.accepted_number, params.row.submission_number)
          // }
          render: params => {
            return this.getACRate(params.row.accepted_number, params.row.submission_number)
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
  // computed: {
  //   rows () {
  //     return this.items.length
  //   }
  // },
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

<style>
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
