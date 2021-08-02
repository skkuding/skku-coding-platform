<template>
  <div id="container">
    <b-navbar id="main-header" type="dark">
      <b-navbar-brand to="/">
        <div class="logo-img">
          <img src="@/assets/logos/logo.svg" alt=""/>
        </div>
      </b-navbar-brand>

      <b-navbar-nav v-if="$route.name && $route.name.indexOf('contest') != -1">
        <b-nav-item to="#">Contests</b-nav-item>
        <b-nav-item>
          <b-icon icon="chevron-right"/>
        </b-nav-item>
        <b-nav-item to="#">{{problem.contest_name}}</b-nav-item>
        <b-nav-item>
          <b-icon icon="chevron-right"/>
        </b-nav-item>
        <b-nav-item to="#" active>{{problem.title}}</b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav v-else>
        <b-nav-item>
          <b-icon icon="chevron-right"/>
        </b-nav-item>
        <b-nav-item to="#" active>{{problem.title}}</b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown v-if="!isAuthenticated" no-caret right>
          <template slot="button-content">
            <b-icon icon="person" scale="1.5"/>
          </template>
          <b-dropdown-item @click="handleBtnClick('login')">Sign In</b-dropdown-item>
          <b-dropdown-item @click="handleBtnClick('register')">Register</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown v-else no-caret right>
          <template slot="button-content">
            <b-icon icon="person" scale="1.5"/>
          </template>
          <b-dropdown-item v-if="isAdminRole" @click="openWindow('/admin/')">Management</b-dropdown-item>
          <b-dropdown-item v-else v-b-modal.setting>Setting</b-dropdown-item>
          <b-dropdown-item to="/logout">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
    <b-modal v-model="modalVisible" hide-footer centered modal-class="modal-med">
      <component
        :is="modalStatus.mode"
        v-if="modalVisible"
      />
    </b-modal>
    <b-modal id="setting" size="xl" hide-footer centered modal-class="modal-med modal-big">
      <profileSetting></profileSetting>
    </b-modal>

    <b-navbar id="inner-header" type="dark">
      <b-navbar-nav>
        <b-nav-item class="menu-icon" active>
          <b-icon icon="list" scale="1.4" v-b-toggle.sidebar/>
        </b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav>
        <b-nav-item to="#" class="active-link problem-title" active>
          {{problem.title}}
        </b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <b-nav-item v-if="statusVisible">
          <template v-if="!this.contestID || (this.contestID && OIContestRealTimePermission)">
            <Tag
              type="dot"
              :color="submissionStatus.color"
              @click.native="()=>{$refs.sidebar.onMySubmissionClicked({ID:submissionId})}"
            >
              {{ submissionStatus.text }}
            </Tag>
          </template>
          <template v-else-if="this.contestID && !OIContestRealTimePermission">
            <Tag type="dot" color="green">Submitted Succesfully</Tag>
          </template>
        </b-nav-item>
        <b-nav-item v-else-if="problem.my_status === 0">
          <Tag type="dot" color="green">You have solved the problem</Tag>
        </b-nav-item>
        <b-nav-item v-else-if="this.contestID && !OIContestRealTimePermission && submissionExists">
          <Tag type="dot" color="green">You have submitted a solution</Tag>
        </b-nav-item>
        <b-nav-item v-if="captchaRequired">
          <img :src="captchaSrc" id="captcha-img">
          <b-button @click="getCaptchaSrc">Refresh</b-button>
          <b-form-input v-model="captchaCode" id="captcha-code"/>
        </b-nav-item>
        <b-nav-item>
          <b-button v-b-tooltip.hover class="btn-reset" title="Click to reset your code" @click="onResetToTemplate">
            <b-icon icon="arrow-clockwise" scale="1.1"/>
          </b-button>
        </b-nav-item>
        <b-nav-item>
          <b-button class="btn">
            <b-icon icon="play" scale="1.4"/>
            Run
          </b-button>
        </b-nav-item>
        <b-nav-item>
          <b-button class="btn-submit"
            :disabled="(contestID && problemSubmitDisabled) || submitted"
            @click="submitCode"
          >
            <span>Submit</span>
          </b-button>
        </b-nav-item>
        <b-nav-item>
          <b-dropdown split class="dropdown" :text="language" @change="onChangeLang">
            <b-dropdown-item v-for="(lang, index) of problem.languages" :key="index"
              @click="()=>onChangeLang(lang)">
              {{lang}}
            </b-dropdown-item>
          </b-dropdown>
        </b-nav-item>
        <b-nav-item>
          <b-dropdown split class="dropdown" :text="theme" @change="onChangeTheme">
            <b-dropdown-item v-for="(theme, index) of theme_list" :key="index"
              @click="()=>onChangeTheme(theme)">
              {{theme}}
            </b-dropdown-item>
          </b-dropdown>
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>

    <b-row id="problem-container">
      <b-col id="problem-description" cols="5">
        <div class="description-io" v-katex>
          <h2>Description</h2>
          <p v-dompurify-html="problem.description"></p>
          <div class="blank-line"></div>
          <h2>Input</h2>
          <p v-dompurify-html="problem.input_description"></p>
          <h2>Output</h2>
          <p v-dompurify-html="problem.output_description"></p>
          <div class="blank-line"></div>
        </div>

        <div v-for="(sample, index) of problem.samples" :key="index">
          <h2>
            Sample Input {{index + 1}}
            <a v-clipboard:copy="sample.input">
              <b-icon id="clipboard1" icon="clipboard" class="copy-icon" scale="0.8"/>
            </a>
            <b-tooltip target="clipboard1" placement="top" triggers="hover">
              Copy
            </b-tooltip>
          </h2>
          <pre class="sample-io">{{sample.input}}</pre>
          <h2>
            Sample Output {{index + 1}}
          </h2>
          <pre class="sample-io">{{sample.output}}</pre>
          <div class="blank-line"></div>
          <b-table
            :items="[{time_limit:problem.time_limit, memory_limit:problem.memory_limit}]"
            :fields="['time_limit', 'memory_limit']"
            class="text-light"
            >
          </b-table>
        </div>

        <div v-if="problem.hint" v-katex>
          <h2>Hint</h2>
          <p v-dompurify-html="problem.hint"></p>
        </div>
      </b-col>
      <b-col id="console" cols="7">
        <b-row id="editor">
          <CodeMirror
            :value.sync="code"
            :language="language"
            :theme="theme"
          />
        </b-row>
        <!-- <b-row id="io">
          <b-row class="io-header">
            <b-col class="io-header-cell right-border">Input</b-col>
            <b-col class="io-header-cell">Output</b-col>
          </b-row>
          <b-row class="io-content">
            <b-col class="io-content-cell right-border">
              <pre></pre>
            </b-col>
            <b-col class="io-content-cell">
              <pre></pre>
            </b-col>
          </b-row>
        </b-row> -->
      </b-col>
    </b-row>
    <b-sidebar id="sidebar" no-header backdrop>
      <template #default="{ hide }">
        <ProblemSidebar ref="sidebar" :hide="hide" :contestID="contestID" :problemID="problemID"/>
      </template>
    </b-sidebar>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { types } from '@/store'
