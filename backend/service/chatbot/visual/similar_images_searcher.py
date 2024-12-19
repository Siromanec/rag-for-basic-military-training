import pathlib
import numpy as np
import PIL.Image

from .index_queries import search_similar_images
from .index_serialization import load_index_and_metadata


class SimilarImagesSearcher:
    def __init__(self, precomputed_data_folder: pathlib.Path):
        self.index, self.metadata = load_index_and_metadata(precomputed_data_folder / "faiss_index.bin",
                                                            precomputed_data_folder / "image_metadata.json")

    @staticmethod
    def _load_image(image_path: str) -> np.ndarray:
        return np.array(PIL.Image.open(image_path).convert("RGB"))

    def search_similar_images(self, query) -> list[np.ndarray]:
        image_paths_and_scores = search_similar_images(query, self.index, self.metadata)
        threshold = 0.3
        image_paths = [image_path for image_path, score in image_paths_and_scores if score > threshold]
        images = [SimilarImagesSearcher._load_image(image_path) for image_path in image_paths]
        return images
