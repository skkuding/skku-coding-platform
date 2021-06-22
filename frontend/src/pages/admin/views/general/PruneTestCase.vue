<template>
  <div>
    <panel>
      <span slot="title">Prune Test Case
        <b-popover
          placement="right"
          triggers="hover"
          target="prune-popover"
        >
          These test cases are not owned by any problem, you can clean them safely.
        </b-popover>
        <b-icon
          id="prune-popover"
          icon="question-circle-fill"
        />
      </span>

      <b-table
        :items="data"
        :fields="dataFields"
      >
        <template #cell(create_time)="row">
          {{ row.item.create_time | timestampFormat }}
        </template>

        <template #cell(option)="row">
          <icon-btn
            name="Delete"
            icon="trash"
            @click.native="deleteTestCase(row.item.id)"
          />
        </template>
      </b-table>

      <div
        v-show="data.length > 0"
        class="panel-options"
      >
        <b-button
          variant="warning"
          size="sm"
          icon="el-icon-fa-trash"
          @click="deleteTestCase()"
          style="margin-top: 18px"
        >
          <b-icon icon="trash-fill" />
          Delete All
        </b-button>
      </div>
    </panel>
  </div>
</template>

<script>
import api from '@admin/api'
import moment from 'moment'

export default {
  name: 'PruneTestCase',
  filters: {
    timestampFormat (value) {
      return moment.unix(value).format('YYYY-M-D  HH:mm:ss')
    }
  },
  data () {
    return {
      data: [],
      dataFields: [
        { key: 'create_time', label: 'Last Modified', tdClass: 'align-middle' },
        { key: 'id', label: 'Test Case ID', tdClass: 'align-middle' },
        { key: 'option', label: 'Option', thStyle: 'min-width: 200px;', tdClass: 'align-middle' }
      ]
    }
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      try {
        const res = await api.getInvalidTestCaseList()
        this.data = res.data.data
      } catch (err) {
      }
    },
    async deleteTestCase (id) {
      if (!id) {
        this.loading = true
      }
      await api.pruneTestCase(id)
      this.loading = false
      await this.init()
    }
  }
}
</script>

<style>

</style>
