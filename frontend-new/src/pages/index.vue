<script setup lang="ts">
import { Head } from '@vueuse/head'
import src from '~/assets/home.png?w=280&webp'
</script>

<template>
  <Head>
    <title>SKKU Coding Platform</title>
    <meta
      name="description"
      content="SKKU Coding Platform helps you enhance your coding ability, providing competitive programming environment."
    >
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@800&text=SKKUCodingPlatform&display=swap"
      rel="stylesheet"
    >
  </Head>
  <main class="flex flex-col items-center m-8">
    <h1
      class="
        py-8 font-extrabold text-6xl font-[Inter]
        bg-clip-text text-transparent bg-gradient-to-r
        from-sky-500 to-lime-500"
    >
      SKKU Coding Platform
    </h1>
    <p
      class="
        mb-8 font-medium text-stone-500 text-xl
      "
    >
      Your Coding Skills Evolves Here.
    </p>
    <img
      class="my-8"
      :src="src"
    >
  </main>
</template>
