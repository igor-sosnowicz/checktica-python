from checktica import detect

nickname = "Johnny The Great"
review = """
    Hi,

    I really don't like this product.
    It isn't handy at all and feels cheap.
    I found much better (and cheaper!) solution from one of competitors.
"""

result = detect(text=review, detection_method="fast")

if result.is_llm_generated:
    print(f"The review from {nickname} will not be published until reviewed.")
else:
    print(f"The review from {nickname} looks legitimate. Publishing it right away...")
