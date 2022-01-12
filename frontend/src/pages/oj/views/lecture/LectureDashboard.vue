<template>
  <div class="dashboard-list-card font-bold">
    <div class="top-bar mb-5" style="margin-top:4px;">
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
      <b-card style="background-color: lightgray" class = "h-100">
      <div>
          {{ value }}
      </div>
      <b-card>
        <div>
        Assignment 3
        </div>
      </b-card>
      </b-card>
    </b-col>
    </b-row>
    <b-row class = "mt-5">
      <b-col >
      <b-button class = "w-100" variant = "warning">Go to Q&A page</b-button>
      </b-col>
      <b-col>
        <b-button class = "w-100" variant = "primary">Go to Assignments page</b-button>
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
    }
  },
  async mounted () {
  },
  methods: {
  },
  computed: {
  }
}
</script>

<style lang="scss" scoped>
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
</style>
