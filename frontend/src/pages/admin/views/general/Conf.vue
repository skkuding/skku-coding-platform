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
          <b-row cols="1">
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

    <Panel :title="$t('m.Website_Config')">
      <b-form
        ref="form"
        label-align="left"
        :model="websiteConfig"
      >
        <b-container fluid>
            <b-row>
              <b-col cols = "4">
                <b-form-group
                label-cols-sm="3"
                label-size="sm"
                :label = "$t('m.Base_Url')"
                 required>
                  <b-form-input
                    v-model="websiteConfig.website_base_url"
                    class="mb-2 mr-sm-2 mb-sm-0"
                    placeholder="Website Base Url"
                  />
                </b-form-group>
              </b-col>
              <b-col cols = "4">
                <b-form-group
                  label-cols-sm="2"
                  label-size="sm"
                  :label ="$t('m.Name')"
                  required>
                <b-form-input
                  class="mb-2 mr-sm-2 mb-sm-0"
                  v-model="websiteConfig.website_name"
                  placeholder="Website Name"
                />
                </b-form-group>
              </b-col>
              <b-col cols = "4">
                <b-form-group
                  label-cols-sm="3"
                  label-size="sm"
                  :label = "$t('m.Shortcut')"
                   required>
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
                  :label = "$t('m.Footer')"
                  required>
                  <b-form-input
                    class="mb-2 mr-sm-2 mb-sm-0"
                    v-model="websiteConfig.website_footer"
                    type="textarea"
                    :autosize="{ minRows: 2, maxRows: 4}"
                    placeholder="Website Footer HTML"
                  />
                </b-form-group>
              </b-col>
            </b-row>
            </b-container>
            <b-container fluid>
            <b-row>
              <b-col cols = "6">
              <b-form-group
                  label-cols-sm="5"
                  label-size="sm"
                  :label = "$t('m.Allow_Register')"
                   required>
                  <b-form-checkbox switch
                    v-model="websiteConfig.allow_register"
                    class="mb-2 mr-sm-2 mb-sm-0"
                  >
                  </b-form-checkbox>
              </b-form-group>
              </b-col>
              <b-col cols = "6">
                <b-form-group
                  label-cols-sm="5"
                  label-size="sm"
                  :label = "$t('m.Submission_List_Show_All')"
                   required>
                  <b-form-checkbox switch
                    v-model="websiteConfig.submission_list_show_all"
                    class="mb-2 mr-sm-2 mb-sm-0">
                  </b-form-checkbox>
                </b-form-group>
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
  mounted () {
    api.getSMTPConfig().then(res => {
      if (res.data.data) {
        this.smtp = res.data.data
      } else {
        this.init = true
        this.$warning('Please setup SMTP config at first')
      }
    })
    api.getWebsiteConfig().then(res => {
      this.websiteConfig = res.data.data
    }).catch(() => {
    })
  },
  methods: {
    saveSMTPConfig () {
      if (!this.init) {
        api.editSMTPConfig(this.smtp).then(() => {
          this.saved = true
        }, () => {
        })
      } else {
        api.createSMTPConfig(this.smtp).then(() => {
          this.saved = true
        }, () => {
        })
      }
    },
    testSMTPConfig () {
      this.$prompt('Please input your email', '', {
        inputPattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
        inputErrorMessage: 'Error email format'
      }).then(({ value }) => {
        this.loadingBtnTest = true
        api.testSMTPConfig(value).then(() => {
          this.loadingBtnTest = false
        }, () => {
          this.loadingBtnTest = false
        })
      }).catch(() => {
      })
    },
    saveWebsiteConfig () {
      api.editWebsiteConfig(this.websiteConfig).then(() => {
      }).catch(() => {
      })
    }
  }
}
</script>
