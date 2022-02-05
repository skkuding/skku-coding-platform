<script setup lang="ts">
import { Head } from '@vueuse/head'
import { onBeforeRouteLeave } from 'vue-router'
import src from '~/assets/404.png?h=320&webp'

onBeforeRouteLeave(() => {
  document.querySelector("[name='robots']")?.remove()
})
</script>

<template>
  <main>
    <Head>
      <title>Page Not found</title>
      <meta name="description" content="This page is invalid" />
      <meta name="robots" content="noindex" />
    </Head>
    <h1 class="mt-12 mb-8 text-8xl font-bold text-sky-700">Oops!</h1>
    <p class="my-2 text-3xl font-bold text-sky-800">404 Page Not Found</p>
    <p class="my-2 text-lg font-medium text-stone-700">
      This is not the page you're looking for.
    </p>
    <img :src="src" alt="404" class="mt-8 mb-20" />
  </main>
</template>
