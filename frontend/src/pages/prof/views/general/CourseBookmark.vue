<template>
  <div class="flex-grow-1 mx-2">
    <b-breadcrumb :items="pageLocations" class="mt-3"></b-breadcrumb>
    <b-row
      type="flex"
      cols = "1"
      id="bookmark-course-list"
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
              @click="setBookmark(data.item.id, data.item.bookmark)"
            >
              <b-icon :icon="setIcon(data.item.bookmark)"/>
            </b-button>
            {{data.value + '  ( ' + data.item.course_code + '-' + data.item.class_number + ' ) '}}
          </template>
          <template #cell(semester)="data">
            {{data.item.registered_year + '-' + semesterStr[data.value]}}
          </template>
        </b-table>
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
      courseList: [],
      courseListFields: [
        'title', 'semester'
      ],
      semesterStr: ['Spring', 'Summer', 'Fall', 'Winter'],
      pageLocations: [
        {
          text: 'Dashboard',
          to: '/dashboard'
        },
        {
          text: 'All courses'
        }
      ]
    }
  },
  computed: {
  },
  async mounted () {
    try {
      const resp = await api.getCourseList()
      this.courseList = resp.data.data.results
    } catch (err) {
    }
  },
  methods: {
    setIcon (bookmark) {
      return bookmark ? 'bookmark-fill' : 'bookmark'
    },
    async setBookmark (courseID, bookmark) {
      await api.setBookmark(courseID, !bookmark)
      this.$parent.updateSidebar += 1
    }
  }
}
</script>

<style lang="scss" scoped>
  #bookmark-course-list {
    margin: auto;
    flex:1 0;
    max-width: 1300px;
  }
  .drop-shadow-custom {
    filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  }
  .bookmark {
    &__btn ::v-deep {
      background-color: transparent;
      border: 1px solid transparent;
      color: #7A7C7B;
    }
    &__btn:hover, __btn:active ::v-deep{
      background-color: transparent;
      color: #AAAAAA;
    }
  }
</style>
