<template>
    <div v-if="$store.state.checkl  && $store.state.checkadmin">
    <Navbar showHomeLink  showReqLink />
    <div text-align="centre" class="margin-form">
      <h1>Admin page</h1>
    </div>
</div>
<div v-else>
  {{ this.log=1 }}
</div>

</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
  name: "Admin",
  components: {
    Navbar,
  },
  data() {
    return {
      log: 0,
    };
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
        async login(){
          console.log("login required")
          this.$router.push("/")
        },
        async logg(){
          if (this.log==1){
              this.login()
          }
        }
    },
    mounted(){
      this.logg()
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