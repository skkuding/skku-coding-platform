<template>
  <div class="page-itm">
    <div @click="changePage(1)" class="page-btn leftedge">«</div>
    <div @click="changePage(currentPage-1)" class="page-btn">&lt;</div>
    <div
      v-for="page in pageList"
      :key="page"
      @click="changePage(page)"
      :class="[ page==currentPage? 'page-btn select': 'page-btn' ]">
      {{page}}
      </div>
    <div @click="changePage(currentPage+1)" class="page-btn">&gt;</div>
    <div @click="changePage(numberOfPages)" class="page-btn rightedge">»</div>
  </div>
</template>

<script>
export default {
  name: 'Pagination',
  props: {
    totalRows: { // number of total rows in table
      type: Number
    },
    perPage: { // number of rows in table per one page
      type: Number
    },
    limit: {
      type: String
    }
  },
  data () {
    return {
      currentPage: 1
    }
  },
  methods: {
    changePage (page) {
      if (page >= 1 && page <= this.numberOfPages) {
        this.currentPage = page
        this.$emit('input', this.currentPage)
      }
    }
  },
  computed: {
    numberOfPages () { // number of pages
      return Math.ceil(this.totalRows / this.perPage)
    },
    startPage () {
      var start = (Math.trunc((this.currentPage - 1) / this.limit)) * this.limit + 1
      return start
    },
    endPage () {
      var end = this.startPage + Number(this.limit) - 1
      return end <= this.numberOfPages ? end : this.numberOfPages
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
.page-itm {
  width: 95%;
  margin: 20px 5% 16px 0;
  display: flex;
  justify-content: flex-end !important;
  flex-direction: row;
}

.page-btn {
  width: 35px;
  height: 38px;
  text-align: center;
  margin-left: -1px;
  line-height: 35px;
  color: #bdbdbd;
  border: thin solid #dadada;
  cursor: pointer;
}

.page-btn.leftedge {
  border-top-left-radius: 0.25rem !important;
  border-bottom-left-radius: 0.25rem !important;
}

.page-btn.rightedge {
  border-top-right-radius: 0.25rem !important;
  border-bottom-right-radius: 0.25rem !important;
}

.page-btn.select {
    background-color: #bdbdbd;
    border: thin solid #bdbdbd;
    color: white;
    pointer-events: none;
}

.page-btn:hover {
  background-color: #e9ecee;
}

</style>
