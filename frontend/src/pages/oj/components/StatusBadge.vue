<template>
  <div class="status-container">
    <div v-if="status_name !== 'Underway'">
      <b-icon
        icon="circle-fill"
        shift-h="-2"
        shift-v="-3"
        class="mx-1 status-icon"
        :style="'color:' + status_color"
      />
      {{ status_name }}
    </div>
    <div v-else>
      <b-icon
        icon="clock-fill"
        :style="'color: ' + status_color"
        style="margin-right: 2px;"
      />
      {{ remaintime.hour + ':' + remaintime.min + ':' + remaintime.sec }}
    </div>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  props: {
    status_name: {
      type: String,
      required: true
    },
    status_color: {
      type: String,
      required: true
    },
    status_endtime: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      remaintime: { hour: '-', min: '-', sec: '-' },
      endtime: ''
    }
  },
  async mounted () {
    this.endtime = moment(this.status_endtime)
    setInterval(() => {
      this.calculateRemainTime()
    }, 1000)
  },
  methods: {
    calculateRemainTime () {
      if (moment(this.endtime).isBefore(moment.now())) {
        this.$set(this.remaintime, 'hour', -1)
        return
      }
      var timeDiff = moment.duration(moment(this.endtime).diff(moment.now())).asSeconds()
      const hour = this.checkNumberformat(parseInt(timeDiff / 3600))
      this.$set(this.remaintime, 'hour', hour)
      timeDiff -= hour * 3600
      const min = this.checkNumberformat(parseInt(timeDiff / 60))
      this.$set(this.remaintime, 'min', min)
      timeDiff -= min * 60
      const sec = this.checkNumberformat(parseInt(timeDiff))
      this.$set(this.remaintime, 'sec', sec)
    },
    checkNumberformat (num) {
      if (num < 10) {
        return '0' + num
      } else {
        return num
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .status-container {
    font-size: 14px;
    padding: 6px 50px;
    display: flex;
    border: 2px solid #eaeaea;
    border-radius: 20px;
    color: #7c7a7b;
    max-height: 40px;
    min-width: fit-content;
  }
  .status-icon {
    margin-bottom: 2px;
  }
</style>
