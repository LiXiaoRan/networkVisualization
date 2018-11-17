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
const d3 = require("d3");

export default {
  data() {
    return {
      icon: '<i class="fa fa-joomla" aria-hidden="true"></i>',
      msgs: "后台布局",
      now_layout_type: null
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
          graphLayOut('random')
          break;
        case "椭圆布局":
          self.now_layout_type = "circle";
          graphLayOut('circle')
          break;
        case "graphopt布局":
          self.now_layout_type = "graphopt";
          graphLayOut('graphopt')
          break;
        case "多元尺度布局":
          self.now_layout_type = "mds";
          graphLayOut('mds')
          break;
        case "网格布局":
          self.now_layout_type = "grid";
          graphLayOut('grid')
          break;
        case "大图布局":
          self.now_layout_type = "lgl";
          graphLayOut('lgl')
          break;
        case "分布式递归布局":
          self.now_layout_type = "drl";
          graphLayOut('drl')
          break;
        case "层次化布局":
          self.now_layout_type = "sugiyama";
          graphLayOut('sugiyama')
          break;
        case "环状RT树布局":
          self.now_layout_type = "rt_circular";
          graphLayOut('rt_circular')
          break;
        default:
          break;
      }
    });
    document.getElementById("layContainer").appendChild(gui.domElement);

    var graphLayOut = function(type){
      self.getDataWithParams({
      where: {
        val: {
          start: 0,
          end: 1000000000
        }
      },
      limit: 50000,
      layout_type: type
    });
    }
    graphLayOut('random')
  },
  methods: {
    getDataWithParams(paramsObj) {
      console.log("getDataWithParams 函数");
      let self = this;
      let Url = "cal-layout";
      let formData = new URLSearchParams();
      formData.append("params", JSON.stringify(paramsObj));
      this.$api.get(Url, formData, data => {
        console.log(data);
        this.drawGraph(data);
      });
    },
    drawGraph(res) {
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
          return Math.ceil(Math.random()*10)
        })
        .attr("stroke", function(d) {
          return "#fff";
        })
        .attr("stroke-width", function(d) {
          return "1";
        })
        .attr('fill','#eee')
        .attr('opacity',0.6)


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
    }
  },
  watch: {}
};
</script>

 
<style lang="less" scoped>
@import "./AppLayout.less";
</style>
