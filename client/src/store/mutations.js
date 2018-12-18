const mutations = {
    
    modifyNodeTypeList(state,obj){
        state.nodeTypeList=obj.nodeTypeList;
    },
    
    modifyNodeAttrList(state,obj){
        state.nodeAttrList=obj.nodeAttrList;
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