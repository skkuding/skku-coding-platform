<template>
  <div class="announcement">
    <div class="list-btn">
      <router-link
        tag="button"
        to="/announcement"
        class="list-btn__router"
      >
        <b-icon icon="list" to="/announcement"/> List
      </router-link>
    </div>
    <div class="announcement__header">
      <div class="announcement__title">{{ announcement.title }}</div>
      <div class="announcement__date">{{ getTimeFormat(announcement.create_time) }}</div>
    </div>
    <div class="announcement__content" v-katex>
      <p v-dompurify-html="announcement.content"/>
    </div>
    <b-list-group class="announcement__pagination">
      <b-list-group-item
        v-if="prevAnnouncement !== null"
        id="announcement__pagination-item"
        :to="'/announcement/' + prevAnnouncement.id"
      >
        <span class="pagination-text"><b-icon class="mr-2" icon="chevron-up"/>Previous</span>
        <span style="color: #696969">{{ prevAnnouncement.title }}</span>
      </b-list-group-item>
      <b-list-group-item
        v-if="nextAnnouncement !== null"
        id="announcement__pagination-item"
        :to="'/announcement/' + nextAnnouncement.id"
      >
        <span class="pagination-text"><b-icon class="mr-2" icon="chevron-down"/>Next</span>
        <span style="color: #696969">{{ nextAnnouncement.title }}</span>
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
import time from '@/utils/time'
import api from '@oj/api'

export default {
  name: 'Announcement Details',
  data () {
    return {
      announcement: null,
      prevAnnouncement: null,
      nextAnnouncement: null,
      btnLoading: false
    }
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      this.btnLoading = true
      try {
        const res = await api.getAnnouncementDetail(this.$route.params.announcementID)
        this.btnLoading = false
        this.announcement = res.data.data.current
        this.prevAnnouncement = 'previous' in res.data.data ? res.data.data.previous : null
        this.nextAnnouncement = 'next' in res.data.data ? res.data.data.next : null
      } catch (err) {
      }
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-M-D')
    }
  },
  watch: {
    async '$route' () {
      await this.init()
    }
  }
}
</script>

<style lang="scss">
  .announcement{
    margin: 0 20%;
  }
  .list-btn{
    margin-top: 100px;
    display: flex;
    justify-content: flex-end;
  }
  .list-btn__router{
    padding: 0.2em 0.6em;
    margin-bottom: 0.2em;
    border-radius: 8px;
    background: transparent;
    color: #7C7C7C;
    border: none;
    &:hover {
      background: #B8B8B8;
    }
  }
  .announcement__header{
    overflow: hidden;
    background: #F9F9F9;
    border-top: 2px solid #7C7C7C;
    border-bottom: 1px solid #B8B8B8;
    color: #7C7C7C;
  }
  .announcement__title{
    float: left;
    margin: 10px 1rem;
    font-size: 24px;
    font-weight: bold;
  }
  .announcement__date{
    float: right;
    margin: 12px 1rem;
    font-size: 20px;
    font-weight: 400;
    text-align: right;
  }
  .announcement__content{
    margin: 30px 1rem;
    color: #696969;

    ul,
    ol {
      padding: 0 1rem;
    }

    code {
      background-color: rgba(#616161, 0.1);
    }

    pre {
      background: #0D0D0D;
      color: #FFF;
      font-family: 'JetBrainsMono', monospace;
      padding: 0.75rem 1rem;
      border-radius: 0.5rem;

      code {
        color: inherit;
        padding: 0;
        background: none;
        font-size: 0.8rem;
      }
    }

    blockquote {
      border-left: 2px solid rgba(#0d0d0d, 0.1);
      padding-left: 1rem;
    }

    img {
      max-width: 100%;
      height: auto;
    }
  }
  .announcement__pagination{
    margin: 120px 0 24px;
    border-top: 2px solid #B8B8B8;
  }
  #announcement__pagination-item {
    border-bottom: 2px solid #B8B8B8;
    height: 50px;
  }
  .pagination-text{
    display: inline-block;
    width: 120px;
    margin: auto 20px;
    color: #696969;
  }
</style>
