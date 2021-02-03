<template>
  <div>
    <div style="border: solid 1px green; width:80px; height:80px">
      Logo
    </div>
    <div>
      <p>SKKU</p>
      <p>Coding Platform<p>
    </div>
    <b-form @on-enter="handleLogin" ref="formLogin" :model="formLogin">
        <b-container fluid="xl">
          <b-row class="mb-2">
            <b-form-input v-model="formLogin.username" :placeholder="$t('m.LoginUsername')" @on-enter="handleLogin" />
          </b-row>
          <b-row class="mb-4">
            <b-form-input type="password" v-model="formLogin.password" :placeholder="$t('m.LoginPassword')" @on-enter="handleLogin" />
          </b-row>
          <b-button @click="handleLogin" variant="success" style="width: 260px; height: 36px;">{{$t('m.UserLogin')}}</b-button>
        </b-container>
      </b-form>
      <a class="modal-low" v-if="website.allow_register" @click.stop="handleBtnClick('register')">{{$t('m.No_Account')}}</a>
      <a class="modal-low" @click.stop="goResetPassword" style="float: right">{{$t('m.Forget_Password')}}</a>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import api from '@oj/api'
  import { FormMixin } from '@oj/components/mixins'

  export default {
    mixins: [FormMixin],
    data () {
      const CheckRequiredTFA = (rule, value, callback) => {
        if (value !== '') {
          api.tfaRequiredCheck(value).then(res => {
            this.tfaRequired = res.data.data.result
          })
        }
        callback()
      }

      return {
        tfaRequired: false,
        btnLoginLoading: false,
        formLogin: {
          username: '',
          password: '',
          tfa_code: ''
        },
        ruleLogin: {
          username: [
            {required: true, trigger: 'blur'},
            {validator: CheckRequiredTFA, trigger: 'blur'}
          ],
          password: [
            {required: true, trigger: 'change', min: 6, max: 20}
          ]
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
      handleLogin () {
        this.btnLoginLoading = true
        let formData = Object.assign({}, this.formLogin)
        if (!this.tfaRequired) {
          delete formData['tfa_code']
        }
        api.login(formData).then(res => {
          this.btnLoginLoading = false
          this.changeModalStatus({visible: false})
          this.getProfile()
          this.$success(this.$i18n.t('m.Welcome_back'))
        }, _ => {
          this.btnLoginLoading = false
        })
      },
      goResetPassword () {
        this.changeModalStatus({visible: false})
        this.$router.push({name: 'apply-reset-password'})
      }
    },
    computed: {
      ...mapGetters(['website', 'modalStatus']),
      visible: {
        get () {
          return this.modalStatus.visible
        },
        set (value) {
          this.changeModalStatus({visible: value})
        }
      }
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
