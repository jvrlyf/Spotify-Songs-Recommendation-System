from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
import plotly.express as px

def apply_dimensionality_reduction(df):
    """Apply PCA to reduce dimensionality of audio features."""
    try:
        # Split audio features
        audio_features = [
            'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'
        ]
        df_audios = df[audio_features]

        # Standard scaling
        std_scaler = StandardScaler()
        std_data = std_scaler.fit_transform(df_audios)
        scaled_df = pd.DataFrame(std_data, columns=df_audios.columns)

        # Apply PCA
        pca = PCA(n_components=3, svd_solver='full')
        lowdim_df = pca.fit_transform(scaled_df)

        # Create PCA DataFrame
        columns = [f'pca_comp_{i}' for i in range(3)]
        df_pca = pd.DataFrame(lowdim_df, columns=columns, index=scaled_df.index)

        # Visualize PCA output
        fig = px.scatter_3d(
            df_pca, x='pca_comp_0', y='pca_comp_1', z='pca_comp_2',
            size_max=20, color_discrete_sequence=['#1db954'],
            title="PCA Output Visualization"
        )
        fig.update_traces(
            marker=dict(size=8, line=dict(width=2, color='#121212')),
            selector=dict(mode='markers')
        )
        fig.update_layout(autosize=False, width=700, height=680)
        fig.show()

        return df_pca
    except Exception as e:
        print(f"Error in dimensionality reduction: {e}")
        return None