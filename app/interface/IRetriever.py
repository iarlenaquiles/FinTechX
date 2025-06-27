from abc import ABC, abstractmethod

class IRetriever(ABC):
    @abstractmethod
    def retrieve(self, question: str, top_k: int = 3) -> str:
        pass