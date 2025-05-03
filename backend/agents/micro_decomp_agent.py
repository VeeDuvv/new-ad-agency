# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/micro_decomp_agent.py

Need for this file (5th-grader explanation):
“Imagine you have one big LEGO step like ‘Draft ad copy.’ This Micro-Decomp Agent
listens to that step and writes down the 3–6 smaller steps you need to finish it—
like ‘Brainstorm headlines,’ ‘Write first draft,’ ‘Edit snappy slogans.’ It gives
you each tiny step with who does it, what tools they need, what they make, and how
long it takes. That way, our robot helpers can follow each little instruction!”
"""

from dotenv import load_dotenv
load_dotenv()  # load OPENAI_API_KEY

import re
import json
from ..utils.openai_client import chat_completion

class MicroDecompAgent:
    """
    Micro-Decomposition Agent:
    Takes a single task and breaks it into concrete subtasks (3–6 items),
    returning detailed JSON for each subtask.
    """

    def drill_down(self, task: dict) -> list[dict]:
        """
        :param task: dict with keys name, role, tools, deliverable, time_estimate
        :return: list of subtasks, each a dict with the same keys
        """
        # Build prompt
        prompt = (
            "You are an expert process architect. Here is a task to decompose:\n\n"
            f"{json.dumps(task, indent=2)}\n\n"
            "Decompose this into 3–6 concrete subtasks. Return ONLY a JSON array of objects, "
            "each with these fields:\n"
            "  name: string\n"
            "  role: string\n"
            "  tools: array of strings\n"
            "  deliverable: string\n"
            "  time_estimate: string\n"
            "Do not include any extra keys or explanatory text—just the JSON array."
        )

        messages = [
            {"role": "system", "content": "You are an expert process architect."},
            {"role": "user",   "content": prompt},
        ]

        # Call the LLM
        resp = chat_completion(messages, model="gpt-4o", temperature=0)
        content = resp.choices[0].message.content.strip()

        # Strip Markdown code fences if present
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        try:
            subtasks = json.loads(content)
            if not isinstance(subtasks, list):
                raise ValueError("Expected a JSON array of subtasks")
            return subtasks
        except (json.JSONDecodeError, ValueError) as e:
            raise RuntimeError(f"Failed to parse subtasks JSON:\n{e}\n\nRaw content:\n{content}")

# Self-test
if __name__ == "__main__":
    agent = MicroDecompAgent()
    sample_task = {
        "name": "Draft ad copy",
        "role": "Copywriter",
        "tools": ["Google Docs", "Grammarly"],
        "deliverable": "3 headline + 2 body copy variants",
        "time_estimate": "4 hours"
    }
    subtasks = agent.drill_down(sample_task)
    print(json.dumps(subtasks, indent=2))
