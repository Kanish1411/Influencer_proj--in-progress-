<template>
  <div v-if="$store.state.checkl && $store.state.checkspn">
  <Navbar showHomeLink showCartLink/>
  <div text-align="centre" class="margin-form">
    <h1>Welcome Sponsor {{ this.idu }}</h1>
</div>
</div>
<div v-else>
{{ this.login() }}
</div>
</template>
<script>
import axios from 'axios';
import Navbar from './Navbar.vue';
export default {
  name: "Sponsor",
  components:{
    Navbar,
  },
  data(){
      return{
      Inf: [],
      idu:0,
      }
  },
  methods: {
      async checklogin(){
          let token = localStorage.getItem("token")
          const response = await axios.get("/check_login", {
              headers: {
                  Authorization: "Bearer " + token
              }}
          )
          if (response.data.message == "success") {
              this.$store.commit("setcheckl", true)
              console.log(response, this.checkl)
          }
          else {
          this.$store.commit("setcheckl", false)
          alert("Please login to access this page")
          console.log(response)
          this.$router.push('/')
          }
      },
      async checkspn(){
          let token = localStorage.getItem("token")
          const response = await axios.get("/check_spn", {
              headers: {
                  Authorization: "Bearer " + token
              }}
          )
          if (response.data.message == "success") {
              this.$store.commit("setcheckspn", true)
              console.log("ashjdguaysdguayfgiasfgouayfg")
          }
          else {
          this.$store.commit("setcheckspn", false)
          alert("You are not an Sponsor redirecting to home page")
          console.log(response)
          this.$router.push('/')
          }
      },
      async Spn(){
        let token = localStorage.getItem("token")
        const response = await axios.post("Sponsor", {
                    id: this.idu,
              },
              {
              headers: {
                  Authorization: "Bearer " + token
              }}
          )
          this.Inf=response.data.inf;
      },
      async login(){
        this.$router.push("/")
      }
  },
  mounted(){
    if(this.$store.checkl && this.$store.checkspn){
      console.log("addd")
      this.Spn();
    }
  },
  created(){
      this.checklogin(),
      this.checkspn(),
      this.idu= this.$route.params.id;
      console.log(this.idu);
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