<template>
    <div class="notice-list-card">
      <h1 class="title">Notice</h1>
      <div class="table">
        <b-table
          hover
          :items="announcements"
          :fields="noticeListColumns"
          :per-page="perPage"
          :current-page="currentPage"
          head-variant="light"
        ></b-table>
      </div>
      <div class="pagination">
          <b-pagination
            aria-controls="notice-list"
            v-model="currentPage"
            :total-rows=100
            :per-page="perPage"
            limit="3"
          ></b-pagination>
      </div>
    </div>
</template>

<script>
import api from '@oj/api'
import time from '@/utils/time'
export default {
  name: 'Announcement',
  data () {
    return {
      limit: 10,
      total: 10,
      btnLoading: false,
      announcements: [],
      announcement: '',
      listVisible: true,
      noticeListColumns: [
        {
          key: 'title',
          label: this.$i18n.t('m.Title'),
          tdClass: 'notice-title-field',
          thClass: 'notice-title-field'
        },
        {
          label: 'Date',
          key: 'create_time',
          formatter: value => {
            return time.utcToLocal(value, 'YYYY-M-D')
          }
        }
      ]
    }
  },
  computed: {
    title () {
      if (this.listVisible) {
        return this.isContest ? this.$i18n.t('m.Contest_Announcements') : this.$i18n.t('m.Announcements')
      } else {
        return this.announcement.title
      }
    },
    isContest () {
      return !!this.$route.params.contestID
    },
    rows () {
      return this.items.length
    }
  },
  mounted () {
    this.init()
  },
  methods: {
    init () {
      if (this.isContest) {
        this.getContestAnnouncementList()
      } else {
        this.getAnnouncementList()
      }
    },
    getAnnouncementList (page = 1) {
      this.btnLoading = true
      api.getAnnouncementList((page - 1) * this.limit, this.limit).then(res => {
        this.btnLoading = false
        this.announcements = res.data.data.results
        this.total = res.data.data.total
      }, () => {
        this.btnLoading = false
      })
    },
    getContestAnnouncementList () {
      this.btnLoading = true
      api.getContestAnnouncementList(this.$route.params.contestID).then(res => {
        this.btnLoading = false
        this.announcements = res.data.data
      }, () => {
        this.btnLoading = false
      })
    },
    goAnnouncement (announcement) {
      this.announcement = announcement
      this.listVisible = false
    },
    goBack () {
      this.listVisible = true
      this.announcement = ''
    }
  }
}
</script>

<style>
  .notice-list-card{
    margin: 0 auto;
    width: 90%;
  }
  .title{
    margin-top: 100px;
  }
  .notice-list-card .table{
    width: 95%;
    margin: 0 auto;
  }
  .pagination{
    display: flex;
    justify-content: flex-end;
  }
  .notice-title-field{
    width: 75%;
  }
</style>
