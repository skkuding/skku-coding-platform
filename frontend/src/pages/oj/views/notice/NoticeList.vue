<template>
    <div>
        <b-card title="Notice" class="border-0" bg-variant="transparent">
          <div class="table">
            <b-table
              hover
              :items="items"
              :per-page="perPage"
              :current-page="currentPage"
              head-variant="light"
            ></b-table>
          </div>
          <div class="pagination">
              <b-pagination
                aria-controls="notice-list"
                v-model="currentPage"
                :total-rows=100
                :per-page="perPage"
                limit="3"
              ></b-pagination>
          </div>
        </b-card>
    </div>
</template>

<script>
export default {
  data () {
    return {
      perPage: 10,
      currentPage: 1,
      items: [
        { title: 'SKKU Coding Platform Contest', date: '2021-01-01' },
        { title: 'SKKU Coding Platform 2nd Contest', date: '2020-01-02' },
        { title: 'SKKU Coding Platform 3rd Contest', date: '2020-01-03' },
        { title: 'SKKU Coding Platform 4th Contest', date: '2020-01-04' }
      ]
    }
  },
  computed: {
    rows () {
      return this.items.length
    }
  }
}
</script>

<style>
  .pagination{

    display: flex;
    justify-content: flex-end;
  }
</style>