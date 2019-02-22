<template>
  <div id="filter-panel">
    <app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
    <div class="filter1">
      <span class="filter-msg">节点类型</span>
      <div class="outer-div">
        <div v-for="item in nodeType" class="inner-div">
          <input
            type="checkbox"
            class="select-checkbox"
            :value="item.value"
            :checked="item.checked"
            @change="changeNodeType(item)"
          >
          <span class="checbok-span">{{item.name}}</span>
        </div>
      </div>
    </div>
    <div class="filter2">
      <div>
        <span class="filter-msg">致瘫级别</span>
        <div class="outer-div">
          <div v-for="item in palsyLevel" class="inner-div">
            <input
              type="checkbox"
              class="select-checkbox"
              :value="item.value"
              :checked="item.checked"
              @change="changePalsyLevel(item)"
            >
            <span class="checbok-span">{{item.name}}</span>
          </div>
        </div>
      </div>
      <div>
        <span class="filter-msg">控制级别</span>
        <div class="outer-div">
          <div v-for="item in controlLevel" class="inner-div">
            <input
              type="checkbox"
              class="select-checkbox"
              :value="item.value"
              :checked="item.checked"
              @change="changeControlLevel(item)"
            >
            <span class="checbok-span">{{item.name}}</span>
          </div>
        </div>
      </div>
      <!-- </br> -->
      <!-- <span class="filtermsg">控制级别</span> -->
    </div>
    <div class="filter-graph">
      <span class="filtermsg-0">节点数量</span>
      <span class="filtermsg-1">类型</span>
      <select class="filtermsg-2" v-model="selected">
        <option v-for="item in items" v-bind:value="item.value" :key="item.value">{{item.text}}</option>
      </select>
      <div id="svg-div">
        <svg id="barchart"></svg>
      </div>
    </div>
  </div>
