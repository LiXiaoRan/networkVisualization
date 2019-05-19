<template>
  <div id="Different">
    <button v-on:click="deteceAnomaly">点击显示异常情况</button>
    <button v-on:click="detectSimilarity">结构详细节点检测</button>

    <svg id="view-svg"></svg>
  </div>
</template>
<script>
import * as d3 from "d3";

export default {
  data() {
    return {
      layoutData: {},
      linksData: [],
      nodesData: [],
      xScale: null,
      yScale: null,
      currentNode: {} //当前单选节点
    };
  },
  mounted() {
    let self = this;
    self.getGraphData();
  },
  methods: {
    getGraphData() {
      let self = this;
      let paramsObj = {};
      let Url = "get-anomaly-layout-data";
      CommunicateWithServer("get", paramsObj, Url, self.drawGraph);
    },

    drawGraph(result) {
      let self = this;
      self.layoutData = result;
      // console.info("different回调函数被调用了");

      self.svg = d3.select("#view-svg");
      let width = parseFloat(self.svg.style("width"));
      let height = parseFloat(self.svg.style("height"));

      // 浏览器可视部分宽高
      let screenWidth = document.documentElement.clientWidth;
      let screenHeight = document.documentElement.clientHeight;

      console.log("width is " + width + " height is " + height);
      self.layoutData.links.forEach(d => self.linksData.push(d));
      self.layoutData.nodes.forEach(d => self.nodesData.push(d));

      self.xScale = d3
        .scaleLinear()
        .domain(d3.extent(self.nodesData, d => d.x))
        .range([screenWidth / 2 - width / 2, screenWidth / 2]);
      // .range([screenWidth / 2 - width / 2, screenWidth / 2 + width / 2]);

      self.yScale = d3
        .scaleLinear()
        .domain(d3.extent(self.nodesData, d => d.y))
        .range([screenHeight / 2 - height / 2, screenHeight / 2]);
      // .range([screenHeight / 2 - height / 2, screenHeight / 2 + height / 2]);

      console.log(self.nodesData);
      console.log(self.linksData);

      let link = self.svg
        .append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(self.linksData)
        .enter()
        .append("line")
        .attr("x1", d => self.xScale(d.x1))
        .attr("y1", d => self.yScale(d.y1))
        .attr("x2", d => self.xScale(d.x2))
        .attr("y2", d => self.yScale(d.y2))
        .attr("stroke", "#BCBCBC")
        .attr("stroke-width", 0.5);

      let node = self.svg
        .append("g")
        .attr("class", "nodes")
        // .attr("width", width)
        // .attr("height", height)
        .selectAll("g")
        .data(self.nodesData)
        .enter()
        .append("g");

      let circles = node
        .append("circle")
        .attr("cx", d => self.xScale(d.x))
        .attr("cy", d => self.yScale(d.y))
        .attr("id", d => d.id)
        .attr("r", 2)
        .attr("fill", function(d) {
          return "#1DBDD2";
        })
        .on("click", function(d) {
          if(self.currentNode.id!=null){
            d3.select("#" + self.currentNode.id).attr("fill", "#1DBDD2");
          }
          self.currentNode = d;
          d3.select("#" + self.currentNode.id).attr("fill", "#000");
          console.log(d.id);
        });
    },
    deteceAnomaly() {
      // 检测异常链接
      console.log("检测异常链接函数");
      // let paramsObj = {AnomalyLayoutDataResult:{'nodes':this.nodesData,'links':this.linksData}};
      // let paramsObj = {AnomalyLayoutDataResult:this.layoutData};
      let paramsObj = {};
      let Url = "detect-anomaly-onflow";
      CommunicateWithServer("get", paramsObj, Url, this.highLiteAnomaly);
    },
    highLiteAnomaly(result) {
      // 高亮异常节点
      console.log(result);
      // 先把所有节点变成默认颜色
      d3.selectAll("circle").attr("fill", "#1DBDD2");
      // 给异常节点设置为金色
      result.forEach(function(d) {
        d3.select("#" + d.id).attr("fill", "#FFD700");
      });
    },
    detectSimilarity() {
      //相似性检测
      let self = this;
      if (self.currentNode != null) {
        let Url = "detect-similarity";
        let paramsObj = { nodeId: self.currentNode.id };
        CommunicateWithServer(
          "get",
          paramsObj,
          Url,
          self.highLiteSimilarityNode
        );
      } else {
        alert('请选择一个节点');
      }
    },
    highLiteSimilarityNode(result) {
      //先把所有节点变成默认颜色,除当前选中节点外
      d3.selectAll("circle").attr("fill", function(d) {
        if (d.id != self.currentNode.id) {
          return "#1DBDD2";
        }
      });
      // 高亮相似性节点为红色
      result.forEach(function(d) {
        d3.select("#" + d.id).attr("fill", "#FF0000");
      });
    }
  }
};
</script>

<style lang="less" scoped>
svg {
  width: 1000px;
  height: 700px;
  position: fixed;
  top: 50%;
  left: 50%;
  margin-left: -600px;
  margin-top: -350px;
}

button {
  margin: 10px;
}

.nodes circle {
  stroke: #fff;
  stroke-width: 1.5px;
}
</style>
