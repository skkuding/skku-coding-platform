<template>
  <div class="relative">
    <button class="z-10 relative flex items-center focus:outline-none select-none" @click="open = !open">
      <slot name="button"></slot>
    </button>

    <!-- to close when clicked on space around it-->
    <button class="fixed inset-0 h-full w-full cursor-default focus:outline-none" v-if="open" @click="open = false" tabindex="-1"></button>
    <!--dropdown content-->
    <transition enter-active-class="transition-all duration-200 ease-out" leave-active-class="transition-all duration-750 ease-in" enter-class="opacity-0 scale-75" enter-to-class="opacity-100 scale-100" leave-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-75">
      <div class="hidden md:block absolute shadow rounded-lg py-1 px-2 mt-4 bg-white"
        :class=set
        v-if="open"
    >
        <slot name="content"></slot>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  data () {
    return {
      open: false,
      set: ''
    }
  },
  props: {
    placement: {
      type: String,
      default: 'right',
      validator: (value) => ['right', 'left'].indexOf(value) !== -1
    },
    width: {
      type: String,
      default: 'w-48'
    }
  },
  mounted () {
    this.setPlacementWidth()
    const onEscape = (e) => {
      if (e.key === 'Esc' || e.key === 'Escape') {
        this.open = false
      }
    }
    document.addEventListener('keydown', onEscape)
    this.$once('hook:beforeDestroy', () => {
      document.removeEventListener('keydown', onEscape)
    })
  },
  methods: {
    setPlacementWidth () {
      if (this.width) {
        this.set += this.width
      } else {
        this.set += 'w-48'
      }
      if (this.placement === 'right') {
        this.set += ' right-0'
      } else {
        this.set += ' left-0'
      }
    }
  }
}
</script>
