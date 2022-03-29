<template>
  <div>
    <color-round-button v-for="problemSet of problemSets" :key="problemSet.id" :color="problemSet.color" class="mr-3" >
      {{ problemSet.title }}
    </color-round-button>
  </div>
</template>

<script>
import ColorRoundButton from './ColorRoundButton.vue'
import api from '@oj/api'

export default {
  name: 'ProblemSet',
  props: {
    problemSetGroupId: {
      type: Number
    }
  },
  components: {
    ColorRoundButton
  },
  data () {
    return {
      problemSets: []
    }
  },
  async mounted () {
    await this.getProblemSets()
  },
  methods: {
    async getProblemSets () {
      const res = await api.getProblemSet(this.problemSetGroupId)
      this.problemSets = res.data.data
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
