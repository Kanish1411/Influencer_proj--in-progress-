<template>
    <div v-if="$store.state.checkl ">
    <Navbar showHomeLink showCampLink/>
    <div text-align="centre" class="margin-form">
      <h1>Find Influencers</h1>
      <form  @submit.prevent="search">
    <input class="form-control" type="text" v-model="keyword" >
    <button class="btn btn-primary">Search</button>
    </form>
        <br>
      <ul v-if="inf.length > 0">
      <h3 v-for="i in inf" :key="i.id">
       <b>name:</b> {{ i.name }} <br>
       <b>Platforms: </b>{{ i.platform }}<br>
       <b> Rating:</b> {{ i.Rating }}
        <br>
        <button class="btn btn-primary" @click="this.$router.push({name: 'Req_inf',params:{ sp_id: this.idu, inf_id:i.id}})">Request</button>
      <br>
      </h3>
    </ul>
    <h4 v-else>No Influencers available Yet</h4>
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
    name: "Find_inf",
    components:{
      Navbar,
    },
    data(){
        return{
       inf:[],
        idu:0,
        }
    },
    methods: {
      async checklogin() {
      let token = localStorage.getItem("token");
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
    async checkspn() {
      let token = localStorage.getItem("token");
      const response = await axios.get("/check_spn", {
        headers: {
          Authorization: "Bearer " + token,
        },
      });
      if (response.data.message === "success") {
        this.$store.commit("setcheckspn", true);
      } else {
        this.$store.commit("setcheckspn", false);
        alert("You are not a Sponsor. Redirecting to home page");
        this.$router.push('/');
      }
    },
    async search(){
          let token = localStorage.getItem("token")
          const response = await axios.post("find_inf", {
            keyword: this.keyword,
                },
                {
                headers: {
                    Authorization: "Bearer " + token
                }}
            )
            this.inf=response.data.inf
        },
        async login(){
          console.log("login required")
          this.$router.push("/")
        }
    },
    async mounted() { 
    if (this.$store.state.checkl && this.$store.state.checkspn) {
      await this.search();
    }
  },
  async created() {
    await this.checklogin();
    await this.checkspn();
    this.idu = this.$route.params.id;
    console.log(this.idu);
  },
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