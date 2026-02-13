from checktica import detect

student_name = "Cheating Student"
student_essay = """
    What is an AI detector?

    The AI detector is a tool that helps to distinguish human writing from one generated
    by the AI model. We have choosen Checktica because, it offers:
    - the free and open-source Python SDK,
    - very high accuracy over 99%,
    - no length limit of checked texts,
    - the free API.
"""

result = detect(student_essay, detection_method="balanced")
threshold = 0.65

if result.is_llm_generated and result.confidence > threshold:
    print(
        f"Hmmm... The essay handed by {student_name} may need double checking for "
        "signs of external help."
    )
else:
    print("It seems to be a student-written esssay. Let's skip this one.")
