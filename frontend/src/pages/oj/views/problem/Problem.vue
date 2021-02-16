<template>
  <div id="container">
    <b-navbar id="main-header" type="dark">
      <b-navbar-brand>
        <svg width="31" height="36" viewBox="0 0 31 36" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M5.95705 30.9543C5.25411 30.3395 4.60951 29.661 4.03149 28.9275C0.846475 25.3548 -2.79105 15.9833 3.26253 7.48047C5.76085 3.97427 9.34617 1.61518 12.9062 0.657934C21.2112 -1.57933 27.5939 2.35249 30.5147 5.51377C30.8311 5.86661 30.7948 6.31596 30.5463 6.52323C30.184 6.82701 29.8581 6.66879 29.1223 6.45677C28.0991 6.1408 27.0202 6.04746 25.9579 6.18305C23.5181 6.49949 21.4043 8.75732 21.697 11.917C21.9644 14.803 24.189 16.8868 25.7522 18.2633C31.2378 23.1033 29.4024 28.2756 28.9546 29.4132C27.4373 33.2754 23.5498 36 18.512 36C16.4171 36 13.3935 35.4573 10.3525 33.5302C10.2338 33.4779 10.1183 33.3213 10.2623 33.0555C10.4949 32.4685 11.4648 30.7549 11.884 30.2597C13.3951 32.0001 15.9456 33.6504 18.7794 33.7532C22.6511 33.8956 25.1462 31.7992 26.0576 29.1395C27.0844 26.1507 25.9927 23.1049 23.0972 20.3566C20.6021 17.9833 18.3775 15.795 18.2477 12.0373C18.0895 7.22415 22.2729 4.36508 26.1588 4.55653C26.2775 4.55653 20.7793 0.600974 13.7147 2.9569C11.1894 3.79431 8.93975 5.30338 7.207 7.32225C7.15726 7.37484 7.12955 7.44448 7.12955 7.51686C7.12955 7.58925 7.15726 7.65889 7.207 7.71147C7.31776 7.8697 9.7164 11.2161 9.7164 11.2161L5.37954 10.2209C5.32917 10.2091 5.27644 10.2128 5.22819 10.2315C5.17994 10.2501 5.13841 10.2828 5.10898 10.3253C3.73245 12.6986 1.70404 19.5591 6.23394 25.8089C6.23394 25.8089 10.0898 19.6984 17.7493 19.1778C18.2588 19.1446 18.1939 19.3266 17.8601 19.4484C11.0186 21.9625 8.31772 26.9798 6.57411 30.8404C6.55004 30.8978 6.51204 30.9483 6.46355 30.9874C6.41506 31.0265 6.35761 31.0528 6.29637 31.0641C6.23514 31.0754 6.17206 31.0713 6.11282 31.0521C6.05358 31.033 6.00004 30.9993 5.95705 30.9543Z" fill="white"/>
        </svg>
      </b-navbar-brand>

      <b-navbar-nav v-if="$route.name.indexOf('contest') != -1">
        <b-nav-item to="#">Contests</b-nav-item>
        <b-nav-item>
          <b-icon icon="chevron-right"/>
        </b-nav-item>
        <b-nav-item to="#">SKKU 코딩 플랫폼 모의 대회</b-nav-item>
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
        <b-nav-item>
          <b-icon icon="person" scale="1.5"/>
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>

    <b-navbar id="inner-header" type="dark">
      <b-navbar-nav>
        <b-nav-item class="menu-icon" active>
          <b-icon icon="list" scale="1.8" shift-v="-3" v-b-toggle.sidebar/>
        </b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav>
        <b-nav-item to="#" class="active-link" active>
          {{problem.title}}
        </b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto">
        <b-nav-item>
          <b-button>
            <b-icon icon="arrow-clockwise" scale="1.1" shift-v="-2"/>
          </b-button>
        </b-nav-item>
        <b-nav-item>
          <b-button variant="success">
            <b-icon icon="play" scale="1.4" shift-v="-1.5"/>
            Run
          </b-button>
        </b-nav-item>
        <b-nav-item>
          <b-button variant="primary">
            Submit
          </b-button>
        </b-nav-item>
        <b-nav-item>
          <b-dropdown split id="language-dropdown" :text="language">
            <b-dropdown-item v-for="(lang, index) of problem.languages" :key="index"
              @click="()=>onChangeLang(lang)">
              {{lang}}
            </b-dropdown-item>
          </b-dropdown>
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>

    <b-row id="problem-container">
      <b-col id="problem-description" cols="5">
        <h2>Description</h2>
        <p v-html=problem.description></p>
        <h2>Input</h2>
        <p v-html=problem.input_description></p>
        <h2>Output</h2>
        <p v-html=problem.output_description></p>

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
        </div>

        <div v-if="problem.hint">
          <p class="title">{{$t('m.Hint')}}</p>
          <Card dis-hover>
            <div class="content" v-html=problem.hint></div>
          </Card>
        </div>
      </b-col>
      <b-col id="console" cols="7">
        <b-row id="editor">
        </b-row>
        <b-row id="io">
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
        </b-row>
      </b-col>
    </b-row>
    <b-sidebar id="sidebar" no-header backdrop>
      <template #default="{ hide }">
        <div id="sidebar-container">
          <b-container>
            <b-row class="sidebar-row bottom-border">
              <b-icon icon="x" scale="2.2" @click="hide"/>
            </b-row>
            <b-row class="sidebar-row bottom-border" v-if="$route.name.indexOf('contest') != -1">
              <h2>
                <b-icon class="sidebar-icon" icon="hash" scale="1.3" shift-v="1"/>
                Problem List
              </h2>
              <ul id="problem-list">
                <li v-for="(contestProblem, index) of contestProblems" :key="index"
                  @click="()=>goContestProblem(contestProblem._id)">
                  {{contestProblem.title}}
                </li>
              </ul>
            </b-row>
            <b-row class="sidebar-row">
              <h2 v-b-modal.clarifications-modal>
                <b-icon class="sidebar-icon" icon="question-circle" scale="1.2"/>
                Clarification
              </h2>
              <h2 v-b-modal.my-submissions-modal>
                <b-icon class="sidebar-icon" icon="person" scale="1.2"/>
                My Submissions
              </h2>
              <h2 v-b-modal.all-submissions-modal>
                <b-icon class="sidebar-icon" icon="people" scale="1.2"/>
                All Submissions
              </h2>
              <h2>
                <b-icon class="sidebar-icon" icon="bar-chart-line" scale="1.2"/>
                Standings
              </h2>
            </b-row>
          </b-container>
        </div>
      </template>
    </b-sidebar>

    <div id="modal-wrapper">
      <b-modal id="clarifications-modal" centered hide-backdrop hide-footer>
        <template #modal-header="{ close }">
          <div class="modal-title-close">
            <h1>Clarifications</h1>
            <b-icon icon="x" scale="3" shift-v="-3" @click="close()"/>
          </div>
        </template>
        <div id="clarifications-table">
          <b-table :items="clarifications"></b-table>
        </div>
      </b-modal>
      <b-modal id="my-submissions-modal" centered hide-backdrop hide-footer>
        <template #modal-header="{ close }">
          <div class="modal-title-close">
            <h1>My Submissions</h1>
            <b-icon icon="x" scale="3" shift-v="-3" @click="close()"/>
          </div>
        </template>
        <div id="my-submissions-table">
          <b-table class="align-center" :items="my_submissions"></b-table>
        </div>
      </b-modal>

      <b-modal id="all-submissions-modal" centered hide-backdrop hide-footer>
        <template #modal-header="{ close }">
          <div class="modal-title-close">
            <h1>All Submissions</h1>
            <b-icon icon="x" scale="3" shift-v="-3" @click="close()"/>
          </div>
        </template>
        <div id="all-submissions-table">
          <b-table class="align-center" :items="all_submissions"></b-table>
        </div>
      </b-modal>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import { types } from '../../../../store'
