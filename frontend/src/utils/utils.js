import Vue from 'vue'
import storage from '@/utils/storage'
import { STORAGE_KEY } from '@/utils/constants'
import ojAPI from '@oj/api'

function submissionMemoryFormat (memory) {
  if (memory === undefined) return '--'
  // 1048576 = 1024 * 1024
  const t = parseInt(memory) / 1048576
  return String(t.toFixed(0)) + 'MB'
}

function submissionTimeFormat (time) {
  if (time === undefined) return '--'
  return time + 'ms'
}

function getACRate (acCount, totalCount) {
  const rate = totalCount === 0 ? 0.00 : (acCount / totalCount * 100).toFixed(2)
  return String(rate) + '%'
}

// 去掉值为空的项，返回object
function filterEmptyValue (object) {
  const query = {}
  Object.keys(object).forEach(key => {
    if (object[key] || object[key] === 0 || object[key] === false) {
      query[key] = object[key]
    }
  })
  return query
}

// 按指定字符数截断添加换行，非英文字符按指定字符的半数截断
function breakLongWords (value, length = 16) {
  let re
  if (escape(value).indexOf('%u') === -1) {
    // 没有中文
    re = new RegExp('(.{' + length + '})', 'g')
  } else {
    // 中文字符
    re = new RegExp('(.{' + (length / 2 + 1) + '})', 'g')
  }
  return value.replace(re, '$1\n')
}

async function downloadFile (url) {
  const res = await Vue.prototype.$http.get(url, { responseType: 'blob' })
  const headers = res.headers
  if (headers['content-type'].indexOf('json') !== -1) {
    const fr = new window.FileReader()
    Vue.prototype.$error(res.data.error | 'Invalid file format')
    fr.onload = (event) => {
      const data = JSON.parse(event.target.result)
      Vue.prototype.$error(data.error ? data.data : 'Invalid file format')
    }
    const b = new window.Blob([res.data], { type: 'application/json' })
    fr.readAsText(b)
    return
  }
  const link = document.createElement('a')
  link.href = window.URL.createObjectURL(new window.Blob([res.data], { type: headers['content-type'] }))
  link.download = (headers['content-disposition'] || '').split('filename=')[1]
  document.body.appendChild(link)
  link.click()
  link.remove()
}

async function getLanguages () {
  const storageLanguages = storage.get(STORAGE_KEY.languages)
  if (storageLanguages) {
    return storageLanguages
  }
  const res = await ojAPI.getLanguages()
  const languages = res.data.data.languages
  storage.set(STORAGE_KEY.languages, languages)
  return languages
}

export default {
  submissionMemoryFormat: submissionMemoryFormat,
  submissionTimeFormat: submissionTimeFormat,
  getACRate: getACRate,
  filterEmptyValue: filterEmptyValue,
  breakLongWords: breakLongWords,
  downloadFile: downloadFile,
  getLanguages: getLanguages
}
