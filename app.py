import flask
import os
import requests
import random

app = flask.Flask(__name__)

# Genius API Token
GENIUS_API_TOKEN = 'QuLMSm9jBlqHAbcDFKdbL3JOel6iEbbVAA2On8KVoKrori_szlma7wNhyAo-Wjlj'

# Function to fetch song data using the Genius API
def fetch_song_data(artist_name):
    base_url = "https://api.genius.com/search"
    headers = {'Authorization': f'Bearer {GENIUS_API_TOKEN}'}
    params = {'q': artist_name}
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code == 200:
        hits = response.json().get('response', {}).get('hits', [])
        valid_hits = [hit for hit in hits if hit['result']['primary_artist']['name'].lower() == artist_name.lower()]
        if valid_hits:
            return random.choice(valid_hits)  # Return a random valid hit
    
    return None  # Return None if no valid results or an error occurred

@app.route('/')
def index():
    # Fetch song data for Gilsons and Tim Maia
    gilsons_song = fetch_song_data("Gilsons")
    tim_song = fetch_song_data("Tim Maia")
    
    # Prepare the data for the template
    song_title_gilsons = gilsons_song['result']['title'] if gilsons_song else "No results found for Gilsons"
    artist_name_gilsons = gilsons_song['result']['primary_artist']['name'] if gilsons_song else "Gilsons"
    song_url_gilsons = gilsons_song['result']['url'] if gilsons_song else "#"
    cover_image_gilsons = gilsons_song['result']['song_art_image_url'] if gilsons_song else ""

    song_title_tim = tim_song['result']['title'] if tim_song else "No results found for Tim Maia"
    artist_name_tim = tim_song['result']['primary_artist']['name'] if tim_song else "Tim Maia"
    song_url_tim = tim_song['result']['url'] if tim_song else "#"
    cover_image_tim = tim_song['result']['song_art_image_url'] if tim_song else ""

    # Render the HTML template with the song information
    return flask.render_template("index.html", 
                                 song_title_gilsons=song_title_gilsons, 
                                 artist_name_gilsons=artist_name_gilsons,
                                 song_url_gilsons=song_url_gilsons,
                                 cover_image_gilsons=cover_image_gilsons,
                                 song_title_tim=song_title_tim, 
                                 artist_name_tim=artist_name_tim,
                                 song_url_tim=song_url_tim,
                                 cover_image_tim=cover_image_tim)

if __name__ == '__main__':
    app.run(
        port=int(os.getenv('PORT', 8080)),
        host=os.getenv('IP', '0.0.0.0'),
        debug=True
    )
