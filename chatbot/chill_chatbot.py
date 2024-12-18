import os
import pathlib
from typing import override

from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from langchain_text_splitters import CharacterTextSplitter
from loguru import logger as console_logger

from .abstract_chatbot import TextAndImagesChatBot


class ChillChatBot(TextAndImagesChatBot):
    @override
    def __init__(self, PDF_paths: list[pathlib.Path]):
        console_logger.debug(f"{PDF_paths=}")
        self.PDF_paths = PDF_paths

        self.text_retriever = None
        self.embedding_model = None
        self.llm = None
        self.retrieval_qa_chain = None

        self._process_PDFs()
        self._load_generator_model(to_test=False)
        self._create_retrieval_qa_chain(to_test=True)


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

        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = []
        for extracted_text in pdfs_extracted_texts:
            doc = Document(page_content=extracted_text, metadata={"source": "local"})
            split_docs = text_splitter.split_documents([doc])
            docs.extend(split_docs)

        logging.getLogger("langchain_text_splitters.base").setLevel(logging.INFO)

        self.embedding_model = HuggingFaceEmbeddings(model_name="lang-uk/ukr-paraphrase-multilingual-mpnet-base")
        vector_store = FAISS.from_documents(docs, self.embedding_model)
        self.text_retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

        console_logger.info(f"Retriever and embedder successfully initialized.")

    def _load_generator_model(self, to_test: bool = True) -> None:
        assert pathlib.Path(".env").exists()
        load_dotenv()
        assert os.getenv("HUGGINGFACEHUB_API_TOKEN")

        repo_id = "microsoft/Phi-3.5-mini-instruct"

        self.llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            temperature=0.5,
            model_kwargs=dict(max_length=256),
            huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
        )

        if to_test:
            self.llm.invoke("test run. Tell me a powerful joke.")

        console_logger.info(f"LLM successfully initialized.")

    def _create_retrieval_qa_chain(self, to_test: bool = True) -> None:
        from langchain.chains import RetrievalQA

        self.retrieval_qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.text_retriever,
            return_source_documents=True,
        )

        if to_test:
            self.retrieval_qa_chain.invoke("Хахаха! Попався!! Це ТЦК!!!!")


    @override
    def answer_query(self, query: str) -> tuple[str, list[...]]:
        ...

    @override
    def get_retrieved_documents(self, query: str) -> list[Document]:
        ...


if __name__ == "__main__":
    ChillChatBot(PDF_paths=list((pathlib.Path(__file__).absolute().parent.parent / "benchmark" / "data").glob("*.pdf")))
