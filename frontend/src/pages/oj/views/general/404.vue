<template>
  <div class="error404">
    <div class="error404-body-con">
      <b-card>
        <div class="error404-body-con-title">
          4<span><b-icon icon="arrow-down-right-circle" scale="0.8"/></span>4
        </div>
        <p class="error404-body-con-message">
          YOU&nbsp;&nbsp;LOOK&nbsp;&nbsp;LOST
        </p>
        <div class="error404-btn-con">
          <b-button
            size="lg"
            style="width: 200px;"
            @click="goHome"
          >
            Go Home
          </b-button>
          <b-button
            size="lg"
            style="width: 200px;margin-left: 40px;"
            @click="backPage"
          >
            Back
          </b-button>
        </div>
      </b-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Error404',
  methods: {
    backPage () {
      this.$router.go(-1)
    },
    async goHome () {
      await this.$router.push({
        name: 'home'
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  @keyframes error404animation {
    0% {
      transform: rotateZ(0deg);
    }
    20% {
      transform: rotateZ(-60deg);
    }
    40% {
      transform: rotateZ(-10deg);
    }
    60% {
      transform: rotateZ(50deg);
    }
    80% {
      transform: rotateZ(-20deg);
    }
    100% {
      transform: rotateZ(0deg);
    }
  }

  .error404-body-con {
    height: 500px;
    margin: 0 auto;
  }

  .error404-body-con-title {
    text-align: center;
    font-size: 180px;
    font-weight: 700;
    color: #2d8cf0;
    height: 260px;
    line-height: 260px;
    margin-top: 40px;
    span {
      display: inline-block;
      color: #19be6b;
      font-size: 180px;
      animation: error404animation 3s ease 0s infinite alternate;
    }
  }

  .error404-body-con-message {
    display: block;
    text-align: center;
    font-size: 30px;
    font-weight: 500;
    letter-spacing: 12px;
    color: #dddde2;
  }

  .error404-btn-con {
    text-align: center;
    padding: 20px 0;
    margin-bottom: 40px;
  }
</style>
