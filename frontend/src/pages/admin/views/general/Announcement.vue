<template>
  <div class="announcement view">
    <Panel :title="$t('m.General_Announcement')">
      <div class="list">
        <el-table
          ref="table"
          v-loading="loading"
          element-loading-text="loading"
          :data="announcementList"
          style="width: 100%"
        >
          <el-table-column
            width="100"
            prop="id"
            label="ID"
          />
          <el-table-column
            prop="title"
            label="Title"
          />
          <el-table-column
            prop="create_time"
            label="CreateTime"
          >
            <template slot-scope="scope">
              {{ scope.row.create_time | localtime }}
            </template>
          </el-table-column>
          <el-table-column
            prop="last_update_time"
            label="LastUpdateTime"
          >
            <template slot-scope="scope">
              {{ scope.row.last_update_time | localtime }}
            </template>
          </el-table-column>
          <el-table-column
            prop="created_by.username"
            label="Author"
          />
          <el-table-column
            width="100"
            prop="visible"
            label="Visible"
          >
            <template slot-scope="scope">
              <el-switch
                v-model="scope.row.visible"
                active-text=""
                inactive-text=""
                @change="handleVisibleSwitch(scope.row)"
              />
            </template>
          </el-table-column>
          <el-table-column
            fixed="right"
            label="Option"
            width="200"
          >
            <div slot-scope="scope">
              <icon-btn
                name="Edit"
                icon="edit"
                @click.native="openAnnouncementDialog(scope.row.id)"
              />
              <icon-btn
                name="Delete"
                icon="trash"
                @click.native="deleteAnnouncement(scope.row.id)"
              />
            </div>
          </el-table-column>
        </el-table>
        <div class="panel-options">
          <el-button
            type="primary"
            size="small"
            icon="el-icon-plus"
            @click="openAnnouncementDialog(null)"
          >
            Create
          </el-button>
          <el-pagination
            v-if="!contestID"
            class="page"
            layout="prev, pager, next"
            :page-size="pageSize"
            :total="total"
            @current-change="currentChange"
          />
        </div>
      </div>
    </Panel>
    <!--대화 상자-->
    <el-dialog
      :title="announcementDialogTitle"
      :visible.sync="showEditAnnouncementDialog"
      :close-on-click-modal="false"
      @open="onOpenEditDialog"
    >
      <el-form label-position="top">
        <el-form-item
          :label="$t('m.Announcement_Title')"
          required
        >
          <el-input
            v-model="announcement.title"
            :placeholder="$t('m.Announcement_Title')"
            class="title-input"
          />
        </el-form-item>
        <el-form-item
          :label="$t('m.Announcement_Content')"
          required
        >
          <Tiptap v-model="announcement.content" />
        </el-form-item>
        <div class="visible-box">
          <span>{{ $t('m.Announcement_visible') }}</span>
          <el-switch
            v-model="announcement.visible"
            active-text=""
            inactive-text=""
          />
        </div>
      </el-form>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <cancel @click.native="showEditAnnouncementDialog = false" />
        <save
          type="primary"
          @click.native="submitAnnouncement"
        />
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Tiptap from '../../components/Tiptap.vue'
import api from '../../api.js'

export default {
  name: 'Announcement',
  components: {
    Tiptap
  },
  data () {
    return {
      contestID: '',
      // 공지 사항 수정 대화 상자 표시
      showEditAnnouncementDialog: false,
      // 공지 목록
      announcementList: [],
      // 한 페이지에 표시되는 공지 사항 수
      pageSize: 15,
      // 총 공지 수
      total: 0,
      // 현재 공지 ID
      currentAnnouncementId: null,
      mode: 'create',
      // 공지 (new | edit) model
      announcement: {
        title: '',
        visible: true,
        content: ''
      },
      // 대화 제목
      announcementDialogTitle: 'Edit Announcement',
      // loading 표시 여부
      loading: true,
      // 현재 페이지 번호
      currentPage: 0
    }
  },
  watch: {
    $route () {
      this.init()
    }
  },
  mounted () {
    this.init()
  },
  methods: {
    init () {
      this.contestID = this.$route.params.contestId
      if (this.contestID) {
        this.getContestAnnouncementList()
      } else {
        this.getAnnouncementList(1)
      }
    },
    // 페이지 번호 콜백 전환
    currentChange (page) {
      this.currentPage = page
      this.getAnnouncementList(page)
    },
    getAnnouncementList (page) {
      this.loading = true
      api.getAnnouncementList((page - 1) * this.pageSize, this.pageSize).then(res => {
        this.loading = false
        this.total = res.data.data.total
        this.announcementList = res.data.data.results
      }, res => {
        this.loading = false
      })
    },
    getContestAnnouncementList () {
      this.loading = true
      api.getContestAnnouncementList(this.contestID).then(res => {
        this.loading = false
        this.announcementList = res.data.data
      }).catch(() => {
        this.loading = false
      })
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
    submitAnnouncement (data = undefined) {
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
      api[funcName](data).then(res => {
        this.showEditAnnouncementDialog = false
        this.init()
      }).catch()
    },
    // 공지 사항 삭제
    deleteAnnouncement (announcementId) {
      this.$confirm('Are you sure you want to delete this announcement?', 'Warning', {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(() => {
        this.loading = true
        const funcName = this.contestID ? 'deleteContestAnnouncement' : 'deleteAnnouncement'
        api[funcName](announcementId).then(res => {
          this.loading = true
          this.init()
        })
      }).catch(() => {
        this.loading = false
      })
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
  }
}
</script>

<style lang="less" scoped>
  .title-input {
    margin-bottom: 20px;
  }

  .visible-box {
    margin-top: 10px;
    width: 205px;
    float: left;
  }
</style>
