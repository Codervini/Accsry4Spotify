import spotipy
import os
from spotipy.oauth2 import SpotifyPKCE
import json

client_id = os.environ.get("SPOTIPY_CLIENT_ID")
redirect_uri = "http://localhost:6942"
scop = ["playlist-read-collaborative", "playlist-read-private", "user-read-currently-playing"]
spotipy_auth_credidentials = SpotifyPKCE(client_id= client_id, redirect_uri= redirect_uri, scope=scop)

sp = spotipy.Spotify(oauth_manager=spotipy_auth_credidentials, language="en")

def jsoner(data, filename):
    with open(f'{filename}.json', "w") as f:
        json.dump(data, f, indent=8)




def currently_playing_downloader():
    data = sp.currently_playing()

    # del data["item"]["album"]["available_markets"]
    # del data["item"]["available_markets"]
    # with open("tmpDevDatarefined.json","w") as f:
    #     json.dump(data, f, indent=8)

    artist = data["item"]['artists'][0]["name"]
    track = data["item"]["name"]
    duration_sec = (data["item"]["duration_ms"]) / 1000
    #print([artist, track, duration_sec])
    return [artist, track, duration_sec]

def playlist_downloader():
    data_playlists = sp.current_user_playlists()

    jsoner(data_playlists, "tmpDevData")
    count = 0
    for i in range(len(data_playlists["items"])):
        playlistName = data_playlists["items"][i]["name"]
        playlistOwner = data_playlists["items"][i]["owner"]["display_name"]
        print(f'{i+1}. {playlistName}  ===BY===  {playlistOwner}')
        count += 1
    print(f'Total: {data_playlists["total"]} ------- {data_playlists["limit"]},,,,{count}')


    uri = data_playlists["items"][0]["uri"]
    total_tracks = data_playlists["items"][0]["tracks"]["total"]

    data_playlists_items = sp.playlist_items(uri, limit=total_tracks)

    jsoner(data_playlists_items, "tmpDevData1")


playlist_downloader()


a = currently_playing_downloader()
if a[0] !="":
    print()
    print("Currently playing " + a[0] + " - " + a[1])