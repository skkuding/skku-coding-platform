<template>
  <button class="rounded-full px-5 h-14 drop-shadow-sm" :style="'background-color:' + color">
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
