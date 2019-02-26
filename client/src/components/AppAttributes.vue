<template>
    <div id="attributes-panel">
		<app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
		<div id="attributes_btn" class="btn-div" @click="handlehistotype">
			<input type="radio" name="histotype" value="0" checked='checked'>&nbsp;<span>flow</span>&nbsp;&nbsp;
			<input type="radio" name="histotype" value="1">&nbsp;<span>protocol</span>
			
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
      height: null,//line
      height2: null,//nodes circle
      height3: null,//histogram
	  svg: null,
	  svg_label: null,
      attributes_g: null,
      hists_g: null,
	  flow0proto1:0,
      curnodes: [],
	  curnode:null,
	  //timedomain:null,
	  protocoldict:{'000': 'unknown','001': 'other','101': 'VAST','102': 'SDH','103': 'Link16','104': 'Link11','201': 'PPP','202': 'Ethernet','203': 'HDLC','204': 'IP','205': 'OSPF','206': 'EIGRP ','207': 'ISIS','208': 'PNNI','209': 'CLNP','210': 'ICMP','211': 'ARP','212': 'TCP','213': 'UDP','214': 'BGP','215': 'RIP','301': 'HTTP','302': 'FTP','303': 'SMTP','304': 'POP3','305': 'H.323','306': 'SIP','307': 'DNS','308': 'SNMP'},
	  protocolcolor:{'000': 'white','001': 'white','101': '#F8C3CD','102': '#F4A7B9','103': '#E16B8C','104': '#D05A6E','201': '#1fa5da','202': '#1fa5da','203': '#1fa5da','204': '#1fa5da','205': '#1fa5da','206': '#1fa5da','207': '#1fa5da','208': '#1fa5da','209': '#1fa5da','210': '#1fa5da','211': '#1fa5da','212': '','213': '#1fa5da','214': '#1fa5da','215': '#1fa5da','301': '#FFB11B','302': '#D19826','303': '#DDA52D','304': '#C99833','305': '#F9BF45','306': '#DCB879','307': '#BA9132','308': '#E8B647'},
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
	self.height=$Div.height()*0.5;
	self.svg=d3.select("#attributes_svg")
			.append("svg")
			.attr("width", self.width)
			.attr("height", $Div.height());
	self.attributes_g=self.svg.append("g").attr("class","attributes");
	
	self.height3=$Div.height()-self.height;
	self.hists_g=self.svg.append("g").attr("class","flowlevel")
		.attr("transform", "translate("+(0)+"," + (self.height) + ")");;
	
	let $Div2=$("#attributes_label");
    self.width2=$Div2.width();
    self.height2=$Div2.height();
	self.svg_label=d3.select("#attributes_label")
			.append("svg")
			.attr("width", self.width2)
			.attr("height", self.height2);
	
	this.start_angle = 0;
    this.end_angle = 180 * (Math.PI / 180);
	this.arcs_width = 2;
	this.collapsed_color_0 = ["#b72626", "#cd4d40", "#d37053", "#da9155", "#dac385"];
    this.control_color_0 = ["#008475", "#00ba8a", "#4dcf8b", "#9ce28d", "#dff68e"];
  },
  methods: {
	inttime2date(num){
		return new Date(num*1000);
	},
	handlehistotype(){
		let obj = document.getElementsByName("histotype");
		for(let i=0; i<obj.length; i ++){
			if(obj[i].checked){
				let newtype=parseInt(obj[i].value);
				if(newtype!=this.flow0proto1){
					
					this.flow0proto1=newtype;
					this.drawhists(this.flowprotodata);
				}
				break;
			}
		}
	},
	drawlines(data,nodesattr){
		//let colors=["#F48061","#56A4C9","#50890E","#AFC0DD","#F6E3BE"];
		let shownnode=this.curnode;
		let rangestart=this.rangestart;
		let rangeend=this.rangeend;
		
		let nodes=this.curnodes;
		if(shownnode==-1){
			shownnode=nodes[0];
		}
		let g=this.attributes_g;
		let h=this.height;
		let w=this.width;
		let padding=this.padding;
		let lineheight=h-padding.top-padding.bottom;
		
		let attrnamx=["degree","clustering","core num","eigen center","reachable percent"];
		let attrnum=5;
		let newdata=[[],[],[],[],[]];
		//let newdata_ind=[[],[],[],[],[]];
		let d_min=[100,100,100,100,100];let d_max=[0,0,0,0,0];
		let timestart=this.timeset["endtime"];
		let timeend=0;
		let time0=this.timeset["starttime"]
		let timestep=this.timeset["timestep"];
		
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
				let tmpstart=time0+k*this.timeset["timestep"];
				let tmpend=time0+(k+1)*this.timeset["timestep"];
				if(newdata[attr_i].length!=0){
					let lastind=newdata[attr_i][newdata[attr_i].length-1][1];
					if(lastind!=k-1){
						newdata[attr_i].push([0,lastind+1]);
					}
					newdata[attr_i].push([tmpdata[attr_i],k]);
				}else{
					newdata[attr_i].push([tmpdata[attr_i],k]);
					//newdata[attr_i].push([tmpdata[attr_i],k+1]);
				}

				if(tmpend>timeend){
					timeend=tmpend;
				}
				if(tmpstart<timestart){
					timestart=tmpstart;
				}
			}
		}
		for(let attr_i=0;attr_i<newdata.length;attr_i++){
			//if(newdata[attr_i].length==1){}
			let lastvalue=newdata[attr_i][newdata[attr_i].length-1][0];
			let lastind=newdata[attr_i][newdata[attr_i].length-1][1];
			newdata[attr_i].push([lastvalue,lastind+1]);
			let tmpend=time0+(lastind+1)*this.timeset["timestep"];
			if(tmpend>timeend){
				timeend=tmpend;
			}
		}
		
		if(rangestart<timestart){timestart=rangestart;}
		if(rangeend>timeend){timeend=rangeend;}
		
		let x = d3.scaleTime().range([0, w-padding.left-padding.right]);
		x.domain([this.inttime2date(timestart),this.inttime2date(timeend)]);
		//this.timedomain=x.domain();
		//console.log([timestart,timeend]);
		//console.log(x.domain());
		console.log(newdata);
		
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
		//timestart=rangestart;
			
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
						return x(this.inttime2date((time0+dd[1]*timestep))); 
					})
					.y((dd)=> {
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
		
		
		let timeendlocx=x(this.inttime2date(rangeend));
		let timestartlocx=x(this.inttime2date(rangestart));
		let timespanwidth=timeendlocx-timestartlocx;
		
		let timerect=g.append("g").attr("transform", "translate("+(padding.left)+"," + (padding.top-4) + ")");
        timerect.append("g").append("rect")
			.attr("class", "upper_timerange")
			.attr("x", timeendlocx - timespanwidth)
			.attr("width", timespanwidth)
			.attr("height", lineheight+8)
			//.style("stroke-width","1px");
        
		
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
				return this.nodesImgList[tmptype];
				/*
				//console.log(tmptype);
				if (tmptype === "主机") {
				  return this.nodesImgList[0];
				} else if (tmptype === "交换机") {
				  return this.nodesImgList[1];
				} else if (tmptype === "服务器") {
				  return this.nodesImgList[2];
				}*/
			})
			.attr("x", d => - noderadius)
			.attr("y", d => - noderadius)
			.attr("width", d => noderadius*2)
			.attr("height", d => noderadius*2)
			.on("click",(d,i)=>{
				this.attributes_g.selectAll("g").remove();
				this.svg_label.selectAll("g").remove();
				this.curnode=d;
				this.drawlines(this.attridata,nodesattr);
				this.drawhists(this.flowprotodata);
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
	drawhists(data_p){
		let flow0proto1=this.flow0proto1;
		let protocoldict=this.protocoldict;
		let shownnode=this.curnode;
		let rangestart=this.rangestart;
		let rangeend=this.rangeend;
		
		let data=JSON.parse(JSON.stringify(data_p));
		let tmpdata;
		let tmpkey;
		let tmpcolor;
		
		if(flow0proto1==0){
			for(let t=0;t<data["flow"][shownnode].length;t++){
				if(_.isArray(data["flow"][shownnode][t])){
					data["flow"][shownnode][t]=_.object(['inflow', 'outflow'], data["flow"][shownnode][t]);
				}
			}
			tmpdata=data["flow"][shownnode];
			tmpkey=['inflow', 'outflow'];
			tmpcolor={"inflow":"#7bc5e3","outflow":"#1fa5da"};
		}else if(flow0proto1==1){
			let keysall=_.keys(this.protocoldict);
			for(let t=0;t<data["level"][shownnode].length;t++){
				let tmpkeys=_.keys(data["level"][shownnode][t]);
				for(let k=0;k<keysall.length;k++){
					if(_.indexOf(tmpkeys,keysall[k])<0){
						data["level"][shownnode][t][keysall[k]]=0;
					}
				}
			}
			tmpdata=data["level"][shownnode];
			tmpkey=keysall;
			tmpcolor=this.protocolcolor;
		}
		//console.log(tmpcolor);
		
		let delstart=-1;
		for(let i=0;i<tmpdata.length;i++){
			if(_.max(_.values(tmpdata[i]))==0){
				delstart=i;
			}else{
				break;
			}
		}
		tmpdata.splice(0,delstart+1);
		delstart=delstart+1;
		
		for(let i=tmpdata.length-1;i>=0;i--){
			if(_.max(_.values(tmpdata[i]))==0){
				tmpdata.splice(i,1);
			}else{
				break;
			}
		}
		//console.log(tmpdata);
		
		let series=d3.stack().keys(tmpkey)(tmpdata);
		//console.log(series);
		
		let time0=this.timeset["starttime"]
		let timestep=this.timeset["timestep"];
		
		let timestart=time0+delstart*timestep;
		let timeend=time0+(delstart+tmpdata.length)*timestep;
		if(rangestart<timestart){timestart=rangestart;}
		if(rangeend>timeend){timeend=rangeend;}
		
		let x = d3.scaleTime().range([0, this.width-this.padding.left-this.padding.right]);
		x.domain([this.inttime2date(timestart),this.inttime2date(timeend)]);
		//console.log(delstart);
		//console.log(x.domain());
		
		let availheight=this.height3-this.padding.top-this.padding.bottom;	
		var y = d3.scaleLinear()
			.domain([d3.min(series, stackMin), d3.max(series, stackMax)])
			.range([availheight, 0]);
		function stackMin(serie) {
		    return d3.min(serie, (d)=>{ return d[0]; });
		}
		function stackMax(serie) {
		    return d3.max(serie, (d)=>{ return d[1]; });
		}
		//console.log(x.bandwidth());
		
		this.hists_g.selectAll("g").remove();
		
		let axis=this.hists_g.append("g").attr("transform", "translate("+(this.padding.left)+"," + (this.padding.top) + ")");
		let xaxis=axis.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + (availheight) + ")")
			.call(d3.axisBottom(x).ticks(5));
		let yaxis=axis.append("g")
			.attr("class", "y axis")
			.call(d3.axisLeft(y).ticks(5));	
		
		let barstack_g=this.hists_g.append("g")
			.attr("transform", "translate(" + this.padding.left + "," + this.padding.top + ")")
			.selectAll("g")
			.data(series)
			.enter().append("g").attr("class",(d,i)=>{return d.key;})
			.attr("fill", (d)=>{
				return tmpcolor[d.key];
			})
		let barstack=barstack_g.selectAll("rect")
			.data((d)=>{return d; })
			.enter().append("rect")
			.attr("opacity",(d,i)=>{
				/*
				if((time0+(delstart+i)*timestep)>rangeend || (time0+(delstart+i+1)*timestep)<rangestart){
					return 0.7;
				}else{return 1;}*/
				return 1;
			})
			.attr("x", (d,i)=>{ 
				return x(this.inttime2date((time0+(delstart+i)*timestep)))
			})
			.attr("y", (d)=>{ return y(d[1]); })
			.attr("height", (d)=>{ return y(d[0]) - y(d[1]); })
			.attr("width", (d,i)=>{
				let x1=x(this.inttime2date((time0+(delstart+i)*timestep)));
				let x2=x(this.inttime2date((time0+(delstart+i+1)*timestep)));
				return x2-x1;
			}).append("title").text(function(d,i){
				//console.log($(this).parent());
				//console.log($(this).parent().parent().attr("class"));
				let tmpkey=$(this).parent().parent().attr("class");
				if(flow0proto1==0){return tmpkey+":"+d.data[tmpkey];}
				else{return protocoldict[tmpkey]+":"+d.data[tmpkey];}
			});
		
		let timeendlocx=x(this.inttime2date(rangeend));
		let timestartlocx=x(this.inttime2date(rangestart));
		let timespanwidth=timeendlocx-timestartlocx;
		
		let timerect=this.hists_g.append("g").attr("transform", "translate("+(this.padding.left)+"," + (this.padding.top-4) + ")");
        timerect.append("g").append("rect")
			.attr("class", "upper_timerange")
			.attr("x", timeendlocx - timespanwidth)
			.attr("width", timespanwidth)
			.attr("height", availheight+8)
			//.style("stroke-width","1px");
		
	},
	getattr(){
		let obj = {
			nodes:JSON.stringify(this.curnodes)
		};
		CommunicateWithServer('get', obj, 'getAttr', (evt_data)=>{
			console.log(evt_data);
			this.attributes_g.selectAll("g").remove();
			this.svg_label.selectAll("g").remove();
			this.attridata=evt_data["attr"];
			this.curnode=this.curnodes[this.curnodes.length-1];
			this.rangestart=evt_data["start"];
			this.rangeend=evt_data["end"];
			this.drawlines(evt_data["attr"],evt_data["nodes"]);
			
			CommunicateWithServer('get', obj, 'getFlow', (evt_data2)=>{
				console.log(evt_data2);
				this.flowprotodata=evt_data2;
				this.drawhists(evt_data2);
			});
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
