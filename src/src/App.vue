<template>
  <div id="app" class="text-center">
      <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
      <app-tracks></app-tracks>
  </div>
</template>

<script>
/* eslint-disable */
import Tracks from './components/Tracks.vue';
import axios from 'axios';
import _ from 'lodash';

export default {
  name: 'app',
  data () {
    return {
        artistName: null,
    }
  },
  components: {
      appTracks: Tracks,
  },
  methods: {

  },
  mounted () {
    axios.post('/set-token/')
        .then(res => {
        })
        .catch(error => console.log(res.error));
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
