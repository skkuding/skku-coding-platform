<template>
  <Row
    type="flex"
    justify="space-around"
  >
    <Banner />
    <Col :span="22">
      <Announcements class="announcement" />
    </Col>
  </Row>
</template>

<script>
import Announcements from './Announcements.vue'
import Banner from '@oj/components/Banner.vue'
import api from '@oj/api'
import time from '@/utils/time'
import { CONTEST_STATUS } from '@/utils/constants'

export default {
  name: 'Home',
  components: {
    Banner,
    Announcements
  },
  data () {
    return {
      contests: [],
      index: 0
    }
  },
  mounted () {
    const params = { status: CONTEST_STATUS.NOT_START }
    api.getContestList(0, 5, params).then(res => {
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
    }
  }
}
</script>

<style lang="less" scoped>
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

  .announcement {
    margin-top: 20px;
  }
</style>
