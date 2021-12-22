<script setup lang="ts">
import { ref } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'

const isMobileNavShown = ref(false)

const openMobileMenu = () => {
  isMobileNavShown.value = !isMobileNavShown.value
}

onBeforeRouteLeave(() => {
  isMobileNavShown.value = false
})
</script>

<template>
  <header
    class="
      w-full px-10 py-3
      flex justify-between items-center
      border-b
    "
  >
    <HeaderLogo />
    <HeaderNav />
    <HeaderMobileButton @click="openMobileMenu" />
  </header>
  <HeaderMobileNav :active="isMobileNavShown" />
</template>
