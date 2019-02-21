const mutations = {

  modifyNodeTypeList(state, obj) {
    state.nodeTypeList = obj.nodeTypeList;
  },

  modifyPalsyList(state, obj) {
    state.palsyLevelList = obj.palsyLevelList;
  },
  modifyControlList(state, obj) {
    state.controlLevelList = obj.controlLevelList;
  },

  modifySelectTime(state, obj) {
    state.selectTime = obj;
  },

  modifySelectData(state, arr) {
    state.selectData = arr;
  },

  modifyLayoutData(state, obj) {
    state.layoutData = obj.layoutData;
  }
}

export default mutations;
