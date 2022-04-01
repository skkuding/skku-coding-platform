<template>
  <nav class="flex justify-between items-center px-5 py-3 font-medium content-center sticky top-0 z-50 bg-white opacity-95">
    <a href="/">
        <img
            src="@/assets/logos/signature.png"
            class="h-12 w-auto"
        />
    </a>

    <div>
      <a class="text-2xl text-text-title mr-4 hover:text-green hover:no-underline active:text-green" href="/announcement">Notice</a>
      <a class="text-2xl text-text-title mr-4 hover:text-green hover:no-underline" href="/contest">Contests</a>
      <a class="text-2xl text-text-title mr-4 hover:text-green hover:no-underline" href="/problem">Problems</a>
      <a class="text-2xl text-text-title mr-8 hover:text-green hover:no-underline" href="/lecture">Lecture</a>
    </div>

    <dropdown placement="right" width="w-40" id="dropdown">
      <template v-slot:button>
        <button>
          <icon :icon="['far', 'user']" class="text-text-title text-3xl hover:text-green"/>
        </button>
      </template>

      <template v-slot:content v-if="!isAuthenticated">
        <button @click="handleBtnClick('login')" class="flex w-full justify-between items-center rounded-lg px-3 py-1 my-1 text-base font-medium text-text-title hover:text-green hover:no-underline">Sign In</button>
        <button @click="handleBtnClick('SendEmailAuth')" class="flex w-full justify-between items-center rounded-lg px-3 py-1 my-1 text-base font-medium text-text-title hover:text-green hover:no-underline">Register</button>
      </template>
      <template v-slot:content v-else>
        <button v-if="isAdminRole" @click="goManagement()" class="flex w-full justify-between items-center rounded-lg px-3 py-1 my-1 text-base font-medium text-text-title hover:text-green hover:no-underline">Management</button>
        <a class="flex w-full justify-between items-center rounded-lg px-3 py-1 my-1 text-base text-text-title font-medium hover:text-green hover:no-underline" href="/#">Settings</a>
        <a class="flex w-full justify-between items-center rounded-lg px-3 py-1 my-1 text-base text-text-title hover:text-green hover:no-underline" href="/logout">Sign Out</a>
      </template>
    </dropdown>
    <modal v-if="modalVisible" v-on:close="modalVisible = false">
      <component
        :is="modalStatus.mode"
        v-if="modalVisible"
      />
    </modal>
  </nav>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import Dropdown from './Dropdown.vue'
import Modal from './Modal.vue'
import register from '@oj/views/user/Register'
import login from '@oj/views/user/Login'
import ApplyResetPassword from '@oj/views/user/ApplyResetPassword'
import DeleteAccount from '@oj/views/user/DeleteAccount'
import SendEmailAuth from '@oj/views/user/SendEmailAuth'

export default {
  components: {
    Dropdown,
    Modal,
    login,
    register,
    ApplyResetPassword,
    DeleteAccount,
    SendEmailAuth
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
    },
    goManagement () {
      if (!this.isSuperAdmin) {
        window.open('/professor/')
      } else {
        window.open('/admin/')
      }
    }
  },
  computed: {
    ...mapGetters(['website', 'modalStatus', 'user', 'isAuthenticated', 'isAdminRole', 'isSuperAdmin']),
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
