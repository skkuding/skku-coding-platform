<template>
  <b-modal
  id="createAssignment"
  title="Create New Assignment"
  size="lg"
  @ok="createNewAssignment"
  @cancel="cancelCreation"
  >
    <b-form>
      <b-form-group
        id="input-group-assignment-title"
        label="Assignment Title"
        label-for="input-assignment-title"
        required
        :state="form.title !== ''"
        invalid-feedback="Assignment Title is required"
      >
        <b-form-input
          id="input-assignment-title"
          v-model="form.title"
          placeholder="Enter Title"
          required
          :state="form.title !== ''"
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-assignment-content"
        label="Assignment Content"
        label-for="input-assignment-content"
        required
        :state="form.content !== ''"
        invalid-feedback="Content is required"
      >
        <tiptap v-model="form.content"/>
      </b-form-group>
      <b-row>
        <b-col>
          <b-form-group
            id="input-group-start-time"
            label="Start Time"
            label-for="input-start-time"
            required
            :state="form.startTime !== ''"
            invalid-feedback="Start Time is required"
          >
            <b-form-datepicker
              id="input-start-time"
              v-model="startDate"
              today-button
              close-button
              type="datetime"
              :date-format-options="{ year: 'numeric', month: '2-digit', day: '2-digit' }"
              locale="en"
              placeholder="Start Time"
              style = "margin-bottom:10px"
            />
            <b-form-timepicker
              v-model="startTime"
              show-seconds
              now-button
            >
            </b-form-timepicker>
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group
            id="input-group-end-time"
            label="End Time"
            label-for="input-end-time"
            required
            :state="form.endTime !== ''"
            invalid-feedback="End Time is required"
          >
            <b-form-datepicker
              id="input-end-time"
              v-model="endDate"
              today-button
              close-button
              type="datetime"
              :date-format-options="{ year: 'numeric', month: '2-digit', day: '2-digit' }"
              locale="en"
              placeholder="End Time"
              style = "margin-bottom:10px"
            />
            <b-form-timepicker
              v-model="endTime"
              show-seconds
              now-button
            >
            </b-form-timepicker>
          </b-form-group>
        </b-col>
      </b-row>
    </b-form>
  </b-modal>
</template>

<script>
import api from '../../api.js'
import Tiptap from '../../components/Tiptap.vue'
export default {
  name: 'RegisterNewLectureModal',
  components: {
    Tiptap
  },
  props: [
    'lecture-id'
  ],
  data () {
    return {
      form: {
        title: '',
        content: '',
        start_time: '',
        end_time: ''
      },
      startDate: '',
      startTime: '',
      endDate: '',
      endTime: ''
    }
  },
  methods: {
    async createNewAssignment () {
      console.log(this.lectureId)
      this.setStartTime()
      this.setEndTime()
      const data = {
        title: this.form.title,
        course_id: this.lectureId,
        content: this.form.content,
        start_time: this.form.start_time,
        end_time: this.form.end_time
      }
      await api.createAssignment(data)
      this.$emit('update')
      console.log(data)
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

<style lang="scss">
  // Be careful of common css selector in admin/oj
</style>
