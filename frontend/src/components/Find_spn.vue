<template>
    <div v-if="$store.state.checkl && $store.state.checkinf">
        <Navbar showinfHomeLink/>
        <h1>Find Ads</h1>
        <form  @submit.prevent="search">
    <input class="form-control" type="text" v-model="keyword" >
    <button class="btn btn-primary">Search</button>
    </form>
        <ul v-if="data.length > 0"> 
    <h4 v-for="c in data" :key="c.id">
        Name: {{ c.ad_name }}­ ­­­ ­ {{   }} <br>
        Campaign:  {{ c.camp_name }} ­ ­­­ ­ <br>
        Task: {{ c.task }} <br>
        Wage: {{ c.price }}<br>
        Rating: {{ c.Rating }}<br><br>
        <button class="btn btn-primary" @click="this.request(c.id)">Request</button>
    <br>
    </h4>
  </ul> 
  </div>
</template>
<script>
import axios from 'axios';
import Navbar from './Navbar.vue';
export default {
    name:"Find_spn",
    components:{
        Navbar,
    },
data(){
    return{
    data: [],
    idu:0,
    keyword:"",
    }
},
methods:{
    async checklogin() {
      let token = localStorage.getItem("token");
      if(token==null){
        this.$store.commit("setcheckl", false);
        alert("Please login to access this page");
        this.$router.push('/');
      }
      const response = await axios.get("/check_login", {
        headers: {
          Authorization: "Bearer " + token,
        },
      });
      if (response.data.message === "success") {
        this.$store.commit("setcheckl", true);
      } else {
        this.$store.commit("setcheckl", false);
        alert("Please login to access this page");
        this.$router.push('/');
      }
    },
      async checkinf(){
          let token = localStorage.getItem("token")
          const response = await axios.get("/check_inf", {
              headers: {
                  Authorization: "Bearer " + token
              }}
          )
          if (response.data.message == "success") {
              this.$store.commit("setcheckinf", true)
          }
          else {
          this.$store.commit("setcheckinf", false)
          alert("You are not an Influencer redirecting to home page")
          this.$router.push('/')
          }
      },
      async request(id){
        let token = localStorage.getItem("token")
          const response = await axios.post("/request_ad", {
            id:id,
            idu:this.idu,
           
          },{
              headers: {
                  Authorization: "Bearer " + token
              }}
          )
          this.search();
      },
      async search(){
          let token = localStorage.getItem("token")
          const response = await axios.post("find_spn", {
            id:this.idu,
            keyword: this.keyword,
                },
                {
                headers: {
                    Authorization: "Bearer " + token
                }}
            )
            this.data=response.data
            console.log(this.data);
            
        },
    
},
mounted(){
      this.search();
  },
  created(){
      this.checklogin(),
      this.checkinf(),
      this.idu= this.$route.params.id;
      console.log(this.idu);
  }

}
</script>

<style scoped>
.margin-form {
margin: 40px;
}

.message {
position: fixed;
top: 6%;
left: 50%;
transform: translateX(-50%);
padding: 10px;
width: 100%;
text-align: center;
transition: top 0.5s ease;
}

.success-message {
background-color: #4CAF50;
color: white;
}

.error-message {
background-color: #FF0000;
color: white;
}
</style>