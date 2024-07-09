import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css';
import './axios';
import router from './router';
import store from './store';


const app= createApp(App)
app.use(router)
app.use(store)
app.mount('#app')
