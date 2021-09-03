<template>
  <div>
    <div class="logo">
      <div class="logo-img">
        <img src="@/assets/logos/logo.svg" alt=""/>
      </div>
      <div class="logo-title font-bold">
        <h4>SKKU</h4>
        <h4>Coding Platform</h4>
      </div>
    </div>
    <b-form @on-enter="handleLogin" ref="formLogin" :model="formLogin" class="font-bold">
      <b-container fluid="xl">
        <b-row class="mb-4">
          <b-form-input v-model="formLogin.username" placeholder="Student ID" @keydown.enter.native="handleLogin" />
        </b-row>
        <b-row class="mb-4">
          <b-form-input type="password" v-model="formLogin.password" placeholder="Password" @keydown.enter.native="handleLogin" />
        </b-row>
        <b-button data-loading-text="a" class="sign-btn" @click="handleLogin" variant="outline">
          <b-spinner v-if="btnLoginLoading" small></b-spinner> Sign In
        </b-button>
      </b-container>
    </b-form>
    <div class="modal-low mt-5 font-bold">
      <a v-if="website.allow_register" @click.stop="handleBtnClick('register')" style="float:left;">Register now</a>
      <a @click.stop="handleBtnClick('ApplyResetPassword')" style="float: right;">Forgot Password</a>
    </div>

    <b-modal
      v-model="askEmailAuthVisible"
      hide-footer
      title="authenticate email"
      centered
    >
      <div>
        <p>Your email is "{{ this.email }}"</p>
        <p>Please check your mailbox.</p>
        <p>If there's no mail, then resend or change email</p>
      </div>
      <div>
        <b-button class="email-btn" @click="resendEmail">Resend email</b-button>
        <b-button class="email-btn" @click="handleBtnClick('ChangeEmailForAuth')">Change email</b-button>
      </div>
    </b-modal>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import api from '@oj/api'
import { FormMixin } from '@oj/components/mixins'

export default {
  mixins: [FormMixin],
  data () {
    return {
      btnLoginLoading: false,
      askEmailAuthVisible: false,
      formLogin: {
        username: '',
        password: ''
      },
      email: ''
    }
  },
  methods: {
    ...mapActions(['changeModalStatus', 'getProfile']),
    handleBtnClick (mode) {
      this.changeModalStatus({
        mode,
        visible: true
      })
    },
    async handleLogin () {
      this.btnLoginLoading = true
      const formData = Object.assign({}, this.formLogin)
      try {
        await api.login(formData)
        this.btnLoginLoading = false
        this.changeModalStatus({ visible: false })
        this.getProfile()
        this.$success('Welcome back!')
      } catch (err) {
        this.btnLoginLoading = false
        if (err.data.data === 'You need to authenticate your email') {
          const res = await api.getUserEmail(this.formLogin.username)
          this.email = res.data.data.email
          this.askEmailAuthVisible = true
        }
      }
    },
    async resendEmail () {
      const formData = Object.assign({}, this.formLogin)
      try {
        await api.resendEmailForAuth(formData)
        this.$success('Please check your mailbox.', 2500)
        this.changeModalStatus({ visible: false })
      } catch (err) {
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
  .logo-img {
    display:block;
    width:116px;
    height:136px;
    margin-left:auto;
    margin-right:auto;
    filter:invert(68%) sepia(59%) saturate(458%) hue-rotate(42deg) brightness(94%) contrast(88%);
  }
  .logo-title {
    margin:8px 0 28px 0;
    color: #8DC63F;
    text-align:center;
  }
  .sign-btn {
    width:284px;
    margin-left:18px;
  }
  .modal-low {
    color:#808080;
    font-size:14px;
  }
  .font-bold {
    font-family: manrope_bold;
  }
  .logo-img {
    display:block;
    width:116px;
    height:136px;
    margin-left:auto;
    margin-right:auto;
    filter:invert(68%) sepia(59%) saturate(458%) hue-rotate(42deg) brightness(94%) contrast(88%);
  }
  .logo-title {
    margin:8px 0 28px 0;
    color: #8DC63F;
    text-align:center;
  }
  .sign-btn {
    width:284px;
    margin-left:18px;
  }
  .modal-low {
    color:#808080;
    font-size:14px;
  }
  .email-btn {
    margin-top: 16px;
    margin-left:30px;
  }
  .font-bold {
    font-family: manrope_bold;
  }
</style>
