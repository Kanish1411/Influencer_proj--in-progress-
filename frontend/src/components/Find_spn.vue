<template>
    <div v-if="$store.state.checkl && $store.state.checkinf">
        <Navbar />
        <!-- change navbar -->
        <ul v-if="data.length > 0"> 
    <h4 v-for="c in data" :key="c.id">
        Name: {{ c.ad_name }}­ ­­­ ­ {{   }} Sponsor_id:  {{ c.Sponser }} ­ ­­­ ­ Campaign_id: {{ c.Campaign_id }}
    <br>
    </h4>
  </ul>
  <h4 v-else>No Active Campaigns available Yet</h4>
  <br>
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
    }
},
methods:{
    async checklogin(){
        let token=localStorage.getItem("token");
        const response = await axios.get("/check_login", {
              headers: {
                  Authorization: "Bearer " + token
              }}
          )
          if (response.data.message == "success") {
              this.$store.commit("setcheckl", true)
              console.log(response, this.$store.checkl)
          }
          else {
          this.$store.commit("setcheckl", false)
          alert("Please login to access this page")
          this.$router.push('/')
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
      async funct(){
        let token = localStorage.getItem("token")
          const response = await axios.get("/find_spn", {
              headers: {
                  Authorization: "Bearer " + token
              }}
          )
          this.data=response.data;
          console.log(this.data)
      },
      async login(){
        this.$router.push("/")
      }
},
mounted(){
      this.funct();
  },
  created(){
      this.checklogin(),
      this.checkinf(),
      this.idu= this.$route.params.id;
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