<template>
  <footer id="footer">
    <div class="footer-info">
      <div class="icons flex">
        <a v-clipboard:copy="email" @click="copy"><img :src="mail" /></a>
        <a href="https://github.com/skkuding/skku-coding-platform"><img :src="github" /></a>
        <a href="http://pf.kakao.com/_UKraK/chat"><img :src="kakao" /></a>
        <a href="https://npc.skku.edu"><img :src="link" /></a>
      </div>
      <div class="footer-bottom">
        <span> © 2020-2022 SKKUDING</span>
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
      kakao: require('@/assets/icons/kakao.svg'),
      link: require('@/assets/icons/link.svg'),
      github: require('@/assets/icons/github.svg'),
      mail: require('@/assets/icons/mail.svg')
    }
  },
  created () {
    try {
      document.body.removeChild(document.getElementById('app-loader'))
    } catch (e) {}
  },
  methods: {
    copy () {
      this.$success('Email is copied')
    }
  }
}
</script>

<style lang="scss" scoped>
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
    padding: 1rem;
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
    & > a{
      margin: 16px 16px 16px 16px;
    }
  }
  img {
    width:20px;
    height:20px;
    filter: invert(36%) sepia(3%) saturate(0%) hue-rotate(153deg) brightness(94%) contrast(88%);
  }
</style>
