# Most Popular Tracks App

An application which runs on Vue JS on frontend and Django on backend,
which consumes the Spotify API to fetch a random artist's top tracks based on
the given genre.

The genres are stored in a JSON file, which is located in the *populartracks/data* folder.

***
### Folder Structure
- populartracks
Contains the Django API. The genres.json file is located under the *./data* folder.
- src
Contains the Vue application. The components are located under *./src/components*.

### How to run
The frontend and the backend components both have isolated Dockerfile's and there is a main docker-compose.yml file which exposes them as containerized services. 
You can start the whole application with this single command, which create the images and boots the conainers:

```
docker-compose up -d --build
# To check if both containers are up and running
docker container ls
```
The frontend component runs at port *8080* and the backend api is at port *8000*.

### Summary
When the main component is mounted to the DOM, it sends a post request to the *set-token* endpoint and the api fetches an access token, which has a 1 hour TTL. Then, this token is saved to the internal django database cache with a 1 hour TTL as well, so subsequent requests which are outdated could ask for new access tokens if the token is expired.
The client credentials flow is used here. You can read more about it from [this link](https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow).

The *tracks/<genre>* endpoint accesses the *genres.json* file and gets a random artist name with the given genre (accessed as a url kwarg).
Then, a GET request is sent to *https://api.spotify.com/v1/search?q=(artistName)&type=artist*
The response contains all matching artists as a list sorted by popularity. The first record is selected since it is the most relevant search result, and the artist URL is fetched.
This is required since this is the only way to get the artist's SPOTIFY ID.
The url looks like this: *https://api.spotify.com/v1/artists/08td7MxkoHQkXnWAYD8d6Q/
Then the *top-tracks* endpoint is called and the response is serialized.

### Third Party Packages
 > Backend 
- Django 2.2 is used as the backend framework.
- Django Rest Framework is used to implement the API Views and serializers.
- requests package is used to handle network requests.
- django-cors-headers package is used to allow cross origin requests, which are coming from the frontend component of the application.
 > Frontend 
- axios is used to handle requests going to the API.
- vue-good-table is used to render the table.
- vue-simple-alert is used to handle warnings and errors.
