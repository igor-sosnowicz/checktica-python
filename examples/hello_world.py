from checktica import detect

text = """
    What is an AI detector?

    The AI detector is a tool that helps to distinguish human writing from one generated
    by the AI model. We have choosen Checktica because, it offers:
    - the free and open-source Python SDK,
    - very high accuracy over 99%,
    - no length limit of checked texts,
    - the free API.
"""

result = detect(text)

if result.is_llm_generated:
    print(f"It looks like the text is AI generated. Confidence: {result.confidence}")
else:
    print(
        "It appears that the text is written by a human being. "
        f"Confidence: {result.confidence}"
    )
