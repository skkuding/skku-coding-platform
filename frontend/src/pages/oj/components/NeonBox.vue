<template>
  <div class="neon-box">
    <img class="logo" src="@/assets/Cup.png">
    <div class="contest-information-flex-col">
      <div class="contest-information-flex-row">
        <div class="contest-information-big">2021 Spring SKKU 프로그래밍 대회 - 참여중 대회</div>
        <div class="contest-information-big">#참여</div>
      </div>
      <div class="contest-information-flex-row">
        <div class="contest-information-small">For SKKU Undergraduate</div>
        <div class="contest-information-small">Started Before 00:07:05 </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'NeonBox',
  data () {
    return {
    }
  },
  methods: {
  },
  computed: {
  },
  watch: {
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../fonts/Manrope-Bold.ttf');
  }
  .neon-box {
    background: #FFFFFF;
    border: 0.89132px solid #8DC63F;
    box-shadow: 0px 0px 8.9132px #8DC63F;
    padding: 1rem;
    display: flex;
    transition: 0.3s ease-in-out;
    &:hover {
      transform: scale(1.01);
    }

    .logo {
      width: 4rem;
      height: 4rem;
      margin-right: 1rem;
    }

    .contest-information-flex-col {
      display: flex;
      flex-direction: column;
      width: 100%;
      justify-content: space-between;
      .contest-information-flex-row {
        display: inline-flex;
        flex-direction: row;
        justify-content: space-between;
        .contest-information-big {
          color: #173747;
          font-size: 1.3rem;
          font-weight: bold;
          white-space: nowrap;
        }
        .contest-information-small {
          color: #173747;
          font-size: 1.0rem;
          white-space: nowrap;
        }
      }
    }
  }
</style>
