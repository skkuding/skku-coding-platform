<template>
  <div class="dashboard-list-card font-bold">
    <div class="mb-5">
      <h3 class = "title"> {{ lecture.title }} </h3>
    </div>
    <b-row>
    <b-col cols = "8">
    <b-calendar block
      v-model="value"
      class="border rounded p-2 calendar"
      :date-info-fn="dateClass"
      selected-variant="success"
      nav-button-variant="secondary"
      locale="en"
      ></b-calendar>
    </b-col>
    <b-col>
      <b-card :title= "value" class = "card h-100">
        <b-button class ="AssignmentName w-100" @click="goAssignmentDetail" variant = "outline-light">
          Assignment 3
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
  name: 'LectureDashboardOj',
  components: {
    // Split into many components
  },
  data () {
    return {
      value: '',
      lectureList: [],
      lecture: {
        title: '',
        status: '',
        start_time: '',
        end_time: ''
      },
      temp: []
    }
  },
  async mounted () {
    try {
      const resp1 = await api.getLectureList()
      const lecturelist = resp1.data.data
      this.lectureList = lecturelist
      const resp2 = await api.getLecture(1)
      this.lecture = resp2.data.data
      const resp3 = await api.getLectureAssignmentList(1)
      this.temp = resp3.data.data
    } catch (err) {
    }
  },
  methods: {
    async goAssignments () {
      await this.$router.push({
        name: 'lecture-assignment'
      })
    },
    async goAssignmentDetail () {
      await this.$router.push({
        name: 'lecture-assignment-detail'
      })
    },
    dateClass (ymd, date) {
      const day = date.getDate()
      return day >= 10 && day <= 20 ? 'AssignmentDates' : ''
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

</style>
