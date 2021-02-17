<template>
  <div>
    <div class="list-btn">
      <b-button
        variant="outline-dark"
        to="announcement"
      >
        <b-icon icon="list" to="/announcement"/>목록
      </b-button>
    </div>

    <hr class="line-first">
    <div class="header">
      <div class="title">{{ announcement.title }}</div>
      <div class="date">{{ getTimeFormat(announcement.create_time) }}</div>
    </div>
    <hr class="line-second">

    <div class="markdown-body">
      <p v-html="announcement.content"/>
    </div>

    <b-list-group class="list-group-updown">
      <b-list-group-item
        v-if="prevAnnouncement !== null"
        id="announcement-toggle"
        :href="'/announcement/' + (announcementID + 1)"
      >
        <span class="page-updown"><b-icon class="mr-2" icon="chevron-up"/>Previous</span>
        <span style="color: #696969;">{{ prevAnnouncement.title }}</span>
      </b-list-group-item>
      <b-list-group-item
        v-if="nextAnnouncement !== null"
        id="announcement-toggle"
        style="top: -2px"
        :href="'/announcement/' + (announcementID - 1)"
      >
        <span class="page-updown"><b-icon class="mr-2" icon="chevron-down"/>Next</span>
        <span style="color: #696969;">{{ nextAnnouncement.title }}</span>
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
import time from '@/utils/time'
import api from '@oj/api'

export default {
  name: 'AnnouncementDetail',
  beforeRouteEnter (to, from, next) {
    // annoucementID => 1-based index
    // offset & limit => 0-based index
    const announcementID = Number(to.params.announcementID)
    const offset = Math.max(0, announcementID - 2)
    const limit = announcementID > 1 ? 3 : 2
    api.getAnnouncementList(offset, limit).then(res => {
      next(vm => {
        vm.announcementID = announcementID
        const results = res.data.data.results
        if (announcementID > 1) {
          vm.nextAnnouncement = results[0]
          vm.announcement = results[1]
        } else {
          vm.nextAnnouncement = null
          vm.announcement = results[0]
        }
        if (results.length === limit) {
          vm.prevAnnouncement = results[limit - 1]
        } else {
          vm.prevAnnouncement = null
        }
        console.log('HIHI')
        console.log(vm.announcement)
      })
    })
  },
  data () {
    return {
      announcements: [],
      announcementID: 0,
      announcement: null,
      prevAnnouncement: null,
      nextAnnouncement: null
    }
  },
  methods: {
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-M-D')
    },
    goAnnouncement () {
      this.$router.push({ name: '/' })
    }
  }
}
</script>

<style>
  hr.line-first{
    width: 80%;
    height: 2px;
    margin: 5px auto;
    background: #7C7C7C;
    border: none;
  }
  hr.line-second{
    width: 80%;
    height: 1.3px;
    margin: 5px auto;
    background: #B8B8B8;
    border: none;
  }
  .list-btn{
    margin: 100px 11% 12px;
    display: flex;
    justify-content: flex-end;
  }
  .title{
    float: left;
    margin: 10px 11%;
    font-size: 24px;
    font-weight: bold;
    color: #7C7C7C;
  }
  .date{
    float: right;
    margin: 12px 11%;
    font-size: 20px;
    text-align: right;
    font-weight: 400;
    color: #7C7C7C;
  }
  .markdown-body{
    margin: 64px 11%;
    color: #696969;
  }
  .header{
    overflow: hidden;
  }
  .list-group-updown{
    margin: 128px 11% 24px;
  }
  #announcement-toggle {
    border-top: 2px solid #B8B8B8;
    border-bottom: 2px solid #B8B8B8;
    height: 50px;
  }
  .page-updown{
    display: inline-block;
    width: 120px;
    margin: auto 20px;
    color: #696969;
  }
</style>
