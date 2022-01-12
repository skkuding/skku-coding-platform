<template>
  <div class="flex-grow-1 mx-2">
    <b-breadcrumb :items="pageLocations" class="mt-3"></b-breadcrumb>
    <b-row
      type="flex"
      cols = "1"
      id="dashboard"
    >
      <b-col>
        <user-list :lecture-title="title"></user-list>
      </b-col>
    </b-row>
    <b-row
      type="flex"
      cols = "1"
      id="dashboard"
    >
      <b-col
        id="first-col"
      >
        <b-card class="admin-info drop-shadow-custom" title="Assignments">
        <b-table
          borderless
          hover
          :fields="assignmentListFields"
          :items="assignmentList"
          :per-page="pageSize"
          :current-page="updateCurrentPage"
        >
          <template #cell(title)="data">
            <b-link :to="{ name: 'lecture-assignment-list', params: { lectureId: data.item.course.id, assignmentAnchor: data.item.id } }"> {{ data.value }}</b-link>
          </template>
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
            v-model="currentPage"
            :per-page="pageSize"
            :total-rows="total"
            style="position: absolute; right: 20px; top: 15px;"
          />
        </div>
      </b-card>
    </b-row>
  </div>
</template>

<script>

import api from '../../api.js'
import UserList from '../users/UserList.vue'
export default {
  name: 'LectureDashboard',
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
      currentPage: 1,
      lectureId: null,
      createdBy: {},
      title: '',
      courseCode: '',
      classNumber: null,
      registeredYear: null,
      semester: null,
      pageLocations: [
        {
          text: '',
          to: '/lecture/' + this.$route.params.lectureId + '/dashboard'
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
      ]
    }
  },
  async created () {
    this.getAssignmentList(1)
  },
  async mounted () {
    this.lectureId = this.$route.params.lectureId
    try {
      const res = await api.getCourseList(this.lectureId)
      this.createdBy = res.data.data.created_by
      this.title = res.data.data.title
      this.courseCode = res.data.data.course_code
      this.classNumber = res.data.data.class_number
      this.registeredYear = res.data.data.registered_year
      this.semester = res.data.data.semester
    } catch (err) {
      this.$error(err)
    }
    console.log(
      this.createdBy + this.title + this.courseCode +
      this.classNumber + this.registeredYear + this.semester
    )
    this.getAssignmentList(1)
    this.pageLocations[0].text = this.title + '_' + this.courseCode + '-' + this.classNumber
  },
  methods: {
    async currentChange (page) {
      this.currentPage = page
      await this.getAssignmentList(page)
    },
    async getAssignmentList (page) {
      this.loading = true
      try {
        const res = await api.getAssignmentList(this.lectureId, null, this.pageSize, (page - 1) * this.pageSize)
        this.total = res.data.data.total
        this.assignmentList = res.data.data.results
      } catch (err) {
        console.log(err)
      } finally {
        this.loading = false
      }
    },
    async updateLectureList () {
      try {
        const res = await api.getCourseList()
        this.lectureList = res.data.data.results
      } catch (err) {
        console.log(err)
      }
    }
  },
  computed: {
    updateCurrentPage () {
      return this.currentChange(this.currentPage)
    }
  }
}
</script>

<style lang="scss">
  .drop-shadow-custom {
    filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  }
</style>
