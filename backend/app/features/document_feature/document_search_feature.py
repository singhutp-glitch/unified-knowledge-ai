import json

from app.prompts.document_search_prompt import DOCUMENT_SEARCH_PROMPT
from app.rag.embeddings.query_embedding import generate_query_embeddings
from app.rag.retrieval.dense.dense_retrieval import retrieve_dense
from app.rag.retrieval.fulltext.fulltext_retrieval import retrieve_fulltext
from app.rag.retrieval.hybrid.hybrid_retrieval import retrieve_hybrid


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

    yield json.dumps(status_data) + "\n"
    

    feature = {}

    print("messages - ", context["userMessages"])

    # Generate embedding for the user's query
    query = context["userPrompt"]
    print("knowledgeScope - ",context["options"]["knowledgeScope"])

    # Retrieve relevant chunks
    chunk_results = await retrieve_hybrid(
        query,
        context["options"]["knowledgeScope"],
        context["chatId"],
        context["userId"],
    )

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
            "citationNumber": index + 1,
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
    yield json.dumps(source_data) + "\n"
    


document_search_feature["should_run"] = should_run
document_search_feature["execute"] = execute