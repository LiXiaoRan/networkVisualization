<template>
    <div id="attributes-panel">
		<app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
		<div id="attributes_btn" class="btn-div">
			<select id="st_attribute" @click="handleattribute">
			  <option value="0"selected = "selected"><span>degree</span></option>
			  <option value="1"><span>clustering</span></option>
			  <option value="2" ><span>k core num</span></option>
			  <option value="3" ><span>eigen centrality</span></option>
			  <option value="4" ><span>reachable num</span></option>
			</select>
			<div id="attributes_label" class="block-div"></div>
		</div>
		
		<div id="attributes_svg" class="block-div"></div>
		
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
      msgs: "属性变化",
      width: null,
      width2: null,
      height: null,
      height2: null,
	  svg: null,
	  svg_label: null,
      attributes_g: null,
      xpadding: 70,
      ypadding: 50,
      curnodes: [],
      curtype: 0
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
	drawlines(data,g,h,w){
		
		let colors=["#F48061","#56A4C9","#50890E","#AFC0DD","#F6E3BE"];
		
		let nodes=this.curnodes;
		//let nodes=_.keys(data);
		let times=_.keys(data[nodes[0]]);
		let lineheight=h-this.ypadding;
		if(times.length<=1){return;}
		//var x = d3.scaleTime().range([0, linewidth]);
		let x = d3.scaleLinear().range([0, w-this.xpadding]).domain([parseInt(times[0]),parseInt(times[times.length-1])]);
		
		let newdata=[];
		let d_min=100;let d_max=0;
		for(let k=0;k<nodes.length;k++){
			let tmpdata=data[nodes[k]];
			newdata.push(_.values(tmpdata));
			let tmpmin=_.min(tmpdata);
			let tmpmax=_.max(tmpdata);
			if(tmpmin<d_min){
				d_min=tmpmin;
			}
			if(tmpmax>d_max){
				d_max=tmpmax;
			}
		}
		//console.log(newdata);
		
		let y=d3.scaleLinear().range([lineheight, 0]).domain(this.yscale(d_min,d_max));
		
		let line=d3.line()
			//.curve(d3.curveBasis)
			.x((d,i)=> { return x(parseInt(times[i])); })
			.y((d)=> { return y(d); });
		
		let g2=g.append("g").attr("transform", "translate("+(this.xpadding/2)+"," + (this.ypadding/2) + ")");
		let xaxis=g2.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + (lineheight) + ")")
			.call(d3.axisBottom(x).ticks(5));
		let yaxis=g2.append("g")
			.attr("class", "y axis")
			.call(d3.axisLeft(y).ticks(5).tickFormat(this.yformat()));	
		
		let g3=g.append("g");
		let attrline = g3.selectAll("g").data(newdata)
			.enter().append("g")
			.attr("transform", (d, i)=>{return "translate("+(this.xpadding/2)+"," + (this.ypadding/2) + ")"; });
		let attrpaths=attrline.append("path")
			.attr("d", (d,i)=>{ return line(d); })
			.style("stroke", (d,i)=>{return colors[i%colors.length];})
			.style("fill","none");
		
		let g4=this.svg_label.append("g");
		let legend = g4.selectAll("g").data(nodes)
			.enter().append("g")
			.attr("transform", (d, i)=>{ return "translate("+(10+50*i)+"," + (20) + ")"; });
		legend.append("text")
			//.attr("class","text")
			.attr("x", 20)
			.attr("y", -5)
			.text((d,i)=>{return d;});
		legend.append("circle")
			.attr("cx", 5).attr("cy", -10)
			.attr("r",5).attr("fill",(d,i)=>{return colors[i%colors.length];})
			.on("mouseover",(d,i)=>{
				let tmpmin=_.min(data[d]);
				let tmpmax=_.max(data[d]);
				let y_local=d3.scaleLinear().range([lineheight, 0]).domain(this.yscale(tmpmin,tmpmax));
				let line_local=d3.line()
					.x((dd,ii)=> { return x(parseInt(times[ii])); })
					.y((dd)=> { return y_local(dd); });
				yaxis.call(d3.axisLeft(y_local).ticks(5).tickFormat(this.yformat()));
				attrpaths.attr("d", (dd,ii)=> { 
						if(i==ii){return line_local(dd);}
						else{return line(dd);}
					})
				attrline.attr("opacity",(dd,ii)=>{
					if(i==ii){return 1;}
					else{return 0.1;}
				});
			}).on("mouseout",(d)=>{
				attrline.attr("opacity",1);
				yaxis.call(d3.axisLeft(y).ticks(5).tickFormat(this.yformat()));
				attrline.selectAll("path")
					.attr("d", (dd,ii) =>{return line(dd);});
			});
	},
	getattr(){
		let obj = {
			type: this.curtype,
			nodes:JSON.stringify(this.curnodes)
		};
		CommunicateWithServer('get', obj, 'getAttr', (evt_data)=>{
			this.attributes_g.selectAll("g").remove();
			this.svg_label.selectAll("g").remove();
			this.drawlines(evt_data["attr"],this.attributes_g,this.height,this.width);
		});
	}
  },
  computed: {
    nodesSelected: function() {
      return this.$store.state.nodesSelected
    },
	timeupdated:function() {
      return this.$store.state.timeupdated
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
    },
	timeupdated: function(newVal, oldVal) {
	  this.curnodes=[];
	  this.attributes_g.selectAll("g").remove();
	  this.svg_label.selectAll("g").remove();
    }
  }
};

</script>
<style lang="less" scoped>
@import "./AppAttributes.less";

</style>
