import os
import time
from google import genai

API_KEY = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=API_KEY)

MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2-flash",
    "gemini-2-flash-lite"
]

print("=" * 90)
print("Gemini Models Health Report")
print("=" * 90)

working = 0
failed = 0

for model in MODELS:

    print(f"\nTesting {model}")

    start = time.time()

    try:

        response = client.models.generate_content(
            model=model,
            contents="Reply with only OK"
        )

        elapsed = round(time.time() - start, 2)

        print("Status  : PASS")
        print("Time    :", elapsed, "sec")
        print("Answer  :", response.text)

        working += 1

    except Exception as e:

        print("Status  : FAIL")
        print("Reason  :", str(e))

        failed += 1

print("\n")
print("=" * 90)
print("SUMMARY")
print("=" * 90)

print("Working :", working)
print("Failed  :", failed)
print("Total   :", len(MODELS))
