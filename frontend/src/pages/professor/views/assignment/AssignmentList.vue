<template>
  <div class="flex-grow-1 mx-2" style="max-width: 1300px;">
    <b-breadcrumb :items="pageLocations" class="mt-3"></b-breadcrumb>
    <b-row
      type="flex"
      cols = "1"
      id="assignment-list"
    >
      <b-col>
        <b-card title="Assignments" class="drop-shadow-custom">
          <div class="table">
            <b-table
              :items="assignmentList"
              :fields="assignmentField"
              :current-page="currentAssignmentList"
              head-variant="light"
              @row-clicked="toggleAssignmentProblem"
              :tbody-tr-class="'assignment-table-body'"
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
              <template #cell(visible)="data">
                <b-form-checkbox
                  switch
                  v-model="data.item.visible"
                  @change="handleVisibleSwitch(data.item)"
                >
                </b-form-checkbox>
              </template>
              <template #cell(status)="data">
                <div
                  v-b-popover.hover.top="data.item.start_time.split(/[T]|[.]|[+]/).slice(0,2).join(' ') + ' ~ ' + data.item.end_time.split(/[T]|[.]|[+]/).slice(0,2).join(' ')"
                  style="width: fit-content; cursor: pointer"
                >
                  <b-icon
                    icon="circle-fill"
                    :style="'color:' + assignmentStatus(data.item.status).color"
                  >
                  </b-icon>
                  {{ assignmentStatus(data.item.status).name }}
                </div>
              </template>
              <template #cell(operation)="data">
                <div>
                  <icon-btn
                    name="Edit Assignment"
                    icon="pencil"
                    @click.native="editAssignment(data.item.id)"
                  />
                  <icon-btn
                    name="Delete Assignment"
                    icon="trash"
                    @click.native="deleteAssignment(data.item.id)"
                  />
                </div>
              </template>
            </b-table>
          </div>
          <b-button
            variant="primary"
            class="mb-2"
            @click="createAssignment()"
          >
            +Create
          </b-button>
          <create-assignment-modal
            :assignment-id="selectedAssignmentId"
            :course-id="courseId"
            :modal-type="modalType"
            @update="getAssignmentList"
          ></create-assignment-modal>
          <import-public-problem-modal
            :assignment-id="selectedAssignmentId"
            @update="updateAssignmentProblemList(selectedAssignmentId)"
          >
          </import-public-problem-modal>
          <div v-if="!assignmentList.length">
            No Assignment
          </div>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import api from '../../api.js'
import CreateAssignmentModal from './CreateAssignment.vue'
import ImportPublicProblemModal from './ImportPublicProblem.vue'
import { ASSIGNMENT_STATUS_REVERSE } from '@/utils/constants'

export default {
  name: 'AssignmentList',
  components: {
    CreateAssignmentModal,
    ImportPublicProblemModal
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
      assignmentField: [
        {
          key: 'show_detail',
          label: ''
        },
        {
          key: 'title',
          label: 'Title'
        },
        {
          key: 'visible',
          label: 'Visible'
        },
        {
          key: 'status',
          label: 'Status'
        },
        'Operation'
      ],
      assignmentList: [

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
    this.courseId = this.$route.params.courseId
    this.routeName = this.$route.name
    try {
      const res = await api.getCourseList(this.courseId)
      this.createdBy = res.data.data.created_by
      this.title = res.data.data.title
      this.courseCode = res.data.data.course_code
      this.classNumber = res.data.data.class_number
      this.registeredYear = res.data.data.registered_year
      this.semester = res.data.data.semester
    } catch (err) {
    }
    try {
      const res = await api.getAssignmentList(this.courseId)
      this.assignmentList = res.data.data.results.map(assignment => Object.assign(assignment, { _showDetails: false }))
    } catch (err) {
    }
    if (this.$route.params.assignmentAnchor) {
      for (const assignment of this.assignmentList) {
        if (assignment.id === this.$route.params.assignmentAnchor) {
          const res = await api.getAssignmentProblem(assignment.id)
          assignment.problemList = res.data.data.results
          assignment._showDetails = true
        }
      }
    }
    this.getUserTotal()
    this.pageLocations[0].text = this.title + '_' + this.courseCode + '-' + this.classNumber
  },
  methods: {
    async getAssignmentList () {
      const res = await api.getAssignmentList(this.courseId)
      this.assignmentList = res.data.data.results
    },
    async createAssignment () {
      this.modalType = 'create'
      this.$bvModal.show('create-assignment')
    },
    async editAssignment (assignmentId) {
      this.modalType = 'edit'
      this.selectedAssignmentId = assignmentId
      await this.$bvModal.show('create-assignment')
    },
    async updateAssignmentProblemList (assignmentId) {
      const res = await api.getAssignmentProblem(assignmentId)
      for (let i = 0; i < this.assignmentList.length; i++) {
        if (this.assignmentList[i].id === assignmentId) {
          this.$set(this.assignmentList[i], 'problemList', res.data.data.results)
          this.assignmentList[i]._showDetails = false
          this.$set(this.assignmentList[i], '_showDetails', true)
        }
      }
    },
    async toggleAssignmentProblem (item) {
      if (item._showDetails) {
        item._showDetails = false
      } else if (item.problemList) {
        this.$set(item, '_showDetails', true)
      } else {
        const res = await api.getAssignmentProblem(item.id)
        item.problemList = res.data.data.results
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
    gradeProblem (assignment, problem) {
      if (this.routeName === 'course-assignment-list') {
        this.$router.push({
          name: 'course-problem-grade',
          params: {
            courseId: this.courseId,
            assignmentId: assignment.id,
            problemId: problem.id,
            courseInfo: this.pageLocations[0].text,
            assignmentInfo: assignment.title,
            problemInfo: problem.title
          }
        })
      }
    },
    async deleteAssignment (assignmentId) {
      try {
        await this.$confirm('Sure to delete this assignment?', 'Delete Assignment', 'warning', false)
        await api.deleteAssignment(this.courseId, assignmentId)
        this.getAssignmentList()
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
    },
    assignmentStatus (status) {
      return {
        name: ASSIGNMENT_STATUS_REVERSE[status].name,
        color: ASSIGNMENT_STATUS_REVERSE[status].color
      }
    },
    async handleVisibleSwitch (res) {
      const data = {
        id: res.id,
        title: res.title,
        course_id: res.course.id,
        content: res.content,
        start_time: res.start_time,
        end_time: res.end_time,
        visible: res.visible
      }
      await api.editAssignment(data)
    },
    showImportPublicProblemModal (assignmentId) {
      this.selectedAssignmentId = assignmentId
      this.$bvModal.show('import-public-problem-modal')
    },
    async getUserTotal () {
      try {
        const res = await api.getCourseStudents(this.courseId, 0, 0)
        this.studentTotal = res.data.data.total
      } catch (err) {
      }
    }
  },
  computed: {
    updateAssignmentList () {
      return this.showAssignmentList(this.courseId)
    }
  }
}
</script>

<style lang="scss" scoped>
  #assignment-list {
    margin: auto;
    flex:1 0;
    max-width: 1300px;
  }
  .drop-shadow-custom {
    filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  }
</style>
<style lang="scss">
  .assignment-table-body:not(.b-table-details) {
    cursor: pointer;
  }
  .assignment-table-body:not(.b-table-details):hover {
    background-color: #d6d6d6
  }
</style>
