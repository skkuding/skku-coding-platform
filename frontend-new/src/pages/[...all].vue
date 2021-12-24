<script setup lang="ts">
import src from '~/assets/404.png?h=320&webp'
</script>

<template>
  <h1 class="text-sky-700 text-8xl font-bold mt-12 mb-8">
    Oops!
  </h1>
  <p class="text-sky-800 text-3xl font-bold my-2">
    404 Page Not Found
  </p>
  <p class="text-stone-700 text-lg my-2 font-medium">
    This is not the page you're looking for.
  </p>
  <img
    :src="src"
    alt="404"
    class="mt-8"
  >
</template>
