<template>
  <div>
    <Sidemenu/>
    <article class="lecture-assignment-card">
      <div class="top-bar mb-4">
        <h2 class="title">Lecture Assignments</h2>
      </div>
      <div
        v-if="!assignments.length"
        class="no-assignment"
      >
        <p>No Lecture Assignment</p>
      </div>
      <div
        class="table"
        v-else
      >
        <b-table
          hover
          :items="assignments"
          :fields="assignmentListFields"
          :per-page="perPage"
          :current-page="currentPage"
          head-variant="light"
          class="table"
          @row-clicked="goAssignment"
          style = "cursor: pointer;"
        >
          <template #cell(status)="data">
            <b-icon
              icon="circle-fill"
              scale="0.7"
              :style="'color:' + assignmentStatus(data.value).color"
            >
            </b-icon>
            {{ assignmentStatus(data.value).name }}
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
          :total-rows="this.assignments.length"
          :per-page="perPage"
          limit='3'
        ></b-pagination>
      </div>
    </article>
  </div>
</template>

<script>
import Sidemenu from '@oj/components/Sidemenu.vue'
import { ASSIGNMENT_STATUS_REVERSE, ASSIGNMENT_STATUS, ASSIGNMENT_SUBMISSION_STATUS, ASSIGNMENT_SUBMISSION_STATUS_REVERSE } from '@/utils/constants'
import api from '@oj/api'
import moment from 'moment'

export default {
  name: 'LectureAssignmentList',
  components: {
    Sidemenu
  },
  data () {
    return {
      perPage: 10,
      currentPage: 1,
      total: 0,
      courseID: '',
      assignmentListFields: [
        {
          key: 'title',
          label: 'Assignment'
        },
        'status',
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
      submission: '',
      ASSIGNMENT_STATUS: ASSIGNMENT_STATUS,
      ASSIGNMENT_STATUS_REVERSE: ASSIGNMENT_STATUS_REVERSE,
      ASSIGNMENT_SUBMISSION_STATUS: ASSIGNMENT_SUBMISSION_STATUS,
      ASSIGNMENT_SUBMISSION_STATUS_REVERSE: ASSIGNMENT_SUBMISSION_STATUS_REVERSE
    }
  },
  async mounted () {
    this.courseID = this.$route.params.courseID
    this.route_name = this.$route.name
    try {
      await this.getLectureAssignmentList(1)
    } catch (err) {
    }
  },
  methods: {
    async goAssignment (assignment) {
      this.assignment = assignment
      this.listVisible = false
      await this.$router.push({
        name: 'lecture-assignment-detail',
        params: { assignmentID: assignment.id }
      })
    },
    async getLectureAssignmentList (page) {
      try {
        const res = await api.getLectureAssignmentList(this.courseID, (page - 1) * this.perPage, 250)
        const assignments = res.data.data.results
        this.total = res.data.data.total
        const underwayAssignment = assignments.filter(assignment => assignment.status === '0')
        const notUnderwayAssignment = assignments.filter(assignment => assignment.status !== '0')
        this.assignments = underwayAssignment.concat(notUnderwayAssignment)
      } catch (err) {
      }
    },
    async currentChange (page) {
      this.courseID = this.$route.params.courseID
      this.currentPage = page
      await this.getLectureAssignmentList(page)
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
      if (_accept === 0) {
        return '1'
      } else if (_accept === _total) {
        return '0'
      } else {
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
  .no-assignment {
    text-align: center;
    font-size: 16px;
    margin: 10px 0;
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
