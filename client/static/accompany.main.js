{
    var upperLineId = "bottom_timeline";
    var upper_width = $("#" + upperLineId).css("width");
    upper_width = parseFloat(upper_width.split("p")[0]);
    var upper_height = $("#" + upperLineId).css("height");
    upper_height = parseFloat(upper_height.split("p")[0]);
    var upper_margin = { "top": 15, "left": 25, "right": 5, "bottom": 20 };

} {
    var lowerLineId = "bottom_timeline";
    var lower_width = $("#" + lowerLineId).css("width");
    lower_width = parseFloat(lower_width.split("p")[0]);
    var lower_height = $("#" + lowerLineId).css("height");
    lower_height = parseFloat(lower_height.split("p")[0]);
    var lower_margin = { "top": 5, "left": 35, "right": 5, "bottom": 20 };
    var context_width = lower_width - lower_margin.left - lower_margin.right
    var context_height = lower_height - lower_margin.top - lower_margin.bottom;

    var lower_svg = d3.select("#" + lowerLineId).append("svg")
        .attr("width", lower_width)
        .attr("height", lower_height);
    var context = lower_svg.append("g")
        .attr("transform", "translate(" + lower_margin.left + "," + lower_margin.top + ")")
        .attr("width", context_width)
        .attr("height", context_height);
    var context_area;
    var context_xAxis;
    var context_yAxis;
    var context_brushhandle;

} {
    var context_x = d3.scaleTime().range([0, context_width]),
        context_y = d3.scaleLinear().range([context_height, 0]);
    var accompanyTime = d3.scaleLinear().range([5, 15]).domain([0, 30]);
    var lowerformat = d3.timeFormat("%Y-%m-%e %H:%M:%S");
    var upperormat = d3.timeFormat("%H:%M:%S");
    var lowerparseTime = d3.timeParse("%Y-%m-%e %H:%M:%S");
} {
    var lower_timeminsplite = 5; //lower timeline axis tick, default:60
    var lower_timeminspan = 30; //global time range, default:60
    var lowertimerange = []; //lower time range
    var axisTime = d3.scaleOrdinal().range([5, 10, 30]).domain([30, 60, 180]);
    var spacing = axisTime(lower_timeminspan)/10;
    var nodeArray = [];
}


let drawId = "left_accompany";
let draw_width = $("#" + drawId).css("width");
draw_width = parseFloat(draw_width.split("p")[0]);
let draw_height = $("#" + drawId).css("height");
draw_height = parseFloat(draw_height.split("p")[0]);

let draw_svg = d3.select("#" + drawId).append("svg")
  .attr('width', draw_width)
  .attr('height', draw_height)
  .attr("viewBox", [-draw_width / 2, -draw_height / 2, draw_width, draw_height]);


d3.csv("../data/accompany.csv").then(function (nodeData) {
    nodeArray = [].concat(nodeData);
    drawTimeLine();
})



function drawTimeLine(){
    d3.json("../data/tsconfig.json") .then(function (timeLine) {
        drawLowerTimeLine(timeLine.data);
    })
}



function drawLowerTimeLine(datap) {

    context_x.domain(d3.extent(datap.map(function(d) { return lowerparseTime(d3.keys(d)[0]); })));
    context_y.domain([0, d3.max(datap.map(function(d) { return d3.values(d)[0]; }))]);
    context_area = d3.area().curve(d3.curveBasis)
        .x(function(d) { return context_x(lowerparseTime(d3.keys(d)[0])); })
        .y0(context_height)
        .y1(function(d) { return context_y(d3.values(d)[0]); });
    context_xAxis = d3.axisBottom(context_x).tickSize(-context_height)
        .ticks(d3.timeMinute.every(lower_timeminsplite));
    context_yAxis = d3.axisLeft(context_y).ticks(5);

    lowertimerange = context_x.domain();

    context.selectAll("g").remove();

    context.append("g").append("path")
        .attr("class", "timeline_path")
        .datum(datap)
        .attr("d", context_area);
    var xaxis = context.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0," + (context_height) + ")")
        .call(context_xAxis);
    xaxis.selectAll(".tick text").attr("transform", "translate(0," + 5 + ")");
    context.append("g")
        .attr("class", "axis")
        .call(context_yAxis);

    var brush = d3.brushX()
        .extent([
            [0, 0],
            [context_width, context_height]
        ])
        .on("end", brushend)
       // .on("start brush", brushed);
    var gbrush = context.append("g")
        .attr("class", "brush")
        .call(brush);
    $("#" + lowerLineId + " .overlay").css("height", context_height).css("width", context_width);
    $("#" + lowerLineId + " .selection").css("height", context_height);
    context_brushhandle = gbrush.selectAll(".handle--lower")
        .data([{ type: "w" }, { type: "e" }])
        .enter().append("path")
        .attr("class", "handle--lower")
        .attr("cursor", "ew-resize")
        .attr("d", resizePath);
    context_brushhandle.attr("display", "none");

    function resizePath(d) {
        //console.log(d);
        var e = +(d.type == "e"),
            x = e ? 1 : -1,
            y = context_height / 5;
        return "M" + (.5 * x) + "," + y +
            "A1.5,1.5 0 0 " + e + " " + (4.5 * x) + "," + (y + 1.5) +
            "V" + (2 * y - 1.5) +
            "A1.5,1.5 0 0 " + e + " " + (.5 * x) + "," + (2 * y);
    }
}

