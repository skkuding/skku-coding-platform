<template>
  <div>
    <b-card
      title="SKKU Coding Platform 2차 모의대회"
      class="border-0"
      bg-variant="transparent"
    >
      <div class="status mb-2">
        <b-badge pill variant="primary">Ongoing</b-badge>
      </div>
      <div class="table">
        <b-table
          hover
          :fields="ACMTableColumns"
          :items="ContestProblemList"
          :per-page="perPage"
          :current-page="currentPage"
          head-variant="light"
        >
          <template #cell(index)="data">
            {{ data.index + 1 }}
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
    </b-card>
  </div>
</template>

<script>
import moment from 'moment'
import api from '@oj/api'
import { mapState, mapGetters, mapActions } from 'vuex'
import { types } from '@/store'
import { CONTEST_STATUS_REVERSE } from '@/utils/constants'
import { ProblemMixin } from '@oj/components/mixins'
// import time from '@/utils/time'
export default {
  name: 'ContestProblemList',
  mixins: [ProblemMixin],
  data () {
    return {
      ACMTableColumns: [
        {
          label: '#',
          key: 'id',
          sortType: 'asc',
          width: 150
        },
        {
          label: this.$i18n.t('m.Title'),
          key: 'title'
        }
      ]
    }
  },
  mounted () {
    this.contestID = this.$route.params.contestID
    this.route_name = this.$route.name
    this.getContestProblems()
    this.$store.dispatch('getContest').then((res) => {
      this.changeDomTitle({ title: res.data.data.title })
      const data = res.data.data
      const endTime = moment(data.end_time)
      if (endTime.isAfter(moment(data.now))) {
        this.timer = setInterval(() => {
          this.$store.commit(types.NOW_ADD_1S)
        }, 1000)
      }
    })
  },
  methods: {
    getContestProblems () {
      this.$store.dispatch('getContestProblems').then((res) => {
        if (this.isAuthenticated) {
          if (this.contestRuleType === 'ACM') {
            this.addStatusColumn(this.ACMTableColumns, res.data.data)
          } else if (this.OIContestRealTimePermission) {
            this.addStatusColumn(this.ACMTableColumns, res.data.data)
          }
        }
      })
    },
    goContestProblem (row) {
      this.$router.push({
        name: 'contest-problem-details',
        params: {
          contestID: this.$route.params.contestID,
          problemID: row._id
        }
      })
    },
    ...mapActions(['changeDomTitle']),
    handleRoute (route) {
      this.$router.push(route)
    },
    checkPassword () {
      if (this.contestPassword === '') {
        this.$error("Password can't be empty")
        return
      }
      this.btnLoading = true
      api.checkContestPassword(this.contestID, this.contestPassword).then(
        (res) => {
          this.$success('Succeeded')
          this.$store.commit(types.CONTEST_ACCESS, { access: true })
          this.btnLoading = false
        },
        (res) => {
          this.btnLoading = false
        }
      )
    }
  },
  computed: {
    ...mapState({
      showMenu: (state) => state.contest.itemVisible.menu,
      contest: (state) => state.contest.contest,
      contest_table: (state) => [state.contest.contest],
      problems: (state) => state.contest.contestProblems,
      now: (state) => state.contest.now
    }),
    ...mapGetters([
      'contestMenuDisabled',
      'contestRuleType',
      'contestStatus',
      'countdown',
      'isContestAdmin',
      'OIContestRealTimePermission',
      'passwordFormVisible',
      'isAuthenticated',
      'contestRuleType',
      'OIContestRealTimePermission'
    ]),
    countdownColor () {
      if (this.contestStatus) {
        return CONTEST_STATUS_REVERSE[this.contestStatus].color
      }
      return 'black'
    },
    showAdminHelper () {
      return this.isContestAdmin && this.contestRuleType === 'ACM'
    }
  },
  watch: {
    $route (newVal) {
      this.route_name = newVal.name
      this.contestID = newVal.params.contestID
      this.changeDomTitle({ title: this.contest.title })
    }
  },
  beforeDestroy () {
    clearInterval(this.timer)
    this.$store.commit(types.CLEAR_CONTEST)
  }
}
</script>

<style>
.pagination {
  display: flex;
  justify-content: flex-end;
}
.status {
  display: flex;
  justify-content: flex-end;
}
</style>
-->