import CodeMirror from '@oj/components/CodeMirror.vue'
import storage from '@/utils/storage'
import { FormMixin } from '@oj/components/mixins'
import { JUDGE_STATUS, CONTEST_STATUS, buildProblemCodeKey } from '@/utils/constants'
import api from '@oj/api'
import ProblemSidebar from './ProblemSidebar.vue'
import moment from 'moment'
import register from '@oj/views/user/Register'
import login from '@oj/views/user/Login'
import profileSetting from '@oj/views/user/ProfileSetting'

export default {
  name: 'ProblemDetails',
  components: {
    CodeMirror,
    ProblemSidebar,
    login,
    register,
    profileSetting
  },
  mixins: [FormMixin],
  data () {
    return {
      statusVisible: false,
      captchaRequired: false,
      graphVisible: false,
      submissionExists: false,
      captchaCode: '',
      captchaSrc: '',
      contestID: '',
      problemID: '',
      submitting: false,

      submissionId: '',
      submitted: false,
      result: {
        result: 9
      },
      problem: {
        title: '',
        description: '',
        hint: '',
        my_status: '',
        template: {},
        languages: [],
        created_by: {
          username: ''
        },
        tags: [],
        io_mode: { io_mode: 'Standard IO' },
        memory_limit: '',
        time_limit: ''
      },
      // CodeMirror
      code: '',
      language: 'C++',
      theme: 'material',
      theme_list: ['solarized', 'monokai', 'material']
    }
  },
  async mounted () {
    this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, { menu: false })
    await this.init()
    if (this.$route.params.contestID) {
      this.route_name = this.$route.name
      await this.getContestProblems()
      const res = await this.$store.dispatch('getContest')
      this.changeDomTitle({ title: res.data.data.title })
      const data = res.data.data
      const endTime = moment(data.end_time)
      if (endTime.isAfter(moment(data.now))) {
        this.timer = setInterval(() => {
          this.$store.commit(types.NOW_ADD_1S)
        }, 1000)
      }
    }
  },
  methods: {
    ...mapActions(['changeDomTitle', 'changeModalStatus']),
    async init () {
      this.$Loading.start()
      this.contestID = this.$route.params.contestID
      this.problemID = this.$route.params.problemID

      const res = this.$route.name === 'problem-details'
        ? await api.getProblem(this.problemID)
        : await api.getContestProblem(this.problemID, this.contestID)

      this.$Loading.finish()
      const problem = res.data.data
      this.changeDomTitle({ title: problem.title })

      const res2 = await api.submissionExists(problem.id)
      this.submissionExists = res2.data.data

      problem.languages = problem.languages.sort()
      this.problem = problem

      if (this.code === '') {
        const userId = this.user.username
        let preferredLanguage = problem.languages[0]
        const res3 = await api.getUserInfo(userId)

        const lang = res3.data.data.language
        if (lang !== null) {
          if (problem.languages.includes(lang)) {
            preferredLanguage = lang
          }
        }
        this.language = preferredLanguage
        const template = this.problem.template
        if (template && template[this.language]) {
          this.code = template[this.language]
        }
      }
    },
    async getContestProblems () {
      const res = await this.$store.dispatch('getContestProblems')
      if (this.isAuthenticated) {
        if (this.contestRuleType === 'ACM' || this.OIContestRealTimePermission) {
          this.addStatusColumn(this.ACMTableColumns, res.data.data)
        }
      }
    },
    async handleRoute (route) {
      await this.$router.push(route)
    },
    openWindow (route) {
      window.open(route)
    },
    // User profile icon
    handleBtnClick (mode) {
      this.changeModalStatus({
        visible: true,
        mode: mode
      })
    },
    // when reset button clicked
    onResetToTemplate () {
      this.$Modal.confirm({
        content: 'Are you sure you want to reset your code?',
        onOk: () => {
          const template = this.problem.template
          if (template && template[this.language]) {
            this.code = template[this.language]
          } else {
            this.code = ''
          }
        }
      })
    },
    // when language dropdown changed
    onChangeLang (newLang) {
      if (this.problem.template[newLang] && this.code.trim() === '') {
        this.code = this.problem.template[newLang]
      }
      this.language = newLang
    },
    // when theme dropdown changed
    onChangeTheme (newTheme) {
      this.theme = newTheme
    },
    checkSubmissionStatus () {
      // Use setTimeout to avoid some problems
      if (this.refreshStatus) {
        // If the previous submission status check has not stopped, stop
        // otherwise the timeout reference will be lost and unlimited requests
        clearTimeout(this.refreshStatus)
      }
      const checkStatus = async () => {
        const id = this.submissionId
        try {
          const res = await api.getSubmission(id)
          this.result = res.data.data
          if (Object.keys(res.data.data.statistic_info).length !== 0) {
            this.submitting = false
            this.submitted = false
            clearTimeout(this.refreshStatus)
            await this.init()
          } else {
            this.refreshStatus = setTimeout(checkStatus, 2000)
          }
        } catch (err) {
          this.submitting = false
          clearTimeout(this.refreshStatus)
        }
      }
      this.refreshStatus = setTimeout(checkStatus, 2000)
    },
    async submitCode () {
      if (this.code.trim() === '') {
        this.$error('Code can not be empty')
        return
      }
      this.submissionId = ''
      this.result = { result: 9 }
      this.submitting = true
      const data = {
        problem_id: this.problem.id,
        language: this.language,
        code: this.code,
        contest_id: this.contestID
      }
      if (this.captchaRequired) {
        data.captcha = this.captchaCode
      }
      const submitFunc = async (data, detailsVisible) => {
        this.statusVisible = true
        try {
          const res = await api.submitCode(data)
          this.submissionId = res.data.data && res.data.data.submission_id
          // Regularly check status
          this.submitting = false
          this.submissionExists = true
          if (!detailsVisible) {
            this.$Modal.success({
              title: 'Success',
              content: 'Submit code successfully'
            })
            return
          }
          this.submitted = true
          this.checkSubmissionStatus()
        } catch (err) {
          this.getCaptchaSrc()
          if (err.data.data.startsWith('Captcha is required')) {
            this.captchaRequired = true
          }
          this.submitting = false
          this.statusVisible = false
        }
      }
      if (this.contestRuleType === 'OI' && !this.OIContestRealTimePermission) {
        if (this.submissionExists) {
          this.$Modal.confirm({
            title: '',
            content: '<h3>' + 'You have submission in this problem, sure to cover it?' + '<h3>',
            onOk: () => {
              // Temporarily solve the conflict between the dialog box
              // and the prompt dialog box behind (otherwise it will flash by)
              setTimeout(async () => {
                await submitFunc(data, false)
              }, 1000)
            },
            onCancel: () => {
              this.submitting = false
            }
          })
        } else {
          await submitFunc(data, false)
        }
      } else {
        await submitFunc(data, true)
      }
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'contestRuleType', 'OIContestRealTimePermission']),
    ...mapGetters(['problemSubmitDisabled', 'contestRuleType', 'OIContestRealTimePermission', 'contestStatus']),
    // for header user dropdown
    ...mapGetters(['website', 'modalStatus', 'user', 'isAdminRole']),

    contest () {
      return this.$store.state.contest.contest
    },
    contestEnded () {
      return this.contestStatus === CONTEST_STATUS.ENDED
    },
    submissionStatus () {
      return {
        text: JUDGE_STATUS[this.result.result].name,
        color: JUDGE_STATUS[this.result.result].color
      }
    },
    submissionRoute () {
      if (this.contestID) {
        return { name: 'contest-submission-list', query: { problemID: this.problemID } }
      } else {
        return { name: 'submission-list', query: { problemID: this.problemID } }
      }
    },
    modalVisible: {
      get () {
        return this.modalStatus.visible
      },
      set (value) {
        this.changeModalStatus({ visible: value })
      }
    }
  },
  beforeRouteLeave (to, from, next) {
    // Prevent constant requests after switching components
    clearInterval(this.refreshStatus)
    this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, { menu: true })
    storage.set(buildProblemCodeKey(this.problem._id, from.params.contestID), {
      code: this.code,
      language: this.language,
      theme: this.theme
    })
    next()
  },
  watch: {
    async '$route' () {
      await this.init()
    },
    contestEnded: function () {
      this.$error('Contest has ended :<')
    }
  },
  beforeDestroy () {
    if (this.contestID) {
      clearInterval(this.timer)
      this.$store.commit(types.CLEAR_CONTEST)
    }
  }
}
</script>

