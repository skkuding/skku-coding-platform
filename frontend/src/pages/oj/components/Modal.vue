<template>
    <div class="fixed w-full h-full top-0 left-0 flex items-center justify-center z-50" v-if="open">
        <div class="absolute w-full h-full bg-black bg-opacity-50" @click="close"></div>
        <div class="absolute max-h-full" :class=setWidth>
        <div class="container py-5 px-4 bg-white overflow-hidden md:rounded-lg shadow">
            <div v-if="!!title" class="px-4 py-3 leading-none flex justify-between items-center font-medium text-sm border-b select-none">
                <h3>{{ title }}</h3>
            </div>

            <div class="max-h-full">
                <slot></slot>
            </div>
        </div>
        </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      open: true
    }
  },
  props: {
    title: {
      type: String,
      default: ''
    },
    header: {
      type: String,
      required: false,
      default: ''
    },
    width: {
      type: String,
      default: 'full',
      validator: (value) => ['xs', 'sm', 'md', 'lg', 'full'].indexOf(value) !== -1
    }
  },
  mounted () {
    const onEscape = (e) => {
      if (e.key === 'Esc' || e.key === 'Escape') {
        this.close()
      }
    }

    document.addEventListener('keydown', onEscape)
    this.$once('hook:beforeDestroy', () => {
      document.removeEventListener('keydown', onEscape)
    })
  },
  methods: {
    close () {
      this.open = false
      this.$emit('close')
    },
    setWidth () {
      switch (this.width) {
        case 'xs':
          return 'max-w-lg'
        case 'sm':
          return 'max-w-xl'
        case 'md':
          return 'max-w-2xl'
        case 'lg':
          return 'max-w-3xl'
        case 'full':
          return 'max-w-full'
      }
    }
  }
}
</script>
