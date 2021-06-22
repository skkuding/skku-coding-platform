<template>
  <div v-if="$route.name && $route.name.indexOf('problem-details') != -1">
      <router-view/>
  </div>
  <div class="app-container" v-else>
    <Header></Header>
    <div class="content-app">
      <transition name="fadeInUp" mode="out-in">
        <router-view/>
      </transition>
    </div>
    <Footer />
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import Header from '@oj/components/Header.vue'
import Footer from '@oj/components/Footer.vue'
import api from '@oj/api'

export default {
  name: 'app',
  components: {
    Header,
    Footer
  },
  data () {
    return {
      version: process.env.VERSION
    }
  },
  created () {
    try {
      document.body.removeChild(document.getElementById('app-loader'))
    } catch (e) {}
  },
  mounted () {
    this.getWebsiteConfig()
  },
  methods: {
    ...mapActions(['getWebsiteConfig', 'changeDomTitle']),
    async getContestList (page = 1) {
      const offset = (page - 1) * this.limit
      try {
        const res = await api.getContestList(offset, this.limit, this.query)
        this.contests = res.data.data.results
        this.total = res.data.data.total
      } catch (err) {
      }
    }
  },
  computed: {
    ...mapState(['website'])
  },
  watch: {
    website () {
      this.changeDomTitle()
    },
    $route () {
      this.changeDomTitle()
    }
  }
}
</script>

<style lang="scss">
html, body {
  min-height: 100%;
  height: 100%;
}

.problem-container {
  min-height: 100%;
}

.app-container {
  padding-bottom: 150px;
  position: relative;
  min-height: 100%;
}

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

</style>
