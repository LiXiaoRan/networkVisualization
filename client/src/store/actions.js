const actions = {

  modifyNodeTypeList_sync(context, obj) {
    context.commit('modifyNodeTypeList', obj)
  },

  modifyPalsyList_sync(context, obj) {
    context.commit('modifyPalsyList', obj)
  },
  modifyControlList_sync(context, obj) {
    context.commit('modifyControlList', obj)
  },
  modifyLayoutData_sync(context, obj) {
    context.commit('modifyLayoutData', obj)
  }
}

export default actions;
