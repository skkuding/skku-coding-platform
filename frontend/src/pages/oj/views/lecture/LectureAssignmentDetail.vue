<template>
  <div>
    <Sidemenu/>
    <article class="lecture-assignment-card">
      <section class="top-bar mb-4">
        <div class="assignment-title">{{ assignment.title }}</div>
        <div class="assignment-info">
          {{ formatTime(assignment.start_time) + ' ~ ' + formatTime(assignment.end_time) }}
          <!-- <b-badge class="due"> {{ '- ' +  this.$store.state.now }}</b-badge> -->
        </div>
      </section>
      <section class="assignment-container">
        <p class="assignment__content" v-dompurify-html="assignment.content"></p>
        <div class="table">
          <b-table
            hover
            :items="assignmentProblems"
            :fields="assignmentProblemListFields"
            head-variant="light"
            class="table"
            @row-clicked="goAssignmentProblem"
          >
            <template #cell(total_score)="data">
              {{ '/ ' + data.item.total_score }}
            </template>
          </b-table>
        </div>
      </section>
      <div class="pagination">
        <b-pagination
          v-model="currentPage"
          :total-rows="assignment.length"
          :per-page="perPage"
          limit="3"
        ></b-pagination>
      </div>
    </article>
  </div>
</template>

<script>
import Sidemenu from '@oj/components/Sidemenu.vue'
// import { types } from '@/store'
import moment from 'moment'
import { mapActions, mapState } from 'vuex'
import time from '@/utils/time'
// import api from '@oj/api'

export default {
  name: 'LectureAssignmentDetail',
  components: {
    Sidemenu
  },
  data () {
    return {
      assignment: {},
      assignmentProblemListFields: [
        {
          key: '_id',
          label: '#'
        },
        'type',
        'title',
        {
          key: 'total_score',
          label: 'score'
        }
      ],
      assignmentProblems: [],
      due: ''
    }
  },
  async mounted () {
    this.assignmentID = this.$route.params.assignmentID
    this.courseID = this.$route.params.courseID
    this.route_name = this.$route.name
    try {
      await this.getLectureAssignment()
      await this.getLectureAssignmentProblems()
      // this.changeDomTitle({ title: res.data.data.title })
      // const data = res.data.data
      // this.assignment = data
      // const endTime = moment(data.end_time)
      // if (endTime.isAfter(moment(data.now))) {
      //   this.timer = setInterval(() => {
      //     // this.due = endTime.diff(this.state.now, 'minutes')
      //     // console.log('now :' + now + ' due: ' + this.due)
      //     this.$store.commit(types.NOW_ADD_1S)
      //   }, 1000)
      // }
    } catch (err) {
      console.log(err)
    }
  },
  methods: {
    async getLectureAssignment () {
      try {
        const res = await this.$store.dispatch('getLectureAssignment')
        const data = res.data.data
        this.assignment = data
        this.changeDomTitle({ title: data.title })
      } catch (err) {
        console.log(err)
      }
    },
    async getLectureAssignmentProblems () {
      try {
        const res = await this.$store.dispatch('getLectureAssignmentProblems')
        const data = res.data.data.results
        this.assignmentProblems = data
      } catch (err) {
      }
    },
    async goAssignmentProblem (row) {
      await this.$router.push({
        name: 'lecture-assignment-problem-details',
        params: {
          courseID: this.$route.params.courseID,
          assignmentID: this.$route.params.assignmentID,
          problemID: row._id
        }
      })
    },
    // remainEndTime (endTime) {
    //   var due = moment(this.assignment.end_time).diff(moment(), 'minutes')
    //   return time.utcToLocal(due, 'DD : hh : mm')
    // },
    formatTime (timeValue) {
      return time.utcToLocal(timeValue, 'YYYY-M-D hh:mm')
    },
    formatTime2 (timeValue) {
      return time.utcToLocal(timeValue, 'hh:mm:ss')
    },
    ...mapActions(['changeDomTitle'])
  },
  computed: {
  },
  watch: {
    ...mapState({
      now: state => state.assignment.now
    }),
    now: function () {
      const endTime = moment(this.assignment.end_time)
      return endTime.diff(this.$store.state.now, 'seconds')
    }
  }
}
</script>

<style lang="scss" scoped>
  @font-face {
    font-family: Manrope_bold;
    src: url('../../../../fonts/Manrope-Bold.ttf');
  }
  .lecture-assignment-card{
    margin: 0 auto;
    width: 70%;
    font-family: Manrope_bold;
    .assignment__content{
      width: 90%;
      margin: 0 auto 20px;
      height: 150px;
      border-radius: 10px;
      background-color: #EDECEC;
      padding: 25px;
      overflow: auto;
    }
    .table{
      width: 95% !important;
      margin: 0 auto;
    }
  }
  .top-bar {
    margin-top: 40px;
    margin-left: 68px;
    & .assignment-title {
      margin-bottom: 10px;
      font-size: 36px;
      color: #7C7A7B;
    }
    & .assignment-info {
      width: 90%;
      display:flex;
      justify-content: space-between;
      font-size: 12px;
      color: #7C7A7B;
      margin: auto 0;
      .due {
        font-weight: 400;
        padding: 5px 10px;
        font-size: 14px;
        background-color: #E9A05A !important;
      }
    }
  }
</style>
