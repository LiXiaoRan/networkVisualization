/*
 * @Author: wakouboy
 * @Date:   2018-11-04 23:57:26
 * @Last Modified by:   wakouboy
 * @Last Modified time: 2018-11-05 18:46:58
 */
import AppNodeTree from '../AppNodeTree.vue'
const d3 = require('d3')
// const _ = require('lodash')
export default class NodeLinkGraph {
  constructor(layoutPara) {
    let self = this
    self.view = layoutPara.view
    let viewWidth = layoutPara.width
    let viewHeight = layoutPara.height
    self.simpleFlag = layoutPara.simpleFlag
    self.nodeDragFlag = layoutPara.nodeDragFlag
    self.hoverHighlight = layoutPara.hoverHighlight
    self.viewSize = {
      width: viewWidth,
      height: viewHeight
    }
    self.initView(self.view)
  }
  initView(view) {
    let self = this
    let linkG = view.append('g').attr('class', 'linkG')
    let nodeG = view.append('g').attr('class', 'nodeG')
    self.viewG = {
      'linkG': linkG,
      'nodeG': nodeG
    }
  }

  setData(data) {
    let self = this
    self.data = data
    console.log('brush+++++++++', data)
    let viewWidth = self.viewSize.viewWidth
    let viewHeight = self.viewSize.viewHeight
    let simpleFlag = getSimpleFlag(data, self.simpleFlag)
    let hoverHighlight = self.hoverHighlight
    let nodeDragFlag = self.nodeDragFlag
    // handle the graph view
    window.test_graphData = data
    self.handleData(data, viewWidth, viewHeight)
    self.drawLayout(data, self.viewG.nodeG, self.viewG.linkG, simpleFlag)
    self.calLayout(data, self.ticked)
    self.addInteraction({
      nodeItem: self.view.selectAll('g.node'),
      linkItem: self.view.selectAll('g.link'),
      nodeG: self.view.select('.nodeG'),
      linkG: self.view.select('.linkG'),
      nodeDragFlag: nodeDragFlag,
      hoverHighlightFlag: hoverHighlight
    }, data.dataVal)

    function getSimpleFlag(vData, vSimpleFlag) {
      if (Array.isArray(vSimpleFlag)) {
        let nodeThre = vSimpleFlag[0]
        let linkThre = vSimpleFlag[1]
        let nodeLen = vData.nodes.length
        let linkLen = vData.links.length
        if (nodeLen >= nodeThre && linkLen >= linkThre) {
          return true
        } else {
          return false
        }
      } else {
        return vSimpleFlag
      }
    }
  }

  handleData(data, width, height) {
    const PI = Math.PI
    let minVal = d3.min(data.nodes, d => d.val)
    let maxVal = d3.max(data.nodes, d => d.val)
    let rScale = d3.scaleLinear().domain([minVal, maxVal]).range([3, 10])
    let cx = width / 2
    let cy = height / 2
    data.nodes.forEach(function(dItem, iItem) {
      let val = dItem.val
      let input = dItem.input
      let output = dItem.output
      let outputAngle = PI * 2 * output / (input + output)
      dItem.r = rScale(val)
      dItem.x = cx
      dItem.y = cy
      dItem.outputArc = {
        startAngle: 0,
        endAngle: outputAngle,
        stroke: '#15ca8c',
        'stroke-width': '2px'
      }
      dItem.inputArc = {
        startAngle: outputAngle,
        endAngle: 2 * PI,
        stroke: '#c80218',
        'stroke-width': '2px'
      }
    })

    data.links.forEach(function(dItem, iItem) {
      let val = dItem.val
      let output = dItem.output
      let ratio = output / val
      dItem.ratio = ratio
    })
  }

