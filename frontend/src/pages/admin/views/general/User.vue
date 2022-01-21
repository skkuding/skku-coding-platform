<template>
  <div class="view">
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

      <div class="panel-options">
        <b-pagination
          v-model="currentPage"
          :total-rows="total"
          :per-page="pageSize"
          align="right"
          style="position: absolute; right:20px; top: 15px;"
        ></b-pagination>
      </div>
    </Panel>

    <Panel>
      <span slot="title"> Import User
        <b-popover
          placement="right"
          triggers="hover"
          target="import-icon"
        >
          <p>Only support csv file without headers, check the <a
            href="http://docs.onlinejudge.me/#/onlinejudge/guide/import_users"
          >link</a> for details</p>
        </b-popover>
        <b-icon
          id="import-icon"
          icon="question-circle-fill"
        />
      </span>

      <b-form-file
        v-if="!uploadUsers.length"
        v-model="uploadUsersFile"
        accept=".csv"
      ></b-form-file>

      <template v-else>
        <b-table
          :items="uploadUsersPage"
          :fields="uploadUsersPageFields"
          :per-page="0"
          :current-page="uploadUsersCurrentPage"
        >
          <template #cell(Username)="row">
            {{ row.item[0] }}
          </template>

          <template #cell(Password)="row">
            {{ row.item[1] }}
          </template>

          <template #cell(Email)="row">
            {{ row.item[2] }}
          </template>
        </b-table>

        <div class="panel-options">
          <b-button
            variant="primary"
            size="sm"
            @click="handleUsersUpload"
            style="margin-right: 10px;"
          >
            <b-icon
              icon="upload"
              size="sm"
            ></b-icon>
            Import All
          </b-button>
          <b-button
            variant="danger"
            size="sm"
            @click="handleResetData"
          >
            <b-icon
              icon="arrow-counterclockwise"
              size="sm"
            ></b-icon>
            Reset Data
          </b-button>
          <b-pagination
            class="page"
            v-model="uploadUsersCurrentPage"
            :total-rows="uploadUsers.length"
            :per-page="uploadUsersPageSize"
            align="right"
            style="position: absolute; right:20px; top: 15px;"
          >
          </b-pagination>
        </div>
      </template>
    </Panel>

    <Panel title="Generate User">
      <b-form-group
        ref="form-generate-user"
      >
        <b-row
          type="flex"
          justify="space-between"
        >
          <b-col cols="2">
            <p class="labels">
              Prefix
            </p>
            <b-form-input
              v-model="formGenerateUser.prefix"
              placeholder="Prefix"
            ></b-form-input>
          </b-col>
          <b-col cols="2">
            <p class="labels">
              Suffix
            </p>
            <b-form-input
              v-model="formGenerateUser.suffix"
              placeholder="Suffix"
            ></b-form-input>
          </b-col>
          <b-col cols="2">
            <p class="labels">
              <span class="text-danger">*</span> Start Number
            </p>
            <b-form-input
              v-model="formGenerateUser.number_from"
              type="number"
            ></b-form-input>
          </b-col>
          <b-col cols="2">
            <p class="labels">
              <span class="text-danger">*</span> End Number
            </p>
            <b-form-input
              v-model="formGenerateUser.number_to"
              type="number"
            ></b-form-input>
          </b-col>
          <b-col cols="3">
            <p class="labels">
              <span class="text-danger">*</span> Password Length
            </p>
            <b-form-input
              v-model="formGenerateUser.password_length"
              placeholder="Password Length"
              type="number"
            ></b-form-input>
          </b-col>
        </b-row>
      </b-form-group>

      <b-button
        variant="primary"
        size="sm"
        @click="generateUser"
      >
        <b-icon icon="people-fill" />
        Generate & Export
      </b-button>
      <span
        v-if="formGenerateUser.number_from && formGenerateUser.number_to &&
          compareNumber(formGenerateUser.number_from, formGenerateUser.number_to) >= 0"
        class="userPreview"
      >
        The usernames will be {{ formGenerateUser.prefix + formGenerateUser.number_from + formGenerateUser.suffix }},
        <span v-if="compareNumber(formGenerateUser.number_from, formGenerateUser.number_to) > 1">
          {{ formGenerateUser.prefix + ((Number)(formGenerateUser.number_from) + 1) + formGenerateUser.suffix + '...' }}
        </span>
        <span v-if="compareNumber(formGenerateUser.number_from, formGenerateUser.number_to) >= 1">
          {{ formGenerateUser.prefix + formGenerateUser.number_to + formGenerateUser.suffix }}
        </span>
      </span>
    </Panel>

    <b-modal
      v-model="showUserDialog"
      title="User"
      size="lg"
      centered
    >
      <b-form-group>
        <b-row style="margin-top: 24px;">
          <b-col cols="3">
            <span class="text-danger">*</span> Username
          </b-col>
          <b-col cols="3">
            <b-form-input
              v-model="user.username"
            ></b-form-input>
          </b-col>
          <b-col cols="3">
            Real Name
          </b-col>
          <b-col cols="3">
            <b-form-input
              v-model="user.real_name"
            ></b-form-input>
          </b-col>
        </b-row>

        <b-row style="margin-top: 24px;">
          <b-col cols="3">
            <span class="text-danger">*</span> Email
          </b-col>
          <b-col cols="3">
            <b-form-input
              v-model="user.email"
            ></b-form-input>
          </b-col>
          <b-col cols="3">
            New password
          </b-col>
          <b-col cols="3">
            <b-form-input
              v-model="user.password"
            ></b-form-input>
          </b-col>
        </b-row>

        <b-row style="margin-top: 24px;">
          <b-col cols="3">
            User Type
          </b-col>
          <b-col cols="3">
            <b-form-select
              v-model="user.admin_type"
              :options="adminTypeOptions"
            ></b-form-select>
          </b-col>
          <b-col cols="3">
            User Major
          </b-col>
          <b-col cols="3">
            <b-form-select
              v-model="user.major"
              :options="majorOptions"
            ></b-form-select>
          </b-col>
        </b-row>

        <b-row style="margin-top: 24px;">
          <b-col cols="3">
            Problem Permission
          </b-col>
          <b-col cols="4">
            <b-form-select
              v-model="user.problem_permission"
              :options="problemPermissionOptions"
              :disabled="user.admin_type!=='Admin'"
            ></b-form-select>
          </b-col>
        </b-row>

        <b-row style="margin-top: 24px;">
          <b-col cols="3">
            Open API
          </b-col>
          <b-col cols="1">
            <b-form-checkbox
              v-model="user.open_api"
              switch
            >
            </b-form-checkbox>
          </b-col>
          <b-col cols="3">
            Is Disabled
          </b-col>
          <b-col cols="1">
            <b-form-checkbox
              v-model="user.is_disabled"
              switch
            >
            </b-form-checkbox>
          </b-col>
        </b-row>
      </b-form-group>
      <template #modal-footer>
        <cancel @click.native="showUserDialog = false">Cancel</cancel>
        <save @click.native="saveUser()" />
      </template>
    </b-modal>
  </div>
