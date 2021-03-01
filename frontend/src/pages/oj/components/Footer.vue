<template>
  <footer id="footer">
    <div class="footer-info">
      <ul class="footer-detail">
        <li class="footer-item">
          <img :src="mail" />
          <p class="footer-text">
            <a href="example@skku.edu">example@skku.edu</a>
          </p>
        </li>
        <li class="footer-item">
          <img :src="phone" />
          <p class="footer-text">031-123-4567</p>
        </li>
        <li class="footer-item">
          <img :src="location" />
          <p class="footer-text">
            <a
              href="https://www.skku.edu/skku/about/campusInfo/campusMap.do?campusCd=2&srSearchValue=#"
            ></a>
            400609, Semiconductor,<br />Natural Sciences Campus
          </p>
        </li>
      </ul>
      <ul class="footer-detail">
        <li class="footer-item">
          <img :src="github" />
          <p class="footer-text">
            <a href="https://github.com/skku-npc/skku-coding-platform"
              >GitHub</a
            >
          </p>
        </li>
        <li class="footer-item">
          <img :src="kakao" />
          <p class="footer-text">
            <a href="http://pf.kakao.com/_UKraK/chat"></a>Kakao Channel
          </p>
        </li>
        <li class="footer-item">
          <img :src="link" />
          <p class="footer-text">
            <a href="https://npc.skku.edu"></a> Algorithm Club NPC
          </p>
        </li>
      </ul>
      <div class="footer-logo">
        <img :src="skku" />
      </div>
    </div>
    <div class="footer-bottom">
      <span> (c) 2011-2021 SKKU NPC Club </span>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
  data () {
    return {
      version: process.env.VERSION,
      phone: require('../../../assets/icons/phone.svg'),
      kakao: require('../../../assets/icons/kakao.svg'),
      link: require('../../../assets/icons/link.svg'),
      github: require('../../../assets/icons/github.svg'),
      mail: require('../../../assets/icons/mail.svg'),
      location: require('../../../assets/icons/location.svg'),
      skku: require('../../../assets/logos/skku.svg')
    }
  },
  created () {
    try {
      document.body.removeChild(document.getElementById('app-loader'))
    } catch (e) {}
  },
  mounted () {
    this.getWebsiteConfig()
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
  bottom: -320px;
  font-size: 18px;
  background: #8dc63f;
}
.footer-info {
  padding-bottom: 1vh;
  color: white;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  flex-wrap: wrap;
}
.footer-detail {
  padding-top: 30px;
  width: 150px;
  height: 20vh;
  text-align: left;
}
.footer-logo {
  width: 300px;
  height: 70px;
  img {
    position:relative;
    width:100%;
    height:100%;
  }
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
img {
  object-fit: contain;
}
.footer-bottom {
  background: white;
  color: #8dc63f;
  text-align: right;
  padding-right: 10px;
}
</style>
