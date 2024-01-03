![Cover photo](cover_photo.jpg)

## SPOTIFY SONG RECOMMENDER

#### Project by Sebastian Bobeth
Ironhack bootcamp, November 2023

## PROJECT AIM
To develop a song recommender by using web scraping / the Spotify API service and modeling with KMeans (unsupervised Machine Learning algorithm).

## TECH USED
The complete procedure was done in Python (Jupyter Notebook). The main focus was on the following steps and modules:
- Data cleaning, feature selection (Pandas)
- Web scraping (Beautiful Soup)
- API (Spotipy)
- Machine learning (Scikit-Learn: KMeans)

## FINAL PRODUCT
The developed song recommender has the following logic:
![Song recommender logic](song_recommender_logic.jpg)

#### Model
After training and testing a variety of models (see 'model' folder), the model that made the best recommendations was 'A2.1-ST45'. The model was based on the following 10 Spotify song features: 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'tempo', 'valence', 'duration_ms', 'loudness'. It was trained on the standardized values of these features and assigned the songs in the database to 45 clusters.

#### Song database
The "hot 100" charts are the Billboard top 100 charts as of November 20, 2023. The API-scraped song database (via Spotify API, Spotipy) consists of 8,460 songs (song IDs) from 73 playlists of various times (e.g., best of various decades), genres, current songs (as of late 2023), and some handpicked artists and playlists.

## HOW TO MAKE USE OF THIS REPO
#### General approach
To use or further develop the song recommender, please fork the repo. 
- To use and test the song recommender, please run the 'song_recommender.ipynb' file (this file is basically a clean file that calls up the program).
- To run the song recommeder with a different model, change the model in the 'song_recommender.py' file.
- To modify models or train new models, you can build on the 'model_development_and_evaluation.ipynb' file in the 'model' folder.
- To change, expand or build a new song database, you can build on the dataframes and .ipynb (Jupyter Notebook) files in the 'dfs' folder.

#### Spotify API
For every usage purpose that engages with Spotify, you will need to configure the Spotify API and place a config.py file with your 'client id' and a 'client secret' in the top level folder. The file has to include no more than the following information to succesfully run the program:
  
client_id = '(pass your client id)'<br>
client_secret = '(pass your client secret)'
  
## ACKNOWLEDGMENT
Cover photo by <a href="https://unsplash.com/@davfts?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">David Pupăză</a> on <a href="https://unsplash.com/photos/a-bunch-of-different-colored-pictures-on-a-wall-Km5J-KCP1Mw?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>.
