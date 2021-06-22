<template>
  <div>
    <panel>
      <span slot="title">{{ $t('m.Test_Case_Prune_Test_Case') }}
        <el-popover
          placement="right"
          trigger="hover"
        >
          These test cases are not owned by any problem, you can clean them safely.
          <i
            slot="reference"
            class="el-icon-fa-question-circle import-user-icon"
          />
        </el-popover>
      </span>
      <el-table :data="data">
        <el-table-column
          label="Last Modified"
        >
          <template slot-scope="{row}">
            {{ row.create_time | timestampFormat }}
          </template>
        </el-table-column>
        <el-table-column
          prop="id"
          label="Test Case ID"
        />
        <el-table-column
          label="Option"
          fixed="right"
          width="200"
        >
          <template slot-scope="{row}">
            <icon-btn
              name="Delete"
              icon="trash"
              @click.native="deleteTestCase(row.id)"
            />
          </template>
        </el-table-column>
      </el-table>
      <div
        v-show="data.length > 0"
        class="panel-options"
      >
        <el-button
          type="warning"
          size="small"
          :loading="loading"
          icon="el-icon-fa-trash"
          @click="deleteTestCase()"
        >
          Delete All
        </el-button>
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
      loading: false
    }
  },
  async mounted () {
    await this.init()
  },
  methods: {
    async init () {
      await api.getInvalidTestCaseList().then(resp => {
        this.data = resp.data.data
      }, () => {
      })
    },
    async deleteTestCase (id) {
      if (!id) {
        this.loading = true
      }
      await api.pruneTestCase(id).then(async resp => {
        this.loading = false
        await this.init()
      })
    }
  }
}
</script>

<style>

</style>
