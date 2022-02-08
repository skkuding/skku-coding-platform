<template>
  <div class="contest-list-card font-bold">
    <page-title text="All Contest"/>
    <Table
      hover
      :items="contests"
      :fields="contestListFields"
      :per-page="perPage"
      :current-page="currentPage"
      @row-clicked="goContest"
    >
      <template v-slot:title="data">
        <div class="w-80">{{ data.row.title }}</div>
      </template>
      <template v-slot:start_time="data">
        {{ getTimeFormat(data.row.start_time) }}
      </template>
      <template v-slot:duration="data">
        {{ getDuration(data.row.start_time, data.row.end_time) }}
      </template>
      <template v-slot:status="data">
        <b-icon
          icon="circle-fill"
          class="mr-2"
          :style="'color:' + contestStatus(data.row.status).color"
        />
        {{ contestStatus(data.row.status).name }}
      </template>
    </Table>
    <div class="pagination">
      <b-pagination
        v-model="currentPage"
        :total-rows="contests.length"
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
import PageTitle from '@oj/components/PageTitle.vue'
import Table from '@oj/components/Table.vue'

export default {
  name: 'ContestList',
  components: {
    PageTitle,
    Table
  },
  async beforeRouteEnter (to, from, next) {
    try {
      const res = await api.getContestList(0, 20)
      next((vm) => {
        vm.contests = res.data.data.results
        vm.total = res.data.data.total
      })
    } catch (err) {
      next()
    }
  },
  data () {
    return {
      limit: 20,
      total: 0,
      perPage: 5,
      currentPage: 1,
      CONTEST_STATUS: CONTEST_STATUS,
      route_name: '',
      contestID: '',
      query: {
        status: '',
        keyword: '',
        rule_type: ''
      },
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
    async getContestList () {
      try {
        const res = await api.getContestList(0, this.limit, this.query)
        this.contests = res.data.data.results
        this.total = res.data.data.total
      } catch (err) {
      }
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
        await this.$store.dispatch('changeModalStatus', { mode: 'login', visible: true })
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

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .contest-list-card{
    margin: 0 auto;
    width: 70%;
    font-family: Manrope;
  }
  div{
    &.pagination{
    margin-right: 5%;
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
    }
  }
  .contest-list-card::v-deep {
    margin: 0 auto;
    width: 70%;
    font-family: Manrope;
    .table {
      width: 95% !important;
      margin: 0 auto;
      td {
        cursor: pointer;
      }
    }
  }
  .font-bold {
    font-family: manrope_bold;
  }
</style>
