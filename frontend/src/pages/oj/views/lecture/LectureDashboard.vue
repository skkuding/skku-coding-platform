<template>
  <div class="dashboard-list-card font-bold">
    <div class="top-bar mb-5">
    <h3 class = "title">프로그래밍 기초와 실습</h3>
    </div>
    <b-row>
    <b-col cols = "8">
    <b-calendar block
      v-model="value"
      class="border rounded p-2 calendar"
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
    <b-row class = "mt-5">
      <b-col >
      <b-button class = "w-100 QnAButton" @click="goQnA">Go to Q&A page</b-button>
      </b-col>
      <b-col>
        <b-button class = "w-100 AssignmentsButton" @click="goAssignments" >Go to Assignments page</b-button>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  name: 'LectureDashboardOj',
  components: {
    // Split into many components
  },
  data () {
    return {
      value: ''
    }
  },
  async mounted () {
  },
  methods: {
    async goQnA () {
      await this.$router.push({
        name: 'lecture-qna'
      })
    },
    async goAssignments () {
      await this.$router.push({
        name: 'lecture-assignment'
      })
    },
    async goAssignmentDetail () {
      await this.$router.push({
        name: 'lecture-assignment-detail'
      })
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

</style>
