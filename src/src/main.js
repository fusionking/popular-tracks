// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
/* eslint-disable */
import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueSimpleAlert from "vue-simple-alert";

Vue.use(VueSimpleAlert);

Vue.config.productionTip = false
axios.defaults.baseURL = 'http://localhost:8000'

new Vue({
  el: '#app',
  render: h => h(App)
})
