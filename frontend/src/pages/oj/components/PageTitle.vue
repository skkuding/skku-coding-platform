<template>
    <div class="text-text-title text-3xl mb-8 mt-10 ml-20">
        {{text}}
    </div>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      required: true
    }
  },
  data () {
    return {
    }
  }
}
</script>
