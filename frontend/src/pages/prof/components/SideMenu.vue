<template>
  <b-list-group class="prof_vertical_menu" v-show="sideMenuShow">
    <div class="logo">
      <img
        src="@/assets/logos/logo.png"
        style="height=35px; width=auto;"
        alt="oj admin"
      >
    </div>
    <div class="put-in">
      My Lecture
      <b-button class="put-in-button" variant="white" @click="$emit('hide')">
        <b-icon icon="chevron-double-left"/>
      </b-button>
    </div>
    <b-list-group-item to="/">
      <b-icon
        icon="journal-text"
        font-scale="1.25"
        style="margin-right: 8px"
      />
      Dashboard
    </b-list-group-item>
    <div v-for="(lecture1,index) in lectures" :key="index">
      <div v-if="lecture1.registered_year===thisyear">

        <b-collapse id="lecture" role="tab">
          <b-list-group-item
            class="list-group-subitem"
            v-b-toggle.lecture_title
          >
          <b-icon icon="caret-down-fill"/>
          {{lecture1.registered_year}} {{lecture1.semester}}
          </b-list-group-item>
        </b-collapse>

        <b-collapse id="lecture_title" role="tab">
          <div v-for="(lecture2, index) in lectures.lecture_title" :key="index">
            <b-list-group-item
              class="list-group-subitem"
              v-b-toggle.inner
            >
            <b-icon icon="caret-down-fill" />
            {{lecture_name}}
            </b-list-group-item>
          </div>
        </b-collapse>
        <b-collapse id="inner" role="tabpanel">
          <b-list-group-item
            to="/lecture/1/dashboard"
            class="list-group-subitem"
          >
            Lecture Dashboard
          </b-list-group-item>
          <b-list-group-item
            to="/lecture/1/assignment"
            class="list-group-subitem"
          >
            Assignments
          </b-list-group-item>
          <b-list-group-item
            to="/lecture/1/qna"
            class="list-group-subitem"
          >
            QnA
          </b-list-group-item>
        </b-collapse>
      </div>
<!--
      <b-collapse id="lecture_title">
        <b-list-group-item>
        </b-list-group-item`
        {{lecture.title}}
      </b-collapse>

      <div v-for="(lecture,id) of lecture_list" :key="id">
        <b-list-group-item
          class="list-group-subitem"
        >
          {{lecture}}
          <b-collapse>
            <b-list-group-item>
            </b-list-group-item>
          </b-collapse>
        </b-list-group-item>
      </div>
-->
    </div>
    <b-list-group-item href="#" role="tab" v-b-toggle.general>
      <b-icon
        icon="grid-fill"
        font-scale="1.25"
        style="margin-right: 8px"
      />
      Lecture
    </b-list-group-item>
  </b-list-group>
</template>

<script>
import { mapGetters } from 'vuex'
// import api from '../api.js'
export default {
  name: 'SideMenu',
  data () {
    return {
      currentPath: '',
      thisyear: 2021,
      lectures: [{
        id: 1,
        title: 'Python Programming',
        course_code: 'GDBEASDF',
        class_number: 41,
        registered_year: '2021',
        semester: 'Spring'
      },
      {
        id: 2,
        title: '프로그래밍 기초와 실습',
        course_code: 'GDBEAqwe',
        class_number: 40,
        registered_year: '2020',
        semester: 'Summer'
      }],
      lectureNumber: 1
    }
    // [{ name: 'Python Programming', id: '1' }, { name: 'Intro to Database', id: '2' }, { name: 'Open Source Software Practice', id: '3' }]
  },
  async mounted () {
    // this.currentPath = this.$route.path
    // const res = await api.getCourseList()
    // const lectures = res.data.data.results
    // this.lectures = lectures.filter(lecture => lecture.created_by.username === username)
  },
  computed: {
    ...mapGetters(['user', 'isSuperAdmin', 'hasProblemPermission'])
  },
  methods: {
    putMenuInside () {
      this.sideMenuShow = false
    }
  }
}
</script>

<style scoped lang="scss">
  #prof_vertical_menu {
    flex-grow: 1;
    flex-shrink: 1;
    width: 200px;
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
      .put-in-text {
        flex: auto;
      }
      .put-in-button {
        width: 8px;
      }
    }
  }
  .list-group-subitem {
    padding: 16px 0px 16px 50px;
  }
</style>
