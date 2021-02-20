<template>
  <div class="contest-list-card">
    <h1 class="title">Contest</h1>
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
      </b-table>
    </div>
    <div class="pagination">
        <b-pagination
          aria-controls="notice-list"
          v-model="currentPage"
          :total-rows="row"
          :per-page="perPage"
          limit="3"
        ></b-pagination>
    </div>
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
    ),
    row () {
      return this.contests.length
    }
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
  .contest-list-card{
    margin: 0 auto;
    width: 90%;
    font-family: Manrope;
  }
  .title{
    margin-top: 100px;
  }
  .contest-list-card .table{
    width: 95%;
    margin: 0 auto;
  }
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
        <template #cell(start_time)="data">
          {{ getTimeFormat(data.value, "YYYY-M-D HH:mm") }}
        </template>
        <template #cell(duration)="data">
          {{ getDuration(data.item.start_time, data.item.end_time) }}
        </template>
        <template #cell(status)="data">
          {{ CONTEST_STATUS_REVERSE[data.value].name }}
        </template>
      </b-table>
    </div>
    <div class="pagination">
      <b-pagination
        aria-controls="notice-list"
        v-model="currentPage"
        :total-rows="100"
        :per-page="perPage"
        limit="3"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
// import moment from 'moment'
import api from '@oj/api'
import { mapState, mapGetters, mapActions } from 'vuex'
import utils from '@/utils/utils'
import time from '@/utils/time'
import {
  CONTEST_STATUS_REVERSE,
  CONTEST_TYPE,
  CONTEST_STATUS
} from '@/utils/constants'
export default {
  name: 'ContestList',
  beforeRouteEnter (to, from, next) {
    api.getContestList(0, 5).then(
      (res) => {
        next((vm) => {
          vm.contests = res.data.data.results
          vm.total = res.data.data.total
        })
      },
      (res) => {
        next()
      }
    )
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
      contests: [
        {
          status: '0',
          contest_type: 'Password Protected',
          title: 'This is Contest',
          description: 'blah blah',
          real_time_rank: true,
          password: 'string',
          rule_type: 'ACM',
          start_time: '2021-02-17T01:00:13.621000+09:00',
          end_time: '2021-02-17T04:22:13.621000+09:00',
          create_time: '2021-02-17T01:00:59.006983+09:00',
          last_update_time: '2021-02-17T01:00:59.007006+09:00',
          visible: true,
          allowed_ip_ranges: []
        }
      ],
      CONTEST_STATUS_REVERSE: CONTEST_STATUS_REVERSE,
      // for password modal use
      cur_contest_id: '',
      contestListFields: [
        {
          label: 'Title',
          key: 'title'
        },
        {
          label: 'Start time',
          key: 'start_time'
        },
        {
          label: 'Duration',
          key: 'duration'
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
        this.$router.push({
          name: 'contest-details',
          params: { contestID: item.id }
        })
      }
    },
    getDuration (startTime, endTime) {
      return time.duration(startTime, endTime)
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-M-D HH:mm')
    },
    remainTime (startTime) {
      const today = new Date()
      return time.duration(today, startTime)
    }
  },
  computed: {
    ...mapState({
      showMenu: (state) => state.contest.itemVisible.menu,
      contest: (state) => state.contest.contest,
      contest_table: (state) => [state.contest.contest],
      now: (state) => state.contest.now
    }),
    ...mapGetters([
      'contestMenuDisabled',
      'countdown',
      'isContestAdmin',
      'OIContestRealTimePermission',
      'passwordFormVisible'
    ])
  },
  watch: {
    $route (newVal, oldVal) {
      if (newVal !== oldVal) {
        this.init()
      }
    }
  }
}
</script>

<style>
.pagination {
  display: flex;
  justify-content: flex-end;
}
</style>
-->
<<<<<<< HEAD
© 2021 GitHub, Inc.
=======
>>>>>>> problem list
