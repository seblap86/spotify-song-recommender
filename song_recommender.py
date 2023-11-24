def song_recommender():
    # Importing libraries
    import random
    import re
    import spotipy
    import json
    import pickle
    import pandas as pd
    import numpy as np
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process
    from IPython.display import clear_output
    from spotipy.oauth2 import SpotifyClientCredentials
    from IPython.display import IFrame
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.cluster import KMeans

    # Import Spotify API config
    import config

    # Connecting to spotify server
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= config.client_id,
                                                               client_secret= config.client_secret)) 

    # Defining functions
    def play_song(track_id):
        return IFrame(src="https://open.spotify.com/embed/track/"+track_id,
            width="320",
            height="80",
            frameborder="0",
            allowtransparency="true",
            allow="encrypted-media",
            )

    def load(filename = "filename.pickle"): 
        try: 
            with open(filename, "rb") as f: 
                return pickle.load(f) 

        except FileNotFoundError: 
            print("File not found!")

    # Imports
    hot100_df = pd.read_csv('dfs/hot100_df.csv')
    df = pd.read_csv('model/7-K17/df_model.csv')
    scaler = load(filename="model/7-K17/model_scaler.pickle")
    kmeans_model = load(filename="model/7-K17/model_kmeans.pickle")
    
    # Creating a hot100 lowercase dataframe (saves trouble later on)
    hot100_df_lowercase = hot100_df.copy() 
    for column in hot100_df_lowercase.columns:
        hot100_df_lowercase[column] = hot100_df_lowercase[column].apply(lambda x: x.lower())

    # Get input
    title_input = input('Please enter a song title. Make sure you only enter the title, not the artist.\nYour input: ') # Asks for input

    # Check if in hot 100
    matching_indices = []
    related_index = -1
    for title in hot100_df_lowercase['title']:
        related_index += 1
        fuzz_ratio = fuzz.ratio(title_input.lower(),title)
        if fuzz_ratio>70:
            matching_indices.append(related_index)

    # If in hot 100...
    if len(matching_indices) > 0:
        if len(matching_indices) > 1:
            print(f'We found multiple matches in the range of your search.')

            matching_titles = []
            matching_artists = []
            counter = 0

            for i in matching_indices:
                matching_artists.append(hot100_df.iloc[i,1])
                matching_titles.append(hot100_df.iloc[i,0])
                counter += 1
                print(f'Input "{counter}" if you mean the song "{matching_titles[counter-1]}" by {matching_artists[counter-1]}.')

            valid_input = False
            while not valid_input:
                try:
                    artist_choice = int(input('Your choice: '))-1
                    if artist_choice < 0 or artist_choice > (len(matching_indices)-1):
                        raise ValueError("Invalid input. Please input one of the previously mentioned integers")
                    valid_input = True
                except:
                    print('Invalid input. Please make sure to input one of the previously mentioned integers.')
            matching_index = matching_indices[artist_choice]
            matching_title = matching_titles[artist_choice]
            matching_artist = matching_artists[artist_choice]

        else:
            matching_index = matching_indices[0]
            matching_title = hot100_df.iloc[matching_index,0]
            matching_artist = hot100_df.iloc[matching_index,1]

        random_row = matching_index
        while random_row == matching_index:
            random_row = random.randint(0, len(hot100_df)-1)
            rec_title = hot100_df.iloc[random_row,0]
            rec_artist = hot100_df.iloc[random_row,1]

        clear_output()
        print(f'Your match: "{matching_title}" by {matching_artist}. This song is in the hot charts right now.')

        song_match = f'{matching_title} {matching_artist}'
        results_for_matching_song = sp.search(q=song_match)
        matching_song_id = results_for_matching_song['tracks']['items'][0]['id']
        display(play_song(matching_song_id))
        
        print(f'Recommendation: From the hot charts, you should also check out "{rec_title}" by {rec_artist}.')

    # If not in hot 100
    else:    
        search_result_input = sp.search(q=title_input)
        search_result_id = search_result_input['tracks']['items'][0]['id']
        search_result_features = pd.DataFrame(sp.audio_features(search_result_id))
        y = search_result_features[['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'tempo', 'valence', 'duration_ms', 'loudness', 'mode', 'time_signature']]

        y_scaled = scaler.transform(y)
        y_scaled = pd.DataFrame(y_scaled, columns = y.columns)
        pred_cluster = kmeans_model.predict(y_scaled)

        df_pred_cluster = df[df['cluster'] == pred_cluster[0]]

        if search_result_id in list(df_pred_cluster['id']):
            df_pred_cluster = df_pred_cluster[(df_pred_cluster['id'] != search_result_id)]

        rec_song_row = random.randint(0, len(df_pred_cluster)-1)
        rec_song_id = df_pred_cluster.iloc[rec_song_row,0]
        search_result_rec_song = sp.search(q=title_input)

        match_info = sp.track(search_result_id)
        matching_title = match_info["name"]

        rec_song_info = sp.track(rec_song_id)
        rec_title = rec_song_info["name"]

        match_artists = []
        for i in range(len(match_info['artists'])):
            artist_uri = match_info['artists'][i]['uri']
            artist_name = sp.artist(artist_uri)['name']
            match_artists.append(artist_name)
        matching_artist = ', '.join(match_artists)

        rec_song_artists = []
        for i in range(len(rec_song_info['artists'])):
            artist_uri = rec_song_info['artists'][i]['uri']
            artist_name = sp.artist(artist_uri)['name']
            rec_song_artists.append(artist_name)
        rec_artist = ', '.join(rec_song_artists)

        clear_output()
        print(f'Your match: "{matching_title}" by {matching_artist}.')
        
        display(play_song(search_result_id))
        
        print(f'Recommendation: From our song database, you should also check out "{rec_title}" by {rec_artist}.')

    # In any case: Song player for recommended song
    rec_song = f'{rec_title} {rec_artist}'
    results_for_user = sp.search(q=rec_song)
    rec_song_id = results_for_user['tracks']['items'][0]['id']
    display(play_song(rec_song_id))
