<template>
  <div class="header">
    <b-navbar sticky-top style="height: 100%;">
      <b-navbar-brand to="/" class="ml-5" style="width: 0">
        <img
          src="@/assets/logos/signature.png"
          style="height: 50px; width: auto;"
        />
      </b-navbar-brand>

      <b-navbar-nav class="mx-auto" align="center">
        <b-nav-item class="header__menu">
          <router-link class="nav-link" active-class="active" to="/announcement">Notice</router-link>
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
          <b-dropdown-item v-if="isAdminRole" @click="openWindow('/admin/')">Management</b-dropdown-item>
          <b-dropdown-item v-b-modal.setting>Setting</b-dropdown-item>
          <b-dropdown-item to="/logout">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
    <b-modal v-model="modalVisible" hide-footer centered modal-class="modal-med">
      <component
        :is="modalStatus.mode"
        v-if="modalVisible"
      />
    </b-modal>
    <b-modal id="setting" size="xl" hide-footer centered modal-class="modal-med modal-big">
      <profileSetting></profileSetting>
    </b-modal>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import register from '@oj/views/user/Register'
import login from '@oj/views/user/Login'
import profileSetting from '@oj/views/user/ProfileSetting'
import ApplyResetPassword from '@oj/views/user/ApplyResetPassword'
import DeleteAccount from '@oj/views/user/DeleteAccount'

export default {
  components: {
    login,
    register,
    profileSetting,
    ApplyResetPassword,
    DeleteAccount
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

<style lang="scss" scoped>
  #header {
    position: relative;
    height: 72px;
    width: 100%;
    z-index: 1000;
    background-color: #fff;
    border-bottom: 2px solid #E2E2E2;
  }
  .header__menu {
    width: 100%;
  }
  .header__menu__item {
    width: 100px;
    text-align: center;
    &:hover {
      text-decoration: underline;
      text-decoration-color: #8dc63f;
    }
  }
  ::v-deep .modal-med {
    .modal-dialog {
      .modal-content {
        position:absolute;
        top:auto;
        left:auto;
        right:auto;
        bottom:auto;
        .modal-header {
          padding-bottom:0;
          padding-top:4px;
        }
        .modal-body {
          padding-top:0;
        }
      }
    }
  }
  ::v-deep .modal-big {
    .modal-dialog {
      .modal-content {
        min-width:800px;
      }
    }
  }
</style>
