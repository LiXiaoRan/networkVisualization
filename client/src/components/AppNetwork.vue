<template>
  <div id='layout-panel'>
    <app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
    <div class='view'>
      <svg class='view-svg'>
      </svg>
      <div id="layContainer"></div>
      <div id="miniMap"></div>
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
  import * as d3 from "d3";

  export default {
    data() {
      return {
        icon: 'joomla',
        msgs: "多层网络",
        nowLayoutType: null,
        layoutData: {},
        limit: 8000,
        start: 0,
        end: 1000000000,
        linkAllShow: true,
        mainMiniMap: null,
        viewSize: {},
        nodesImgList: [hostImg, switchImg, serverImg]
      };
    },
    components: {AppTitle},
    mounted() {
      this.svg = d3.select(".view-svg");
      this.viewSize = {width: parseFloat(this.svg.style("width")), height: parseFloat(this.svg.style("height"))};
      this.padding = {top: 50, bottom: 50, left: 50, right: 50};
      let rateWH = Math.sqrt(this.viewSize.width * this.viewSize.height / 1200 / 400);
      let maxLinkWidth = 3 * rateWH;
      let minLinkWidth = 0.6 * rateWH;
      this.linkScale = d3.scaleLog().range([minLinkWidth, maxLinkWidth]);
      let maxNodeR = 30 * rateWH;
      let minNodeR = 6 * rateWH;
      this.nodeScale = d3.scaleLog().range([minNodeR, maxNodeR]);

      let self = this;
      this.nowLayoutType = "大图布局";
      const gui = new dat.GUI();
      let obj = {
        布局: "力导向布局",
        显示所有边: true
      };
      let f1 = gui.addFolder('控制');
      let layoutText = f1.add(obj, "布局", [
        "力导向布局",
        "随机布局",
        "椭圆布局",
        "graphopt布局",
        "多元尺度布局",
        "网格布局",
        "大图布局",
        "分布式递归布局",
        "层次化布局",
        "环状RT树布局"
      ]);
      let linkAllShow = f1.add(obj, '显示所有边').listen();
      linkAllShow.onFinishChange(() => {
        this.linkAllShow = !this.linkAllShow;
        this.switchLinkShow();
      });

      let graphLayout = function (type) {
        self.getDataWithParams({
          where: {
            val: {
              start: self.start,
              end: self.end
            }
          },
          limit: self.limit,
          layout_type: type
        });
      };

      let switchGraph = function (type) {
        self.drawSwitchGraph(type);
      };

      layoutText.onChange(value => {
        switch (value) {
          case "力导向布局":
            this.nowLayoutType = "kk";
            switchGraph("kk");
            break;
          case "随机布局":
            this.nowLayoutType = "random";
            switchGraph("random");
            break;
          case "椭圆布局":
            this.nowLayoutType = "circle";
            switchGraph("circle");
            break;
          case "graphopt布局":
            this.nowLayoutType = "graphopt";
            switchGraph("graphopt");
            break;
          case "多元尺度布局":
            this.nowLayoutType = "mds";
            switchGraph("mds");
            break;
          case "网格布局":
            this.nowLayoutType = "grid";
            switchGraph("grid");
            break;
          case "大图布局":
            this.nowLayoutType = "lgl";
            switchGraph("lgl");
            break;
          case "分布式递归布局":
            this.nowLayoutType = "drl";
            switchGraph("drl");
            break;
          case "层次化布局":
            this.nowLayoutType = "sugiyama";
            switchGraph("sugiyama");
            break;
          case "环状RT树布局":
            this.nowLayoutType = "rt_circular";
            switchGraph("rt_circular");
            break;
          default:
            break;
        }
      });
      document.getElementById("layContainer").appendChild(gui.domElement);
      graphLayout("kk");
    },
    methods: {
      drawSwitchGraph(type) {
        let paramsObj = {
          layoutData: JSON.stringify(this.layoutData),
          layout_type: type
        };
        let Url = "get-layout-data";
        CommunicateWithServer('post', paramsObj, Url, this.drawGraph)
      },

      getDataWithParams(paramsObj) {
        CommunicateWithServer('get', paramsObj, 'cal-layout', this.drawGraph)
      },

      drawGraph(result) {
        console.log(result);
        this.layoutData = {'links': result.links, "nodes": result.nodes};
        if (this.svg.select("g")) this.svg.select("g").remove();
        let zoom = d3.zoom().scaleExtent([1, 10]).on("zoom", () => {
          this.nodesLinksG.attr("transform", d3.event.transform);
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
          .append("g");
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
          .append("g");
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

          }).on("mouseout", (d) => {

        });
        this.$store.state.init_dim2 = Math.random();
        this.$store.state.timeupdated = Math.random();
        this.miniMap = d3.select("#miniMap").append("svg")
          .attr("width", $("#miniMap").width())
          .attr("height", $("#miniMap").height());
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
        this.allNodesG.attr("display", d => {
          if (typeList.includes(d.nodeType) && attributeList.includes(d.nodeAttribute)) {
            return "block";
          } else {
            this.allLinksG.attr("display", d => {
              if (d.source === d.id || d.target === d.id) return "none";
              else return "block";
            });
            return "none";
          }
        });
      }
    },
    computed: {
      ...mapGetters(['nodeTypeList_get', 'nodeAttrList_get']),
      testData: function () {
        return this.$store.state.testData
      },
      selectTime: function () {
        return this.$store.state.selectTime
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

      },
      'selectTime.start': function (val) {
        console.log(this.selectTime)
      }
    }
  };

</script>
<style lang="less" scoped>
  @import "./AppNetwork.less";

</style>
