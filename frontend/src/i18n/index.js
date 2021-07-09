import Vue from 'vue'
// ivew UI
import ivenUS from 'iview/dist/locale/en-US'

const languages = [
  { value: 'en-US', label: 'English', iv: ivenUS }
]
const messages = {}

// combine admin and oj
for (const lang of languages) {
  const locale = lang.value
  const m = require(`./oj/${locale}`).m
  Object.assign(m, require(`./admin/${locale}`).m)
  const ui = Object.assign(lang.iv, lang.el)
  messages[locale] = Object.assign({ m: m }, ui)
}
