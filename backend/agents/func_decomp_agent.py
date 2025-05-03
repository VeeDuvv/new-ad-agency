# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Vamsi Duvvuri

# File: backend/agents/func_decomp_agent.py

"""
Need for this file (5th-grader explanation):
Imagine you have a big toy set called 'make ads.' This Blueprint Maker listens to
the name of the toy set and writes down every little step you need to complete it—
including who does it (role), what tools they use, what they deliver, and how long
it takes. That way, all our robot helpers know exactly what to do, step by step,
just like reading a detailed recipe.
"""

from dotenv import load_dotenv
load_dotenv()  # auto-load OPENAI_API_KEY

import re
import json
from ..utils.openai_client import chat_completion

class FuncArchAgent:
    """
    Function Decomposition Agent:
    Break a high-level agency function into processes, activities, and tasks
    with detailed fields (name, role, tools, deliverable, time_estimate).
    """

    def decompose(self, function_name: str, context: str = "AI-native ad agency"):
        """
        :param function_name: e.g. "Media Buying & Execution"
        :param context: business context for tailoring the steps
        :return: dict with key 'processes', each an array of:
                 {
                   name: str,
                   activities: [
                       {
                         name: str,
                         tasks: [
                             {
                               name: str,
                               role: str,
                               tools: [str, …],
                               deliverable: str,
                               time_estimate: str
                             }
                         ]
                       }
                   ]
                 }
        """
        prompt = (
            f"Decompose the function '{function_name}' in the context of a {context}. "
            "Return ONLY valid JSON with a top-level key 'processes', which is an array of objects each containing:\n"
            "  - name: string (process name)\n"
            "  - activities: array of objects {\n"
            "        name: string (activity name),\n"
            "        tasks: array of objects {\n"
            "            name: string (task name),\n"
            "            role: string (role responsible),\n"
            "            tools: array of strings (tools/software used),\n"
            "            deliverable: string (what is produced),\n"
            "            time_estimate: string (how long it takes)\n"
            "        }\n"
            "    }\n"
            "Do not include any extra text—just the JSON."
        )

        messages = [
            {"role": "system", "content": "You are an expert ad-agency process architect."},
            {"role": "user",   "content": prompt},
        ]

        resp = chat_completion(messages, model="gpt-4o", temperature=0)
        content = resp.choices[0].message.content.strip()
        # Strip Markdown code fences if present
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON:\n{e}\n\nRaw content:\n{content}")

# Self-test (run `python -m backend.agents.func_decomp_agent "Media Buying & Execution"`)
if __name__ == "__main__":
    agent = FuncArchAgent()
    import sys
    fn = sys.argv[1] if len(sys.argv) > 1 else "Media Buying & Execution"
    result = agent.decompose(fn)
    print(json.dumps(result, indent=2))
