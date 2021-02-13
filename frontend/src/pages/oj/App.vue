<template>
  <div v-if="$route.name == 'problem-details'">
      <router-view/>
  </div>
    <div v-else>
      <Header></Header>
      <div class="content-app">
        <transition name="fadeInUp" mode="out-in">
          <router-view/>
        </transition>
      </div>
      <Footer />
    </div>
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
    getContestList (page = 1) {
      const offset = (page - 1) * this.limit
      api.getContestList(offset, this.limit, this.query).then((res) => {
        this.contests = res.data.data.results
        this.total = res.data.data.total
      })
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

.fadeInUp-enter-active {
  animation: fadeInUp .8s;
}
</style>
