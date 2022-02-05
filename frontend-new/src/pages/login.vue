<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { Head } from '@vueuse/head'

const loading = ref(false)
const info = reactive({ username: '', password: '' })
const message = computed(() => (loading.value ? 'Signing In...' : 'Sign In'))

// just for demo
function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

const login = async () => {
  loading.value = true
  await sleep(2000) // TODO: call API
  loading.value = false
}
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
      <form class="flex w-64 flex-col gap-4" @submit.prevent="login">
        <AtomsInput
          v-model="info.username"
          type="text"
          placeholder="Student ID"
        />
        <AtomsInput
          v-model="info.password"
          type="password"
          placeholder="Password"
        />
        <AtomsButton
          type="submit"
          variant="primary"
          class="h-8 w-full"
          :disabled="loading"
        >
          {{ message }}
        </AtomsButton>
      </form>
    </div>
  </main>
</template>

<route lang="yml">
meta:
  layout: simple
</route>
