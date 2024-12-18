import pathlib
from abc import ABC, abstractmethod

from langchain.docstore.document import Document


class TextAndImagesChatBot(ABC):
    @abstractmethod
    def __init__(self, PDF_paths: list[pathlib.Path]) -> None:
        pass

    @abstractmethod
    def get_retrieved_documents(self, query: str) -> list[Document]:
        """
        Retrieved by RAG documents.
        """
        pass

    @abstractmethod
    def answer_query(self, query: str) -> tuple[str, list[...]]:
        """
        A pair: text (response), and a list of potentially suitable images.
        """
        pass
