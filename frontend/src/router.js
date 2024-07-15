import { createRouter,createWebHistory } from "vue-router";
import Login from "./components/Login.vue"
import Register from "./components/Register.vue"
import Influencer from "./components/Influencer.vue"
import Sponsor from "./components/Sponsor.vue";
import Admin from "./components/Admin.vue"
import Request from '.\\components\\Request.vue'
import Add_camp from "./components/Add_camp.vue"
import Add_ad from "./components/Add_ad.vue"
import Update_camp from "./components/Update_camp.vue"
import Update_ad from "./components/Update_ad.vue"


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
    {
        path:"/add_camp/:id",
        component:Add_camp
    },
    {
         path:"/add_ad/:sp_id/:id",
        name:"Addad",
        component:Add_ad,

    },
    {
       path:"/update_camp/:sp_id/:id",
       name:"Update_camp",
       component:Update_camp,
   },
   {
    path:"/update_ad/:sp_id/:id",
    name:"Update_ad",
    component:Update_ad,
},
    


]

const router=createRouter({
    history:createWebHistory(),
    routes,
})

export default router;