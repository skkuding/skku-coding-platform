<template>
  <!-- Please split into many componenets !-->
  <b-modal
    id="registerNew"
    title="Register New Lecture"
    size="lg"
    @ok="submitNewLecture"
    @cancel="cancelRegistration"
  >
    <b-form>
      <b-form-group
        id="input-group-lecture-title"
        label="Lecture Title"
        label-for="input-lecture-title"
        required
        :state="form.lectureTitle !== ''"
        valid-feedback="Checked"
        invalid-feedback="Lecture Title is required"
      >
        <b-form-input
          id="input-lecture-title"
          v-model="form.lectureTitle"
          placeholder="Enter Title"
          required
          :state="form.lectureTitle !== ''"
        ></b-form-input>
      </b-form-group>
      <b-row>
        <b-col>
          <b-form-group
            id="input-group-course-code"
            label="Course Code"
            label-for="input-course-code"
            required
            :state="form.courseCode.length === 7"
            valid-feedback="Checked"
            invalid-feedback="Invalid course code"
          >
            <b-form-input
              id="input-course-code"
              v-model="form.courseCode"
              placeholder="Example: GED0001"
              required
              :state="form.courseCode.length === 7"
            ></b-form-input>
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group
            id="input-group-class-number"
            label="Class Number"
            label-for="input-class-number"
            required
            :state="form.classNumber !== null"
            valid-feedback="Checked"
            invalid-feedback="Invalid class number"
          >
            <b-form-input
              id="input-class-number"
              v-model="form.classNumber"
              placeholder="Example: 52"
              required
              :state="form.classNumber !== null"
              type="number"
            ></b-form-input>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-form-group
            id="input-group-year"
            label="Year"
            label-for="input-year"
            required
            :state="form.year !== null"
            valid-feedback="Checked"
            invalid-feedback="Registered Year is required"
          >
            <b-form-input
              id="input-year"
              v-model="form.year"
              placeholder="Enter lecture's registered year"
              required
              :state="form.year !== null"
              type="number"
            ></b-form-input>
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group
            id="input-group-semester"
            label="Semester"
            label-for="input-semester"
            required
            :state="form.semester > 2020"
            valid-feedback="Checked"
            invalid-feedback="Registered Semester is required"
          >
            <b-form-select
              id="input-semester"
              v-model="form.semester"
              :options="semesters"
              :state="form.semester > 2020"
            ></b-form-select>
          </b-form-group>
        </b-col>
      </b-row>
    </b-form>
  </b-modal>
</template>

<script>
// import api from '../../api.js'
export default {
  name: 'RegisterNewLectureModal',
  components: {
  },
  data () {
    return {
      form: {
        lectureTitle: '',
        courseCode: '',
        classNumber: null,
        year: null,
        semester: null
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
    async submitNewLecture () {
      // await api.registerNewLecture(this.form)
      alert(this.form)
    }
  },
  computed: {
  }
}
</script>

<style lang="scss">
  // Be careful of common css selector in admin/oj
</style>
