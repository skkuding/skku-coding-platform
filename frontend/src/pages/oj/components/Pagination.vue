<template>
  <div class="pagination">
    <div class="page-itm">
      <div v-on:click="toFront" class="page-btn">&lt;&lt;</div>
      <div v-on:click="toPrev" class="page-btn">&lt;</div>
      <div class="page-btn">{{currentPage}}</div>
      <div v-on:click="toNext" class="page-btn">&gt;</div>
      <div v-on:click="toEnd" class="page-btn">&gt;&gt;</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Pagination',
  props: {},
  methods: {
    toFront: function () {
      console.log('front')
      this.currentPage = 1
    },
    toPrev: function () {
      console.log('prev')
      if (this.currentPage > 1) {
        this.currentPage -= 1
      }
    },
    toNext: function () {
      console.log('next')
      if (this.currentPage < this.limit) {
        this.currentPage += 1
      }
    },
    toEnd: function () {
      console.log('end')
      this.currentPage = this.limit
    }
  },
  data () {
    return {
      limit: 5,
      currentPage: 3
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
  padding: 0.25rem;
  display: flex;
  flex-direction: row;
}

.page-btn {
  width: 30px;
  height: 30px;
  text-align: center;
  line-height: 25px;
  margin-right: 0.25rem;
  border-radius: 5px !important;
  color: #bdbdbd;
  border: thin solid #bdbdbd;
  cursor: pointer;
}

.page-btn:hover{
  background-color: #bdbdbd;
  color: white;
}
</style>
