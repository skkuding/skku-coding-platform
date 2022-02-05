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
    class="flex h-14 w-full items-center justify-center border-b px-8 md:px-10"
  >
    <div class="flex w-full max-w-7xl items-center">
      <router-link
        to="/"
        class="w-36 transition duration-150 hover:opacity-75 hover:ease-in-out active:opacity-50"
      >
        <AtomsSignature />
      </router-link>
      <MoleculesHeaderNav class="absolute left-1/2 translate-x-[-50%]" />
      <div class="ml-auto hidden gap-2 sm:flex">
        <AtomsButton size="small" @click="$router.push('login')">
          Sign In
        </AtomsButton>
        <AtomsButton size="small" outline @click="$router.push('register')">
          Sign Up
        </AtomsButton>
      </div>
      <AtomsHeaderMobileButton
        class="ml-auto sm:ml-4 lg:hidden"
        @click="openMobileMenu"
      />
    </div>
  </header>
  <MoleculesHeaderMobileNav :active="isMobileNavShown" class="lg:hidden" />
</template>
