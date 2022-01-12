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
                <template #cell(operation)>
                  <div>
                    <icon-btn
                      name="Edit"
                      icon="pencil"
                    />
                    <icon-btn
                      name="Save"
                      icon="box-arrow-in-down"
                    />
                    <icon-btn
                      name="Delete Contest"
                      icon="trash"
                    />
                  </div>
                </template>
              </b-table>
              <b-button size="sm" variant="warning" class="mr-2" v-b-modal.importProblem>
                +problem<br>From SKKU coding platform
              </b-button>
              <import-public-problem-modal></import-public-problem-modal>
              <b-button size="sm" variant="primary" class="mr-2">
                +problem<br>Create a new problem
              </b-button>
              <!--<div v-if="!problemList.length" v-text="center-align">
                No Problem
              </div>-->
            </template>
            <template #cell(title)="data">
              {{ data.item.title }}
            </template>
            <template #cell(visible)>
              <b-form-checkbox switch size="sm"></b-form-checkbox>
            </template>
            <template #cell(status)>
              <b-icon
                icon="circle-fill"
                class="mb-2"
              >
              </b-icon>
            </template>
            <template #cell(operation)>
              <div>
                <icon-btn
                  name="Edit"
                  icon="pencil"
                />
                <icon-btn
                  name="Save"
                  icon="box-arrow-in-down"
                />
                <icon-btn
                  name="Delete Contest"
                  icon="trash"
                />
              </div>
            </template>
          </b-table>
        </div>
        <b-button variant="primary" class="mb-2" v-b-modal.createAssignment>
          +Create
        </b-button>
        <create-assignment-modal
          :lecture-id="lectureId"
          @update="updateAssignmentList"
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

export default {
  name: 'AssignmentList',
  components: {
    CreateAssignmentModal,
    ImportPublicProblemModal
  },
  props: [
    'lecture-id'
  ],
  data () {
    return {
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
      ],
      problemList: [
        {
          number: 'A',
          type: 'Problem',
          title: '가파른 경사',
          submission: '58/60'
        }
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
