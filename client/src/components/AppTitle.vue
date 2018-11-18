<template>
  <div class = 'title'>
    <span class="icon" v-html="icon"></span>
    <span class="text">{{msgs}}</span>
  </div>
</template>

<script>
  export default {
    props: ['icon', 'msgs'],
    ready () {}
  }
</script>
<style lang="less" scoped>
  @import "./AppTitle.less";
</style>