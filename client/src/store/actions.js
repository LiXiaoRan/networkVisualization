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
  modiftLayoutData_sync(context, obj) {
    context.commit('modiftLayoutData', obj)
  }
}

export default actions;
