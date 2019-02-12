<template>
  <div id='filter-panel'>
    <app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
    <div class="filter1">
      <span class="filtermsg">节点类型</span>
      <div class="fcheckbox">
        <div class="select1">
          <input type="checkbox" value="主机" v-model="nodeType" id="node1" /><label for="node1"></label><span>{{ span1 }}</span>
        </div>
        <div class="select2">
          <input type="checkbox" value="交换机" v-model="nodeType" id="node2" /><label for="node2"></label><span>{{ span2 }}</span>
        </div>
        <div class="select3">
          <input type="checkbox" value="服务器" v-model="nodeType" id="node3" /><label for="node3"></label><span>{{ span3 }}</span>
        </div>
      </div>
    </div>
    <div class="filter2">
          <span class="filtermsg">致瘫级别</span>
          <span class="button-dropdown button-dropdown-plain" data-buttons="dropdown" >
						<button class="button button-caution button-pill pasly_button" id="global_time_span_btn">
						  5级
              <!-- <i class="fa fa-caret-down"></i> -->
              <font-awesome-icon icon="caret-down" />
						</button>
						<ul class="button-dropdown-list is-below">
              <li id="global_tl_fourth"><a @click="switchPaslyLevel(5)">5级</a></li>
						  <li id="global_tl_fourth"><a @click="switchPaslyLevel(4)">4级</a></li>
						  <li id="global_tl_three"><a @click="switchPaslyLevel(3)">3级</a></li>
						  <li id="global_tl_two"><a @click="switchPaslyLevel(2)">2级</a></li>
						  <li id="global_tl_one"><a @click="switchPaslyLevel(1)">1级</a></li>
						</ul>
					</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <span class="filtermsg">控制级别</span>
          <span class="button-dropdown button-dropdown-plain" data-buttons="dropdown">
						<button class="button button-caution button-pill control_button" id="global_time_span_btn">
						  5级
              <!-- <i class="fa fa-caret-down"></i> -->
              <font-awesome-icon icon="caret-down" />
						</button>
						<ul class="button-dropdown-list is-below" >
						  <li id="global_tl_fourthc"><a @click="switchControlLevel(5)">5级</a></li>
						  <li id="global_tl_fourthc"><a @click="switchControlLevel(4)">4级</a></li>
						  <li id="global_tl_threec"><a @click="switchControlLevel(4)">3级</a></li>
						  <li id="global_tl_twoc"><a @click="switchControlLevel(4)">2级</a></li>
						  <li id="global_tl_onec"><a @click="switchControlLevel(4)">1级</a></li>
						</ul>
					</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  
    </div>
    <div class="filtergraph">
      <span class="filtermsg-0">节点数量</span>
      <span class="filtermsg-1">类型</span>
      <select class="filtermsg-2" v-model="selected">
        <option v-for="item in items" v-bind:value="item.value" :key="item.value" >{{item.text}}</option>
      </select>
      <div id='svgdiv'>
        <svg id="barchart"></svg>
      </div>
    </div>
  </div>
