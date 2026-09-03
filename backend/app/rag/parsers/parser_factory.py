from fastapi import UploadFile

from app.rag.parsers.txt_parser import parse_txt
from app.rag.parsers.docling_parser.docling_parser import parse_docling

PARSER_MAP = {
    "application/pdf": parse_docling,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": parse_docling,
    "text/plain": parse_txt,
}


async def parse_document(file: UploadFile):

    parser = PARSER_MAP.get(file.content_type)

    if parser is None:
        raise ValueError("Unsupported file type")

    return await parser(file)