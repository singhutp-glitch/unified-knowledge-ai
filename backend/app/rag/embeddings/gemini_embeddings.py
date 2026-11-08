from google import genai
from google.genai import types

from app.config import settings


ai = genai.Client(
    api_key=settings.gemini_api_key
)


def gemini_embeddings(texts):

    response = ai.models.embed_content(
        model="gemini-embedding-2",
        contents=texts,
        config=types.EmbedContentConfig(
            output_dimensionality=768
        )
    )

    return [
        embedding.values
        for embedding in response.embeddings
    ]


def gemini_query_embedding(text):

    response = ai.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=768
        )
    )

    return response.embeddings[0].values