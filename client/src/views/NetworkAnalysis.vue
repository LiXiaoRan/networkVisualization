<template>
  <div id="AnalysisList">
    <h1>高级网络特性分析</h1>
    <div class="analysis-container">
      <router-link target="_blank" to="/different">
        <button class="analysis-btn">异常检测</button>
      </router-link>
      <router-link target="_blank" to="/compare">
        <button class="analysis-btn">属性判证</button>
      </router-link>
      <router-link target="_blank" to="/multilayer">
        <button class="analysis-btn">多层结构</button>
      </router-link>
      <router-link target="_blank" to="/accompany">
        <button class="analysis-btn">伴随关系</button>
      </router-link>
    </div>
  </div>
</template>
<style lang="less" scoped>
  #AnalysisList {
    h1 {
      margin-left: 10px;
      text-align: center;
    }

    .analysis-container {
      width: 80%;
      margin: 50px auto;
      text-align: center;

      .analysis-btn {
        width: 100px;
        height: 30px;
        margin: 10px;
        border-radius: 5px;
      }
    }
  }
</style>
