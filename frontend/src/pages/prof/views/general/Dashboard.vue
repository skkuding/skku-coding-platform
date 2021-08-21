<template>
  <b-row
    type="flex"
    cols = "2"
    id="dashboard"
  >
    <b-col
      :md="5"
      :lg="4"
      id="first-col"
    >
      <img id="coding-platform-logo" src="@/assets/logos/codingPlatformLogo.png" alt="coding-platform-logo">
      <b-card class="admin-info drop-shadow-custom" :title="'Welcome, Prof. ' + user.username">
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
          message="Assignments Submissions Today"
          class="info-item drop-shadow-custom"
          :value="infoData.today_submission_count"
        />
        <info-card
          color="#28A5FF"
          message="Underway Assignments"
          class="info-item drop-shadow-custom"
          :value="infoData.recent_contest_count"
        />
      </div>
      <b-card title="My Lecture - 2021 Summer" class="admin-info drop-shadow-custom">
        <b-list-group>
          <b-list-group-item
            v-for="(lecture,index) in lectureList"
            :to="'lecture/'+ lecture.id +'/dashboard'"
            :key="index">{{ lecture.title + '_' + lecture.course_code + '-' + lecture.class_number }}
          </b-list-group-item>
        </b-list-group>
        <b-button variant="primary" class="float-right" v-b-modal.registerNew>
          + New Lecture
        </b-button>
      </b-card>
    </b-col>
    <register-new-lecture-modal @newLectureCreated="updateLectureList"></register-new-lecture-modal>
    <b-col
      :md="7"
      :lg="8"
    >
      <b-card class="admin-info drop-shadow-custom" title="Underway Assignments">
        <b-table
          borderless
          hover
          :fields="assignmentListFields"
          :items="assignmentList"
          :per-page="pageSize"
          :current-page="updateCurrentPage"
        >
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
import InfoCard from '@prof/components/infoCard.vue'
import api from '../../api.js'
import RegisterNewLectureModal from './RegisterNewLecture.vue'

export default {
  name: 'Dashboard',
  components: {
    InfoCard,
    RegisterNewLectureModal
  },
  data () {
    return {
      pageSize: 10,
      currentPage: 1,
      infoData: {
        user_count: 0,
        recent_contest_count: 0,
        today_submission_count: 0,
        judge_server_count: 0,
        env: {}
      },
      lectureList: [
      ],
      assignmentListFields: [
        {
          key: 'title',
          label: ''
        },
        {
          key: 'course.title',
          label: ''
        }
      ],
      assignmentList: [
      ],
      session: {}
    }
  },
  async mounted () {
    try {
      const resp = await api.getDashboardInfo()
      this.infoData = resp.data.data
    } catch (err) {
    }

    try {
      const resp = await api.getSessions()
      this.parseSession(resp.data.data)
    } catch (err) {
    }

    try {
      const res = await api.getCourseList()
      this.lectureList = res.data.data.results
    } catch (err) {
      console.log(err)
    }
    // try {
    //   const res = await api.getAssignmentList()
    //   this.assignmentList = res.data.data.results
    // } catch (err) {
    //   console.log(err)
    // }
  },
  methods: {
    async currentChange (page) {
      this.currentPage = page
      await this.getAssignmentList(page)
    },
    async getAssignmentList (page) {
      this.loading = true
      try {
        const res = await api.getAssignmentList(false, (page - 1) * this.pageSize, this.pageSize)
        this.total = res.data.data.total
        this.assignmentList = res.data.data.results
      } catch (err) {
        console.log(err)
      } finally {
        this.loading = false
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
      flex: 1 0 auto;
      min-width: 200px;
      margin-bottom: 10px;
    }
  }
  .drop-shadow-custom {
    filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  }
</style>
