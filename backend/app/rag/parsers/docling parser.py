from io import BytesIO

from fastapi import UploadFile
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream
from docling_core.types.doc.document import DoclingDocument


converter = DocumentConverter()


async def parse_docling(file: UploadFile) -> DoclingDocument:

    file_bytes = await file.read()

    source = DocumentStream(
        name=file.filename,
        stream=BytesIO(file_bytes)
    )

    print(f"Parsing {file.filename}")

    result = converter.convert(source)

    return result.document