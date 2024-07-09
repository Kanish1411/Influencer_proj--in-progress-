import { createRouter,createWebHistory } from "vue-router";
import Login from "./components/Login.vue"
import Register from "./components/Register.vue"
// import Sponser_Register from "./components/Sponser_Register.vue";
import Influencer from "./components/Influencer.vue"
import Sponsor from "./components/Sponsor.vue";
import Admin from "./components/Admin.vue"
import Request from '.\\components\\Request.vue'
const routes=[
    {
        path:'/',
        name:'Login',
        component:Login
    },
    {
        path:'/register',
        name:'register',
        component:Register
    },
    {
        path:"/influencer/:id",
        component:Influencer,
        name:"Influencer"
    },
    {
        path:"/sponsor/:id",
        component:Sponsor,
        name:"Sponsor"
    },
    {
        path:"/admin",
        component:Admin,
        name:"Admin"
    },
    {
        path:"/request",
        component:Request
    },

]

const router=createRouter({
    history:createWebHistory(),
    routes,
})

export default router;