<template>
  <div style="display: inline-block;">
    <b-button
      variant="outline-secondary"
      size="sm"
      v-b-tooltip.hover
      v-bind:title="name"
    >
      <b-icon v-bind:icon="icon"></b-icon>
    </b-button>
  </div>
</template>

<script>
export default {
  name: 'IconBtn',
  props: {
    name: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      required: true
    }
  }
}
</script>
