from fastapi import APIRouter
from app.models.document_models import DocumentTestRequest, DocumentTestResponse
from app.core.document_loader import load_text_as_document
from app.core.text_splitter import split_documents

router = APIRouter()


@router.post("/split", response_model=DocumentTestResponse)
def split_text(request: DocumentTestRequest):
    documents = load_text_as_document(
        text=request.text,
        source=request.source
    )

    chunks = split_documents(documents)

    return DocumentTestResponse(
        source=request.source,
        total_chunks=len(chunks),
        chunks=[chunk.page_content for chunk in chunks]
    )