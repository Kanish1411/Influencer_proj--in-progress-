<template>
  <Navbar showRegisterLink showAboutLink />
  <div class="margin-form">
    <h1>Login</h1>
    <form @submit.prevent="login">
        <label for="username">Username:</label>
        <input class="form-control" type="text" v-model="username" required>
        <br>
        <label  for="password">Password:</label>
        <input class="form-control" type="password" v-model="password" required>
        <br>
        <button class="btn btn-primary" type="submit">Login</button>
      </form>
      <div v-if="error" class="message error-message">{{ error }}</div>
      <div v-if="message" class="message success-message">{{ message }}</div>
  </div>
  
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';
export default {
  name : "login",
  components:{
      Navbar,
    },
  data() {
    return {
        username: '',
        password: '',
        error: null,
        message: null,
      };

  },
  methods: {
    async login() {
      try {
        const response = await axios.post('login', {
          username: this.username,
          password: this.password,
        });
        const msg = response.data.message;
        this.$store.commit("setcheckl", true);
        if (msg == 'Sponsor login successful') {
          console.log("Sponser login successful", response.data);
          localStorage.setItem("token", response.data.access_token);
          this.$store.commit("setcheckspn", true);
          this.$router.push({ name: 'Sponsor', params: { id: response.data.id } })
        } else if (msg == 'Admin login successful') {
          console.log("Admin login successful", response.data);
          localStorage.setItem("token", response.data.access_token);
          this.$store.commit("setcheckadmin", true);
          this.$router.push('/admin');
        } else if (msg === 'Influencer login successful') {
          console.log("Influencer login successful", response.data);
          localStorage.setItem("token", response.data.access_token);
          this.$store.commit("setcheckinf", true);
          this.$router.push({ name: 'Influencer', params: { id: response.data.id }} );
        } else {
          this.$store.commit("setcheckl", false);
          this.error=msg;
          this.$router.push('/');
        }
      } catch (error) {
        console.log(error)
        this.error = 'Invalid credentials';
      }
      setTimeout(() => {
        this.message = null;
        this.error = null;
      }, 3000);
      },
  },
  mounted(){
    console.log("Logged out");
    this.$store.state.checkl = false;
    this.$store.state.checkadmin = false;
    this.$store.state.checkspn=false;
    this.$store.state.checkinf=false;
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