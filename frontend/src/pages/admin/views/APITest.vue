<template>
  <div>
    <b-card>
      <h3>Create Course(created by current login user)</h3>
      <b-row class="my-1" v-for="(value, field) in course_fields" :key="field">
        <b-col sm="3">
          <label :for="field">{{ field }}</label>
        </b-col>
        <b-col sm="9">
          <b-form-input :id="field" v-model="value.data"></b-form-input>
        </b-col>
      </b-row>
      <b-button @click="addProfessorCourse()">
        POST
      </b-button>
    </b-card>

    <b-card>
      <h3>Create Assignment</h3>
      <b-row class="my-1" v-for="(value, field) in assignment_fields" :key="field">
        <b-col sm="3">
          <label :for="field">{{ field }}</label>
        </b-col>
        <b-col sm="9">
          <b-form-input :id="field" v-model="value.data"></b-form-input>
        </b-col>
      </b-row>
      <b-form-datepicker
        id="Assignment_Start_Time"
        v-model="assignment.start_date"
        today-button
        close-button
        type="datetime"
        :date-format-options="{ year: 'numeric', month: '2-digit', day: '2-digit' }"
        locale="en"
        placeholder="Start Time"
        style="margin-bottom:10px"
      />
      <b-form-timepicker
        v-model="assignment.start_time"
        show-seconds
        now-button
      >
      </b-form-timepicker>
      <b-form-datepicker
        id="Assignment_End_Time"
        v-model="assignment.end_date"
        today-button
        close-button
        type="datetime"
        :date-format-options="{ year: 'numeric', month: '2-digit', day: '2-digit' }"
        locale="en"
        placeholder="End Time"
        style="margin-bottom:10px"
      />
      <b-form-timepicker
        v-model="assignment.end_time"
        show-seconds
        now-button
      >
      </b-form-timepicker>
      <b-button @click="addProfessorAssignment()">
        POST
      </b-button>
    </b-card>

    <b-card>
      <h3>Register Student</h3>
      <b-row class="my-1" v-for="(value, field) in takes_fields" :key="field">
        <b-col sm="3">
          <label :for="field">{{ field }}</label>
        </b-col>
        <b-col sm="9">
          <b-form-input :id="field" v-model="value.data"></b-form-input>
        </b-col>
      </b-row>
      <b-button @click="registerStudents()">
        POST
      </b-button>
    </b-card>

    <b-card>
      <h3>Get Course List(created by current login user)</h3>
      <p>{{ course_list_prof }}</p>
      <b-button @click="getProfessorCourseList()">
        GET
      </b-button>
    </b-card>

    <b-card>
      <h3>Get Course(professor)</h3>
      <p>{{ course_get_prof }}</p>
      <b-form-input label="course id" v-model="course_id_prof"></b-form-input>
      <b-button @click="getProfessorCourse()">
        GET
      </b-button>
    </b-card>

    <b-card>
      <h3>Get Course List(current login user) - from Takes</h3>
      <p>{{ course_list_student }}</p>
      <b-button @click="getStudentCourseList()">
        GET
      </b-button>
    </b-card>

    <b-card>
      <h3>Get Course(student)</h3>
      <p>{{ course_get_student }}</p>
      <b-form-input label="course id" v-model="course_id_student"></b-form-input>
      <b-button @click="getStudentCourse()">
        GET
      </b-button>
    </b-card>

    <b-card>
      <h3>Get Assignment List</h3>
      <b-button>
        GET
      </b-button>
    </b-card>
  </div>
</template>
<script>
import api from '../api'
import { mapGetters } from 'vuex'
export default {
  name: 'APITest',
  data () {
    return {
      course_fields: {
        title: {
          data: ''
        },
        course_code: {
          data: ''
        },
        class_number: {
          data: ''
        },
        registered_year: {
          data: ''
        },
        semester: {
          data: ''
        }
      },
      assignment_fields: {
        title: {
          data: ''
        },
        content: {
          data: ''
        },
        course_id: {
          data: ''
        }
      },
      takes_fields: {
        course_id: {
          data: ''
        },
        user_id: {
          data: ''
        }
      },
      assignment: {
        start_date: '',
        start_time: '',
        end_date: '',
        end_time: ''
      },
      course_post_response: null,
      assignment_post_response: null,
      takes_post_response: null,
      user_id: '',
      course_id_prof: '',
      course_id_student: '',
      assignment_id: '',
      course_get_prof: '',
      course_get_student: '',
      course_list_prof: '',
      course_list_student: ''
    }
  },
  computed: {
    ...mapGetters(['website', 'modalStatus', 'user', 'isAdminRole'])
  },
  methods: {
    startTime () {
      return this.assignment.start_date + ' ' + this.assignment.start_time
    },
    endTime () {
      return this.assignment.end_date + ' ' + this.assignment.end_time
    },
    async getProfessorCourseList () {
      try {
        const res = await api.getProfessorCourseList(0, 10)
        this.course_list_prof = res.data.data
      } catch (err) {
      }
    },
    async getProfessorCourse () {
      try {
        const res = await api.getProfessorCourse(this.course_id_prof)
        this.course_get_prof = res.data.data
      } catch (err) {
      }
    },
    async getStudentCourseList () {
      try {
        const res = await api.getCourseList(0, 10)
        this.course_list_student = res.data.data
      } catch (err) {
      }
    },
    async getStudentCourse () {
      try {
        const res = await api.getCourse(this.course_id_student)
        this.course_get_student = res.data.data
      } catch (err) {
      }
    },
    async addProfessorCourse () {
      try {
        const data = {
          title: this.course_fields.title.data,
          course_code: this.course_fields.course_code.data,
          class_number: this.course_fields.class_number.data,
          registered_year: this.course_fields.registered_year.data,
          semester: this.course_fields.semester.data
        }
        const res = await api.addProfessorCourse(data)
        this.course_post_response = res.data.data
      } catch (err) {
      }
    },
    async addProfessorAssignment () {
      try {
        const data = {
          title: this.assignment_fields.title.data,
          content: this.assignment_fields.content.data,
          course: this.assignment_fields.course_id.data,
          start_time: this.startTime(),
          end_time: this.endTime()
        }
        const res = await api.addAssignment(data)
        this.assignment_post_response = res.data.data
      } catch (err) {
      }
    },
    async registerStudents () {
      try {
        const data = {
          course_id: this.takes_fields.course_id.data,
          user_id: this.takes_fields.user_id.data
        }
        const res = await api.registerStudent(data)
        this.takes_post_response = res.data.data
      } catch (err) {
      }
    }
  }
}
</script>
