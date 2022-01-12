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
            <template #cell()="row">
              <b-button size="sm" @click="row.toggleDetails" class="mb-2">
                <b-icon icon="caret-right-fill" aria-hidden="true"></b-icon>
              </b-button>
            </template>
            <template #row-details>
              <b-table
                borderless
                hover
                :items="problemList"
                :fields="problemField"
              >
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
              <div v-if="!problemList.length" v-text="center-align">
                No Problem
              </div>
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
        <create-assignment-modal></create-assignment-modal>
        <div class="pagination">
          <b-pagination
            v-model="currentPage"
            :total-rows="assignmentList.length"
            :per-page="perPage"
            limit="3"
        ></b-pagination>
        </div>
        <div v-if="!assignmentList.length" v-text="center-align">
          No Assignment
        </div>
      </b-card>
    </b-col>
  </b-row>
</template>

<script>
import CreateAssignmentModal from './CreateAssignment.vue'
import ImportPublicProblemModal from './ImportPublicProblem.vue'

export default {
  name: 'AssignmentList',
  components: {
    CreateAssignmentModal,
    ImportPublicProblemModal
  },
  data () {
    return {
      assignmentField: [
        {
          label: ''
        },
        {
          key: 'title',
          label: 'Title'
        },
        'Visible',
        {
          key: 'status',
          label: 'Status'
        },
        'Operation'
      ],
      assignmentList: [
        {
          id: 1,
          title: '1주차 과제',
          content: '<p>1주차 과제입니다.</p>',
          created_by: {
            id: 2,
            username: 'youngHoon',
            real_name: '김영훈'
          },
          course: {
            id: 1,
            title: 'Programming Basics',
            course_code: 'GEDT018',
            class_number: 41,
            registered_year: '2021',
            semester: 1
          },
          start_time: '2021-08-23T18:25:43+09:00',
          end_time: '2021-08-25T19:25:43+09:00',
          status: '-1',
          submitted_problem: 8,
          total_problem: 10
        },
        {
          id: 2,
          title: '2주차 과제',
          content: '<p>2주차 과제입니다. </p>',
          created_by: {
            id: 2,
            username: 'youngHoon',
            real_name: '김영훈'
          },
          course: {
            id: 1,
            title: 'Computer Engineering',
            course_code: 'GEDT018',
            class_number: 41,
            registered_year: '2021',
            semester: 1
          },
          start_time: '2021-08-17T18:25:43+09:00',
          end_time: '2021-08-23T19:25:43+09:00',
          status: '0',
          submitted_problem: 8,
          total_problem: 10
        }
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
  },
  methods: {
  },
  computed: {
  }
}
</script>

<style lang="scss">
  div{
    &.pagination{
    //margin-right: 5%;
    //margin-top: 20px;
    display: flex;
    justify-content: flex-end;
    }
  }
</style>
