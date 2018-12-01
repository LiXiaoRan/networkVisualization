// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faChartLine, faFilter } from '@fortawesome/free-solid-svg-icons'
import { faChevronLeft,faBackward,faChevronRight,faForward} from '@fortawesome/free-solid-svg-icons'
import { faJoomla, faUsb } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faJoomla, faUsb, faChartLine, faFilter,faChevronLeft,faBackward,faChevronRight,faForward)

Vue.component('font-awesome-icon', FontAwesomeIcon)




Vue.config.productionTip = false
import api from './api/index.js'
Vue.prototype.$api = api
/* eslint-disable no-new */
import $ from 'jquery'
window.$ = $

var buildCodes = false

// buildCodes = true

{
  window.CommunicateWithServer = function(type, paramsObj, url, callback) {
    if (buildCodes) {
      paramsObj = JSON.stringify(paramsObj)
      $.ajax({
        type: type,
        url: url,
        data: { 'params': paramsObj },
        dataType: "json",
        success: function(data) {
          callback(data);
        },
        error: function(err) {
          callback(err)
        }
      })
    } else {
      let formData = new URLSearchParams();
      formData.append("params", JSON.stringify(paramsObj));
      if (type == 'get') {
        api.get(url, formData, data => {
          callback(data)
        }, error => {
          callback(error)
        })
      } else if (type == 'post') {
        api.post(url, formData, data => {
          callback(data)
        }, error => {
          callback(error)
        })
      }
    }
  }
}

import store from './store/index.js';
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
