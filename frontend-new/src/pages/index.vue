<script setup lang="ts">
import { Head } from '@vueuse/head'
import src from '~/assets/banner.png?h=613&webp'
</script>

<template>
  <Head>
    <title>SKKU Coding Platform</title>
    <meta
      name="description"
      content="SKKU Coding Platform helps you enhance your coding ability, providing competitive programming environment."
    >
  </Head>
  <img
    :src="src"
    class="w-full"
  >
</template>
