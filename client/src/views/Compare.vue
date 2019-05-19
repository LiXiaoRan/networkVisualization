<template>
  <div id="Compare">
	<div id='button'></div>
	<div id="id"></div>
	<div id='show' style="position:absolute; top:100px"></div>
  </div>
</template>
<script>
	import * as d3 from 'd3';
	import echarts from 'echarts';
  export default {
  	data() {
  		return {
  			node1: [{'time': '20160715135005114569', 'attributes': {'attribute1': 32, 'attribute2': 'A'}},
				{'time': '20160715135205114569', 'attributes': {'attribute1': 50, 'attribute2': 'A'}},
				{'time': '20160715135505114569', 'attributes': {'attribute1': 43, 'attribute2': 'B'}},
				{'time': '20160715135905114569', 'attributes': {'attribute1': 61, 'attribute2': 'B'}},
				{'time': '20160715140305114569', 'attributes': {'attribute1': 70, 'attribute2': 'C'}},
				{'time': '20160715140505114569', 'attributes': {'attribute1': 55, 'attribute2': 'C'}}],
				node2: [{'time': '20160715135005114569', 'attributes': {'attribute1': 32, 'attribute2': 'A'}},
				{'time': '20160715135205114569', 'attributes': {'attribute1': 50, 'attribute2': 'A'}},
				{'time': '20160715135305114569', 'attributes': {'attribute1': 47, 'attribute2': 'A'}},
				{'time': '20160715135705114569', 'attributes': {'attribute1': 50, 'attribute2': 'A'}},
				{'time': '20160715135905114569', 'attributes': {'attribute1': 56, 'attribute2': 'A'}},
				{'time': '20160715140305114569', 'attributes': {'attribute1': 50, 'attribute2': 'A'}}],
				time_range: ['20160715134555000000', '20160715140655000000'],
				nodes_id: ['节点A', '节点B'],
				width: 1200,
				height: 500,
				padding: {
					top : 50,
					right : 20,
					bottom : 20,
					left : 20
				},
				rectStep: 30,
				rectWidth: 1,
				show_attribute: '选择属性',
				show_graph: '选择图表',
				showed_info: []
  		};
  	},
  	mounted() {
  		
  		this.yAxisWidth = this.height - this.padding.top - this.padding.bottom;
			this.xAxisWidth = this.width - this.padding.right - this.padding.left;
			
			let parsetime = d3.timeParse("%Y%m%d%H%M%S%f");
			
  		let select = d3.select("#button")
						.append('select');
		
			select.append('option')
				.text('选择属性');
			
			for(let i in this.node1[0].attributes){
				select.append('option')
					//.attr('id', i)
					.text(i);
			}
			
			//document.getElementsByTagName("select")[0].onchange=change;
			d3.selectAll('select')
				.on('change', () => {
				let index=document.getElementsByTagName("select")[0].selectedIndex;
				this.show_attribute=document.getElementsByTagName("select")[0].options[index].value;
				document.getElementsByTagName("select")[1].options.length = 1;
				if(this.show_attribute != '选择属性'){
					if(typeof(this.node1[0].attributes[this.show_attribute]) == 'number'){
						
						select2.append('option')
							.text('折线图');
						select2.append('option')
							.text('面积图');
						select2.append('option')
							.text('柱状图');
						select2.append('option')
							.text('堆叠图');
					}
					else if(typeof(this.node1[0].attributes[this.show_attribute]) == 'string'){
						select2.append('option')
							.text('小圆圈');
						select2.append('option')
							.text('饼图');
						select2.append('option')
							.text('雷达图');
					}
				}
			});
			
			let select2 = d3.select('#button')
			.append('select');
		
			select2.append('option')
				.text('选择图表');
				
			
			let go = d3.select('#button')
				.append('input')
				.attr('type', 'button')
				.attr('value', 'go')
				.on('click', () => {
				let index=document.getElementsByTagName("select")[0].selectedIndex;
				this.show_attribute=document.getElementsByTagName("select")[0].options[index].value;
				let index2=document.getElementsByTagName("select")[1].selectedIndex;
				this.show_graph=document.getElementsByTagName("select")[1].options[index2].value;
				if(this.show_attribute != '选择属性' && this.show_graph != '选择图表'){
					draw(this.show_attribute, this.show_graph);
					this.showed_info.push([this.show_attribute, this.show_graph]);
					console.log(this.showed_info);
				}
			});
  		
			let draw = (show_attribute, graph) => {
				//判断数据类型，根据数据类型设置y坐标及绘图
				if(typeof(this.node1[0].attributes[show_attribute]) == 'number'){
					if(graph == '折线图'){
						draw_number_line(show_attribute, graph);
					}
					else if(graph == '面积图'){
						draw_number_arealine(show_attribute, graph);
					}
					else if(graph == '柱状图'){
						draw_number_bar(show_attribute, graph);
					}
					else if(graph == '堆叠图'){
						draw_number_stack(show_attribute, graph);
					}
				}
				else if(typeof(this.node1[0].attributes[show_attribute]) == 'string'){
					if(graph == '小圆圈'){
						draw_string_circle(show_attribute);
					}
					else if(graph == '饼图'){
						draw_string_pie(show_attribute, graph);
					}
					else if(graph == '雷达图'){
						draw_string_radar(show_attribute, graph);
					}
				}	
			}
			
			let draw_number_arealine = (show_attribute, graph) => {
				//定义一块SVG的绘制区域
				let div = d3.select('#show')
					.append('div')
					.attr('style', 'height: ' + this.height + 'px; width: ' + this.width + 'px')
					.attr('id', show_attribute + graph);
				
				let dom = document.getElementById(show_attribute + graph);
				var myChart = echarts.init(dom);
				var app = {};
				var option = null;
				function randomData() {
				    now = new Date(+now + oneDay);
				    value = value + Math.random() * 21 - 10;
				    return {
				        name: now.toString(),
				        value: [
				            [now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'),
				            Math.round(value)
				        ]
				    }
				}
				
				var data = [];
				var now = +new Date(2016, 6, 15);
				var oneDay = 24 * 3600 * 1000;
				var value = Math.random() * 1000;
				for (var i = 0; i < 1000; i++) {
				    data.push(randomData());
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
				        end: 10
				    }, {
				    	type: 'slider',
				    	xAxisIndex: [0, 1],
				        start: 0,
				        end: 10,
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
				            name:'节点A',
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
				            name:'节点B',
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
				            data: data
				        }
				    ]
				};
				;
				if (option && typeof option === "object") {
				    myChart.setOption(option, true);
				}
			}
  	
  		let draw_number_line = (show_attribute, graph) => {
				//定义一块SVG的绘制区域
				let div = d3.select('#show')
					.append('div')
					.attr('style', 'height: ' + this.height + 'px; width: ' + this.width + 'px')
					.attr('id', show_attribute + graph);
				
				let dom = document.getElementById(show_attribute + graph);
				var myChart = echarts.init(dom);
				var app = {};
				var option = null;
				function randomData() {
				    now = new Date(+now + oneDay);
				    value = value + Math.random() * 21 - 10;
				    return {
				        name: now.toString(),
				        value: [
				            [now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'),
				            Math.round(value)
				        ]
				    }
				}
				
				var data = [];
				var now = +new Date(2016, 6, 15);
				var oneDay = 24 * 3600 * 1000;
				var value = Math.random() * 1000;
				for (var i = 0; i < 1000; i++) {
				    data.push(randomData());
				}
				
				var data2 = [];
				var now = +new Date(2016, 6, 15);
				var value = Math.random() * 1000;
				for (var i = 0; i < 1000; i++) {
				    data2.push(randomData());
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
											let index = this.showed_info.indexOf([show_attribute, graph]);
											console.log(index);
											if(index > -1) {
												this.showed_info.splice(index, 1);
											}
											console.log(this.showed_info);
		                }
		            	}
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
				        end: 10
				    }, {
				    	type: 'slider',
				        start: 0,
				        end: 10,
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
				            name:'节点A',
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
				            name:'节点B',
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
			}
  	
  		let draw_number_bar = (show_attribute, graph) => {
  			//定义一块SVG的绘制区域
				let div = d3.select('#show')
					.append('div')
					.attr('style', 'height: ' + this.height + 'px; width: ' + this.width + 'px')
					.attr('id', show_attribute + graph);
				
				let dom = document.getElementById(show_attribute + graph);
				var myChart = echarts.init(dom);
				var app = {};
				var option = null;
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
										let index = this.showed_info.indexOf([show_attribute, graph]);
										console.log(index);
										if(index > -1) {
											this.showed_info.splice(index, 1);
										}
										console.log(this.showed_info);
	                }
				    		}
				    	}
				    },
				    legend: {
				        data: ['2011年', '2012年']
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
				    	data: ['time1', 'time2', 'time3', 'time4', 'time5', 'time6']
				    },{
				        type: 'category',
				        gridIndex: 1,
				        axisTick: {
				        	show: false
				        },
				        axisLabel: {
				        	
				        },
				        data: ['time1', 'time2', 'time3', 'time4', 'time5', 'time6']
				    }],
				    series: [
				        {
				            name: 'A',
				            type: 'bar',
				            xAxisIndex: 0,
				            yAxisIndex: 0,
				            data: [18203, 23489, 29034, 104970, 131744, 630230]
				        },
				        {
				            name: 'B',
				            type: 'bar',
				            xAxisIndex: 1,
				            yAxisIndex: 1,
				            data: [19325, 23438, 31000, 121594, 134141, 681807]
				        }
				    ]
				};
				if (option && typeof option === "object") {
				    myChart.setOption(option, true);
				}
  		}
  	
  		let draw_number_stack = (show_attribute, graph) => {
  			//定义一块SVG的绘制区域
				let div = d3.select('#show')
					.append('div')
					.attr('style', 'height: ' + this.height + 'px; width: ' + this.width + 'px')
					.attr('id', show_attribute + graph);
				
				let dom = document.getElementById(show_attribute + graph);
				var myChart = echarts.init(dom);
				var app = {};
				var option = null;
				function randomData() {
				    now = new Date(+now + oneDay);
				    value = value + Math.random() * 21 - 10;
				    return {
				        name: now.toString(),
				        value: [
				            [now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'),
				            Math.round(value)
				        ]
				    }
				}
				
				var data = [];
				var now = +new Date(1997, 9, 3);
				var oneDay = 24 * 3600 * 1000;
				var value = Math.random() * 1000;
				for (var i = 0; i < 1000; i++) {
				    data.push(randomData());
				}
				
				var data2 = [];
				var now = +new Date(1997, 9, 3);
				var value = Math.random() * 1000;
				for (var i = 0; i < 1000; i++) {
				    data2.push(randomData());
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
										let index = this.showed_info.indexOf([show_attribute, graph]);
										console.log(index);
										if(index > -1) {
											this.showed_info.splice(index, 1);
										}
										console.log(this.showed_info);
	                }
				    		}
				    	}
				    },
				    legend: {
				        data:['节点A','节点B']
				    },
				    grid: {
				        left: '3%',
				        right: '4%',
				        bottom: '3%',
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
				        end: 10
				    }, {
				    	type: 'slider',
				        start: 0,
				        end: 10,
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
				            name:'节点A',
				            type:'line',
				            symbol: 'none',
				            smooth:true,
				            stack: '总量',
				            areaStyle: {},
				            data:data
				        },
				        {
				            name:'节点B',
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
  		}
			
			let draw_string_circle = (show_attribute, graph) => {
				//定义一块SVG的绘制区域
				let div = d3.select('#show')
					.append('div')
					.attr('id', show_attribute);
				
				let svg = div.append('svg')  // body中添加SVG
							.attr('width', this.width)  // SVG的宽度
							.attr('height', this.height);  // SVG的高度
				
				//X轴时间比例尺
								
				let xScale = d3.scaleTime()
					.domain([parsetime(this.time_range[0]), parsetime(this.time_range[1])])
					.range([this.width / 2 - this.padding.left, 0]);
				
				let xScale2 = d3.scaleTime()
					.domain([parsetime(this.time_range[0]), parsetime(this.time_range[1])])
					.range([this.width / 2 - this.padding.left, this.xAxisWidth]);
				
				
				//定义X坐标轴
				let xAxis = d3.axisBottom(xScale);  // 设置刻度朝向
				
				let xAxis2 = d3.axisBottom(xScale2);
				
				//添加元素
				let gxAxis = svg.append("g")
								.attr('transform', 'translate(' + this.padding.left + ',' + (this.height - this.padding.bottom) + ')')
								.call(xAxis);
				
				let gxAxis2 = svg.append("g")
								.attr('transform', 'translate(' + this.padding.left + ',' + (this.height - this.padding.bottom) + ')')
								.call(xAxis2);
				
				//画一条直线
				let line_data = [[0, 0], [0, this.yAxisWidth]];
					
				let gyAxis = svg.append("g")
								.attr('transform', 'translate(' + this.width / 2 + ',' + this.padding.top + ')');
								
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
				let color = d3.schemeSet3;
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
					.attr('cy', d => (this.height - this.padding.bottom - this.padding.top) / 2)  // 设置y坐标
					.attr('r', d => {
						if(d == null){
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
					.attr('cy', d => (this.height - this.padding.bottom - this.padding.top) / 2)  // 设置y坐标
					.attr('r', d => {
						if(d == null){
							return 0;
						}
						else{
							return this.rectStep / 4;
						}
					});  // 设置半径
				
				
				
				/*//在SVG中添加分组元素，里面存放标签元素
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
				}*/
				
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
					.attr('x', d => this.width / 2)
					.attr('y', d => 0)
					.text(d => d);
					
				let close_button = div.append('span')
					.attr('class', 'close big')
					.attr('left', this.width)
					.on('click', () => {
						div.remove();
						let index = this.showed_info.indexOf([show_attribute, graph]);
						console.log(index);
						if(index > -1) {
							this.showed_info.splice(index, 1);
						}
						console.log(this.showed_info);
					});
			}

			let draw_string_pie = (show_attribute, graph) => {
				//定义一块SVG的绘制区域
				let div = d3.select('#show')
					.append('div')
					.attr('style', 'height: ' + this.height + 'px; width: ' + this.width + 'px')
					.attr('id', show_attribute + graph);
				
				let dom = document.getElementById(show_attribute + graph);
				var myChart = echarts.init(dom);
				var app = {};
				var option = null;
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
										let index = this.showed_info.indexOf([show_attribute, graph]);
										console.log(index);
										if(index > -1) {
											this.showed_info.splice(index, 1);
										}
										console.log(this.showed_info);
	                }
				    		}
				    	}
				    },
				    dataset: {
				        source: [
				            ['node', '节点A', '节点B', 'C', 'D', 'E', 'F'],
				            ['attribute_A', 41.1, 30.4, 65.1, 53.3, 83.8, 98.7],
				            ['attribute_B', 86.5, 92.1, 85.7, 83.1, 73.4, 55.1],
				            ['attribute_C', 24.1, 67.2, 79.5, 86.4, 65.2, 82.5],
				            ['attribute_D', 55.2, 67.1, 69.2, 72.4, 53.9, 39.1]
				        ]
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
				            value: '节点B'
				        }
				    }]
				};
				if (option && typeof option === "object") {
				    myChart.setOption(option, true);
				}
			}
			
			let draw_string_radar = (show_attribute, graph) => {
				//定义一块SVG的绘制区域
				let div = d3.select('#show')
					.append('div')
					.attr('style', 'height: ' + this.height + 'px; width: ' + this.width + 'px')
					.attr('id', show_attribute + graph);
				
				let dom = document.getElementById(show_attribute + graph);
				var myChart = echarts.init(dom);
				var app = {};
				var option = null;
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
										let index = this.showed_info.indexOf([show_attribute, graph]);
										console.log(index);
										if(index > -1) {
											this.showed_info.splice(index, 1);
										}
										console.log(this.showed_info);
	                }
				    		}
				    	}
				    },
				    legend: {
				        data: ['节点A', '节点B']
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
				        indicator: [
				           { name: '属性值A', max: 6500},
				           { name: '属性值B', max: 16000},
				           { name: '属性值C', max: 30000},
				           { name: '属性值D', max: 38000},
				           { name: '属性值E', max: 52000},
				           { name: '属性值F', max: 25000}
				        ]
				    },
				    series: [{
				        //name: '预算 vs 开销（Budget vs spending）',
				        type: 'radar',
				        // areaStyle: {normal: {}},
				        data : [
				            {
				                value : [4300, 10000, 28000, 35000, 50000, 19000],
				                name : '节点A'
				            },
				             {
				                value : [5000, 14000, 28000, 31000, 42000, 21000],
				                name : '节点B'
				            }
				        ]
				    }]
				};;
				if (option && typeof option === "object") {
				    myChart.setOption(option, true);
				}
			}	
  	}
  };
</script>
<style >
	.close {
  position: absolute;
  display: inline-block;
  width: 20px;
  height: 20px;
  overflow: hidden;
}

.close:hover::before, .close:hover::after {
  background: #1ebcc5;
}

.close::before, .close::after {
  content: '';
  position: absolute;
  height: 2px;
  width: 100%;
  top: 50%;
  left: 0;
  margin-top: -1px;
  background: #000;
}

.close::before {
  -webkit-transform: rotate(45deg);
  -moz-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  -o-transform: rotate(45deg);
  transform: rotate(45deg);
}

.close::after {
  -webkit-transform: rotate(-45deg);
  -moz-transform: rotate(-45deg);
  -ms-transform: rotate(-45deg);
  -o-transform: rotate(-45deg);
  transform: rotate(-45deg);
}

.close.big {
  -webkit-transform: scale(1);
  -moz-transform: scale(1);
  -ms-transform: scale(1);
  -o-transform: scale(1);
  transform: scale(1);
}
</style>
