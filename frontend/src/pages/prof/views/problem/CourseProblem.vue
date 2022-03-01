<template>
  <div class="flex-grow-1 mx-2" style="max-width: 1300px;">
    <b-breadcrumb :items="pageLocations" class="mt-3"></b-breadcrumb>
    <b-row
      type="flex"
      cols = "1"
      class="course-problem"
    >
      <b-col
        id="first-col"
      >
        <b-card class="admin-info drop-shadow-custom" title="Problems">
          <b-table
            borderless
            hover
            tbody-class="table-body"
            :fields="problemListField"
            :items="problemList"
            :per-page="pageSize"
            :current-page="updateCurrentPage"
          >
            <template #cell(assignment_name)="data">
              <div v-if="data.value"> {{ data.value }} </div>
              <div v-else> - </div>
            </template>
            <template #cell(operation)="data">
                <div>
                  <icon-btn
                    name="Edit Problem"
                    icon="pencil"
                    @click.native="editCourseProblem(data.item.assignment, data.item.id)"
                  />
                  <icon-btn
                    name="Delete Problem"
                    icon="trash"
                    @click.native="deleteCourseProblem(data.item.id)"
                  />
                </div>
              </template>
          </b-table>
          <div class="footer">
            <div class="footer-button">
                <b-button
                    size="sm"
                    style="background-color: #4891FE; border-color: unset;"
                    class="mr-2 text-light"
                    @click="showImportPublicProblemModal()"
                >
                    +problem<br>From SKKU coding platform
                </b-button>
                <b-button
                    size="sm"
                    style="background-color: #E9A05A; border-color: unset"
                    class="mr-2 text-light"
                    @click="createCourseProblem()"
                >
                    +problem<br>Create a new problem
                </b-button>
            </div>
            <b-pagination
              v-model="currentPage"
              :per-page="pageSize"
              :total-rows="total"
              limit="3"
            />
          </div>
        </b-card>
      </b-col>
    </b-row>
    <import-public-problem-modal
      :courseId = "courseId"
      @update="updateCourseProblemList()"
      mode="course"
    ></import-public-problem-modal>
  </div>
</template>

<script>
import api from '../../api.js'
import moment from 'moment'
import ImportPublicProblemModal from '../assignment/ImportPublicProblem.vue'

export default {
  name: 'CourseProblem',
  components: {
    ImportPublicProblemModal
  },
  data () {
    return {
      pageSize: 20,
      currentPage: 1,
      pageLocations: [
        {
          text: '',
          to: '/course/' + this.$route.params.courseId + '/dashboard'
        },
        {
          text: 'Problems'
        }
      ],
      problemListField: [
        {
          key: '_id',
          label: '#'
        },
        'title',
        {
          key: 'assignment_name',
          label: 'Assignment'
        },
        {
          key: 'create_time',
          label: 'Create Time',
          formatter: (value) => {
            return moment(value).format('YYYY-M-D HH:mm')
          }
        },
        {
          key: 'operation',
          label: 'Operation'
        }
      ],
      problemList: [],
      total: 0,
      courseId: 0,
      title: '',
      courseCode: '',
      classNumber: ''
    }
  },
  async mounted () {
    this.courseId = this.$route.params.courseId
    // for breadcrumb - get course information
    try {
      const res = await api.getCourseList(this.courseId)
      const data = res.data.data
      this.title = data.title
      this.courseCode = data.course_code
      this.classNumber = data.class_number
    } catch (err) {
    }
    this.pageLocations[0].text = this.title + '_' + this.courseCode + '-' + this.classNumber
  },
  methods: {
    async getCourseProblem (page) {
      try {
        this.problemList = []
        const res = await api.getCourseProblem(this.$route.params.courseId, null, this.pageSize, (page - 1) * this.pageSize)
        const data = res.data.data.results
        this.problemList.push(...data)
        this.total = res.data.data.total
        console.log(this.problemList)
      } catch (err) {
      }
    },
    showImportPublicProblemModal () {
      this.$bvModal.show('import-public-problem-modal')
    },
    async updateCourseProblemList () {
      await this.getCourseProblem(1)
    },
    async updateCurrentPageProblem (page) {
      this.currentPage = page
      await this.getCourseProblem(page)
    },
    createCourseProblem () {
      this.$router.push({
        name: 'create-course-problem',
        params: {
          courseId: this.courseId,
          courseInfo: this.pageLocations[0].text
        }
      })
    },
    async editCourseProblem (assignment, problemId) {
      if (assignment) {
        const res = await api.getAssignmentList(this.courseId, assignment)
        this.$router.push({
          name: 'edit-assignment-problem',
          params: {
            courseId: this.courseId,
            assignmentId: assignment,
            problemId: problemId,
            courseInfo: this.pageLocations[0].text,
            assignmentInfo: res.data.data.title
          }
        })
      } else {
        this.$router.push({
          name: 'edit-course-problem',
          params: {
            courseId: this.courseId,
            problemId: problemId,
            courseInfo: this.pageLocations[0].text
          }
        })
      }
    },
    async deleteCourseProblem (problemId) {
      try {
        await this.$confirm('Sure to delete this problem?', 'Delete Problem', 'warning', false)
        await api.deleteCourseProblem(problemId)
        await this.updateCourseProblemList(this.courseId)
      } catch (err) {
      }
    }
  },
  computed: {
    updateCurrentPage () {
      return this.updateCurrentPageProblem(this.currentPage)
    }
  }
}
</script>

<style lang="scss">
  .footer {
    display: flex;
    justify-content: space-between;
  }
</style>
