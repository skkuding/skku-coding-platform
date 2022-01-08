<template>
  <router-link
    class="
      text-lg font-semibold
      text-gray-600
      hover:text-gray-400
      active:text-gray-300
      transition hover:ease-in-out
    "
    active-class="
      text-lime-500
      hover:text-lime-400
      active:text-lime-300
    "
  >
    <!-- TODO: text color SKKU - #8DC63F -->
    <slot />
  </router-link>
</template>
