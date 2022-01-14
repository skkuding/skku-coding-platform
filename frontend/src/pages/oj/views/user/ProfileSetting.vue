<template>
  <div class="container">
    <div class="setting-main font-bold">
      <div class="section-title logo-title font-bold">
        <h2>Setting</h2>
      </div>
      <div style="display:flex; flex-direction:row; margin-bottom:12px;" class="profileSetting">
        <b-form>
          <h4 class="columnName font-bold">Preferred Language</h4>
            <b-row class="mb-4">
            <b-form-select class="setting-select" v-model="formProfile.language" :options="languages" :selected="formProfile.language"></b-form-select>
            </b-row>
            <b-row class="mb-4">
              <b-button class="setting-btn" variant="success" @click="updateLanguage">
                <b-spinner v-if="loading.btnLanguage" small></b-spinner> Change Language
              </b-button>
            </b-row>
        </b-form>
        <b-form>
          <h4 class="columnName font-bold">Major</h4>
            <b-row class="mb-4">
            <b-form-select class="setting-select" v-model="formProfile.major" :options="majors" :selected="formProfile.major"></b-form-select>
            </b-row>
            <b-row>
              <b-button class="setting-btn" variant="success" @click="updateMajor">
                <b-spinner v-if="loading.btnMajor" small></b-spinner> Change Major
              </b-button>
            </b-row>
        </b-form>
      </div>
      <div style="display:flex; flex-direction:row;" class="accountSetting">
        <b-form>
          <h4 class="columnName font-bold">Change Password</h4>
          <b-form-group class="setting-label" label= "Current Password" prop="old_password">
            <b-form-input class="setting-input" type="password" v-model="formPassword.old_password" required></b-form-input>
          </b-form-group>
          <b-form-group class="setting-label" label="New Password" prop="new_password">
            <b-form-input class="setting-input" type="password" v-model="formPassword.new_password" required></b-form-input>
          </b-form-group>
          <b-form-group class="setting-label" label="Confirm New Password" prop="again_password">
            <b-form-input class="setting-input" type="password" v-model="formPassword.again_password" required></b-form-input>
          </b-form-group>
          <b-button class="setting-btn" variant="success" @click="changePassword">
            <b-spinner v-if="loading.btnPassword" small></b-spinner> Change Password
          </b-button>
        </b-form>
        <b-form>
          <h4 class="columnName font-bold">Change Email</h4>
          <b-form-group class="setting-label" label="Old Email" >
            <b-form-input class="setting-input" v-model="formEmail.old_email" disabled></b-form-input>
          </b-form-group>
          <b-form-group class="setting-label" label="New Email" prop="new_email">
            <b-form-input class="setting-input" type="email" v-model="formEmail.new_email"></b-form-input>
          </b-form-group>
          <b-form-group class="setting-label" label="Current Password" prop="password">
            <b-form-input class="setting-input" type="password" v-model="formEmail.password"></b-form-input>
          </b-form-group>
          <b-button class="setting-btn" variant="success" @click="changeEmail">
            <b-spinner v-if="loading.btnEmail" small></b-spinner> Change Email
          </b-button>
        </b-form>
      </div>
    </div>
    <div class="modal-low mt-5 font-bold">
      <a @click.stop="handleBtnClick('DeleteAccount')" style="float: right;">Delete Account</a>
    </div>
  </div>
</template>

<script>
import api from '@oj/api'
import utils from '@/utils/utils'
import { types } from '@/store'
import { mapActions } from 'vuex'

