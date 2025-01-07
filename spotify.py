import requests
import json
import base64
import time
import os

res = requests.post("https://maxbrain.vercel.app/obscured/please/stop/right/here",json={"pypy":"true"})
CLIENT_ID = res.json()["id"]
CLIENT_SECRET = res.json()["secret"]

def get_token():
    global token, token_expiry
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch token: {response.content}")
    
    json_result = response.json()
    token = json_result["access_token"]
    expires_in = json_result["expires_in"]
    token_expiry = time.time() + (expires_in - 300)
    with open("./tmp/token.json", "w") as f:
        json.dump({"token": token, "expires_in": token_expiry}, f)
    return token

def get_auth_token():
    if "tmp" not in os.listdir("."):
        os.mkdir("./tmp")
    if "token.json" not in os.listdir("./tmp"):
        with open("./tmp/token.json", "w") as f:
            json.dump({"token": "", "expires_in": 0}, f)

    with open("./tmp/token.json", "r") as f:
        token_raw = json.load(f)

    token = token_raw["token"]
    expires_in = token_raw["expires_in"]

    if(token == "" or time.time() >= expires_in):
        res = get_token()
        token = res
    return {"Authorization": "Bearer " + token}

def get_playlist_name(playlist_id):
    try:
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        auth_token = get_auth_token()
        response = requests.get(url, headers=auth_token)
        if response.status_code != 200:
            print(f"Failed to fetch playlist: {response.content}")
            return None
        return response.json()["name"]
    except Exception as e:
        print(e)
        return None

def get_playlist_tracks(playlist_id):
    try:
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        auth_token = get_auth_token()
        response = requests.get(url, headers=auth_token)
        if response.status_code != 200:
            print(f"Failed to fetch playlist: {response.content}")
            return None
        return response.json()
    except Exception as e:
        print(e)
        return None

def get_playlist(URL):
    playlist_id = URL.split("/")[-1].split("?")[0]
    data = get_playlist_tracks(playlist_id)
    time.sleep(1)
    playlist_name = get_playlist_name(playlist_id)
    songs = []
    if data == None:
        print("Failed to fetch playlist")
        return None
    for track in data["items"]:
        if(track["track"] == None):
            continue
        thumnail_url = ""
        if(track["track"]["album"]["images"] != None):
            thumnail_url = track["track"]["album"]["images"][0]["url"]
        artist_names = []
        if(track["track"]["artists"] != None):
            artist_names = [artist["name"] for artist in track["track"]["artists"]]
        search_query = track["track"]["name"] + "+" + "+".join(artist_names)+"+lyrical+video"
        name = track["track"]["name"]
        if name == None or name == "":
            continue
        for ch in name:
            if ch >= 'A' and ch <= 'Z':
                continue
            if ch >= 'a' and ch <= 'z':
                continue
            if ch >= '0' and ch <= '9':
                continue
            if ch == '(' or ch == ')':
                continue
            if ch == '[' or ch == ']':
                continue
            if ch == '{' or ch == '}':
                continue
            if ch == '-':
                continue
            if ch == '_':
                continue
            if ch == "'":
                name = name.replace(ch, '')
                continue
            if ch == '"':
                name = name.replace(ch, '')
                continue
            else:
                name = name.replace(ch, ' ')
        contributing_artists = ""
        if len(artist_names) > 1:
            contributing_artists = ", ".join(artist_names[:-1]) + " and " + artist_names[-1]
        else:
            contributing_artists = artist_names[0]
        for ch in contributing_artists:
            if ch >= 'A' and ch <= 'Z':
                continue
            if ch >= 'a' and ch <= 'z':
                continue
            if ch >= '0' and ch <= '9':
                continue
            if ch == ' ': 
                continue
            if ch == ',':
                continue
            else:
                contributing_artists = contributing_artists.replace(ch, ' ')
        for ch in search_query:
            if ch >= 'A' and ch <= 'Z':
                continue
            if ch >= 'a' and ch <= 'z':
                continue
            if ch >= '0' and ch <= '9':
                continue
            else:
                search_query = search_query.replace(ch, '+')
        song = {
            "name": name,
            "artists": [artist["name"] for artist in track["track"]["artists"]],
            "search_query": search_query,
            "contributing_artists": contributing_artists,
            "album": track["track"]["album"]["name"],
            "thumbnail": thumnail_url
        }
        songs.append(song)
    with open("./tmp/playlist.json", "w") as f:
        json.dump(songs, f)
    return playlist_name
