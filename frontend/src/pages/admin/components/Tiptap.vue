<template>
  <div>
    <div v-if="editor">
      <b-button-toolbar>
        <b-button-group>
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().toggleBold().run()" :class="{ 'is-active': editor.isActive('bold') }">
            <b-icon icon="type-bold" aria-hidden="true"></b-icon>
          </b-button>
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().toggleItalic().run()" :class="{ 'is-active': editor.isActive('italic') }">
            <b-icon icon="type-italic" aria-hidden="true"></b-icon>
          </b-button>
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().toggleStrike().run()" :class="{ 'is-active': editor.isActive('strike') }">
            <b-icon icon="type-strikethrough" aria-hidden="true"></b-icon>
          </b-button>
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().toggleCode().run()" :class="{ 'is-active': editor.isActive('code') }">
            <b-icon icon="code" aria-hidden="true"></b-icon>
          </b-button>
        </b-button-group>
        <b-button-group >
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().setParagraph().run()" :class="{ 'is-active': editor.isActive('paragraph') }">
            <b-icon icon="paragraph" aria-hidden="true"></b-icon>
          </b-button>
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }">
            <b-icon icon="type-h1" aria-hidden="true"></b-icon>
          </b-button>
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }">
            <b-icon icon="type-h2" aria-hidden="true"></b-icon>
          </b-button>
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }">
            <b-icon icon="type-h3" aria-hidden="true"></b-icon>
          </b-button>
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'is-active': editor.isActive('bulletList') }">
            <b-icon icon="list-ul" aria-hidden="true"></b-icon>
          </b-button>
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().toggleOrderedList().run()" :class="{ 'is-active': editor.isActive('orderedList') }">
            <b-icon icon="list-ol" aria-hidden="true"></b-icon>
        </b-button>
        </b-button-group>
        <b-button-group >
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().toggleCodeBlock().run()" :class="{ 'is-active': editor.isActive('codeBlock') }">
            <b-icon icon="code-square" aria-hidden="true"></b-icon>
          </b-button>
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().toggleBlockquote().run()" :class="{ 'is-active': editor.isActive('blockquote') }">
            <b-icon icon="blockquote-left" aria-hidden="true"></b-icon>
          </b-button>
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().setHorizontalRule().run()">
            <b-icon icon="distribute-horizontal" aria-hidden="true"></b-icon>
          </b-button>
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().undo().run()">
            <b-icon icon="arrow-counterclockwise" aria-hidden="true"></b-icon>
          </b-button>
          <b-button type="button" variant="outline-dark" @click="editor.chain().focus().redo().run()">
            <b-icon icon="arrow-clockwise" aria-hidden="true"></b-icon>
          </b-button>
        </b-button-group>
      </b-button-toolbar>
    </div>
    <editor-content :editor="editor" />
  </div>
</template>

<script>
import { Editor, EditorContent } from '@tiptap/vue-2'
import StarterKit from '@tiptap/starter-kit'

export default {
  components: {
    EditorContent
  },
  props: {
    value: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      editor: null
    }
  },
  watch: {
    value (value) {
      const isSame = this.editor.getHTML() === value
      if (isSame) {
        return
      }
      this.editor.commands.setContent(this.value, false)
    }
  },
  mounted () {
    this.editor = new Editor({
      extensions: [
        StarterKit
      ],
      content: this.value,
      onUpdate: () => {
        this.$emit('input', this.editor.getHTML())
      }
    })
  },

  beforeDestroy () {
    this.editor.destroy()
  }
}
</script>