export default {
  name: 'ProfileSetting',
  data () {
    return {
      loading: {
        btnPassword: false,
        btnEmail: false,
        btnLanguage: false,
        btnMajor: false
      },
      loadingSaveBtn: false,
      loadingUploadBtn: false,
      uploadModalVisible: false,
      preview: {},
      uploadImgSrc: '',
      formProfile: {
        language: '',
        major: null,
        semester: null
      },
      languages: [
        { value: null, text: 'Preferred Language' },
        { value: 'C', text: 'C' },
        { value: 'C++', text: 'C++' },
        { value: 'Golang', text: 'Golang' },
        { value: 'Java', text: 'JAVA' },
        { value: 'Python2', text: 'Python2' },
        { value: 'Python3', text: 'Python3' }
      ],
      majors: [
        { value: 'Major', text: 'Major(원전공)' },
        { value: 'Double Major', text: 'Double Major(복수전공)' },
        { value: 'Non-CS Major', text: 'Non-CS Major(비전공)' }
      ],
      semesters: [
        { value: null, text: 'Semesters' },
        { value: 1, text: '1~2' },
        { value: 2, text: '3~4' },
        { value: 3, text: '5~6' },
        { value: 4, text: '7+' }
      ],
      formPassword: {
        old_password: '',
        new_password: '',
        again_password: ''
      },
      visible: {
        passwordAlert: false,
        emailAlert: false
      },
      formEmail: {
        password: '',
        old_email: '',
        new_email: ''
      }
    }
  },
  async mounted () {
    const profile = this.$store.state.user.profile
    Object.keys(this.formProfile).forEach(element => {
      if (profile[element] !== undefined) {
        this.formProfile[element] = profile[element]
      }
    })
    const user = this.$store.getters.user
    const [res, infoRes] = await Promise.all([api.getUser(user.username), api.getUserInfo(user.username)])
    this.formProfile.major = res.data.data.major
    this.formEmail.old_email = res.data.data.email
    this.formProfile.language = infoRes.data.data.language
  },
  methods: {
    ...mapActions(['changeModalStatus']),
    handleBtnClick (mode) {
      this.$bvModal.hide('setting')
      this.changeModalStatus({
        mode,
        visible: true
      })
    },
    async updateLanguage () {
      this.loading.btnLanguage = true
      const updateData = utils.filterEmptyValue(Object.assign({}, this.formProfile))
      try {
        const res = await api.updateProfile(updateData)
        this.$success('Success')
        this.$store.commit(types.CHANGE_PROFILE, { profile: res.data.data })
      } catch (err) {
      } finally {
        this.loading.btnLanguage = false
      }
    },
    async updateMajor () {
      this.loading.btnMajor = true
      const major = {
        major: this.formProfile.major
      }
      try {
        await api.updateUser(major)
        this.$success('Success')
        this.loading.btnMajor = false
      } catch (err) {
        this.loading.btnMajor = false
      }
    },
    async changePassword () {
      this.loading.btnPassword = true
      const data = Object.assign({}, this.formPassword)
      if (data.again_password !== data.new_password) {
        this.loading.btnPassword = false
        return this.$error('New password does not match')
      }
      if (data.old_password === data.new_password) {
        this.loading.btnPassword = false
        return this.$error('New password doesn\'t change')
      }
      delete data.again_password
      if (!this.visible.tfaRequired) {
        delete data.tfa_code
      }
      try {
        await api.changePassword(data)
        this.loading.btnPassword = false
        this.visible.passwordAlert = true
        this.$success('Updated password successfully.\nPlease login with new password.', 2500)
        this.visible.passwordAlert = false
        setTimeout(() => {
          this.$bvModal.hide('setting')
          this.$router.push({ name: 'logout' })
        }, 2500)
      } catch (err) {
        if (err.data.data === 'tfa_required') {
          this.visible.tfaRequired = true
        }
        this.loading.btnPassword = false
      }
    },
    async changeEmail () {
      this.loading.btnEmail = true
      const data = Object.assign({}, this.formEmail)
      if (!this.visible.tfaRequired) {
        delete data.tfa_code
      }
      try {
        await api.changeEmail(data)
        this.loading.btnEmail = false
        this.visible.emailAlert = true
        this.$success('Email changed successfully')
        this.formEmail.old_email = this.formEmail.new_email
      } catch (err) {
        if (err.data.data === 'tfa_required') {
          this.visible.tfaRequired = true
        }
        this.loading.btnEmail = false
      }
    }
  },
  computed: {
    previewStyle () {
      return {
        width: this.preview.w + 'px',
        height: this.preview.h + 'px',
        overflow: 'hidden'
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
  .container {
    min-width: 800px;
    margin: auto;
    padding: 0;
  }
  .setting-main {
    position: relative;
    margin: 10px 40px;
    padding-bottom: 20px;
    .setting-content {
      margin-left: 20px;
    }
    .mini-container {
      width: 500px;
    }
  }
  .profileSetting {
    display:flex;
    justify-content: space-around;
    margin-bottom:80px;
  }
  .accountSetting {
    display:flex;
    justify-content: space-around;
  }
  .columnName {
    text-align:center;
    margin-bottom:32px;
    color:#808080;
  }
  .logo-title {
    margin:8px 0 16px 0;
    color: #8DC63F;
    text-align:center;
  }
  .font-bold {
    font-family: manrope_bold;
  }
  .setting-label {
    color:#808080;
  }
  .setting-input {
    width:326px;
  }
  .setting-select {
    border-radius: 8px;
    width:326px;
    border:none;
    box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.25);
    color:#828282;
  }
  .setting-btn {
    width:284px;
    display:block;
    margin-left:auto !important;
    margin-right:auto !important;
  }
  .modal-low {
    color:#808080;
    font-size:14px;
  }
</style>
