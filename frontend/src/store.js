import { createStore }from 'vuex'
const store =  createStore({
    state(){
        return{
            token: localStorage.getItem('token'),
            user: null,
            checkl: false,
            checkadmin: false,
            checkspn:false,
            checkinf:false,
        }
    },
    mutations:{
        setcheckl(state, payload){
            state.checkl = payload
        },
        setcheckinf(state, payload){
            state.checkinf = payload
        },
        setcheckspn(state, payload){
            state.checkspn = payload
        },
        setcheckadmin(state, payload){
            state.checkadmin = payload
        }
    }
}
);
export default store