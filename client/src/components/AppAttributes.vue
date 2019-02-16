<template>
    <div id="attributes-panel">
		<app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
		<div id="attributes_btn" class="btn-div">
			<div id="attributes_label" class="block-div"></div>
		</div>
		
		<div id="attributes_svg" class="block-div"></div>
		
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
      msgs: "属性变化",
      width: null,
      width2: null,
      height: null,
      height2: null,
	  svg: null,
	  svg_label: null,
      attributes_g: null,
      curnodes: [],
	  nodesImgList: [hostImg, switchImg, serverImg],
	  padding:{top: 10, bottom: 20, left: 70, right: 30},
	  timeset:{"starttime": 1468561795, "curtime": 1468561795, "endtime": 1468633627, "timestep": 60,"timewindow": 60}
	};
  },
  components: { AppTitle },
  mounted() {
    let self = this;
	let $Div=$("#attributes_svg");
    self.width=$Div.width();
	self.height=$Div.height();
	self.svg=d3.select("#attributes_svg")
			.append("svg")
			.attr("width", self.width)
			.attr("height", self.height);
	let $Div2=$("#attributes_label");
    self.width2=$Div2.width();
    self.height2=$Div2.height();
	self.svg_label=d3.select("#attributes_label")
			.append("svg")
			.attr("width", self.width2)
			.attr("height", self.height2);
	self.attributes_g=self.svg.append("g").attr("class","attributes");
	this.start_angle = 0;
    this.end_angle = 180 * (Math.PI / 180);
	this.arcs_width = 2;
	this.collapsed_color_0 = ["#b72626", "#cd4d40", "#d37053", "#da9155", "#dac385"];
    this.control_color_0 = ["#008475", "#00ba8a", "#4dcf8b", "#9ce28d", "#dff68e"];
  },
  methods: {
	handleattribute(){
		let newtype=parseInt(document.getElementById("st_attribute").value);
		if(newtype!=this.curtype){
			this.curtype=newtype;
			this.getattr();
		}
	},
	yformat(){
		if(this.curtype==0 || this.curtype==2){
			return d3.format("d");
		}else{
			return d3.formatPrefix(",.0", 1e-3);
		}
	},
	yscale(min,max){
		if(min==max){
			if(this.curtype==0 || this.curtype==2){
				return [min-1,max+1];
			}else{
				return [min-0.001,max+0.001];
			}
		}else{
			return [min,max];
		}
	},
	inttime2date(num){
		return new Date(num*1000);
	},
	drawlines(data,nodesattr,shownnode,rangestart,rangeend){

		//let colors=["#F48061","#56A4C9","#50890E","#AFC0DD","#F6E3BE"];
		
		let nodes=this.curnodes;
		if(shownnode==-1){
			shownnode=nodes[0];
		}
		let g=this.attributes_g;
		let h=this.height;
		let w=this.width;
		let padding=this.padding;
		let lineheight=h-padding.top-padding.bottom;
		//console.log(w,h,lineheight);
		//let timenum=data[nodes[0]].length;
		//Math.ceil((this.timeset["endtime"]-this.timeset["starttime"])/this.timeset["timestep"]);
		let x = d3.scaleTime().range([0, w-padding.left-padding.right])
			//.domain([this.inttime2date(this.timeset["starttime"]),this.inttime2date(this.timeset["endtime"])]);
		
		let attrnamx=["degree","clustering","core num","eigen center","reachable percent"];
		let attrnum=5;
		let newdata=[[],[],[],[],[]];
		//let newdata_ind=[[],[],[],[],[]];
		let d_min=[100,100,100,100,100];let d_max=[0,0,0,0,0];
		let timestart=this.timeset["endtime"];
		let timeend=0;
		
		for(let k=0;k<data[shownnode].length;k++){
			let tmpdata=data[shownnode][k];
			if(tmpdata.length==0){
				continue;
			}
			for(let attr_i=0;attr_i<tmpdata.length;attr_i++){
				if(tmpdata[attr_i]>d_max[attr_i]){
					d_max[attr_i]=tmpdata[attr_i];
				}else if(tmpdata[attr_i]<d_min[attr_i]){
					d_min[attr_i]=tmpdata[attr_i];
				}
				let tmpstart=rangestart+k*this.timeset["timestep"];
				let tmpend=rangestart+(k+1)*this.timeset["timestep"];
				if(newdata[attr_i].length!=0){
					let lastind=newdata[attr_i][newdata[attr_i].length-1][1];
					if(lastind!=k-1){
						newdata[attr_i].push([0,lastind+1]);
						//newdata_ind[attr_i].push(lastind+1);
					}
				}else{
					if(k-1>0){
						newdata[attr_i].push([tmpdata[attr_i],k-1]);
						tmpstart=rangestart+(k-1)*this.timeset["timestep"];
					}
				}
				newdata[attr_i].push([tmpdata[attr_i],k]);

				if(tmpend>timeend){
					timeend=tmpend;
				}
				if(tmpstart<timestart){
					timestart=tmpstart;
				}
			}
		}
		if(rangestart<timestart){timestart=rangestart;}
		if(rangeend>timeend){timeend=rangeend;}
		
		x.domain([this.inttime2date(timestart),this.inttime2date(timeend)]);
		
		//console.log([timestart,timeend]);
		//console.log(newdata);
		
		let y=d3.scaleLinear().range([lineheight, 0])
				.domain([0,1]);
		/*
		let y=[];
		for(var attr_i=0;attr_i<attrnum;attr_i++){
			let tmpy=d3.scaleLinear().range([lineheight, 0])
				.domain([d_min[attr_i],d_max[attr_i]]);
			//console.log(tmpy.domain());
			y.push(tmpy);
		}
		*/
		timestart=rangestart;
		let timestep=this.timeset["timestep"];
		
			
		let axis=g.append("g").attr("transform", "translate("+(padding.left)+"," + (padding.top) + ")");
		let xaxis=axis.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + (lineheight) + ")")
			.call(d3.axisBottom(x).ticks(5));
		
		let yaxis=axis.append("g")
			.attr("class", "y axis")
			.call(d3.axisLeft(y).ticks(5));	
		
		let g3=g.append("g").attr("transform", "translate("+(padding.left)+"," + (padding.top) + ")");
		let attrline = g3.selectAll("g").data(newdata)
			.enter().append("g");
		
		let attrpaths=attrline
			.append("path")
			.attr("class",(d,i)=>{
				return "attr_"+i;
			})
			.attr("d", (d,i)=>{
				let linemaker=d3.line()
					.curve(d3.curveBasis)
					.x((dd)=> { 
						return x(this.inttime2date((timestart+dd[1]*timestep))); 
					})
					.y((dd)=> {
						//console.log(dd,i);
						/*
						if(dd[0]==0){return 0;}
						else{return y[i](dd[0]); }
						*/
						if(d_max[i]>1){return y(dd[0]/d_max[i]);}
						else{return y(dd[0]);}
					});
				return linemaker(d,i); 
			})
			.attr("stroke", "#1fa5da")
			.attr("stroke-width", 1.5)
			.attr("fill","none")
			.append("title").text((d,i)=>{
				return attrnamx[i];
			});
		/*
		let timeendlocx=x(this.inttime2date(rangeend));
		let timestartlocx=x(this.inttime2date(rangestart));
		let timespanwidth=timeendlocx-timestartlocx;
		
		let timerect=g.append("g").attr("transform", "translate("+(padding.left)+"," + (padding.top-4) + ")");
        timerect.append("g").append("rect")
			.attr("class", "upper_timerange")
			.attr("x", timeendlocx - timespanwidth)
			.attr("width", timespanwidth)
			.attr("height", lineheight+8);
        */
		var noderadius=8;
		var nodesall=_.keys(nodesattr);
		let g4=this.svg_label.append("g");
		let legend = g4.selectAll("g").data(nodesall)
			.enter().append("g")
			.attr("transform", (d, i)=>{ return "translate("+(30+(2*noderadius*2)*i)+"," + (noderadius) + ")"; });
		
		legend.append("circle")
			.attr("r", noderadius)
			.on("mouseover",(d)=>{
				this.$store.state.hlnodes = d;
				this.$store.state.hlview = "subgraph";
			}).on("mouseout",(d)=>{
				this.$store.state.hlnodes = [];
				this.$store.state.hlview = "subgraph";
			}).attr("fill","#282c37");
			
		legend.append("image")
			.attr("xlink:href", d => {
				let tmptype=nodesattr[d]["nodeType"];
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
			.on("click",(d,i)=>{
				this.attributes_g.selectAll("g").remove();
				this.svg_label.selectAll("g").remove();
				this.drawlines(data,nodesattr,d,rangestart,rangeend);
			})
			.append("title").text((d,i)=>{
				return d;
			});
		legend.append("path")
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
		legend.append("path")
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
		legend.attr("opacity",(d,i)=>{
			if(d==shownnode){return 1;}
			else{return 0.3;}
		})
		
	},
	getattr(){
		let obj = {
			nodes:JSON.stringify(this.curnodes)
		};
		CommunicateWithServer('get', obj, 'getAttr', (evt_data)=>{
			console.log(evt_data);
			this.attributes_g.selectAll("g").remove();
			this.svg_label.selectAll("g").remove();
			this.drawlines(evt_data["attr"],evt_data["nodes"],this.curnodes[this.curnodes.length-1],evt_data["start"],evt_data["end"]);
		});
	}
  },
  computed: {
    nodesSelected: function() {
      return this.$store.state.nodesSelected
    }
  },
  watch: {
    nodesSelected: function(newVal, oldVal) {
		this.curnodes=newVal;
	    if(this.curnodes.length==0){
		  this.attributes_g.selectAll("g").remove();
		  this.svg_label.selectAll("g").remove();
	    }else{
		    this.getattr();
	    }
    }
  }
};

</script>
<style lang="less" scoped>
@import "./AppAttributes.less";

</style>
