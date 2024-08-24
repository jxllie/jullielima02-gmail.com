What was the theme you chose? 
- I chose to create an app that showcases two different Brazilian artists. Tim Maia was one of the first Brazilian artist to introduce soul music to the country. Gilsons the band, countinues Tim Maia's legacy while creating their own social space in Brazil's music industry. Both artists have personal meaning in my life and I wanted to highlight their songs in my project. 

What were 3 issues you encountered in your project? How did you fix them?
- The first issue I encountered was when I accessed my Genius API, I would reload my app and there would be no results for the artists. Which I knew was incorrect! I had to specify and tweak my code a bit more in order for it to work correctly.
- The second issue I encountered was that my images were not updating based on the html or css I provided. I had to learn what "inline coding" was and instead of having a seperate place to adjust my code, I had to do it within the "img source" line of code.
- The final issue I encountered was that prevously, while testing my remote connection to github, I created a "test" file that was messing with my code. I had to learn how to merge the files in order to properly get them on github!

Are there any known issues with your project? 
- I believe I resolved all issues before deploying my app.

What would you do to improve your project in the future?
- I would like to add audio or videos to enhance the experience of my app!


# App.py code is below </br>
</br>

import flask
import os
import requests
import random

app = flask.Flask(__name__)

Genius API Token
GENIUS_API_TOKEN = '[token here]'

Function to fetch song data using the Genius API
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
