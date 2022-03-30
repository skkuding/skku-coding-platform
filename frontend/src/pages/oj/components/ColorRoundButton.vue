<template>
  <button class="color-round-button rounded-full px-5 h-14 hover:shadow-lg transition duration-200 ease-in-out" :style="cssColor">
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
        '--color': this.color
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .color-round-button {
    background-color: var(--color);
  }
  .color-round-button:hover {
    background-color: var(--color);
  }
</style>
