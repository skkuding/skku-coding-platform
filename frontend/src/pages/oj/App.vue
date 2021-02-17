<template>
  <div>
    <Header />
    <div class="content-app">
      <transition name="fadeInUp" mode="out-in">
        <router-view></router-view>
      </transition>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import Header from '@oj/components/Header.vue'

export default {
  name: 'App',
  components: {
    Header
  },
  data () {
    return {
      version: process.env.VERSION
    }
  },
  created () {
    try {
      document.body.removeChild(document.getElementById('app-loader'))
    } catch (e) {
    }
  },
  mounted () {
    this.getWebsiteConfig()
  },
  methods: {
    ...mapActions(['getWebsiteConfig', 'changeDomTitle'])
  },
  computed: {
    ...mapState(['website'])
  },
  watch: {
    'website' () {
      this.changeDomTitle()
    },
    '$route' () {
      this.changeDomTitle()
    }
  }
}
</script>

<style lang="less">

* {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}

a {
  text-decoration: none;
  background-color: transparent;
  &:active, &:hover {
    outline-width: 0;
  }
}

@media screen and (max-width: 1200px) {
  .content-app {
    margin-top: 72px;
  }
}

@media screen and (min-width: 1200px) {
  .content-app {
    margin-top: 72px;
  }
}

.fadeInUp-enter-active {
  animation: fadeInUp .8s;
}

</style>
