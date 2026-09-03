from datetime import datetime, timezone


async def parse_txt(file):

    text = (await file.read()).decode("utf-8")

    return {
        "text": text,
        "metaData": {
            "fileName": file.filename,
            "fileType": file.content_type,
            "uploadedAt": datetime.now(timezone.utc)
        }
    }