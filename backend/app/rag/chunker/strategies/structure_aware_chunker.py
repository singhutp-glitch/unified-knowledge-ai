def structure_aware_chunking(normalized_document):

    chunks = []

    chunk_index = 0
    current_heading = ""

    for element in normalized_document.elements:

        if (
            element.type == "key_value_area"
            or element.type == "page_footer"
            or element.type == "page_header"
        ):
            continue

        # Remember the latest heading
        if element.type== "section_header":
            current_heading = element.markdown
            continue

        chunks.append({
            "index": chunk_index,
            "text": element.markdown,
            "type": element.type,
            "sectionHeading": current_heading,
            "pages": element.pages,
            "startPage": element.pages[0],
            "endPage": element.pages[-1]
        })

        chunk_index += 1

    return chunks