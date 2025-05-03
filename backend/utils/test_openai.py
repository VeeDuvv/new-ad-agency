# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

# backend/utils/test_openai.py

from dotenv import load_dotenv
load_dotenv()

import os
from openai import OpenAI, OpenAIError

def test_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("🔥 OPENAI_API_KEY not set")
        return

    client = OpenAI(api_key=api_key)

    try:
        # ChatCompletion via new client interface
        chat_resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role":"user","content":"Hello, OpenAI!"}]
        )
        print("✅ ChatCompletion OK:", chat_resp.choices[0].message.content)

        # Embedding via new client interface
        emb_resp = client.embeddings.create(
            model="text-embedding-3-small",
            input="test embedding"
        )
        print("✅ Embedding OK; vector length:", len(emb_resp.data[0].embedding))

    except OpenAIError as e:
        print("❌ OpenAI API error:", e)

if __name__ == "__main__":
    test_openai()
