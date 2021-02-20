<template>
  <div id="header">
    <b-navbar style="height: 100%">
      <b-navbar-brand class="ml-5">
        <img
          src="../../../assets/signature.png"
          style="height: 50px; width: auto;"
        />
      </b-navbar-brand>

      <b-navbar-nav class="mx-auto">
        <b-nav-item to="/">Notice</b-nav-item>
        <b-nav-item to="/contest">Contests</b-nav-item>
        <b-nav-item to="/problem">Problems</b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="mr-5">
        <b-icon icon="person" style="width: 32px; height: 32px"></b-icon>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  mounted () {
    this.getProfile()
  },
  methods: {
    ...mapActions(['getProfile', 'changeModalStatus']),
    handleRoute (route) {
      if (route && route.indexOf('admin') < 0) {
        this.$router.push(route)
      } else {
        window.open('/admin/')
      }
    },
    handleBtnClick (mode) {
      if (mode === 'register') {
        this.$alert('아이디(Username)는 자신의 학번으로 설정해주세요')
      }
      this.changeModalStatus({
        visible: true,
        mode: mode
      })
    }
  },
  computed: {
    ...mapGetters(['website', 'modalStatus', 'user', 'isAuthenticated', 'isAdminRole']),
    // 跟随路由变化
    activeMenu () {
      return '/' + this.$route.path.split('/')[1]
    },
    modalVisible: {
      get () {
        return this.modalStatus.visible
      },
      set (value) {
        this.changeModalStatus({ visible: value })
      }
    }
  }
}
</script>

<style scoped>
#header {
  position: relative;
  height: 72px;
  width: 100%;
  z-index: 1000;
  background-color: #fff;
}

.navbar-center {
  position: absolute;
  left: 50%;
}
</style>
