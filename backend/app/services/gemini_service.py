from google import genai
from google.genai import types

from app.config import settings
from app.prompts.system_prompt import SYSTEM_PROMPT


ai = genai.Client(
    api_key=settings.gemini_api_key
)


def generate_response_stream(contents):

    print('content - ',contents)

    stream = ai.models.generate_content_stream(
        model="gemini-3.1-flash-lite",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=1000,
            temperature=1.0,
            top_p=0.95,
        ),
    )

    return stream