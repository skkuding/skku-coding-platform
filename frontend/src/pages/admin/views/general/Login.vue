<template>
  <b-form
    ref="ruleForm2"
    :model="ruleForm2"
    :rules="rules2"
    label-position="left"
    label-width="0px"
    class="demo-ruleForm login-container"
  >
    <h3 class="title">
      {{ $t('m.Welcome_to_Login') }}
    </h3>
    <div class = "remember">
      <b-form prop="account" >
        <b-input
          v-model="ruleForm2.account"
          type="text"
          auto-complete="off"
          :placeholder="$t('m.username')"
          @keyup.enter.native="handleLogin"
        />
      </b-form>
    </div>
    <div class = "remember">
      <b-form prop="password">
        <b-input
          v-model="ruleForm2.password"
          type="password"
          auto-complete="off"
          :placeholder="$t('m.password')"
          @keyup.enter.native="handleLogin"
        />
      </b-form>
    </div>
    <div class = "remember">
      <b-form style="width:100%;">
        <b-button
          variant="primary"
          style="width:100%;"
          :loading="logining"
          @click.native.prevent="handleLogin"
        >
          {{ $t('m.GO') }}
        </b-button>
      </b-form>
    </div>
  </b-form>
</template>

<script>
import api from '../../api'

export default {
  data () {
    return {
      logining: false,
      ruleForm2: {
        account: '',
        password: ''
      },
      rules2: {
        account: [
          { required: true, trigger: 'blur' }
        ],
        password: [
          { required: true, trigger: 'blur' }
        ]
      },
      checked: true
    }
  },
  methods: {
    handleLogin (ev) {
      this.$refs.ruleForm2.validate((valid) => {
        if (valid) {
          this.logining = true
          api.login(this.ruleForm2.account, this.ruleForm2.password).then(data => {
            this.logining = false
            this.$router.push({ name: 'dashboard' })
          }, () => {
            this.logining = false
          })
        } else {
          this.$error('Please check the error fields')
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
  .login-container {
    /*box-shadow: 0 0px 8px 0 rgba(0, 0, 0, 0.06), 0 1px 0px 0 rgba(0, 0, 0, 0.02);*/
    -webkit-border-radius: 5px;
    border-radius: 5px;
    -moz-border-radius: 5px;
    background-clip: padding-box;
    margin: 180px auto;
    width: 350px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
    .title {
      margin: 0px auto 40px auto;
      text-align: center;
      color: #505458;
    }
    .remember {
    margin: 0px 0px 35px 0px;
    }
  }
</style>
