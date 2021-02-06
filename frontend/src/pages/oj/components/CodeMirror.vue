<template>
  <div style="margin: 0px 0px 15px 0px">
    <Row
      type="flex"
      justify="space-between"
      class="header"
    >
      <Col :span="12">
      <div>
        <span>{{ $t('m.Language') }}:</span>
        <Select
          :value="language"
          class="adjust"
          @on-change="onLangChange"
        >
          <Option
            v-for="item in languages"
            :key="item"
            :value="item"
          >
            {{ item }}
          </Option>
        </Select>

        <Tooltip
          :content="this.$i18n.t('m.Reset_to_default_code_definition')"
          placement="top"
          style="margin-left: 10px"
        >
          <Button
            icon="refresh"
            @click="onResetClick"
          />
        </Tooltip>

        <Tooltip
          :content="this.$i18n.t('m.Upload_file')"
          placement="top"
          style="margin-left: 10px"
        >
          <Button
            icon="upload"
            @click="onUploadFile"
          />
        </Tooltip>

        <input
          id="file-uploader"
          type="file"
          style="display: none"
          @change="onUploadFileDone"
        >
      </div>
      </Col>
      <Col :span="12">
      <div class="fl-right">
        <span>{{ $t('m.Theme') }}:</span>
        <Select
          :value="theme"
          class="adjust"
          @on-change="onThemeChange"
        >
          <Option
            v-for="item in themes"
            :key="item.label"
            :value="item.value"
          >
            {{ item.label }}
          </Option>
        </Select>
      </div>
      </Col>
    </Row>
    <codemirror
      ref="myEditor"
      :value="value"
      :options="options"
      @change="onEditorCodeChange"
    />
  </div>
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
    }
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
        // 代码折叠
        foldGutter: true,
        gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
        // 选中文本自动高亮，及高亮方式
        styleSelectedText: true,
        lineWrapping: true,
        highlightSelectionMatches: { showToken: /\w/, annotateScrollbar: true }
      },
      mode: {
        'C++': 'text/x-csrc'
      },
      themes: [
        { label: this.$i18n.t('m.Monokai'), value: 'monokai' },
        { label: this.$i18n.t('m.Solarized_Light'), value: 'solarized' },
        { label: this.$i18n.t('m.Material'), value: 'material' }
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
  },
  methods: {
    onEditorCodeChange (newCode) {
      this.$emit('update:value', newCode)
    },
    onLangChange (newVal) {
      this.editor.setOption('mode', this.mode[newVal])
      this.$emit('changeLang', newVal)
    },
    onThemeChange (newTheme) {
      this.editor.setOption('theme', newTheme)
      this.$emit('changeTheme', newTheme)
    },
    onResetClick () {
      this.$emit('resetCode')
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
  .header {
    margin: 5px 5px 15px 5px;
    .adjust {
      width: 150px;
      margin-left: 10px;
    }
    .fl-right {
      float: right;
    }
  }
</style>

<style>
  .CodeMirror {
    height: auto !important;
  }
  .CodeMirror-scroll {
    min-height: 300px;
    max-height: 1000px;
  }
</style>
