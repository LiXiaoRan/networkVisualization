<template>
  <div>
    <div id='layout-panel'>
      <app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
      <div class='view'>
        <svg class='view-svg'></svg>
        <div id="lay-container"></div>
        <div id="func-switch">
          <router-link target="_blank" to="/networkAnalysis">
            <button class="func-btn">高级网络特性分析</button>
          </router-link>
        </div>
      </div>
    </div>
    <div id="legend-index">
      <app-title v-bind:icon="icon" v-bind:msgs="legendMsgs"></app-title>
      <div class="legend">
        <div id="time_legend">
          <table border="0" width="100%">
            <tr>
              <td class="network_text1">起时间</td>
            </tr>
            <tr>
              <td class="network_text2">{{startTime}}</td>
            </tr>
            <tr>
              <td class="network_text1">讫时间</td>
            </tr>
            <tr>
              <td class="network_text2">{{endTime}}</td>
            </tr>
          </table>
        </div>
        <div id="nodes_legend">
          <table border="0" width="100%">
            <tr class="network_text3">
              <td class="graph_nodelegend_svg"></td>
              <td>主机</td>
            </tr>
            <tr>
              <td class="network_text2">{{hostNum}}</td>
              <td class="network_text1">当前数量</td>
            </tr>
            <tr>
              <td class="network_text2">{{totalHostNumPer}}</td>
              <td class="network_text1">占所有主机比例</td>
            </tr>
            <tr class="network_text3">
              <td class="graph_nodelegend_svg"></td>
              <td>交换机</td>
            </tr>
            <tr>
              <td class="network_text2">{{switchNum}}</td>
              <td class="network_text1">当前数量</td>
            </tr>
            <tr>
              <td class="network_text2">{{totalSwitchNumPer}}</td>
              <td class="network_text1">占所有交换机比例</td>
            </tr>
            <tr class="network_text3">
              <td class="graph_nodelegend_svg"></td>
              <td>服务器</td>
            </tr>
            <tr>
              <td class="network_text2">{{serverNum}}</td>
              <td class="network_text1">当前数量</td>
            </tr>
            <tr>
              <td class="network_text2">{{totalServerNumPer}}</td>
              <td class="network_text1">占所有服务器比例</td>
            </tr>
          </table>
        </div>
        <div id="control_legend">
          <div class="items_div">网络层次
            <div>
              <label v-for="item in levelList" class="label_network_level">
                <input type="radio" name="networkLevel" :value="item.value" :checked="item.isChecked"
                       class="input_network_level" @change="changeLevel(item)">
                {{item.name}}</label>
            </div>
          </div>
          <div class="items_div">布局方式
            <div>
              <button class="layout_btn" :class="{active: item.selected}"
                      v-for="item in layoutList" @click="switchLayout(item)">{{item.name}}
              </button>
            </div>
          </div>
          <div class="items_div">
            <span>显示边</span>
            <span class="switch_btn" :class="{'switch_btn_on' : linkAllShow}" @click="showLinks"></span>
            <span style="margin-left: 40px">
              <span>频繁通信</span>
              <span class="switch_btn" :class="{'switch_btn_on' : frameShow}" @click="showFrame"></span>
            </span>
          </div>
        </div>
        <div id="level_legend">
          <table border="0" width="100%">
            <tr style="height: 25px">
              <td class="graph_level_svg" width="10%"></td>
              <td class="network_text4" width="32%" style="padding-right: 5px;font-size: 12px">致瘫级别</td>
              <td class="legend_color" width="58%"></td>
            </tr>
            <tr style="height: 25px">
              <td class="graph_level_svg" width="10%"></td>
              <td class="network_text4" width="32%" style="padding-right: 5px;font-size: 12px">控制级别</td>
              <td class="legend_color" width="58%"></td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>

