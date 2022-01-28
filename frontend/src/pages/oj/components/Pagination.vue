<template>
  <div class="pagination">
    <div class="page-itm">
      <div @click="changePage(1)" class="page-btn">&lt;&lt;</div>
      <div @click="changePage(currentPage-1)" class="page-btn">&lt;</div>
      <div
        v-for="page in pageList"
        :key="page"
        @click="changePage(page)"
        :class="[ page==currentPage? 'page-btn select': 'page-btn' ]">
        {{page}}
        </div>
      <div @click="changePage(currentPage+1)" class="page-btn">&gt;</div>
      <div @click="changePage(numberOfPages)" class="page-btn">&gt;&gt;</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Pagination',
  props: {},
  data () {
    return {
      rows: 45, // number of total rows in table
      perPage: 3, // number of rows in table per one page
      currentPage: 1,
      limit: 3 // maximum of number of pages
    }
  },
  methods: {
    changePage (page) {
      if (page >= 1 && page <= this.numberOfPages) {
        this.currentPage = page
      }
    }
  },
  computed: {
    numberOfPages () { // number of pages (if 9 rows and 3 for each pages, then 3 pages)
      return Math.ceil(this.rows / this.perPage)
    },
    startPage () {
      var start = (Math.trunc((this.currentPage - 1) / this.limit)) * this.limit + 1
      return start
    },
    endPage () {
      var end = this.startPage + this.limit - 1
      return end < this.numberOfPages ? end : this.numberOfPages
    },
    pageList () {
      var pages = []
      for (let i = this.startPage; i <= this.endPage; i++) {
        pages.push(i)
      }
      return pages
    }
  }
}
</script>

<style lang="scss" scoped>
.pagination {
  width: 95%;
  margin-right: 10%;
  margin-top: 10px;
  display: flex;
  justify-content: flex-end !important;
}

.page-itm {
  border-radius: 50rem !important;
  margin: 20px 5% 16px 0;
  display: flex;
  flex-direction: row;
}

.page-btn {
  width: 30px;
  height: 30px;
  text-align: center;
  line-height: 25px;
  margin-left: 0.25rem;
  border-radius: 5px !important;
  color: #bdbdbd;
  border: thin solid #bdbdbd;
  cursor: pointer;
}

.page-btn.select {
    background-color: #bdbdbd;
    color: white;
}

.page-btn:hover {
  background-color: #bdbdbd;
  color: white;
}

</style>
