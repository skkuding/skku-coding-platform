<template>
  <div class="contest-problem-list-card font-bold">
    <Table
      :items="clarifications"
      :fields="contestClarificationFields"
      :per-page="perPage"
      :current-page="currentPage"
      text="No Clarifications"
    >
      <template v-slot:Problem="data">
        {{ data.row.Problem }}
      </template>
      <template v-slot:created_time="data">
        {{ getTimeFormat(data.row.created_time) }}
      </template>
      <template v-slot:Clarifications="data">
        <div v-katex>
          <p v-dompurify-html="data.row.Clarifications"/>
        </div>
      </template>
    </Table>
    <div class="pagination">
      <b-pagination
        v-model="currentPage"
        :total-rows="clarifications.length"
        :per-page="perPage"
        limit="3"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
import api from '@oj/api'
import time from '@/utils/time'
import Table from '@oj/components/Table.vue'

export default {
  name: 'ContestClarification',
  components: {
    Table
  },
  data () {
    return {
      limit: 200,
      total: 0,
      perPage: 10,
      currentPage: 1,
      contestID: '',
      contestProblems: [],
      clarifications: [],
      contestClarificationFields: [
        { key: 'Problem' },
        { key: 'Clarifications' },
        {
          label: 'Create Time',
          key: 'created_time'
        }
      ]
    }
  },
  async mounted () {
    this.contestID = this.$route.params.contestID
    await this.getContestProblems()
    await this.getContestAnnouncementList()
  },
  methods: {
    async getContestProblems () {
      try {
        const res = await this.$store.dispatch('getContestProblems')
        const data = res.data.data
        this.contestProblems = data
      } catch (err) {
      }
    },
    async getContestAnnouncementList () {
      const result = await api.getContestAnnouncementList(this.contestID)
      const data = result.data.data
      this.clarifications = data.map(v => {
        let problemInfo = ''
        for (const problem of this.contestProblems) {
          if (problem.id === v.problem) {
            problemInfo = problem._id + ' ' + problem.title
          }
        }
        return {
          Clarifications: v.content,
          created_time: v.create_time,
          Problem: problemInfo
        }
      })
    },
    getTimeFormat (value) {
      return time.utcToLocal(value, 'YYYY-MM-DD HH:mm')
    }
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
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  div {
    &.pagination{
      margin-right: 5%;
      margin-top: 20px;
      display: flex;
      justify-content: flex-end;
    }
  }
  .font-bold {
    font-family: manrope_bold;
  }
</style>
