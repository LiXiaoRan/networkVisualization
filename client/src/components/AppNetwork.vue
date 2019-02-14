<template>
  <div>
    <div id='layout-panel'>
      <app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
      <div class='view'>
        <svg class='view-svg'>
        </svg>
        <div id="layContainer"></div>
        <div id="miniMap"></div>
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
              <td id='start_text_time' class="network_text2">2015.00.00 00:00:00</td>
            </tr>
            <tr>
              <td class="network_text1">讫时间</td>
            </tr>
            <tr>
              <td id='end_text_time' class="network_text2">2015.00.00 00:00:00</td>
            </tr>
          </table>
        </div>
        <div id="nodes_legend">
          <table border="0" width="100%">
            <tr class="network_text3">
              <td valign="middle" vertical-align="middle" class="graph_nodelegend_svg"></td>
              <td>主机</td>
              <td></td>
            </tr>
            <tr class="network_text2">
              <td></td>
              <td>{{hostNum}}</td>
              <td>0%</td>
            </tr>
            <tr class="network_text1">
              <td></td>
              <td>当前数量 &nbsp;</td>
              <td>占所有主机比例</td>
            </tr>
            <tr class="graph_tabel_padding">
              <td></td>
            </tr>
            <tr class="network_text3">
              <td class="graph_nodelegend_svg"></td>
              <td>交换机</td>
              <td></td>
            </tr>
            <tr class="network_text2">
              <td></td>
              <td>{{switchNum}}</td>
              <td>0%</td>
            </tr>
            <tr class="network_text1">
              <td></td>
              <td>当前数量 &nbsp;</td>
              <td>占所有交换机比例</td>
            </tr>
            <tr class="graph_tabel_padding">
              <td></td>
            </tr>
            <tr class="network_text3">
              <td class="graph_nodelegend_svg"></td>
              <td>服务器</td>
              <td></td>
            </tr>
            <tr class="network_text2">
              <td></td>
              <td>{{serverNum}}</td>
              <td>0%</td>
            </tr>
            <tr class="network_text1">
              <td></td>
              <td>当前数量 &nbsp;</td>
              <td>占所有服务器比例</td>
            </tr>
          </table>
        </div>
        <div id="level_legend">
          <table border="0" width="100%">
            <tr>
              <td class="graph_level_svg" width="12%"></td>
              <td class="network_text4" width="30%">致瘫级别</td>
              <td class="legend_color" width="58%"></td>
            </tr>
            <tr class="graph_tabel_padding">
              <td></td>
            </tr>
            <tr>
              <td class="graph_level_svg" width="12%"></td>
              <td class="network_text4" width="30%">控制级别</td>
              <td class="legend_color" width="58%"></td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>

