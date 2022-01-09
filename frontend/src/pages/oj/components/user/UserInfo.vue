<template>
  <div class="user-info">
    <div class="flex-column mx-2">
      <div class="font-weight-bold mb-2" style="font-size: 20px">
        {{ info.nickname }}
        <span class="ml-1" style="color: #FF6663">
          {{ info.temperature }}°C
        </span>
      </div>
      <div>
        {{ info.username }} / {{ info.major }}
      </div>
    </div>
    <div class="d-flex">
      <div class="d-flex flex-column-reverse mx-2">
        <div style="font-size: 17px">
          # {{ info.weeklyRank }}
        </div>
        <div class="mb-1" style="font-size: 13px">
          Weekly
        </div>
      </div>
      <div class="d-flex flex-column-reverse mx-2">
        <div style="font-size: 17px">
          # {{ info.monthlyRank }}
        </div>
        <div class="mb-1" style="font-size: 13px">
          Monthly
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'UserInfo',
  components: {
  },
  props: {
    // info: {
    //     nickname: 'Nickname1234',
    //     temperature: 670,
    //     username: '2022123456',
    //     major: 'CSE',
    //     weeklyRank: 11,
    //     monthlyRank: 9,
    //     presentRank: 6
    //   },
    info: Object
  },
  data () {
    return {
    }
  },
  async mounted () {
  },
  methods: {

  },
  computed: {
  }
}
</script>

<style lang="scss" scoped>
  .user-info {
    display: flex;
    margin: 0px 10px;
    justify-content: space-between;
  }

</style>
