<template>
  <b-form-gorup>
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
    <div v-html="text" />
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
