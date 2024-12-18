from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import pymupdf

import os

import logging
logging.getLogger("langchain_text_splitters.base").setLevel(logging.ERROR)


## DATA LOADING

print('Loading PDFs')
doc_names = os.listdir('data')
pdfs = []

for doc_name in doc_names:
    pdf = pymupdf.open(f'data/{doc_name}')
    pdfs.append("\n\n".join([pdf[i].get_text() for i in range(len(pdf))]))

print('Loaded PDFs')

docs = []
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
for pdf in pdfs:
    doc = Document(page_content=pdf, metadata={"source": "local"})
    doc = text_splitter.split_documents([doc])
    docs.extend(doc)

print('Splitted PDFs')

# embedding_model = HuggingFaceEmbeddings(model_name="lang-uk/ukr-paraphrase-multilingual-mpnet-base")
# vector_store = FAISS.from_documents(docs, embedding_model)
# retriever = vector_store.as_retriever()

# print('Created text retriever')
