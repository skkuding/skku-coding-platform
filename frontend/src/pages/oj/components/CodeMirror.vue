<template>
  <codemirror
    id="codemirror"
    ref="myEditor"
    :value="value"
    :options="options"
    @change="onEditorCodeChange"
  />
</template>
<script>
import utils from '@/utils/utils'
import { codemirror } from 'vue-codemirror-lite'

// theme
import 'codemirror/theme/monokai.css'
import 'codemirror/theme/solarized.css'
import 'codemirror/theme/material.css'

// mode
import 'codemirror/mode/clike/clike.js'
import 'codemirror/mode/python/python.js'

// active-line.js
import 'codemirror/addon/selection/active-line.js'

// foldGutter
import 'codemirror/addon/fold/foldgutter.css'
import 'codemirror/addon/fold/foldgutter.js'
import 'codemirror/addon/fold/brace-fold.js'
import 'codemirror/addon/fold/indent-fold.js'

export default {
  name: 'CodeMirror',
  components: {
    codemirror
  },
  props: {
    value: {
      type: String,
      default: ''
    },
    language: {
      type: String,
      default: 'C++'
    },
    theme: {
      type: String,
      default: 'material'
    },
    readOnly: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      options: {
        // codemirror options
        tabSize: 4,
        mode: 'text/x-csrc',
        theme: 'material',
        lineNumbers: true,
        line: true,
        // code folding
        foldGutter: true,
        gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
        // selected text auto highlighting
        styleSelectedText: true,
        lineWrapping: true,
        highlightSelectionMatches: { showToken: /\w/, annotateScrollbar: true },
        readOnly: this.readOnly
      },
      mode: {},
      themes: [
        { label: 'Monokai', value: 'monokai' },
        { label: 'm.Solarized_Light', value: 'solarized' },
        { label: 'm.Material', value: 'material' }
      ]
    }
  },
  computed: {
    editor () {
      // get current editor object
      return this.$refs.myEditor.editor
    }
  },
  watch: {
    'theme' (newVal, oldVal) {
      this.editor.setOption('theme', newVal)
    },
    'language' (newVal, oldVal) {
      this.editor.setOption('mode', this.mode[newVal])
    }
  },
  mounted () {
    utils.getLanguages().then(languages => {
      const mode = {}
      languages.forEach(lang => {
        mode[lang.name] = lang.content_type
      })
      this.mode = mode
      this.editor.setOption('mode', this.mode[this.language])
    })
    this.editor.focus()
  },
  methods: {
    onEditorCodeChange (newCode) {
      this.$emit('update:value', newCode)
    }
  }
}
</script>

<style lang="less" scoped>
  #codemirror {
    width: 100%;
    height: 100%;
  }
</style>
