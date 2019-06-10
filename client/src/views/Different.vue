<template>
  <div id="Different">
    <div id="btnd">
      <button v-on:click="deteceAnomaly">点击显示异常情况</button>
      <button v-on:click="detectSimilarity">结构相似节点检测</button>
      <button v-on:click="fixState=!fixState">手动补边</button>
      <button v-on:click="finishFix">完成补边</button>
    </div>
    <div id="attr-compare-div"></div>
    <div class="svg-div">
      <svg id="view-svg"></svg>
    </div>
    <div id="notice_div">
      <p id="notice_text" v-show="fixState">
        已经开启了手动补边模式
        <br>
      </p>
    </div>
    <div id="table-div" class="table-responsive">
      <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">id</th>
            <th scope="col">flow</th>
            <th scope="col">flow_in</th>
            <th scope="col">flow_out</th>
            <th scope="col" v-for="n in 30">num_{{n}}</th>
            <th scope="col" v-for="n in 20">cluster_{{n}}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item,index) in simNodesDataList">
            <th scope="row">{{index}}</th>
            <td>{{item.id}}</td>
            <td>{{item.flow}}</td>
            <td>{{item.flow_in}}</td>
            <td>{{item.flow_out}}</td>
            <td v-for="attr_num in item.attr_num_list">{{attr_num.value}}</td>
            <td v-for="attr_cluster in item.attr_culster_list">{{attr_cluster.value}}</td>
          </tr>
        </tbody>
      </table>
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
      simNodesDataList: [],

      xScale: null, //绘制布局的x比例尺

      yScale: null, //绘制布局y轴的比例尺,
      yAxisScale: null, //绘制坐标轴y轴的比例尺,需要多次重绘y轴，所以要保存

      currentNode: {}, //当前单选节点

      similarityDetc: false, //是否开启对比模式
      fixState: false, //是否处于补边状态

      minMaxList: [], //所有数值类属性的最大值最小值 [min,max]
      allNumAttrList: [], //存储所有30个类别的数值类属性，有30个list
      allCulsterAttrList: [], //存储所有20个类别的枚举类属性，有20个list
      numAttrNameList: [], //存储属性名字列表，用来绘制坐标轴Y轴
      culsterAttrList: [],
      infoSvg: null, //信息对比的svg
      yScaleBandWidth: 0, //每一个bar 的高度
      infoSvgXScaleList: [], //每一个类数值类信息的横向比例尺，有30个
      InfoSvgHeight: 770, //对比区域svg高度
      InfoSvgWidth: 380, //对比区域svg宽度
      // yScale:0,//需要多次重绘y轴，所以要保存
      colorScale: null, //20个d3颜色列表颜色

      firstNode: null, //补边状态点击的第一个节点
      secondNode: null //补边状态点击的第二个节点
    };
  },
  mounted() {
    let self = this;
    // self.colorScale=d3.scaleOrdinal(d3.schemeCategory10)
    self.colorScale = d3
      .scaleOrdinal()
      .range([
        "#2578B2",
        "#AFC7E7",
        "#FD7D26",
        "#FEBA7D",
        "#32A034",
        "#9ADF8E",
        "#D4212E",
        "#FD9798",
        "#9367BB",
        "#C4B0D4",
        "#8B554C",
        "#C39C95",
        "#E176C1",
        "#F6B5D1",
        "#7F7F7F",
        "#C7C7C7",
        "#BCBD34",
        "#DBDB91",
        "#28BECD",
        "#A0DAE4",
        "#FFFF9F"
      ]);

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
        .attr("class", "abclink")
        .attr("x1", d => self.xScale(d.x1))
        .attr("y1", d => self.yScale(d.y1))
        .attr("x2", d => self.xScale(d.x2))
        .attr("y2", d => self.yScale(d.y2))
        .attr("stroke", "#BCBCBC")
        .attr("stroke-width", 0.5);

      let node = self.svg
        .append("g")
        .attr("class", "nodes")
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
          if (!self.fixState) {
            //如果没有开启补边模式
            console.log("没有开启补边模式");
            if (!self.similarityDetc) {
              if (self.currentNode.id != null) {
                d3.select("#" + self.currentNode.id).attr("fill", "#1DBDD2");
              }
              self.currentNode = d;
              d3.select("#" + self.currentNode.id).attr("fill", "#000");
              console.log(d);

              try {
                self.drawLeftInfo(d);
              } catch (e) {
                console.log(e);
              }
            } else {
              //绘制右侧信息面板
              try {
                self.drawRightInfo(d);
              } catch (e) {
                console.log(e);
              }
            }
          } else {
            //开启了补边模式
            console.log("处于补边状态");

            if (self.firstNode != null && self.secondNode != null) {
              if (self.firstNode.id == self.secondNode.id) {
                self.secondNode = null;
              } else {
                self.firstNode = d;
              }
            }
            if (self.firstNode == null) {
              self.firstNode = d;
            } else {
              self.secondNode = d;
            }

            let str = "已经开启了手动补边模式";
            let source = self.firstNode ? self.firstNode.id : "null";
            let target = self.secondNode ? self.secondNode.id : "null";
            str = str + "<br> source: " + source + " <br>taregt: " + target;
            let ptext = document.getElementById("notice_text");
            ptext.innerHTML = str;

            //设置补边状态下的选中节点高亮
            // d3.selectAll("circle").attr("fill", function (d) {
            //   if (d.id!=self.currentNode.id) {

            //   }
            // });

            // if (self.firstNode!=null) {
            //   d3.select("#"+self.firstNode.id).attr("fill","#9267B9");
            // }
            // if (self.secondNode!=null) {
            //   d3.select("#"+self.secondNode.id).attr("fill","#9267B9");
            // }
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
     * 绘制对比信息坐标轴
     */
    drawInfoSvgAxis() {
      let self = this;
      self.infoSvg = d3
        .select("#attr-compare-div")
        .append("svg")
        .attr("class", "infosvg")
        .attr("width", "400px")
        .attr("height", "790px");
      let xScale = d3
        .scaleBand()
        .domain(["当前节点", "对比节点"])
        .range([20, self.InfoSvgWidth]);
      let xAxis = self.infoSvg
        .append("g")
        .attr("class", "xAixs")
        .attr("transform", "translate(0, " + self.InfoSvgHeight + ")")
        .call(d3.axisBottom(xScale));
      let yNumNameList = [];
      for (let index = 1; index <= 30; index++) {
        yNumNameList.push("num" + index);
      }
      for (let index = 1; index <= 20; index++) {
        yNumNameList.push("culster" + index);
      }
      console.log(yNumNameList);
      self.yAxisScale = d3
        .scaleBand()
        .domain(yNumNameList)
        .range([0, self.InfoSvgHeight]);
      let yAxis = self.infoSvg
        .append("g")
        .attr("class", "yAixs")
        .attr("transform", "translate(" + self.InfoSvgWidth * 0.5 + ",0)")
        .call(d3.axisLeft(self.yAxisScale));
      self.yScaleBandWidth = self.yAxisScale.bandwidth();
      for (let index = 0; index < self.minMaxList.length; index++) {
        self.infoSvgXScaleList.push(
          d3
            .scaleLinear()
            .domain(self.minMaxList[index])
            .range([0, 0.5 * self.InfoSvgWidth])
        );
      }
    },
    /**
     *绘制左侧信息面板
     */
    drawLeftInfo(node) {
      let self = this;
      console.log(node.id);

      if (!d3.select(".barChartSvgLeft").empty()) {
        d3.select(".barChartSvgLeft").remove();
      }
      let barChartSvgLeft = d3
        .select(".infosvg")
        .append("g")
        .attr("class", "barChartSvgLeft");
      let currAllData = [];
      currAllData.push(...node.attr_num_list);
      currAllData.push(...node.attr_culster_list);

      //绘制条形图
      let bar = barChartSvgLeft
        .selectAll(".bar_left")
        .data(currAllData)
        .enter()
        .append("rect");
      bar
        .attr("x", function(d, i) {
          if (i <= 29) {
            return 0.5 * self.InfoSvgWidth - self.infoSvgXScaleList[i](d.value);
          } else {
            return 0;
          }
        })
        .attr("y", function(d, i) {
          return i * self.yScaleBandWidth;
        })
        .attr("width", function(d, i) {
          if (i <= 29) return self.infoSvgXScaleList[i](d.value);
          else return self.InfoSvgWidth / 2;
        })
        .attr("height", function(d, i) {
          return self.yScaleBandWidth - 2;
        })
        .attr("fill", function(d, i) {
          if (i <= 29) return "steelblue";
          else {
            // console.log(self.colorScale(d.value));
            return self.colorScale(d.value);
          }
        });

      if (!d3.selectAll(".yAixs").empty()) {
        d3.selectAll(".yAixs").remove();
      }
      //需要重新绘制Y轴，这样就不会被条形图遮挡
      let yAxis = self.infoSvg
        .append("g")
        .attr("class", "yAixs")
        .attr("transform", "translate(" + self.InfoSvgWidth * 0.5 + ",0)")
        .call(d3.axisLeft(self.yAxisScale));

      //设置条形图文字
      barChartSvgLeft
        .selectAll(".bar-text")
        .data(currAllData)
        .enter()
        .append("text")
        .text(function(d) {
          return d.value;
        })
        .attr("x", function(d, i) {
          // console.log("x is "+0.5*self.InfoSvgWidth-self.infoSvgXScaleList[i](d.value));
          if (i <= 29)
            return 0.5 * self.InfoSvgWidth - self.infoSvgXScaleList[i](d.value);
          else return 0;
        })
        .attr("y", function(d, i) {
          // console.log("y is "+(i*self.yScaleBandWidth-self.yScaleBandWidth/2));
          return i * self.yScaleBandWidth + self.yScaleBandWidth / 2 + 4;
        })
        .attr("fill", "white");
    },
    /**
     * 绘制右侧信息面板
     */
    drawRightInfo(node) {
      console.log("绘制右侧信息板");
      let self = this;

      if (!d3.select(".barChartSvgRight").empty()) {
        d3.select(".barChartSvgRight").remove();
      }
      let barChartSvgRight = d3
        .select(".infosvg")
        .append("g")
        .attr("class", "barChartSvgRight");

      let currAllData = [];
      currAllData.push(...node.attr_num_list);
      currAllData.push(...node.attr_culster_list);

      //绘制条形图
      let bar = barChartSvgRight
        .selectAll(".bar_right")
        .data(currAllData)
        .enter()
        .append("rect");
      bar
        .attr("x", function(d, i) {
          // if(i<=29)
          return 0.5 * self.InfoSvgWidth;
        })
        .attr("y", function(d, i) {
          return i * self.yScaleBandWidth;
        })
        .attr("width", function(d, i) {
          if (i <= 29) return self.infoSvgXScaleList[i](d.value);
          else return 0.5 * self.InfoSvgWidth;
        })
        .attr("height", function(d, i) {
          return self.yScaleBandWidth - 2;
        })
        .attr("fill", function(d, i) {
          if (i <= 29) {
            return "steelblue";
          } else {
            return self.colorScale(d.value);
          }
        });

      if (!d3.selectAll(".yAixs").empty()) {
        d3.selectAll(".yAixs").remove();
      }
      //需要重新绘制Y轴，这样就不会被条形图遮挡
      let yAxis = self.infoSvg
        .append("g")
        .attr("class", "yAixs")
        .attr("transform", "translate(" + self.InfoSvgWidth * 0.5 + ",0)")
        .call(d3.axisLeft(self.yAxisScale));

      //设置条形图文字
      barChartSvgRight
        .selectAll(".bar-text")
        .data(currAllData)
        .enter()
        .append("text")
        .text(function(d) {
          return d.value;
        })
        .attr("x", function(d, i) {
          // console.log("x is "+0.5*self.InfoSvgWidth+self.infoSvgXScaleList[i](d.value));
          if (i <= 29)
            return (
              0.5 * self.InfoSvgWidth +
              self.infoSvgXScaleList[i](d.value) -
              this.getBBox().width
            );
          else return self.InfoSvgWidth - this.getBBox().width;
        })
        .attr("y", function(d, i) {
          // console.log("y is "+(i*self.yScaleBandWidth-self.yScaleBandWidth/2));
          return i * self.yScaleBandWidth + self.yScaleBandWidth / 2 + 4;
        })
        .attr("fill", "white");
    },

    /**
     * 检测异常链接
     */
    deteceAnomaly() {
      let self = this;
      //清空补边状态
      self.fixState = false;
      self.firstNode = null;
      self.secondNode = null;

      console.log("检测异常链接函数");
      let paramsObj = {};
      let Url = "detect-anomaly-onflow";
      CommunicateWithServer("get", paramsObj, Url, this.highLiteAnomaly);
    },
    /**
     * 高亮异常节点
     */
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
    /**
     * 高亮top10相似性节点
     */
    highLiteSimilarityNode(result) {
      let self = this;
      let tempList = [];
      self.simNodesDataList = [];
      // let resultIdList=[]
      console.log("相似性节点的数据如下：");
      console.log(result);

      //先把所有节点变成默认颜色,除当前选中节点外
      d3.selectAll("circle").attr("fill", "#1DBDD2");
      d3.select("#" + this.currentNode.id).attr("fill", "#000");

      // 高亮相似性节点为红色
      result.forEach(function(d) {
        if (d.id != self.currentNode.id) {
          d3.select("#" + d.id).attr("fill", "#FF0000");
        }
        // resultIdList.push(d.id)
      });

      self.nodesData.forEach(node => {
        result.forEach(function(d) {
          if (d.id == node.id && d.id!=self.currentNode.id ) {
            self.simNodesDataList.push(node);
          }
        });
      });
      console.log("self.simNodesDataList is ", self.simNodesDataList);
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
      }
    },
    /**
     * 手动补边
     */
    fixEdge() {
      let self = this;
      self.fixState = true;

      // self.linksData.push({
      //   flow:100,
      //   source:'',
      //   target:'',
      //   times:'3',
      //   x1:1,
      //   x2:2,
      //   y1:1,
      //   y2:2
      // })
    },
    /**
     * 完成补边
     */
    finishFix() {
      let self = this;
      if (self.fixState) {
        if (self.firstNode == null || self.secondNode == null) {
          alert("请至少选择两个节点");
        } else {
          console.log(self.firstNode, self.secondNode);
          let newLink = {
            x1: self.firstNode.x,
            x2: self.secondNode.x,
            y1: self.firstNode.y,
            y2: self.secondNode.y,
            flow: (self.secondNode.flow + self.firstNode.flow) / 2,
            source: self.firstNode.id,
            target: self.secondNode.id,
            times: 1
          };
          console.log("新添加的边的属性：", newLink);
          self.linksData.push(newLink);
          // if(!d3.select(".links").empty()){
          //   d3.select(".links").remove;
          // }

          // d3.select("#view-svg")
          // .append("g")
          // .attr("class", "links")
          d3.select(".links")
            // .selectAll("line")
            // .data(self.linksData)
            // .enter()
            .append("line")
            .attr("x1", self.xScale(newLink.x1))
            .attr("y1", self.yScale(newLink.y1))
            .attr("x2", self.xScale(newLink.x2))
            .attr("y2", self.yScale(newLink.y2))
            .attr("class", "abclink newline")
            .attr("stroke", "#BCBCBC")
            .attr("stroke-width", 0.5);

          console.log("补边完成之后：");
          //清空目前选择的效果
          self.firstNode = null;
          self.secondNode = null;
          console.log(d3.selectAll(".links"));
          console.log(self.linksData);
        }
      } else {
        alert('请在"手动补边"模式下操作');
      }
    }
  },
  watch: {}
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

#notice_div {
  display: inline-block;
  width: 400px;
  height: 800px;
  padding: 1%;
  margin-left: 20px;
  border: 1px dashed gray;
  border-radius: 20px;
  position: absolute;
}

#notice_text {
  // width: 100%;
  // height: 100%;
  display: inline-block;
  position: absolute;
  left: 29%;
  top: 50%-5;
}

#table-div {
  margin-top: 50px;
  width: 100%;
  height: auto;
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
