<script setup lang="ts">
import { OnClickOutside } from '@vueuse/components'

defineProps<{ show: boolean }>()
defineEmits<{ (e: 'close'): void }>()
</script>

<template>
  <OnClickOutside @trigger="$emit('close')">
    <ul
      class="rounded-lg bg-white py-2 text-sm leading-6 shadow-lg ring-1 ring-stone-500/20 transition"
      :class="show ? 'opacity-100' : 'opacity-0'"
    >
      <slot />
    </ul>
  </OnClickOutside>
</template>
