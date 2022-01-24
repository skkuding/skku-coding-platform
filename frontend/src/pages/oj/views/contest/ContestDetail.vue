<template>
  <div class="contest-list-card font-bold">
    <div class="mb-4 flex justify-between">
      <page-title :text="contest.title"/>
      <status-badge
        class="my-auto"
        style="margin-right: 40px;"
        :status_name="contestStatus.name"
        :status_color="contestStatus.color"
        :status_endtime="contest.end_time"
      ></status-badge>
    </div>

    <div>
      <b-tabs
        content-class="mt-3"
        class="contest-tab"
        pills
        align="center"
      >
        <b-tab title="Top">
          <p class="contest-tab-description" v-dompurify-html="contest.description"></p>
        </b-tab>
        <b-tab title="Problems" lazy>
          <contest-problem-list></contest-problem-list>
        </b-tab>
        <b-tab title="Standings" lazy>
          <contest-ranking></contest-ranking>
        </b-tab>
        <b-tab title="Clarifications" lazy>
          <contest-clarification></contest-clarification>
        </b-tab>
      </b-tabs>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import api from '@oj/api'
import { mapState, mapGetters, mapActions } from 'vuex'
import { types } from '@/store'
import { CONTEST_STATUS_REVERSE } from '@/utils/constants'
import StatusBadge from '../../components/StatusBadge.vue'
import ContestProblemList from './ContestProblemList.vue'
import ContestRanking from './ContestRanking.vue'
import ContestClarification from './ContestClarification.vue'
import PageTitle from '../../components/PageTitle.vue'

export default {
  name: 'ContestDetail',
  components: {
    StatusBadge,
    ContestProblemList,
    ContestRanking,
    ContestClarification,
    PageTitle
  },
  data () {
    return {
      // ACMTableColumns: [
      //   {
      //     label: '#',
      //     key: 'id',
      //     sortType: 'asc',
      //     width: 150
      //   },
      //   {
      //     label: this.$i18n.t('m.Title'),
      //     key: 'title'
      //   }
      // ],
      contestID: '',
      contest: {}
    }
  },
  async mounted () {
    this.contestID = this.$route.params.contestID
    this.route_name = this.$route.name
    try {
      const res = await this.$store.dispatch('getContest')
      this.changeDomTitle({ title: res.data.data.title })
      const data = res.data.data
      this.contest = data
      const endTime = moment(data.end_time)
      if (endTime.isAfter(moment(data.now))) {
        this.timer = setInterval(() => {
          this.$store.commit(types.NOW_ADD_1S)
        }, 1000)
      }
    } catch (err) {
    }
  },
  methods: {
    async getContestProblems () {
      try {
        const res = await this.$store.dispatch('getContestProblems')
        const data = res.data.data
        this.contestProblems = data
      } catch (err) {
      }
    },
    ...mapActions(['changeDomTitle']),
    async handleRoute (route) {
      await this.$router.push(route)
    },
    async checkPassword () {
      if (this.contestPassword === '') {
        this.$error('Password can\'t be empty')
        return
      }
      this.btnLoading = true
      try {
        await api.checkContestPassword(this.contestID, this.contestPassword)
        this.$success('Succeeded')
        this.$store.commit(types.CONTEST_ACCESS, { access: true })
        this.btnLoading = false
      } catch (err) {
        this.btnLoading = false
      }
    }
  },
  computed: {
    ...mapState({
      contest: state => state.contest.contest,
      problems: state => state.contest.contestProblems,
      now: state => state.contest.now
    }),
    ...mapGetters(
      ['contestMenuDisabled', 'contestRuleType', 'contestStatus', 'countdown', 'isContestAdmin',
        'OIContestRealTimePermission', 'passwordFormVisible', 'isAuthenticated', 'contestRuleType', 'OIContestRealTimePermission']
    ),
    contestStatus () {
      return {
        name: CONTEST_STATUS_REVERSE[this.contest.status].name,
        color: CONTEST_STATUS_REVERSE[this.contest.status].color
      }
    }
  },
  watch: {
    '$route' (newVal) {
      this.route_name = newVal.name
      this.contestID = newVal.params.contestID
      this.changeDomTitle({ title: this.contest.title })
    }
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .top-bar {
    margin-top: 40px;
    margin-left: 68px;
    width: 90%;
    display: flex;
    justify-content: space-between;
  }
  .title {
    color: #7C7A7B;
    display:inline;
    position:relative;
    word-break: keep-all;
    // top:36px;
  }
  .contest-list-card {
    margin: 0 auto;
    width: 70%;
    font-family: Manrope;
  }
  .contest-tab {
    width: 95%;
    margin: 0 auto;
    &-description {
      width: 95%;
      margin: 0 auto;
    }
  }
  .font-bold {
    font-family: manrope_bold;
  }
</style>
