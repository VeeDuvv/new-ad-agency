# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

# ----------------------------------------
# openai_client.py
# ----------------------------------------
# Description:
#   Centralized OpenAI client wrapper with retry logic
#
# Imagine you and your friends all need to call the same super-smart robot (OpenAI) to help with different jobs—one friend writes ad copy, another picks the best bids, another builds reports. Instead of each friend figuring out their own way to dial the robot’s phone number (and what to do if the call drops), you give everyone a single “phone” that already knows the number and will automatically redial if the line cuts out.

# Here’s why that’s awesome:

# One Phone to Rule Them All (Centralized)
# You only have to teach this one phone how to talk to the robot.
# Every helper (agent) uses the same phone, so calls are always made the same way—no confusion.
# Automatic Redials (Retry-Enabled)
# If the line goes dead or the robot is busy, the phone will try again on its own.
# Your agents don’t get stuck waiting or crash—they just keep trying until they get an answer or decide it really won’t work.
# Powering All Your Helpers
# Instead of copying robot-calling code everywhere, every agent just picks up this shared phone.
# That makes your project simpler: one file to update if the robot’s number or language changes.
# In the bigger picture of building an AI-native ad agency, this “centralized, retry-enabled OpenAI client” is like your trusty control panel. It guarantees that no matter which tiny AI helper you build—whether it drafts ads, optimizes bids, or writes reports—they all talk to the robot brain the right way and handle hiccups gracefully, so your whole agency runs smoothly.

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
