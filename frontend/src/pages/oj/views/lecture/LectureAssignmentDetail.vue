<template>
  <div>
    <sidemenu/>
    <article class="lecture-assignment-card">
      <section class="mb-4">
        <page-title :text="assignment.title"/>
        <div class="assignment-info">
          {{ formatTime(assignment.start_time) + ' ~ ' + formatTime(assignment.end_time) }}
        </div>
      </section>
      <section class="assignment-container">
        <p class="assignment__content" v-dompurify-html="assignment.content" v-katex:auto></p>
        <Table
          hover
          :items="assignmentProblems"
          :fields="assignmentProblemListFields"
          @row-clicked="goAssignmentProblem"
        >
          <template v-slot:_id="data">
            {{data.row._id}}
          </template>
          <template v-slot:title="data">
            {{data.row.title}}
          </template>
          <template v-slot:total_score="data">
            <span v-if="data.row.my_score!==-1">{{ data.row.my_score + ' / ' + data.row.total_score }}</span>
            <span v-else>No Submission</span>
          </template>
        </Table>
      </section>
    </article>
  </div>
</template>

<script>
import sidemenu from '@oj/components/Sidemenu.vue'
import { mapActions } from 'vuex'
import time from '@/utils/time'
import api from '@oj/api'
import PageTitle from '@oj/components/PageTitle.vue'
import Table from '@oj/components/Table.vue'

export default {
  name: 'CourseAssignmentDetail',
  components: {
    sidemenu,
    PageTitle,
    Table
  },
  data () {
    return {
      assignment: {},
      assignmentProblemListFields: [
        {
          key: '_id',
          label: '#'
        },
        {
          key: 'title'
        },
        {
          key: 'total_score',
          label: 'score'
        }
      ],
      assignmentProblems: []
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
    async getAssignmentScore (problemID) {
      const params = {
        myself: '1',
        page: 1,
        problem_id: problemID,
        assignment_id: this.assignmentID
      }
      const result = await api.getAssignmentSubmissionList(0, 1000, params)
      const data = result.data.data.results
      const score = !data.length ? -1 : data[0].statistic_info.score
      return score
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
  .lecture-assignment-card::v-deep{
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
  }
  .assignment-info {
    width: 90%;
    display:flex;
    justify-content: space-between;
    font-size: 12px;
    color: #7C7A7B;
    margin: auto 0 auto 68px;
  }
</style>