</template>
<script>
  import AppTitle from './AppTitle.vue';
  import {mapGetters, mapActions} from 'vuex';
  import hostImg from '../assets/host.png';
  import switchImg from '../assets/switch.png';
  import serverImg from '../assets/server.png';
  import hostSelectedImg from '../assets/host_selected.png';
  import switchSelectedImg from '../assets/switch_selected.png';
  import serverSelectedImg from '../assets/server_selected.png';
  import hostClickImg from '../assets/host_click.png';
  import switchClickImg from '../assets/switch_click.png';
  import serverClickImg from '../assets/server_click.png';
  import * as d3 from 'd3';
  import * as dat from 'dat.gui';

  export default {
    data() {
      return {
        icon: 'joomla',
        msgs: '多层网络',
        iconLegend: 'joomla',
        legendMsgs: '图例与指示',
        nowLayoutType: 'rt_circular',
        layoutData: {},
        startTime: '2016-07-15 15.52:12',
        endTime: '2016-07-15 15.53:12',
        linkAllShow: true,
        frameShow: false,
        mainMiniMap: null,
        viewSize: {},
        levelList: [{value: 0, isChecked: true, name: '全部'},
          {value: 1, isChecked: false, name: '链路'},
          {value: 2, isChecked: false, name: '网络'},
          {value: 3, isChecked: false, name: '应用'}],
        layoutList: [{name: 'RT树', value: 'rt_circular', selected: true},
          {name: '力导', value: 'kk', selected: false},
          {name: '降维', value: 'reduce', selected: false},
          {name: '环形', value: 'circle', selected: false},
          {name: '尺度', value: 'mds', selected: false},
          {name: '网格', value: 'grid', selected: false},
          {name: '大图', value: 'lgl', selected: false},
          {name: '递归', value: 'drl', selected: false},
          {name: '层次', value: 'sugiyama', selected: false}],
        nodesImgList: [hostImg, switchImg, serverImg],
        nodeSelectedList: [hostSelectedImg, switchSelectedImg, serverSelectedImg],
        nodeClickList: [hostClickImg, switchClickImg, serverClickImg],
        hostNum: 0,
        serverNum: 0,
        switchNum: 0,
        totalHostNumPer: '0%',
        totalSwitchNumPer: '0%',
        totalServerNumPer: '0%',
        nowLevel: 0,
        obj: {},
        selectedNode: null, // 选择单个节点
        selectedNodes: [], // 选择多个节点
        selectedFlag: false,
        disappearNodes: []
      };
    },
    components: {
      AppTitle
    },
    mounted() {
      let self = this;
      let node_legend_svg = d3.selectAll('.graph_nodelegend_svg').append('svg')
        .attr('width', '25px').attr('height', '25px').append('image');
      node_legend_svg.attr('class', 'brandCircle_image')
        .attr('xlink:href', (d, i) => this.nodesImgList[i])
        .attr('x', 0).attr('y', 4)
        .attr('width', 16).attr('height', 16);
      this.start_angle = 0;
      this.end_angle = 180 * (Math.PI / 180);
      let legend_r = 3;
      let legend_level_height = parseFloat(d3.select('#level_legend .network_text4').style('height'));
      let collapsed_color = ['#dac385', '#b72626'];
      let control_color = ['#008475', '#dff68e'];
      this.collapsed_color_0 = ['#b72626', '#cd4d40', '#d37053', '#da9155', '#dac385'];
      this.control_color_0 = ['#008475', '#00ba8a', '#4dcf8b', '#9ce28d', '#dff68e'];
      let arcs_level = d3.arc()
        .startAngle(this.start_angle)
        .endAngle(this.end_angle)
        .innerRadius(2.4 * legend_r)
        .outerRadius(1.7 * legend_r);
      let level_svg = d3.selectAll('.graph_level_svg').append('svg')
        .attr('width', legend_level_height).attr('height', legend_level_height);
      level_svg.each(function (p, j) {
        d3.select(this).selectAll('path').data([0, 1]).enter().append('path')
          .attr('d', arcs_level)
          .attr('fill', function (d, i) {
            if (j === 0) {
              return collapsed_color[i];
            } else {
              return control_color[i];
            }
          })
          .attr('transform', function (d, i) {
            return 'translate(' + (legend_level_height / 2) + ',' + (legend_level_height / 2 + 1) + ')' + 'rotate(' + 180 * i + ')';
          });
      });
      let legend_color_width = parseFloat(d3.select('.legend_color').style('width'));
      let legend_color_height = parseFloat(d3.select('.legend_color').style('height'));
      let legend_color_svg = d3.selectAll('.legend_color').append('svg')
        .attr('width', legend_color_width)
        .attr('height', legend_color_height);
      legend_color_svg.each(function (p, j) {
        d3.select(this).selectAll('rect')
          .data(d3.range(5)).enter().append('rect')
          .attr('x', function (d, i) {
            return legend_color_width / 5 * i;
          })
          .attr('y', legend_color_height / 4 * 2)
          .attr('width', legend_color_width / 5)
          .attr('height', legend_color_height / 4)
          .style('fill', (d, i) => {
            if (j === 0) {
              return self.collapsed_color_0[i];
            } else {
              return self.control_color_0[i];
            }
          });
        d3.select(this).selectAll('.levelText')
          .data(d3.range(5)).enter().append('text')
          .attr('class', 'levelText')
          .style('fill', '#959595')
          .style('font-size', '7px')
          .attr('x', function (d, i) {
            return legend_color_width / 5 * i;
          })
          .attr('y', legend_color_height / 4 * 2 - 3)
          .text(function (d) {
            return d + 1;
          });
      });
      this.svg = d3.select('.view-svg');
      let width = parseFloat(this.svg.style('width'));
      let height = parseFloat(this.svg.style('height'));
      this.viewSize = {width: width, height: height};

      this.padding = {top: 20, bottom: 20, left: (width - height + 40) / 2, right: (width - height + 40) / 2};
      let rateWH = Math.sqrt(this.viewSize.width * this.viewSize.height / 1200 / 400);
      this.arcs_width = rateWH * 2;
      let maxLinkWidth = 3 * rateWH;
      let minLinkWidth = 0.6 * rateWH;
      this.linkScale = d3.scaleLog().range([minLinkWidth, maxLinkWidth]);
      let maxNodeR = 30 * rateWH;
      let minNodeR = 6 * rateWH;
      this.nodeScale = d3.scaleLog().range([minNodeR, maxNodeR]);

      const gui = new dat.GUI();
      this.obj = {
        节点类型: '',
        致瘫级别: 1,
        控制级别: 1
      };
      this.folder = gui.addFolder('节点属性');

      // 节点类型
      let nodeType = this.folder.add(this.obj, '节点类型', [
        '主机',
        '交换机',
        '服务器'
      ]).listen();
      let nodeTypeFun = function (item, value) {
        let type = -1;
        if (value === '主机') {
          type = 0;
        } else if (value === '交换机') {
          type = 1;
        } else if (value === '服务器') {
          type = 2;
        }
        d3.select('#node_' + item.id)
          .select('image')
          .attr('xlink:href', self.nodeClickList[type]);
      };
      nodeType.onFinishChange((value) => {
        if (this.selectedFlag) {
          this.selectedNodes.forEach(item => {
            nodeTypeFun(item, value);
          });
        } else {
          nodeTypeFun(this.selectedNode, value);
        }
      });
      // 控制级别
      let controlLevel = this.folder.add(this.obj, '控制级别').min(1).max(5).step(1).listen();
      let controlLevelFun = function (item, value) {
        d3.select('#node_' + item.id)
          .select('.arc_control')
          .attr('fill', self.control_color_0[value - 1]);
      };
      controlLevel.onFinishChange((value) => {
        if (this.selectedFlag) {
          this.selectedNodes.forEach(item => {
            controlLevelFun(item, value);
          });
        } else {
          controlLevelFun(this.selectedNode, value);
        }
      });

      // 致瘫级别
      let collapsedLevel = this.folder.add(this.obj, '致瘫级别').min(1).max(5).step(1).listen();
      let collapsedLevelFun = function (item, value) {
        d3.select('#node_' + item.id)
          .attr('fill', (d) => {
            d.palsy = value - 1;
          })
          .select('.arc_collapse')
          .attr('fill', () => self.collapsed_color_0[value - 1]);
      };
      collapsedLevel.onFinishChange((value) => {
        if (this.selectedFlag) {
          this.selectedNodes.forEach(item => {
            controlLevelFun(item, value);
          });
        } else {
          collapsedLevelFun(this.selectedNode, value);
        }
      });
      document.getElementById('lay-container').appendChild(gui.domElement);
    },
    methods: {
      ...mapActions(['modifyLayoutData_sync']),
      drawSwitchGraph() {
        let paramsObj = {
          layout_type: this.nowLayoutType,
          network_level: this.nowLevel
        };
        let Url = 'get-layout-data';
        CommunicateWithServer('get', paramsObj, Url, this.drawGraph);
      },
      changeLevel(item) {
        this.levelList.forEach(obj => obj.isChecked = false);
        item.isChecked = true;
        this.nowLevel = item.value;
        this.drawSwitchGraph();

      },
      switchLayout(item) {
        this.layoutList.forEach(obj => obj.selected = false);
        item.selected = true;
        if (item.value === 'reduce') {
          d3.select('#dim2-panel').style('display', 'block');
          this.$store.state.init_dim2 = Math.random();
          this.$store.state.timeupdated = Math.random();
        } else {
          d3.select('#dim2-panel').style('display', 'none');
          this.nowLayoutType = item.value;
          this.drawSwitchGraph();
        }
      },
      showLinks() {
        //切换边显示状态
        this.linkAllShow = !this.linkAllShow;
        if (this.allLinksG) {
          this.allLinksG.attr('display', this.linkAllShow ? 'block' : 'none');
          if (this.disappearNodes.length && this.linkAllShow) {
            this.allLinksG.attr('display', link => {
              if (this.disappearNodes.includes(link.source) || this.disappearNodes.includes(link.target)) return 'none';
            });
          }
        }
      },
      showFrame() {
        let self = this;
        this.frameShow = !this.frameShow;
        if (this.frameShow) {
          this.allNodesG.selectAll('image').on('click', null).on('mouseover', null).on('mouseout', null);//去除事件响应
          this.allLinksG.attr('display', 'none');
          this.allNodesG.attr('display', 'none');
          //以次数表示边的宽度
          this.linkScale.domain(d3.extent(this.layoutData.links, d => d.times));
          this.allLinksG.attr('stroke-width', d => this.linkScale(d.times));
          //显示前百分之十
          let num = Math.floor(this.layoutData.links.length * 0.1);
          for (let i = 0; i < num; i++) {
            d3.select('#link_' + i).attr('display', 'block');
            d3.select('#node_' + this.layoutData.links[i].source).attr('display', 'block');
            d3.select('#node_' + this.layoutData.links[i].target).attr('display', 'block');
          }
        } else {
          //还原操作
          this.linkScale.domain(d3.extent(this.layoutData.links, d => d.flow));
          this.allLinksG.attr('stroke-width', d => this.linkScale(d.flow));
          this.allNodesG.selectAll('image')
            .on('click', function (d) {
              self.folder.open();
              if (d3.event.ctrlKey) {
                //清除单选信息
                self.selectedNode = null;
                if (self.nowClickNode !== null) {
                  self.nowClickNode.attr('xlink:href', (l) => self.nodesImgList[l.nodeType]).classed('clicked', false);
                  self.nowClickNode = null;
                }
                // 多选
                let index = self.selectedNodes.findIndex(item => item.id === d.id);
                if (index !== -1) {
                  self.selectedNodes.splice(index, 1);
                  d3.select(this).attr('xlink:href', self.nodesImgList[d.nodeType]).classed('clicked', false);
                } else {
                  self.selectedNodes.push(d);
                  d3.select(this).attr('xlink:href', self.nodeClickList[d.nodeType]).classed('clicked', true);
                }
                self.selectedFlag = true;
              } else {
                self.selectedNodes.forEach(item => {
                  d3.select('#node_' + item.id + ' image').attr('xlink:href', self.nodesImgList[item.nodeType]).classed('clicked', false);
                });
                self.selectedNodes = [];
                self.selectedNode = d;
                if (self.nowClickNode === null) {
                  self.nowClickNode = d3.select(this);
                } else {
                  self.nowClickNode.attr('xlink:href', (l) => self.nodesImgList[l.nodeType]).classed('clicked', false);
                  self.nowClickNode = d3.select(this);
                }
                d3.select(this).attr('xlink:href', self.nodeClickList[d.nodeType]).classed('clicked', true);
                self.selectedFlag = false;
              }
              self.updated(d);

              if (self.selectedFlag) {
                let tmpNodes = [];
                for (let m = 0; m < self.selectedNodes.length; m++) {
                  tmpNodes.push(self.selectedNodes[m]['id']);
                }
                self.$store.state.nodesSelected = tmpNodes;
              } else {
                self.$store.state.nodesSelected = [self.selectedNode['id']];
              }
            })
            .on('mouseover', function (d) {
              d3.select(this).attr('xlink:href', () => self.nodeSelectedList[d.nodeType]);
              self.layoutData.links.forEach((t, i) => {
                if (t.source === d.id) {
                  d3.select('#link_' + i).attr('display', 'block').select('line').attr('stroke', '#00FFFF');
                  d3.select('#node_' + t.target + ' image').attr('xlink:href', () => {
                    let connect = self.layoutData.nodes.find(item => (item.id === t.target));
                    return self.nodeSelectedList[connect.nodeType];
                  });
                } else if (t.target === d.id) {
                  d3.select('#link_' + i).attr('display', 'block').select('line').attr('stroke', '#00FFFF');
                  d3.select('#node_' + t.source + ' image').attr('xlink:href', () => {
                    let connect = self.layoutData.nodes.find(item => (item.id === t.source));
                    return self.nodeSelectedList[connect.nodeType];
                  });
                }
              });
            })
            .on('mouseout', function (d) {
              d3.select(this).attr('xlink:href', self.nodesImgList[d.nodeType]);
              self.layoutData.links.forEach((t, i) => {
                if (t.source === d.id) {
                  d3.select('#link_' + i).attr('display', self.linkAllShow ? 'block' : 'none').select('line').attr('stroke', '#999999');
                  d3.select('#node_' + t.target + ' image').attr('xlink:href', () => {
                    let connect = self.layoutData.nodes.find(item => (item.id === t.target));
                    return self.nodesImgList[connect.nodeType];
                  });
                } else if (t.target === d.id) {
                  d3.select('#link_' + i).attr('display', self.linkAllShow ? 'block' : 'none').select('line').attr('stroke', '#999999');
                  d3.select('#node_' + t.source + ' image').attr('xlink:href', () => {
                    let connect = self.layoutData.nodes.find(item => (item.id === t.source));
                    return self.nodesImgList[connect.nodeType];
                  });
                }
              });
              if (d3.select(this).classed('clicked'))
                d3.select(this).attr('xlink:href', () => self.nodeClickList[d.nodeType]).classed('clicked', true);
            });
          this.allLinksG.attr('display', 'block');
          this.allNodesG.attr('display', 'block');
        }


      },
      drawGraph(result) {
        let self = this;
        this.hostNum = 0;
        this.switchNum = 0;
        this.serverNum = 0;
        this.nowClickNode = null;
        this.layoutData = result;
        this.layoutData.links.sort((first, second) => second.times - first.times);
        this.layoutData.nodes.forEach(d => {
          if (d.nodeType === 0) {
            this.hostNum++;
          } else if (d.nodeType === 1) {
            this.switchNum++;
          } else if (d.nodeType === 2) {
            this.serverNum++;
          }
        });
        this.totalHostNumPer = (this.hostNum / nodesNumber.hostNumber * 100).toFixed(2) + '%';
        this.totalSwitchNumPer = (this.switchNum / nodesNumber.switchNumber * 100).toFixed(2) + '%';
        this.totalServerNumPer = (this.serverNum / nodesNumber.serverNumber * 100).toFixed(2) + '%';
        if (this.svg.select('g')) this.svg.select('g').remove();
        let zoom = d3.zoom().scaleExtent([1, 10]).on('zoom', () => {
          this.nodesLinksG.attr('transform', d3.event.transform);
          /*g放大的时候其子节点不放大*/
          if (d3.event.transform.k > 1) {
            this.allNodesG.selectAll('image').attr('width', d => this.nodeScale(d.degree) / d3.event.transform.k)
              .attr('height', d => this.nodeScale(d.degree) / d3.event.transform.k)
              .attr('x', d => (this.xScale(d.x) - this.nodeScale(d.degree) / 2 / d3.event.transform.k))
              .attr('y', d => (this.yScale(d.y) - this.nodeScale(d.degree) / 2 / d3.event.transform.k));
            this.allNodesG.selectAll('path').attr('d', (d) => {
              let tmp_r = this.nodeScale(d.degree) / 2 / d3.event.transform.k;
              let arcs = d3.arc().startAngle(this.start_angle).endAngle(this.end_angle)
                .innerRadius(tmp_r - this.arcs_width / 2 / d3.event.transform.k).outerRadius(tmp_r + this.arcs_width / 2 / d3.event.transform.k);
              return arcs(d);
            });
            this.allLinksG.selectAll('line').attr('stroke-width', d => this.linkScale(d.flow) / d3.event.transform.k);
          }
        });
        this.svg.call(zoom);
        this.nodesLinksG = this.svg.append('g');
        this.layoutLinksG = this.nodesLinksG.append('g').attr('class', 'links');
        this.layoutNodesG = this.nodesLinksG.append('g').attr('class', 'nodes');
        this.xScale = d3.scaleLinear()
          .domain(d3.extent(result.nodes, d => d.x))
          .range([this.padding.left, this.viewSize.width - this.padding.right]);
        this.yScale = d3.scaleLinear()
          .domain(d3.extent(result.nodes, d => d.y))
          .range([this.padding.top, this.viewSize.height - this.padding.bottom]);
        this.linkScale.domain(d3.extent(result.links, d => d.flow));
        this.nodeScale.domain(d3.extent(result.nodes, d => d.degree));
        this.svg.on('click', () => {
          if (event.target.nodeName === 'svg') {
            //清除单选信息
            this.selectedNode = null;
            if (this.nowClickNode !== null) {
              this.nowClickNode.attr('xlink:href', (l) => self.nodesImgList[l.nodeType]).classed('clicked', false);
              this.nowClickNode = null;
            }
            this.selectedNodes.forEach(item => {
              d3.select('#node_' + item.id + ' image').attr('xlink:href', self.nodesImgList[item.nodeType]).classed('clicked', false);
            });
            this.selectedNodes = [];
            this.folder.close();
            //此处清空所选节点信息，交大写上对应变更
            this.$store.state.nodesSelected = [];
          }
        });
        this.allLinksG = this.layoutLinksG.selectAll('g')
          .data(result.links)
          .enter()
          .append('g')
          .attr('id', (d, i) => 'link_' + i)
          .attr('display', this.linkAllShow ? 'block' : 'none');
        this.allLinksG.append('line')
          .attr('stroke', '#999999')
          .attr('stroke-width', d => this.linkScale(d.flow))
          .attr('x1', d => this.xScale(d.x1))
          .attr('y1', d => this.yScale(d.y1))
          .attr('x2', d => this.xScale(d.x2))
          .attr('y2', d => this.yScale(d.y2));
        this.allNodesG = this.layoutNodesG.selectAll('g')
          .data(result.nodes)
          .enter()
          .append('g')
          .attr('id', d => 'node_' + d.id);
        this.allNodesG.append('image')
          .attr('xlink:href', d => this.nodesImgList[d.nodeType])
          .attr('x', d => this.xScale(d.x) - this.nodeScale(d.degree) / 2)
          .attr('y', d => this.yScale(d.y) - this.nodeScale(d.degree) / 2)
          .attr('width', d => this.nodeScale(d.degree))
          .attr('height', d => this.nodeScale(d.degree))
          .classed('clicked', false)
          .on('click', function (d) {
            self.folder.open();
            if (d3.event.ctrlKey) {
              //清除单选信息
              self.selectedNode = null;
              if (self.nowClickNode !== null) {
                self.nowClickNode.attr('xlink:href', (l) => self.nodesImgList[l.nodeType]).classed('clicked', false);
                self.nowClickNode = null;
              }
              // 多选
              let index = self.selectedNodes.findIndex(item => item.id === d.id);
              if (index !== -1) {
                self.selectedNodes.splice(index, 1);
                d3.select(this).attr('xlink:href', self.nodesImgList[d.nodeType]).classed('clicked', false);
              } else {
                self.selectedNodes.push(d);
                d3.select(this).attr('xlink:href', self.nodeClickList[d.nodeType]).classed('clicked', true);
              }
              self.selectedFlag = true;
            } else {
              self.selectedNodes.forEach(item => {
                d3.select('#node_' + item.id + ' image').attr('xlink:href', self.nodesImgList[item.nodeType]).classed('clicked', false);
              });
              self.selectedNodes = [];
              self.selectedNode = d;
              if (self.nowClickNode === null) {
                self.nowClickNode = d3.select(this);
              } else {
                self.nowClickNode.attr('xlink:href', (l) => self.nodesImgList[l.nodeType]).classed('clicked', false);
                self.nowClickNode = d3.select(this);
              }
              d3.select(this).attr('xlink:href', self.nodeClickList[d.nodeType]).classed('clicked', true);
              self.selectedFlag = false;
            }
            self.updated(d);

            if (self.selectedFlag) {
              let tmpNodes = [];
              for (let m = 0; m < self.selectedNodes.length; m++) {
                tmpNodes.push(self.selectedNodes[m]['id']);
              }
              self.$store.state.nodesSelected = tmpNodes;
            } else {
              self.$store.state.nodesSelected = [self.selectedNode['id']];
            }
          })
          .on('mouseover', function (d) {
            d3.select(this).attr('xlink:href', () => self.nodeSelectedList[d.nodeType]);
            self.layoutData.links.forEach((t, i) => {
              if (t.source === d.id) {
                d3.select('#link_' + i).attr('display', 'block').select('line').attr('stroke', '#00FFFF');
                d3.select('#node_' + t.target + ' image').attr('xlink:href', () => {
                  let connect = self.layoutData.nodes.find(item => (item.id === t.target));
                  return self.nodeSelectedList[connect.nodeType];
                });
              } else if (t.target === d.id) {
                d3.select('#link_' + i).attr('display', 'block').select('line').attr('stroke', '#00FFFF');
                d3.select('#node_' + t.source + ' image').attr('xlink:href', () => {
                  let connect = self.layoutData.nodes.find(item => (item.id === t.source));
                  return self.nodeSelectedList[connect.nodeType];
                });
              }
            });
          })
          .on('mouseout', function (d) {
            d3.select(this).attr('xlink:href', self.nodesImgList[d.nodeType]);
            self.layoutData.links.forEach((t, i) => {
              if (t.source === d.id) {
                d3.select('#link_' + i).attr('display', self.linkAllShow ? 'block' : 'none').select('line').attr('stroke', '#999999');
                d3.select('#node_' + t.target + ' image').attr('xlink:href', () => {
                  let connect = self.layoutData.nodes.find(item => (item.id === t.target));
                  return self.nodesImgList[connect.nodeType];
                });
              } else if (t.target === d.id) {
                d3.select('#link_' + i).attr('display', self.linkAllShow ? 'block' : 'none').select('line').attr('stroke', '#999999');
                d3.select('#node_' + t.source + ' image').attr('xlink:href', () => {
                  let connect = self.layoutData.nodes.find(item => (item.id === t.source));
                  return self.nodesImgList[connect.nodeType];
                });
              }
            });
            if (d3.select(this).classed('clicked'))
              d3.select(this).attr('xlink:href', () => self.nodeClickList[d.nodeType]).classed('clicked', true);
          });
        this.allNodesG.append('path').attr('d', (d) => {
          let tmp_r = this.nodeScale(d.degree) / 2;
          let arcs = d3.arc().startAngle(this.start_angle).endAngle(this.end_angle)
            .innerRadius(tmp_r - this.arcs_width / 2).outerRadius(tmp_r + this.arcs_width / 2);
          return arcs(d);
        })
          .attr('class', 'arc_collapse')
          .attr('transform', (d) => 'translate(' + (this.xScale(d.x)) + ',' + (this.yScale(d.y)) + ')')
          .attr('fill', (d) => this.collapsed_color_0[d.palsy]);
        this.allNodesG.append('path').attr('d', (d) => {
          let tmp_r = this.nodeScale(d.degree) / 2;
          let arcs = d3.arc().startAngle(this.start_angle).endAngle(this.end_angle)
            .innerRadius(tmp_r - this.arcs_width / 2).outerRadius(tmp_r + this.arcs_width / 2);
          return arcs(d);
        }).attr('class', 'arc_control')
          .attr('transform', (d) => 'translate(' + (this.xScale(d.x)) + ',' + (this.yScale(d.y)) + ')' + 'rotate(180)')
          .attr('fill', (d) => this.control_color_0[d.control]);
      },
      updated(item) {
        if (item.nodeType === 0) {
          this.obj['节点类型'] = '主机';
        } else if (item.nodeType === 1) {
          this.obj['节点类型'] = '交换机';
        } else if (item.nodeType === 2) {
          this.obj['节点类型'] = '服务器';
        }
        this.obj['控制级别'] = item.control + 1;
        this.obj['致瘫级别'] = item.palsy + 1;
      }
    },
    computed: {
      ...mapGetters(['nodeTypeList_get', 'palsyList_get', 'controlList_get', 'selectTime_get', 'brushData_get'])
    },
    watch: {
      //监听过滤组件中的变化
      nodeTypeList_get: function (typeList) {
        let disappearNodes = new Set();
        this.allNodesG.attr('display', node => {
          if (typeList.includes(node.nodeType)) {
            return 'block';
          } else {
            disappearNodes.add(node.id);
            return 'none';
          }
        });
        this.disappearNodes = [...disappearNodes];
        if (this.linkAllShow) {
          this.allLinksG.attr('display', link => {
            if (this.disappearNodes.includes(link.source) || this.disappearNodes.includes(link.target)) return 'none';
          });
        }
      },
      palsyList_get: function (palsyList) {
        this.allNodesG.selectAll('.arc_collapse').attr('fill', (d) => {
          if (!palsyList.includes(d.palsy)) {
            return '#FFFFFF';
          } else {
            return this.collapsed_color_0[d.palsy];
          }
        });
      },
      controlList_get: function (controlList) {
        this.allNodesG.selectAll('.arc_control').attr('fill', (d) => {
          if (!controlList.includes(d.control)) {
            return '#FFFFFF';
          } else {
            return this.control_color_0[d.control];
          }
        });
      },
      selectTime_get: function (val) {
        this.startTime = val.start;
        this.endTime = val.end;
        this.drawSwitchGraph();
      },
      layoutData: function (val) {
        this.modifyLayoutData_sync({layoutData: val});
      },
      brushData_get: function (brushList) {
        //这里的val为刷取的节点数据
        let disappearNodes = [];
        this.allNodesG.attr('display', node => {
          if (brushList.includes(node.id)) {
            return 'block';
          } else {
            disappearNodes.push(node.id);
            return 'none';
          }
        });
        this.disappearNodes = disappearNodes;
        if (this.linkAllShow) {
          this.allLinksG.attr('display', link => {
            if (this.disappearNodes.includes(link.source) || this.disappearNodes.includes(link.target)) return 'none';
          });
        }
      }
    }
  };
</script>
<style lang="less">
  @import "./AppNetwork.less";
</style>
