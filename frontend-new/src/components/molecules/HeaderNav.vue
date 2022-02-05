<script setup lang="ts">
const items = [
  { label: 'Notices', link: '/notice' },
  { label: 'Contests', link: '/contest' },
  { label: 'Problems', link: '/problem' },
  { label: 'Lectures', link: '/lecture' }
]
</script>

<template>
  <div class="hidden lg:flex lg:items-center lg:gap-4">
    <router-link
      v-for="item in items"
      :key="item.label"
      :to="item.link"
      class="text-md font-semibold text-stone-600 transition hover:opacity-75 hover:ease-in-out active:opacity-50"
      active-class="text-lime-500"
    >
      {{ item.label }}
    </router-link>
  </div>
</template>
