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
    languages: {
      type: Array,
      default: () => {
        return ['C', 'C++', 'Java', 'Python2']
      }
    },
    language: {
      type: String,
      default: 'C++'
    },
    theme: {
      type: String,
      default: 'solarized'
    },
    bus: Object
  },
  data () {
    return {
      options: {
        // codemirror options
        tabSize: 4,
        mode: 'text/x-csrc',
        theme: 'solarized',
        lineNumbers: true,
        line: true,
        // code folding
        foldGutter: true,
        gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
        // selected text auto highlighting
        styleSelectedText: true,
        lineWrapping: true,
        highlightSelectionMatches: { showToken: /\w/, annotateScrollbar: true }
      },
      mode: {
        'C++': 'text/x-csrc'
      },
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

    this.bus.$on('changeLang', this.onChangeLang)
    this.bus.$on('changeTheme', this.onChangeTheme)
    this.bus.$on('uploadFile', this.onUploadFile)
    this.bus.$on('uploadFileDone', this.onUploadFileDone)
  },
  methods: {
    onEditorCodeChange (newCode) {
      this.$emit('update:value', newCode)
    },
    onChangeLang (newVal) {
      this.editor.setOption('mode', this.mode[newVal])
    },
    onChangeTheme (newTheme) {
      this.editor.setOption('theme', newTheme)
    },
    onUploadFile () {
      document.getElementById('file-uploader').click()
    },
    onUploadFileDone () {
      const f = document.getElementById('file-uploader').files[0]
      const fileReader = new window.FileReader()
      const self = this
      fileReader.onload = function (e) {
        const text = e.target.result
        self.editor.setValue(text)
        document.getElementById('file-uploader').value = ''
      }
      fileReader.readAsText(f, 'UTF-8')
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

<style>
  .CodeMirror {
    height: 100% !important;
  }
  .CodeMirror-scroll {
    min-height: 300px;
    max-height: 100%;
  }
</style>
