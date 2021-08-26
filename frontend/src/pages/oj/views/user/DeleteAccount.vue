<template>
    <div class="font-bold">
        <div class="logo-title font-bold">
            <h4>Delete Account</h4>
        </div>
        <b-form ref="formDeleteAccount" :model="formDeleteAccount">
            <b-container fluid="xl">
                <b-row class="mb-4">
                    <b-form-input type="email" v-model="formDeleteAccount.email" placeholder="Your Email Address"/>
                </b-row>
                <b-row class="mb-4">
                    <b-form-input type="password" v-model="formDeleteAccount.password" placeholder="Password"/>
                </b-row>
                <b-button @click="deleteAccount" variant="success" class="delete-btn mb-4">
                    <b-spinner v-if="btnLoading" small></b-spinner> Delete Account
                </b-button>
            </b-container>
        </b-form>
    </div>
</template>

<script>
import api from '@oj/api'
import { mapActions } from 'vuex'
export default {
  data () {
    return {
      btnLoading: false,
      formDeleteAccount: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    ...mapActions(['changeModalStatus']),
    async deleteAccount () {
      const formData = Object.assign({}, this.formDeleteAccount)
      this.btnLoading = true
      try {
        await this.$confirm('Sure to delete your account?', 'confirm', 'warning', false)
        await api.deleteAccount(formData)
        this.btnLoading = false
        this.changeModalStatus({ visible: false })
        this.$store.dispatch('clearProfile')
        this.$router.replace({
          path: '/'
        })
      } catch (err) {
        this.btnLoading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
    @font-face {
        font-family: Manrope_bold;
        src: url('../../../../fonts/Manrope-Bold.ttf');
    }
    .logo-title {
        margin:8px 0 28px 0;
        color: #8DC63F;
        text-align:center;
    }
    .font-bold {
        font-family: manrope_bold;
    }
    .delete-btn {
        width:284px;
        margin-left:18px;
    }
</style>
