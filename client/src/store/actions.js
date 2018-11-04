/**
 * Created by huangxinxin on 16/6/16.
 */
import * as types from './mutations'

export const updateTestData = function (store, data) {
  Math.random() * 10 >= 5 ? store.dispatch(types.TEST_DATA_UPDATE_SUCCESS, data)
    : store.dispatch(types.TEST_DATA_UPDATE_FAILED)
}
