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
      <!-- <button type="button" value="Connect" @click="compile()">compile</button> -->
      <button type="button" value="Connect" @click="run()">Run</button>
    </form>
    <div style = "margin-left: 30px; margin-right:30px" ref="terminal"/>
    <h1> stdin </h1>
    <form>
      <input type="text" v-model="stdin" readonly>
      <!-- <button type="button" value="input" @click="postStdin()">input</button> -->
    </form>
    <h1> stdout </h1>
    <p><textarea cols="40" rows="6" v-model="stdout" readonly></textarea></p>
  </div>
</template>

<script>
import io from 'socket.io-client'
import axios from 'axios'
import { Terminal } from 'xterm'

import 'xterm/lib/addons/fullscreen/fullscreen.css'
import 'xterm/dist/xterm.css'

export default {
  name: 'socket',
  data () {
    return {
      stdin: '',
      stdout: '',
      stderr: '',
      socket: '',
      code: 'for i in range(0, 4, 1):\n    inp = input()\n    print(inp, inp)',
      compileResult: '',
      dir: null,
      lang: '',
      lastStdin: '',
      userinput: false,
      writable: false
    }
  },
  mounted () {
    this.term = new Terminal({
      rendererType: 'canvas',
      rows: 25,
      cols: 100,
      convertEol: true,
      scrollback: 50,
      disableStdin: false,
      cursorBlink: true,
      cursorStyle: 'underline',
      theme: {
        foreground: '#7e9192',
        background: '#002833',
        cursor: 'help',
        lineHeight: 16
      }
    })
    this.term.prompt = () => {
      this.term.write('\r< ')
    }
    this.term.writeln(
      `
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▒▒      ░▒▓▓▓▓
▓▓▓▓▒ ▒░░   ░▒▓░ ░ ▓
▓▓▒  ▒░░░ ░▒ ░▓▓▓▓▓▓
▓▒ ▒░░   ░░▓ ▒▓▓▓▓▓▓
▓░ ░░░  ░░░▒   ▓▓▓▓▓
▓  ░   ░░░▒  ▒ ▒▓▓▓▓
▓▓ ▒ ░▒░▒▓▓▓▓▓ ░ ▒▓▓
▓▓░ ▒ ▓▓▓▓▓▓ ▓▓▓ ░▓▓
▓▓▓▒ ▒▓▓▓ ▓▓▓▓▓  ▓▓▓
▓▓▓▓▓▓▓░░▒▓▓▓▓▒ ▒▓▓▓
▓▓▓▓▓▓▓▓▓▒▒▒▒▒▓▓▓▓▓▓
      `
    )
    this.term.writeln('Welcome to \x1B[1;32mSKKU Coding platform!\x1B[0m')
    this.term.writeln('Please Run your code!!')
    this.term.open(this.$refs.terminal)
    this.term.onKey(e => {
      console.log(e)
      if (!this.writable) {
        return
      }
      const printable = !e.domEvent.altKey && !e.domEvent.altGraphKey && !e.domEvent.ctrlKey && !e.domEvent.metaKey
      if (e.domEvent.keyCode === 13) {
        this.term.write('\n')
        this.userinput = true
        this.socket.emit('stdin', this.stdin)
        this.writable = false
      } else if (e.domEvent.keyCode === 8) {
        if (this.term._core.buffer.x > 2) {
          this.term.write('\b \b')
          this.stdin = this.stdin.length === 1 ? '' : this.stdin.substring(0, this.stdin.length - 1)
        }
      } else if (e.key.length === 1 && printable) {
        console.log(e.domEvent.keyCode + 'Printable')
        console.log(e.domEvent.key)
        this.term.write(e.key)
        this.stdin += e.key
      } else {
        console.log(e.domEvent.keyCode + 'Not acceptable character')
      }
    })
    this.term.attachCustomKeyEventHandler(async (e) => {
      if (e.ctrlKey && e.code === 'KeyV' && e.type === 'keydown') {
        const selection = this.term.getSelection
        if (selection) {
          const clipboardData = await navigator.clipboard.readText()
          const splitedData = clipboardData.split(/\r?\n/)

          this.lastLine = splitedData[splitedData.length - 1]
          const exceptLastLine = splitedData.slice(0, -1).join('\n')
          console.log('11', this.lastLine, exceptLastLine)

          if (exceptLastLine) {
            this.term.writeln(exceptLastLine)
            this.stdin = exceptLastLine
            this.userinput = true
            this.socket.emit('stdin', this.stdin)
            this.writable = false
          }

          return false
        }
        return true
      }
      return true
    })
  },
  beforeDestroy () {
    if (this.term) {
      this.term.dispose()
    }
  },
  methods: {
    async run () {
      const ack = await this.compile()

      if (this.dir === null) {
        console.log('Not compiled yet')
        return
      }
      if (ack === -1) {
        return
      }
      this.term.clear()
      this.term.writeln('\x1B[1;3;31mCode running...\x1B[0m')
      this.term.prompt()
      this.stdin = ''
      this.stdout = ''
      this.stderr = ''
      // TODO: Add additional URI
      this.socket = io('https://localhost', {
        reconnection: false,
        query: {
          token: this.dir,
          lang: this.lang
        }
      })

      this.writable = true

      this.socket.on('stdout', (output) => {
        if (this.userinput) {
          console.log('22', this.lastLine)
          if (this.lastLine) {
            console.log('Lastline')
            this.stdin.replaceAll(/(?<=[^\r])\n/g, '\r\n')
          }
          this.stdout = output.replace(this.stdin + '\r\n', '')
          this.stdin = ''
          this.term.write(this.stdout)
          this.userinput = false
          this.writable = true
        } else {
          this.stdout += output
          this.term.write(this.stdout)
        }
        if (this.lastLine) {
          this.term.write(this.lastLine)
          this.stdin = this.lastLine
        }
      })

      this.socket.on('exited', () => {
        this.term.writeln('\x1B[1;3;31mProgram exited\x1B[0m')
        this.writable = false
      })
    },
    postStdin () {
      this.socket.emit('stdin', this.stdin)
      this.userinput = true
    },
    async compile () {
      try {
        const res = await axios.post('https://localhost/code-run/compile', { lang: this.lang, code: this.code })
        console.log(res.data)
        this.stderr = ''
        if (res.data.status !== 1) {
          this.stderr = res.data.output
          this.term.writeln('\x1B[1;31m' + res.data.output + '\x1B[0m')
          return -1
        } else {
          this.dir = res.data.output
          return 0
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
