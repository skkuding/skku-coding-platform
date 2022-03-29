<template>
  <div class="view">
    <Panel title="Problem Set">
      <div class="table">
        <b-table
          :items="problemSetGroupList"
          :fields="problemSetGroupField"
          head-variant="light"
          @row-clicked="toggleProblemSetGroup"
          :tbody-tr-class="'problem-set-group-table-body'"
        >
          <template #cell(show_detail)="row">
            <b-icon :icon="row.item._showDetails ? 'caret-down-fill':'caret-right-fill'" aria-hidden="true"></b-icon>
          </template>
          <template v-slot:row-details="row" style="padding-left:50px; padding-right:50px">
            <div v-if="!row.item.problemSet.length">
              No Problem Set data! Please add some problem sets
            </div>
            <b-table
              v-else
              :items="row.item.problemSet"
              :fields="problemSetField"
              no-border-collapse
              class="px-5"
            >
              <template v-slot:cell(number)="data">
                {{ data.item.number }}
              </template>
              <template v-slot:cell(title)="data">
                {{ data.item.title }}
              </template>
              <template v-slot:cell(color)="data">
                {{ data.item.color }}
              </template>
              <template v-slot:cell(is_disabled)="data">
                {{ data.item.is_disabled }}
              </template>
              <template v-slot:cell(is_public)="data">
                {{ data.item.is_public }}
              </template>
              <template #cell(operation)="data">
                <div>
                  <icon-btn
                    name="Edit Problem Set"
                    icon="pencil"
                    @click.native="editProblemSet(row.item.id, data.item.id)"
                  />
                  <icon-btn
                    name="Delete Problem Set"
                    icon="trash"
                    @click.native="deleteProblemSet(row.item.id, data.item.id)"
                  />
                  <icon-btn
                    name="Manage problem set's problem list"
                    icon="list"
                    @click.native="showManageProblem(row.item.id, data.item)"
                  />
                </div>
              </template>
            </b-table>
            <b-col class="text-right">
              <b-button
                size="sm"
                style="background-color: #E9A05A; border-color: unset"
                class="mr-2 text-light"
                @click="createProblemSet(row.item.id)"
              >
                +problem set<br>Create a new problem set
              </b-button>
            </b-col>
          </template>
          <template #cell(title)="data">
            {{ data.item.title }}
          </template>
          <template #cell(button_type)="data">
            {{ data.item.button_type }}
          </template>
          <template #cell(is_disabled)="data">
            {{ data.item.is_disabled }}
          </template>
          <template #cell(operation)="data">
            <div>
              <icon-btn
                name="Edit Problem set group"
                icon="pencil"
                @click.native="editProblemSetGroup(data.item.id)"
              />
              <icon-btn
                name="Delete Problem set group"
                icon="trash"
                @click.native="deleteProblemSetGroup(data.item.id)"
              />
            </div>
          </template>
        </b-table>
      </div>
      <b-button
        variant="primary"
        class="mb-2"
        @click="createProblemSetGroup()"
      >
        +Create
      </b-button>
      <problem-set-group-modal
        :problem-set-group-id="selectedProblemSetGroupId"
        :modal-type="modalTypeProblemSetGroup"
        @update="getProblemSetGroupList"
      ></problem-set-group-modal>
      <div v-if="!problemSetGroupList.length">
        No Problem set group
      </div>
    </Panel>
    <problem-set-modal
      :problem-set-id="selectedProblemSetId"
      :problem-set-group-id="selectedProblemSetGroupId"
      :modal-type="modalTypeProblemSet"
      @update="updateProblemSetList(selectedProblemSetGroupId)"
    ></problem-set-modal>
    <manage-problem-modal
      :problem-set="selectedProblemSet"
      @update="updateProblemSetList(selectedProblemSetGroupId)"
    ></manage-problem-modal>
  </div>
</template>

<script>
import api from '../../api.js'
import Panel from '../../components/Panel.vue'
import ProblemSetGroupModal from '../../components/ProblemSetGroupModal.vue'
import ProblemSetModal from '../../components/ProblemSetModal.vue'
import manageProblemModal from '../../components/ManageProblemModal.vue'

