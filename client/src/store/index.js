/**
 * Created by huangxinxin on 16/8/24.
 */
import Vue from 'vue'
import Vuex from 'vuex'
import utils from './utils'
import * as types from './mutations'

Vue.use(Vuex)
Vue.prototype.VuexUtils = utils
Vue.prototype.VuexMutations = types

const state = {
  testData: null,
  status: {
    testData: {
      update: null
    }
  }
}

const mutations = {
  [types.TEST_DATA_UPDATE_SUCCESS] (state, data) {
    state.testData = data
    utils.setStatus(state, 'testData.update', types.TEST_DATA_UPDATE_SUCCESS)
  },
  [types.TEST_DATA_UPDATE_FAILED] (state) {
    utils.setStatus(state, 'testData.update', types.TEST_DATA_UPDATE_FAILED)
  }
}

export default new Vuex.Store({
  strict: true,
  state, mutations
})
