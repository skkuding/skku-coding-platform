<template>
  <div>
    <Header />
    <div class="content-app">
      <transition name="fadeInUp" mode="out-in">
        <router-view></router-view>
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
  name: 'App',
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
  // text-decoration: none;
  // background-color: transparent;
  // &:active,
  // &:hover {
  //   outline-width: 0;
  // }
  text-decoration: none;
  background-color: transparent;
  // link 설정 추가
  &:link {
    color: white;
  }
  // 기존 active에 color 속성 추가
  &:active {
    color: white;
  }
  &:hover {
    outline-width: 0;
  }
  // visited 설정 추가
  &:visited {
    color: white;
  }
}

@media screen and (max-width: 1200px) {
  .content-app {
    margin-top: 160px;
    padding: 0 2%;
  }
}

@media screen and (min-width: 1200px) {
  // .content-app {
  //   margin-top: 80px;
  //   padding: 0 2%;
  // }
  .content-app {
    margin-top: 80px;
    padding: 0; // 좌우 패딩 삭제(padding: 0 2%;)
    width: 100%; // width 추가
    height: 100%; // height 추가
  }
  .footer {
    margin-top: 20px;
    font-size: 18px; // font-size : small -> 18px
    min-width: 300px;
    position: relative;
    top: 0;
    left: 0;
    background: #8dc63f;
  }
  .fadeInUp-enter-active {
    animation: fadeInUp 0.8s;
  }
  // 이하의 코드는 새롭게 추가된 내용
  .footer-info {
    height: 30vh;
    padding-top: 1vh;
    padding-bottom: 1vh;
    color: white;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
  }
  .footer-detail {
    width: 300px;
    height: 20vh;
    text-align: left;
    margin-left: 100px;
  }
  .footer-logo {
    width: 300px;
    height: 20vh;
    margin-left: 100px;
    margin-right: 50px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: right;
  }
  .footer-item {
    width: 270px;
    height: 3vh;
    margin-bottom: 3vh;
    display: flex;
    flex-direction: row;
  }
  .footer-text {
    margin-left: 20px;
  }
  // 로고 사이즈 비율 고정
  img {
    object-fit: contain;
  }

  .copyright {
    background: white;
    color: #8dc63f;
    text-align: right;
    padding-right: 10px;
  }
}

.fadeInUp-enter-active {
  animation: fadeInUp 0.8s;
}
</style>
