from app.interface.IRetriever import IRetriever
class RetrieverService(IRetriever):
    def __init__(self, documents: list[str]):
        self.documents = documents

    def retrieve(self, question: str, top_k: int = 3) -> str:
        results = [doc for doc in self.documents if any(word.lower() in doc.lower() for word in question.split())]
        return "\n".join(results[:top_k])