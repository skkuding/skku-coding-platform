<template>
  <div id="container">
    <b-overlay
      :show="overlayShow"
      bg-color="#0B232F"
      spinner-variant="primary"
      spinner-type="grow"
      spinner-small
      rounded="sm"
    >
      <b-navbar id="main-header" type="dark">
        <b-navbar-brand to="/">
          <div class="logo-img">
            <img src="@/assets/logos/logo.svg" alt="" />
          </div>
        </b-navbar-brand>

        <b-navbar-nav
          v-if="$route.name && $route.name.indexOf('contest') != -1"
        >
          <b-nav-item to="/contest">Contests</b-nav-item>
          <b-nav-item>
            <b-icon icon="chevron-right" />
          </b-nav-item>
          <b-nav-item :to="'/contest/' + this.contestID">{{
            problem.contest_name || this.contest_title /* problem bank일 경우 contest_name이 없음 */
          }}</b-nav-item>
          <b-nav-item>
            <b-icon icon="chevron-right" />
          </b-nav-item>
          <b-nav-item to="#" active>{{ problem.title }}</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav
          v-else-if="$route.name && $route.name.indexOf('assignment') != -1"
        >
          <b-nav-item @click="goAssignmentList">Assignment</b-nav-item>
          <b-nav-item>
            <b-icon icon="chevron-right" />
          </b-nav-item>
          <b-nav-item @click="goAssignmentDetail">{{
            this.assignment_name
          }}</b-nav-item>
          <b-nav-item>
            <b-icon icon="chevron-right" />
          </b-nav-item>
          <b-nav-item active>{{ problem.title }}</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav v-else>
          <b-nav-item>
            <b-icon icon="chevron-right" />
          </b-nav-item>
          <b-nav-item to="#" active>{{ problem.title }}</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown v-if="!isAuthenticated" no-caret right>
            <template slot="button-content">
              <b-icon icon="person" scale="1.5" />
            </template>
            <b-dropdown-item @click="handleBtnClick('login')"
              >Sign In</b-dropdown-item
            >
            <b-dropdown-item @click="handleBtnClick('register')"
              >Register</b-dropdown-item
            >
          </b-nav-item-dropdown>
          <b-nav-item-dropdown v-else no-caret right>
            <template slot="button-content">
              <b-icon icon="person" scale="1.5" />
            </template>
            <b-dropdown-item v-if="isAdminRole" @click="openWindow('/admin/')"
              >Management</b-dropdown-item
            >
            <b-dropdown-item v-else v-b-modal.setting>Setting</b-dropdown-item>
            <b-dropdown-item to="/logout">Sign Out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-navbar>
      <b-modal
        v-model="modalVisible"
        hide-footer
        centered
        modal-class="modal-med"
      >
        <component :is="modalStatus.mode" v-if="modalVisible" />
      </b-modal>
      <b-modal
        id="setting"
        size="xl"
        hide-footer
        centered
        modal-class="modal-med modal-big"
      >
        <profileSetting></profileSetting>
      </b-modal>

      <b-navbar id="inner-header" type="dark">
        <b-navbar-nav>
          <b-nav-item class="menu-icon" active>
            <b-icon icon="list" scale="1.4" v-b-toggle.sidebar />
          </b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav>
          <b-nav-item to="#" class="active-link problem-title" active>
            {{ problem.title }}
          </b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-nav-item v-if="statusVisible">
            <template>
              <div @click.stop="onMySubmissionClicked">
                <b-badge class="statusBadge" variant="light">
                  <b-icon
                    id="badgeIcon"
                    icon="circle-fill"
                    :class="[submissionStatus.color]"
                    scale="0.9"
                  />
                  {{ submissionStatus.text }}
                </b-badge>
              </div>
            </template>
          </b-nav-item>
          <b-nav-item v-else-if="problem.my_status === 0">
            <b-badge class="statusBadge" variant="light">
              <b-icon
                id="badgeIcon"
                icon="circle-fill"
                class="green"
                scale="0.9"
              />
              You have solved the problem
            </b-badge>
          </b-nav-item>
          <b-nav-item
            v-else-if="
              this.contestID && !OIContestRealTimePermission && submissionExists
            "
          >
            <b-badge class="statusBadge" variant="light">
              <b-icon
                id="badgeIcon"
                icon="circle-fill"
                class="green"
                scale="0.9"
              />
              You have submitted a solution
            </b-badge>
          </b-nav-item>
          <b-nav-item v-if="captchaRequired">
            <img :src="captchaSrc" id="captcha-img" />
            <b-button @click="getCaptchaSrc">Refresh</b-button>
            <b-form-input v-model="captchaCode" id="captcha-code" />
          </b-nav-item>
          <b-nav-item>
            <b-button
              v-b-tooltip.hover
              class="btn-reset"
              title="Click to reset your code"
              @click="onResetToTemplate"
              data-cy="button-reset"
            >
              <b-icon icon="arrow-clockwise" scale="1.1" />
            </b-button>
          </b-nav-item>
          <!-- <b-nav-item>
            <b-button class="btn">
              <b-icon icon="play" scale="1.4"/>
              Run
            </b-button>
          </b-nav-item> -->
          <b-nav-item>
            <b-button
              class="btn-submit"
              :disabled="(contestID && problemSubmitDisabled) || submitted"
              @click="submitCode"
              data-cy="button-submit"
            >
              <span>Submit</span>
            </b-button>
          </b-nav-item>
          <b-nav-item>
            <b-dropdown
              split
              class="dropdown"
              data-cy="toggle-language"
              :text="language"
              @change="onChangeLang"
            >
              <b-dropdown-item
                v-for="(lang, index) of problem.languages"
                :key="index"
                @click="() => onChangeLang(lang)"
                data-cy="select-langauge"
              >
                {{ lang }}
              </b-dropdown-item>
            </b-dropdown>
          </b-nav-item>
          <b-nav-item>
            <b-dropdown
              split
              class="dropdown"
              :text="theme"
              @change="onChangeTheme"
            >
              <b-dropdown-item
                v-for="(theme, index) of theme_list"
                :key="index"
                @click="() => onChangeTheme(theme)"
              >
                {{ theme }}
              </b-dropdown-item>
            </b-dropdown>
          </b-nav-item>
        </b-navbar-nav>
      </b-navbar>

      <b-row id="problem-container" ref="container">
        <vue-resizable
          active="r"
          :fit-parent="true"
          :width="`50vw`"
          :min-width="200"
          :max-width="problemWidth - 200"
          :disable-attributes="['h']"
        >
          <b-col id="problem-description">
            <div class="description-io">
              <h2>Description</h2>
              <p v-dompurify-html="problem.description" v-katex:auto></p>
              <div class="blank-line"></div>
              <h2>Input</h2>
              <p v-dompurify-html="problem.input_description" v-katex:auto></p>
              <h2>Output</h2>
              <p v-dompurify-html="problem.output_description" v-katex:auto></p>
              <div class="blank-line"></div>
            </div>

            <div v-for="(sample, index) of problem.samples" :key="index">
              <h2>
                Sample Input {{ index + 1 }}
                <a v-clipboard:copy="sample.input">
                  <b-icon
                    id="clipboard1"
                    icon="clipboard"
                    class="copy-icon"
                    scale="0.8"
                  />
                </a>
                <b-tooltip target="clipboard1" placement="top" triggers="hover">
                  Copy
                </b-tooltip>
              </h2>
              <pre class="sample-io">{{ sample.input }}</pre>
              <h2>Sample Output {{ index + 1 }}</h2>
              <pre class="sample-io">{{ sample.output }}</pre>
              <div class="blank-line"></div>
            </div>

            <div v-if="problem.hint">
              <h2>Hint</h2>
              <p v-dompurify-html="problem.hint" v-katex:auto></p>
            </div>
            <Table
              :items="problemInfo"
              :fields="problemInfoField"
              lightStyle
            >
              <template v-slot:time_limit="data">
                {{data.row.time_limit}}
              </template>
              <template v-slot:memory_limit="data">
                {{data.row.memory_limit}}
              </template>
            </Table>
          </b-col>
        </vue-resizable>
        <b-col id="console">
          <b-row id="editor">
            <CodeMirror
              ref="codemirror"
              :value.sync="code"
              :language="language"
              :theme="theme"
              :key="$route.fullPath"
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
          <ProblemSidebar
            ref="sidebar"
            :hide="hide"
            :contestID="contestID"
            :problemID="problemID"
            :bank="bank"
            v-if="renderSidebar"
          />
        </template>
      </b-sidebar>
    </b-overlay>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { types } from '@/store'
