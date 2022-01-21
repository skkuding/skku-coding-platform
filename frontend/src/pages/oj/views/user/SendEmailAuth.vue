<template>
    <div class="font-bold">
      <div class="logo-title font-bold">
        <h4>Email Auth For Register</h4>
      </div>
    <template v-if="!successApply">
      <b-form ref="formEmailAuth" :model="formEmailAuth">
        <b-container fluid="xl">
          <b-row class="mb-4">
            <b-form-input type="email" v-model="formEmailAuth.email" placeholder="Your Email Address"/>
          </b-row>
          <b-row class="mb-4">
            <div class="oj-captcha">
              <div class="oj-captcha-code">
                <b-form-input class="captcha-input" v-model="formEmailAuth.captcha" placeholder="Captcha"></b-form-input>
              </div>
              <div class="oj-captcha-img">
                <img class="captcha-img" :src="captchaSrc" @click="getCaptchaSrc" v-b-tooltip.hover title="Click to refresh"/>
              </div>
            </div>
          </b-row>
          <b-button @click="sendEmail" variant="success" class="sign-btn mb-4">
            <b-spinner v-if="btnResetLoading" small></b-spinner> Send Authentication Email
          </b-button>
        </b-container>
      </b-form>
    </template>
    <template v-else>
      <p>Email for authentication is now sent to your email.</p>
      <p>Please Check your mailbox and Authenticate your mail in 20 minutes.</p>
      <p>If you haven't received the mail, <a href="http://pf.kakao.com/_UKraK/chat">contact us</a>.</p>
    </template>
  </div>
</template>

<script>
import api from '@oj/api'
import { FormMixin } from '@oj/components/mixins'
import { mapGetters, mapActions } from 'vuex'

export default {
  mixins: [FormMixin],
  data () {
    return {
      captchaSrc: '',
      successApply: false,
      btnResetLoading: false,
      formEmailAuth: {
        email: '',
        captcha: ''
      }
    }
  },
  mounted () {
    this.getCaptchaSrc()
  },
  methods: {
    ...mapActions(['changeModalStatus']),
    async sendEmail () {
      this.btnResetLoading = true
      try {
        await api.sendEmailAuth(this.formEmailAuth)
        setTimeout(() => {
          this.btnResetLoading = false
          this.successApply = true
        }, 2000)
      } catch (err) {
        this.btnResetLoading = false
        this.formResetPassword.captcha = ''
        this.getCaptchaSrc()
      }
    }
  },
  computed: {
    ...mapGetters(['website', 'modalStatus']),
    visible: {
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
  .modal-low {
      color:#808080;
      font-size:14px;
  }
  .captcha-img {
    margin-right:36px;
    border-radius:8px;
    cursor: pointer;
  }
  .captcha-input {
    width:140px;
    margin-left:34px;
  }
</style>
