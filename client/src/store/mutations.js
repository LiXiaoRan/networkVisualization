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
  }

}

export default mutations;


// export const mutations = {
//     modifyNodeTypeList(state, obj) {
//         state.nodeTypeList=obj.nodeTypeList
//     },
//     modifyNodeAttrList (state,obj) {
//         state.nodeAttrList=obj.nodeAttrList
//     }
//   }
