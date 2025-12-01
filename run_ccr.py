import os
import openai
import sys
import json

# --- Step 1: API Key setup ---
openai_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY2")
if not openai_key:
    print("❌ No valid OpenAI API key found. Please set OPENAI_API_KEY or OPENAI_API_KEY2 environment variable.")
    sys.exit(1)

openai.api_key = openai_key

# --- Step 2: Determine file type (plan or task) ---
if len(sys.argv) < 2:
    print("Usage: python run_ccr.py <plan.json|task.json>")
    sys.exit(1)

file_path = sys.argv[1]
if not os.path.exists(file_path):
    print(f"❌ File not found: {file_path}")
    sys.exit(1)

# Load JSON content
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Step 3: Make OpenAI API call ---
try:
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a CCR assistant."},
            {"role": "user", "content": json.dumps(data)}
        ]
    )
    print("✅ CCR Response:")
    print(response.choices[0].message.content)

except openai.error.RateLimitError:
    print("⚠️ Rate limit exceeded. Your OpenAI API key quota is used up. Please check your plan or use another key.")

except openai.error.AuthenticationError:
    print("❌ Invalid OpenAI API key. Please check your key and environment variable.")

except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
