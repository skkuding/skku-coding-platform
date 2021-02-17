r<template>
  <div>
    <b-card
      header-tag="header"
      header-bg-variant="white"
      header-border-variant="white"
    >
      <template #header>
        <div class="post-panel">
            <div class = 'post-title'>
            <b-icon icon="exclamation-circle"></b-icon>
            <h6 class="mb-0">Nice to meet you</h6>
          </div>
          <h6 class="mb-0">Header Slot</h6>
        </div>
      </template>
      <div class="table">
        <template>
          <div>
            <b-table
              striped: False
              hover
              :items="items"
              thead-tr-class="d-none"
              borderless
            ></b-table>
          </div>
        </template>
      </div>
    </b-card>
  </div>
</template>
<script>
export default {
  data () {
    return {
      items: [
        { icon: 21, title: 'Larsen', date: 'Shaw' },
        { icon: 89, title: 'Geneva', date: 'Wilson' },
        { icon: 38, title: 'Jami', date: 'Carney' }
      ]
    }
  }
}
</script>
<style scoped>
.post-panel {
  display: flex;
  text-align: center;
  justify-content: space-between;
  flex-direction: row;
}
.post-title {
  display: flex;
  justify-content: space-between;
  flex-direction: row;
}

.card {
  width: 35rem;
}

.table {
  width: 28rem;
}

.tbody-tr-class {
  variant: white;
}

.date {
  color: red;
}
</style>
