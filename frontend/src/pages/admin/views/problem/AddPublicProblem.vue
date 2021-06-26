<template>
  <div>
    <b-form-input
      v-model="keyword"
      placeholder="Keywords"
    ></b-form-input>
    <b-table
      :items="problems"
      :fields="fields"
      :per-page="limit"
      :current-page="updatePage"
      >
      <template #cell(option)="row">
        <icon-btn
          icon="plus"
          name="Add the problem"
          @click.native="showConfirmModal(row.item.id)"
        />
      </template>
    </b-table>
    <b-modal
      title="Confirm"
      ref="add-public-problem-confirm"
      centered
      @show="resetConfirmModal"
      @hidden="resetConfirmModal"
      @ok="handleAddProblem"
    >
      <b-form-group
        label="Please input Display ID for the contest problem"
        label-for="display-id-input"
      >
        <b-form-input
          id="display-id-input"
          v-model="displayID"
          required
        ></b-form-input>
      </b-form-group>
    </b-modal>
    <b-pagination
      v-model="page"
      :total-rows="total"
      :per-page="limit"
      >
    </b-pagination>
  </div>
</template>
<script>
import api from '@admin/api'

export default {
  name: 'AddProblemFromPublic',
  props: ['contestID'],
  data () {
    return {
      page: 1,
      limit: 10,
      total: 0,
      problems: [],
      contest: {},
      keyword: '',
      fields: [
        { key: 'id', label: 'ID' },
        { key: '_id', label: 'DisplayID' },
        { key: 'title', label: 'Title' },
        'option'
      ],
      problemID: '',
      displayID: '',
      confirmModalState: null
    }
  },
  watch: {
    'keyword' () {
      this.getPublicProblem(this.page)
    }
  },
  mounted () {
    api.getContest(this.contestID).then(res => {
      this.contest = res.data.data
      this.getPublicProblem()
    }).catch(() => {
    })
  },
  methods: {
    async getPublicProblem (page) {
      const params = {
        keyword: this.keyword,
        offset: (page - 1) * this.limit,
        limit: this.limit,
        rule_type: this.contest.rule_type
      }
      try {
        const results = await api.getProblemList(params)
        this.total = results.data.data.total
        this.problems = results.data.data.results
      } catch (error) {
        console.log(error)
      }
    },
    async handleAddProblem () {
      const data = {
        problem_id: this.problemID,
        contest_id: this.contestID,
        display_id: this.displayID
      }
      try {
        await api.addProblemFromPublic(data)
        this.$emit('on-change')
      } catch (error) {
        console.log(error)
      }
    },
    showConfirmModal (problemID) {
      this.problemID = problemID
      this.$refs['add-public-problem-confirm'].show()
    },
    resetConfirmModal () {
      this.confirmModalState = null
      this.displayID = ''
    }
  },
  computed: {
    updatePage () {
      return this.getPublicProblem(this.page)
    }
  }
}
</script>
<style scoped>
  .page {
    margin-top: 20px;
    text-align: right
  }
</style>
