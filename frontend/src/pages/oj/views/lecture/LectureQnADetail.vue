<template>
  <div>
    <sidemenu/>
    <article class="lecture-qna-card">
      <section class="question-container">
        <div class="question__header">
          <div class="question__title">{{ question.title }}</div>
          <div class="question__date">{{ getTimeFormat(question.create_time) }}</div>
        </div>
        <div v-if="question.created_by.username===user.username || isAdminRole" class="question-nav">
          <span class="question-nav__button">
            <b-icon icon="circle-fill" scale="0.4"/>
            <span style="cursor: pointer" @click="showEditQuestionDialog = true">Edit</span>
            <b-icon icon="circle-fill" scale="0.4" style="margin-left: 3px;"/>
            <span style="cursor: pointer" @click="showDeleteQuestionDialog = true">Delete</span>
          </span>
          <b-form-checkbox v-model="resolveStatus" switch>
            <b-badge
              variant="light"
              id="question-badge"
            >
              <b-icon icon="circle-fill" :color="getColor(question.is_open)"/>
              {{ getStatus(question.is_open) }}
            </b-badge>
          </b-form-checkbox>
        </div>
        <div v-else class="question-status">
          <b-badge
            variant="light"
            id="question-badge-only"
          >
            <b-icon icon="circle-fill" :color="getColor(question.is_open)"/>
            {{ getStatus(question.is_open) }}
          </b-badge>
        </div>
        <div class="question__content">
          <p v-dompurify-html="question.content"/>
        </div>
      </section>

      <section class="answer-container">
        <div class="answer-enter">
          <b-form-textarea
            class="answer-enter__text"
            v-model="answerContent"
            no-resize
            size="lg"
          ></b-form-textarea>
          <b-button class="answer-enter__btn" @click="createAnswer">등록</b-button>
        </div>
      </section>

      <div v-for="i in answers" :key="i">
        <section class="answer-container">
          <div class="answer-registered">
            <div class="answer-registered__header">
              <span class="answer-registered__by">{{ i.name }}</span>
              <b-badge
                id="answer-usertype"
                pill
              >
                {{ i.admin_type }}
              </b-badge>
              <span class="answer-registered__date">{{ getTimeFormat(i.last_update_time) }}</span>
              <span v-if="i.name===user.username || isAdminRole">
                <span class="answer-registered__button">
                  <b-icon icon="circle-fill" scale="0.4"/>
                  <span style="cursor: pointer" @click="goEditAnswer(i.id)">Edit</span>
                  <b-icon icon="circle-fill" scale="0.4" style="margin-left: 3px;"/>
                  <span style="cursor: pointer" @click="showDeleteAnswer(i.id)">Delete</span>
                </span>
              </span>
            </div>
            <p class="answer-registered__content">{{ i.content }}</p>
          </div>
          <div v-if="showEditAnswerDialog === true && editAnswer.id === i.id">
            <div class="answer-enter">
              <b-form-textarea
                class="answer-enter__text"
                v-model="editAnswer.content"
                no-resize
                size="lg"
              ></b-form-textarea>
              <b-button class="answer-enter__btn" @click="showEditAnswer">수정</b-button>
            </div>
          </div>
        </section>
      </div>

      <b-modal
        centered
        v-model="showEditQuestionDialog"
        title="Edit Question"
        size="lg"
      >
        <div class="modal-content">
          <b-form-group
            id="question-title"
            label="Title"
            label-for="title"
          >
            <b-form-input
              v-model="editQuestionTitle"
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
              v-model="editQuestionContent"
              placeholder="Content"
              rows="6"
              max-rows="6"
              required
              no-resize
            ></b-form-textarea>
          </b-form-group>
        </div>
        <template #modal-footer>
          <b-button style="cursor: pointer" @click="cancelEditQuestion">Cancel</b-button>
          <b-button @click="editQuestion">Save</b-button>
        </template>
      </b-modal>
      <b-modal
        centered
        v-model="showDeleteQuestionDialog"
        @ok="deleteQuestion"
      >
        Are you sure you want to delete this question? :o
      </b-modal>
      <b-modal
        centered
        v-model="showDeleteAnswerDialog"
        @ok="deleteAnswer"
      >
        Are you sure you want to delete this answer? :o
      </b-modal>
    </article>
  </div>
</template>

<script>
import sidemenu from '@oj/components/Sidemenu.vue'
import api from '@oj/api'
// import moment from 'moment'
import time from '@/utils/time'
import { mapGetters } from 'vuex'

