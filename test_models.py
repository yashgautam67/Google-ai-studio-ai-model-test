import os
import json
import time

from google import genai

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

print("="*80)
print("Fetching Available Models...")
print("="*80)

models = client.models.list()

results = []

for model in models:

    name = model.name

    # Sirf GenerateContent models test karna
    if "generateContent" not in model.supported_actions:
        continue

    print(f"\nTesting {name}")

    start = time.time()

    try:

        response = client.models.generate_content(
            model=name,
            contents="Reply only with OK"
        )

        elapsed = round(time.time()-start,2)

        print("PASS")

        results.append({
            "model": name,
            "status": "PASS",
            "time": elapsed,
            "response": response.text
        })

    except Exception as e:

        print("FAIL")

        results.append({
            "model": name,
            "status": "FAIL",
            "error": str(e)
        })


# JSON Report

with open("report.json","w") as f:
    json.dump(results,f,indent=2)


# Markdown Report

with open("report.md","w") as f:

    f.write("# Gemini Model Health Report\n\n")

    f.write("| Model | Status | Time | Response/Error |\n")
    f.write("|------|------|------|------|\n")

    for r in results:

        if r["status"]=="PASS":

            f.write(
                f"| {r['model']} | ✅ PASS | {r['time']} sec | {r['response']} |\n"
            )

        else:

            f.write(
                f"| {r['model']} | ❌ FAIL | - | {r['error']} |\n"
            )

print("\nDone.")
