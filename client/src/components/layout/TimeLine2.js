const d3 = require('d3')
export default class TimeLine2 {
   constructor(){
     this.Timeline();
   }
   Timeline() {

     var timeline_data = [];//获取下面整体时间段中的所有数据
     var select_data = [];//brush选中时间段的数据
     Date.prototype.Format = function(fmt) {
       var o = {
         "M+": this.getMonth() + 1, //月份
         "d+": this.getDate(), //日
         "h+": this.getHours(), //小时
         "m+": this.getMinutes(), //分
         "s+": this.getSeconds(), //秒
         "q+": Math.floor((this.getMonth() + 3) / 3), //季度
         "S": this.getMilliseconds() //毫秒
       };
       if (/(y+)/.test(fmt))
         fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
       for (var k in o) {
         if (new RegExp("(" + k + ")").test(fmt)) {
           fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
         }
       }
       return fmt;
     }

    var Center = {};
    var timeline = {};
    let obj = {};
    var newstr = '';
    let startTime ='20160715152212400000'//"20160716004757000000" //'20160716084707500000'
    let maxendtime='20160715162212400000'//"20160716014757000000"//"20160716094707500000";
    Center.startTime = newdatestr(startTime)
    Center.endTime = newdatestr(maxendtime)
    obj.data = JSON.stringify([startTime, maxendtime]);

    var globalSpan = [
      { "id": "global_tl_real", "text": "最近半小时", "minCnt": 30 },
      { "id": "global_tl_day", "text": "最近1小时", "minCnt": 60 },
      { "id": "global_tl_week", "text": "最近3小时", "minCnt": 3 * 60 },
      { "id": "global_tl_month", "text": "最近5小时", "minCnt": 5 * 60 }
    ];
    var timelineGranulariy = [
      { "id": "granulariy_tl_5", "text": "1分钟", "minCnt": 1 },
      { "id": "granulariy_tl_15", "text": "5分钟", "minCnt": 5 },
      { "id": "granulariy_tl_30", "text": "10分钟", "minCnt": 10 },
      { "id": "granulariy_tl_60", "text": "15分钟", "minCnt": 15 },
    ];

    function globalBtnFunc(mincnt) {
      //console.log("globalBtnFunc "+mincnt);
      lower_timeminspan = mincnt;
      if (mincnt!=-1){
        var timeend=new Date(newdatestr(maxendtime));
        var timestart=new Date(timeend.getTime()-mincnt*60*1000);
        startTime=date2str(timestart);
        Center.startTime = newdatestr(startTime);
        obj.data = JSON.stringify([startTime, maxendtime]);
        console.log(obj.data);
        redrawTimeline();
      }
    }

    function granulariyBtnFunc(mincnt) {
      upper_timemin_gran = mincnt;
      focusToStart();
    }
    setTimelineBtn("#global_time_span_list li", globalSpan, "global_time_span_btn", '<i class="fa fa-caret-down"></i>', globalBtnFunc);
    setTimelineBtn("#time_granulariy_list li", timelineGranulariy, "time_granulariy_btn", '<i class="fa fa-caret-down"></i>', granulariyBtnFunc);

    function setTimelineBtn(listid, listobj, btnid, iHTML, func) {
      $(listid).on("click", function(d) {
        let tmpclickedid = (d.currentTarget.id);
        for (let i = 0; i < listobj.length; i++) {
          if (listobj[i].id == tmpclickedid) {
            document.getElementById(btnid).innerHTML = listobj[i].text + " " + iHTML;
            func(listobj[i].minCnt);
            break;
          }
        }
      })
    }
    var autoplaytimer;

    $("#timeline_play").on("click", function(d) {
      let tmphtml = (document.getElementById("timeline_play").innerHTML);
      let playbool = tmphtml.indexOf("play") >= 0 ? true : false;
      if (playbool) {
        //开始
        document.getElementById("timeline_play").innerHTML = '<i class="fa fa-pause"></i>&nbsp;&nbsp;暂停动画';
        autoplaytimer = window.setInterval(function() {
          var newtime = uppertimewindow[1].valueOf() + upper_timemin_gran * 60 * 1000;
          var maxtime = focus_x.invert(focus_width).valueOf();
          if (newtime > maxtime) {
            focusToEnd();
            autoplaytimer = window.clearInterval(autoplaytimer);
          } else {
            focusToTime(newtime);
          }
        }, 1000);

      } else {
        //暂停
        // document.getElementById("timeline_play").innerHTML = '<i class="fa fa-play"></i>&nbsp;&nbsp;开始动画';
        document.getElementById("timeline_play").innerHTML = '<font-awesome-icon icon="play" /></i>&nbsp;&nbsp;开始动画';
        autoplaytimer = window.clearInterval(autoplaytimer);
      }
    })


    {
      var upperLineId = "upper_line";
      var upper_width = $("#" + upperLineId).css("width");
      upper_width = parseFloat(upper_width.split("p")[0]);
      var upper_height = $("#" + upperLineId).css("height");
      upper_height = parseFloat(upper_height.split("p")[0]);
      var upper_margin = { "top": 8, "left": 25, "right": 5, "bottom": 20 };
      var focus_width = upper_width - upper_margin.left - upper_margin.right
      var focus_height = upper_height - upper_margin.top - upper_margin.bottom;

      var upper_svg = d3.select("#" + upperLineId).append("svg")
        .attr("width", upper_width)
        .attr("height", upper_height);
      var focusline = upper_svg.append("g")
        .attr("transform", "translate(" + upper_margin.left + "," + upper_margin.top + ")")
        .attr("width", focus_width)
        .attr("height", focus_height);
      var focus_area;
      var focus_area_stroke;
      var focus_xAxis;
      var focus_yAxis;
      var focus_timerect;
    } {
      var lowerLineId = "lower_line";
      var lower_width = $("#" + lowerLineId).css("width");
      lower_width = parseFloat(lower_width.split("p")[0]);
      var lower_height = $("#" + lowerLineId).css("height");
      lower_height = parseFloat(lower_height.split("p")[0]);
      var lower_margin = { "top": 5, "left": 25, "right": 5, "bottom": 20 };
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
      var focus_x = d3.scaleTime().range([0, focus_width]),
        context_x = d3.scaleTime().range([0, context_width]),
        focus_y = d3.scaleLinear().range([focus_height, 0]),
        context_y = d3.scaleLinear().range([context_height, 0]);

      var lowerformat = d3.timeFormat("%Y-%m-%e %H:%M:%S");
      var upperormat = d3.timeFormat("%H:%M:%S");
      var lowerparseTime = d3.timeParse("%Y-%m-%e %H:%M:%S");
    } {
      var lower_timeminsplite = 30; //lower timeline axis tick, default:60
      var upper_timeminsplite = 15; //upper timeline axis tick, default:30
      var lower_timeminspan = 60; //global time range, default:60
      var upper_timemin_gran = 5; //upper time granulariy, default:5

      var lowertimerange = []; //lower time range
      var lowertimebrushed = []; //upper time range
      var uppertimewindow = []; //uper time window

      var lower_data = new Array();
    }

    function redrawTimeline(){
      CommunicateWithServer('get',obj,'getData',redrawTimeLine);
      // $.ajax({
      //   type: 'GET',
      //   url: 'getData',
      //   data: obj,
      //   dataType: 'json',
      //   success: function(evt_data) {
      //     lower_data=evt_data.data
      //     console.log(lower_data);
      //     drawLowerTimeLine(lower_data);
      //     drawUpperTimeLine(lower_data);
      //     // Datacenter.getMultipleGraphs(data)
      //   },
      //   error: function(jqXHR) {
      //     console.log('post error!!', jqXHR);
      //   },
      // })
    }
    function redrawTimeLine(evt_data) {
        lower_data= evt_data.data;
        timeline_data = evt_data.timeLineData;//获取下面整体时间段中的所有数据
        drawLowerTimeLine(lower_data);
        drawUpperTimeLine(lower_data);
    }
    function newdatestr(strdate) {
      newstr = strdate[0] + strdate[1] + strdate[2] + strdate[3] + "-" + strdate[4] + strdate[5] + "-" + strdate[6] + strdate[7] + " " + strdate[8] + strdate[9] + ":" + strdate[10] + strdate[11] + ":" + strdate[12] + strdate[13]
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
        .on("start brush", brushed);
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
      focusToStart();
    }

    function brushed() {
      var s = d3.event.selection;
      var select_x = s[0],
        select_x1 = s[1];
      var dx = select_x1 - select_x;
      //console.log(s);
      if (dx) {
        lowertimebrushed = [context_x.invert(select_x), context_x.invert(select_x1)];
        context_brushhandle.attr("display", null).attr("transform", function(d, i) { return "translate(" + s[i] + "," + (context_height - context_height / 5 - lower_margin.bottom) / 2 + ")"; });
        //timedata = [context_x.invert(select_x), context_x.invert(select_x1)];
        focus_x.domain([context_x.invert(select_x), context_x.invert(select_x1)]);
        lowertimebrushed = focus_x.domain();
        focusline.select(".timeline_path").attr("d", focus_area);
        focusline.select(".timeline_path_stroke").attr("d", focus_area_stroke);
        focusline.select(".axis").call(focus_xAxis);
        focusline.selectAll(".axis .tick text").attr("transform", "translate(0," + 5 + ")");
      } else {
        lowertimebrushed = context_x.domain();
        context_brushhandle.attr("display", "none");

        focus_x.domain(context_x.domain());
        lowertimebrushed = focus_x.domain();
        focusline.select(".timeline_path").attr("d", focus_area);
        focusline.select(".timeline_path_stroke").attr("d", focus_area_stroke);
        focusline.select(".axis").call(focus_xAxis);
        focusline.selectAll(".axis .tick text").attr("transform", "translate(0," + 5 + ")");

      }
      document.getElementById("timeline_play").innerHTML = '<i class="fa fa-play"></i>&nbsp;&nbsp;开始动画'
      autoplaytimer = window.clearInterval(autoplaytimer);
    }

    function drawUpperTimeLine(datap) {

      focusline.selectAll("g").remove();

      focus_x.domain(context_x.domain());
      focus_y.domain(context_y.domain());
      focus_xAxis = d3.axisBottom(focus_x).tickSize(-focus_height)
        .ticks(d3.timeMinute.every(upper_timeminsplite));
      focus_yAxis = d3.axisLeft(focus_y).ticks(5);
      focus_area = d3.area().curve(d3.curveBasis)
        .x(function(d) { return focus_x(lowerparseTime(d3.keys(d)[0])); })
        .y0(focus_height)
        .y1(function(d) { return focus_y(d3.values(d)[0]); });
      focus_area_stroke = d3.line().curve(d3.curveBasis)
        .x(focus_area.x()).y(focus_area.y1());
      lowertimebrushed = focus_x.domain();
      //path
      var patharea = focusline.append("g");
      patharea.append("defs").append("clipPath")
        .attr("id", "tl_clip").append("rect")
        .attr("width", focus_width)
        .attr("height", focus_height);
      patharea.append("path")
        .attr("class", "timeline_path")
        .datum(datap)
        .attr("clip-path", "url(#tl_clip)")
        .attr("d", focus_area);
      patharea.append("path")
        .attr("class", "timeline_path_stroke")
        .datum(datap)
        .attr("clip-path", "url(#tl_clip)")
        .attr("d", focus_area_stroke);
      //axis
      var axisarea = focusline.append("g");
      var xaxis = axisarea.append("g")
        .attr("class", "axis")
        .attr("transform", "translate(0," + (focus_height) + ")")
        .call(focus_xAxis);
      xaxis.selectAll(".tick text").attr("transform", "translate(0," + 5 + ")");
      axisarea.append("g")
        .attr("class", "axis")
        .call(focus_yAxis);
      //focus window
      focus_timerect = focusline.append("g");
      //mouseover
      var mouseoverarea = focusline.append("g");
      var linearGradient = mouseoverarea.append("defs").append("linearGradient")
        .attr("id", "focusline_linearColor")
        .attr("x1", "0%").attr("y1", "0%")
        .attr("x2", "0%").attr("y2", "100%");
      linearGradient.append("stop").attr("offset", "0%")
        .style("stop-color", "rgba(230,230,31,0)");
      linearGradient.append("stop").attr("offset", "50%")
        .style("stop-color", "rgba(230,230,31,1)");
      linearGradient.append("stop").attr("offset", "100%")
        .style("stop-color", "rgba(230,230,31,0)");
      var focus_mousemove = mouseoverarea.append("rect")
        .attr("class", "upper_mousemove")
        .attr("x", 0).attr("y", 0)
        .attr("width", 2).attr("height", focus_height)
        .attr("fill", "url(#focusline_linearColor)");
      focus_mousemove.attr("display", "none");
      //mouseover layer
      var focusarea = focusline.append("g").attr("class", "focusarea");
      focusarea.append("rect").attr("class", "overlay")
        .attr("x", 0).attr("y", 0) //.attr("opacity",0)
        .attr("width", focus_width).attr("height", focus_height);
      focusarea.attr("cursor", "pointer")
        .on("mousemove", function() {
          var pardom = $("#upper_line .focusarea .overlay")[0];
          var curx = d3.mouse(pardom)[0];
          //var curtime=focus_x.invert(curx);
          //console.log(curx);console.log(curtime);
          focus_mousemove.attr("x", curx - 1);
        }).on("mouseenter", function() {
        focus_mousemove.attr("display", "block");
      }).on("mouseleave", function() {
        focus_mousemove.attr("display", "none");
      }).on("click", function() {
        var pardom = $("#upper_line .focusarea .overlay")[0];
        var curx = d3.mouse(pardom)[0];
        var curtime = focus_x.invert(curx);
        focusToTime(curtime);
      });
      focusToStart();
    }

    function focusToTime(time) {

      var timeend = focus_x.invert(focus_width).valueOf();
      var timestart = focus_x.invert(0).valueOf();
      if (time.valueOf() - upper_timemin_gran * 60 * 1000 < timestart) {
        focusToStart();
      } else {
        drawUpperRectRangeDateE(time, upper_timemin_gran);
      }
    }

    function focusToEnd() {
      drawUpperRectRangeDateE(focus_x.invert(focus_width), upper_timemin_gran);
    }

    function focusToStart() {
      drawUpperRectRangeDateS(focus_x.invert(0), upper_timemin_gran);
    }

    function drawUpperRectRangeDateS(timestart, timespan) {
      var timeend = timestart.valueOf() + timespan * 60 * 1000;
      timeend = new Date(timeend);
      var timespw = focus_x(timeend) - focus_x(timestart);
      drawUpperRectRangeLoc(focus_x(timeend), timespw)
    }

    function drawUpperRectRangeDateE(timeend, timespan) {
      var starttime = timeend.valueOf() - timespan * 60 * 1000;
      starttime = new Date(starttime);
      var timespw = focus_x(timeend) - focus_x(starttime);
      drawUpperRectRangeLoc(focus_x(timeend), timespw)
    }

    function drawUpperRectRangeLoc(timeendlocx, timespanwidth) {
      if (timeendlocx > focus_width) {
        timeendlocx = focus_width;
      }

      uppertimewindow = [focus_x.invert(timeendlocx - timespanwidth), focus_x.invert(timeendlocx)];//刷子获取到的时间段
      document.getElementById("timeline_tip").innerHTML = "时刻指示器:&nbsp;" + upperormat(focus_x.invert(timeendlocx));

      focus_timerect.selectAll("g").remove();
      focus_timerect.append("g").append("rect")
        .attr("class", "upper_timerange")
        .attr("x", timeendlocx - timespanwidth)
        .attr("width", timespanwidth)
        .attr("height", focus_height);
      focus_timerect.append("g").append("path")
        .attr("class", "upper_timerange_t")
        .attr("d", resizePath);
      focus_timerect.append("g").append("line")
        .attr("class", "upper_timerange_t")
        .attr("x1", timeendlocx).attr("y1", 0)
        .attr("x2", timeendlocx).attr("y2", focus_height);

      function resizePath() {
        var pathw = 5;
        var pathh = upper_margin.top;
        var rectanglerate = 1 / 4.5;
        var str = "M" + (timeendlocx - pathw / 2) + ",-" + (1 * pathh) +
          " L" + (timeendlocx + pathw / 2) + ",-" + (1 * pathh) +
          " L" + (timeendlocx + pathw / 2) + ",-" + (pathh * rectanglerate) +
          " L" + timeendlocx + "," + 0 +
          " L" + (timeendlocx - pathw / 2) + ",-" + (pathh * rectanglerate) +
          " Z";
        //console.log(str);
        return str;

      }
      console.log(uppertimewindow);
      $('#start_text_time').text(uppertimewindow[0].Format("yyyy-MM-dd hh:mm:ss"))
      $('#end_text_time').text(uppertimewindow[1].Format("yyyy-MM-dd hh:mm:ss"))


      /*********
       * 这里获取到brush选择的时间段的数据
       * *********/
     var brush_startTime = date2str(uppertimewindow[0]);
     var brush_endTime = date2str(uppertimewindow[1]);
     var brush_data = [];
     timeline_data.forEach(function (item) {
       if(item.start_time >= brush_startTime && item.end_time <= brush_endTime){
         brush_data.push(item);
       }
     })
      select_data = [].concat(brush_data);//看作为一层的深拷贝
      console.log(brush_startTime, brush_endTime)

      /****
       * 可以在这里写与主界面布局的接口，
       * 也可自行传出选中的数据：select_data，
       * 以及选中的时间：uppertimewindow（为Date格式），brush_startTime、brush_endTime（为String格式）
       * ***/

    }
    redrawTimeline();

  }
}


