import pathlib

import PIL.Image

from .index_queries import search_similar_images
from .index_serialization import load_index_and_metadata


class SimilarImagesSearcher:
    def __init__(self, precomputed_data_folder: pathlib.Path):
        self.index, self.metadata = load_index_and_metadata(precomputed_data_folder / "faiss_index.bin",
                                                            precomputed_data_folder / "image_metadata.json")

    @staticmethod
    def _load_image(image_path: str):
        return PIL.Image.open(image_path).convert("RGB")

    def search_similar_images(self, query):
        image_paths_and_scores = search_similar_images(query, self.index, self.metadata)
        image_paths = [image_paths_and_scores[i][0] for i in range(len(image_paths_and_scores))]
        images = [SimilarImagesSearcher._load_image(image_path) for image_path in image_paths]
        return images
