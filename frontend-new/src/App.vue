<script setup lang="ts">
import { onMounted } from 'vue'
import api from '~/modules/axios'

onMounted(async () => {
  // ensure csrf cookie
  await api.get('profile/')
})
</script>

<template>
  <router-view />
  <AtomsToast />
</template>
