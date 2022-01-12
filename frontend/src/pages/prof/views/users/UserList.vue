<template>
  <Panel title="Users">
    <div slot="header">
      <b-row align-v="center" align-h="center" style="margin: 0px">
        <b-col cols="3" style="padding: 0px">
          <b-button
            :disabled="!selectedUserIDs.length"
            variant="danger"
            size="sm"
            @click="deleteUsers(selectedUserIDs)"
          >
            <b-icon icon="trash-fill"></b-icon> Delete
          </b-button>
        </b-col>
        <b-col cols="3" style="padding: 0px">
          <b-button
            variant="outline-primary"
            size="sm"
            @click="selectAll()"
          >
            Select All
          </b-button>
        </b-col>
        <b-col cols="6" style="padding: 0px">
          <b-form-input
            v-model="keyword"
            placeholder="Keywords"
          />
        </b-col>
      </b-row>
    </div>

    <b-table
      v-model="usersPerPage"
      :items="userList"
      :fields="userListFields"
      :per-page="pageSize"
      :current-page="updateCurrentPage"
      responsive
      style="width: 100%"
    >
      <template #cell(selection)="row">
        <b-form-checkbox
          v-model="selectedUserIDs"
          :value="row.item.id"
        >
        </b-form-checkbox>
      </template>

      <template #cell(create_time)="row">
        {{ row.item.create_time | localtime }}
      </template>

      <template #cell(last_login)="row">
        {{ row.item.last_login | localtime }}
      </template>

      <template #cell(Option)="row">
        <icon-btn
          name="Edit"
          icon="clipboard-plus"
          @click.native="openUserDialog(row.item.id)"
        />
        <icon-btn
          name="Delete"
          icon="trash"
          @click.native="deleteUsers([row.item.id])"
        />
      </template>
    </b-table>
    <b-row cols="2" h-align="around">
      <b-col col="3">
        <b-button v-b-modal.register-new-user>+ Register New User</b-button>
        <register-new-user-modal></register-new-user-modal>
      </b-col>
      <b-col class="panel-options" col="5">
        <b-pagination
          v-model="currentPage"
          :total-rows="total"
          :per-page="pageSize"
          align="right"
          style="position: absolute; right:20px; top: 15px;"
        ></b-pagination>
      </b-col>
    </b-row>
  </Panel>
</template>

<script>
import api from '../../api.js'
import RegisterNewUserModal from './RegisterNewUser.vue'

export default {
  name: 'UserList',
  components: {
    RegisterNewUserModal
  },
  data () {
    return {
      pageSize: 10,
      total: 0,
      userList: [],
      userListFields: [
        { key: 'selection', label: '' },
        { key: 'id', label: 'ID' },
        { key: 'username', label: 'Username' },
        { key: 'create_time', label: 'Create Time' },
        { key: 'last_login', label: 'Last Login' },
        { key: 'real_name', label: 'Real Name' },
        { key: 'email', label: 'Eamil' },
        { key: 'admin_type', label: 'User Type' },
        { key: 'major', label: 'User Major' },
        { key: 'Option', label: 'Option', thClass: 'userTable' }
      ],
      usersPerPage: [],
      uploadUsersFile: null,
      uploadUsers: [],
      uploadUsersPage: [],
      uploadUsersPageFields: [
        { key: 'Username', label: 'Username', thClass: 'uploadUserTable' },
        { key: 'Password', label: 'Password', thClass: 'uploadUserTable' },
        { key: 'Email', label: 'Email', thClass: 'uploadUserTable' }
      ],
      uploadUsersCurrentPage: 1,
      uploadUsersPageSize: 15,
      keyword: '',
      showUserDialog: false,
      user: {},
      loadingTable: false,
      currentPage: 0,
      adminTypeOptions: [
        { value: 'Regular User', text: 'Regular User' },
        { value: 'Admin', text: 'Admin' },
        { value: 'Super Admin', text: 'Super Admin' }
      ],
      majorOptions: [
        { value: 'Major', text: 'Major(원전공)' },
        { value: 'Double Major', text: 'Double Major(복수전공)' },
        { value: 'Non-CS Major', text: 'Non-CS Major(비전공)' }
      ],
      problemPermissionOptions: [
        { value: 'None', text: 'None' },
        { value: 'Own', text: 'Own' },
        { value: 'All', text: 'All' }
      ],
      selectedUserIDs: []
    }
  },
  async mounted () {
    await this.getUserList(1)
  },
  methods: {
    async currentChange (page) {
      this.currentPage = page
      await this.getUserList(page)
    },
    // 사용자 정보 수정을 위해 제출
    async saveUser () {
      try {
        await api.editUser(this.user)
        // 업데이트 목록
        await this.getUserList(this.currentPage)
        this.showUserDialog = false
      } catch (err) {
      }
    },
    // 사용자 대화 상자 열기
    async openUserDialog (id) {
      this.showUserDialog = true
      const res = await api.getUser(id)
      this.user = res.data.data
    },
    // 사용자 목록 가져 오기
    async getUserList (page) {
      this.loadingTable = true
      try {
        const res = await api.getUserList((page - 1) * this.pageSize, this.pageSize, this.keyword)
        this.total = res.data.data.total
        this.userList = res.data.data.results
      } catch (err) {
      } finally {
        this.loadingTable = false
      }
    },
    async deleteUsers (ids) {
      try {
        await this.$confirm('Sure to delete the user? The associated resources created by this user will be deleted as well, like problem, contest, announcement, etc.', 'confirm', 'warning', false)
      } catch (err) {
      }
      try {
        await api.deleteUsers(ids.join(','))
      } catch (err) {
      } finally {
        await this.getUserList(this.currentPage)
        this.selectedUserIDs = []
      }
    },
    compareNumber (start, end) {
      start *= 1
      end *= 1
      return end - start
    },
    async handleUsersUpload () {
      try {
        await api.importUsers(this.uploadUsers)
        await this.getUserList(1)
        this.handleResetData()
      } catch (err) {
      }
    },
    handleResetData () {
      this.uploadUsers = []
    },
    selectAll () {
      if (this.selectedUserIDs.length === this.usersPerPage.length) {
        this.selectedUserIDs = []
      } else {
        for (const users of this.usersPerPage) {
          if (this.selectedUserIDs.indexOf(users.id) === -1) {
            this.selectedUserIDs.push(users.id)
          }
        }
      }
    }
  },
  computed: {
    updateCurrentPage () {
      return this.currentChange(this.currentPage)
    }
  },
  watch: {
    'keyword' () {
      this.currentChange(1)
    },
    'user.admin_type' () {
      if (this.user.admin_type === 'Super Admin') {
        this.user.problem_permission = 'All'
      } else if (this.user.admin_type === 'Regular User') {
        this.user.problem_permission = 'None'
      }
    },
    'uploadUsersCurrentPage' (page) {
      this.uploadUsersPage = this.uploadUsers.slice((page - 1) * this.uploadUsersPageSize, page * this.uploadUsersPageSize)
    },
    'uploadUsersFile' () {
      this.handleUsersCSV(this.uploadUsersFile)
    }
  }
}
</script>

<style lang="scss">
  // Be careful of common css selector in admin/oj
</style>
