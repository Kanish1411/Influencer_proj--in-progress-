<template>
  <div v-if="$store.state.checkl && $store.state.checkspn">
    <Navbar showHomeLink showCampLink/>
    <h2>Influencer Details</h2>
    <h4>
    <p><strong>Name:</strong> {{ influencer?.name }}</p>
    <p><strong>Email:</strong> {{ influencer?.email }}</p>
    <form @submit.prevent="request">
    <div>
      <label for="campaignSelect">Select Campaign:</label>
      <select id="campaignSelect" v-model="camp_id" @change="fetch_ad">
        <option v-for="campaign in campaigns" :key="campaign.id" :value="campaign.id">
          {{ campaign.name }}
        </option>
      </select>
    </div>
    <br>
    <div v-if="ads.length > 0">
      <label for="adSelect">Select Ad:</label>
      <select id="adSelect" v-model="ad_id">
        <option v-for="ad in ads" :key="ad.id" :value="ad.id">
          <template v-if="ad.inf_id !=this.inf_id">
            {{ ad.name }}
          </template>
        </option>
      </select>
      <br>
      
    </div>
    <div v-else>
      No ads found
    </div>
    <button class="btn btn-primary" type="submit">Submit</button>
  </form>
  </h4>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
  name: "Req_inf",
  components: {
    Navbar,
  },
  data() {
    return {
      sp_id: 0,
      inf_id: 0,
      camp_id: 0,
      ad_id: null,
      influencer: null,
      campaigns: [],
      ads: [],
    };
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
    async request(){
      const res=await axios.post("/request_inf",{
        inf_id:this.inf_id,
        camp_id:this.camp_id,
        ad_id:this.ad_id,
        sp_id:this.sp_id,
      })
      if(res.data.message=="success"){
        this.$router.push({name:"Sponsor",params:{id:this.sp_id}});
      }
      else if(res.data.message=="Failed"){
        window.alert("Request For the following ad is Accepted");
        this.$router.push({name:"Sponsor",params:{id:this.sp_id}});
      }
      else{
        window.alert(res.data.message);
        this.$router.push({name:"Sponsor",params:{id:this.sp_id}});
      }
    },
  async fetch_inf() {
    try {
      const response = await axios.get('/inf_details', {
        params: { id: this.inf_id }
      });
      console.log('Influencer Details:', response.data);
      this.influencer = response.data;
    } catch (error) {
      console.error('Error fetching influencer details:', error);
    }
  },
  async fetch_camp() {
    try {
      const response = await axios.get(`/camp_fetch`, {
        params: { id: this.sp_id }
      });
      this.campaigns = response.data;
      console.log(this.campaigns);
    } catch (error) {
      console.error('Error fetching campaigns:', error);
    }
  },
  async fetch_ad() {
    if (this.camp_id) {
      try {
        const response = await axios.get(`/ad_fetch`, {
          params: { id: this.camp_id }
        });
        console.log('Ads:', response.data); 
        this.ads = response.data;
      } catch (error) {
        console.error('Error fetching ads:', error);
      }
    }
  },
  async login(){
        this.$router.push("/")
      }
},

  mounted() {
    this.sp_id = this.$route.params.sp_id;
    this.inf_id = this.$route.params.inf_id;
    console.log(this.inf_id);
    this.fetch_inf();
    this.fetch_camp();
  },
  created(){
      this.checklogin(),
      this.checkspn(),
      this.id= this.$route.params.id;
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