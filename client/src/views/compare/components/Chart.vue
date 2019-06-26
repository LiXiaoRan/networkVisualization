<template>
  <div id="comparechart">
    <div style="border-bottom: 1px #ccc dashed;
    position: relative;
    padding-bottom: 10px;
    padding-top: 10px;
    margin-right: 30px">
      <span style="font-size: large;">属性对比图 &nbsp&nbsp {{this.selectId}}（左） &nbsp&nbsp {{this.compareId}}（右）</span>
    </div>
    <div id='button'>
      <select @change="modeKinds">
        <option>选择属性</option>
        <option v-for="attr in attributes">
          {{attr}}
        </option>
      </select>
      <select>
        <option>选择图表</option>
        <option v-for="mode in modes">
          {{mode}}
        </option>
      </select>
      <button @click="startDraw">go</button>
    </div>
    <!-- <div id="id">
      <table v-if="show_attribute == '选择属性'">
        <tr>
          <th style="width:50%">{{this.selectId}}</th>
          <th style="width:50%">{{this.compareId}}</th>
        </tr>
      </table>
    </div> -->
    <div id='show' style="position:absolute; top:100px; height:80%; width:90%"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import echarts from 'echarts';
export default {
  name: 'Chart',
  props: {
    compareId: String
  },
  data () {
    return {
      selectId: '',
      modes: [],
      timenodes_attr: {},
      node1: [],
      attributes: [],
      show_attribute: '选择属性',
      show_graph: '选择图表',
      time_range: JSON.parse(localStorage.getItem('timerange')),
      width: '100%',
      height: '100%',
      padding: {
        top : 50,
        right : 20,
        bottom : 20,
        left : 20
      },
      rectStep: 30,
      rectWidth: 1,
    };
  },
  computed: {
    node2 () {
      return this.timenodes_attr[this.compareId];
    }
  },
  watch: {
  },
  mounted () {
    this.selectId = localStorage.getItem('selectid');
    let timerange = JSON.parse(localStorage.getItem('timerange'));
    //timerange['end'] = this.timeCovert(timerange['start']);
    this.timerange = timerange;
    this.getData();
  },
  methods: {
    getData () {
      let paramsObj = {
        timerange: this.timerange,
        id: this.selectId,
      };
      let Url = "get-chart-data";
      CommunicateWithServer("get", paramsObj, Url, this.showTop);
    },
    showTop (result) {
      this.timenodes_attr = result;
      let attr_arr = [];
      let temp_attrs = this.timenodes_attr[this.selectId][0]['attributes'];
      for(let key in temp_attrs) {
        attr_arr.push(key);
      }
      this.attributes = attr_arr;
      this.node1 = this.timenodes_attr[this.selectId];
      //console.log(this.timenodes_attr);
      //console.log(this.node1);
    },
    timeCovert (str) {
      let time1 = +new Date(str);
      let min =  1 * 60 * 1000;
      time1 = new Date(+time1 + min);
      let dataobj = time1.toLocaleString();
      let dataobj2 = time1.toTimeString();
      let riqi = dataobj.slice(0, 10);
      let shijian = dataobj2.slice(0, 8);
      let time = riqi + " " + shijian;
      return time;
    },
    modeKinds (e) {
      let index = e.target.selectedIndex; // 获取索引
      let selected = e.target[index].value; // 获取选框中的属性名
      let kind = selected.split('_')[0];
      if(kind == 'num') {
        this.modes = ['折线图', '面积图', '柱状图', '堆叠图'];
      }
      else if(kind == 'cluster') {
        this.modes = ['小圆圈', '饼图', '雷达图'];
      }
    },
    
    startDraw () {
      let index=document.getElementsByTagName("select")[0].selectedIndex;
      this.show_attribute=document.getElementsByTagName("select")[0].options[index].value;
      let index2=document.getElementsByTagName("select")[1].selectedIndex;
      this.show_graph=document.getElementsByTagName("select")[1].options[index2].value;
      if(this.show_attribute != '选择属性' && this.show_graph != '选择图表'){
				let e = d3.select('#showchart');
				e.remove();
        this.draw(this.show_attribute, this.show_graph);
      }
    },
    
    draw (show_attribute, graph) {
      if(graph == '折线图'){
        this.draw_number_line(show_attribute, graph);
      }
      else if(graph == '面积图'){
        this.draw_number_arealine(show_attribute, graph);
      }
      else if(graph == '柱状图'){
        this.draw_number_bar(show_attribute, graph);
      }
      else if(graph == '堆叠图'){
        this.draw_number_stack(show_attribute, graph);
      }
      else if(graph == '小圆圈'){
        this.draw_string_circle(show_attribute);
      }
      else if(graph == '饼图'){
        this.draw_string_pie(show_attribute, graph);
      }
      else if(graph == '雷达图'){
        this.draw_string_radar(show_attribute, graph);
      }
    },
    
    draw_number_arealine (show_attribute, graph) {
      //定义一块SVG的绘制区域
      let div = d3.select('#show')
        .append('div')
        .attr('style', 'height: ' + this.height + '; width: ' + this.width)
        .attr('id', 'showchart');
      
      let dom = document.getElementById('showchart');
      var myChart = echarts.init(dom);
      var app = {};
      var option = null;
      
      var data = [];
      for(let i = 0; i < this.node1.length; i++) {
        let value = this.node1[i]['attributes'][show_attribute];
        let value_time = this.node1[i]['time'];
				if(value == null) {
					value = 0;
				}
        data.push([value_time, value]);
      }
      
      var data2 = [];
      for(let i = 0; i < this.node2.length; i++) {
        let value = this.node2[i]['attributes'][show_attribute];
        let value_time = this.node2[i]['time'];
				if(value == null) {
					value = 0;
				}
        data2.push([value_time, value]);
      }
			console.log(data);
      
      option = {
          tooltip: {
              trigger: 'axis',
              position: function (pt) {
                  return [pt[0], '10%'];
              }
          },
          title: {
              left: 'center',
              text: '面积图',
          },
          toolbox: {
              feature: {
                  dataZoom: {
                      yAxisIndex: 'none'
                  },
                  restore: {},
                  myTool1: {
                    show: true,
                    title: '关闭',
                    icon: 'path://M17.36,34.736l17.368-17.472M34.78,34.684L17.309,17.316',
                    onclick: () => {
                      div.remove();
                      let index = this.showed_info.indexOf([show_attribute, graph]);
                      console.log(index);
                      if(index > -1) {
                        this.showed_info.splice(index, 1);
                      }
                      console.log(this.showed_info);
                    }
                  }
                  //saveAsImage: {}
              }
          },
          grid: [
              {x: '7%', y: '10%', width: '38%'},
              {x2: '7%', y: '10%', width: '38%'}
          ],
          xAxis: [{
              type: 'time',
              splitLine: {
                show: false
              },
              gridIndex: 0,
              inverse: true
          },{
              type: 'time',
              splitLine: {
                show: false
              },
              gridIndex: 1
          }],
          yAxis: [{
              type: 'value',
              gridIndex: 0,
              boundaryGap: [0, '100%'],
              position: 'right'
          },{
              type: 'value',
              gridIndex: 1,
              boundaryGap: [0, '100%']
          }],
          dataZoom: [{
              type: 'inside',
              xAxisIndex: [0, 1],
              start: 0,
              end: 100
          }, {
            type: 'slider',
            xAxisIndex: [0, 1],
              start: 0,
              end: 100,
              handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
              handleSize: '80%',
              handleStyle: {
                  color: '#fff',
                  shadowBlur: 3,
                  shadowColor: 'rgba(0, 0, 0, 0.6)',
                  shadowOffsetX: 2,
                  shadowOffsetY: 2
              },
              left: 'center'
          }],
          series: [
              {
                  name:this.selectId,
                  type:'line',
                  xAxisIndex: 0,
									yAxisIndex: 0,
                  smooth:true,
                  symbol: 'none',
                  sampling: 'average',
                  itemStyle: {
                      color: 'rgb(255, 70, 131)'
                  },
                  areaStyle: {
                      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                          offset: 0,
                          color: 'rgb(255, 158, 68)'
                      }, {
                          offset: 1,
                          color: 'rgb(255, 70, 131)'
                      }])
                  },
                  data: data
              },
              {
                  name:this.compareId,
                  type:'line',
                  xAxisIndex: 1,
									yAxisIndex: 1,
                  smooth:true,
                  symbol: 'none',
                  sampling: 'average',
                  itemStyle: {
                      color: 'rgb(255, 70, 131)'
                  },
                  areaStyle: {
                      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                          offset: 0,
                          color: 'rgb(255, 158, 68)'
                      }, {
                          offset: 1,
                          color: 'rgb(255, 70, 131)'
                      }])
                  },
                  data: data2
              }
          ]
      };
      ;
      if (option && typeof option === "object") {
          myChart.setOption(option, true);
      }
    },
    
    draw_number_line (show_attribute, graph) {
      //定义一块SVG的绘制区域
      let div = d3.select('#show')
        .append('div')
        .attr('style', 'height: ' + this.height + '; width: ' + this.width)
        .attr('id', 'showchart');
      
      let dom = document.getElementById('showchart');
      var myChart = echarts.init(dom);
      var app = {};
      var option = null;
			
      var data = [];
      for(let i = 0; i < this.node1.length; i++) {
        let value = this.node1[i]['attributes'][show_attribute];
        let value_time = this.node1[i]['time'];
				if(value == null) {
					value = 0;
				}
        data.push([value_time, value]);
      }
      
      var data2 = [];
      for(let i = 0; i < this.node2.length; i++) {
        let value = this.node2[i]['attributes'][show_attribute];
        let value_time = this.node2[i]['time'];
				if(value == null) {
					value = 0;
				}
        data2.push([value_time, value]);
      }
      
      option = {
          tooltip: {
              trigger: 'axis',
              position: function (pt) {
                  return [pt[0], '10%'];
              }
          },
          title: {
              left: 'center',
              text: '折线图',
          },
          toolbox: {
              feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                restore: {},
                myTool1: {
                  show: true,
                  title: '关闭',
                  icon: 'path://M17.36,34.736l17.368-17.472M34.78,34.684L17.309,17.316',
                  onclick: () => {
                    div.remove();
                }
              },
						}
          },
          xAxis: {
              type: 'time',
              splitLine: {
                show: false
              }
          },
          yAxis: {
              type: 'value',
              boundaryGap: [0, 0.1]
          },
          dataZoom: [{
              type: 'inside',
              start: 0,
              end: 100
          }, {
            type: 'slider',
              start: 0,
              end: 100,
              handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
              handleSize: '80%',
              handleStyle: {
                  color: '#fff',
                  shadowBlur: 3,
                  shadowColor: 'rgba(0, 0, 0, 0.6)',
                  shadowOffsetX: 2,
                  shadowOffsetY: 2
              }
          }],
          series: [
              {
                  name:this.selectId,
                  type:'line',
                  smooth:true,
                  symbol: 'none',
                  sampling: 'average',
                  itemStyle: {
                      color: 'rgb(255, 70, 131)'
                  },
                  data: data
              },
              {
                  name:this.compareId,
                  type:'line',
                  smooth:true,
                  symbol: 'none',
                  sampling: 'average',
                  itemStyle: {
                      color: '#5793f3'
                  },
                  data: data2
              }
          ]
      };
      if (option && typeof option === "object") {
          myChart.setOption(option, true);
      }
    },
    
    draw_number_bar (show_attribute, graph) {
      //定义一块SVG的绘制区域
      let div = d3.select('#show')
        .append('div')
        .attr('style', 'height: ' + this.height + '; width: ' + this.width)
        .attr('id', 'showchart');
      
      let dom = document.getElementById('showchart');
      var myChart = echarts.init(dom);
      var app = {};
      var option = null;
			
			let time_data = [];
			for(let i = 0; i < this.node1.length; i++) {
				let value_time = this.node1[i]['time'];
				value_time = value_time.slice(14);
				time_data.push(value_time);
			}
			
			let data1 = [];
			for(let i = 0; i < this.node1.length; i++) {
				let value = this.node1[i]['attributes'][show_attribute];
				data1.push(value);
			}
			
			let data2 = [];
			for(let i = 0; i < this.node2.length; i++) {
				let value = this.node2[i]['attributes'][show_attribute];
				data2.push(value);
			}
			
      option = {
          title: {
              text: 'Population Pyramid'
          },
          tooltip: {
              trigger: 'axis',
              axisPointer: {
                  type: 'shadow'
              }
          },
          toolbox: {
            feature: {
              myTool1: {
                show: true,
                title: '关闭',
                icon: 'path://M17.36,34.736l17.368-17.472M34.78,34.684L17.309,17.316',
                onclick: () => {
                  div.remove();
								},
							}
            }
          },
          grid: [{
          left: '3%',
            right: '52.5%'
          },{
            left: '52%',
            right: '3%'
            //containLabel: true
          }],
          xAxis: [{
            type: 'value',
            gridIndex: 0,
            inverse: true,
            boundaryGap: [0, 0.01]
          },{
              type: 'value',
              gridIndex: 1,
              boundaryGap: [0, 0.01]
          }],
          yAxis: [{
            type: 'category',
            gridIndex: 0,
            axisTick: {
                show: false
              },
              axisLabel: {
                show: false
              },
            position: 'right',
            data: time_data
          },{
              type: 'category',
              gridIndex: 1,
              axisTick: {
                show: false
              },
              axisLabel: {
                
              },
              data: time_data
          }],
          series: [
              {
                  name: this.selectId,
                  type: 'bar',
                  xAxisIndex: 0,
                  yAxisIndex: 0,
                  data: data1
              },
              {
                  name: this.compareId,
                  type: 'bar',
                  xAxisIndex: 1,
                  yAxisIndex: 1,
                  data: data2
              }
          ],
      };
      if (option && typeof option === "object") {
          myChart.setOption(option, true);
      }
    },
    
    draw_number_stack (show_attribute, graph) {
      //定义一块SVG的绘制区域
      let div = d3.select('#show')
        .append('div')
        .attr('style', 'height: ' + this.height + '; width: ' + this.width)
        .attr('id', 'showchart');
      
      let dom = document.getElementById('showchart');
      var myChart = echarts.init(dom);
      var app = {};
      var option = null;
			
      var data = [];
      for(let i = 0; i < this.node1.length; i++) {
        let value = this.node1[i]['attributes'][show_attribute];
        let value_time = this.node1[i]['time'];
      	if(value == null) {
      		value = 0;
      	}
        data.push([value_time, value]);
      }
      
      var data2 = [];
      for(let i = 0; i < this.node2.length; i++) {
        let value = this.node2[i]['attributes'][show_attribute];
        let value_time = this.node2[i]['time'];
      	if(value == null) {
      		value = 0;
      	}
        data2.push([value_time, value]);
      }
			
      option = {
          title: {
              text: '堆叠区域图'
          },
          tooltip : {
              trigger: 'axis',
              axisPointer: {
                  type: 'cross',
                  label: {
                      backgroundColor: '#6a7985'
                  }
              }
          },
          toolbox: {
            feature: {
              myTool1: {
                show: true,
                title: '关闭',
                icon: 'path://M17.36,34.736l17.368-17.472M34.78,34.684L17.309,17.316',
                onclick: () => {
                  div.remove();
								},
							}
            }
          },
          grid: {
              left: '3%',
              right: '4%',
              bottom: '9%',
              containLabel: true
          },
          xAxis : [
              {
                  type : 'time',
                  boundaryGap : false
              }
          ],
          yAxis : [
              {
                  type : 'value'
              }
          ],
          dataZoom: [{
              type: 'inside',
              start: 0,
              end: 100
          }, {
            type: 'slider',
              start: 0,
              end: 100,
              handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
              handleSize: '80%',
              handleStyle: {
                  color: '#fff',
                  shadowBlur: 3,
                  shadowColor: 'rgba(0, 0, 0, 0.6)',
                  shadowOffsetX: 2,
                  shadowOffsetY: 2
              }
          }],
          series : [
              {
                  name:this.selectId,
                  type:'line',
                  symbol: 'none',
                  smooth:true,
                  stack: '总量',
                  areaStyle: {},
                  data:data
              },
              {
                  name:this.compareId,
                  type:'line',
                  symbol: 'none',
                  smooth:true,
                  stack: '总量',
                  label: {
                      normal: {
                          show: true,
                          position: 'top'
                      }
                  },
                  areaStyle: {normal: {}},
                  data:data2
              }
          ]
      };
      if (option && typeof option === "object") {
          myChart.setOption(option, true);
      }
    },
    
    /* draw_string_circle (show_attribute, graph) {
    	 //定义一块SVG的绘制区域
    	let div = d3.select('#show')
    		.append('div')
        .attr('style', 'height: ' + this.height + '; width: ' + this.width)
    		.attr('id', 'showchart');
    	
      let width = document.getElementById('show').offsetWidth;
      let height = document.getElementById('show').offsetHeight;
      console.log(width, height);
      
      this.yAxisWidth = height - this.padding.top - this.padding.bottom;
      this.xAxisWidth = width - this.padding.right - this.padding.left;
      
    	let svg = div.append('svg')  // body中添加SVG
    				.attr('width', width)  // SVG的宽度
    				.attr('height', height);  // SVG的高度
    	
      
      let parsetime = d3.timeParse("%Y-%m-%d %H:%M:%S");
      
      console.log(this.timerange);
      
    	//X轴时间比例尺
    					
    	let xScale = d3.scaleTime()
    		.domain([parsetime(this.time_range['start']), parsetime(this.time_range['end'])])
    		.range([width / 2 - this.padding.left, 0]);
    	
    	let xScale2 = d3.scaleTime()
    		.domain([parsetime(this.time_range['start']), parsetime(this.time_range['end'])])
    		.range([width / 2 - this.padding.left, this.xAxisWidth]);
    	
    	
    	//定义X坐标轴
    	let xAxis = d3.axisBottom(xScale);  // 设置刻度朝向
    	
    	let xAxis2 = d3.axisBottom(xScale2);
    	
    	//添加元素
    	let gxAxis = svg.append("g")
    					.attr('transform', 'translate(' + this.padding.left + ',' + (height - this.padding.bottom) + ')')
    					.call(xAxis);
    	
    	let gxAxis2 = svg.append("g")
    					.attr('transform', 'translate(' + this.padding.left + ',' + (height - this.padding.bottom) + ')')
    					.call(xAxis2);
    	
    	//画一条直线
    	let line_data = [[0, 0], [0, this.yAxisWidth]];
    		
    	let gyAxis = svg.append("g")
    					.attr('transform', 'translate(' + width / 2 + ',' + this.padding.top + ')');
    					
    	let lineGenerator = d3.line()
    					.x(d => d[0])
    					.y(d => d[1]);
    	
    	gyAxis.append('path')
    		.attr('stroke', 'black')
    		.attr('stroke-width', '2')
    		.attr('fill', 'black')
    		.attr('d', lineGenerator(line_data));
    	
    	
    	//在SVG中添加分组元素，里面存放圆元素
    	let gCircle = svg.append("g")
    					.attr('transform', 'translate(' + this.padding.left + ',' + this.padding.top + ')');
    	
    	let gCircle2 = svg.append("g")
    					.attr('transform', 'translate(' + this.padding.left + ',' + this.padding.top + ')');
    	
    	
    	//创建序数比例尺，让数据与一种颜色相对应
    	let color = d3.schemeCategory10;
    	//console.log(color);
    	let all_datas = [];
    	for(let i = 0; i < this.node1.length; i++) {
    		all_datas.push(this.node1[i].attributes[show_attribute]);
    	}
    	for(let i = 0; i < this.node2.length; i++) {
    		all_datas.push(this.node2[i].attributes[show_attribute]);
    	}
    	let cScale = d3.scaleOrdinal()
    					.domain(all_datas)
    					.range(color);
    	
    	
    	//添加圆
    	
    	gCircle.selectAll("circle")
    		.data(this.node1)
    		.enter()  // 获取enter部分
    		.append('circle')  // 添加rect元素，使其与绑定数组的长度相同
    		.attr('fill', d => cScale(d.attributes[show_attribute]))  // 设置圆的颜色
    		.attr('cx', d => xScale(parsetime(d.time)))  // 设置x坐标
    		.attr('cy', d => (height - this.padding.bottom - this.padding.top) / 2)  // 设置y坐标
    		.attr('r', d => {
    			if(d.attributes[show_attribute] == null){
    				return 0;
    			}
    			else{
    				return (this.rectStep / 4);
            
    			}
    		});  // 设置半径
    	
    	
    	
    	gCircle2.selectAll("circle")
    		.data(this.node2)
    		.enter()  // 获取enter部分
    		.append('circle')  // 添加rect元素，使其与绑定数组的长度相同
    		.attr('fill', d => cScale(d.attributes[show_attribute]))  // 设置圆的颜色
    		.attr('cx', d => xScale2(parsetime(d.time)))  // 设置x坐标
    		.attr('cy', d => (height - this.padding.bottom - this.padding.top) / 2)  // 设置y坐标
    		.attr('r', d => {
    			if(d.attributes[show_attribute] == null){
    				return 0;
    			}
    			else{
    				return this.rectStep / 4;
    			}
    		});  // 设置半径
    	
    	
    	
    	//在SVG中添加分组元素，里面存放标签元素
    	let gText = svg.append("g")
    					.attr('transform', 'translate(' + padding.left + ',' + padding.top + ')');
    					
    	let gText2 = svg.append("g")
    					.attr('transform', 'translate(' + padding.left + ',' + padding.top + ')');
    	
    	
    	//添加标签文字
    	gText.selectAll("text")
    		.data(node1.attributes[show_attribute])
    		.enter()
    		.append('text')
    		.attr('fill', 'black')
    		.attr('font-size', '20px')
    		.attr('text-anchor', 'middle')
    		.attr('x', (d, i) => rectStep / 2 + xScale(times[i]))  // 与圆的x坐标一样
    		.attr('y', d => (height - padding.bottom - padding.top) / 2)  // 与圆的y坐标一样
    		.attr('dy', '0.5em')  // em单位表示的是当前文字所占一行的高度
    		.text(d => d);  // 显示的文字内容
    	
    	if(node2.id != null){
    		gText2.selectAll("text")
    			.data(node2.attributes[show_attribute])
    			.enter()
    			.append('text')
    			.attr('fill', 'black')
    			.attr('font-size', '20px')
    			.attr('text-anchor', 'middle')
    			.attr('x', (d, i) => rectStep / 2 + xScale2(times[i]))  // 与矩形的x坐标一样
    			.attr('y', d => (height - padding.bottom - padding.top) / 2)  // 与圆的y坐标一样
    			.attr('dy', '0.5em')  // em单位表示的是当前文字所占一行的高度
    			.text(d => d);  // 显示的文字内容
    	}
    	
    	 //该元素放入属性信息
    	let gAttrText = svg.append('g')
    					.attr('transform', 'translate(' + 0 + ',' + this.padding.top / 2 + ')');
    					
    	//添加属性信息
    	gAttrText.selectAll('text')
    		.data([show_attribute])
    		.enter()
    		.append('text')
    		.attr('fill', 'black')
    		.attr('font-size', '30px')
    		.attr('text-anchor', 'middle')
    		.attr('x', d => width / 2)
    		.attr('y', d => 0)
    		.text(d => d); 
    		
    	let close_button = div.append('span')
    		.attr('class', 'close big')
    		.attr('left', width)
    		.on('click', () => {
    			div.remove();
    		}); 
    }, */
    
    draw_string_circle (show_attribute, graph) {
      let div = d3.select('#show')
        .append('div')
        .attr('style', 'height: ' + this.height + '; width: ' + this.width)
        .attr('id', 'showchart');
      
      let dom = document.getElementById('showchart');
      var myChart = echarts.init(dom);
      var app = {};
      var option = null;
      
      let attributes = [];
      for(let i = 0; i < this.node1.length; i++) {
      	let temp_attr = this.node1[i]['attributes'][show_attribute];
      	if(attributes.indexOf(temp_attr) == -1) {
      		attributes.push(temp_attr);
      	}
      }
      for(let i = 0; i < this.node2.length; i++) {
      	let temp_attr = this.node2[i]['attributes'][show_attribute];
      	if(attributes.indexOf(temp_attr) == -1) {
      		attributes.push(temp_attr);
      	}
      }
      
      let index = attributes.indexOf(null);
      if(index > -1) {
        attributes.splice(index, 1);
      }
      
      let times = [];
      for(let i = 0; i < this.node1.length; i++) {
      	times.push(this.node1[i]['time'].slice(14));
      }
      
      let times_re = times.concat();
      times_re.reverse();
      
      let datas = [];
      for(let k = 0; k < attributes.length; k++) {
      	for(let i = 0; i < times.length; i++) {
      		let temp_data = this.node1[i]['attributes'][show_attribute];
      		if(temp_data == attributes[k]) {
      			datas.push([k, i, 1]);
      		}
      		else {
      			datas.push([k, i, 0]);
      		}
      	}
      }
      for(let k = 0; k < attributes.length; k++) {
      	for(let i = 0; i < times.length; i++) {
      		let temp_data = this.node2[i]['attributes'][show_attribute];
      		if(temp_data == attributes[k]) {
      			datas.push([k + attributes.length, times.length - 1 - i, 1]);
      		}
      		else {
      			datas.push([k + attributes.length, times.length - 1 - i, 0]);
      		}
      	}
      }
      
      let colors = ['#c23531','#2f4554', '#61a0a8', '#d48265', '#91c7ae','#749f83',  '#ca8622', '#bda29a','#6e7074', '#546570', '#c4ccd3'];
      
      option = {
          tooltip: {
              position: 'top'
          },
          title: [],
          singleAxis: [],
          series: []
      };
      
      echarts.util.each(attributes, function (attribute, idx) {
          option.title.push({
              left: '49%',
              right: '51%',
              textAlign: 'center',
              textBaseline: 'middle',
              top: (idx + 0.5) * 95 / attributes.length + '%',
              text: attribute
          });
          option.singleAxis.push({
              left: '55%',
              type: 'category',
              boundaryGap: false,
              data: times,
              top: (idx * 95 / attributes.length + 5) + '%',
              height: (95 / attributes.length - 7) + '%',
              //right: '50%',
              axisLabel: {
                  interval: 10
              }
          });
          option.series.push({
              singleAxisIndex: idx,
              coordinateSystem: 'singleAxis',
              type: 'scatter',
              data: [],
              symbolSize: function (dataItem) {
                  return dataItem[1] * 9;
              },
              itemStyle: {
                color: colors[idx]
              }
          });
      });
      echarts.util.each(attributes, function (attribute, idx) {
          option.singleAxis.push({
              right: '55%',
              type: 'category',
              boundaryGap: false,
              data: times_re,
              top: (idx * 95 / attributes.length + 5) + '%',
              height: (95 / attributes.length - 7) + '%',
              //right: '50%',
              axisLabel: {
                  interval: 10
              }
          });
          option.series.push({
              singleAxisIndex: idx + attributes.length,
              coordinateSystem: 'singleAxis',
              type: 'scatter',
              data: [],
              symbolSize: function (dataItem) {
                  return dataItem[1] * 9;
              },
              itemStyle: {
                color: colors[idx]
              }
          });
      });
      
      echarts.util.each(datas, function (dataItem) {
          option.series[dataItem[0]].data.push([dataItem[1], dataItem[2]]);
      });
      
      if (option && typeof option === "object") {
          myChart.setOption(option, true);
      }
    },
	
    draw_string_pie (show_attribute, graph) {
      console.log(this.node2);
      //定义一块SVG的绘制区域
      let div = d3.select('#show')
        .append('div')
        .attr('style', 'height: ' + this.height + '; width: ' + this.width)
        .attr('id', 'showchart');
      
      let dom = document.getElementById('showchart');
      var myChart = echarts.init(dom);
      var app = {};
      var option = null;
			
			let data1 = [];
			for(let i = 0; i < this.node1.length; i++) {
			  let value = this.node1[i]['attributes'][show_attribute];
				if(value != null) {
					data1.push(value);
				}
			}
			let data1_obj = {};
			for(let i = 0; i < data1.length; i++) {
				let name = data1[i];
				data1_obj[name] = (data1_obj[name] + 1) || 1;
			}
			let data = [['node', this.selectId, this.compareId]];
			for(let k in data1_obj) {
				data.push([k, data1_obj[k], 0]);
			}
			for(let i = 0; i < this.node2.length; i++) {
			  let value = this.node2[i]['attributes'][show_attribute];
				for(let j = 0; j < data.length; j++) {
					if(value == data[j][0]) {
						data[j][2]++;
					}
				}
			}
			
			
      var option = {
        //legend: {},
        //tooltip: {},
        title: {
          text: '各属性值出现次数统计'
        },
        toolbox: {
          feature: {
            myTool1: {
              show: true,
              title: '关闭',
              icon: 'path://M17.36,34.736l17.368-17.472M34.78,34.684L17.309,17.316',
              onclick: () => {
                div.remove();
              }
            }
          }
        },
        dataset: {
          source: data
        },
        series: [{
          type: 'pie',
          radius: 60,
          center: ['25%', '50%']
          // No encode specified, by default, it is '2012'.
        }, {
          type: 'pie',
          radius: 60,
          center: ['75%', '50%'],
          encode: {
            itemName: 'node',
            value: this.compareId
          }
        }]
    };
      if (option && typeof option === "object") {
        myChart.setOption(option, true);
      }
    },
    
    draw_string_radar (show_attribute, graph) {
      //定义一块SVG的绘制区域
      let div = d3.select('#show')
        .append('div')
        .attr('style', 'height: ' + this.height + '; width: ' + this.width)
        .attr('id', 'showchart');
      
      let dom = document.getElementById('showchart');
      var myChart = echarts.init(dom);
      var app = {};
      var option = null;
			
			let data1 = [];
			for(let i = 0; i < this.node1.length; i++) {
			  let value = this.node1[i]['attributes'][show_attribute];
				if(value != null) {
					data1.push(value);
				}
			}
			let data1_obj = {};
			for(let i = 0; i < data1.length; i++) {
				let name = data1[i];
				data1_obj[name] = (data1_obj[name] + 1) || 1;
			}
			let data = [];
			for(let k in data1_obj) {
				data.push([k, data1_obj[k], 0]);
			}
			for(let i = 0; i < this.node2.length; i++) {
			  let value = this.node2[i]['attributes'][show_attribute];
				for(let j = 0; j < data.length; j++) {
					if(value == data[j][0]) {
						data[j][2]++;
					}
				}
			}
			console.log(data);
			let a_data = [];
			for(let i = 0; i < data.length; i++) {
				a_data.push(data[i][1]);
			}
			let b_data = [];
			for(let i = 0; i < data.length; i++) {
				b_data.push(data[i][2]);
			}
			let max_data = [];
			for(let i = 0; i < a_data.length; i++) {
				max_data.push(Math.max(a_data[i], b_data[i]));
			}
			let name_data = [];
			for(let i = 0; i < data.length; i++) {
				name_data.push(data[i][0]);
			}
			let indicator_data = [];
			for(let i = 0; i < data.length; i++) {
				let obj = {
					name: name_data[i],
					max: max_data[i]
				};
				indicator_data.push(obj);
			}
			
      option = {
          title: {
              text: '属性值出现频率对比'
          },
          tooltip: {},
          toolbox: {
            feature: {
              myTool1: {
                show: true,
                title: '关闭',
                icon: 'path://M17.36,34.736l17.368-17.472M34.78,34.684L17.309,17.316',
                onclick: () => {
                  div.remove();
                }
              }
            }
          },
          radar: {
              // shape: 'circle',
              name: {
                  textStyle: {
                      color: '#fff',
                      backgroundColor: '#999',
                      borderRadius: 3,
                      padding: [3, 5]
                 }
              },
              indicator: indicator_data
          },
          series: [{
              //name: '预算 vs 开销（Budget vs spending）',
              type: 'radar',
              // areaStyle: {normal: {}},
              data : [
                  {
                      value : a_data,
                      name : this.compareId
                  },
                   {
                      value : b_data,
                      name : this.compareId
                  }
              ]
          }]
      };;
      if (option && typeof option === "object") {
          myChart.setOption(option, true);
      }
    },
  }
}
</script>

<style type='text/css' scoped>
  #comparechart {
    width: 65%;
    height: 55%;
    position: absolute;
    left: 2%;
    top: 1%;
    /* background: #303243 */
  }
  /* select {
      color:#10FBFE;
      #008C8C;
      background-color:#696969
  } */
  select {
    color: black
  }
  table {
    width: 99%;
  }
  tr {
    height: 40px;
  }
  th {
    text-align: center;
    /* color: #008C8C; */
    font-size: medium;
  }
  td {
    font-size: medium;
    text-align: center;
    width: 33%;
    /* color: #008C8C; */
    border: rgba(204, 204, 204, 1) dashed;
    border-width: 0 1px 1px 0
  }
</style>
