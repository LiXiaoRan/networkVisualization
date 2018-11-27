<template>
  <div id='nodetree-panel'>
    <app-title v-bind:icon='icon' v-bind:msgs='msgs'></app-title>
    <div id='Panel' class='view'>
    </div>
    <div page-max=50 current-page=1 nodes-length=300 class='page'>
    </div>
  </div>
</template>
<script>
import $ from 'jquery'
const d3 = require('d3')
import AppTitle from './AppTitle.vue'
export default {
  data() {
    return {
      // icon: '<i class = "fa fa-usb" aria-hidden = "true"></i>',
      icon: 'usb',
      msgs: '节点树',
      currentPage: 1,
      pageMax: 50,
      nodesLength: 300
    }
  },
  components: { AppTitle },
  methods: {
    HistogramInit(divname, options) {
      options.divWidth = options.divWidthh ? options.divWidth : parseInt($('#' + divname).css('width').split('px')[0])
      options.divHeight = options.divHeight ? options.divHeight : parseInt($('#' + divname).css('height').split('px')[0])
      this.margin = {
        top: options.divHeight * 0.03,
        right: options.divWidth * 0.07,
        bottom: options.divHeight * 0.08,
        left: options.divWidth * 0.07
      }

      this.width = options.divWidth - this.margin.left - this.margin.right
      this.height = options.divHeight - this.margin.top - this.margin.bottom
      this.barPadding = 1
      this.xPadding = this.width * 0.05
      this.yPadding = this.height * 0.05
      this.svg = d3.select('#' + divname).append('svg')
        .attr('width', this.width + this.margin.left + this.margin.right)
        .attr('height', this.height + this.margin.top + this.margin.bottom)
        .attr('class', 'mainNode')
      let that = this
      this.xScale = d3.scaleLinear()
        .range([0, this.width / options.dictLength])
        .domain(d3.range(options.dictLength))
      this.yleftDownScale = d3.scaleLinear()
        .range([this.height * 0.1, this.height / 2])
        .domain([d3.max(options.data, function(d) {
          return d3.max(d)
        }), 0])
      this.yleftUpScale = d3.scaleLinear()
        .range([this.height / 2.5, 0])
        .domain([d3.max(options.data, function(d) {
          return d3.max(d)
        }), 0])

      this.svgaxisLeftDown = this.svg.append('g').attr('class', 'axis')
        .attr('transform', 'translate(' + this.margin.left + ',' + (this.margin.top + this.height / 2) + ')')
        .attr('id', 'svgaxisLeftDown')
        .call(d3.axisLeft(this.yleftDownScale).ticks(3, 's'))
        .style('fill', '#95a5a6')
      this.svgaxisLeftUp = this.svg.append('g').attr('class', 'axis')
        .attr('transform', 'translate(' + (this.margin.left) + ',' + (this.margin.top * 2) + ')')
        .attr('id', 'svgaxisRightUp')
        .call(d3.axisLeft(this.yleftUpScale).ticks(3, 's'))
        .attr('fill', '#95a5a6')

      this.svg.selectAll('.axis text')
        .attr('fill', '#95a5a6')
        .attr('font-size', 11)
      this.svg.selectAll('.axis line')
        .attr('stroke', '#95a5a6')

      this.svg.append('g')
      let rect = this.svg.append('g')
        .attr('id', 'rect')
        .attr('transform', 'translate(' + 0 + ',' + this.margin.top + ')')
      that = this
      rect.selectAll('Xrect')
        .data(options.data)
        .enter()
        .append('rect')
        .attr('x', function(d, i) {
          return that.margin.left + i * (that.width / options.data.length)
        })
        .attr('y', function(d, i) {
          let max = d3.max(options.data, function(d) {
            return d[0]
          })
          if (max === 0) {
            return 0
          }
          return (that.height - (d[0] * that.height / (2.2 * max)))
        })
        .attr('width', function(d, i) {
          if (that.width / options.data.length >= that.barPadding * 5) {
            return that.width / options.data.length - that.barPadding
          } else {
            return that.width / options.data.length
          }
        })
        .attr('height', function(d, i) {
          let max = d3.max(options.data, function(d) {
            return d[0]
          })
          if (max === 0) {
            return 0
          }
          return d[0] * that.height / (2.2 * max)
        })
        .attr('opacity', 0.5)
        .style('fill', '#3F5765')

      rect.selectAll('Xrect')
        .data(options.data)
        .enter()
        .append('rect')
        .attr('x', function(d, i) {
          return that.margin.left + i * (that.width / options.data.length)
        })
        .attr('y', function(d, i) {
          return that.margin.top
        })
        .attr('width', function(d, i) {
          if (that.width / options.data.length >= that.barPadding * 5) {
            return that.width / options.data.length - that.barPadding
          } else {
            return that.width / options.data.length
          }
        })
        .attr('height', function(d, i) {
          let max = d3.max(options.data, function(d) {
            return d[1]
          })
          if (max === 0) {
            return 0
          }
          return d[1] * that.height / (2.2 * max)
        })
        .attr('opacity', 0.5)
        .style('fill', '#FF530D')
    },
    Histogram() {
      let that = this
      this.svg.append('g')
        .attr('id', 'firstLine')

      that.svg.selectAll('.domain').remove()
    },
    MainNodeInf(Data) {
      // d3.select('.mainNode').remove()
      this.HistogramInit('Panel', { divHeight: 150, dictLength: 30, data: Data })
    },
    HeatLineInit(divname, options) {
      options.divWidth = options.divWidth ? options.divWidth : parseInt($('#' + divname).css('width').split('px')[0])
      options.divHeight = options.divHeight ? options.divHeight : parseInt($('#' + divname).css('height').split('px')[0])

      this.margin = {
        top: options.divHeight * 0.03,
        right: options.divWidth * 0.07,
        bottom: options.divHeight * 0.08,
        left: options.divWidth * 0.07
      }
      this.width = options.divWidth - this.margin.left - this.margin.right
      this.height = options.divHeight - this.margin.top - this.margin.bottom
      this.barPadding = 1
      this.xPadding = this.width * 0.05
      this.yPadding = this.height * 0.05

      this.svg = d3.select('#' + divname).append('svg')
        .attr('width', this.width + this.margin.left + this.margin.right)
        .attr('height', this.height * 2 + this.margin.top + this.margin.bottom)
        .attr('id', options.num)
        .attr('class', 'relatedNodes')

      let that = this
      if (options.dictLength === 1) {
        options.data.push([0, 0])
        options.dictLength = options.data.length
      }
      this.xScale = d3.scaleLinear()
        .range([0, this.width / options.dictLength])
        .domain(d3.range(options.dictLength))

      this.yleftDownScale = d3.scaleLinear()
        .range([this.height * 0.1, this.height / 2])
        .domain([d3.max(options.data, function(d) {
          return d[0]
        }), 0])

      this.yleftUpScale = d3.scaleLinear()
        .range([this.height / 2.5, 0])
        .domain([d3.max(options.data, function(d) {
          return d[1]
        }), 0])
      this.yrightScale = d3.scaleLinear()
        .range([that.margin.top, this.height])
        .domain([d3.max(options.data, function(d) {
          return d3.max(d)
        }) * 1.3, 0])

      this.svgaxisRight = this.svg.append('g').attr('class', 'axis')
        .attr('transform', 'translate(' + (this.margin.left + this.width) + ',' + (this.margin.top) + ')')
        .attr('id', 'svgaxisRightUp')
        .call(d3.axisRight(this.yrightScale).ticks(2, 's'))

      d3.selectAll('.axis text')
        .attr('fill', '#95a5a6')
        .attr('font-size', 8)
      d3.selectAll('.axis line')
        .attr('stroke', '#95a5a6')

      let firstvalueLine = d3.area()
        .x(function(d, i) {
          return that.xScale(i)
        })
        .y0(that.yrightScale(0))
        .y1(function(d, i) {
          return that.yrightScale(d[0])
        })

      let secondvalueLine = d3.area()
        .x(function(d, i) {
          return that.xScale(i)
        })
        .y0(that.yrightScale(0))
        .y1(function(d, i) {
          return that.yrightScale(0) - that.yrightScale(d[1]) + that.yrightScale(0)
        })

      let Line = this.svg.append('g')
        .attr('id', 'firstLine')

      Line.selectAll('Xline')
        .data([options.data])
        .enter()
        .append('path')
        .attr('fill', '#45BF55')
        .attr('stroke', 'none')
        .attr('stroke-width', 2)
        .attr('opacity', 0.5)
        .attr('d', firstvalueLine)
        .attr('transform', 'translate(' + (this.margin.left) + ',' + 0 + ')')

      Line.selectAll('Xline')
        .data([options.data])
        .enter()
        .append('path')
        .attr('fill', 'steelblue')
        .attr('stroke', 'none')
        .attr('stroke-width', 3)
        .attr('opacity', 0.5)
        .attr('d', secondvalueLine)
        .attr('transform', 'translate(' + (this.margin.left) + ',' + 0 + ')')

      this.svg.append('circle')
        .attr('cx', that.xScale(0) - 10)
        .attr('cy', that.yrightScale(0))
        .attr('r', 3)
        .attr('fill', 'grey')
        .attr('transform', 'translate(' + (this.margin.left) + ',' + 0 + ')')

      this.svg.append('line')
        .attr('x1', that.xScale(0) - 10)
        .attr('y1', that.yrightScale(0))
        .attr('x2', that.width)
        .attr('y2', that.yrightScale(0))
        .attr('stroke', 'grey')
        .attr('transform', 'translate(' + (this.margin.left) + ',' + 0 + ')')

      this.svg.append('text')
        .attr('x', that.xScale(0) + 10)
        .attr('y', that.height * 2)
        .attr('font-size', 12)
        .attr('fill', '#95a5a6')
        .style('text-anchor', 'start')
        .text(options.id)
      d3.selectAll('.domain').remove()
      // d3.selectAll('.axis text').remove()
    },
    HeatLineInf(Id, nodeData) {
      for (let j = 0; j < nodeData.length; j++) {
        this.HeatLineInit('Panel', { divHeight: 30, dictLength: nodeData[j].length, data: nodeData[j], id: Id[j], num: (j + 1) })
      }
      this.Paginate(nodeData.length)
      d3.select('.previous').on('click', this.prev)
      d3.select('.next').on('click', this.next)
    },
    Paginate(length) {
      let nodesLength = length
      let pageMax = Math.floor(nodesLength / 6) + 1
      d3.select('.page').attr('nodes-length', nodesLength)
      d3.select('.page').attr('page-max', pageMax)
      // let c1 = 'pager'
      // let c2 = 'previous disabled'
      let h1 = 'this.prev()'
      // let c3 = 'next'
      let h2 = 'this.next()'

      let str = "<div class = 'pager' align='right' style='margin: 10px 40px'><button class = 'previous' v-on:click = '" + h1 + "' style='margin: 10px;color: whitesmoke;background-color: #9864CC; border-radius:10px; border:0;'>← Prev</button><button class = 'next'  v-on:click = '" + h2 + "'  style='margin: 10px;color: whitesmoke;background-color: #9864CC; border-radius:10px; border:0;'>Next →</button></div>"
      if (length > 7) {
        document.getElementById('Panel').innerHTML += str
        for (let i = 7; i <= length; i++) {
          document.getElementById('' + i).style.display = 'none'
        }
      }
    },
    next() {
      let pageMax = d3.select('.page').attr('page-max')
      let currentPage = d3.select('.page').attr('current-page')
      let nodesLength = d3.select('.page').attr('nodes-length')
      currentPage++
      d3.select('.page').attr('current-page', currentPage)
      if (currentPage > pageMax) {
        currentPage = pageMax
        d3.select('.page').attr('current-page', currentPage)
        return
      }
      d3.select('.previous').classed('disabled', false)
      for (let i = 1; i <= nodesLength; i++) {
        if ((currentPage - 1) * 6 < i && i <= currentPage * 6) {
          document.getElementById('' + i).style.display = 'block'
        } else {
          document.getElementById('' + i).style.display = 'none'
        }
      }
      if (currentPage === pageMax) {
        d3.select('.next').classed('disabled', true)
      }
    },

    prev() {
      let currentPage = d3.select('.page').attr('current-page')
      let nodesLength = d3.select('.page').attr('nodes-length')
      currentPage--
      d3.select('.page').attr('current-page', currentPage)
      if (currentPage < 1) {
        currentPage = 1
        d3.select('.page').attr('current-page', currentPage)
        return
      }
      d3.select('.next').classed('disabled', false)
      for (let i = 1; i <= nodesLength; i++) {
        if ((currentPage - 1) * 6 < i && i <= currentPage * 6) {
          document.getElementById('' + i).style.display = 'block'
        } else {
          document.getElementById('' + i).style.display = 'none'
        }
      }
      if (currentPage === 1) {
        d3.select('.previous').classed('disabled', true)
      }
    }
  },
  mounted() {
    let Data = []
    for (let i = 0; i < 30; i++) {
      let temp = [Math.floor(Math.random() * 50), Math.floor(Math.random() * 50)]
      Data.push(temp)
    }
    this.MainNodeInf(Data)

    let Id = ['10.59.212.181', '220.181.157.93', '101.226.161.183', '106.38.199.36', '140.207.197.241', '106.38.199.36', '10.59.212.142', '10.66.120.187', '10.66.204.123', '10.59.212.181', '106.38.199.36', '10.59.212.142', '10.66.120.187', '10.66.204.123', '10.59.212.181']
    let nodeData = []

    for (let j = 0; j < 8; j++) {
      let node = []
      for (let i = 0; i < 100; i++) {
        let temp = [Math.floor(Math.random() * 10), Math.floor(Math.random() * 10)]
        node.push(temp)
      }
      nodeData.push(node)
    }
    this.HeatLineInf(Id, nodeData)
  }
}

</script>
<style lang='less' scoped>
@import './AppNodeTree.less';

</style>
