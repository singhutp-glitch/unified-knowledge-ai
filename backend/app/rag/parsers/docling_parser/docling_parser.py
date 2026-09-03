from io import BytesIO

from fastapi import UploadFile
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream
from docling_core.types.doc.document import DoclingDocument
from app.rag.parsers.docling_parser.extractor import normalize_docling_document

converter = DocumentConverter()


async def parse_docling(file: UploadFile) -> DoclingDocument:

    source = DocumentStream(
        name=file.filename,
        stream=BytesIO(file.file_content)
    )

    print(f"Parsing {file.filename}")

    result = converter.convert(source)
    document = result.document
    print(document.export_to_markdown()[:2000])
    normalized_document = normalize_docling_document(document)
        

    return normalized_document