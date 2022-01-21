<template>
  <div class="view">
    <Panel title="Contest List">
      <div slot="header">
        <b-form-input
          v-model="keyword"
          placeholder="Keywords"
        />
      </div>
      <b-table
        ref="table"
        :items="contestList"
        :fields="contestListFields"
        :per-page="pageSize"
        :current-page="updateCurrentPage"
        style="width: 100%"
      >
        <template #cell(expand)="row">
          <b-icon
            :icon="row.detailsShowing ? 'chevron-down' : 'chevron-right'"
            style="cursor: pointer"
            @click="row.toggleDetails"
            class
          />
        </template>

        <template #cell(rule_type)="row">
          <b-button
            size="sm"
            variant="outline-primary"
            disabled
          >
            {{ row.item.rule_type }}
          </b-button>
        </template>

        <template #cell(contest_type)="row">
          <b-button
            size="sm"
            :variant="row.item.contest_type === 'Public' ? 'outline-success' : 'outline-primary'"
            disabled
          >
            {{ row.item.contest_type }}
          </b-button>
        </template>

        <template #cell(status)="row">
          <b-button
            size="sm"
            :variant="
              row.item.status === '-1'
                ? 'outline-danger'
                : row.item.status === '0'
                ? 'outline-success'
                : 'outline-primary'
            "
            disabled
          >
            {{ row.item.status | contestStatus }}
          </b-button>
        </template>

        <template #cell(visible)="row">
          <b-form-checkbox
            switch
            v-model="row.item.visible"
            @change="handleVisibleSwitch(row.item)"
          >
          </b-form-checkbox>
        </template>

        <template #cell(operation)="row">
          <div>
            <icon-btn
              name="Edit"
              icon="clipboard-plus"
              @click.native="goEdit(row.item.id)"
            />
            <icon-btn
              name="Problem"
              icon="list"
              @click.native="goContestProblemList(row.item.id)"
            />
            <icon-btn
              name="Announcement"
              icon="info-circle"
              @click.native="goContestAnnouncement(row.item.id)"
            />
            <icon-btn
              name="Download Accepted Submissions"
              icon="download"
              @click.native="openDownloadOptions(row.item.id)"
            />
            <icon-btn
              name="Delete Contest"
              icon="trash"
              @click.native="deleteContest(row.item.id)"
            />
          </div>
        </template>

        <template #row-details="row">
          <b-card>
            <p>Start Time: {{ row.item.start_time | localtime }}</p>
            <p>End Time: {{ row.item.end_time | localtime }}</p>
            <p>Create Time: {{ row.item.create_time | localtime }}</p>
            <p>Creator: {{ row.item.created_by.username }}</p>
          </b-card>
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
    </Panel>

    <b-modal
      title="Download Contest Submissions"
      v-model="downloadDialogVisible"
      centered
    >
      <b-form-checkbox
        switch
        v-model="excludeAdmin"
      >
        Exclude admin submissions
      </b-form-checkbox>
      <template #modal-footer>
        <b-button
          variant="primary"
          @click="downloadSubmissions"
        >
          Download
        </b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import api from '../../api.js'
import utils from '@/utils/utils'
import { CONTEST_STATUS_REVERSE } from '@/utils/constants'

export default {
  name: 'ContestList',
  filters: {
    contestStatus (value) {
      return CONTEST_STATUS_REVERSE[value].name
    }
  },
  data () {
    return {
      pageSize: 10,
      total: 0,
      contestList: [],
      contestListFields: [
        { key: 'expand', label: '' },
        { key: 'id', label: 'ID' },
        { key: 'title', label: 'Title', tdClass: 'contestTitle' },
        { key: 'rule_type', label: 'Rule Type' },
        { key: 'contest_type', label: 'Contest Type' },
        { key: 'status', label: 'Status' },
        { key: 'visible', label: 'Visible' },
        { key: 'operation', label: 'Operation' }
      ],
      keyword: '',
      excludeAdmin: true,
      currentPage: 1,
      currentId: 1,
      downloadDialogVisible: false
    }
  },
  watch: {
    async keyword () {
      await this.currentChange(1)
    }
  },
  async mounted () {
    await this.getContestList(this.currentPage)
  },
  methods: {
    // 切换页码回调
    async currentChange (page) {
      this.currentPage = page
      await this.getContestList(page)
    },
    async getContestList (page) {
      this.loading = true
      try {
        const res = await api.getContestList((page - 1) * this.pageSize, this.pageSize, this.keyword)
        this.total = res.data.data.total
        this.contestList = res.data.data.results
      } catch (err) {
      } finally {
        this.loading = false
      }
    },
    openDownloadOptions (contestId) {
      this.downloadDialogVisible = true
      this.currentId = contestId
    },
    downloadSubmissions () {
      const excludeAdmin = this.excludeAdmin ? '1' : '0'
      const url = `/admin/download_submissions?contest_id=${this.currentId}&exclude_admin=${excludeAdmin}`
      utils.downloadFile(url)
    },
    async goEdit (contestId) {
      await this.$router.push({ name: 'edit-contest', params: { contestId } })
    },
    async goContestAnnouncement (contestId) {
      await this.$router.push({
        name: 'contest-announcement',
        params: { contestId }
      })
    },
    async deleteContest (contestId) {
      try {
        await this.$confirm('Sure to delete this Contest? The associated problems will be deleted as well.', 'Delete Contest', 'warning', false)
        await api.deleteContest(contestId)
        await this.getContestList(this.currentPage - 1)
      } catch (err) {
      }
    },
    async goContestProblemList (contestId) {
      await this.$router.push({
        name: 'contest-problem-list',
        params: { contestId }
      })
    },
    async handleVisibleSwitch (row) {
      await api.editContest(row)
    }
  },
  computed: {
    updateCurrentPage () {
      return this.currentChange(this.currentPage)
    }
  }
}
</script>

<style>
  .contestTitle {
    max-width: 120px;
    word-break: break-all;
  }
  .table::v-deep {
    cursor: default;
  }
</style>
