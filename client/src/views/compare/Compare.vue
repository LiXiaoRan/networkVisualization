<template>
  <div id="Compare">
    <compare-chart :compareId="compareId"></compare-chart>
    <compare-top @compare_change="changeCompareId" :topnodes="topnodes"></compare-top>
    <compare-attributes1 :topnodes_attr="topnodes_attr" :compareId="compareId" :select_attr="select_attr"></compare-attributes1>
    <compare-attributes2 @attr_change="changeAttr" :topnodes_attr="topnodes_attr" :compareId="compareId" :select_attr="select_attr_copy"></compare-attributes2>
  </div>
</template>
<script>
import CompareChart from './components/Chart'
import CompareTop from './components/Top'
import CompareAttributes1 from './components/Attributes1'
import CompareAttributes2 from './components/Attributes2'
export default {
  name: 'Compare',
  data () {
    return {
      timerange: {},
      selectId: '',
      select_attr: {},
      select_attr_copy: {},
      compareId: '',
      topnodes: [],
      topnodes_attr: {},
      timenodes_attr: {}
    };
  },
  components: {
    CompareChart,
    CompareTop,
    CompareAttributes1,
    CompareAttributes2
  },
  mounted () {
    let timerange = JSON.parse(localStorage.getItem('timerange'));
    //console.log(timerange);
    this.timerange = timerange;
    this.selectId = localStorage.getItem('selectid');
    //console.log(this.selectId);
    this.getData();
  },
  methods: {
    getData () {
      let paramsObj = {
        timerange: this.timerange,
        id: this.selectId,
      };
      let Url = "get-top-node-data";
      CommunicateWithServer("get", paramsObj, Url, this.showTop);
    },
    
    showTop (result) {
      this.topnodes = result[0];
      this.topnodes_attr = result[1];
      this.select_attr = result[2];
      //console.log(this.select_attr);
      let obj = result[2];
      let newObj = Object.assign({}, obj);
      this.select_attr_copy = newObj;
      this.select_attr['hasChange'] = false;
      this.compareId = this.topnodes[0].id;
      
      // 数据造假
      /* for(let key in result[2]) {
        let arr = key.split('_');
        if(arr[1] <= 5) {
          result[2][key]['value'] = null;
        }
      } */
    },
    
    changeCompareId (data) {
      this.compareId = data;
      console.log(this.compareId);
    },
    
    changeAttr (data) {
      this.select_attr['hasChange'] = true;
      this.select_attr[data[0]] = {
        key: data[0],
        value: data[1]
      };
    }
  },
  computed: {
  },
}
</script>
<style scoped>
  body {
    margin: 0;
    padding: 0;
    background-color: #222;
    color: rgba(255, 255, 255, 0.8);
    font-family: 'Microsoft YaHei', Arial, sans-serif;
  }
  #Compare {
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    position: absolute;
    overflow-x: auto;
    overflow-y: hidden;
  }
</style>
