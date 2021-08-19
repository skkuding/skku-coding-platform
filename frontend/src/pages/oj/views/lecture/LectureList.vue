<template>
  <div class="lecture-list-card font-bold">
    <div class="mb-5" style="margin-top:4px;">
      <h2 class = "title">Lectures</h2>
    </div>
    <div class = "table lecture-list-table mt-4" >
      <b-table
      hover
      id="lecturelist"
      :items="lectureList"
      :fields="lectureTableColumns"
      :per-page="perPage"
      head-variant="light"
      :current-page="currentPage"
      @row-clicked = "goLectureDashboard"></b-table>
    </div>
    <div class="pagination">
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="lecturelist"
      align="right"
    ></b-pagination>
    </div>
  </div>
</template>

<script>
import api from '@oj/api'

export default {
  name: 'LectureList',
  components: {
    // Split into many components
  },
  data () {
    return {
      perPage: 10,
      currentPage: 1,
      lectureList: [
        { subject: '프로그래밍 기초와 실습', semester: '2021 spring' },
        { subject: '공학 컴퓨터 프로그래밍', semester: '2021 fall' } //test
      ],
      lectureTableColumns: [
        {
          label: 'Subject',
          key: 'title'
        },
        {
          label: 'Semester',
          key: 'semester'
        }
      ]
    }
  },
  async mounted () {
    try {
      const resp = await api.getLectureList()
      const data = resp.data.data
      this.lectureList = data.results
    } catch (err) {
    }
  },
  methods: {
    async goLectureDashboard (item) {
      await this.$router.push({
        name: 'lecture-dashboard',
        params: { courseID: item.id }
      })
    }
  },
  computed: {
    rows () {
      return this.lectureList.length
    }
  }
}
</script>

<style lang="scss" scoped>
  .font-bold {
    font-family: manrope_bold;
  }
  .lecture-list-card{
    margin:0 auto;
    width:70%;
    .lecture-list-table{
      width: 95%;
      margin: 0 auto;
    }
  }
  .table {
    width:95% !important;
    margin-left:auto;
    margin-right:auto;
  }
  .title {
    margin-bottom:0;
    color: #7C7A7B;
    display:inline;
    position:relative;
    top:36px;
    }
  div {
    &.pagination{
      margin-right: 5%;
      margin-top: 20px;
      display: flex;
      justify-content: flex-end;
    }
  }
  // Be careful of common css selector in admin/oj
</style>
