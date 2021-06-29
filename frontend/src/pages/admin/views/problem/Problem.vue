<template>
  <div class="problem">

    <Panel :title="title">
      <b-row>
        <b-col cols="3">
          <b-form-group
            label-for="input-display-id"
          >
            <template v-slot:label>
              <p class="labels">
                Display ID
              </p>
            </template>
            <b-form-input
              id="input-display-id"
              v-model="problem._id"
              placeholder="Display ID"
            ></b-form-input>
          </b-form-group>
        </b-col>
        <b-col cols="9">
          <b-form-group
            label-for="input-title"
            :invalid-feedback="titleInvalidFeedback"
            :state="titleState"
          >
            <template v-slot:label>
              <p class="labels">
                <span class="text-danger">*</span> Title
              </p>
            </template>
            <b-form-input
              id="input-title"
              v-model="problem.title"
              placeholder="Title"
              :state="titleState"
            ></b-form-input>
          </b-form-group>
        </b-col>
      </b-row>

      <b-row>
        <b-col>
          <p class="labels">
            <span class="text-danger">*</span> Description
          </p>
          <tiptap v-model="problem.description"></tiptap>
        </b-col>
      </b-row>

      <b-row>
        <b-col>
          <p class="labels">
            <span class="text-danger">*</span> Input Description
          </p>
          <tiptap v-model="problem.input_description"></tiptap>
        </b-col>
      </b-row>

      <b-row>
        <b-col>
          <p class="labels">
            <span class="text-danger">*</span> Output Description
          </p>
          <tiptap v-model="problem.output_description"></tiptap>
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="4">
          <p class="labels">
            <span class="text-danger">*</span> Time Limit (ms)
          </p>
          <b-form-input
            v-model="problem.time_limit"
            placeholder="Time Limit"
            type="number"
          ></b-form-input>
        </b-col>
        <b-col cols="4">
          <p class="labels">
            <span class="text-danger">*</span> Memory Limit (MB)
          </p>
          <b-form-input
            v-model="problem.memory_limit"
            placeholder="Memory Limit"
            type="number"
          ></b-form-input>
        </b-col>
        <b-col cols="2">
          <p class="labels">
            Difficulty
          </p>
          <b-form-select
            v-model="problem.difficulty"
            :options="difficultyOptions"
            size="sm"
          ></b-form-select>
        </b-col>
      </b-row>

      <b-row>
        <b-col cols="2">
          <p class="labels">
            Visible
          </p>
          <b-form-checkbox
            v-model="problem.visible"
            switch
          >
          </b-form-checkbox>
        </b-col>
        <b-col cols="2">
          <p class="labels">
            Share Submission
          </p>
          <b-form-checkbox
            v-model="problem.share_submission"
            switch
          >
          </b-form-checkbox>
        </b-col>
        <b-col cols="4">
          <p class="labels">
            <span class="text-danger">*</span> Tag
          </p>
          <b-form-tags
            v-model="problem.tags"
            size="sm"
            variant="success"
          >
          </b-form-tags>
        </b-col>
        <b-col cols="4">
          <b-form-group>
            <template v-slot:label>
              <p class="labels">
                <span class="text-danger">*</span> Languages
              </p>
            </template>
            <b-form-checkbox-group
              id="languages-checkbox-group"
              v-model="problem.languages"
            >
              <b-form-checkbox
                v-for="lang in allLanguage.languages"
                :key="lang.name"
                :value="lang.name"
                :title="lang.description"
                v-b-tooltip.hover
                style="margin: 0px 24px 24px 0px;"
              >
              {{ lang.name }}
              </b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
        </b-col>
      </b-row>

      <div>
        <b-form-group v-for="(sample, index) in problem.samples" :key="'sample'+index">
          <Accordion :title="'Sample' + (index + 1)">
            <b-button variant="danger" size="sm" slot="header" @click="deleteSample(index)">
              <b-icon icon="trash-fill"></b-icon> Delete
            </b-button>
            <b-row>
              <b-col cols="6">
                <p class="labels" style="margin-top: 8px">
                  <span class="text-danger">*</span> Input Samples
                </p>
                <b-form-textarea
                  v-model="sample.input"
                  placeholder="Input Samples"
                  rows="5"
                ></b-form-textarea>
              </b-col>
              <b-col cols="6">
                <p class="labels" style="margin-top: 8px">
                  <span class="text-danger">*</span> Output Samples
                </p>
                <b-form-textarea
                  v-model="sample.output"
                  placeholder="Output Samples"
                  rows="5"
                ></b-form-textarea>
              </b-col>
            </b-row>
          </Accordion>
        </b-form-group>
      </div>

      <div class="add-sample-btn">
        <button type="button" class="add-samples" @click="addSample()"><b-icon icon="plus"></b-icon> Add Sample
        </button>
      </div>

      <b-row>
        <b-col>
          <p class="labels">
            Hint
          </p>
          <tiptap v-model="problem.hint" placeholder=""></tiptap>
        </b-col>
      </b-row>

      <p class="labels">
        Code Template
      </p>
      <b-row v-for="(v, k) in template" :key="'template'+k" style="margin: 12px 0px;">
        <p><b-form-checkbox v-model="v.checked">{{ k }}</b-form-checkbox></p>
        <div v-if="v.checked">
          <code-mirror v-model="v.code" :mode="v.mode"></code-mirror>
        </div>
      </b-row>

      <b-row>
        <b-col>
          <p class="labels">
            Special Judge
          </p>
          <b-form-checkbox v-model="problem.spj" @click.native.prevent="switchSpj()">Use Special Judge</b-form-checkbox>
        </b-col>
      </b-row>

      <b-form-group v-if="problem.spj" style="margin-top: 20px;">
        <Accordion :title="$t('m.Special_Judge_Code')">
          <template slot="header">
            <b-row style="align-items: center;">
              <span style="margin-right: 8px">SPJ Language</span>
              <b-form-radio-group
                id="spj-radio-group"
                v-model="problem.spj_language"
              >
                <b-form-radio
                  v-for="spj_lang in allLanguage.spj_languages"
                  :key="'spj'+spj_lang.name"
                  :value="spj_lang.name"
                  :title="spj_lang.description"
                  v-b-tooltip.hover
                >
                {{ spj_lang.name }}
                </b-form-radio>
              </b-form-radio-group>
              <b-button
                variant="primary"
                size="sm"
                style="margin-right: 16px"
                @click="compileSPJ"
              >
                <b-icon icon="shuffle"></b-icon> Compile
              </b-button>
            </b-row>
          </template>
          <code-mirror v-model="problem.spj_code" :mode="spjMode"></code-mirror>
        </Accordion>
      </b-form-group>

      <b-row>
        <b-col cols="4">
          <b-form-group>
            <template v-slot:label>
              <p class="labels">
                IO Mode
              </p>
            </template>
            <b-form-radio-group v-model="problem.io_mode.io_mode">
              <b-form-radio value="Standard IO">Standard IO</b-form-radio>
              <b-form-radio value="File IO">File IO</b-form-radio>
            </b-form-radio-group>
          </b-form-group>
        </b-col>
        <b-col cols="3" v-if="problem.io_mode.io_mode == 'File IO'">
          <b-form-group
            label-for="file-input"
          >
            <template v-slot:label>
              <p class="labels">
                <span class="text-danger">*</span> Input File Name
              </p>
            </template>
            <b-form-input
              id="file-input"
              v-model="problem.io_mode.input"
            ></b-form-input>
          </b-form-group>
        </b-col>
        <b-col cols="3" v-if="problem.io_mode.io_mode == 'File IO'">
          <b-form-group
            label-for="file-output"
          >
            <template v-slot:label>
              <p class="labels">
                <span class="text-danger">*</span> Output File Name
              </p>
            </template>
            <b-form-input
              id="file-output"
              v-model="problem.io_mode.output"
            ></b-form-input>
          </b-form-group>
        </b-col>
      </b-row>

      <b-form-checkbox
        style="margin: 24px 0px;"
        v-model="testcase_file_upload"
        @click.native.prevent="switchTestcase()"
      >
        Upload with file
      </b-form-checkbox>
      <b-row>
        <b-col cols="6" v-if="testcase_file_upload">
          <b-form-file
            multiple
            v-model="testcaseFile"
            :state="Boolean(testcaseFile)"
          ></b-form-file>
        </b-col>
      </b-row>

      <div v-if="!testcase_file_upload">
        <b-form-group v-for="(testcase, index) in problem.testcases" :key="'testcase'+index">
          <Accordion :title="'Testcase' + (index + 1)">
            <b-button variant="danger" size="sm" slot="header" @click="deleteTestCase(index)">
              <b-icon icon="trash-fill"></b-icon> Delete
            </b-button>
            <b-row>
              <b-col cols="6">
                <p class="labels" style="margin-top: 8px">
                  Input
                </p>
                <b-form-textarea
                  v-model="testcase.input"
                  placeholder="Input"
                  rows="5"
                ></b-form-textarea>
              </b-col>
              <b-col cols="6">
                <p class="labels" style="margin-top: 8px">
                  Output
                </p>
                <b-form-textarea
                  v-model="testcase.output"
                  placeholder="Output"
                  rows="5"
                ></b-form-textarea>
              </b-col>
            </b-row>
          </Accordion>
        </b-form-group>
      </div>

      <div class="add-sample-btn" v-if="!testcase_file_upload">
        <button type="button" class="add-samples" @click="addTestCase()"><b-icon icon="plus"></b-icon> Add Testcase
        </button>
      </div>

      <b-row>
        <b-col>
          <b-table
            :items="problem.test_case_score"
            :fields="testcaseTableFields"
            style="width: 100%"
          >
            <template #cell(score)="row">
              <b-form-input
                size="sm"
                v-model="row.item.score"
                :placeholder="Score"
                :disabled="problem.rule_type !== 'OI'"
              />
            </template>
          </b-table>
        </b-col>
      </b-row>

      <p class="labels">
        Source
      </p>
      <b-form-input
        v-model="problem.source"
        placeholder="Source"
      ></b-form-input>
      <save @click.native="submit()" style="margin-top: 24px;">Save</save>
    </Panel>
  </div>
