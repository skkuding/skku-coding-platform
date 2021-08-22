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
    <p style="font-size: 20px;">
      <b> lecture Title: {{ lectureTitle }} </b>
    </p>
    <div style="font-size: 20px;" class="mb-3">
      <b>Student ID </b>
      <div class="float-right">
        <label class="students-button" for="input-file">
          <b-icon-cloud-arrow-up></b-icon-cloud-arrow-up>
        </label>
        <input ref="uploadStudentsInput" @change="uploadStudentsFromCSV" type="file" id="input-file" accept=".csv" style="display: none;"/>
        <button type="button" @click="addStudent" class="students-button">
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
    'lecture-title'
  ],
  data () {
    return {
      form: {
        studentIds: [
          {
            value: null
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
      lectureId: null
    }
  },
  mounted () {
    this.lectureId = this.$route.params.lectureId
  },
  methods: {
    async submitRegistration (bvModalEvt) {
      bvModalEvt.preventDefault()
      console.log(this.lectureId)
      for (const studentId of this.form.studentIds) {
        if (studentId.value === null) {
          continue
        }
        const data = {
          course_id: this.lectureId,
          user_id: studentId.value
        }
        try {
          await api.registerStudent(data)
        } catch (error) {
          console.log(error)
        }
      }
      this.$emit('update')
      this.$nextTick(() => {
        this.$bvModal.hide('register-new-user')
      })
    },
    cancelRegistration () {
      // await api.registerNewLecture(this.form)
    },
    handleStudentsCSV (file) {
      papa.parse(file, {
        complete: (results) => {
          try {
            this.form.studentIds = results.data.flat().map(studentId => Object({ value: studentId }))
          } catch (error) {
            this.$error(error)
          }
        },
        error: (error) => {
          this.$error(error)
        }
      })
    },
    async uploadStudentsFromCSV (evt) {
      if (evt.target.files.length !== 0 && this.form.studentIds.length !== 1 && this.form.studentIds[1] !== null) {
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
        value: null
      })
    }
  },
  computed: {
  }
}
</script>
<style>
  #register-new-user___BV_modal_title_{
    font-size: 24px
  }
</style>
<style lang="scss" scoped>
  // Be careful of common css selector in admin/oj
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
