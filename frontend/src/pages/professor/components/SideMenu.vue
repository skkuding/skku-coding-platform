<template>
  <div id="sidebar-wrapper">
    <b-list-group class="prof_vertical_menu" v-show="sideMenuShow">
      <img id="coding-platform-logo" src="@/assets/logos/codingPlatformLogo.png" alt="coding-platform-logo" @click="goHome">
      <b-list-group-item>
        <div style="width: 100%;height:1px;background-color: #B8B8B8;"></div>
      </b-list-group-item>
      <b-list-group-item to="/" class="list-group-subitem">
        <b-icon
          icon="house"
          style="margin-right: 8px"
        />
        Home
      </b-list-group-item>

      <div v-for="(term,index) in registeredTerms" :key="index">
        <b-list-group-item
          class="list-group-subitem"
        >
          <b-icon
            icon="caret-right-fill"
            font-scale="1"
            style="margin-right: 8px; cursor:pointer;"
            v-b-toggle="String(term.registered_year) + '-' + String(term.semester)"
          />
          <span v-b-toggle="String(term.registered_year) + '-' + String(term.semester)"> {{term.registered_year}} {{semester_name[term.semester]}} </span>
        </b-list-group-item>

        <div v-for="(course,index) in courses" :key="index">
          <div v-if="term.registered_year === course.registered_year && term.semester === course.semester">
            <b-collapse :id="String(term.registered_year) + '-' + String(term.semester)" :ref="String(term.registered_year) + '-' + String(term.semester)">
              <b-list-group-item
                class="list-group-course"
              >
                <b-icon
                  icon="caret-right-fill"
                  font-scale="1"
                  style="margin-right: 8px; cursor:pointer"
                  v-b-toggle="'inner'+course.id"
                />
                <span v-b-toggle="'inner'+course.id">{{course.title}}_{{course.course_code}}-{{course.class_number}}</span>
              </b-list-group-item>

              <b-collapse :id="'inner'+course.id" :ref="'inner'+course.id" role="tabpanel">
                <b-list-group-item
                  :to="'/course/'+course.id+'/dashboard'"
                  class="list-group-inner"
                >
                  <b-icon
                    icon="record-fill"
                    font-scale="0.5"
                    style="margin-right: 8px; vertical-align:1px"
                  />
                  Dashboard
                </b-list-group-item>
                <b-list-group-item
                  :to="'/course/'+course.id+'/assignment'"
                  class="list-group-inner"
                >
                  <b-icon
                    icon="record-fill"
                    font-scale="0.5"
                    style="margin-right: 8px; vertical-align:1px "
                  />
                  Assignments
                </b-list-group-item>
                <b-list-group-item
                  :to="'/course/'+course.id+'/qna'"
                  class="list-group-inner"
                >
                  <b-icon
                    icon="record-fill"
                    font-scale="0.5"
                    style="margin-right: 8px; vertical-align:1px"
                  />
                  Questions
                </b-list-group-item>
              </b-collapse>
            </b-collapse>
          </div>
        </div>
      </div>
    </b-list-group>
    <b-button size="sm" variant="light" id="put-in-button" @click="$emit('hide')">
      <b-icon-box-arrow-left />
    </b-button>
    <b-button size="sm" variant="primary" id="all-course-button" @click="goBookmark">
      See All Course
    </b-button>
  </div>
</template>

<script>
import api from '../api.js'
export default {
  name: 'SideMenu',
  data () {
    return {
      currentPath: '',
      registeredTerms: [],
      click: true,
      semester_name: ['Spring', 'Summer', 'Fall', 'Winter'],
      courses: [],
      courseNumber: 1,
      sideMenuShow: true
    }
  },
  mounted () {
    this.currentPath = this.$route.path
    this.groupCourses()
  },
  props: ['update'],
  computed: {
  },
  methods: {
    putMenuInside () {
      this.sideMenuShow = false
    },
    async groupCourses () {
      const res = await api.getBookmarkCourseList(null, 250, 0)
      const courses = res.data.data.results
      for (const course of courses) {
        this.courses.push(course.course)
      }
      // Make registered term unique list
      const registeredTerms = new Set()
      this.courses.forEach(course => {
        registeredTerms.add(JSON.stringify({
          semester: course.semester,
          registered_year: course.registered_year
        }))
      })
      this.registeredTerms = Array.from(registeredTerms).map(term =>
        JSON.parse(term)
      )
    },
    async goBookmark () {
      await this.$router.push({
        name: 'course-bookmark'
      })
    },
    goHome () {
      this.$router.push({
        name: 'dashboard'
      })
    }
  },
  watch: {
    'update' () {
      this.groupCourses()
    },
    '$route' () {
      this.courses.forEach(course => {
        if (String(course.id) === String(this.$route.params.courseId)) {
          const id = String(course.registered_year) + '-' + String(course.semester)
          for (const courseRef of this.$refs[id]) {
            courseRef.show = true
          }
          this.$refs['inner' + course.id][0].show = true
        }
      })
    }
  }
}
</script>

<style scoped lang="scss">
  #sidebar-wrapper {
    min-height: 100vh;
    width: 15%;
    min-width: 270px;
    height: 100%;
    top: 0px;
    position: sticky;
    padding-bottom: 150px;
    background-color: white;
    word-break: break-all;
    overflow-y: scroll;
  }
  #coding-platform-logo {
    display: block;
    margin: auto;
    cursor: pointer;
  }
  #prof_vertical_menu {
    flex-grow: 1;
    flex-shrink: 1;
    width: 250px;
    min-width: 200px;
    resize: horizontal;
    height: 100%;
    z-index: 1;
    background-color: white;
    .put-in {
      display: flex;
      flex-direction: row;
      /* .put-in-text {
        flex: auto;
      }
      .put-in-button {
        width: 8px;
      } */
    }
  }
  .list-group-subitem {
    padding: 10px 16px 10px 30px;
    font-size: 15px;
  }
  .list-group-course {
    padding: 5px 16px 5px 50px;
    font-size: 15px;
  }
  .list-group-inner {
    padding: 5px 16px 5px 75px;
  }
  #put-in-button {
    bottom: 0px;
    left: 10px;
    position: fixed;
  }
  #all-course-button {
    bottom: 0px;
    left: 46px;
    position: fixed;
  }
</style>
