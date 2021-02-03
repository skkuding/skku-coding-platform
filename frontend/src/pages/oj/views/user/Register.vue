<template>
<div>
    <div>
      <p>Welcome to</p>
      <p>SKKU Coding Platform<p>
    </div>
    <b-form ref="formRegister" :model="formRegister">
      <b-container fluid="xl">
        <b-row class="mb-2">
          <b-form-input type="text" v-model="formRegister.username" :placeholder="$t('m.RegisterUsername')" @on-enter="handleRegister" pattern="[0-9]{10}"></b-form-input>
        </b-row>
        <b-row class="mb-2">
          <b-form-input type = "email" v-model="formRegister.email" :placeholder="$t('m.Email_Address')" @on-enter="handleRegister"></b-form-input>
        </b-row>
        <b-row class="mb-2">
          <b-form-select v-model="formRegister.major" :options="majors" placeholder="Major" @on-enter="handleRegister"></b-form-select>
        </b-row>
        <b-row class="mb-2">
          <b-form-input type="password" v-model="formRegister.password" :placeholder="$t('m.RegisterPassword')" @on-enter="handleRegister"></b-form-input>
        </b-row>
        <b-row class="mb-2">
          <b-form-input type="password" v-model="formRegister.passwordAgain" :placeholder="$t('m.Password_Again')"  @on-enter="handleRegister"></b-form-input>
        </b-row>
        <div class="oj-captcha">
          <div class="oj-captcha-code">
            <b-form-input v-model="formRegister.captcha" :placeholder="$t('m.Captcha')" size="large" @on-enter="handleRegister"></b-form-input>
          </div>
        <div class="oj-captcha-img">
          <img :src="captchaSrc" @click="getCaptchaSrc" v-b-tooltip.hover title="Click to refresh"/>
        </div>
      </div>
      </b-container>
    </b-form>
    <div class="footer">
      <Button
        type="primary"
        @click="handleRegister"
        class="btn" long
        :loading="btnRegisterLoading">
        {{$t('m.UserRegister')}}
      </Button>
      <Button
        type="ghost"
        @click="switchMode('login')"
        class="btn" long>
        {{$t('m.Already_Registed')}}
      </Button>
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
      const CheckUsernameNotExist = (rule, value, callback) => {
        api.checkUsernameOrEmail(value, undefined).then(res => {
          if (res.data.data.username === 1) {
            callback(new Error(this.$i18n.t('m.The_username_already_exists')))
          } else if (res.data.data.username === 2) {
            callback(new Error(this.$i18n.t('m.The_username_is_not_student_ID')))
          } else {
            callback()
          }
        }, _ => callback())
      }
      const CheckEmailNotExist = (rule, value, callback) => {
        api.checkUsernameOrEmail(undefined, value).then(res => {
          if (res.data.data.email === 1) {
            callback(new Error(this.$i18n.t('m.The_email_already_exists')))
          } else if (res.data.data.email === 2) {
            callback(new Error(this.$i18n.t('m.The_email_domain_not_match')))
          } else {
            callback()
          }
        }, _ => callback())
      }
      const CheckPassword = (rule, value, callback) => {
        if (this.formRegister.password !== '') {
          // 对第二个密码框再次验证
          this.$refs.formRegister.validateField('passwordAgain')
        }
        callback()
      }

      const CheckAgainPassword = (rule, value, callback) => {
        if (value !== this.formRegister.password) {
          callback(new Error(this.$i18n.t('m.password_does_not_match')))
        }
        callback()
      }

      return {
        btnRegisterLoading: false,
        formRegister: {
          username: '',
          password: '',
          passwordAgain: '',
          email: '',
          major: null,
          captcha: ''
        },
        majors: [
            {value: null, text: 'Major'},
            {value: 'CSE', text: 'Computer Science and Engineering (소프트웨어학과)'},
            {value: 'CS', text: 'Computer Science (컴퓨터공학과)'},
            {value: 'Eng', text: 'Engineering (공학계열)'},
            {value: 'Nat.Sci', text: 'Natural Science (자연과학계열)'},
            {value: 'SOC', text: 'School of Convergence (글로벌융합학부)'},
            {value: 'BE', text: 'Biomedical Engineering (글로벌바이오메디컬공학과)'},
            {value: 'EE', text: 'Electronic and Electrical Engineering (전자전기공학부)'},
            {value: 'SSE', text: 'Semiconductor Systems Engineering (반도체시스템공학과)'},
            {value: 'SS', text: 'Sport Science (스포츠과학과)'},
            {value: 'Phar.', text: 'Pharmacy (약학과)'},
            {value: 'Medi.', text: 'Medicine (의예과/의학과)'},
            {value: 'Others', text: 'Others (이 외 다른 학과)'}
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
      handleRegister () {
        let formData = Object.assign({}, this.formRegister)
        if (formData.password !== formData.passwordAgain) {
          return this.$error('Password does not match')
        }
        delete formData['passwordAgain']
        this.btnRegisterLoading = true
        api.register(formData).then(res => {
          this.$success(this.$i18n.t('m.Thanks_for_registering'))
          this.switchMode('login')
          this.btnRegisterLoading = false
        }, _ => {
          this.getCaptchaSrc()
          this.formRegister.captcha = ''
          this.btnRegisterLoading = false
        })
      }
    },
    computed: {
      ...mapGetters(['website', 'modalStatus'])
    }
  }
</script>

<style scoped lang="less">
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
</style>
