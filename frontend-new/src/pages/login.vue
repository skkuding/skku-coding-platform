<script setup lang="ts">
import { computed, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { Head } from '@vueuse/head'
import { isAuthenticated, useLogin } from '~/composables/user'

const { loading, errorMessage, form, login } = useLogin(useRouter())

onBeforeMount(() => {
  if (isAuthenticated.value) {
    useRouter().replace('/')
  }
})

const buttonMessage = computed(() =>
  loading.value ? 'Signing In...' : 'Sign In'
)
</script>

<template>
  <main class="grid flex-1 place-items-center">
    <Head>
      <title>Sign In</title>
      <meta
        name="description"
        content="SKKU Coding Platform helps you enhance your coding ability, providing competitive programming environment."
      />
    </Head>
    <div>
      <h1 class="mb-12 text-center text-2xl font-bold text-stone-600">
        SKKU<br />Coding Platform
      </h1>
      <div
        v-show="errorMessage"
        class="mb-2 text-center font-medium text-red-500"
      >
        <!-- TODO: show error message as toast -->
        {{ errorMessage }}
      </div>
      <form class="flex w-80 flex-col gap-4" @submit.prevent="login">
        <AtomsInput
          v-model="form.username"
          type="text"
          placeholder="Student ID"
        />
        <AtomsInput
          v-model="form.password"
          type="password"
          placeholder="Password"
        />
        <AtomsButton
          type="submit"
          variant="primary"
          class="h-8 w-full"
          :disabled="loading"
        >
          {{ buttonMessage }}
        </AtomsButton>
      </form>
    </div>
  </main>
</template>

<route lang="yml">
meta:
  layout: simple
</route>
