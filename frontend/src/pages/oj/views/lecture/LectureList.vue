<template>
  <div class="lecture-list-card font-bold">
    <div class="top-bar mb-2">
      <h2 class="title">Lectures</h2>
    </div>
    <div class="lecture-card-list">
      <b-card
        v-for="(lecture,index) in lectureList"
        :key="index"
        style="width: 300px; margin: 35px 35px 0 0;"
      >
        <b-card-text class="lecture-card__card">
          <div
            class="lecture-card__cardcolor"
            :style="'background-color:' + backcolor[index % 7]"
          ></div>
          <div class="lecture-card__lectureInfo">
            <div class="lecture-card__title">
              {{ lecture.course.title }}
              <b-buttons
                class="lecture-card__btn"
                @click="changeVisibleState"
              >
                <b-icon icon="bookmark-fill"/>
              </b-button>
              <!-- <b-button v-else><b-icon icon="heart"/></b-button> -->
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

export default {
  name: 'LectureList',
  components: {
    // Split into many components
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
      visible: '',
      backcolor: [ //
        '#8DC63F', '#9EC1CF', '#CC99C9', '#FEB144', '#FF6663', '#7C7A7B', '#E2E2E2'
      ]
    }
  },
  async mounted () {
    try {
      const resp = await api.getLectureList()
      const data = resp.data.data
      this.lectureList = data.results
      // 백엔드에서 구현하면 lecture visible 가져다 쓰기
      this.visible = 'true'
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
    getSemester (semesterno) {
      return this.semesters[semesterno]
    },
    changeVisibleState () {
      return this.visible === 'true' ? 'false' : 'true'
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
    margin-top: 40px;
    margin-left: 68px;
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
      /* background-color: #9EC1CF; */
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
