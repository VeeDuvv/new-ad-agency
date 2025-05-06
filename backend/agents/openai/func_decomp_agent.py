# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/openai/func_decomp_agent.py

Need for this file (5th-grader explanation):
“Remember our Blueprint Maker that draws out all the steps? Now it will write 
down five full lists: one for the big job (Function), one for each of the four 
next levels (Processes, Activities, Tasks, Subtasks). That way, your map and 
the tables all know exactly what goes where—no steps get hidden under the wrong 
heading!”
"""

import re
import json
import logging

from backend.utils.openai_client import chat_completion
from backend.agents.base import Agent

logger = logging.getLogger("blueprint_maker.func_decomp")

class FuncArchAgent(Agent):
    def run(self, payload: dict) -> dict:
        fn = payload["function_name"]
        fw = payload["framework"]
        return self.decompose(fn, fw)

    def decompose(
        self,
        function_name: str,
        framework: str = "APQC",
        context: str = "AI-native ad agency"
    ) -> dict:
        # 1) Build the prompt
        prompt = (
            f"Use the {framework} process classification framework. "
            f"Decompose the function '{function_name}' in the context of a {context} "
            "into five levels: L0 (Function), L1 (Process), L2 (Activity), "
            "L3 (Task), and L4 (Subtask).\n\n"
            "Return ONLY valid JSON with a top-level key \"levels\", whose value is an object with keys:\n"
            "- \"L0\": an array containing exactly one object representing the function, with fields name, role, tools, deliverable, time_estimate, and subitems (array of its processes).\n"
            "- \"L1\": an array of each process (same objects from L0[0].subitems), each with subitems (activities).\n"
            "- \"L2\": an array of each activity (from every L1[].subitems), each with subitems (tasks).\n"
            "- \"L3\": an array of each task (from every L2[].subitems), each with subitems (subtasks).\n"
            "- \"L4\": an array of each subtask (from every L3[].subitems), each with fields name, role, tools, deliverable, time_estimate (no subitems).\n\n"
            "Do not include any other keys or explanatory text—just the JSON."
        )
        messages = [
            {"role": "system", "content": "You are an expert process architect."},
            {"role": "user",   "content": prompt},
        ]

        # 2) Call the LLM
        resp = chat_completion(messages, model="gpt-4o", temperature=0)

        # 3) Strip markdown fences
        content = resp.choices[0].message.content.strip()
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        # 4) Parse JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            logger.error("JSON parse error: %s\nRaw content:\n%s", e, content)
            raise RuntimeError(f"Failed to parse JSON:\n{e}\n\nRaw content:\n{content}")

        # 5) Normalize: ensure each L0–L4 is a list
        levels = data.get("levels", {})
        for lvl in ["L0", "L1", "L2", "L3", "L4"]:
            if lvl in levels and not isinstance(levels[lvl], list):
                levels[lvl] = [levels[lvl]]
        data["levels"] = levels

        # 6) Normalize each item's tools and subitems recursively
        def normalize_item(item: dict):
            if "tools" in item and not isinstance(item["tools"], list):
                item["tools"] = [item["tools"]]
            # Subitems might be missing or a single object
            subs = item.get("subitems")
            if subs is None:
                item["subitems"] = []
            else:
                if not isinstance(subs, list):
                    subs = [subs]
                item["subitems"] = subs
                for child in item["subitems"]:
                    normalize_item(child)

        for lvl in ["L0", "L1", "L2", "L3", "L4"]:
            for itm in data["levels"].get(lvl, []):
                normalize_item(itm)

        return data
