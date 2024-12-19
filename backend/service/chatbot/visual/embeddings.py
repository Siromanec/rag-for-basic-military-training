import pathlib

import clip
import torch
from PIL import Image

from .load_multimodal_model import CLIP_model, CLIP_preprocess, DEVICE


def generate_image_embedding(image_path: pathlib.Path):
    image = CLIP_preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        image_features = CLIP_model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)  # Normalize embeddings
    return image_features.cpu().numpy().squeeze()


def generate_query_embedding(query):
    max_context_length = 77
    text = clip.tokenize([query[:max_context_length - 3] + "..."]).to(DEVICE)
    with torch.no_grad():
        text_features = CLIP_model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)  # Normalize embeddings
    return text_features.cpu().numpy().squeeze()



if __name__ == "__main__":
    raise NotImplementedError()
