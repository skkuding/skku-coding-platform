<template>
  <div class="page-top">
    <h2 class="text-3xl">
      <slot name="title"></slot>
    </h2>
    <div class="description text-xl">
      <slot name="description"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'pageTop',
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
  .page-top {
    background: linear-gradient(270deg, rgba(26, 62, 81, 0.90) 0%, #1A3E51 25%, #1A3E51 75%, rgba(26, 62, 81, 0.90) 100%);;
    padding: 50px 0px;
    text-align: center;
    font-family: Manrope;
    .description {
      font-size: 1rem;
      color: white;
      margin-top: 1rem;
    }
  }
</style>
