<template>
  <b-form-group>
    <p class="labels text-center">
      Put LaTeX in the following format to use LaTeX in our editor.<br/>
    \( ... \), $$ ... $$, \[ ... \]<br/>
    For example, \( \pm\sqrt{a^2 + b^2}  \) or $$ \pm\sqrt{a^2 + b^2} $$
    </p>
    <p class="labels">
      Input
    </p>
    <b-form-textarea
      v-model="input"
      style="margin-bottom: 24px"
      rows="4"
    >
    </b-form-textarea>
    <p class="labels">
      Output
    </p>
    <katex-element :expression="this.input" :throw-on-error="false" />
  </b-form-group>
</template>

<script>
export default {
  name: '',
  data () {
    return {
      input: 'c = \\pm\\sqrt{a^2 + b^2}'
    }
  }
}
</script>

<style scoped>
  .labels {
    margin-bottom: 24px;
  }
</style>
