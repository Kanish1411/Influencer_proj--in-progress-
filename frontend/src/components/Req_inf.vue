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
      <select id="campaignSelect" v-model="camp_id" @change="fetchAds">
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
          {{ ad.name }}
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
      ad_id: 0,
      influencer: null,
      campaigns: [],
      ads: [],
    };
  },
  methods: {
    async request(){
      console.log("askjdgiagbsdkjabdb");
      const res=await axios.post("/request_inf",{
        inf_id:this.inf_id,
        camp_id:this.camp_id,
        ad_id:this.ad_id,
      })
    },
  async fetchInfluencerDetails() {
    try {
      const response = await axios.get(`/influencers`, {
        params: { id: this.inf_id }
      });
      console.log('Influencer Details:', response.data);
      this.influencer = response.data;
    } catch (error) {
      console.error('Error fetching influencer details:', error);
    }
  },
  async fetchCampaigns() {
    try {
      const response = await axios.get(`/campaigns`, {
        params: { id: this.sp_id }
      });
      this.campaigns = response.data;
      console.log(this.campaigns);
    } catch (error) {
      console.error('Error fetching campaigns:', error);
    }
  },
  async fetchAds() {
    if (this.camp_id) {
      try {
        const response = await axios.get(`/ads`, {
          params: { id: this.camp_id }
        });
        console.log('Ads:', response.data); 
        this.ads = response.data;
      } catch (error) {
        console.error('Error fetching ads:', error);
      }
    }
  },
},

  mounted() {
    this.sp_id = this.$route.params.sp_id;
    this.inf_id = this.$route.params.inf_id;
    console.log(this.inf_id);
    this.fetchInfluencerDetails();
    this.fetchCampaigns();
  },
};
</script>

<style scoped>
/* Add any relevant styles here */
</style>
