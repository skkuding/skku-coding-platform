<template>
  <div class="flex-grow-1 mx-2" style="max-width: 1300px;">
    <b-breadcrumb :items="pageLocations" class="mt-3"></b-breadcrumb>
    <b-row
      type="flex"
      cols = "1"
      class="course-dashboard"
    >
      <b-col>
        <user-list :course-title="title"></user-list>
      </b-col>
    </b-row>
    <b-row
      type="flex"
      cols = "1"
      class="course-dashboard"
    >
      <b-col>
        <b-card style="margin-bottom: 20px;" class="drop-shadow-custom" title="Assignments">
          <b-table
            borderless
            hover
            tbody-class="table-body"
            :fields="assignmentListFields"
            :items="assignmentList"
            :per-page="pageSize"
            :current-page="updateAssignmentCurrentPage"
            @row-clicked="goAssignment"
          >
            <template #cell(status)="data">
              <b-button
                size="sm"
                :variant="
                  data.item.status === '-1'
                    ? 'outline-danger'
                    : data.item.status === '0'
                    ? 'outline-success'
                    : 'outline-primary'
                "
                disabled
              >
                {{ ASSIGNMENT_STATUS_REVERSE[data.item.status] }}
              </b-button>
            </template>
          </b-table>
          <div class="panel-options">
            <b-pagination
              v-model="assignmentCurrentPage"
              :per-page="pageSize"
              :total-rows="assignmentTotal"
              style="position: absolute; right: 20px; top: 15px;"
            />
          </div>
        </b-card>
      </b-col>
    </b-row>
    <b-row
      type="flex"
      cols = "1"
      class="course-dashboard"
    >
      <b-col>
        <b-card style="margin-bottom: 20px;" class="drop-shadow-custom" title="Problems">
          <b-table
            borderless
            hover
            tbody-class="table-body"
            :fields="problemListField"
            :items="problemList"
            :per-page="pageSize"
            :current-page="updateProblemCurrentPage"
          >
            <template #cell(assignment_name)="data">
              <div v-if="data.value"> {{ data.value }} </div>
              <div v-else> - </div>
            </template>
          </b-table>
          <div class="panel-options">
            <b-pagination
              v-model="problemCurrentPage"
              :per-page="pageSize"
              :total-rows="problemTotal"
              style="position: absolute; right: 20px; top: 15px;"
            />
          </div>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>

import api from '../../api.js'
import UserList from '../users/UserList.vue'
import moment from 'moment'

export default {
  name: 'CourseDashboard',
  components: {
    UserList
  },
  data () {
    return {
      newAssignmentCourseId: null,
      ASSIGNMENT_STATUS_REVERSE: {
        1: 'Not Started',
        0: 'Underway',
        '-1': 'Ended'
      },
      pageSize: 5,
      mode: '',
      assignmentCurrentPage: 1,
      problemCurrentPage: 1,
      assignmentTotal: 0,
      problemTotal: 0,
      courseId: null,
      createdBy: {},
      title: '',
      courseCode: '',
      classNumber: null,
      registeredYear: null,
      semester: null,
      pageLocations: [
        {
          text: '',
          to: '/course/' + this.$route.params.courseId + '/dashboard'
        },
        {
          text: 'Dashboard'
        }
      ],
      assignmentListFields: [
        {
          key: 'title',
          label: ''
        },
        {
          key: 'course.title',
          label: ''
        },
        {
          key: 'status',
          label: ''
        }
      ],
      assignmentList: [
      ],
      problemListField: [
        'title',
        {
          key: 'assignment_name',
          label: 'Assignment'
        },
        {
          key: 'create_time',
          label: 'Create Time',
          formatter: (value) => {
            return moment(value).format('YYYY-M-D HH:mm')
          }
        }
      ],
      problemList: []
    }
  },
  async mounted () {
    this.courseId = this.$route.params.courseId
    try {
      const res = await api.getCourseList(this.courseId)
      this.createdBy = res.data.data.created_by
      this.title = res.data.data.title
      this.courseCode = res.data.data.course_code
      this.classNumber = res.data.data.class_number
      this.registeredYear = res.data.data.registered_year
      this.semester = res.data.data.semester
    } catch (err) {
      this.$error(err)
    }
    await this.getCourseProblem(1)
    await this.getAssignmentList(1)
    this.pageLocations[0].text = this.title + '_' + this.courseCode + '-' + this.classNumber
  },
  methods: {
    async currentAssignmentChange (page) {
      this.assignmentCurrentPage = page
      await this.getAssignmentList(page)
    },
    async currentProblemChange (page) {
      this.problemCurrentPage = page
      await this.getCourseProblem(page)
    },
    async getAssignmentList (page) {
      this.loading = true
      try {
        const res = await api.getAssignmentList(this.courseId, null, this.pageSize, (page - 1) * this.pageSize)
        this.assignmentTotal = res.data.data.total
        this.assignmentList = res.data.data.results
      } catch (err) {
      } finally {
        this.loading = false
      }
    },
    async getCourseProblem (page) {
      this.loading = true
      try {
        const res = await api.getCourseProblem(this.$route.params.courseId, null, this.pageSize, (page - 1) * this.pageSize)
        this.problemList = res.data.data.results
        this.problemTotal = res.data.data.total
      } catch (err) {
      } finally {
        this.loading = false
      }
    },
    async updateCourseList () {
      try {
        const res = await api.getCourseList()
        this.courseList = res.data.data.results
      } catch (err) {
      }
    },
    async goAssignment (item) {
      await this.$router.push({ name: 'course-assignment-list', params: { courseId: item.course.id, assignmentAnchor: item.id } })
    }
  },
  computed: {
    updateAssignmentCurrentPage () {
      return this.currentAssignmentChange(this.assignmentCurrentPage)
    },
    updateProblemCurrentPage () {
      return this.currentProblemChange(this.problemCurrentPage)
    }
  }
}
</script>

<style lang="scss">
  .drop-shadow-custom {
    filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  }
  .course-dashboard {
    margin: auto;
    flex:1 0;
    max-width: 1300px;
  }
  .table-body {
    cursor: pointer;
  }
</style>
