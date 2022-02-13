<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { isAuthenticated, useLogout } from '~/composables/user'

const isUserMenuShown = ref(false)

const toggleUserMenu = () => {
  isUserMenuShown.value = !isUserMenuShown.value
}

const { logout } = useLogout(useRouter())
</script>

<template>
  <Transition name="fade" mode="out-in">
    <div
      v-if="isAuthenticated"
      class="relative ml-auto hidden text-stone-500 sm:flex"
    >
      <AtomsButton class="text-lg">
        <IconFaSolidUser @click="toggleUserMenu" />
      </AtomsButton>
      <AtomsDropdownMenu
        :show="isUserMenuShown"
        class="absolute right-0 top-8 z-10 w-24"
        @close="isUserMenuShown = false"
      >
        <AtomsDropdownItem>Settings</AtomsDropdownItem>
        <AtomsDropdownItem @click="logout">Sign Out</AtomsDropdownItem>
      </AtomsDropdownMenu>
    </div>
    <div v-else class="ml-auto hidden gap-2 sm:flex">
      <AtomsButton size="small" @click="$router.push('login')">
        Sign In
      </AtomsButton>
      <AtomsButton size="small" outline @click="$router.push('register')">
        Sign Up
      </AtomsButton>
    </div>
  </Transition>
</template>
