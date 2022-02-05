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
    class="flex w-full flex-col items-center justify-center gap-2 overflow-hidden transition-all ease-out sm:flex-row sm:gap-4"
    :class="active ? 'h-48 border-b sm:h-12' : 'h-0'"
  >
    <router-link
      v-for="item in items"
      :key="item.label"
      :to="item.link"
      class="text-md font-semibold text-stone-600 transition hover:opacity-75 hover:ease-in-out active:opacity-50"
      active-class="text-lime-500"
    >
      {{ item.label }}
    </router-link>
    <div class="mt-2 flex gap-4 sm:hidden">
      <AtomsButton size="small" @click="$router.push('login')">
        Sign In
      </AtomsButton>
      <AtomsButton size="small" outline @click="$router.push('register')">
        Sign Up
      </AtomsButton>
    </div>
  </div>
</template>
