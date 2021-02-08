<template>
  <div>
    <Form
      ref="formRegister"
      :model="formRegister"
      :rules="ruleRegister"
    >
      <FormItem prop="username">
        <Input
          v-model="formRegister.username"
          type="text"
          :placeholder="$t('m.RegisterUsername')"
          size="large"
          @on-enter="handleRegister"
        >
        <Icon
          slot="prepend"
          type="ios-person-outline"
        />
        </Input>
      </FormItem>
      <FormItem prop="email">
        <Input
          v-model="formRegister.email"
          :placeholder="$t('m.Email_Address')"
          size="large"
          @on-enter="handleRegister"
        >
        <Icon
          slot="prepend"
          type="ios-email-outline"
        />
        </Input>
      </FormItem>
      <FormItem prop="major">
        <Select
          v-model="formRegister.major"
          :placeholder="$t('m.RegisterMajor')"
          size="large"
          class="adjust"
          @on-enter="handleRegister"
        >
          <Icon
            slot="prepend"
            type="ios-book-outline"
          />
          <Option
            v-for="item in majors"
            :key="item"
            :value="item"
          >
            {{ item }}
          </Option>
        </Select>
      </FormItem>
      <FormItem prop="password">
        <Input
          v-model="formRegister.password"
          type="password"
          :placeholder="$t('m.RegisterPassword')"
          size="large"
          @on-enter="handleRegister"
        >
        <Icon
          slot="prepend"
          type="ios-locked-outline"
        />
        </Input>
      </FormItem>
      <FormItem prop="passwordAgain">
        <Input
          v-model="formRegister.passwordAgain"
          type="password"
          :placeholder="$t('m.Password_Again')"
          size="large"
          @on-enter="handleRegister"
        >
        <Icon
          slot="prepend"
          type="ios-locked-outline"
        />
        </Input>
      </FormItem>
      <FormItem
        prop="captcha"
        style="margin-bottom:10px"
      >
        <div class="oj-captcha">
          <div class="oj-captcha-code">
            <Input
              v-model="formRegister.captcha"
              :placeholder="$t('m.Captcha')"
              size="large"
              @on-enter="handleRegister"
            >
            <Icon
              slot="prepend"
              type="ios-lightbulb-outline"
            />
            </Input>
          </div>
          <div class="oj-captcha-img">
            <Tooltip
              content="Click to refresh"
              placement="top"
            >
              <img
                :src="captchaSrc"
                @click="getCaptchaSrc"
              >
            </Tooltip>
          </div>
        </div>
      </FormItem>
    </Form>
    <div class="footer">
      <Button
        type="primary"
        class="btn"
        long
        :loading="btnRegisterLoading"
        @click="handleRegister"
      >
        {{ $t('m.UserRegister') }}
      </Button>
      <Button
        type="ghost"
        class="btn"
        long
        @click="switchMode('login')"
      >
        {{ $t('m.Already_Registed') }}
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
        major: '',
        captcha: ''
      },
      ruleRegister: {
        username: [
          { required: true, trigger: 'blur' },
          { validator: CheckUsernameNotExist, trigger: 'blur' }
        ],
        email: [
          { required: true, type: 'email', trigger: 'blur' },
          { validator: CheckEmailNotExist, trigger: 'blur' }
        ],
        major: [
          { required: true, trigger: 'blur' }
        ],
        password: [
          { required: true, trigger: 'blur', min: 6, max: 20 },
          { validator: CheckPassword, trigger: 'blur' }
        ],
        passwordAgain: [
          { required: true, validator: CheckAgainPassword, trigger: 'change' }
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
    ...mapActions(['changeModalStatus', 'getProfile']),
    switchMode (mode) {
      this.changeModalStatus({
        mode,
        visible: true
      })
    },
    handleRegister () {
      this.validateForm('formRegister').then(valid => {
        const formData = Object.assign({}, this.formRegister)
        delete formData.passwordAgain
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
      })
    }
  },
  props: {
    majors: {
      type: Array,
      default: () => {
        return [
          'Computer Science and Engineering (소프트웨어학과)',
          'Computer Science (컴퓨터공학과)',
          'Engineering (공학계열)',
          'Natural Science (자연과학계열)',
          'School of Convergence (글로벌융합학부)',
          'Biomedical Engineering (글로벌바이오메디컬공학과)',
          'Electronic and Electrical Engineering (전자전기공학부)',
          'Semiconductor Systems Engineering (반도체시스템공학과)',
          'Sport Science (스포츠과학과)',
          'Pharmacy (약학과)',
          'Medicine (의예과/의학과)'
        ]
      }
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
