<template>
  <div>
    <b-modal ref="modal" centered hide-footer modal-class="modal-md">
    <template>
      <div class="font-bold">
      <div class="logo-title font-bold">
          <h4>Password Reset</h4>
      </div>
        <b-form
          ref="formResetPassword"
          :model="formResetPassword"
          @keydown.enter.native="resetPassword"
        >
        <b-container fluid="xl">
          <b-row class="mb-4">
            <b-form-input
              v-model="formResetPassword.password"
              type="password"
              placeholder="Password"
              @keydown.enter.native="resetPassword"
            >
            </b-form-input>
          </b-row>
          <b-row class="mb-4">
            <b-form-input
              v-model="formResetPassword.passwordAgain"
              type="password"
              placeholder="Password Again"
              @keydown.enter.native="resetPassword"
            >
            </b-form-input>
          </b-row>
          <b-row class="mb-4">
              <div class="oj-captcha">
                <div class="oj-captcha-code">
                  <b-form-input class="captcha-input" v-model="formResetPassword.captcha" placeholder="Captcha" @keydown.enter.native="resetPassword"></b-form-input>
                </div>
                <div class="oj-captcha-img">
                  <img class="captcha-img" :src="captchaSrc" @click="getCaptchaSrc" v-b-tooltip.hover title="Click to refresh"/>
                </div>
              </div>
            </b-row>
          </b-container>
        </b-form>
        <b-button class="sign-btn" variant="primary" @click="resetPassword" style="margin-left:32px;">
          <b-spinner v-if="btnLoading" small></b-spinner> Reset Password
        </b-button>
      </div>
    </template>
    </b-modal>
  </div>
</template>

<script>
import { FormMixin } from '@oj/components/mixins'
import api from '@oj/api'

export default {
  name: 'ResetPassword',
  mixins: [FormMixin],
  data () {
    return {
      btnLoading: false,
      captchaSrc: '',
      resetSuccess: false,
      formResetPassword: {
        captcha: '',
        password: '',
        passwordAgain: '',
        token: ''
      }
    }
  },
  mounted () {
    this.formResetPassword.token = this.$route.params.token
    this.getCaptchaSrc()
    this.showModal()
  },
  methods: {
    async resetPassword () {
      this.btnLoading = true
      const data = Object.assign({}, this.formResetPassword)
      if (data.password !== data.passwordAgain) {
        this.btnLoading = false
        this.formResetPassword.captcha = ''
        this.getCaptchaSrc()
        return this.$error('Password does not match')
      }
      delete data.passwordAgain
      try {
        await api.resetPassword(data)
        this.resetSuccess = true
        this.$success('Update password successfully.\nPlease login with new password.')
        this.$router.push({ name: 'logout' })
      } catch (err) {
        this.btnLoading = false
        this.formResetPassword.captcha = ''
        this.getCaptchaSrc()
      }
    },
    showModal () {
      this.$refs.modal.show()
    },
    hideModal () {
      this.$refs.modal.hide()
    }
  }
}
</script>
<style lang="less" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .container {
    width: 450px;
    margin: auto;
    .center {
      text-align: center;
    }
    .btn {
      margin-top: 18px;
      text-align: center;
    }
  }
  .logo-title {
    margin:8px 0 28px 0;
    color: #8DC63F;
    text-align:center;
  }
  .font-bold {
      font-family: manrope_bold;
  }
  .sign-btn {
    width:284px;
    margin-left:18px;
  }
  .captcha-img {
    margin-right:36px;
    border-radius:8px;
  }
  .captcha-input {
    width:140px;
    margin-left:34px;
  }
  /deep/ .modal-md > .modal-dialog > .modal-content > .modal-header {
    padding-bottom:0;
    padding-top:4px;
  }
  /deep/ .modal-md > .modal-dialog > .modal-content > .modal-body {
    padding-top:0;
  }
  /deep/ .modal-md > .modal-dialog > .modal-content {
    position:absolute;
    top:auto;
    left:auto;
    right:auto;
    bottom:auto;
  }
</style>
