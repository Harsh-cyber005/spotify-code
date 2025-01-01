from spotify import get_playlist
from url import get_url
from yt import download
import json
import random
import time
import os
import requests

output_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'getspotify')

if __name__ == "__main__":
    URL = input("Enter the Spotify playlist Link: ")
    playlist_name = get_playlist(URL)

    data = []

    with open ("./tmp/playlist.json", "r") as f:
        data = json.load(f)

    for song in data:
        thumbnail_url = song["thumbnail"]
        if thumbnail_url != "":
            thumbnail = requests.get(thumbnail_url)
            with open("./tmp/thumbnail.jpg", "wb") as f:
                f.write(thumbnail.content)
        song_path = os.path.join(output_dir, playlist_name, f"{song['name']}.mp3")
        if os.path.exists(song_path):
            print(f"{song['name']} by {song['contributing_artists']} is already downloaded. Skipping...")
            time.sleep(0.2)
            continue
        print("--------------------------------------------------")
        print(f"Downloading {song['name']} by {song['contributing_artists']}...")
        url = get_url(song["search_query"])
        if url == None:
            print(f"Failed to fetch video URL for {song['name']} by {song['contributing_artists']}")
            continue
        download(url, playlist_name, song["name"], song["contributing_artists"], song["album"])
        with open("./tmp/thumbnail.jpg", "wb") as f:
            f.write(b'')
        os.remove("./tmp/thumbnail.jpg")
        gap = random.randint(5, 10)
        print(f"Waiting for {gap} seconds...")
        time.sleep(gap)
        print("--------------------------------------------------\n")
    
    print("Downloaded all songs!")