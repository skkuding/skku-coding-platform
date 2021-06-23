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
  async mounted () {
    this.formEmailAuth.token = this.$route.params.token
    const data = Object.assign({}, this.formEmailAuth)
    await api.emailAuth(data)
    this.$router.replace({
      path: '/'
    })
    this.$success('Email authentication succeeded. Now you can sign in!', 2500)
  }
}
</script>
