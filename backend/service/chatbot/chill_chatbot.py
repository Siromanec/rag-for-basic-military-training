import os
import pathlib
from overrides import override

import google.generativeai as genai
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from loguru import logger as console_logger

from .abstract_chatbot import TextAndImagesChatBot
from .gemini_helpers import generate_RAG_response
from .visual.similar_images_searcher import SimilarImagesSearcher


class ChillChatBot(TextAndImagesChatBot):
    @override
    def __init__(self, PDF_paths: list[pathlib.Path]):
        console_logger.debug(f"{PDF_paths=}")
        self.PDF_paths = PDF_paths

        self.text_retriever = None
        self.embedding_model = None
        self.llm = None
        self.RAG_pipeline = None

        self._process_PDFs()
        self._load_generator_model()
        self._generate_RAG_pipeline()

        self.similar_image_searcher = SimilarImagesSearcher(pathlib.Path(".") / "backend" / "data")

    def _process_PDFs(self) -> None:
        """
        Processes PDFs and creates a text chunks retriever.
        """
        import pymupdf

        pdfs_extracted_texts = []
        for pdf_path in self.PDF_paths:
            pdf = pymupdf.open(pdf_path)
            pdfs_extracted_texts.append("\n\n".join([pdf[i].get_text() for i in range(len(pdf))]))

        import logging
        logging.getLogger("langchain_text_splitters.base").setLevel(logging.ERROR)

        self.embedding_model = HuggingFaceEmbeddings(model_name="lang-uk/ukr-paraphrase-multilingual-mpnet-base")
        # text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        text_splitter = SemanticChunker(embeddings=self.embedding_model, breakpoint_threshold_type="percentile")
        docs = []
        for extracted_text in pdfs_extracted_texts:
            doc = Document(page_content=extracted_text, metadata={"source": "local"})
            split_docs = text_splitter.split_documents([doc])
            docs.extend(split_docs)

        logging.getLogger("langchain_text_splitters.base").setLevel(logging.INFO)

        vector_store = FAISS.from_documents(docs, self.embedding_model)
        self.text_retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 20})

        console_logger.info(f"Retriever and embedder successfully initialized.")

    def _load_generator_model(self) -> None:
        assert pathlib.Path(".env").exists()
        load_dotenv()
        assert os.getenv("GEMINI_API_KEY")

        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        model_name = "gemini-1.5-flash"
        model = genai.GenerativeModel(model_name, generation_config=genai.GenerationConfig(
            max_output_tokens=1000,
            temperature=0.1,
        ))

        self.llm = model

        console_logger.info(f"LLM successfully initialized.")

    def _generate_RAG_pipeline(self) -> None:
        self.RAG_pipeline = lambda query: generate_RAG_response(query, self.text_retriever, self.llm)
        console_logger.info(f"RAG pipeline successfully initialized.")

    @override
    def answer_query(self, query: str) -> tuple[str, list[...]]:
        result = self.RAG_pipeline(query)
        images = self.similar_image_searcher.search_similar_images(query)
        return result["response"], images

    @override
    def get_retrieved_documents(self, query: str) -> list[Document]:
        return self.text_retriever.invoke(query)


if __name__ == "__main__":
    ChillChatBot(PDF_paths=list((pathlib.Path(__file__).absolute().parent.parent / "backend" / "data").glob("*.pdf")))