export default {
  name: 'ProblemSetList',
  components: {
    Panel,
    ProblemSetGroupModal,
    ProblemSetModal,
    manageProblemModal
  },
  props: [
  ],
  data () {
    return {
      modalTypeProblemSetGroup: '',
      modalTypeProblemSet: '',
      problemSetGroupField: [
        {
          key: 'show_detail',
          label: ''
        },
        {
          key: 'title',
          label: 'Title'
        },
        {
          key: 'button_type',
          label: 'Button type'
        },
        {
          key: 'is_disabled',
          label: 'Disabled'
        },
        'Operation'
      ],
      problemSetGroupList: [
      ],
      problemSetField: [
        {
          key: '_id',
          label: '#'
        },
        {
          key: 'title',
          label: 'Title'
        },
        {
          key: 'color',
          label: 'Color'
        },
        {
          key: 'is_disabled',
          label: 'Disabled'
        },
        {
          key: 'is_public',
          label: 'Public'
        },
        'Operation'
      ],
      selectedProblemSetGroupId: null,
      selectedProblemSetId: null,
      selectedProblemSet: {}
    }
  },
  async mounted () {
    this.routeName = this.$route.name
    try {
      const res = await api.getProblemSetGroup()
      this.problemSetGroupList = res.data.data.map(problemSetGroup => Object.assign(problemSetGroup, { _showDetails: false }))
    } catch (err) {
    }
  },
  methods: {
    async getProblemSetGroupList () {
      const res = await api.getProblemSetGroup()
      this.problemSetGroupList = res.data.data
    },
    async createProblemSetGroup () {
      this.modalTypeProblemSetGroup = 'create'
      this.$bvModal.show('create-problem-set-group')
    },
    async editProblemSetGroup (problemSetGroupId) {
      this.modalTypeProblemSetGroup = 'edit'
      this.selectedProblemSetGroupId = problemSetGroupId
      await this.$bvModal.show('create-problem-set-group')
    },
    async updateProblemSetList (problemSetGroupId) {
      const res = await api.getProblemSet(problemSetGroupId)
      for (let i = 0; i < this.problemSetGroupList.length; i++) {
        if (this.problemSetGroupList[i].id === problemSetGroupId) {
          this.$set(this.problemSetGroupList[i], 'problemSet', res.data.data)
          this.problemSetGroupList[i]._showDetails = false
          this.$set(this.problemSetGroupList[i], '_showDetails', true)
        }
      }
    },
    async toggleProblemSetGroup (item) {
      if (item._showDetails) {
        item._showDetails = false
      } else if (item.problemSet) {
        this.$set(item, '_showDetails', true)
      } else {
        const res = await api.getProblemSet(item.id)
        item.problemSet = res.data.data
        this.$set(item, '_showDetails', true)
      }
    },
    async createProblemSet (problemSetGroupId) {
      this.modalTypeProblemSet = 'create'
      this.selectedProblemSetGroupId = problemSetGroupId
      this.$bvModal.show('create-problem-set')
    },
    async editProblemSet (problemSetGroupId, problemSetId) {
      this.modalTypeProblemSet = 'edit'
      this.selectedProblemSetGroupId = problemSetGroupId
      this.selectedProblemSetId = problemSetId
      await this.$bvModal.show('create-problem-set')
    },
    async deleteProblemSetGroup (problemSetGroupId) {
      try {
        await this.$confirm('Sure to delete this problemSetGroup?', 'Delete problem set group', 'warning', false)
        await api.deleteProblemSetGroup(problemSetGroupId)
        this.getProblemSetGroupList()
      } catch (err) {
      }
    },
    async deleteProblemSet (problemSetGroupId, problemSetId) {
      try {
        await this.$confirm('Sure to delete this problem set?', 'Delete Problem set', 'warning', false)
        await api.deleteProblemSet(problemSetId)
        await this.updateProblemSetList(problemSetGroupId)
      } catch (err) {
      }
    },
    async showManageProblem (problemSetGroupId, problemSet) {
      this.selectedProblemSet = problemSet
      this.selectedProblemSetGroupId = problemSetGroupId
      await this.$bvModal.show('manage-problem')
    }
  },
  computed: {
  }
}
</script>

<style lang="scss">
  .problem-set-group-table-body:not(.b-table-details) {
    cursor: pointer;
  }
  .problem-set-group-table-body:not(.b-table-details):hover {
    background-color: #d6d6d6
  }
</style>
