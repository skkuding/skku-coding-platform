<template>
  <b-list-group class="vertical_menu">
    <div class="logo">
      <img
        src="@/assets/logos/logo.png"
        style="height=35px; width=auto;"
        alt="oj admin"
      >
    </div>
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
      General
    </b-list-group-item>
    <b-collapse id="general" role="tabpanel">
      <b-list-group-item
        to="/user"
        class="list-group-subitem"
      >
        User
      </b-list-group-item>
      <b-list-group-item
        to="/announcement"
        class="list-group-subitem"
      >
        Announcement
      </b-list-group-item>
      <b-list-group-item
        to="/banner"
        class="list-group-subitem"
      >
        Banner
      </b-list-group-item>
      <b-list-group-item
        to="/conf"
        class="list-group-subitem"
      >
        System Config
      </b-list-group-item>
      <b-list-group-item
        to="/judge-server"
        class="list-group-subitem"
      >
        Judge Server
      </b-list-group-item>
      <b-list-group-item
        to="/prune-test-case"
        class="list-group-subitem"
      >
        Prune Test Case
      </b-list-group-item>
    </b-collapse>

    <b-list-group-item href="#" role="tab" v-b-toggle.problem>
      <b-icon
        icon="list"
        font-scale="1.25"
        style="margin-right: 8px"
      />
      Problem
    </b-list-group-item>
    <b-collapse id="problem" role="tabpanel">
      <b-list-group-item
        to="/problems"
        class="list-group-subitem"
      >
        Problem List
      </b-list-group-item>
      <b-list-group-item
        to="/problem/create"
        class="list-group-subitem"
      >
        Create Problem
      </b-list-group-item>
      <b-list-group-item
        to="/problem-set"
        class="list-group-subitem"
      >
        Problem Set
      </b-list-group-item>
    </b-collapse>

    <b-list-group-item href="#" role="tab" v-b-toggle.contest>
      <b-icon
        icon="trophy"
        font-scale="1.25"
        style="margin-right: 8px"
      />
      Contest
    </b-list-group-item>
    <b-collapse id="contest" role="tabpanel">
      <b-list-group-item
        to="/contest"
        class="list-group-subitem"
      >
        Contest List
      </b-list-group-item>
      <b-list-group-item
        to="/contest/create"
        class="list-group-subitem"
      >
        Create Contest
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
      currentPath: ''
    }
  },
  mounted () {
    this.currentPath = this.$route.path
  },
  computed: {
    ...mapGetters(['user', 'isSuperAdmin', 'hasProblemPermission'])
  }
}
</script>

<style scoped lang="scss">
  .vertical_menu {
    overflow: auto;
    width: 200px;
    height: 100%;
    position: fixed !important;
    z-index: 100;
    top: 0;
    bottom: 0;
    left: 0;
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
