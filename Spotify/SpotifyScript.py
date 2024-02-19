import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Set up Spotify API credentials
client_id = '#'
client_secret = '#'
redirect_uri = '#'

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

df = pd.read_csv('Spotify2023.csv', encoding='ISO-8859-1')

print(df.columns)

column_with_track_names = 'track_name'

column_with_artist_names = 'artist(s)_name'

# Get image URL with fallback to default image
def get_image_url(track_name, artist_name):
    try:
        # Try fetching the album cover image
        results = sp.search(q=f"track:{track_name}", type='track', limit=1)
        track_info = results['tracks']['items'][0]
        image_url = track_info['album']['images'][0]['url']
        return image_url
    except:
        try:
            # If album cover image fails, try fetching the artist image
            results = sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
            artist_info = results['artists']['items'][0]
            image_url = artist_info['images'][0]['url']
            return image_url
        except:
            # If both attempts fail, return a default image URL
            return 'https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Green.png'

# Apply function to create a new column
df['image_url'] = df.apply(lambda row: get_image_url(row[column_with_track_names], row[column_with_artist_names]), axis=1)

# Save the updated DataFrame to a new CSV file with encoding
df.to_csv('Spotify2023URLs.csv', index=False, encoding='ISO-8859-1')