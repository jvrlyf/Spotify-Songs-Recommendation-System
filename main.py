from src.data_collection import (
    setup_spotify_client, collect_songs, collect_audio_features,
    collect_playlist_songs, save_data
)
from src.data_cleaning import clean_data
from src.data_analysis import analyze_data
from src.dimensionality_reduction import apply_dimensionality_reduction
from src.clustering import apply_clustering

def main():
    # Initialize Spotify client
    sp = setup_spotify_client()
    if not sp:
        return

    # Collect data
    years = ['2017', '2018', '2019', '2020', '2021', '2022']
    df_songs = collect_songs(sp, years)
    df_audios = collect_audio_features(sp, df_songs['id'])
    df_songs = df_songs.merge(df_audios, on='id')
    save_data(df_songs, 'spotify_songs_2017_2022.csv')

    df_playlist_songs = collect_playlist_songs(sp, PLAYLIST_LINK)
    df_playlist_audios = collect_audio_features(sp, df_playlist_songs['id'])
    df_playlist = df_playlist_songs.merge(df_playlist_audios, on='id')
    save_data(df_playlist, 'fav_playlist_songs.csv')

    # Clean data
    df_songs = clean_data(df_songs)
    df_playlist = clean_data(df_playlist)

    # Analyze data
    analyze_data(df_songs, "Songs")
    analyze_data(df_playlist, "Playlist")

    # Dimensionality reduction
    df_pca = apply_dimensionality_reduction(df_songs)

    # Clustering
    if df_pca is not None:
        df_pca, km_pred = apply_clustering(df_pca)
        df_songs["cluster"] = km_pred

if __name__ == "__main__":
    main()