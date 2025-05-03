# backend/utils/test_openai.py

import os
from openai import OpenAI
from openai.error import OpenAIError

def test_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("🔥 OPENAI_API_KEY not set")
        return

    client = OpenAI()
    try:
        # Simple ChatCompletion test
        chat = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role":"user","content":"Hello, OpenAI!"}]
        )
        print("✅ ChatCompletion OK:", chat.choices[0].message.content)

        # Simple Embedding test
        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input="test embedding"
        )
        print("✅ Embedding OK; vector length:", len(emb.data[0].embedding))

    except OpenAIError as e:
        print("❌ OpenAI API error:", e)

if __name__ == "__main__":
    test_openai()
