<template>
  <div v-if="$store.state.checkl && $store.state.checkspn">
    <Navbar showHomeLink showCartLink />
    <div text-align="centre" class="margin-form">
      <h1>Welcome Sponsor {{ idu }}</h1>
      <h3>Active Campaigns</h3>
      <ul v-if="camp.length > 0">
        <li v-for="c in camp" :key="c.camp_id">
          <h3>
            Name: {{ c.Camp_name }} Visibility: {{ c.Camp_vis }}
          </h3>
          <h3 v-if="c.ads.length > 0">
            <ul>
              <li v-for="a in c.ads" :key="a.Ad_id">
                Ad Name: {{ a.Name }} Details: {{ a.Details }} Worker: {{ a.Worker }}
              </li>
            </ul>
          </h3>
          <h3 v-else>
            No ads
          </h3>
        </li>
      </ul>
      <h4 v-else>No Active Campaigns available Yet</h4>
      <br>
      <h3>Requests</h3>
      <ul v-if="req.length > 0">
        <li v-for="r in req" :key="r.req_id">
          Request ID: {{ r.req_id }}
        </li>
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
