<template>
  <div id="compareattributes1">
    <div style="border-bottom: 1px #ccc dashed;
    position: relative;
    padding-bottom: 10px;
    padding-top: 10px;
    margin-right: 30px;">
      <span style="font-size: large;">属性列表</span>
    </div>
    <table>
      <tr>
        <th style="width:33%"></th>
        <th style="width:33%">{{this.selectId}}</th>
        <th style="width:33%">{{this.compareId}}</th>
      </tr>
      <tr v-for="item in view_data">
        <td>{{item[0]}}</td>
        <td>{{item[1]}}</td>
        <td>{{item[2]}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  name: 'Attributes1',
  props: {
    topnodes_attr: Object,
    compareId: String,
    select_attr: Object
  },
  data () {
    return {
      selectId: '',
      view_data: ''
    };
  },
  mounted () {
    this.selectId = localStorage.getItem('selectid');
  },
  methods: {
  },
  computed: {
    /* view_data () {
      let viewData = [];
      let temp_data = [];
      let obj = this.select_attr;
      for(let i in obj) {
        viewData.push([i, obj[i]['value']]);
      }
      let id = this.compareId;
      obj = (this.topnodes_attr)[id];
      for(let i in obj) {
        temp_data.push([i, obj[i]['value']]);
      }
      for(let i = 0; i < viewData.length; i++) {
        for(let j = 0; j < temp_data.length; j++) {
          if(temp_data[j][0] == viewData[i][0]) {
            viewData[i].push(temp_data[j][1]);
            break;
          }
        }
      }
      return viewData;
    } */
  },
  watch: {
    select_attr: {
      handler: function (val, oldVal) {
        let viewData = [];
        let temp_data = [];
        let obj = val;
        for(let i in obj) {
          if(i != 'hasChange'){
            viewData.push([i, obj[i]['value']]);
          }
        }
        let id = this.compareId;
        obj = (this.topnodes_attr)[id];
        for(let i in obj) {
          temp_data.push([i, obj[i]['value']]);
        }
        for(let i = 0; i < viewData.length; i++) {
          for(let j = 0; j < temp_data.length; j++) {
            if(temp_data[j][0] == viewData[i][0]) {
              viewData[i].push(temp_data[j][1]);
              break;
            }
          }
        }
        this.view_data = viewData;
      },
      deep: true
    },
  },
}
</script>

<style type='text/css' scoped>
  #compareattributes1 {
    width: 32%;
    height: 60%;
    position: absolute;
    left: 68%;
    top: 1%;
    overflow: auto;
  }
  table {
    width: 99%;
  }
  tr {
    height: 40px;
  }
  th {
    text-align: center;
    /* color: #008C8C; */
    font-size: large;
  }
  td {
    font-size: medium;
    text-align: center;
    width: 33%;
    /* color: #008C8C; */
    border: rgba(204, 204, 204, 1) dashed;
    border-width: 0 1px 1px 0
  }
</style>
