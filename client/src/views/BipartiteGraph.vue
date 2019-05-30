<template>
  <div id = "blackGround">
  <div id = "draw"> </div>
  </div>
</template>

<script>
  const d3 = require('d3')
  import '../../static/accompany.less'
    export default {
        name: "bipartiteGraph",
      mounted() {


        let draw_data = window.localStorage;

        let nodeData = JSON.parse( draw_data.data)

        drawBipartiteGraph(nodeData);
        //用于绘制二部图
        function drawBipartiteGraph(nodeData) {
          d3.select("#draw").selectAll("svg").remove();
        //  $("#selectTime").hide();
          let linkLayer = [], networkLayer = [], appLayer = [];
          // let nodesArray = [].concat(nodes);
          nodeData.forEach(function (item, index) {

            if(item.netLevel >= 100 && item.netLevel < 200){
              linkLayer.push(item.source);
              linkLayer.push(item.target);
            }else if(item.netLevel >= 200 && item.netLevel < 300){
              if(index <= 3){
                linkLayer.push(item.source);
                linkLayer.push(item.target);
              }

              if(index >= nodeData.length -4){
                appLayer.push(item.source);
                appLayer.push(item.target);
              }
              networkLayer.push(item.source);
              networkLayer.push(item.target);
            }else {
              appLayer.push(item.source);
              appLayer.push(item.target);
            }
          })
          linkLayer = delectRepeat(linkLayer);
          networkLayer = delectRepeat(networkLayer);
          appLayer = delectRepeat(appLayer);

          let linkNodes = [], networkNodes = [], appNodes = [];
          let links = [];
          nodeData.forEach(d => {
            if(linkLayer.includes(d.source) == true && networkLayer.includes(d.target) == true && networkNodes.length < 5){
              if (networkNodes.includes(d.source) == false && linkNodes.includes(d.target) == false) {
                linkNodes.push(d.source);
                networkNodes.push(d.target);
                links.push(d);
              }

            } else if(linkLayer.includes(d.target) == true && networkLayer.includes(d.source) == true && networkNodes.length < 5){

              if (networkNodes.includes(d.target) == false && linkNodes.includes(d.source) == false) {
                linkNodes.push(d.target);
                networkNodes.push(d.source);
                links.push(d);
              }

            }

            if(appLayer.includes(d.source) == true && networkLayer.includes(d.target) == true && networkNodes.length < 5){

              if (networkNodes.includes(d.source) == false && appNodes.includes(d.target) == false) {
                appNodes.push(d.source);
                networkNodes.push(d.target);
                links.push(d);
              }
            } else if(appLayer.includes(d.target) == true && networkLayer.includes(d.source) == true && networkNodes.length < 5){

              if (networkNodes.includes(d.target) == false && appNodes.includes(d.source) == false) {
                appNodes.push(d.target);
                networkNodes.push(d.source);
                links.push(d);
              }

            }

          })

          linkNodes = delectRepeat(linkNodes);
          networkNodes = delectRepeat(networkNodes);
          appNodes = delectRepeat(appNodes);
          console.log(linkNodes, networkNodes, appNodes, links);


          // d3.select("#left_accompany").selectAll("svg").remove()

          let nodesWidth = $("#draw").css("width")
          nodesWidth = +nodesWidth.split("px")[0];

          let nodesHeight = $("#draw").css("height");
          nodesHeight = +nodesHeight.split("px")[0];

          d3.select("#nodesLevel").remove()
          let layer_svg = d3.select("#draw").append("svg")
            .attr("id", "nodesLevel")
            .attr("width", nodesWidth)
            .attr("height", nodesHeight);

          let maxLength =  Math.max(linkNodes.length, networkNodes.length, appNodes.length);
          let number = 1;
          let  rectArray = [];

          let drawLink_g = layer_svg.append("g");
          let links_g = layer_svg.append("g");
          let network_g = layer_svg.append("g");
          let app_g = layer_svg.append("g");
          let rect_g = layer_svg.append("g");

          if(linkNodes.length != 0){

            let item = {length : linkNodes.length, color: "#20b2aa"}
            rectArray.push(item)
            number++;
          }
          if(networkNodes.length != 0){
            let item = {length : networkNodes.length, color: "#517fdb"}
            rectArray.push(item)
            number++;
          }
          if(appNodes.length != 0){
            let item = {length : appNodes.length, color: "#2bab36"}
            rectArray.push(item)
            number++;
          }

          let heightSpace =  nodesHeight/ (maxLength + 1) - 9;
          let space = nodesWidth/number - 10;
          if(linkNodes.length != 0){
            links_g
              .append("text")
              .text("链路层")
              .attr("x", space - 22)
              .attr("y", 100  - 35)

          }
          if(networkNodes.length != 0){
            network_g
              .append("text")
              .text("网络层")
              .attr("x", space*2 - 22)
              .attr("y", 100  - 35)
          }
          if(appNodes.length != 0){
            app_g
              .append("text")
              .text("应用层")
              .attr("x", space*3 - 22)
              .attr("y", 100  - 35)
          }

          let position = {};

          links_g
            .selectAll("circle")
            .data(linkNodes)
            .enter()
            .append("circle")
            .attr("id", d => d)
            .attr("r", 9)
            .attr("fill", '#20b2aa')
            .attr("cx", d => {
              position[d] = {x: 0, y: 0};
              position[d].x = space;
              return space
            } )
            .attr("cy", (d, i) => {
              position[d].y = 100 + heightSpace*i;
              return 100 + heightSpace*i;
            })
            .append("title")
            .text(d => d);




          network_g
            .selectAll("circle")
            .data(networkNodes)
            .enter()
            .append("circle")
            .attr("id", d => d)
            .attr("r", 9)
            .attr("fill", '#517fdb')
            .attr("cx", d => {
              position[d] = {x: 0, y: 0};
              position[d].x = space*2;
              return space*2
            } )
            .attr("cy", (d, i) => {
              position[d].y = 100 + heightSpace*i;
              return 100 + heightSpace*i;
            })
            .append("title")
            .text(d => d);




          app_g
            .selectAll("circle")
            .data(appNodes)
            .enter()
            .append("circle")
            .attr("id", d => d)
            .attr("r", 9)
            .attr("fill", '#2bab36')
            .attr("cx", d => {
              position[d] = {x: 0, y: 0};
              position[d].x = space*3;
              return space*3
            } )
            .attr("cy", (d, i) => {
              position[d].y = 100 + heightSpace*i;
              return 100 + heightSpace*i;
            })
            .append("title")
            .text(d => d);

          drawLink_g
            .selectAll("line")
            .data(links)
            .enter()
            .append("line")
            .attr("stroke-width", 3)
            .attr("stroke", "#999")
            .attr("z-index", 1)
            .attr("x1", d => position[d.source].x)
            .attr("y1", d => position[d.source].y)
            .attr("x2", d => position[d.target].x)
            .attr("y2", d => position[d.target].y);


          rect_g
            .selectAll("rect")
            .data(rectArray)
            .enter()
            .append("rect")
            .attr("width", 30)
            .attr("height", d => 40 + heightSpace* (d.length - 1) )
            .attr("x", (d, i) => space * (i + 1) - 15)
            .attr("y", 100 - 20)
            .attr("fill", "none")
            .attr("stroke", d => d.color)
            .attr("stroke-width", 2)
            .attr("stroke-dasharray", '5,5')
            .attr("rx", 20)
            .attr("ry", 20)

        }

        function delectRepeat(array) {
          let set = new Set(array);
          return [...set]
        }

      },
      methods:{
          back(){
            history.go(-1);
          }
      }
    }
</script>

<style lang = "less" scoped>
  #blackGround {
    height: 100%;
    width: 100%;
    left: 0;
    top: 0;
    position: absolute;
    background: #282c37;

    #draw {
      position: absolute;
      height: calc(65% - 5px);
      width: calc(35% - 15px);
      left: calc(33% + 5px);
      top: calc(17% + 5px);
      background: #303243;

    }

  }



</style>