function brushend() {
    var s = d3.event.selection;
    var select_x = s[0],
        select_x1 = s[1];
    var dx = select_x1 - select_x;

    if(dx){
        let clickState = 0;
        let clickNodes = [];

        let lowertimebrushed = [context_x.invert(select_x), context_x.invert(select_x1)];
        let brush_startTime = date2str(lowertimebrushed[0]);
        let brush_endTime = date2str(lowertimebrushed[1]);
        let spaceTime = Math.round(lowertimebrushed[1] - lowertimebrushed[0])/1000/60;
        let selectArray = selectNode(nodeArray, brush_startTime, brush_endTime);
        let accompanyNodes = cooutAccompanyNodes(selectArray);
        let accompanyEdges = cooutAccompanyEades(selectArray, spaceTime);
        let accompanyRateArray = accompanyRate(accompanyNodes, accompanyEdges);
        accompanyRateArray =  accompanyRateArray.filter(d => d.rate >= 50);

        let links = accompanyRateArray.map(d => Object.create(d));
        let linksToNodes = [];

        let linkWidth = d3.scaleLinear().range([1, 5]).domain([50, 100])
        accompanyRateArray.forEach(d => {
          linksToNodes.push(d.source);
          linksToNodes.push(d.target);
        })

       let node = new  Set(linksToNodes);
       let nodesCopy = [...node];

       let nodes = []
        nodesCopy.forEach(d => {
          let  item = {'id': d};
          nodes.push(item);
       })
       nodes = nodes.map(d => Object.create(d));

        //绘制力导向图

      d3.select("#left_accompany").selectAll('g').remove();

      const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody())
        .force("x", d3.forceX())
        .force("y", d3.forceY());



      const svg_link = draw_svg.append("g")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", d => linkWidth(d.rate));

      const svg_node = draw_svg.append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1)
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", 5)
        .attr("id", d => d.id)
        .attr("fill", 'gray')
        .on('click',function (d) {

          clickState++;
          if(clickState === 3){
            clickNodes.forEach(d => {
              d3.select('#' + d).attr("fill", 'gray');
            })
            clickNodes = [];
            clickNodes.push(d.id);
            clickState = 1;
          }
          if(clickState === 2){
            //展示详细共现关系的两个节点为：clickNodes[0] 和 this；
            if(clickNodes[0] === d.id){ //点击同一节点两次
              d3.select(this).attr('fill', 'gray');
              clickNodes = [];
              clickState = 0;
              return ;
            }

            let isLink = [];
            accompanyRateArray.forEach(d => {
              if (d.source === clickNodes[0]){
                isLink.push(d.target);
              } else if( d.target === clickNodes[0]){
                isLink.push(d.source);
              }
            })

            //判断选择的两节点是否相连
            if(isLink.includes(d.id)){

              d3.select("#right_detail").selectAll("svg").remove();
              drawTitle(clickNodes[0], d.id);

            let detailData = detailRate(nodeArray, clickNodes[0], d.id);
            console.log(detailData);

              drawDetailAccompany(detailData)

            }else {
              alert("两节点间不存在共现率，请重新选择!")
            }
          }

          d3.select(this).attr('fill', 'blue');
          clickNodes.push(d.id);
        })


      svg_node.append("title")
        .text(d => d.id);

      svg_link.append("title")
        .text(d =>  "共现率：" + d.rate + '%');

      simulation.on("tick", () => {
        svg_link
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

        svg_node
          .attr("cx", d => d.x)
          .attr("cy", d => d.y);
      });
      let svg = d3.select("#left_accompany svg");
      svg.call( d3.zoom()
        .scaleExtent( [ 0.1, 5] )
        .on( "zoom", zoomed ) );

      let  zoom_g = d3.select("#left_accompany").selectAll('g')
      function zoomed() {
        zoom_g.attr("transform", d3.event.transform);
      }

    }else{
        return;
    }

}

