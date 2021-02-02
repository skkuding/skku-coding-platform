<template>
  <Panel :padding="30" class="container">
    <div slot="title" class="center">{{$t('m.Email_Authentication')}}</div>
    <template v-if="!authSuccess">
    <Button type="primary"
            @click="emailAuth"
            class="btn" long
            :loading="btnLoading">{{$t('m.Email_Authentication')}}
    </Button>
    </template>
    <template v-else>
      <Alert type="success">{{$t('m.Your_email_has_authenticated')}}</Alert>
    </template>
  </Panel>
</template>

<script>
  import {FormMixin} from '@oj/components/mixins'
  import api from '@oj/api'

  export default {
    name: 'email-auth',
    mixins: [FormMixin],
    data () {
      return {
        btnLoading: false,
        authSuccess: false,
        formEmailAuth: {
          token: ''
        }
      }
    },
    mounted () {
      this.formEmailAuth.token = this.$route.params.token
    },
    methods: {
      emailAuth () {
        this.btnLoading = true
        let data = Object.assign({}, this.formEmailAuth)
        api.emailAuth(data).then(res => {
          this.btnLoading = false
          this.authSuccess = true
          console.log('Email Auth success')
        })
      }
    }
  }
</script>
<style lang="less" scoped>
  .container {
    width: 450px;
    margin: auto;
    .center {
      text-align: center;
    }
  }
</style>
