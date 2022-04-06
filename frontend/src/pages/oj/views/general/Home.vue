<template>
  <div>
    <Banner />
    <div class="post-area">
      <b-card class="post-card">
        <div class="post-card-header">
          <div class="post-card-title">
            <b-icon icon="exclamation-circle"/>
            <p>Notice</p>
          </div>
          <b-icon style="cursor: pointer" icon="list" shift-v="-4" @click="goAnnouncement()"/>
        </div>
        <Table
          hover
          noHeader
          noBorder
          :items="announcements"
          :fields="announcement_fields"
          text=""
          @row-clicked="goAnnouncement"
          class="post-card-table mb-0 cursor-pointer text-lg"
        >
          <template v-slot:icon>
            <icon icon="chevron-right"/>
          </template>
          <template v-slot:title="data">
            <div class="w-80">{{data.row.title}}</div>
          </template>
          <template v-slot:create_time="data">
            <span class="whitespace-nowrap">{{ getTimeFormat(data.row.create_time, 'MMM D, YYYY') }}</span>
          </template>
        </Table>
      </b-card>
      <b-card class="post-card">
        <div class="post-card-header">
          <div class="post-card-title">
            <b-icon icon="award"/>
            <p>Current/Upcoming Contests</p>
          </div>
          <b-icon style="cursor: pointer" icon="list" shift-v="-4" @click="goContestList()"/>
        </div>
        <Table
          hover
          noHeader
          noBorder
          :items="contests"
          :fields="contest_fields"
          @row-clicked="goContest"
          text=""
          class="post-card-table mb-0 cursor-pointer text-lg"
        >
          <template v-slot:icon="data">
            <icon :icon="data.row.status === '0' ? 'ellipsis-h' : ['far', 'calendar']"/>
          </template>
          <template v-slot:title="data">
            <div class="w-80">{{ data.row.title }}</div>
          </template>
          <template v-slot:start_time="data" class="text-right">
            <span class="whitespace-nowrap">{{ getTimeFormat(data.row.start_time, "MMM D, YYYY") }}</span>
          </template>
        </Table>
      </b-card>
    </div>
  </div>
</template>
<script>
import Banner from '@oj/components/Banner.vue'
import api from '@oj/api'
import { mapState, mapGetters } from 'vuex'
import time from '@/utils/time'
import {
  CONTEST_TYPE,
  CONTEST_STATUS
} from '@/utils/constants'
import Table from '../../components/Table.vue'

export default {
  name: 'Home',
  components: {
    Banner,
    Table
  },
  data () {
    return {
      announcements: [],
      contests: [],
      announcement_fields: [
        {
          label: 'icon',
          key: 'icon',
          tdClass: 'icon-field',
          thClass: 'icon-field'
        },
        {
          label: 'title',
          key: 'title',
          tdClass: 'title-field',
          thClass: 'title-field'
        },
        {
          label: 'create_time',
          key: 'create_time',
          tdClass: 'date-field',
          thClass: 'date-field'
        }
      ],
      contest_fields: [
        {
          label: 'icon',
          key: 'icon',
          tdClass: 'icon-field',
          thClass: 'icon-field'
        },
        {
          label: 'title',
          key: 'title',
          tdClass: 'title-field',
          thClass: 'title-field'
        },
        {
          label: 'start_time',
          key: 'start_time',
          tdClass: 'date-field',
          thClass: 'date-field'
        }
      ]
    }
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      await this.getContestList()
      await this.getAnnouncementList()
    },
    async getAnnouncementList () {
      const res = await api.getAnnouncementList(0, 3)
      this.announcements = res.data.data.results
      this.total = res.data.data.total
    },
    async getContestList () {
      const res = await api.getContestList(0, 10)
      let contests = res.data.data.results
      this.total = res.data.data.total

      const status = [CONTEST_STATUS.UNDERWAY, CONTEST_STATUS.NOT_START]
      contests = contests.filter(contest => contest.status in status)
      if (contests.length >= 3) {
        this.contests = [contests[0], contests[1], contests[2]]
      } else {
        this.contests = [...contests]
      }
    },
    async goAnnouncement (item) {
      if (item && item.id) {
        await this.$router.push({ name: 'announcement-details', params: { announcementID: item.id } })
      } else {
        await this.$router.push({ name: 'announcement-list' })
      }
    },
    async goContest (item) {
      if (item.contest_type !== CONTEST_TYPE.PUBLIC && !this.isAuthenticated) {
        this.$error('Please login first!')
        await this.$store.dispatch('changeModalStatus', { mode: 'login', visible: true })
      } else {
        this.$router.push({
          name: 'contest-details',
          params: { contestID: item.id }
        })
      }
    },
    async goContestList () {
      await this.$router.push({ name: 'contest-list' })
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

<style lang="scss" scoped>
  .contest-title {
    font-style: italic;
    font-size: 21px;
  }

  .contest-content {
    padding: 0 70px 40px 70px;
  }

  .contest-content-description {
    margin-top: 25px;
  }

  .post-area {
    width: 100%;
    height: 100%;
    margin-top: 30px;
    display: flex;
    justify-content: space-around;
    align-items: flex-start;
    flex-direction: row;
    flex-wrap: wrap;
    position: relative;
  }

  .card {
    max-width:800px;
  }
  .post-card {
    margin-top: 30px;
    margin-bottom: 30px;
    min-height: 255px;
    width: 45%;
    min-width: 600px;
    &-table {
      cursor: pointer;
      :hover {
        background-color: #0000;
      }
    }
  }

  .post-card-header {
    border-radius: 12px;
    display: flex;
    justify-content: space-between;
    font-size: 25px;

    * {
      display: inline-block;
    }

    .post-card-title {
      margin-left: 8px;

      p {
        font-size: 21px;
        margin-left: 15px;
      }
    }
  }

  @media screen and (max-width: 1300px) {
    .post-card {
      width:80%;
      margin-top: 40px;
    }
  }
</style>
