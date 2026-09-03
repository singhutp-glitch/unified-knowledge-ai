from docling_core.types.doc.document import DoclingDocument

from app.rag.parsers.docling_parser.models import (
    DocumentElement,
    NormalizedDocument
)


def normalize_docling_document(
    doclingDocument: DoclingDocument
) -> NormalizedDocument:

    elements = []

    for index, child in enumerate(doclingDocument.body.children):

        #
        # Resolve the body reference into the real object
        #
        element = child.resolve(doclingDocument)

        #
        # Collect page numbers
        #
        pages = []

        if hasattr(element, "prov") and element.prov:

            pages = sorted(
                {
                    p.page_no
                    for p in element.prov
                }
            )
        elif element.label == 'list':
            pages = list_to_pages(element,doclingDocument )

        #
        # Convert different element types
        #
        if hasattr(element, "export_to_markdown"):

            try:
               markdown = element.export_to_markdown()

            except TypeError:
                markdown = element.export_to_markdown(doclingDocument)

        elif hasattr(element, "text"):

            markdown = element.text

        elif element.label == "list":
            markdown = list_to_markdown(element,doclingDocument)
        else:

            markdown = ""

        #
        # Store normalized element
        #
        elements.append(

            DocumentElement(

                element_index=index,

                type=element.label,

                markdown=markdown,

                pages=pages

            )

        )

    return NormalizedDocument(elements=elements)


def list_to_markdown(list_group, doc):

    markdown_lines = []

    for child_ref in list_group.children:

        child = child_ref.resolve(doc)

        markdown_lines.append(f"- {child.text}")

    return "\n".join(markdown_lines)

def list_to_pages(list_group, doc):

    pages = []
    seen = set()

    for child_ref in list_group.children:

        child = child_ref.resolve(doc)

        provs = getattr(child, "prov", None)

        if not provs:
            continue

        for prov in provs:
            page = getattr(prov, "page_no", None)

            if page is not None and page not in seen:
                seen.add(page)
                pages.append(page)

    return pages