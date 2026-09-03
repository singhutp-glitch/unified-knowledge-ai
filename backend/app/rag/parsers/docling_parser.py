from io import BytesIO

from fastapi import UploadFile
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream
from docling_core.types.doc.document import DoclingDocument


converter = DocumentConverter()


async def parse_docling(file: UploadFile) -> DoclingDocument:

    source = DocumentStream(
        name=file.filename,
        stream=BytesIO(file.file_content)
    )

    print(f"Parsing {file.filename}")

    result = converter.convert(source)
    print(result.document.export_to_markdown()[:2000])

    return result.document