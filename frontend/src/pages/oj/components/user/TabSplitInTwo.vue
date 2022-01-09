<template>
  <div class="tab-split-in-two">
    <div class="d-flex">
      <button v-for="tabName in left" :key="tabName" @click="showTab(tabName)" class="tab-split-in-two__tab">
        {{ tabName }}
      </button>
    </div>
    <div class="mx-4"></div>
    <div class="d-flex">
      <button v-for="tabName in right" :key="tabName" @click="showTab(tabName)" class="tab-split-in-two__tab">
        {{ tabName }}
      </button>
    </div>
  </div>
</template>

<script>

export default {
  name: 'TabSplitInTwo',
  components: {
  },
  props: {
    left: Array,
    right: Array
  },
  data () {
    return {
    }
  },
  async mounted () {
  },
  methods: {
    showTab (tabName) {
      this.$emit('show-tab', tabName)
    }
  },
  computed: {
  }
}
</script>

<style lang="scss" scoped>
  .tab-split-in-two {
    display: flex;
    justify-content: space-between;
    margin: 0px 50px;
    overflow: auto;
    .tab-split-in-two__tab {
      margin: 0px 10px;
      font-size: 18px;
      border: 0px;
      background-color: transparent;
    }
    .tab-split-in-two__tab:hover {
      color: #8DC63F;
    }
  }

</style>
