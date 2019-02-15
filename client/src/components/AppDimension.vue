<template>
  <div id="dim2">
  <div id="dim2-panel">
    <!--<app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>-->
    <!--<div id="dimension2_btn" class="btn-div">
		DimReduce:&nbsp;&nbsp;
		<select id="st_dim_redu_func" @click="handledim">
		  <option value="0"><span>PCA</span></option>
		  <option value="1"><span>ICA</span></option>
		  <option value="2" selected = "selected"><span>t-SNE</span></option>
		</select>
		&nbsp;&nbsp;
		Outlier Detection:&nbsp;&nbsp;
		<select id="st_outlier_func" @click="handleoutlier">
		  <option value="0"selected = "selected"><span>EllipticEnvelope</span></option>
		  <option value="1"><span>BayesianGMM</span></option>
		</select>
	</div>-->
	<div id="dimension2_svg" class="block-div">
	    
	</div>
	
  </div>
  <div id="dim2_wait" class="outer-div"></div>
  </div>
</template>
<script>
import AppTitle from "./AppTitle.vue";
import {Spinner} from 'spin.js';
const d3 = require("d3");
const $ = require("jquery");
const _ = require("underscore");
import hostImg from "../assets/host.png";
import switchImg from "../assets/switch.png";
import serverImg from "../assets/server.png";

