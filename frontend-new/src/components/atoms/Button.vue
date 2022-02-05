<script setup lang="ts">
import { computed } from 'vue'

type Variant = 'primary' | 'secondary' | 'danger'
type Size = 'small' | 'large'

const props = defineProps<{
  class?: string
  variant?: Variant
  outline?: boolean
  size?: Size
  disabled?: boolean
}>()

const classList = computed(() => [
  props.class, // parent's style has to be prioritized

  props.variant === undefined ? 'text-stone-500' : 'text-white',
  props.variant === 'primary' ? 'bg-lime-500' : '',
  props.variant === 'secondary' ? 'bg-stone-500' : '',
  props.variant === 'danger' ? 'bg-red-500' : '',

  props.outline ? 'border-2 border-stone-500' : '',

  props.size === undefined ? 'font-medium rounded-md' : '',
  props.size === 'small' ? 'text-sm rounded-md' : '',
  props.size === 'large' ? '' : '',

  props.disabled
    ? 'opacity-60 cursor-not-allowed'
    : 'hover:opacity-75 active:opacity-50',

  'px-2 py-1 font-medium',
  'transition hover:ease-in-out'
])
</script>

<template>
  <button :class="classList">
    <slot />
  </button>
</template>