<style lang="scss">
  @font-face {
    font-family: 'Manrope';
    src: url("../../../../fonts/Manrope-Bold.ttf");
  }
  * {
    font-family: 'Manrope', sans-serif;
  }

  #container {
    display: flex;
    flex-flow: column;
    height: 100vh;
  }

  #main-header {
    background: #0B232F;
  }

  .logo-img {
    display:block;
    width:31px;
    height:36px;
    filter: invert(100%) sepia(92%) saturate(0%) hue-rotate(62deg) brightness(110%) contrast(101%);
  }

  #inner-header {
    height: 58px;
    padding-top: 0px;
    padding-bottom: 0px;
    padding-left: 15px;
    background: #173747;
    border-bottom: 1px solid #3B4F56;

    .menu-icon {
      margin-right: 10px;
    }

    .active-link {
      a {
        margin-top: 9px;
      }

      height: 58px;
      border-bottom: 2px solid white;
      font-size: 18px;
    }

    .dropdown {
      min-width: 125px;
    }

    /deep/ .dropdown button{
      background: #45576C;
    }

    /deep/ .dropdown ul {
      background: #45576C;

      li a {
        color: white;
      }

      li a:hover {
        background: #2F3B49;
      }
    }
  }

  #problem-container {
    padding: 0;
    margin: 0;
    flex: 1 1 auto;

    #problem-description {
      background: #173747;
      border-right: 1px solid #3B4F56;
      padding-left: 20px;
      color: white;

      h2 {
        font-size: 20px;
        margin-top: 25px;
        margin-bottom: 15px;
      }

      p {
        font-size: 15px;
        margin-bottom: 40px;
      }

      .description-io {
        @import '@/styles/tiptapview.scss';
        code {
          background-color: #0D0D0D;
          color: #FFF;
        }

        pre {
          background: #24272D;
          font-family: 'Manrope', monospace;
        }

        blockquote {
          border-left: 2px solid rgba(#fcfcfc, 0.5);
          padding-left: 1rem;
        }

        hr {
          border-top: 2px solid rgba(#fcfcfc, 0.5);
        }
      }

      .copy-icon {
        position: absolute;
        right: 17px;
      }

      .sample-io {
        min-height: 90px;
        padding: 12px;
        border-radius: 5px;
        background: #24272D;
        color: white;
      }

      .blank-line {
        margin-bottom: 70px;
      }
    }

    #captcha-img {
      height: 38px;
    }

    #captcha-code {
      display: inline-block;
      width: 150px;
    }

    #console {
      display: flex;
      padding: 0;
      flex-flow: column;
      background: #24272D;

      #editor {
        margin: 0;
        padding: 0;
        flex: 1 1 auto;
      }

      #io {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 40%;
        flex: 0 1 500px;
        border-top: 1px solid #3B4F56;
        display: flex;
        flex-flow: column;

        * {
          margin: 0;
          padding: 0;
        }

        .right-border {
          border-right: 1px solid #3B4F56;
        }

        .io-header {
          flex: 0 1 auto;
          color: #829BB5;
          border-bottom: 1px solid #3B4F56;

          .io-header-cell {
            padding: 3px 15px;
          }
        }

        .io-content {
          flex: 1 1 auto;
          color: white;

          .io-content-cell {
            padding: 10px 15px;
          }
        }
      }
    }
  }
</style>
