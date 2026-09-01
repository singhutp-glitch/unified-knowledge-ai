from app.pipeline.context_builder.context_builder import build_context
from app.features.document_feature.document_search_feature import (
    document_search_feature
)


async def build_pipeline_context(context):
    try:
        features = [
            document_search_feature
        ]

        for feature in features:

            if feature.should_run(context):
                await feature.execute(context)

        await build_context(context)

    except Exception as error:
        print(error)