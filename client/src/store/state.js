/*
* @Author: wakouboy
* @Date:   2018-08-08 23:30:38
* @Last Modified by:   wakouboy
* @Last Modified time: 2018-11-30 18:29:26
*/
const state = {
  testData: null,
	nodesSelected: null,
	timeupdated: null,
	hlnodes:null,
	hlview:null,
	nodeTypeList:['主机','交换机','服务器'],
	nodeAttrList:['致瘫','控制','正常'],
  selectTime:{start: '', end: ''},
  selectData:[]
	//cleargraph:0,
	//init_dim2:0,
	//init_subgraph:0,
};
export default state;
