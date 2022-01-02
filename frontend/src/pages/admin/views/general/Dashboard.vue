<template>
  <b-row
    type="flex"
    cols = "2"
  >
    <b-col
      :md="5"
      :lg="4"
    >
      <b-card class="admin-info">
        <b-row cols ="3">
          <b-col cols = "4">
            <img
              class = "avatar"
              :src = "profile.avatar"
              >
          </b-col>
          <b-col cols = "8">
            <p class="admin-info-name">
              {{ user.username }}
            </p>
            <p>{{ user.admin_type }}</p>
          </b-col>
        </b-row>
        <hr>
        <div class="last-info">
          <p class="last-info-title" >
            {{ "Last Login" }}
          </p>
          <b-form class="last-info-body">
            <b-form-group label-cols="3"
            label= "Time:">
              <span>{{ session.last_activity | localtime }}</span>
            </b-form-group>
            <b-form-group label-cols="3"
            label = "IP:">
              <label class=“mr-sm-2”></label>
              <span>{{ ip }}</span>
            </b-form-group>
            <b-form-group label-cols="3"
            label = "OS">
              <span>{{ os }}</span>
            </b-form-group>
            <b-form-group label-cols="4"
            label = "Browser:" >
              <span>{{ browser }}</span>
            </b-form-group>
          </b-form>
        </div>
      </b-card>
      <panel
        v-if="isSuperAdmin"
        title="System Overview"
      >
        <p>{{ "Judge Server" }}  :  {{ infoData.judge_server_count }}</p>
        <p>
            HTTPS Status:
          <b-badge
            :variant="https ? 'success' : 'danger'"
            size="small"
          >
            {{ https ? 'Enabled' : 'Disabled' }}
          </b-badge>
        </p>
      </panel>
    </b-col>

    <b-col
      v-if="isSuperAdmin"
      :md="7"
      :lg="8"
    >
      <div class="info-container">
        <info-card
          color="#909399"
          icon="people-fill"
          message="Total Users"
          icon-size="30px"
          class="info-item"
          :value="infoData.user_count"
        />
        <info-card
          color="#67C23A"
          icon="list"
          message="Today Submissions"
          class="info-item"
          :value="infoData.today_submission_count"
        />
        <info-card
          color="#409EFF"
          icon="trophy"
          message="Recent Contests"
          class="info-item"
          :value="infoData.recent_contest_count"
        />
      </div>
      <panel style="margin-top: 5px">
        <span
          slot="title"
          v-loading="loadingReleases"
        >Release Notes
        <b-icon size = "sm" id = "rel" icon="question-circle-fill"> </b-icon>
          <b-popover target="rel" triggers="hover focus">
          <p>
            Please upgrade to the latest version to enjoy the new features.
          </p>
          <p> Reference: <a href="http://docs.onlinejudge.me/#/onlinejudge/guide/upgrade"
                          target="_blank">
            http://docs.onlinejudge.me/#/onlinejudge/guide/upgrade</a> </p>
        </b-popover>
        </span>
        <div class="accordion" role="tablist">
          <b-collapse
            v-for="(release, index) of releases"
            :key="'release' + index"
            v-model="activeNames">
                <b-link v-b-toggle="'accordion-' + index">
                  <b-card border-variant="light" :name="index+1" class="p-1" :id="index+1">
                  <div style="color:black" v-if="release.new_version">
                    {{ release.title }}
                    <b-badge
                      size="mini"
                      variant="success"
                    >
                      New Version
                    </b-badge>
                  </div>
                  <span v-else style="color:black">{{ release.title }}</span>
                  </b-card>
                </b-link>
              <b-collapse :name="index+1" :id="'accordion-' + index" role="tabpanel">
                <b-card-body>
                  <p>Level: {{ release.level }}</p>
                  <p>Details: </p>
                  <div class="release-body">
                    <ul
                      v-for="detail in release.details"
                      :key="detail"
                    >
                      <li v-dompurify-html="detail" />
                    </ul>
                  </div>
                </b-card-body>
              </b-collapse>
          </b-collapse>
        </div>
      </panel>
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters } from 'vuex'
import browserDetector from 'browser-detect'
import InfoCard from '@admin/components/infoCard.vue'
import api from '@admin/api'

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
      activeNames: [1],
      session: {},
      loadingReleases: true,
      releases: [],
      ip: ''
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
      const resp = await api.getIPAddress()
      this.ip = resp.data.data.ip
    } catch (err) {
    }

    try {
      const resp = await api.getReleaseNotes()
      this.loadingReleases = false
      const data = resp.data.data
      if (!data) {
        return
      }
      const currentVersion = data.local_version
      data.update.forEach(release => {
        if (release.version > currentVersion) {
          release.new_version = true
        }
      })
      this.releases = data.update
    } catch (err) {
      this.loadingReleases = false
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
    https () {
      return document.URL.slice(0, 5) === 'https'
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
  .admin-info {
    margin-bottom: 20px;
    &-name {
      font-size: 24px;
      font-weight: 700;
      margin-bottom: 10px;
      color: #409EFF;
    }
    .avatar {
      max-width: 100%;
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
