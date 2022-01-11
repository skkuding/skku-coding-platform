<template>
  <div class="dashboard-list-card font-bold">
    <div class="mb-5">
      <h5 class = "title"> {{ lecture.title }}_{{lecture.course_code}} </h5>
    </div>
    <b-row class="mt-5">
    <b-col cols = "8">
    <b-calendar block
      v-model="value"
      class="border rounded p-2 calendar"
      :date-info-fn="dateClass"
      @context="onContext"
      selected-variant="success"
      nav-button-variant="secondary"
      locale="en"
      ></b-calendar>
    </b-col>
    <b-col>
      <b-card :title= "value" class = "card h-100">
        <b-button v-if = assignmentExists() class ="AssignmentName w-100" @click="goAssignmentDetail(assignmentFind().id)" variant = "outline-light">
          {{ assignmentFind().title }}
        </b-button>
      </b-card>
    </b-col>
    </b-row>
    <b-row class = "mt-5 justify-content-center">
      <b-col cols = "6">
        <b-button class = "w-100 AssignmentsButton" @click="goAssignments" >Go to Assignments page</b-button>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import api from '@oj/api'
export default {
  name: 'CourseDashboard',
  components: {
    // Split into many components
  },
  data () {
    return {
      value: '',
      courseID: '',
      context: '',
      lecture: {
        title: '',
        course_code: '',
        class_number: '',
        registered_year: '',
        semester: '',
        created_by: ''
      },
      assignment: [],
      datepick: [],
      assignmentnums: [],
      assignmentflag: false
    }
  },
  async mounted () {
    try {
      this.$Loading.start()
      this.courseID = this.$route.params.courseID
      const res = await api.getCourse(this.courseID)
      this.$Loading.finish()
      this.lecture = res.data.data.course
      const res2 = await api.getCourseAssignmentList(this.courseID)
      this.assignment = res2.data.data.results
    } catch (err) {
    }
  },
  methods: {
    async goAssignments () {
      await this.$router.push({
        name: 'lecture-assignment'
      })
    },
    async goAssignmentDetail (id) {
      await this.$router.push({
        name: 'lecture-assignment-detail',
        params: { courseID: this.courseID, assignmentID: id }
      })
    },
    dateClass (ymd, date) {
      const moment = require('moment')
      for (var i in this.assignment) {
        this.assignmentnums.push(i)
        this.datepick.push(moment(date).isBetween(this.assignment[i].start_time, this.assignment[i].end_time) ? date : '')
      }
      for (var j in this.datepick) {
        if (moment(this.datepick[j]).isSame(date)) {
          return 'AssignmentDates'
        }
      }
    },
    onContext (ctx) {
      this.context = ctx
    },
    assignmentFind () {
      const moment = require('moment')
      for (var i in this.datepick) {
        if (moment(this.datepick[i]).isSame(this.value)) {
          return this.assignment[this.assignmentnums[i]]
        }
      }
    },
    assignmentExists () {
      const moment = require('moment')
      var flag = false
      for (var i in this.datepick) {
        if (moment(this.datepick[i]).isSame(this.value)) {
          flag = true
          return true
        }
      }
      if (flag === false) {
        return false
      }
    }
  },
  computed: {
  }
}
</script>

<style lang="scss" scoped>
  .card {
    background-color: lightgray;
    box-shadow: none;
  }
  .font-bold {
    font-family: manrope_bold;
  }
  .title {
    margin-bottom:0;
    color: #7C7A7B;
    display:inline;
    position:relative;
    top:36px;
  }
  .dashboard-list-card {
    margin:0 auto;
    width:70%;
  }
  .calendar::v-deep .form-control {
    width:100%;
    box-shadow: none;
  }
  .calendar::v-deep .b-calendar-grid {
    width:100%;
    box-shadow: none;
  }
  .calendar::v-deep .btn {
    background-color: white;
    color: #4f4f4f;
  }
  .QnAButton {
    background-color: #E9A05A;
    &:hover{
      background-color: #b97f48;
    }
  }
  .AssignmentsButton {
    background-color: #3391E5;
    &:hover{
      background-color: #276fad;
    }
  }
  .AssignmentName {
    background-color: white;
    color : #4f4f4f;
    box-shadow: 0 0 0 1px #4f4f4f;
    &:hover{
      background-color: #c4c4c4;
    }
  }
  .calendar::v-deep .AssignmentDates{
    border-bottom-width: 5px;
    border-bottom-style: solid;
    position: relative;
    border-bottom-color: #8DC63F;
  }
  .button {
    cursor: pointer;
  }

</style>
