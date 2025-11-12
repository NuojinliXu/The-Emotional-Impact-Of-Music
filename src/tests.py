# include your tests here 
# for example for your Progress report you should be able to load data from at least one API source.
from load import get_kaggle_data, get_youtube_stats, fetch_youtube_data
import pandas as pd

music_df1 = get_kaggle_data("solomonameh/spotify-music-dataset", 'high_popularity_spotify_data.csv')
music_df2 = get_kaggle_data("solomonameh/spotify-music-dataset", 'low_popularity_spotify_data.csv')
music_df = pd.concat([music_df1, music_df2], ignore_index=True)
print(music_df.head())
health_df = get_kaggle_data("catherinerasgaitis/mxmh-survey-results", 'mxmh_survey_results.csv')

songs = music_df['track_name']
print(songs)

youtube_df = fetch_youtube_data(music_df, limit=5)
print(youtube_df.head())