import 'chartjs-chart-box-and-violin-plot'
import { generateChart, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

const BoxPlot = generateChart('boxplot', 'boxplot')

export default {
  extends: BoxPlot,
  mixins: [reactiveProp],
  props: ['options'],
  mounted () {
    // this.chartData is created in the mixin.
    // If you want to pass options please create a local options object
    this.renderChart(this.chartData, this.options)
  }
}
