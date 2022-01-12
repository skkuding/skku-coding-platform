<template>
  <div>
    <Sidemenu/>
    <article class="lecture-qna-card">
      <section class="question-container">
        <div class="question__header">
          <div class="question__title">{{ question.title }}</div>
          <div class="question__date">{{ question.create_time }}</div>
        </div>
        <div class="question-nav">
          <div class="question-nav__button">
            <b-icon icon="circle-fill" scale="0.4"/>
            <span style="cursor: pointer" @click="showEditQuestion">Edit</span>
            <b-icon icon="circle-fill" scale="0.4" style="margin-left: 3px;"/>
            <span style="cursor: pointer" @click="showDeleteQuestion">Delete</span>
          </div>
          <div class="question-nav__status">
            <b-form-checkbox v-model="resolveStatus" switch/>
            <b-badge
              variant="light"
              id="question-badge"
            >
              <b-icon icon="circle-fill" :color="question.statuscolor"/>
              {{ question.status }}
            </b-badge>
          </div>
        </div>
        <div class="question__content">
          <p v-dompurify-html="question.content"/>
        </div>
      </section>

      <section class="answer-container">
        <div class="answer-registered">
          <div class="answer-registered__header">
            <span class="answer-registered__by">{{ answer.create_by }}</span>
            <b-badge
              id="answer-usertype"
              pill
            >
              Professor
            </b-badge>
            <span class="answer-registered__date">{{ answer.create_time }}</span>
            <span class="answer-registered__button">
              <b-icon icon="circle-fill" scale="0.4"/>
              <span style="cursor: pointer">Edit</span>
              <b-icon icon="circle-fill" scale="0.4" style="margin-left: 3px;"/>
              <span style="cursor: pointer" @click="showDeleteAnswer">Delete</span>
            </span>
          </div>
          <p class="answer-registered__content">{{ answer.content }}</p>
        </div>
        <div class="answer-enter">
          <b-form-textarea
            class="answer-enter__text"
            no-resize
            size="lg"
          ></b-form-textarea>
          <b-button class="answer-enter__btn">등록</b-button>
        </div>
      </section>

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
              v-model="question.title"
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
              v-model="question.content"
              placeholder="Content"
              rows="6"
              max-rows="6"
              required
              no-resize
            ></b-form-textarea>
          </b-form-group>
        </div>
        <template #modal-footer>
          <b-button @click="showEditQuestionDialog = false">Cancel</b-button>
          <b-button>Save</b-button>
        </template>
      </b-modal>
      <b-modal
        centered
        v-model="showDeleteQuestionDialog"
      >
        Are you sure you want to delete this question? :o
      </b-modal>
      <b-modal
        centered
        v-model="showDeleteAnswerDialog"
      >
        Are you sure you want to delete this answer? :o
      </b-modal>
    </article>
  </div>
</template>

<script>
import Sidemenu from '@oj/components/Sidemenu.vue'

export default {
  name: 'LectureQnaDetail',
  components: {
    Sidemenu
  },
  data () {
    return {
      resolveStatus: false,
      question: {
        id: '1',
        title: 'first',
        status: 'Resolved',
        statuscolor: '#8DC63F',
        create_time: '2021-08-09',
        content: 'first question content'
      },
      answer: {
        create_by: '김영훈',
        create_time: '2021-08-10 18:30',
        content: '이번엔 프로젝트로 진행합니다.'
      },
      showEditQuestionDialog: false,
      showDeleteQuestionDialog: false,
      showDeleteAnswerDialog: false
    }
  },
  async mounted () {
  },
  methods: {
    showEditQuestion () {
      this.showEditQuestionDialog = true
    },
    showDeleteQuestion () {
      this.showDeleteQuestionDialog = true
    },
    showDeleteAnswer () {
      this.showDeleteAnswerDialog = true
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
    margin: 30px auto 0 auto;
    width: 70%;
    font-family: Manrope_bold;
    .table{
      width: 95% !important;
      margin: 0 auto;
    }
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
      text-align: right;
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
