// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

Vue.config.productionTip = false
import api from './api/index.js'
Vue.prototype.$api = api
/* eslint-disable no-new */

import store from './store/index.js';
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
