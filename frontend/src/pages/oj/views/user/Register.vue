<template>
  <div class="font-bold">
    <div class="logo-title font-bold">
      <h4>Welcome to</h4>
      <h4>SKKU Coding Platform</h4>
    </div>
    <b-form ref="formRegister" :model="formRegister">
      <b-container fluid="xl">
        <b-row class="mb-4">
          <b-form-input type="text" v-model="formRegister.username" placeholder="Student ID" @keydown.enter.native="handleRegister" pattern="[0-9]{10}"></b-form-input>
        </b-row>
        <b-row class="mb-4">
          <b-form-input type="email" v-model="formRegister.email" placeholder="Email Address" @keydown.enter.native="handleRegister"></b-form-input>
        </b-row>
        <b-row class="mb-4">
            <b-form-select class="modal-select" v-model="formRegister.major" :options="majors" @keydown.enter.native="handleRegister"></b-form-select>
        </b-row>
        <b-row class="mb-4">
          <b-form-input type="password" v-model="formRegister.password" placeholder="Password" @keydown.enter.native="handleRegister"></b-form-input>
        </b-row>
        <b-row class="mb-4">
          <b-form-input type="password" v-model="formRegister.passwordAgain" placeholder="Password Again" @keydown.enter.native="handleRegister"></b-form-input>
        </b-row>
        <div class="oj-captcha mb-4">
          <div class="oj-captcha-code">
            <b-form-input v-model="formRegister.captcha" placeholder="Captcha" size="large" @keydown.enter.native="handleRegister"></b-form-input>
          </div>
          <div class="oj-captcha-img">
            <img :src="captchaSrc" @click="getCaptchaSrc" v-b-tooltip.hover title="Click to refresh" style="border-radius:8px !important;"/>
          </div>
        </div>
      </b-container>
    </b-form>
    <b-button variant="primary" @click="handleRegister" class="sign-btn">
      <b-spinner v-if="btnRegisterLoading" small></b-spinner> Register
    </b-button>
    <div class="modal-low mt-3 font-bold" style="text-align:center;">
      <a @click="switchMode('login')">
        <p style="margin-bottom:0">Already have account?</p>
        <p>Sign In</p>
      </a>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import api from '@oj/api'
import { FormMixin } from '@oj/components/mixins'
export default {
  mixins: [FormMixin],
  mounted () {
    this.getCaptchaSrc()
  },
  data () {
    return {
      btnRegisterLoading: false,
      formRegister: {
        username: '',
        password: '',
        passwordAgain: '',
        email: '',
        major: '',
        captcha: ''
      },
      majors: [
        { value: '', text: '-- Select Your Major --', disabled: 'true' },
        { value: 'Major(원전공)', text: 'Major(원전공)' },
        { value: 'Double Major(복수전공)', text: 'Double Major(복수전공)' },
        { value: 'Non-CS Major(비전공)', text: 'Non-CS Major(비전공)' }
      ]
    }
  },
  methods: {
    ...mapActions(['changeModalStatus', 'getProfile']),
    switchMode (mode) {
      this.changeModalStatus({
        mode,
        visible: true
      })
    },
    async handleRegister () {
      const formData = Object.assign({}, this.formRegister)
      if (formData.password !== formData.passwordAgain) {
        return this.$error('Password does not match')
      }
      delete formData.passwordAgain
      this.btnRegisterLoading = true
      try {
        await api.register(formData)
        this.$success('You can login after email authentication. Please check your mailbox.', 2500)
        this.switchMode('login')
        this.btnRegisterLoading = false
      } catch (err) {
        this.getCaptchaSrc()
        this.formRegister.captcha = ''
        this.btnRegisterLoading = false
      }
    }
  },
  computed: {
    ...mapGetters(['website', 'modalStatus'])
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .footer {
    overflow: auto;
    margin-top: 20px;
    margin-bottom: -15px;
    text-align: left;
    .btn {
      margin: 0 0 15px 0;
      &:last-child {
        margin: 0;
      }
    }
  }
  .logo-title {
    margin:8px 0 28px 0;
    color: #8DC63F;
    text-align:center;
  }
  .sign-btn {
    width:284px;
    margin-left:32px;
  }
  .modal-low {
    color:#808080;
    font-size:14px;
  }
  .font-bold {
    font-family: manrope_bold;
  }
  .dropdown button {
    color:black !important;
    background-color:white !important;
    border-radius:8px;
  }
  .modal-select {
    width:280px;
    border-radius:8px;
    border:none;
    box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.25);
    margin-left:36px;
    color:#828282;
  }
  .oj-captcha-img {
    margin-right:20px !important;
    border-radius:4px;
  }
  input::placeholder {
    color: rgb(158, 158, 158)
  }
</style>
