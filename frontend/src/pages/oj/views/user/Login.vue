<template>
  <div>
    <Form
      ref="formLogin"
      :model="formLogin"
      :rules="ruleLogin"
    >
      <FormItem prop="username">
        <Input
          v-model="formLogin.username"
          type="text"
          :placeholder="$t('m.LoginUsername')"
          size="large"
          @on-enter="handleLogin"
        >
        <Icon
          slot="prepend"
          type="ios-person-outline"
        />
        </Input>
      </FormItem>
      <FormItem prop="password">
        <Input
          v-model="formLogin.password"
          type="password"
          :placeholder="$t('m.LoginPassword')"
          size="large"
          @on-enter="handleLogin"
        >
        <Icon
          slot="prepend"
          type="ios-locked-outline"
        />
        </Input>
      </FormItem>
      <FormItem
        v-if="tfaRequired"
        prop="tfa_code"
      >
        <Input
          v-model="formLogin.tfa_code"
          :placeholder="$t('m.TFA_Code')"
        >
        <Icon
          slot="prepend"
          type="ios-lightbulb-outline"
        />
        </Input>
      </FormItem>
    </Form>
    <div class="footer">
      <Button
        type="primary"
        class="btn"
        long
        :loading="btnLoginLoading"
        @click="handleLogin"
      >
        {{ $t('m.UserLogin') }}
      </Button>
      <a
        v-if="website.allow_register"
        @click.stop="handleBtnClick('register')"
      >{{ $t('m.No_Account') }}</a>
      <a
        style="float: right"
        @click.stop="goResetPassword"
      >{{ $t('m.Forget_Password') }}</a>
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
          { required: true, trigger: 'blur' },
          { validator: CheckRequiredTFA, trigger: 'blur' }
        ],
        password: [
          { required: true, trigger: 'change', min: 6, max: 20 }
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
      this.validateForm('formLogin').then(valid => {
        this.btnLoginLoading = true
        const formData = Object.assign({}, this.formLogin)
        if (!this.tfaRequired) {
          delete formData.tfa_code
        }
        api.login(formData).then(res => {
          this.btnLoginLoading = false
          this.changeModalStatus({ visible: false })
          this.getProfile()
          this.$success(this.$i18n.t('m.Welcome_back'))
        }, _ => {
          this.btnLoginLoading = false
        })
      })
    },
    goResetPassword () {
      this.changeModalStatus({ visible: false })
      this.$router.push({ name: 'apply-reset-password' })
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
