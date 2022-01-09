<template>
  <div style="text-align: center;">
    <div ref="terminal"/>
  </div>
</template>

<script>
import io from 'socket.io-client'
import axios from 'axios'
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'

import 'xterm/lib/addons/fullscreen/fullscreen.css'
import 'xterm/dist/xterm.css'

export default {
  name: 'RunInCLI',
  props: {
    code: String,
    language: String,
    runInCliKey: Number
  },
  data () {
    return {
      stdin: '',
      stdout: '',
      stderr: '',
      socket: '',
      dir: null,
      userinput: false,
      writable: false
    }
  },
  mounted () {
    this.term = new Terminal({
      rendererType: 'canvas',
      rows: 25,
      cols: 80,
      convertEol: true,
      scrollback: 50,
      disableStdin: false,
      cursorBlink: true,
      cursorStyle: 'underline',
      theme: {
        foreground: '#7e9192',
        background: '#24272D',
        cursor: '#FFFFFF',
        lineHeight: 16
      }
    })

    const fitAddon = new FitAddon()
    this.term.loadAddon(fitAddon)
    fitAddon.fit()

    this.term.writeln(
      `
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▒▒      ░▒▓▓▓▓
▓▓▓▓▒ ▒░░   ░▒▓░ ░ ▓
▓▓▒  ▒░░░ ░▒ ░▓▓▓▓▓▓
▓▒ ▒░░   ░░▓ ▒▓▓▓▓▓▓
▓░ ░░░  ░░░▒   ▓▓▓▓▓             Welcome to \x1B[1;32mSKKU Coding platform!\x1B[0m
▓  ░   ░░░▒  ▒ ▒▓▓▓▓
▓▓ ▒ ░▒░▒▓▓▓▓▓ ░ ▒▓▓
▓▓░ ▒ ▓▓▓▓▓▓ ▓▓▓ ░▓▓
▓▓▓▒ ▒▓▓▓ ▓▓▓▓▓  ▓▓▓
▓▓▓▓▓▓▓░░▒▓▓▓▓▒ ▒▓▓▓
▓▓▓▓▓▓▓▓▓▒▒▒▒▒▓▓▓▓▓▓
      `
    )
    this.term.writeln('')
    this.term.open(this.$refs.terminal)
    this.term.onKey(e => {
      if (!this.writable) {
        return
      }
      const printable = !e.domEvent.altKey && !e.domEvent.altGraphKey && !e.domEvent.ctrlKey && !e.domEvent.metaKey
      if (e.domEvent.keyCode === 13) { // Enter Key
        this.term.write('\n')
        this.userinput = true
        this.socket.emit('stdin', this.stdin)
        this.writable = false
      } else if (e.domEvent.keyCode === 8) { // Backspace Key
        this.term.write('\b \b')
        this.stdin = this.stdin.length === 1 ? '' : this.stdin.substring(0, this.stdin.length - 1)
      } else if (e.key.length === 1 && printable) { // printable character
        this.term.write(e.key)
        this.stdin += e.key
      } else {
        console.log(e.domEvent.keyCode + 'Not acceptable character')
      }
    })
    this.term.attachCustomKeyEventHandler(async (e) => {
      if (!this.writable) {
        return
      }
      if (e.ctrlKey && e.code === 'KeyV' && e.type === 'keydown') {
        const selection = this.term.getSelection
        if (selection) {
          const clipboardData = await navigator.clipboard.readText()
          const splitedData = clipboardData.split(/\r?\n/)
          const joinedData = splitedData.join('\n')

          if (joinedData) {
            this.term.write(joinedData)
            this.stdin = joinedData
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
      this.stdin = ''
      this.stdout = ''
      this.stderr = ''
      // TODO: Add additional URI
      this.socket = io('https://localhost', {
        reconnection: false,
        query: {
          token: this.dir,
          lang: this.shortLanguage
        }
      })

      this.writable = true

      this.socket.on('stdout', (output) => {
        if (this.userinput) {
          const replaceStdin = this.stdin.replaceAll(/\r?\n/g, '\r\n')
          this.stdout = output.replace(replaceStdin + '\r\n', '')
          this.stdin = ''
          this.term.write(this.stdout)
          this.userinput = false
          this.writable = true
        } else {
          this.stdout += output
          this.term.write(this.stdout)
        }
      })

      this.socket.on('exited', () => {
        this.term.writeln('\x1B[1;3;31mProgram exited\x1B[0m')
        this.writable = false
        this.$emit('completeRun')
      })
    },
    async compile () {
      this.term.clear()
      this.term.writeln(
        `
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ▓▓▓▓▓▓▒▒      ░▒▓▓▓▓
  ▓▓▓▓▒ ▒░░   ░▒▓░ ░ ▓
  ▓▓▒  ▒░░░ ░▒ ░▓▓▓▓▓▓
  ▓▒ ▒░░   ░░▓ ▒▓▓▓▓▓▓
  ▓░ ░░░  ░░░▒   ▓▓▓▓▓                       Compiling... 
  ▓  ░   ░░░▒  ▒ ▒▓▓▓▓
  ▓▓ ▒ ░▒░▒▓▓▓▓▓ ░ ▒▓▓
  ▓▓░ ▒ ▓▓▓▓▓▓ ▓▓▓ ░▓▓
  ▓▓▓▒ ▒▓▓▓ ▓▓▓▓▓  ▓▓▓
  ▓▓▓▓▓▓▓░░▒▓▓▓▓▒ ▒▓▓▓
  ▓▓▓▓▓▓▓▓▓▒▒▒▒▒▓▓▓▓▓▓
        `
      )
      try {
        const res = await axios.post('https://localhost/code-run/compile', { lang: this.shortLanguage, code: this.code })
        this.stderr = ''
        if (res.data.status !== 1) {
          this.stderr = res.data.output
          this.term.clear()
          this.term.writeln('\x1B[1;31m ### Compile Error ### \x1B[0m')
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
  },
  computed: {
    shortLanguage () {
      const language = {
        C: 'c',
        'C++': 'cpp',
        Java: 'java',
        Python2: 'py2',
        Python3: 'py3',
        Golang: 'go'
      }
      return language[this.language]
    }
  },
  watch: {
    'runInCliKey' () {
      this.run()
    }
  }
}
</script>

<style scoped>
  button {
    margin: 0px 5px;
  }
</style>
