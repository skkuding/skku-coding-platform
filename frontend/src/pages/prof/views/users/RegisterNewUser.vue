<template>
  <!-- Please split into many componenets !-->
  <b-modal
    id="register-new-user"
    title="Register New Students"
    size="md"
    @ok="submitRegistration"
    @cancel="cancelRegistration"
    scrollable
  >
    <p style="font-size: 22px;">
      <b>Lecture Title: 공학컴퓨터 프로그래밍</b>
    </p>
    <div style="font-size: 22px;" class="mb-3">
      <b>Student ID </b>
      <div class="float-right">
        <b-button type="button" @click="registerByCSVFile" variant="outline-info" title="" sqaured >
          <b-icon-cloud-arrow-up></b-icon-cloud-arrow-up>
        </b-button>
        <b-button type="button" variant="outline-info" sqaured>
          <b-icon-person-plus></b-icon-person-plus>
        </b-button>
      </div>
    </div>
    <b-form>
      <!-- <b-form-group
        id="input-group-student-id"
        label="Student ID"
        label-for="input-student-id"
        required
        :state="form.lectureTitle !== ''"
      >
      valid-feedback="Checked"
        invalid-feedback="Invalid Student Id" -->
        <b-form-input
          v-for="studentId in form.studentIds" :key="studentId.id"
          id="input-student-id"
          v-model="studentId.value"
          required
          :state="studentId.value !== '' "
          class="mb-2"
        ></b-form-input>
        <b-form-file
          v-if="!uploadUsers.length"
          v-model="uploadUsersFile"
          accept=".csv"
        ></b-form-file>
      <!-- </b-form-group> -->
    </b-form>
  </b-modal>
</template>

<script>
// import api from '../../api.js'
import papa from 'papaparse'

export default {
  name: 'RegisterNewUserModal',
  components: {
  },
  data () {
    return {
      form: {
        lectureId: 1,
        studentIds: [{
          id: 1,
          value: '2020311666'
        },
        {
          id: 2,
          value: '2020311667'
        }
        ]
      },
      semesters: [
        { text: 'Select One', value: null },
        { text: 'Spring', value: 0 },
        { text: 'Summer', value: 1 },
        { text: 'Fall', value: 2 },
        { text: 'Winter', value: 3 }
      ]
    }
  },
  methods: {
    submitRegistration () {
      // await api.registerNewLecture(this.form)
      alert(this.form)
    },
    cancelRegistration () {
      // await api.registerNewLecture(this.form)
    },
    handleUsersCSV (file) {
      papa.parse(file, {
        complete: (results) => {
          const data = results.data.filter(user => {
            return user[0] && user[1] && user[2]
          })
          const delta = results.data.length - data.length
          if (delta > 0) {
            this.$warning(delta + ' users have been filtered due to empty value')
          }
          this.uploadUsersCurrentPage = 1
          this.uploadUsers = data
          this.uploadUsersPage = data.slice(0, this.uploadUsersPageSize)
        },
        error: (error) => {
          this.$error(error)
        }
      })
    },
    registerStudentsByFile () {
      if (this.form.studentIds.length !== 0) {
        const sure = this.$bvModal.msgBoxConfirm('Are you sure?')
        if (sure === true) {
          this.handleStudentsCSV()
        }
      }
    }
  },
  computed: {
  }
}
</script>

<style lang="scss">
  // Be careful of common css selector in admin/oj
</style>
