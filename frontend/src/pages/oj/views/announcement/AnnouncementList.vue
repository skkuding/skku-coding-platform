<template>
    <div class="notice-list-card font-bold">
      <page-title text="Notice"/>
      <div class="table">
        <b-table
          hover
          :items="announcements"
          :fields="noticeListColumns"
          :per-page="perPage"
          :current-page="currentPage"
          head-variant="light"
          @row-clicked="goAnnouncement"
        >
          <template #cell(top_fixed)="row">
            <div v-if="row.item.top_fixed === true"><b-icon icon="tag-fill" scale="0.8"/></div>
            <div v-else>{{ calculateIdx(row) }}</div>
          </template>
          <template #cell(title)="row">
            <div v-if="row.item.top_fixed === true">{{ changeRowColor(row.item) }}</div>
            {{row.item.title}}
          </template>
        </b-table>
        <div
          v-if="!announcements.length"
          class="no-announcement"
        >
          <p>No Notice</p>
        </div>
      </div>
      <div class="pagination">
          <b-pagination
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
            limit="3"
          ></b-pagination>
      </div>
    </div>
</template>

<script>
import api from '@oj/api'
import time from '@/utils/time'
import PageTitle from '@oj/components/PageTitle.vue'

export default {
  name: 'Announcement',
  components: {
    PageTitle
  },
  data () {
    return {
      perPage: 10,
      currentPage: 1,
      total: 10,
      btnLoading: false,
      announcements: [],
      announcement: '',
      listVisible: true,
      topFixedCount: 0,
      noticeListColumns: [
        {
          key: 'top_fixed',
          label: ''
        },
        {
          key: 'title',
          label: 'Title',
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
    isContest () {
      return !!this.$route.params.contestID
    },
    rows () {
      return this.announcements.length
    }
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      if (this.isContest) {
        await this.getContestAnnouncementList()
      } else {
        await this.getAnnouncementList()
      }
    },
    async getAnnouncementList () {
      this.btnLoading = true
      try {
        const res = await api.getAnnouncementList(0, 250)
        this.btnLoading = false
        const announcements = res.data.data.results
        const topFixed = announcements.filter(announcement => (announcement.top_fixed === true))
        this.topFixedCount = topFixed.length
        const notTopFixed = announcements.filter(announcement => (announcement.top_fixed === false))
        this.announcements = [...topFixed, ...notTopFixed]
        this.total = res.data.data.total
      } catch (err) {
        this.btnLoading = false
      }
    },
    async getContestAnnouncementList () {
      this.btnLoading = true
      try {
        const res = await api.getContestAnnouncementList(this.$route.params.contestID)
        this.btnLoading = false
        this.announcements = res.data.data
      } catch (err) {
        this.btnLoading = false
      }
    },
    async goAnnouncement (announcement) {
      this.announcement = announcement
      this.listVisible = false
      await this.$router.push({ name: 'announcement-details', params: { announcementID: announcement.id } })
    },
    changeRowColor (announcement) {
      announcement._rowVariant = 'secondary'
    },
    calculateIdx (row) {
      return row.index - this.topFixedCount + 1
    }
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .notice-list-card{
    margin: 0 auto;
    width: 70%;
    font-family: Manrope;
  }
  .table{
    width: 95% !important;
    margin: 0 auto;
    td {
      cursor: pointer;
    }
  }
  .no-announcement {
    text-align: center;
    font-size: 16px;
    margin: 10px 0;
  }
  .pagination{
    margin-right: 5%;
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
  .notice-title-field{
    width: 75%;
  }
  .font-bold {
    font-family: manrope_bold;
  }
</style>
