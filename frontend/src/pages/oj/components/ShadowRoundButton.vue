<template>
  <button class="rounded-2xl px-5 h-10" :style="'box-shadow: 4px 4px 15px ' + color">
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
  }

}
</script>

<style lang="scss" scoped>

</style>
