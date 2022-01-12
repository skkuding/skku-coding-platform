<template>
  <b-form
    @submit.stop.prevent
    label-position="left"
    label-width="0px"
    class="demo-ruleForm login-container"
  >
    <h3 class="title">
      Welcome to Login
    </h3>
    <div class = "remember">
      <b-form-group>
        <b-form-input
          id="input-account"
          v-model="account"
          auto-complete="off"
          placeholder="username"
          @keyup.enter="handleLogin"
          :state="accountState"
        />
        <b-form-invalid-feedback id="input-account-feedback">
          Account is required
        </b-form-invalid-feedback>
      </b-form-group>
    </div>
    <div class = "remember">
      <b-form-group>
        <b-form-input
          id="password-account"
          v-model="password"
          type="password"
          auto-complete="off"
          placeholder="password"
          @keyup.enter="handleLogin"
          :state="passwordState"
        />
        <b-form-invalid-feedback id="input-password-feedback">
          Password is required
        </b-form-invalid-feedback>
      </b-form-group>
    </div>
    <div class = "remember">
      <b-form-group style="width:100%;">
        <b-button
          variant="primary"
          style="width:100%;"
          :loading="logining"
          @click="handleLogin"
        >
          GO
        </b-button>
      </b-form-group>
    </div>
  </b-form>
</template>

<script>
import api from '../../api'

export default {
  data () {
    return {
      logining: false,
      account: '',
      password: ''
    }
  },
  methods: {
    async handleLogin () {
      try {
        await api.login(this.account, this.password)
        this.logining = false
        this.$router.push({ name: 'dashboard' })
      } catch (err) {
        this.logining = false
      }
    }
  },
  computed: {
    accountState () {
      return this.account.length > 0
    },
    passwordState () {
      return this.password.length > 0
    }
  }
}
</script>

<style lang="scss" scoped>
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
