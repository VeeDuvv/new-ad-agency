# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/func_decomp_agent.py

Need for this file (5th-grader explanation):
“Remember our Blueprint Maker that lists steps for a toy set? Now 
it can read the rulebook you pick (APQC or eTOM) and break the 
job into FIVE levels: the big function, then processes, activities, 
tasks, and even subtasks. It follows the rulebook’s names so big 
companies can plug it right into their way of doing things!”
"""

from dotenv import load_dotenv
load_dotenv()  # auto-load OPENAI_API_KEY

import re
import json
from ..utils.openai_client import chat_completion

class FuncArchAgent:
    """
    Function Decomposition Agent:
    Break a high-level agency function into L0–L4 structure under a chosen framework.
    """

    def decompose(
        self, 
        function_name: str, 
        framework: str = "APQC", 
        context: str = "AI-native ad agency"
    ):
        """
        :param function_name: e.g. "Media Buying & Execution"
        :param framework: "APQC" or "eTOM"
        :param context: for tailoring language
        :return: dict with keys L0…L4 mapping to nested arrays of objects
        """
        prompt = (
            f"Use the {framework} process classification framework. "
            f"Decompose the function '{function_name}' in the context of a {context} "
            "into five levels: L0 (Function), L1 (Process), L2 (Activity), "
            "L3 (Task), L4 (Subtask). Return ONLY valid JSON with a top-level key "
            "'levels', which is an object with keys 'L0','L1','L2','L3','L4'. Each level "
            "should be an array of items. For each item at every level include:\n"
            "  name: string\n"
            "  role: string\n"
            "  tools: array of strings\n"
            "  deliverable: string\n"
            "  time_estimate: string\n"
            "Do not include any extra text—just the JSON."
        )

        messages = [
            {"role": "system", "content": "You are an expert process architect."},
            {"role": "user",   "content": prompt},
        ]

        resp = chat_completion(messages, model="gpt-4o", temperature=0)
        content = resp.choices[0].message.content.strip()
        # Strip code fences
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON:\n{e}\n\nRaw content:\n{content}")
