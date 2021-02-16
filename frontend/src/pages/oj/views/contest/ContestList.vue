<template>
  <div>
    <b-card
      title="All Contest"
      class="border-0"
      bg-variant="transparent"
    >
      <div class="table">
        <b-table
          hover
          :items="contests"
          :fields="contestListColumns"
          :per-page="perPage"
          :current-page="currentPage"
          head-variant="light"
          @row-clicked="goContest"
        >
          <!-- <template #cell(title)="data">
            <a href="#">{{data.value}}</a>
          </template> -->
          <!-- <template #cell(status)>
            {{countdown}}
          </template> -->
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
// import moment from 'moment'
import api from '@oj/api'
import { mapState, mapGetters, mapActions } from 'vuex'
import utils from '@/utils/utils'
import time from '@/utils/time'
import { CONTEST_STATUS_REVERSE, CONTEST_TYPE, CONTEST_STATUS } from '@/utils/constants'

export default {
  name: 'ContestList',
  beforeRouteEnter (to, from, next) {
    api.getContestList(0, 5).then((res) => {
      next((vm) => {
        vm.contests = res.data.data.results
        vm.total = res.data.data.total
      })
    }, (res) => {
      next()
    })
  },
  data () {
    return {
      CONTEST_STATUS: CONTEST_STATUS,
      route_name: '',
      contestID: '',
      page: 1,
      query: {
        status: '',
        keyword: '',
        rule_type: ''
      },
      // limit: limit,
      total: 0,
      rows: '',
      contests: [],
      CONTEST_STATUS_REVERSE: CONTEST_STATUS_REVERSE,
      //      for password modal use
      cur_contest_id: '',
      contestListColumns: [
        {
          label: 'Title',
          key: 'title'
          // formatter: 'goContestDetails'
          // render: (h, params) => {
          //   return h('Button', {
          //     props: {
          //       type: 'text',
          //       size: 'large'
          //     },
          //     on: {
          //       click: () => {
          //         this.$router.push({ name: 'contest-details', params: { contestID: params.row._id } })
          //       }
          //     }
          //   }, params.row.title)
          // }
        },
        {
          label: 'Start time',
          key: 'start_time',
          formatter: 'getFormat'
          // formatter: value => {
          //   return time.utcToLocal(value, 'YYYY-M-D HH:mm')
          // }
        },
        {
          label: 'Duration',
          key: 'duration'
          // formatter: value => {
          //   return this.getDuration(value.row.start_time, value.row.end_time)
          // }
        },
        {
          label: 'Status',
          key: 'status'
        }
      ]
    }
  },
  methods: {
    ...mapActions(['changeDomTitle']),
    handleRoute (route) {
      this.$router.push(route)
    },
    init () {
      const route = this.$route.query
      this.query.status = route.status || ''
      this.query.rule_type = route.rule_type || ''
      this.query.keyword = route.keyword || ''
      this.page = parseInt(route.page) || 1
      this.getContestList()
    },
    getContestList (page = 1) {
      const offset = (page - 1) * this.limit
      api.getContestList(offset, this.limit, this.query).then((res) => {
        this.contests = res.data.data.results
        this.total = res.data.data.total
      })
    },
    changeRoute () {
      const query = Object.assign({}, this.query)
      query.page = this.page
      this.$router.push({
        name: 'contest-list',
        query: utils.filterEmptyValue(query)
      })
    },
    onRuleChange (rule) {
      this.query.rule_type = rule
      this.page = 1
      this.changeRoute()
    },
    onStatusChange (status) {
      this.query.status = status
      this.page = 1
      this.changeRoute()
    },
    goContest (item) {
      this.cur_contest_id = item.id
      if (item.contest_type !== CONTEST_TYPE.PUBLIC && !this.isAuthenticated) {
        this.$error(this.$i18n.t('m.Please_login_first'))
        this.$store.dispatch('changeModalStatus', { visible: true })
      } else {
        this.$router.push({ name: 'contest-details', params: { contestID: item.id } })
      }
    },
    getDuration (startTime, endTime) {
      return time.duration(startTime, endTime)
    },
    getFormat (value) {
      return time.utcToLocal(value, 'YYYY-M-D HH:mm')
    },
    remainTime (startTime) {
      const today = new Date()
      return time.duration(today, startTime)
    }
  },
  computed: {
    ...mapState({
      showMenu: state => state.contest.itemVisible.menu,
      contest: state => state.contest.contest,
      contest_table: state => [state.contest.contest],
      now: state => state.contest.now
    }),
    ...mapGetters(
      ['contestMenuDisabled', 'countdown', 'isContestAdmin',
        'OIContestRealTimePermission', 'passwordFormVisible']
    )
  },
  watch: {
    '$route' (newVal, oldVal) {
      if (newVal !== oldVal) {
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
</style>

<!--
<template>
  <Row type="flex">
    <Col :span="24">
    <Panel
      id="contest-card"
      shadow
    >
      <div slot="title">
        {{ query.rule_type === '' ? this.$i18n.t('m.All') : query.rule_type }} {{ $t('m.Contests') }}
      </div>
      <div slot="extra">
        <ul class="filter">
          <li>
            <Dropdown @on-click="onRuleChange">
              <span>{{ query.rule_type === '' ? this.$i18n.t('m.Rule') : this.$i18n.t('m.' + query.rule_type) }}
                <Icon type="arrow-down-b" />
              </span>
              <Dropdown-menu slot="list">
                <Dropdown-item name="">
                  {{ $t('m.All') }}
                </Dropdown-item>
                <Dropdown-item name="OI">
                  {{ $t('m.OI') }}
                </Dropdown-item>
                <Dropdown-item name="ACM">
                  {{ $t('m.ACM') }}
                </Dropdown-item>
              </Dropdown-menu>
            </Dropdown>
          </li>
          <li>
            <Dropdown @on-click="onStatusChange">
              <span>{{ query.status === '' ? this.$i18n.t('m.Status') : this.$i18n.t('m.' + CONTEST_STATUS_REVERSE[query.status].name.replace(/ /g,"_")) }}
                <Icon type="arrow-down-b" />
              </span>
              <Dropdown-menu slot="list">
                <Dropdown-item name="">
                  {{ $t('m.All') }}
                </Dropdown-item>
                <Dropdown-item name="0">
                  {{ $t('m.Underway') }}
                </Dropdown-item>
                <Dropdown-item name="1">
                  {{ $t('m.Not_Started') }}
                </Dropdown-item>
                <Dropdown-item name="-1">
                  {{ $t('m.Ended') }}
                </Dropdown-item>
              </Dropdown-menu>
            </Dropdown>
          </li>
          <li>
            <Input
              id="keyword"
              v-model="query.keyword"
              icon="ios-search-strong"
              placeholder="Keyword"
              @on-enter="changeRoute"
              @on-click="changeRoute"
            />
          </li>
        </ul>
      </div>
      <p
        v-if="contests.length == 0"
        id="no-contest"
      >
        {{ $t('m.No_contest') }}
      </p>
      <ol id="contest-list">
        <li
          v-for="contest in contests"
          :key="contest.title"
        >
          <Row
            type="flex"
            justify="space-between"
            align="middle"
          >
            <img
              class="trophy"
              src="../../../../assets/Cup.png"
            >
            <Col
              :span="18"
              class="contest-main"
            >
            <p class="title">
              <a
                class="entry"
                @click.stop="goContest(contest)"
              >
                {{ contest.title }}
              </a>
              <template v-if="contest.contest_type != 'Public'">
                <Icon
                  type="ios-locked-outline"
                  size="20"
                />
              </template>
            </p>
            <ul class="detail">
              <li>
                <Icon
                  type="calendar"
                  color="#3091f2"
                />
                {{ contest.start_time | localtime('YYYY-M-D HH:mm') }}
              </li>
              <li>
                <Icon
                  type="android-time"
                  color="#3091f2"
                />
                {{ getDuration(contest.start_time, contest.end_time) }}
              </li>
              <li>
                <Button
                  size="small"
                  shape="circle"
                  @click="onRuleChange(contest.rule_type)"
                >
                  {{ contest.rule_type }}
                </Button>
              </li>
            </ul>
            </Col>
            <Col
              :span="4"
              style="text-align: center"
            >
            <Tag
              type="dot"
              :color="CONTEST_STATUS_REVERSE[contest.status].color"
            >
              {{ $t('m.' + CONTEST_STATUS_REVERSE[contest.status].name.replace(/ /g, "_")) }}
            </Tag>
            </Col>
          </Row>
        </li>
      </ol>
    </Panel>
    <Pagination
      :total="total"
      :page-size="limit"
      :current.sync="page"
      @on-change="getContestList"
    />
    </Col>
  </Row>
</template>

<script>
import api from '@oj/api'
import { mapGetters } from 'vuex'
import utils from '@/utils/utils'
import Pagination from '@/pages/oj/components/Pagination'
import time from '@/utils/time'
import { CONTEST_STATUS_REVERSE, CONTEST_TYPE } from '@/utils/constants'

const limit = 8

export default {
  name: 'ContestList',
  components: {
    Pagination
  },
  beforeRouteEnter (to, from, next) {
    api.getContestList(0, limit).then((res) => {
      next((vm) => {
        vm.contests = res.data.data.results
        vm.total = res.data.data.total
      })
    }, (res) => {
      next()
    })
  },
  data () {
    return {
      page: 1,
      query: {
        status: '',
        keyword: '',
        rule_type: ''
      },
      limit: limit,
      total: 0,
      rows: '',
      contests: [],
      CONTEST_STATUS_REVERSE: CONTEST_STATUS_REVERSE,
      //      for password modal use
      cur_contest_id: ''
    }
  },
  methods: {
    init () {
      const route = this.$route.query
      this.query.status = route.status || ''
      this.query.rule_type = route.rule_type || ''
      this.query.keyword = route.keyword || ''
      this.page = parseInt(route.page) || 1
      this.getContestList()
    },
    getContestList (page = 1) {
      const offset = (page - 1) * this.limit
      api.getContestList(offset, this.limit, this.query).then((res) => {
        this.contests = res.data.data.results
        this.total = res.data.data.total
      })
    },
    changeRoute () {
      const query = Object.assign({}, this.query)
      query.page = this.page
      this.$router.push({
        name: 'contest-list',
        query: utils.filterEmptyValue(query)
      })
    },
    onRuleChange (rule) {
      this.query.rule_type = rule
      this.page = 1
      this.changeRoute()
    },
    onStatusChange (status) {
      this.query.status = status
      this.page = 1
      this.changeRoute()
    },
    goContest (contest) {
      this.cur_contest_id = contest.id
      if (contest.contest_type !== CONTEST_TYPE.PUBLIC && !this.isAuthenticated) {
        this.$error(this.$i18n.t('m.Please_login_first'))
        this.$store.dispatch('changeModalStatus', { visible: true })
      } else {
        this.$router.push({ name: 'contest-details', params: { contestID: contest.id } })
      }
    },

    getDuration (startTime, endTime) {
      return time.duration(startTime, endTime)
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'user'])
  },
  watch: {
    '$route' (newVal, oldVal) {
      if (newVal !== oldVal) {
        this.init()
      }
    }
  }

}
</script>
<style lang="less" scoped>
  #contest-card {
    #keyword {
      width: 80%;
      margin-right: 30px;
    }
    #no-contest {
      text-align: center;
      font-size: 16px;
      padding: 20px;
    }
    #contest-list {
      > li {
        padding: 20px;
        border-bottom: 1px solid rgba(187, 187, 187, 0.5);
        list-style: none;

        .trophy {
          height: 40px;
          margin-left: 10px;
          margin-right: -20px;
        }
        .contest-main {
          .title {
            font-size: 18px;
            a.entry {
              color: #495060;
              &:hover {
                color: #2d8cf0;
                border-bottom: 1px solid #2d8cf0;
              }
            }
          }
          li {
            display: inline-block;
            padding: 10px 0 0 10px;
            &:first-child {
              padding: 10px 0 0 0;
            }
          }
        }
      }
    }
  }
</style>
-->
