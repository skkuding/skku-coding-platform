<template>
  <footer id="footer">
    <div class="footer-info">
      <div class="icons">
        <a v-clipboard:copy="email" @click="copy"><img :src="mail" /></a>
        <a href="https://github.com/skku-npc/skku-coding-platform"><img :src="github" /></a>
        <a href="http://pf.kakao.com/_UKraK/chat"><img :src="kakao" /></a>
        <a href="https://npc.skku.edu"><img :src="link" /></a>
      </div>
      <div class="footer-bottom">
        <span> © 2011-2021 SKKU NPC Club </span>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
  data () {
    return {
      version: process.env.VERSION,
      email: 'example@skku.edu',
      phone: require('@/assets/icons/phone.svg'),
      kakao: require('@/assets/icons/kakao.svg'),
      link: require('@/assets/icons/link.svg'),
      github: require('@/assets/icons/github.svg'),
      mail: require('@/assets/icons/mail.svg'),
      location: require('@/assets/icons/location.svg'),
      skku: require('@/assets/logos/skku.svg')
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
    copy () {
      this.$success('Email is copied')
    }
  }
}
</script>

<style lang='less' scoped>
*, *:before, *:after {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}
a {
  text-decoration: none;
  background-color: transparent;
  &:link {
    color: white;
  }
  &:active {
    color: white;
  }
  &:hover {
    outline-width: 0;
  }
  &:visited {
    color: white;
  }
}
#footer {
  width: 100%;
  position: absolute;
  bottom: 0;
  background: #FFFFFF;
  color:#aaaaaa;
}
.footer-info {
  padding-bottom: 1vh;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}
.footer-bottom {
  font-size:16px;
}
.icons {
  margin-top:16px;
  margin-bottom:16px;
  > a{
    margin: 16px 16px 16px 16px;
  }
}
img {
  width:20px;
  height:20px;
  filter: invert(36%) sepia(3%) saturate(0%) hue-rotate(153deg) brightness(94%) contrast(88%);
}
</style>
