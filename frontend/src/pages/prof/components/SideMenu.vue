<template>
  <b-list-group class="prof_vertical_menu" v-show="sideMenuShow">
    <b-list-group-item class="logo">
      <img
        src="@/assets/logos/logo.png"
        style="height=35px; width=auto;"
        alt="oj admin"
      >
    </b-list-group-item>
    <b-list-group-item class="put-in">
      My Lecture
      <b-button class="put-in-button" variant="white" @click="$emit('hide')">
        <b-icon icon="chevron-double-left" style="margin-left: 45px"/>
      </b-button>
    </b-list-group-item>
    <b-list-group-item to="/">
      <b-icon icon="house"/>
      Home
    </b-list-group-item>

    <div v-for="(term,index) in lecture_term" :key="index">
      <b-list-group-item
        class="list-group-subitem"
        v-b-toggle="term.year + term.semester"
      >
        <b-icon
          :icon="click ? 'caret-right-fill' : 'caret-down-fill'"
          font-scale="1"
          style="margin-right: 8px"
        />
        {{term.year}} {{semester_name[term.semester]}}
      </b-list-group-item>

      <div v-for="(lecture,index) in lectures" :key="index">
        <div v-if="term.year === lecture.registered_year && term.semester === lecture.semester">

          <b-collapse :id="term.year + term.semester" role="tab">
            <b-list-group-item
              class="list-group-lecture"
              v-b-toggle="'inner'+lecture.id"
            >
              <b-icon
                :icon="click ? 'caret-right-fill' : 'caret-down-fill'"
                font-scale="1"
                style="margin-right: 8px"
              />
              {{lecture.title}}_{{lecture.course_code}}_{{lecture.class_number}}
            </b-list-group-item>

            <b-collapse :id="'inner'+lecture.id" role="tabpanel">
              <b-list-group-item
                :to="'/lecture/'+lecture.id+'/dashboard'"
                class="list-group-inner"
              >
                <b-icon
                  icon="record-fill"
                  font-scale="0.5"
                  style="margin-right: 8px"
                />
                Dashboard
              </b-list-group-item>
              <b-list-group-item
                :to="'/lecture/'+lecture.id+'/assignments'"
                class="list-group-inner"
              >
                <b-icon
                  icon="record-fill"
                  font-scale="0.5"
                  style="margin-right: 8px"
                />
                Assignments
              </b-list-group-item>
              <b-list-group-item
                :to="'/lecture/'+lecture.id+'/qna'"
                class="list-group-inner"
              >
                <b-icon
                  icon="record-fill"
                  font-scale="0.5"
                  style="margin-right: 8px"
                />
                Questions
              </b-list-group-item>
            </b-collapse>
          </b-collapse>
        </div>
      </div>
    </div>
  </b-list-group>
</template>

<script>
import { mapGetters } from 'vuex'
import api from '../api.js'
export default {
  name: 'SideMenu',
  data () {
    return {
      currentPath: '',
      lecture_term: [],
      click: true,
      semester_name: ['Spring', 'Summer', 'Fall', 'Winter'],
      lectures: [],
      lectureNumber: 1
    }
  },
  mounted () {
    this.currentPath = this.$route.path
    this.lectureGroup()
  },
  computed: {
    ...mapGetters(['user', 'isSuperAdmin', 'hasProblemPermission'])
  },
  methods: {
    putMenuInside () {
      this.sideMenuShow = false
    },
    lectureGroup () {
      const res = api.getCourseList() // id, limit, offset=0 
      const apilectures = res.data.data.results
      /* const apilectures = [{ // 여기서 api 불러옴
        id: 1,
        title: 'Python Programming',
        course_code: 'GDBEASDF',
        class_number: 41,
        created_by: {
          id: 1,
          username: 'minchae',
          real_name: '고민채'
        },
        registered_year: '2021',
        semester: 0
      },
      {
        id: 2,
        title: '프로그래밍 기초와 실습',
        course_code: 'GDBEAPOI',
        class_number: 40,
        created_by: {
          id: 1,
          username: 'minchae',
          real_name: '고민채'
        },
        registered_year: '2020',
        semester: 1
      }]
      */
      const registerTerm = []
      apilectures.sort((a, b) => { return a.registered_year < b.registered_year })
      apilectures.sort((a, b) => {
        if (a.registered_year === b.registered_year) {
          return a.semester < b.semester
        } else { return 0 }
      })
      apilectures.sort((a, b) => { return a.title < b.title })
      apilectures.sort((a, b) => {
        if (a.title === b.title) {
          return a.class_number < b.class_number
        } else { return 0 }
      })
      apilectures.forEach(lecture => {
        if (!({ year: lecture.registered_year, semester: lecture.semester } in registerTerm)) {
          registerTerm.push({ year: lecture.registered_year, semester: lecture.semester })
        }
      })

      this.lectures = apilectures
      this.lecture_term = registerTerm
    }
  }
}
</script>

<style scoped lang="scss">
  #prof_vertical_menu {
    flex-grow: 1;
    flex-shrink: 1;
    width: 250px;
    min-width: 200px;
    resize: horizontal;
    height: 100%;
    z-index: 1;
    background-color: white;
    .logo {
      margin: 20px 0;
      text-align: center;
    }
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
    padding: 16px 16px 16px 50px;
  }
  .list-group-lecture {
    padding: 16px 16px 16px 70px;
  }
  .list-group-inner {
    padding: 16px 16px 16px 90px;
  }
</style>
