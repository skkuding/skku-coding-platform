<template>
  <div>
    <Sidemenu/>
    <article class="lecture-assignment-card">
      <div class="top-bar mb-4">
        <h2 class="title">Lecture Assignments</h2>
      </div>
      <div class="table">
        <b-table
          hover
          :items="assignments"
          :fields="assignmentListFields"
          head-variant="light"
          class="table"
          @row-clicked="goAssignment"
        >
          <template #cell(title)="data">
            {{ data.value }}
            <b-badge
              variant="light"
              style="border: solid 1px #EDECEC; margin-left: 16px;"
            >
              <b-icon
                icon="circle-fill"
                scale="0.7"
                :style="'color:' + assignmentStatus(data.item.status).color"
              >
              </b-icon>
              {{ assignmentStatus(data.item.status).name }}
            </b-badge>
          </template>
          <template #cell(accepted_problem)="data">
            <span v-if="data.item.accepted_problem === 0">Not Accepted</span>
            <span v-else>{{ data.item.accepted_problem + '/' + data.item.total_problem + ' Accepted'}}</span>
          </template>
        </b-table>
      </div>
      <div class="pagination">
        <b-pagination
          v-model="currentPage"
          :total-rows="assignment.length"
          :per-page="perPage"
          limit="3"
        ></b-pagination>
      </div>
    </article>
  </div>
</template>

<script>
import Sidemenu from '@oj/components/Sidemenu.vue'
import { ASSIGNMENT_STATUS_REVERSE, ASSIGNMENT_STATUS, ASSIGNMENT_SUBMISSION_STATUS, ASSIGNMENT_SUBMISSION_STATUS_REVERSE } from '@/utils/constants'
import api from '@oj/api'
// import utils from '@/utils/utils'
import moment from 'moment'

export default {
  name: 'LectureAssignmentList',
  components: {
    Sidemenu
  },
  data () {
    return {
      page: 1,
      courseID: '',
      assignmentListFields: [
        {
          key: 'title',
          label: 'Assignment'
        },
        {
          key: 'end_time',
          label: 'Due',
          formatter: endTime => {
            return moment(endTime).format('YYYY-M-D hh:mm')
          }
        },
        {
          key: 'accepted_problem',
          label: 'Accepted'
        }
      ],
      assignments: [],
      assignment: '',
      ASSIGNMENT_STATUS: ASSIGNMENT_STATUS,
      ASSIGNMENT_STATUS_REVERSE: ASSIGNMENT_STATUS_REVERSE,
      ASSIGNMENT_SUBMISSION_STATUS: ASSIGNMENT_SUBMISSION_STATUS,
      ASSIGNMENT_SUBMISSION_STATUS_REVERSE: ASSIGNMENT_SUBMISSION_STATUS_REVERSE,
      submission: ''
    }
  },
  async mounted () {
    this.courseID = this.$route.params.courseID
    this.route_name = this.$route.name
    const res = await api.getLectureAssignmentList(this.courseID)
    this.assignments = res.data.data.results
    console.log(res)
    console.log(res.data.data.results)
  },
  methods: {
    async goAssignment (assignment) {
      this.assignment = assignment
      this.listVisible = false
      await this.$router.push({ name: 'lecture-assignment-detail', params: { assignmentID: assignment.id } })
    },
    async getLectureAssignmentList () {
      const res = await this.$store.dispatch('getLectureAssignmentList')
      this.assignments = res.data.data.results
      console.log(this.assignments)
    },
    assignmentStatus (value) {
      return {
        name: ASSIGNMENT_STATUS_REVERSE[value].name,
        color: ASSIGNMENT_STATUS_REVERSE[value].color
      }
    },
    assignmentSubmissionStatus (value) {
      return {
        name: ASSIGNMENT_SUBMISSION_STATUS_REVERSE[value].name,
        color: ASSIGNMENT_SUBMISSION_STATUS_REVERSE[value].color
      }
    },
    submissionStatus (accept, total) {
      var _accept = accept * 1
      var _total = total * 1
      if (_accept === 0) { // 빨강
        return '1'
      } else if (_accept === _total) { // 연두
        return '0'
      } else { // 주황
        return '-1'
      }
    }
  },
  computed: {
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .title{
    color: #7C7A7B;
  }
  .top-bar {
    margin-top: 40px;
    margin-left: 68px;
  }
  .lecture-assignment-card{
    margin: 0 auto;
    width: 70%;
    font-family: Manrope_bold;
    .table{
      width: 95% !important;
      margin: 0 auto;
    }
  }
  div{
    &.pagination{
    margin-right: 5%;
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
    }
  }
</style>
