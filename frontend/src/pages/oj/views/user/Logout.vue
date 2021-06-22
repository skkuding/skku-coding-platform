<script>
import api from '../../api.js'

export default {
  async mounted () {
    await api.logout()
    this.$store.dispatch('clearProfile')
    this.$router.replace({
      path: '/'
    })
  }
}
</script>
