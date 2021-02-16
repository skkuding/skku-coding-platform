<template>
    <div>
      <b-card title="SKKU Coding Platform 2차 모의대회" class="border-0" bg-variant="transparent">
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
              :total-rows=100
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
          key: 'contest_id',
          sortType: 'asc',
          width: 150,
          render: (h, params) => {
            return h('span', params.row._id)
          }
        },
        {
          label: this.$i18n.t('m.Title'),
          key: 'title',
          render: (h, params) => {
            return h('span', params.row.title)
          }
        }
      ]
    }
  },
  mounted () {
    this.getContestProblems()
    this.contestID = this.$route.params.contestID
    this.route_name = this.$route.name
    this.$store.dispatch('getContest').then(res => {
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
      this.$store.dispatch('getContestProblems').then(res => {
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
        this.$error('Password can\'t be empty')
        return
      }
      this.btnLoading = true
      api.checkContestPassword(this.contestID, this.contestPassword).then((res) => {
        this.$success('Succeeded')
        this.$store.commit(types.CONTEST_ACCESS, { access: true })
        this.btnLoading = false
      }, (res) => {
        this.btnLoading = false
      })
    }
  },
  computed: {
    ...mapState({
      showMenu: state => state.contest.itemVisible.menu,
      contest: state => state.contest.contest,
      contest_table: state => [state.contest.contest],
      problems: state => state.contest.contestProblems,
      now: state => state.contest.now
    }),
    ...mapGetters(
      ['contestMenuDisabled', 'contestRuleType', 'contestStatus', 'countdown', 'isContestAdmin',
        'OIContestRealTimePermission', 'passwordFormVisible', 'isAuthenticated', 'contestRuleType', 'OIContestRealTimePermission']
    ),
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
    '$route' (newVal) {
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
  .pagination{

    display: flex;
    justify-content: flex-end;
  }
  .status{
    display: flex;
    justify-content: flex-end;
  }
</style>

<!--
<template>
  <Row
    type="flex"
    justify="space-around"
  >
    <Col :span="22">
    <Panel :padding="10">
      <div slot="title">
        {{ $t('m.ACM_Ranklist') }}
      </div>
      <div class="echarts">
        <ECharts
          ref="chart"
          :options="options"
          auto-resize
        />
      </div>
    </Panel>
    <Table
      :data="dataRank"
      :columns="columns"
      :loading="loadingTable"
      size="large"
    />
    <Pagination
      :total="total"
      :page-size.sync="limit"
      :current.sync="page"
      show-sizer
      @on-change="getRankData"
      @on-page-size-change="getRankData(1)"
    />
    </Col>
  </Row>
</template>

<script>
import api from '@oj/api'
import Pagination from '@oj/components/Pagination'
import utils from '@/utils/utils'
import { RULE_TYPE } from '@/utils/constants'

export default {
  name: 'AcmRank',
  components: {
    Pagination
  },
  data () {
    return {
      page: 1,
      limit: 30,
      total: 0,
      loadingTable: false,
      dataRank: [],
      columns: [
        {
          align: 'center',
          width: 60,
          render: (h, params) => {
            return h('span', {}, params.index + (this.page - 1) * this.limit + 1)
          }
        },
        {
          title: this.$i18n.t('m.User_User'),
          align: 'center',
          render: (h, params) => {
            return h('a', {
              style: {
                display: 'inline-block',
                'max-width': '200px'
              },
              on: {
                click: () => {
                  this.$router.push(
                    {
                      name: 'user-home',
                      query: { username: params.row.user.username }
                    })
                }
              }
            }, params.row.user.username)
          }
        },
        {
          title: this.$i18n.t('m.mood'),
          align: 'center',
          key: 'mood'
        },
        {
          title: this.$i18n.t('m.AC'),
          align: 'center',
          key: 'accepted_number'
        },
        {
          title: this.$i18n.t('m.Total'),
          align: 'center',
          key: 'submission_number'
        },
        {
          title: this.$i18n.t('m.Rating'),
          align: 'center',
          render: (h, params) => {
            return h('span', utils.getACRate(params.row.accepted_number, params.row.submission_number))
          }
        }
      ],
      options: {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: [this.$i18n.t('m.AC'), this.$i18n.t('m.Total')]
        },
        grid: {
          x: '3%',
          x2: '3%'
        },
        toolbox: {
          show: true,
          feature: {
            dataView: { show: true, readOnly: true },
            magicType: { show: true, type: ['line', 'bar', 'stack'] },
            saveAsImage: { show: true }
          },
          right: '10%'
        },
        calculable: true,
        xAxis: [
          {
            type: 'category',
            data: ['root'],
            axisLabel: {
              interval: 0,
              showMinLabel: true,
              showMaxLabel: true,
              align: 'center',
              formatter: (value, index) => {
                return utils.breakLongWords(value, 10)
              }
            }
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: this.$i18n.t('m.AC'),
            type: 'bar',
            data: [0],
            markPoint: {
              data: [
                { type: 'max', name: 'max' }
              ]
            }
          },
          {
            name: this.$i18n.t('m.Total'),
            type: 'bar',
            data: [0],
            markPoint: {
              data: [
                { type: 'max', name: 'max' }
              ]
            }
          }
        ]
      }
    }
  },
  mounted () {
    this.getRankData(1)
  },
  methods: {
    getRankData (page) {
      const offset = (page - 1) * this.limit
      const bar = this.$refs.chart
      bar.showLoading({ maskColor: 'rgba(250, 250, 250, 0.8)' })
      this.loadingTable = true
      api.getUserRank(offset, this.limit, RULE_TYPE.ACM).then(res => {
        this.loadingTable = false
        if (page === 1) {
          this.changeCharts(res.data.data.results.slice(0, 10))
        }
        this.total = res.data.data.total
        this.dataRank = res.data.data.results
        bar.hideLoading()
      }).catch(() => {
        this.loadingTable = false
        bar.hideLoading()
      })
    },
    changeCharts (rankData) {
      const [usernames, acData, totalData] = [[], [], []]
      rankData.forEach(ele => {
        usernames.push(ele.user.username)
        acData.push(ele.accepted_number)
        totalData.push(ele.submission_number)
      })
      this.options.xAxis[0].data = usernames
      this.options.series[0].data = acData
      this.options.series[1].data = totalData
    }
  }
}
</script>

<style scoped lang="less">
  .echarts {
    margin: 0 auto;
    width: 95%;
    height: 400px;
  }
</style>
-->
