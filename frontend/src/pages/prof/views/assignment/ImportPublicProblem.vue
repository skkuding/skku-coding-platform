<template>
  <b-modal
  id="importProblem"
  title="Import a Problem from SKKU Coding platform"
  size="lg"
  ok-title="Select"
  @ok="importProblem"
  @cancel="cancelImportProblem"
  >
    <div>
      <b-icon icon="search" class="search-icon"/>
      <b-input placeholder="keywords" class="search-input mb-4"
        v-model="keyword" @input="filterByKeyword"/>
      <div class="table">
        <b-table
          borderless
          hover
          :items="problemList"
          :fields="problemField"
          head-variant="light"
        >
          <template #cell(number)="data">
            {{ data.item.number }}
          </template>
          <template #cell(title)="data">
            {{ data.item.title }}
          </template>
          <template #cell(level)="data">
            <b-icon
              icon="circle-fill"
              class="mr-2"
            />
            {{ data.item.level }}
          </template>
          <template #cell(submission)="data">
            {{ data.item.submission }}
          </template>
          <template #cell(rate)="data">
            {{ data.item.rate }}
          </template>
        </b-table>
      </div>
      <div class="pagination">
        <b-pagination
          v-model="currentPage"
          :total-rows="problemList.length"
          :per-page="perPage"
          limit="3"
      ></b-pagination>
      </div>
      <div v-if="!problemList.length" v-text="center-align">
        No Problem
      </div>
    </div>
  </b-modal>
</template>

<script>
// import api from '../../api.js'
export default {
  name: 'RegisterNewLectureModal',
  components: {
  },
  data () {
    return {
      problemField: [
        {
          key: 'number',
          label: '#'
        },
        {
          key: 'title',
          label: 'Title'
        },
        {
          key: 'level',
          label: 'Level'
        },
        {
          key: 'submission',
          lable: 'Submissions'
        },
        {
          key: 'rate',
          label: 'AC Rate'
        }
      ],
      problemList: [
        {
          number: '1',
          title: '가파른 경사',
          level: 'Level1',
          submission: '132',
          rate: '92.14%'
        }
      ]
    }
  },
  methods: {
    async submitNewLecture () {
      // await api.registerNewLecture(this.form)
      alert(this.form)
    },
    initTime () {
      ;[this.startDate, this.startTime] = this.form.start_time.split(/T|[+]/)
      ;[this.endDate, this.endTime] = this.form.end_time.split(/T|[+]/)
    },
    setStartTime () {
      this.form.start_time = this.startDate + ' ' + this.startTime
    },
    setEndTime () {
      this.form.end_time = this.endDate + ' ' + this.endTime
    }
  },
  computed: {
  }
}
</script>

<style lang="scss" scoped>
  .search-icon {
    position:absolute;
  }
  .search-input {
    margin-left: -5px;
    padding-left: 37px;
  }
</style>
