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
    <div class="table">
      <b-table
        hover
        :items="contestProblems"
        :fields="contestProblemListFields"
        :per-page="perPage"
        :current-page="currentPage"
        head-variant="light"
        @row-clicked="goContestProblem"
      >
      </b-table>
    </div>
    <div class="pagination">
      <b-pagination
        v-model="currentPage"
        :total-rows="contestProblems.length"
        :per-page="perPage"
        limit="3"
      ></b-pagination>
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
      await this.$store.dispatch('getContestProblems').then(res => {
        const data = res.data.data
        this.contestProblems = data
      })
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

<style lang="less" scoped>
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
    width: 90%;
    font-family: Manrope;
  }
  .contest-list-card .problem-list-table {
    margin: 0 0 0 auto;
  }
  .table{
    width: 95% !important;
    margin: 0 auto;
  }
  div.pagination{
    margin-right: 5%;
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
  .status-container {
    position: relative;
    top: 10px;
    margin-right: 60px;
    padding: 5px 8px 4px;
    display: flex;
    border: 2px solid #bdbdbd;
    border-radius: 6px;
    color: #828282;
  }
  .font-bold {
    font-family: manrope_bold;
  }
</style>