</template>
<script>
  import AppTitle from "./AppTitle.vue";
  import * as dat from "dat.gui"
  import {mapGetters} from 'vuex';
  import hostImg from "../assets/host.png";
  import switchImg from "../assets/switch.png";
  import serverImg from "../assets/server.png";
  import hostSelectedImg from "../assets/host_selected.png";
  import switchSelectedImg from "../assets/switch_selected.png";
  import serverSelectedImg from "../assets/server_selected.png";
  import * as d3 from "d3";

  export default {
    data() {
      return {
        icon: 'joomla',
        msgs: "多层网络",
        iconLegend: "joomla",
        legendMsgs: "图例与指示",
        nowLayoutType: "rt_circular",
        layoutData: {},
        limit: 500,
        start: 0,
        end: 1000000000,
        linkAllShow: true,
        mainMiniMap: null,
        viewSize: {},
        nodesImgList: [hostImg, switchImg, serverImg],
        nodeSelectedList: [hostSelectedImg, switchSelectedImg, serverSelectedImg],
        hostNum: 0,
        serverNum: 0,
        switchNum: 0,
        nowLevel: 0,
      };
    },
    components: {AppTitle},
    mounted() {
      let self = this;
      let node_legend_svg = d3.selectAll(".graph_nodelegend_svg").append("svg")
        .attr("width", "20px").attr("height", "20px").append("image");
      node_legend_svg.attr("class", "brandCircle_image")
        .attr("xlink:href", (d, i) => this.nodesImgList[i])
        .attr("x", 0).attr("y", 4)
        .attr("width", 16).attr("height", 16);

      this.start_angle = 0;
      this.end_angle = 180 * (Math.PI / 180);
      let legend_r = 3;
      let legend_level_height = parseFloat(d3.select("#level_legend .network_text4").style("height"));
      let collapsed_color = ["white", "#b72626"];
      let control_color = ["#008475", "white"];
      this.collapsed_color_0 = ["#b72626", "#cd4d40", "#d37053", "#da9155", "#dac385"];
      this.control_color_0 = ["#008475", "#00ba8a", "#4dcf8b", "#9ce28d", "#dff68e"];
      let arcs_level = d3.arc()
        .startAngle(this.start_angle)
        .endAngle(this.end_angle)
        .innerRadius(2.4 * legend_r)
        .outerRadius(1.7 * legend_r);
      let level_svg = d3.selectAll(".graph_level_svg").append("svg")
        .attr("width", legend_level_height).attr("height", legend_level_height);
      level_svg.each(function (p, j) {
        d3.select(this).selectAll("path").data([0, 1]).enter().append("path")
          .attr("d", arcs_level)
          .attr("fill", function (d, i) {
            if (j === 0) {
              return collapsed_color[i];
            } else {
              return control_color[i];
            }
          })
          .attr("transform", function (d, i) {
            return "translate(" + (legend_level_height / 2) + "," + (legend_level_height / 2 + 2) + ")" + "rotate(" + 180 * i + ")";
          });
      });
      let legend_color_width = parseFloat(d3.select(".legend_color").style("width"));
      let legend_color_height = parseFloat(d3.select(".legend_color").style("height"));
      let legend_color_svg = d3.selectAll(".legend_color").append("svg")
        .attr("width", legend_color_width)
        .attr("height", legend_color_height);
      legend_color_svg.each(function (p, j) {
        d3.select(this).selectAll("rect")
          .data(d3.range(5)).enter().append("rect")
          .attr("x", function (d, i) {
            return legend_color_width / 5 * i;
          })
          .attr("y", legend_color_height / 4 * 3)
          .attr("width", legend_color_width / 5)
          .attr("height", legend_color_height / 4)
          .style("fill", (d, i) => {
            if (j === 0) {
              return self.collapsed_color_0[i];
            } else {
              return self.control_color_0[i];
            }
          });
        d3.select(this).selectAll(".levelText")
          .data(d3.range(5)).enter().append("text")
          .attr("class", "levelText")
          .style("fill", "#959595")
          .style("font-size", "5px")
          .attr("x", function (d, i) {
            return legend_color_width / 5 * i;
          })
          .attr("y", legend_color_height / 4 * 3 - 3)
          .text(function (d) {
            return d + 1;
          });
      });

      this.svg = d3.select(".view-svg");
      this.viewSize = {width: parseFloat(this.svg.style("width")), height: parseFloat(this.svg.style("height"))};
      this.padding = {top: 50, bottom: 50, left: 50, right: 50};
      let rateWH = Math.sqrt(this.viewSize.width * this.viewSize.height / 1200 / 400);
      this.arcs_width = rateWH * 2;
      let maxLinkWidth = 3 * rateWH;
      let minLinkWidth = 0.6 * rateWH;
      this.linkScale = d3.scaleLog().range([minLinkWidth, maxLinkWidth]);
      let maxNodeR = 30 * rateWH;
      let minNodeR = 6 * rateWH;
      this.nodeScale = d3.scaleLog().range([minNodeR, maxNodeR]);
      const gui = new dat.GUI();
      let obj = {
        网络层次: "全部层级",
        网络布局: "环状RT树布局",
        显示所有边: true
      };
      let f1 = gui.addFolder('控制');
      let levelText = f1.add(obj, "网络层次", ["全部层级", "链路层", "网络层", "应用层"]);
      let layoutText = f1.add(obj, "网络布局", [
        "环状RT树布局",
        "随机布局",
        "椭圆布局",
        "graphopt布局",
        "多元尺度布局",
        "网格布局",
        "大图布局",
        "分布式递归布局",
        "层次化布局",
        "力导向布局",
		"降维布局"
      ]);
      let linkAllShow = f1.add(obj, '显示所有边').listen();
      linkAllShow.onFinishChange(() => {
        this.linkAllShow = !this.linkAllShow;
        this.switchLinkShow();
      });

      let graphLayout = function () {
        self.getDataWithParams({
          where: {
            val: {
              start: self.start,
              end: self.end
            }
          },
          limit: self.limit,
          layout_type: self.nowLayoutType,
          level: self.nowLevel
        });
      };

      levelText.onChange(value => {
        //向后台传输所需层次数据
        switch (value) {
          case "全部层级":
            this.nowLevel = 0;
            break;
          case "链路层":
            this.nowLevel = 1;
            break;
          case "网络层":
            this.nowLevel = 2;
            break;
          case "应用层":
            this.nowLevel = 3;
            break;
        }
        graphLayout();
      });

      layoutText.onChange(value => {
		if(value=="降维布局"){
			this.$store.state.init_dim2 = Math.random();
			this.$store.state.timeupdated = Math.random();
		}else{
			switch (value) {
			  case "力导向布局":
				this.nowLayoutType = "kk";
				break;
			  case "随机布局":
				this.nowLayoutType = "random";
				break;
			  case "椭圆布局":
				this.nowLayoutType = "circle";
				break;
			  case "graphopt布局":
				this.nowLayoutType = "graphopt";
				break;
			  case "多元尺度布局":
				this.nowLayoutType = "mds";
				break;
			  case "网格布局":
				this.nowLayoutType = "grid";
				break;
			  case "大图布局":
				this.nowLayoutType = "lgl";
				break;
			  case "分布式递归布局":
				this.nowLayoutType = "drl";
				break;
			  case "层次化布局":
				this.nowLayoutType = "sugiyama";
				break;
			  case "环状RT树布局":
				this.nowLayoutType = "rt_circular";
				break;
			  default:
				break;
			}
			this.drawSwitchGraph();
		}
      });
      document.getElementById("layContainer").appendChild(gui.domElement);
      graphLayout();
    },
    methods: {
      drawSwitchGraph() {
        let paramsObj = {
          layoutData: JSON.stringify(this.layoutData),
          layout_type: this.nowLayoutType,
          level: this.nowLevel,
        };
        let Url = "get-layout-data";
        CommunicateWithServer('post', paramsObj, Url, this.drawGraph)
      },

      getDataWithParams(paramsObj) {
        CommunicateWithServer('get', paramsObj, 'cal-layout', this.drawGraph)
      },

      drawGraph(result) {
        let nodeType = this.nodeTypeList_get;
        let nodeAttrType = this.nodeAttrList_get;
        let self = this;
        this.layoutData = {'links': result.links, "nodes": result.nodes};
        this.layoutData.nodes.forEach(d => {
          if (d.nodeType === "主机") {
            this.hostNum++;
          } else if (d.nodeType === "交换机") {
            this.switchNum++;
          } else if (d.nodeType === "服务器") {
            this.serverNum++;
          }
        });
        if (this.svg.select("g")) this.svg.select("g").remove();
        let zoom = d3.zoom().scaleExtent([1, 10]).on("zoom", () => {
          this.nodesLinksG.attr("transform", d3.event.transform);
          /*g放大的时候其子节点不放大*/
          if (d3.event.transform.k > 1) {
            this.allNodesG.selectAll("image").attr("width", d => this.nodeScale(d.degree) / d3.event.transform.k)
              .attr("height", d => this.nodeScale(d.degree) / d3.event.transform.k)
              .attr("x", d => (this.xScale(d.x) - this.nodeScale(d.degree) / 2 / d3.event.transform.k))
              .attr("y", d => (this.yScale(d.y) - this.nodeScale(d.degree) / 2 / d3.event.transform.k));
            this.allNodesG.selectAll("path").attr("d", (d) => {
              let tmp_r = this.nodeScale(d.degree) / 2 / d3.event.transform.k;
              let arcs = d3.arc().startAngle(this.start_angle).endAngle(this.end_angle)
                .innerRadius(tmp_r - this.arcs_width / 2 / d3.event.transform.k).outerRadius(tmp_r + this.arcs_width / 2 / d3.event.transform.k);
              return arcs(d);
            });
            this.allLinksG.selectAll("line").attr("stroke-width", d => this.linkScale(d.flow) / d3.event.transform.k);
          }
        });
        this.svg.call(zoom);
        this.nodesLinksG = this.svg.append("g");

        this.layoutLinksG = this.nodesLinksG.append("g").attr("class", "links");
        this.layoutNodesG = this.nodesLinksG.append("g").attr("class", "nodes");

        this.xScale = d3.scaleLinear()
          .domain(d3.extent(result.nodes, d => d.x))
          .range([this.padding.left, this.viewSize.width - this.padding.right]);

        this.yScale = d3.scaleLinear()
          .domain(d3.extent(result.nodes, d => d.y))
          .range([this.padding.top, this.viewSize.height - this.padding.bottom]);

        this.linkScale.domain(d3.extent(result.links, d => d.flow));
        this.nodeScale.domain(d3.extent(result.nodes, d => d.degree));

        this.svg.on("mouseup", () => {
          if (event.target.nodeName === "svg") {
            this.nodesSelected = [];
            this.$store.state.nodesSelected = this.nodesSelected;
          }
        });

        this.allLinksG = this.layoutLinksG.selectAll("g")
          .data(result.links)
          .enter()
          .append("g")
          .attr("id", (d, i) => "link_" + i);
        this.allLinksG.append("line")
          .attr("stroke", "#999999")
          .attr("stroke-width", d => this.linkScale(d.flow))
          .attr("x1", d => this.xScale(d.x1))
          .attr("y1", d => this.yScale(d.y1))
          .attr("x2", d => this.xScale(d.x2))
          .attr("y2", d => this.yScale(d.y2));

        this.allNodesG = this.layoutNodesG.selectAll("g")
          .data(result.nodes)
          .enter()
          .append("g")
          .attr("id", d => "node_" + d.id);
        this.allNodesG.append("image")
          .attr("xlink:href", d => {
            if (d.nodeType === "主机") {
              return this.nodesImgList[0];
            } else if (d.nodeType === "交换机") {
              return this.nodesImgList[1];
            } else if (d.nodeType === "服务器") {
              return this.nodesImgList[2];
            }
          })
          .attr("x", d => this.xScale(d.x) - this.nodeScale(d.degree) / 2)
          .attr("y", d => this.yScale(d.y) - this.nodeScale(d.degree) / 2)
          .attr("width", d => this.nodeScale(d.degree))
          .attr("height", d => this.nodeScale(d.degree))
          .on("click", (d) => {
            //console.log(d.id);
            let tmpind = this.$store.state.nodesSelected.indexOf(d.id);
            if (tmpind >= 0) {
              this.$store.state.nodesSelected.splice(tmpind, 1);
            } else {
              this.$store.state.nodesSelected.push(d.id);
            }
          }).on("mouseover", function (d) {
          d3.select(this).attr("xlink:href", () => {
            if (d.nodeType === "主机") {
              return self.nodeSelectedList[0];
            } else if (d.nodeType === "交换机") {
              return self.nodeSelectedList[1];
            } else if (d.nodeType === "服务器") {
              return self.nodeSelectedList[2];
            }
          });
          self.layoutData.links.forEach((t, i) => {
            if (t.source === d.id) {
              d3.select("#link_" + i + " line").attr("stroke", "#00FFFF");
              d3.select("#node_" + t.target + " image").attr("xlink:href", () => {
                let connect = self.layoutData.nodes.find(item => (item.id === t.target));
                if (connect.nodeType === "主机") {
                  return self.nodeSelectedList[0];
                } else if (connect.nodeType === "交换机") {
                  return self.nodeSelectedList[1];
                } else if (connect.nodeType === "服务器") {
                  return self.nodeSelectedList[2];
                }
              });
            } else if (t.target === d.id) {
              d3.select("#link_" + i + " line").attr("stroke", "#00FFFF");
              d3.select("#node_" + t.source + " image").attr("xlink:href", () => {
                let connect = self.layoutData.nodes.find(item => (item.id === t.source));
                if (connect.nodeType === "主机") {
                  return self.nodeSelectedList[0];
                } else if (connect.nodeType === "交换机") {
                  return self.nodeSelectedList[1];
                } else if (connect.nodeType === "服务器") {
                  return self.nodeSelectedList[2];
                }
              });
            }
          })
        })
          .on("mouseout", function (d) {
            d3.select(this).attr("xlink:href", () => {
              if (d.nodeType === "主机") {
                return self.nodesImgList[0];
              } else if (d.nodeType === "交换机") {
                return self.nodesImgList[1];
              } else if (d.nodeType === "服务器") {
                return self.nodesImgList[2];
              }
            });
            self.layoutData.links.forEach((t, i) => {
              if (t.source === d.id) {
                d3.select("#link_" + i + " line").attr("stroke", "#999999");
                d3.select("#node_" + t.target + " image").attr("xlink:href", () => {
                  let connect = self.layoutData.nodes.find(item => (item.id === t.target));
                  if (connect.nodeType === "主机") {
                    return self.nodesImgList[0];
                  } else if (connect.nodeType === "交换机") {
                    return self.nodesImgList[1];
                  } else if (connect.nodeType === "服务器") {
                    return self.nodesImgList[2];
                  }
                });
              } else if (t.target === d.id) {
                d3.select("#link_" + i + " line").attr("stroke", "#999999");
                d3.select("#node_" + t.source + " image").attr("xlink:href", () => {
                  let connect = self.layoutData.nodes.find(item => (item.id === t.source));
                  if (connect.nodeType === "主机") {
                    return self.nodesImgList[0];
                  } else if (connect.nodeType === "交换机") {
                    return self.nodesImgList[1];
                  } else if (connect.nodeType === "服务器") {
                    return self.nodesImgList[2];
                  }
                });
              }
            })
          });

        this.allNodesG.append("path").attr("d", (d) => {
          let tmp_r = this.nodeScale(d.degree) / 2;
          let arcs = d3.arc().startAngle(this.start_angle).endAngle(this.end_angle)
            .innerRadius(tmp_r - this.arcs_width / 2).outerRadius(tmp_r + this.arcs_width / 2);
          return arcs(d);
        })
          .attr("class", "arc_collapse")
          .attr("transform", (d) => {
            return "translate(" + (this.xScale(d.x)) + "," + (this.yScale(d.y)) + ")"
          })
          .attr("fill", (d, i) => {
            return this.collapsed_color_0[i % 5];
          });

        this.allNodesG.append("path").attr("d", (d) => {
          let tmp_r = this.nodeScale(d.degree) / 2;
          let arcs = d3.arc().startAngle(this.start_angle).endAngle(this.end_angle)
            .innerRadius(tmp_r - this.arcs_width / 2).outerRadius(tmp_r + this.arcs_width / 2);
          return arcs(d);
        }).attr("class", "arc_control")
          .attr("transform", (d) => {
            return "translate(" + (this.xScale(d.x)) + "," + (this.yScale(d.y)) + ")" + "rotate(180)"
          })
          .attr("fill", (d, i) => {
            return this.control_color_0[i % 5];
          });

        this.secondFilter(nodeType, nodeAttrType);

        //this.$store.state.init_dim2 = Math.random();
        //this.$store.state.timeupdated = Math.random();
        if (d3.select("#miniMap").select("svg")) d3.select("#miniMap").select("svg").remove();
        this.miniMap = d3.select("#miniMap").append("svg")
          .attr("width", d3.select("#miniMap").style("width"))
          .attr("height", d3.select("#miniMap").style("height"));
      },

      drawMiniMap: function (res) {
        //绘制小地图
        if (miniMapG) miniMapG.remove();
        let miniMapG = this.miniMap.append("g");

        miniMapG.selectAll(".m_links")
          .data(res.links)
          .enter()
          .append("line")
          .attr("stroke", "#fff")
          .attr("stroke-width", 0.5)
          .attr("x1", d => this.posMiniX(this.xScale(d.x1)))
          .attr("y1", d => this.posMiniY(this.yScale(d.y1)))
          .attr("x2", d => this.posMiniX(this.xScale(d.x2)))
          .attr("y2", d => this.posMiniY(this.yScale(d.y2)));

        miniMapG.selectAll(".m_nodes")
          .data(res.nodes)
          .enter()
          .append("circle")
          .attr("r", 1)
          .attr("opacity", 0.9)
          .attr("fill", "#C4C9CF")
          .attr("cx", d => this.posMiniX(this.xScale(d.x)))
          .attr("cy", d => this.posMiniY(this.yScale(d.y)));

      },

      posMiniX: function (x) {
        return this.viewSize.width * $("#miniMap").width();
      },

      posMiniY: function (Y) {
        return this.viewSize.height * $("#miniMap").height();
      },

      switchLinkShow: function () {
        //切换边显示状态
        if (this.layoutLinksG) {
          if (this.linkAllShow) {
            this.layoutLinksG.attr("display", "block");
          } else {
            this.layoutLinksG.attr("display", "none");
          }
        }
      },

      secondFilter: function (typeList, attributeList) {
        //二级过滤
        let disappearNodes = new Set();
        this.allNodesG.attr("display", node => {
          if (typeList.includes(node.nodeType) && attributeList.includes(node.nodeAttribute)) {
            return "block";
          } else {
            disappearNodes.add(node.id);
            return "none";
          }
        });
        disappearNodes = [...disappearNodes];
        this.allLinksG.attr("display", link => {
          if (disappearNodes.includes(link.source) || disappearNodes.includes(link.target)) return "none";
          else return "block";
        });
      },
      transformData: function (data) {
        //转化为后台需要的布局
        let typeArray = ["主机", "交换机", "服务器"];
        let attrtArray = ["致瘫", "控制", "正常"];
        let formatData_node = [], formatData_link = [];
        let nodes = [], links = [];
        let source = '', target = '';
        data.forEach(function (d) {
          source = d.send_node_global_id.trim();
          target = d.receive_node_global_id.trim();
          nodes.push(source);
          nodes.push(target);
          links.push({source: source, target: target, flow: +d.val});
        });


        //去重
        nodes = [...new Set(nodes)];

        let strObj = {};
        links.forEach(function (item) {
          let str = JSON.stringify({source: item.source, target: item.target})

          if (!strObj[str]) {
            strObj[str] = item;//第一次出现
            //formatData_link.push({ source: item.source, target: item.target, flow: 0 });//不含重复项
          } else {
            strObj[str].flow += item.flow;//重复出现
          }
        });


        //按格式处理nodes
        nodes.forEach(function (d) {
          let obj = {
            id: d, nodeAttribute: attrtArray[parseInt(Math.random() * 3)],
            nodeType: typeArray[parseInt(Math.random() * 3)],
            in: 0, out: 0, x: 0, y: 0
          };
          formatData_node.push(obj);
        });
        //按格式处理links
        for (let link in strObj) {
          formatData_link.push(strObj[link]);
        }
        let formatData = {nodes: formatData_node, links: formatData_link};

        return formatData;
      }
    },
    computed: {
      ...mapGetters(['nodeTypeList_get', 'nodeAttrList_get']),
      ...mapGetters(['selectTime_get', 'selectData_get']),
      testData: function () {
        return this.$store.state.testData
      }
    },
    watch: {
      //监听过滤组件中的变化
      nodeTypeList_get: function (val) {
        this.secondFilter(val, this.nodeAttrList_get)
      },
      nodeAttrList_get: function (val) {
        this.secondFilter(this.nodeTypeList_get, val)
      },
      testData: function (newVal, oldVal) {

      }
      // ,
      // 'selectTime_get.start': {
      //   handler: function (val) {
      //     //根据时间轴的筛选进行布局
      //     let data = [].concat(this.selectData_get);
      //     this.layoutData = this.transformData(data);
      //     this.drawSwitchGraph();
      //
      //   },
      //   //immediate: true
      // }
    }
  };

</script>
<style lang="less" scoped>
  @import "./AppNetwork.less";

</style>
