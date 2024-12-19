import numpy as np

from .embeddings import generate_query_embedding


def search_similar_images(query, index, metadata, top_k=3):
    query_vector = generate_query_embedding(query)
    distances, indices = index.search(np.array([query_vector]), top_k)
    results = [(metadata[i], distances[0][j]) for j, i in enumerate(indices[0])]
    return results
