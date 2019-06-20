<template>
  <div id="largerGraph">
  </div>
</template>


<script>
  import ForceGraph3D from '3d-force-graph';

  export default {
    name: 'largerGraph',
    mounted() {
      const elem = document.getElementById('largerGraph');
      let width = document.getElementById('largeContainer').clientWidth;
      let height = document.getElementById('largeContainer').clientHeight;

      document.getElementById('largeContainer').style.visibility = 'hidden';
      const Graph = ForceGraph3D()(elem)
        .width(width)
        .height(height)
        .jsonUrl('../../static/save1.json')
        .nodeLabel('id')
        .nodeRelSize(3)
        .nodeAutoColorBy('group')
        .numDimensions(2)
        .d3AlphaDecay(0.9)
        .enableNodeDrag(false)

      setTimeout(function () {
        document.getElementById('largeContainer').style.visibility = 'visible';
      },100)

    }
  }

</script>

<style scoped lang="css">
  #largerGraph {
    position: fixed;
    z-index: 200;
  }
</style>
