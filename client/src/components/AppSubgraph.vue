<template>
	<div id="subgraph-panel" class="outer-div">
		<app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
		<div id="subgraph-inner">
			<div id="subgraph_left">
				<table border="0" width="100%">
					<tr>
						<td><span id="left_btn" @click="handleleft"><font-awesome-icon icon="chevron-left" size="xs" :style="{ color: 'grey' }"/></span></td>
					</tr>
					<tr>
						<td><span id="leftmax_btn" @click="handleleftmax"><font-awesome-icon icon="backward" size="xs" :style="{ color: 'grey' }"/></span></td>
					</tr>
				</table>
			</div>
			<div id="subgraph_svg"></div>
			<div id="subgraph_right">
				<table border="0" width="100%">
					<tr>
						<td><span id="right_btn" @click="handleright"><font-awesome-icon icon="chevron-right" size="xs" :style="{ color: 'grey' }"/></span></td>
					</tr>
					<tr>
						<td><span id="rightmax_btn" @click="handlerightmax"><font-awesome-icon icon="forward" size="xs" :style="{ color: 'grey' }"/></span></td>
					</tr>
				</table>
			</div>
		</div>
	</div>
</template>
<script>

import AppTitle from "./AppTitle.vue";
const d3 = require("d3");
const $ = require("jquery");
const _ = require("underscore");

