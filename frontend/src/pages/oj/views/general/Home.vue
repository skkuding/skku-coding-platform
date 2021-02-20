<template>
  <div>
    <Banner />
    <div class="post-area">
      <AnnouncementPanel></AnnouncementPanel>
      <ContestPanel></ContestPanel>
    </div>
  </div>
</template>
<script>
import Banner from '@oj/components/Banner.vue'
import AnnouncementPanel from '@oj/components/AnnouncementPanel.vue'
import ContestPanel from '@oj/components/ContestPanel.vue'
export default {
  name: 'Home',
  components: {
    Banner,
    AnnouncementPanel,
    ContestPanel
  },
  data () {
    return {
      contests: [],
      index: 0
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
  height: 100%;
  display: flex;
  margin-top: 30px;
  justify-content: space-around;
  flex-direction: row;
  flex-wrap: wrap;
  position: relative;
}
</style>
