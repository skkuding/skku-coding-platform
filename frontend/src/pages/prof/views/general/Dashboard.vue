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
      <b-card class="admin-info" :title="'Welcome, Prof. ' + user.username">
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
          class="info-item"
          :value="infoData.user_count"
        />
        <info-card
          color="#8DC63F"
          message="Assignments Submissions Today"
          class="info-item"
          :value="infoData.today_submission_count"
        />
        <info-card
          color="#28A5FF"
          message="Underway Assignments"
          class="info-item"
          :value="infoData.recent_contest_count"
        />
      </div>
      <b-card title="My Lecture - 2021 Summer">
        <b-list-group>
          <b-list-group-item
            v-for="(lecture,index) in lectureList"
            href="#"
            :key="index">{{ lecture.title + '_' + lecture.course_code + '-' + lecture.class_number }}
          </b-list-group-item>
        </b-list-group>
        <b-button variant="dark">
          ef
        </b-button>
      </b-card>
    </b-col>

    <b-col
      v-if="isSuperAdmin"
      :md="7"
      :lg="8"
    >
      <b-card class="admin-info" title="Recent Questions">
        <div class="table">
          <b-table
            hover
            :items="problemList"
            :fields="problemTableColumns"
            :per-page="perPage"
            :current-page="currentPage"
            head-variant="light"
            @row-clicked="goProblem"
          >
            <template #cell(title)="data">
              {{data.value}}
              <b-icon icon="check2-circle" style="color: #8DC63F;" font-scale="1.2" v-if="data.item.my_status===0"></b-icon>
            </template>
            <template #cell(difficulty)="data">
              <b-icon
                icon="circle-fill"
                class="mr-2"
                :style="'color:' + difficultyColor(data.value)"
              />
              {{ data.value }}
            </template>
            <template #cell(AC_Rate)="data">
              {{ getACRate(data.item.accepted_number, data.item.submission_number) }}
            </template>
            <template v-slot:cell(tags)="data">
              <span v-show="checked" v-for="item in data.item.tags" :key="item.id">{{ item }}  </span>
            </template>
            <template v-slot:head(tags)="field">
              <div v-show="checked">{{ field.label }}</div>
            </template>
          </b-table>
        </div>
        <div class="pagination">
          <b-pagination
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
            limit="3"
          ></b-pagination>
        </div>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters } from 'vuex'
import browserDetector from 'browser-detect'
import InfoCard from '@prof/components/infoCard.vue'
import api from '@prof/api'

export default {
  name: 'Dashboard',
  components: {
    InfoCard
  },
  data () {
    return {
      infoData: {
        user_count: 0,
        recent_contest_count: 0,
        today_submission_count: 0,
        judge_server_count: 0,
        env: {}
      },
      lectureList: [
        {
          id: 1,
          title: 'Programming Basics',
          course_code: 'GEDT018',
          class_number: 41,
          created_by: {
            id: 1,
            username: 'youngHoon',
            real_name: '김영훈'
          },
          registered_year: '2021',
          semester: 1
        },
        {
          id: 2,
          title: 'Programming Advanced',
          course_code: 'GEDT019',
          class_number: 41,
          created_by: {
            id: 1,
            username: 'youngHoon',
            real_name: '김영훈'
          },
          registered_year: '2021',
          semester: 1
        }
      ],
      lectureListTotal: 2,
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
  },
  methods: {
    parseSession (sessions) {
      let session = sessions[0]
      if (sessions.length > 1) {
        session = sessions.filter(s => !s.current_session).sort((a, b) => {
          return a.last_activity < b.last_activity
        })[0]
      }
      this.session = session
    }
  },
  computed: {
    ...mapGetters(['profile', 'user', 'isSuperAdmin']),
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
    }
  }
}
</script>

<style lang="scss">
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
    margin-bottom: 20px;
    &-name {
      font-size: 24px;
      font-weight: 700;
      margin-bottom: 10px;
      color: #409EFF;
    }
    .last-info {
      &-title {
        font-size: 16px;
      }
      &-body {
        .b-form {
          margin-bottom: 5px;
        }
      }
    }
  }
  .list-group-item {
    padding: 1rem 2rem;
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
</style>
