<template>
  <div id="sidebar-wrapper">
    <b-list-group class="prof_vertical_menu" v-show="sideMenuShow">
      <img id="coding-platform-logo" src="@/assets/logos/codingPlatformLogo.png" alt="coding-platform-logo">
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

        <div v-for="(lecture,index) in lectures" :key="index">
          <div v-if="term.registered_year === lecture.registered_year && term.semester === lecture.semester">

            <b-collapse :id="String(term.registered_year) + '-' + String(term.semester)">
              <b-list-group-item
                class="list-group-lecture"
              >
                <b-icon
                  icon="caret-right-fill"
                  font-scale="1"
                  style="margin-right: 8px; cursor:pointer"
                  v-b-toggle="'inner'+lecture.id"
                />
                <span v-b-toggle="'inner'+lecture.id">{{lecture.title}}_{{lecture.course_code}}-{{lecture.class_number}}</span>
              </b-list-group-item>

              <b-collapse :id="'inner'+lecture.id" role="tabpanel">
                <b-list-group-item
                  :to="'/lecture/'+lecture.id+'/dashboard'"
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
                  :to="'/lecture/'+lecture.id+'/assignment'"
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
                  :to="'/lecture/'+lecture.id+'/qna'"
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
    <b-button variant="light" id="put-in-button" @click="$emit('hide')">
      <b-icon-box-arrow-left>
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
      lectures: [],
      lectureNumber: 1,
      sideMenuShow: true
    }
  },
  mounted () {
    this.currentPath = this.$route.path
    this.groupLectures()
  },
  props: ['update'],
  computed: {
  },
  methods: {
    putMenuInside () {
      this.sideMenuShow = false
    },
    async groupLectures () {
      const res = await api.getCourseList() // id, limit, offset=0
      const lectures = res.data.data.results
      // Make registered term unique list
      const registeredTerms = new Set()
      lectures.forEach(lecture => {
        registeredTerms.add(JSON.stringify({
          semester: lecture.semester,
          registered_year: lecture.registered_year
        }))
      })
      this.registeredTerms = Array.from(registeredTerms).map(term =>
        JSON.parse(term)
      )
      console.log(this.registeredTerms)
      this.lectures = lectures
    }
  },
  watch: {
    'update' () {
      console.log('update sidebar')
      this.groupLectures()
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
    margin:auto;
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
  .list-group-lecture {
    padding: 5px 16px 5px 50px;
    font-size: 15px;
  }
  .list-group-inner {
    padding: 5px 16px 5px 75px;
  }
  #put-in-button {
    bottom: 0px;
    left: 0px;
    position: fixed;
  }
</style>
