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
            <div v-if="!row.item.problemList.length">
              No Problem data! Please add some problems
            </div>
            <b-table
              v-else
              :items="row.item.problemList"
              :fields="problemField"
              no-border-collapse
              class="px-5"
            >
              <template v-slot:cell(number)="data">
                {{ data.item.number }}
              </template>
              <template v-slot:cell(title)="data">
                {{ data.item.title }}
              </template>
              <template v-slot:cell(submission)="data">
                {{ data.item.total_submission_assignment }} / {{ studentTotal }}
              </template>
              <template #cell(operation)="data">
                <div>
                  <icon-btn
                    name="Edit Problem"
                    icon="pencil"
                    @click.native="editAssignmentProblem(row.item, data.item.id)"
                  />
                  <icon-btn
                    name="Grade Problem"
                    icon="check2-all"
                    @click.native="gradeProblem(row.item, data.item)"
                  />
                  <icon-btn
                    name="Delete Problem"
                    icon="trash"
                    @click.native="deleteAssignmentProblem(row.item.id, data.item.id)"
                  />
                </div>
              </template>
            </b-table>
            <b-col class="text-right">
              <b-button
                size="sm"
                style="background-color: #4891FE; border-color: unset;"
                class="mr-2 text-light"
                @click="showImportPublicProblemModal(row.item.id)"
              >
                +problem<br>From SKKU coding platform
              </b-button>
              <b-button
                size="sm"
                style="background-color: #E9A05A; border-color: unset"
                class="mr-2 text-light"
                @click="createAssignmentProblem(row.item)"
              >
                +problem<br>Create a new problem
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
      <create-problem-set-group-modal
        :problem-set-group-id="selectedProblemSetGroupId"
        :modal-type="modalType"
        @update="getProblemSetGroupList"
      ></create-problem-set-group-modal>
      <div v-if="!problemSetGroupList.length">
        No Problem set group
      </div>
    </Panel>
  </div>
</template>

<script>
import api from '../../api.js'
import Panel from '../../components/Panel.vue'
import CreateProblemSetGroupModal from '../../components/CreateProblemSetGroupModal.vue'

export default {
  name: 'ProblemSetList',
  components: {
    Panel,
    CreateProblemSetGroupModal
  },
  props: [
    'course-id',
    'modal-type'
  ],
  data () {
    return {
      modalType: '',
      pageLocations: [
        {
          text: '',
          to: '/course/' + this.$route.params.courseId + '/dashboard'
        },
        {
          text: 'Assignments'
        }
      ],
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
      problemField: [
        {
          key: '_id',
          label: '#'
        },
        {
          key: 'title',
          label: 'Title'
        },
        {
          key: 'submission',
          label: 'Submission rate'
        },
        'Operation'
      ],
      selectedAssignmentId: null,
      studentTotal: 0
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
      const res = await api.getProblemSetGroup(this.courseId)
      this.problemSetGroupList = res.data.data
    },
    async createProblemSetGroup () {
      this.modalType = 'create'
      this.$bvModal.show('create-problem-set-group')
    },
    async editProblemSetGroup (problemSetGroupId) {
      this.modalType = 'edit'
      this.selectedProblemSetGroupId = problemSetGroupId
      await this.$bvModal.show('create-problem-set-group')
    },
    async updateAssignmentProblemList (assignmentId) {
      const res = await api.getAssignmentProblem(assignmentId)
      for (let i = 0; i < this.assignmentList.length; i++) {
        if (this.assignmentList[i].id === assignmentId) {
          this.$set(this.assignmentList[i], 'problemList', res.data.data)
          this.assignmentList[i]._showDetails = false
          this.$set(this.assignmentList[i], '_showDetails', true)
        }
      }
    },
    async toggleProblemSetGroup (item) {
      if (item._showDetails) {
        item._showDetails = false
      } else if (item.problemList) {
        this.$set(item, '_showDetails', true)
      } else {
        const res = await api.getAssignmentProblem(item.id)
        item.problemList = res.data.data
        this.$set(item, '_showDetails', true)
      }
    },
    createAssignmentProblem (assignment) {
      if (this.routeName === 'course-assignment-list') {
        this.$router.push({
          name: 'create-course-problem',
          params: {
            assignmentId: assignment.id,
            courseInfo: this.pageLocations[0].text,
            assignmentInfo: assignment.title
          }
        })
      }
    },
    editAssignmentProblem (assignment, problemId) {
      if (this.routeName === 'course-assignment-list') {
        this.$router.push({
          name: 'edit-course-problem',
          params: {
            courseId: this.courseId,
            assignmentId: assignment.id,
            problemId: problemId,
            courseInfo: this.pageLocations[0].text,
            assignmentInfo: assignment.title
          }
        })
      }
    },
    async deleteProblemSetGroup (problemSetGroupId) {
      try {
        await this.$confirm('Sure to delete this problemSetGroup?', 'Delete problem set group', 'warning', false)
        await api.deleteProblemSetGroup(this.courseId, problemSetGroupId)
        this.getProblemSetGroupList()
      } catch (err) {
      }
    },
    async deleteAssignmentProblem (assignmentId, problemId) {
      try {
        await this.$confirm('Sure to delete this problem?', 'Delete Problem', 'warning', false)
        await api.deleteAssignmentProblem(problemId)
        await this.updateAssignmentProblemList(assignmentId)
      } catch (err) {
      }
    }
  },
  computed: {
  }
}
</script>

<style lang="scss" scoped>
  #assignment-list {
    margin: auto;
    flex:1 0;
    max-width: 1300px;
  }
</style>
<style lang="scss">
  .problem-set-group-table-body:not(.b-table-details) {
    cursor: pointer;
  }
  .problem-set-group-table-body:not(.b-table-details):hover {
    background-color: #d6d6d6
  }
</style>
