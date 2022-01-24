<template>
  <div class="lecture-list-card font-bold">
    <div class="flex justify-between mr-32">
      <page-title text="Course"/>
      <div class="my-auto h-8">
        <b-button
          v-if="!saveBtnVisible"
          size="sm"
          @click="setBookmark"
        >All Course</b-button>
        <b-button
          v-if="saveBtnVisible"
          size="sm"
          @click="saveBookmark"
        >
          <b-icon icon="check"/> Save
        </b-button>
      </div>
    </div>
    <div class="no-lecture" v-if="!lectureList.length">No Course</div>
    <div class="lecture-card-list">
      <b-card
        v-for="(lecture,index) in lectureList"
        :key="index"
        style="width: 230px; margin: 25px 25px 0 0; cursor: pointer;"
      >
        <b-card-text class="lecture-card__card">
          <div
            class="lecture-card__cardcolor"
            :style="'background-color:' + backcolor[index % 7]"
          ></div>
          <div class="lecture-card__lectureInfo">
            <div class="lecture-card__title">
              {{ lecture.course.title }}
              <b-button
                class="lecture-card__btn"
                @click="setBookmarkCourse(index, lecture.course.id, lecture.bookmark)"
                v-if="saveBtnVisible"
              >
                <b-icon :icon="setIcon(lecture.bookmark)"/>
              </b-button>
            </div>
            <div class="lecture-card__info">
              {{ lecture.course.course_code + '-' + lecture.course.class_number }}
              <span v-if="lecture.course.created_by.real_name">{{ '(' + lecture.course.created_by.real_name + ')' }} </span><br/>
              {{ lecture.course.registered_year + ' ' + getSemester(lecture.course.semester) }} <br/>
            </div>
            <div>
              <b-button
                class="lecture-card__btn mr-3"
                size="sm"
                v-b-tooltip.hover.bottomright="'Assignment'"
                :to="'lecture/' + lecture.course.id + '/assignment'">
                <b-icon icon="journal-text"/>
              </b-button>
              <b-button
                class="lecture-card__btn"
                size="sm"
                v-b-tooltip.hover.bottomright="'QnA'"
                :to="'lecture/' + lecture.course.id + '/question'">
                <b-icon icon="patch-question"/>
              </b-button>
            </div>
          </div>
        </b-card-text>
      </b-card>
    </div>
  </div>
</template>

<script>
import api from '@oj/api'
import PageTitle from '@oj/components/PageTitle.vue'

export default {
  name: 'CourseList',
  components: {
    PageTitle
  },
  data () {
    return {
      perPage: 10,
      currentPage: 1,
      lectureList: [],
      lectureTableColumns: [
        {
          label: 'Subject',
          key: 'course.title'
        },
        'Semester'
      ],
      semesters: ['Spring', 'Summer', 'Fall', 'Winter'],
      backcolor: [
        '#9EC1CF', '#CC99C9', '#FEB144', '#FF6663', '#7C7A7B', '#E2E2E2'
      ],
      saveBtnVisible: false
    }
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      try {
        const resp = await api.getBookmarkCourseList()
        const data = resp.data.data
        this.lectureList = data.results
      } catch (err) {
      }
    },
    async goCourseDashboard (item) {
      await this.$router.push({
        name: 'lecture-dashboard',
        params: { courseID: item.course.id }
      })
    },
    async goAssignmentList (courseID) {
      await this.$router.push({
        name: 'lecture-assignment',
        params: {
          courseID: courseID
        }
      })
    },
    async setBookmark () {
      const resp = await api.getCourseList()
      const data = resp.data.data
      this.lectureList = data.results
      this.saveBtnVisible = true
    },
    async setBookmarkCourse (index, courseID, bookmark) {
      await api.setBookmark(courseID, !bookmark)
      this.lectureList[index].bookmark = !bookmark
    },
    async saveBookmark () {
      this.saveBtnVisible = !this.saveBtnVisible
      await this.init()
    },
    setIcon (bookmark) {
      return bookmark ? 'bookmark-fill' : 'bookmark'
    },
    getSemester (semesterno) {
      return this.semesters[semesterno]
    }
  },
  computed: {
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
  }
  .no-lecture {
    text-align: center;
  }
  .lecture-card-list {
    display: flex;
    flex-wrap: wrap;
    margin-left: 68px;
  }
  .card-body {
    padding: 0 !important;
  }
  .lecture-card {
    &__card ::v-deep{
      color: #7C7A7B;
      cursor: default;
    }
    &__cardcolor {
      height: 135px;
      border-radius: 8px 8px 0 0;
    }
    &__lectureInfo {
      padding: 25px;
    }
    &__title {
      font-size: 16px;
      display: flex;
      justify-content: space-between;
      word-break: keep-all;
    }
    &__info {
      margin-bottom: 10px;
      font-size: 12px;
    }
    &__btn ::v-deep {
      background-color: transparent;
      color: #7A7C7B;
    }
    &__btn:hover, __btn:active ::v-deep{
      background-color: transparent;
      color: #AAAAAA;
    }
  }
</style>
