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
      <a v-if="website.allow_register" @click.stop="handleBtnClick('SendEmailAuth')" style="float:left;">Register now</a>
      <a @click.stop="handleBtnClick('ApplyResetPassword')" style="float: right;">Forgot Password</a>
    </div>
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
      formLogin: {
        username: '',
        password: ''
      }
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
  .font-bold {
    font-family: manrope_bold;
  }
</style>
