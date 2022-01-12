<template>
  <div class="contest-list-card font-bold">
    <div class="top-bar mb-4">
      <h2 class="title">All Contest</h2>
    </div>
    <b-card >
      <div class="table">
        <b-table
          hover
          :items="qna"
          :fields="qnalist"
          :per-page="perPage"
          :current-page="currentPage"
          head-variant="light"
          @row-clicked="goContest"
        >
        </b-table>
      </div>
      <div
        v-if="!qnalist.length"
      >
        No Question
      </div>
    </b-card>
    <div class="pagination">
      <b-pagination
        v-model="currentPage"
        :total-rows="contest.length"
        :per-page="perPage"
        limit="3"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
// import api from '../../api.js'

export default {
  name: 'QnA',
  components: {
    // Split into many components
  },
  data () {
    return {
      qnafield: ['Title', 'Status', 'Date'],
      qnalist: [
      ]
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
