<template>
  <div style="text-align: center;">
    <h1>Code</h1>
    <select v-model="lang">
      <option disabled value="">languages</option>
      <option>c</option>
      <option>cpp</option>
      <option>py2</option>
      <option>py3</option>
    </select>
    <form>
      <p><textarea cols="60" rows="8" v-model="code"></textarea></p>
      <button type="button" value="Connect" @click="compile()">compile</button>
      <button type="button" value="Connect" @click="run()">Run</button>
    </form>
    <h1> stdin </h1>
    <form>
      <input type="text" v-model="stdin">
      <button type="button" value="input" @click="postStdin()">input</button>
    </form>
    <h1> stdout </h1>
    <p><textarea cols="40" rows="6" v-model="stdout"></textarea></p>
    <h1> stderr </h1>
    <p>{{ stderr }}</p>
  </div>
</template>

<script>
import io from 'socket.io-client'
import axios from 'axios'
export default {
  name: 'socket',
  data () {
    return {
      stdin: '',
      stdout: '',
      stderr: '',
      socket: '',
      code: '',
      compileResult: '',
      dir: null,
      lang: '',
      lastStdin: '',
      userinput: false
    }
  },
  methods: {
    run () {
      if (this.dir === null) {
        console.log('Not compiled yet')
        return
      }
      this.stdout = ''
      this.stderr = ''
      this.socket = io('http://localhost:40000', {
        reconnection: false,
        query: {
          token: this.dir,
          lang: this.lang
        }
      })
      this.socket.on('stdout', (output) => {
        if (this.userinput) {
          this.stdout += output.replace(this.stdin, '')
          this.userinput = false
        } else {
          this.stdout += output
        }
      })
      this.socket.on('exited', () => {
        console.log('program exited')
      })
    },
    postStdin () {
      this.socket.emit('stdin', this.stdin)
      this.userinput = true
    },
    async compile () {
      try {
        const res = await axios.post('http://localhost:40000/compile', { lang: this.lang, code: this.code })
        console.log(res.data)
        this.stderr = ''
        if (res.data.status !== 1) {
          this.stderr = res.data.output
        } else {
          this.dir = res.data.output
        }
      } catch (err) {
        console.log(err)
      }
    }
  }
}
</script>

<style scoped>
  button {
    margin: 0px 5px;
  }
</style>
