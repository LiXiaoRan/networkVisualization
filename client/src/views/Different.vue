<template>
  <div id="Different">
    <div id="btnd">
      <button v-on:click="deteceAnomaly">点击显示异常情况</button>
      <button v-on:click="detectSimilarity">结构相似节点检测</button>
    </div>
    <div id="attr-compare-div"></div>
    <div class="svg-div">
      <svg id="view-svg"></svg>
    </div>
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
      currentNode: {}, //当前单选节点
      similarityDetc: false,
      minMaxList: [],
      allNumAttrList: [],
      allCulsterAttrList: [],
      numAttrNameList: [],
      culsterAttrList: [],
      infoSvg: null
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
        .range([0, 600]);
      // .range([screenWidth / 2 - width / 2, screenWidth / 2]);
      // .range([screenWidth / 2 - width / 2, screenWidth / 2 + width / 2]);

      self.yScale = d3
        .scaleLinear()
        .domain(d3.extent(self.nodesData, d => d.y))
        .range([0, 600]);
      // .range([screenHeight / 2 - height / 2, screenHeight / 2]);/
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
          if (!self.similarityDetc) {
            if (self.currentNode.id != null) {
              d3.select("#" + self.currentNode.id).attr("fill", "#1DBDD2");
            }
            self.currentNode = d;
            d3.select("#" + self.currentNode.id).attr("fill", "#000");
            console.log(d);

            self.drawLeftInfo(d);
          } else {
            //绘制右侧信息面板
            self.drawRightInfo(d);
          }
        });

      d3.select("#view-svg").call(
        d3
          .zoom()
          .scaleExtent([1, 8])
          .on("zoom", zoomed)
      );
      function zoomed() {
        self.svg.attr("transform", d3.event.transform);
      }
      self.dataProcess();
      self.drawInfoSvgAxis();
    },

    /**
     * 绘制左侧对比信息坐标轴
     */
    drawInfoSvgAxis() {
      self.infoSvg = d3
        .select("#attr-compare-div")
        .append("svg")
        .attr("class", "infosvg")
        .attr("width", "400px")
        .attr("height", "790px");
      let xScale = d3
        .scaleBand()
        .domain(["当前节点", "对比节点"])
        .range([20, 380]);
      let xAxis = self.infoSvg
        .append("g")
        .attr("class", "xAixs")
        .attr("transform", "translate(0, 770)")
        .call(d3.axisBottom(xScale));
      // let yScale=d3.scaleBand().domain()
    },
    /**
     *绘制左侧信息面板
     */
    drawLeftInfo(node) {
      console.log(node.id);

      // if (!d3.select(".barChartSvgLeft").empty()) {
      //   d3.select(".barChartSvgLeft").remove();
      // }
      // let barChartSvgLeft = d3
      //   .select("#attr-curr")
      //   .append("svg")
      //   .attr("class", "barChartSvgLeft")
      //   .attr("width", "180px")
      //   .attr("height", "785px");
      // let barChartG = barChartSvgLeft.append("g");
      // let keyList = [];
      // let valueList = [];
      // for (let index = 0; index < node.attr_num_list.length; index++) {
      //   keyList.push(node.attr_num_list[index].key);
      //   valueList.push(node.attr_num_list[index].value);
      // }
      // let yScale = d3
      //   .scaleBand()
      //   .domain(keyList)
      //   .rangeRound([785, 0]);
      // console.log(yScale.bandwidth());
      // let xScale = d3
      //   .scaleLinear()
      //   .domain(valueList)
      //   .range([0, 180]);

      // barChartG
      //   .selectAll(".bar")
      //   .data(node.attr_num_list)
      //   .enter()
      //   .append("rect")
      //   .attr("x", 0)
      //   .attr("y", function(d) {
      //     return yScale(d.key);
      //   })
      //   .attr("height", yScale.bandwidth())
      //   .attr("width", function(d) {
      //     console.log("d.value= " + d.value);
      //     console.log("xScale(d.value)= " + xScale(d.value));
      //     return xScale(d.value);
      //   })
      //   .attr("fill", "#ff0");
    },
    /**
     * 绘制右侧信息面板
     */
    drawRightInfo(node) {
      console.log(node.attr_culster_list);
    },

    /**
     * 检测异常链接
     */
    deteceAnomaly() {
      console.log("检测异常链接函数");
      let paramsObj = {};
      let Url = "detect-anomaly-onflow";
      CommunicateWithServer("get", paramsObj, Url, this.highLiteAnomaly);
    },

    highLiteAnomaly(result) {
      let self = this;
      self.similarityDetc = false;
      // self.currentNode={};
      // 高亮异常节点
      console.log(result);
      // 先把所有节点变成默认颜色
      d3.selectAll("circle").attr("fill", "#1DBDD2");
      // 给异常节点设置为金色
      result.forEach(function(d) {
        d3.select("#" + d.id).attr("fill", "#FFD700");
      });
    },
    /**
     * 相似性检测
     */
    detectSimilarity() {
      let self = this;
      if (!self.isEmpty(self.currentNode)) {
        self.similarityDetc = true;
        let Url = "detect-similarity";
        let paramsObj = { nodeId: self.currentNode.id };
        CommunicateWithServer(
          "get",
          paramsObj,
          Url,
          self.highLiteSimilarityNode
        );
      } else {
        alert("请选择一个节点");
      }
    },
    highLiteSimilarityNode(result) {
      console.log("相似性节点的数据如下：");
      console.log(result);

      //先把所有节点变成默认颜色,除当前选中节点外
      d3.selectAll("circle").attr("fill", "#1DBDD2");
      d3.select("#" + this.currentNode.id).attr("fill", "#000");

      // 高亮相似性节点为红色
      result.forEach(function(d) {
        d3.select("#" + d.id).attr("fill", "#FF0000");
      });
    },
    /**
     * 绘制信息图
     */
    drawInfoBarChart(node) {
      if (d3.select("#attr-curr")) {
        d3.select("#attr-curr").remove();
      }
      let barChart_g = d3
        .select("#attr-curr")
        .append("g")
        .classed(".barChart_g");
    },
    isEmpty(value) {
      return Object.keys(value).length === 0;
    },
    /**
     * 数据处理
     */
    dataProcess() {
      let self = this;

      if (self.minMaxList.length == 0) {
        for (let i = 0; i < 30; i++) {
          self.allNumAttrList.push(new Array());
        }
        //获取30个类别的数值属性，存入30个匿名数组中，然后存入总的list中
        self.nodesData.forEach((node, index) => {
          for (let j = 0; j < node.attr_num_list.length; j++) {
            self.allNumAttrList[j].push(node.attr_num_list[j].value);
          }
        });

        console.log(self.allNumAttrList);
        //求所有类别数值属性的最大最小值
        self.allNumAttrList.forEach(element => {
          try {
            self.minMaxList.push(d3.extent(element));
          } catch (e) {
            console.log(e);
          }
        });

        console.log(self.minMaxList);

        //存储属性名字到list中
        self.nodesData[0].attr_num_list.forEach(element => {
          try {
            console.log(element.key);
          } catch (e) {
            console.log(e);
          }
        });
      }
    }
  }
};
</script>

<style lang="less" scoped>
#view-svg {
  width: 100%;
  height: 100%;
}

.svg-div {
  width: 800px;
  height: 800px;
  overflow: hidden;
  margin-left: 20px;
  display: inline-block;
}

#attr-compare-div {
  display: inline-block;
  width: 400px;
  height: 800px;
  margin-left: 10px;
  background-color: #fff;
  padding-top: 5px;
  padding-bottom: 5px;
}

.compare-div-inner {
  display: inline-block;
  padding: 5px;
  background-color: #fff;
  margin-left: 5px;
  width: 50%-2px;
  height: 100%;
}

button {
  margin: 10px;
}

#btnd {
  z-index: 10;
}
.nodes circle {
  stroke: #fff;
  stroke-width: 1.5px;
}

.barChartSvgLeft {
}
</style>
