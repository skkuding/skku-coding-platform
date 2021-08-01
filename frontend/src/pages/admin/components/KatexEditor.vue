<template>
  <b-form-gorup>
    에디터에서 LaTeX를 사용하시려면 \( \pm\sqrt{a^2 + b^2}  \) 과 같이 \( 와  \) 사이에 넣어주세요.
    To use LaTeX in our editor, put LaTeX text between \( and \).
    For example, \( \pm\sqrt{a^2 + b^2}  \)
    <p class="labels">
      Input
    </p>
    <b-form-textarea
      v-model="input"
      style="margin-bottom: 24px"
      @keyup.enter.native="changeInput"
      rows="4"
    >
    </b-form-textarea>

    <p class="labels">
      Output
    </p>
    <div v-dompurify-html="text" />
  </b-form-gorup>
</template>

<script>
import katex from 'katex'
export default {
  name: '',
  data () {
    return {
      input: 'c = \\pm\\sqrt{a^2 + b^2}',
      text: ''
    }
  },
  mounted () {
    this.text = this.renderTex(this.input)
  },
  methods: {
    renderTex (data) {
      return katex.renderToString(data, {
        displayMode: true,
        throwOnError: false
      })
    },
    changeInput () {
      try {
        this.text = this.renderTex(this.input)
      } catch (e) {
        this.text = '<p style="text-align: center"><span style="color:red">Error Input</span></p>'
      }
    }
  },
  watch: {
    'input' () {
      this.changeInput()
    }
  }
}
</script>

<style scoped>
  .labels {
    margin-bottom: 24px;
  }
</style>
