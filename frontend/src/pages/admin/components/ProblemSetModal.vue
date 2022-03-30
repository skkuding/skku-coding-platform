<template>
  <b-modal
  id="create-problem-set"
  :title="modalTitle"
  size="lg"
  @ok="(modalType === 'create') ? createProblemSet() : editProblemSet()"
  @cancel="cancelCreation"
  >
    <b-form>
      <b-form-group
        id="input-group-problem-set-title"
        label="Title"
        label-for="input-problem-set-title"
        required
        :state="form.title !== ''"
        invalid-feedback="Problem set title is required"
      >
        <b-form-input
          id="input-problem-set-title"
          v-model="form.title"
          placeholder="Enter Title"
          required
          :state="form.title !== ''"
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-problem-set-color"
        label="Color"
        label-for="input-problem-set-color"
      >
        <b-button id="popover-1-color">
          Select Color
        </b-button>
      </b-form-group>
      <b-popover
        boundary-padding
        target="popover-1-color"
        placement="auto"
        title="Pick color for the problem set"
        triggers="click"
      >
        <color-picker
          :color="color"
          :onStartChange="color => onChangeColor(color, 'start')"
          :onChange="color => onChangeColor(color, 'change')"
          :onEndChange="color => onChangeColor(color, 'end')"
        >
        </color-picker>
      </b-popover>
      <b-form-group
        id="input-group-is-disabled"
        label="Disabled"
        label-for="input-is-disabled"
      >
        <b-form-checkbox id="input-is-disabled" v-model="form.is_disabled" switch>
        </b-form-checkbox>
      </b-form-group>
      <b-form-group
        id="input-group-is-public"
        label="Public"
        label-for="input-is-public"
      >
        <b-form-checkbox id="input-is-public" v-model="form.is_public" switch>
        </b-form-checkbox>
      </b-form-group>
    </b-form>
  </b-modal>
</template>

<script>
import api from '../api.js'
import { ColorPicker } from 'vue-color-gradient-picker'

export default {
  name: 'ProblemSetModal',
  components: {
    ColorPicker
  },
  props: {
    modalType: {
      type: Boolean
    },
    problemSetId: {
      type: Number
    },
    problemSetGroupId: {
      type: Number
    }
  },
  data () {
    return {
      modalTitle: '',
      color: {
        red: 255,
        green: 0,
        blue: 0,
        alpha: 1
      },
      form: {
        id: '',
        title: '',
        color: '',
        is_disabled: false,
        is_public: true,
        problems: []
      }
    }
  },
  methods: {
    async createProblemSet () {
      const data = {
        title: this.form.title,
        problem_set_group_id: this.problemSetGroupId,
        color: this.RGBAColorToString(this.color),
        is_disabled: this.form.is_disabled,
        is_public: this.form.is_public
      }
      await api.createProblemSet(data)
      this.$emit('update')
    },
    async editProblemSet () {
      const data = {
        id: this.form.id,
        title: this.form.title,
        problem_set_group_id: this.problemSetGroupId,
        color: this.RGBAColorToString(this.color),
        is_disabled: this.form.is_disabled,
        is_public: this.form.is_public,
        problems: this.form.problems
      }
      await api.editProblemSet(data)
      this.$emit('update')
    },
    resetModal () {
      this.form.title = ''
      this.form.color = ''
      this.form.is_disabled = false
      this.form.is_public = true
    },
    async getProblemSetDetail () {
      const res = await api.getProblemSet(this.problemSetGroupId, this.problemSetId)
      this.form = res.data.data
    },
    onChangeColor (attrs, name) {
      this.color = { ...attrs }
    },
    RGBAColorToString (rgbaColor) {
      return `rgba(${rgbaColor.red}, ${rgbaColor.green}, ${rgbaColor.blue}, ${rgbaColor.alpha})`
    }
  },
  computed: {
    modalTypeOrProblemSetId () {
      return `${this.modalType}|${this.problemSetId}`
    }

  },
  watch: {
    async modalTypeOrProblemSetId () {
      if (this.modalType === 'edit') {
        this.resetModal()
        this.modalTitle = 'Edit Problem Set'
        this.getProblemSetDetail()
      } else {
        this.resetModal()
        this.modalTitle = 'Create New Problem Set'
      }
    }
  }
}
</script>

<style lang="scss">
  .popover-color {
    min-width: 320px;
  }
</style>
<style src="vue-color-gradient-picker/dist/index.css" lang="css" />
