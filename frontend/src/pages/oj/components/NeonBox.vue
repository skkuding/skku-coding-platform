<template>
  <div class="neon-box-container" :style="cssColor">
    <div class="neon-box-hover">
      <div class="ellipse">
        <slot name="overlay-icon"></slot>
      </div>
    </div>
    <div class="neon-box">
      <img class="logo" src="@/assets/Cup.png">
      <div class="contest-information-flex-col">
        <div class="contest-information-flex-row">
          <div class="contest-information-big">{{ leftTop }}</div>
          <div class="contest-information-big"><icon :icon="rightTopIcon" class="mr-2"/>{{ rightTop }}</div>
        </div>
        <div class="contest-information-flex-row">
          <div class="contest-information-small">{{ leftBottom }}</div>
          <div class="contest-information-small">{{ rightBottom }} </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'NeonBox',
  props: {
    color: {
      type: String,
      required: true
    },
    shadow: {
      type: Boolean
    },
    leftTop: {
      type: String
    },
    rightTop: {
      type: String
    },
    leftBottom: {
      type: String
    },
    rightBottom: {
      type: String
    },
    rightTopIcon: {
      type: String
    }
  },
  data () {
    return {
    }
  },
  methods: {
  },
  computed: {
    cssColor () {
      return {
        '--main-color': this.color,
        '--shadow': this.shadow ? '9px' : '0'
      }
    }
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
  .neon-box-container {
    position: relative;
    .neon-box-hover {
      display: none;
    }
    &:hover .neon-box-hover {
      position: absolute;
      display: flex;
      justify-content: flex-end;
      right: 1px;
      width: 100%;
      height: 98%;
      margin: 1px;
      background: linear-gradient(90deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.5) 30.39%, rgba(255, 255, 255, 0.9) 71%, #FFFFFF 100%);
      cursor: pointer;

      .ellipse {
        height: 60px;
        width: 60px;
        margin: auto 10px;
        background: white;
        border-radius: 50%;
        // border: var(--main-color) 1px solid;
        // box-shadow: 0px 0px var(--shadow) var(--main-color);
        display: flex;
        align-items: center;
        justify-content: center;
      }
    }
    .neon-box {
      background: #FFFFFF;
      border: 1px solid var(--main-color);
      box-shadow: 0px 0px var(--shadow) var(--main-color);
      padding: 0.8rem;
      display: flex;
      .logo {
        width: 3.1rem;
        height: 3.1rem;
        margin: 0.2rem 1rem 0.2rem 0.2rem;
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
            font-size: 1.2rem;
            white-space: nowrap;
          }
          .contest-information-small {
            color: var(--main-color);
            font-size: 0.9rem;
            white-space: nowrap;
          }
        }
      }
    }
  }
</style>
