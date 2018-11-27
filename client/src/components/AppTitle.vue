<template>
  <div class='title'>
    <span class="icon">
        <font-awesome-icon :icon="[prefix, icon]" />
    </span>
    <span class="text">{{msgs}}</span>
  </div>
</template>
<script>
export default {
  props: ['icon', 'msgs'],
  computed: {
    prefix: function() {
      if (this.icon == 'joomla' || this.icon == 'usb') {
        return 'fab'
      } else {
        return 'fas'
      }
    }
  },
  ready() {}
}

</script>
<style lang="less" scoped>
@import "./AppTitle.less";

</style>
