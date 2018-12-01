<!-- 入口文件 -->
<template>
  <div id="App">
    <app-network v-bind:params-msg="paramsMsg"></app-network>
    <app-node-tree></app-node-tree>
    <app-time-line @time_change="handleTimeChange"></app-time-line>
    <app-filter></app-filter>
	<app-dimension></app-dimension>
	<app-attributes></app-attributes>
  </div>
</template>
<script>

import Vue from 'vue'
// import { updateTestData } from './vuex/actions'
// import { testData, testDataUpdateStatus } from './vuex/getters'
import { mapActions, mapGetters } from 'vuex'
import AppNetwork from './components/AppNetwork.vue'
import AppNodeTree from './components/AppNodeTree.vue'
import AppTimeLine from './components/AppTimeLine.vue'
import AppFilter from './components/AppFilter.vue'
import AppDimension from './components/AppDimension.vue'
import AppAttributes from './components/AppAttributes.vue'

export default {
  data() {
    return {
      message: 'Hello World :)',
      isSuccess: false,
      isFailed: false,
      httpData: {
        demoMysql: null,
        demoPerson: null,
        postDemoPerson: null
      },
      paramsMsg: ''
    }
  },
  components: { AppNetwork, AppNodeTree, AppTimeLine, AppFilter , AppDimension, AppAttributes},
  computed: {
    privateTestData: {
      get() {
        return this.$store.state.testData
      },
      set(v) {
        this.updateTestData(v)
      }
    },
    testDataUpdateStatus: function() {
      return this.$store.state.testDataUpdateStatus
    }
  },
  watch: {
    testDataUpdateStatus(now) {
      if (this.CommonsConfig.debug) {
        console.log(now)
        this.isSuccess = this.VuexUtils.isStatusEqual(now, this.VuexMutations.TEST_DATA_UPDATE_SUCCESS)
        this.isFailed = this.VuexUtils.isStatusEqual(now, this.VuexMutations.TEST_DATA_UPDATE_FAILED)
      }
    }
  },
  methods: {
    ...mapActions([
      'removeAllSubgraph',
    ]),
    getDemoMysql() {
      this.$http.get('/api/demo-mysql')
        .then((res) => {
          window.test_res = res.body
          this.httpData.demoMysql = res.body
        }, (res) => {
          this.httpData.demoMysql = res.body
        })
    },
    getDemoPerson() {
      this.$http.get('/api/demo-person')
        .then((res) => {
          this.httpData.demoPerson = res.body
        }, (res) => {
          this.httpData.demoPerson = res.body
        })
    },
    postDemoPerson() {
      this.$http.post('/api/demo-person', {
        name: 'name-' + Math.random(),
        sex: ['F', 'M'][~~(Math.random() * 2)],
        description: 'some desc -' + Math.random()
      }).then((res) => {
        this.httpData.postDemoPerson = res.body
      }, (res) => {
        this.httpData.postDemoPerson = res.body
      })
    },
    handleTimeChange(res) {
      console.log('index vue!! hanle time change~~', res)
      this.paramsMsg = {
        where: {
          start_time: {
            start: res[0],
            end: res[1]
          }
        },
        limit: 5000
      }
    }
  },
  mounted() {
    // test
    // this.getDemoMysql()
    // this.getDemoPerson()
  }
}

</script>
<style lang="less" scoped>
@import "./style.less";

</style>
