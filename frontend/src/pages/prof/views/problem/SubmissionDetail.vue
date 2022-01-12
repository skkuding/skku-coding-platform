<template>
  <b-modal id="submission-detail-modal" centered hide-backdrop hide-footer @shown="rerenderCodemirror()">
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
        <template #cell(create_time)="data">
          <span>{{data.item.create_time.split(/[T]|[.]|[+]/).slice(0,2).join(' ')}}</span>
        </template>
        <template #cell(result)="data">
          <span :style="'color: '+resultTextColor(data.item.result)">{{getJudgeStatus(data.item.result)}}</span>
        </template>
      </b-table>
    </div>
    <div id="submission-compile-error-message" v-if="compile_error_message_show">
      <p class="text-danger"> Compile error message: {{ submission_detail.statistic_info.err_info }} </p>
    </div>
    <div id="submission-source-code">
      <h3>Source Code</h3>
      <p>({{ getCodeSize(submission_detail.code) }} Bytes)</p>
      <CodeMirror
        readOnly
        :key="codemirror_key"
        :value="submission_detail.code"
        :language="submission_detail.language"
        theme="material"/>
    </div>
    <div id="submission-detail-table">
      <b-table class="align-center"
        v-if="submission_detail.info"
        :items="submission_detail.info.data"
        :per-page="5"
        :fields="submission_detail_table_fields">
        <template #cell(result)="data">
          <span :style="'color: '+resultTextColor(data.item.result)">{{getJudgeStatus(data.item.result)}}</span>
        </template>
      </b-table>
    </div>
  </b-modal>
</template>
<script>
import CodeMirror from '@oj/components/CodeMirror.vue'
import { JUDGE_STATUS } from '@/utils/constants'

export default {
  name: 'SubmissionDetailModal',
  props: ['submission_detail'],
  mounted () {
  },
  components: {
    CodeMirror
  },
  data () {
    return {
      submission_info_table_fields: [
        { label: 'Submission Time', key: 'create_time' },
        { label: 'User', key: 'username' },
        { label: 'Language', key: 'language' },
        { label: 'Result', key: 'result' }
      ],
      submission_detail_table_fields: [
        { label: '#', key: 'test_case' },
        { label: 'Result', key: 'result' },
        { label: 'Exec time', key: 'real_time' },
        { label: 'Memory', key: 'memory' }
      ],
      codemirror_key: 1
    }
  },
  methods: {
    resultTextColor (result) {
      return JUDGE_STATUS[result].color
    },
    rerenderCodemirror () {
      this.codemirror_key += 1
    },
    getJudgeStatus (result) {
      return JUDGE_STATUS[result].name
    },
    getCodeSize (code) {
      const blob = new Blob([code]).size
      return blob
    }
  },
  computed: {
  }
}
</script>

<style lang="scss" scoped>
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
