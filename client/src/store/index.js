/*
* @Author: wakouboy
* @Date:   2018-08-08 23:30:27
* @Last Modified by:   wakouboy
* @Last Modified time: 2018-11-30 18:32:54
*/
import vue from 'vue';
import vuex from 'vuex';
import state from './state.js';
import * as getters from './getters.js';
import mutations from './mutations.js';
import actions from './actions.js';
import createLogger from 'vuex/dist/logger'; // 修改日志

vue.use(vuex);

const debug = process.env.NODE_ENV !== 'production'; // 开发环境中为true，否则为false

export default new vuex.Store({
    state,
    getters,
    mutations,
    actions,
    plugins: debug ? [createLogger()] : [] // 开发环境下显示vuex的状态修改
});