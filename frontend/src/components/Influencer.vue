<template>
  <div v-if="$store.state.checkl && $store.state.checkinf">
  <Navbar showHomeLink showFindspn/>
  <div text-align="centre" class="margin-form">
    <h2>Welcome Influencer {{ this.idu }}</h2>
    <h3>Active Campaigns</h3>
    <ul v-if="camp.length > 0"> 
    <h4 v-for="c in camp" :key="c.id">
        Name: {{ c.ad_name }}­ ­­­ ­ {{   }} Sponsor_id:  {{ c.Sponser }} ­ ­­­ ­ Campaign_id: {{ c.Campaign_id }}
    <br>
    </h4>
  </ul>
  <h4 v-else>No Active Campaigns available Yet</h4>
  <br>
  <h3>Requests</h3>
    <ul v-if="req.length > 0"> 
    <h4 v-for="r in req" :key="r.id">
        Name: {{ r.name }}    <br>
        Request: {{ r.req }}<br>
        Campaign: {{ r.camp }} <br>
        <button class="btn btn-primary" @click="this.accept(r.id)">Accept</button>{{  }}
        <button class="btn btn-primary" @click="this.reject(r.id)">Reject</button>
      </h4>
  </ul>
  <h4 v-else>No Request available Yet</h4>
</div>
</div>
</template> 

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';
export default {
  name: "Influencer",
  components:{
    Navbar,
  },
  data(){
      return{
      camp: [],
      req:[],
      idu:0,
      }
  },
  methods: {
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
      async Inf(){
        let token = localStorage.getItem("token")
        const response = await axios.post("/Influencer", {
                id: this.$route.params.id,
              },
              {
              headers: {
                  Authorization: "Bearer " + token
              }}
          )
          this.camp=response.data.camp;
          this.req=response.data.req;
      },
      async accept(id){
        let token=localStorage.getItem("token")
        const resp=await axios.post("/accept_req",{
          id:id,
        },{
          headers:{
            Authorization:"Bearer"+token
          }
        })
        this.Inf();
      },
      async reject(id){
        let token=localStorage.getItem("token")
        const resp=await axios.post("/reject_req",{
          id:id,
        },{
          headers:{
            Authorization:"Bearer"+token
          }
        })
        this.Inf();
      },
  },
  mounted(){
      this.Inf();
  },
  created(){
      this.checklogin(),
      this.checkinf(),
      this.idu= this.$route.params.id;
  }
};
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