function drawTitle(source, target) {
  let titleWidth = 400, titleHeight = 200;
  let svg_title =  d3.select("#title").append("svg")
    .attr("id", "title")
    .attr("width", titleWidth)
    .attr("height", titleHeight)

  let  g_title = svg_title.append("g");

  g_title.append("line")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
    .attr("stroke-width", 5)
    .attr("x1", titleWidth/2 - 80)
    .attr("y1",  titleHeight/2)
    .attr("x2", titleWidth/2 + 80)
    .attr("y2", titleHeight/2);

  g_title.append("circle")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1)
    .attr("id", source)
    .attr("r", 10)
    .attr("fill", 'gray')
    .attr("cx", titleWidth/2 - 80)
    .attr("cy", titleHeight/2);

  g_title.append("circle")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1)
    .attr("id", target)
    .attr("r", 10)
    .attr("fill", 'gray')
    .attr("cx", titleWidth/2 + 80)
    .attr("cy", titleHeight/2);

  g_title.append('text').text(source)
    .attr("x", titleWidth/2 - 130)
    .attr("y", titleHeight/2 - 30)

  g_title.append('text').text(target)
    .attr("x", titleWidth/2 + 30)
    .attr("y", titleHeight/2 - 30)
}

function drawDetailAccompany(detailData) {

  let detailWidth = $("#right_detail").css("width")
  detailWidth = +detailWidth.split("px")[0];
  let cellSize = 0;
  if(detailWidth*0.9 > 21.5 * 30){
    cellSize = 21;
  }else{
    cellSize = Math.floor(detailWidth*0.9/31);
  }

  let startTime = detailData[0].date;
  let endTime = detailData[detailData.length -1].date;
  let color = d3.scaleSequential(d3.interpolatePiYG).domain([-1, 1])
  let svg = d3.select("#detail").append("svg")
    .attr("height", 280)
    .style("font", "10px sans-serif")
    .style("width", "90%");

  let g = svg.append("g");

  g.append("text")
    .attr("x", cellSize)
    .attr("y", 10)
    .attr("font-weight", "bold")
    .text(newdatestr(date2str(startTime)));

  g.append("text")
    .attr("x", cellSize * 31)
    .attr("y", cellSize * 8)
    .attr("font-weight", "bold")
    .attr("text-anchor", "end")
    .text(newdatestr(date2str(endTime)));

  g.append("g")
    .selectAll("rect")
    .data(detailData)
    .join("rect")
    .attr("width", cellSize - 1)
    .attr("height", cellSize - 1)
    .attr("x", d => (Math.floor((d.date - startTime)/10/1000/6) + 1) * cellSize + 0.5)
    .attr("y", d => ((d.date - startTime)/10/1000 %6 + 1) * cellSize + 0.5)
    .attr("fill", d => {
      if(d.value === 0){
        return color(0.3)
      }else {
        return color(-d.value/100);
      }
    })
    .append("title")
    .text(d => {
      let str = date2str(d.date);
      return newdatestr(str) + ",   共现率:" +d.value + "";
    });
  
}

function selectNode(allNode, startTime, endTime) {
    let selectArray = [];
    allNode.forEach(function (d) {
        if(d.event_begintime >= startTime&&d.event_endtime <= endTime){
            selectArray.push(d);
        }
    })
    return selectArray;
}
//结构为：节点-出现次数
function cooutAccompanyNodes(nodeData) {
    let accompanyNodes = {};
    nodeData.forEach(function (d) {
        if(!accompanyNodes[d.recv_node_golbal_no]){
            accompanyNodes[d.recv_node_golbal_no] = 1;
        }else{
            accompanyNodes[d.recv_node_golbal_no]++;
        }

        if(!accompanyNodes[d.trans_node_global_no]){
            accompanyNodes[d.trans_node_global_no] = 1;
        }else{
            accompanyNodes[d.trans_node_global_no]++;
        }

    })
    return accompanyNodes;
}
//结构为：source-target-出现次数
function cooutAccompanyEades(nodeData, spaceTime) {

    let accompanyNumber = 3;
    if(spaceTime >= 0){
      accompanyNumber = accompanyTime(spaceTime)
    }
    let accompanyEades = [];
    let accompanyEadesDict = {};
    let item = '';
    nodeData.forEach(function (d) {
       if(d.recv_node_golbal_no <= d.trans_node_global_no ){
           item = d.recv_node_golbal_no + '-' + d.trans_node_global_no;
       }else{
           item = d.trans_node_global_no  + '-' + d.recv_node_golbal_no;
       }

       if(!accompanyEadesDict[item]){
           let edge = item.split('-')
           let source = edge[0];
           let target = edge[1];
           accompanyEadesDict[item] = {source: source, target: target, number: 1}
       }else{
           accompanyEadesDict[item].number++;
       }

    })

    for (let head in accompanyEadesDict) {
       if(accompanyEadesDict[head].number >= accompanyNumber){
         accompanyEades.push(accompanyEadesDict[head]);
       }
    }

    return accompanyEades;
}

