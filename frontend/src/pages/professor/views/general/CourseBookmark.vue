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
          <template #cell(course)="data">
            <b-button
              class="bookmark__btn"
              @click="setBookmark(data.index, data.item.course.id, data.item.bookmark)"
            >
              <b-icon :icon="setIcon(data.item.bookmark)"/>
            </b-button>
            {{data.item.course.title + '  ( ' + data.item.course.course_code + '-' + data.item.course.class_number + ' ) '}}
          </template>
          <template #cell()="data">
            {{data.item.course.registered_year + '-' + semesterStr[data.value]}}
          </template>
          <template #cell(option)="data">
            <icon-btn
              name="Edit"
              icon="clipboard-plus"
              v-b-modal.registerNew
              @click.native="updateCourseId(data.item.course.id)"
            />
            <icon-btn
              name="Delete"
              icon="trash"
              @click.native="deleteCourse(data.item.course.id)"
            />
          </template>
        </b-table>
      </b-card>
      <course-modal :mode="mode" :courseId="courseId" @submitCourseData="updateCourseList" :key="modalKey"/>
    </b-row>
  </div>
</template>

<script>
import api from '../../api.js'
import CourseModal from './CourseModal.vue'

export default {
  name: 'CourseBookmark',
  components: {
    CourseModal
  },
  data () {
    return {
      courseList: [],
      courseListFields: [
        {
          label: 'title',
          key: 'course'
        },
        {
          label: 'semester',
          key: 'course.semester'
        },
        'option'
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
      ],
      mode: 'edit',
      courseId: null,
      modalKey: 0
    }
  },
  computed: {
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      try {
        const resp = await api.getCourseList()
        this.courseList = resp.data.data.results
        console.log(this.courseList)
      } catch (err) {
      }
    },
    setIcon (bookmark) {
      return bookmark ? 'bookmark-fill' : 'bookmark'
    },
    async setBookmark (index, courseID, bookmark) {
      this.courseList[index].bookmark = !bookmark
      await api.setBookmark(courseID, !bookmark)
      this.$parent.updateSidebar += 1
    },
    async deleteCourse (courseId) {
      await api.deleteCourse(courseId)
      await this.init()
    },
    async updateCourseId (courseId) {
      this.courseId = courseId
      this.modalKey += 1
    },
    async updateCourseList () {
      await this.init()
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
