<template>
  <b-modal
  id="create-assignment"
  :title="modalTitle"
  size="lg"
  @ok="(modalType === 'create') ? createNewAssignment() : editAssignment()"
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
      <b-form-group
        v-if="modalType === 'create'"
        id="input-group-visible"
        label="Visible"
        label-for="input-visible"
      >
        <b-form-checkbox id="input-visible" v-model="form.visible" style="pointer:" switch>
        </b-form-checkbox>
      </b-form-group>
    </b-form>
  </b-modal>
</template>

<script>
import api from '../../api.js'
import Tiptap from '../../components/Tiptap.vue'
export default {
  name: 'CreateAssignmentModal',
  components: {
    Tiptap
  },
  props: [
    'courseId',
    'modalType',
    'assignmentId'
  ],
  data () {
    return {
      modalTitle: '',
      form: {
        id: '',
        title: '',
        content: '',
        start_time: '',
        end_time: '',
        visible: false
      },
      startDate: '',
      startTime: '',
      endDate: '',
      endTime: ''
    }
  },
  methods: {
    async createNewAssignment () {
      this.setStartTime()
      this.setEndTime()
      const data = {
        title: this.form.title,
        course_id: this.courseId,
        content: this.form.content,
        start_time: this.form.start_time,
        end_time: this.form.end_time,
        visible: this.form.visible
      }
      await api.createAssignment(data)
      this.$emit('update')
    },
    async editAssignment () {
      this.setStartTime()
      this.setEndTime()
      const data = {
        id: this.form.id,
        title: this.form.title,
        course_id: this.courseId,
        content: this.form.content,
        start_time: this.form.start_time,
        end_time: this.form.end_time,
        visible: this.form.visible
      }
      await api.editAssignment(data)
      this.$emit('update')
    },
    resetModal () {
      this.form.title = ''
      this.form.content = ''
      this.startDate = ''
      this.startTime = ''
      this.endDate = ''
      this.endTime = ''
    },
    setStartTime () {
      this.form.start_time = this.startDate + ' ' + this.startTime
    },
    setEndTime () {
      this.form.end_time = this.endDate + ' ' + this.endTime
    },
    async getAssignmentDetail () {
      const res = await api.getAssignmentList(this.courseId, this.assignmentId)
      this.form.title = res.data.data.title
      this.form.content = res.data.data.content
      ;[this.startDate, this.startTime] = res.data.data.start_time.split(/T|[+]/)
      ;[this.endDate, this.endTime] = res.data.data.end_time.split(/T|[+]/)
      this.startTime = this.startTime.split('.')[0]
      this.endTime = this.endTime.split('.')[0]
      this.form.visible = res.data.data.visible
      this.form.id = res.data.data.id
    }
  },
  computed: {
    modalTypeOrAssignmentId () {
      return `${this.modalType}|${this.assignmentId}`
    }
  },
  watch: {
    async modalTypeOrAssignmentId () {
      if (this.modalType === 'edit') {
        this.resetModal()
        this.modalTitle = 'Edit Assignment'
        this.getAssignmentDetail()
      } else {
        this.resetModal()
        this.modalTitle = 'Create New Assignment'
      }
    }
  }
}
</script>

<style lang="scss">
</style>
