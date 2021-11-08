<template>
  <div class="contest-list-card font-bold">
    <div class="top-bar mb-4">
      <h2 class="title"> {{ contest.title }} </h2>
      <div class="problem-list-table">
        <div class="status-container">
          <b-icon
            icon="circle-fill"
            shift-h="-2"
            shift-v="-3"
            class="mx-1"
            :style="'color:' + contestStatus.color"
          />
          {{ contestStatus.name }}
        </div>
      </div>
    </div>

    <b-navbar sticky-top style="height: 100%;">
      <b-navbar-nav class="mx-auto" align="center">
        <b-nav-item class="contest__menu">
          <router-link class="nav-link" :to="{ name: 'contest-details', param: { contest_id : contestID }}">Top</router-link>
        </b-nav-item>
        <b-nav-item class="contest__menu">
          <router-link class="nav-link" :to="{ name: 'contest-problems', param: { contest_id : contestID }}">Problems</router-link>
        </b-nav-item>
        <b-nav-item class="contest__menu">
          <router-link class="nav-link" :to="{ name: 'contest-ranking', param: { contest_id : contestID }}">Standings</router-link>
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>

    <div class="description">
      <p v-dompurify-html="contest.description"></p>
    </div>
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
      contest: {},
      contestProblems: [],
      contestProblemListFields: [
        {
          label: '#',
          key: '_id'
        },
        {
          label: 'Title',
          key: 'title'
        }
      ]
    }
  },
  async mounted () {
    this.contestID = this.$route.params.contestID
    this.route_name = this.$route.name
    this.getContestProblems()
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
    async goContestProblem (row) {
      await this.$router.push({
        name: 'contest-problem-details',
        params: {
          contestID: this.$route.params.contestID,
          problemID: row._id
        }
      })
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
  },
  beforeDestroy () {
    clearInterval(this.timer)
    this.$store.commit(types.CLEAR_CONTEST)
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
  }
  .title {
    color: #7C7A7B;
    display:inline;
    position:relative;
    // top:36px;
  }
  .contest-list-card {
    margin: 0 auto;
    width: 70%;
    font-family: Manrope;
    .problem-list-table {
      margin: 0 0 0 auto;
    }
  }
  .description {
    margin-left: 68px;
    margin-right: 68px;

    p {
      margin-top: 1rem;
    }
  }
</style>
