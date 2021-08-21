<template>
  <div class="flex-grow-1 mx-2">
    <b-row
      type="flex"
      cols = "1"
      id="dashboard"
    >
      <b-col>
        <user-list></user-list>
      </b-col>
    </b-row>
    <b-row
      type="flex"
      cols = "2"
      id="dashboard"
    >
      <b-col
        :md="6"
        :lg="6"
        id="first-col"
      >
        <b-card class="admin-info drop-shadow-custom" title="Underway Assignments">
          <b-table
            borderless
            hover
            :fields="assignmentListFields"
            :items="assignmentList"
            :per-page="pageSize"
            :current-page="updateCurrentPage"
          >
          </b-table>
          <div class="panel-options">
            <b-pagination
              v-model="currentPage"
              :per-page="pageSize"
              :total-rows="total"
              style="position: absolute; right: 20px; top: 15px;"
            />
          </div>
        </b-card>
      </b-col>
      <b-col
        :md="6"
        :lg="6"
        id="first-col"
      >
      </b-col>
    </b-row>
  </div>
</template>

<script>

import UserList from '../users/UserList.vue'
export default {
  name: 'LectureDashboard',
  components: {
    UserList
  },
  data () {
    return {
    }
  },
  async mounted () {
  },
  methods: {
  },
  computed: {
  }
}
</script>

<style lang="scss">
  // Be careful of common css selector in admin/oj
</style>
