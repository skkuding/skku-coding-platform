<template>
  <div id="profile-submission-container">
    <div class="submission-list-card font-bold">
      <div class="top-bar mb-4" style="margin-top:4px;">
        <h2 class="title">Submission List</h2>
        <div class="submission-list-table">
          <div class="category-container">
            <button type="button" class="ac-btn btn-outline-success" @click="filterByResult('AC')">Accepted</button>
            <button type="button" class="ac-btn btn-outline-danger" @click="filterByResult('NAC')">Not Accepted</button>
            <div class="col-4">
              <b-icon icon="search" class="search-icon"/>
              <b-input placeholder="keywords" class="search-input"
                v-model="keyword" @input="filterByKeyword"/>
            </div>
          </div>
        </div>
      </div>
      <div class="table">
        <b-table
          hover
          :items="submissionList"
          :fields="submissionTableColumns"
          :per-page="perPage"
          :current-page="currentPage"
          head-variant="light"
          @row-clicked="onMySubmissionClicked"
        >
          <template #cell(result)="data">
            <span style="color: #8DC63F;" v-if="data.item.result==='Accepted'"> {{ data.value }} </span>
            <span style="color: #FF4F28;" v-else> {{ data.value }} </span>
          </template>
          <template #cell(execution)="data">
            <div v-if="data.item.result==='Accepted'">
              <span>{{ data.item.statistic_info.memory_cost }}KB</span> / <span>{{ data.item.statistic_info.time_cost }}ms</span>
            </div>
            <div v-else>
              -
            </div>
          </template>
          <template #cell(code)="data">
            <span>{{ data.item.language }}</span> / <span>{{ data.item.code_length }}B</span>
          </template>
          <template #cell(created_time))="data">
            <span> {{ data.value }} </span>
          </template>
        </b-table>
      </div>
      <div class="pagination">
        <b-pagination
          v-model="currentPage"
          :total-rows="rows"
          :per-page="perPage"
          limit="3"
        ></b-pagination>
      </div>
    </div>
    <b-modal id="submission-detail-modal" centered hide-backdrop hide-footer
      v-model="submission_detail_modal_show">
      <template #modal-header="{ close }">
        <div class="modal-title-close">
          <h1>Submission #{{submission_detail.id}}</h1>
          <b-icon icon="x" class="close-icon" @click="close()"/>
        </div>
      </template>
      <div id="submission-info-table">
        <b-table borderless class="align-center"
          :items="[submission_detail]"
          :fields="submission_info_table_fields">
          <template #cell(result)="data">
            <span :style="'color: '+resultTextColor(data.item.result)">{{data.item.result}}</span>
          </template>
        </b-table>
      </div>
      <div id="submission-compile-error-message" v-if="compile_error_message_show">
        <p class="text-danger"> Compile error message: {{ submission_detail.statistic_info.err_info }} </p>
      </div>
      <div id="submission-source-code">
        <h3>Source Code</h3>
        <p>({{submission_detail.bytes}} Bytes)</p>
        <CodeMirror
          readOnly
          :key="codemirror_key"
          :value="submission_detail.code"
          :language="submission_detail.language"
          theme="material"/>
      </div>
      <div id="submission-detail-table">
        <b-table class="align-center"
          :items="submission_detail.testcases"
          :per-page="submission_detail_table_rows"
          :fields="submission_detail_table_fields"
          v-show="submission_detail.testcases">
          <template #cell(result)="data">
            <span :style="'color: '+resultTextColor(data.item.result)">{{data.item.result}}</span>
          </template>
        </b-table>
      </div>
    </b-modal>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import api from '@oj/api'
import time from '@/utils/time'
import { JUDGE_STATUS } from '@/utils/constants'
import { ProblemMixin } from '@oj/components/mixins'
import CodeMirror from '@oj/components/CodeMirror.vue'

