<template>
  <!-- Please split into many componenets !-->
  <b-modal
    id="register-new-user"
    title="Register New Students"
    size="md"
    @ok="submitRegistration"
    scrollable
  >
    <p>Register students to {{ courseTitle }}</p>
    <div v-if="showErrorResult" class="text-danger" >
      <p style="font-size: 18px;" >Registration Error! Please Try Again</p>
      <p>{{ getUserNotExistUserList }}</p>
      <p>{{ getAlreadyRegisteredUserList }}</p>
    </div>
    <div style="font-size: 20px;" class="mb-3">
      <b>Enter Student ID </b>
      <div class="float-right">
        <label class="students-button" for="input-file" title="Register with csv file">
          <b-icon-cloud-arrow-up></b-icon-cloud-arrow-up>
        </label>
        <input ref="uploadStudentsInput" @change="uploadStudentsFromCSV" type="file" id="input-file" accept=".csv" style="display: none;"/>
        <button type="button" @click="addStudent" class="students-button" title="Add empty student block" >
          <b-icon-person-plus></b-icon-person-plus>
        </button>
      </div>
    </div>
    <b-form>
      <b-form-input
        v-for="(studentId, index) in form.studentIds" :key="index"
        v-model="studentId.value"
        class="mb-2"
        type="number"
      ></b-form-input>
    </b-form>
    <template #modal-footer="{ ok }">
      <b-button size="sm" variant="success" @click="ok()">
        Register all
      </b-button>
    </template>
  </b-modal>
</template>

<script>
import api from '../../api.js'
import papa from 'papaparse'

export default {
  name: 'RegisterNewUserModal',
  components: {
  },
  props: [
    'course-title'
  ],
  data () {
    return {
      form: {
        studentIds: [
          {
            value: ''
          }
        ]
      },
      semesters: [
        { text: 'Select One', value: null },
        { text: 'Spring', value: 0 },
        { text: 'Summer', value: 1 },
        { text: 'Fall', value: 2 },
        { text: 'Winter', value: 3 }
      ],
      courseId: null,
      showErrorResult: false,
      userNotExistUserList: [],
      alreadyRegisteredUserList: []
    }
  },
  mounted () {
    this.courseId = this.$route.params.courseId
  },
  methods: {
    resetModal () {
      this.form.studentIds = [
        {
          value: ''
        }
      ]
    },
    async submitRegistration (bvModalEvt) {
      bvModalEvt.preventDefault()
      this.showErrorResult = false
      const data = {
        username: this.form.studentIds.filter(studentId => (studentId.value !== '')).map(studentId => studentId.value),
        course_id: this.$route.params.courseId
      }
      const res = await api.registerStudent(data)
      if (!res.data.error && !res.data.data) {
        this.$success('Registration Succeeded')
        this.$emit('update')
        this.resetModal()
        this.$nextTick(() => {
          this.$bvModal.hide('register-new-user')
        })
      } else {
        this.$error('Registration Failed! Please try again')
        this.showErrorResult = true
        this.userNotExistUserList = res.data.data.user_not_exist
        this.alreadyRegisteredUserList = res.data.data.already_registered_user
      }
    },
    handleStudentsCSV (file) {
      papa.parse(file, {
        complete: (results) => {
          try {
            this.form.studentIds = results.data.flat().map(studentId => Object({ value: studentId }))
          } catch (error) {
          }
        },
        error: (error) => {
          this.$error(error)
        }
      })
    },
    async uploadStudentsFromCSV (evt) {
      if (evt.target.files.length !== 0 && this.form.studentIds.length !== 1 && this.form.studentIds[1] !== '') {
        const sure = await this.$bvModal.msgBoxConfirm('Sure to upload student ID by csv file? It will override current student ID inputs', {
          title: 'Are you sure?',
          size: 'md',
          centered: true
        })
        if (sure === true) {
          this.handleStudentsCSV(evt.target.files[0])
        }
      } else {
        this.handleStudentsCSV(evt.target.files[0])
      }
      this.$refs.uploadStudentsInput.value = null
    },
    addStudent () {
      this.form.studentIds.push({
        value: ''
      })
    }
  },
  computed: {
    getUserNotExistUserList () {
      let errorMsg = ''
      if (this.userNotExistUserList !== null && this.userNotExistUserList.length !== 0) {
        errorMsg += 'User does not exist: ' + this.userNotExistUserList.join(', ')
      }
      return errorMsg
    },
    getAlreadyRegisteredUserList () {
      let errorMsg = ''
      if (this.alreadyRegisteredUserList !== null && this.alreadyRegisteredUserList.length !== 0) {
        errorMsg += 'Already Registered User Found: ' + this.alreadyRegisteredUserList.join(', ')
      }
      return errorMsg
    }
  }
}
</script>
<style>
  #register-new-user___BV_modal_title_{
    font-size: 24px
  }
</style>
<style lang="scss">
  .students-button {
    all: unset;
    border-radius: 4px;
    color: #212529;
    cursor: pointer;
    height: 33px;
    padding: 0px 9px 0px 9px;
  }
  .students-button:hover {
    color: #fff;
    background-color: #17a2b8;
    border-color: #17a2b8;
  }
</style>
