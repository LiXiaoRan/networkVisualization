<template>
  <div id = 'network-panel'>
      <app-title v-bind:icon="icon" v-bind:msgs="msgs"></app-title>
      <div class = 'view'>
          <svg class = 'view-svg'>
            <g class = 'container'></g>
          </svg>
      </div>
  </div>
</template>

<script>
  import AppTitle from './AppTitle.vue'
  import NodeLinkGraph from './layout/NodeLinkGraph.js'
  const d3 = require('d3')
  export default {
    data () {
      return {
        icon: '<i class="fa fa-joomla" aria-hidden="true"></i>',
        msgs: '多层网络'
      }
    },
    components: {AppTitle},
    props: {
      paramsMsg: {
        default () {
          return {
            limit: 50
          }
        }
      }
    },
    methods: {
      // 数据查询样例
      // api：https://itbilu.com/nodejs/npm/V1PExztfb.html
      getDemoMysql (handleMethod) {
        // insert
        this.$http
        .post('/api/demo-mysql', {id: 345, name: 'testststst'})
        .then((res) => {
          console.log('插入成功！')
        })
        .catch((error) => {
          console.log('插入失败', error)
        })

        // delete
        this.$http
        .delete('/api/demo-mysql', {params: {id: 345}})
        .then((res) => {
          console.log('删除成功！')
        })
        .catch((error) => {
          console.log('删除失败', error)
        })

        // update
        this.$http.put('/api/demo-mysql', {id: 23, name: 'update'})
        .then((res) => {
          console.log('更新成功')
          window.test_sqlData = res.body.data
          handleMethod(res.body.data)
        })
        .catch((error) => {
          console.log('更新失败', error)
        })

        // query
        this.$http.get('/api/demo-mysql', {params: {id: 23}})
          .then((res) => {
            console.log('查询成功')
          }).catch((error) => {
            console.log('查询失败', error)
          })
      },
      searchData (params) {
        // query
        this.getDataWithParams(this.handleGraphData, params)
      },
      getDataWithParams (handleMethod, paramsObj) {
        // test /api/demo-mysql   发布： /network_security/api/demo-mysql
        this.$http.get('/api/demo-mysql', {params: paramsObj})
          .then((res) => {
            console.log('查询成功')
            let data = JSON.parse(JSON.stringify(res.body.data))
            handleMethod(data)
          }).catch((error) => {
            console.log('查询失败', error)
          })
      },
      enableZoomEvent (flag) {
        let self = this
        let domItem = d3.select(self.$el)
        let svg = domItem.select('.view-svg')
        if (flag === true) {
          let container = svg.select('.container')
          svg.call(d3.zoom().on('zoom', function () {
            container.attr('transform', d3.event.transform)
          }))
        } else {
          svg.call(d3.zoom().on('zoom', null))
        }
      },
      handleGraphData (data) {
        console.log('zenmela2')
        window.test_sqlGraphData = data
        let self = this
        let nodes = []
        let nodeDict = {}
        let links = []
        let linkDict = {}
        data.forEach(function (dItem, iItem) {
          let sourceId = dItem['send_node_global_id']
          let targetId = dItem['receive_node_global_id']
          let val = +dItem['val']
          addNode(sourceId, nodeDict, nodes, val)
          addNode(targetId, nodeDict, nodes, val)
          if (sourceId !== targetId) {
            addLink(sourceId, targetId, linkDict, links, val)
          }
        })
        let graphData = {
          nodes: nodes,
          links: links,
          dataVal: data
        }
        window.test_graphData = graphData
        self.nodeLinkGraph.setData(graphData)

        function addNode (nodeId, nodeDict, nodes, val, type) {
          if (nodeDict[nodeId] === undefined) {
            let obj = {
              id: nodeId,
              val: val,
              input: (type === 'source' ? 0 : val),
              output: (type === 'target' ? 0 : val)
            }
            nodeDict[nodeId] = nodes.length
            nodes.push(obj)
          } else {
            let node = nodes[nodeDict[nodeId]]
            node.val += val
            if (type === 'source') {
              node.output += val
            } else {
              node.input += val
            }
          }
        }

        function addLink (sourceId, targetId, linkDict, links, val) {
          let linkId = 's-' + sourceId + '-t-' + targetId
          let linkId1 = 's-' + targetId + 't-' + sourceId
          if (linkDict[linkId] === undefined && linkDict[linkId1] === undefined) {
            let obj = {
              id: linkId,
              source: sourceId,
              target: targetId,
              val: val,
              input: 0,
              output: 0
            }
            linkDict[linkId] = links.length
            links.push(obj)
          } else {
            links[linkDict[linkId]].val += val
          }
          if (linkDict[linkId] !== undefined) {
            links[linkDict[linkId]].output += val
          } else {
            links[linkDict[linkId1]].input += val
          }
        }
      }
    },
    mounted () {
      let self = this
      // console.log('nihao~~~~~')
      // // 相关的api请查看https://itbilu.com/nodejs/npm/VJIR1CjMb.html
      // let params = {
      //   where: {
      //     start_time: {
      //       $gte: '20160716014752000000',
      //       $lt: '20160716014754000000'
      //     }
      //   },
      //   limit: 50
      // }
      // console.log(params, '~~~', this.paramsMsg)
      // // this.searchData(params)
      let domItem = d3.select(self.$el)
      let svg = domItem.select('.view-svg')
      let width = parseFloat((svg.attr('width')) === null ? (svg.style('width')) : (svg.attr('width')))
      let height = parseFloat((svg.attr('height')) === null ? (svg.style('height')) : (svg.attr('height')))
      let graphG = svg.select('.container').append('g')
      self.nodeLinkGraph = new NodeLinkGraph({
        view: graphG,
        width: width,
        height: height,
        simpleFlag: [1000, 1000],
        nodeDragFlag: true,
        hoverHighlight: true
      })
      self.enableZoomEvent(true)
    },
    watch: {
      paramsMsg: function (res) {
        console.log('watch~~~', this.paramsMsg)
        this.searchData(res)
      }
    }
  }
</script>


<style lang="less" scoped>
  @import "./AppNetwork.less";
</style>