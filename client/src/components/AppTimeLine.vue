<!--*author:Ye Zhang *day:2018-1-06 -->
<template>
  <div id='timeline-panel'>
    <app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
    <div id="timeline_bottom">
      <div id="timeline_select">
        <div id="time_span_outer">
          全局时间跨度:&nbsp;
          <span class="button-dropdown button-dropdown-plain" data-buttons="dropdown" id="time_span1">
						<button class="button button-caution button-pill" id="global_time_span_btn">
						  最近半小时
              <!-- <i class="fa fa-caret-down"></i> -->
              <font-awesome-icon icon="caret-down" />

						</button>
						<ul class="button-dropdown-list is-below" id="global_time_span_list">
						  <li id="global_tl_real"><a >最近半小时</a></li>
						  <li id="global_tl_day"><a >最近1小时</a></li>
						  <li id="global_tl_week"><a >最近3小时</a></li>
						</ul>
					</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 时间粒度:&nbsp;
          <span class="button-dropdown button-dropdown-plain" data-buttons="dropdown" id="time_span2">
						<button class="button button-caution button-pill" id="time_granulariy_btn">
						  1分钟
              <!-- <i class="fa fa-caret-down"></i> -->
              <font-awesome-icon icon="caret-down" />
						</button>
						<ul class="button-dropdown-list is-below" id="time_granulariy_list">
						  <li id="granulariy_tl_5"><a >1分钟</a></li>
						  <li id="granulariy_tl_15"><a >5分钟</a></li>
						  <li id="granulariy_tl_30"><a >10分钟</a></li>
						</ul>
					</span>
        </div>
        <div id="timeline_tip">时刻指示器:&nbsp;00:00:00</div>
        <button class="button button-box button-tiny" id="timeline_play">
          <i class="fa fa-play"></i>
          <!-- <font-awesome-icon icon="play" /> -->
          &nbsp;&nbsp;开始动画</button>
      </div>
      <div id="timeline_line">
        <div id="upper_level">
          <div class="timeline_text" id="timeline_text2">选中时段流量</div>
          <div id="upper_line"></div>
        </div>
        <div id="lower_level">
          <div class="timeline_text" id="timeline_text1">全局时段流量</div>
          <div id="lower_line"></div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import AppTitle from './AppTitle.vue'
  import TimeLine2 from './layout/TimeLine2'
  import '../../static/bootstrap.min.css'
  import '../../static/buttons.css'
  // import '../../static/font-awesome.min.css'
  import 'font-awesome/css/font-awesome.css'

  window.timeTimePlay = false
  const d3 = require('d3')

  export default {
    data() {
      return {
        // icon: '<i class="fa fa-line-chart" aria-hidden="true"></i>',
        icon: 'chart-line',
        msgs: '时间轴',
        networkData: null,
        loadedData: null
      }
    },
    components: { AppTitle },
    watch: {
    },
    methods: {
      //绘制时间轴
      drawTimeLine() {
        let self = this
        self.TimeLine = new TimeLine2()
      },
      getDataWithParams(paramsObj) {
        let self = this
        let Url = 'recent-data'
        CommunicateWithServer('get', paramsObj, Url, data => {
          self.networkData = data['data']
          self.loadedData = Math.random()
          self.$store.state.testData = Math.random()
        })
      },
      timeChangeHandler(params) {
        let self = this
        // console.log('timeData+++++++++++++----', data)
        console.log('timeChange~~', params)
        self.emitEvent('time_change', params)
      },
      emitEvent(name, params) {
        console.log('hello ~~ emit event ', name)
        this.$emit(name, params)
      }

    },
    mounted() {
      let self = this
      self.getDataWithParams({
        timeRange: '1day'
      })
      self.drawTimeLine();
      //监听全局变量windows.select_time
      Object.defineProperty(select_time, 'observe',{
        set:function(value){
          //需要触发的渲染函数可以写在这...
          let tranformTime = {start: select_time.start, end: select_time.end };
          localStorage.setItem('timerange', JSON.stringify(tranformTime));
          self.$store.commit('modifySelectTime', tranformTime);
          self.$store.commit('modifySelectData', select_time.data);
        }
      })

      // setInterval(function () {
      //   alert(this.selectTime)
      // },2200)

    }
  }

</script>
<style lang="less" scoped>
  @import "AppTimeLine.less";

</style>
