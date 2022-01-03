<template>
  <div class="banner">
    <b-carousel
      :interval="4000"
      indicators
      @sliding-start="onSlideStart"
      @sliding-end="onSlideEnd"
    >
      <b-carousel-slide
        v-for="(image, index) in bannerImageList"
        :key="index"
        :img-src=image.path
      ></b-carousel-slide>
    </b-carousel>
  </div>
</template>

<script>
import api from '../api'

export default {
  data () {
    return {
      slide: 0,
      sliding: null,
      bannerImageList: []
    }
  },
  async mounted () {
    const res = await api.getBannerImage()
    this.bannerImageList = res.data.data.path
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

<style lang="scss" scoped>
  .banner {
    position: relative;
  }
</style>