</template>
<script type="text/javascript">
  import {mapState, mapGetters, mapMutations, mapActions} from "vuex";
  import AppTitle from "./AppTitle.vue";
  import "../../static/bootstrap.min.css";
  import "../../static/buttons.css";
  import "font-awesome/css/font-awesome.css";

  const d3 = require("d3");
  export default {
    data() {
      return {
        icon: "filter",
        msgs: "二级过滤器",
        span4: "致瘫",
        span5: "控制",
        span6: "正常",
        nodeType: [
          {value: 0, name: "主机", checked: true},
          {value: 1, name: "交换机", checked: true},
          {value: 2, name: "服务器", checked: true}
        ],
        palsyLevel: [
          {value: 4, name: "5级", checked: true},
          {value: 3, name: "4级", checked: true},
          {value: 2, name: "3级", checked: true},
          {value: 1, name: "2级", checked: true},
          {value: 0, name: "1级", checked: true}
        ],
        controlLevel: [
          {value: 4, name: "5级", checked: true},
          {value: 3, name: "4级", checked: true},
          {value: 2, name: "3级", checked: true},
          {value: 1, name: "2级", checked: true},
          {value: 0, name: "1级", checked: true}
        ],
        items: [
          {text: "总流量", value: "总流量"},
          {text: "流入量", value: "流入量"},
          {text: "流出量", value: "流出量"}
        ],
        selected: "总流量",
        FilterLayoutData: [],
        HistogramData: [],
        HistogramFlowInData: [],
        HistogramFlowOutData: []
      };
    },
    components: {AppTitle},
    methods: {
      ...mapActions([
        "modifyNodeTypeList_sync",
        "modifyPalsyList_sync",
        "modifyControlList_sync",
        "modifyBrushData_sync"
      ]),
      changeNodeType(item) {
        item.checked = !item.checked;
        let data = [];
        this.nodeType.forEach(d => {
          if (d.checked) data.push(d.value);
        });
        this.modifyNodeTypeList_sync({nodeTypeList: data});
      },
      changePalsyLevel(item) {
        item.checked = !item.checked;
        let data = [];
        this.palsyLevel.forEach(d => {
          if (d.checked) data.push(d.value);
        });
        this.modifyPalsyList_sync({palsyLevelList: data});
      },
      changeControlLevel(item) {
        item.checked = !item.checked;
        let data = [];
        this.controlLevel.forEach(d => {
          if (d.checked) data.push(d.value);
        });
        this.modifyControlList_sync({controlLevelList: data});
      },
      dataProcess(layoutData) {
        //处理当前布局原始数据
        let self = this;
        let maxFlow = -1;
        let minFlow = -1;
        let num = 0;//节点数目
        let nodes = [];
        nodes = layoutData.nodes;

        self.HistogramData = [];
        self.HistogramFlowInData = [];
        self.HistogramFlowOutData = [];


        if (self.selected == "总流量") {
          maxFlow = d3.max(nodes, d => {
            return d.flow
          });
          minFlow = d3.min(nodes, d => {
            return d.flow
          });
          let step = Math.ceil(maxFlow / 50);
          let item_attr = [];
          item_attr = d3.range(0, maxFlow, step);
          for (let index = 1; index < item_attr.length; index++) {
            num = 0;
            nodes.forEach(d => {
              if (d.flow > item_attr[index - 1] && d.flow <= item_attr[index]) {
                num++
              }
            })

            self.HistogramData.push([index, num])
          }
          this.drawHistogram(self.HistogramData, 50)
        }
        if (self.selected == "流入量") {
          // if(self.HistogramFlowInData!=null) self.HistogramFlowInData=[];
          maxFlow = d3.max(nodes, d => {
            return d.flow_in
          });
          minFlow = d3.min(nodes, d => {
            return d.flow_in
          });
          let step = Math.ceil(maxFlow / 50);
          let item_attr = [];
          item_attr = d3.range(0, maxFlow, step);
          console.log(item_attr);
          for (let index = 1; index < item_attr.length; index++) {
            num = 0;
            nodes.forEach(d => {
              if (d.flow_in > item_attr[index - 1] && d.flow_in <= item_attr[index]) {
                num++
              }
            })

            self.HistogramFlowInData.push([index, num])
          }
          this.drawHistogram(self.HistogramFlowInData, 50)
        }
        if (self.selected == "流出量") {
          maxFlow = d3.max(nodes, d => {
            return d.flow_out
          });
          minFlow = d3.min(nodes, d => {
            return d.flow_out
          });
          let step = Math.ceil(maxFlow / 50);
          let item_attr = [];
          item_attr = d3.range(0, maxFlow, step);
          console.log(item_attr);
          for (let index = 1; index < item_attr.length; index++) {
            num = 0;
            nodes.forEach(d => {
              if (d.flow_out > item_attr[index - 1] && d.flow_out <= item_attr[index]) {
                num++
              }
            })

            self.HistogramFlowOutData.push([index, num])
          }
          this.drawHistogram(self.HistogramFlowOutData, 50)
        }
      },
      drawHistogram(randomData, randomDataLength) {
        //绘制直方图
        if (d3.select("#barchart").select('g')) d3.select("#barchart").select('g').remove();
        let self = this;
        let width = d3.select("#svg-div").style("width").split("px")[0];
        let height = d3.select("#svg-div").style("height").split("px")[0];
        let brushleft = 0;
        let brushright = 0;

        let padding = {top: 0, left: 30, bottom: 10, right: 10};

        let group = d3.select("#barchart")
          .attr("width", width)
          .attr("height", height)
          .append("g");


        let xScale = d3.scaleBand()
          .rangeRound([0, width - padding.left - padding.right], 0.1)
          .domain(randomData.map(function (d) {
            return d[0];
          }));

        let y = d3.scaleLinear()
          .domain([d3.max(randomData, function (d) {
            return d[1];
          }), 0])
          .range([0, height - padding.top - padding.bottom]);

        let x = d3.scaleLinear()
          .domain([0, randomDataLength])
          .range([0, width - padding.left - padding.right]);

        let brush = d3.brushX()
          .extent([[0, 0], [width - padding.left - padding.right, height - padding.top - padding.bottom]])
          .on("end", function () {
            let range = d3.brushSelection(this).map(x.invert);
            brushleft = Math.round(range[0]);
            brushright = Math.round(range[1]);
            self.decodeBrushData(randomData.slice(brushleft, brushright))
          });


        let svg = group.append("g")
          .attr("id", "yaxis")
          .attr("transform", "translate(" + padding.left + "," + padding.top + ")")
          .call(d3.axisLeft().scale(y).ticks(3));

        d3.select("#yaxis")
          .select("path")
          .remove();

        d3.select("#yaxis")
          .selectAll(".tick")
          .select("line")
          .remove();

        d3.select("#yaxis")
          .selectAll(".tick")
          .selectAll("text")
          .attr("transform", "translate(0, 5)")
          .attr("fill", "#95a5a6");

        group.append("g")
          .attr("transform", "translate(" + padding.left + "," + (padding.top + padding.bottom) + ")")
          .selectAll(".bar")
          .data(randomData)
          .enter()
          .append("rect")
          .attr("width", xScale.bandwidth())
          .attr("height", function (d, i) {
            return ((d[1] * (height - padding.top - padding.bottom)) /
              d3.max(randomData, function (d) {
                return d[1];
              })
            );
          })
          .attr("x", function (d) {
            return x(d[0]);
          })
          .attr("y", function (d, i) {
            return (
              (height - padding.top - padding.bottom) - (d[1] * (height - padding.top - padding.bottom)) /
              d3.max(randomData, function (d) {
                return d[1];
              })
            );
          })
          .style("fill", "rgb(31,165,218)")
          .style("stroke", "rgb(48,50,67)");

        group.append("g")
          .attr("class", "brush")
          .attr("transform", "translate(" + padding.left + "," + (padding.top + padding.bottom) + ")")
          .call(brush);
      },
      decodeBrushData(data) {
        //解构刷取的数据
        let self = this;
        let maxFlow = -1;
        let minFlow = -1;
        let brushNodes = [];
        let nodes = [];
        nodes = self.FilterLayoutData.nodes;
        if (self.selected == "总流量") {
          maxFlow = d3.max(nodes, d => {
            return d.flow
          });
          let step = Math.ceil(maxFlow / 50);
          let item_attr = [];
          item_attr = d3.range(0, maxFlow, step);

          data.forEach(d => {
            for (let index = 1; index < item_attr.length; index++) {
              if (d[0] == index) {
                nodes.forEach(d => {
                  if (d.flow > item_attr[index - 1] && d.flow <= item_attr[index]) {
                    brushNodes.push(d)
                  }
                })
              }

            }
          });
        }
        if (self.selected == "流入量") {
          maxFlow = d3.max(nodes, d => {
            return d.flow_in
          });
          let step = Math.ceil(maxFlow / 50);
          let item_attr = [];
          item_attr = d3.range(0, maxFlow, step);

          data.forEach(d => {
            for (let index = 1; index < item_attr.length; index++) {
              if (d[0] == index) {
                nodes.forEach(d => {
                  if (d.flow_in > item_attr[index - 1] && d.flow_in <= item_attr[index]) {
                    brushNodes.push(d)
                  }
                })
              }

            }
          });
        }
        if (self.selected == "流出量") {
          maxFlow = d3.max(nodes, d => {
            return d.flow_out
          });
          let step = Math.ceil(maxFlow / 50);
          let item_attr = [];
          item_attr = d3.range(0, maxFlow, step);

          data.forEach(d => {
            for (let index = 1; index < item_attr.length; index++) {
              if (d[0] == index) {
                nodes.forEach(d => {
                  if (d.flow_out > item_attr[index - 1] && d.flow_out <= item_attr[index]) {
                    brushNodes.push(d)
                  }
                })
              }

            }
          });
        }
        //将解构完成的brushNodes发送到AppNetwork
        // console.log(brushNodes);
        self.modifyBrushData_sync({brushData: brushNodes})
      }
    },
    mounted() {
    },
    computed: {
      ...mapGetters(["layoutData_get"])
    },
    watch: {
      layoutData_get: function (data) {
        //这里获取到当前布局的数据，然后重新绘制直方图
        console.log(data);
        this.FilterLayoutData = data;
        this.dataProcess(data);
      },
      selected: function (data) {

        if (data == '总流量') {
          if (typeof this.HistogramData.increase_num !== 'undefined' && this.HistogramData.increase_num.length > 0) {
            //如果总流量数组不为空，绘制总流量直方图
            this.drawHistogram(this.HistogramData, 50)
          } else {
            this.dataProcess(this.FilterLayoutData)
          }
        }
        if (data == '流入量') {
          if (typeof this.HistogramFlowInData.increase_num !== 'undefined' && this.HistogramFlowInData.increase_num.length > 0) {
            console.log('流入量不为空');

            this.drawHistogram(this.HistogramFlowInData, 50)
          } else {
            this.dataProcess(this.FilterLayoutData)
          }
        }
        if (data == '流出量') {
          if (typeof this.HistogramFlowOutData.increase_num !== 'undefined' && this.HistogramFlowOutData.increase_num.length > 0) {
            this.drawHistogram(this.HistogramFlowOutData, 50)
          } else {
            this.dataProcess(this.FilterLayoutData)
          }
        }
        console.log(data);
      }
    }
  };
</script>
<style lang="less" scoped>
  @import "AppTimeLine.less";
  @import "./AppFilter.less";
</style>
