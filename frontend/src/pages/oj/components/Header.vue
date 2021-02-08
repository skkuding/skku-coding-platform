<template>
  <div id="header">
    <b-navbar>
      <b-navbar-brand class="header__logo">
        <img
          src="https://www.skku.edu/_res/skku//img/common/logo.png"
          style="margin-left: 20px"
        />
      </b-navbar-brand>

      <b-navbar-nav class="header__items" align="center">
        <b-nav-item>Notice</b-nav-item>
        <b-nav-item>Contests</b-nav-item>
        <b-nav-item>Problems</b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="header__account" align="right">
        <b-icon icon="person" style="width: 32px; height: 32px"></b-icon>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>
//   import { mapGetters, mapActions } from 'vuex'
// import login from '@oj/views/user/Login'
// import register from '@oj/views/user/Register'
//   export default {
// components: {
//   login,
//   register
// },
// mounted () {
//   this.getProfile()
// },
// methods: {
//   ...mapActions(['getProfile', 'changeModalStatus']),
//   handleRoute (route) {
//     if (route && route.indexOf('admin') < 0) {
//       this.$router.push(route)
//     } else {
//       window.open('/admin/')
//     }
//   },
//   handleBtnClick (mode) {
//     if (mode === 'register') {
//       this.$alert('아이디(Username)는 자신의 학번으로 설정해주세요')
//     }
//     this.changeModalStatus({
//       visible: true,
//       mode: mode
//     })
//   }
// },
// computed: {
//   ...mapGetters(['website', 'modalStatus', 'user', 'isAuthenticated', 'isAdminRole']),
//   // Follow routing changes
//   activeMenu () {
//     return '/' + this.$route.path.split('/')[1]
//   },
//   modalVisible: {
//     get () {
//       return this.modalStatus.visible
//     },
//     set (value) {
//       this.changeModalStatus({visible: value})
//     }
//   }
// }
//   }
</script>

<style lang="less" scoped>
  #header {
    position: fixed;
    top: 0;
    left: 0;
    height: 72px;
    width: 100%;
    z-index: 1000;
    background-color: #fff;
  }
  .header__items {
    width: 100%;
  }
</style>
