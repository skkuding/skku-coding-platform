<template>
    <div class="font-bold">
        <div class="logo-title font-bold">
            <h4>Change Email</h4>
        </div>
        <b-form ref="formChangeEmail" :model="formChangeEmail">
            <b-container fluid="xl">
                <b-row class="mb-4">
                    <b-form-input v-model="formChangeEmail.username" placeholder="Student ID"/>
                </b-row>
                <b-row class="mb-4">
                    <b-form-input type="password" v-model="formChangeEmail.password" placeholder="Password"/>
                </b-row>
                <b-row class="mb-4">
                    <b-form-input type="email" v-model="formChangeEmail.email" placeholder="New Email Address"/>
                </b-row>
                <b-button @click="changeEmail" variant="success" class="delete-btn mb-4">
                    <b-spinner v-if="btnLoading" small></b-spinner> Change Email And Request Auth
                </b-button>
            </b-container>
        </b-form>
    </div>
</template>

<script>
import api from '@oj/api'
import { mapActions } from 'vuex'
export default {
  data () {
    return {
      btnLoading: false,
      formChangeEmail: {
        username: '',
        password: '',
        email: ''
      }
    }
  },
  methods: {
    ...mapActions(['changeModalStatus']),
    async changeEmail () {
      const formData = Object.assign({}, this.formChangeEmail)
      this.btnLoading = true
      try {
        await api.changeEmailForAuth(formData)
        this.$success('Please check your mailbox.', 2500)
        this.changeModalStatus({ visible: false })
        this.btnLoading = false
      } catch (err) {
        this.btnLoading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
    @font-face {
        font-family: Manrope_bold;
        src: url('../../../../fonts/Manrope-Bold.ttf');
    }
    .logo-title {
        margin:8px 0 28px 0;
        color: #8DC63F;
        text-align:center;
    }
    .font-bold {
        font-family: manrope_bold;
    }
    .delete-btn {
        width:284px;
        margin-left:18px;
    }
</style>
