<template>
  <div>
    <div v-if="editor">
      <b-button-toolbar class="mb-1">
        <b-button-group class="mr-2">
          <b-button size="sm" title="Bold(Ctrl+B/Cmd+B)" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleBold().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('bold') }">
            <b-icon icon="type-bold"></b-icon>
          </b-button>
          <b-button size="sm" title="Italic(Ctrl+I/Cmd+i)" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleItalic().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('italic') }">
            <b-icon icon="type-italic"></b-icon>
          </b-button>
          <b-button size="sm" title="Strike" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleStrike().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('strike') }">
            <b-icon icon="type-strikethrough"></b-icon>
          </b-button>
          <b-button size="sm" title="Code" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleCode().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('code') }">
            <b-icon icon="code"></b-icon>
          </b-button>
          <b-button size="sm" title="Unset Marks" type="button" variant="outline-secondary" @click="editor.chain().focus().unsetAllMarks().run()">
            <b-icon icon="x-square"></b-icon>
          </b-button>
        </b-button-group>
        <div class="divider"></div>
        <b-button-group class="mx-2">
          <b-button size="sm" title="Heading 1" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" class="EditorButton" :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }">
            <b-icon icon="type-h1"></b-icon>
          </b-button>
          <b-button size="sm" title="Heading 2" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleHeading({ level: 4 }).run()" class="EditorButton" :class="{ 'is-active': editor.isActive('heading', { level: 4 }) }">
            <b-icon icon="type-h2"></b-icon>
          </b-button>
          <b-button size="sm" title="Paragraph" type="button" variant="outline-secondary" @click="editor.chain().focus().setParagraph().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('paragraph') }">
            <b-icon icon="paragraph"></b-icon>
          </b-button>
          <b-button size="sm" title="Bullet List" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleBulletList().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('bulletList') }">
            <b-icon icon="list-ul"></b-icon>
          </b-button>
          <b-button size="sm" title="Ordered List" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleOrderedList().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('orderedList') }">
            <b-icon icon="list-ol"></b-icon>
          </b-button>
          <b-button size="sm" name="Code Block" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleCodeBlock().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('codeBlock') }">
            <b-icon icon="code-square"></b-icon>
          </b-button>
        </b-button-group>
        <div class="divider"></div>
        <b-button-group class="mx-2">
          <b-button size="sm" title="Hard Break(Ctrl+Enter/Cmd+Enter)" type="button" variant="outline-secondary" @click="editor.chain().focus().setHardBreak().run()">
            <b-icon icon="arrow-return-left"></b-icon>
          </b-button>
          <b-button size="sm" title="Block Quote" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleBlockquote().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('blockquote') }">
            <b-icon icon="blockquote-left"></b-icon>
          </b-button>
          <b-button size="sm" title="Horizontal Rule" type="button" variant="outline-secondary" @click="editor.chain().focus().setHorizontalRule().run()">
            <b-icon icon="distribute-vertical"></b-icon>
          </b-button>
        </b-button-group>
        <div class="divider"></div>
        <b-button-group class="mx-2">
          <b-button size="sm" title="Undo" type="button" variant="outline-secondary" @click="editor.chain().focus().undo().run()">
            <b-icon icon="arrow-counterclockwise"></b-icon>
          </b-button>
          <b-button size="sm" title="Redo" type="button" variant="outline-secondary" @click="editor.chain().focus().redo().run()">
            <b-icon icon="arrow-clockwise"></b-icon>
          </b-button>
        </b-button-group>
        <div class="divider"></div>
        <b-button-group class="mx-2">
          <b-button size="sm" title="Link" type="button" variant="outline-secondary" :class="{ 'is-disabled': shouldDisableButton(editor.isActive('link')), 'is-active': editor.isActive('link') }"
                    @click.prevent="editor.isActive('link') ? editor.chain().focus().unsetLink() : addLinkDialog()">
            <b-icon icon="link"></b-icon>
          </b-button>
          <b-button size="sm" title="Upload Image" type="button" variant="outline-secondary" @click='openImageModal'>
            <b-icon icon="card-image"></b-icon>
          </b-button>
          <b-button size="sm" title="Upload File" type="button" variant="outline-secondary" @click='openFileModal'>
            <b-icon icon="file-earmark-arrow-up"></b-icon>
          </b-button>
        </b-button-group>
      </b-button-toolbar>
    </div>
    <bubble-menu :editor="editor" v-if="editor">
      <b-button size="sm" title="Bold(Ctrl+B/Cmd+B)" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleBold().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('bold') }">
        <b-icon icon="type-bold"></b-icon>
      </b-button>
      <b-button size="sm" title="Italic(Ctrl+I/Cmd+i)" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleItalic().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('italic') }">
        <b-icon icon="type-italic"></b-icon>
      </b-button>
      <b-button size="sm" title="Strike(Ctrl+B/Cmd+B)" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleStrike().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('strike') }">
        <b-icon icon="type-strikethrough"></b-icon>
      </b-button>
      <b-button size="sm" title="Code" type="button" variant="outline-secondary" @click="editor.chain().focus().toggleCode().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('code') }">
        <b-icon icon="code"></b-icon>
      </b-button>
      <b-button size="sm" title="Link" type="button" variant="outline-secondary" :class="{ 'is-disabled': shouldDisableButton(editor.isActive('link')), 'is-active': editor.isActive('link') }"
          @click.prevent="editor.isActive('link') ? editor.chain().focus().unsetLink() : addLinkDialog()">
        <b-icon icon="link"></b-icon>
      </b-button>
      <b-button size="sm" title="Unset Marks" type="button" variant="outline-secondary" @click="editor.chain().focus().unsetAllMarks().run()" class="EditorButton">
        <b-icon icon="x-square"></b-icon>
      </b-button>
    </bubble-menu>
    <editor-content :editor="editor" class="border" :data-cy="name"/>
    <b-modal id="image-modal" v-model="imageModal" max-width="540" title="Insert Image" hide-footer>
      <b-card class="pa-1">
        <b-tabs v-model="imageTab">
          <b-tab href="#Insert-With-URL" title="Insert With URL" active>
            <b-card-text class="mt-3 mb-3">
              <b-form-textarea v-model="fileURL" single-line label="Paste link here">
              </b-form-textarea>
            </b-card-text>
            <b-btn dark @click="insertImage(); $bvModal.hide('image-modal')" :class="{ 'is-disabled': fileURL === null }">
              Insert image
            </b-btn>
          </b-tab>
          <b-tab href="#Upload-From-Local" title="Upload From Local">
            <b-form-file class="mt-3 mb-3" v-model="selectedFile" accept="image/*" drop-placeholder="Drop a Image here" placeholder="Select a Image or Drop a file here" @input="uploadImage">
            </b-form-file>
            <b-btn :disabled="disableInsertImage" dark @click="insertImage(); $bvModal.hide('image-modal')" :class="{ 'is-disabled': selectedFile === null }">
              Insert image
            </b-btn>
          </b-tab>
        </b-tabs>
      </b-card>
    </b-modal>
    <b-modal id="file-modal" v-model="fileModal" max-width="540" title="Insert File" hide-footer>
      <b-card class="pa-1" >
        <b-form-file class="mb-3" v-model="selectedFile" accept="*" drop-placeholder="Drop a file here" placeholder="Select a file or Drop a file here" @input="uploadFile">
        </b-form-file>
        <b-btn :disabled="disableInsertFile" type="submit" dark @click="insertFile(); $bvModal.hide('file-modal')" :class="{ 'is-disabled': selectedFile === null }" >
          Insert File
        </b-btn>
      </b-card>
    </b-modal>
  </div>
