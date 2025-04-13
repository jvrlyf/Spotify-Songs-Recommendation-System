import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from config.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, PLAYLIST_LINK

def setup_spotify_client():
    """Set up Spotify API client."""
    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
        )
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except Exception as e:
        print(f"Error setting up Spotify client: {e}")
        return None

def collect_songs(sp, years):
    """Collect songs from Spotify for specified years."""
    songs_list = []
    for year in years:
        for i in range(0, 1000, 50):
            try:
                track_results = sp.search(q=f'year:{year}', type='track', limit=50, offset=i)
                for t in track_results['tracks']['items']:
                    artist = sp.artist(t["artists"][0]["external_urls"]["spotify"])
                    album = sp.album(t["album"]["external_urls"]["spotify"])
                    songs_data = {
                        'id': t['id'],
                        'song_name': t['name'],
                        'artist_name': t['artists'][0]['name'],
                        'artist_genres': artist["genres"],
                        'album_genres': album["genres"],
                        'release_date': t['album']['release_date'],
                        'song_link': t['external_urls']['spotify'],
                        'image': t['album']['images'][0]['url'] if t['album']['images'] else None,
                        'song_duration': t['duration_ms'],
                        'song_popularity': t['popularity']
                    }
                    songs_list.append(songs_data)
            except Exception as e:
                print(f"Error collecting songs for year {year}: {e}")
    return pd.DataFrame(songs_list)

def collect_audio_features(sp, song_ids):
    """Collect audio features for given song IDs."""
    audio_features = []
    for ids in song_ids:
        try:
            results = sp.audio_features(ids)
            if results and results[0]:
                audio_data = {
                    'id': ids,
                    'danceability': results[0]['danceability'],
                    'energy': results[0]['energy'],
                    'key': results[0]["key"],
                    'loudness': results[0]["loudness"],
                    'mode': results[0]['mode'],
                    'speechiness': results[0]['speechiness'],
                    'acousticness': results[0]['acousticness'],
                    'instrumentalness': results[0]['instrumentalness'],
                    'liveness': results[0]['liveness'],
                    'valence': results[0]['valence'],
                    'tempo': results[0]['tempo'],
                    'time_signature': results[0]['time_signature']
                }
                audio_features.append(audio_data)
        except Exception as e:
            print(f"Error collecting audio features for ID {ids}: {e}")
    return pd.DataFrame(audio_features)

def collect_playlist_songs(sp, playlist_link):
    """Collect songs from a Spotify playlist."""
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    playlist_songs = []
    try:
        for t in sp.playlist_tracks(playlist_URI)["items"]:
            artist = sp.artist(t['track']["artists"][0]["external_urls"]["spotify"])
            album = sp.album(t['track']["album"]["external_urls"]["spotify"])
            songs_data = {
                'id': t['track']['id'],
                'song_name': t['track']['name'],
                'artist_name': t['track']['artists'][0]['name'],
                'artist_genres': artist["genres"],
                'album_genres': album["genres"],
                'release_date': t['track']['album']['release_date'],
                'song_link': t['track']['external_urls']['spotify'],
                'image': t['track']['album']['images'][0]['url'] if t['track']['album']['images'] else None,
                'song_duration': t['track']['duration_ms'],
                'song_popularity': t['track']['popularity']
            }
            playlist_songs.append(songs_data)
    except Exception as e:
        print(f"Error collecting playlist songs: {e}")
    return pd.DataFrame(playlist_songs)

def save_data(df, filename):
    """Save DataFrame to CSV."""
    try:
        df.to_csv(f'data/{filename}', index=False)
        print(f"Saved data to {filename}")
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")