</template>
<script type="text/javascript">
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'
import AppTitle from './AppTitle.vue'
import '../../static/bootstrap.min.css'
import '../../static/buttons.css'
import 'font-awesome/css/font-awesome.css'
const d3 = require('d3')
export default {
  data() {
    return {
      icon: 'filter',
      msgs: '二级过滤器',
      span1: '主机',
      span2: '交换机',
      span3: '服务器',
      span4: '致瘫',
      span5: '控制',
      span6: '正常',
      nodeType: ['主机','交换机','服务器'],
      nodeAttr: ['致瘫','控制','正常'],
      items: [{ text: '总流量', value: '总流量' }, { text: '流入量', value: '流入量' }, { text: '流出量', value: '流出量' }],
      selected: '总流量'
    }
  },
  components: { AppTitle },
  methods: {
    ...mapActions(['modifyNodeTypeList_sync','modifyNodeAttrList_sync']),
    drawHistogram(randomData, randomDataLength) {
      let self = this
      let domItem = d3.select(self.$el)
      let brushleft = 0
      let brushright = 0
      let width = +domItem.select('.filtergraph').style('width').split('px')[0] * 0.90
      let height = +domItem.select('.filtergraph').style('height').split('px')[0] * 0.5
      let margin = +width * 0.05

      let xScale = d3.scaleBand().rangeRound([0, width], 0.1)
        .domain(randomData.map(function(d) { return d[0] }))
        .rangeRound([0, width], 0.1)

      let y = d3.scaleLinear()
        .domain([d3.max(randomData, function(d) {
          return d[1]
        }), 0])
        .range([0, height])

      let x = d3.scaleLinear()
        .domain([0, randomDataLength])
        .range([0, width])

      let brush = d3.brushX()
        .extent([
          [0, 0],
          [width, height]
        ])
        .on('end', function() {
          let range = d3.brushSelection(this).map(x.invert)
          brushleft = Math.round(range[0])
          brushright = Math.round(range[1])
          console.log(randomData.slice(brushleft, brushright))
        })
      let svg = d3.select('#barchart')
        .attr('width', width + margin * 2)
        .attr('height', height + margin + margin)
        .append('g')
        .attr('id', 'yaxis')
        .attr('transform', 'translate(' + margin + ',' + margin + ')')
        .call(d3.axisLeft()
          .scale(y)
          .ticks(3))

      d3.select('#yaxis').select('path').remove()
      d3.select('#yaxis').selectAll('.tick').select('line').remove()
      d3.select('#yaxis').selectAll('.tick').selectAll('text').attr('transform', 'translate(' + margin * 0.8 + ',0)').attr('fill', '#95a5a6')
      let translateMarginX = margin + 10
      d3.select('#barchart').append('g').selectAll('rect')
        .data(randomData).enter().append('rect')
        .attr('width', xScale.bandwidth())
        .attr('height', function(d, i) {
          return d[1] * height / (d3.max(randomData, function(d) {
            return d[1]
          }))
        })
        .attr('x', function(d) {
          return x(d[0])
        })
        .attr('y', function(d, i) {
          return (height - (d[1] * height / (d3.max(randomData, function(d) {
            return d[1]
          }))))
        })
        .attr('transform', 'translate(' + translateMarginX + ',' + margin + ')')
        .style('fill', 'rgb(31,165,218)')
        .style('stroke', 'rgb(48,50,67)')

      svg.append('g')
        .attr('class', 'brush')
        .call(brush)
    }
  },
  mounted() {
    let self = this
    let randomData = []
    let randomDataLength = 50
    for (let i = 0; i < randomDataLength; i++) {
      let rand = Math.floor(Math.random() * 500)
      randomData.push([i, rand])
    }
    self.drawHistogram(randomData, randomDataLength)
  },
  methods:{
    switchPaslyLevel(level){
      // alert(level)
      $(".pasly_button").html(level+"级 "+'<i class="fa fa-caret-down"></i>')
      switch (level) {
        //在这里写切换瘫痪等级的逻辑
        case 1:
          
          break;
        case 2:
          
          break;
        case 3:
          
          break;
        case 4:
          
          break;
        case 5:
          
          break;      
        default:
          break;
      }
    },
    switchControlLevel(level){
      // alert(level)
      $(".control_button").html(level+"级 "+'<i class="fa fa-caret-down"></i>')
      switch (level) {
        //在这里写切换控制等级的逻辑
        case 1:
          
          break;
        case 2:
          
          break;
        case 3:
          
          break;
        case 4:
          
          break;
        case 5:
          
          break;      
        default:
          break;
      }
    }
  },
  watch: {
    nodeType: function(data) {
      console.log( $.type(data) +"  "+data)
      this.modifyNodeTypeList_sync({nodeTypeList :data});

    },
    nodeAttr: function(data) {
      console.log(data)
      this.modifyNodeAttrList_sync({nodeAttrList : data})
    },
    selected: function(data) {
      console.log(data)
    }
  }
}

</script>
<style lang="less" scoped>
@import "AppTimeLine.less";
@import "./AppFilter.less";

</style>
