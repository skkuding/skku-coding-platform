<template>
  <div class="view">
    <Panel title="SMTP Config">
      <b-form
        label-size="sm"
      >
        <b-container fluid>
          <b-row cols="2">
            <b-col cols ="6">
              <b-form-group
              label-cols-sm="2"
              label-size="sm"
              label-for="server"
              >
                <template v-slot:label>
                  <span class="text-danger">*</span> Server
                </template>
                <b-form-input
                  id="server"
                  v-model="smtp.server"
                  placeholder="SMTP Server Address"
                />
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group
              label-cols-sm="2"
              label-size="sm"
              label-for="port"
              >
                <template v-slot:label>
                  <span class="text-danger">*</span> Port
                </template>
                <b-form-input
                  id="port"
                  v-model="smtp.port"
                  type="number"
                  placeholder="SMTP Server Port"
                />
              </b-form-group>
            </b-col>
          </b-row>
        </b-container>
        <b-container fluid>
          <b-row cols="2">
            <b-col cols="6">
              <b-form-group
              label-cols-sm="2"
              label-size="sm"
              label-for="email"
              >
                <template v-slot:label>
                  <span class="text-danger">*</span> Email
                </template>
                <b-form-input
                  id="email"
                  v-model="smtp.email"
                  placeholder="Account Used To Send Email"
                />
              </b-form-group>
            </b-col>
            <b-col cols = "6">
              <b-form-group
              label-cols-sm="3"
              label-size="sm"
              label-for="password"
              >
                <template v-slot:label>
                  <span class="text-danger">*</span> Password
                </template>
                <b-form-input
                  id="password"
                  v-model="smtp.password"
                  type="password"
                  placeholder="SMTP Server Password"
                />
              </b-form-group>
            </b-col>
          </b-row>
          </b-container>
          <b-container fluid>
          <b-row>
            <b-col cols="3">
              <b-form-group
              label-cols-sm="4"
              label-size="sm"
              label="TLS"
              >
                <b-form-checkbox
                  switch
                  v-model="smtp.tls"
                >
                </b-form-checkbox>
              </b-form-group>
            </b-col>
          </b-row>
        </b-container>
        <b-button
          variant="primary"
          style="margin-right: 8px;"
          @click="saveSMTPConfig"
        >
          Save
        </b-button>
        <b-button
          v-if="saved"
          variant="warning"
          @click="testSMTPConfig"
        >
          Send Test Email
        </b-button>
      </b-form>
    </Panel>

    <Panel title="Web Config">
      <b-form
        ref="form"
        label-align="left"
        :model="websiteConfig"
      >
        <b-container fluid>
          <b-row>
            <b-col cols = "4">
              <b-form-group
              label-cols-sm="4"
              label-size="sm"
              >
              <template v-slot:label>
                <span class="text-danger">*</span> Base Url
              </template>
                <b-form-input
                  v-model="websiteConfig.website_base_url"
                  class="mb-2 mr-sm-2 mb-sm-0"
                  placeholder="Website Base Url"
                />
              </b-form-group>
            </b-col>
            <b-col cols = "4">
              <b-form-group
                label-cols-sm="3"
                label-size="sm"
                >
                <template v-slot:label>
                <span class="text-danger">*</span> Name
              </template>
              <b-form-input
                class="mb-2 mr-sm-2 mb-sm-0"
                v-model="websiteConfig.website_name"
                placeholder="Website Name"
              />
              </b-form-group>
            </b-col>
            <b-col cols = "4">
              <b-form-group
                label-cols-sm="4"
                label-size="sm"
                >
                <template v-slot:label>
                <span class="text-danger">*</span> Shortcut
              </template>
                <b-form-input
                  class="mb-2 mr-sm-2 mb-sm-0"
                  v-model="websiteConfig.website_name_shortcut"
                  placeholder="Website Name Shortcut"
                />
              </b-form-group>
            </b-col>
          </b-row>
          </b-container>
          <b-container fluid>
          <b-row>
            <b-col cols = "12">
              <b-form-group
                label-cols-sm="2"
                label-size="sm"
                >
                <template v-slot:label>
                <span class="text-danger">*</span> Footer
              </template>
                <b-form-textarea
                  class="mb-2 mr-sm-2 mb-sm-0"
                  v-model="websiteConfig.website_footer"
                  rows="2"
                  max-rows="4"
                  placeholder="Website Footer HTML"
                />
              </b-form-group>
            </b-col>
          </b-row>
          </b-container>
          <b-container fluid>
          <b-row>
            <b-col cols="2" style="padding-right: 0px">
              <p>
                Allow Register
              </p>
            </b-col>
            <b-col cols="2">
              <b-form-checkbox
                switch
                v-model="websiteConfig.allow_register"
                class="mb-2 mr-sm-2 mb-sm-0"
              >
              </b-form-checkbox>
            </b-col>
            <b-col cols="3">
              <p>
                Submission List Show All
              </p>
            </b-col>
            <b-col cols="2">
              <b-form-checkbox
                switch
                v-model="websiteConfig.submission_list_show_all"
                class="mb-2 mr-sm-2 mb-sm-0"
              >
              </b-form-checkbox>
            </b-col>
          </b-row>
        </b-container>
      </b-form>
      <b-button
        variant="primary"
        @click="saveWebsiteConfig"
      >
        Save
      </b-button>
    </Panel>
  </div>
</template>

<script>
import api from '../../api.js'

export default {
  name: 'Conf',
  data () {
    return {
      init: false,
      saved: false,
      loadingBtnTest: false,
      smtp: {
        server: 'smtp.example.com',
        port: 25,
        password: '',
        email: 'email@example.com',
        tls: true
      },
      websiteConfig: {}
    }
  },
  async mounted () {
    try {
      const [resSMTP, resWeb] = await Promise.all([api.getSMTPConfig(), api.getWebsiteConfig()])
      if (resSMTP.data.data) {
        this.smtp = resSMTP.data.data
      } else {
        this.init = true
        this.$error('Please setup SMTP config at first')
      }
      this.websiteConfig = resWeb.data.data
    } catch (err) {
    }
  },
  methods: {
    async saveSMTPConfig () {
      try {
        const funcName = this.init ? 'createSMTPConfig' : 'editSMTPConfig'
        await api[funcName](this.smtp)
        this.saved = true
      } catch (err) {
      }
    },
    async testSMTPConfig () {
      try {
        const value = await this.$prompt('Please input your email', '', '', 'info', {
          inputValidator: async (value) => {
            if (/[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/.test(value)) {
              return false
            } else {
              return 'Error email format'
            }
          }
        })
        this.loadingBtnTest = true
        await api.testSMTPConfig(value)
      } catch (err) {
      } finally {
        this.loadingBtnTest = false
      }
    },
    async saveWebsiteConfig () {
      await api.editWebsiteConfig(this.websiteConfig).catch(() => {})
    }
  }
}
</script>
