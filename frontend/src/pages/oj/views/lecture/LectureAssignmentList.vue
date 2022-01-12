<template>
  <div>
    <sidemenu/>
    <article class="lecture-assignment-card">
      <div class="top-bar mb-4">
        <h2 class="title">Course Assignments</h2>
      </div>
      <div
        v-if="!assignments.length"
        class="no-assignment"
      >
        <p>No Course Assignment</p>
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
import sidemenu from '@oj/components/Sidemenu.vue'
import { ASSIGNMENT_STATUS_REVERSE, ASSIGNMENT_SUBMISSION_STATUS, ASSIGNMENT_SUBMISSION_STATUS_REVERSE } from '@/utils/constants'
import api from '@oj/api'
import moment from 'moment'

export default {
  name: 'CourseAssignmentList',
  components: {
    sidemenu
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
      ASSIGNMENT_STATUS_REVERSE: ASSIGNMENT_STATUS_REVERSE,
      ASSIGNMENT_SUBMISSION_STATUS: ASSIGNMENT_SUBMISSION_STATUS,
      ASSIGNMENT_SUBMISSION_STATUS_REVERSE: ASSIGNMENT_SUBMISSION_STATUS_REVERSE
    }
  },
  async mounted () {
    this.courseID = this.$route.params.courseID
    this.route_name = this.$route.name
    try {
      await this.getCourseAssignmentList(1)
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
    async getCourseAssignmentList (page) {
      try {
        const res = await api.getCourseAssignmentList(this.courseID, (page - 1) * this.perPage, 250)
        this.sortAssignmentList(res.data.data.results)
        this.total = res.data.data.total
      } catch (err) {
      }
    },
    async currentChange (page) {
      this.courseID = this.$route.params.courseID
      this.currentPage = page
      await this.getCourseAssignmentList(page)
    },
    assignmentStatus (value) {
      return {
        name: ASSIGNMENT_STATUS_REVERSE[value].name,
        color: ASSIGNMENT_STATUS_REVERSE[value].color
      }
    },
    sortAssignmentList (assignmentList) {
      assignmentList.sort(function (a, b) {
        const aDue = a.end_time
        const bDue = b.end_time
        const result = moment(aDue).isAfter(bDue)
        if (result === true) {
          return 1
        } else {
          return -1
        }
      })
      const underwayAssignment = assignmentList.filter(assignment => assignment.status === '0')
      const notUnderwayAssignment = assignmentList.filter(assignment => assignment.status !== '0')
      this.assignments = underwayAssignment.concat(notUnderwayAssignment)
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