import storage from '@/utils/storage'
import { FormMixin } from '@oj/components/mixins'
import { JUDGE_STATUS, CONTEST_STATUS, buildProblemCodeKey } from '@/utils/constants'
import api from '@oj/api'
export default {
  name: 'Problem Details',
  components: {
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
      code: '',
      language: 'C++',
      theme: 'solarized',
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
      }
    }
  },
  beforeRouteEnter (to, from, next) {
    const problemCode = storage.get(buildProblemCodeKey(to.params.problemID, to.params.contestID))
    if (problemCode) {
      next(vm => {
        vm.language = problemCode.language
        vm.code = problemCode.code
        vm.theme = problemCode.theme
      })
    } else {
      next()
    }
  },
  mounted () {
    this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, { menu: false })
    this.init()
    this.getContestProblems()
  },
  methods: {
    ...mapActions(['changeDomTitle']),
    init () {
      this.$Loading.start()
      this.contestID = this.$route.params.contestID
      this.problemID = this.$route.params.problemID
      const func = this.$route.name === 'problem-details' ? 'getProblem' : 'getContestProblem'
      api[func](this.problemID, this.contestID).then(res => {
        this.$Loading.finish()
        const problem = res.data.data
        this.changeDomTitle({ title: problem.title })
        api.submissionExists(problem.id).then(res => {
          this.submissionExists = res.data.data
        })
        problem.languages = problem.languages.sort()
        this.problem = problem
        // 在beforeRouteEnter中修改了, 说明本地有code，无需加载template
        if (this.code !== '') {
          return
        }
        // try to load problem template
        const userId = this.$route.query.username
        let preferredLanguage = problem.languages[0]
        api.getUserInfo(userId).then(res => {
          const lang = res.data.data.language
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
        })
      }, () => {
        this.$Loading.error()
      })
    },
    handleRoute (route) {
      this.$router.push(route)
    },
    onChangeLang (newLang) {
      if (this.problem.template[newLang]) {
        if (this.code.trim() === '') {
          this.code = this.problem.template[newLang]
        }
      }
      this.language = newLang
    },
    onChangeTheme (newTheme) {
      this.theme = newTheme
    },
    onResetToTemplate () {
      this.$Modal.confirm({
        content: this.$i18n.t('m.Are_you_sure_you_want_to_reset_your_code'),
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
    checkSubmissionStatus () {
      // 使用setTimeout避免一些问题
      if (this.refreshStatus) {
        // 如果之前的提交状态检查还没有停止,则停止,否则将会失去timeout的引用造成无限请求
        clearTimeout(this.refreshStatus)
      }
      const checkStatus = () => {
        const id = this.submissionId
        api.getSubmission(id).then(res => {
          this.result = res.data.data
          if (Object.keys(res.data.data.statistic_info).length !== 0) {
            this.submitting = false
            this.submitted = false
            clearTimeout(this.refreshStatus)
            this.init()
          } else {
            this.refreshStatus = setTimeout(checkStatus, 2000)
          }
        }, res => {
          this.submitting = false
          clearTimeout(this.refreshStatus)
        })
      }
      this.refreshStatus = setTimeout(checkStatus, 2000)
    },
    submitCode () {
      if (this.code.trim() === '') {
        this.$error(this.$i18n.t('m.Code_can_not_be_empty'))
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
      const submitFunc = (data, detailsVisible) => {
        this.statusVisible = true
        api.submitCode(data).then(res => {
          this.submissionId = res.data.data && res.data.data.submission_id
          // 定时检查状态
          this.submitting = false
          this.submissionExists = true
          if (!detailsVisible) {
            this.$Modal.success({
              title: this.$i18n.t('m.Success'),
              content: this.$i18n.t('m.Submit_code_successfully')
            })
            return
          }
          this.submitted = true
          this.checkSubmissionStatus()
        }, res => {
          this.getCaptchaSrc()
          if (res.data.data.startsWith('Captcha is required')) {
            this.captchaRequired = true
          }
          this.submitting = false
          this.statusVisible = false
        })
      }
      if (this.contestRuleType === 'OI' && !this.OIContestRealTimePermission) {
        if (this.submissionExists) {
          this.$Modal.confirm({
            title: '',
            content: '<h3>' + this.$i18n.t('m.You_have_submission_in_this_problem_sure_to_cover_it') + '<h3>',
            onOk: () => {
              // 暂时解决对话框与后面提示对话框冲突的问题(否则一闪而过）
              setTimeout(() => {
                submitFunc(data, false)
              }, 1000)
            },
            onCancel: () => {
              this.submitting = false
            }
          })
        } else {
          submitFunc(data, false)
        }
      } else {
        submitFunc(data, true)
      }
    },
    getContestProblems () {
      this.$store.dispatch('getContestProblems').then(res => {
        // if (this.isAuthenticated) {
        //   if (this.contestRuleType === 'ACM') {
        //     this.addStatusColumn(this.ACMTableColumns, res.data.data)
        //   } else if (this.OIContestRealTimePermission) {
        //     this.addStatusColumn(this.ACMTableColumns, res.data.data)
        //   }
        // }
      })
    },
    goContestProblem (problemID) {
      this.$router.push({
        name: 'contest-problem-details',
        params: {
          contestID: this.$route.params.contestID,
          problemID: problemID
        }
      })
    }
  },
  computed: {
    // from ContestProblemList.vue
    ...mapState({
      contestProblems: state => state.contest.contestProblems
    }),
    ...mapGetters(['isAuthenticated', 'contestRuleType', 'OIContestRealTimePermission']),

    ...mapGetters(['problemSubmitDisabled', 'contestRuleType', 'OIContestRealTimePermission', 'contestStatus']),
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
    }
  },
  beforeRouteLeave (to, from, next) {
    // 防止切换组件后仍然不断请求
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
    '$route' () {
      this.init()
    }
  }
}
</script>

<style lang="less" scoped>
#container {
  display: flex;
  flex-flow: column;
  height: 100vh;
}

#main-header {
  background: #0B232F;
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
  }

  #language-dropdown {
    min-width: 115px;
  }

  /deep/ #language-dropdown button{
    background: #45576C;
  }

  /deep/ #language-dropdown ul {
    background: #45576C;
    left: -90px;

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

