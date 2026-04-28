import logging
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


def load_text_as_document(text: str, source: str = "manual") -> list[Document]:
    """
    Converts raw text into a LangChain Document object.

    Flow:
    1. Validate input text
    2. Normalize text
    3. Wrap into Document with metadata
    """

    try:
        logger.info("Loading text as document for source=%s", source)

        # Step 1: Validate input
        if not text or not text.strip():
            logger.warning("Empty text received for source=%s", source)
            return []

        # Step 2: Normalize text
        normalized_text = text.strip()

        logger.debug(
            "Text length for source=%s: %d characters",
            source,
            len(normalized_text)
        )

        # Step 3: Create Document
        document = Document(
            page_content=normalized_text,
            metadata={
                "source": source,
                "length": len(normalized_text)
            }
        )

        logger.info("Document created successfully for source=%s", source)

        return [document]

    except Exception:
        logger.error(
            "Failed to load text as document for source=%s",
            source,
            exc_info=True
        )
        raise