<template>
  <div>
    <sidemenu/>
    <article class="lecture-assignment-card">
      <page-title text="Course Assignments"/>
      <div
        v-if="!assignments.length"
        class="no-assignment"
      >
        <p>No Course Assignment</p>
      </div>
      <Table
        v-else
        hover
        :items="assignments"
        :fields="assignmentListFields"
        :per-page="perPage"
        :current-page="currentPage"
        @row-clicked="goAssignment"
      >
        <template v-slot:title="data">
          {{data.row.title}}
        </template>
        <template v-slot:status="data">
          <b-icon
            icon="circle-fill"
            scale="0.7"
            :style="'color:' + assignmentStatus(data.row.status).color"
          >
          </b-icon>
          {{ assignmentStatus(data.row.status).name }}
        </template>
        <template v-slot:end_time="data">
          {{ getTimeFormat(data.row.end_time) }}
        </template>
        <template v-slot:accepted_problem="data">
          <span v-if="data.row.accepted_problem === 0">Not Accepted</span>
          <span v-else>{{ data.row.accepted_problem + '/' + data.row.total_problem + ' Accepted'}}</span>
        </template>
      </Table>

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
import time from '@/utils/time'
import PageTitle from '@oj/components/PageTitle.vue'
import Table from '@oj/components/Table.vue'

export default {
  name: 'CourseAssignmentList',
  components: {
    sidemenu,
    PageTitle,
    Table
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
        { key: 'status' },
        {
          key: 'end_time',
          label: 'Due'
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
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-MM-DD HH:mm')
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
  .no-assignment {
    text-align: center;
    font-size: 16px;
    margin: 10px 0;
  }
  .lecture-assignment-card::v-deep{
    margin: 0 auto;
    width: 70%;
    font-family: Manrope_bold;
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
