<template>
  <div class="header">
    <b-navbar>
      <b-navbar-brand class="header__logo" to="/">
        <img
          src="https://www.skku.edu/_res/skku//img/common/logo.png"
          style="margin-left: 20px"
        />
      </b-navbar-brand>

      <b-navbar-nav class="header__menu" align="center">
        <b-nav-item class="header__menu__item" to="/">Notice</b-nav-item>
        <b-nav-item class="header__menu__item" to="/contest">Contests</b-nav-item>
        <b-nav-item class="header__menu__item" to="/problem">Problems</b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="header__account" align="left">
        <b-nav-item-dropdown v-if="!isAuthenticated" no-caret right>
          <template slot="button-content">
            <b-icon icon="person" style="width: 32px; height: 32px"></b-icon>
          </template>
          <b-dropdown-item @click="handleBtnClick('login')">Sign In</b-dropdown-item>
          <b-dropdown-item @click="handleBtnClick('register')">Register</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown v-else no-caret right>
          <template slot="button-content">
            <b-icon icon="person" style="width: 32px; height: 32px"></b-icon>
          </template>
          <b-dropdown-item to="/user-home">My Account</b-dropdown-item>
          <b-dropdown-item to="/setting/profile">Setting</b-dropdown-item>
          <b-dropdown-item to="/logout">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
    <b-modal v-model="modalVisible">
      <div slot="header" class="modal-title">
        {{ $t('m.Welcome_to') }} {{ website.website_name_shortcut }}
      </div>
      <component
        :is="modalStatus.mode"
        v-if="modalVisible"
      />
      <div
        slot="footer"
        style="display: none"
      />
    </b-modal>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import login from '@oj/views/user/Login'
import register from '@oj/views/user/Register'

export default {
  components: {
    login,
    register
  },
  mounted () {
    this.getProfile()
  },
  methods: {
    ...mapActions(['getProfile', 'changeModalStatus']),
    handleBtnClick (mode) {
      this.changeModalStatus({
        visible: true,
        mode: mode
      })
    }
  },
  computed: {
    ...mapGetters(['website', 'modalStatus', 'user', 'isAuthenticated', 'isAdminRole']),
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

<style lang="less" scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  height: 72px;
  width: 100%;
  z-index: 1000;
  background-color: #fff;
}
.header__menu {
  width: 100%;
}
.header__menu__item {
  width: 100px;
  text-align: center;
  :hover {
    text-decoration: underline;
    text-decoration-color: #8dc63f;
  }
}
</style>
