<template>
  <div class="flex-grow-1 mx-2 problem" style="max-width: 1300px;">
    <b-breadcrumb :items="pageLocations" class="mt-3"></b-breadcrumb>
    <b-row
      type="flex"
      cols = "1"
      id="add-or-edit-problem"
    >
      <b-col>
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
                <b-button class ="ml-3 mb-1" variant="outline-secondary" size="sm" v-b-modal.description_preview>Preview</b-button>
              </p>
              <tiptap v-model="problem.description"></tiptap>
              <b-modal id="description_preview" title="Description Preview" hide-footer>
                <template #default>
                  <div v-katex:auto>
                    <p v-dompurify-html="problem.description"></p>
                  </div>
                </template>
              </b-modal>
            </b-col>
          </b-row>

          <b-row>
            <b-col>
              <p class="labels">
                <span class="text-danger">*</span> Input Description
                <b-button class ="ml-3 mb-1" variant="outline-secondary" size="sm" v-b-modal.input_description_preview>Preview</b-button>
              </p>
              <tiptap v-model="problem.input_description"></tiptap>
              <b-modal id="input_description_preview" title="Input Description Preview" hide-footer>
                <template #default>
                  <div v-katex:auto>
                    <p v-dompurify-html="problem.input_description"></p>
                  </div>
                </template>
              </b-modal>
            </b-col>
          </b-row>

          <b-row>
            <b-col>
              <p class="labels">
                <span class="text-danger">*</span> Output Description
                <b-button class ="ml-3 mb-1" variant="outline-secondary" size="sm" v-b-modal.output_description_preview>Preview</b-button>
              </p>
              <tiptap v-model="problem.output_description"></tiptap>
              <b-modal id="output_description_preview" title="Output Description Preview" hide-footer>
                <template #default>
                  <div v-katex:auto>
                    <p v-dompurify-html="problem.output_description"></p>
                  </div>
                </template>
              </b-modal>
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
              <div>
                <b-form-tags v-model="problem.tags">
                  <template v-slot="{tags, addTag, removeTag}">
                    <div>
                      <ul v-if="tags.length > 0" class="list-inline d-inline-block mb-2">
                        <li v-for="tag in tags" :key="tag" class="list-inline-item">
                          <b-form-tag
                            @remove="removeTag(tag)"
                            :title="tag"
                            :disabled="disabled"
                            variant="info"
                          >{{ tag }}</b-form-tag>
                        </li>
                      </ul>
                    </div>
                    <b-dropdown size="sm" text="tag" variant="outline-secondary" block-menu-class="w-100" class="tag-dropdown" drop-right>
                      <b-dropdown-form @submit.stop.prevent="() => {}">
                        <b-form-group>
                          <b-input-group class="mb-2">
                            <b-form-input
                              v-model="search"
                              type="search"
                              size="sm"
                              autocomplete="off"
                              @keyup.enter="onAddClick({ search, addTag })"
                            ></b-form-input>
                            <b-input-group-append>
                              <b-button size="sm" @click="onAddClick({search, addTag})" variant="primary">Add</b-button>
                            </b-input-group-append>
                          </b-input-group>
                        </b-form-group>
                      </b-dropdown-form>
                      <b-dropdown-divider></b-dropdown-divider>
                      <b-dropdown-item-button
                        v-for="item in availableTags"
                        :key="item"
                        @click="onTagClick({ item, addTag })"
                      >
                        {{ item }}
                      </b-dropdown-item-button>
                    </b-dropdown>
                  </template>
                </b-form-tags>
              </div>
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
                <b-button class ="ml-3 mb-1" variant="outline-secondary" size="sm" v-b-modal.hintpreview>Preview</b-button>
              </p>
              <tiptap v-model="problem.hint" placeholder=""></tiptap>
              <b-modal id="hintpreview" title="Hint Preview" hide-footer>
                <template #default>
                  <div v-katex:auto>
                    <p v-dompurify-html="problem.hint"></p>
                  </div>
                </template>
              </b-modal>
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
            <Accordion title="Special Judge Code">
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
            <button type="button" class="add-samples" @click="addTestCase()"><b-icon icon="plus"></b-icon>
              Add Testcase
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
                    :disabled="problem.rule_type !== 'ASSIGNMENT'"
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
          <b-modal id="checkTestcaseScoreModal" title="Check testcase points" ok-only>
            <p>
              Testcase upload success!
              Please check points at each testcase. After revising testcase points, press OK button.
            </p>
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
                  :disabled="problem.rule_type !== 'ASSIGNMENT'"
                />
              </template>
            </b-table>
          </b-modal>
        </Panel>
      </b-col>
    </b-row>
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
      ],
      search: '',
      assignmentId: '',
      pageLocations: [
        {
          text: this.$route.params.courseInfo,
          to: '/course/' + this.$route.params.courseId + '/dashboard'
        },
        {
          text: this.$route.params.assignmentInfo,
          to: '/course/' + this.$route.params.courseId + '/assignment'
        }
      ]
    }
  },
  async mounted () {
    this.routeName = this.$route.name
    if (this.routeName === 'edit-course-problem') {
      this.mode = 'edit'
    } else {
      this.mode = 'add'
    }
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
      rule_type: 'ASSIGNMENT',
      hint: '',
      source: '',
      io_mode: { io_mode: 'Standard IO', input: 'input.txt', output: 'output.txt' }
    }
    this.assignmentId = this.$route.params.assignmentId
    if (this.assignmentId) {
      this.problem.assignment_id = this.reProblem.assignment_id = this.assignmentId
      const res = await api.getAssignmentList(null, this.assignmentId)
      this.assignment = res.data.data
    }
    this.problem.spj_language = 'C'

    const res = await api.getLanguages()
    const allLanguage = res.data.data
    this.allLanguage = allLanguage
    // get problem after getting languages list to avoid find undefined value in `watch problem.languages`
    if (this.mode === 'edit') {
      this.title = 'Edit Problem'
      const problemRes = await api.getAssignmentProblem(this.assignemntId, this.$route.params.problemId)
      const data = problemRes.data.data
      if (!data.spj_code) {
        data.spj_code = ''
      }
      data.spj_language = data.spj_language || 'C'
      data.testcases = []
      this.problem = data
      this.testCaseUploaded = true
      const testcaseRes = await api.getTestCase(this.$route.params.problemId)
      const testcaseData = testcaseRes.data.data
      this.problem.testcases = this.problem.testcases.concat(testcaseData.testcases)
      if (testcaseData.spj === 'True') this.problem.spj = true
      else this.problem.spj = testcaseData.spj === 'True'
      this.pageLocations.push({
        text: this.$route.params.problemId + ' - ' + this.problem.title
      }, {
        text: 'Edit problem'
      })
    } else {
      this.title = 'Add Problem'
      for (const item of allLanguage.languages) {
        this.problem.languages.push(item.name)
      }
      this.pageLocations.push({
        text: 'Create Problem'
      })
    }
    this.getProblemTagList()
  },
  watch: {
    '$route' () {
      this.$refs.form.resetFields()
      this.problem = this.reProblem
    },
    'problem.languages' (newVal) {
      const data = {}
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
    'problem.spj_language' () {
      if (!this.allLanguage.spj_languages) {
        return
      }
      this.spjMode = this.allLanguage.spj_languages.find(item => {
        return item.name === this.problem.spj_language
      }).content_type
    },
    'testcaseFile' () {
      this.uploadTestcase()
    }
  },
  methods: {
    onTagClick ({ item, addTag }) {
      addTag(item)
      this.search = ''
    },
    onAddClick ({ search, addTag }) {
      addTag(search)
      this.search = ''
    },
    async switchSpj () {
      if (this.testCaseUploaded) {
        try {
          await this.$confirm('If you change problem judge method, you need to re-upload test cases', 'Warning', 'warning', false)
          this.problem.spj = !this.problem.spj
          this.resetTestCase()
        } catch (err) {
        }
      } else {
        this.problem.spj = !this.problem.spj
      }
    },
    async switchTestcase () {
      if (this.testCaseUploaded) {
        try {
          await this.$confirm('If you change upload method, you need to re-upload testcases', 'Warning', 'warning', false)
          this.testcase_file_upload = !this.testcase_file_upload
          this.resetTestCase()
        } catch (err) {
        }
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
        const formData = new FormData()
        const blob = new Blob([this.testcaseFile])
        formData.append('spj', this.problem.spj)
        formData.append('file', blob, this.testcaseFile.name)
        const res = await api.uploadTestCase(formData)
        this.uploadSucceeded(res)
      } catch (err) {
      }
    },
    uploadSucceeded (response) {
      const fileList = response.data.data.info
      for (const file of fileList) {
        file.score = (100 / fileList.length).toFixed(0)
        if (!file.output_name && this.problem.spj) {
          file.output_name = '-'
        }
      }
      this.$set(this.problem, 'test_case_score', fileList)
      this.testCaseUploaded = true
      this.problem.test_case_id = response.data.data.id
    },
    async compileSPJ () {
      const data = {
        id: this.problem.id,
        spj_code: this.problem.spj_code,
        spj_language: this.problem.spj_language
      }
      this.loadingCompile = true
      try {
        await api.compileSPJ(data)
        this.loadingCompile = false
        this.problem.spj_compile_ok = true
        this.error.spj = ''
      } catch (err) {
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
      }
    },
    async submit () {
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
      if (this.problem.rule_type === 'ASSIGNMENT') {
        for (const item of this.problem.test_case_score) {
          try {
            if (parseInt(item.score) <= 0) {
              this.$error('Invalid test case score')
              return
            }
          } catch (err) {
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
        'create-course-problem': 'createAssignmentProblem',
        'edit-course-problem': 'editAssignmentProblem'
      }[this.routeName]
      if (funcName === 'editAssignmentProblem') {
        this.problem.assignment_id = this.assignment.id
      }
      if (!this.testcase_file_upload) {
        try {
          const response = await api.createTestCase({
            testcases: this.problem.testcases,
            spj: this.problem.spj
          })
          const fileList = response.data.data.info
          let testcaseScoreSum = 0
          for (const file of fileList) {
            file.score = (100 / fileList.length).toFixed(0)
            testcaseScoreSum += Number(file.score)
            if (!file.output_name && this.problem.spj) {
              file.output_name = '-'
            }
          }
          // To make Automatic testcase score sum 100
          if (testcaseScoreSum !== 100) {
            fileList[0].score = Number(fileList[0].score) + (100 - testcaseScoreSum)
          }
          this.problem.test_case_score = fileList
          this.testCaseUploaded = true
          this.problem.test_case_id = response.data.data.id
          // for check testcase score after testcase upload
          const self = this
          await new Promise(function (resolve, reject) {
            self.$bvModal.show('checkTestcaseScoreModal')
            self.$root.$on('bv::modal::hide', (bvEvent) => {
              if (bvEvent.componentId === 'checkTestcaseScoreModal' && bvEvent.trigger === 'ok') {
                let testcaseScoreSum = 0
                for (const file of fileList) {
                  testcaseScoreSum += Number(file.score)
                }
                if (testcaseScoreSum !== 100) {
                  bvEvent.preventDefault()
                  self.$error('Testcase Score Sum must be 100!')
                } else {
                  resolve()
                }
              } else {
                reject(new Error('user canceled'))
              }
            })
          })
          await api[funcName](this.problem)
          this.$router.push({ name: 'course-assignment-list', params: { assignmentId: this.assignmentId } })
        } catch (err) {
          console.error(err)
        }
      } else {
        try {
          await api[funcName](this.problem)
          this.$router.push({ name: 'course-assignment-list', params: { assignmentId: this.assignmentId } })
        } catch (err) {
        }
      }
    }
  },
  computed: {
    availableTags () {
      const tagInput = this.search.trim().toLowerCase()
      const tags = this.problemTagList.filter(tag => this.problem.tags.indexOf(tag) === -1)
      if (tagInput) {
        return tags.filter(tag => tag.toLowerCase().indexOf(tagInput) > -1)
      }
      return tags
    },
    titleState () {
      return this.problem.title.length > 0
    },
    titleInvalidFeedback () {
      return 'Title is required'
    }
  }
}
</script>

<style lang="scss" scoped>
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
  #add-or-edit-problem {
    margin: auto;
    flex:1 0;
    max-width: 1300px;
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

  .tag-dropdown .dropdown-menu{
    max-height: 400px;
    overflow-y: auto;
  }
</style>
