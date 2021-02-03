'use strict'
import ora from 'ora'
import rm from 'rimraf'
import { join } from 'path'
import webpack from 'webpack'
import { build } from '../config'
import { red, cyan, yellow } from 'chalk'
import webpackConfig from './webpack.prod.conf'

require('./check-versions')()

process.env.NODE_ENV = 'production'

const spinner = ora('building for production...')
spinner.start()

rm(join(build.assetsRoot, build.assetsSubDirectory), err => {
  if (err) throw err
  webpack(webpackConfig, function (err, stats) {
    spinner.stop()
    if (err) throw err
    process.stdout.write(stats.toString({
      colors: true,
      modules: false,
      children: false,
      chunks: false,
      chunkModules: false
    }) + '\n\n')

    if (stats.hasErrors()) {
      console.log(red('  Build failed with errors.\n'))
      process.exit(1)
    }

    console.log(cyan('  Congratulations, the project built complete without error\n'))
    console.log(yellow(
      ' You can now check the onlinejudge in http://YouIP/'
    ))
  })
})
