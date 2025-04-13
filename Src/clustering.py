from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
import plotly.express as px

def apply_clustering(df_pca):
    """Apply KMeans clustering to PCA output."""
    try:
        # Select optimal k
        Elbow_M = KElbowVisualizer(KMeans(random_state=42), k=10)
        Elbow_M.fit(df_pca)
        Elbow_M.show()

        # Fit KMeans
        n_clusters = Elbow_M.elbow_value_ if Elbow_M.elbow_value_ else 5
        KM = KMeans(n_clusters=n_clusters, random_state=42)
        km_pred = KM.fit_predict(df_pca)

        # Add cluster labels
        df_pca["cluster"] = km_pred

        # Visualize clusters
        fig = px.scatter_3d(
            df_pca, x='pca_comp_0', y='pca_comp_1', z='pca_comp_2',
            title="Clusters Visualization", color="cluster"
        )
        fig.update_traces(marker=dict(size=4), selector=dict(mode='markers'))
        fig.update_layout(autosize=False, width=700, height=680)
        fig.show()

        return df_pca, km_pred
    except Exception as e:
        print(f"Error in clustering: {e}")
        return df_pca, None