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
        :md="5"
        :lg="4"
        id="first-col"
      >

      </b-col>
      <b-col
        :md="5"
        :lg="4"
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
