<template>
  <div class="view">
    <Panel title="Judge Server Token">
      <code>{{ token }}</code>
    </Panel>
    <Panel title="Judge Server">
      <b-table
        :items="servers"
        :fields="serverTableFields"
        bordered
        responsive
      >
        <template #cell(status)="row">
          <b-button :variant="row.item.status === 'normal' ? 'success' : 'danger'" size="sm" disabled>
            {{ row.item.status === 'normal' ? 'Normal' : 'Abnormal' }}
          </b-button>
        </template>

        <template #cell(ip)="row">
          <b-button variant="success" size="sm" disabled>
            {{ row.item.ip }}
          </b-button>
        </template>

        <template #cell(judger_version)="row">
          <b-button variant="success" size="sm" disabled>
            {{ row.item.judger_version }}
          </b-button>
        </template>

        <template #cell(service_url)="row">
            <code>{{ row.item.service_url }}</code>
        </template>

        <template #cell(last_heartbeat)="row">
            {{ row.item.last_heartbeat | localtime }}
        </template>

        <template #cell(create_time)="row">
            {{ row.item.create_time | localtime }}
        </template>

        <template #cell(disabled)="row">
          <b-form-checkbox
            v-model="row.item.is_disabled"
            @change="handleDisabledSwitch(row.item.id, row.item.is_disabled)"
            switch
          >
          </b-form-checkbox>
        </template>

        <template #cell(options)="row">
          <b-button
            variant="outline-danger"
            size="sm"
            @click="deleteJudgeServer(row.item.hostname)"
          >
            <b-icon icon="trash-fill" />
          </b-button>
        </template>

        <template #row-details="row">
          <b-card style="padding: 24px;">
            <p>
              IP:
              <b-button variant="success" disabled>
                {{ row.item.ip }}
              </b-button>&nbsp;&nbsp;
                Judger Version:
              <b-button variant="success" disabled>
                {{ row.item.judger_version }}
              </b-button>
            </p>
            <p>Service URL: <code>{{ row.item.service_url }}</code></p>
            <p>Last Heartbeat: {{ row.item.last_heartbeat | localtime }}</p>
            <p>Create Time: {{ row.item.create_time | localtime }}</p>
          </b-card>
        </template>
      </b-table>

    </Panel>
  </div>
</template>

<script>
import api from '../../api.js'

export default {
  name: 'JudgeServer',
  beforeRouteLeave (to, from, next) {
    clearInterval(this.intervalId)
    next()
  },
  data () {
    return {
      servers: [],
      token: '',
      intervalId: -1,
      serverTableFields: [
        { key: 'status', label: 'Status', tdClass: 'align-middle' },
        { key: 'hostname', label: 'hostname', tdClass: 'align-middle' },
        { key: 'task_number', label: 'Task Number', tdClass: 'align-middle' },
        { key: 'cpu_core', label: 'CPU Core', tdClass: 'align-middle' },
        { key: 'cpu_usage', label: 'CPU Usage', tdClass: 'align-middle' },
        { key: 'memory_usage', label: 'Memory Usage', tdClass: 'align-middle' },
        { key: 'ip', label: 'IP', tdClass: 'align-middle' },
        { key: 'judger_version', label: 'Judger Version', tdClass: 'align-middle' },
        { key: 'service_url', label: 'Service URL', tdClass: 'align-middle' },
        { key: 'last_heartbeat', label: 'Last Heartbeat', thStyle: 'min-width: 90px;', tdClass: 'align-middle' },
        { key: 'create_time', label: 'Create time', thStyle: 'min-width: 90px;', tdClass: 'align-middle' },
        { key: 'disabled', label: 'Disabled', tdClass: 'align-middle' },
        { key: 'options', label: 'Options', tdClass: 'align-middle' }
      ]
    }
  },
  async mounted () {
    await this.refreshJudgeServerList()
    this.intervalId = setInterval(async () => {
      await this.refreshJudgeServerList()
    }, 5000)
  },
  methods: {
    async refreshJudgeServerList () {
      const res = await api.getJudgeServer()
      this.servers = res.data.data.servers
      this.token = res.data.data.token
    },
    async deleteJudgeServer (hostname) {
      try {
        await this.$confirm('If you delete this judge server, it can\'t be used until next heartbeat', 'Warning', 'warning', false)
        await api.deleteJudgeServer(hostname)
        await this.refreshJudgeServerList()
      } catch (err) {
      }
    },
    async handleDisabledSwitch (id, value) {
      const data = {
        id,
        is_disabled: value
      }
      await api.updateJudgeServer(data).catch(() => {})
    }
  }
}
</script>
