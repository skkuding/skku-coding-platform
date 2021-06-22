import api from '@oj/api'

export default {
  data () {
    return {
      captchaSrc: ''
    }
  },
  methods: {
    async validateForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (!valid) {
          this.$error('please validate the error fields')
        } else {
          return valid
        }
      })
    },
    async getCaptchaSrc () {
      try {
        const res = await api.getCaptcha()
        this.captchaSrc = res.data.data
      } catch (err) {
      }
    }
  }
}
