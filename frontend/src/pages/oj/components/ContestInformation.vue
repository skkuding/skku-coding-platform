<template>
  <div class="contest-information-container">
    <h2 class="title">{{ title }}</h2>
    <div class="summary">
      <div class="summary-contents-container">
        <h3 class="subtitle">Requirements</h3>
        <div class="summary-content-row">
          <div class="summary-content-col">
            <div class="requirement" v-for="(requirement, index) of requirements" :key="index">{{requirement}}</div>
            <div class="constraint" v-for="(constraint, index) of constraints" :key="index">{{constraint}}></div>
          </div>
        </div>
        </div>
      <div class="summary-contents-container">
        <h3 class="subtitle">Scoring</h3>
        <div class="summary-content-row">
          <div class="summary-content-col">
            <div class="scoring">{{ scoring }}</div>
          </div>
        </div>
      </div>
      <div class="summary-contents-container">
        <h3 class="subtitle">Prize</h3>
        <div class="summary-content-row">
          <div class="summary-content-col">
            <div class="prize-col" v-for="(prize, index) of prizes" :key="index" :style="'color: ' + prize.color + ';'" >
              <b-icon-circle-fill class="mr-2" :color="prize.color" width="1.3rem" height="1.3rem"></b-icon-circle-fill>
              <div>{{ prize.name }}</div>
              <div class="line"></div>
              <div>{{ prize.reward }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="description-container">
      <h3 class="subtitle">Description</h3>
      <div class="description" v-dompurify-html="description"></div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'ContestInformation',
  props: {
    title: {
      type: String,
      required: true
    },
    requirements: {
      type: Array,
      required: true
    },
    constraints: {
      type: Array,
      required: true
    },
    scoring: {
      type: String,
      required: true
    },
    prizes: {
      type: Array,
      required: true
    },
    description: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      // title: '2021 Spring SKKU 프로그래밍 대회 in 소프트의 밤',
      // requirements: [
      //   'SKKU undergrate enrolled 2021 Spring'
      // ],
      // constraints: [
      //   'Not Awarded in same past competition'
      // ],
      // scoring: 'ACM-ICPC style',
      // prizes: [
      //   {
      //     color: '#FF6663',
      //     name: 'Top 2',
      //     reward: '1,000,000 Won'
      //   },
      //   {
      //     color: '#FFD700',
      //     name: '3(3~5)',
      //     reward: '500,000 Won'
      //   },
      //   {
      //     color: '#C0C0C0',
      //     name: '5(6~10)',
      //     reward: '100,000 Won'
      //   },
      //   {
      //     color: '#CD7F32',
      //     name: '10(11~20)',
      //     reward: '50,000 Won'
      //   }
      // ],
      // description: `
      // <p data-v-5ab32299="" class="contest-tab-description"><p>Description</p><p>dd</p><p>dd</p><p>ee</p><p>eee</p></p>
      // `
    }
  },
  methods: {
  },
  computed: {
  },
  watch: {
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../fonts/Manrope-Bold.ttf');
  }
  .contest-information-container {
    display: flex;
    width: 100%;
    max-width: 100%;
    justify-content: space-around;
    align-items: flex-start;
    flex-flow: row wrap;
    font-family: Manrope_bold;
    .title {
      font-size: 2rem;
      text-align: center;
    }

    .summary {
      display: flex;
      width: 100%;
      margin: 2rem 4rem;
      justify-content: space-around;
      align-items: center;
      flex-wrap: wrap;
      flex-grow: 1;
      .summary-contents-container {
        display: flex;
        flex-direction: column;
        border-left: #BCBCBC 1px solid;
        padding: 0 1rem 0 1rem;
        flex: 1 0 20rem;
        min-height: 10rem;
        margin-bottom: 1rem;
        .requirement {
          color: #8DC63F;
          font-size: 1rem;
          margin-bottom: 1rem;
        }
        .constraint {
          color: #FF6663;
          font-size: 1rem;
          margin-bottom: 1rem;
        }
        .scoring {
          color: #8DC63F;
          font-size: 1.2rem;
        }
        .summary-content-row {
          display: flex;
          flex-direction: row;
          justify-content: flex-start;
          margin: auto 0;
          .summary-content-col {
            display: flex;
            flex-direction: column;
            justify-content: space-evenly;
            align-items: stretch;
            flex: 1
          }
          .prize-col {
            display: flex;
            flex-direction: row;
            justify-content: stretch;
            align-items: center;
            flex: 1;
            margin-bottom: 0.5rem;
            .circle {
              width: 4rem;
              height: 4rem;
              border-radius: 50%;
            }
            .line {
              flex: 1 0 1rem;
              margin: 0 1.5rem;
              height: 1px;
              background-color:#BCBCBC;
            }
          }
        }
      }
    }
    .description-container {
      display: flex;
      flex-direction: column;
      flex: 1 0 20rem;
      width: 100%;
      align-items: flex-start;
      margin: 2rem 4rem;
    }
  }
  .subtitle {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
</style>
