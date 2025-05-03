# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/func_decomp_agent.py

Need for this file (5th-grader explanation):
“Remember our Blueprint Maker that draws out all the steps? Now it will write 
down five full lists: one for the big job (Function), one for each of the four 
next levels (Processes, Activities, Tasks, Subtasks). That way, your map and 
the tables all know exactly what goes where—no steps get hidden under the wrong 
heading!”
"""

from dotenv import load_dotenv
load_dotenv()

import re, json
from ...utils.openai_client import chat_completion
from ..base import Agent
from ..openai.micro_decomp_agent import MicroDecompAgent

class FuncArchAgent (Agent):
    def decompose(
        self,
        function_name: str,
        framework: str = "APQC",
        context: str = "AI-native ad agency"
    ):
        prompt = (
            f"Use the {framework} process classification framework. "
            f"Decompose the function '{function_name}' in the context of a {context} "
            "into five levels: L0 (Function), L1 (Process), L2 (Activity), "
            "L3 (Task), and L4 (Subtask).  \n\n"
            "Return ONLY valid JSON with a top-level key \"levels\", whose value is an object with keys:\n"
            "- \"L0\": an array containing exactly one object representing the function, with fields name, role, tools, deliverable, time_estimate, and subitems (an array of its processes).\n"
            "- \"L1\": an array containing each process (the same objects from L0[0].subitems), each with the same fields including subitems (activities).\n"
            "- \"L2\": an array containing each activity (from every L1[].subitems), each with the same fields including subitems (tasks).\n"
            "- \"L3\": an array containing each task (from every L2[].subitems), each with the same fields including subitems (subtasks).\n"
            "- \"L4\": an array containing each subtask (from every L3[].subitems), each with only fields name, role, tools, deliverable, time_estimate (no subitems).\n\n"
            "Do not include any other keys or any explanatory text—just the JSON."
        )

        messages = [
            {"role": "system", "content": "You are an expert process architect."},
            {"role": "user",   "content": prompt},
        ]
        resp = chat_completion(messages, model="gpt-4o", temperature=0)
        content = resp.choices[0].message.content.strip()
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON:\n{e}\n\nRaw content:\n{content}")
