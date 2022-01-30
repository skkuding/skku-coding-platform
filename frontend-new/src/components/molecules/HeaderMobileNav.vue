<script setup lang="ts">
defineProps({
  active: {
    type: Boolean,
    default: false
  }
})

const items = [
  { label: 'Notices', link: '/notice' },
  { label: 'Contests', link: '/contest' },
  { label: 'Problems', link: '/problem' },
  { label: 'Lectures', link: '/lecture' }
]
</script>

<template>
  <div
    class="
      flex flex-col sm:flex-row gap-2 sm:gap-4
      items-center justify-center
      w-full overflow-hidden
      transition-all ease-out
    "
    :class="active ? 'max-h-40 py-2 border-b' : 'max-h-0'"
  >
    <router-link
      v-for="item in items"
      :key="item.label"
      :to="item.link"
      class="
        text-md text-stone-600 font-semibold
        hover:opacity-75 active:opacity-50
        transition hover:ease-in-out"
    >
      {{ item.label }}
    </router-link>
  </div>
</template>
