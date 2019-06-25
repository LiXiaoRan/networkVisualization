<template>
  <div id="compareattributes2">
    <div style="border-bottom: 1px #ccc dashed;
    position: relative;
    padding-bottom: 10px;
    padding-top: 10px;
    margin-right: 30px;">
      <span style="font-size: large;">缺失属性</span>
    </div>
    <table>
      <tr v-for="item in view_data">
        <td>{{item[0]}}</td>
        <!-- <td><input type="text" @input="attrChange" :value="item[1]" /></td> -->
        <td contenteditable="true" @blur="attrChange">{{item[1]}}</td>
        <td>{{item[2]}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  name: 'Attributes2',
	props: {
	  topnodes_attr: Object,
	  compareId: String,
	  select_attr: Object
	},
  data () {
    return {
			selectId: '',
    };
  },
	mounted () {
	  this.selectId = localStorage.getItem('selectid');
	},
  methods: {
    attrChange(e) {
      let value = e.target.innerText;
      let attr = e.path[1].cells[0].innerText;
      this.$emit('attr_change', [attr, value]);
    },
  },
	computed: {
	  view_data () {
	    let viewData = [];
	    let temp_data = [];
	    let obj = this.select_attr;
	    for(let i in obj) {
				if(!obj[i]['value']) {
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
      return viewData;
	  }
  },
  watch: {
  },
}
</script>

<style type='text/css' scoped>
  #compareattributes2 {
    width: 32%;
    height: 37%;
    position: absolute;
    left: 68%;
    top: 62%;
    overflow: auto;
  }
  table {
    width: 100%;
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
