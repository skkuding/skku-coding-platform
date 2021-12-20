<script setup lang="ts">
defineProps({
  to: {
    type: String,
    required: true
  }
})
</script>

<template>
  <router-link
    :to="to"
    class="
      text-lg font-semibold tracking-wide
      text-gray-600
      hover:text-gray-400
      active:text-gray-300
      transition duration-150 hover:ease-in-out
    "
    active-class="
      text-lime-500
      hover:text-lime-400
      active:text-lime-300
    "
  >
    <!-- TODO: text color SKKU - #8DC63F -->
    <slot />
  </router-link>
</template>
