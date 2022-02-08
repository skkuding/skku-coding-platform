const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,jsx}'],
  darkMode: false,
  theme: {
    extend: {
      fontFamily: {
        sans: [
          'Manrope',
          ...defaultTheme.fontFamily.sans
        ]
      }
    },
    colors: {
      white: '#ffffff',
      green: '#8DC63F',
      blue: '#3391E5',
      black: '#000000',
      transparent: '#0000',
      level: {
        level1: '#CC99C9',
        level2: '#9EC1CF',
        level3: '#A1F2C2',
        level4: '#B8FF81',
        level5: '#F3EC53',
        level6: '#FEB144',
        level7: '#FF6663'
      },
      text: {
        title: '#7C7A7B',
        content: '#495057'
      },
      table: {
        header: '#F9F9FA',
        hover: '#072B604D',
        border: '#e0e2e3'
      }
    }
  },
  plugins: []
}
