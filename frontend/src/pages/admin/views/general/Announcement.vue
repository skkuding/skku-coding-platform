<template>
  <div class="announcement view">
    <Panel title="Announcement">
      <div class="list">
        <b-table
          v-if="!contestID"
          :items="announcementList"
          :fields="announcementListFields"
          :per-page="pageSize"
          :current-page="updateCurrentPage"
          style="width: 100%"
        >
          <template #cell(create_time)="row">
            {{ row.item.create_time | localtime }}
          </template>

          <template #cell(last_update_time)="row">
            {{ row.item.last_update_time | localtime }}
          </template>

          <template #cell(visible)="row">
            <b-form-checkbox
              v-model="row.item.visible"
              @change="handleSwitch(row.item)"
              switch
            >
            </b-form-checkbox>
          </template>

          <template #cell(top_fixed)="row">
            <b-form-checkbox
              v-model="row.item.top_fixed"
              @change="handleSwitch(row.item)"
              switch
            >
            </b-form-checkbox>
          </template>

          <template #cell(option)="row">
            <icon-btn
              name="Edit"
              icon="clipboard-plus"
              @click.native="openAnnouncementDialog(row.item.id)"
            />
            <icon-btn
              name="Delete"
              icon="trash"
              @click.native="deleteAnnouncement(row.item.id)"
            />
          </template>
        </b-table>

        <b-table
          v-else
          :items="contestAnnouncementList"
          :fields="announcementListFields"
          style="width: 100%"
        >
          <template #cell(create_time)="row">
            {{ row.item.create_time | localtime }}
          </template>

          <template #cell(last_update_time)="row">
            {{ row.item.last_update_time | localtime }}
          </template>

          <template #cell(visible)="row">
            <b-form-checkbox
              v-model="row.item.visible"
              @change="handleSwitch(row.item)"
              switch
            >
            </b-form-checkbox>
          </template>

          <template #cell(top_fixed)="row">
            <b-form-checkbox
              v-model="row.item.top_fixed"
              @change="handleSwitch(row.item)"
              switch
            >
            </b-form-checkbox>
          </template>

          <template #cell(option)="row">
            <icon-btn
              name="Edit"
              icon="clipboard-plus"
              @click.native="openAnnouncementDialog(row.item.id)"
            />
            <icon-btn
              name="Delete"
              icon="trash"
              @click.native="deleteAnnouncement(row.item.id)"
            />
          </template>
        </b-table>

        <div class="panel-options">
          <b-button
            variant="primary"
            size="sm"
            @click="openAnnouncementDialog(null)"
          >
            <b-icon icon="plus" />
            Create
          </b-button>

          <b-pagination
            v-if="!contestID"
            v-model="currentPage"
            :total-rows="total"
            :per-page="pageSize"
            style="position: absolute; right: 20px; top: 15px;"
          >
          </b-pagination>
        </div>
      </div>
    </Panel>

    <b-modal
      v-model="showEditAnnouncementDialog"
      :title="announcementDialogTitle"
      size="lg"
      centered
    >
      <p class="labels">
        <span class="text-danger">*</span> Title
      </p>
      <b-form-input
        v-model="announcement.title"
        placeholder="Title"
      >
      </b-form-input>
      <p class="labels" v-if="contestID">
        <span class="text-danger">*</span> Related Problem ID
      </p>
      <b-form-select
        v-if="contestID"
        v-model="announcement.problem_id"
        placeholder="Problem ID"
        :options="problemOption"
      >
      </b-form-select>
      <p class="labels">
        <span class="text-danger">*</span> Content
      </p>
      <tiptap v-model="announcement.content" />
      <div class="switch-box">
        <span>Visible</span>
        <b-form-checkbox
          v-model="announcement.visible"
          switch
          style="magin-right: 20px;"
        />
      </div>
      <div class="switch-box">
        <span>Top Fixed</span>
        <b-form-checkbox
          v-model="announcement.top_fixed"
          switch
        />
      </div>
      <template #modal-footer>
        <cancel @click.native="showEditAnnouncementDialog = false">Cancel</cancel>
        <save @click.native="submitAnnouncement" />
      </template>
    </b-modal>
  </div>
</template>

<script>
import tiptap from '../../components/Tiptap.vue'
import api from '../../api.js'

