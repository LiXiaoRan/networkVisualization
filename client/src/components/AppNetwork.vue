<template>
  <div id='layout-panel'>
    <app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
    <div class='view'>
      <svg class='view-svg'>
      </svg>
      <div id="layContainer"></div>
    </div>
  </div>
</template>
<script>
import AppTitle from "./AppTitle.vue";
import * as dat from "dat.gui";
import qs from 'qs'
const d3 = require("d3");

export default {
  data() {
    return {
      icon: 'joomla', //需要再main.js 中注册
      msgs: "多层网络",
      now_layout_type: null,
      layout_data: {},
      limit: 5000,
      start: 0,
      end: 1000000000
    };
  },
  components: { AppTitle },
  mounted() {
    let self = this;
    self.now_layout_type = "random";
    // self.getLayout();
    const gui = new dat.GUI();
    let obj = {
      布局: "随机布局"
    };
    var layout_text = gui.add(obj, "布局", [
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
    layout_text.onChange(function(value) {
      switch (value) {
        case "随机布局":
          self.now_layout_type = "random";
          SwitchGraph("random");
          break;
        case "椭圆布局":
          self.now_layout_type = "circle";
          SwitchGraph("circle");
          break;
        case "graphopt布局":
          self.now_layout_type = "graphopt";
          SwitchGraph("graphopt");
          break;
        case "多元尺度布局":
          self.now_layout_type = "mds";
          SwitchGraph("mds");
          break;
        case "网格布局":
          self.now_layout_type = "grid";
          SwitchGraph("grid");
          break;
        case "大图布局":
          self.now_layout_type = "lgl";
          SwitchGraph("lgl");
          break;
        case "分布式递归布局":
          self.now_layout_type = "drl";
          SwitchGraph("drl");
          break;
        case "层次化布局":
          self.now_layout_type = "sugiyama";
          SwitchGraph("sugiyama");
          break;
        case "环状RT树布局":
          self.now_layout_type = "rt_circular";
          SwitchGraph("rt_circular");
          break;
        default:
          break;
      }
    });
    document.getElementById("layContainer").appendChild(gui.domElement);

    var graphLayOut = function(type) {
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
    graphLayOut("random");

    var SwitchGraph = function(type) {
      self.drawSwitchGraph(type);
    };
  },
  methods: {
    drawSwitchGraph(type) {
      let self = this;

      let paramsObj = {
        layoutData: JSON.stringify(self.layout_data),
        layout_type: type
      };
      let Url = "get-layout-data";
      CommunicateWithServer('post', paramsObj, Url, this.drawGraph)
    },
    getDataWithParams(paramsObj) {
      CommunicateWithServer('get', paramsObj, 'cal-layout', this.drawGraph)
    },
    drawGraph(res) {
      console.log(res)
      this.layout_data = {'links': res.links, nodes: res.nodes}
      let startTime = +new Date();
      let padding = { top: 50, bottom: 50, left: 70, right: 70 };
      let svg = d3.select(".view-svg");
      let width = parseFloat(
        svg.attr("width") === null ? svg.style("width") : svg.attr("width")
      );
      let height = parseFloat(
        svg.attr("height") === null ? svg.style("height") : svg.attr("height")
      );
      if (svg.select("g")) svg.select("g").remove();
      let g = svg.append("g");

      let xScale = d3
        .scaleLinear()
        .domain(
          d3.extent(res.nodes, function(d) {
            return d.x;
          })
        )
        .range([padding.left, width - padding.right]);
      let yScale = d3
        .scaleLinear()
        .domain(
          d3.extent(res.nodes, function(d) {
            return d.y;
          })
        )
        .range([padding.top, height - padding.bottom]);

      g.append("g")
        .selectAll("circle")
        .data(res.nodes)
        .enter()
        .append("circle")
        .attr("cx", function(d) {
          return xScale(d.x);
        })
        .attr("cy", function(d) {
          return yScale(d.y);
        })
        .attr("r", function(d) {
          return Math.ceil(Math.random() * 10);
        })
        .attr("stroke", function(d) {
          return "#fff";
        })
        .attr("stroke-width", function(d) {
          return "1";
        })
        .attr("fill", "#eee")
        .attr("opacity", 0.6);

      g.append("g")
        .selectAll("line")
        .data(res.links)
        .enter()
        .append("line")
        .attr("stroke", function(d) {
          return "#fff";
        })
        .attr("stroke-width", function(d) {
          return "1";
        })
        .attr("x1", function(d) {
          return xScale(d.x1);
        })
        .attr("y1", function(d) {
          return yScale(d.y1);
        })
        .attr("x2", function(d) {
          return xScale(d.x2);
        })
        .attr("y2", function(d) {
          return yScale(d.y2);
        });

      let endTime = +new Date();
      console.log("渲染时间 :" + (endTime - startTime) / 1000);
	  this.$store.state.init_dim2 = Math.random();
    this.$store.state.timeupdated = Math.random();
    }
  },
  computed: {
    testData: function() {
      return this.$store.state.testData
    }
  },
  watch: {
    testData: function(newVal, oldVal) {
      console.log('communnication', newVal)
    }
  }
};

</script>
<style lang="less" scoped>
@import "./AppNetwork.less";

</style>
