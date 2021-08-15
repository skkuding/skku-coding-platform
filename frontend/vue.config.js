const path = require('path')

module.exports = {
  productionSourceMap: false,
  pages: {
    oj: {
      entry: './src/pages/oj/index.js',
      template: './src/pages/oj/index.html',
      filename: 'index.html',
      title: 'SKKU Coding Platform',
      chunks: ['chunk-vendors', 'chunk-common', 'oj']
    },
    admin: {
      entry: './src/pages/admin/index.js',
      template: './src/pages/admin/index.html',
      filename: 'admin/index.html',
      title: 'SKKU Coding Platform Admin',
      chunks: ['chunk-vendors', 'chunk-common', 'admin']
    }
  },
  configureWebpack: {
    resolve: {
      extensions: ['.js', '.vue', '.json'],
      alias: {
        '@': path.join(__dirname, 'src'),
        '@oj': path.join(__dirname, 'src/pages/oj'),
        '@admin': path.join(__dirname, 'src/pages/admin'),
        '@public': path.join(__dirname, 'public')
      }
    }
  },
  pluginOptions: {
    dll: {
      entry: [
        'vue',
        'vuex',
        'vue-router',
        'bootstrap-vue',
        'iview',
        'highlight.js',
        'moment',
        'katex',
        'core-js',
        '@tiptap/vue-2'
      ],
      cacheFilePath: path.resolve(__dirname, './public')
    }
  },
  pwa: {
    workboxPluginMode: 'InjectManifest',
    workboxOptions: {
      swSrc: './public/sw.js'
    }
  }
}
