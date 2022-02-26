<template>
  <div class="profile-container">
    <div class="user-info-container">
      <user-info :info="info"></user-info>
    </div>
    <hr style="border-top-width: 2px;"/>
    <div class="tab-container">
      <tab-split-in-two :left="leftTabs" :right="rightTabs" :current-tab="currentTab" @show-tab="showTab"></tab-split-in-two>
    </div>
    <div class="tab-content">
      <!--v-show: rendering once when Profile.vue mounted, v-if: rendering every time tab clicked -->
      <profile-summary v-if="currentTab==='Summary'"></profile-summary>
      <profile-submission v-if="currentTab==='Submission'"></profile-submission>
      <profile-history v-show="currentTab==='History'"></profile-history>
      <profile-contest v-if="currentTab==='Contest'"></profile-contest>
      <profile-badge v-show="currentTab==='Badge'"></profile-badge>
      <profile-storage v-show="currentTab==='Storage'"></profile-storage>
      <profile-group v-if="currentTab==='Group'"></profile-group>
    </div>
  </div>
</template>

<script>

import UserInfo from '../../components/user/UserInfo'
import TabSplitInTwo from '../../components/user/TabSplitInTwo.vue'
import ProfileSubmission from '../../components/user/ProfileSubmission.vue'
import ProfileContest from '../../components/user/ProfileContest.vue'
import ProfileGroup from '../../components/user/ProfileGroup.vue'

export default {
  name: 'Profile',
  components: {
    UserInfo,
    TabSplitInTwo,
    ProfileSubmission,
    ProfileContest,
    ProfileGroup
  },
  data () {
    return {
      info: {
        nickname: 'Nickname1234',
        temperature: 670,
        username: '2022123456',
        major: 'CSE',
        weeklyRank: 11,
        monthlyRank: 9,
        presentRank: 6
      },
      leftTabs: [
        'Summary',
        'Submission',
        'History',
        'Contest',
        'Badge'
      ],
      rightTabs: [
        'Storage',
        'Group'
      ],
      currentTab: 'Summary'
    }
  },
  async mounted () {
  },
  methods: {
    showTab (tabName) {
      this.currentTab = tabName
    }
  },
  computed: {
  }
}
</script>

<style lang="scss" scoped>
  .profile-container{
    margin: 0 auto;
    width: 75%;
    font-family: Manrope;
  }
  .user-info-container{
    margin: 30px 0px 10px 0px;
  }
</style>
