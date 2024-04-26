from bs4 import BeautifulSoup
import requests
import spotipy

# ADD OWN KEYS
SPOTIPY_CLIENT_ID = "ABC"
SPOTIPY_CLIENT_SECRET = "ABC"
SPOTIPY_REDIRECT_URI = "https://example.com/"

date = input("Which year do you want to travel to? (YYYY-MM-DD)")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
billboard_songs = response.text
soup = BeautifulSoup(billboard_songs, "html.parser")

songs_in_charts = []
chart_results = soup.select("div li ul li h3")
for song in chart_results:
    chart_songs = song.getText().strip()
    songs_in_charts.append(chart_songs)

scope = "playlist-modify-private"
sp_oauth = spotipy.oauth2.SpotifyOAuth(
    SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope, cache_path="token.txt", show_dialog=True
)
token = sp_oauth.get_access_token(as_dict=False)

sp = spotipy.Spotify(auth=token)
user_id = sp.current_user()["id"]

year = date.split("-")[0]
song_uris = []

for song in songs_in_charts:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

new_playlist = sp.user_playlist_create(user=user_id, name=f"Top Songs in {date}!", public=False, description="enjoyyyy :)")
sp.playlist_add_items(playlist_id=new_playlist["id"], items=song_uris)
