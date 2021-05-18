# import necessary packages
import spotipy
import spotipy.util as util
from config.config import USERNAME, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

# set the scope for the script
scope = 'user-read-currently-playing'

token = util.prompt_for_user_token(USERNAME, scope, client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

# check if the token is working
if token:
    sp = spotipy.Spotify(auth=token)

    # Get the currently-playing song
    current_song = sp.currently_playing()
    artist = current_song['item']['artists'][0]['name']
    name_song = current_song['item']['name']

    print("Currently Playing:  " + name_song + " by " + artist)

else:
    print("Can't get token for", USERNAME)
