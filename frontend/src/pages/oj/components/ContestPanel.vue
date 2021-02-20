<template>
  <div class="panel">
    <b-card
      header-tag="header"
      header-bg-variant="white"
      header-border-variant="white"
      style="max-width: 60rem; border-radius: 12px"
    >
      <template #header>
        <div class="panel-title">
          <div class="post-title">
            <b-icon icon = "award" shift-v="-3"></b-icon>
            <p style="margin-left: 0.5rem">Current/Upcoming Contests</p>
          </div>
          <b-icon icon="list" shift-v="-3" @click="goContestList()"></b-icon>
        </div>
      </template>
      <b-card-body>
        <b-table
          striped: False
          hover:False
          :items="contests"
          :fields="contestListFields"
          :per-page ="perPage"
          thead-tr-class="d-none"
          class="align-center"
          borderless
          @row-clicked="goContest"
        >
        <template #cell(icon)='data'>
          <b-icon icon="three-dots" v-if="data.item.status==='0'"></b-icon>
          <b-icon icon="calendar2" v-if="data.item.status==='1'"></b-icon>
        </template>
        <template #cell(start_time)>
            {{ getTimeFormat(value, "MMM D, YYYY") }}
        </template>
        </b-table>
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
import api from '@oj/api'
import { mapState, mapGetters } from 'vuex'
import time from '@/utils/time'
import {
  CONTEST_TYPE,
  CONTEST_STATUS
} from '@/utils/constants'

export default {
  name: 'ContestPanel',
  data () {
    return {
      contestID: '',
      page: 1,
      query: '',
      limit: 3,
      total: 3,
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
      cur_contest_id: '',
      contestListFields: [
        {
          label: 'Icon',
          key: 'icon',
          tdClass: 'icon-field',
          thClass: 'icon-field',
          thStyle: 'width: 2rem;'
        },
        {
          label: 'Title',
          key: 'title',
          tdClass: 'title-field',
          thClass: 'title-field',
          thStyle: 'width: 50rem;'
        },
        {
          label: 'Start time',
          key: 'start_time',
          tdClass: 'date-field',
          thClass: 'date-field',
          thStyle: 'width: 4rem;'
        }
      ]
    }
  },
  mounted () {
    this.init()
  },
  methods: {
    init () {
      const route = this.$route.query
      this.page = parseInt(route.page) || 1
      this.getContestList()
    },
    getContestList (page = 1) {
      const offset = (page - 1) * this.limit
      api.getContestList(offset, this.limit, this.query).then((res) => {
        this.contests = res.data.data.results.reverse()
        this.total = res.data.data.total
      })
      var status = [CONTEST_STATUS.UNDERWAY, CONTEST_STATUS.NOT_START]
      const result = this.contests.filter(contest =>
        contest.status in status
      )
      this.contests = result
      console.log(this.contests)
    },
    goContest (item) {
      this.contestID = item.id
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
    goContestList () {
      this.$router.push({ name: 'contest-list' })
    },
    getTimeFormat (value, format) {
      return time.utcToLocal(value, format)
    }
  },
  computed: {
    ...mapState({
      contest: (state) => state.contest.contest
    }),
    ...mapGetters([
      'countdown'
    ])
  }
}
</script>
<style scoped>
.panel {
  padding: 20px 10px;
}
.card-header {
  width: 40rem;
  height: 3rem;
  padding: 0.5rem;
  border-radius: 12px;
}
.card-body {
  height: 12rem;
  padding: 0.5rem;
  margin-top: 0.25rem;
  border-radius: 12px;
  font-size: 1.2rem;
}
.panel-title {
  display: flex;
  text-align: center;
  justify-content: space-between;
  flex-direction: row;
  font-size: 1.5rem;
  padding-top: 0.5rem;
}
.post-title {
  display: flex;
  justify-content: space-between;
  flex-direction: row;
}
/deep/ .table .date-field {
  text-align: right;
}
</style>