  calLayout(data) {
    let self = this
    let width = self.viewSize.width
    let height = self.viewSize.height
    // function
    let updateNodePos = function() {
      let xMin = d3.min(data.nodes, d => d.x)
      let xMax = d3.max(data.nodes, d => d.x)
      let yMin = d3.min(data.nodes, d => d.y)
      let yMax = d3.max(data.nodes, d => d.y)
      let widthScale = d3.scaleLinear().range([xMin, xMax]).domain([xMin, xMax])
      let heightScale = d3.scaleLinear().range([yMin, yMax]).domain([yMin, yMax])
      if (xMin < 0 || xMax > width) {
        widthScale.range([0 + 20, width - 20])
      }
      if (yMin < 0 || yMax > height) {
        heightScale.range([0 + 20, height - 20])
      }
      data.nodes.forEach(function(dItem, iItem) {
        dItem.x = widthScale(dItem.x)
        dItem.y = heightScale(dItem.y)
      })
    }
    let ticked = function() {
      if (this.alpha() > 0.5) return
      let nodes = self.viewG.nodeG.selectAll('.node')
      let links = self.viewG.linkG.selectAll('.link')
      if (this.alpha() < 0.03) {
        updateNodePos()
      }
      // if (this.alpha() < 0.02) {
      //   this.simulation.stop()
      // }
      nodes.attr('transform', function(d, i) {
        if (isNaN(d.x) || isNaN(d.y)) {
          return d3.select(this).attr('transform')
        } else {
          return 'translate( ' + d.x + ', ' + d.y + ')'
        }
      })
      links.selectAll('.centerPath').attr('d', function(d, i) {
        if (isNaN(d.source.x) || isNaN(d.source.y) || isNaN(d.target.x) || isNaN(d.target.y)) {
          return d3.select(this).attr('d')
        } else {
          return 'M ' + d.source.x + ', ' + d.source.y + ' L ' + d.target.x + ', ' + d.target.y
        }
      })
      // update other path
      links.selectAll('.bottomBar').attr('transform', function(d, i) {
        let r = d.target.r + 2
        let len = Math.sqrt((d.target.y - d.source.y) * (d.target.y - d.source.y) + (d.target.x - d.source.x) * (d.target.x - d.source.x))
        let ratio = (len - r) / len
        let x = (d.target.x - d.source.x) * ratio + d.source.x
        let y = (d.target.y - d.source.y) * ratio + d.source.y
        let angle = Math.atan((d.target.y - d.source.y) / (d.target.x - d.source.x))
        angle = (angle) / Math.PI * 180
        if (isNaN(x) || isNaN(y) || isNaN(angle)) {
          return d3.select(this).attr('transform')
        } else {
          return 'translate( ' + x + ', ' + y + ') rotate(' + angle + ')'
        }
      })

      links.selectAll('.linkH').attr('transform', function(d, i) {
        let x = (d.source.x + d.target.x) / 2
        let y = (d.source.y + d.target.y) / 2
        let angle = Math.atan((d.target.y - d.source.y) / (d.target.x - d.source.x))
        angle = (angle) / Math.PI * 180
        if (isNaN(angle)) {
          return 'translate( ' + x + ', ' + y + ')'
        } else {
          return 'translate( ' + x + ', ' + y + ') rotate(' + angle + ')'
        }
      })
    }
    this.simulation = d3.forceSimulation()
      .force('center', d3.forceCenter().x(width * 0.5).y(height * 0.5))
      .force('index-collide', d3.forceCollide(d => d.r * 1.5))
      .force('link', d3.forceLink().id(d => d.id).distance(function() {
        let nodeNum = data.nodes.length
        let linkNum = data.links.length
        let alpha = 0.8
        let divisor = nodeNum * alpha + linkNum * (1 - alpha)
        let idealDistance = width * height / divisor
        if (isNaN(idealDistance) || divisor < 10000) {
          return 35
        } else if (idealDistance < 10) {
          return 10
        } else {
          return idealDistance
        }
      }))
      .force('charge', d3.forceManyBody().strength(-50))
      .force('x', d3.forceX().strength(0.11))
      .force('y', d3.forceY().strength(0.11))
    this.simulation
      .nodes(data.nodes)
      .on('tick', ticked)

    this.simulation
      .force('link')
      .links(data.links)
  }

