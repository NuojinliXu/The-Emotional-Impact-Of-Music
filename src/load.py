import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import time


def get_kaggle_data(url, file):
    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        url,
        file,
        )
    return df.dropna()



load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_youtube_stats(song_title, max_results=1, top_comments=10):
    try:
        search_response = youtube.search().list(
            part="snippet",
            q=song_title,
            type="video",
            maxResults=max_results
        ).execute()

        if not search_response["items"]:
            return None
        video_id = search_response["items"][0]["id"]["videoId"]
        video_title = search_response["items"][0]["snippet"]["title"]

        stats_response = youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()
        stats = stats_response["items"][0]["statistics"]
        comment_response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=top_comments,
            order="relevance",
            textFormat="plainText"
        ).execute()

        comments = []
        for item in comment_response.get("items", []):
            comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment_text.strip())
        return {
            "track_name": song_title,
            "video_id": video_id,
            "video_title": video_title,
            "viewCount": int(stats.get("viewCount", 0)),
            "likeCount": int(stats.get("likeCount", 0)),
            "commentCount": int(stats.get("commentCount", 0)),
            "comments": comments
        }
    except Exception as e:
        return None

def fetch_youtube_data(music_df, limit=5, sleep_time=1.0):
    results = []
    songs = music_df["track_name"].dropna().unique()[:limit]
    for i, song in enumerate(songs, 1):
        data = get_youtube_stats(song)
        if data:
            results.append(data)
        time.sleep(sleep_time) 
    youtube_df = pd.DataFrame(results)
    return youtube_df