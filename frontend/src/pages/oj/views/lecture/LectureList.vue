<template>
  <!-- Please split into many componenets !-->
  <div>
    <b-list-group>
      <b-list-group-item
        to="/lecture/1"
        class="list-group"
      >
        Lecture Dashboard
      </b-list-group-item>
      <b-list-group-item
        to="/lecture/1/assignment"
        class="list-group"
      >
        Lecture Assignments
      </b-list-group-item>
      <b-list-group-item
        to="/lecture/1/question"
        class="list-group"
      >
        QnA
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
export default {
  name: 'LectureList',
  components: {
    // Split into many components
  },
  data () {
    return {
    }
  },
  async mounted () {
  },
  methods: {
  },
  computed: {
  }
}
</script>

<style lang="scss">
  // Be careful of common css selector in admin/oj
</style>