</template>

<script>
import tiptap from '../../components/Tiptap'
import Accordion from '../../components/Accordion'
import CodeMirror from '../../components/CodeMirror'
import api from '../../api'

export default {
  name: 'Problem',
  components: {
    tiptap,
    Accordion,
    CodeMirror
  },
  data () {
    return {
      rules: {
        title: { required: true, message: 'Title is required', trigger: 'blur' },
        input_description: { required: true, message: 'Input Description is required', trigger: 'blur' },
        output_description: { required: true, message: 'Output Description is required', trigger: 'blur' }
      },
      loadingCompile: false,
      mode: '',
      contest: {},
      problem: {
        title: '',
        languages: [],
        io_mode: { io_mode: 'Standard IO', input: 'input.txt', output: 'output.txt' }
      },
      reProblem: {
        languages: [],
        io_mode: { io_mode: 'Standard IO', input: 'input.txt', output: 'output.txt' }
      },
      testCaseUploaded: false,
      testcase_file_upload: false,
      allLanguage: {},
      inputVisible: false,
      tagInput: '',
      problemTagList: [],
      template: {},
      title: '',
      spjMode: '',
      disableRuleType: false,
      routeName: '',
      error: {
        tags: '',
        spj: '',
        languages: '',
        testCase: ''
      },
      difficultyOptions: [
        { value: 'Level1', text: 'Level 1' },
        { value: 'Level2', text: 'Level 2' },
        { value: 'Level3', text: 'Level 3' },
        { value: 'Level4', text: 'Level 4' },
        { value: 'Level5', text: 'Level 5' },
        { value: 'Level6', text: 'Level 6' },
        { value: 'Level7', text: 'Level 7' }
      ],
      testcaseFile: null,
      testcaseFileList: [],
      testcaseTableFields: [
        { key: 'input_name', label: 'Input' },
        { key: 'output_name', label: 'Output' },
        { key: 'score', label: 'Score' }
      ]
    }
  },
  mounted () {
    this.routeName = this.$route.name
    if (this.routeName === 'edit-problem' || this.routeName === 'edit-contest-problem') {
      this.mode = 'edit'
    } else {
      this.mode = 'add'
    }
    api.getLanguages().then(res => {
      this.problem = this.reProblem = {
        _id: '',
        title: '',
        description: '',
        input_description: '',
        output_description: '',
        time_limit: 1000,
        memory_limit: 256,
        difficulty: 'Level1',
        visible: true,
        share_submission: false,
        tags: [],
        languages: [],
        template: {},
        samples: [{ input: '', output: '' }],
        testcases: [{ input: '', output: '' }],
        spj: false,
        spj_language: '',
        spj_code: '',
        spj_compile_ok: false,
        test_case_id: '',
        test_case_score: [],
        rule_type: 'ACM',
        hint: '',
        source: '',
        io_mode: { io_mode: 'Standard IO', input: 'input.txt', output: 'output.txt' }
      }
      const contestID = this.$route.params.contestId
      if (contestID) {
        this.problem.contest_id = this.reProblem.contest_id = contestID
        this.disableRuleType = true
        api.getContest(contestID).then(res => {
          this.problem.rule_type = this.reProblem.rule_type = res.data.data.rule_type
          this.contest = res.data.data
        })
      }

      this.problem.spj_language = 'C'

      const allLanguage = res.data.data
      this.allLanguage = allLanguage

      // get problem after getting languages list to avoid find undefined value in `watch problem.languages`
      if (this.mode === 'edit') {
        this.title = this.$i18n.t('m.Edit_Problem')
        const funcName = { 'edit-problem': 'getProblem', 'edit-contest-problem': 'getContestProblem' }[this.routeName]
        api[funcName](this.$route.params.problemId).then(problemRes => {
          const data = problemRes.data.data
          if (!data.spj_code) {
            data.spj_code = ''
          }
          data.spj_language = data.spj_language || 'C'
          data.testcases = []
          this.problem = data
          this.testCaseUploaded = true
          api.getTestCase(this.$route.params.problemId).then(testcaseRes => {
            const testcaseData = testcaseRes.data.data
            this.problem.testcases = this.problem.testcases.concat(testcaseData.testcases)
            if (testcaseData.spj === 'True') this.problem.spj = true
            else this.problem.spj = false
          })
        })
      } else {
        this.title = this.$i18n.t('m.Add_Problem')
        for (const item of allLanguage.languages) {
          this.problem.languages.push(item.name)
        }
      }
    })
    this.getProblemTagList()
  },
  watch: {
    '$route' () {
      this.$refs.form.resetFields()
      this.problem = this.reProblem
    },
    'problem.languages' (newVal) {
      const data = {}
      // use deep copy to avoid infinite loop
      const languages = JSON.parse(JSON.stringify(newVal)).sort()
      for (const item of languages) {
        if (this.template[item] === undefined) {
          const langConfig = this.allLanguage.languages.find(lang => {
            return lang.name === item
          })
          if (this.problem.template[item] === undefined) {
            data[item] = { checked: false, code: langConfig.config.template, mode: langConfig.content_type }
          } else {
            data[item] = { checked: true, code: this.problem.template[item], mode: langConfig.content_type }
          }
        } else {
          data[item] = this.template[item]
        }
      }
      this.template = data
    },
    'problem.spj_language' (newVal) {
      this.spjMode = this.allLanguage.spj_languages.find(item => {
        return item.name === this.problem.spj_language
      }).content_type
    },
    'testcaseFile' () {
      // this.uploadTestcase()
    }
  },
  methods: {
    switchSpj () {
      if (this.testCaseUploaded) {
        this.$confirm('If you change problem judge method, you need to re-upload test cases', 'Warning', {
          confirmButtonText: 'Yes',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          this.problem.spj = !this.problem.spj
          this.resetTestCase()
        }).catch(() => {
        })
      } else {
        this.problem.spj = !this.problem.spj
      }
    },
    switchTestcase () {
      if (this.testCaseUploaded) {
        this.$confirm('If you change upload method, you need to re-upload testcases', 'Warning', {
          confirmButtonText: 'Yes',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          this.testcase_file_upload = !this.testcase_file_upload
          this.resetTestCase()
        }).catch(() => {
        })
      } else {
        this.testcase_file_upload = !this.testcase_file_upload
      }
    },
    async getProblemTagList () {
      const response = await api.getProblemTagList()
      for (const tag of response.data.data) {
        this.problemTagList.push(tag.name)
      }
    },
    resetTestCase () {
      this.testCaseUploaded = false
      this.problem.test_case_score = []
      this.problem.test_case_id = ''
    },
    addTag () {
      const inputValue = this.tagInput
      if (inputValue) {
        this.problem.tags.push(inputValue)
      }
      this.inputVisible = false
      this.tagInput = ''
    },
    closeTag (tag) {
      this.problem.tags.splice(this.problem.tags.indexOf(tag), 1)
    },
    addSample () {
      this.problem.samples.push({ input: '', output: '' })
    },
    deleteSample (index) {
      this.problem.samples.splice(index, 1)
    },
    addTestCase () {
      this.problem.testcases.push({ input: '', output: '' })
    },
    deleteTestCase (index) {
      this.problem.testcases.splice(index, 1)
    },
    async uploadTestcase () {
      if (this.testcaseFile === null) {
        this.$error('No file selected')
        return
      }
      try {
        const response = await api.uploadTestcase({
          file: this.testcaseFile,
          spj: this.problem.spj
        })
        this.uploadSucceeded(response)
      } catch (err) {
        this.uploadFailed()
      }
    },
    uploadSucceeded (response) {
      if (response.error) {
        this.$error(response.data)
        return
      }
      const fileList = response.data.info
      for (const file of fileList) {
        file.score = (100 / fileList.length).toFixed(0)
        if (!file.output_name && this.problem.spj) {
          file.output_name = '-'
        }
      }
      this.problem.test_case_score = fileList
      this.testCaseUploaded = true
      this.problem.test_case_id = response.data.id
    },
    uploadFailed () {
      this.$error('Upload failed')
    },
    compileSPJ () {
      const data = {
        id: this.problem.id,
        spj_code: this.problem.spj_code,
        spj_language: this.problem.spj_language
      }
      this.loadingCompile = true
      api.compileSPJ(data).then(res => {
        this.loadingCompile = false
        this.problem.spj_compile_ok = true
        this.error.spj = ''
      }, err => {
        this.loadingCompile = false
        this.problem.spj_compile_ok = false
        const h = this.$createElement
        this.$msgbox({
          title: 'Compile Error',
          type: 'error',
          message: h('pre', err.data.data),
          showCancelButton: false,
          closeOnClickModal: false,
          customClass: 'dialog-compile-error'
        })
      })
    },
    submit () {
      if (!this.problem.samples.length) {
        this.$error('Sample is required')
        return
      }
      for (const sample of this.problem.samples) {
        if (!sample.input || !sample.output) {
          this.$error('Sample input and output is required')
          return
        }
      }

      if (!this.problem.tags.length) {
        this.error.tags = 'Please add at least one tag'
        this.$error(this.error.tags)
        return
      }
      if (this.problem.spj) {
        if (!this.problem.spj_code) {
          this.error.spj = 'Spj code is required'
          this.$error(this.error.spj)
        } else if (!this.problem.spj_compile_ok) {
          this.error.spj = 'SPJ code has not been successfully compiled'
        }
        if (this.error.spj) {
          this.$error(this.error.spj)
          return
        }
      }
      if (!this.problem.languages.length) {
        this.error.languages = 'Please choose at least one language for problem'
        this.$error(this.error.languages)
        return
      }
      if (!this.testcase_file_upload) {
        for (const testcase of this.problem.testcases) {
          if (!testcase.input || !testcase.output) {
            this.$error('Testcase input and output is required')
            return
          }
        }
        this.resetTestCase()
      } else if (!this.testCaseUploaded) {
        this.error.testCase = 'Test case is not uploaded yet'
        this.$error(this.error.testCase)
        return
      }
      if (this.problem.rule_type === 'OI') {
        for (const item of this.problem.test_case_score) {
          try {
            if (parseInt(item.score) <= 0) {
              this.$error('Invalid test case score')
              return
            }
          } catch (e) {
            this.$error('Test case score must be an integer')
            return
          }
        }
      }
      this.problem.languages = this.problem.languages.sort()
      this.problem.template = {}
      for (const k in this.template) {
        if (this.template[k].checked) {
          this.problem.template[k] = this.template[k].code
        }
      }
      const funcName = {
        'create-problem': 'createProblem',
        'edit-problem': 'editProblem',
        'create-contest-problem': 'createContestProblem',
        'edit-contest-problem': 'editContestProblem'
      }[this.routeName]
      // edit contest problem 时, contest_id会被后来的请求覆盖掉
      if (funcName === 'editContestProblem') {
        this.problem.contest_id = this.contest.id
      }

      if (!this.testcase_file_upload) {
        api.createTestCase({
          testcases: this.problem.testcases,
          spj: this.problem.spj
        }).then(response => {
          const fileList = response.data.data.info
          for (const file of fileList) {
            file.score = (100 / fileList.length).toFixed(0)
            if (!file.output_name && this.problem.spj) {
              file.output_name = '-'
            }
          }
          this.problem.test_case_score = fileList
          this.testCaseUploaded = true
          this.problem.test_case_id = response.data.data.id
          api[funcName](this.problem).then(res => {
            if (this.routeName === 'create-contest-problem' || this.routeName === 'edit-contest-problem') {
              this.$router.push({ name: 'contest-problem-list', params: { contestId: this.$route.params.contestId } })
            } else {
              this.$router.push({ name: 'problem-list' })
            }
          }).catch(() => {
          })
        })
      } else {
        api[funcName](this.problem).then(res => {
          if (this.routeName === 'create-contest-problem' || this.routeName === 'edit-contest-problem') {
            this.$router.push({ name: 'contest-problem-list', params: { contestId: this.$route.params.contestId } })
          } else {
            this.$router.push({ name: 'problem-list' })
          }
        }).catch(() => {
        })
      }
    }
  },
  computed: {
    titleState () {
      return this.problem.title.length > 0
    },
    titleInvalidFeedback () {
      return 'Title is required'
    }
  }
}
</script>

<style lang="less" scoped>
  .problem {
    .difficulty-select {
      width: 120px;
    }
    .spj-radio {
      margin-left: 10px;
      &:last-child {
        margin-right: 20px;
      }
    }
    .input-new-tag {
      width: 78px;
    }
    .button-new-tag {
      height: 24px;
      line-height: 22px;
      padding-top: 0;
      padding-bottom: 0;
    }
    .tags {
      .el-tag {
        margin-right: 10px;
      }
    }
    .accordion {
      margin-bottom: 10px;
    }
    .add-samples {
      width: 100%;
      background-color: #fff;
      border: 1px dashed #aaa;
      outline: none;
      cursor: pointer;
      color: #666;
      height: 35px;
      font-size: 14px;
      &:hover {
        background-color: #f9fafc;
      }
      i {
        margin-right: 10px;
      }
    }
    .add-sample-btn {
      margin-bottom: 10px;
    }
  }
  .labels {
    margin-top: 24px;
    margin-bottom: 24px;
  }
</style>

<style>
  .dialog-compile-error {
    width: auto;
    max-width: 80%;
    overflow-x: scroll;
  }
</style>