import CodeMirror from '@oj/components/CodeMirror.vue'
import storage from '@/utils/storage'
import { FormMixin } from '@oj/components/mixins'
import {
  JUDGE_STATUS,
  CONTEST_STATUS,
  buildProblemCodeKey
} from '@/utils/constants'
import api from '@oj/api'
import ProblemSidebar from './ProblemSidebar.vue'
import moment from 'moment'
import register from '@oj/views/user/Register'
import login from '@oj/views/user/Login'
import profileSetting from '@oj/views/user/ProfileSetting'
import Table from '@oj/components/Table.vue'
import VueResizable from 'vue-resizable'

export default {
  name: 'ProblemDetails',
  components: {
    CodeMirror,
    ProblemSidebar,
    login,
    register,
    profileSetting,
    Table,
    VueResizable
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
      courseID: '',
      bank: false,
      renderSidebar: false,
      assignmentID: '',
      assignment_name: '',
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
        io_mode: { io_mode: 'Standard IO' }
      },
      problemInfo: [],
      problemInfoField: [
        {
          key: 'time_limit',
          label: 'Time Limit'
        },
        {
          key: 'memory_limit',
          label: 'Memory Limit'
        }
      ],

      // CodeMirror
      code: '',
      language: 'C++',
      theme: 'material',
      theme_list: ['solarized', 'monokai', 'material'],

      overlayShow: false,
      problemWidth: undefined
    }
  },
  async mounted () {
    this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, { menu: false })
    this.overlayShow = true
    await this.init()
    this.overlayShow = false
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
    if (this.$route.params.assignmentID) {
      this.route_name = this.$route.name
      await this.getAssignmentProblems()
      const res = await this.$store.dispatch('getCourseAssignment')
      this.changeDomTitle({ title: res.data.data.title })
      const data = res.data.data
      this.assignment_name = data.title
    }
    window.addEventListener('resize', this.updateProblemWidth)
  },
  methods: {
    ...mapActions(['changeDomTitle', 'changeModalStatus']),
    async init () {
      this.contestID = this.$route.params.contestID
      this.problemID = this.$route.params.problemID
      this.assignmentID = this.$route.params.assignmentID
      this.courseID = this.$route.params.courseID
      const route = this.$route.name
      var res

      if (route === 'contest-problem-details') {
        const res2 = await api.getContest(this.contestID)
        this.bank = res2.data.data.is_bank
        this.contest_title = res2.data.data.title
        if (!this.bank) {
          res = await api.getContestProblem(this.problemID, this.contestID)
        } else {
          res = await api.getProblemBankContestProblem(this.contestID, this.problemID)
        }
      } else if (route === 'lecture-assignment-problem-details') {
        res = await api.getCourseAssignmentProblem(
          this.assignmentID,
          this.problemID
        )
      } else {
        res = await api.getProblem(this.problemID)
      }
      this.renderSidebar = true

      const problem = res.data.data
      this.changeDomTitle({ title: problem.title })

      const res2 = await api.submissionExists(problem.id)
      this.submissionExists = res2.data.data

      problem.languages = problem.languages.sort()
      this.problem = problem
      const problemInfo = {}
      this.$set(problemInfo, 'time_limit', problem.time_limit + ' ms')
      this.$set(problemInfo, 'memory_limit', problem.memory_limit + ' MB')
      this.problemInfo.pop()
      this.problemInfo.push(problemInfo)

      let precode = storage.get(buildProblemCodeKey(this.problemID, this.contestID))

      // For Backward compatibility before Github pr #272
      if (precode && typeof precode.code === 'string') {
        storage.remove(buildProblemCodeKey(this.problemID, this.contestID))
        precode = null
      }

      if (precode) {
        this.language = precode.language
        this.code = precode.code[this.language]
        this.theme = precode.theme
        this.$refs.codemirror.editor.setOption('theme', this.theme)
      } else {
        this.code = ''
        this.language = 'C++'
        this.theme = 'material'
      }

      if (this.code === '' && !precode) {
        const userId = this.user.username
        let preferredLanguage = problem.languages[0]
        const res3 = await api.getUserInfo(userId)

        const lang = res3.data.data?.language
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
      const res = await this.$store.dispatch(this.bank ? 'getProblemBankContestProblems' : 'getContestProblems')
      if (this.isAuthenticated) {
        if (
          this.contestRuleType === 'ACM' ||
          this.OIContestRealTimePermission
        ) {
          this.addStatusColumn(this.ACMTableColumns, res.data.data)
        }
      }
    },
    async getAssignmentProblems () {
      await this.$store.dispatch('getCourseAssignmentProblemList')
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
    async onResetToTemplate () {
      const isConfirmed = await this.$bvModal.msgBoxConfirm(
        'Are you sure you want to reset your code?'
      )
      if (isConfirmed) {
        const template = this.problem.template
        if (template && template[this.language]) {
          this.code = template[this.language]
        } else {
          this.code = ''
        }
      }
    },
    // when language dropdown changed
    onChangeLang (newLang) {
      const sstorage = this.getstorage()
      sstorage.code[this.language] = this.code
      storage.set(buildProblemCodeKey(this.problemID, this.contestID), sstorage)

      this.language = newLang
      sstorage.language = newLang
      storage.set(buildProblemCodeKey(this.problemID, this.contestID), sstorage)
      if (sstorage.code[newLang]) {
        this.code = sstorage.code[newLang]
      } else {
        if (this.problem.template[newLang]) {
          this.code = this.problem.template[newLang]
        } else {
          this.code = ''
        }
      }
    },
    // when theme dropdown changed
    onChangeTheme (newTheme) {
      const sstorage = this.getstorage()
      this.theme = newTheme
      sstorage.theme = newTheme
      storage.set(buildProblemCodeKey(this.problemID, this.contestID), sstorage)
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
      const sstorage = this.getstorage()

      sstorage.code[this.language] = this.code
      storage.set(buildProblemCodeKey(this.problemID, this.contestID), sstorage)
      this.submissionId = ''
      this.result = { result: 9 }
      this.submitting = true
      const data = {
        problem_id: this.problem.id,
        language: this.language,
        code: this.code,
        contest_id: this.contestID,
        assignment_id: this.assignmentID
      }
      if (this.bank) {
        delete data.contest_id
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
      if (!this.OIContestRealTimePermission) {
        if (this.submissionExists) {
          const isConfirmed = await this.$bvModal.msgBoxConfirm(
            'You have submission in this problem, sure to cover it?'
          )
          if (isConfirmed) {
            await submitFunc(data, false)
          } else {
            this.submitting = false
          }
        } else {
          await submitFunc(data, false)
        }
      } else {
        await submitFunc(data, true)
      }
    },
    async onMySubmissionClicked () {
      await this.$refs.sidebar.onMySubmissionClicked({ ID: this.submissionId })
      await this.$nextTick()
      this.$refs.sidebar.codemirror_key += 1
    },
    async goAssignmentList () {
      await this.$router.push({
        name: 'lecture-assignment',
        params: {
          courseID: this.$route.params.courseID
        }
      })
    },
    async goAssignmentDetail () {
      await this.$router.push({
        name: 'lecture-assignment-detail',
        params: {
          courseID: this.$route.params.courseID,
          assignmentID: this.$route.params.assignmentID
        }
      })
    },
    getstorage () {
      const getstorage = storage.get(buildProblemCodeKey(this.problemID, this.contestID))
      const sstorage = getstorage || {
        code: {},
        language: this.language,
        theme: this.theme
      }
      return sstorage
    },
    updateProblemWidth () {
      this.problemWidth = this.$refs.container.clientWidth
    }
  },
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'contestRuleType',
      'OIContestRealTimePermission'
    ]),
    ...mapGetters([
      'problemSubmitDisabled',
      'contestRuleType',
      'OIContestRealTimePermission',
      'contestStatus'
    ]),
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
        return {
          name: 'contest-submission-list',
          query: { problemID: this.problemID }
        }
      } else {
        return {
          name: 'submission-list',
          query: { problemID: this.problemID }
        }
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
    const sstorage = this.getstorage()
    sstorage.code[this.language] = this.code
    storage.set(buildProblemCodeKey(this.problem._id, from.params.contestID), sstorage)
    next()
  },
  beforeRouteUpdate (to, from, next) {
    const sstorage = this.getstorage()
    sstorage.code[this.language] = this.code
    storage.set(buildProblemCodeKey(from.params.problemID, from.params.contestID), sstorage)
    next()
  },
  watch: {
    async $route () {
      this.statusVisible = false
      this.code = ''
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
    window.removeEventListener('resize', this.updateProblemWidth)
  }
}
</script>

