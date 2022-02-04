<script setup lang="ts">
import { ref, reactive, computed } from 'vue'

const loading = ref(false)
const info = reactive({ username: '', password: '' })
const message = computed(() => loading.value ? 'Signing In...' : 'Sign In')

// just for demo
function sleep (ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

const login = async () => {
  loading.value = true
  await sleep(2000) // TODO: call API
  loading.value = false
}
</script>

<template>
  <main class="flex-1 grid place-items-center">
    <div>
      <h1 class="mb-12 text-center text-2xl font-bold text-stone-600">
        SKKU<br>Coding Platform
      </h1>
      <form
        class="flex flex-col gap-4 w-64"
        @submit.prevent="login"
      >
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
          class="w-full h-8"
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
