<template>
    <div v-if="$store.state.checkl  && $store.state.checkadmin">
    <Navbar showadHomeLink />
    <div text-align="centre" class="margin-form">
      <h1>Request page</h1>
      <br>
      <ul v-if="req.length > 0">
        <h4 v-for="r in req" :key="r.id">
  
          Sponsor id : {{ r.id }} <br>
          Sponsor Name : {{ r.name }} <br>
          <br>
          <button class="btn btn-primary" @click="acc(r.id)">Accept</button>
          <br>
          <br>
        </h4>
        
      </ul>
      <h4 v-else>No Requests available Yet</h4>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';
export default {
    name: "Request",
    components:{
      Navbar,
    },
    data(){
        return{
        req: [],
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
          }
          else {
          this.$store.commit("setcheckl", false)
          alert("Please login to access this page")
          this.$router.push('/')
          }
      },
        async checkad(){
          let token = localStorage.getItem("token")
            const response = await axios.get("/check_ad",{
                headers: {
                    Authorization: "Bearer " + token
                }}
            )
            if (response.data.message == "success") {
                this.$store.commit("setcheckadmin", true);

            }
            else {
            this.$store.commit("setcheckadmin", false)
            alert("You are not an Admin redirecting to home page")
            this.$router.push('/')
            }
        },
        async getreq(){
            const response =await axios.get("Sponsor_req",{})
            this.req=response.data
        },
        async acc(id){
          try {
        let token = localStorage.getItem("token");
        const response = await axios.post("/accept", {
          id: id,
        }, {
          headers: {
            Authorization: "Bearer " + token,
          },
        });
        window.location.reload();
        console.log(response.data.message);
            } catch (error) {
          console.error("Error accepting request:", error);
      }
        },
    },
    mounted(){
        this.getreq()
    },
    created(){
        this.checklogin()
        this.checkad()
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