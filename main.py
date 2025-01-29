import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:1234",
        client_id= "c7fa9d72a40747d9a0557451f43e80a0",
        client_secret="ccf184967bbd4f4eb0e640f74eb318fb",
        show_dialog=True,
        cache_path="token.txt",
        username="Thathieswarreddy", 
    )
)
user_id = sp.current_user()["id"]
print(f"user ID: {user_id} ")



date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
URL = "https://www.billboard.com/charts/hot-100/"+date
response = requests.get(url=URL,headers= header)
web_page = response.text
soup = BeautifulSoup(web_page,"html.parser")
song_names_title = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_title]

#for song in song_names:
#    print(song)

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    #print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#for i in range(len(song_uris)):
#    print(f"{song_names[i]} : {song_uris[i]}")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
#print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
