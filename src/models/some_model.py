import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer


def cluster_movies_by_plot(movies_with_characters, n_clusters=20):
    """
    Cluster movies based on their plot summaries using TF-IDF vectorization,
    dimensionality reduction, and K-means clustering.
    
    Args:
        movies_with_characters (pd.DataFrame): DataFrame containing movie data with plot summaries
        n_clusters (int): Number of clusters to create (default: 20)
        
    Returns:
        pd.DataFrame: Original DataFrame with cluster assignments added
        dict: Dictionary containing the clustering model components
    """
    # Preprocess and vectorize the plot text
    tfidf = TfidfVectorizer(
        max_features=1000,  # Limit to top 1000 terms
        stop_words="english", 
        ngram_range=(1, 2),  # Consider both single words and bigrams
        min_df=5,  # Ignore terms that appear in less than 5 documents
    )

    # Create document-term matrix
    plot_features = tfidf.fit_transform(movies_with_characters["plot"])

    # Reduce dimensionality
    svd = TruncatedSVD(n_components=100)
    plot_features_reduced = svd.fit_transform(plot_features)

    # Cluster the movies
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    movies_with_characters["cluster"] = kmeans.fit_predict(plot_features_reduced)

    def get_top_terms_per_cluster():
        # Get the cluster centers in terms of the original TF-IDF features
        original_space_centroids = svd.inverse_transform(kmeans.cluster_centers_)

        cluster_terms = {}
        for cluster in range(n_clusters):
            top_indices = np.argsort(original_space_centroids[cluster])[-10:]  # Top 10 terms
            top_terms = [tfidf.get_feature_names_out()[i] for i in top_indices]
            cluster_terms[cluster] = top_terms
            print(f"\nCluster {cluster} top terms:")
            print(", ".join(top_terms))
        return cluster_terms

    cluster_terms = get_top_terms_per_cluster()
    
    return movies_with_characters, {
        "tfidf": tfidf,
        "svd": svd, 
        "kmeans": kmeans,
        "cluster_terms": cluster_terms
    }