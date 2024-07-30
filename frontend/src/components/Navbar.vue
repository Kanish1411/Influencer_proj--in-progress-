<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="#"></a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active"  v-if="showHomeLink">
        <router-link to="/" class="nav-link">Home</router-link>
      </li>
      <li class="nav-item active"  v-if="showinfHomeLink">
        <router-link to="`/Influencer/${id}`" class="nav-link">Dashboard</router-link>
      </li>
      <li class="nav-item active"  v-if="showadHomeLink">
        <router-link to="/admin" class="nav-link">Dashboard</router-link>
      </li>
      <li class="nav-item active"  v-if="showspHomeLink">
        <router-link :to="{ name: 'Sponsor', params: { id: this.id } }"  class="nav-link">Dashboard</router-link>
      </li>
      <li class="nav-item active"  v-if="showLoginLink">
        <router-link to="/" class="nav-link">Login</router-link>
      </li>
      <li class="nav-item active"  v-if="showRegisterLink">
        <router-link to="/register" class="nav-link">Register</router-link>
      </li>
      <li class="nav-item active"  v-if="showAboutLink">
        <router-link to="/about" class="nav-link">About</router-link>
      </li>
      <li class="nav-item active"  v-if="showAddcatLink">
        <router-link to="/addcat" class="nav-link">Add Campaign</router-link>
      </li>
      <li class="nav-item active"  v-if="showReqLink">
        <router-link to="/request" class="nav-link">Requests</router-link>
      </li>
      <li class="nav-item active"  v-if="showCampLink">
        <router-link :to="`/add_camp/${id}`"  class="nav-link">Add Campaign</router-link>
      </li>
      <li class="nav-item active"  v-if="showUserhome">
        <router-link :to="`/user/${id}`" class="nav-link">Dashboard</router-link>
      </li>
      <li class="nav-item active"  v-if="showReqtab">
        <router-link :to="`/req/${id}`" class="nav-link">Request</router-link>
      </li>
      <li class="nav-item active"  v-if="showDashman">
        <router-link :to="`/manager/${id}`" class="nav-link">Dashboard</router-link>
      </li>
      <li class="nav-item active"  v-if="showFindinf">
        <router-link :to="`/find_inf/${id}`" class="nav-link">Find Influencers</router-link>
      </li>
      <li class="nav-item active"  v-if="showFindspn">
        <router-link :to="`/find_spn/${id}`" class="nav-link">Find Sponsors</router-link>
      </li>
    </ul>
  </div>
</nav>
</template>

<script>
export default {
  
  props: {
    showHomeLink: {
      type: Boolean,
      default: false,
    },
    showLoginLink: {
      type: Boolean,
      default: false,
    },
    showAboutLink: {
      type: Boolean,
      default: false,
    },
    showRegisterLink: {
      type: Boolean,
      default: false,
    },
    showAddcatLink: {
      type: Boolean,
      default: false,
    },
    showReqLink: {
      type: Boolean,
      default: false,
    },
    showinfHomeLink: {
      type: Boolean,
      default: false,
    },
    showspHomeLink: {
      type: Boolean,
      default: false,
    },
    showadHomeLink: {
      type: Boolean,
      default: false,
    },
    showCampLink: {
      type: Boolean,
      default: false,
    },
    showUserhome: {
      type: Boolean,
      default: false,
    },
    showReqtab: {
      type: Boolean,
      default: false,
    },
    showDashman: {
      type: Boolean,
      default: false,
    },
    showFindinf: {
      type: Boolean,
      default: false,
    },
    showFindspn: {
      type: Boolean,
      default: false,
    },
    id:{
      type:Number,
      default:0,
    }
    
  },
  data() {
  return {
    id: null,
  };
},
created() {
  this.id = this.$route.params.id;
},
  
};
</script>


<style>

</style>