  drawLayout(data, nodeG, linkG, simpleFlag) {
    let inputArc = d3.arc()
      .innerRadius(0)
      .outerRadius(d => d.r)
      .startAngle(d => d.inputArc.startAngle)
      .endAngle(d => d.inputArc.endAngle)

    let outputArc = d3.arc()
      .innerRadius(0)
      .outerRadius(d => d.r)
      .startAngle(d => d.outputArc.startAngle)
      .endAngle(d => d.outputArc.endAngle)
    // draw nodes
    let nodes = nodeG.selectAll('.node').data(data['nodes'], function(d, i) {
      return d.id
    })
    let newNodes = nodes.enter().append('g').attr('class', function(d, i) {
      return 'node ' + d.id
    })
    if (simpleFlag === false) {
      newNodes.append('path').attr('class', 'input-arc').attr('d', inputArc).attr('stroke-width', d => d['inputArc']['stroke-width']).attr('stroke', d => d.inputArc.stroke)
      newNodes.append('path').attr('class', 'output-arc').attr('d', outputArc).attr('stroke-width', d => d['outputArc']['stroke-width']).attr('stroke', d => d.outputArc.stroke)
    }
    newNodes.append('circle').attr('r', d => d.r)
    nodeG.selectAll('.node').attr('transform', function(d, i) {
      if (!isNaN(d.x) && !isNaN(d.y)) {
        return 'translate( ' + d.x + ', ' + d.y + ')'
      }
    })
    nodeG.selectAll('.node circle').classed('simpleCircle', simpleFlag)
    nodes.exit().remove()
    // draw links
    linkG.selectAll('.link').remove()
    let links = linkG.selectAll('.link').data(data['links'], function(d, i) {
      return d.id
    })
    let newLinks = links.enter().append('g').attr('class', function(d, i) {
      return 'link ' + d.id + ' s-' + d.source + ' t-' + d.target
    })
    newLinks.append('path').attr('class', 'centerPath').attr('stroke-width', '1px').attr('stroke', '#888')
    if (simpleFlag === false) {
      let linkH = newLinks.append('g').attr('class', 'linkH')
      linkH.append('path').attr('class', 'topH').attr('stroke-width', '1px').attr('d', 'M -2, 1.5 L 2, 1.5')
      linkH.append('path').attr('class', 'bottomH').attr('stroke-width', '1px').attr('d', 'M -2, -1.5 L 2, -1.5')
      linkH.append('path').attr('class', 'centerH').attr('stroke-width', '1px').attr('d', 'M 0, -1.5 L 0, 1.5')
      newLinks.append('path').attr('class', 'bottomBar').attr('stroke-width', '1px').attr('d', 'M 0, -3 L 0, 3')
    }
    links.exit().remove()
  }

  getNeighborNodeIdArr(nodeId) {
    let self = this
    let links = self.data.links
    let nodeIdArr = []
    let nodeIdDict = {}
    links.forEach(function(dLink, iLink) {
      let sourceId, targetId
      if ((typeof dLink.source) === 'object') {
        sourceId = dLink.source.id
        targetId = dLink.target.id
      } else {
        sourceId = dLink.source
        targetId = dLink.target
      }
      if (sourceId === nodeId && nodeIdDict[targetId] === undefined) {
        nodeIdDict[targetId] = true
        nodeIdArr.push(targetId)
      }
      if (targetId === nodeId && nodeIdDict[sourceId] === undefined) {
        nodeIdDict[sourceId] = true
        nodeIdArr.push(sourceId)
      }
    })
    return nodeIdArr
  }

