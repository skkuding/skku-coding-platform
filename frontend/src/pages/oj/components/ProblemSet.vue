<template>
  <div class="flex">
    <div v-for="problemSet of problemSets" :key="problemSet.id">
      <color-round-button
        v-if="problemSetGroup.button_type === 'color-round-button'"
        :color="problemSet.color" class="mr-5"
      >
        {{ problemSet.title }}
      </color-round-button>
      <shadow-round-button
        v-else-if="problemSetGroup.button_type === 'shadow-round-button'"
        :color="problemSet.color" class="mr-12"
      >
        {{ problemSet.title }}
      </shadow-round-button>
    </div>
  </div>
</template>

<script>
import ColorRoundButton from './ColorRoundButton.vue'
import ShadowRoundButton from './ShadowRoundButton.vue'
import api from '@oj/api'

export default {
  name: 'ProblemSet',
  props: {
    problemSetGroup: {
      type: Object
    }
  },
  components: {
    ColorRoundButton,
    ShadowRoundButton
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
      const res = await api.getProblemSet(this.problemSetGroup.id)
      this.problemSets = res.data.data
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