#sidebar-container {
  height: 100%;
  background: #24272D;
  color: white;

  .sidebar-row {
    padding: 15px 15px;
    padding-left: 25px;

    .sidebar-icon {
      margin-right: 7px;
    }

    h2 {
      width: 100%;
      margin-top: 10px;
      margin-bottom: 20px;
      font-size: 18px;
    }

    #problem-list {
      margin-left: 30px;

      li {
        list-style-type: none;
        margin-top: 10px;
        margin-bottom: 20px;
        font-size: 18px;
      }
    }
  }

  .bottom-border {
    border-bottom: 1px solid #3B4F56;
  }
}

/deep/ .modal {
  .modal-dialog {
    min-width: 1200px;

    .modal-content {
      border-radius: 10px;
      background: #24272D;
      color: white;

      .modal-header {
        border-bottom: none;

        .modal-title-close {
          width: 100%;
          display: flex;
          flex-direction: row;
          justify-content: space-between;

          h1 {
            display: inline-block;
            margin-top: 10px;
            margin-left: 10px;
            font-size: 35px;
          }
        }
      }

      .modal-body {
        padding: 0;

        #clarifications-table {
          table {
            color: white;

            th {
              min-width: 230px;
              padding: 15px 25px;
              border: none;
            }

            td {
              min-width: 230px;
              padding: 15px 25px;
              border-top: 1px solid #3B4F56;
            }
          }
        }

        #my-submissions-table, #all-submissions-table {
          table {
            color: white;

            th {
              min-width: 100px;
              padding: 15px 25px;
              border: none;
            }

            td {
              min-width: 100px;
              padding: 15px 25px;
              border-top: 1px solid #3B4F56;
            }
          }
        }
      }
    }
  }
}

</style>
