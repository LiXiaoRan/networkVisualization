import Vue from 'vue';
import App from './App';
import router from './router';

import {library} from '@fortawesome/fontawesome-svg-core';
import {faChartLine, faFilter, faCaretDown, faPlay} from '@fortawesome/free-solid-svg-icons';
import {faChevronLeft, faBackward, faChevronRight, faForward} from '@fortawesome/free-solid-svg-icons';
import {faJoomla, faUsb} from '@fortawesome/free-brands-svg-icons';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

library.add(faJoomla, faUsb, faChartLine, faCaretDown, faPlay, faFilter, faChevronLeft, faBackward, faChevronRight, faForward);

Vue.component('font-awesome-icon', FontAwesomeIcon);


Vue.config.productionTip = false;
import api from './api/index.js';

Vue.prototype.$api = api;
/* eslint-disable no-new */
import $ from 'jquery';

window.$ = $;

var buildCodes = false;

// buildCodes = true

{
  window.CommunicateWithServer = function (type, paramsObj, url, callback) {
    if (buildCodes) {
      paramsObj = JSON.stringify(paramsObj);
      $.ajax({
        type: type,
        url: url,
        data: {'params': paramsObj},
        dataType: 'json',
        success: function (data) {
          callback(data);
        },
        error: function (err) {
          callback(err);
        }
      });
    } else {
      let formData = new URLSearchParams();
      formData.append('params', JSON.stringify(paramsObj));
      if (type === 'get') {
        api.get(url, formData, data => {
          callback(data);
        }, error => {
          callback(error);
        });
      } else if (type ==='post') {
        api.post(url, formData, data => {
          callback(data);
        }, error => {
          callback(error);
        });
      }
    }
  };
  window.select_time = {observe: '', start: '', end: '', data: []};//定义全局变量，方便数据传出
  window.nodesNumber = {};//整个数据中，节点的总数，以及主机、交换机、服务器的总数

}

import store from './store/index.js';

new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
});
