<template>
  <div>
    <page-top>
      <template #title>
        <span class="title-white">🏆 SKKU Coding Platform</span>
        <span class="title-gold"> Contests</span>
      </template>
      <template #description>
        Compete with schoolmates & win the prizes!
      </template>
    </page-top>
    <div class="contest-list-container">
      <h4 class="subtitle-blue text-xl" v-if="contestsUnderway.length || contestsUnderwayNoPermission.length">
        Active Contests >>
      </h4>
      <neon-box color="#8DC63F" class="my-3" v-for="(contest, index) in contestsUnderway" :key="'unp' + index"
                :leftTop="contest.title" :leftBottom="makeGroupRequirementInfo(contest)" :rightBottom="'Started ' + contest.startedTimeFromNow" :rightTop="contest.participants_count" rightTopIcon="users"
                :shadow="true" @click.native="goContest(contest)">
        <template #overlay-icon>
          <icon icon="arrow-right"></icon>
        </template>
      </neon-box>
      <neon-box color="#B4B4B4" v-for="(contest, index) in contestsUnderwayNoPermission"
                :leftTop="contest.title" :leftBottom="makeGroupRequirementInfo(contest)" :rightBottom="'Started ' + contest.startedTimeFromNow" :rightTop="contest.participants_count" rightTopIcon="users"
                :key="'unn' + index"  :shadow="true" class="my-3" @click.native="showContestInformationModal(contest)">
        <template #overlay-icon>
          <b-icon-zoom-in color="#B4B4B4" width="1.5em" height="1.5em"></b-icon-zoom-in>
        </template>
      </neon-box>
      <button v-if="contestsUnderwayRendered < contestsUnderwayTotal" @click="loadMoreContests(CONTEST_STATUS.UNDERWAY)">Load More..</button>
      <h4 class="subtitle-blue text-xl" v-if="contestsUpcoming.length || contestsUpcomingNoPermission.length">
        Upcoming Contests >>
      </h4>
      <neon-box color="#8DC63F" class="my-3" v-for="(contest, index) in contestsUpcoming" :key="'upp' + index"
                :leftTop="contest.title" :leftBottom="makeGroupRequirementInfo(contest)" :rightBottom="'Start ' + contest.remainTime" :rightTop="contest.participants_count" rightTopIcon="users"
                @click.native="showContestInformationModal(contest)">
        <template #overlay-icon>
          <b-icon-zoom-in color="#8DC63F" width="1.5em" height="1.5em"></b-icon-zoom-in>
        </template>
      </neon-box>
      <neon-box v-for="(contest, index) in contestsUpcomingNoPermission"
                :leftTop="contest.title" :leftBottom="makeGroupRequirementInfo(contest)" :rightBottom="'Start ' + contest.remainTime" :rightTop="contest.participants_count" rightTopIcon="users"
                :key="'upn' + index" color="#B4B4B4" class="my-3" @click.native="showContestInformationModal(contest)">
        <template #overlay-icon>
          <b-icon-zoom-in color="#B4B4B4" width="1.5em" height="1.5em"></b-icon-zoom-in>
        </template>
      </neon-box>
      <button v-if="contestsUpcomingRendered < contestsUpcomingTotal" @click="loadMoreContests(CONTEST_STATUS.NOT_START)">Load More..</button>
      <h4 class="subtitle-red text-xl">
        Finished Contests
        <button class="subtitle-toggle" @click="showFinishedContests = !showFinishedContests">
          <b-icon :icon="showFinishedContests ? 'caret-up-fill':'caret-down-fill'" color="#FF6663"></b-icon>
        </button>
      </h4>
      <neon-box v-show="showFinishedContests" v-for="(contest, index) in contestsFinished"
                :leftTop="contest.title" :leftBottom="makeGroupRequirementInfo(contest)" :rightBottom="'Finished ' + contest.finishedTimeFromNow" :rightTop="contest.participants_count" rightTopIcon="users"
                :key="'fi' + index" color="#FF6663" class="my-3" @click.native="goContest(contest)">
        <template #overlay-icon>
          <icon icon="arrow-right"></icon>
        </template>
      </neon-box>
      <b-pagination
        v-show="showFinishedContests"
        v-model="currentPage"
        :per-page="perPage"
        align="right"
        :total-rows="contestsFinishedTotal"
      />
    </div>
    <b-modal id="modal-contest-information" size="xl">
      <contest-information
        :title="contestInformation.title" :requirements="contestInformation.requirements"
        :constraints="contestInformation.constraints" :scoring="contestInformation.scoring"
        :prizes="contestInformation.prizes" :description="contestInformation.description"
      >
      </contest-information>
      <template #modal-footer>
        <b-button @click="goContest(contestInformation)">Go Contest</b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import api from '@oj/api'
