<template>
  <div class="view">
    <Panel :title="$t('m.Select_Contests') " v-if="this.routeName === 'statistics'">
      <div slot="header">
          <el-input
            v-model="keyword"
            prefix-icon="el-icon-search"
            placeholder="Keywords"
          />
      </div>
      <el-table
        ref="table"
        v-loading="loading"
        element-loading-text="loading"
        :data="contestList"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column
          type="selection"
          width="55"
        />

        <el-table-column
          prop="id"
          width="80"
          label="ID"
        />

        <el-table-column
          prop="title"
          label="Title"
        />

        <el-table-column
          label="Status"
          width="130"
        >
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.status === '-1' ? 'danger' : scope.row.status === '0' ? 'success' : 'primary'"
            >
              {{ scope.row.status | contestStatus }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      <div class="panel-options">
        <el-pagination
          class="page"
          layout="prev, pager, next"
          :page-size="pageSize"
          :total="total"
          @current-change="currentChange"
        />
      </div>
    </Panel>
    <Panel :title="$t('m.Statistics') ">
      <div class="small">
        <box-plot :chart-data="datacollection" />
        <button @click="fillData();">Randomize</button>
      </div>
    </Panel>
  </div>
</template>

<script>
import api from '../../api.js'
import { CONTEST_STATUS_REVERSE } from '@/utils/constants'
import BoxPlot from './BoxPlot.js'

export default {
  name: 'Statistics',
  components: {
    BoxPlot
  },
  filters: {
    contestStatus (value) {
      return CONTEST_STATUS_REVERSE[value].name
    }
  },
  data () {
    return {
      pageSize: 10,
      total: 0,
      contestList: [],
      keyword: '',
      loading: false,
      currentPage: 0,
      selectedContests: [],
      datacollection: null,
      routeName: ''
    }
  },
  computed: {
    selectedContestIDs () {
      const ids = []
      for (const user of this.selectedContests) {
        ids.push(user.id)
      }
      return ids
    }
  },
  watch: {
    'keyword' () {
      this.currentChange(1)
    }
  },
  mounted () {
    this.routeName = this.$route.name
    // if (this.routeName === 'statistics' || this.routeName === 'contest-statistics') {
    //   this.mode = 'contest'
    // } else {
    //   this.mode = 'statistics'
    // }
    this.getContestList(this.currentPage)
    this.fillData()
  },
  methods: {
    getContestList (page) {
      this.loading = true
      api.getContestList((page - 1) * this.pageSize, this.pageSize, this.keyword).then(res => {
        this.loading = false
        this.total = res.data.data.total
        this.contestList = res.data.data.results
      }, res => {
        this.loading = false
      })
    },
    handleSelectionChange (val) {
      this.selectedContests = val
    },
    fillData () {
      this.datacollection = {
        labels: [this.getRandomInt(), this.getRandomInt()],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#f87979',
            data: [this.getRandomValues(100, 200), this.getRandomValues()]
          },
          {
            label: 'Data One',
            backgroundColor: 'blue',
            data: [this.getRandomValues(), this.getRandomValues(20, 80)]
          }
        ]
      }
    },
    getRandomInt () {
      return Math.floor(Math.random() * (50 - 5 + 1)) + 5
    },
    getRandomValues (min = 0, max = 100) {
      return Array.from({ length: 100 }).map(
        () => Math.random() * (max - min) + min
      )
    }
  }
}
</script>

<style scoped lang="less">
  .notification {
    p {
      margin: 0;
      text-align: left;
    }
  }

  .small {
    max-width: 600px;
    margin:  150px auto;
  }
</style>
