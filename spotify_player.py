import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Configura tus credenciales de Spotify
# Reemplaza con tus propios datos
client_id = "[b79242c34df640939089953fd01e8004]"
client_secret = "[1fd2b0b8e6864cf389cf946d439914c3]"
redirect_uri = "http://192.168.1.51:8888/callback"
scope = "user-read-playback-state,user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    open_browser=False  # ¡Esta es la nueva línea!
))

print("Conexión exitosa a Spotify.")
print("Buscando y reproduciendo una canción...")

# Busca una canción y la reproduce
results = sp.search(q="Never Gonna Give You Up Rick Astley", limit=1)
if results['tracks']['items']:
    track_uri = results['tracks']['items'][0]['uri']
    sp.start_playback(uris=[track_uri])
    print("Reproduciendo 'Never Gonna Give You Up'...")
else:
    print("No se encontró la canción.")
