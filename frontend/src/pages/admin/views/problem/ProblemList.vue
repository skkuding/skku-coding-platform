<template>
  <div class="view">
    <Panel :title="contestId ? 'Contest Problem List' : 'Problem List'">
      <div slot="header">
        <b-form-input
          v-model="keyword"
          placeholder="Keywords"
        ></b-form-input>
      </div>
      <b-table
        :items="problemList"
        :fields="fields"
        :per-page="pageSize"
        :current-page="updateCurrentPage"
        responsive
        style="width: 100%"
        @row-dblclicked="handleDblclick"
      >
        <template #cell(edit-id)="row">
          <span v-show="!row.item.isEditing">{{ row.item._id }}</span>
          <b-form-input
            size="sm"
            v-show="row.item.isEditing"
            v-model="row.item._id"
            @keyup.enter.native="handleInlineEdit(row.item)"
          />
        </template>
        <template #cell(is_bank)="row">
          <span v-show="row.item.bank">🏦</span>
        </template>
        <template #cell(edit-title)="row">
          <span v-show="!row.item.isEditing">{{ row.item.title }}</span>
          <b-form-input
            size="sm"
            v-show="row.item.isEditing"
            v-model="row.item.title"
            @keyup.enter.native="handleInlineEdit(row.item)"
          />
        </template>
        <template #cell(create-time)="row">
          {{ row.item.create_time | localtime }}
        </template>
        <template #cell(switch-visible)="row">
          <b-form-checkbox
            v-model="row.item.visible"
            @change="updateProblem(row.item)"
            switch
          >
          </b-form-checkbox>
        </template>
        <template #cell(operation)="row">
          <icon-btn
            name="Edit"
            icon="clipboard-plus"
            @click.native="goEdit(row.item.id)"
          />
          <icon-btn
            v-if="contestId"
            name="Make Public"
            icon="files"
            @click.native="makeContestProblemPublic(row.item.id)"
          />
          <icon-btn
            icon="download"
            name="Download TestCase"
            @click.native="downloadTestCase(row.item.id)"
          />
          <icon-btn
            icon="trash"
            name="Delete Problem"
            @click.native="deleteProblem(row.item.id)"
          />
        </template>
      </b-table>
      <div class="panel-options">
        <b-button
          class="panel-button"
          variant="primary"
          size="sm"
          @click="goCreateProblem"
        >
          + Create
        </b-button>
        <b-button
          class="panel-button"
          v-if="contestId"
          variant="primary"
          size="sm"
          @click="showAddPublicProblemModal"
        >
          + Add From Public Problem
        </b-button>
        <b-pagination
          v-model="currentPage"
          :total-rows="total"
          :per-page="pageSize"
          align="right"
          style="position: absolute; right:20px; top: 15px;"
        />
      </div>
    </Panel>

    <b-modal
      title="Sure to update the problem?"
      centered
      ref="update-problem"
      @ok="updateProblem(currentRow)"
      @hidden="getProblemList(currentPage)"
    >
      <div>
        <p>DisplayID: {{ currentRow._id }}</p>
        <p>Title: {{ currentRow.title }}</p>
      </div>
    </b-modal>

    <b-modal
      v-if="contestId"
      title="Add Contest Problem"
      hide-footer
      ref="add-public-problem"
      size="lg"
      centered
    >
      <add-problem-component
        :contest-i-d="contestId"
        @on-change="getProblemList"
      />
    </b-modal>
  </div>
</template>

<script>
import api from '../../api.js'
import utils from '@/utils/utils'
import AddProblemComponent from './AddPublicProblem.vue'

