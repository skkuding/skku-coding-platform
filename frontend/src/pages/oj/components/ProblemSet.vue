<template>
  <div>
    <page-top>
      <template #title>
        <span class="title-white">🏆 SKKU Coding Platform</span>
        <span class="title-gold"> Contests</span>
      </template>
      <template #description>
        Compete with schoolmates & win the prizes!
      </template>
    </page-top>
  </div>
</template>

<script>
import PageTop from '@oj/components/PageTop.vue'

export default {
  name: 'problemSet',
  components: {
    PageTop
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
  .sidemenu {
  }
</style>
