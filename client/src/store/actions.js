const actions = {
    
    modifyNodeTypeList_sync(context,obj){
        context.commit('modifyNodeTypeList',obj)
    },
    
    modifyNodeAttrList_sync(context,obj){
        context.commit('modifyNodeAttrList',obj)
    }

}

export default actions;
