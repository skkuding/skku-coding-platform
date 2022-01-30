<script setup lang="ts">
const props = defineProps<{
  outline?: boolean
}>()
</script>

<template>
  <button
    class="
      px-2 py-1 text-sm text-stone-600 font-medium
      rounded-md
      hover:opacity-75 active:opacity-50
      transition hover:ease-in-out"
    :class="{'border-2 border-stone-500': props.outline}"
  >
    <slot />
  </button>
</template>
