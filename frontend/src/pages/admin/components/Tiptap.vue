<template>
  <div>
    <div v-if="editor">
      <b-button-toolbar class="mb-1">
        <b-button-group class="mr-2">
          <b-button size="sm" title="Bold(Ctrl+B/Cmd+B)" type="button" variant="outline-dark" @click="editor.chain().focus().toggleBold().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('bold') }">
            <b-icon icon="type-bold" aria-hidden="true"></b-icon>
          </b-button>
          <b-button size="sm" title="Italic(Ctrl+I/Cmd+i)" type="button" variant="outline-dark" @click="editor.chain().focus().toggleItalic().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('italic') }">
            <b-icon icon="type-italic" aria-hidden="true"></b-icon>
          </b-button>
          <b-button size="sm" title="Strike(Ctrl+B/Cmd+B)" type="button" variant="outline-dark" @click="editor.chain().focus().toggleStrike().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('strike') }">
            <b-icon icon="type-strikethrough" aria-hidden="true"></b-icon>
          </b-button>
          <b-button size="sm" title="Code" type="button" variant="outline-dark" @click="editor.chain().focus().toggleCode().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('code') }">
            <b-icon icon="code" aria-hidden="true"></b-icon>
          </b-button>
        </b-button-group>
        <div class="divider"></div>
        <b-button-group class="mx-2">
          <b-button size="sm" title="Heading 3" type="button" variant="outline-dark" @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" class="EditorButton" :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }">
            <b-icon icon="type-h1" aria-hidden="true"></b-icon>
          </b-button>
          <b-button size="sm" title="Heading 4" type="button" variant="outline-dark" @click="editor.chain().focus().toggleHeading({ level: 4 }).run()" class="EditorButton" :class="{ 'is-active': editor.isActive('heading', { level: 4 }) }">
            <b-icon icon="type-h2" aria-hidden="true"></b-icon>
          </b-button>
          <b-button size="sm" title="Paragraph" type="button" variant="outline-dark" @click="editor.chain().focus().setParagraph().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('paragraph') }">
            <b-icon icon="paragraph" aria-hidden="true"></b-icon>
          </b-button>
          <b-button size="sm" title="Bullet List" type="button" variant="outline-dark" @click="editor.chain().focus().toggleBulletList().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('bulletList') }">
            <b-icon icon="list-ul" aria-hidden="true"></b-icon>
          </b-button>
          <b-button size="sm" title="Ordered List" type="button" variant="outline-dark" @click="editor.chain().focus().toggleOrderedList().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('orderedList') }">
            <b-icon icon="list-ol" aria-hidden="true"></b-icon>
          </b-button>
          <b-button size="sm" name="Code Block" type="button" variant="outline-dark" @click="editor.chain().focus().toggleCodeBlock().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('codeBlock') }">
            <b-icon icon="code-square" aria-hidden="true"></b-icon>
          </b-button>
        </b-button-group>
        <div class="divider"></div>
        <b-button-group class="mx-2">
          <b-button size="sm" title="Block Quote" type="button" variant="outline-dark" @click="editor.chain().focus().toggleBlockquote().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('blockquote') }">
            <b-icon icon="blockquote-left" aria-hidden="true"></b-icon>
          </b-button>
          <b-button size="sm" title="Horizontal Rule" type="button" variant="outline-dark" @click="editor.chain().focus().setHorizontalRule().run()">
            <b-icon icon="distribute-vertical" aria-hidden="true"></b-icon>
          </b-button>
        </b-button-group>
        <div class="divider"></div>
        <b-button-group class="mx-2">
          <b-button size="sm" title="Undo" type="button" variant="outline-dark" @click="editor.chain().focus().undo().run()">
            <b-icon icon="arrow-counterclockwise" aria-hidden="true"></b-icon>
          </b-button>
          <b-button size="sm" title="Redo" type="button" variant="outline-dark" @click="editor.chain().focus().redo().run()">
            <b-icon icon="arrow-clockwise" aria-hidden="true"></b-icon>
          </b-button>
        </b-button-group>
      </b-button-toolbar>
    </div>
    <div>
    <bubble-menu :editor="editor" v-if="editor">
      <b-button size="sm" title="Bold(Ctrl+B/Cmd+B)" type="button" variant="outline-dark" @click="editor.chain().focus().toggleBold().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('bold') }">
        <b-icon icon="type-bold" aria-hidden="true"></b-icon>
      </b-button>
      <b-button size="sm" title="Italic(Ctrl+I/Cmd+i)" type="button" variant="outline-dark" @click="editor.chain().focus().toggleItalic().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('italic') }">
        <b-icon icon="type-italic" aria-hidden="true"></b-icon>
      </b-button>
      <b-button size="sm" title="Strike(Ctrl+B/Cmd+B)" type="button" variant="outline-dark" @click="editor.chain().focus().toggleStrike().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('strike') }">
        <b-icon icon="type-strikethrough" aria-hidden="true"></b-icon>
      </b-button>
      <b-button size="sm" title="Code" type="button" variant="outline-dark" @click="editor.chain().focus().toggleCode().run()" class="EditorButton" :class="{ 'is-active': editor.isActive('code') }">
        <b-icon icon="code" aria-hidden="true"></b-icon>
      </b-button>
    </bubble-menu>
    <editor-content :editor="editor" class="border" />
  </div>
</template>

<script>
import { Editor, EditorContent, BubbleMenu } from '@tiptap/vue-2'
import StarterKit from '@tiptap/starter-kit'

export default {
  components: {
    EditorContent,
    BubbleMenu
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

<style lang="scss">

.EditorButton:not(.is-active) {
  background: white;
  color: black;
}

.EditorButton.is-active {
  background: black;
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
  border

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
  }

  blockquote {
    padding-left: 1rem;
    border-left: 2px solid rgba(#0D0D0D, 0.1);
  }

  hr {
    border: none;
    border-top: 2px solid rgba(#0D0D0D, 0.1);
    margin: 2rem 0;
  }
}
</style>
