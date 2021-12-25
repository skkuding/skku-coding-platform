<script setup lang="ts">
defineProps({
  active: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
  <div
    class="
      flex flex-col sm:flex-row gap-2 sm:gap-4
      items-center justify-center
      w-full overflow-hidden
      transition-all ease-out
    "
    :class="active ? 'max-h-40 py-2 border-b' : 'max-h-0'"
  >
    <AtomsNavItem to="/notice">
      Notices
    </AtomsNavItem>
    <AtomsNavItem to="/contest">
      Contests
    </AtomsNavItem>
    <AtomsNavItem to="/problem">
      Problems
    </AtomsNavItem>
    <AtomsNavItem to="/lecture">
      Lectures
    </AtomsNavItem>
  </div>
</template>
