<template>
  <b-row
    type="flex"
    id="dashboard"
  >
    <b-col
      :sm="12"
      :xs="12"
      :md="5"
      :lg="4"
      :xl="4"
      id="first-col"
    >
      <b-card class="admin-info drop-shadow-custom" :title="'Welcome, Professor. ' + user.username">
        <b-card-text>
          Last login
          <ul style="margin:10px 0 0 25px">
            <li>Time: {{ session.last_activity | localtime }} </li>
            <li>IP: {{ session.ip | localtime }} </li>
            <li>OS: {{ os }} </li>
            <li>Browser: {{ browser }} </li>
          </ul>
        </b-card-text>
      </b-card>
      <div class="info-container">
        <info-card
          color="#E9A05A"
          message="Total Students"
          icon-size="30px"
          class="info-item drop-shadow-custom"
          :value="infoData.user_count"
        />
        <info-card
          color="#8DC63F"
          message="Submissions Today"
          class="info-item drop-shadow-custom"
          :value="infoData.today_submission_count"
        />
        <info-card
          color="#28A5FF"
          message="Underway Assignments"
          class="info-item drop-shadow-custom"
          :value="infoData.underway_assignments_count"
        />
      </div>
      <b-card title="My Course" class="admin-info drop-shadow-custom">
        {{ currentYear + ' ' + semester[currentSemester] }}
        <b-list-group>
          <b-list-group-item
            v-for="(course,index) in currentSemesterCourseList"
            :to="'course/'+ course.id +'/dashboard'"
            :key="index">{{ course.title + '_' + course.course_code + '-' + course.class_number }}
          </b-list-group-item>
        </b-list-group>
        <b-button variant="primary" class="float-right" v-b-modal.registerNew>
          + New Course
        </b-button>
      </b-card>
    </b-col>
    <course-modal @submitCourseData="updateCourseList" :mode="mode"/>
    <b-col
      :sm="12"
      :xs="12"
      :md="7"
      :lg="8"
      :xl="8"
    >
      <b-card class="admin-info drop-shadow-custom" title="Underway Assignments">
        <b-table
          borderless
          hover
          tbody-class="table-body"
          :fields="assignmentListFields"
          :items="assignmentList"
          :per-page="pageSize"
          :current-page="updateCurrentPage"
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
            v-model="currentPage"
            :per-page="pageSize"
            :total-rows="total"
            style="position: absolute; right: 20px; top: 15px;"
          />
        </div>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters } from 'vuex'
import browserDetector from 'browser-detect'
import InfoCard from '@professor/components/infoCard.vue'
import api from '../../api.js'
import CourseModal from './CourseModal.vue'