</template>

<script>
import papa from 'papaparse'
import api from '../../api.js'
import utils from '@/utils/utils'

export default {
  name: 'User',
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
        { key: 'email', label: 'Email' },
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
      formGenerateUser: {
        prefix: '',
        suffix: '',
        number_from: 0,
        number_to: 0,
        password_length: 8
      },
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
  },
  async mounted () {
    await this.getUserList(1)
  },
  methods: {
    // 페이지 번호 콜백 전환
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
        await api.deleteUsers(ids.join(','))
      } catch (err) {
      } finally {
        await this.getUserList(this.currentPage)
        this.selectedUserIDs = []
      }
    },
    async generateUser () {
      this.loadingGenerate = true
      const data = Object.assign({}, this.formGenerateUser)
      try {
        const res = await api.generateUser(data)
        this.loadingGenerate = false
        const url = '/admin/generate_user?file_id=' + res.data.data.file_id
        await utils.downloadFile(url)
        this.$alert('All users created successfully, the users sheets have downloaded to your disk.', 'Notice')
        await this.getUserList(1)
      } catch (err) {
        this.loadingGenerate = false
      }
    },
    compareNumber (start, end) {
      start *= 1
      end *= 1
      return end - start
    },
    handleUsersCSV (file) {
      papa.parse(file, {
        complete: (results) => {
          const data = results.data.filter(user => {
            return user[0] && user[1] && user[2]
          })
          const delta = results.data.length - data.length
          if (delta > 0) {
            this.$error(delta + ' users have been filtered due to empty value')
          }
          this.uploadUsersCurrentPage = 1
          this.uploadUsers = data
          this.uploadUsersPage = data.slice(0, this.uploadUsersPageSize)
        },
        error: (error) => {
          this.$error(error)
        }
      })
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
  }
}
</script>

<style scoped lang="scss">
  .import-user-icon {
    color: #555555;
    margin-left: 4px;
  }

  .userPreview {
    padding-left: 10px;
  }

  .notification {
    p {
      margin: 0;
      text-align: left;
    }
  }
  .table{
    cursor: default;
  }
</style>
<style>
  .userTable {
    min-width: 100px;
  }
  .uploadUserTable {
    word-break: break-all;
    max-width: 200px;
  }
</style>
