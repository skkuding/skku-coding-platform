<template>
  <div class="lecture-list-card font-bold">
    <div class="top-bar mb-2">
      <h2 class="title">Lectures</h2>
      <div>
        <b-button
          class="top-bar__btn"
          v-if="!saveBtnVisible"
          size="sm"
          @click="setBookmark"
        >All Lecture</b-button>
        <b-button
          class="top-bar__btn"
          v-if="saveBtnVisible"
          size="sm"
          @click="saveBookmark"
        >
          <b-icon icon="check"/> Save
        </b-button>
      </div>
    </div>
    <div class="no-lecture" v-if="!lectureList.length">No Lecture</div>
    <div class="lecture-card-list">
      <b-card
        v-for="(lecture,index) in lectureList"
        :key="index"
        style="width: 300px; margin: 35px 35px 0 0; cursor: pointer;"
      >
        <!-- @click="goAssignmentList(lecture.course.id)" -->
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
                @click="setBookmarkLecture(lecture.course.id)"
                v-if="saveBtnVisible"
              >
                <b-icon :icon="setIcon(lecture.course.id)"/>
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
    <b-modal
      v-model="showInformation"
      centered
      ok-only
      title="Lecture Registration"
    >
      If you have a lecture you are taking but you can't see it,
      press the "All Lecture" button and register the lecture you want to see. :>
    </b-modal>
  </div>
</template>

<script>
import api from '@oj/api'

export default {
  name: 'LectureList',
  components: {
  },
  data () {
    return {
      perPage: 10,
      currentPage: 1,
      lectureList: [],
      bookmarkList: [],
      bookmarkIDList: [],
      lectureTableColumns: [
        {
          label: 'Subject',
          key: 'course.title'
        },
        'Semester'
      ],
      semesters: ['Spring', 'Summer', 'Fall', 'Winter'],
      visible: '',
      backcolor: [
        '#9EC1CF', '#CC99C9', '#FEB144', '#FF6663', '#7C7A7B', '#E2E2E2'
      ],
      saveBtnVisible: false,
      showInformation: false
    }
  },
  async mounted () {
    try {
      const resp = await api.getBookmarkLectureList()
      const data = resp.data.data
      this.lectureList = data.results
      this.bookmarkList = data.results
      for (var lecture of this.bookmarkList) {
        (this.bookmarkIDList).push(lecture.course.id)
      }
      if (!(this.bookmarkList).length) {
        this.showInformation = true
      }
    } catch (err) {
    }
  },
  methods: {
    async goLectureDashboard (item) {
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
      const resp = await api.getLectureList()
      const data = resp.data.data
      this.lectureList = data.results
      this.saveBtnVisible = true
    },
    async setBookmarkLecture (courseID) {
      await api.setBookmark(courseID)
      const resp = await api.getBookmarkLectureList()
      this.bookmarkList = resp.data.data.results
      this.bookmarkIDList = []
      for (var lecture of this.bookmarkList) {
        (this.bookmarkIDList).push(lecture.course.id)
      }
    },
    saveBookmark () {
      this.$router.go()
    },
    setIcon (id) {
      return (this.bookmarkIDList).includes(id) ? 'bookmark-fill' : 'bookmark'
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
  .title {
    color: #7C7A7B;
  }
  .top-bar {
    margin: 40px 68px 0;
    display: flex;
    justify-content: space-between;
    &__btn ::v-deep {
      height: 30px;
      margin: auto 5px;
    }
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
    }
    &__cardcolor {
      height: 150px;
      border-radius: 8px 8px 0 0;
    }
    &__lectureInfo {
      padding: 30px;
    }
    &__title {
      font-size: 22px;
      display: flex;
      justify-content: space-between;
      word-break: keep-all;
    }
    &__info {
      margin-bottom: 10px;
      font-size: 14px;
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
