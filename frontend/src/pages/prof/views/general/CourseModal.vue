<template>
  <b-modal
    id="registerNew"
    :title="modalTitle"
    size="lg"
    @ok="submitCourse"
    @cancel="cancelRegistration"
  >
    <b-form>
      <b-form-group
        id="input-group-course-title"
        label="Course Title"
        label-for="input-course-title"
        required
        :state="form.courseTitle !== ''"
        valid-feedback="Checked"
        invalid-feedback="Course Title is required"
      >
        <b-form-input
          id="input-course-title"
          v-model="form.courseTitle"
          placeholder="Enter Title"
          required
          :state="form.courseTitle !== ''"
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
              placeholder="Enter course's registered year"
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
            :state="form.semester !== null"
            valid-feedback="Checked"
            invalid-feedback="Registered Semester is required"
          >
            <b-form-select
              id="input-semester"
              v-model="form.semester"
              :options="semesters"
              :state="form.semester !== null"
            ></b-form-select>
          </b-form-group>
        </b-col>
      </b-row>
    </b-form>
  </b-modal>
</template>

<script>
import api from '../../api.js'
export default {
  name: 'RegisterNewCourseModal',
  props: ['mode', 'courseId'],
  components: {
  },
  data () {
    return {
      form: {
        courseTitle: '',
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
      ],
      modalTitle: ''
    }
  },
  async mounted () {
    if (this.mode === 'create') {
      this.modalTitle = 'Register New Course'
      this.form = {
        courseTitle: '',
        courseCode: '',
        classNumber: null,
        year: null,
        semester: null
      }
    } else {
      this.modalTitle = 'Edit Course'
      const res = await api.getCourseList(this.courseId)
      const course = res.data.data
      this.form = {
        courseTitle: course.title,
        courseCode: course.course_code,
        classNumber: course.class_number,
        year: course.registered_year,
        semester: course.semester
      }
    }
  },
  methods: {
    init () {
      this.form = {
        courseTitle: '',
        courseCode: '',
        classNumber: null,
        year: null,
        semester: null
      }
    },
    async submitCourse (bvModalEvt) {
      bvModalEvt.preventDefault()
      if (this.mode === 'create') {
        const data = {
          title: this.form.courseTitle,
          course_code: this.form.courseCode,
          class_number: this.form.classNumber,
          registered_year: this.form.year,
          semester: this.form.semester
        }
        await api.createCourse(data)
      } else {
        const data = {
          id: this.courseId,
          title: this.form.courseTitle,
          course_code: this.form.courseCode,
          class_number: this.form.classNumber,
          registered_year: this.form.year,
          semester: this.form.semester
        }
        await api.editCourse(data)
      }
      this.$emit('submitCourseData')
      this.$nextTick(() => {
        this.$bvModal.hide('registerNew')
      })
      this.init()
    }
  },
  computed: {
  }
}
</script>

<style lang="scss">
</style>