export default {
  data() {
    return {
      icon: 'joomla', //需要再main.js 中注册
      msgs: "树/路径/子图",
      width: null,
      height: null,
	  svg: null,
      padding_w: 20,
      padding_h: 40,
	  none0tree1sub2:0,
	  links_dom:null,
	  nodes_dom:null,
	  texts:null,
	  sub_Gs:[],
	  subg_nodes_g:[],
	  subg_edges_g:[],
	  subg_texts_g:[],
	  timelinetext:null,
	  cuttingline:null,
	  maxshownnum:3,
	  curstartnum:0,
	  subGwidth:0,
	  subGheight:0,
	  highlightnodes:[],
	  highlightnodes_sel:[],
	  d3tree:null,
	  d3cluster:null
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
	self.links_dom= self.svg.append("g").attr("transform", "translate(" + 40 + "," + 15 + ")");
	self.nodes_dom= self.svg.append("g").attr("transform", "translate(" + 40 + "," + 15 + ")");
	self.timelinetext=self.svg.append("g");
	self.cuttingline=self.svg.append("g");
	self.subGwidth=(self.width-2*self.padding_w-(self.maxshownnum-1)*self.padding_w)/self.maxshownnum;
	self.subGheight=self.height-2*self.padding_h;
	self.d3tree = d3.tree()
		.size([self.height - 30, self.width - 80]);
	self.d3cluster = d3.cluster()
		.size([self.height, self.width - 80]);
  },
  methods: {
	diagonal(d) {
	    return "M" + d.y + "," + d.x
		  + "C" + (d.parent.y + 100) + "," + d.x
		  + " " + (d.parent.y + 100) + "," + d.parent.x
		  + " " + d.parent.y + "," + d.parent.x;
	},
	updatetree(source,root){
		let duration=500;
		let nodesdata=root.descendants().reverse();
		let linkdata=root.descendants().slice(1);
		this.d3tree(root);
		nodesdata.forEach((d)=> {
			d.x0 = d.x;
			d.y0 = d.y;
		});
		let nodes = this.nodes_dom.selectAll(".node")
			.data(nodesdata, (d)=>{ return d.id ; });
		// Enter any new nodes at the parent's previous position.
		let nodeEnter = nodes.enter().append("g")
			.attr("class", "node")
			.attr("transform", (d)=>{ return "translate(" + source.y0 + "," + source.x0 + ")"; })
			.on("click", (d)=>{
				if(d.depth!=0){
					d.children = d.children ? null : d._children;
					this.updatetree(d,root);
				}
			});
		nodeEnter.append("circle")
			.attr("r", (d)=>{return this.circlefill(parseInt(d.id),1);})
			.attr("fill",(d)=>{return this.circlefill(parseInt(d.id),0);})
			.on("mouseover",(d)=>{
				this.$store.state.hlnodes = [parseInt(d.id)];
				this.$store.state.hlview = "subgraph";
			}).on("mouseout",(d)=>{
				this.$store.state.hlnodes = [];
				this.$store.state.hlview = "subgraph";
			});
			
		nodeEnter.append("text")
			.attr("font-family", "sans-serif")
			.attr("font-size", 12)
			.attr("dy", 3)
			.attr("x", (d)=>{ return d.children || d._children ? -15 : 15; })
			.style("text-anchor", (d)=>{ return (d.children || d._children) ? "end" : "start"; })
			.text((d)=>{ return d.id.substring(d.id.lastIndexOf(".") + 1); });
		
		// Transition nodes to their new position.
		let nodeUpdate = nodes.merge(nodeEnter)
				.transition().duration(duration)
				.attr("transform", (d)=>{ return "translate(" + d.y + "," + d.x + ")"; });
		// Stash the old positions for transition.
		let nodeExit = nodes.exit()
			.transition().duration(duration).remove()
			.attr("transform", (d)=>{ return "translate(" + source.y + "," + source.x + ")"; });
		
		let links=this.links_dom.selectAll(".treelink")
			.data(linkdata);
		let linkEnter=links.enter().append("path")
			.attr("class", "treelink")
			.attr("d", this.diagonal)
			.attr("fill","none");
		links.merge(linkEnter).transition().duration(duration)
			.attr("d", this.diagonal);
		links.exit().transition().duration(duration).remove()
			.attr("d", d => {
			  return this.diagonal({parent: {x: source.x, y: source.y}, x: source.x, y: source.y});
			});
		this.svg.selectAll(".treelink").attr("stroke","grey").attr("fill","none");
		this.svg.selectAll("text").attr("fill","grey");
	},
	handleleft(){
		if(this.sub_Gs.length>this.maxshownnum){
			if(this.curstartnum>0){
				this.curstartnum=this.curstartnum-1;
				this.turnleft();
				this.adjust_positions();
				this.drawsubgraph(this.subg_edges_g[0],this.subg_nodes_g[0],this.subg_texts_g[0],this.sub_Gs[this.curstartnum][1],this.sub_Gs[this.curstartnum][0],this.subGwidth,this.subGheight);
			}
		}
	},
	handleright(){
		if(this.sub_Gs.length>this.maxshownnum){
			if(this.curstartnum<this.maxshownnum-1){
				this.curstartnum=this.curstartnum+1;
				this.turnright();
				this.adjust_positions();
				let tmplen=this.subg_nodes_g.length;
				this.drawsubgraph(this.subg_edges_g[tmplen-1],this.subg_nodes_g[tmplen-1],this.subg_texts_g[tmplen-1],this.sub_Gs[this.curstartnum+this.maxshownnum-1][1],this.sub_Gs[this.curstartnum+this.maxshownnum-1][0],this.subGwidth,this.subGheight);
			}
		}
	},
	handleleftmax(){
		if(this.sub_Gs.length>this.maxshownnum){
			if(this.curstartnum>0){
				if(this.curstartnum-this.maxshownnum+1<=0){
					//有重叠
					for(let i=0;i<this.curstartnum;i++){
						this.turnleft();
						this.drawsubgraph(this.subg_edges_g[0],this.subg_nodes_g[0],this.subg_texts_g[0],this.sub_Gs[this.curstartnum-i-1][1],this.sub_Gs[this.curstartnum-i-1][0],this.subGwidth,this.subGheight);
					}
					curstartnum=0;
				}else{
					console.log("redraw all subgraph");
					for(let i=0;i<this.subg_nodes_g.length;i++){
						this.subg_nodes_g[i].selectAll("circle").remove();
						this.subg_edges_g[i].selectAll("line").remove();
						this.subg_texts_g[i].selectAll("text").remove();
					}
					this.subg_nodes_g=[];this.subg_edges_g=[];this.subg_texts_g=[];
					this.curstartnum=0;
					for(let i=0;i<maxshownnum;i++){
						this.subg_nodes_g.push(this.svg.append("g").attr("class", "nodes"));
						this.subg_edges_g.push(this.svg.append("g").attr("class", "links"));
						this.subg_texts_g.push(this.svg.append("g"));
						this.drawsubgraph(this.subg_edges_g[i],this.subg_nodes_g[i],this.subg_texts_g[i],this.sub_Gs[this.curstartnum+i][1],this.sub_Gs[this.curstartnum+i][0],this.subGwidth,this.subGheight);
					}
				}
				this.adjust_positions();
			}
		}
	},
	handlerightmax(){
		if(this.sub_Gs.length>this.maxshownnum){
			if(this.curstartnum<this.maxshownnum-1){
				this.showsubgraph(1);
			}
		}
	},
	draw_cuttinglines(){
		let tmpdata=[];
		for(let i=0;i<this.maxshownnum-1;i++){
			tmpdata.push(0);
		}
		this.cuttingline.selectAll("line").remove();
		this.cuttingline.selectAll("line")
			.data(tmpdata).enter()
			.append("line")
			.attr("stroke","#aaa")
			.attr("x1", (d,i)=> { return (i+1.5)*this.padding_w+(i+1)*this.subGwidth; })
			.attr("y1", (d,i)=> { return this.padding_h; })
			.attr("x2", (d,i)=> { return (i+1.5)*this.padding_w+(i+1)*this.subGwidth; })
			.attr("y2", (d,i)=> { return this.height-this.padding_h; });
	},
	turnleft(){
		let tmp=this.subg_nodes_g.pop();
		tmp.remove();
		tmp=this.subg_edges_g.pop();
		tmp.remove();
		tmp=sthis.ubg_texts_g.pop();
		tmp.remove();
		this.subg_edges_g.unshift(this.svg.append("g").attr("class", "links"));
		this.subg_nodes_g.unshift(this.svg.append("g").attr("class", "nodes"));
		this.subg_texts_g.unshift(this.svg.append("g"));
	},
	turnright(){
		let tmp=this.subg_nodes_g.shift();
		tmp.remove();
		tmp=this.subg_edges_g.shift();
		tmp.remove();
		tmp=this.subg_texts_g.shift();
		tmp.remove();
		this.subg_edges_g.push(this.svg.append("g").attr("class", "links"));
		this.subg_nodes_g.push(this.svg.append("g").attr("class", "nodes"));
		this.subg_texts_g.push(this.svg.append("g"));
	},
	circlefill(id,color0r1){
		if(this.highlightnodes_sel.length>=3){
			if(color0r1==0){
				return "white";
			}else{
				return 3;
			}
		}else{
			if(_.contains(this.highlightnodes, id)){
				if(color0r1==0){
					return "#b8ddf3";
				}else{
					return 5;
				}
			}else if(_.contains(this.highlightnodes_sel, id)){
				if(color0r1==0){
					return "#87CEFA";
				}else{
					return 5;
				}
			}else{
				if(color0r1==0){
					return "white";
				}else{
					return 3;
				}
			}
		}
	},
	adjust_positions(){
		//console.log(subg_nodes_g);
		for(let i=0;i<this.subg_nodes_g.length;i++){
			this.subg_nodes_g[i].attr("transform", "translate(" + ((i+1)*this.padding_w+i*this.subGwidth)+ "," + this.padding_h + ")");
			this.subg_texts_g[i].attr("transform", "translate(" + ((i+1)*this.padding_w+i*this.subGwidth)+ "," + this.padding_h + ")");
			this.subg_edges_g[i].attr("transform", "translate(" + ((i+1)*this.padding_w+i*this.subGwidth)+ "," + this.padding_h + ")");
		}
		this.drawtimelinetext();
		this.draw_cuttinglines();
	},
	drawtimelinetext(){
		let tmpdata=[];
		for(let i=this.curstartnum;i<this.sub_Gs.length;i++){
			tmpdata.push(i+1);
		}
		//console.log(tmpdata);
		this.timelinetext.selectAll("text").remove();
		this.timelinetext.selectAll("text").data(tmpdata)
			.enter()
			.append("text")
			.attr("font-family", "sans-serif")
			.attr("fill", "grey")
			.attr("font-size", 12)
			.attr("x",(d,i)=>{return (i+1)*this.padding_w+i*this.subGwidth+0.5*this.subGwidth;})
			.attr("y",(d,i)=>{return this.height-this.padding_h;})
			.attr("dx", 0)
			.attr("dy", "0.35em")
			.text((d)=>{return d;});
	},
	drawsubgraph(g_link1,g_node1,g_text1,data_link,data_node,w,h){
		let simulation = d3.forceSimulation()
			.force("link", d3.forceLink().id((d)=>{ return d.id; }))
			.force("charge", d3.forceManyBody())
			.force("center", d3.forceCenter(w / 2, h / 2));
			
		let g_link=g_link1.selectAll("line");
		let g_node=g_node1.selectAll("circle");
		let g_text=g_text1.selectAll("text");
		
		g_link = g_link.data(data_link,(d)=>{return d;});
		g_link.exit().remove();
		g_link=g_link.enter().append("line")
			//.attr("stroke","#555")
			.merge(g_link);
			
		g_node = g_node.data(data_node,(d)=>{return d;});
		g_node.exit().transition().attr("r", 0).remove();
		
		let nodes_new=g_node.enter().append("circle")
			.attr("r", (d)=>{return this.circlefill(d.id,1);})
			.attr("fill",(d,i)=>{
				return this.circlefill(d.id,0);
			})
			.on("mouseover",(d)=>{
				this.$store.state.hlnodes = [d.id];
				this.$store.state.hlview = "subgraph";
			}).on("mouseout",(d)=>{
				this.$store.state.hlnodes = [];
				this.$store.state.hlview = "subgraph";
			});
		g_node=nodes_new.merge(g_node);

		g_text1.selectAll("text").remove();
		g_text=g_text1.selectAll("text").data(data_node,(d)=>{return d;})
			.enter()
			.append("text")
			.attr("font-family", "sans-serif")
			.attr("font-size", 12)
			//.attr("fill", "grey")
			.attr("dx", 12)
			.attr("dy", "0.35em")
			.text((d)=>{return d.id;} )
			
		simulation
			.nodes(data_node)
			.on("tick", ticked);
		simulation.force("link")
			.links(data_link);
		simulation.alpha(1).restart();
		function ticked() {
			g_node.attr("cx", (d)=>{  return d.x = Math.max(20, Math.min(w - 20, d.x)); })
				.attr("cy", (d)=>{ return d.y = Math.max(20, Math.min(h - 20, d.y));  });
				
			g_link.attr("x1", (d)=> { return d.source.x; })
				.attr("y1", (d)=> { return d.source.y; })
				.attr("x2", (d)=> { return d.target.x; })
				.attr("y2", (d)=> { return d.target.y; });

			g_text.attr("x", d => d.x)
				.attr("y", d => d.y);
		}
		//console.log(g_text1.selectAll("text"));
		this.svg.selectAll("line").attr("stroke","grey");
		this.svg.selectAll("text").attr("fill","grey");
		
	},
	showsubgraph(new0cur1){
		
		let newlen=this.sub_Gs.length;
		if(newlen>this.maxshownnum || new0cur1==1){
			let turnnum=newlen-this.maxshownnum-this.curstartnum;
			if(0<turnnum && turnnum<this.maxshownnum && newlen>this.maxshownnum){
				//console.log("overlap",turnnum);
				for(let i=0;i<turnnum;i++){
					this.curstartnum=this.curstartnum+1;
					this.turnright();
					let tmplen=this.subg_nodes_g.length;
					this.drawsubgraph(this.subg_edges_g[tmplen-1],this.subg_nodes_g[tmplen-1],this.subg_texts_g[tmplen-1],this.sub_Gs[this.curstartnum+this.maxshownnum-1][1],this.sub_Gs[this.curstartnum+this.maxshownnum-1][0],this.subGwidth,this.subGheight);
				}
			}else if(new0cur1==1){
				//console.log("update current subgraph");
				let tmplen=this.subg_nodes_g.length;
				this.drawsubgraph(this.subg_edges_g[tmplen-1],this.subg_nodes_g[tmplen-1],this.subg_texts_g[tmplen-1],this.sub_Gs[newlen-1][1],this.sub_Gs[newlen-1][0],this.subGwidth,this.subGheight);
			}else{
				//console.log("redraw all subgraph");
				for(let i=0;i<this.subg_nodes_g.length;i++){
					this.subg_nodes_g[i].remove();
					this.subg_edges_g[i].remove();
					this.subg_texts_g[i].remove();
				}
				this.subg_nodes_g=[];this.subg_edges_g=[];this.subg_texts_g=[];
				this.curstartnum=newlen-this.maxshownnum;
				for(let i=0;i<this.maxshownnum;i++){
					this.subg_nodes_g.push(this.svg.append("g").attr("class", "nodes"));
					this.subg_edges_g.push(this.svg.append("g").attr("class", "links"));
					this.subg_texts_g.push(this.svg.append("g"));
					this.drawsubgraph(this.subg_edges_g[i],this.subg_nodes_g[i],this.subg_texts_g[i],this.sub_Gs[this.curstartnum+i][1],this.sub_Gs[this.curstartnum+i][0],this.subGwidth,this.subGheight);
				}
			}
		}else{
			this.curstartnum=0;
			this.subg_nodes_g.push(this.svg.append("g").attr("class", "nodes"));
			this.subg_edges_g.push(this.svg.append("g").attr("class", "links"));
			this.subg_texts_g.push(this.svg.append("g"));
			let tmplen=this.subg_nodes_g.length;
			//console.log("kkk");
			this.drawsubgraph(this.subg_edges_g[tmplen-1],this.subg_nodes_g[tmplen-1],this.subg_texts_g[tmplen-1],this.sub_Gs[newlen-1][1],this.sub_Gs[newlen-1][0],this.subGwidth,this.subGheight);
		}
		//console.log("hhh");
		this.adjust_positions();
		//console.log("curstartnum",curstartnum);
	},
	cleartree(){
		this.links_dom.selectAll(".treelink").remove();
		this.nodes_dom.selectAll(".node").remove();
		this.none0tree1sub2=0;
	},
	clearsubgraph(){
		for(let i=0;i<this.subg_nodes_g.length;i++){
			this.subg_nodes_g[i].remove();
			this.subg_edges_g[i].remove();
			this.subg_texts_g[i].remove();
		}
		this.timelinetext.selectAll("text").remove();
		this.cuttingline.selectAll("line").remove();
		this.sub_Gs=[];this.subg_nodes_g=[];this.subg_edges_g=[];this.subg_texts_g=[];
		this.curstartnum=0;
		this.none0tree1sub2=0;
		//highlightnodes_sel=[];
	},
	
	gettreedata(evt_data){
		console.log(evt_data);
		let tmpdata=evt_data["treeinfo"]["bfstree"];
		let rootid=evt_data["treeinfo"]["rootid"];
		tmpdata[rootid]["p"]="";
		let root=_.map(tmpdata, (val, key)=>{ return {"name":parseInt(key),"parent":val["p"]}; });
		//console.log(root);
		root = d3.stratify()
			.id((d)=>{ return d.name; })
			.parentId((d)=>{ return d.parent; })
			(root);
		this.d3cluster(root);
		
		function collapse(d) {
		  if (d.children) {
			d._children = d.children;
			d._children.forEach(collapse);
			if(d.depth >1){d.children = null};
		  }
		}
		root.children.forEach(collapse);
		this.updatetree(root,root);
	},
	paths2subg(evt_data){
		var tmpnodes=_.flatten(evt_data["paths"]);
		tmpnodes=_.uniq(tmpnodes);
		var tmppaths=[];
		for(var i=0;i<evt_data["paths"].length;i++){
			for(var j=0;j<evt_data["paths"][i].length-1;j++){
				tmppaths.push([evt_data["paths"][i][j],evt_data["paths"][i][j+1]]);
				//console.log();
			}
		}
		return [tmpnodes,tmppaths];
	}
  },
  
  computed: {
    nodesSelected: function() {
      return this.$store.state.nodesSelected
    },
	hlnodes:function() {
      return this.$store.state.hlnodes
    },
	timeupdated:function() {
      return this.$store.state.timeupdated
    }
  },
  watch: {
    nodesSelected: function(newVal, oldVal) {
	  this.highlightnodes_sel=newVal;
	  let obj = {nodes: this.highlightnodes_sel};
	  
	  if(this.highlightnodes_sel.length==0){
		  console.log("clear all");
		  this.none0tree1sub2=0;
		  this.clearsubgraph();
		  this.cleartree();
		  CommunicateWithServer('get', obj, "choosenone", ()=>{});
	  }else if(this.highlightnodes_sel.length==1){
		  	this.none0tree1sub2=1;
			this.clearsubgraph();
			//let obj = {nodes: this.highlightnodes_sel};
			CommunicateWithServer('get', obj, 'getBFStree', (evt_data)=>{
				this.gettreedata(evt_data);
			});
	  }else{
		    this.none0tree1sub2=2;
		    //let obj = {nodes:JSON.stringify(this.highlightnodes_sel)};
			let url="";
			if(this.highlightnodes_sel.length==2){url="getSPs";}
			else{url="getSubgraph";}
			CommunicateWithServer('get', obj, url, (evt_data)=>{
				console.log(evt_data);
				let data=[];
				if(this.highlightnodes_sel.length==2){
					data=this.paths2subg(evt_data);
				}else{
					data=[evt_data["subgraph_nodes"],evt_data["subgraph_edges"]];
				}
				
				//console.log(data);
				for(let i=0;i<data[0].length;i++){
					data[0][i]={"id":data[0][i]};
				}
				for(let i=0;i<data[1].length;i++){
					data[1][i]={"source":data[1][i][0],"target":data[1][i][1]};
				}
				//console.log(data);
				if(this.sub_Gs.length==0){
					this.sub_Gs.push(data);
					this.cleartree();
					this.showsubgraph(0);
				}else{
					this.sub_Gs[this.sub_Gs.length-1]=data;
					this.showsubgraph(1);
				}
		    })
	  }
    },
	timeupdated:function(newVal, oldVal) {
		//let obj = {nodes:JSON.stringify(this.highlightnodes_sel)};
		CommunicateWithServer('get', {}, "getsubdata", (evt_data)=>{
			if(this.highlightnodes_sel.length==0){
			
			}else if(this.highlightnodes_sel.length==1){
				this.gettreedata(evt_data);
			}else{
				let data=[];
				if(this.highlightnodes_sel.length==2){
					data=this.paths2subg(evt_data);
				}else{
					data=[evt_data["subgraph_nodes"],evt_data["subgraph_edges"]];
				}
				for(var i=0;i<data[0].length;i++){
					data[0][i]={"id":data[0][i]};
				}
				for(var i=0;i<data[1].length;i++){
					data[1][i]={"source":data[1][i][0],"target":data[1][i][1]};
				}
				//console.log(data);
				this.cleartree();
				this.none0tree1sub2=2;
				this.sub_Gs.push(data);
				this.showsubgraph(0);
			}
		});
	},
	hlnodes: function(newVal, oldVal) {
	  if(this.$store.state.hlview!="subgraph"){
		this.highlightnodes=newVal;
		//console.log(this.highlightnodes);
		//console.log(this.highlightnodes_sel);
		//console.log(this.none0tree1sub2);
		if(this.highlightnodes_sel.length==1){
			this.nodes_dom.selectAll("circle")
				.attr("r",(d)=>{return this.circlefill(parseInt(d.id),1);})
				.attr("fill",(d)=>{return this.circlefill(parseInt(d.id),0);});
		}else if(this.highlightnodes_sel.length>=2){
			for(var i=0;i<this.subg_nodes_g.length;i++){
				this.subg_nodes_g[i].selectAll("circle")
					.attr("r",(d,i)=>{return this.circlefill(d.id,1);})
					.attr("fill",(d,i)=>{return this.circlefill(d.id,0);});
			}
		}
	  }
    }
  }
};

</script>
<style lang="less" scoped>
@import "./AppSubgraph.less";

</style>