</template>

<script>
import { Editor, EditorContent, BubbleMenu } from '@tiptap/vue-2'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import Link from '@tiptap/extension-link'
import api from '../api'
export default {
  components: {
    EditorContent,
    BubbleMenu
  },
  props: {
    value: {
      type: String,
      default: ''
    },
    name: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      editor: null,
      imageModal: false,
      imageTab: null,
      fileModal: false,
      fileURL: null,
      fileLink: null,
      selectedFile: null,
      disableInsertImage: true,
      disableInsertFile: true
    }
  },
  watch: {
    value (value) {
      if (this.editor.getHTML() === value) {
        return
      }
      this.editor.commands.setContent(this.value, false)
    }
  },
  mounted () {
    this.editor = new Editor({
      extensions: [
        StarterKit,
        Image,
        Link
      ],
      content: this.value,
      onUpdate: () => {
        this.$emit('input', this.editor.getHTML())
      }
    })
  },
  beforeDestroy () {
    this.editor.destroy()
  },
  methods: {
    openImageModal () {
      this.imageModal = true
    },
    openFileModal () {
      this.fileModal = true
    },
    shouldDisableButton (isActive) {
      return !isActive & window.getSelection().isCollapsed
    },
    async addLinkDialog () {
      if (window.getSelection().isCollapsed) {
        return
      }
      const res = await window.prompt('Add link', 'https://')
      if (res && res !== 'https://' && res !== 'http://') {
        this.editor.chain().focus().setLink({ href: res }).run()
      }
    },
    insertImage () {
      const url = this.fileURL
      if (url) {
        this.editor.chain().focus().setImage({ src: url }).run()
      }
      this.selectedFile = null
      this.fileURL = null
      this.imageModal = false
      this.disableInsertImage = true
    },
    async uploadImage () {
      const formData = new FormData()
      formData.append('image', this.selectedFile)
      if (this.selectedFile === null) {
        return
      }
      const res = await api.uploadImage(formData)
      this.fileURL = res.data.data.file_path
      this.disableInsertImage = false
    },
    insertFile () {
      this.editor.chain().focus().insertContent(this.fileLink).run()
      this.disableInsertFile = true
    },
    async uploadFile () {
      const formData = new FormData()
      formData.append('file', this.selectedFile)
      if (this.selectedFile == null) {
        return
      }
      const res = await api.uploadFile(formData)
      const link = '<a target="_blank" href="' + res.data.data.file_path + '">' + res.data.data.file_name + '</a>'
      this.fileLink = link
      this.disableInsertFile = false
    }
  }
}
</script>

