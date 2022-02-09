<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  modelValue?: string
  class?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value?: string): void
}>()

const handleInput = (e: Event) => {
  const target = e.target as HTMLInputElement
  emit('update:modelValue', target.value)
}

const classList = computed(() => [
  props.class, // parent's style has to be prioritized

  // TODO: predefined styles like `Button` component
  'w-full h-8 block border-stone-300 rounded-md',
  'placeholder:font-medium placeholder:stone-300',
  'focus:border-lime-500 focus:ring focus:ring-lime-200',
  'transition duration-300 ease-in-out'
])
</script>

<template>
  <input :class="classList" :value="modelValue" @input="handleInput" />
</template>
