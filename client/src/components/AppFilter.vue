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
        selected: "总流量"
      };
    },
    components: {AppTitle},
    methods: {
      ...mapActions([
        "modifyNodeTypeList_sync",
        "modifyPalsyList_sync",
        "modifyControlList_sync"
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
        let maxFlow=-1;
        let minFlow=-1;
        let num=0;//节点数目
        let nodes=[];
        let HistogramData=[]
        nodes=layoutData.nodes;
        maxFlow=d3.max(nodes,d=> {return d.flow});
        minFlow=d3.min(nodes,d=> {return d.flow});
        let step=Math.ceil(maxFlow/50);
        let item_attr=[];
        item_attr=d3.range(0,maxFlow,step);
        console.log(item_attr);
        for (let index = 1; index < item_attr.length; index++) {
          num=0;
          nodes.forEach(d=>{
            if(d.flow>item_attr[index-1]&&d.flow<=item_attr[index]){
              num++
            }
          })

          HistogramData.push([index,num])
        }
        this.drawHistogram(HistogramData,50)
      },
      drawHistogram(randomData, randomDataLength) {
        console.log('data is ');
        console.log(randomData);
        
        let self = this;
        let domItem = d3.select(self.$el);
        let brushleft = 0;
        let brushright = 0;
        let width =
          +domItem
            .select(".filter-graph")
            .style("width")
            .split("px")[0] * 0.9;
        let height =
          +domItem
            .select(".filter-graph")
            .style("height")
            .split("px")[0] * 0.5;
        let margin = +width * 0.05;

        let xScale = d3
          .scaleBand()
          .rangeRound([0, width], 0.1)
          .domain(
            randomData.map(function (d) {
              return d[0];
            })
          )
          .rangeRound([0, width], 0.1);

        let y = d3
          .scaleLinear()
          .domain([
            d3.max(randomData, function (d) {
              return d[1];
            }),
            0
          ])
          .range([0, height]);

        let x = d3
          .scaleLinear()
          .domain([0, randomDataLength])
          .range([0, width]);

        let brush = d3
          .brushX()
          .extent([[0, 0], [width, height]])
          .on("end", function () {
            let range = d3.brushSelection(this).map(x.invert);
            brushleft = Math.round(range[0]);
            brushright = Math.round(range[1]);
            console.log(randomData.slice(brushleft, brushright));
          });
        let svg = d3
          .select("#barchart")
          .attr("width", width + margin * 2)
          .attr("height", height + margin + margin)
          .append("g")
          .attr("id", "yaxis")
          .attr("transform", "translate(" + margin + "," + margin + ")")
          .call(
            d3
              .axisLeft()
              .scale(y)
              .ticks(3)
          );

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
          .attr("transform", "translate(" + margin * 0.8 + ",0)")
          .attr("fill", "#95a5a6");
        let translateMarginX = margin + 10;
        d3.select("#barchart")
          .append("g")
          .selectAll("rect")
          .data(randomData)
          .enter()
          .append("rect")
          .attr("width", xScale.bandwidth())
          .attr("height", function (d, i) {
            return (
              (d[1] * height) /
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
              height -
              (d[1] * height) /
              d3.max(randomData, function (d) {
                return d[1];
              })
            );
          })
          .attr("transform", "translate(" + translateMarginX + "," + margin + ")")
          .style("fill", "rgb(31,165,218)")
          .style("stroke", "rgb(48,50,67)");

        svg
          .append("g")
          .attr("class", "brush")
          .call(brush);
      },
      
    },
    mounted() {
      // let self = this;
      // let randomData = [];
      // let randomDataLength = 50;
      // for (let i = 0; i < randomDataLength; i++) {
      //   let rand = Math.floor(Math.random() * 500);
      //   randomData.push([i, rand]);
      // }
      // self.drawHistogram(randomData, randomDataLength);
    },
    computed: {
      ...mapGetters(["layoutData_get"])
    },
    watch: {
      layoutData_get: function (data) {
        //这里获取到当前布局的数据，然后重新绘制直方图
        console.log(data)
        this.dataProcess(data)
      },
      selected: function (data) {
        console.log(data);
      }
    }
  };
</script>
<style lang="less" scoped>
@import "AppTimeLine.less";
@import "./AppFilter.less";
</style>
