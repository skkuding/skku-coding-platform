<template>
  <div class="notice-list-card font-bold">
    <page-title text="Notice" />
    <Table
      hover
      :items="announcements"
      :fields="announcementListField"
      :per-page="perPage"
      :current-page="currentPage"
      text="No Notice"
      @row-clicked="goAnnouncement"
    >
      <template v-slot:title="data">
        {{data.row.title}}
      </template>
      <template v-slot:create_time="data">
        {{ getTimeFormat(data.row.create_time) }}
      </template>
      <template v-slot:top_fixed="data">
        <icon v-if="data.row.top_fixed===true" icon='thumbtack'/>
      </template>
    </Table>
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
import Table from '@oj/components/Table.vue'

export default {
  name: 'Announcement',
  components: {
    PageTitle,
    Table
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
      announcementListField: [
        {
          key: 'top_fixed',
          label: ''
        },
        { key: 'title' },
        {
          key: 'create_time',
          label: 'Date'
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
        const topFixed = announcements.filter(
          (announcement) => announcement.top_fixed === true
        )
        this.topFixedCount = topFixed.length
        const notTopFixed = announcements.filter(
          (announcement) => announcement.top_fixed === false
        )
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
      await this.$router.push({
        name: 'announcement-details',
        params: { announcementID: announcement.id }
      })
    },
    changeRowColor (announcement) {
      announcement._rowVariant = 'secondary'
    },
    calculateIdx (row) {
      return row.index - this.topFixedCount + 1
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-M-D')
    }
  }
}
</script>

<style lang="scss" scoped>
@font-face {
  font-family: Manrope_bold;
  src: url("../../../../fonts/Manrope-Bold.ttf");
}
.notice-list-card {
  margin: 0 auto;
  width: 70%;
  font-family: Manrope;
}
.no-announcement {
  text-align: center;
  font-size: 16px;
  margin: 10px 0;
}
.pagination {
  margin-right: 5%;
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
.notice-title-field {
  width: 75%;
}
.font-bold {
  font-family: manrope_bold;
}
</style>
