<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  class?: string
}>()

const classList = computed(() => [
  props.class, // parent's style has to be prioritized

  // TODO: predefined styles like `Button` component
  'w-64 h-8 block border-stone-300 rounded-md',
  'placeholder:font-medium placeholder:stone-300',
  'focus:border-lime-500 focus:ring focus:ring-lime-200',
  'transition duration-300 ease-in-out'
])
</script>

<template>
  <input :class="classList" />
</template>
