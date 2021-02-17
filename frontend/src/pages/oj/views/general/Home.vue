<template>
  <Row type="flex" justify="space-around">
    <Banner />
    <div class="post-area">
      <HomePanel id="notice-panel"> </HomePanel>
      <HomePanel id="contest-panel"></HomePanel>
    </div>
    <Col :span="22">
      <Announcements class="announcement" />
    </Col>
  </Row>
</template>

<script>
// import Announcements from './Announcements.vue'
import Banner from '@oj/components/Banner.vue'
import HomePanel from '@oj/components/HomePanel.vue'
import api from '@oj/api'
import time from '@/utils/time'
import { CONTEST_STATUS } from '@/utils/constants'

export default {
  name: 'Home',
  components: {
    Banner,
    HomePanel
    // Announcements
  },
  data () {
    return {
      contests: [],
      index: 0
    }
  },
  mounted () {
    const params = { status: CONTEST_STATUS.NOT_START }
    api.getContestList(0, 5, params).then((res) => {
      this.contests = res.data.data.results
    })
  },
  methods: {
    getDuration (startTime, endTime) {
      return time.duration(startTime, endTime)
    },
    goContest () {
      this.$router.push({
        name: 'contest-details',
        params: { contestID: this.contests[this.index].id }
      })
    },
    getContestList (page = 1) {
      const offset = (page - 1) * this.limit
      api.getContestList(offset, this.limit, this.query).then((res) => {
        this.contests = res.data.data.results
        this.total = res.data.data.total
      })
    },
    getAnnouncementList (offset, limit) {
      const params = {
        offset: offset,
        limit: limit
      }
      return ajax('announcement', 'get', {
        params
      })
    }
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
  height: 30vh;
  display: flex;
  justify-content: space-around;
  flex-direction: row;
  flex-wrap: wrap;
}

.announcement {
  margin-top: 20px;
}
</style>
