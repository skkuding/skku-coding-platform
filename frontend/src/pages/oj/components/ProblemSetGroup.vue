<template>
  <div class="flex">
    <div v-for="problemSet of problemSets" :key="problemSet.id">
      <color-round-button
        v-if="problemSetGroup.button_type === 'color-round-button'"
        :color="problemSet.color" class="mr-5 my-3"
        @click.native="goProblemSet(problemSet.id)"
      >
        {{ problemSet.title }}
      </color-round-button>
      <shadow-round-button
        v-else-if="problemSetGroup.button_type === 'shadow-round-button'"
        :color="problemSet.color" class="mr-5 my-3"
        @click.native="goProblemSet(problemSet.id)"
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
  name: 'ProblemSetGroup',
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
    },
    goProblemSet (problemSetId) {
      this.$router.push({
        name: 'problem-set',
        params: { problemSetId, problemSetGroupId: this.problemSetGroup.id }
      })
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
