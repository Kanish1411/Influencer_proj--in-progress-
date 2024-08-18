

<template>
    <Navbar showLoginLink showAboutLink/>
    <div text-align="centre" class="margin-form">
      <h1>Register</h1>
      <form @submit.prevent="register">
        <label for="regUsername">Username:</label>
        <input class="form-control" type="text" v-model="regUsername" required>
        <br>
        <label for="regPassword">Password:</label>
        <input class="form-control" type="password" v-model="regPassword" required>
        <br>
        <label for="regEmail">Email:</label>
        <input class="form-control" type="text" v-model="regEmail" required>
        <br>
        <label for="regRole">Role:</label>
        <select class="form-control" v-model="regRole" required>
          <option value="Sponsor">Sponsor</option>
          <option value="Influencer">Influencer</option>
          
        </select>
        <br>
        <label for="addon">Additional details (Platform for Inf, Industry for spn):</label>
        <input class="form-control" type="text" v-model="addon">
        <br>
        <button class="btn btn-primary" type="submit">Register</button>
      </form>
      <div v-if="error" class="message error-message">{{ error }}</div>
      <div v-if="message" class="message success-message">{{ message }}</div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';
export default {
  components:{
      Navbar,
    },
  data() {
    return {
      regUsername: '',
      regPassword: '',
      regEmail: '',
      regRole: '',
      addon:"",
      error: null,
      message: null,
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('register', {
          username: this.regUsername,
          password: this.regPassword,
          email: this.regEmail,
          role: this.regRole,
          addon:this.addon,
        });
        this.message = response.data.message;
        this.regUsername = '';
        this.regPassword = '';
        this.regEmail = '';
        this.regRole = '';
        this.addon="";
        window.scrollTo(0, 0);
        
      } catch (error) {
        this.error = error.response.data.error || 'Registration failed';
      }
      setTimeout(() => {
          this.message = null;
          this.error=null;
        }, 3000);
    },
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