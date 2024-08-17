<template>
  <div v-if="$store.state.checkl && $store.state.checkspn">
  <Navbar showHomeLink showCartLink/>
  <div text-align="centre" class="margin-form">
    <form @submit.prevent="Add_ad">
        <label for="camp_name">Ad Name:</label>
        <input class="form-control" type="text" v-model="ad_name" id="ad_name" required />
        <br />

        <label for="camp_bud">Ad Budget:</label>
        <input class="form-control" type="number" v-model="ad_bud" id="ad_bud" required />
        <br />
        <label for="camp_vis">Ad requirements:</label>
        <input class="form-control" type="text" v-model="ad_req" id="ad_req" required />
        <br />
        <button class="btn btn-primary" type="submit">Add Ad</button>
    </form>
</div>
</div>
</template>
<script>
import axios from 'axios';
import Navbar from './Navbar.vue';
export default {
  name: "Add_ad",
  components:{
    Navbar,
  },
  data(){
      return{
      idu:0,
      sp_id:0,
      ad_name:"",
      ad_bud:0,
      ad_req:""
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
      async checkspn(){
          let token = localStorage.getItem("token")
          const response = await axios.get("/check_spn", {
              headers: {
                  Authorization: "Bearer " + token
              }}
          )
          if (response.data.message == "success") {
              this.$store.commit("setcheckspn", true)
          }
          else {
          this.$store.commit("setcheckspn", false)
          alert("You are not an Sponsor redirecting to home page")
          console.log(response)
          this.$router.push('/')
          }
      },
      async Add_ad(){
        let token = localStorage.getItem("token");
        try {
            const response = await axios.post("/add_ad", {
                ad_name: this.ad_name,
                ad_bud: this.ad_bud,
                ad_req: this.ad_req,
                id:this.idu
            }, {
                headers: {
                    Authorization: "Bearer " + token,
                    'Content-Type': 'application/json'
                }
            });
            if (response.data.message === "success") {
                this.$router.push({ name:'Sponsor', params:{id: this.sp_id } });

            } else {
                console.error("Failed to add Campaign");
            }
        } catch (error) {
            console.error("Error adding campaign:", error);
        }
    },
  },
  mounted(){
  },
  created(){
    console.log(this.$route.params.sp_id);
      this.checklogin(),
      this.checkspn(),
      this.idu= this.$route.params.id;
      this.sp_id=this.$route.params.sp_id;
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