<template>
  <div class="footer">
    <div class="footer-info">
      <div class="footer-detail first">
        <!--각 문장 위치 조정 및 아이콘 필요-->
        <div class="footer-item">
          <img :src="mail" />
          <p class="footer-text">
            <a href="example@skku.edu">example@skku.edu</a>
          </p>
        </div>
        <div class="footer-item">
          <img :src="phone" />
          <p class="footer-text">031-123-4567</p>
        </div>
        <div class="footer-item">
          <img :src="location" />
          <p class="footer-text">
            <a
              href="https://www.skku.edu/skku/about/campusInfo/campusMap.do?campusCd=2&srSearchValue=#"
            ></a>
            400609, Semiconductor,<br />Natural Sciences Campus
          </p>
        </div>
      </div>
      <div class="footer-detail second">
        <div class="footer-item">
          <img :src="github" />
          <p class="footer-text">
            <a href="https://github.com/skku-npc/skku-coding-platform"
              >GitHub</a
            >
          </p>
        </div>
        <div class="footer-item">
          <!--<span v-if="version">&nbsp; Version: {{ version }}</span>-->
          <img :src="kakao" />
          <p class="footer-text">
            <a href="http://pf.kakao.com/_UKraK/chat"></a>Kakao Channel
          </p>
        </div>
        <div class="footer-item">
          <img :src="link" />
          <p class="footer-text">
            <a href="https://npc.skku.edu"></a> Algorithm Club NPC
          </p>
        </div>
      </div>
      <div class="footer-logo">
        <img :src="skku" />
      </div>
    </div>
    <div class="copyright">
      <span> (c) 2011-2021 SKKU NPC Club </span>
    </div>
  </div>
</template>
<script>
// import { mapActions, mapState } from 'vuex'
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
  //   methods: {
  //     ...mapActions(['getWebsiteConfig', 'changeDomTitle'])
  //   },
  //   computed: {
  //     ...mapState(['website'])
  //   },
  //   watch: {
  //     website () {
  //       this.changeDomTitle()
  //     },
  //     $route () {
  //       this.changeDomTitle()
  //     }
  //   }
}
</script>
<style lang='less'>
* {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}
a {
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
/*media max-width : 1200px 에서 모바일 환경(769px)으로 변경*/
@media screen and (max-width: 1200px) {
  .content-app {
    margin-top: 160px;
    padding: 0;
  }
}
@media screen and (min-width: 1200px) {
  .content-app {
    margin-top: 80px;
    padding: 0; // 좌우 패딩 삭제(padding: 0 2%;)
    width: 100%; // width 추가
    height: 100%; // height 추가
  }
  //   .footer {
  //     margin-top: 20px;
  //     font-size: 18px; // font-size : small -> 18px
  //     min-width: 300px;
  //     position: fixed;
  //     top: 0;
  //     left: 0;
  //     background: #8dc63f;
  //   }
  //   .fadeInUp-enter-active {
  //     animation: fadeInUp 0.8s;
  //   }
  //   // 이하의 코드는 새롭게 추가된 내용
  //   .footer-info {
  //     height: 30vh;
  //     padding-top: 1vh;
  //     padding-bottom: 1vh;
  //     color: white;
  //     display: flex;
  //     flex-direction: row;
  //     justify-content: space-between;
  //     align-items: center;
  //     flex-wrap: wrap;
  //   }
  //   .footer-detail {
  //     width: 300px;
  //     height: 20vh;
  //     text-align: left;
  //     margin-left: 100px;
  //   }
  //   .footer-logo {
  //     width: 300px;
  //     height: 20vh;
  //     margin-left: 100px;
  //     margin-right: 50px;
  //     display: flex;
  //     flex-direction: column;
  //     justify-content: flex-end;
  //     align-items: right;
  //   }
  //   .footer-item {
  //     width: 270px;
  //     height: 3vh;
  //     margin-bottom: 3vh;
  //     display: flex;
  //     flex-direction: row;
  //   }
  //   .footer-text {
  //     margin-left: 20px;
  //   }
  //   // 로고 사이즈 비율 고정
  //   img {
  //     object-fit: contain;
  //   }
  //   .copyright {
  //     background: white;
  //     color: #8dc63f;
  //     text-align: right;
  //     padding-right: 10px;
  //   }
}
