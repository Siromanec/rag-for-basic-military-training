import json
import pathlib

import faiss
import numpy as np
from loguru import logger as console_logger

from .embeddings import generate_image_embedding

embedding_dim = 512
index = faiss.IndexFlatL2(embedding_dim)

image_metadata = []


def add_images_to_index(image_paths):
    global index, image_metadata
    for image_path in image_paths:
        embedding = generate_image_embedding(image_path)
        index.add(np.array([embedding]))
        image_metadata.append(str(image_path.resolve()))


def save_index_and_metadata(index, metadata, index_path: pathlib.Path, metadata_path: pathlib.Path):
    faiss.write_index(index, str(index_path))
    with open(metadata_path, "w") as f:
        json.dump(metadata, f)
    console_logger.info("Index and metadata saved successfully.")


def load_index_and_metadata(index_path: pathlib.Path, metadata_path: pathlib.Path):
    index = faiss.read_index(str(index_path))
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    console_logger.info("Index and metadata loaded successfully.")
    return index, metadata



if __name__ == "__main__":
    data_dir = pathlib.Path(".") / "backend" / "data"
    for image_path in (data_dir / "extracted_images").rglob("*"):
        if image_path.is_dir() or image_path.suffix == "":
            continue
        try:
            add_images_to_index([image_path])
        except Exception as e:
            console_logger.warning(f"{str(e)=}")

    save_index_and_metadata(index, image_metadata, data_dir / "faiss_index.bin", data_dir / "image_metadata.json")