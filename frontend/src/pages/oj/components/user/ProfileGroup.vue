<template>
  <div class="profile-group">
    <div class="top-bar mb-4" style="margin-top:4px;">
      <div class="group-top">
        <h2 class="title">My Group</h2>
        <button class="group-create">
          Create
        </button>
      </div>
    </div>
    <div class="top-bar mb-4 group">
      <div class="group-information">
        <div class="group-left">
          <img id="logo" src="@/assets/logos/logo.png" alt="coding-platform-logo">
          <div class="group-detail">
            <h4 class="group-name"> {{ groupName }} </h4>
            <div class="group-description">
              {{ groupDescription }}
            </div>
          </div>
        </div>
        <div class="group-right">
          <div class="group-role">
            {{ groupRole }}
          </div>
          <button class="group-button">
            <b-icon :icon="showMember ? 'caret-down' : 'caret-up' " @click="showMemberList()"></b-icon>
          </button>
        </div>
      </div>
      <div v-if="showMember">
        <div class="admin-container">
          <h4 class="admin_title"> Administrator </h4>
          <div class="admin-list">
            <span v-for="admin in adminList" :key="admin">
              <span class="admin-name">
                {{ admin }}
              </span>
            </span>
          </div>
        </div>
        <div class="member-container">
          <h4 class="member_title"> Member </h4>
          <div class="member-list">
            <span v-for="member in memberList" :key="member"> {{ member }}
              <span v-if="groupRole==='Administrator'">
                <button class="promote">
                  <b-icon icon="arrow-up" style="color: #FFFFFF"> </b-icon>
                </button>
                <button class="delete" style="color: #FF6663">
                  <b-icon icon="x"> </b-icon>
                </button>
              </span>
            </span>
          </div>
        </div>
        <div v-if="groupRole==='Administrator'">
          <div class="apply-container">
            <h4 class="apply_title"> Application </h4>
            <div class="apply-list">
              <span v-for="apply in applyList" :key="apply">
                <span class="apply-name">
                  {{ apply.name }}
                </span>
                <span class="apply-intro">
                  {{ apply.intro }}
                </span>
              </span>
              <button class="resolve">
                Resolve
              </button>
              <button class="reject">
                Reject
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'ProfileGroup',
  components: {
  },
  props: {
  },
  data () {
    return {
      showMember: false,
      groupName: 'SKKUDing',
      groupDescription: 'SKKU Development Crew',
      groupRole: 'Administrator',
      adminList: ['Cocoa123', 'SOLBI1234', 'dotoleeoak', 'minseo123', 'jimin9038'],
      memberList: ['Cocoa123', 'SOLBI1234', 'dotoleeoak', 'minseo123', 'jimin9038', 'Cocoa123', 'SOLBI1234', 'dotoleeoak', 'minseo123', 'jimin9038', 'Cocoa123', 'SOLBI1234', 'dotoleeoak', 'minseo123', 'jimin9038'],
      applyList: [{ name: 'Giraffe', intro: "I'm the cutest dog in the world." }]
    }
  },
  async mounted () {
  },
  methods: {
    showMemberList () {
      this.showMember = !this.showMember
    }
  },
  computed: {
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .profile-group {
    display: flex;
    flex-direction: column;
  }
  .top-bar {
    margin-top: 40px;
    margin-inline: 40px;
  }
  .group-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .title {
    margin-bottom:0;
    color: #7C7A7B;
    display:inline;
    position:relative;
    top:36px;
  }
  .group-create {
    margin-bottom:0;
    color: #FFFFFF;
    display:inline;
    position:relative;
    top:36px;
    background-color: #8DC63F !important;
    border-color: transparent;
    border: none;
    border-radius: 7px;
    width: 6%;
  }
  .group {
    display: flex;
    flex-direction: column;
    border: 1px solid;
    border-color: gray;
  }
  .group-information {
    display: flex;
    height: 107.45px;
    justify-content: space-between;
    align-items: center;
  }
  .group-left {
    display: flex;
  }
  .group-detail {
    display: flex;
    flex-direction: column;
    justify-items: center;
    margin-left: 20px;
  }
  .group-name{
    color: #173747;
    font-weight: bold;
    margin-block: 7px;
  }
  .group-description {
    color: #7C7A7B;
    font-weight: bold;
    margin-top: 5px;
  }
  #logo {
    width: 89px;
    height: 83px;
    margin-left: 20px;
  }
  .group-right {
    display: flex;
    justify-content: space-between;
  }
  .group-role {
    margin-right: 20px;
    color: #173747;
    font-weight: bold;
  }
  .group-button {
    background-color: transparent !important;
    border-color: transparent;
    border: none;
    margin-right: 20px;
  }
  .admin-container {
    display: flex;
    flex-direction: column;
    margin-block: 20px;
    margin-left: 20px;
  }
  .admin-list {
    color: #7C7A7B;
    font-weight: bold;
    margin-block: 20px;
  }
  .admin-name {
    margin-right: 20px;
  }
  .member-container {
    display: flex;
    flex-direction: column;
    margin-block: 20px;
    margin-left: 20px;
  }
  .member-list {
    color: #7C7A7B;
    font-weight: bold;
    margin-block: 20px;
  }
  .promote {
    background-color: #569BD8 !important;
    border-color: transparent;
    border: none;
    border-radius: 2px;
  }
  .delete {
    background-color: transparent !important;
    border-color: transparent;
    border: none;
  }
  .apply-container {
    display: flex;
    flex-direction: column;
    margin-block: 20px;
    margin-left: 20px;
  }
  .apply-list {
    margin-block: 20px;
  }
  .apply-name {
    color: #7C7A7B;
    font-weight: bold;
  }
  .apply-intro {
    font-weight: bold;
    margin-inline: 20px;
  }
  .resolve {
    background-color: #8DC63F !important;
    border-color: transparent;
    border: none;
    border-radius: 7px;
    width: 7%;
    margin-inline: 10px;
    color: #FFFFFF;
  }
  .reject {
    background-color: #FF6663 !important;
    border-color: transparent;
    border: none;
    border-radius: 7px;
    width: 7%;
    margin-inline: 10px;
    color: #FFFFFF;
  }
</style>
