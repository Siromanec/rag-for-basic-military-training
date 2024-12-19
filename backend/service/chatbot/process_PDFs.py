import pathlib
import pickle

from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger as console_logger


def process_PDFs(PDF_paths: list[pathlib.Path], embedding_model) -> VectorStoreRetriever:
    import pymupdf

    pdfs_extracted_texts = []
    for pdf_path in PDF_paths:
        pdf = pymupdf.open(pdf_path)
        pdfs_extracted_texts.append("\n\n".join([pdf[i].get_text() for i in range(len(pdf))]))

    import logging
    logging.getLogger("langchain_text_splitters.base").setLevel(logging.ERROR)

    from langchain_text_splitters import CharacterTextSplitter

    # text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    # text_splitter = SemanticChunker(embeddings=self.embedding_model, breakpoint_threshold_type="percentile")
    # text_splitter = SentenceTransformersTokenTextSplitter(
    #     model_name="lang-uk/ukr-paraphrase-multilingual-mpnet-base")
    # text_splitter = RecursiveCharacterTextSplitter(separators=[".", "\n\n"], chunk_size=500, chunk_overlap=200)

    text_splitter = CharacterTextSplitter(separator=".", chunk_size=350, chunk_overlap=200)

    docs = []
    for extracted_text in pdfs_extracted_texts:
        doc = Document(page_content=extracted_text, metadata={"source": "local"})
        split_docs = text_splitter.split_documents([doc])
        docs.extend(split_docs)

    logging.getLogger("langchain_text_splitters.base").setLevel(logging.INFO)

    vector_store = FAISS.from_documents(docs, embedding_model)
    text_retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 30})
    console_logger.info(f"Retriever successfully initialized.")
    return text_retriever


def serialize_retriever(retriever, vectorstore_path: pathlib.Path, metadata_path: pathlib.Path):
    retriever.vectorstore.save_local(str(vectorstore_path))

    retriever_metadata = {
        "search_kwargs": retriever.search_kwargs
    }
    with open(metadata_path, "wb") as f:
        pickle.dump(retriever_metadata, f)

    console_logger.info("Retriever and metadata serialized successfully.")


def deserialize_retriever(vectorstore_path: pathlib.Path, metadata_path: pathlib.Path,
                          embedding_model) -> VectorStoreRetriever:
    vectorstore = FAISS.load_local(str(vectorstore_path), embedding_model, allow_dangerous_deserialization=True)

    with open(metadata_path, "rb") as f:
        retriever_metadata = pickle.load(f)

    retriever = VectorStoreRetriever(vectorstore=vectorstore, **retriever_metadata)
    console_logger.info("Retriever deserialized successfully.")
    return retriever


if __name__ == "__main__":
    data_dir = pathlib.Path(__file__).absolute().parent.parent.parent / "data"
    PDF_paths = list(data_dir.glob("*.pdf"))
    embedding_model = HuggingFaceEmbeddings(model_name="lang-uk/ukr-paraphrase-multilingual-mpnet-base")
    text_retriever = process_PDFs(PDF_paths, embedding_model)
    serialize_retriever(text_retriever, data_dir / "text_vectorstore", data_dir / "text_metadata.pkl")
    retriever_loaded = deserialize_retriever(data_dir / "text_vectorstore", data_dir / "text_metadata.pkl",
                                             embedding_model)
    retriever_loaded.invoke("Як поводитись в умовах стресу?")
