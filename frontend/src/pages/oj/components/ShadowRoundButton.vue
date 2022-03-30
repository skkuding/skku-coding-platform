<template>
  <button class="rounded-2xl px-5 h-10 shadow-round-button transition duration-200 ease-in-out" :style="cssColor">
    <slot></slot>
  </button>
</template>

<script>

export default {
  name: 'ColorRoundButton',
  props: {
    color: {
      type: String
    }
  },
  components: {
  },
  data () {
    return {
    }
  },
  async mounted () {
  },
  methods: {
  },
  computed: {
    cssColor () {
      return {
        // for opacity purpose. Use tailwindcss v3 class after migrating to tailwindcss v3
        '--color-opacity': this.color
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .shadow-round-button {
    box-shadow: 4px 4px 15px var(--color-opacity)
  }
  .shadow-round-button:hover {
    background-color: var(--color-opacity)
  }
</style>
