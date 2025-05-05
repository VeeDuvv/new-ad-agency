# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/openai/micro_decomp_agent.py

Need for this file (5th-grader explanation):
“Imagine you have a big task like ‘Draft Campaign Brief.’ MicroDecompAgent
chops it into 3–6 bite-sized steps—like ‘Write outline,’ ‘Add KPIs,’
‘Review with team’—so our robots (and people) know exactly what to do first,
second, third, and so on.”
"""

import re, json
from ..base import Agent
from ...utils.openai_client import chat_completion

class MicroDecompAgent(Agent):
    def run(self, payload: dict) -> dict:
        """
        :param payload: {
            "name": str,
            "role": str,
            "tools": List[str],
            "deliverable": str,
            "time_estimate": str
        }
        :return: { "subtasks": [ {name, role, tools, deliverable, time_estimate}, ... ] }
        """
        prompt = (
            "You are an expert task decomposer.\n"
            "Below is a single task from our campaign blueprint. "
            "Decompose this task into 3–6 ordered subtasks. "
            "Return ONLY a JSON array named `subtasks` where each element has keys:\n"
            "  • name: string\n"
            "  • role: string\n"
            "  • tools: array of strings\n"
            "  • deliverable: string\n"
            "  • time_estimate: string\n\n"
            "Task:\n"
            f"{json.dumps(payload, indent=2)}\n\n"
        )

        messages = [
            {"role": "system",  "content": "You are a helpful micro-decomp assistant."},
            {"role": "user",    "content": prompt}
        ]

        resp = chat_completion(messages, model="gpt-4o", temperature=0.3)
        content = resp.choices[0].message.content.strip()
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        # The LLM might return either an object {"subtasks":[...]} or just [...]
        data = json.loads(content)
        if isinstance(data, list):
            return {"subtasks": data}
        return {"subtasks": data.get("subtasks", [])}


# Self-test
if __name__ == "__main__":
    agent = MicroDecompAgent()
    sample = {
        "name": "Develop creative brief",
        "role": "Creative Director",
        "tools": ["Google Docs", "Brand Guidelines"],
        "deliverable": "Creative brief document",
        "time_estimate": "2 days"
    }
    print(json.dumps(agent.run(sample), indent=2))
