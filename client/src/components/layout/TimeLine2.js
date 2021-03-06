const d3 = require('d3')
export default class TimeLine2 {
  constructor(){
    let self = this;
    self.select_time = "";
    self.Timeline();
  }
  Timeline() {
    let self = this
    var timeline_data = [];//获取下面整体时间段中的所有数据
    var select_data = [];//brush选中时间段的数据
    let hoursData = {};
    let distinguish_time = 30; //默认值为半小时
    var upper_data_copy = [];
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
    let startTime ='20160715155212400000'//"20160716004757000000" //'20160716084707500000'
    let maxendtime='20160715162212400000'//"20160716014757000000"//"20160716094707500000";
    Center.startTime = newdatestr(startTime)
    Center.endTime = newdatestr(maxendtime)
    obj.data = JSON.stringify([startTime, maxendtime]);
    obj.name = 'timeLineData_halfhour';

    var globalSpan = [
      { "id": "global_tl_real", "text": "最近半小时", "minCnt": 30 },
      { "id": "global_tl_day", "text": "最近1小时", "minCnt": 60 },
      { "id": "global_tl_week", "text": "最近3小时", "minCnt": 3 * 60 },
    ];
    var timelineGranulariy = [
      { "id": "granulariy_tl_5", "text": "1分钟", "minCnt": 1 },
      { "id": "granulariy_tl_15", "text": "5分钟", "minCnt": 5 },
      { "id": "granulariy_tl_30", "text": "10分钟", "minCnt": 10 },
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
        console.log(obj.data, obj.name, '+++++++++');
        redrawTimeLineD(mincnt);
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
        let newTime_x = uppertimewindow[1].valueOf();
        let maxTime_x = focus_x.invert(focus_width).valueOf();
        if(newTime_x >= maxTime_x){
          focusToStart();
        }
        document.getElementById("timeline_play").innerHTML = '<i class="fa fa-pause"></i>&nbsp;&nbsp;暂停动画';
        autoplaytimer = window.setInterval(function() {
          var newtime = uppertimewindow[1].valueOf() + upper_timemin_gran * 60 * 1000;
          var maxtime = focus_x.invert(focus_width).valueOf();
          if (newtime > maxtime) {
            focusToEnd();
            autoplaytimer = window.clearInterval(autoplaytimer);
            document.getElementById("timeline_play").innerHTML = '<i class="fa fa-play"></i>&nbsp;&nbsp;开始动画';
          } else {
            focusToTime(newtime);
          }
        }, 2000);

      } else {
        //暂停
        // document.getElementById("timeline_play").innerHTML = '<i class="fa fa-play"></i>&nbsp;&nbsp;开始动画';
        document.getElementById("timeline_play").innerHTML = '<i class="fa fa-play"></i>&nbsp;&nbsp;开始动画';
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
      var upper_timeminsplite = 5; //upper timeline axis tick, default:30
      var lower_timeminspan = 30; //global time range, default:60
      var upper_timemin_gran = 1; //upper time granulariy, default:5

      var lowertimerange = []; //lower time range
      var lowertimebrushed = []; //upper time range
      var uppertimewindow = []; //uper time window
      var axisTime = d3.scaleOrdinal().range([5, 10, 30]).domain([30, 60, 180]);
      var spacing = axisTime(lower_timeminspan)/10;
      var lower_data = new Array();
    }

    function drawTimeLine() {
      CommunicateWithServer('get',obj,'get-timeLine-json',drawTimeLineD);
    }

    function drawTimeLineD(evt_data) {
      hoursData[lower_timeminspan] = evt_data
      lower_data= evt_data.data;
      drawLowerTimeLine(lower_data);
      redrawTimeLineD(lower_timeminspan);//第一次为默认值：30分钟

      nodesNumber = evt_data.nodesNumber;
      console.log(nodesNumber)
    }

    //根据选择重新绘制上层时间轴
    function redrawTimeLineD(mincnt) {
      let lower_endTime = lowerparseTime(d3.keys(lower_data[lower_data.length - 1])[0])
      let upper_data = [];
      lower_data.forEach(function (d) {
        if(lower_endTime - lowerparseTime(d3.keys(d)[0]) <= mincnt*60*1000){
          upper_data.push(d);
        }
      })

      drawUpperTimeLine(lower_data, upper_data);
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
     console.log(lowertimebrushed)
      let upper_data = [];
      let lower_startTime = lowertimebrushed[0];
      let lower_endTime = lowertimebrushed[1];
      lower_data.forEach(function (d) {
        if(lowerparseTime(d3.keys(d)[0]) <= lower_endTime && lowerparseTime(d3.keys(d)[0]) >= lower_startTime){
          upper_data.push(d);
        }
      })
      spacing = (lower_endTime - lower_startTime)/10/60/1000;
      drawPeakValueLabe(upper_data);
      focusToStart();
    }

    function brushed() {
      d3.select('.peakRect').remove()
      var s = d3.event.selection;
      var select_x = s[0],
        select_x1 = s[1];
      var dx = select_x1 - select_x;
      //console.log(s);
      if (dx) {
        let timeMinute = d3.scaleLinear().range([0, 60]).domain([0, 360]);
        lowertimebrushed = [context_x.invert(select_x), context_x.invert(select_x1)];
        let spaceTime = (context_x.invert(select_x1) - context_x.invert(select_x))/1000/60;
        context_brushhandle.attr("display", null).attr("transform", function(d, i) { return "translate(" + s[i] + "," + (context_height - context_height / 5 - lower_margin.bottom) / 2 + ")"; });
        //timedata = [context_x.invert(select_x), context_x.invert(select_x1)];
        focus_x.domain([context_x.invert(select_x), context_x.invert(select_x1)]);
        lowertimebrushed = focus_x.domain();
        focusline.select(".timeline_path").attr("d", focus_area);
        focusline.select(".timeline_path_stroke").attr("d", focus_area_stroke);
        focus_xAxis = d3.axisBottom(focus_x).tickSize(-focus_height)
          .ticks(d3.timeMinute.every(parseInt(timeMinute(spaceTime))));
        focusline.select(".axis").call(focus_xAxis);

        focusline.selectAll(".axis .tick text").attr("transform", "translate(0," + 5 + ")");
      } else {
        lowertimebrushed = context_x.domain();
        context_brushhandle.attr("display", "none");

        focus_x.domain(d3.extent(upper_data_copy.map(function(d) { return lowerparseTime(d3.keys(d)[0]); })));
        lowertimebrushed = focus_x.domain();
        focusline.select(".timeline_path").attr("d", focus_area);
        focusline.select(".timeline_path_stroke").attr("d", focus_area_stroke);
        focusline.select(".axis").call(focus_xAxis);
        focusline.selectAll(".axis .tick text").attr("transform", "translate(0," + 5 + ")");

      }
      document.getElementById("timeline_play").innerHTML = '<i class="fa fa-play"></i>&nbsp;&nbsp;开始动画'
      autoplaytimer = window.clearInterval(autoplaytimer);
    }

    function drawPeakValueLabe(upperdata) {
      d3.select('.peakRect').remove()
      let peakValue = [];
      peakValue = upperdata.filter(function (d) {
        return d3.values(d)[0] > 200;
      });

      let peakValue_now = [];
      let peakValue_spacing = [];

      for(let i = 0; i < peakValue.length; i++){
        let pre_time, cur_time, next_time;
        if(i === 0){
          pre_time = lowerparseTime('2015-12-25 15:32:33');//设置一个足够小的初始值
        }else {
          pre_time = lowerparseTime(d3.keys(peakValue[i - 1])[0]);
        }
        cur_time = lowerparseTime(d3.keys(peakValue[i])[0]);
        if(i === peakValue.length - 1){
          next_time = new Date();//设置一个足够大的结束值
        }else {
          next_time = lowerparseTime(d3.keys(peakValue[i + 1])[0]);
        }
        if (cur_time - pre_time >= spacing*60*1000 && next_time - cur_time >= spacing*60*1000) {
          peakValue_now.push(peakValue[i]);
        }else{
          peakValue_spacing.push(peakValue[i]);
        }
      }

      if (peakValue_spacing.length != 0){
        let max_index = 0;
        let max = 0;
        peakValue_spacing.forEach(function (d, index) {
          if (d3.values(d)[0] > max){
            max = d3.values(d)[0];
            max_index = index;
          }
        })
        peakValue_now.push(peakValue_spacing[max_index])
      }
      peakValue_now = peakValue_now.filter(d => lowerparseTime(d3.keys(d)[0]).getMinutes() + spacing < 60 )

      let peakValue_pos = peakValue_now.map(function (d) {
        let time = lowerparseTime(d3.keys(d)[0]);
        let hour = time.getHours();
        let minute = time.getMinutes();

        if(hour >= 12){
          hour = '0' + (hour - 12);
        }else{
          hour = '0' + hour;
        }
        if(minute < 10){
          minute = '0' + minute;
        }

        let time_str = hour + ":" + minute;
        return {'time': time_str ,'x': focus_x(lowerparseTime(d3.keys(d)[0])), 'y': focus_height - focus_y(d3.values(d)[0])}
      })

      let peakRect = focusline.append('g').attr('class', 'peakRect');

      peakRect.append('g').attr('class','lines')
        .selectAll('line').data(peakValue_pos).enter()
        .append('line')
        .attr('x1', d => d.x)
        .attr('y1', focus_height)
        .attr('x2', d => d.x)
        .attr('y2', 0)
        .attr('stroke-width', 1)
        .attr('stroke', '#ada63c')
        .attr('stroke-dasharray', '5,5')

      peakRect.append('g').attr('class','times')
        .selectAll('text').data(peakValue_pos).enter()
        .append('text')
        .attr('x', d => d.x - 11)
        .attr('y', focus_height)
        .text(d => d.time)
        .attr("font-size", "9px")
        .attr("fill", "#ada63c")
        .attr("dy", '1.53em')
    }

    function drawUpperTimeLine(datap, upperdata) {

       focusline.selectAll("g").remove();
      spacing = axisTime(lower_timeminspan)/10
      upper_data_copy = upperdata;
      focus_x.domain(d3.extent(upperdata.map(function(d) { return lowerparseTime(d3.keys(d)[0]); })))

      //focus_x.domain(context_x.domain());
      focus_y.domain(context_y.domain());

      drawPeakValueLabe(upperdata);
      focus_xAxis = d3.axisBottom(focus_x).tickSize(-focus_height)
        .ticks(d3.timeMinute.every(axisTime(lower_timeminspan)));
      focus_yAxis = d3.axisLeft(focus_y).ticks(3);
      focus_area = d3.area().curve(d3.curveBasis)
        .x(function(d) { return focus_x(lowerparseTime(d3.keys(d)[0])); })
        .y0(focus_height)
        .y1(function(d) { return focus_y(d3.values(d)[0]) ; });
      focus_area_stroke = d3.line().curve(d3.curveBasis)
        .x(focus_area.x()).y(focus_area.y1());
    //  lowertimebrushed = focus_x.domain();
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
        //暂停动画
        document.getElementById("timeline_play").innerHTML = '<i class="fa fa-play"></i>&nbsp;&nbsp;开始动画'
        autoplaytimer = window.clearInterval(autoplaytimer);

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


      /*********
       * 这里获取到brush选择的时间段的数据
       * *********/
      var brush_startTime = date2str(uppertimewindow[0]);
      var brush_endTime = date2str(uppertimewindow[1]);
      var brush_data = [];
      let param = {};
      param.data = JSON.stringify([brush_startTime, brush_endTime]);

      CommunicateWithServer('get',param,'getData2',transfromSelectData);



      /****
       * 可以在这里写与主界面布局的接口，
       * 也可自行传出选中的数据：select_data，
       * 以及选中的时间：uppertimewindow（为Date格式），brush_startTime、brush_endTime（为String格式）
       * ***/
      //传出数据;
      function transfromSelectData(brush_data){

        select_data = [].concat(brush_data);//看作为一层的深拷贝
        //console.log(brush_startTime, brush_endTime)

        select_time.start = uppertimewindow[0].Format("yyyy-MM-dd hh:mm:ss");
        select_time.end = uppertimewindow[1].Format("yyyy-MM-dd hh:mm:ss");
        select_time.data = select_data;
        select_time.observe = brush_startTime;//用于监听
      }
    }
    drawTimeLine();

  }
}
