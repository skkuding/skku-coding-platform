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
              @change="handleVisibleSwitch(row.item)"
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
              @change="handleVisibleSwitch(row.item)"
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
      <p class="labels">
        <span class="text-danger">*</span> Content
      </p>
      <tiptap v-model="announcement.content" />
      <div class="visible-box">
        <span>Visible</span>
        <b-form-checkbox
          v-model="announcement.visible"
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
        { key: 'option', label: 'Option', thClass: 'announcementOption', tdClass: 'announcementOption' }
      ],
      pageSize: 15,
      total: 0,
      currentAnnouncementId: null,
      mode: 'create',
      announcement: {
        title: '',
        visible: true,
        content: ''
      },
      announcementDialogTitle: 'Edit Announcement',
      currentPage: 0
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
          visible: this.announcement.visible
        }
      }
      if (this.contestID) {
        data.contest_id = this.contestID
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
    openAnnouncementDialog (id) {
      this.showEditAnnouncementDialog = true
      if (id !== null) {
        this.currentAnnouncementId = id
        this.announcementDialogTitle = 'Edit Announcement'
        this.announcementList.find(item => {
          if (item.id === this.currentAnnouncementId) {
            this.announcement.title = item.title
            this.announcement.visible = item.visible
            this.announcement.content = item.content
            this.mode = 'edit'
            return true
          }
          return false
        })
      } else {
        this.announcementDialogTitle = 'Create Announcement'
        this.announcement.title = ''
        this.announcement.visible = true
        this.announcement.content = ''
        this.mode = 'create'
      }
    },
    handleVisibleSwitch (row) {
      this.mode = 'edit'
      this.submitAnnouncement({
        id: row.id,
        title: row.title,
        content: row.content,
        visible: row.visible
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

  .visible-box {
    margin-top: 10px;
    width: 205px;
    float: left;
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
