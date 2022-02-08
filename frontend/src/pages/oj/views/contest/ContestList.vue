<template>
  <div>
    <div class="page-top">
      <h2>
        <span class="title-white">🏆 SKKU Coding Platform</span>
        <span class="title-gold"> Contests</span>
      </h2>
      <div class="description">Compete with schoolmates & win the prizes!</div>
    </div>
    <div class="contest-list-container font-bold">
      <h4 class="subtitle-blue">
        Enter >>
      </h4>
      <neon-box color="#8DC63F" :shadow="true" class="my-3"></neon-box>
      <h4 class="subtitle-blue">
        Register Now >>
      </h4>
      <neon-box color="#8DC63F" class="my-3"></neon-box>
      <neon-box color="#8DC63F" class="my-3"></neon-box>
      <h4 class="subtitle-blue">
        Upcoming Contests >>
      </h4>
      <neon-box color="#8DC63F" class="my-3"></neon-box>
      <neon-box color="#8DC63F" class="my-3"></neon-box>
      <h4 class="subtitle-red">
        Cannot Participate
        <button class="subtitle-toggle">
          <b-icon-caret-down-fill color="#FF6663"></b-icon-caret-down-fill>
        </button>
      </h4>
      <neon-box color="#FF6663" :shadow="true" class="my-3"></neon-box>
      <h4 class="subtitle-red">
        Finished Contests
        <button class="subtitle-toggle">
          <b-icon-caret-down-fill color="#FF6663"></b-icon-caret-down-fill>
        </button>
      </h4>
      <neon-box color="#FF6663" class="my-3"></neon-box>
      <!-- <div class="table">
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
          :total-rows="contests.length"
          :per-page="perPage"
          limit="3"
        ></b-pagination>
      </div> -->
    </div>
  </div>
</template>

<script>
import api from '@oj/api'
import { mapGetters, mapActions } from 'vuex'
import utils from '@/utils/utils'
import time from '@/utils/time'
import { CONTEST_STATUS_REVERSE, CONTEST_TYPE, CONTEST_STATUS } from '@/utils/constants'
import NeonBox from '@oj/components/NeonBox.vue'

export default {
  name: 'ContestList',
  components: {
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
  components: {
    NeonBox
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
  .page-top {
    background: linear-gradient(270deg, rgba(26, 62, 81, 0.90) 0%, #1A3E51 25%, #1A3E51 75%, rgba(26, 62, 81, 0.90) 100%);;
    padding: 50px 0px;
    text-align: center;
    font-family: Manrope;
    .title-white {
      color: white;
    }
    .title-gold {
      color: #FEB144;
    }
    .description {
      font-size: 1rem;
      color: white;
      margin-top: 1rem;
    }
  }
  .subtitle-blue {
    color: #1A3E51;
    margin: 2rem 0 1rem 0;
  }

  .subtitle-red {
    color: #FF6663;
    margin: 2rem 0 1rem 0;
  }
  .subtitle-toggle {
    display: inline-block;
    width: 1.5rem;
    height: 1.5rem;
    border: none;
    background: none;
  }
  .contest-list-container {
    margin: 0 auto;
    width: 70%;
    font-family: Manrope;
  }
  .font-bold {
    font-family: manrope_bold;
  }
</style>