<style lang="scss" scoped>
@font-face {
  font-family: "Manrope";
  src: url("../../../../fonts/Manrope-Bold.ttf");
}

$main-header-height: 60px;
$inner-header-height: 58px;

* {
  font-family: "Manrope", sans-serif;
}

#container {
  display: flex;
  flex-flow: column;
  height: 100vh;
}

#main-header {
  background: #0b232f;
  height: #{$main-header-height};
}

.logo-img {
  display: block;
  width: 31px;
  height: 36px;
  filter: invert(100%) sepia(92%) saturate(0%) hue-rotate(62deg)
    brightness(110%) contrast(101%);
}

#inner-header {
  height: #{$inner-header-height};
  padding-top: 0px;
  padding-bottom: 0px;
  padding-left: 15px;
  background: #173747;
  border-bottom: 1px solid #3b4f56;

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

  .statusBadge {
    font-size: 12px;
    padding: 6px 10px;
    color: #4f4f4f;
  }

  #badgeIcon {
    margin-right: 8px;
  }

  .yellow {
    color: #feb144;
  }
  .red {
    color: #ff6663;
  }
  .green {
    color: #9ee09e;
  }
  .blue {
    color: #9ec1cf;
  }

  .dropdown {
    min-width: 125px;
  }

  .dropdown::v-deep button {
    background: #45576c;
  }

  .dropdown::v-deep ul {
    background: #45576c;

    li a {
      color: white;
    }

    li a:hover {
      background: #2f3b49;
    }
  }
}

