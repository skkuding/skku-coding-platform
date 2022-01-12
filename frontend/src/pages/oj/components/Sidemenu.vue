<template>
  <div class="Sidemenu">
    <b-card>
      <b-list-group class="menu-container">
        <b-list-group-item class="menu-item" @click="goDashboard">
          <b-icon class="icon" icon="calendar2-check"/>
          <p>Dashboard</p>
        </b-list-group-item>
        <b-list-group-item class="menu-item" @click="goAssignmentList">
          <b-icon class="icon" icon="journal-text"/>
          <p>Assignment</p>
        </b-list-group-item>
        <b-list-group-item class="menu-item" @click="goQuestionList">
          <b-icon class="icon" icon="patch-question"/>
          <p>QnA</p>
        </b-list-group-item>
      </b-list-group>
    </b-card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      courseID: ''
    }
  },
  async mounted () {
    this.courseID = this.$route.params.courseID
  },
  methods: {
    async goDashboard () {
      await this.$router.push({
        name: 'lecture-dashboard',
        params: {
          courseID: this.$route.params.courseID
        }
      })
    },
    async goAssignmentList () {
      await this.$router.push({
        name: 'lecture-assignment',
        params: {
          courseID: this.$route.params.courseID
        }
      })
    },
    async goQuestionList () {
      await this.$router.push({
        name: 'lecture-qna',
        params: {
          courseID: this.$route.params.courseID
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .Sidemenu {
    position: fixed;
    top: 30%;
    right: 70px;
    & .card {
      box-shadow: none !important;
      height: 230px;
    }
    & .menu-item {
      padding: 5px;
      cursor: pointer;
    }
    & .icon {
      display: flex;
      justify-content: center;
      width: 30px;
      height: 30px;
      margin: 0 auto 5px auto;
    }
    & p {
      text-align: center;
      margin: 0;
    }
  }
</style>
