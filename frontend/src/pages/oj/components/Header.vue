<template>
  <div class="header">
    <b-navbar sticky-top style="height: 100%;">
      <b-navbar-brand to="/" class="ml-5" style="width: 0">
        <img
          src="../../../assets/signature.png"
          style="height: 50px; width: auto;"
        />
      </b-navbar-brand>

      <b-navbar-nav class="mx-auto" align="center">
        <b-nav-item class="header__menu">
          <router-link class="nav-link" active-class="active" to="/notice">Notice</router-link>
        </b-nav-item>
        <b-nav-item class="header__menu">
          <router-link class="nav-link" active-class="active" to="/contest">Contests</router-link>
        </b-nav-item>
        <b-nav-item class="header__menu">
          <router-link class="nav-link" active-class="active" to="/problem">Problems</router-link>
        </b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="mr-5" style="width: 0">
        <b-nav-item-dropdown v-if="!isAuthenticated" no-caret right>
          <template slot="button-content">
            <b-icon icon="person" style="width: 36px; height: 36px"></b-icon>
          </template>
          <b-dropdown-item @click="handleBtnClick('login')">Sign In</b-dropdown-item>
          <b-dropdown-item @click="handleBtnClick('register')">Register</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown v-else no-caret right>
          <template slot="button-content">
            <b-icon icon="person" style="width: 36px; height: 36px"></b-icon>
          </template>
          <b-dropdown-item to="/user-home">My Account</b-dropdown-item>
          <b-dropdown-item v-if="isAdminRole" @click="openWindow('/admin/')">Management</b-dropdown-item>
          <b-dropdown-item v-else to="/setting/profile">Setting</b-dropdown-item>
          <b-dropdown-item to="/logout">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
    <b-modal v-model="modalVisible">
      <div slot="header" class="modal-title">
        Welcome to {{ website.website_name_shortcut }}
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
    openWindow (route) {
      window.open(route)
    },
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
  width: 170px;
  &:hover {
    text-decoration: underline;
  }
  .active {
    text-decoration: underline;
  }
}
</style>