export default {
  name: 'Announcement',
  components: {
    tiptap
  },
  data () {
    return {
      contestID: '',
      showEditAnnouncementDialog: false,
      contestAnnouncementList: [],
      announcementList: [],
      announcementListFields: [
        { key: 'id', label: 'ID', thStyle: 'width: 100px' },
        { key: 'title', label: 'Title', thClass: 'announcementTitle', tdClass: 'announcementTitle' },
        { key: 'create_time', label: 'CreateTime' },
        { key: 'last_update_time', label: 'LastUpdateTime' },
        { key: 'created_by.username', label: 'Author' },
        { key: 'visible', label: 'Visible' },
        { key: 'top_fixed', label: 'Top Fixed' },
        { key: 'option', label: 'Option', thClass: 'announcementOption', tdClass: 'announcementOption' }
      ],
      pageSize: 15,
      total: 0,
      currentAnnouncementId: null,
      mode: 'create',
      announcement: {
        title: '',
        visible: true,
        top_fixed: false,
        content: ''
      },
      announcementDialogTitle: 'Edit Announcement',
      currentPage: 0,
      problemOption: [],
      bank: false
    }
  },
  watch: {
    async '$route' () {
      await this.init()
    }
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      this.contestID = this.$route.params.contestId
      const res = await api.getContest(this.contestID)
      if (res.data.data.is_bank === true) {
        this.bank = true
      }
      if (this.contestID) {
        await this.getContestAnnouncementList()
      } else {
        await this.getAnnouncementList(1)
      }
    },
    // 페이지 번호 콜백 전환
    async currentChange (page) {
      this.currentPage = page
      await this.getAnnouncementList(page)
    },
    async getAnnouncementList (page) {
      this.loading = true
      try {
        const res = await api.getAnnouncementList((page - 1) * this.pageSize, this.pageSize)
        this.loading = false
        this.total = res.data.data.total
        this.announcementList = res.data.data.results
      } catch (err) {
        this.loading = false
      }
    },
    async getContestAnnouncementList () {
      this.loading = true
      try {
        const res = await api.getContestAnnouncementList(this.contestID)
        this.loading = false
        this.contestAnnouncementList = res.data.data
      } catch (err) {
        this.loading = false
      }
    },
    // 편집 대화 상자를 열기위한 콜백
    onOpenEditDialog () {
      // 최적화 필요
      // 텍스트 편집기 디스플레이 비정상적인 버그를 일시적으로 해결
      setTimeout(() => {
        if (document.createEvent) {
          const event = document.createEvent('HTMLEvents')
          event.initEvent('resize', true, true)
          window.dispatchEvent(event)
        } else if (document.createEventObject) {
          window.fireEvent('onresize')
        }
      }, 0)
    },
    // 수정 제출
    // MouseEvent 기본 수신
    async submitAnnouncement (data = undefined) {
      let funcName = ''
      if (!data.title) {
        data = {
          id: this.currentAnnouncementId,
          title: this.announcement.title,
          content: this.announcement.content,
          visible: this.announcement.visible,
          top_fixed: this.announcement.top_fixed
        }
      }
      if (this.contestID) {
        data.contest_id = this.contestID
        data.problem_id = this.announcement.problem_id
        funcName = this.mode === 'edit' ? 'updateContestAnnouncement' : 'createContestAnnouncement'
      } else {
        funcName = this.mode === 'edit' ? 'updateAnnouncement' : 'createAnnouncement'
      }
      try {
        await api[funcName](data)
        this.showEditAnnouncementDialog = false
        await this.init()
      } catch (err) {
      }
    },
    // 공지 사항 삭제
    async deleteAnnouncement (announcementId) {
      try {
        await this.$confirm('Are you sure you want to delete this announcement?', 'Warning', 'warning', false)
        this.loading = true
        const funcName = this.contestID ? 'deleteContestAnnouncement' : 'deleteAnnouncement'
        await api[funcName](announcementId)
        this.loading = true
        await this.init()
      } catch (err) {
        this.loading = true
      }
    },
    async getProblemOption () {
      const data = this.bank
        ? await this.getProblemBankContestProblem()
        : await this.getContestProblemList()
      this.problemOption = data.map(item => ({
        value: item.id,
        text: item._id + ' ' + item.title
      })
      )
    },
    async getProblemBankContestProblem () {
      const res = await api.getProblemBankContestProblem(this.contestID)
      return res.data.data
    },
    async getContestProblemList () {
      const res = await api.getContestProblemList({
        contest_id: this.contestID,
        limit: 100,
        offset: 0
      })
      return res.data.data.results
    },
    async openAnnouncementDialog (id) {
      this.showEditAnnouncementDialog = true
      if (id !== null) {
        if (this.contestID) {
          this.currentAnnouncementId = id
          this.announcementDialogTitle = 'Edit Clarification'
          this.contestAnnouncementList.find(item => {
            if (item.id === this.currentAnnouncementId) {
              this.announcement.title = item.title
              this.announcement.visible = item.visible
              this.announcement.top_fixed = item.top_fixed
              this.announcement.content = item.content
              this.announcement.problem_id = item.problem
              this.mode = 'edit'
              return true
            }
            return false
          })
          await this.getProblemOption()
        } else {
          this.currentAnnouncementId = id
          this.announcementDialogTitle = 'Edit Announcement'
          this.announcementList.find(item => {
            if (item.id === this.currentAnnouncementId) {
              this.announcement.title = item.title
              this.announcement.visible = item.visible
              this.announcement.top_fixed = item.top_fixed
              this.announcement.content = item.content
              this.mode = 'edit'
              return true
            }
            return false
          })
        }
      } else {
        this.announcementDialogTitle = 'Create Announcement'
        this.announcement.title = ''
        this.announcement.visible = true
        this.announcement.top_fixed = false
        this.announcement.content = ''
        this.announcement.problem_id = ''
        this.mode = 'create'
        if (this.contestID) {
          await this.getProblemOption()
        }
      }
    },
    handleSwitch (row) {
      this.mode = 'edit'
      this.submitAnnouncement({
        id: row.id,
        title: row.title,
        content: row.content,
        visible: row.visible,
        top_fixed: row.top_fixed
      })
    }
  },
  computed: {
    updateCurrentPage () {
      return this.currentChange(this.currentPage)
    }
  }
}
</script>

<style lang="scss" scoped>
  .title-input {
    margin-bottom: 20px;
  }

  .switch-box {
    display: flex;
    margin-top: 10px;
    margin-right: 20px;
    & span {
      margin-right: 10px;
    }
  }
  .table td {
    cursor: default;
  }
</style>

<style>
  .announcementTitle {
    max-width: 150px;
    word-break: break-all;
  }

  .announcementOption {
    min-width: 150px;
  }
</style>
