<template>
  <el-row
    type="flex"
    :gutter="20"
  >
    <el-col
      :md="10"
      :lg="8"
    >
      <el-card class="admin-info">
        <el-row :gutter="20">
          <el-col :span="10">
            <img
              class="avatar"
              :src="profile.avatar"
            >
          </el-col>
          <el-col :span="14">
            <p class="admin-info-name">
              {{ user.username }}
            </p>
            <p>{{ user.admin_type }}</p>
          </el-col>
        </el-row>
        <hr>
        <div class="last-info">
          <p class="last-info-title">
            {{ $t('m.Last_Login') }}
          </p>
          <el-form
            label-width="80px"
            class="last-info-body"
          >
            <el-form-item label="Time:">
              <span>{{ session.last_activity | localtime }}</span>
            </el-form-item>
            <el-form-item label="IP:">
              <span>{{ session.ip }}</span>
            </el-form-item>
            <el-form-item label="OS">
              <span>{{ os }}</span>
            </el-form-item>
            <el-form-item label="Browser:">
              <span>{{ browser }}</span>
            </el-form-item>
          </el-form>
        </div>
      </el-card>
      <panel
        v-if="isSuperAdmin"
        :title="$t('m.System_Overview')"
      >
        <p>{{ $t('m.DashBoardJudge_Server') }}:  {{ infoData.judge_server_count }}</p>
        <p>
          {{ $t('m.HTTPS_Status') }}:
          <el-tag
            :type="https ? 'success' : 'danger'"
            size="small"
          >
            {{ https ? 'Enabled' : 'Disabled' }}
          </el-tag>
        </p>
        <p>
          {{ $t('m.Force_HTTPS') }}:
          <el-tag
            :type="forceHttps ? 'success' : 'danger'"
            size="small"
          >
            {{ forceHttps ? 'Enabled' : 'Disabled' }}
          </el-tag>
        </p>
        <p>
          {{ $t('m.CDN_HOST') }}:
          <el-tag
            :type="cdn ? 'success' : 'warning'"
            size="small"
          >
            {{ cdn ? cdn : 'Not Use' }}
          </el-tag>
        </p>
      </panel>
    </el-col>

    <el-col
      v-if="isSuperAdmin"
      :md="14"
      :lg="16"
    >
      <div class="info-container">
        <info-card
          color="#909399"
          icon="el-icon-fa-users"
          message="Total Users"
          icon-size="30px"
          class="info-item"
          :value="infoData.user_count"
        />
        <info-card
          color="#67C23A"
          icon="el-icon-fa-list"
          message="Today Submissions"
          class="info-item"
          :value="infoData.today_submission_count"
        />
        <info-card
          color="#409EFF"
          icon="el-icon-fa-trophy"
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
          <el-popover
            placement="right"
            trigger="hover"
          >
            <i
              slot="reference"
              class="el-icon-fa-question-circle import-user-icon"
            />
            <p>Please upgrade to the latest version to enjoy the new features. </p>
            <p>Reference: <a
              href="http://docs.onlinejudge.me/#/onlinejudge/guide/upgrade"
              target="_blank"
            >
              http://docs.onlinejudge.me/#/onlinejudge/guide/upgrade</a>
            </p>
          </el-popover>
        </span>

        <el-collapse
          v-for="(release, index) of releases"
          :key="'release' + index"
          v-model="activeNames"
        >
          <el-collapse-item :name="index+1">
            <template slot="title">
              <div v-if="release.new_version">
                {{ release.title }}
                <el-tag
                  size="mini"
                  type="success"
                >
                  New Version
                </el-tag>
              </div>
              <span v-else>{{ release.title }}</span>
            </template>
            <p>Level: {{ release.level }}</p>
            <p>Details: </p>
            <div class="release-body">
              <ul
                v-for="detail in release.details"
                :key="detail"
              >
                <li v-html="detail" />
              </ul>
            </div>
          </el-collapse-item>
        </el-collapse>
      </panel>
    </el-col>
  </el-row>
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
      releases: []
    }
  },
  async mounted () {
    await api.getDashboardInfo().then(resp => {
      this.infoData = resp.data.data
    }, () => {
    })
    await api.getSessions().then(resp => {
      this.parseSession(resp.data.data)
    }, () => {
    })
    await api.getReleaseNotes().then(resp => {
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
    }, () => {
      this.loadingReleases = false
    })
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

<style lang="less">
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
        .el-form-item {
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
