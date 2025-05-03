# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

# ----------------------------------------
# openai_client.py
# ----------------------------------------
# Description:
#   Centralized OpenAI client wrapper with retry logic
#
# Responsibilities:
#   - Load environment variables (OPENAI_API_KEY) via python-dotenv
#   - Instantiate the OpenAI client once
#   - Provide retry-enabled functions:
#       * chat_completion(messages, functions=None, model, temperature)
#       * create_embedding(text, model)
#   - Use tenacity for exponential backoff on API calls
#   - Define and manage default model names and parameters
#   - Consistent error handling (catch OpenAIError)
#   - Simplify API usage for all downstream agents
from dotenv import load_dotenv
load_dotenv()  # load OPENAI_API_KEY into environment

import os
from openai import OpenAI, OpenAIError
from tenacity import retry, stop_after_attempt, wait_exponential

# Instantiate a single OpenAI client with the API key
_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def chat_completion(messages, functions=None, model="gpt-4o", temperature=0.2):
    """
    Wrapper for OpenAI Chat Completion with retry logic.
    :param messages: list of dicts [{role, content}, ...]
    :param functions: optional list of function schemas for function-calling
    :param model: LLM model name
    :param temperature: sampling temperature
    :return: OpenAI API response
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
    Wrapper for OpenAI Embedding creation with retry logic.
    :param text: string or list of strings
    :param model: embedding model name
    :return: OpenAI API response
    """
    return _client.embeddings.create(
        model=model,
        input=text,
    )
