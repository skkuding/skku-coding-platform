<script setup lang="ts">
import src from '~/assets/signature.png?h=40'
</script>

<template>
  <router-link
    to="/"
    class="
      hover:opacity-75
      active:opacity-50
      transition duration-150 hover:ease-in-out
    "
  >
    <img
      alt="Sungkyunkwan University"
      width="168"
      height="40"
      :src="src"
    >
  </router-link>
</template>
