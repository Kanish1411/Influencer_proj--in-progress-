<template>
    <router-view/>
</template>

<script>
import Navbar from './components/Navbar.vue';
export default {
  name: 'App',
  components: {
    Navbar
  }
}
</script>

<style>
 body, html, #app {
  margin: 0;
  padding: 0;
  width: 100%;
} 

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
</style>
