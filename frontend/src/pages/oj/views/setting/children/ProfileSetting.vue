<template>
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
            <b-button class="setting-btn" variant="success" @click="updateProfile" :loading="loadingSaveBtn">
              Change Language
            </b-button>
          </b-row>
      </b-form>
      <b-form>
        <h4 class="columnName font-bold">Major</h4>
          <b-row class="mb-4">
          <b-form-select class="setting-select" v-model="formProfile.major" :options="majors" :selected="formProfile.major"></b-form-select>
          </b-row>
          <b-row>
            <b-button class="setting-btn" variant="success" @click="updateMajor" :loading="loadingSaveBtn">
              Change Major
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
        <b-form-group v-if="visible.tfaRequired" label="Two Factor Auth" prop="tfa_coded">
          <b-form-input class="setting-input" type="password" v-model="formPassword.again_password" required></b-form-input>
        </b-form-group>
        <b-button class="setting-btn" variant="success" @click="changePassword">
          Change Password
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
        <b-form-group v-if="visible.tfaRequired" label="Two Factor Auth" prop="tfa_coded">
          <b-form-input type="text" v-model="formEmail.tfa_code"></b-form-input>
        </b-form-group>
        <b-button class="setting-btn" variant="success" @click="changeEmail">
          Change Email
        </b-button>
      </b-form>
    </div>
  </div>
</template>

<script>
import api from '@oj/api'
import utils from '@/utils/utils'
import { types } from '@/store'

export default {
  data () {
    return {
      loading: {
        btnPassword: false,
        btnEmail: false
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
        { value: null, text: 'Major' },
        { value: 'CS', text: 'Computer Science' },
        { value: 'CSE', text: 'Computer Science and Engineering' },
        { value: 'Eng', text: 'Engineering' },
        { value: 'Nat.Sci', text: 'Natural Science' },
        { value: 'SOC', text: 'School of Convergence' },
        { value: 'BE', text: 'Biomedical Engineering' },
        { value: 'EE', text: 'Electronic and Electrical' },
        { value: 'SSE', text: 'Semiconductor Systems Engineering' },
        { value: 'SS', text: 'Sport Science' },
        { value: 'Phar.', text: 'Pharmacy' },
        { value: 'Medi.', text: 'Medicine' },
        { value: 'Others', text: 'Others' }
      ],
      semesters: [
        { value: null, text: 'Semesters' },
        { value: 1, text: '1~2' },
        { value: 2, text: '3~4' },
        { value: 3, text: '5~6' },
        { value: 4, text: '7+' }
      ],
      formPassword: {
        tfa_code: '',
        old_password: '',
        new_password: '',
        again_password: ''
      },
      visible: {
        passwordAlert: false,
        emailAlert: false,
        tfaRequired: false
      },
      formEmail: {
        tfa_code: '',
        password: '',
        old_email: '',
        new_email: ''
      }
    }
  },
  mounted () {
    const profile = this.$store.state.user.profile
    Object.keys(this.formProfile).forEach(element => {
      if (profile[element] !== undefined) {
        this.formProfile[element] = profile[element]
      }
    })
    const user = this.$store.getters.user
    api.getUser(user.username).then(res => {
      this.formProfile.major = res.data.data.major
      this.formEmail.old_email = res.data.data.email
    })
    api.getUserInfo(user.username).then(res => {
      this.formProfile.language = res.data.data.language
    })
  },
  methods: {
    updateProfile () {
      this.loadingSaveBtn = true
      const updateData = utils.filterEmptyValue(Object.assign({}, this.formProfile))
      api.updateProfile(updateData).then(res => {
        this.$success('Success')
        this.$store.commit(types.CHANGE_PROFILE, { profile: res.data.data })
        this.loadingSaveBtn = false
      }, _ => {
        this.loadingSaveBtn = false
      })
    },
    updateMajor () {
      const major = {
        major: this.formProfile.major
      }
      api.updateUser(major).then(res => {
        this.$success('Success')
      })
    },
    changePassword () {
      this.loading.btnPassword = true
      const data = Object.assign({}, this.formPassword)
      if (data.again_password !== data.new_password) {
        return this.$error('New password does not match')
      }
      if (data.old_password === data.new_password) {
        return this.$error('The new password doesn\'t change')
      }
      delete data.again_password
      if (!this.visible.tfaRequired) {
        delete data.tfa_code
      }
      api.changePassword(data).then(res => {
        this.loading.btnPassword = false
        this.visible.passwordAlert = true
        this.$success('Updated password successfully.\nPlease login with new password.', 2500)
        setTimeout(() => {
          this.$bvModal.hide('setting')
          this.visible.passwordAlert = false
          this.$router.push({ name: 'logout' })
        }, 2500)
      }, res => {
        if (res.data.data === 'tfa_required') {
          this.visible.tfaRequired = true
        }
        this.loading.btnPassword = false
      })
    },
    changeEmail () {
      this.loading.btnEmail = true
      const data = Object.assign({}, this.formEmail)
      if (!this.visible.tfaRequired) {
        delete data.tfa_code
      }
      api.changeEmail(data).then(res => {
        this.loading.btnEmail = false
        this.visible.emailAlert = true
        this.$success('Change email successfully')
      }, res => {
        if (res.data.data === 'tfa_required') {
          this.visible.tfaRequired = true
        }
      })
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

<style lang="less" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../../fonts/Manrope-Bold.ttf');
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
</style>