function accompanyRate(accompanyNodes, accompanyEdges) {
  let rate = 0;
  let rateArray = [];
  accompanyEdges.forEach(function (item) {
    let rateA = item.number/(accompanyNodes[item.source]);
    let rateB = item.number/(accompanyNodes[item.target]);
    rate = rateA > item.number/rateB ? rateA : rateB;
    rate = Math.round(rate*100);

      item['rate'] = rate;
      rateArray.push(item);

  })
  return rateArray;
}

//用于绘制详细共现关系的日历图，返回的数据结构为{date;时间, value:值2 }
function detailRate(allData, source, target) {
  let startTime = "20160715155200000000"
  let detailRateArray = [];
  let minuteData = {};
  let startDate = new Date(newdatestr(startTime));

  allData.forEach(d => {
    let date = new Date(newdatestr(d.event_endtime));
    let time = Math.floor((date - startDate)/10/1000);//间隔时间（10秒）
    if(!minuteData[time]){
      minuteData[time] = [];
      minuteData[time].push(d);
    }else {
      minuteData[time].push(d);
    }
  })
  for (let i = 1; i <= 180; i++){
    if(!minuteData[i - 1]){
      minuteData[i - 1] = [];
    }
    let minute = minuteRate(minuteData[i - 1], source, target);
    let rate = 0;
    if(Object.keys(minute).length != 0){
       rate = minute.rate;
     }
    let nowDate = startDate.getTime() + (i - 1)*10*1000;
    nowDate = new Date(nowDate);
    let item = {"date": nowDate, "value": rate};
    console.log(item)
    detailRateArray.push(item);
  }

  return detailRateArray;
}

//分为每一分钟的数据来计算共现率
function minuteRate(data, source, target) {

  if(data.length === 0){
    return {"source": source, "target": target, "rate": 0};
  }
  let filterData = [];
  data.forEach(d => {
    if(d.recv_node_golbal_no === source|| d.recv_node_golbal_no === target){
      filterData.push(d);
   }
  })

  let accompanyNodes = cooutAccompanyNodes(filterData);
  let accompanyEdges = cooutAccompanyEades(filterData, -1);
  let accompanyRateArray = accompanyRate(accompanyNodes, accompanyEdges);

  let resultObj = {};
  accompanyRateArray.forEach(d => {
     if((d.source === source && d.target === target) || (d.source === target && d.target === source)){
       resultObj = d;
     }
  })
  return resultObj;
}

function newdatestr(strdate) {
    let newstr = strdate[0] + strdate[1] + strdate[2] + strdate[3] + "-" + strdate[4] + strdate[5] + "-" + strdate[6] + strdate[7] + " " + strdate[8] + strdate[9] + ":" + strdate[10] + strdate[11] + ":" + strdate[12] + strdate[13]
    //console.log(newstr)
    return newstr;
}

function date2str(date){
    var datestr=date.getFullYear()+"";
    if((date.getMonth()+1)<10){
        datestr=datestr+"0"+(date.getMonth()+1);
    }else{
        datestr=datestr+(date.getMonth()+1);
    }
    if(date.getDate()<10){datestr=datestr+"0"+date.getDate();}else{datestr=datestr+date.getDate();}
    if(date.getHours()<10){datestr=datestr+"0"+date.getHours();}else{datestr=datestr+date.getHours();}
    if(date.getMinutes()<10){datestr=datestr+"0"+date.getMinutes();}else{datestr=datestr+date.getMinutes();}
    if(date.getSeconds()<10){datestr=datestr+"0"+date.getSeconds();}else{datestr=datestr+date.getSeconds();}
    datestr=datestr+"000000";
    //console.log(datestr);
    return datestr;
}
