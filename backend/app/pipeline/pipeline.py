from app.pipeline.context_builder.context_builder import build_context
from app.features.document_feature.document_search_feature import (
    document_search_feature
)


async def build_pipeline_context(context):
    try:
        print("enter in pipeline")
        features = [
            document_search_feature
        ]

        for feature in features:

            if feature["should_run"](context):
                async for event in feature["execute"](context):
                    yield event
        print("start build_context")
        build_context(context)

    except Exception as error:
        print(error)
        raise