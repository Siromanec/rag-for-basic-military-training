# RAG for basic military training

Requirements:
- Python 3.12+

## Installation

### Python Dependencies

```bash
pip install -r requirements.txt
```

## Benchmarking

```bash
python benchmark.py
```

## Indexing the text in PDFs
```bash
 python -m backend.service.chatbot.process_PDFs
```
Now, you can use the chill bot.

## Creating the index for image retrieval

1. Extract images from the PDFs.
    ```bash
   python -m backend.service.chatbot.visual.image_extractor
   ```
2. Create the FAISS index out of them:
   ```bash
   python -m backend.service.chatbot.visual.index_serialization
   ```

Now, you are to use a [chill chatbot](backend/service/chatbot/chill_chatbot.py).