<style lang="scss">

.EditorButton:not(.is-active) {
  background: white;
  color: gray;
}

.EditorButton.is-active {
  background: gray;
  color: white;
}
.divider {
  background-color: #bbbec4;
  margin-left: 0.5rem;
  margin-right: 0.5rem;
  width:2px;
}
.ProseMirror {
  padding: 1.25rem 1rem;

  > * + * {
    margin-top: 0.75em;
  }

  ul,
  ol {
    padding: 0 1rem;
  }

  p {
    line-height: 1.5;
  }

  h3,
  h4 {
    line-height: 1.1;
  }

  code {
    background-color: rgba(#616161, 0.1);
    color: #616161;
  }

  pre {
    background: #0D0D0D;
    color: #FFF;
    font-family: 'JetBrainsMono', monospace;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;

    code {
      color: inherit;
      padding: 0;
      background: none;
      font-size: 0.8rem;
    }
  }

  img {
    max-width: 100%;
    height: auto;

    &.ProseMirror-selectednode {
      outline: 3px solid #68CEF8;
    }
  }

  blockquote {
    padding-left: 1rem;
    border-left: 2px solid rgba(#0D0D0D, 0.1);
  }

  hr {
    border: none;
    border-top: 2px solid rgba(#0D0D0D, 0.1);
    margin: 2rem 0;
    &.ProseMirror-selectednode {
      outline: 3px solid #68CEF8;
    }
  }
}
</style>
