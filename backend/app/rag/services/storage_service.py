from pathlib import Path


UPLOAD_DIR = Path("app/rag/upload/uploads").resolve()


def upload_document(buffer: bytes, filename: str) -> str:

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = UPLOAD_DIR / filename

    file_path.write_bytes(buffer)

    return str(file_path)