import { mapGetters, mapActions } from 'vuex'
import utils from '@/utils/utils'
import time from '@/utils/time'
import { CONTEST_STATUS_REVERSE, CONTEST_TYPE, CONTEST_STATUS } from '@/utils/constants'
import NeonBox from '@oj/components/NeonBox.vue'
import PageTop from '@oj/components/PageTop.vue'
import ContestInformation from '@oj/components/ContestInformation.vue'
import store from '@/store'
import moment from 'moment'

export default {
  name: 'ContestList',
  async beforeRouteEnter (to, from, next) {
    try {
      const res = await api.getContestList(0, 10, {
        status: CONTEST_STATUS.UNDERWAY
      })
      const res2 = await api.getContestList(0, 10, {
        status: CONTEST_STATUS.NOT_START
      })
      const res3 = await api.getContestList(0, 20, {
        status: CONTEST_STATUS.ENDED
      })
      next((vm) => {
        vm.contestsUnderway = res.data.data.results
        vm.contestsUnderwayRendered = 10
        vm.contestsUnderwayTotal = res.data.data.total

        vm.contestsUpcoming = res2.data.data.results
        vm.contestsUpcomingRendered = 10
        vm.contestsUpcomingTotal = res2.data.data.total

        vm.contestsFinished = res3.data.data.results
        vm.contestsFinishedTotal = res3.data.data.total
      })
    } catch (err) {
      next()
    }
  },
  async mounted () {
    if (this.isAuthenticated) {
      this.filterWithGroupPermission()
    }
    this.calculateTimeDiff()
    setInterval(() => {
      this.calculateTimeDiff()
    }, 10000)
  },
  components: {
    NeonBox,
    ContestInformation,
    PageTop
  },
  data () {
    return {
      showCannotParticipate: false,
      showFinishedContests: false,
      CONTEST_STATUS: CONTEST_STATUS,
      route_name: '',
      query: {
        status: '',
        keyword: '',
        rule_type: ''
      },
      rows: '',
      contestsUnderway: [],
      contestsUnderwayNoPermission: [],
      contestsUnderwayRendered: 0,
      contestsUnderwayTotal: 0,

      contestsUpcoming: [],
      contestsUpcomingNoPermission: [],
      contestsUpcomingRendered: 0,
      contestsUpcomingTotal: 0,

      contestsFinished: [],
      contestsFinishedNoPermission: [],
      contestsFinishedTotal: 0,
      perPage: 20,
      currentPage: 1,

      contestInformation: {},
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
    ...mapActions(['changeDomTitle', 'getGroupList']),
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
      await this.filterWithGroupPermission()
    },
    async getContestList () {
      try {
        const res = await api.getContestList(0, 10, {
          status: CONTEST_STATUS.UNDERWAY
        })
        const res2 = await api.getContestList(0, 10, {
          status: CONTEST_STATUS.NOT_START
        })
        const res3 = await api.getContestList(0, 20, {
          status: CONTEST_STATUS.ENDED
        })
        this.contestsUnderway = res.data.data.results
        this.contestsUnderwayRendered = 10
        this.contestsUnderwayTotal = res.data.data.total

        this.contestsUpcoming = res2.data.data.results
        this.contestsUpcomingRendered = 10
        this.contestsUpcomingTotal = res2.data.data.total

        this.contestsFinished = res3.data.data.results
        this.contestsFinishedTotal = res3.data.data.total
      } catch (err) {
      }
    },
    async currentChange (page) {
      this.currentPage = page
      const res = await api.getContestList(20 * (page - 1), 20, {
        status: CONTEST_STATUS.ENDED
      })
      this.contestsFinished = res.data.data.results
      this.calculateTimeDiff()
    },
    async filterWithGroupPermission () {
      await store.dispatch('getGroupList')
      this.group_as_member = [...this.adminGroups, ...this.groups]
      function partition (array, filter) {
        const pass = []
        const fail = []
        array.forEach((e, idx, arr) => (filter(e, idx, arr) ? pass : fail).push(e))
        return [pass, fail]
      }
      const [a, b] = partition(this.contestsUnderway, contest => {
        if (!contest.allowed_groups.length) {
          return true
        }
        for (const allowedGroup of contest.allowed_groups) {
          if (allowedGroup.id in this.group_as_member) {
            return true
          }
        }
        return false
      })
      this.contestsUnderway = a
      this.contestsUnderwayNoPermission = b

      const [c, d] = partition(this.contestsUpcoming, contest => {
        if (!contest.allowed_groups.length) {
          return true
        }
        for (const allowedGroup of contest.allowed_groups) {
          if (allowedGroup.id in this.group_as_member) {
            return true
          }
        }
        return false
      })
      this.contestsUpcoming = c
      this.contestsUpcomingNoPermission = d
    },
    async loadMoreContests (status) {
      if (status === CONTEST_STATUS.UNDERWAY) {
        const res = await api.getContestList(this.contestsUnderwayRendered, 10, {
          status: CONTEST_STATUS.UNDERWAY
        })
        this.contestsUnderwayRendered += 10
        this.contestsUnderway = this.contestsUnderway.concat(res.data.data.results)
      } else if (status === CONTEST_STATUS.NOT_START) {
        const res = await api.getContestList(this.contestsUpcoming, 10, {
          status: CONTEST_STATUS.ENDED
        })
        this.contestsUpcomingRendered += 10
        this.contestsUpcoming = this.contestsUpcoming.concat(res.data.data.results)
      } else {
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
        if (item.contest_type === CONTEST_TYPE.PRIVATE && !this.isContestAdmin) {
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
    },
    showContestInformationModal (contest) {
      this.contestInformation = contest
      this.$bvModal.show('modal-contest-information')
    },
    makeGroupRequirementInfo (contest) {
      return 'For ' + (contest.allowed_groups.map(g => g.name).join(', ') || 'All Groups')
    },
    calculateTimeDiff () {
      for (const contest of this.contestsUpcoming) {
        this.$set(contest, 'remainTime', moment().to(moment(contest.start_time)))
      }
      for (const contest of this.contestsUpcomingNoPermission) {
        this.$set(contest, 'remainTime', moment().to(moment(contest.start_time)))
      }
      for (const contest of this.contestsFinished) {
        this.$set(contest, 'finishedTimeFromNow', moment(contest.end_time).fromNow())
      }
      for (const contest of this.contestsUnderway) {
        this.$set(contest, 'startedTimeFromNow', moment(contest.start_time).fromNow())
      }
      for (const contest of this.contestsUnderwayNoPermission) {
        this.$set(contest, 'startedTimeFromNow', moment(contest.start_time).fromNow())
      }
    }
  },
  computed: {
    ...mapGetters(
      ['contestMenuDisabled', 'countdown', 'isContestAdmin',
        'OIContestRealTimePermission', 'passwordFormVisible', 'isAuthenticated',
        'groups', 'adminGroups', 'otherGroups']
    ),
    updateCurrentPage () {
      return this.currentChange(this.currentPage)
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
  .title-white {
    color: white;
  }
  .title-gold {
    color: #FEB144;
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
  #triangle-right {
    width: 0;
    height: 0;
    margin-left: 4px;
    border-top: 10px solid transparent;
    border-left: 18px solid var(--main-color);
    border-bottom: 10px solid transparent;
  }
</style>
