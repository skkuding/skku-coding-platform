<template>
  <div class="flex-grow-1 mx-2">
    <b-row
      type="flex"
      cols = "1"
      id="dashboard"
    >
      <b-card title="All Course" class="admin-info drop-shadow-custom">
        <b-table
          borderless
          hover
          :fields="courseListFields"
          :items="courseList"
          :per-page="pageSize"
          :current-page="updateCurrentPage"
        >
          <template #cell(title)="data">
            <b-button
              class="bookmark__btn"
              @click="setBookmark(data.item.id)"
            >
              <b-icon :icon="setIcon(data.item.id)"/>
            </b-button>
            {{data.value + '  ( ' + data.item.course_code + '-' + data.item.class_number + ' ) '}}
          </template>
          <template #cell(semester)="data">
            {{data.item.registered_year + '-' + semesterStr[data.value]}}
          </template>
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
    </b-row>
  </div>
</template>

<script>
import api from '../../api.js'

export default {
  name: 'CourseBookmark',
  data () {
    return {
      pageSize: 10,
      currentPage: 1,
      bookmarkList: [],
      bookmarkIDList: [],
      courseList: [],
      courseListFields: [
        'title', 'semester'
      ],
      semesterStr: ['Spring', 'Summer', 'Fall', 'Winter']
    }
  },
  computed: {
  },
  async mounted () {
    try {
      const res = await api.getBookmarkCourseList(null, 250, 0)
      this.bookmarkList = res.data.data.results
      for (var course of this.bookmarkList) {
        (this.bookmarkIDList).push(course.id)
      }
      const resp = await api.getCourseList()
      this.courseList = resp.data.data.results
    } catch (err) {
    }
  },
  methods: {
    setIcon (id) {
      return (this.bookmarkIDList).includes(id) ? 'bookmark-fill' : 'bookmark'
    },
    async setBookmark (courseID) {
      await api.setBookmark(courseID)
      const resp = await api.getBookmarkCourseList(null, 250, 0)
      this.bookmarkList = resp.data.data.results
      this.bookmarkIDList = []
      for (var course of this.bookmarkList) {
        (this.bookmarkIDList).push(course.id)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .drop-shadow-custom {
    filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  }
  .bookmark {
    &__btn ::v-deep {
      background-color: transparent;
      border: transparent 1px solid;
      color: #7A7C7B;
    }
    &__btn:hover, __btn:active ::v-deep{
      background-color: transparent;
      color: #AAAAAA;
    }
  }
</style>