export default {
  name: 'CourseQnaDetail',
  components: {
    sidemenu
  },
  data () {
    return {
      answers: {},
      resolveStatus: false,
      question: {},
      course_id: 1,
      answerContent: '',
      editAnswer: {},
      toDelete: 1,
      question_id: 1,
      editQuestionContent: '',
      editQuestionTitle: '',
      showEditQuestionDialog: false,
      showDeleteQuestionDialog: false,
      showDeleteAnswerDialog: false,
      showEditAnswerDialog: false
    }
  },
  async mounted () {
    this.course_id = this.$route.params.courseID
    this.question_id = this.$route.params.questionID
    this.getQuestion()
    this.getAnswerList()
  },
  methods: {
    async getQuestion () {
      const params = {
        course_id: this.course_id,
        question_id: this.question_id
      }
      const res = await api.getQuestionList(params)
      this.question = res.data.data
      this.editQuestionContent = this.question.content
      this.editQuestionTitle = this.question.title
    },
    async editQuestion () {
      const data = {
        id: this.question.id,
        title: this.editQuestionTitle,
        content: this.editQuestionContent,
        is_open: this.question.is_open
      }
      const res = await api.updateQuestion(data)
      this.question = res.data.data
      this.showEditQuestionDialog = false
    },
    async deleteQuestion () {
      const params = {
        course_id: this.course_id,
        question_id: this.question_id
      }
      await api.deleteQuestion(params)
      await this.$router.push({ name: 'lecture-qna', params: { courseID: this.course_id } })
    },
    cancelEditQuestion () {
      this.showEditQuestionDialog = false
      this.editQuestionContent = this.question.content
      this.editQuestionTitle = this.question.title
    },
    async getAnswerList () {
      const res = await api.getAnswerList({ question_id: this.question_id })
      this.answers = res.data.data
    },
    async showDeleteAnswer (id) {
      this.toDelete = id
      this.showDeleteAnswerDialog = true
    },
    async deleteAnswer () {
      await api.deleteAnswer({ id: this.toDelete })
      this.showDeleteAnswerDialog = false
      this.getAnswerList()
    },
    async createAnswer () {
      const data = {
        question_id: this.question_id,
        content: this.answerContent,
        closure: false
      }
      await api.createAnswer(data)
      this.answerContent = ''
      this.getAnswerList()
    },
    goEditAnswer (id) {
      if (!this.showEditAnswerDialog) {
        this.showEditAnswerDialog = true
        const newans = this.answers.find(ans => {
          if (id === ans.id) { return ans }
        })
        this.editAnswer = JSON.parse(JSON.stringify(newans))
      } else {
        this.showEditAnswerDialog = false
      }
    },
    async showEditAnswer () {
      this.showEditAnswerDialog = false
      const data = {
        id: this.editAnswer.id,
        content: this.editAnswer.content
      }
      await api.updateAnswer(data)
      const res = await api.getAnswerList({ question_id: this.question_id })
      this.answers = res.data.data
      this.editAnswer = {}
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-MM-DD HH:mm')
    },
    getColor (value) {
      if (value) {
        return '#D75B66'
      } else {
        return '#8DC63F'
      }
    },
    getStatus (value) {
      if (value) {
        return 'Not resolved'
      } else {
        return 'Resolved'
      }
    },
    async updateStatus () {
      const data = {
        id: this.question.id,
        title: this.editQuestionTitle,
        content: this.editQuestionContent,
        is_open: !this.question.is_open
      }
      await api.updateQuestion(data)
      this.getQuestion()
    }
  },
  computed: {
    ...mapGetters(['user', 'isAdminRole'])
  },
  watch: {
    resolveStatus () {
      this.updateStatus()
    }
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }

  .lecture-qna-card{
    margin: 30px auto 0 auto;
    width: 70%;
    font-family: Manrope_bold;
  }

  .question-container {
    width: 90%;
    margin: 0 auto;
  }
  .question__header{
    overflow: hidden;
    background: #F9F9F9;
    border-top: 2px solid #7C7C7C;
    border-bottom: 1px solid #B8B8B8;
    color: #7C7C7C;
    display: flex;
    justify-content: space-between;
    & .question__title{
      margin: 10px 1rem;
      font-size: 18px;
      font-weight: 700;
    }
    & .question__date{
      margin: auto 1rem;
      font-size: 14px;
      font-weight: 400;
      //text-align: right;
    }
  }
  .question-nav {
    color: #7c7c7c;
    font-size: 12px;
    margin: 10px;
    display: flex;
    justify-content: space-between;
    &__status {
      display: flex;
    }
    #question-badge{
      padding: 6px 6px;
      border: 1px solid #EDECEC;
      color: #7C7A7B !important;
    }
  }
  .question-status {
    font-size: 12px;
    margin: 10px;
    display: flex;
    justify-content: flex-end;
    #question-badge-only{
      padding: 6px 6px;
      border: 1px solid #EDECEC;
      color: #7C7A7B;
    }

  }
  .question__content{
    @import '@/styles/tiptapview.scss';
    margin: 50px 1rem 60px;
    color: #4f4f4f;
  }

  .answer-container{
    width: 90%;
    margin: 0 auto;
    border-radius: 5px;
    padding: 30px;
    background-color: #EDECEC;
    color: #4f4f4f;
    font-size: 12px;
    font-weight: 700;
  }
  .answer-registered {
    padding: 0 10px 30px;
    border-bottom: 1px solid #C4C4C4;
    &__header {
      margin-bottom: 10px;
    }
    &__by {
      font-size: 14px;
      margin-right: 5px;
    }
    #answer-usertype{
      padding: 3px 6px;
      margin-right: 5px;
      font-size: 8px;
      font-weight: 400;
    }
    &__date, &__button{
      color: #AAAAAA;
      font-weight: 400;
    }
    &__content{
      margin: 0;
    }
  }

  .answer-enter {
    display: flex;
    height: 60px;
    &__text ::v-deep {
      box-shadow: none;
      border: 1px solid #C4C4C4;
      border-radius: 0px;
      font-size: 14px;
      margin: 0;
      width: calc(100% - 60px);
    }
    &__text:focus, __text:active ::v-deep{
      box-shadow: none;
      border: 1px solid #C4C4C4;
    }
    &__btn ::v-deep {
      color: #4f4f4f;
      background-color: #c4c4c4;
      border-radius: 0px;
      width: 60px;
      font-size: 12px;
      font-weight: 700;
    }
    &__btn:hover, __btn:active ::v-deep{
      color: #fff;
      background-color: #7C7A7B;
    }
  }

  .modal-content::v-deep {
    width: 90%;
    margin: 0 auto;
  }
  .form-control {
    width: 100% !important;
  }
</style>
