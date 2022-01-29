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
      w-full px-10 py-2
      flex justify-between items-center
      border-b
    "
  >
    <router-link
      to="/"
      class="
        w-40
        hover:opacity-75
        active:opacity-50
        transition duration-150 hover:ease-in-out
      "
    >
      <AtomsSignature />
    </router-link>
    <MoleculesHeaderNav />
    <AtomsHeaderMobileButton @click="openMobileMenu" />
  </header>
  <MoleculesHeaderMobileNav :active="isMobileNavShown" />
</template>
