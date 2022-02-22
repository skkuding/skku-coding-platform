<template>
  <div class="lecture-qna-card">
    <sidemenu/>
    <div class="top-bar mb-4">
      <h2 class="title">Course QnA</h2>
      <b-button
        class="button"
        size="sm"
        @click="editCreateQuestionDialog"
      >New Question</b-button>
    </div>
    <div style="margin-left: 68px;">QnA Page will be provided soon. :></div>
    <div class="table">
      <b-table
        hover
        :items="questions"
        :fields="questionListFields"
        head-variant="light"
        class="table"
        @row-clicked="goQuestion"
      >
        <template #cell(date)="data">
          {{ data.item.date }}
        </template>
        <template #cell(status)="data">
          <b-icon
            icon="circle-fill"
            scale="0.7"
            :style="'color:' + data.item.color"
          ></b-icon>
          {{ data.item.status }}
        </template>
      </b-table>
    </div>
    <b-modal
      v-model="showCreateQuestionDialog"
      title="Create a New Question"
      centered
      ref="create-question"
      size="lg"
    >
      <div class="modal-content">
        <b-form-group
          id="question-title"
          label="Title"
          label-for="title"
        >
          <b-form-input
            v-model="questions.title"
            placeholder="Title"
            id="title"
            required
          >
          </b-form-input>
        </b-form-group>

        <b-form-group
          id="question-content"
          label="Content"
          label-for="content"
        >
          <b-form-textarea
            id="content"
            v-model="questions.content"
            placeholder="Content"
            rows="6"
            max-rows="6"
            required
            no-resize
          ></b-form-textarea>
        </b-form-group>
      </div>
      <template #modal-footer>
        <b-button @click="showCreateQuestionDialog = false">Cancel</b-button>
        <b-button @click="submitQuestion">Save</b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
import sidemenu from '@oj/components/Sidemenu.vue'
import api from '@oj/api'
import moment from 'moment'

export default {
  name: 'CourseQna',
  components: {
    sidemenu
  },
  data () {
    return {
      questionListFields: [
        'title',
        'status',
        'date'
      ],
      course_id: 1,
      questions: [
        {
          id: 3,
          title: 'third',
          status: 'Not Resolved',
          date: '2021-08-09',
          color: '#D75B66',
          content: ''
        },
        {
          id: 2,
          title: 'second',
          status: 'Not Resolved',
          date: '2021-08-09',
          color: '#D75B66',
          content: ''
        },
        {
          id: 1,
          title: 'first',
          status: 'Resolved',
          date: '2021-08-09',
          color: '#8DC63F',
          content: ''
        }
      ],

      showCreateQuestionDialog: false,
      listVisible: true
    }
  },
  async mounted () {
    this.course_id = this.$route.params.courseID
  },
  methods: {
    async init () {
      await this.getQuestionList()
    },
    async getQuestionList () {
      const res = await api.getQuestionList(0, 20) // 개수?
      this.questions = res.data.data.results
    },
    async editCreateQuestionDialog () {
      this.showCreateQuestionDialog = true
      /*
      const localtime = moment().format()
      const data = {
        course_id: this.course_id,
        title: this.questions.title,
        content: this.questions.content,
        last_update_time: localtime,
        create_time: this.questions.date
      }
      console.log(data)
      const res = await api.updateQuestion(data)
      console.log(res)
      */
    },
    async submitQuestion () {
      this.showCreateQuestionDialog = false
      const localtime = moment().format()
      /*
      if (this.questions) {
        const data = {
          id: this.questions.id,
          title: this.questions.title,
          content: this.questions.content
        }
        console.log(data)
        const res = await api.createQuestion(data)
        console.log(res)
      } else {
        const data = {
          course_id: this.course_id,
          title: this.questions.title,
          content: this.questions.content,
          last_update_time: localtime,
          create_time: this.questions.date
        }
        console.log(data)
        const res = await api.updateQuestion(data)
        console.log(res)
      }
*/
      const data = {
        course_id: this.course_id,
        title: this.questions.title,
        content: this.questions.content,
        last_update_time: localtime,
        create_time: this.questions.date
      }
      console.log(data)
      const res = await api.createQuestion(data)
      console.log(res)
    },
    async goQuestion (question) {
      this.question = question
      this.listVisible = false
      await this.$router.push({ name: 'lecture-qna-detail', params: { questionID: question.id } })
    }
  },
  computed: {
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .lecture-qna-card{
    margin: 0 auto;
    width: 70%;
    font-family: Manrope_bold;
    .table{
      width: 95% !important;
      margin: 0 auto;
    }
  }
  .title{
    color: #7C7A7B;
  }
  .button {
    height:30px;
    margin: auto 0;
  }
  .top-bar {
    margin: 40px 68px 0;
    display: flex;
    justify-content: space-between;
  }
  .modal-content::v-deep {
    width: 90%;
    margin: 0 auto;
  }
  .form-control {
    width: 100% !important;
  }
</style>