#problem-container {
  padding: 0;
  margin: 0;
  flex: 1 1 auto;
  flex-direction: row;
  flex-wrap: nowrap;

  #problem-description {
    background: #173747;
    border-right: 1px solid #3b4f56;
    padding-left: 20px;
    color: white;
    height: calc(100vh - #{$main-header-height} - #{$inner-header-height});
    overflow: auto;

    h2 {
      font-size: 20px;
      margin-top: 25px;
      margin-bottom: 15px;
    }

    p {
      font-size: 15px;
      // margin-bottom: 40px;
    }

    .description-io {
      @import "@/styles/tiptapview.scss";
      code {
        background-color: #0d0d0d;
        color: #fff;
      }

      pre {
        background: #24272d;
        font-family: "Manrope", monospace;
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
      background: #24272d;
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
    background: #24272d;
    height: calc(100vh - #{$main-header-height} - #{$inner-header-height});

    #editor {
      margin: 0;
      padding: 0;
      flex: 1 1 auto;
      overflow: auto;
    }

    #io {
      margin: 0;
      padding: 0;
      width: 100%;
      height: 40%;
      flex: 0 1 500px;
      border-top: 1px solid #3b4f56;
      display: flex;
      flex-flow: column;

      * {
        margin: 0;
        padding: 0;
      }

      .right-border {
        border-right: 1px solid #3b4f56;
      }

      .io-header {
        flex: 0 1 auto;
        color: #829bb5;
        border-bottom: 1px solid #3b4f56;

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