export default {
  name: 'ProfileSubmission',
  mixins: [ProblemMixin],
  components: {
    CodeMirror
  },
  data () {
    return {
      perPage: 20,
      currentPage: 1,
      checked: false,
      submissionList: [],
      limit: 50,
      total: 0,
      keyword: '',
      result: 'All',
      page: 1,
      submissionTableColumns: [
        {
          label: 'Title',
          key: 'title',
          tdClass: 'problem-title-field',
          thClass: 'problem-title-field'
        },
        {
          label: 'Result',
          key: 'result',
          tdClass: 'result'
        },
        {
          label: 'Execution',
          key: 'execution'
        },
        {
          label: 'Code',
          key: 'code'
        },
        {
          label: 'Date',
          key: 'create_time',
          tdClass: 'date'
        }
      ],
      submission_detail: {},
      submission_info_table_fields: [
        { label: 'Submission Time', key: 'create_time' },
        { label: 'User', key: 'username' },
        { label: 'Language', key: 'language' },
        { label: 'Result', key: 'result' }
      ],
      submission_detail_table_rows: 5,
      submission_detail_table_fields: [
        { label: '#', key: 'title' },
        { label: 'Result', key: 'result' },
        { label: 'Exec time', key: 'exec_time' },
        { label: 'Memory', key: 'memory' }
      ],
      submission_detail_modal_show: false,
      compile_error_message_show: false,
      codemirror_key: 1
    }
  },
  computed: {
    rows () {
      return this.submissionList.length
    },
    ...mapGetters(['isAuthenticated'])
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      await this.getProfileSubmissionList()
    },
    async getProfileSubmissionList () {
      const offset = (this.page - 1) * this.limit
      console.log(this.result, this.keyword)
      const res = await api.getProfileSubmissionList(offset, this.limit,
        {
          result: this.result,
          keyword: this.keyword,
          page: this.page
        }
      )
      this.total = res.data.data.total
      this.submissionList = res.data.data.results.map(v => {
        v.create_time = time.utcToLocal(v.create_time, 'YYYY-MM-DD HH:mm')
        console.log(v.result)
        v.result = JUDGE_STATUS[v.result].name
        console.log(v.result)
        return v
      })
    },
    async filterByResult (item) {
      this.result = item
      await this.getProfileSubmissionList()
    },
    async filterByKeyword () {
      this.page = 1
      await this.getProfileSubmissionList()
    },
    resultTextColor (result) {
      return result === 'Accepted' ? '#8DC63F' : '#FF4F28'
    },
    async onMySubmissionClicked (item) {
      await this.getSubmissionDetail(item.id)

      this.submission_detail_modal_show = true
      await this.$nextTick()
      await this.$nextTick()
      this.codemirror_key += 1
    },
    async getSubmissionDetail (submissionID) {
      const res = await api.getSubmission(submissionID)
      let data = res.data.data
      if (!this.contestID) {
        delete data.problem
      }
      data = {
        ...data,
        ...data.statistic_info,
        id: data.id.substring(0, 6),
        create_time: time.utcToLocal(data.create_time, 'YYYY-MM-DD HH:mm'),
        result: JUDGE_STATUS[data.result].name,
        bytes: new Blob([data.code]).size,
        testcases: data.info && data.info.data && data.info.data.map(
          tc => {
            return {
              title: tc.test_case,
              result: JUDGE_STATUS[tc.result].name,
              exec_time: tc.real_time,
              memory: tc.memory
            }
          }
        )
      }
      this.compile_error_message_show = data.result === 'Compile Error'

      if (data.info && data.info.data) {
        // score exist means the submission is OI problem submission
        if (data.info.data[0].score !== undefined) {
          // TODO : 테이블에 Score field 추가
        }
        if (this.isAdminRole) {
          // TODO : 테이블에 Admin Column(Real time, Signal) 추가
        }
      }
      this.submission_detail = data
    }
  },
  watch: {
    async 'isAuthenticated' (newVal) {
      await this.init()
    }
  }

}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .top-bar {
    margin-top: 40px;
    margin-left: 68px;
  }
  .title{
    margin-bottom:0;
    color: #7C7A7B;
    display:inline;
    position:relative;
    top:36px;
  }
  .submission-list-card{
    margin:0 auto;
    width:95%;
    font-family:Manrope;
    .submission-list-table{
      width: 95%;
      margin: 0 auto;
    }
  }
  div {
    &.pagination{
      margin-right: 5%;
      margin-top: 20px;
      display: flex;
      justify-content: flex-end;
    }
  }
  .category-container{
    display:flex;
    justify-content:flex-end;
  }
  .ac-btn {
    display: inline-block;
    padding: 2px;
    margin: 0px 2px 0px 2px;
    border-radius: 8px;
    background-color: white;
    color: back;
    font-size: 16px;
    font-family: Manrope;
    text-align: center;
    vertical-align: middle;
    cursor: pointer;
  }

  .problem-title-field{
    width: 25%;
  }
  .dropdown-item{
    font-family: Manrope;
  }
  .search-icon {
    position:absolute;
    top: 11px;
    left: 23px;
  }
  .search-input {
    margin-left: -5px;
    padding-left: 37px;
  }
  .font-bold {
    font-family: manrope_bold;
  }
  .table {
    width:95% !important;
    margin-left:auto;
    margin-right:auto;
  }
  ::v-deep .modal {
    .modal-dialog {
      min-width: 1200px;

      .modal-content {
        color: white;
        border: none;
        border-radius: 10px;
        background: #24272D;
        box-shadow: 0px 0px 15px #000000;

        .modal-header {
          border-bottom: none;

          .modal-title-close {
            width: 100%;
            display: flex;
            flex-direction: row;
            justify-content: space-between;

            h1 {
              display: inline-block;
              margin-top: 10px;
              margin-left: 10px;
              font-size: 35px;
            }

            .close-icon {
              font-size: 60px;
            }
          }
        }

        .modal-body {
          padding: 0;

          #clarifications-table {
            table {
              color: white;

              th {
                min-width: 230px;
                padding: 15px 25px;
                border: none;
              }

              td {
                min-width: 230px;
                padding: 15px 25px;
                border-top: 1px solid #3B4F56;
              }
            }
          }

          #my-submissions-table, #all-submissions-table {
            table {
              color: white;

              th {
                min-width: 100px;
                padding: 15px 25px;
                border: none;
              }

              td {
                min-width: 100px;
                padding: 15px 25px;
                border-top: 1px solid #3B4F56;
                cursor: pointer;
              }
            }
          }

          #submission-info-table {
            table {
              color: white;
              font-size: 15px;
            }

            tr th:first-child,
            tr td:first-child {
              padding-left: 50px;
            }

            tr th:last-child,
            tr td:last-child {
              padding-right: 50px;
            }
          }

          #submission-compile-error-message {
            padding: 20px 50px;
          }

          #submission-source-code {
            padding: 20px 50px;
            padding-bottom: 40px;
            color: white;

            h3 {
              font-size: 30px;
              display: inline;
            }
            p {
              font-size: 25px;
            }
          }

          // occasional code indent css fix
          #submission-source-code::v-deep .CodeMirror-sizer {
            margin-left: 38px !important;
          }

          #submission-source-code::v-deep .CodeMirror-gutter-wrapper {
            left: -38px !important;
          }

          #submission-detail-table {
            table {
              font-size: 13px;
              color: white;
              border-collapse: collapse;

              th {
                border: none;
              }

              td {
                border-color: #3B4F56;
              }

              tr th:first-child,
              tr td:first-child {
                padding-left: 70px;
              }

              tr th:last-child,
              tr td:last-child {
                padding-right: 70px;
              }
            }
          }
        }
      }
    }
  }
</style>
