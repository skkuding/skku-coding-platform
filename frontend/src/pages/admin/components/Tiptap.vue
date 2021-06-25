<template>
  <div>
    <div v-if="editor">
      <div>
        <b-button type="button" @click="editor.chain().focus().toggleBold().run()" :class="{ 'is-active': editor.isActive('bold') }">
          <b-icon icon="type-bold"></b-icon>
        </b-button>
        <b-button type="button" @click="editor.chain().focus().toggleItalic().run()" :class="{ 'is-active': editor.isActive('italic') }">
          <b-icon icon="type-italic"></b-icon>
        </b-button>
        <b-button type="button" @click="editor.chain().focus().toggleStrike().run()" :class="{ 'is-active': editor.isActive('strike') }">
          <b-icon icon="type-strikethrough"></b-icon>
        </b-button>
        <b-button type="button" @click="editor.chain().focus().toggleCode().run()" :class="{ 'is-active': editor.isActive('code') }">
          <b-icon icon="code"></b-icon>
        </b-button>
        <button type="button" @click="editor.chain().focus().unsetAllMarks().run()">
          clear marks
        </button>
        <button type="button" @click="editor.chain().focus().clearNodes().run()">
          clear nodes
        </button>
        <button type="button" @click="editor.chain().focus().setParagraph().run()" :class="{ 'is-active': editor.isActive('paragraph') }">
          paragraph
        </button>
        <button type="button" @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }">
          h1
        </button>
        <button type="button" @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }">
          h2
        </button>
        <button type="button" @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }">
          h3
        </button>
        <button type="button" @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'is-active': editor.isActive('bulletList') }">
          bullet list
        </button>
        <button type="button" @click="editor.chain().focus().toggleOrderedList().run()" :class="{ 'is-active': editor.isActive('orderedList') }">
          ordered list
        </button>
        <button type="button" @click="editor.chain().focus().toggleCodeBlock().run()" :class="{ 'is-active': editor.isActive('codeBlock') }">
          code block
        </button>
        <button type="button" @click="editor.chain().focus().toggleBlockquote().run()" :class="{ 'is-active': editor.isActive('blockquote') }">
          blockquote
        </button>
        <button type="button" @click="editor.chain().focus().setHorizontalRule().run()">
          horizontal rule
        </button>
        <button type="button" @click="editor.chain().focus().setHardBreak().run()">
          hard break
        </button>
        <button type="button" @click="editor.chain().focus().undo().run()">
          undo
        </button>
        <button type="button" @click="editor.chain().focus().redo().run()">
          redo
        </button>
      </div>
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
      // HTML
      const isSame = this.editor.getHTML() === value

      // JSON
      // const isSame = this.editor.getJSON().toString() === value.toString()

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
        // HTML
        this.$emit('input', this.editor.getHTML())

        // JSON
        // this.$emit('input', this.editor.getJSON())
      }
    })
  },

  beforeDestroy () {
    this.editor.destroy()
  }
}
</script>
