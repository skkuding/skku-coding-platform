<template>
  <div class="view">
    <Panel :title="title">
      <el-form label-position="top">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item
              :label="$t('m.ContestTitle')"
              required
            >
              <el-input
                v-model="contest.title"
                :placeholder="$t('m.ContestTitle')"
              />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item
              :label="$t('m.ContestDescription')"
              required
            >
              <tiptap v-model="contest.description"/>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item
              :label="$t('m.Contest_Start_Time')"
              required
            >
              <el-date-picker
                v-model="contest.start_time"
                type="datetime"
                :placeholder="$t('m.Contest_Start_Time')"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item
              :label="$t('m.Contest_End_Time')"
              required
            >
              <el-date-picker
                v-model="contest.end_time"
                type="datetime"
                :placeholder="$t('m.Contest_End_Time')"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Contest_Password')">
              <el-input
                v-model="contest.password"
                :placeholder="$t('m.Contest_Password')"
              />
            </el-form-item>
          </el-col>
          <!-- <el-col :span="8">
               <el-form-item :label="$t('m.Contest_Rule_Type')">
               <el-radio class="radio" v-model="contest.rule_type" label="ACM" :disabled="disableRuleType">ACM</el-radio>
               <el-radio class="radio" v-model="contest.rule_type" label="OI" :disabled="disableRuleType">OI</el-radio>
               </el-form-item>
               </el-col> -->
          <el-col :span="8">
            <el-form-item :label="$t('m.Real_Time_Rank')">
              <el-switch
                v-model="contest.real_time_rank"
                active-color="#13ce66"
                inactive-color="#ff4949"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item :label="$t('m.Contest_Status')">
              <el-switch
                v-model="contest.visible"
                active-text=""
                inactive-text=""
              />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item :label="$t('m.Allowed_IP_Ranges')">
              <div
                v-for="(range, index) in contest.allowed_ip_ranges"
                :key="index"
              >
                <el-row
                  :gutter="20"
                  style="margin-bottom: 15px"
                >
                  <el-col :span="8">
                    <el-input
                      v-model="range.value"
                      :placeholder="$t('m.CIDR_Network')"
                    />
                  </el-col>
                  <el-col :span="10">
                    <el-button
                      plain
                      icon="el-icon-fa-plus"
                      @click="addIPRange"
                    />
                    <el-button
                      plain
                      icon="el-icon-fa-trash"
                      @click="removeIPRange(range)"
                    />
                  </el-col>
                </el-row>
              </div>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <save @click.native="saveContest" />
    </Panel>
  </div>
</template>

<script>
import api from '../../api.js'
import Tiptap from '../../components/Tiptap.vue'

export default {
  name: 'CreateContest',
  components: {
    Tiptap
  },
  data () {
    return {
      title: 'Create Contest',
      disableRuleType: false,
      contest: {
        title: '',
        description: '',
        start_time: '',
        end_time: '',
        rule_type: 'ACM',
        password: '',
        real_time_rank: true,
        visible: true,
        allowed_ip_ranges: [{
          value: ''
        }]
      }
    }
  },
  mounted () {
    if (this.$route.name === 'edit-contest') {
      this.title = 'Edit Contest'
      this.disableRuleType = true
      api.getContest(this.$route.params.contestId).then(res => {
        const data = res.data.data
        const ranges = []
        for (const v of data.allowed_ip_ranges) {
          ranges.push({ value: v })
        }
        if (ranges.length === 0) {
          ranges.push({ value: '' })
        }
        data.allowed_ip_ranges = ranges
        this.contest = data
      }).catch(() => {
      })
    }
  },
  methods: {
    saveContest () {
      const funcName = this.$route.name === 'edit-contest' ? 'editContest' : 'createContest'
      const data = Object.assign({}, this.contest)
      const ranges = []
      for (const v of data.allowed_ip_ranges) {
        if (v.value !== '') {
          ranges.push(v.value)
        }
      }
      data.allowed_ip_ranges = ranges
      api[funcName](data).then(res => {
        this.$router.push({ name: 'contest-list', query: { refresh: 'true' } })
      }).catch(() => {
      })
    },
    addIPRange () {
      this.contest.allowed_ip_ranges.push({ value: '' })
    },
    removeIPRange (range) {
      const index = this.contest.allowed_ip_ranges.indexOf(range)
      if (index !== -1) {
        this.contest.allowed_ip_ranges.splice(index, 1)
      }
    }
  }
}
</script>