export default {
  name: 'ProblemList',
  components: {
    AddProblemComponent
  },
  data () {
    return {
      pageSize: 10,
      total: 0,
      problemList: [],
      keyword: '',
      loading: false,
      currentPage: 1,
      routeName: '',
      contestId: '',
      // for make public use
      currentProblemID: '',
      currentRow: {},
      fields: [
        { key: 'id', label: 'ID', tdClass: 'problemListTable' },
        { key: 'edit-id', label: 'Display ID', tdClass: 'problemListTable' },
        { key: 'is_bank', label: 'Bank', tdClass: 'problemListTable' },
        { key: 'edit-title', label: 'Title', tdClass: 'problemListTable' },
        { key: 'created_by.username', label: 'Author', tdClass: 'problemListTable' },
        { key: 'create-time', label: 'Create Time', tdClass: 'problemListTable' },
        { key: 'switch-visible', label: 'Visible', tdClass: 'problemListTable' },
        { key: 'operation', label: 'Operation', tdClass: 'problemOptionField', thClass: 'problemOptionField' }
      ]
    }
  },
  watch: {
    async '$route' (newVal, oldVal) {
      this.contestId = newVal.params.contestId
      this.routeName = newVal.name
      await this.getProblemList(this.currentPage)
    },
    async 'keyword' () {
      await this.currentChange()
    }
  },
  mounted () {
    this.routeName = this.$route.name
    this.contestId = this.$route.params.contestId
    this.getProblemList(this.currentPage)
  },
  methods: {
    handleDblclick (row) {
      row.isEditing = true
    },
    goEdit (problemId) {
      if (this.routeName === 'problem-list') {
        this.$router.push({ name: 'edit-problem', params: { problemId } })
      } else if (this.routeName === 'contest-problem-list') {
        this.$router.push({ name: 'edit-contest-problem', params: { problemId: problemId, contestId: this.contestId } })
      }
    },
    goCreateProblem () {
      if (this.routeName === 'problem-list') {
        this.$router.push({ name: 'create-problem' })
      } else if (this.routeName === 'contest-problem-list') {
        this.$router.push({ name: 'create-contest-problem', params: { contestId: this.contestId } })
      }
    },
    // 切换页码回调
    async currentChange (page) {
      if (this.contestId !== '') {
        this.currentPage = page
        await this.getProblemList(page)
      }
    },
    async getProblemList (page = 1) {
      this.loading = true
      const funcName = this.routeName === 'problem-list' ? 'getProblemList' : 'getContestProblemList'
      const params = {
        limit: this.pageSize,
        offset: (page - 1) * this.pageSize,
        keyword: this.keyword,
        contest_id: this.contestId
      }
      try {
        const res = await api[funcName](params)
        this.loading = false
        this.total = res.data.data.total
        for (const problem of res.data.data.results) {
          problem.isEditing = false
        }
        this.problemList = res.data.data.results
      } catch (err) {
        this.loading = false
      }
    },
    async deleteProblem (id) {
      try {
        await this.$confirm('Sure to delete this problem? The associated submissions will be deleted as well.', 'Delete Problem', 'warning', false)
        const funcName = this.routeName === 'problem-list' ? 'deleteProblem' : 'deleteContestProblem'
        await api[funcName](id)
        await this.getProblemList(this.currentPage - 1)
      } catch (err) {
      }
    },
    async makeContestProblemPublic (problemID) {
      try {
        const value = await this.$prompt('Please input display id for the public problem', 'confirm')
        await api.makeContestProblemPublic({ id: problemID, display_id: value }).catch()
      } catch (err) {
      }
    },
    async updateProblem (row) {
      const data = Object.assign({}, row)
      let funcName = ''
      if (this.contestId) {
        data.contest_id = this.contestId
        funcName = 'editContestProblem'
      } else {
        funcName = 'editProblem'
      }
      try {
        await api[funcName](data)
        this.InlineEditDialogVisible = false
        this.getProblemList(this.currentPage)
      } catch (err) {
        this.InlineEditDialogVisible = false
      }
    },
    handleInlineEdit (row) {
      this.currentRow = row
      this.showUpdateProblemModal()
    },
    downloadTestCase (problemID) {
      const url = '/admin/test_case?problem_id=' + problemID
      utils.downloadFile(url)
    },
    showUpdateProblemModal () {
      this.$refs['update-problem'].show()
    },
    showAddPublicProblemModal () {
      this.$refs['add-public-problem'].show()
    }
  },
  computed: {
    updateCurrentPage () {
      return this.currentChange(this.currentPage)
    }
  }
}
</script>

<style lang="scss" scoped>
  .problemListTable{
    max-width: 120px;
    word-wrap: break-word;
  }
  .problemOptionField {
    min-width: 150px;
  }
  ::v-deep .table td{
    cursor: pointer;
  }
</style>
