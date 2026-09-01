from app.pipeline.context_builder.prompt_builder import build_prompt


async def build_context(context):
    contents = [
        {
            "role": (
                "model"
                if message["role"] == "assistant"
                else "user"
            ),
            "parts": [
                {
                    "text": message["content"]
                }
            ]
        }
        for message in context["userMessages"]
    ]

    final_prompt = build_prompt(context)

    contents[-1] = {
        "role": "user",
        "parts": [
            {
                "text": final_prompt
            }
        ]
    }

    context["contents"] = contents