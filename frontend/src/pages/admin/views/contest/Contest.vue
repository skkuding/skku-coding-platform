<template>
  <div class="view">
    <Panel :title="title">
      <b-row>
        <b-col cols="12">
          <b-form-group
            label-for="ContestTitle"
          >
            <template #label>
              <p class="labels">
                <span class="text-danger">*</span>
                Title
              </p>
            </template>
            <b-form-input
              id="ContestTitle"
              v-model="contest.title"
              placeholder="Title"
            />
          </b-form-group>
        </b-col>
        <b-col cols="12">
          <p
            class="labels"
            v-b-popover.hover="`Detail description about this contest. It may includes contest schedule,
                                eligibility for participation, how to score and rank and what is the prizes, etc.`"
          >
            <span class="text-danger">*</span>
            Description
          </p>
          <tiptap v-model="contest.description"/>
        </b-col>
        <b-col cols="6">
          <b-form-group>
            <template #label>
              <p
                class="labels"
                style="margin-top:16px"
                v-b-popover.hover="`Short descriptions of who are eligible to participate in this contest.
                                    If there are multiple eligiblity requirement, split into multiple pieces.
                                    Example: SKKU students enrolled this semester`"
              >
                <span class="text-danger">*</span>
                Eligibility for participation
              </p>
            </template>
            <div
              v-for="(range, index) in contest.requirements"
              :key="index"
            >
              <b-row style="margin-bottom: 15px">
                <b-col cols="8">
                  <b-form-input
                    v-model="range.value"
                    placeholder="Contest Requirement"
                  />
                </b-col>
                <b-col cols="1">
                  <b-button @click="addRequirement" variant="outline-secondary">
                      <b-icon icon="plus"></b-icon>
                  </b-button>
                </b-col>
                <b-col cols="1">
                  <b-button @click="removeRequirement(range)" variant="outline-secondary">
                      <b-icon icon="trash-fill"></b-icon>
                  </b-button>
                </b-col>
              </b-row>
            </div>
          </b-form-group>
        </b-col>
        <b-col cols="6">
          <b-form-group>
            <template #label>
              <p
                class="labels"
                style="margin-top:16px"
                v-b-popover.hover="`Short descriptions of who are restricted to participate in this contest.
                                    If there are multiple constraints, split into multiple pieces.
                                    Example: Students who have awarded in same contest before.`"
              >
                Constraints
              </p>
            </template>
            <div
              v-for="(range, index) in contest.constraints"
              :key="index"
            >
              <b-row style="margin-bottom: 15px">
                <b-col cols="8">
                  <b-form-input
                    v-model="range.value"
                    placeholder="Contest Constraints"
                  />
                </b-col>
                <b-col cols="1">
                  <b-button @click="addConstraint" variant="outline-secondary">
                      <b-icon icon="plus"></b-icon>
                  </b-button>
                </b-col>
                <b-col cols="1">
                  <b-button @click="removeConstraint(range)" variant="outline-secondary">
                      <b-icon icon="trash-fill"></b-icon>
                  </b-button>
                </b-col>
              </b-row>
            </div>
          </b-form-group>
        </b-col>
        <b-col cols="12">
          <b-form-group
            label-for="ContestScoring"
          >
            <template #label>
              <p
                class="labels"
                v-b-popover.hover="`Short description of how to score problems and how to decide the rank of this contest.
                                    Example: ACM-ICPC style`"
              >
                <span class="text-danger">*</span>
                Scoring
              </p>
            </template>
            <b-form-input
              id="ContestScoring"
              v-model="contest.scoring"
              placeholder="Scoring"
            />
          </b-form-group>
        </b-col>
        <b-col cols="12">
          <b-form-group>
            <template #label>
              <p
                class="labels"
                style="margin-top:16px"
                v-b-popover.hover="`What is the prizes of this contest? Set representative color, name and reward of every prizes
                                    Example: #abcdef / Top 1 - 10 / Cute teddy bear`"
              >
                Prizes
              </p>
            </template>
            <div
              v-for="(range, index) in contest.prizes"
              :key="index"
            >
              <b-row style="margin-bottom: 15px">
                <b-col cols="2">
                  <b-form-input
                    v-model="range.color"
                    placeholder="Representative color"
                  />
                </b-col>
                <b-col cols="4">
                  <b-form-input
                    v-model="range.name"
                    placeholder="Name"
                  />
                </b-col>
                <b-col cols="4">
                  <b-form-input
                    v-model="range.reward"
                    placeholder="Reward"
                  />
                </b-col>
                <b-col cols="1">
                  <b-button @click="addPrize" variant="outline-secondary">
                    <b-icon icon="plus"></b-icon>
                  </b-button>
                </b-col>
                <b-col cols="1">
                  <b-button @click="removePrize(range)" variant="outline-secondary">
                      <b-icon icon="trash-fill"></b-icon>
                  </b-button>
                </b-col>
              </b-row>
            </div>
          </b-form-group>
        </b-col>
        <b-col cols="4">
          <b-form-group label-for="Contest_Start_Time">
            <template #label>
              <p class="labels" style="margin-top:16px">
                <span class="text-danger">*</span>
                Start Time
              </p>
            </template>
            <b-form-datepicker
              id="Contest_Start_Time"
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
        <b-col cols="4">
          <b-form-group label-for="Contest_End_Time">
            <template #label>
              <p class="labels" style="margin-top:16px">
                <span class="text-danger">*</span>
                End Time
              </p>
            </template>
            <b-form-datepicker
              id="Contest_End_Time"
              v-model="endDate"
              today-button
              close-button
              type="datetime"
              :date-format-options="{ year: 'numeric', month: '2-digit', day: '2-digit' }"
              locale="en"
              placeholder="End Time"
              style="margin-bottom:10px"
            />
            <b-form-timepicker
              v-model="endTime"
              show-seconds
              now-button
            >
            </b-form-timepicker>
          </b-form-group>
        </b-col>
        <b-col cols="4">
          <b-form-group label-for="Contest_Password">
            <template #label>
              <p
                class="labels"
                style="margin-top:16px"
                v-b-popover.hover="`You can set password for this contest and protect from unauthorized users.`"
              >
                Password
              </p>
            </template>
            <b-input
              v-model="contest.password"
              placeholder="Password"
            />
          </b-form-group>
        </b-col>
        <!-- <b-col :span="8">
              <b-form-group :label="$t('m.Contest_Rule_Type')">
              <b-button v-model="contest.rule_type" label="ACM" :disabled="disableRuleType">ACM</b-radio>
              <b-button v-model="contest.rule_type" label="OI" :disabled="disableRuleType">OI</b-radio>
              </b-form-item>
              </b-col> -->
        <b-col cols="4">
          <b-form-group>
            <template #label>
              <p class="labels">
                Real Time Rank
              </p>
            </template>
            <b-form-checkbox v-model="contest.real_time_rank" switch>
            </b-form-checkbox>
          </b-form-group>
        </b-col>
        <b-col cols="4">
          <b-form-group>
            <template #label>
              <p class="labels">
                Visible
              </p>
            </template>
            <b-form-checkbox v-model="contest.visible" switch>
            </b-form-checkbox>
          </b-form-group>
        </b-col>
        <b-col cols="4">
          <b-form-group>
            <template #label>
              <p
                class="labels"
                v-b-popover.hover="`Select the visibility of penalty on user's ranking page.
                                    If disabled, users won't see contest participants' penalty.`"
              >
                Show Rank Penalty
              </p>
            </template>
            <b-form-checkbox v-model="contest.rank_penalty_visible" switch>
            </b-form-checkbox>
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group>
            <template #label>
              <p
                class="labels"
                v-b-popover.hover="`Only members of certain group can participate in the contest.
                                    If not set, all group members can participate.`"
              >
                Allowed Groups
              </p>
            </template>
            <b-form-select v-model="contest.allowed_groups" :options="groupOptions" multiple :select-size="4" value-field="id" text-field="name">
            </b-form-select>
          </b-form-group>
        </b-col>
        <b-col>
          <b-form-group>
            <template #label>
              <p class="labels">
                Allowed IP Ranges
              </p>
            </template>
            <div
              v-for="(range, index) in contest.allowed_ip_ranges"
              :key="index"
            >
              <b-row style="margin-bottom: 15px">
                <b-col cols="4">
                  <b-form-input
                    v-model="range.value"
                    placeholder="CIDR Network"
                  />
                </b-col>
                <b-col cols="1">
                  <b-button @click="addIPRange" variant="outline-secondary">
                      <b-icon icon="plus"></b-icon>
                  </b-button>
                </b-col>
                <b-col cols="1">
                  <b-button @click="removeIPRange(range)" variant="outline-secondary">
                      <b-icon icon="trash-fill"></b-icon>
                  </b-button>
                </b-col>
              </b-row>
            </div>
          </b-form-group>
        </b-col>
        <b-col cols="12">
          <b-form-group>
            <template #label>
              <p class="labels">
                Problem Bank Contest Mode
              </p>
            </template>
            <b-form-checkbox v-model="useProblemBankFilter" switch>
            </b-form-checkbox>
          </b-form-group>
        </b-col>
        <b-col cols="12" v-show="useProblemBankFilter">
          <b-form-group>
            <template #label>
              <p
                class="labels"
                style="margin-top:16px"
                v-b-popover.hover="`Use Problem bank feature for this contest.
                                    Each users will get random problems according to this conditions.
                                    level/tag condition is supported now on.`"
              >
                Problem Bank Filter
              </p>
            </template>
            <div>
              <b-row
                v-for="(range, index) in contest.bank_filter"
                :key="range.id"
                style="margin-bottom: 15px"
              >
                <b-col cols="3">
                  <b-form-select
                    v-model="range.level"
                    :options="levelOptions"
                  />
                </b-col>
                <b-col cols="3">
                  <b-form-select
                    v-model="range.tag"
                    :options="problemTagList"
                  />
                </b-col>
                <b-col cols="3">
                  <div class="d-flex">
                    <span class="bank-filter__count mx-3">X</span>
                    <b-form-input
                      v-model="range.count"
                      placeholder="the number of this problems"
                      type="number"
                      :state="0 < range.count && range.count <= problemLevelCount[range.level]"
                    />
                    <span class="bank-filter__count mx-3"> / {{ problemLevelCount[range.level] || 0 }}</span>
                  </div>
                </b-col>
                <b-col cols="3">
                  <b-button @click="removeBankFilter(index)" variant="outline-secondary">
                    <b-icon icon="trash-fill"></b-icon>
                  </b-button>
                </b-col>
              </b-row>
              <b-button @click="addBankFilter" variant="outline-secondary">
                  <b-icon icon="plus"></b-icon>
              </b-button>
            </div>
          </b-form-group>
        </b-col>
        <b-col>
          Preview (Some styles may differ from actual appearance.)
          <neon-box color="#8DC63F" class="my-3"
                :leftTop="contest.title" :leftBottom="makeGroupRequirementInfo(contest)" rightBottom="Start in / Started from / Finished ago" rightTop="Pariticipants count"
                :shadow="true" @click.native="showContestInformationModal(contest)"
          >
            <template #overlay-icon>
              <b-icon-zoom-in color="#B4B4B4" width="1.5em" height="1.5em"></b-icon-zoom-in>
            </template>
          </neon-box>
          <b-modal id="modal-contest-information" size="xl">
            <contest-information
              :title="contest.title" :requirements="contest.requirements.map(r => r.value)"
              :constraints="contest.constraints.map(r => r.value)" :scoring="contest.scoring"
              :prizes="contest.prizes" :description="contest.description"
            >
            </contest-information>
            <template #modal-footer>
              <b-button>Go Contest</b-button>
            </template>
          </b-modal>
        </b-col>
      </b-row>
      <save @click.native="saveContest" />
    </Panel>
  </div>
</template>

<script>
import api from '../../api.js'
import Tiptap from '../../components/Tiptap.vue'
import NeonBox from '@oj/components/NeonBox.vue'
import ContestInformation from '@oj/components/ContestInformation.vue'

export default {
  name: 'CreateContest',
  components: {
    Tiptap,
    NeonBox,
    ContestInformation
  },
  data () {
    return {
      title: 'Create Contest',
      disableRuleType: false,
      contest: {
        title: '',
        description: '',
        requirements: [{
          value: ''
        }],
        constraints: [{
          value: ''
        }],
        scoring: '',
        prizes: [{
          color: '',
          name: '',
          reward: ''
        }],
        allowed_groups: [],
        start_time: '',
        end_time: '',
        rule_type: 'ACM',
        password: '',
        real_time_rank: true,
        visible: true,
        allowed_ip_ranges: [{
          value: ''
        }],
        bank_filter: [
          // {
          //   level: "unselected",
          //   tag: '',
          //   count: 0
          // }
        ],
        rank_penalty_visible: true
      },
      groupOptions: [],
      startTime: '',
      startDate: '',
      endTime: '',
      endDate: '',
      levelOptions: [
        { value: 'unselected', text: 'Select Please', disabled: true },
        'Level1',
        'Level2',
        'Level3',
        'Level4',
        'Level5',
        'Level6',
        'Level7'
      ],
      problemTagList: [
        { value: 'unselected', text: 'Select Please', disabled: true }
      ],
      problemLevelCount: {
        // "null": 0,
        // "Level1": 1,
        // "Level2": 3,
        // "Level5": 2,
      },
      useProblemBankFilter: false
    }
  },
  async mounted () {
    const res = await api.getGroupList()
    this.groupOptions = res.data.data
    if (this.$route.name === 'edit-contest') {
      this.title = 'Edit Contest'
      this.disableRuleType = true
      try {
        const res = await api.getContest(this.$route.params.contestId)
        const data = res.data.data

        const ranges = []
        for (const v of data.allowed_ip_ranges) {
          ranges.push({ value: v })
        }
        if (ranges.length === 0) {
          ranges.push({ value: '' })
        }
        data.allowed_ip_ranges = ranges

        const requirements = []
        for (const v of data.requirements) {
          requirements.push({ value: v })
        }
        if (requirements.length === 0) {
          requirements.push({ value: '' })
        }
        data.requirements = requirements

        const constraints = []
        for (const v of data.constraints) {
          constraints.push({ value: v })
        }
        if (constraints.length === 0) {
          constraints.push({ value: '' })
        }
        data.constraints = constraints

        const prizes = []
        for (const v of data.prizes) {
          prizes.push({
            color: v.color,
            name: v.name,
            reward: v.reward
          })
        }
        if (prizes.length === 0) {
          prizes.push({ value: '' })
        }
        data.prizes = prizes

        const allowedGroups = []
        for (const v of data.allowed_groups) {
          allowedGroups.push(v.id)
        }
        data.allowed_groups = allowedGroups
        this.contest = data
        this.initTime()
      } catch (err) {
      }
    }
    await this.getProblemTagList()
    await this.getProblemLevelCount()
  },
  methods: {
    async saveContest () {
      this.setStartTime()
      this.setEndTime()
      const funcName = this.$route.name === 'edit-contest' ? 'editContest' : 'createContest'
      const data = Object.assign({}, this.contest)
      const ranges = []
      for (const v of data.allowed_ip_ranges) {
        if (v.value !== '') {
          ranges.push(v.value)
        }
      }
      data.allowed_ip_ranges = ranges

      const requirements = []
      for (const v of data.requirements) {
        if (v.value !== '') {
          requirements.push(v.value)
        }
      }
      data.requirements = requirements
      const constraints = []
      for (const v of data.constraints) {
        if (v.value !== '') {
          constraints.push(v.value)
        }
      }
      data.constraints = constraints
      const prizes = []
      for (const v of data.prizes) {
        if (v.color !== '' && v.name !== '' && v.reward !== '') {
          prizes.push({
            color: v.color,
            name: v.name,
            reward: v.reward
          })
        }
      }
      data.prizes = prizes

      if (!this.useProblemBankFilter) {
        data.bank_filter = []
      }
      try {
        await api[funcName](data)
        await this.$router.push({ name: 'contest-list', query: { refresh: 'true' } })
      } catch (err) {
      }
    },
    initTime () {
      ;[this.startDate, this.startTime] = this.contest.start_time.split(/T|[+]/)
      ;[this.endDate, this.endTime] = this.contest.end_time.split(/T|[+]/)
    },
    setStartTime () {
      this.contest.start_time = this.startDate + ' ' + this.startTime
    },
    setEndTime () {
      this.contest.end_time = this.endDate + ' ' + this.endTime
    },
    addIPRange () {
      this.contest.allowed_ip_ranges.push({ value: '' })
    },
    removeIPRange (range) {
      const index = this.contest.allowed_ip_ranges.indexOf(range)
      if (index !== -1 && this.contest.allowed_ip_ranges.length !== 1) {
        this.contest.allowed_ip_ranges.splice(index, 1)
      }
    },
    addRequirement () {
      this.contest.requirements.push({ value: '' })
    },
    removeRequirement (range) {
      const index = this.contest.requirements.indexOf(range)
      if (index !== -1 && this.contest.requirements.length !== 1) {
        this.contest.requirements.splice(index, 1)
      }
    },
    addConstraint () {
      this.contest.constraints.push({ value: '' })
    },
    removeConstraint (range) {
      const index = this.contest.constraints.indexOf(range)
      if (index !== -1 && this.contest.constraints.length !== 1) {
        this.contest.constraints.splice(index, 1)
      }
    },
    addPrize () {
      this.contest.prizes.push({ value: '' })
    },
    removePrize (range) {
      const index = this.contest.prizes.indexOf(range)
      if (index !== -1 && this.contest.prizes.length !== 1) {
        this.contest.prizes.splice(index, 1)
      }
    },
    async getProblemTagList () {
      const response = await api.getProblemTagList()
      for (const tag of response.data.data) {
        this.problemTagList.push(tag.name)
      }
    },
    async getProblemLevelCount () {
      const data = await api.getProblemLevelCount().then((x) => x.data.data)
      data.unselected = 0
      this.problemLevelCount = data
    },
    addBankFilter () {
      this.contest.bank_filter.push({
        level: 'unselected',
        tag: 'unselected',
        count: 0
      })
    },
    removeBankFilter (index) {
      if (index !== -1) {
        this.contest.bank_filter.splice(index, 1)
      }
    },
    makeGroupRequirementInfo (contest) {
      return 'For ' + (contest.allowed_groups.map(g => g.name).join(', ') || 'All Groups')
    },
    showContestInformationModal (contest) {
      this.contestInformation = contest
      this.$bvModal.show('modal-contest-information')
    }
  }
}
</script>

<style scoped>
  .row, .col {
    word-wrap: break-word;
  }
  .bank-filter__count {
    font-size: 20px;
    margin-right:5px;
    padding: 0.275rem 0.1rem;
    white-space: nowrap;
  }
</style>
