from app.rag.chunker.strategies.fixed_chunker import fixed_chunking
from app.rag.chunker.strategies.structure_aware_chunker import (
    structure_aware_chunking
)


async def chunk_document(parsed_document):
    chunks = structure_aware_chunking(
        parsed_document
    )

    return chunks