def build_prompt(context):
    if context["features"]:

        enabled_capabilities = []

        for feature in context["features"]:

            resource = feature.get("resource") or "None"

            capability = f"""
<{feature["name"]}>
    <instruction>
    {feature["instruction"]}
    </instruction>
    <resource>
    {resource}
    </resource>
</{feature["name"]}>
"""

            enabled_capabilities.append(capability)

        final_prompt = f"""
<enabledCapabilities>
    {"".join(enabled_capabilities)}
</enabledCapabilities>
<task>
    <objective>
        Answer user question using above instructions
    </objective>
    <userQuestion>
        {context["userPrompt"]}
    </userQuestion>
</task>
"""

    else:

        final_prompt = f"""
<enabledCapabilities>
    -None
</enabledCapabilities>
<task>
    <objective>
        Answer user question
    </objective>
    <userQuestion>
        {context["userPrompt"]}
    </userQuestion>
</task>
"""

    return final_prompt