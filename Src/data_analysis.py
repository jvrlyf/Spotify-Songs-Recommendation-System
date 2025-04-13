import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from termcolor import cprint
import plotly.express as px
from matplotlib import colors

def analyze_data(df, dataset_name="Songs"):
    """Analyze the DataFrame and generate visualizations."""
    try:
        # Shape of the data
        cprint(f"Shape of {dataset_name}: {df.shape}", 'green')
        cprint('*' * 42, 'green')

        # Check column dtypes
        print(f"\nColumn dtypes for {dataset_name}:")
        df.info()
        print()

        # Check for null values
        cprint(f"Null values in {dataset_name}:", 'green')
        print(df.isnull().sum())
        print()

        # Describe numerical values
        cprint(f"Numerical description for {dataset_name}:", 'green')
        print(df.describe())
        print()

        # Correlation heatmap
        cmap = colors.ListedColormap(["#131212", "#212121", "#535353", "#b3b3b3", "#1db954"])
        corr = df.corr(numeric_only=True)
        plt.figure(figsize=(16, 16))
        sns.heatmap(corr, annot=True, cmap=cmap, vmax=1, vmin=-1)
        plt.title(f"Correlation Heatmap - {dataset_name}")
        plt.show()

        # Number of songs per year
        cprint(f'Number of songs per year in {dataset_name}:', 'green')
        year_counts = df['release_date'].apply(lambda x: str(x).split('-')[0]).value_counts()
        print(year_counts)
        cprint('*' * 50, 'green')
        plt.figure(figsize=(16, 8))
        sns.countplot(
            x=df['release_date'].apply(lambda x: str(x).split('-')[0]),
            palette=["#1db954"]
        )
        plt.title(f'Number of Songs per Year - {dataset_name}', fontsize=16)
        plt.show()

        # Song duration distribution
        cprint(f'Min, Avg, Max song duration in {dataset_name}:', 'green')
        print(df['song_duration'].describe())
        cprint('*' * 50, 'green')
        plt.figure(figsize=(16, 8))
        sns.histplot(x=df['song_duration'], color="#1db954")
        plt.title(f'Song Duration Distribution - {dataset_name}')
        plt.show()

        # Song popularity distribution
        cprint(f'Song popularity stats in {dataset_name}:', 'green')
        print(df['song_popularity'].describe())
        cprint(f'Most frequent popularity value:', 'green')
        print(df['song_popularity'].mode())
        cprint('*' * 50, 'green')
        plt.figure(figsize=(16, 8))
        sns.countplot(x=df['song_popularity'], color="#1db954")
        plt.title(f'Song Popularity Distribution - {dataset_name}')
        plt.show()

        # Artist genres word cloud
        plt.figure(figsize=(20, 20))
        wordcloud = WordCloud(min_font_size=3, max_words=250, width=1600, height=680).generate(
            " ".join(df['artist_genres'].dropna())
        )
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'Artist Genres Word Cloud - {dataset_name}')
        plt.axis('off')
        plt.show()

        # Audio features analysis
        plt.figure(figsize=(16, 8))
        sns.barplot(x=df['key'], y=df['song_popularity'], color="#1db954")
        plt.title(f'Key vs Popularity - {dataset_name}')
        plt.show()

        plt.figure(figsize=(16, 8))
        sns.jointplot(x=df['acousticness'], y=df['song_popularity'], color="#1db954")
        plt.suptitle(f'Acousticness vs Popularity - {dataset_name}', y=1.02)
        plt.show()

        plt.figure(figsize=(16, 8))
        sns.jointplot(x=df['loudness'], y=df['song_popularity'], color="#1db954")
        plt.suptitle(f'Loudness vs Popularity - {dataset_name}', y=1.02)
        plt.show()

    except Exception as e:
        print(f"Error analyzing data for {dataset_name}: {e}")