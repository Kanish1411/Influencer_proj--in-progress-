<template>
  <div v-if="$store.state.checkl && $store.state.checkspn">
    <Navbar showHomeLink showCampLink showFindinf />
    <div text-align="centre" class="margin-form">
      <h1>Welcome Sponsor {{ idu }}</h1>
      <h2>Active Campaigns</h2>
      <ul v-if="camp.length > 0">
        <h4 v-for="c in camp" :key="c.camp_id">
          <h3>
            Name: {{ c.Camp_name }} Visibility: {{ c.Camp_vis }}
          </h3>
          <h5 v-if="c.ads.length > 0">
              <h5 v-for="a in c.ads" :key="a.Ad_id">
                Ad Name: {{ a.Name }} requirements: {{ a.Req }} Worker: {{ a.Worker }}
                <button class="btn btn-primary" @click="this.$router.push({ name: 'Update_ad', params: { id: a.Ad_id,sp_id:idu } })">Update</button>{{  }}
                <button class="btn btn-danger" @click="this.del_ad(a.Ad_id)">Delete</button>
              </h5>
            <button class="btn btn-primary" @click="this.$router.push({ name: 'Addad', params: { id: c.camp_id,sp_id:idu } })">Add Ad</button>  {{  }}
            <button class="btn btn-primary" @click="this.$router.push({ name: 'Update_camp', params: { id: c.camp_id,sp_id:idu } })">Update Campaign</button>{{  }}
            <button class="btn btn-danger" @click="this.del_camp(c.camp_id)">Delete Campaign</button>
          </h5>
          <h5 v-else>
            <button class="btn btn-primary" @click="this.$router.push({ name: 'Addad', params: { id: c.camp_id,sp_id:idu } })">Add Ad</button>  {{  }}
            <button class="btn btn-primary" @click="this.$router.push({ name: 'Update_camp', params: { id: c.camp_id,sp_id:idu } })">Update Campaign</button>{{  }}
            <button class="btn btn-danger" @click="this.del_camp(c.camp_id)">Delete Campaign</button>
          </h5>
        </h4>
      </ul>
      <h4 v-else>No Active Campaigns available Yet</h4>
      <br>
      <h3>Requests</h3>
      <ul v-if="req.length > 0">
        <h4 v-for="r in req" :key="r.req_id">
          Request ID: {{ r.req_id }}<br>
          Ad: {{ r.ad_name }}<br>
          <button class="btn btn-primary" @click="this.accept(r.req_id)">Accept</button>  {{  }}
        </h4>
      </ul>
      <h4 v-else>No Requests available Yet</h4>
    </div>
  </div>
  <div v-else>
    {{ login() }}
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
  name: "Sponsor",
  components: {
    Navbar,
  },
  data() {
    return {
      camp: [],
      req:[],
      idu: 0,
    };
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
    async Spn() {
      try{
      let token = localStorage.getItem("token");
      const response = await axios.post(
        "/Sponsor",
        {
          id: this.$route.params.id,
        },
        {
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );
      this.camp=response.data.camp;
      this.req=response.data.req;
      console.log(this.camp);
      }
      catch(error){
        console.error("Error fetching DATA:", error);
      }
    },
    async accept(id){
      let token=localStorage.getItem("token");
      const r=await axios.post("/accept_req",{
        id:id,
      },{
        headers:{
          Authorization:"Bearer"+token,
        }
      })
    },
    async del_camp(id){
      try {
            const isConfirmed = window.confirm("are you sure you want to delete this Campaign, (deleteing this leads to removal of all ads in this campaign)");
            if (isConfirmed){
            let token = localStorage.getItem("token");
            const response = await axios.post("/delete_camp", {
              id: id,
            },
            {
            headers: {
              Authorization: "Bearer " + token,
            },
            });
            window.location.reload();
            console.log(response.data.message);
            }
            } catch (error) {
          console.error("Error accepting request:", error);
        }
    },
    async del_ad(id){
      try {
            const isConfirmed = window.confirm("are you sure you want to delete this Ad");
            if (isConfirmed){
            let token = localStorage.getItem("token");
            const response = await axios.post("/delete_ad", {
              id: id,
            },
            {
            headers: {
              Authorization: "Bearer " + token,
            },
            });
            window.location.reload();
            console.log(response.data.message);
            }
            } catch (error) {
          console.error("Error accepting request:", error);
        }
    },
    login() {
      this.$router.push("/");
    },
  },
  async mounted() { 
    if (this.$store.state.checkl && this.$store.state.checkspn) {
      await this.Spn();
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
