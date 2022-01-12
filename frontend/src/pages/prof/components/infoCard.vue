<template>
  <b-card
    class="info-card"
    no-body
  >
    <b-row
      class="info-card-container"
    >
      <b-col
        class="info-card-text"
      >
        <p :style="textStyle" class="p-header">
          {{ value }}
        </p>
        <p style="font-weight: 300;">
          {{ message }}
        </p>
      </b-col>
    </b-row>
  </b-card>
</template>

<script>
export default {
  name: 'InfoCard',
  props: {
    value: [String, Number],
    color: String,
    message: String,
    icon: String,
    iconSize: {
      type: String,
      default: '35px'
    },
    countSize: {
      type: String,
      default: '25px'
    },
    countWeight: {
      type: Number,
      default: 700
    }
  },
  computed: {
    textStyle () {
      return {
        'font-size': this.countSize,
        'font-weight': this.countWeight,
        color: this.color
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  $card-height: 90px;

  .info-card {
    display: inline-block;
    width: 250px;
    text-align: center;
    vertical-align: middle;
  }
  .info-card-container {
    height: 90px;
    margin: 0px;
    align-items: stretch;
    justify-content: center;
  }
  .info-card-icon {
    line-height: #{$card-height};
    color: white;
    margin-top: calc( #{$card-height} / 3 );
  }
  .info-card-text {
    p {
      margin: 0;
      .minor-text {
        font-weight: 300;
        margin-top: 2px;
        font-size: 20px;
      }
    }
  }

  .p-header {
    padding-top: calc( #{$card-height} / 6 );
  }
</style>