export default {
  name: 'Dashboard',
  components: {
    InfoCard,
    CourseModal
  },
  data () {
    return {
      ASSIGNMENT_STATUS_REVERSE: {
        1: 'Not Started',
        0: 'Underway',
        '-1': 'Ended'
      },
      pageSize: 10,
      currentPage: 1,
      infoData: {
        user_count: 0,
        today_submission_count: 0,
        underway_assignments_count: 0,
        env: {}
      },
      courseList: [],
      currentSemesterCourseList: [],
      assignmentListFields: [
        {
          key: 'title',
          label: 'Assignment title'
        },
        {
          key: 'course.title',
          label: 'Course'
        }
      ],
      assignmentList: [
      ],
      session: {},
      semester: ['Spring', 'Summer', 'Fall', 'Winter'],
      currentYear: '',
      currentSemester: '',
      mode: 'create'
    }
  },
  async mounted () {
    try {
      const res = await api.getSessions()
      this.parseSession(res.data.data)
    } catch (err) {
    }
    try {
      const res = await api.getBookmarkCourseList(null, 250, 0)
      res.data.data.results.map(course => {
        this.courseList.push(course.course)
      })
      if (res.data.data.total > 250) {
        this.$error('Since there are too much courses, failed to get all course list')
      }
    } catch (err) {
    }
    const res = await api.getDashboardInfo()
    this.infoData.user_count = res.data.data.student_count
    this.infoData.today_submission_count = res.data.data.today_submission_count
    this.infoData.underway_assignments_count = res.data.data.underway_assignments.total
    this.assignmentList = res.data.data.underway_assignments.results
    if (res.data.data.underway_assignments.results < res.data.data.underway_assignments.total) {
      this.$error('Since the amount of underway assignment exceeds system limit, failed to load all underway assignments.')
    }
    const now = new Date()
    this.currentYear = now.getFullYear()
    const nowMonth = now.getMonth() + 1
    if (nowMonth >= 2 && nowMonth <= 5) {
      this.currentSemester = 0
    } else if (nowMonth >= 6 && nowMonth <= 8) {
      this.currentSemester = 1
    } else if (nowMonth >= 8 && nowMonth <= 12) {
      this.currentSemester = 2
    } else {
      this.currentSemester = 3
    }
    this.currentSemesterCourseList = this.courseList.filter((course) => {
      return course.semester === this.currentSemester && course.registered_year === this.currentYear
    })
  },
  methods: {
    async currentChange (page) {
      this.currentPage = page
      await this.getAssignmentList(page)
    },
    async getAssignmentList (page) {
      try {
        const res = await api.getDashboardInfo(this.pageSize, (page - 1) * this.pageSize)
        this.total = res.data.data.underway_assignments.total
        this.assignmentList = res.data.data.underway_assignments.results
      } catch (err) {
      }
    },
    parseSession (sessions) {
      let session = sessions[0]
      if (sessions.length > 1) {
        session = sessions.filter(s => !s.current_session).sort((a, b) => {
          return a.last_activity < b.last_activity
        })[0]
      }
      this.session = session
    },
    async updateCourseList () {
      try {
        const res = await api.getBookmarkCourseList()
        res.data.data.results.map(course => {
          this.courseList.push(course.course)
        })
        this.$parent.updateSidebar += 1
      } catch (err) {
      }
    },
    async goAssignment (item) {
      await this.$router.push({ name: 'course-assignment-list', params: { courseId: item.course.id, assignmentAnchor: item.id } })
    }
  },
  computed: {
    ...mapGetters(['profile', 'user']),
    cdn () {
      return this.infoData.env.STATIC_CDN_HOST
    },
    https () {
      return document.URL.slice(0, 5) === 'https'
    },
    forceHttps () {
      return this.infoData.env.FORCE_HTTPS
    },
    browser () {
      const b = browserDetector(this.session.user_agent)
      if (b.name && b.version) {
        return b.name + ' ' + b.version
      } else {
        return 'Unknown'
      }
    },
    os () {
      const b = browserDetector(this.session.user_agent)
      return b.os ? b.os : 'Unknown'
    },
    updateCurrentPage () {
      return this.currentChange(this.currentPage)
    }
  }
}
</script>

<style lang="scss" scoped>
  #dashboard {
    margin: auto;
    flex:1 0;
    max-width: 1300px;
  }
  #first-col {
    background: rgba(153, 169, 172, 0.26);
    height: 100%;
    min-height: 100vh;
    #coding-platform-logo {
      display: block;
      margin:auto;
    }
  }
  .admin-info {
    margin-top: 20px;
    margin-bottom: 20px;
  }
  .list-group-item {
    padding: 1rem 0rem;
    border: 0 solid
  }

  .list-group-item-action:focus, .list-group-item-action:hover {
    background-color: #40a0ff38;
  }

  .info-container {
    display: flex;
    justify-content: flex-start;
    flex-wrap: wrap;
    .info-item {
      flex: 1 1 auto;
      min-width: 200px;
      margin-bottom: 10px;
    }
  }
  .drop-shadow-custom {
    filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  }
  .table-body {
    cursor: pointer;
  }
</style>
