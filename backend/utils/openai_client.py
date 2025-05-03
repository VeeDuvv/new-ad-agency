# backend/utils/openai_client.py

from dotenv import load_dotenv
load_dotenv()  # load OPENAI_API_KEY

import os
from openai import OpenAI, OpenAIError
from tenacity import retry, stop_after_attempt, wait_exponential

# instantiate client
_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def chat_completion(messages, functions=None, model="gpt-4o", temperature=0.2):
    """
    Wrapper for chat completions with retry.
    :param messages: list of {role, content} dicts
    :param functions: optional list of function definitions
    """
    return _client.chat.completions.create(
        model=model,
        messages=messages,
        functions=functions,
        temperature=temperature,
    )

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def create_embedding(text, model="text-embedding-3-small"):
    """
    Wrapper for embeddings with retry.
    :param text: string or list of strings
    """
    return _client.embeddings.create(
        model=model,
        input=text
    )

# Self-test when run directly
if __name__ == "__main__":
    try:
        resp = chat_completion([{"role":"user","content":"Testing wrapper"}])
        print("Wrapper chat OK:", resp.choices[0].message.content)
        emb = create_embedding("wrapper test")
        print("Wrapper embedding length:", len(emb.data[0].embedding))
    except OpenAIError as e:
        print("Wrapper error:", e)
