<template>
  <b-modal
  id="create-problem-set-group"
  :title="modalTitle"
  size="lg"
  @ok="(modalType === 'create') ? createNewProblemSetGroup() : editProblemSetGroup()"
  @cancel="cancelCreation"
  >
    <b-form>
      <b-form-group
        id="input-group-problem-set-group-title"
        label="Title"
        label-for="input-problem-set-group-title"
        required
        :state="form.title !== ''"
        invalid-feedback="Problem set group title is required"
      >
        <b-form-input
          id="input-problem-set-group-title"
          v-model="form.title"
          placeholder="Enter Title"
          required
          :state="form.title !== ''"
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-problem-set-group-button-type"
        label="Button Type"
        label-for="input-problem-set-group-button-type"
        required
        :state="form.button_type !== ''"
        invalid-feedback="Problem set group button type is required"
      >
        <b-form-select
          id="input-problem-set-group-button-type"
          v-model="form.button_type"
          placeholder="Enter Button Type"
          :options="options_button_type"
          required
        ></b-form-select>
      </b-form-group>
      <b-form-group
        id="input-group-is-disabled"
        label="Disabled"
        label-for="input-is-disabled"
      >
        <b-form-checkbox id="input-is-disabled" v-model="form.is_disabled" switch>
        </b-form-checkbox>
      </b-form-group>
    </b-form>
  </b-modal>
</template>

<script>
import api from '../api.js'
export default {
  name: 'CreateProblemSetGroupModal',
  components: {
  },
  props: [
    'modalType',
    'problemSetGroupId'
  ],
  data () {
    return {
      modalTitle: '',
      form: {
        id: '',
        title: '',
        is_disabled: false,
        button_type: 'color-round-button'
      },
      options_button_type: [
        { text: 'Color round button', value: 'color-round-button', disabled: false },
        { text: 'Shadow round button', value: 'shadow-round-button', disabled: false }
      ]
    }
  },
  methods: {
    async createNewProblemSetGroup () {
      const data = {
        title: this.form.title,
        button_type: this.form.button_type,
        is_disabled: this.form.is_disabled
      }
      await api.createProblemSetGroup(data)
      this.$emit('update')
    },
    async editProblemSetGroup () {
      const data = {
        id: this.form.id,
        title: this.form.title,
        button_type: this.form.button_type,
        is_disabled: this.form.is_disabled
      }
      await api.editProblemSetGroup(data)
      this.$emit('update')
    },
    resetModal () {
      this.form.title = ''
      this.form.button_type = ''
      this.form.is_disabled = false
    },
    async getProblemSetGroupDetail () {
      const res = await api.getProblemSetGroup(this.problemSetGroupId)
      this.form.id = res.data.data.id
      this.form.title = res.data.data.title
      this.form.is_disabled = res.data.data.is_disabled
      this.form.button_type = res.data.data.button_type
    }
  },
  computed: {
    modalTypeOrProblemSetGroupId () {
      return `${this.modalType}|${this.problemSetGroupId}`
    }
  },
  watch: {
    async modalTypeOrProblemSetGroupId () {
      if (this.modalType === 'edit') {
        this.resetModal()
        this.modalTitle = 'Edit Problem Set Group'
        this.getProblemSetGroupDetail()
      } else {
        this.resetModal()
        this.modalTitle = 'Create New Problem Set Group'
      }
    }
  }
}
</script>

<style lang="scss">
</style>
