<template>
  <div id="comparetop">
    <div style="border-bottom: 1px #ccc dashed;
    position: relative;
    padding-bottom: 10px;
    padding-top: 10px;
    margin-right: 30px;">
      <span style="font-size: large;">相似节点列表</span>
    </div>
    <div style="width:50%; height: 90%; float:left">
      <table>
        <tr>
          <th style="width:15%">排名</th>
          <th style="width:55%">节点ID</th>
          <th style="width:30%">相似度</th>
        </tr>
        <tr v-for="(data, index) in topdata1">
          <td>{{index + 1}}</td>
          <td @click="getCompareId">{{data.id}}</td>
          <td class="right-td">{{data.Similarity}}</td>
        </tr>
      </table>
    </div>
    <div style="width:50%; height: 90%; float:right">
      <table>
        <tr>
          <th style="width:15%">排名</th>
          <th style="width:55%">节点ID</th>
          <th style="width:30%">相似度</th>
        </tr>
        <tr v-for="(data, index) in topdata2">
          <td>{{index + 6}}</td>
          <td @click="getCompareId">{{data.id}}</td>
          <td class="right-td">{{data.Similarity}}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Top',
  props: {
    topnodes: Array
  },
  data () {
    return {
      timerange: {},
      compareId: ''
    };
  },
  mounted () {
  },
  methods: {
    getCompareId (e) {
      //console.log(e.target.innerText);
      this.compareId = e.target.innerText;
      //this.$emit('compare_change', this.compareId);
    }
  },
  computed: {
    topdata1 () {
      let result = [];
      for(let i = 0; i < 5; i++) {
        result.push(this.topnodes[i]);
      }
      return result;
    },
    topdata2 () {
      let result = [];
      for(let i = 5; i < 10; i++) {
        result.push(this.topnodes[i]);
      }
      //console.log(result);
      return result;
    }
  },
  watch: {
    compareId () {
      this.$emit('compare_change', this.compareId);
    }
  },
};
</script>

<style type='text/css' scoped>
  #comparetop {
    width: 65%;
    height: 42%;
    position: absolute;
    left: 2%;
    bottom: 1%;
  }
  table {
    width: 90%;
    height: 100%;
  }
  tr {
    height: 16.6%;
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
  .right-td {
    border-width: 0 0 1px 0
  }
</style>
