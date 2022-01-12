<template>
  <b-row
    type="flex"
    cols = "1"
    id="dashboard"
  >
    <b-col>
      <b-card title="Assignments">
        <div class="table">
          <b-table
            borderless
            hover
            :items="assignmentList"
            :fields="assignmentField"
            :current-page="updateAssignmentList"
            head-variant="light"
          >
            <template #cell(show_detail)="row">
              <b-button size="sm" @click="updateAssignmentProblem(row.item.id);row.toggleDetails()" class="mb-2">
                <b-icon icon="caret-right-fill" aria-hidden="true"></b-icon>
              </b-button>
            </template>
            <template v-slot:row-details="row">
              <b-table
                borderless
                hover
                :items="row.item.problemList"
                :fields="problemField"
              >
                <template #cell(number)="data">
                  {{ data.item.number }}
                </template>
                <template #cell(type)="data">
                  {{ data.item.type }}
                </template>
                <template #cell(title)="data">
                  {{ data.item.title }}
                </template>
                <template #cell(submission)="data">
                  {{ data.item.submission }}
                </template>
                <template #cell(operation)="data">
                  <div>
                    <icon-btn
                      name="Edit Problem"
                      icon="pencil"
                      @click.native="editAssignmentProblem(data.item.id)"
                    />
                    <icon-btn
                      name="Grade Problem"
                      icon="check2-all"
                      @click="gradeProblem(data.item.id)"
                    />
                    <icon-btn
                      name="Delete Problem"
                      icon="trash"
                      @click.native="deleteAssignmentProblem(row.item.id, data.item.id)"
                    />
                  </div>
                </template>
              </b-table>
              <b-button
                size="sm"
                variant="warning"
                class="mr-2"
                v-b-modal.importProblem
              >
                +problem<br>From SKKU coding platform
              </b-button>
              <import-public-problem-modal></import-public-problem-modal>
              <b-button
                size="sm"
                variant="primary"
                class="mr-2"
                @click.native="createAssignmentProblem(row.item.id)"
              >
                +problem<br>Create a new problem
              </b-button>
              <!--<div v-if="!problemList.length" v-text="center-align">
                No Problem
              </div>-->
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
                class="mb-2"
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
                <create-assignment-modal
                  :lecture-id="lectureId"
                  :modal-type="modalType"
                  @update="showAssignmentList"
                ></create-assignment-modal>
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
          @click.native="createAssignment()"
        >
          +Create
        </b-button>
        <create-assignment-modal
          :lecture-id="lectureId"
          :modal-type="modalType"
          @update="showAssignmentList"
        ></create-assignment-modal>
        <div v-if="!assignmentList.length" v-text="center-align">
          No Assignment
        </div>
      </b-card>
    </b-col>
  </b-row>
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
          key: 'number',
          label: '#'
        },
        {
          key: 'type',
          label: 'Type'
        },
        {
          key: 'title',
          label: 'Title'
        },
        {
          key: 'submission',
          lable: 'Submission'
        },
        'Operation'
      ]
    }
  },
  async mounted () {
    this.lectureId = this.$route.params.lectureId
    console.log(this.lectureId)
    const res = await api.getAssignmentList(this.lectureId)
    this.assignmentList = res.data.data.results
  },
  methods: {
    async showAssignmentList () {
      api.getAssignmentList(this.lectureId)
    },
    async createAssignment () {
      this.modalType = 'create'
      this.$bvModal.show('createAssignment')
    },
    async editAssignment () {
      this.modalType = 'edit'
      this.$bvModal.show('createAssignment')
    },
    async showAssignmentProblemList (assignmentId) {
      api.getAssignmentProblemList(assignmentId)
    },
    async updateAssignmentProblem (assignmentId) {
      const res = await api.getAssignmentProblemList(assignmentId)
      for (let i = 0; i < this.assignmentList.length; i++) {
        if (this.assignmentList[i].id === assignmentId) {
          this.assignmentList[i].problemList = res.data.data.results
        }
        console.log(this.assignmentList[i])
      }
      await this.showAssignmentProblemList(assignmentId)
    },
    createAssignmentProblem () {
      if (this.routeName === 'lecture-assignment-list') {
        this.$router.push({ name: 'create-lecture-problem' })
      }
    },
    editAssignmentProblem (problemId) {
      if (this.routeName === 'lecture-assignment-list') {
        this.$router.push({ name: 'edit-lecture-problem', params: { problemId } })
      }
    },
    gradeProblem (problemId) {
      if (this.routeName === 'lecture-assignment-list') {
        this.$router.push({ name: 'lecture-problem-grade', params: { problemId } })
      }
    },
    async deleteAssignment (assignmentId) {
      try {
        await this.$confirm('Sure to delete this assignment? The associated submissions will be deleted as well.', 'Delete Assignment', 'warning', false)
        api.deleteAssignment(this.lectureId, assignmentId)
        await this.showAssignmentList(this.lectureId)
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
        end_time: res.end_time
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

<style lang="scss">
</style>
