import pandas as pd
import re

def clean_data(df):
    """Clean the DataFrame by dropping columns, removing duplicates, and converting genres."""
    try:
        # Drop album genres column
        if 'album_genres' in df.columns:
            df = df.drop('album_genres', axis=1)
        
        # Drop duplicated songs
        df = df.drop_duplicates(['song_name', 'artist_name'], keep='first')
        
        # Convert artist genres to string
        df['artist_genres'] = df['artist_genres'].apply(
            lambda x: re.sub(r"'", '', str(x)[2:-1]) if pd.notnull(x) else ''
        )
        
        return df
    except Exception as e:
        print(f"Error cleaning data: {e}")
        return df