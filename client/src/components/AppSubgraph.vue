<template>
	<div id="subgraph-panel" class="outer-div">
		<app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
		<div id="subgraph-inner">
			<div id="subgraph_svg"></div>
		</div>
	</div>
</template>
<script>

import AppTitle from "./AppTitle.vue";
import hostImg from "../assets/host.png";
import switchImg from "../assets/switch.png";
import serverImg from "../assets/server.png";
const d3 = require("d3");
const $ = require("jquery");
const _ = require("underscore");

export default {
  data() {
    return {
      icon: 'joomla', //需要再main.js 中注册
      msgs: "邻居节点/最短路径",
      width: null,
      height: null,
	  svg: null,
	  highlightnodes:[],
	  selectednodes:[],
	  showntype:-1,
	  d3tree:null,
	  d3cluster:null,
	  nodesImgList: [hostImg, switchImg, serverImg],
	  padding:{top: 20, bottom: 20, left: 50, right: 50},
	  timeset:{"starttime": 1468561795, "curtime": 1468561795, "endtime": 1468633627, "timestep": 60,"timewindow": 60}
    };
  },
  components: { AppTitle },
  mounted() {
    let self = this;
	let $Div=$("#subgraph_svg");
    self.width=$Div.width();
	self.height=$Div.height();
	self.svg=d3.select("#subgraph_svg")
			.append("svg")
			.attr("width", self.width)
			.attr("height", self.height);
	self.d3tree = d3.tree()
		.size([self.height-self.padding.top-self.padding.bottom, (self.width-self.padding.left-self.padding.right)*0.25]);
	self.d3cluster = d3.cluster()
		.size([self.height-self.padding.top-self.padding.bottom, (self.width-self.padding.left-self.padding.right)*0.25]);
	this.start_angle = 0;
    this.end_angle = 180 * (Math.PI / 180);
	this.arcs_width = 2;
	this.collapsed_color_0 = ["#b72626", "#cd4d40", "#d37053", "#da9155", "#dac385"];
    this.control_color_0 = ["#008475", "#00ba8a", "#4dcf8b", "#9ce28d", "#dff68e"];
  },
  methods: {
	diagonal(d) {
	    return "M" + d.y + "," + d.x
		  + "C" + (d.parent.y + 100) + "," + d.x
		  + " " + (d.parent.y + 100) + "," + d.parent.x
		  + " " + d.parent.y + "," + d.parent.x;
	},
	curvepath(d) {
      let x0 = d.source[0],
          x1 = d.target[0],
          xi = d3.interpolateNumber(x0, x1),
          x2 = xi(0.5),
          x3 = xi(1 - 0.5),
          y0 = d.source[1] ,
          y1 = d.target[1] ;
      return "M" + x0 + "," + y0
           + "C" + x2 + "," + y0
           + " " + x3 + "," + y1
           + " " + x1 + "," + y1;
    },
	inttime2str(num){
		let str;
		let t = new Date(num*1000);
		if (t.getMinutes()<10){
			str=(t.getMonth()+1)+"/"+t.getDate()+" "+t.getHours()+":"+"0"+t.getMinutes();
		}else{
			str=(t.getMonth()+1)+"/"+t.getDate()+" "+t.getHours()+":"+t.getMinutes();
		}
		return str;
	},
	singleNeighbor(rootnode,nodesappears,nodesattr){
		let root=_.map(nodesappears, (val, key)=>{ return {"name":key,"parent":rootnode}; });
		root.push({name: rootnode, parent: ""});
		let treeroot = d3.stratify()
			.id((d)=>{ return d.name; })
			.parentId((d)=>{ return d.parent; })
			(root);
		this.d3cluster(treeroot);
		let nodesdata=treeroot.descendants().reverse();
		let linkdata=treeroot.descendants().slice(1);
		this.d3tree(treeroot);
		
		let locations={};
		
		this.svg.selectAll("g").remove();
		let g=this.svg.append("g")
			.attr("transform", (d)=>{ return "translate(" + this.padding.left + "," + this.padding.top + ")"; });
		
		let links = g.selectAll(".treelink")
			.data(linkdata)
			.enter().append("path")
			.attr("class", "treelink")
			.attr("d", this.diagonal).attr("fill","none").attr("stroke","#999");
		let node = g.selectAll(".nodeg")
			.data(nodesdata)
			.enter().append("g")
			.attr("class","nodeg")
			.attr("transform", (d)=>{ 
				locations[d.data.name]=d.x;
				return "translate(" + d.y + "," + d.x + ")"; 
			})
			.on("mouseover",(d)=>{
				this.$store.state.hlnodes = [d.data.name];
				this.$store.state.hlview = "subgraph";
			}).on("mouseout",(d)=>{
				this.$store.state.hlnodes = [];
				this.$store.state.hlview = "subgraph";
			})
		var noderadius=8;
		node.append("circle")
			.attr("r", noderadius)
			.attr("fill","#282c37");
			
		node.append("image")
			.attr("xlink:href", d => {
				let tmptype=nodesattr[d.data.name]["nodeType"];
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
				return d.data.name;
			});
		node.append("path")
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
		node.append("path")
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
		g.append("text").attr("x",-this.padding.left)
			.attr("y",this.height/2-this.padding.top-2*noderadius)
			.text(nodesdata[0].data.name)
			.attr("fill","grey").attr("font-size","14px");
		//console.log(locations);
		
		let innerpadding=15;
		let timew=this.width-(this.padding.left+this.d3cluster.size()[1]+innerpadding)-this.padding.right;
		let timenumall=Math.ceil((this.timeset["endtime"]-this.timeset["starttime"])/this.timeset["timestep"]);
		let timerange=_.values(nodesappears);
		let timerangemax=_.map(timerange, (d)=>{ return d[d.length-1][1]; });
		timerangemax=_.max(timerangemax);
		let timerangemin=_.map(timerange, (d)=>{ return d[0][0]; });
		timerangemin=_.min(timerangemin);
		//console.log(timerangemin,timerangemax);
		
		let timeScale= d3.scaleLinear()
			  .domain([timerangemin,timerangemax])
			  .range([0, this.width-this.d3cluster.size()[1]-this.padding.left-this.padding.right]);
		
		let allneighbors=_.keys(nodesappears);
		let strokewidth=5;
		if((this.height-this.padding.top-this.padding.bottom)/allneighbors.length-2<strokewidth){
			strokewidth=(this.height-this.padding.top-this.padding.bottom)/allneighbors.length-2;
		}
		for(let i=0;i<allneighbors.length;i++){
			let timesg=this.svg.append("g")
				.attr("transform", (d)=>{ return "translate(" + (this.padding.left+this.d3cluster.size()[1]+innerpadding) + "," + this.padding.top + ")"; });
			timesg.selectAll("line").data(nodesappears[allneighbors[i]])
				.enter().append("line")
				.attr("class","timeappear")
				.attr("x1",(d,ii)=>{
					return timeScale(d[0]);
				}).attr("y1",(d,ii)=>{
					return locations[allneighbors[i]];
				}).attr("x2",(d,ii)=>{
					return timeScale(d[1]);
				}).attr("y2",(d,ii)=>{
					return locations[allneighbors[i]];
				}).attr("stroke","#999").attr("stroke-width",strokewidth)
				.attr("stroke-linecap","round")
				.append("title").text((d,i)=>{
					return this.inttime2str(this.timeset["starttime"]+d[0]*this.timeset["timestep"])+" - "+this.inttime2str(this.timeset["starttime"]+d[1]*this.timeset["timestep"]);
				});
		}
		
	},
	multipsps(nodessps,nodesrecord,nodesattr){
		this.svg.selectAll("g").remove();
		if(nodessps.length==0){
			return;
		}
		
		//console.log(nodessps);
		let maxlen=_.map(nodessps, (d)=>{ return d[0][0].length; });
		let lensum=0;
		for(let i=0;i<maxlen.length;i++){
			lensum=lensum+maxlen[i];
		}

		let corey=(this.height-this.padding.top-this.padding.bottom)/2;
		let corex=[0];
		for(let i=0;i<maxlen.length;i++){
			let tmpx=(this.width-this.padding.left-this.padding.right)/lensum*maxlen[i];
			corex.push(corex[corex.length-1]+tmpx);
		}
		
		let linkdata=[];
		var nodesrecord_new=[];
		let nodespos={};
		let corenodes=[nodessps[0][0][0]+"_0"];
		for(let i=0;i<nodessps.length;i++){
			let pathnum=nodessps[i].length;	
			let availw=corex[i+1]-corex[i];
			for(let pi=0;pi<pathnum;pi++){
				let cury;
				if(pathnum==1){
					cury=(this.height-this.padding.top-this.padding.bottom)/2;
				}else{
					cury=(this.height-this.padding.top-this.padding.bottom)/(pathnum-1)*(pi);
				}
				let pathlen=nodessps[i][pi].length;
					
				for(let ni=0;ni<pathlen-1;ni++){
					nodesrecord_new.push(nodesrecord[i][pi][ni]);
					
					let tmpnx1=0; let tmpny1=0;
					let tmpnx2=0; let tmpny2=0;
					let tmpnode1=nodessps[i][pi][ni];
					let tmpnode2=nodessps[i][pi][ni+1];

					let tmpkey1=tmpnode1+"_"+i;
					if(i!=0 && ni==0){
						tmpkey1=tmpnode1+"_"+(i-1);
					}
					if(_.indexOf(_.keys(nodespos),tmpkey1)>=0){
						tmpnx1=nodespos[tmpkey1][0];
						tmpny1=nodespos[tmpkey1][1];
						
					}else{
						tmpnx1=(this.padding.left+corex[i])+(availw/(pathlen-1))*(ni);
						tmpny1=cury;
						if(ni==0){tmpny1=(this.height-this.padding.top-this.padding.bottom)/2;}
						nodespos[tmpkey1]=[tmpnx1,tmpny1];
					}
					let tmpkey2=tmpnode2+"_"+i;
					if(_.indexOf(_.keys(nodespos),tmpkey2)>=0){
						tmpnx2=nodespos[tmpkey2][0];
						tmpny2=nodespos[tmpkey2][1];
					}else{
						tmpnx2=(this.padding.left+corex[i])+(availw/(pathlen-1))*(ni+1);
						tmpny2=cury;
						if(ni+1==pathlen-1){
							corenodes.push(tmpkey2);
							tmpny2=(this.height-this.padding.top-this.padding.bottom)/2;
						}
						nodespos[tmpkey2]=[tmpnx2,tmpny2];
					}
					linkdata.push({"source":[tmpnx1,tmpny1,tmpkey1],"target":[tmpnx2,tmpny2,tmpkey2]});
				}
			}
		}
		//console.log(linkdata);
		//console.log(nodesrecord_new);
		
		for(let i=0;i<linkdata.length;i++){
			let tmpleft=linkdata[i]["source"][0];
			let tmpwidth=linkdata[i]["target"][0]-tmpleft;
			let tmpsrctop=linkdata[i]["source"][1];
			let tmpdsttop=linkdata[i]["target"][1];
			this.svg.append("g")
				.attr("transform", (d)=>{ return "translate(" + (0) + "," + this.padding.top + ")"; })
				.selectAll("line").data(nodesrecord_new[i])
				.enter().append("line")
				.attr("class", "link")
				.attr("x1",(dd,ii)=>{
					return tmpleft+tmpwidth/nodesrecord_new[i].length*ii;
				}).attr("x2",(dd,ii)=>{
					return tmpleft+tmpwidth/nodesrecord_new[i].length*(ii+1);
				}).attr("y1",(dd,ii)=>{
					return tmpsrctop+(tmpdsttop-tmpsrctop)/nodesrecord_new[i].length*ii;
				}).attr("y2",(dd,ii)=>{
					return tmpsrctop+(tmpdsttop-tmpsrctop)/nodesrecord_new[i].length*(ii+1);
				}).attr("stroke",(dd,ii)=>{
					if(dd>0){return "#999";}
					else{return "#616161";}
				})
				.attr("stroke-width",2)
				.attr("stroke-dasharray",(dd,ii)=>{
					if(dd>0){return null;}
					else{return 5;}
				})
				.append("title").text((dd,ii)=>{
					return this.inttime2str(this.timeset["starttime"]+ii*this.timeset["timestep"])+" - "+this.inttime2str(this.timeset["starttime"]+(ii+1)*this.timeset["timestep"]);
				});
		}
		//console.log(nodespos);
		
		let nodesdom=this.svg.append("g")
			.selectAll(".nodeg")
			.data(_.keys(nodespos))
			.enter().append("g")
			.attr("class","nodeg")
			.attr("transform", (d)=>{ return "translate(" + (nodespos[d][0]) + "," + (this.padding.top+nodespos[d][1]) + ")"; })
			/*.on("mouseover",(d)=>{
				let name=d.split("_");
				name.pop();
				this.$store.state.hlnodes = [name.join("_")];
				this.$store.state.hlview = "subgraph";
			}).on("mouseout",(d)=>{
				this.$store.state.hlnodes = [];
				this.$store.state.hlview = "subgraph";
			})*/
			.on("click",(d)=>{
				let name=d.split("_");
				name.pop()
				let nodeid=name.join("_");
				let tmpind = this.$store.state.nodesSelected.indexOf(nodeid);
				if (tmpind >= 0) {
				  this.$store.state.nodesSelected.splice(tmpind, 1);
				} else {
				  this.$store.state.nodesSelected.push(nodeid);
				}
				//console.log(this.$store.state.nodesSelected);
			})
		var noderadius=8;
		nodesdom.append("circle")
			.attr("r", noderadius)
			.on("mouseover",(d)=>{
				this.$store.state.hlnodes = d.data.name;
				this.$store.state.hlview = "subgraph";
			}).on("mouseout",(d)=>{
				this.$store.state.hlnodes = [];
				this.$store.state.hlview = "subgraph";
			}).attr("fill","#282c37");
			
		nodesdom.append("image")
			.attr("xlink:href", d => {
				let name=d.split("_");
				name.pop();
				name=name.join("_");
				let tmptype=nodesattr[name]["nodeType"];
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
				let name=d.split("_");
				name.pop();
				return name.join("_");
			});
		nodesdom.append("path")
			.attr("d", (d) => {
				let tmp_r = noderadius;
				let arcs = d3.arc().startAngle(this.start_angle).endAngle(this.end_angle)
				  .innerRadius(tmp_r - this.arcs_width / 2).outerRadius(tmp_r + this.arcs_width / 2);
				return arcs(d);
            })
            .attr("class", "arc_collapse")
            .attr("fill", (d, i) => {
                return this.collapsed_color_0[i % 5];
            });
		nodesdom.append("path")
			.attr("d", (d) => {
                let tmp_r = noderadius;
                let arcs = d3.arc().startAngle(this.start_angle).endAngle(this.end_angle)
                  .innerRadius(tmp_r - this.arcs_width / 2).outerRadius(tmp_r + this.arcs_width / 2);
                return arcs(d);
            }).attr("class", "arc_control")
			.attr("transform", (d) => {
                return "translate(" + (0) + "," + (0) + ")" + "rotate(180)"
            })
            .attr("fill", (d, i) => {
                return this.control_color_0[i % 5];
            });
		nodesdom.append("text")
			.attr("dy",-2*noderadius).attr("dx",-this.padding.left)
			.text((d)=>{
				if(_.indexOf(corenodes,d)>=0){
					let name=d.split("_");
					name.pop();
					return name.join("_");
				}else{return null;}
			}).attr("fill","grey").attr("font-size","14px");
	}
  },
  
  computed: {
    nodesSelected: function() {
      return this.$store.state.nodesSelected
    },
	hlnodes:function() {
      return this.$store.state.hlnodes
    }
  },
  watch: {
    nodesSelected: function(newVal, oldVal) {
	  this.selectednodes=newVal;
	  let obj = {nodes: this.selectednodes};
	  
	  if(this.selectednodes.length==0){
		  this.showntype=-1;
		  this.svg.selectAll("g").remove();
		  CommunicateWithServer('get', obj, "choosenone", ()=>{});
	  }else if(this.selectednodes.length==1){
		  	this.showntype=0;
			CommunicateWithServer('get', obj, 'gettree', (evt_data)=>{
				console.log(evt_data);
				this.singleNeighbor(evt_data["root"],evt_data["appear"],evt_data["nodes"]);
			});
	  }else{
		    this.showntype=1;
			CommunicateWithServer('get', obj, 'getSPs', (evt_data)=>{
				console.log(evt_data);
				this.multipsps(evt_data["paths"],evt_data["records"],evt_data["nodes"]);
		    })
	  }
    },
	hlnodes: function(newVal, oldVal) {
	  if(this.$store.state.hlview!="subgraph"){
		this.highlightnodes=newVal;
		if(this.highlightnodes.length!=0){
			if(this.showntype==0){//single node
				this.svg.selectAll(".nodeg").attr("opacity",(d)=>{
					if(_.indexOf(this.highlightnodes,d.data.name)>=0){
						return 1;
					}else{
						return 0.2;
					}
				})
			}else if(this.showntype==1){//multi nodes
				this.svg.selectAll(".nodeg").attr("opacity",(d)=>{
					let tmpname=d.split("_");
					tmpname.pop();
					tmpname=tmpname.join("_");
					if(_.indexOf(this.highlightnodes,tmpname)>=0){
						return 1;
					}else{
						return 0.2;
					}
				})
			}
		}else{
			this.svg.selectAll(".nodeg").attr("opacity",1);
		}
		
	  }
    }
  }
};

</script>
<style lang="less" scoped>
@import "./AppSubgraph.less";

</style>
