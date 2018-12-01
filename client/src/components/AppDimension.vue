<template>
  <div>
  <div id="dim2-panel">
    <app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
    <div id="dimension2_btn" class="btn-div">
		DimReduce:&nbsp;&nbsp;
		<select id="st_dim_redu_func" @click="handledim">
		  <option value="0"selected = "selected"><span>PCA</span></option>
		  <option value="1"><span>ICA</span></option>
		  <option value="2" ><span>t-SNE</span></option>
		</select>
		&nbsp;&nbsp;
		Outlier Detection:&nbsp;&nbsp;
		<select id="st_outlier_func" @click="handleoutlier">
		  <option value="0"selected = "selected"><span>EllipticEnvelope</span></option>
		  <option value="1"><span>BayesianGMM</span></option>
		</select>
	</div>
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
      xpadding: 30,
      ypadding: 50,
	  brush: null,
      x_scale: null,
      y_scale: null,
      latestdata: null,
      hlnodes_hl: [],
      hlnodes_sel: [],
      curdim2type: 0,
      curoutliertype: null,
      minoutliernum: null,
      maxoutliernum: null,
      nodesrecorded: null,
      nodecolor_abnormal:d3.interpolate(d3.rgb("#EE3B3B"),d3.rgb("#f3bcbc")),
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
			.attr("height", self.height);
			
	self.brush = d3.brush().on("end", self.brushended);
	self.svg.append("g")
		.attr("class", "brush")
		.call(self.brush);
		
	self.linkdom = self.svg.append("g").attr("class", "links");
    self.nodedom = self.svg.append("g").attr("class", "nodes");

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
			for(let i=0;i<self.latestdata["nodes_embedded"].length;i++){
				let tmpx=self.x_scale(self.latestdata["nodes_embedded"][i][0]);
				let tmpy=self.y_scale(self.latestdata["nodes_embedded"][i][1]);
				if ((tmpx>=xmin && tmpx<=xmax) && (tmpy>=ymin && tmpy<=ymax)){
					nodesselected.push(self.latestdata["nodes"][i]);
				}
			}
		}
		console.log(nodesselected);
		self.$store.state.hlnodes = nodesselected;
		self.$store.state.hlview = "dim2";
	},
	setscale(data){
		let self = this;
		let featurexmax=_.max(data, (f)=>{ return f[0]; })[0];
		let featurexmin=_.min(data, (f)=>{ return f[0]; })[0];
		let featureymax=_.max(data, (f)=>{ return f[1]; })[1];
		let featureymin=_.min(data, (f)=>{ return f[1]; })[1];
		
		self.x_scale = d3.scaleLinear().range([self.xpadding,self.width-self.xpadding]).domain([featurexmin,featurexmax]);
		self.y_scale = d3.scaleLinear().range([self.ypadding,self.height-self.ypadding]).domain([featureymin,featureymax]);
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
		self.nodedom.selectAll("circle").remove();
		let circles=self.nodedom.selectAll("circle").data(evt_data["nodes_embedded"])
			.enter().append("circle")//.attr("id",function(d,i){return "nodes_"+d.id;})
			.attr("fill", (d,i)=>{
				let tmpnode=evt_data["nodes"][i];
				return self.nodesmap(tmpnode,0);
			})
			.attr("stroke","#555")
			.attr("r", 3)
			.attr("cx", (d,i)=>{return self.x_scale(d[0]);})
			.attr("cy", (d,i)=>{return self.y_scale(d[1]);})
			.on("mouseover",(d,i)=>{
				self.$store.state.hlnodes = [evt_data["nodes"][i]];
				self.$store.state.hlview = "dim2";
			}).on("mouseout",(d,i)=>{
				self.$store.state.hlnodes = [];
				self.$store.state.hlview = "dim2";
			});
		circles.append("title")
			    .text((d,i)=>{
				  return evt_data["nodes"][i];
				});	
	},
	nodesmap(id,color0r1){
		let self = this;
		if(_.contains(self.hlnodes_hl, id)){
			if(color0r1==0){
				return "#b8ddf3";
			}else{
				return 6;
			}
		}else if(_.contains(self.hlnodes_sel, id)){
			if(color0r1==0){
				return "#87CEFA";
			}else{
				return 6;
			}
		}else{
			if(color0r1==0){
				if(_.contains(self.nodesrecorded,id+"")){
					let tmpnewdata=self.normalize(self.outlierrecords[id],self.minoutliernum,self.maxoutliernum);
					return self.nodecolor_abnormal(tmpnewdata);
				}else{
					return "white";
				}
			}else{
				return 3;
			}
		}
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
			//console.log(evt_data);
			$("#dim2_wait").hide();
			self.latestdata=evt_data;
			self.setscale(evt_data["nodes_embedded"]);
			self.drawgraph(evt_data);
		});
	}
  },
  computed: {
    timeupdated: function() {
      return this.$store.state.timeupdated
    },
	hlnodes:function() {
      return this.$store.state.hlnodes
    },
	nodesSelected:function() {
      return this.$store.state.nodesSelected
    }
  },
  watch: {
    timeupdated: function(newVal, oldVal) {
      this.getdim2results();
    },
	hlnodes: function(newVal, oldVal) {
	  if(this.$store.state.hlview!="dim2"){
		  this.hlnodes_hl=newVal;
		  this.nodedom.selectAll("circle").attr("r", (d,i)=>{return this.nodesmap(this.latestdata["nodes"][i],1);})
			.attr("fill", (d,i)=>{return this.nodesmap(this.latestdata["nodes"][i],0);})
	  }
    },
	nodesSelected: function(newVal, oldVal) {
	  this.hlnodes_sel=newVal;
	  this.nodedom.selectAll("circle").attr("r", (d,i)=>{return this.nodesmap(this.latestdata["nodes"][i],1);})
			.attr("fill", (d,i)=>{return this.nodesmap(this.latestdata["nodes"][i],0);})
    }
  }
};

</script>
<style lang="less" scoped>
@import "./AppDimension.less";

</style>
