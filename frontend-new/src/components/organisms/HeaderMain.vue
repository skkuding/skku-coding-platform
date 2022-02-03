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
  <header class="h-14 w-full px-8 md:px-10 flex items-center justify-center border-b">
    <div class="w-full max-w-7xl flex items-center">
      <router-link
        to="/"
        class="
        w-36
        hover:opacity-75 active:opacity-50
        transition duration-150 hover:ease-in-out
      "
      >
        <AtomsSignature />
      </router-link>
      <MoleculesHeaderNav class="absolute left-1/2 translate-x-[-50%]" />
      <div class="hidden sm:flex gap-2 ml-auto">
        <AtomsButton
          size="small"
          @click="$router.push('login')"
        >
          Sign In
        </AtomsButton>
        <AtomsButton
          size="small"
          outline
          @click="$router.push('register')"
        >
          Sign Up
        </AtomsButton>
      </div>
      <AtomsHeaderMobileButton
        class="ml-auto sm:ml-4 lg:hidden"
        @click="openMobileMenu"
      />
    </div>
  </header>
  <MoleculesHeaderMobileNav
    :active="isMobileNavShown"
    class="lg:hidden"
  />
</template>
