import clip
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
CLIP_model, CLIP_preprocess = clip.load("ViT-B/32", device=DEVICE)

