

from langchain_core.documents import Document


def load_text_as_document(text: str, source: str = "manual") -> list[Document]:
    return [
        Document(
            page_content=text,
            metadata={
                "source": source
            }
        )
    ]