def fixed_chunking(parsed_document):

    start = 0
    chunks_index = 0

    chunk_size = 1000
    overlap = 200

    chunks = []

    while start < len(parsed_document):

        end = start + chunk_size

        chunk_text = parsed_document[start:end]

        chunk = {
            "text": chunk_text,
            "index": chunks_index
        }

        chunks.append(chunk)

        start = end - overlap
        chunks_index += 1

    return chunks