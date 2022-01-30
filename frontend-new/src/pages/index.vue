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

<style>
@font-face {
  font-family: Inter;
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url("https://fonts.gstatic.com/l/font?kit=UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuDyYMZ1rj72Aqf-XMmHeTOYuSQFW3ERAF4dN&skey=c491285d6722e4fa&v=v7") format("woff2");
}
</style>
