<template>
  <div class="setting-main">
    <div class="section-title" style="text-align:center">{{$t('m.Profile_Setting')}}</div>
    <div style="display:flex; flex-direction:row;" class="profileSetting">
      <b-form>
        <h3 class="columnName">{{$t('m.Preferred_Language')}}</h3>
          <b-form-select v-model="formProfile.language" :options="language_tmp"></b-form-select>
        <b-button variant="success" @click="updateProfile" :loading="loadingSaveBtn">
          {{$t('m.Change_Language')}}
        </b-button>
      </b-form>

      <b-form>
        <h3 class="columnName">{{$t('m.Major')}}</h3>
          <b-form-select v-model="formProfile.major" :options="majors" :selected="formProfile.major"></b-form-select>
        <b-button variant="success" @click="updateProfile" :loading="loadingSaveBtn">
          {{$t('m.Change_Major')}}
        </b-button>
      </b-form>

      <b-form>
        <h3 class="columnName">{{$t('m.Semester')}}</h3>
          <b-form-select v-model="formProfile.semester" :options="semesters" :selected="formProfile.semester"></b-form-select>
        <b-button variant="success" @click="updateProfile" :loading="loadingSaveBtn">
          {{$t('m.Change_Semester')}}
        </b-button>
      </b-form>
    </div>

    <div style="display:flex; flex-direction:row;" class="accountSetting">
      <b-form>
        <h3 class="columnName">{{$t('m.ChangePassword')}}</h3>
        <b-form-group label="Current Password" prop="old_password">
          <b-form-input type="password" v-model="formPassword.old_password" required></b-form-input>
        </b-form-group>
        <b-form-group label="New Password" prop="new_password">
          <b-form-input type="password" v-model="formPassword.new_password" required></b-form-input>
        </b-form-group>
        <b-form-group label="Confirm New Password" prop="again_password">
          <b-form-input type="password" v-model="formPassword.again_password" required></b-form-input>
        </b-form-group>
        <b-form-group v-if="visible.tfaRequired" label="Two Factor Auth" prop="tfa_coded">
          <b-form-input type="password" v-model="formPassword.again_password" required></b-form-input>
        </b-form-group>
        <b-form-group v-if="visible.passwordAlert">
          <b-alert variant="success">You will need to login again after 5 seconds..</b-alert>
        </b-form-group>
        <b-button variant="success" @click="changePassword">
          {{$t('m.ChangePassword')}}
        </b-button>
      </b-form>

        <b-form>
        <h3 class="columnName">{{$t('m.ChangeEmail')}}</h3>
        <b-form-group label="Old Email" >
          <b-form-input v-model="formEmail.old_email" disabled></b-form-input>
        </b-form-group>
        <b-form-group label="New Email" prop="new_email">
          <b-form-input type="email" v-model="formEmail.new_email"></b-form-input>
        </b-form-group>
        <b-form-group label="Current Password" prop="password">
          <b-form-input type="password" v-model="formEmail.password"></b-form-input>
        </b-form-group>
        <b-form-group v-if="visible.tfaRequired" label="Two Factor Auth" prop="tfa_coded">
          <b-form-input type="text" v-model="formEmail.tfa_code"></b-form-input>
        </b-form-group>
        <b-button variant="success" @click="changeEmail">
          {{$t('m.ChangeEmail')}}
        </b-button>
      </b-form>

    </div>
  </div>
</template>

<script>
import api from '@oj/api'
import utils from '@/utils/utils'
// import { VueCropper } from 'vue-cropper'
import { types } from '@/store'

export default {
  components: {
    // VueCropper
  },
  data () {
    // const oldPasswordCheck = [{required: true, trigger: 'blur', min: 6, max: 20}]
    //   const tfaCheck = [{required: true, trigger: 'change'}]
    //   const CheckAgainPassword = (rule, value, callback) => {
    //     if (value !== this.formPassword.new_password) {
    //       callback(new Error('password does not match'))
    //     }
    //     callback()
    //   }
    //   const CheckNewPassword = (rule, value, callback) => {
    //     if (this.formPassword.old_password !== '') {
    //       if (this.formPassword.old_password === this.formPassword.new_password) {
    //         callback(new Error('The new password doesn\'t change'))
    //       } else {
    //         // 对第二个密码框再次验证
    //         this.$refs.formPassword.validateField('again_password')
    //       }
    //     }
    //     callback()
    //   }
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
      avatarOption: {
        imgSrc: '',
        size: 0.8,
        outputType: 'png'
      },
      formProfile: {
        language: '',
        major: null,
        semester: null
      },
      language_tmp: [
        { value: null, text: 'Please select an option' },
        { value: 'a', text: 'This is First option' },
        { value: 'b', text: 'Selected Option' },
        { value: 'c', text: 'This is an option with object value' },
        { value: 'd', text: 'This one is disabled', disabled: true }
      ],
      majors: [
        { value: null, text: 'Major' },
        { value: 'CS', text: 'Computer Science (컴퓨터공학과)' },
        { value: 'CSE', text: 'Computer Science and Engineering (소프트웨어학과)' },
        { value: 'Eng', text: 'Engineering (공학계열)' },
        { value: 'Nat.Sci', text: 'Natural Science (자연과학계열)' },
        { value: 'SOC', text: 'School of Convergence (글로벌융합학부)' },
        { value: 'BE', text: 'Biomedical Engineering (글로벌바이오메디컬공학과)' },
        { value: 'EE', text: 'Electronic and Electrical Engineering (전자전기공학부)' },
        { value: 'SSE', text: 'Semiconductor Systems Engineering (반도체시스템공학과)' },
        { value: 'SS', text: 'Sport Science (스포츠과학과)' },
        { value: 'Phar.', text: 'Pharmacy (약학과)' },
        { value: 'Medi.', text: 'Medicine (의예과/의학과)' },
        { value: 'Others', text: 'Others (이 외 다른 학과)' }
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
      // rulePassword: {
      //   old_password: oldPasswordCheck,
      //   new_password: [
      //     { required: true, trigger: 'blur', min: 6, max: 20 },
      //     { validator: CheckNewPassword, trigger: 'blur' }
      //   ],
      //   again_password: [
      //     { required: true, validator: CheckAgainPassword, trigger: 'change' }
      //   ],
      //   tfa_code: tfaCheck
      // },
      // ruleEmail: {
      //   password: oldPasswordCheck,
      //   new_email: [{required: true, type: 'email', trigger: 'change'}],
      //   tfa_code: tfaCheck
      // }
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
    this.formEmail.old_email = this.$store.getters.user.email || ''
    this.formProfile.major = user.major
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
        this.$success('Update password successfully')
        setTimeout(() => {
          this.visible.passwordAlert = false
          this.$router.push({ name: 'logout' })
        }, 3000)
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
  .inline {
    display: inline-block;
  }

  .copper-img {
    width: 400px;
    height: 300px;
  }

  .flex-container {
    flex-wrap: wrap;
    justify-content: flex-start;
    margin-bottom: 10px;
    .cropper-main {
      flex: none;
      .copper-img;
    }
    .cropper-btn {
      flex: none;
      vertical-align: top;
    }
    .cropper-preview {
      flex: none;
      /*margin: 10px;*/
      margin-left: 20px;
      box-shadow: 0 0 1px 0;
      .copper-img;
    }
  }

  .upload-modal {
    .notice {
      font-size: 16px;
      display: inline-block;
      vertical-align: top;
      padding: 10px;
      padding-right: 15px;
    }
    img {
      box-shadow: 0 0 1px 0;
      border-radius: 50%;
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
</style>
