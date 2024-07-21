<template>
  <div v-if="$store.state.checkl && $store.state.checkspn">
  <Navbar showspHomeLink/>
  <div text-align="centre" class="margin-form">
    <form @submit.prevent="Add_camp">
        <label for="camp_name">Campaign Name:</label>
        <input class="form-control" type="text" v-model="camp_name" id="camp_name" required />
        <br />
        <label for="camp_det">Campaign Details:</label>
        <input class="form-control" type="text" v-model="camp_det" id="camp_det" required />
        <br />
        <label for="camp_bud">Campaign Budget:</label>
        <input class="form-control" type="number" v-model="camp_bud" id="camp_bud" required />
        <br />
        <label for="camp_vis">Campaign visibility:</label>
            <select class="form-control" v-model="camp_vis" id="camp_vis" required>
                <option disabled value="">Please select one</option>
                <option value="public">Public</option>
                <option value="private">Private</option>
            </select>
        <br />
        <button class="btn btn-primary" type="submit">Add Campaign</button>
    </form>
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
  name: "Add_camp",
  components:{
    Navbar,
  },
  data(){
      return{
      idu:0,
      camp_name:"",
      camp_det:"",
      camp_bud:0,
      camp_vis:""
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
      async Add_camp(){
        let token = localStorage.getItem("token");
        try {
            const response = await axios.post("/add_camp", {
                camp_name: this.camp_name,
                camp_det: this.camp_det,
                camp_bud: this.camp_bud,
                camp_vis: this.camp_vis,
                sp_id:this.idu
            }, {
                headers: {
                    Authorization: "Bearer " + token,
                    'Content-Type': 'application/json'
                }
            });
            if (response.data.message === "success") {
                this.$router.push({ name:'Sponsor', params:{id: this.idu } });

            } else {
                console.error("Failed to add Campaign");
            }
        } catch (error) {
            console.error("Error adding campaign:", error);
        }
},

      async login(){
        this.$router.push("/")
      }
  },
  mounted(){
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