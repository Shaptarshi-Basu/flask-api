# Flask-api

#### Basic Flask API with dockerized mongodb database
#### Use instructions.txt to run the application




#### Endpoint details
*GET /songs*

accepts query parameters 'limit' and 'offset'. These should be int values
default offset is 0 and limit is 5.Returns all songs.

*GET /songs/avg/difficulty*

accepts query parameter 'level'. Its should be int value
default level is 0.Returns the average difficulty for all songs based on level

*GET /songs/search*

accepts query parameter 'message'. Its should be present.
It is case insensitive search.Return a list of songs for the matched criteria.

*POST /songs/rating*

accepts query parameter 'song_id' and 'rating'. They should be present.
adds a rating to the song. Ratings should be between 1 and 5.

*GET /songs/avg/rating/<song_id>*
 
 Returns the average, the lowest and the highest rating of the given song id.
