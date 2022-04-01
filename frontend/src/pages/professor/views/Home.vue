<template>
  <div id="container">
    <side-menu @hide="showSideMenu=false" v-show="showSideMenu" :update="updateSidebar"/>
    <div style="flex: 1 1 auto">
      <div id="professor-header">
        <b-button
          variant="light"
          size="sm"
          v-b-tooltip.hover
          title="showSideMenu"
          @click="showSideMenu = !showSideMenu"
          v-if="!showSideMenu"
          class="float-left"
          >
          <b-icon-list></b-icon-list>
        </b-button>
        <b-button-group class="float-right">
          <b-button
            variant="light"
            size="sm"
            v-b-tooltip.hover
            title="KatexEditor"
            @click="showKatexEditor"
          >
            <b-icon icon="fonts"></b-icon>
          </b-button>
          <b-dropdown
            variant="light"
            size="sm"
            v-bind:text="user.username"
            >
            <b-dropdown-item
              @click="handleCommand('logout')"
              >
              Logout
            </b-dropdown-item>
          </b-dropdown>
        </b-button-group>
      </div>
      <div id="content-app">
        <transition
          name="fadeInUp"
          mode="out-in"
        >
          <router-view :key="$route.path"/>
        </transition>
      </div>

      <b-modal
        hide-footer
        centered
        size="lg"
        ref="latex-editor"
        title="Latex Editor"
      >
        <katex-editor />
      </b-modal>
    </div>
  </div>
</template>

<script>
import { types } from '@/store'
import { mapGetters } from 'vuex'
import SideMenu from '../components/SideMenu.vue'
import KatexEditor from '@professor/components/KatexEditor.vue'
import api from '../api'

export default {
  name: 'App',
  components: {
    SideMenu,
    KatexEditor
  },
  async beforeRouteEnter (to, from, next) {
    const res = await api.getProfile()
    if (!res.data.data) {
      // not login
      next({ name: 'login' })
    } else {
      next(vm => {
        vm.$store.commit(types.CHANGE_PROFILE, { profile: res.data.data })
      })
    }
  },
  data () {
    return {
      showSideMenu: true,
      version: process.env.VERSION,
      updateSidebar: 0
    }
  },
  methods: {
    async handleCommand (command) {
      if (command === 'logout') {
        await api.logout()
        await this.$router.push({ name: 'login' })
      }
    },
    showKatexEditor () {
      this.$refs['latex-editor'].show()
    }
  },
  computed: {
    ...mapGetters(['user'])
  }
}
</script>
<style lang="scss">
  a {
    background-color: transparent;
  }

  a:active, a:hover {
    outline-width: 0
  }

  img {
    border-style: none
  }

  #container {
    overflow: auto;
    font-weight: 400;
    display:flex;
    height: 100%;
    -webkit-font-smoothing: antialiased;
    background-color: #EDECEC;
    overflow-y: scroll;
    min-width: 1000px;
  }

  * {
    box-sizing: border-box;
  }

  #professor-header {
    /* padding-left: 10px;
    padding-right: 10px; */
    line-height: 50px;
    height: auto;
  }

  #content-app {
    padding-left: 15px;
    display: flex;
    flex: 1 1;
    justify-content: center;
  }

  .footer {
    margin: 15px;
    text-align: center;
    font-size: small;
  }

  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translate(0, 30px);
    }

    to {
      opacity: 1;
      transform: none;
    }
  }

  .fadeInUp-enter-active {
    animation: fadeInUp .8s;
  }

  .katex-editor {
    margin-right: 5px;
    /*font-size: 18px;*/
  }

  .list-group-item {
    padding: 1rem 2rem;
    border: 0px solid
  }

  .list-group-item-action:focus, .list-group-item-action:hover {
    background-color: #40a0ff38;
  }

  .table td, .table th {
    vertical-align: middle;
  }
</style>
