<template>
  <div class="contest-list-card font-bold">
    <div class="top-bar mb-4">
      <h2 class="title">All Contest</h2>
    </div>
    <div class="table">
      <b-table
        hover
        :items="contests"
        :fields="contestListFields"
        :per-page="perPage"
        :current-page="currentPage"
        head-variant="light"
        @row-clicked="goContest"
      >
        <template #cell(start_time)="data">
          {{ getTimeFormat(data.value) }}
        </template>
        <template #cell(duration)="data">
          {{ getDuration(data.item.start_time, data.item.end_time) }}
        </template>
        <template #cell(status)="data">
          <b-icon
            icon="circle-fill"
            class="mr-2"
            :style="'color:' + contestStatus(data.value).color"
          />
          {{ contestStatus(data.value).name }}
        </template>
      </b-table>
    </div>
    <div class="pagination">
      <b-pagination
        v-model="currentPage"
        :total-rows="contest.length"
        :per-page="perPage"
        limit="3"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
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
      total: 0,
      rows: '',
      contests: [],
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
    async handleRoute (route) {
      await this.$router.push(route)
    },
    async init () {
      const route = this.$route.query
      this.query.status = route.status || ''
      this.query.rule_type = route.rule_type || ''
      this.query.keyword = route.keyword || ''
      this.page = parseInt(route.page) || 1
      await this.getContestList()
    },
    async getContestList (page = 1) {
      const offset = (page - 1) * this.limit
      await api.getContestList(offset, this.limit, this.query).then((res) => {
        this.contests = res.data.data.results
        this.total = res.data.data.total
      })
    },
    async changeRoute () {
      const query = Object.assign({}, this.query)
      query.page = this.page
      await this.$router.push({
        name: 'contest-list',
        query: utils.filterEmptyValue(query)
      })
    },
    async goContest (item) {
      this.cur_contest_id = item.id
      if (!this.isAuthenticated) {
        this.$error('Please login first!')
        await this.$store.dispatch('changeModalStatus', { visible: true })
      } else {
        if (item.contest_type === CONTEST_TYPE.PRIVATE) {
          this.$error('This contest is locked')
        } else {
          await this.$router.push({ name: 'contest-details', params: { contestID: item.id } })
        }
      }
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-MM-DD HH:mm')
    },
    getDuration (startTime, endTime) {
      return time.duration(startTime, endTime)
    },
    contestStatus (value) {
      return {
        name: CONTEST_STATUS_REVERSE[value].name,
        color: CONTEST_STATUS_REVERSE[value].color
      }
    }
  },
  computed: {
    ...mapState({
      contest: state => state.contest.contest
    }),
    ...mapGetters(
      ['contestMenuDisabled', 'countdown', 'isContestAdmin',
        'OIContestRealTimePermission', 'passwordFormVisible', 'isAuthenticated']
    ),
    row () {
      return this.contests.length
    }
  },
  watch: {
    async '$route' (newVal, oldVal) {
      if (newVal !== oldVal) {
        await this.init()
      }
    }
  }
}
</script>

<style scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .contest-list-card{
    margin: 0 auto;
    width: 90%;
    font-family: Manrope;
  }
  .top-bar {
    margin-top: 40px;
    margin-left: 68px;
  }
  .title{
    color: #7C7A7B;
  }
  .contest-list-card .table{
    width: 95% !important;
    margin: 0 auto;
  }
  div.pagination{
    margin-right: 5%;
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
  .font-bold {
    font-family: manrope_bold;
  }
</style>
