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
    <NavItem to="/notice">
      Notices
    </NavItem>
    <NavItem to="/contest">
      Contests
    </NavItem>
    <NavItem to="/problem">
      Problems
    </NavItem>
    <NavItem to="/lecture">
      Lectures
    </NavItem>
  </div>
</template>
