# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

"""
File: backend/agents/openai/codegen_agent.py

Need for this file (5th-grader explanation):
“Imagine you have a tiny step like ‘Generate insertion order.’ The CodeGen Agent
writes a little Python function stub—complete with a docstring explaining who does
it, what tools they need, what they make, and how long it takes—so our robot helpers
know exactly what code to run next!”
"""

import re
import json
from typing import Any, Dict
from ..base import Agent
from ...utils.openai_client import chat_completion
import logging
logger = logging.getLogger("blueprint_maker.codegen")
class CodeGenAgent(Agent):
    """
    Code Generation Agent:
    Takes a leaf task (with name, role, tools, deliverable, time_estimate)
    and generates a Python function stub.
    """

    def run(self, payload: Dict[str, Any]) -> Dict[str, str]:
        logger.debug("CodeGenAgent.run: payload: %s", payload)
        """
        :param payload: {
            "name": str,
            "role": str,
            "tools": List[str],
            "deliverable": str,
            "time_estimate": str
        }
        :return: {"code": "<python function stub>"}
        """
        prompt = (
            "You are a senior Python engineer. Below is a task specification:\n\n"
            f"{json.dumps(payload, indent=2)}\n\n"
            "Generate a Python function stub that implements this task. "
            "The function name should be a snake_case version of the task name, "
            "the docstring should describe the role, tools, deliverable, and time estimate, "
            "and the function should accept parameters corresponding to these fields. "
            "Include a placeholder `pass` in the function body. "
            "Return only the code block, with no extra explanation."
        )
        messages = [
            {"role": "system", "content": "You are a senior Python engineer."},
            {"role": "user",   "content": prompt}
        ]

        # Call the LLM
        response = chat_completion(messages, model="gpt-4o", temperature=0)
        code = response.choices[0].message.content.strip()

        # Strip Markdown fences if present
        code = re.sub(r"^```(?:python)?\s*", "", code)
        code = re.sub(r"\s*```$", "", code)
        logger.debug("CodeGenAgent.run: code: %s", code)
        return {"code": code}

# Self-test (optional)
if __name__ == "__main__":
    agent = CodeGenAgent()
    sample = {
        "name": "Generate insertion order",
        "role": "Media Buyer",
        "tools": ["DSP API", "Excel"],
        "deliverable": "Filled insertion order JSON",
        "time_estimate": "2 hours"
    }
    result = agent.run(sample)
    print(result["code"])
