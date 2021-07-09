<template>
  <pre v-highlight="code"><code
:class="language"
                                :style="styleObject"
  /></pre>
</template>

<script>
export default {
  name: 'Highlight',
  props: {
    language: {
      type: String
    },
    code: {
      required: true,
      type: String
    },
    borderColor: {
      type: String,
      default: 'green'
    }
  },
  data () {
    return {
      styleObject: {
        'border-left': '2px solid green'
      }
    }
  },
  watch: {
    'borderColor' (newVal, oldVal) {
      this.styleObject['border-left'] = '2.5px solid ' + newVal
    }
  }
}
</script>

<style lang="scss" scoped>
  pre {
    padding: 0;
    display: block;
    code {
      padding: 20px;
      font-size: 1.1em;
    }
  }
</style>
