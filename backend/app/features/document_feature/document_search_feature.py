import json

from app.prompts.document_search_prompt import DOCUMENT_SEARCH_PROMPT
# from app.rag.embeddings.query_embedding import generate_query_embeddings
# from app.rag.services.retrieval_service import retrieve_chunks


document_search_feature = {
    "name": "documentSearch",
}


def should_run(context):
    return context["options"].get("documentSearch", False)


async def execute(context):
    # Send status to the client
    status_data = {
        "type": "status",
        "status": "Searching..."
    }

    # context["stream"].write(
    #     json.dumps(status_data) + "\n"
    # )

    feature = {}

    print("messages - ", context["userMessages"])

    # # Generate embedding for the user's query
    # query_embedding = await generate_query_embeddings(
    #     context["userPrompt"]
    # )

    # # Retrieve relevant chunks
    # chunk_results = await retrieve_chunks(
    #     query_embedding,
    #     context["chatId"]
    # )
    chunk_results = []

    # Build text representation of retrieved chunks
    result_text = "\n".join(
        f"""
Source id: [{index + 1}]
Name: {chunk["originalFileName"]}
content: {chunk["text"]}
"""
        for index, chunk in enumerate(chunk_results)
    )

    # Add citation numbers to retrieved chunks
    context["documentSources"] = [
        {
            **chunk,
            "citationNumber": index + 1
        }
        for index, chunk in enumerate(chunk_results)
    ]

    # Build feature information
    feature["name"] = "documentSearch"
    feature["instruction"] = DOCUMENT_SEARCH_PROMPT
    feature["resource"] = result_text

    # Add feature to shared context
    context["features"].append(feature)

    # Send document source information to client
    source_data = {
        "type": "documentSources",
        "sources": context["documentSources"]
    }

    context["stream"].write(
        json.dumps(source_data) + "\n"
    )


document_search_feature["should_run"] = should_run
document_search_feature["execute"] = execute