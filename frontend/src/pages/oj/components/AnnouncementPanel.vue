<template>
  <div class="panel">
    <b-card
      header-tag="header"
      header-bg-variant="white"
      header-border-variant="white"
      style="max-width: 60rem; border-radius: 12px"
    >
      <template #header>
        <div class="panel-title">
          <div class="post-title">
            <b-icon icon="exclamation-circle"></b-icon>
            <p class="mb-0" style="margin-left: 0.5rem">Announcement</p>
          </div>
          <b-icon icon="list" @click='goAnnouncement()'></b-icon>
        </div>
      </template>
      <!-- 클릭 시 CSS 수정 -->
      <b-card-body>
          <b-table
            striped: False
            hover:False
            :items="announcements"
            :fields="announcementListColumns"
            :per-page="perPage"
            :current-page="currentPage"
            thead-tr-class="d-none"
            borderless
            @row-clicked="goAnnouncement"
          >
          <template #cell(icon)>
              <b-icon icon="chevron-right"></b-icon>
          </template>
          <template #cell(create_time)>
              {{ getTimeFormat(value, 'MMM D, YYYY') }}
          </template>
          </b-table>
      </b-card-body>
    </b-card>
  </div>
</template>

<script>
import api from '@oj/api'
import time from '@/utils/time'
export default {
  name: 'Announcement Panel',
  data () {
    return {
      limit: 3,
      total: 3,
      btnLoading: false,
      announcements: [],
      announcementListColumns: [
        {
          key: 'icon',
          tdClass: 'icon-field',
          thClass: 'icon-field',
          thStyle: 'width: 2rem;'
        },
        {
          key: 'title',
          label: this.$i18n.t('m.Title'),
          tdClass: 'title-field',
          thClass: 'title-field',
          thStyle: 'width: 28rem;'
        },
        {
          label: 'Date',
          key: 'create_time',
          tdClass: 'date-field',
          thClass: 'date-field',
          thStyle: 'width: 4rem;'
        }
      ]
    }
  },
  computed: {
    rows () {
      return this.items.length
    }
  },
  mounted () {
    this.init()
  },
  methods: {
    init () {
      this.getAnnouncementList()
    },
    getAnnouncementList (page = 1) {
      this.btnLoading = true
      api.getAnnouncementList((page - 1) * this.limit, this.limit).then(
        (res) => {
          this.btnLoading = false
          this.announcements = res.data.data.results
          this.total = res.data.data.total
        },
        () => {
          this.btnLoading = false
        }
      )
    },
    goAnnouncement (announcementID) {
      if (announcementID) {
        this.$router.push({ name: 'announcement-details', params: { announcementID: announcementID } })
      } else {
        this.$router.push({ name: 'announcement-list' })
      }
    },
    getTimeFormat (value, format) {
      return time.utcToLocal(value, format)
    }
  }
}
</script>

<style scoped>
.panel {
  padding: 20px 10px;
}
.card-header {
  width: 40rem;
  height: 3rem;
  padding: 0.5rem;
  border-radius: 12px;
}
.card-body {
  padding: 0.5rem;
  height: 12rem;
  border-radius: 12px;
  font-size: 1rem;
}
.panel-title {
  display: flex;
  text-align: center;
  justify-content: space-between;
  flex-direction: row;
  font-size: 1.5rem;
}
.post-title {
  display: flex;
  justify-content: space-between;
  flex-direction: row;
}
/deep/ .table .date-field {
  text-align: right;
}
</style>
