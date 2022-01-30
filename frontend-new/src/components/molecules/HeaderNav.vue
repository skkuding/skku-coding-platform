<script setup lang="ts">
const items = [
  { label: 'Notices', link: '/notice' },
  { label: 'Contests', link: '/contest' },
  { label: 'Problems', link: '/problem' },
  { label: 'Lectures', link: '/lecture' }
]
</script>

<template>
  <div class="hidden lg:flex lg:gap-4 lg:items-center">
    <router-link
      v-for="item in items"
      :key="item.label"
      :to="item.link"
      class="
        text-md text-stone-600 font-semibold
        hover:opacity-75 active:opacity-50
        transition hover:ease-in-out"
      active-class="text-lime-500"
    >
      {{ item.label }}
    </router-link>
  </div>
</template>
