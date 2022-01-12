<template>
  <div class="flex-grow-1 mx-2">
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
              hover
              :items="assignmentList"
              :fields="assignmentField"
              :current-page="currentAssignmentList"
              head-variant="light"
            >
              <template #cell(show_detail)="row">
                <b-button size="sm" variant="light" @click="updateAssignmentProblem(row.item)">
                  <b-icon :icon="row.item._showDetails ? 'caret-down-fill':'caret-right-fill'" aria-hidden="true"></b-icon>
                </b-button>
              </template>
              <template v-slot:row-details="row">
                <div v-if="!row.item.problemList.length">
                  No Problem data! Please add some problems
                </div>
                <b-table
                  v-else
                  hover
                  :items="row.item.problemList"
                  :fields="problemField"
                >
                  <template v-slot:cell(number)="data">
                    {{ data.item.number }}
                  </template>
                  <template v-slot:cell(title)="data">
                    {{ data.item.title }}
                  </template>
                  <template v-slot:cell(submission)="data">
                    {{ data.item.accepted_number }} / {{ data.item.submission_number }}
                  </template>
                  <template #cell(operation)="data">
                    <div>
                      <icon-btn
                        name="Edit Problem"
                        icon="pencil"
                        @click.native="editAssignmentProblem(row.item.id, data.item.id)"
                      />
                      <icon-btn
                        name="Grade Problem"
                        icon="check2-all"
                        @click.native="gradeProblem(row.item, data.item.id)"
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
                    v-b-modal.import-public-problem-modal
                  >
                    +problem<br>From SKKU coding platform
                  </b-button>
                  <b-button
                    size="sm"
                    style="background-color: #E9A05A; border-color: unset"
                    class="mr-2 text-light"
                    @click="createAssignmentProblem(row.item.id)"
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
                <b-icon
                  icon="circle-fill"
                  :style="'color:' + assignmentStatus(data.item.status).color"
                >
                </b-icon>
                {{ assignmentStatus(data.item.status).name }}
              </template>
              <template #cell(operation)="data">
                <div>
                  <icon-btn
                    name="Edit Assignment"
                    icon="pencil"
                    @click.native="editAssignment()"
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
            :lecture-id="lectureId"
            :modal-type="modalType"
            @update="getAssignmentList"
          ></create-assignment-modal>
          <import-public-problem-modal></import-public-problem-modal>
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
    'lecture-id',
    'modal-type'
  ],
  data () {
    return {
      ASSIGNMENT_STATUS_REVERSE: ASSIGNMENT_STATUS_REVERSE,
      modalType: '',
      pageLocations: [
        {
          text: '',
          to: '/lecture/' + this.$route.params.lectureId + '/dashboard'
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
          key: 'id',
          label: '#'
        },
        {
          key: 'title',
          label: 'Title'
        },
        {
          key: 'submission',
          label: 'Accepted rate'
        },
        'Operation'
      ]
    }
  },
  async mounted () {
    this.lectureId = this.$route.params.lectureId
    this.routeName = this.$route.name
    console.log(this.lectureId)
    try {
      const res = await api.getCourseList(this.lectureId)
      this.createdBy = res.data.data.created_by
      this.title = res.data.data.title
      this.courseCode = res.data.data.course_code
      this.classNumber = res.data.data.class_number
      this.registeredYear = res.data.data.registered_year
      this.semester = res.data.data.semester
    } catch (err) {
    }
    try {
      const res = await api.getAssignmentList(this.lectureId)
      this.assignmentList = res.data.data.results
    } catch (err) {
    }
    this.pageLocations[0].text = this.title + '_' + this.courseCode + '-' + this.classNumber
  },
  methods: {
    async getAssignmentList () {
      const res = await api.getAssignmentList(this.lectureId)
      this.assignmentList = res.data.data.results
    },
    async createAssignment () {
      this.modalType = 'create'
      this.$bvModal.show('create-assignment')
    },
    async editAssignment () {
      this.modalType = 'edit'
      this.$bvModal.show('create-assignment')
    },
    async showAssignmentProblemList (assignmentId) {
      api.getAssignmentProblem(assignmentId)
    },
    async updateAssignmentProblem (item) {
      console.log('update assignment problem call')
      console.log(item)
      if (item._showDetails) {
        item._showDetails = false
        console.log(item.id + ' close')
      } else if (item.problemList) {
        this.$set(item, '_showDetails', true)
        console.log('data exists ' + item.id + ' open')
      } else {
        const res = await api.getAssignmentProblem(item.id)
        item.problemList = res.data.data.results
        await this.showAssignmentProblemList(item.id)
        this.$set(item, '_showDetails', true)
        console.log('data downloaded ' + item.id + ' open')
      }
    },
    createAssignmentProblem (assignmentId) {
      console.log('route name' + this.routeName + 'assignmentId' + assignmentId)
      if (this.routeName === 'lecture-assignment-list') {
        this.$router.push({ name: 'create-lecture-problem', params: { assignmentId: assignmentId } })
      }
    },
    editAssignmentProblem (assignmentId, problemId) {
      if (this.routeName === 'lecture-assignment-list') {
        this.$router.push({
          name: 'edit-lecture-problem',
          params: { lectureId: this.lectureId, assignmentId: assignmentId, problemId: problemId }
        })
      }
    },
    gradeProblem (assignment, problemId) {
      if (this.routeName === 'lecture-assignment-list') {
        this.$router.push({
          name: 'lecture-problem-grade',
          params: {
            lectureId: this.lectureId,
            assignmentId: assignment.id,
            problemId: problemId,
            lectureInfo: this.pageLocations[0].text,
            assignmentInfo: assignment.title
          }
        })
      }
    },
    async deleteAssignment (assignmentId) {
      try {
        await this.$confirm('Sure to delete this assignment? The associated submissions will be deleted as well.', 'Delete Assignment', 'warning', false)
        api.deleteAssignment(this.lectureId, assignmentId)
        await this.getAssignmentList(this.lectureId)
      } catch (err) {
      }
    },
    async deleteAssignmentProblem (assignmentId, problemId) {
      try {
        await this.$confirm('Sure to delete this problem? The associated submissions will be deleted as well.', 'Delete Problem', 'warning', false)
        api.deleteAssignmentProblem(problemId)
        await this.updateAssignmentProblem(assignmentId)
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
    }
  },
  computed: {
    updateAssignmentList () {
      return this.showAssignmentList(this.lectureId)
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
