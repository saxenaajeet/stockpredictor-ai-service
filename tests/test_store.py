from app.ingestion.vector_store import store_documents

# fake document object (simple version)
class Doc:
    def __init__(self, text):
        self.page_content = text
        self.metadata = {"source": "test"}

docs = [
    Doc("Apple faces supply chain risk"),
    Doc("Apple revenue is growing from services"),
    Doc("iPhone demand is slowing in some regions")
]

store_documents(docs, ticker="AAPL")

print("Stored successfully!")