export default {
  data() {
    return {
      icon: 'joomla', //需要再main.js 中注册
      msgs: "降维",
      width: null,
      height: null,
	  svg: null,
      linkdom: null,
      nodedom: null,
	  nodedom_hl: null,
	  nodedom_sel: null,
      xpadding: 50,
      ypadding: 50,
	  padding:{top: 50, bottom: 50, left: 70, right: 70},
	  brush: null,
      x_scale: null,
      y_scale: null,
      latestdata: null,
      hlnodes_hl: [],
      hlnodes_sel: [],
	  nodes_embedded: [],
      curdim2type: 2,
      curoutliertype: null,
      minoutliernum: null,
      maxoutliernum: null,
      nodesrecorded: null,
      nodecolor_abnormal:d3.interpolate(d3.rgb("#EE3B3B"),d3.rgb("#f3bcbc")),
	  nodesImgList: [hostImg, switchImg, serverImg],
	  opts : {
            lines: 8, 
            length: 10, 
            width: 10,
            radius: 15, 
            corners: 1, 
            rotate: 0, 
            direction: 1, 
            color: '#fff', 
			opacity: 0.8,
            speed: 1, 
            trail: 60, 
            shadow: false, 
            hwaccel: false,          
            className: 'spinner', 
            zIndex: 2e9,
            top: '50%',
            left: '50%'
      },
	  spinner : new Spinner(this.opts)
    };
  },
  components: { AppTitle },
  mounted() {
	$("#dim2_wait").hide();
    let self = this;
	let $Div=$("#dimension2_svg");
    self.width=$Div.width();
    self.height=$Div.height();
	self.svg=d3.select("#dimension2_svg")
			.append("svg")
			.attr("width", self.width)
			.attr("height", self.height).append("g");
			
	self.brush = d3.brush().on("end", self.brushended);
	self.svg.append("g")
		.attr("class", "brush")
		.call(self.brush);
		
	self.linkdom = self.svg.append("g").attr("class", "links");
    self.nodedom = self.svg.append("g").attr("class", "nodes");
	self.nodedom_hl = self.svg.append("g").attr("class", "nodes_hl");
	self.nodedom_sel = self.svg.append("g").attr("class", "nodes_sel");
	this.start_angle = 0;
    this.end_angle = 180 * (Math.PI / 180);
	this.arcs_width = 2;
	this.collapsed_color_0 = ["#b72626", "#cd4d40", "#d37053", "#da9155", "#dac385"];
    this.control_color_0 = ["#008475", "#00ba8a", "#4dcf8b", "#9ce28d", "#dff68e"];
	$("#dim2").hide();
  },
  methods: {
	handledim(){
		let newtype=parseInt(document.getElementById("st_dim_redu_func").value);
		if(newtype!=this.curdim2type){
			this.curdim2type=newtype;
			this.getdim2results();
		}
	},
	handleoutlier(){
		let newtype=parseInt(document.getElementById("st_outlier_func").value);
		if(newtype!=this.curoutliertype){
			this.curoutliertype=newtype;
			let obj = {
				type: this.curoutliertype
			};
			CommunicateWithServer('get', obj, 'changeOutlierType', function(){});
		}
	},
	brushended() {
		let self = this;
	    let s = d3.event.selection;
		//console.log(s);
		let nodesselected=[];
		if(s){
			let xmin=_.min([s[0][0], s[1][0]]);
			let xmax=_.max([s[0][0], s[1][0]]);
			let ymin=_.min([s[1][1], s[0][1]]);
			let ymax=_.max([s[1][1], s[0][1]]);
			let nodesall=_.keys(self.latestdata["nodes"]);
			for(let i=0;i<nodesall.length;i++){
				let tmploc=self.latestdata["nodes"][nodesall[i]]["embedded"];
				let tmpx=self.x_scale(tmploc[0]);
				let tmpy=self.y_scale(tmploc[1]);
				if ((tmpx>=xmin && tmpx<=xmax) && (tmpy>=ymin && tmpy<=ymax)){
					nodesselected.push(nodesall[i]);
				}
			}
		}
		console.log(nodesselected);
		//self.$store.state.hlnodes = nodesselected;
		//self.$store.state.hlview = "dim2";
		this.$store.state.nodesSelected=nodesselected;
	},
	setscale(data){
		let nodesall=_.keys(data);
		let featurexmax=data[nodesall[0]]["embedded"][0];
		let featurexmin=featurexmax;
		let featureymax=data[nodesall[0]]["embedded"][1];
		let featureymin=featureymax;
		for(let i=0;i<nodesall.length;i++){
			let locations=data[nodesall[i]]["embedded"];
			let tmpx=locations[0];
			let tmpy=locations[1];
			if(tmpx>featurexmax){featurexmax=tmpx;}
			else if(tmpx<featurexmin){featurexmin=tmpx;}
			if(tmpy>featureymax){featureymax=tmpy;}
			else if(tmpy<featureymin){featureymin=tmpy;}
		}
		this.x_scale = d3.scaleLinear().range([this.padding.left,this.width-this.padding.right]).domain([featurexmin,featurexmax]);
		this.y_scale = d3.scaleLinear().range([this.padding.top,this.height-this.padding.bottom]).domain([featureymin,featureymax]);
	},
	RandomNum(Min,Max){
		let Range = Max - Min;
		let Rand = Math.random();
		let num = Min + Math.round(Rand * Range);
		return num;
	},
	normalize(data,min,max){
		if (min==max){
			return 0.5;
		}else{
			return (data-min)/(max-min);
		}
	},
	drawgraph(evt_data){
		let self = this;
		//=================outlier================	
		self.outlierrecords=evt_data["outlier"];
		self.maxoutliernum=_.max(self.outlierrecords);
		self.minoutliernum=_.min(self.outlierrecords);
		self.nodesrecorded=_.keys(self.outlierrecords);
		//=================draw nodes================
		//let nodesattr=evt_data["nodesattr"];
		let nodesall=_.keys(evt_data["nodes"]);
		let nodesdata=evt_data["nodes"];
		
		self.nodedom.selectAll(".nodeg").remove();
		let circles = self.nodedom.selectAll(".nodeg")
			.data(nodesall)
			.enter().append("g")
			.attr("class","nodeg")
			.attr("transform", (d,i)=>{ 
				let locationdata=nodesdata[d]["embedded"];
				let tmpx=Math.max(0, Math.min(self.x_scale(locationdata[0])+self.RandomNum(-0.02*self.width,0.02*self.width), self.width));
				let tmpy=Math.max(0, Math.min(self.y_scale(locationdata[1])+self.RandomNum(-0.02*self.height,0.02*self.height), self.height));
				return "translate(" + tmpx + "," + tmpy + ")"; 
			})/*
			.on("mouseover",(d,i)=>{
				this.$store.state.hlnodes = [d];
				this.$store.state.hlview = "dim2";
			}).on("mouseout",(d)=>{
				this.$store.state.hlnodes = [];
				this.$store.state.hlview = "dim2";
			})*/
			.on("click",(d)=>{
				let tmpind = this.$store.state.nodesSelected.indexOf(d);
				if (tmpind >= 0) {
				  this.$store.state.nodesSelected.splice(tmpind, 1);
				} else {
				  this.$store.state.nodesSelected.push(d);
				}
			})
		
		let noderadius=8;
		/*circles.append("circle")
			.attr("r", noderadius)
			.attr("fill","#282c37");*/
		
		circles.append("image")
			.attr("xlink:href", (d,i) => {
				let tmptype=nodesdata[d]["nodeType"];
				if (tmptype === "主机") {
				  return this.nodesImgList[0];
				} else if (tmptype === "交换机") {
				  return this.nodesImgList[1];
				} else if (tmptype === "服务器") {
				  return this.nodesImgList[2];
				}
			})
			.attr("x", d => - noderadius)
			.attr("y", d => - noderadius)
			.attr("width", d => noderadius*2)
			.attr("height", d => noderadius*2)
			.append("title").text((d,i)=>{
				return d;
			});
		circles.append("path")
			.attr("d", (d) => {
				let tmp_r = noderadius;
				let arcs = d3.arc().startAngle(this.start_angle).endAngle(this.end_angle)
				  .innerRadius(tmp_r - this.arcs_width / 2).outerRadius(tmp_r + this.arcs_width / 2);
				return arcs(d.data);
            })
            .attr("class", "arc_collapse")
            .attr("fill", (d, i) => {
                return this.collapsed_color_0[i % 5];
            });
		circles.append("path")
			.attr("d", (d) => {
                let tmp_r = noderadius;
                let arcs = d3.arc().startAngle(this.start_angle).endAngle(this.end_angle)
                  .innerRadius(tmp_r - this.arcs_width / 2).outerRadius(tmp_r + this.arcs_width / 2);
                return arcs(d.data);
            }).attr("class", "arc_control")
			.attr("transform", (d) => {
                return "translate(" + (0) + "," + (0) + ")" + "rotate(180)"
            })
            .attr("fill", (d, i) => {
                return this.control_color_0[i % 5];
            });
	},
	getdim2results(){
		let self = this;
		let obj = {
			type: self.curdim2type
		};
		$("#dim2_wait").show(()=>{
			let target= document.getElementById('dim2_wait');
			self.spinner.spin(target);  
		});
		CommunicateWithServer('get', obj, 'getDim2', (evt_data)=>{
			console.log(evt_data);
			$("#dim2_wait").hide();
			self.latestdata=evt_data;
			self.setscale(evt_data["nodes"]);
			self.drawgraph(evt_data);
			$("#dim2").show()
		});
	},
	drawhlnodes(hlnodes,dom){
		let prenodes=this.nodedom.selectAll(".nodeg")["_groups"][0];
		let nodesall=_.keys(this.latestdata["nodes"]);
		
		dom.selectAll(".nodeg_hl").remove();
		let nodeshl=dom.selectAll(".nodeg_hl").data(hlnodes)
			.enter().append("g")
			.attr("class","nodeg_hl")
			.attr("transform", (d)=>{ 
				let tmpid=_.indexOf(nodesall,d);
				return prenodes[tmpid].getAttribute("transform"); 
			})
		let noderadius=8;
		nodeshl.append("circle")
			.attr("r", noderadius)
			.attr("fill","#282c37");
			
		nodeshl.append("image")
			.attr("xlink:href", (d,i) => {
				let tmptype=this.latestdata["nodes"][d]["nodeType"];
				//console.log(tmptype);
				if (tmptype === "主机") {
				  return this.nodesImgList[0];
				} else if (tmptype === "交换机") {
				  return this.nodesImgList[1];
				} else if (tmptype === "服务器") {
				  return this.nodesImgList[2];
				}
			})
			.attr("x", d => - noderadius)
			.attr("y", d => - noderadius)
			.attr("width", d => noderadius*2)
			.attr("height", d => noderadius*2)
			.append("title").text((d,i)=>{
				return d;
			});
		nodeshl.append("path")
			.attr("d", (d) => {
				let tmp_r = noderadius;
				let arcs = d3.arc().startAngle(this.start_angle).endAngle(this.end_angle)
				  .innerRadius(tmp_r - this.arcs_width / 2).outerRadius(tmp_r + this.arcs_width / 2);
				return arcs(d.data);
            })
            .attr("class", "arc_collapse")
            .attr("fill", (d, i) => {
                return this.collapsed_color_0[i % 5];
            });
		nodeshl.append("path")
			.attr("d", (d) => {
                let tmp_r = noderadius;
                let arcs = d3.arc().startAngle(this.start_angle).endAngle(this.end_angle)
                  .innerRadius(tmp_r - this.arcs_width / 2).outerRadius(tmp_r + this.arcs_width / 2);
                return arcs(d.data);
            }).attr("class", "arc_control")
			.attr("transform", (d) => {
                return "translate(" + (0) + "," + (0) + ")" + "rotate(180)"
            })
            .attr("fill", (d, i) => {
                return this.control_color_0[i % 5];
            });
		
			
	}
  },
  computed: {
    timeupdated: function() {
      return this.$store.state.timeupdated
    },
	hlnodes:function() {
      return this.$store.state.hlnodes
    }/*,
	nodesSelected:function() {
      return this.$store.state.nodesSelected
    }*/
  },
  watch: {
    timeupdated: function(newVal, oldVal) {
      this.getdim2results();
    },
	hlnodes: function(newVal, oldVal) {
	  if(this.latestdata!=null){
		  if(this.$store.state.hlview!="dim2"){
			  this.hlnodes_hl=newVal;
			  if(newVal.length==0){
				  this.nodedom.selectAll(".nodeg").attr("opacity",1);
			  }else{
				  this.nodedom.selectAll(".nodeg").attr("opacity",0.1);
				  this.drawhlnodes(this.hlnodes_hl,this.nodedom_hl);
			  }
		  }
	  }
	  
    }/*,
	nodesSelected: function(newVal, oldVal) {
	  this.hlnodes_sel=newVal;
	  if(newVal.length==0){
		  this.nodedom.selectAll(".nodeg").attr("opacity",1);
	  }else{
		  this.nodedom.selectAll(".nodeg").attr("opacity",0.1);
		  this.drawhlnodes(this.hlnodes_sel,this.nodedom_sel);
	  }
	}*/
  }
};

</script>
<style lang="less" scoped>
@import "./AppDimension.less";

</style>
