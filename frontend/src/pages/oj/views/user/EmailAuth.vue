<script>
import api from '@oj/api'

export default {
  data () {
    return {
      formEmailAuth: {
        token: ''
      }
    }
  },
  mounted () {
    this.formEmailAuth.token = this.$route.params.token
    const data = Object.assign({}, this.formEmailAuth)
    api.emailAuth(data).then(res => {
      this.$router.replace({
        path: '/'
      })
      this.$success('Email authentication succeeded. Now you can sign in!', 2500)
    })
  }
}
</script>
