<template>
  <Panel :padding="30" class="container">
    <div slot="title" class="center">{{$t('m.Reset_Password')}}</div>
    <template v-if="!successApply">
        <b-form ref="formResetPassword" :model="formResetPassword" :rules="ruleLogin">
        <b-container fluid="xl">
          <b-row class="mb-2">
            <b-form-input type="email" v-model="formResetPassword.email" :placeholder="$t('m.ApplyEmail')"/>
          </b-row>
          <b-row class="mb-4">
            <div class="oj-captcha">
              <div class="oj-captcha-code">
                <b-form-input v-model="formResetPassword.captcha" :placeholder="$t('m.RCaptcha')"></b-form-input>
              </div>
              <div class="oj-captcha-img">
                <img :src="captchaSrc" @click="getCaptchaSrc" v-b-tooltip.hover title="Click to refresh"/>
              </div>
            </div>
          </b-row>
          <b-button @click="sendEmail" variant="success" style="width: 260px; height: 36px;">{{$t('m.Send_Password_Reset_Email')}}</b-button>
        </b-container>
      </b-form>
    </template>
    <template v-else>
      <Alert type="success" show-icon>
        {{$t('Success')}}
        <span slot="desc"> {{$t('Password_reset_mail_sent')}}</span>
      </Alert>
    </template>
  </Panel>
</template>
<script>
import api from '@oj/api'
import { FormMixin } from '@oj/components/mixins'

export default {
  mixins: [FormMixin],
  data () {
    const CheckEmailExist = (rule, value, callback) => {
      if (value !== '') {
        api.checkUsernameOrEmail(undefined, value).then(res => {
          if (res.data.data.email === false) {
            callback(new Error(this.$i18n.t('m.The_email_doesnt_exist')))
          } else {
            callback()
          }
        }, _ => callback())
      } else {
        callback()
      }
    }
    return {
      captchaSrc: '',
      successApply: false,
      btnLoading: false,
      formResetPassword: {
        email: '',
        captcha: ''
      },
      ruleResetPassword: {
        email: [
          { required: true, type: 'email', trigger: 'blur' },
          { validator: CheckEmailExist, trigger: 'blur' }
        ],
        captcha: [
          { required: true, trigger: 'blur', min: 1, max: 10 }
        ]
      }
    }
  },
  mounted () {
    this.getCaptchaSrc()
  },
  methods: {
    sendEmail () {
      this.btnLoading = true
      api.applyResetPassword(this.formResetPassword).then(res => {
        // 伪加载
        setTimeout(() => {
          this.btnLoading = false
          this.successApply = true
        }, 2000)
      }, _ => {
        this.btnLoading = false
        this.formResetPassword.captcha = ''
        this.getCaptchaSrc()
      })
    }
  }
}
</script>

<style scoped lang="less">
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
</style>
