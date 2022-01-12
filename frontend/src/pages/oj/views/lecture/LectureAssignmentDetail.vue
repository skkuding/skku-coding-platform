<template>
  <div>
    <sidemenu/>
    <article class="lecture-assignment-card">
      <section class="top-bar mb-4">
        <div class="assignment-title">{{ assignment.title }}</div>
        <div class="assignment-info">
          {{ formatTime(assignment.start_time) + ' ~ ' + formatTime(assignment.end_time) }}
        </div>
      </section>
      <section class="assignment-container">
        <p class="assignment__content" v-dompurify-html="assignment.content" v-katex:auto></p>
        <div class="table">
          <b-table
            hover
            :items="assignmentProblems"
            :fields="assignmentProblemListFields"
            head-variant="light"
            class="table"
            style = "cursor: pointer;"
            @row-clicked="goAssignmentProblem"
          >
            <template #cell(total_score)="data">
              {{ data.item.my_score + ' / ' + data.item.total_score }}
            </template>
          </b-table>
        </div>
      </section>
    </article>
  </div>
</template>

<script>
import sidemenu from '@oj/components/Sidemenu.vue'
import { mapActions } from 'vuex'
import time from '@/utils/time'

export default {
  name: 'CourseAssignmentDetail',
  components: {
    sidemenu
  },
  data () {
    return {
      assignment: {},
      assignmentProblemListFields: [
        {
          key: '_id',
          label: '#'
        },
        'title',
        {
          key: 'total_score',
          label: 'score'
        }
      ],
      assignmentProblems: [],
      due: ''
    }
  },
  async mounted () {
    this.assignmentID = this.$route.params.assignmentID
    this.courseID = this.$route.params.courseID
    this.route_name = this.$route.name
    try {
      await this.getCourseAssignment()
      await this.getCourseAssignmentProblemList()
    } catch (err) {
    }
  },
  methods: {
    async getCourseAssignment () {
      try {
        const res = await this.$store.dispatch('getCourseAssignment')
        const data = res.data.data
        this.assignment = data
        this.changeDomTitle({ title: data.title })
      } catch (err) {
      }
    },
    async getCourseAssignmentProblemList () {
      try {
        const res = await this.$store.dispatch('getCourseAssignmentProblemList')
        const data = res.data.data.results
        this.assignmentProblems = data
        for (const assignmentProblem of this.assignmentProblems) {
          const myScore = await this.getAssignmentScore(assignmentProblem._id)
          this.$set(assignmentProblem, 'my_score', myScore)
        }
      } catch (err) {
      }
    },
    async goAssignmentProblem (row) {
      await this.$router.push({
        name: 'lecture-assignment-problem-details',
        params: {
          courseID: this.$route.params.courseID,
          assignmentID: this.$route.params.assignmentID,
          problemID: row._id
        }
      })
    },
    formatTime (timeValue) {
      return time.utcToLocal(timeValue, 'YYYY-M-D HH:mm')
    },
    ...mapActions(['changeDomTitle'])
  },
  computed: {
  },
  watch: {
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .lecture-assignment-card{
    margin: 0 auto;
    width: 70%;
    font-family: Manrope_bold;
    .assignment__content{
      width: 90%;
      margin: 0 auto 20px;
      height: 150px;
      border-radius: 10px;
      background-color: #EDECEC;
      padding: 25px;
      overflow: auto;
    }
    .table{
      width: 95% !important;
      margin: 0 auto;
    }
  }
  .top-bar {
    margin-top: 40px;
    margin-left: 68px;
    & .assignment-title {
      margin-bottom: 10px;
      font-size: 36px;
      color: #7C7A7B;
    }
    & .assignment-info {
      width: 90%;
      display:flex;
      justify-content: space-between;
      font-size: 12px;
      color: #7C7A7B;
      margin: auto 0;
      .due {
        font-weight: 400;
        padding: 5px 10px;
        font-size: 14px;
        background-color: #E9A05A !important;
      }
    }
  }
</style>
