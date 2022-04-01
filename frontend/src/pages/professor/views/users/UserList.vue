<template>
  <Panel title="Students">
    <div slot="header">
      <b-row align-v="center"  style="margin: 0px">
        <b-col cols="6" >
          <b-button
            :disabled="!selectedUserIDs.length"
            variant="danger"
            size="sm"
            style="min-width:90px"
            @click="deleteUsers(selectedUserIDs)"
          >
            <b-icon icon="trash-fill"></b-icon> Delete
          </b-button>
        </b-col>
        <b-col cols="6">
          <b-button
            variant="outline-primary"
            size="sm"
            @click="selectAll()"
          >
            Select All
          </b-button>
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
          :value="row.item.registration_id"
        >
        </b-form-checkbox>
      </template>

      <template #cell(index)="data">
        {{ (currentPage - 1) * pageSize + (data.index + 1) }}
      </template>

      <template #cell(create_time)="data">
        {{ data.item.create_time ? data.item.create_time.split(/[T]|[.]|[+]/).slice(0,2).join(' ') : 'No data' }}
      </template>

      <template #cell(last_login)="data">
        {{ data.item.last_login ? data.item.last_login.split(/[T]|[.]|[+]/).slice(0,2).join(' ') : 'No data'}}
      </template>

      <template #cell(Option)="row">
        <icon-btn
          name="Delete"
          icon="trash"
          @click.native="deleteUsers([row.item.registration_id])"
        />
      </template>
    </b-table>
    <b-row cols="2" h-align="around">
      <b-col col="3">
        <b-button v-b-modal.register-new-user>+ Register New Students</b-button>
        <register-new-user-modal :course-title="courseTitle" @update="currentChange(currentPage)"></register-new-user-modal>
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
  props: [
    'course-title'
  ],
  data () {
    return {
      pageSize: 5,
      total: 0,
      userList: [],
      userListFields: [
        { key: 'selection', label: '' },
        'index',
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
      user: {},
      currentPage: 1,
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
      selectedUserIDs: [],
      courseId: null,
      mounted: false
    }
  },
  async mounted () {
    this.mounted = true
    this.courseId = this.$route.params.courseId
    await this.getUserList(1)
  },
  methods: {
    currentChange (page) {
      if (!this.mounted) {
        return
      }
      this.currentPage = page
      this.getUserList(page)
    },
    async getUserList (page) {
      try {
        const res = await api.getCourseStudents(this.courseId, this.pageSize, (page - 1) * this.pageSize)
        this.total = res.data.data.total
        this.userList = res.data.data.results.map(result => Object({
          registration_id: result.id,
          course: result.course,
          ...result.user
        }))
      } catch (err) {
      }
    },
    async deleteUsers (registrationIds) {
      const sure = await this.$bvModal.msgBoxConfirm('Sure to delete the user? All Associated submissions and informations will be deleted', {
        title: 'Are you sure?',
        size: 'md',
        centered: true
      })
      if (sure === true) {
        for (const registrationId of registrationIds) {
          try {
            await api.deleteStudent(registrationId)
          } catch (error) {
            this.$error(error)
          }
        }
        await this.getUserList(this.currentPage)
        this.selectedUserIDs = []
      }
    },
    selectAll () {
      if (this.selectedUserIDs.length === this.usersPerPage.length) {
        this.selectedUserIDs = []
      } else {
        for (const users of this.usersPerPage) {
          if (this.selectedUserIDs.indexOf(users.registration_id) === -1) {
            this.selectedUserIDs.push(users.registration_id)
          }
        }
      }
    }
  },
  computed: {
    updateCurrentPage () {
      return this.currentChange(this.currentPage)
    }
  }
}
</script>

<style lang="scss">
</style>
