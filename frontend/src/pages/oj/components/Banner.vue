<template>
  <div class="banner">
    <b-carousel
      :interval="4000"
      indicators
      img-width="2048"
      img-height="912"
      @sliding-start="onSlideStart"
      @sliding-end="onSlideEnd"
    >
      <b-carousel-slide :img-src="require('../../../assets/banner1.png')"></b-carousel-slide>
      <b-carousel-slide :img-src="require('../../../assets/banner2.png')"></b-carousel-slide>
      <b-carousel-slide :img-src="require('../../../assets/banner3.png')"></b-carousel-slide>
      <b-carousel-slide :img-src="require('../../../assets/banner4.png')"></b-carousel-slide>

    </b-carousel>
  </div>
</template>

<script>
export default {
  data () {
    return {
      slide: 0,
      sliding: null
    }
  },
  methods: {
    onSlideStart (slide) {
      this.sliding = true
    },
    onSlideEnd (slide) {
      this.sliding = false
    }
  }
}
</script>

<style lang="less" scoped>
.banner {
  position: relative;
}
/deep/ .banner img {
  height:412px;
}
.carousel-item {
  height:512px;
}
</style>
