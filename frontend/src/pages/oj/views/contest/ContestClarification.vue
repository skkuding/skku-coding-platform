<template>
  <div class="contest-problem-list-card font-bold">
    <div class="table">
      <b-table
        hover
        :items="clarifications"
        :fields="contestClarificationFields"
        :per-page="perPage"
        :current-page="currentPage"
        head-variant="light"
        class="text-center"
      >
        <template #cell(Clarifications)="data">
          <div v-katex>
            <p v-dompurify-html="data.value"/>
          </div>
        </template>
        <template #cell(created_time)="data">
          {{ getTimeFormat(data.value) }}
        </template>
      </b-table>
    </div>
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

export default {
  name: 'ContestClarification',
  components: {
  },
  data () {
    return {
      limit: 200,
      total: 0,
      perPage: 10,
      currentPage: 1,
      contestProblems: [],
      clarifications: [],
      contestClarificationFields: [
        'Problem',
        'Clarifications',
        {
          label: 'Created Time',
          key: 'created_time'
        }
      ]
    }
  },
  async mounted () {
    await this.getContestProblems()
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
  .table {
    cursor: pointer;
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
