<template>
  <b-list-group class="prof_vertical_menu" v-show="sideMenuShow">
    <div class="logo">
      <img
        src="@/assets/logos/logo.png"
        style="height=35px; width=auto;"
        alt="oj admin"
      >
    </div>
    <b-button @click="$emit('hide')">
      Put in
    </b-button>
    <b-list-group-item to="/">
      <b-icon
        icon="journal-text"
        font-scale="1.25"
        style="margin-right: 8px"
      />
      Dashboard
    </b-list-group-item>

    <b-list-group-item href="#" role="tab" v-b-toggle.general>
      <b-icon
        icon="grid-fill"
        font-scale="1.25"
        style="margin-right: 8px"
      />
      Lecture
    </b-list-group-item>
    <b-collapse id="general" role="tab">
      <b-list-group-item
        class="list-group-subitem"
        v-b-toggle.lecture
      >
        Introduction to Database
      </b-list-group-item>
      <b-collapse id="lecture" role="tabpanel">
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
      <b-list-group-item
        to="/lecture/2"
        class="list-group-subitem"
      >
        Computer Programming
      </b-list-group-item>
      <b-list-group-item
        to="/lecture/3"
        class="list-group-subitem"
      >
        Python Programming
      </b-list-group-item>
      <b-list-group-item
        to="/lecture/4"
        class="list-group-subitem"
      >
        Introduction to Algorithms
      </b-list-group-item>
    </b-collapse>
  </b-list-group>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'SideMenu',
  data () {
    return {
      currentPath: '',
      lectures: [{ name: 'Python Programming', id: '1' }, { name: 'Intro to Database', id: '2' }, { name: 'Open Source Software Practice', id: '3' }]
    }
  },
  mounted () {
    this.currentPath = this.$route.path
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
  }
  .list-group-subitem {
    padding: 16px 0px 16px 50px;
  }
</style>
