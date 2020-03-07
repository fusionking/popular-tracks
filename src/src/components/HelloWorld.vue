<template>
    <div class="col-md-12 text-center pb-5">
        <h1 class="heading mb-4">Most Popular Tracks of {{ artistName }}</h1>
        <p>Availabe genres: rock, alternative rock, pop, blues, country,
        electronic, jazz, r&b, rap, reggae</p>
        <input v-model="genreName" placeholder="Type a genre name here:">
        <button @click="searchArtist" class="mb-4">Search For Artist Tracks</button>
        <br>
        <vue-good-table
          :columns="columns"
          :rows="rows"
          >
        </vue-good-table>
    </div>
</template>

<script>
/* eslint-disable */
import 'vue-good-table/dist/vue-good-table.css'
import { VueGoodTable } from 'vue-good-table';
import axios from 'axios';
import VueAxios from 'vue-axios';

export default {
    data: function() {
      return {
        columns: [
            {label: 'Artist Name', field: 'artist', type: 'String'},
            {label: 'Track Name', field: 'track', type: 'String'},
            {label: 'Image Url', field: 'imageUrl', html: true},
            {label: 'Release Date', field: 'releaseDate', type: 'String'}
        ],
        rows: [],
        artistName: null,
        genreName: null,
        error: null
      }
    },
    components: {
        VueGoodTable,
    },
    methods: {
        searchArtist: function() {
            let currentObj = this;
            let newRows = [];
            axios
                .get('tracks/' + this.genreName + '/')
                .then(function (response) {
                    if(response.data.hasOwnProperty("error")) {
                        currentObj.error = response.data.error.message;
                        currentObj.$fire({
                            text: currentObj.error,
                            type: 'error',
                            timer: 2000
                        });
                    }
                    else {
                        const result = response.data.result;
                        currentObj.artistName = result[0].artist;
                        for(var i = 0; i < result.length; i++) {
                            let trackResult = result[i];
                            newRows.push({
                                artist: trackResult.artist,
                                track: trackResult.track,
                                imageUrl: '<img src="' +
                                trackResult.album_image_url + '" alt="placeholder" height="80" width="80">',
                                releaseDate: trackResult.release_date
                            });
                      };
                      currentObj.rows = newRows;}
                })
        }
    }
}
</script>