  addInteraction(interactionTypeObj, dataVal) {
    let self = this
    let nodeItem = interactionTypeObj.nodeItem
    // let linkItem = interactionTypeObj.linkitem
    let linkG = interactionTypeObj.linkG
    let nodeG = interactionTypeObj.nodeG
    let nodeDragFlag = interactionTypeObj.nodeDragFlag
    let hoverHighlightFlag = interactionTypeObj.hoverHighlightFlag
    addNodeDrag(nodeDragFlag)
    addNodeHoverHighlight(hoverHighlightFlag)

    function addNodeDrag(flag) {
      if (flag === true) {
        nodeItem.call(d3.drag()
          .on('start', dragStart)
          .on('drag', dragging)
          .on('end', dragEnd)
        )
        nodeItem.on('click', function() {
          let neighborId = []
          let mainId
          let nodeTree = {}
          mainId = d3.select(this).attr('class').split(' ')[1]
          neighborId.push(mainId)
          d3.selectAll('.hover-active').each(function(d) {
            neighborId.push(d3.select(this).attr('class').split(' ')[1])
          })
          for (let i = 0; i < neighborId.length; i++) {
            dataVal.forEach(function(d) {
              if (d.send_node_global_id === neighborId[i] && d.receive_node_global_id !== neighborId[i]) {
                if (nodeTree[neighborId[i]]) {
                  let val = +d.val
                  let temp = [val, 0]
                  nodeTree[neighborId[i]]['sendAndrec'].push(temp)
                } else {
                  nodeTree[neighborId[i]] = { 'sendAndrec': [] }
                  let val = +d.val
                  let temp = [val, 0]
                  nodeTree[neighborId[i]]['sendAndrec'].push(temp)
                }
              }
              if (d.receive_node_global_id === neighborId[i] && d.send_node_global_id !== neighborId[i]) {
                if (nodeTree[neighborId[i]]) {
                  let val = +d.val
                  let temp = [0, val]
                  nodeTree[neighborId[i]]['sendAndrec'].push(temp)
                } else {
                  nodeTree[neighborId[i]] = { 'sendAndrec': [] }
                  let val = +d.val
                  let temp = [0, val]
                  nodeTree[neighborId[i]]['sendAndrec'].push(temp)
                }
              }
              if (d.receive_node_global_id === neighborId[i] && d.send_node_global_id === neighborId[i]) {
                if (nodeTree[neighborId[i]]) {
                  let val = +d.val
                  let temp = [val, val]
                  nodeTree[neighborId[i]]['sendAndrec'].push(temp)
                } else {
                  nodeTree[neighborId[i]] = { 'sendAndrec': [] }
                  let val = +d.val
                  let temp = [val, val]
                  nodeTree[neighborId[i]]['sendAndrec'].push(temp)
                }
              }
            })
          }
          let mainData = []
          let neighborNodeData = []
          let id = []
          for (let i = 1; i < neighborId.length; i++) {
            let temp = nodeTree[neighborId[i]]['sendAndrec']
            id.push(neighborId[i])
            neighborNodeData.push(temp)
          }
          mainData = nodeTree[mainId]['sendAndrec']
          console.log(nodeTree)
          d3.select('#Panel').selectAll('svg').remove()
          d3.select('#Panel').selectAll('div').remove()
          AppNodeTree.methods.MainNodeInf(mainData)
          console.log(id)
          AppNodeTree.methods.HeatLineInf(id, neighborNodeData)
        })
      } else {
        nodeItem.on('mousedown.drag', null)
      }

      function dragStart() {
        d3.select(this).raise().classed('drag-active', true)
      }

      function dragging(d) {
        d.x = d3.event.x
        d.y = d3.event.y
        d3.select(this).attr('transform', 'translate(' + d.x + ', ' + d.y + ')')
        // update link
        let nodeId = d.id
        updateLink(linkG.selectAll('.s-' + nodeId))
        updateLink(linkG.selectAll('.t-' + nodeId))
      }

      function dragEnd() {
        d3.select(this).classed('drag-active', false)
      }

      function updateLink(linkItem) {
        linkItem.selectAll('.centerPath').attr('d', d => 'M ' + d.source.x + ', ' + d.source.y + ' L ' + d.target.x + ', ' + d.target.y)
        // update other path
        linkItem.selectAll('.bottomBar').attr('transform', function(d, i) {
          let r = d.target.r + 2
          let len = Math.sqrt((d.target.y - d.source.y) * (d.target.y - d.source.y) + (d.target.x - d.source.x) * (d.target.x - d.source.x))
          let ratio = (len - r) / len
          let x = (d.target.x - d.source.x) * ratio + d.source.x
          let y = (d.target.y - d.source.y) * ratio + d.source.y
          let angle = Math.atan((d.target.y - d.source.y) / (d.target.x - d.source.x))
          angle = (angle) / Math.PI * 180
          if (isNaN(x) || isNaN(y) || isNaN(angle)) {
            return d3.select(this).attr('transform')
          } else {
            return 'translate( ' + x + ', ' + y + ') rotate(' + angle + ')'
          }
        })

        linkItem.selectAll('.linkH').attr('transform', function(d, i) {
          let x = (d.source.x + d.target.x) / 2
          let y = (d.source.y + d.target.y) / 2
          let angle = Math.atan((d.target.y - d.source.y) / (d.target.x - d.source.x))
          angle = (angle) / Math.PI * 180
          if (isNaN(angle)) {
            return 'translate( ' + x + ', ' + y + ')'
          } else {
            return 'translate( ' + x + ', ' + y + ') rotate(' + angle + ')'
          }
        })
      }
    }

    function addNodeHoverHighlight(flag) {
      if (flag === true) {
        nodeItem.on('mouseover', function(d) {
            let nodeId = d.id
            let neighborNodeIdArr = self.getNeighborNodeIdArr(nodeId)
            neighborNodeIdArr.forEach(function(dId, iId) {
              nodeG.selectAll('g.node.' + dId).classed('hover-active', true)
            })
          })
          .on('mouseout', function(d) {
            nodeG.selectAll('g.node').classed('hover-active', false)
          })
      } else {
        nodeItem.on('mouseover', null)
      }
    }
  }

}
