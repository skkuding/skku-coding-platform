<template>
  <div class="grade">
    <p>{{pageInfo.title}}_{{pageInfo.class_number}}_{{pageInfo.course_code}}-Assignment{{pageInfo.assignment_id}}</p>
    <Panel :title="'Assignment'+assignmentId+' - '+problemId+' '+problemTitle">
      <b-table
        ref="table"
        :items="scoreList"
        :fields="field"
        :per-page="pageSize"
        :current-page="updateCurrentPage"
        style="width: 100%"
      >
        <template #cell(studentId)="row">
          {{row.item.student_id}}
        </template>

        <template #cell(name)="row">
          {{row.item.name}}
        </template>

        <template #head(code)="row">
          <span>
            {{row.label}}
            <icon-btn icon="download" varient="outline-*" @click.native="download()"/>
          </span>
        </template>

        <template #cell(code)="row">
          <b-button v-b-modal.submission-detail-modal> <!-- id를 어떻게 잘 바꿔서 모달이 하나만 뜨게 하자 -->
            <b-icon
              :icon="row.item.code ? 'code' : 'dash'"
              variant="outline-*"
            />
          </b-button>
          <!-- <Modal :problemID="problemId"/> -->
        </template>

        <template #cell(score)="row">
          <b-row style="max-width: 100%" >
            <div v-if="newScore" style="margin-top: 6px">
              {{newScore}} / {{row.item.total_score}}
            </div>
            <div v-if="!newScore" style="margin: 6px 12px">
              {{row.item.user_score ? row.item.user_score : '- '}} / {{row.item.total_score}}
            </div>
            <b-button :pressed.sync="press" variant="outline-*">
              <b-icon icon="pencil" />
            </b-button>
            <div v-if="press" style="margin-left: 12px">
              <b-form-input
                v-model="newScore"
                :id="'input-new-score'+row.item.student_id"
                style="padding-left: 12px"
              >
              {{newScore}} / {{row.item.total_score}} <!-- api로 점수 바꾸기 -->
              </b-form-input>
            </div>
          </b-row>
        </template>
      </b-table>
      <div class="panel-options">
        <b-pagination
          v-model="currentPage"
          :per-page="pageSize"
          :total-rows="total"
          style="position: absolute; right: 20px; top: 15px;"
        />
      </div>
    </Panel>
  </div>
</template>

<script>
import IconBtn from '../../components/btn/IconBtn.vue'
// import Modal from '../components/modal.vue'
// import api from '../api.js'
// import utils from '@/utils/utils'
export default {
  name: 'ProblemGrade',
  components: {
    IconBtn
    // Modal
  },
  data () {
    return {
      problemId: 'A',
      assignmentId: 1,
      lectureId: 3,
      problemTitle: '가파른 경사',
      pageSize: 10,
      total: 1,
      currentPage: 0,
      press: false,
      newScore: 0,
      submissionlist: [],
      field: [
        { key: 'studentId', label: 'Student ID' },
        { key: 'name', label: 'Name' },
        { key: 'code', label: 'Code' },
        { key: 'score', label: 'Score' }
      ],
      scoreList: [{
        student_id: 1,
        name: 'qwerqwer',
        user_score: 90,
        total_score: 100,
        code: true
      },
      {
        student_id: 2,
        name: 'itsme',
        user_score: 60,
        total_score: 100,
        code: false
      },
      {
        student_id: 5,
        name: 'puupuupu',
        user_score: 70,
        total_score: 100,
        code: false
      },
      {
        student_id: 7,
        name: 'qiwieoro',
        user_score: 99,
        total_score: 100,
        code: true
      }],
      pageInfo: {
        title: 'Python Programming',
        course_code: 'GDBEASDF',
        class_number: 41,
        assignment_id: 1,
        problem_id: 1
      }
    }
  },
  watch: {
  },
  mounted () {
    this.init()
    this.getSubmissionList()
  },
  methods: {
    init () {
      // this.$route.assignmentId
    },
    // downloadAll () {

    // },
    download () {
      // const url = `/prof/download_submissions?contest_id=${this.currentId}&exclude_admin=${excludeAdmin}`
      // utils.downloadFile(url)
      // admin은 api가 있기했다
    },
    goCode (id) {
      this.$router.push({ name: 'announcement', params: { id } }) // 길을 잃었다~ 어딜가야 할까~~
    },
    currentChange (page) {
      this.currentPage = page
      this.getSubmissionList(page)
    },
    getSubmissionList (page) {
      // const res = api.SubmissionList(this.pageSize, (page-1)*this.pageSize, this.pageInfo.assignment_id, this.pageInfo.problem_id)
    }
  },
  computed: {
  }
}
</script>

<style  scoped lang="scss">
</style>
