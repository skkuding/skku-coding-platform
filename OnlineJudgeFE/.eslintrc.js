module.exports = {
  root: true,
  parserOptions: {
    parser: '@babel/eslint-parser',
    sourceType: 'module',
    requireConfigFile: false
  },
  extends: [
    'standard',
    'plugin:vue/recommended'
  ],
  plugins: ['vue'],
  rules: {
    // allow paren-less arrow functions
    'arrow-parens': 'off',
    // allow async-await
    'generator-star-spacing': 'off',
    // allow debugger during development
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-irregular-whitespace': ['error', {
      skipComments: true,
      skipTemplates: true
    }],
    'vue/no-parsing-error': ['error', {
      'x-invalid-end-tag': false
    }]
  }
}
