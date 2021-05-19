# import necessary packages
import sys
import time
import spotipy
import spotipy.util as util
import requests
from config.config import USERNAME, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from bs4 import BeautifulSoup

# set the scope for the script
scope = 'user-read-currently-playing'

token = util.prompt_for_user_token(USERNAME, scope, client_id=SPOTIPY_CLIENT_ID,
    client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

def sing():
    # check if the token is working
    if token:
        sp = spotipy.Spotify(auth=token)

        # Get the currently-playing song
        current_song = sp.currently_playing()
        # Get the artist from the JSON response
        artist = current_song['item']['artists'][0]['name']
        # Get the song name from the JSON reponse
        song_name = current_song['item']['name']

        # Create a valid URL to use for web scraping
        # including the song name and artist
        song_url = '{}-{}-lyrics'.format(str(artist).strip().replace(' ','-'), str(song_name).strip().replace(' ','-'))

        print('\nSong: {}\nArtist: {}'.format(song_name, artist))

        print("Currently Playing:  " + song_name + " by " + artist)

    else:
        print("Can't get token for ", USERNAME)

    return (song_url, (current_song['item']['duration_ms'] - current_song['progress_ms']) / 1000)


# Make sure the song name is in the correct format
def notation(raw_song_name):

    song_notations = []
    raw_song_name.replace('&' , 'and')
    raw_song_name.replace("'" , "")
    song_notations.append(raw_song_name)
    dashindexs = raw_song_name.find('---')
    song_notations.append(raw_song_name[:dashindexs + 1])

    return song_notations

def lyricsrequest(raw_names):

    search_places = ['genius.com']

    for raw_name in raw_names:
        for server in search_places:
            # New request using song_url created before
            print(f"\nServer request: https://{server}/{raw_name}")
            request = requests.get(f"https://{server}/{raw_name}")

            # Verify status_code of request
            if request.status_code == 200:

                # BeautifulSoup library return an html code
                html_code = BeautifulSoup(request.text, features="html.parser")

                # fail safe
                if html_code.find("div", {"class": "lyrics"}) is None:
                    print('---making a new request because was redirected---')
                    time.sleep(2)
                    lyricsrequest([raw_name])
                    return False

                # Extract lyrics from beautifulsoup response using the correct prefix {"class": "lyrics"}
                lyrics = html_code.find("div", {"class": "lyrics"}).get_text()

                print(lyrics)
                print(f'Lyrics found on {server} with a search on {raw_name}')

                return True

            else:
                print("Unfortunately, the lyrics can't be found.")
    return False

if __name__ == "__main__":
    while True:
        raw_song_name , wait = sing()
        song_notations = notation(raw_song_name)
        lyricsrequest(song_notations)
        time.sleep(wait)
