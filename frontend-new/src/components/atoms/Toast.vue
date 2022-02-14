<script setup lang="ts">
import { ref } from 'vue'
import { promiseTimeout } from '@vueuse/core'
import { useToast, Toast } from '~/composables/toast'

interface ToastItem extends Toast {
  id: number
}

const toastId = ref(0)
const toastItems = ref<ToastItem[]>([])
const { onTrigger } = useToast()

onTrigger(async (option) => {
  toastItems.value.unshift({ id: toastId.value++, ...option })
  await promiseTimeout(option.duration || 3000)
  toastItems.value.pop()
})

const getClassName = (item: ToastItem): string[] => [
  item.variant === undefined ? 'bg-white text-stone-500' : 'text-white',
  item.variant === 'info' ? 'bg-stone-500' : '',
  item.variant === 'success' ? 'bg-lime-500' : '',
  item.variant === 'warning' ? 'bg-yellow-500' : '',
  item.variant === 'danger' ? 'bg-red-500' : '',

  'rounded px-4 py-1 font-medium shadow'
]
</script>

<template>
  <section
    class="pointer-events-none fixed inset-x-0 top-0 z-10 grid justify-center justify-items-center gap-2 pt-4"
  >
    <transition-group name="list">
      <output
        v-for="item in toastItems"
        :key="item.id"
        role="status"
        :class="getClassName(item)"
      >
        {{ item.message }}
      </output>
    </transition-group>
  </section>
</template>

<style>
.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
