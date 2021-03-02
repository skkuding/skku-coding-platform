<template>
  <div>
    <Banner />
    <div class="post-area">
      <b-card class="post-card">
        <div class="post-card-header">
          <div class="post-card-title">
            <b-icon icon="exclamation-circle"/>
            <p>Announcement</p>
          </div>
          <b-icon icon="list" shift-v="-4" @click="goAnnouncement()"/>
        </div>
        <b-table borderless
          :items="announcements"
          :fields="announcement_fields"
          @row-clicked="goAnnouncement"
        >
          <template #cell(icon)>
            <b-icon icon="chevron-right"/>
          </template>
          <template #cell(create_time)="data">
            {{ getTimeFormat(data.value, 'MMM D, YYYY') }}
          </template>
        </b-table>
      </b-card>
      <b-card class="post-card">
        <div class="post-card-header">
          <div class="post-card-title">
            <b-icon icon="award"/>
            <p>Current/Upcoming Contests</p>
          </div>
          <b-icon icon="list" shift-v="-4" @click="goContestList()"/>
        </div>
        <b-table borderless
          :items="contests"
          :fields="contest_fields"
          @row-clicked="goContest"
        >
          <template #cell(icon)="data">
            <b-icon :icon="data.item.status === '0' ? 'three-dots' : 'calendar2'"/>
          </template>
          <template #cell(start_time)="data">
            {{ getTimeFormat(data.value, "MMM D, YYYY") }}
          </template>
        </b-table>
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

export default {
  name: 'Home',
  components: {
    Banner
  },
  data () {
    return {
      announcements: [],
      contests: [],
      announcement_fields: [
        {
          label: 'icon',
          key: 'icon'
        },
        {
          label: 'title',
          key: 'title'
        },
        {
          label: 'create_time',
          key: 'create_time',
          tdClass: 'date-field'
        }
      ],
      contest_fields: [
        {
          label: 'icon',
          key: 'icon'
        },
        {
          label: 'title',
          key: 'title'
        },
        {
          label: 'start_time',
          key: 'start_time',
          tdClass: 'date-field'
        }
      ]
    }
  },
  mounted () {
    this.init()
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
      const res = await api.getContestList(0, 3)
      const contests = res.data.data.results
      this.total = res.data.data.total

      const status = [CONTEST_STATUS.UNDERWAY, CONTEST_STATUS.NOT_START]
      this.contests = contests.filter(contest => contest.status in status).reverse()
    },
    goAnnouncement (item) {
      if (item && item.id) {
        this.$router.push({ name: 'announcement-details', params: { announcementID: item.id } })
      } else {
        this.$router.push({ name: 'announcement-list' })
      }
    },
    goContest (item) {
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
<style lang='less' scoped>
.contest {
  &-title {
    font-style: italic;
    font-size: 21px;
  }
  &-content {
    padding: 0 70px 40px 70px;
    &-description {
      margin-top: 25px;
    }
  }
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
  height: 255px;
  width: 45%;
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

/deep/ .table tr {
  outline: none;
  font-size: 16px;

  th {
    display: none;
  }

  td {
    max-width: 60%;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }
}

/deep/ .table .date-field {
  text-align:right;
}

@media screen and (max-width: 1016px) {
  .post-card {
    width:80%;
    margin-top: 40px;
  }
}

</style>
